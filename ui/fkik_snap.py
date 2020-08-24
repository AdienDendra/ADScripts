"""
FkIk Snap script.
Stable on any version of Autodesk Maya.
Script description :
    This script purposes to match Fk/Ik task.
Instruction to use:
    You may go to this link for have more detail >>
    project.adiendendra.com/snap_fkik

Author:   Adien Dendra
Contact:  adien.dendra@gmail.com | hello@adiendendra.com
Date:     17 / 08 / 2020
Version:  1.0

"""

import maya.OpenMaya as om
import pymel.core as pm

layout = 265
percentage = 0.01 * layout


def ad_snap_fkik_ui():
    adien_snap_fkIk = 'AD_SnapFkIk'
    pm.window(adien_snap_fkIk, exists=True)

    if pm.window(adien_snap_fkIk, exists=True):
        pm.deleteUI(adien_snap_fkIk)

    with pm.window(adien_snap_fkIk, title='AD Fk/Ik Snap', width=layout + 10, height=150):
        with pm.columnLayout(rs=5, co=('both', 5), adj=True):
            pm.text(l='Select Leg/Arm Ctrl Setup:')
            pm.button(label='To Fk', width=layout, height=40, backgroundColor=[0.46, 0.86, 0.46],
                      command=pm.Callback(ad_ik_to_fk))
            pm.button(label='To Ik', width=layout, height=40, backgroundColor=[0.86, 0.46, 0.46],
                      command=pm.Callback(ad_fk_to_ik))
            with pm.rowLayout(nc=2, cw2=(32 * percentage, 32 * percentage),
                              cl2=('left', 'center'),
                              columnAttach=[(1, 'both', 1 * percentage), (2, 'both', 1 * percentage)],
                              adj=True):
                pm.text(l='Adien Dendra | 08/2020 | Ver. 1.0')
                pm.text(l='<a href="http://projects.adiendendra.com/">detail to use>> </a>', hl=True)
            pm.separator(h=2, st="single")

    pm.showWindow()


def ad_ik_to_fk():
    fkik_ctrl_select = pm.ls(sl=1)
    fk_ik_attr_name = pm.getAttr(fkik_ctrl_select[0] +'.'+ 'Fk_Ik_Attr_Name')
    value_fk_attr = pm.getAttr(fkik_ctrl_select[0] +'.'+ 'Fk_Value_On')

    if pm.objExists(fkik_ctrl_select[0] +'.'+ 'Upper_Limb_Joint'):
        # condition of controller
        getattr_ctrl = pm.getAttr(fkik_ctrl_select[0] + '.' + fk_ik_attr_name)
        if getattr_ctrl == 0:
            return fkik_ctrl_select[0]
        else:
            upper_limb_jnt = pm.listConnections(fkik_ctrl_select[0] +'.'+ 'Upper_Limb_Joint')[0]
            middle_limb_jnt = pm.listConnections(fkik_ctrl_select[0] +'.'+ 'Middle_Limb_Joint')[0]
            lower_limb_jnt = pm.listConnections(fkik_ctrl_select[0] +'.'+ 'Lower_Limb_Joint')[0]
            upper_limb_fk_ctrl = pm.listConnections(fkik_ctrl_select[0] +'.'+ 'Upper_Limb_Fk_Ctrl')[0]
            middle_limb_fk_ctrl = pm.listConnections(fkik_ctrl_select[0] +'.'+ 'Middle_Limb_Fk_Ctrl')[0]
            lower_limb_fk_ctrl = pm.listConnections(fkik_ctrl_select[0] +'.'+ 'Lower_Limb_Fk_Ctrl')[0]
            fk_ik_arm_ctrl = pm.listConnections(fkik_ctrl_select[0] +'.'+ 'FkIk_Arm_Setup_Controller', s=1)
            fk_ik_leg_ctrl = pm.listConnections(fkik_ctrl_select[0] +'.'+ 'FkIk_Leg_Setup_Controller', s=1)

            # run snap for arm
            if fk_ik_arm_ctrl:
                ad_ik_to_fk_setup(upper_limb_jnt=upper_limb_jnt, middle_limb_jnt=middle_limb_jnt,
                                  lower_limb_jnt=lower_limb_jnt, middle_limb_ctrl=middle_limb_fk_ctrl,
                                  lower_limb_ctrl=lower_limb_fk_ctrl, upper_limb_ctrl=upper_limb_fk_ctrl
                                  )
            # run snap for leg
            if fk_ik_leg_ctrl:
                end_limb_jnt = pm.listConnections(fkik_ctrl_select[0] +'.'+ 'End_Limb_Joint')[0]
                end_limb_fk_ctrl = pm.listConnections(fkik_ctrl_select[0] +'.'+ 'End_Limb_Fk_Ctrl')[0]

                ad_ik_to_fk_setup(upper_limb_jnt=upper_limb_jnt, middle_limb_jnt=middle_limb_jnt,
                                  lower_limb_jnt=lower_limb_jnt, middle_limb_ctrl=middle_limb_fk_ctrl,
                                  lower_limb_ctrl=lower_limb_fk_ctrl, upper_limb_ctrl=upper_limb_fk_ctrl,
                                  end_limb_jnt=end_limb_jnt, end_limb_ctrl=end_limb_fk_ctrl,
                                  leg=True)

            pm.setAttr(fkik_ctrl_select[0] + '.' + fk_ik_attr_name, value_fk_attr)

    else:
        pm.error('Select arm or leg setup controller for snapping to Fk!')


def ad_fk_to_ik():
    # listing fk ik setup selection
    fkik_ctrl_select = pm.ls(sl=1)
    fk_ik_attr_name = pm.getAttr(fkik_ctrl_select[0] +'.'+ 'Fk_Ik_Attr_Name')
    value_ik_attr = pm.getAttr(fkik_ctrl_select[0] +'.'+ 'Ik_Value_On')

    if pm.objExists(fkik_ctrl_select[0] +'.'+ 'Upper_Limb_Joint'):
        # condition of controller
        getattr_ctrl = pm.getAttr(fkik_ctrl_select[0] + '.' + fk_ik_attr_name)
        if getattr_ctrl == 1:
            return fkik_ctrl_select[0]
        else:
            upper_limb_jnt = pm.listConnections(fkik_ctrl_select[0] +'.'+ 'Upper_Limb_Joint')[0]
            middle_limb_jnt = pm.listConnections(fkik_ctrl_select[0] +'.'+ 'Middle_Limb_Joint')[0]
            lower_limb_jnt = pm.listConnections(fkik_ctrl_select[0] +'.'+ 'Lower_Limb_Joint')[0]
            poleVector_ctrl = pm.listConnections(fkik_ctrl_select[0] +'.'+ 'Pole_Vector_Ik_Ctrl')[0]
            lower_limb_ik_ctrl = pm.listConnections(fkik_ctrl_select[0] +'.'+ 'Lower_Limb_Ik_Ctrl')[0]
            upper_limb_ik_ctrl = pm.listConnections(fkik_ctrl_select[0] +'.'+ 'Upper_Limb_Ik_Ctrl')[0]
            aim_axis = pm.getAttr(fkik_ctrl_select[0] +'.'+ 'Aim_Axis')
            middle_aim_axis_value = pm.getAttr(fkik_ctrl_select[0] +'.'+ 'Middle_Translate_Aim_Joint')
            lower_aim_axis_value = pm.getAttr(fkik_ctrl_select[0] +'.'+ 'Lower_Translate_Aim_Joint')
            fk_ik_arm_ctrl = pm.listConnections(fkik_ctrl_select[0] +'.'+ 'FkIk_Arm_Setup_Controller', s=1)
            fk_ik_leg_ctrl = pm.listConnections(fkik_ctrl_select[0] +'.'+ 'FkIk_Leg_Setup_Controller', s=1)
            ik_snap_ctrl_name = pm.getAttr(fkik_ctrl_select[0] + '.' + 'Ik_Snap_Ctrl_Name')
            ik_snap_attr_name = pm.getAttr(fkik_ctrl_select[0] + '.' + 'Ik_Snap_Attr_Name')
            ik_snap_on = pm.getAttr(fkik_ctrl_select[0] + '.' + 'Ik_Snap_On')

            print (ik_snap_ctrl_name, ik_snap_attr_name, ik_snap_on)

            # run for snap arm
            if fk_ik_arm_ctrl:
                ad_fk_to_ik_setup(upper_limb_jnt=upper_limb_jnt, middle_limb_jnt=middle_limb_jnt,
                                  lower_limb_jnt=lower_limb_jnt, polevector_limb_ctrl=poleVector_ctrl,
                                  lower_limb_ctrl=lower_limb_ik_ctrl, upper_limb_ctrl=upper_limb_ik_ctrl,
                                  value_axis_aim_middle=middle_aim_axis_value,
                                  value_axis_aim_lower=lower_aim_axis_value,
                                  aim_axis=aim_axis, fkik_setup_controller=fkik_ctrl_select,
                                  ik_snap_ctrl_name=ik_snap_ctrl_name,
                                  ik_snap_attr_name=ik_snap_attr_name,
                                  ik_snap_on= ik_snap_on
                                  )
            # run for snap leg
            if fk_ik_leg_ctrl:
                end_limb_jnt = pm.listConnections(fkik_ctrl_select[0] +'.'+ 'End_Limb_Joint')[0]

                ad_fk_to_ik_setup(upper_limb_jnt=upper_limb_jnt, middle_limb_jnt=middle_limb_jnt,
                                  lower_limb_jnt=lower_limb_jnt, polevector_limb_ctrl=poleVector_ctrl,
                                  lower_limb_ctrl=lower_limb_ik_ctrl, upper_limb_ctrl=upper_limb_ik_ctrl,
                                  value_axis_aim_middle=middle_aim_axis_value,
                                  value_axis_aim_lower=lower_aim_axis_value,
                                  aim_axis=aim_axis, fkik_setup_controller=fkik_ctrl_select,
                                  ik_snap_ctrl_name=ik_snap_ctrl_name,
                                  ik_snap_attr_name=ik_snap_attr_name,
                                  ik_snap_on=ik_snap_on,
                                  end_limb_jnt=end_limb_jnt, leg=True)

            pm.setAttr(fkik_ctrl_select[0] + '.' + fk_ik_attr_name, value_ik_attr)
    else:
        pm.error('Select arm or leg setup controller for snapping to Ik!')


def ad_ik_to_fk_setup(upper_limb_jnt, middle_limb_jnt, lower_limb_jnt,
                      middle_limb_ctrl, lower_limb_ctrl, upper_limb_ctrl,
                      end_limb_jnt=None, end_limb_ctrl=None, leg=None):
    # query world position
    xform_upper_limb_rot = pm.xform(upper_limb_jnt, ws=1, q=1, ro=1)
    xform_middle_limb_rot = pm.xform(middle_limb_jnt, ws=1, q=1, ro=1)
    xform_low_limb_rot = pm.xform(lower_limb_jnt, ws=1, q=1, ro=1)
    xform_upper_limb_pos = pm.xform(upper_limb_jnt, ws=1, q=1, t=1)
    xform_middle_limb_pos = pm.xform(middle_limb_jnt, ws=1, q=1, t=1)
    xform_low_limb_pos = pm.xform(lower_limb_jnt, ws=1, q=1, t=1)

    # set the position
    pm.xform(upper_limb_ctrl, ws=1, ro=(xform_upper_limb_rot[0], xform_upper_limb_rot[1], xform_upper_limb_rot[2]))
    pm.xform(middle_limb_ctrl, ws=1, ro=(xform_middle_limb_rot[0], xform_middle_limb_rot[1], xform_middle_limb_rot[2]))
    pm.xform(lower_limb_ctrl, ws=1, ro=(xform_low_limb_rot[0], xform_low_limb_rot[1], xform_low_limb_rot[2]))
    pm.xform(upper_limb_ctrl, ws=1, t=(xform_upper_limb_pos[0], xform_upper_limb_pos[1], xform_upper_limb_pos[2]))
    pm.xform(middle_limb_ctrl, ws=1, t=(xform_middle_limb_pos[0], xform_middle_limb_pos[1], xform_middle_limb_pos[2]))
    pm.xform(lower_limb_ctrl, ws=1, t=(xform_low_limb_pos[0], xform_low_limb_pos[1], xform_low_limb_pos[2]))

    # exeption for the leg
    if leg:
        xform_end_limb_rot = pm.xform(end_limb_jnt, ws=1, q=1, ro=1)
        xform_end_limb_pos = pm.xform(end_limb_jnt, ws=1, q=1, t=1)
        pm.xform(end_limb_ctrl, ws=1, ro=(xform_end_limb_rot[0], xform_end_limb_rot[1], xform_end_limb_rot[2]))
        pm.xform(end_limb_ctrl, ws=1, t=(xform_end_limb_pos[0], xform_end_limb_pos[1], xform_end_limb_pos[2]))


def ad_fk_to_ik_setup(upper_limb_jnt, middle_limb_jnt, lower_limb_jnt,
                      polevector_limb_ctrl, lower_limb_ctrl, upper_limb_ctrl,
                      value_axis_aim_middle,
                      value_axis_aim_lower, fkik_setup_controller,
                      aim_axis, ik_snap_ctrl_name,
                      ik_snap_attr_name,
                      ik_snap_on,
                      end_limb_jnt=None, leg=None
                      ):
    # set to default
    selection = fkik_setup_controller[0]
    list_attribute_additional = pm.listAttr(selection)
    if filter(lambda x: '_DOTIK_AT_' in x or '_DOTIK_VA_' in x, list_attribute_additional):
        filtering_attr = filter(lambda x: '_DOTIK_AT_' in x, list_attribute_additional)
        filtering_value = filter(lambda x: '_DOTIK_VA_' in x, list_attribute_additional)
        for item_attr, item_value in zip (filtering_attr, filtering_value):
            get_item_attr = pm.getAttr('%s.%s' % (selection, item_attr))
            get_value_attr = pm.getAttr('%s.%s' % (selection, item_value))
            replace_dot_attr = item_attr.replace('_DOTIK_AT_', '.')
            pm.setAttr('%s%s' % (get_item_attr, replace_dot_attr), get_value_attr)

    if leg:
        if not pm.objExists(fkik_setup_controller[0] +'.'+ 'End_Limb_Ik_Ctrl'):
            xform_end_limb_rot = pm.getAttr(end_limb_jnt + '.' + (fkik_setup_controller[0] +'.'+ 'Rotation_Wiggle'))
            if fkik_setup_controller[0] + '.Reverse_Wiggle_Value':
                pm.setAttr('%s.%s' % ((fkik_setup_controller[0] +'.'+ 'Ik_Toe_Wiggle_Ctrl',
                                       (fkik_setup_controller[0] +'.'+ 'Ik_Toe_Wiggle_Attr_Name'))),
                           (-1 * xform_end_limb_rot))
            else:
                pm.setAttr('%s.%s' % ((fkik_setup_controller[0] +'.'+ 'Ik_Toe_Wiggle_Ctrl',
                                       (fkik_setup_controller[0] +'.'+ 'Ik_Toe_Wiggle_Attr_Name'))),
                           (xform_end_limb_rot))
        else:
            xform_end_limb_pos = pm.xform(end_limb_jnt, ws=1, q=1, t=1)
            xform_end_limb_rot = pm.xform(end_limb_jnt, ws=1, q=1, ro=1)

            pm.xform((fkik_setup_controller[0] +'.'+ 'End_Limb_Ik_Ctrl'), ws=1,
                     ro=(xform_end_limb_rot[0], xform_end_limb_rot[1], xform_end_limb_rot[2]))
            pm.xform((fkik_setup_controller[0] +'.'+ 'End_Limb_Ik_Ctrl'), ws=1,
                     t=(xform_end_limb_pos[0], xform_end_limb_pos[1], xform_end_limb_pos[2]))

    # query position and rotation
    xform_upper_limb_rot = pm.xform(upper_limb_jnt, ws=1, q=1, ro=1)
    xform_low_limb_rot = pm.xform(lower_limb_jnt, ws=1, q=1, ro=1)
    xform_upper_limb_pos = pm.xform(upper_limb_jnt, ws=1, q=1, t=1)
    xform_middle_limb_pos = pm.xform(middle_limb_jnt, ws=1, q=1, t=1)
    xform_low_limb_pos = pm.xform(lower_limb_jnt, ws=1, q=1, t=1)

    # set position and rotation
    pm.xform(upper_limb_ctrl, ws=1, ro=(xform_upper_limb_rot[0], xform_upper_limb_rot[1], xform_upper_limb_rot[2]))
    pm.xform(lower_limb_ctrl, ws=1, ro=(xform_low_limb_rot[0], xform_low_limb_rot[1], xform_low_limb_rot[2]))
    pm.xform(upper_limb_ctrl, ws=1, t=(xform_upper_limb_pos[0], xform_upper_limb_pos[1], xform_upper_limb_pos[2]))
    pm.xform(lower_limb_ctrl, ws=1, t=(xform_low_limb_pos[0], xform_low_limb_pos[1], xform_low_limb_pos[2]))

    # for pole vector position
    up_joint_position = pm.xform(upper_limb_jnt, q=1, ws=1, t=1)
    mid_joint_position = pm.xform(middle_limb_jnt, q=1, ws=1, t=1)
    low_joint_position = pm.xform(lower_limb_jnt, q=1, ws=1, t=1)

    get_poleVector_position = ad_get_pole_vector_position(up_joint_position, mid_joint_position, low_joint_position)
    pm.move(get_poleVector_position.x, get_poleVector_position.y, get_poleVector_position.z, polevector_limb_ctrl)

    # calculate for stretching and snapping the pole vector controller
    total_value_default = value_axis_aim_middle + value_axis_aim_lower
    current_value_axis_towards_middle_jnt = pm.getAttr('%s.%s' % (middle_limb_jnt, aim_axis))
    current_value_axis_towards_lower_jnt = pm.getAttr('%s.%s' % (lower_limb_jnt, aim_axis))
    total_current_value = current_value_axis_towards_middle_jnt + current_value_axis_towards_lower_jnt

    # negative position (right)
    if current_value_axis_towards_middle_jnt < 0:
        if abs(total_current_value + total_value_default) > 0.01:
            ad_ik_snap_set_on(polevector_limb_ctrl, xform_middle_limb_pos, ik_snap_ctrl_name, ik_snap_attr_name, ik_snap_on)

    # positive position (left)
    else:
        if abs(total_current_value - total_value_default) > 0.01:
            ad_ik_snap_set_on(polevector_limb_ctrl, xform_middle_limb_pos, ik_snap_ctrl_name, ik_snap_attr_name, ik_snap_on)


def ad_ik_snap_set_on(polevector_limb_ctrl, xform_middle_limb_pos, ik_snap_ctrl_name,ik_snap_attr_name,
                      ik_snap_on):

    pm.setAttr('%s.%s' % (ik_snap_ctrl_name, ik_snap_attr_name), ik_snap_on)
    pm.xform(polevector_limb_ctrl, ws=1, t=(xform_middle_limb_pos[0], xform_middle_limb_pos[1],
                                            xform_middle_limb_pos[2]))


def ad_get_pole_vector_position(root_pos, mid_pos, end_pos):
    root_jnt_vector = om.MVector(root_pos[0], root_pos[1], root_pos[2])
    mid_jnt_vector = om.MVector(mid_pos[0], mid_pos[1], mid_pos[2])
    end_jnt_vector = om.MVector(end_pos[0], end_pos[1], end_pos[2])

    line = (end_jnt_vector - root_jnt_vector)
    point = (mid_jnt_vector - root_jnt_vector)

    scale_value = (line * point) / (line * line)
    projection_vector = line * scale_value + root_jnt_vector

    pole_vector_position = (mid_jnt_vector - projection_vector).normal() + mid_jnt_vector

    return pole_vector_position
