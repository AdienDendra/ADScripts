# Copyright (C) Animal Logic Pty Ltd. All rights reserved.
from __future__ import absolute_import
from builtins import str
import logging

from AL.maya2 import cmds, om2

from AL.rig.jobs.common import constants
from AL.rig.jobs.common.libs import plugs, OMSel
from AL.maya2.iterators import plugs as alm2i_plugs
from AL.maya2.session import plugs as alm2s_plugs
from AL.beast.core.constants import types as bcc_types
from AL.beast.maya.nodes import factory as bmn_factory
from AL.beast.core.nodes.interface import shapes as bcn_shapes
from AL.breed.ui.commands.maya import entityTreeCmds as bucm_entityTree
from AL.breed.ui import public as bui_public


logger = logging.getLogger(__name__)

EXCLUDED_PLUGNAMES = (
    "defaultsAttributes",
    "msg",
    "layer_control",
    "layer_deform",
    "layer_guide",
)


def copyMultipleShapes(nodeList):
    """
    This function will get the shape of one object and it will apply it to all the other
    @param nodeList: a list object manipulator selection in Breed
    @return: nothing
    """
    # selection sync to the breed
    bucm_entityTree.SelectInBreedCMD().doIt(nodeList)
    manipulatorNodeList = bui_public.Accessor().entityEditor_selection()
    manipulatorSource = manipulatorNodeList.pop(0)

    dagModifier = om2.MDagModifier()

    # get the shape source manipulator
    shapeSource = [
        shpSrc
        for shpSrc in manipulatorSource.iterDescendants()
        if shpSrc.isA(bcc_types.BEAST_NODE_SHAPE_CURVE)
    ]

    for targetManipulator in manipulatorNodeList:
        shapeTarget = [
            shpTgt
            for shpTgt in targetManipulator.iterDescendants()
            if shpTgt.isA(bcc_types.BEAST_NODE_SHAPE_CURVE)
        ]
        # clean up all manipulator nodeList[1:]
        if shapeTarget:
            for shapeTgt in shapeTarget:
                bmn_factory.functorFromNode(shapeTgt).remove()

        # all the shapes on nodeList[0]
        for objectShape in shapeSource:
            # collect the data
            shapePrimitiveData = bcn_shapes.ShapeCurveNode.primitiveData(objectShape)

            colorData = bcn_shapes.ShapeCurveNode.color(objectShape)
            lineWidthData = bcn_shapes.ShapeCurveNode.lineWidth(objectShape)
            shapePrimitiveData["shapeName"] = objectShape.name()

            # deliver data to the target
            if "pt" in shapePrimitiveData.keys() and shapePrimitiveData["pt"] != 0:
                shape = bcn_shapes.ShapeCurveNode.fromPrimitiveType(
                    shapePrimitiveData["shapeName"],
                    shapePrimitiveData["pt"],
                    parent=targetManipulator,
                )

            else:
                shape = bcn_shapes.ShapeCurveNode(
                    shapePrimitiveData["shapeName"], targetManipulator
                )
                shape.primitiveData()["cvs"] = shapePrimitiveData["cvs"]
                shape.primitiveData()["form"] = shapePrimitiveData["form"]
                shape.primitiveData()["degree"] = shapePrimitiveData["degree"]

            shape.setColor(colorData)
            shape.setLineWidth(lineWidthData)

            # create shape to the target
            bmn_factory.functorFromNode(shape).create(dagModifier)


def copyShape(nodeList, deleteOthers=True, renameAsOld=True, shapePosition=0):
    """
    This function will get the shape of one object and it will apply it to all the other
    @param nodeList: a list of strings with the name of the transforms
    @param deleteOthers: boolean, if True it will delete any other shape of the dst node
    @param renameAsOld: boolean, if True it will rename the new shape as the old one
    @param shapePosition: integer, determinate the position of the shape of reference
    @return: nothing
    """
    shapeObj = nodeList.pop(shapePosition)
    shapeObjShape = cmds.listRelatives(shapeObj, shapes=True, f=True)
    shapeObjShapeLineWidthVal = cmds.getAttr(
        "{}.{}".format(shapeObjShape[0], "lineWidth")
    )

    # TODO REMOVE THIS RETURN! SHOULD BE DONE IN THE RESOLVE!
    if not cmds.listRelatives(shapeObj, shapes=True):
        logger.error("select first a shape")
        return

    for targetObj in nodeList:
        visibilitySource = False
        colorSource = False
        if deleteOthers:
            oldShapesNames = cmds.listRelatives(targetObj, shapes=True, f=True)
            if oldShapesNames:
                visibilitySource = cmds.connectionInfo(
                    "{}.visibility".format(oldShapesNames[0]),
                    sourceFromDestination=True,
                )
                colorSource = cmds.connectionInfo(
                    "{}.overrideColorRGB".format(oldShapesNames[0]),
                    sourceFromDestination=True,
                )
                cmds.delete(oldShapesNames)
                oldShapesNames = oldShapesNames[0].split("|")[-1]

        newObject = cmds.duplicate(shapeObj, returnRootsOnly=True)
        newObjectShape = cmds.listRelatives(newObject, shapes=True, f=True)

        # Set lineWidth on new crv to match shapeObj
        cmds.setAttr(
            "{}.{}".format(newObjectShape[0], "lineWidth"), shapeObjShapeLineWidthVal
        )

        if deleteOthers and visibilitySource:
            cmds.connectAttr(visibilitySource, newObjectShape[0] + ".visibility")

        if deleteOthers and colorSource:
            cmds.connectAttr(colorSource, newObjectShape[0] + ".overrideColorRGB")

        if deleteOthers and renameAsOld and oldShapesNames:
            newNameShapeName = oldShapesNames
        else:
            newNameShapeName = targetObj.split("|")[-1] + "Shape"

        newObjectShape = cmds.rename(newObjectShape[0], newNameShapeName)
        cmds.parent(newObjectShape, targetObj, shape=True, r=True)
        cmds.delete(newObject)

        oldContainer = cmds.container(query=True, findContainer=targetObj)
        if oldContainer is not None:
            cmds.container(
                oldContainer,
                edit=True,
                force=True,
                includeShapes=True,
                includeTransform=True,
                addNode=[newObjectShape],
            )
