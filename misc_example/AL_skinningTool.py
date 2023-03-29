# Copyright (C) Animal Logic Pty Ltd. All rights reserved.
from __future__ import absolute_import
import logging
import random
from AL.rig.jobs.common.libs import OMSel


from AL.maya2 import om2, cmds

from AL.maya2.session import plugs as alm2_plugs
from AL.libs.commandmaya import undoablecommands as mayacommand
from AL.rig.jobs.common.assets import icons

logger = logging.getLogger(__name__)

# JOINT LABEL
class LabelAllJointsCmd(mayacommand.Command):

    uiData = {
        "title": "Label All Joints",
        "tooltip": "Sets the label name and side for all joints in scene (in deform layers) to support precise mirroring",
        "iconPath": icons.TAG,
    }

    @classmethod
    def id(cls):
        return "AL.rig.tools.LabelAllJointsCmd"

    def resolve(self):
        if not self.hasArgumentValue("joints"):
            jointList = om2.MSelectionList()
            for joint in cmds.ls(type="joint", l=True):
                jointList.add(joint)

            self.setArgumentValue("joints", jointList)

    def doIt(self, joints=None):
        """
        @param joints: MSelectionList of the joints
        @return:
        """
        for x in range(joints.length()):
            jntMObj = joints.getDependNode(x)
            jntMFnDep = om2.MFnDependencyNode(jntMObj)
            typePlug = alm2_plugs.findPlug(plugName="type", node=jntMObj)
            typePlug.setInt(18)

            sidePlug = alm2_plugs.findPlug(plugName="side", node=jntMObj)
            if "_L_" in jntMFnDep.name():
                sideSplit = "_L_"
                sidePlug.setInt(1)
            elif "_R_" in jntMFnDep.name():
                sideSplit = "_R_"
                sidePlug.setInt(2)
            elif "_M_" in jntMFnDep.name():
                sideSplit = "_M_"
            else:
                continue

            # Prefix purpose in case component names aren't unique
            pathTo = joints.getDagPath(x).fullPathName()
            if "deform|" not in pathTo:
                continue

            finName = om2.MNamespace.stripNamespaceFromName(jntMFnDep.name())
            jntPurpose = (
                pathTo.partition("deform|")[0].split(":", 1)[1].split("|", 1)[0]
            )

            name = "{}_{}".format(jntPurpose, finName.replace(sideSplit, "_"))

            otherTypePlug = alm2_plugs.findPlug(plugName="otherType", node=jntMObj)
            otherTypePlug.setString(name)

# RANDOM JOINT COLOR
class RandomJointColorsCmd(mayacommand.UndoablePureMayaCmdsCommand):
    """
    Colour the selected joints
    """

    uiData = {
        "title": "Random Colour Joints",
        "subtitle": "Random Colour joints",
        "tooltip": "Select the joints, then run the tool",
        "iconPath": icons.COLOR01,
    }

    randomIndexList = [x for x in range(1, 8)]

    @classmethod
    def id(cls):
        return "AL.rig.tools.RandomJointColorsCmd"

    def resolve(self):
        if not self.hasArgumentValue("jointList"):
            self.setArgumentValue("jointList", cmds.ls(sl=True, type="joint"))

    def doIt(self, jointList=None):
        for jointName in jointList:
            self.setColour(jointName)

    def setColour(self, jointName):
        colourIndex = random.choice(self.randomIndexList)

        cmds.setAttr("{}.useObjectColor".format(jointName), 1)
        cmds.setAttr("{}.objectColor".format(jointName), colourIndex)
        cmds.color(jointName, ud=colourIndex)

# RENAME SKIN CLUSTER

class RenameSkinClustersCmd(mayacommand.UndoablePureMayaCmdsCommand):
    """
    Tool to rename all skinClusters in the scene to their geoName_[constants.SKINCLUSTER_SUFFIX]
    This will also find connected for objectSet, groupParts, and groupId nodes and rename those as well.
    """

    uiData = {
        "title": "Rename SkCls",
        "subtitle": "Rename SkinClusters",
        "menuTitle": "",
        "toolbarTitle": "",
        "tooltip": "Changes names for the skinCluster and respective sets, groupIds etc\nUsage: Just click the tool :)",
        "iconPath": icons.RENAME,
    }
    skinClusters_name = "skinClusters"
    dgMod = None

    @classmethod
    def id(cls):
        return "AL.rig.tools.RenameSkinClustersCmd"

    def resolve(self):
        self.dgMod = om2.MDGModifier()
        scnSkinClusters = cmds.ls(type="skinCluster")
        if not scnSkinClusters:
            logger.warning("No skinClusters in scene. Aborting!")
            return self.cancelExecution()
        if not self.hasArgumentValue(self.skinClusters_name):
            scls = om2.MSelectionList()
            for sk in scnSkinClusters:
                scls.add(sk)
            self.setArgumentValue(self.skinClusters_name, scls)

    def undoIt(self):
        logger.info("Undo rename skinClusters.")
        self.dgMod.undoIt()

    def doIt(self, skinClusters=None):
        for x in range(skinClusters.length()):
            inMeshName = None
            ## Create a base MFnDep node for the mesh
            mFn = om2.MFnDependencyNode(skinClusters.getDependNode(x))

            ## OUTPUTGEOMETRY[0]
            outputGeometryPlug = getMPlugArray_byAttribute(
                mFn, constants.MAYA_PLUGNAME_OUTPUTGEOMETRY, False
            )
            for o in range(outputGeometryPlug.evaluateNumElements()):
                inMeshName = getConnectedNodeName_byPlug(
                    outputGeometryPlug.elementByLogicalIndex(o), False, True
                )

            if not inMeshName:
                continue

            ############################
            ## skinCluster Name
            fixName(self.dgMod, mFn.name(), inMeshName, constants.SKINCLUSTER_SUFFIX)
            ############################
            ## skinCluster Set
            scSetName = getConnectedNodeName_byAttribute(
                mFn, constants.MAYA_PLUGNAME_MESSAGE, False, True
            )
            fixName(self.dgMod, scSetName, inMeshName, "scls_Set")

        self.dgMod.doIt()
        logger.info("All skin clusters renamed successfully!")


def fixName(dgMod, nameToCheck, geoPrefix, suffix):
    """
    @param dgMod: A valid dgModifer instance
    @param nameToCheck: The nodeName to validate
    @param geoPrefix: The meshName the skinCluster and related nodes belongs to
    @param suffix: The suffix for the node you want to clean
    @type dgMod: om2.MDGModifier()
    @type nameToCheck: string
    @type geoPrefix: string
    @type suffix: string
    @return:
    """
    if nameToCheck == None:
        return
    newName = "{}_{}".format(geoPrefix, suffix)
    if not nameToCheck.startswith(geoPrefix) or nameToCheck != newName:
        dgMod.renameNode(getMobject(nameToCheck), newName)


def getMPlugArray_byAttribute(mFn, attributeName, wantNetworkedPlug):
    attr = mFn.attribute(attributeName)
    plug = mFn.findPlug(attr, wantNetworkedPlug)
    if not plug:
        return None
    return plug


## TO DO Push these into the lib as proper functions for re use
def getConnectedNodeName_byAttribute(mFn, attributeName, asDest, asSrc):
    """
    @param mFn: The maya MFnDependencyNode instance
    @param attributeName: The name of the attribute you want to find a plug for
    @param asDest: Destination connections
    @param asSrc: Source connections
    @type mFn: om2.MFnDependencyNode
    @type attributeName: string
    @type asDest: bool
    @type asSrc: bool
    @return:
    """
    attr = mFn.attribute(attributeName)
    plug = mFn.findPlug(attr, False)
    conn = plug.connectedTo(asDest, asSrc)
    if not conn:
        return None
    return om2.MFnDependencyNode(conn[0].node()).name()


def getConnectedNodeName_byPlug(plug, asDest, asSrc):
    """
    @param plug: The maya MPlug instance
    @param asDest: Destination connections
    @param asSrc: Source connections
    @type plug: om2.MPug
    @type asDest: bool
    @type asSrc: bool
    @return:
    """
    conn = plug.connectedTo(asDest, asSrc)
    if not conn:
        return None
    return om2.MFnDependencyNode(conn[0].node()).name()


def getMobject(nodeName):
    """
    Trys to fetch an MObject for a node in scene from it's name
    @param nodeName: Name of the node in scene
    @type nodeName: string
    @return:
    """
    mySel = om2.MSelectionList()
    mySel.add(nodeName)
    return mySel.getDependNode(0)


# TRANSFER WEIGHT
class TransferWeightsHierarchyCmd(mayacommand.UndoablePureMayaCmdsCommand):
    uiData = {
        "title": "Transfer Weights Hrc",
        "subtitle": "Transfer Weights for Source to Target Hierarchy",
        "tooltip": "Transfer Weights for Source to Target Hierarchy",
        "iconPath": icons.COPY01,
    }

    @classmethod
    def id(cls):
        return "AL.rig.tools.TransferWeightsHierarchyCmd"

    def resolve(self):
        if not self.hasArgumentValue("source") or not self.hasArgumentValue(
            "destination"
        ):
            ## Check we have a valid selection
            logger.info("Checking for valid selection...")
            activeSel = OMSel.OMSelection()
            if (
                activeSel.length < 2
                or activeSel.curSel.isEmpty()
                or activeSel.componentSelection
            ):
                logger.error("Select one source mesh, and one destination mesh")
                return self.cancelExecution()
            self.setArgumentValue("source", activeSel.asMObjects()[0])
            self.setArgumentValue("destination", activeSel.asMObjects()[1])

    def doIt(self, source=None, destination=None):
        """
        Transfer the skin from one mesh to another.
        @param source: Valid MObject
        @param destination: Valid MObject
        @return:
        """
        srcCol = tuple(alm2i_nodes.iterChildren(source))
        for item in srcCol:
            if not item.hasFn(om2.MFn.kShape):
                continue
            for target in alm2i_nodes.iterChildren(destination):
                if (
                    om2.MFnDependencyNode(item).name()
                    == om2.MFnDependencyNode(target).name()
                ):
                    srcDag = om2.MDagPath.getAPathTo(item)
                    destDag = om2.MDagPath.getAPathTo(target)
                    cmds.transferMayaWeights(destDag, srcDag)
                    break


class TransferWeightsFromPurposesCmd(mayacommand.UndoablePureMayaCmdsCommand):
    uiData = {
        "title": "Transfer Weights From Purposes",
        "subtitle": "Transfer Weights for input purposes to destination joint",
        "tooltip": "Transfer Weights for input purposes to destination joint",
        "iconPath": icons.PLACEHOLDER,
    }

    husk_argName = "husk"
    dest_argName = "destination"
    skin_argName = "skin"

    @classmethod
    def id(cls):
        return "AL.rig.tools.TransferWeightsFromPurposesCmd"

    def resolve(self):
        if not self.hasArgumentValue(self.husk_argName):
            executor = Executor()
            husk = executor.execute("cmdLib.BREED_BREED_GETACTIVEHUSKCMD")
            self.setArgumentValue(self.husk_argName, husk)

        if not self.hasArgumentValue(self.dest_argName):
            ## Check we have a valid selection
            activeSel = om2.MGlobal.getActiveSelectionList()
            joint = activeSel.getDependNode(0)
            if joint.hasFn(om2.MFn.kJoint):
                self.setArgumentValue(self.dest_argName, joint)
            else:
                logger.error("please select destination joint")
                self.cancelExecution()

        if not self.hasArgumentValue(self.skin_argName):
            ## Check we have a valid selection
            activeSel = om2.MGlobal.getActiveSelectionList()
            skin = activeSel.getDependNode(1)
            if skin.hasFn(om2.MFn.kSkinClusterFilter):
                self.setArgumentValue(self.skin_argName, skin)
            else:
                logger.error("please select skinCluster")
                self.cancelExecution()

    def doIt(self, husk=None, skin=None, destination=None, purposes=("face",)):
        """
        Transfer the skin from all joints found in purposes.
        @param husk: Valid beast husk
        @param destination: Valid MObject
        @param purposes: list of purposes to transfer
        @return:
        """

        if (
            not destination
            or destination.isNull()
            or not destination.hasFn(om2.MFn.kJoint)
        ):
            logger.error("destination joint invalid!")
            return

        if not skin or skin.isNull() or not skin.hasFn(om2.MFn.kSkinClusterFilter):
            logger.error("skinCluster invalid!")
            return

        destDagPath = om2.MDagPath.getAPathTo(destination)
        skinFn = om2.MFnDependencyNode(skin)

        rig = husk.rig()
        jointsToTransfer = list()
        for purpose in rig.purposes():
            if purpose.name() in purposes:
                for component in purpose.components():
                    compFn = public.FunctorNode(component)
                    for mob in compFn.iterContaineredObjects():
                        if mob.hasFn(om2.MFn.kJoint):
                            nodeFn = om2.MFnDependencyNode(mob)
                            # print nodeFn.name()
                            jointsToTransfer.append(nodeFn.name())

        if jointsToTransfer:
            jointString = " ".join(jointsToTransfer)
            # transfer to destination

            cmds.transferMayaJointWeights(
                sk=skinFn.name(), src=jointString, target=destDagPath.fullPathName()
            )
