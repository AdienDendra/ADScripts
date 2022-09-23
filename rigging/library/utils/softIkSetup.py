from __future__ import absolute_import

import maya.cmds as cmds

from rigging.tools import utils as rt_utils


def run_soft_ik_joint(prefix, side, lower_limb_ik_gimbal, foot_reverse_joint_or_position_soft_jnt,
                      position_lower_limb_jnt,
                      lowerLimbIkControl):
    ori_constraint = cmds.orientConstraint(lower_limb_ik_gimbal, foot_reverse_joint_or_position_soft_jnt, mo=1)

    # constraint the soft jnt from gimbal control and lower limb distance
    stretch_ik_point_constraint = cmds.pointConstraint(lower_limb_ik_gimbal, position_lower_limb_jnt,
                                                       foot_reverse_joint_or_position_soft_jnt, mo=1)
    # set the key driver key for stretch setup
    stretch_ik_reverse = cmds.shadingNode('reverse', asUtility=1, n='%s%s%s_rev' % (prefix, 'StretchIk', side))

    # connect the attribute stretch from the limb controller
    cmds.connectAttr(lowerLimbIkControl + '.stretch', stretch_ik_reverse + '.inputX')
    cmds.connectAttr(stretch_ik_reverse + '.outputX',
                     stretch_ik_point_constraint[0] + ('.%sW1' % position_lower_limb_jnt))
    cmds.connectAttr(lowerLimbIkControl + '.stretch',
                     stretch_ik_point_constraint[0] + ('.%sW0' % lower_limb_ik_gimbal))

    # rename constraint
    ori_constraint = rt_utils.constraint_rename(ori_constraint)
    stretch_ik_point_constraint = rt_utils.constraint_rename(stretch_ik_point_constraint)

    return ori_constraint[0], stretch_ik_point_constraint[0]
