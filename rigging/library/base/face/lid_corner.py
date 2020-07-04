import re
from __builtin__ import reload
from string import digits

import maya.cmds as mc

from rigging.library.utils import controller as ct
from rigging.tools import AD_utils as au

reload (ct)
reload (au)

class Build:
    def __init__(self,
                 upLid01, lowLid01,
                 upLid05, lowLid05,
                 upLidjointBind01OffsetGrp,
                 lowLidjointBind01OffsetGrp,
                 upLidjointBind05OffsetGrp,
                 lowLidjointBind05OffsetGrp,
                 scale,
                 sideRGT,
                 sideLFT,
                 upLidControllerBindGrpZro01,
                 lowLidControllerBindGrpZro01,
                 upLidControllerBindGrpZro05,
                 lowLidControllerBindGrpZro05,
                 prefixNameIn,
                 prefixNameOut,
                 side,
                 ctrlShape,
                 ctrlColor,
                 suffixController,
                 lidOut=False):

        # ==================================================================================================================
        #                                                  CORNER CONTROLLER
        # ==================================================================================================================
        # controller in corner
        lidCornerCtrlIn = self.cornerCtrl(matchPosOne=upLid01,
                                          matchPosTwo=lowLid01,
                                          prefix=prefixNameIn,
                                          scale=scale,
                                          side=side,
                                          ctrlShape=ctrlShape,
                                          ctrlColor=ctrlColor,
                                          addAttr=lidOut,
                                          suffixController=suffixController)

        # controller in corner
        lidCornerCtrlOut = self.cornerCtrl(matchPosOne=upLid05,
                                           matchPosTwo=lowLid05,
                                           prefix=prefixNameOut,
                                           scale=scale,
                                           side=side,
                                           ctrlShape=ctrlShape,
                                           ctrlColor=ctrlColor,
                                           addAttr=lidOut,
                                           suffixController=suffixController)

        self.inParentGrpZro = lidCornerCtrlIn[1]
        self.outParentGrpZro = lidCornerCtrlOut[1]
        self.inCtrl = lidCornerCtrlIn[0]
        self.outCtrl = lidCornerCtrlOut[0]

        pos = mc.xform(lidCornerCtrlOut[0], ws=1, q=1, t=1)[0]
        if pos > 0:
            # parent constraint corner grp bind jnt
            au.connectAttrTransRot(lidCornerCtrlIn[0], upLidjointBind01OffsetGrp)
            au.connectAttrTransRot(lidCornerCtrlIn[0], lowLidjointBind01OffsetGrp)
            au.connectAttrTransRot(lidCornerCtrlOut[0], upLidjointBind05OffsetGrp)
            au.connectAttrTransRot(lidCornerCtrlOut[0], lowLidjointBind05OffsetGrp)
        else:
            self.cornerReverseNode(sideRGT, sideLFT, lidCornerCtrl=lidCornerCtrlOut[0], side=side,
                                   lidCornerName=prefixNameOut,
                                   targetUp=upLidjointBind05OffsetGrp, targetLow=lowLidjointBind05OffsetGrp)

            self.cornerReverseNode(sideRGT, sideLFT, lidCornerCtrl=lidCornerCtrlIn[0], side=side,
                                   lidCornerName=prefixNameIn,
                                   targetUp=upLidjointBind01OffsetGrp, targetLow=lowLidjointBind01OffsetGrp)

        # SHOW AND HIDE CONTROLLER CORNER
        if lidOut:
            # ADD ATTRIBUTE FOR LID OUT CONTROLLER
            mc.connectAttr(lidCornerCtrlIn[0]+'.%s' % lidCornerCtrlIn[3], upLidControllerBindGrpZro01+'.visibility')
            mc.connectAttr(lidCornerCtrlIn[0]+'.%s' % lidCornerCtrlIn[3], lowLidControllerBindGrpZro01+'.visibility')
            mc.connectAttr(lidCornerCtrlOut[0]+'.%s' % lidCornerCtrlOut[3], upLidControllerBindGrpZro05+'.visibility')
            mc.connectAttr(lidCornerCtrlOut[0]+'.%s' % lidCornerCtrlOut[3], lowLidControllerBindGrpZro05+'.visibility')

        # OFFSET GRP CONTROLLER
        self.lidCornerCtrlInOffset = lidCornerCtrlIn[2]
        self.lidCornerCtrlOutOffset = lidCornerCtrlOut[2]
        # ==================================================================================================================
        #                                              PARENT TO GROUP
        # ==================================================================================================================
        mc.parent(upLidControllerBindGrpZro01, lidCornerCtrlIn[0])
        mc.parent(lowLidControllerBindGrpZro01, lidCornerCtrlIn[0])
        mc.parent(upLidControllerBindGrpZro05, lidCornerCtrlOut[0])
        mc.parent(lowLidControllerBindGrpZro05, lidCornerCtrlOut[0])

    def reorderNumber(self, prefix, sideRGT, sideLFT):
        # get the number
        newPrefix = self.replacePosLFTRGT(object=prefix, sideRGT=sideRGT, sideLFT=sideLFT)
        try:
            patterns = [r'\d+']
            prefixNumber = au.prefix_name(newPrefix)
            for p in patterns:
                prefixNumber = re.findall(p, prefixNumber)[0]
        except:
            prefixNumber=''

        # get the prefix without number
        prefixNoNumber = str(newPrefix).translate(None, digits)

        return prefixNoNumber, prefixNumber

    def replacePosLFTRGT(self, object, sideRGT, sideLFT):
        if sideRGT in object:
            crvNewName = object.replace(sideRGT, '')
        elif sideLFT in object:
            crvNewName = object.replace(sideLFT, '')
        else:
            crvNewName = object

        return crvNewName

    def cornerReverseNode(self, sideRGT, sideLFT, lidCornerCtrl, side, lidCornerName='', targetUp='', targetLow=''):
        newName, numberNew = self.reorderNumber(prefix=lidCornerName, sideRGT=sideRGT, sideLFT=sideLFT)

        transRev = mc.createNode('multiplyDivide', n=newName + 'Trans' + numberNew + side + '_mdn')
        rotRev = mc.createNode('multiplyDivide', n=newName+ 'Rot' + numberNew + side + '_mdn')
        mc.connectAttr(lidCornerCtrl + '.translate', transRev + '.input1')
        mc.setAttr(transRev + '.input2X', -1)

        mc.connectAttr(lidCornerCtrl + '.rotate', rotRev + '.input1')
        mc.setAttr(rotRev + '.input2Y', -1)
        mc.setAttr(rotRev + '.input2Z', -1)

        mc.connectAttr(transRev + '.output', targetUp + '.translate')
        mc.connectAttr(rotRev + '.output', targetUp + '.rotate')
        mc.connectAttr(transRev + '.output', targetLow + '.translate')
        mc.connectAttr(rotRev + '.output', targetLow + '.rotate')

    def cornerCtrl(self, matchPosOne, matchPosTwo, prefix, scale, side, ctrlShape, ctrlColor, suffixController, addAttr=False):
        cornerCtrl = ct.Control(match_obj_first_position=matchPosOne, match_obj_second_position=matchPosTwo,
                                prefix=prefix,
                                shape=ctrlShape, groups_ctrl=['Zro', 'Offset'],
                                ctrl_size=scale * 0.07, suffix=suffixController,
                                ctrl_color=ctrlColor, lock_channels=['v', 's'], side=side)

        # check position
        pos = mc.xform(cornerCtrl.control, ws=1, q=1, t=1)[0]

        # flipping the controller
        if pos < 0:
            mc.setAttr(cornerCtrl.parent_control[0] + '.scaleX', -1)

        self.control = cornerCtrl.control
        self.parentControlZro = cornerCtrl.parent_control[0]
        self.parentControlOffset = cornerCtrl.parent_control[1]

        # ADD ATTRIBUTE
        if addAttr:
            self.showDtlCtrl = au.add_attribute(objects=[cornerCtrl.control], long_name=['showDetailCtrl'],
                                                attributeType="long", min=0, max=1, dv=0, keyable=True)

            return cornerCtrl.control, cornerCtrl.parent_control[0], cornerCtrl.parent_control[1], self.showDtlCtrl

        else:
            return cornerCtrl.control, cornerCtrl.parent_control[0], cornerCtrl.parent_control[1]
