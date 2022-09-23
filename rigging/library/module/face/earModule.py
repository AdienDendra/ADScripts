from __future__ import absolute_import

import maya.cmds as cmds

from rigging.library.utils import controller as rlu_controller, transform as rlu_transform
from rigging.tools import utils as rt_utils


class Ear:
    def __init__(self,
                 scale,
                 ear_jnt,
                 ear_prefix,
                 head_ctrl_gimbal,
                 side,
                 side_LFT,
                 side_RGT,
                 suffix_controller
                 ):

        position = cmds.xform(ear_jnt, ws=1, q=1, t=1)[0]

        # CREATE GROUP PARENT
        rlu_transform.create_parent_transform(parent_list=[''], object=ear_jnt, match_position=ear_jnt,
                                              prefix=ear_prefix, suffix='_jnt', side=side)

        # CREATE EAR CONTROL
        ear_ctrl = rlu_controller.Control(match_obj_first_position=ear_jnt, prefix=ear_prefix,
                                          shape=rlu_controller.CUBE, suffix=suffix_controller,
                                          groups_ctrl=[''], ctrl_size=scale * 0.25,
                                          ctrl_color='red', lock_channels=['v'], side=side)

        # ADD REVERSING NODE
        if position < 0:
            cmds.setAttr(ear_ctrl.parent_control[0] + '.scaleX', -1)
            self.reverse_node(ear_ctrl.control, ear_jnt, side_RGT, side_LFT, side)
            rt_utils.connect_attr_scale(ear_ctrl.control, ear_jnt)
        else:
            rt_utils.connect_attr_object(ear_ctrl.control, ear_jnt)

        # PARENT EAR CTRL TO HEAD GIMBAL
        cmds.parent(ear_ctrl.parent_control[0], head_ctrl_gimbal)

    def reverse_node(self, object, target_jnt, side_RGT, side_LFT, side, input_trans2X=-1, input_trans2Y=1,
                     input_trans2Z=1,
                     input_rotate2X=1, input_rotate2Y=-1, input_rotate2Z=-1):

        if side_RGT in target_jnt:
            newName = target_jnt.replace(side_RGT, '')
        elif side_LFT in target_jnt:
            newName = target_jnt.replace(side_LFT, '')
        else:
            newName = target_jnt

        transMdn = cmds.createNode('multiplyDivide', n=rt_utils.prefix_name(newName) + 'Trans' + side + '_mdn')
        cmds.connectAttr(object + '.translate', transMdn + '.input1')
        cmds.setAttr(transMdn + '.input2X', input_trans2X)
        cmds.setAttr(transMdn + '.input2Y', input_trans2Y)
        cmds.setAttr(transMdn + '.input2Z', input_trans2Z)

        cmds.connectAttr(transMdn + '.output', target_jnt + '.translate')

        rotMdn = cmds.createNode('multiplyDivide', n=rt_utils.prefix_name(newName) + 'Rot' + side + '_mdn')
        cmds.connectAttr(object + '.rotate', rotMdn + '.input1')
        cmds.setAttr(rotMdn + '.input2X', input_rotate2X)
        cmds.setAttr(rotMdn + '.input2Y', input_rotate2Y)
        cmds.setAttr(rotMdn + '.input2Z', input_rotate2Z)
        cmds.connectAttr(rotMdn + '.output', target_jnt + '.rotate')
