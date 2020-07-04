from __builtin__ import reload

import maya.cmds as mc

from rigging.library.utils import controller as ct
from rigging.library.utils import transform as tf
from rigging.tools import AD_utils as au

reload (ct)
reload (au)
reload (tf)

class Build:
    def __init__(self,
                 pupilJnt,
                 irisJnt,
                 pupilPrefix,
                 irisPrefix,
                 eyeballJnt,
                 eyeJntOffsetGrp,
                 scale,
                 eyeCtrl,
                 side,
                 suffixController
                 ):
        # create group brow

        # check position
        # pos = mc.xform(irisJnt, ws=1, q=1, t=1)[0]

        self.irisConnectGrp = mc.group(em=1, n='irisConnect'+side+'_grp')
        mc.delete(mc.parentConstraint(eyeballJnt, self.irisConnectGrp))

        # CREATE CONTROLLER
        pupilCtrl = ct.Control(match_obj_first_position=pupilJnt,
                               prefix=pupilPrefix,
                               shape=ct.CIRCLEPLUS, groups_ctrl=[''],
                               ctrl_size=scale * 0.08,
                               ctrl_color='red', lock_channels=['v'],
                               suffix=suffixController,
                               side=side)

        irisCtrl = ct.Control(match_obj_first_position=irisJnt,
                              prefix=irisPrefix,
                              shape=ct.CIRCLEPLUS, groups_ctrl=[''],
                              ctrl_size=scale * 0.12,
                              suffix=suffixController,
                              ctrl_color='blue', lock_channels=['v'], side=side)

        # CREATE GROUP CORESPONDENT THE JOINTS
        pupilGrp = tf.create_parent_transform(parent_list=[''], object=pupilJnt, match_position=pupilJnt,
                                              prefix=pupilPrefix, suffix='_jnt', side=side)

        irisGrp = tf.create_parent_transform(parent_list=[''], object=irisJnt, match_position=irisJnt,
                                             prefix=irisPrefix, suffix='_jnt', side=side)

        # ASSIGNED THE INSTANCE CLASS
        self.pupilCtrl = pupilCtrl.control
        self.pupilCtrlGrp= pupilCtrl.parent_control[0]
        self.irisCtrl = irisCtrl.control
        self.irisCtrlGrp= irisCtrl.parent_control[0]

        # if pos < 0:
        #     mc.setAttr(self.pupilCtrlGrp + '.scaleX', -1)
        #     mc.setAttr(self.irisCtrlGrp + '.scaleX', -1)
        #     self.reverseNode(self.pupilCtrl, pupilJnt, sideRGT, sideLFT, side)
        #     self.reverseNode(self.irisCtrl, irisJnt, sideRGT, sideLFT, side)
        #     au.connectAttrScale(self.pupilCtrl, pupilJnt)
        #     au.connectAttrScale(self.irisCtrl, irisJnt)
        #
        # else:
        au.connect_attr_object(pupilCtrl.control, pupilJnt)
        au.connect_attr_object(irisCtrl.control, irisJnt)

        mc.parent(self.pupilCtrlGrp, self.irisCtrl)
        mc.parent(self.irisConnectGrp, eyeCtrl)
        au.connect_attr_rotate(eyeJntOffsetGrp, self.irisConnectGrp)

        mc.parent(irisGrp[0], eyeballJnt)
        mc.parent(self.irisCtrlGrp, self.irisConnectGrp)



    # def reverseNode(self, object, targetJnt, sideRGT, sideLFT, side, inputTrans2X=-1, inputTrans2Y=1,
    #                 inputTrans2Z=1,
    #                 inputRot2X=1, inputRot2Y=-1, inputRot2Z=-1):
    #     if sideRGT in targetJnt:
    #         newName = targetJnt.replace(sideRGT, '')
    #     elif sideLFT in targetJnt:
    #         newName = targetJnt.replace(sideLFT, '')
    #     else:
    #         newName = targetJnt
    #
    #     transMdn = mc.createNode('multiplyDivide', n=au.prefixName(newName) + 'Trans' + side + '_mdn')
    #     mc.connectAttr(object + '.translate', transMdn + '.input1')
    #     mc.setAttr(transMdn + '.input2X', inputTrans2X)
    #     mc.setAttr(transMdn + '.input2Y', inputTrans2Y)
    #     mc.setAttr(transMdn + '.input2Z', inputTrans2Z)
    #
    #     mc.connectAttr(transMdn + '.output', targetJnt + '.translate')
    #
    #     rotMdn = mc.createNode('multiplyDivide', n=au.prefixName(newName) + 'Rot' + side + '_mdn')
    #     mc.connectAttr(object + '.rotate', rotMdn + '.input1')
    #     mc.setAttr(rotMdn + '.input2X', inputRot2X)
    #     mc.setAttr(rotMdn + '.input2Y', inputRot2Y)
    #     mc.setAttr(rotMdn + '.input2Z', inputRot2Z)
    #     mc.connectAttr(rotMdn + '.output', targetJnt + '.rotate')

