from __builtin__ import reload

import os
import maya.cmds as mc
import pymel.core as pm
import rigging.library.utils.pole_vector as pv
import rigging.tools.AD_utils as au

reload(au)
reload(pv)

def display_ui():

    adien_snap_fkIk = 'AdienSnapFkIk'
    pm.window(adien_snap_fkIk, exists=True)

    if pm.window(adien_snap_fkIk, exists=True):
        pm.deleteUI(adien_snap_fkIk)

    with pm.window(adien_snap_fkIk, title='Adien Fk/Ik Snap', width=275, height=50):
        with pm.columnLayout(rs=10, adjustableColumn=True):
            pm.button(label='To Fk', width=275, height=50, backgroundColor=[0.46, 0.86, 0.46],
                      command=pm.Callback(ik_to_fk))
            pm.button(label='To Ik', width=275, height=50, backgroundColor=[0.86, 0.46, 0.46],
                      command=pm.Callback(fk_to_ik))

            pm.text(l="http://google.com", hyperlink=True)

    pm.showWindow()

def ik_to_fk():

    # listing fk ik setup selection
    fkik_ctrl_select = pm.ls(sl=1)

    # assign as instance fkik leg setup
    if fkik_ctrl_select:

        # listing the connection
        try:
            mc.listConnections(fkik_ctrl_select[0] + '.upper_limb_snap_jnt')[0]
        except:
            mc.error('To run the snapping fk/ik please select arm or leg setup controller!')

        upper_limb_snap_jnt = mc.listConnections(fkik_ctrl_select[0] + '.upper_limb_snap_jnt')[0]
        middle_limb_snap_jnt = mc.listConnections(fkik_ctrl_select[0] + '.middle_limb_snap_jnt')[0]
        lower_limb_snap_jnt = mc.listConnections(fkik_ctrl_select[0] + '.lower_limb_snap_jnt')[0]
        upper_limb_fk_ctrl = mc.listConnections(fkik_ctrl_select[0] + '.upper_limb_fk_ctrl')[0]
        middle_limb_fk_ctrl = mc.listConnections(fkik_ctrl_select[0] + '.middle_limb_fk_ctrl')[0]
        lower_limb_fk_ctrl = mc.listConnections(fkik_ctrl_select[0] + '.lower_limb_fk_ctrl')[0]
        fk_ik_arm_ctrl = mc.listConnections(fkik_ctrl_select[0] + '.fk_ik_arm_ctrl', s=1)
        fk_ik_leg_ctrl = mc.listConnections(fkik_ctrl_select[0] + '.fk_ik_leg_ctrl', s=1)
        # run snap for arm
        try:
            if fkik_ctrl_select[0] + '.FkIk'==0:
                return fkik_ctrl_select[0]
        except:
            pass

        if fk_ik_arm_ctrl:
            ik_to_fk_setup(upper_limb_snap_jnt=upper_limb_snap_jnt, middle_limb_snap_jnt=middle_limb_snap_jnt,
                           lower_limb_snap_jnt=lower_limb_snap_jnt, middle_limb_ctrl=middle_limb_fk_ctrl,
                           lower_limb_ctrl=lower_limb_fk_ctrl, upper_limb_ctrl=upper_limb_fk_ctrl
                           )
        # run snap for leg
        if fk_ik_leg_ctrl:
            end_limb_snap_jnt = mc.listConnections(fkik_ctrl_select[0] + '.end_limb_snap_jnt')[0]
            end_limb_fk_ctrl = mc.listConnections(fkik_ctrl_select[0] + '.end_limb_fk_ctrl')[0]

            ik_to_fk_setup(upper_limb_snap_jnt=upper_limb_snap_jnt, middle_limb_snap_jnt=middle_limb_snap_jnt,
                           lower_limb_snap_jnt=lower_limb_snap_jnt, middle_limb_ctrl=middle_limb_fk_ctrl,
                           lower_limb_ctrl=lower_limb_fk_ctrl, upper_limb_ctrl=upper_limb_fk_ctrl,
                           end_limb_snap_jnt=end_limb_snap_jnt, end_limb_ctrl=end_limb_fk_ctrl,
                           leg=True)

        mc.setAttr(fkik_ctrl_select[0] + '.FkIk', 0)

def fk_to_ik(value_axis_towards_middle_arm_jnt=2.25326085, value_axis_towards_lower_arm_jnt=2.39415336,
             value_axis_towards_middle_leg_jnt=5.36579657, value_axis_towards_lower_leg_jnt=4.69395685,
             axis_towards='translateY'):
    # listing fk ik setup selection
    fkik_ctrl_select = pm.ls(sl=1)

    # assign as instance fkik leg setup
    if fkik_ctrl_select:
        # query the connection
        try:
            mc.listConnections(fkik_ctrl_select[0] + '.upper_limb_snap_jnt')[0]
        except:
            mc.error('for run the snapping fk/ik please select arm or leg setup controller!')

        upper_limb_snap_jnt = mc.listConnections(fkik_ctrl_select[0] + '.upper_limb_snap_jnt')[0]
        middle_limb_snap_jnt = mc.listConnections(fkik_ctrl_select[0] + '.middle_limb_snap_jnt')[0]
        lower_limb_snap_jnt = mc.listConnections(fkik_ctrl_select[0] + '.lower_limb_snap_jnt')[0]
        poleVector_ctrl = mc.listConnections(fkik_ctrl_select[0] + '.poleVector_ctrl')[0]
        lower_limb_ik_ctrl = mc.listConnections(fkik_ctrl_select[0] + '.lower_limb_ik_ctrl')[0]
        upper_limb_ik_ctrl = mc.listConnections(fkik_ctrl_select[0] + '.upper_limb_ik_ctrl')[0]
        middle_limb_jnt = mc.listConnections(fkik_ctrl_select[0] + '.middle_limb_jnt')[0]
        lower_limb_jnt = mc.listConnections(fkik_ctrl_select[0] + '.lower_limb_jnt')[0]
        fk_ik_arm_ctrl = mc.listConnections(fkik_ctrl_select[0] + '.fk_ik_arm_ctrl', s=1)
        fk_ik_leg_ctrl = mc.listConnections(fkik_ctrl_select[0] + '.fk_ik_leg_ctrl', s=1)

        # condition of controller
        try:
            if fkik_ctrl_select[0] + '.FkIk'==1:
                return fkik_ctrl_select[0]
        except:
            pass

        # run for snap arm
        if fk_ik_arm_ctrl:
            fk_to_ik_setup(upper_limb_snap_jnt=upper_limb_snap_jnt, middle_limb_snap_jnt=middle_limb_snap_jnt,
                           lower_limb_snap_jnt=lower_limb_snap_jnt, polevector_limb_ctrl=poleVector_ctrl,
                           lower_limb_ctrl=lower_limb_ik_ctrl, upper_limb_ctrl=upper_limb_ik_ctrl,
                           value_axis_towards_middle_jnt=value_axis_towards_middle_arm_jnt,
                           value_axis_towards_lower_jnt=value_axis_towards_lower_arm_jnt,
                           middle_limb_jnt=middle_limb_jnt, lower_limb_jnt=lower_limb_jnt, axis_towards=axis_towards,
                           )
        # run for snap leg
        if fk_ik_leg_ctrl:
            end_limb_jnt = mc.listConnections(fkik_ctrl_select[0] + '.end_limb_jnt')[0]
            toe_wiggle_attr = mc.listConnections(fkik_ctrl_select[0] + '.toe_wiggle_attr')[0]

            fk_to_ik_setup(upper_limb_snap_jnt=upper_limb_snap_jnt, middle_limb_snap_jnt=middle_limb_snap_jnt,
                           lower_limb_snap_jnt=lower_limb_snap_jnt, polevector_limb_ctrl=poleVector_ctrl,
                           lower_limb_ctrl=lower_limb_ik_ctrl, upper_limb_ctrl=upper_limb_ik_ctrl,
                           value_axis_towards_middle_jnt=value_axis_towards_middle_leg_jnt,
                           value_axis_towards_lower_jnt=value_axis_towards_lower_leg_jnt,
                           middle_limb_jnt=middle_limb_jnt, lower_limb_jnt=lower_limb_jnt, axis_towards=axis_towards,
                           end_limb_jnt=end_limb_jnt, end_limb_ctrl=toe_wiggle_attr, leg=True)

        mc.setAttr(fkik_ctrl_select[0] + '.FkIk', 1)

def ik_to_fk_setup(upper_limb_snap_jnt, middle_limb_snap_jnt, lower_limb_snap_jnt,
                   middle_limb_ctrl, lower_limb_ctrl, upper_limb_ctrl,
                   end_limb_snap_jnt=None, end_limb_ctrl=None, leg=None):

    # query world position
    xform_upper_limb_rot = mc.xform(upper_limb_snap_jnt, ws=1, q=1, ro=1)
    xform_middle_limb_rot = mc.xform(middle_limb_snap_jnt, ws=1, q=1, ro=1)
    xform_low_limb_rot = mc.xform(lower_limb_snap_jnt, ws=1, q=1, ro=1)
    xform_upper_limb_pos = mc.xform(upper_limb_snap_jnt, ws=1, q=1, t=1)
    xform_middle_limb_pos = mc.xform(middle_limb_snap_jnt, ws=1, q=1, t=1)
    xform_low_limb_pos = mc.xform(lower_limb_snap_jnt, ws=1, q=1, t=1)

    # set the position
    mc.xform(upper_limb_ctrl, ws=1, ro=(xform_upper_limb_rot[0], xform_upper_limb_rot[1], xform_upper_limb_rot[2]))
    mc.xform(middle_limb_ctrl, ws=1, ro=(xform_middle_limb_rot[0], xform_middle_limb_rot[1], xform_middle_limb_rot[2]))
    mc.xform(lower_limb_ctrl, ws=1, ro=(xform_low_limb_rot[0], xform_low_limb_rot[1], xform_low_limb_rot[2]))
    mc.xform(upper_limb_ctrl, ws=1, t=(xform_upper_limb_pos[0], xform_upper_limb_pos[1], xform_upper_limb_pos[2]))
    mc.xform(middle_limb_ctrl, ws=1, t=(xform_middle_limb_pos[0], xform_middle_limb_pos[1], xform_middle_limb_pos[2]))
    mc.xform(lower_limb_ctrl, ws=1, t=(xform_low_limb_pos[0], xform_low_limb_pos[1], xform_low_limb_pos[2]))

    # exeption for the leg
    if leg:
        xform_end_limb_rot = mc.xform(end_limb_snap_jnt, ws=1, q=1, ro=1)
        xform_end_limb_pos = mc.xform(end_limb_snap_jnt, ws=1, q=1, t=1)
        mc.xform(end_limb_ctrl, ws=1, ro=(xform_end_limb_rot[0], xform_end_limb_rot[1], xform_end_limb_rot[2]))
        mc.xform(end_limb_ctrl, ws=1, t=(xform_end_limb_pos[0], xform_end_limb_pos[1], xform_end_limb_pos[2]))

def fk_to_ik_setup(upper_limb_snap_jnt, middle_limb_snap_jnt, lower_limb_snap_jnt,
                   polevector_limb_ctrl, lower_limb_ctrl, upper_limb_ctrl, value_axis_towards_middle_jnt,
                   value_axis_towards_lower_jnt, middle_limb_jnt, lower_limb_jnt, axis_towards,
                   end_limb_jnt=None, end_limb_ctrl=None, leg=None):

    # set to default
    mc.setAttr(lower_limb_ctrl + '.stretch', 1)
    mc.setAttr(lower_limb_ctrl + '.softIk', 0)
    mc.setAttr(lower_limb_ctrl + '.ikSnap', 0)
    mc.setAttr(lower_limb_ctrl + '.slide', 0)
    mc.setAttr(lower_limb_ctrl + '.twist', 0)

    # set to default leg
    if leg :
        mc.setAttr(lower_limb_ctrl+'.footRoll', 0)
        mc.setAttr(lower_limb_ctrl+'.ballStartLift', 30)
        mc.setAttr(lower_limb_ctrl+'.toeStartStraight', 60)
        mc.setAttr(lower_limb_ctrl+'.tilt', 0)
        mc.setAttr(lower_limb_ctrl+'.heelSpin', 0)
        mc.setAttr(lower_limb_ctrl+'.toeSpin', 0)
        mc.setAttr(lower_limb_ctrl+'.toeSpin', 0)
        mc.setAttr(lower_limb_ctrl+'.toeRoll', 0)
        mc.setAttr(lower_limb_ctrl+'.toeWiggle', 0)

        xform_end_limb_rot = mc.getAttr(end_limb_jnt+'.rotateX')
        mc.setAttr('%s.toeWiggle' % (end_limb_ctrl),(-1*xform_end_limb_rot))

    # query position and rotation
    xform_upper_limb_rot = mc.xform(upper_limb_snap_jnt, ws=1, q=1, ro=1)
    xform_low_limb_rot = mc.xform(lower_limb_snap_jnt, ws=1, q=1, ro=1)
    xform_upper_limb_pos = mc.xform(upper_limb_snap_jnt, ws=1, q=1, t=1)
    xform_middle_limb_pos = mc.xform(middle_limb_snap_jnt, ws=1, q=1, t=1)
    xform_low_limb_pos = mc.xform(lower_limb_snap_jnt, ws=1, q=1, t=1)

    # set position and rotation
    mc.xform(upper_limb_ctrl, ws=1, ro=(xform_upper_limb_rot[0], xform_upper_limb_rot[1], xform_upper_limb_rot[2]))
    mc.xform(lower_limb_ctrl, ws=1, ro=(xform_low_limb_rot[0], xform_low_limb_rot[1], xform_low_limb_rot[2]))
    mc.xform(upper_limb_ctrl, ws=1, t=(xform_upper_limb_pos[0], xform_upper_limb_pos[1], xform_upper_limb_pos[2]))
    mc.xform(lower_limb_ctrl, ws=1, t=(xform_low_limb_pos[0], xform_low_limb_pos[1], xform_low_limb_pos[2]))

    # for pole vector position
    up_joint_position = mc.xform(upper_limb_snap_jnt, q=1, ws=1, t=1)
    mid_joint_position = mc.xform(middle_limb_snap_jnt, q=1, ws=1, t=1)
    low_joint_position = mc.xform(lower_limb_snap_jnt, q=1, ws=1, t=1)
    get_poleVector_position = pv.get_poleVector_position(up_joint_position, mid_joint_position, low_joint_position)
    mc.move(get_poleVector_position.x, get_poleVector_position.y, get_poleVector_position.z, polevector_limb_ctrl)

    # calculate for stretching and snapping the pole vector controller
    total_value_default = value_axis_towards_middle_jnt + value_axis_towards_lower_jnt
    current_value_axis_towards_middle_jnt = mc.getAttr('%s.%s' % (middle_limb_jnt, axis_towards))
    current_value_axis_towards_lower_jnt = mc.getAttr('%s.%s' % (lower_limb_jnt, axis_towards))
    total_current_value = current_value_axis_towards_middle_jnt + current_value_axis_towards_lower_jnt

    # negative position (right)
    if current_value_axis_towards_middle_jnt < 0:
        if abs(total_current_value+total_value_default) > 0.01:
            mc.setAttr(lower_limb_ctrl+'.ikSnap', 1)
            mc.xform(polevector_limb_ctrl, ws=1, t=(xform_middle_limb_pos[0], xform_middle_limb_pos[1],
                                                    xform_middle_limb_pos[2]))
    # positive position (left)
    else:
        if abs(total_current_value-total_value_default) > 0.01:
            mc.setAttr(lower_limb_ctrl+'.ikSnap', 1)
            mc.xform(polevector_limb_ctrl, ws=1, t=(xform_middle_limb_pos[0], xform_middle_limb_pos[1],
                                                    xform_middle_limb_pos[2]))