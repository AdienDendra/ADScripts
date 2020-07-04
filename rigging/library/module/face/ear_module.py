from __builtin__ import reload

import maya.cmds as mc

from rigging.library.utils import controller as ct
from rigging.library.utils import transform as tf
from rigging.tools import AD_utils as au

reload (ct)
reload (tf)
reload(au)

class Ear:
    def __init__(self,
                 scale,
                 earJnt,
                 earPrefix,
                 headCtrlGimbal,
                 side,
                 sideLFT,
                 sideRGT,
                 suffixController
                 ):

        pos = mc.xform(earJnt, ws=1, q=1, t=1)[0]

        # CREATE GROUP PARENT
        tf.create_parent_transform(parent_list=[''], object=earJnt, match_position=earJnt,
                                   prefix=earPrefix, suffix='_jnt', side=side)

        # CREATE EAR CONTROL
        earCtrl = ct.Control(match_obj_first_position=earJnt, prefix=earPrefix,
                             shape=ct.CUBE, suffix=suffixController,
                             groups_ctrl=[''], ctrl_size=scale * 0.25,
                             ctrl_color='red', lock_channels=['v'], side=side)

        # ADD REVERSING NODE
        if pos < 0:
            mc.setAttr(earCtrl.parent_control[0] + '.scaleX', -1)
            self.reverseNode(earCtrl.control, earJnt, sideRGT, sideLFT, side)
            au.connect_attr_scale(earCtrl.control, earJnt)
        else:
            au.connect_attr_object(earCtrl.control, earJnt)

        # PARENT EAR CTRL TO HEAD GIMBAL
        mc.parent(earCtrl.parent_control[0], headCtrlGimbal)


    def reverseNode(self, object, targetJnt, sideRGT, sideLFT, side, inputTrans2X=-1, inputTrans2Y=1,
                    inputTrans2Z=1,
                    inputRot2X=1, inputRot2Y=-1, inputRot2Z=-1):

        if sideRGT in targetJnt:
            newName = targetJnt.replace(sideRGT, '')
        elif sideLFT in targetJnt:
            newName = targetJnt.replace(sideLFT, '')
        else:
            newName = targetJnt

        transMdn = mc.createNode('multiplyDivide', n=au.prefix_name(newName) + 'Trans' + side + '_mdn')
        mc.connectAttr(object + '.translate', transMdn + '.input1')
        mc.setAttr(transMdn + '.input2X', inputTrans2X)
        mc.setAttr(transMdn + '.input2Y', inputTrans2Y)
        mc.setAttr(transMdn + '.input2Z', inputTrans2Z)

        mc.connectAttr(transMdn + '.output', targetJnt + '.translate')

        rotMdn = mc.createNode('multiplyDivide', n=au.prefix_name(newName) + 'Rot' + side + '_mdn')
        mc.connectAttr(object + '.rotate', rotMdn + '.input1')
        mc.setAttr(rotMdn + '.input2X', inputRot2X)
        mc.setAttr(rotMdn + '.input2Y', inputRot2Y)
        mc.setAttr(rotMdn + '.input2Z', inputRot2Z)
        mc.connectAttr(rotMdn + '.output', targetJnt + '.rotate')


