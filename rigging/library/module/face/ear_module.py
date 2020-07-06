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
                 ear_jnt,
                 # ear_skn,
                 ear_prefix,
                 head_ctrl_gimbal,
                 side,
                 side_LFT,
                 side_RGT,
                 suffix_controller
                 ):

        position = mc.xform(ear_jnt, ws=1, q=1, t=1)[0]

        # CREATE GROUP PARENT
        tf.create_parent_transform(parent_list=[''], object=ear_jnt, match_position=ear_jnt,
                                   prefix=ear_prefix, suffix='_jnt', side=side)

        # CREATE EAR CONTROL
        ear_ctrl = ct.Control(match_obj_first_position=ear_jnt, prefix=ear_prefix,
                              shape=ct.CUBE, suffix=suffix_controller,
                              groups_ctrl=[''], ctrl_size=scale * 0.25,
                              ctrl_color='red', lock_channels=['v'], side=side)

        # ADD REVERSING NODE
        if position < 0:
            mc.setAttr(ear_ctrl.parent_control[0] + '.scaleX', -1)
            self.reverse_node(ear_ctrl.control, ear_jnt, side_RGT, side_LFT, side)
            au.connect_attr_scale(ear_ctrl.control, ear_jnt)
        else:
            au.connect_attr_object(ear_ctrl.control, ear_jnt)

        # PARENT EAR CTRL TO HEAD GIMBAL
        mc.parent(ear_ctrl.parent_control[0], head_ctrl_gimbal)

        # # CONSTRAINT SKIN
        # au.parent_scale_constraint(ear_jnt, ear_skn)


    def reverse_node(self, object, target_jnt, side_RGT, side_LFT, side, input_trans2X=-1, input_trans2Y=1,
                     input_trans2Z=1,
                     input_rotate2X=1, input_rotate2Y=-1, input_rotate2Z=-1):

        if side_RGT in target_jnt:
            newName = target_jnt.replace(side_RGT, '')
        elif side_LFT in target_jnt:
            newName = target_jnt.replace(side_LFT, '')
        else:
            newName = target_jnt

        transMdn = mc.createNode('multiplyDivide', n=au.prefix_name(newName) + 'Trans' + side + '_mdn')
        mc.connectAttr(object + '.translate', transMdn + '.input1')
        mc.setAttr(transMdn + '.input2X', input_trans2X)
        mc.setAttr(transMdn + '.input2Y', input_trans2Y)
        mc.setAttr(transMdn + '.input2Z', input_trans2Z)

        mc.connectAttr(transMdn + '.output', target_jnt + '.translate')

        rotMdn = mc.createNode('multiplyDivide', n=au.prefix_name(newName) + 'Rot' + side + '_mdn')
        mc.connectAttr(object + '.rotate', rotMdn + '.input1')
        mc.setAttr(rotMdn + '.input2X', input_rotate2X)
        mc.setAttr(rotMdn + '.input2Y', input_rotate2Y)
        mc.setAttr(rotMdn + '.input2Z', input_rotate2Z)
        mc.connectAttr(rotMdn + '.output', target_jnt + '.rotate')


