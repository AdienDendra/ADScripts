from __builtin__ import reload

import pymel.core as pm
import maya.OpenMaya as om
from rigging.tools import AD_utils as au

reload(au)


def display_ui():

    adien_snap_fkIk = 'AdienSnapFkIk'
    pm.window(adien_snap_fkIk, exists=True)

    if pm.window(adien_snap_fkIk, exists=True):
        pm.deleteUI(adien_snap_fkIk)

    with pm.window(adien_snap_fkIk, title='Adien Fk/Ik Snap', width=275, height=150):
        with pm.columnLayout(rs=5, co=('both',5), adj=True):
            pm.text(l='Select Leg/Arm Ctrl Setup:')
            pm.button(label='To Fk', width=265, height=40, backgroundColor=[0.46, 0.86, 0.46],
                      command=pm.Callback(ik_to_fk))
            pm.button(label='To Ik', width=265, height=40, backgroundColor=[0.86, 0.46, 0.46],
                      command=pm.Callback(fk_to_ik))
            pm.text(l='<a href="http://projects.adiendendra.com/">find out how to use it! >> </a>', hl=True)
            pm.separator(h=2, st="single")

    pm.showWindow()

def ik_to_fk():

    # listing fk ik setup selection`
    fkik_ctrl_select = pm.ls(sl=1)

    # assign as instance fkik leg setup
    # if fkik_ctrl_select:?

    # listing the connection
    try:
        pm.listConnections(fkik_ctrl_select[0] + '.Upper_Limb_Joint')[0]
    except:
        pm.error('To run the snapping fk/ik please select arm or leg setup controller!')

    # condition of controller
    getattr_ctrl = pm.getAttr(fkik_ctrl_select[0]+'.FkIk')
    if getattr_ctrl == 0:
        return fkik_ctrl_select[0]
    else:
        upper_limb_jnt = pm.listConnections(fkik_ctrl_select[0] + '.Upper_Limb_Joint')[0]
        middle_limb_jnt = pm.listConnections(fkik_ctrl_select[0] + '.Middle_Limb_Joint')[0]
        lower_limb_jnt = pm.listConnections(fkik_ctrl_select[0] + '.Lower_Limb_Joint')[0]
        upper_limb_fk_ctrl = pm.listConnections(fkik_ctrl_select[0] + '.Upper_Limb_Fk_Ctrl')[0]
        middle_limb_fk_ctrl = pm.listConnections(fkik_ctrl_select[0] + '.Middle_Limb_Fk_Ctrl')[0]
        lower_limb_fk_ctrl = pm.listConnections(fkik_ctrl_select[0] + '.Lower_Limb_Fk_Ctrl')[0]
        fk_ik_arm_ctrl = pm.listConnections(fkik_ctrl_select[0] + '.FkIk_Arm_Setup_Controller', s=1)
        fk_ik_leg_ctrl = pm.listConnections(fkik_ctrl_select[0] + '.FkIk_Leg_Setup_Controller', s=1)

        # run snap for arm
        if fk_ik_arm_ctrl:
            ik_to_fk_setup(upper_limb_snap_jnt=upper_limb_jnt, middle_limb_snap_jnt=middle_limb_jnt,
                           lower_limb_snap_jnt=lower_limb_jnt, middle_limb_ctrl=middle_limb_fk_ctrl,
                           lower_limb_ctrl=lower_limb_fk_ctrl, upper_limb_ctrl=upper_limb_fk_ctrl
                           )
        # run snap for leg
        if fk_ik_leg_ctrl:
            end_limb_jnt = pm.listConnections(fkik_ctrl_select[0] + '.End_Limb_Joint')[0]
            end_limb_fk_ctrl = pm.listConnections(fkik_ctrl_select[0] + '.End_Limb_Fk_Ctrl')[0]

            ik_to_fk_setup(upper_limb_snap_jnt=upper_limb_jnt, middle_limb_snap_jnt=middle_limb_jnt,
                           lower_limb_snap_jnt=lower_limb_jnt, middle_limb_ctrl=middle_limb_fk_ctrl,
                           lower_limb_ctrl=lower_limb_fk_ctrl, upper_limb_ctrl=upper_limb_fk_ctrl,
                           end_limb_snap_jnt=end_limb_jnt, end_limb_ctrl=end_limb_fk_ctrl,
                           leg=True)

        pm.setAttr(fkik_ctrl_select[0] + '.FkIk', 0)

def fk_to_ik(axis_aim='translateY'):
    # listing fk ik setup selection
    fkik_ctrl_select = pm.ls(sl=1)

    # assign as instance fkik leg setup
    # if fkik_ctrl_select:
    # query the connection
    try:
        pm.listConnections(fkik_ctrl_select[0] + '.Upper_Limb_Joint')[0]
    except:
        pm.error('for run the snapping fk/ik please select arm or leg setup controller!')

    # condition of controller
    getattr_ctrl = pm.getAttr(fkik_ctrl_select[0]+'.FkIk')
    if getattr_ctrl == 1:
        return fkik_ctrl_select[0]
    else:
        upper_limb_jnt = pm.listConnections(fkik_ctrl_select[0] + '.Upper_Limb_Joint')[0]
        middle_limb_jnt = pm.listConnections(fkik_ctrl_select[0] + '.Middle_Limb_Joint')[0]
        lower_limb_jnt = pm.listConnections(fkik_ctrl_select[0] + '.Lower_Limb_Joint')[0]
        poleVector_ctrl = pm.listConnections(fkik_ctrl_select[0] + '.Pole_Vector_Ik_Ctrl')[0]
        lower_limb_ik_ctrl = pm.listConnections(fkik_ctrl_select[0] + '.Lower_Limb_Ik_Ctrl')[0]
        upper_limb_ik_ctrl = pm.listConnections(fkik_ctrl_select[0] + '.Upper_Limb_Ik_Ctrl')[0]
        middle_ref_jnt = pm.listConnections(fkik_ctrl_select[0] + '.middle_ref_jnt')[0]
        lower_ref_jnt = pm.listConnections(fkik_ctrl_select[0] + '.lower_ref_jnt')[0]
        fk_ik_arm_ctrl = pm.listConnections(fkik_ctrl_select[0] + '.FkIk_Arm_Setup_Controller', s=1)
        fk_ik_leg_ctrl = pm.listConnections(fkik_ctrl_select[0] + '.FkIk_Leg_Setup_Controller', s=1)

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
            end_limb_jnt = pm.listConnections(fkik_ctrl_select[0] + '.End_Limb_Joint')[0]
            toe_wiggle_attr = pm.listConnections(fkik_ctrl_select[0] + '.toe_wiggle_attr')[0]

            fk_to_ik_setup(upper_limb_snap_jnt=upper_limb_jnt, middle_limb_snap_jnt=middle_limb_jnt,
                           lower_limb_snap_jnt=lower_limb_jnt, polevector_limb_ctrl=poleVector_ctrl,
                           lower_limb_ctrl=lower_limb_ik_ctrl, upper_limb_ctrl=upper_limb_ik_ctrl,
                           value_axis_aim_middle_jnt=middle_ref_jnt,
                           value_axis_aim_lower_jnt=lower_ref_jnt,
                           axis_towards=axis_aim,
                           end_limb_snap_jnt=end_limb_jnt, end_limb_ctrl=toe_wiggle_attr, leg=True)

        pm.setAttr(fkik_ctrl_select[0] + '.FkIk', 1)

def ik_to_fk_setup(upper_limb_snap_jnt, middle_limb_snap_jnt, lower_limb_snap_jnt,
                   middle_limb_ctrl, lower_limb_ctrl, upper_limb_ctrl,
                   end_limb_snap_jnt=None, end_limb_ctrl=None, leg=None):

    # query world position
    xform_upper_limb_rot = pm.xform(upper_limb_snap_jnt, ws=1, q=1, ro=1)
    xform_middle_limb_rot = pm.xform(middle_limb_snap_jnt, ws=1, q=1, ro=1)
    xform_low_limb_rot = pm.xform(lower_limb_snap_jnt, ws=1, q=1, ro=1)
    xform_upper_limb_pos = pm.xform(upper_limb_snap_jnt, ws=1, q=1, t=1)
    xform_middle_limb_pos = pm.xform(middle_limb_snap_jnt, ws=1, q=1, t=1)
    xform_low_limb_pos = pm.xform(lower_limb_snap_jnt, ws=1, q=1, t=1)

    # set the position
    pm.xform(upper_limb_ctrl, ws=1, ro=(xform_upper_limb_rot[0], xform_upper_limb_rot[1], xform_upper_limb_rot[2]))
    pm.xform(middle_limb_ctrl, ws=1, ro=(xform_middle_limb_rot[0], xform_middle_limb_rot[1], xform_middle_limb_rot[2]))
    pm.xform(lower_limb_ctrl, ws=1, ro=(xform_low_limb_rot[0], xform_low_limb_rot[1], xform_low_limb_rot[2]))
    pm.xform(upper_limb_ctrl, ws=1, t=(xform_upper_limb_pos[0], xform_upper_limb_pos[1], xform_upper_limb_pos[2]))
    pm.xform(middle_limb_ctrl, ws=1, t=(xform_middle_limb_pos[0], xform_middle_limb_pos[1], xform_middle_limb_pos[2]))
    pm.xform(lower_limb_ctrl, ws=1, t=(xform_low_limb_pos[0], xform_low_limb_pos[1], xform_low_limb_pos[2]))

    # exeption for the leg
    if leg:
        xform_end_limb_rot = pm.xform(end_limb_snap_jnt, ws=1, q=1, ro=1)
        xform_end_limb_pos = pm.xform(end_limb_snap_jnt, ws=1, q=1, t=1)
        pm.xform(end_limb_ctrl, ws=1, ro=(xform_end_limb_rot[0], xform_end_limb_rot[1], xform_end_limb_rot[2]))
        pm.xform(end_limb_ctrl, ws=1, t=(xform_end_limb_pos[0], xform_end_limb_pos[1], xform_end_limb_pos[2]))


def fk_to_ik_setup(upper_limb_snap_jnt, middle_limb_snap_jnt, lower_limb_snap_jnt,
                   polevector_limb_ctrl, lower_limb_ctrl, upper_limb_ctrl,
                   value_axis_aim_middle_jnt,
                   value_axis_aim_lower_jnt,
                   axis_towards, end_limb_snap_jnt=None, end_limb_ctrl=None, leg=None):
    # set to default
    pm.setAttr(lower_limb_ctrl + '.stretch', 1)
    pm.setAttr(lower_limb_ctrl + '.softIk', 0)
    pm.setAttr(lower_limb_ctrl + '.ikSnap', 0)
    pm.setAttr(lower_limb_ctrl + '.slide', 0)
    pm.setAttr(lower_limb_ctrl + '.twist', 0)

    # set to default leg
    if leg :
        pm.setAttr(lower_limb_ctrl+'.footRoll', 0)
        pm.setAttr(lower_limb_ctrl+'.ballStartLift', 30)
        pm.setAttr(lower_limb_ctrl+'.toeStartStraight', 60)
        pm.setAttr(lower_limb_ctrl+'.tilt', 0)
        pm.setAttr(lower_limb_ctrl+'.heelSpin', 0)
        pm.setAttr(lower_limb_ctrl+'.toeSpin', 0)
        pm.setAttr(lower_limb_ctrl+'.toeSpin', 0)
        pm.setAttr(lower_limb_ctrl+'.toeRoll', 0)
        pm.setAttr(lower_limb_ctrl+'.toeWiggle', 0)

        xform_end_limb_rot = pm.getAttr(end_limb_snap_jnt + '.rotateX')
        pm.setAttr('%s.toeWiggle' % (end_limb_ctrl),(-1*xform_end_limb_rot))

    # query position and rotation
    xform_upper_limb_rot = pm.xform(upper_limb_snap_jnt, ws=1, q=1, ro=1)
    xform_low_limb_rot = pm.xform(lower_limb_snap_jnt, ws=1, q=1, ro=1)
    xform_upper_limb_pos = pm.xform(upper_limb_snap_jnt, ws=1, q=1, t=1)
    xform_middle_limb_pos = pm.xform(middle_limb_snap_jnt, ws=1, q=1, t=1)
    xform_low_limb_pos = pm.xform(lower_limb_snap_jnt, ws=1, q=1, t=1)

    # set position and rotation
    pm.xform(upper_limb_ctrl, ws=1, ro=(xform_upper_limb_rot[0], xform_upper_limb_rot[1], xform_upper_limb_rot[2]))
    pm.xform(lower_limb_ctrl, ws=1, ro=(xform_low_limb_rot[0], xform_low_limb_rot[1], xform_low_limb_rot[2]))
    pm.xform(upper_limb_ctrl, ws=1, t=(xform_upper_limb_pos[0], xform_upper_limb_pos[1], xform_upper_limb_pos[2]))
    pm.xform(lower_limb_ctrl, ws=1, t=(xform_low_limb_pos[0], xform_low_limb_pos[1], xform_low_limb_pos[2]))

    # for pole vector position
    up_joint_position = pm.xform(upper_limb_snap_jnt, q=1, ws=1, t=1)
    mid_joint_position = pm.xform(middle_limb_snap_jnt, q=1, ws=1, t=1)
    low_joint_position = pm.xform(lower_limb_snap_jnt, q=1, ws=1, t=1)

    get_poleVector_position = get_pole_vector_position(up_joint_position, mid_joint_position, low_joint_position)
    pm.move(get_poleVector_position.x, get_poleVector_position.y, get_poleVector_position.z, polevector_limb_ctrl)

    # get attribute value of middle_ref_joint and lower_ref_joint
    value_axis_middle_jnt = pm.getAttr('%s.%s' % (value_axis_aim_middle_jnt, axis_towards))
    value_axis_lower_jnt = pm.getAttr('%s.%s' % (value_axis_aim_lower_jnt, axis_towards))

    # calculate for stretching and snapping the pole vector controller
    total_value_default = value_axis_middle_jnt + value_axis_lower_jnt
    current_value_axis_towards_middle_jnt = pm.getAttr('%s.%s' % (middle_limb_snap_jnt, axis_towards))
    current_value_axis_towards_lower_jnt = pm.getAttr('%s.%s' % (lower_limb_snap_jnt, axis_towards))
    total_current_value = current_value_axis_towards_middle_jnt + current_value_axis_towards_lower_jnt

    # negative position (right)
    if current_value_axis_towards_middle_jnt < 0:
        if abs(total_current_value+total_value_default) > 0.01:
            pm.setAttr(lower_limb_ctrl+'.ikSnap', 1)
            pm.xform(polevector_limb_ctrl, ws=1, t=(xform_middle_limb_pos[0], xform_middle_limb_pos[1],
                                                    xform_middle_limb_pos[2]))
    # positive position (left)
    else:
        if abs(total_current_value-total_value_default) > 0.01:
            pm.setAttr(lower_limb_ctrl+'.ikSnap', 1)
            pm.xform(polevector_limb_ctrl, ws=1, t=(xform_middle_limb_pos[0], xform_middle_limb_pos[1],
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
