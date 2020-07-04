import core as cr
import maya.cmds as mc
import transform as tr
from rigLib.utils import controller as ct

from rigging.tools import AD_utils as au

reload(cr)
reload(tr)
reload(ct)
reload(au)

class CreateRibbon:
    def __init__(self,
                 createCtrl =False,
                 tip = '',
                 base ='',
                 ctrlTip =ct.SQUARE,
                 ctrlMid = ct.SQUARE,
                 ctrlBase =ct.SQUARE,
                 ctrlDetails = ct.CIRCLEPLUS,
                 prefix='prefix',
                 width=5.0,
                 numJoints=5):

        """
        :param createCtrl: bool, parameters for creating the control module and tip
        :param tip: str, transform or joint as the tip of ribbon
        :param base: str, transform or joint as the module of ribbon
        :param prefix: str, prefix name for ribbon
        :param width: float, width of surface for ribbon
        :param numJoints: int, number of joint as well as the control of ribbon part
        """

        self.pos       = (0,0,0)
        self.upPoint   = (width / 2.0 * -1)
        self.downPoint = (width / 2.0)

        # Create the main groups
        self.grpAllRibbon  = mc.group(empty=True, name=(prefix + 'AllRibbon_grp'))

        self.grpTransform        = mc.group(empty=True, name=(prefix + 'Transform_grp'))
        cr.decompose_matrix(base, self.grpTransform)
        self.grpOffsetTransform  = mc.duplicate(self.grpTransform, name=(prefix + 'TransformOffset_grp'))
        self.grpCtrl             = mc.duplicate(self.grpTransform, name=(prefix + 'Ctrl_grp'))
        self.grpJntCluster       = mc.duplicate(self.grpTransform, name=(prefix + 'JntCluster_grp'))

        self.grpNoTransform = mc.duplicate(self.grpAllRibbon, name=(prefix + 'NoTransform_grp'))
        self.grpUtils       = mc.duplicate(self.grpAllRibbon, name=(prefix + 'Utils_grp'))
        self.grpSurface     = mc.duplicate(self.grpAllRibbon, name=(prefix + 'Surface_grp'))
        self.grpDeformers   = mc.duplicate(self.grpAllRibbon, name=(prefix + 'Deformer_grp'))
        self.grpMisc        = mc.duplicate(self.grpAllRibbon, name=(prefix + 'Misc_grp'))
        self.grpSurfaces    = mc.duplicate(self.grpAllRibbon, name=(prefix + 'Surfaces_grp'))
        self.grpFollMain    = mc.duplicate(self.grpAllRibbon, name=(prefix + 'FolliclesSkin_grp'))
        self.grpFollVolume  = mc.duplicate(self.grpAllRibbon, name=(prefix + 'FolliclesVolume_grp'))

        # Parenting the groups
        mc.parent(self.grpUtils, self.grpFollMain, self.grpFollVolume, self.grpNoTransform)
        mc.parent(self.grpSurfaces, self.grpDeformers, self.grpJntCluster, self.grpMisc, self.grpUtils)
        mc.parent(self.grpSurface, self.grpCtrl ,self.grpOffsetTransform )
        mc.parent(self.grpOffsetTransform,self.grpTransform )
        mc.parent(self.grpNoTransform, self.grpTransform, self.grpAllRibbon)

        # Create a NURBS-plane to use as a module
        tmpPlane = mc.nurbsPlane(axis=(0,1,0), width=width, lengthRatio=(1.0 / width),
                                 u=numJoints, v=1, degree=3, ch=0)[0]

        # Create the NURBS-planes to use in the setup
        geoPlane        = mc.duplicate(tmpPlane, name=(prefix + '_geo'))
        geoPlaneTwist   = mc.duplicate(tmpPlane, name=(prefix + 'TwistDef_geo'))
        geoPlaneSine    = mc.duplicate(tmpPlane, name=(prefix + 'SineDef_geo'))
        geoPlaneWire    = mc.duplicate(tmpPlane, name=(prefix + 'WireDef_geo'))
        geoPlaneVolume  = mc.duplicate(tmpPlane, name=(prefix + 'Volume_geo'))

        # Offset the volume-plane
        mc.setAttr((geoPlaneVolume[0] + '.translateZ'), -0.5)

        # Delete the module surface
        mc.delete(tmpPlane)

       # Create the controllers
        ctrlUp   = ct.Control(prefix =prefix + 'Up', groups_ctrl=['Zro', 'Offset', 'SDK'], shape=ctrlTip)
        ctrlMid  = ct.Control(prefix =prefix + 'Mid', groups_ctrl=['Zro', 'Offset', 'SDK'], ctrl_color='blue', ctrl_size=1.3, shape=ctrlMid)
        ctrlDown = ct.Control(prefix =prefix + 'Down', groups_ctrl=['Zro', 'Offset', 'SDK'], shape=ctrlBase)

        # PointConstraint the midCtrl between the top/end
        mc.pointConstraint(ctrlDown.control, ctrlUp.control, ctrlMid.parent_control[-1])

        # adjusting controller vector position
        self.ctrlUpPos   = cr.decompose_matrix(base, ctrlUp.parent_control[0])
        self.ctrlMidPos  = cr.decompose_matrix(base, ctrlMid.parent_control[0])
        self.ctrlDownPos = cr.decompose_matrix(base, ctrlDown.parent_control[0])

        # position
        self.ctrlUpPos   = mc.setAttr((ctrlUp.parent_control[0] + '.translate'), self.upPoint, self.pos[1], self.pos[2])
        self.ctrlDownPos = mc.setAttr((ctrlDown.parent_control[0] + '.translate'), self.downPoint, self.pos[1], self.pos[2])

        # Add attributes: Twist/Roll attributes
        self.addAttribute(objects=[ctrlDown.control, ctrlMid.control, ctrlUp.control],
                          longName=['twistSep'], niceName=[' '], at="enum", en='Twist', cb=True)

        self.addAttribute(objects=[ctrlDown.control, ctrlUp.control], longName=['twist'], at="float", k=True)
        self.addAttribute(objects=[ctrlDown.control, ctrlUp.control], longName=['twistOffset'], at="float", k=True)
        self.addAttribute(objects=[ctrlDown.control, ctrlUp.control], longName=['affectToMid'], at="float", min=0, max=10, dv=10, k=True)
        self.addAttribute(objects=[ctrlMid.control], longName=['roll'], at="float", k=True)
        self.addAttribute(objects=[ctrlMid.control], longName=['rollOffset'], at="float", k=True)

        # Add attributes: Volume attributes
        self.addAttribute(objects=[ctrlMid.control], longName=['volumeSep'], niceName=[' '], at="enum",
                          en='Volume', cb=True)

        self.addAttribute(objects=[ctrlMid.control], longName=['volume'], at="float", min=-1, max=1, k=True)
        self.addAttribute(objects=[ctrlMid.control], longName=['volumeMultiplier'], at="float", min=1, dv=3, k=True)
        self.addAttribute(objects=[ctrlMid.control], longName=['startDropoff'], at="float", min=0, max=1, dv=1, k=True)
        self.addAttribute(objects=[ctrlMid.control], longName=['endDropoff'], at="float", min=0, max=1, dv=1, k=True)
        self.addAttribute(objects=[ctrlMid.control], longName=['volumeScale'], at="float", min=self.upPoint * 0.9, max=self.downPoint * 2, k=True)
        self.addAttribute(objects=[ctrlMid.control], longName=['volumePosition'], min=self.upPoint, max=self.downPoint, at="float", k=True)

        # Add attributes: Sine attributes
        self.addAttribute(objects=[ctrlMid.control], longName=['sineSep'], niceName=[' '], attributeType='enum', en="Sine:", cb=True)

        self.addAttribute(objects=[ctrlMid.control], longName=['amplitude'], attributeType="float", k=True)
        self.addAttribute(objects=[ctrlMid.control], longName=['offset'], attributeType="float", k=True)
        self.addAttribute(objects=[ctrlMid.control], longName=['twist'], attributeType="float", k=True)
        self.addAttribute(objects=[ctrlMid.control], longName=['sineLength'], min=0.1, dv=2, attributeType="float", k=True)

        # Add attributes: Extra attributes
        self.addAttribute(objects=[ctrlMid.control], longName=['extraSep'], niceName=[' '], at="enum", en='Extra', cb=True)
        self.addAttribute(objects=[ctrlMid.control], longName=['showExtraCtrl'], at="long",  min=0, max=1, dv=0, cb=True)

        # Create deformers: Twist deformer, Sine deformer, Squash deformer
        self.twistDef   = self.nonlinearDeformer(objects=[geoPlaneTwist[0]], defType='twist',
                                                 name=au.prefix_name(geoPlaneTwist[0]), lowBound=-1,
                                                 highBound=1, rotate=(0, 0, 90))

        self.sineDef    = self.nonlinearDeformer(objects=[geoPlaneSine[0]], defType='sine',
                                                 name=au.prefix_name(geoPlaneSine[0]), lowBound=-1,
                                                 highBound=1, rotate=(0, 0, 90))

        self.squashDef  = self.nonlinearDeformer(objects=[geoPlaneVolume[0]], defType='squash',
                                                 name=au.prefix_name(geoPlaneVolume[0]), lowBound=-1,
                                                 highBound=1, rotate=(0, 0, 90))
        mc.setAttr((self.sineDef[0] + '.dropoff'), 1)

        # Create deformers: Wire deformer
        deformCrv  = mc.curve(p=[(self.downPoint, 0, 0), (0, 0, 0), (self.upPoint, 0, 0)], degree=2)
        deformCrv  = mc.rename(deformCrv, (prefix + 'Wire_crv'))
        wireDef    = mc.wire(geoPlaneWire, dds=(0, 15), wire=deformCrv)
        wireDef[0] = mc.rename(wireDef[0], (au.prefix_name(geoPlaneWire[0]) + '_wireNode'))

        # Create Joint reference
        jointCreate = mc.createNode('joint')
        cr.decompose_matrix(base, jointCreate)
        mc.makeIdentity(jointCreate, apply=True, r=1, n=1)

        # Duplicate joint from reference for skinning to the wire curve
        self.jointUp   = mc.duplicate(jointCreate, n=prefix + 'Up_jnt')
        self.jointMid  = mc.duplicate(jointCreate, n=prefix + 'Mid_jnt')
        self.jointDown = mc.duplicate(jointCreate, n=prefix + 'Down_jnt')

        # set the position for joints
        mc.setAttr((self.jointUp[0] + '.translate'),self.upPoint, self.pos[1], self.pos[2])
        mc.setAttr((self.jointMid[0] + '.translate'),self.pos[0], self.pos[1], self.pos[2])
        mc.setAttr((self.jointDown[0] + '.translate'), self.downPoint, self.pos[1], self.pos[2])

        # Create Group for joints
        self.jointUpParent   = tr.create_parent_transform(['Zro', 'Offset'], self.jointUp[0], self.jointUp[0])
        self.jointMidParent  = tr.create_parent_transform(['Zro', 'Offset'], self.jointMid[0], self.jointMid[0])
        self.jointDownParent = tr.create_parent_transform(['Zro', 'Offset'], self.jointDown[0], self.jointDown[0])

        # Delete the joint reference
        mc.delete(jointCreate)

        mc.pointConstraint(self.jointUp, self.jointDown, self.jointMidParent[-1])

        # Skining joints to curve
        mc.skinCluster([self.jointUp[0], self.jointMid[0], self.jointDown[0]], deformCrv,
                       n='wireSkinCluster', tsb=True, bm=0, sm=0, nw=1, mi=1)

        posUpPma = mc.shadingNode('plusMinusAverage', asUtility=1, name=(prefix + 'DownCtrl_pma'))
        mc.connectAttr((ctrlUp.control + '.translate'), (posUpPma + '.input3D[0]'))
        mc.connectAttr((ctrlUp.parent_control[1] + '.translate'), (posUpPma + '.input3D[1]'))
        mc.connectAttr((ctrlUp.parent_control[2] + '.translate'), (posUpPma + '.input3D[2]'))
        mc.connectAttr((posUpPma + '.output3D'), (self.jointUp[0] + '.translate'))

        mc.connectAttr((ctrlMid.control + '.translate'), (self.jointMid[0] + '.translate'))

        posDownPma = mc.shadingNode('plusMinusAverage', asUtility=1, name=(prefix + 'UpCtrl_pma'))
        mc.connectAttr((ctrlDown.control + '.translate'), (posDownPma + '.input3D[0]'))
        mc.connectAttr((ctrlDown.parent_control[1] + '.translate'), (posDownPma + '.input3D[1]'))
        mc.connectAttr((ctrlDown.parent_control[2] + '.translate'), (posDownPma + '.input3D[2]'))
        mc.connectAttr((posDownPma + '.output3D'), (self.jointDown[0] + '.translate'))

        # Create deformers: Blendshape
        blndDef = mc.blendShape(geoPlaneWire[0], geoPlaneTwist[0], geoPlaneSine[0],
                                geoPlane[0], name=(prefix + '_bsn'), weight=[(0, 1), (1, 1), (2, 1)])

        # Twist deformer: Sum the twist and the roll
        sumTopPma = mc.shadingNode('plusMinusAverage', asUtility=1, name=(prefix + 'TwistUpSum_pma'))
        mc.connectAttr((ctrlDown.control + '.twist'), (sumTopPma + '.input1D[0]'))
        mc.connectAttr((ctrlDown.control + '.twistOffset'), (sumTopPma + '.input1D[1]'))
        mc.connectAttr((ctrlMid.control + '.roll'), (sumTopPma + '.input1D[2]'))
        mc.connectAttr((ctrlMid.control + '.rollOffset'), (sumTopPma + '.input1D[3]'))
        mc.connectAttr((sumTopPma + '.output1D'), (self.twistDef[0] + '.startAngle'))

        sumEndPma = mc.shadingNode('plusMinusAverage', asUtility=1, name=(prefix + 'TwistDownSum_pma'))
        mc.connectAttr((ctrlUp.control + '.twist'), (sumEndPma + '.input1D[0]'))
        mc.connectAttr((ctrlUp.control + '.twistOffset'), (sumEndPma + '.input1D[1]'))
        mc.connectAttr((ctrlMid.control + '.roll'), (sumEndPma + '.input1D[2]'))
        mc.connectAttr((ctrlMid.control + '.rollOffset'), (sumEndPma + '.input1D[3]'))
        mc.connectAttr((sumEndPma + '.output1D'), (self.twistDef[0] + '.endAngle'))

        # Twist deformer: Set up the affect of the deformer
        topAffMdl = mc.shadingNode('multDoubleLinear', asUtility=1, name=(prefix + 'TwistUpAffect_mdl'))
        mc.setAttr((topAffMdl + '.input1'), -0.1)
        mc.connectAttr((ctrlDown.control + '.affectToMid'), (topAffMdl + '.input2'))
        mc.connectAttr((topAffMdl + '.output'), (self.twistDef[0] + '.lowBound'))

        endAffMdl = mc.shadingNode('multDoubleLinear', asUtility=1, name=(prefix + 'TwistDownAffect_mdl'))
        mc.setAttr((endAffMdl + '.input1'), 0.1)
        mc.connectAttr((ctrlUp.control + '.affectToMid'), (endAffMdl + '.input2'))
        mc.connectAttr((endAffMdl + '.output'), (self.twistDef[0] + '.highBound'))

        # Squash deformer: Set up the connections for the volume control
        volumeRevfMdl = mc.shadingNode('multDoubleLinear', asUtility=1, name=(prefix + 'VolumeReverse_mdl'))
        mc.setAttr((volumeRevfMdl + '.input1'), -1)
        mc.connectAttr((ctrlMid.control + '.volume'), (volumeRevfMdl + '.input2'))
        mc.connectAttr((volumeRevfMdl + '.output'), (self.squashDef[0] + '.factor'))
        mc.connectAttr((ctrlMid.control + '.startDropoff'), (self.squashDef[0] + '.startSmoothness'))
        mc.connectAttr((ctrlMid.control + '.endDropoff'), (self.squashDef[0] + '.endSmoothness'))
        mc.connectAttr((ctrlMid.control + '.volumePosition'), (self.squashDef[1] + '.translateX'))

        # Squash deformer: Set up the volume scaling
        sumScalePma = mc.shadingNode('plusMinusAverage', asUtility=1, name=(prefix + 'VolumeScaleSum_pma'))
        mc.setAttr((sumScalePma + '.input1D[0]'), self.downPoint)
        mc.connectAttr((ctrlMid.control + '.volumeScale'), (sumScalePma + '.input1D[1]'))
        mc.connectAttr((sumScalePma + '.output1D'), (self.squashDef[1] + '.scaleY'))

        # Sine deformer: Set up the connections for the sine
        mc.connectAttr((ctrlMid.control + '.amplitude'), (self.sineDef[0] + '.amplitude'))
        mc.connectAttr((ctrlMid.control + '.offset'), (self.sineDef[0] + '.offset'))
        mc.connectAttr((ctrlMid.control + '.twist'), (self.sineDef[1] + '.rotateY'))
        mc.connectAttr((ctrlMid.control + '.sineLength'), (self.sineDef[0] + '.wavelength'))

        # Cleanup: Hierarchy
        mc.parent(geoPlaneWire[0], geoPlaneTwist[0], geoPlaneSine[0], geoPlaneVolume[0], self.grpSurfaces)
        mc.parent(self.twistDef[1], self.sineDef[1], self.squashDef[1], self.grpDeformers)
        mc.parent(self.jointUpParent[0], self.jointMidParent[0], self.jointDownParent[0], self.grpJntCluster)
        mc.parent(ctrlDown.parent_control[0], ctrlMid.parent_control[0], ctrlUp.parent_control[0], self.grpCtrl)
        mc.parent(geoPlane[0], self.grpSurface)
        mc.parent(deformCrv, (mc.listConnections(wireDef[0] + '.baseWire[0]')[0]), self.grpMisc)

        # Cleanup: Visibility
        mc.hide(self.grpUtils, self.grpFollVolume, self.grpSurface)
        for x in mc.listConnections(ctrlMid.parent_control[-1]):
            mc.setAttr((x + '.isHistoricallyInteresting'), 0)
            for y in mc.listConnections(x):
                mc.setAttr((y + '.isHistoricallyInteresting'), 0)

        # Match position with the module and tip joint
        mc.delete(mc.parentConstraint(base, tip, self.grpTransform))
        mc.parentConstraint(base, ctrlUp.parent_control[1])
        mc.parentConstraint(tip, ctrlDown.parent_control[1])

        # Aiming the mid control to the module
        mc.aimConstraint(ctrlUp.control, ctrlMid.parent_control[-1], mo=1, wut='objectrotation', wuo=ctrlUp.control)
        mc.aimConstraint(self.jointUp, self.jointMidParent[-1], mo=1, wut='objectrotation',wuo=self.jointUp[0])

        # Scaling the follicle with decompose matrix
        decomposeMtxScale = mc.createNode('decomposeMatrix', n=(prefix + 'scaleFol_dmt'))
        mc.connectAttr(self.grpOffsetTransform[0]+'.worldMatrix[0]', decomposeMtxScale+'.inputMatrix')

        # Create follicles: The main-surface and the volume-surface
        for x in range(0, numJoints):
            # Declare a variable for the current index
            num = str('%02d' % (x + 1))
            # Get the normalized position of where to place the current follicle
            uVal = ((0.5 / numJoints) * (x + 1) * 2) - ((0.5 / (numJoints * 2)) * 2)

            # Create a follicle for the bind-plane and the volume-plane
            follicleS = self.createFollicle(prefix= (prefix + num), suffix='fol',
                                            connectFol=['rotateConn','transConn'],
                                            inputSurface=mc.listRelatives(geoPlane[0], type="shape"),
                                            uVal=uVal)

            follicleV = self.createFollicle(prefix= (prefix + num ), suffix ='volumeFol',
                                            connectFol=['rotateConn','transConn'],
                                            inputSurface=mc.listRelatives(geoPlaneVolume[0], type="shape"),
                                            uVal=uVal, vVal=0)

            mc.setAttr(follicleS[1]+'.visibility', 0)
            mc.parent(follicleS[0], self.grpFollMain)
            mc.parent(follicleV[0], self.grpFollVolume)

            follicleGrpOffset = mc.group(empty=True, name=(prefix + 'OffsetRibbon_grp'))
            mc.delete(mc.parentConstraint(follicleS[0], follicleGrpOffset))

            # Create offset group follicle
            follicleGrpOffset = mc.parent(follicleGrpOffset, follicleS[0])

            # Create a joint, controller and a group for the current skin-follicle
            mc.select(clear=True)

            # Create joint for follicle
            follicleJoint = mc.joint(name=(prefix + num + '_jnt'), radius=0.2)

            # Create control for joint in follicle
            follicleCtrl = ct.Control(prefix =prefix+num, groups_ctrl=['Zro', 'Offset'], ctrl_color='lightPink', shape=ctrlDetails)

            # Parent joint to controller
            mc.parent(follicleJoint, follicleCtrl.control)

            # Positioning skin-follicle control
            mc.delete(mc.parentConstraint(ctrlMid.control, follicleCtrl.parent_control[0]))
            mc.delete(mc.pointConstraint(follicleGrpOffset, follicleCtrl.parent_control[0]))

            # Parent controller to group offset follicle
            mc.parent(follicleCtrl.parent_control[0], follicleGrpOffset)

            # connect the visibility-switch for the controller
            mc.connectAttr((ctrlMid.control + '.showExtraCtrl'),
                           (follicleGrpOffset[0]+ '.visibility'))

            # Make the connections for the volume
            multMpd = mc.shadingNode('multiplyDivide', asUtility=1, name=(prefix + num + 'Multiplier_mdn'))
            mc.connectAttr((ctrlMid.control + '.volumeMultiplier'), (multMpd + '.input1Z'))
            mc.connectAttr((follicleV[0] + '.translate'), (multMpd + '.input2'))

            sumPma = mc.shadingNode('plusMinusAverage', asUtility=1, name=(prefix + num + 'VolumeSum_pma'))
            mc.connectAttr((multMpd + '.outputZ'), (sumPma + '.input1D[0]'))
            mc.setAttr((sumPma + '.input1D[1]'), 1)
            mc.connectAttr((sumPma + '.output1D'), (follicleGrpOffset[0] + '.scaleY'))
            mc.connectAttr((sumPma + '.output1D'), (follicleGrpOffset[0] + '.scaleZ'))

            # Connect scale decompose matrix to the object follicle
            mc.connectAttr(decomposeMtxScale+'.outputScale', follicleS[0]+'.scale')

        # Creating control the module and tip
        if createCtrl:
            baseCtrl = ct.Control(prefix =base + 'Base', groups_ctrl=['Zro', 'Offset'], ctrl_color='yellow', shape=ct.CUBE)
            mc.delete(mc.parentConstraint(base, baseCtrl.parent_control[0]))
            mc.parent(base, baseCtrl.control)

            tipCtrl = ct.Control(prefix =tip + 'Tip', groups_ctrl=['Zro', 'Offset'], ctrl_color='yellow', shape=ct.CUBE)
            mc.delete(mc.parentConstraint(tip, tipCtrl.parent_control[0]))
            mc.parent(tip, tipCtrl.control)

            mc.parent(baseCtrl.parent_control[0], tipCtrl.parent_control[0], self.grpOffsetTransform)

        # Lock some groups
        au.lock_attr(['t', 'r', 's'], self.grpAllRibbon)
        au.lock_attr(['t', 'r', 's'], self.grpNoTransform[0])
        au.lock_attr(['t', 'r', 's'], self.grpUtils[0])
        au.lock_attr(['t', 'r', 's'], self.grpFollMain[0])
        au.lock_attr(['t', 'r', 's'], self.grpFollVolume[0])
        au.lock_attr(['t', 'r', 's'], self.grpFollVolume[0])
        au.lock_attr(['t', 'r', 's'], self.grpTransform)

        # Clear all selection
        mc.select(cl=1)

    # GENERAL FUNCTION: ADD ATTRIBUTE(S) ON MULTIPLE OBJECTS
    def addAttribute(self, objects=[], longName='', niceName='', separator=False, k=False, cb=False, **kwargs):
        # For each object
        for obj in objects:
            # For each attribute
            for x in range(0, len(longName)):
                # See if a niceName was defined
                attrNice = '' if not niceName else niceName[x]
                # If the attribute does not exists
                if not mc.attributeQuery(longName[x], node=obj, exists=True):
                    # Add the attribute
                    mc.addAttr(obj, longName=longName[x], niceName=attrNice, **kwargs)
                    # If lock was set to True
                    mc.setAttr((obj + '.' + longName[x]), k=k, e=1, cb=cb) if separator else mc.setAttr((obj + '.' + longName[x]), k=k, e=1, cb=cb)


    # GENERAL FUNCTION: CREATE A NONLINEAR DEFORMER
    def nonlinearDeformer(self, objects=[], defType=None, lowBound=-1, highBound=1, translate=None, rotate=None,
                          name='nonLinear'):

        # If something went wrong or the type is not valid, raise exception
        if not objects or defType not in ['bend', 'flare', 'sine', 'squash', 'twist', 'wave']:
            raise Exception, "function: 'nonlinearDeformer' - Make sure you specified a mesh and a valid deformer"

        # Create and rename the deformer
        nonLinDef = mc.nonLinear(objects[0], type=defType, lowBound=lowBound, highBound=highBound)
        nonLinDef[0] = mc.rename(nonLinDef[0], (name + '_' + defType + 'Def'))
        nonLinDef[1] = mc.rename(nonLinDef[1], (name + '_' + defType + 'Handle'))

        # If translate was specified, set the translate
        if translate:
            mc.setAttr((nonLinDef[1] + '.translate'), translate[0], translate[1], translate[2])

        # If rotate was specified, set the rotate
        if rotate:
            mc.setAttr((nonLinDef[1] + '.rotate'), rotate[0], rotate[1], rotate[2])

        # Return the deformer
        return nonLinDef


    # GENERAL FUNCTION: SET PIVOT OF OBJECT(S)
    def setPivot(self, objects=[], rotatePivot=1, scalePivot=1, pivot=(0, 0, 0)):
        # Make sure the input is passed on as a list
        objects = [objects] if isinstance(objects, (str, unicode)) else objects
        # For each object
        for obj in objects:
            # If rotatePivot was set to True, set the rotatePivot
            if rotatePivot:
                mc.xform(obj, worldSpace=True, rotatePivot=pivot)
            # If scalePivot was set to True, set the scalePivot
            if scalePivot:
                mc.xform(obj, worldSpace=True, scalePivot=pivot)


    # GENERAL FUNCTION: CREATE A FOLLICLE AND ATTACH IT TO A SURFACE
    def createFollicle(self, prefix='follicle', suffix='', inputSurface=[], connectFol=[''], scaleGrp='',
                       uVal=0.5, vVal=0.5, hide=0):

        # Create a follicle
        follicleShape = mc.createNode('follicle')

        # Get the transform of the follicle
        follicleTrans = mc.listRelatives(follicleShape, type='transform', p=True)

        # If the inputSurface is of type 'nurbsSurface', connect the surface to the follicle
        if mc.objectType(inputSurface[0]) == 'nurbsSurface':
            mc.connectAttr((inputSurface[0] + '.local'), (follicleShape + '.inputSurface'))

        # If the inputSurface is of type 'mesh', connect the surface to the follicle
        if mc.objectType(inputSurface[0]) == 'mesh':
            mc.connectAttr((inputSurface[0] + '.outMesh'), (follicleShape + '.inputMesh'))

        # Connect the worldMatrix of the surface into the follicleShape
        mc.connectAttr((inputSurface[0] + '.worldMatrix[0]'), (follicleShape + '.inputWorldMatrix'))

        # connecting the shape follicle to transform follicle
        au.dic_connect_follicle(connectFol, follicleShape, follicleTrans[0])

        # Set the uValue and vValue for the current follicle
        mc.setAttr((follicleShape + '.parameterU'), uVal)
        mc.setAttr((follicleShape + '.parameterV'), vVal)

        # If it was set to be hidden, hide the follicle
        if hide:
            mc.setAttr((follicleShape + '.visibility'), 1)

        # If a scale-group was defined and exists
        if scaleGrp and mc.objExists(scaleGrp):
            # Connect the scale-group to the follicle
            mc.connectAttr((scaleGrp + '.scale'), (follicleTrans + '.scale'))

        follicleTrans = mc.rename(follicleTrans, '%s_%s' % (au.prefix_name(prefix), suffix))

        follicleShape = mc.listRelatives(follicleTrans, s=1)[0]

        # Return the follicle and it's shape
        return follicleTrans, follicleShape