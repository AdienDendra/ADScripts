from __future__ import absolute_import

import maya.OpenMaya as om
import maya.cmds as cmds
import pymel.core as pm


def ik_to_fk():
    # listing fk ik setup selection`
    fkik_ctrl_select = pm.ls(sl=1)

    # assign as instance fkik leg setup
    # if fkik_ctrl_select:?

    # listing the connection
    try:
        cmds.listConnections(fkik_ctrl_select[0] + '.upper_limb_jnt')[0]
    except:
        cmds.error('To run the snapping fk/ik please select arm or leg setup controller!')

    # condition of controller
    getattr_ctrl = pm.getAttr(fkik_ctrl_select[0] + '.FkIk')
    if getattr_ctrl == 0:
        return fkik_ctrl_select[0]
    else:
        upper_limb_jnt = cmds.listConnections(fkik_ctrl_select[0] + '.upper_limb_jnt')[0]
        middle_limb_jnt = cmds.listConnections(fkik_ctrl_select[0] + '.middle_limb_jnt')[0]
        lower_limb_jnt = cmds.listConnections(fkik_ctrl_select[0] + '.lower_limb_jnt')[0]
        upper_limb_fk_ctrl = cmds.listConnections(fkik_ctrl_select[0] + '.upper_limb_fk_ctrl')[0]
        middle_limb_fk_ctrl = cmds.listConnections(fkik_ctrl_select[0] + '.middle_limb_fk_ctrl')[0]
        lower_limb_fk_ctrl = cmds.listConnections(fkik_ctrl_select[0] + '.lower_limb_fk_ctrl')[0]
        fk_ik_arm_ctrl = cmds.listConnections(fkik_ctrl_select[0] + '.fk_ik_arm_ctrl', s=1)
        fk_ik_leg_ctrl = cmds.listConnections(fkik_ctrl_select[0] + '.fk_ik_leg_ctrl', s=1)

        # run snap for arm
        if fk_ik_arm_ctrl:
            ik_to_fk_setup(upper_limb_snap_jnt=upper_limb_jnt, middle_limb_snap_jnt=middle_limb_jnt,
                           lower_limb_snap_jnt=lower_limb_jnt, middle_limb_ctrl=middle_limb_fk_ctrl,
                           lower_limb_ctrl=lower_limb_fk_ctrl, upper_limb_ctrl=upper_limb_fk_ctrl
                           )
        # run snap for leg
        if fk_ik_leg_ctrl:
            end_limb_jnt = cmds.listConnections(fkik_ctrl_select[0] + '.end_limb_jnt')[0]
            end_limb_fk_ctrl = cmds.listConnections(fkik_ctrl_select[0] + '.end_limb_fk_ctrl')[0]

            ik_to_fk_setup(upper_limb_snap_jnt=upper_limb_jnt, middle_limb_snap_jnt=middle_limb_jnt,
                           lower_limb_snap_jnt=lower_limb_jnt, middle_limb_ctrl=middle_limb_fk_ctrl,
                           lower_limb_ctrl=lower_limb_fk_ctrl, upper_limb_ctrl=upper_limb_fk_ctrl,
                           end_limb_snap_jnt=end_limb_jnt, end_limb_ctrl=end_limb_fk_ctrl,
                           leg=True)

        cmds.setAttr(fkik_ctrl_select[0] + '.FkIk', 0)


def fk_to_ik(axis_aim='translateY'):
    # listing fk ik setup selection
    fkik_ctrl_select = pm.ls(sl=1)

    # assign as instance fkik leg setup
    # if fkik_ctrl_select:
    # query the connection
    try:
        cmds.listConnections(fkik_ctrl_select[0] + '.upper_limb_jnt')[0]
    except:
        cmds.error('for run the snapping fk/ik please select arm or leg setup controller!')

    # condition of controller
    getattr_ctrl = pm.getAttr(fkik_ctrl_select[0] + '.FkIk')
    if getattr_ctrl == 1:
        return fkik_ctrl_select[0]
    else:
        upper_limb_jnt = cmds.listConnections(fkik_ctrl_select[0] + '.upper_limb_jnt')[0]
        middle_limb_jnt = cmds.listConnections(fkik_ctrl_select[0] + '.middle_limb_jnt')[0]
        lower_limb_jnt = cmds.listConnections(fkik_ctrl_select[0] + '.lower_limb_jnt')[0]
        poleVector_ctrl = cmds.listConnections(fkik_ctrl_select[0] + '.poleVector_ctrl')[0]
        lower_limb_ik_ctrl = cmds.listConnections(fkik_ctrl_select[0] + '.lower_limb_ik_ctrl')[0]
        upper_limb_ik_ctrl = cmds.listConnections(fkik_ctrl_select[0] + '.upper_limb_ik_ctrl')[0]
        middle_ref_jnt = cmds.listConnections(fkik_ctrl_select[0] + '.middle_ref_jnt')[0]
        lower_ref_jnt = cmds.listConnections(fkik_ctrl_select[0] + '.lower_ref_jnt')[0]
        fk_ik_arm_ctrl = cmds.listConnections(fkik_ctrl_select[0] + '.fk_ik_arm_ctrl', s=1)
        fk_ik_leg_ctrl = cmds.listConnections(fkik_ctrl_select[0] + '.fk_ik_leg_ctrl', s=1)

        # run for snap arm
        if fk_ik_arm_ctrl:
            fk_to_ik_setup(upper_limb_snap_jnt=upper_limb_jnt, middle_limb_snap_jnt=middle_limb_jnt,
                           lower_limb_snap_jnt=lower_limb_jnt, polevector_limb_ctrl=poleVector_ctrl,
                           lower_limb_ctrl=lower_limb_ik_ctrl, upper_limb_ctrl=upper_limb_ik_ctrl,
                           value_axis_aim_middle_jnt=middle_ref_jnt,
                           value_axis_aim_lower_jnt=lower_ref_jnt,
                           axis_towards=axis_aim,
                           )
        # run for snap leg
        if fk_ik_leg_ctrl:
            end_limb_jnt = cmds.listConnections(fkik_ctrl_select[0] + '.end_limb_jnt')[0]
            toe_wiggle_attr = cmds.listConnections(fkik_ctrl_select[0] + '.toe_wiggle_attr')[0]

            fk_to_ik_setup(upper_limb_snap_jnt=upper_limb_jnt, middle_limb_snap_jnt=middle_limb_jnt,
                           lower_limb_snap_jnt=lower_limb_jnt, polevector_limb_ctrl=poleVector_ctrl,
                           lower_limb_ctrl=lower_limb_ik_ctrl, upper_limb_ctrl=upper_limb_ik_ctrl,
                           value_axis_aim_middle_jnt=middle_ref_jnt,
                           value_axis_aim_lower_jnt=lower_ref_jnt,
                           axis_towards=axis_aim,
                           end_limb_snap_jnt=end_limb_jnt, end_limb_ctrl=toe_wiggle_attr, leg=True)

        cmds.setAttr(fkik_ctrl_select[0] + '.FkIk', 1)


def ik_to_fk_setup(upper_limb_snap_jnt, middle_limb_snap_jnt, lower_limb_snap_jnt,
                   middle_limb_ctrl, lower_limb_ctrl, upper_limb_ctrl,
                   end_limb_snap_jnt=None, end_limb_ctrl=None, leg=None):
    # query world position
    xform_upper_limb_rot = cmds.xform(upper_limb_snap_jnt, ws=1, q=1, ro=1)
    xform_middle_limb_rot = cmds.xform(middle_limb_snap_jnt, ws=1, q=1, ro=1)
    xform_low_limb_rot = cmds.xform(lower_limb_snap_jnt, ws=1, q=1, ro=1)
    xform_upper_limb_pos = cmds.xform(upper_limb_snap_jnt, ws=1, q=1, t=1)
    xform_middle_limb_pos = cmds.xform(middle_limb_snap_jnt, ws=1, q=1, t=1)
    xform_low_limb_pos = cmds.xform(lower_limb_snap_jnt, ws=1, q=1, t=1)

    # set the position
    cmds.xform(upper_limb_ctrl, ws=1, ro=(xform_upper_limb_rot[0], xform_upper_limb_rot[1], xform_upper_limb_rot[2]))
    cmds.xform(middle_limb_ctrl, ws=1,
               ro=(xform_middle_limb_rot[0], xform_middle_limb_rot[1], xform_middle_limb_rot[2]))
    cmds.xform(lower_limb_ctrl, ws=1, ro=(xform_low_limb_rot[0], xform_low_limb_rot[1], xform_low_limb_rot[2]))
    cmds.xform(upper_limb_ctrl, ws=1, t=(xform_upper_limb_pos[0], xform_upper_limb_pos[1], xform_upper_limb_pos[2]))
    cmds.xform(middle_limb_ctrl, ws=1, t=(xform_middle_limb_pos[0], xform_middle_limb_pos[1], xform_middle_limb_pos[2]))
    cmds.xform(lower_limb_ctrl, ws=1, t=(xform_low_limb_pos[0], xform_low_limb_pos[1], xform_low_limb_pos[2]))

    # exeption for the leg
    if leg:
        xform_end_limb_rot = cmds.xform(end_limb_snap_jnt, ws=1, q=1, ro=1)
        xform_end_limb_pos = cmds.xform(end_limb_snap_jnt, ws=1, q=1, t=1)
        cmds.xform(end_limb_ctrl, ws=1, ro=(xform_end_limb_rot[0], xform_end_limb_rot[1], xform_end_limb_rot[2]))
        cmds.xform(end_limb_ctrl, ws=1, t=(xform_end_limb_pos[0], xform_end_limb_pos[1], xform_end_limb_pos[2]))


def fk_to_ik_setup(upper_limb_snap_jnt, middle_limb_snap_jnt, lower_limb_snap_jnt,
                   polevector_limb_ctrl, lower_limb_ctrl, upper_limb_ctrl,
                   value_axis_aim_middle_jnt,
                   value_axis_aim_lower_jnt,
                   axis_towards, end_limb_snap_jnt=None, end_limb_ctrl=None, leg=None):
    # set to default
    cmds.setAttr(lower_limb_ctrl + '.stretch', 1)
    cmds.setAttr(lower_limb_ctrl + '.softIk', 0)
    cmds.setAttr(lower_limb_ctrl + '.ikSnap', 0)
    cmds.setAttr(lower_limb_ctrl + '.slide', 0)
    cmds.setAttr(lower_limb_ctrl + '.twist', 0)

    # set to default leg
    if leg:
        cmds.setAttr(lower_limb_ctrl + '.footRoll', 0)
        cmds.setAttr(lower_limb_ctrl + '.ballStartLift', 30)
        cmds.setAttr(lower_limb_ctrl + '.toeStartStraight', 60)
        cmds.setAttr(lower_limb_ctrl + '.tilt', 0)
        cmds.setAttr(lower_limb_ctrl + '.heelSpin', 0)
        cmds.setAttr(lower_limb_ctrl + '.toeSpin', 0)
        cmds.setAttr(lower_limb_ctrl + '.toeSpin', 0)
        cmds.setAttr(lower_limb_ctrl + '.toeRoll', 0)
        cmds.setAttr(lower_limb_ctrl + '.toeWiggle', 0)

        xform_end_limb_rot = cmds.getAttr(end_limb_snap_jnt + '.rotateX')
        cmds.setAttr('%s.toeWiggle' % (end_limb_ctrl), (-1 * xform_end_limb_rot))

    # query position and rotation
    xform_upper_limb_rot = cmds.xform(upper_limb_snap_jnt, ws=1, q=1, ro=1)
    xform_low_limb_rot = cmds.xform(lower_limb_snap_jnt, ws=1, q=1, ro=1)
    xform_upper_limb_pos = cmds.xform(upper_limb_snap_jnt, ws=1, q=1, t=1)
    xform_middle_limb_pos = cmds.xform(middle_limb_snap_jnt, ws=1, q=1, t=1)
    xform_low_limb_pos = cmds.xform(lower_limb_snap_jnt, ws=1, q=1, t=1)

    # set position and rotation
    cmds.xform(upper_limb_ctrl, ws=1, ro=(xform_upper_limb_rot[0], xform_upper_limb_rot[1], xform_upper_limb_rot[2]))
    cmds.xform(lower_limb_ctrl, ws=1, ro=(xform_low_limb_rot[0], xform_low_limb_rot[1], xform_low_limb_rot[2]))
    cmds.xform(upper_limb_ctrl, ws=1, t=(xform_upper_limb_pos[0], xform_upper_limb_pos[1], xform_upper_limb_pos[2]))
    cmds.xform(lower_limb_ctrl, ws=1, t=(xform_low_limb_pos[0], xform_low_limb_pos[1], xform_low_limb_pos[2]))

    # for pole vector position
    up_joint_position = cmds.xform(upper_limb_snap_jnt, q=1, ws=1, t=1)
    mid_joint_position = cmds.xform(middle_limb_snap_jnt, q=1, ws=1, t=1)
    low_joint_position = cmds.xform(lower_limb_snap_jnt, q=1, ws=1, t=1)

    get_poleVector_position = get_pole_vector_position(up_joint_position, mid_joint_position, low_joint_position)
    cmds.move(get_poleVector_position.x, get_poleVector_position.y, get_poleVector_position.z, polevector_limb_ctrl)

    # get attribute value of middle_ref_joint and lower_ref_joint
    value_axis_middle_jnt = cmds.getAttr('%s.%s' % (value_axis_aim_middle_jnt, axis_towards))
    value_axis_lower_jnt = cmds.getAttr('%s.%s' % (value_axis_aim_lower_jnt, axis_towards))

    # calculate for stretching and snapping the pole vector controller
    total_value_default = value_axis_middle_jnt + value_axis_lower_jnt
    current_value_axis_towards_middle_jnt = cmds.getAttr('%s.%s' % (middle_limb_snap_jnt, axis_towards))
    current_value_axis_towards_lower_jnt = cmds.getAttr('%s.%s' % (lower_limb_snap_jnt, axis_towards))
    total_current_value = current_value_axis_towards_middle_jnt + current_value_axis_towards_lower_jnt

    # negative position (right)
    if current_value_axis_towards_middle_jnt < 0:
        if abs(total_current_value + total_value_default) > 0.01:
            cmds.setAttr(lower_limb_ctrl + '.ikSnap', 1)
            cmds.xform(polevector_limb_ctrl, ws=1, t=(xform_middle_limb_pos[0], xform_middle_limb_pos[1],
                                                      xform_middle_limb_pos[2]))
    # positive position (left)
    else:
        if abs(total_current_value - total_value_default) > 0.01:
            cmds.setAttr(lower_limb_ctrl + '.ikSnap', 1)
            cmds.xform(polevector_limb_ctrl, ws=1, t=(xform_middle_limb_pos[0], xform_middle_limb_pos[1],
                                                      xform_middle_limb_pos[2]))


def get_pole_vector_position(root_pos, mid_pos, end_pos):
    root_jnt_vector = om.MVector(root_pos[0], root_pos[1], root_pos[2])
    mid_jnt_vector = om.MVector(mid_pos[0], mid_pos[1], mid_pos[2])
    end_jnt_vector = om.MVector(end_pos[0], end_pos[1], end_pos[2])

    line = (end_jnt_vector - root_jnt_vector)
    point = (mid_jnt_vector - root_jnt_vector)

    scale_value = (line * point) / (line * line)
    projection_vector = line * scale_value + root_jnt_vector

    pole_vector_position = (mid_jnt_vector - projection_vector).normal() + mid_jnt_vector

    return pole_vector_position
