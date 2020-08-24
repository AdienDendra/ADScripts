"""
FkIk Setup tool by Adien Dendra | 2020.
Stable on any version of Autodesk Maya.
Script description :
    This script purposes to setup for match Fk/Ik task.
Instruction to use:
    You may go to this link for have more detail >>
    project.adiendendra.com/setup_fkik

Author:   Adien Dendra
Contact: adien.dendra@gmail.com | hello@adiendendra.com
Date:     17 / 08 / 2020
Version:   1.0

"""

from functools import partial

import pymel.core as pm

layout = 600
percentage = 0.01 * layout
on_selector = 0


def ad_setup_fkik_ui():
    adien_snap_fkIk = 'AD_SnapSetupFkIk'
    pm.window(adien_snap_fkIk, exists=True)
    if pm.window(adien_snap_fkIk, exists=True):
        pm.deleteUI(adien_snap_fkIk)
    with pm.window(adien_snap_fkIk, title='AD Fk/Ik Snap Setup', width=600, height=800):
        with pm.scrollLayout('scroll'):
            with pm.columnLayout(rowSpacing=1 * percentage, w=layout, co=('both', 1 * percentage), adj=1):
                with pm.frameLayout(collapsable=True, l='Select Controller', mh=5):
                    with pm.rowColumnLayout('fkIk_controller_layout', nc=2, rowSpacing=(2, 1 * percentage),
                                            co=(1 * percentage, 'both', 1 * percentage),
                                            cw=[(1, 5 * percentage), (2, 93 * percentage)], ca=True):
                        direction_control = pm.radioCollection()
                        pm.radioButton(label='', cc=partial(ad_enabling_disabling_ui,
                                                            ['FkIk_Arm_Setup_Controller',
                                                             'ik_ball_rotation_layout',
                                                             'ik_ball_layout']))
                        ad_defining_object_text_field(define_object='FkIk_Arm_Setup_Controller',
                                                      label="Fk/Ik Arm Setup Controller:",
                                                      add_feature=True, enable=False)

                        direction1 = pm.radioButton(label='',
                                                    cc=partial(ad_enabling_disabling_ui, ['FkIk_Leg_Setup_Controller',
                                                                                          'endlimb_fk_ctrl_layout',
                                                                                          'endlimb_joint_ctrl_layout',
                                                                                          'endlimb_ik_ctrl_layout',
                                                                                          'endlimb_ik_ctrl']))

                        ad_defining_object_text_field(define_object='FkIk_Leg_Setup_Controller',
                                                      label="Fk/Ik Leg Setup Controller:",
                                                      add_feature=True)
                pm.separator(h=5, st="in", w=layout)
                with pm.frameLayout(collapsable=True, l='Define Objects', mh=5):
                    ad_defining_object_text_field(define_object='Upper_Limb_Joint', label="Upper Limb Joint:")
                    ad_defining_object_text_field(define_object='Middle_Limb_Joint', label="Middle Limb Joint:")
                    ad_defining_object_text_field(define_object='Lower_Limb_Joint', label="Lower Limb Joint:")
                    with pm.rowColumnLayout('endlimb_joint_ctrl_layout', nc=1, rowSpacing=(1, 1 * percentage),
                                            co=(1 * percentage, 'both', 1 * percentage), cw=[(2, 98 * percentage)]):
                        ad_defining_object_text_field(define_object='End_Limb_Joint', label="End Limb Joint:",
                                                      enable=False)

                    ad_defining_object_text_field(define_object='Upper_Limb_Fk_Ctrl', label="Upper Limb Fk Ctrl:")
                    ad_defining_object_text_field(define_object='Middle_Limb_Fk_Ctrl', label="Middle Limb Fk Ctrl:")
                    ad_defining_object_text_field(define_object='Lower_Limb_Fk_Ctrl', label="Lower Limb Fk Ctrl:")
                    with pm.rowColumnLayout('endlimb_fk_ctrl_layout', nc=1, rowSpacing=(1, 1 * percentage),
                                            co=(1 * percentage, 'both', 1 * percentage), cw=[(2, 98 * percentage)]):
                        ad_defining_object_text_field(define_object='End_Limb_Fk_Ctrl', label="End Limb Fk Ctrl:",
                                                      enable=False)

                    with pm.rowColumnLayout(nc=2, rowSpacing=(2, 1 * percentage),
                                            co=(1 * percentage, 'both', 1 * percentage),
                                            cw=[(1, 5 * percentage), (2, 93 * percentage)]):
                        pm.checkBox(label='', cc=partial(ad_enabling_disabling_ui, ['Upper_Limb_Ik_Ctrl']), value=True)
                        ad_defining_object_text_field(define_object='Upper_Limb_Ik_Ctrl', label="Upper Limb Ik Ctrl:",
                                                      add_feature=True)
                    ad_defining_object_text_field(define_object='Pole_Vector_Ik_Ctrl', label="Pole Vector Ik Ctrl:")
                    ad_defining_object_text_field(define_object='Lower_Limb_Ik_Ctrl', label="Lower Limb Ik Ctrl:")

                    with pm.rowColumnLayout('endlimb_ik_ctrl_layout', nc=2, rowSpacing=(2, 1 * percentage),
                                            co=(1 * percentage, 'both', 1 * percentage),
                                            cw=[(1, 5 * percentage), (2, 93 * percentage)]):
                        pm.checkBox('endlimb_ik_ctrl', label='', cc=partial(ad_enabling_disabling_ui,
                                                                            ['End_Limb_Ik_Ctrl', 'ik_ball_layout',
                                                                             'ik_ball_rotation_layout']),
                                    )
                        pm.checkBox('endlimb_ik_ctrl', edit=True, value=False)

                        ad_defining_object_text_field(define_object='End_Limb_Ik_Ctrl', label="End Limb Ik Ctrl:",
                                                      add_feature=True, enable=False)

                    with pm.rowLayout(nc=1, cw1=(35 * percentage), cl1=('center'),
                                      columnAttach=[(1, 'both', 2 * percentage)]
                                      ):
                        pm.button(bgc=(1, 1, 0), l="Clear All Define Objects!",
                                  c=partial(ad_clearing_all_text_field, 'Upper_Limb_Joint',
                                            'Middle_Limb_Joint', 'Lower_Limb_Joint', 'End_Limb_Joint',
                                            'Upper_Limb_Fk_Ctrl',
                                            'Middle_Limb_Fk_Ctrl', 'Lower_Limb_Fk_Ctrl', 'End_Limb_Fk_Ctrl',
                                            'Upper_Limb_Ik_Ctrl',
                                            'Pole_Vector_Ik_Ctrl', 'Lower_Limb_Ik_Ctrl', 'End_Limb_Ik_Ctrl'))

                pm.separator(h=5, st="in", w=layout)
                # radio button translate
                with pm.frameLayout(collapsable=True, l='Additional Setup', mh=5):
                    with pm.rowLayout(nc=2, columnAttach=[(1, 'right', 0), (2, 'left', 1 * percentage)],
                                      cw2=(30 * percentage, 64.8)):
                        pm.text('Does Translate Fk ctrl locked?:')
                        pm.checkBox('Translate_Fk', label='')
                    with pm.rowLayout(nc=4, columnAttach=[(1, 'right', 0), (2, 'left', 1 * percentage),
                                                          (3, 'left', 1 * percentage), (4, 'left', 1 * percentage)],
                                      cw4=(30 * percentage, 16 * percentage, 16 * percentage, 20 * percentage)):
                        pm.text('Limb Aim Axis:')
                        direction_control_translate = pm.radioCollection()
                        direction_translateX = pm.radioButton(label='Translate X',
                                                              onCommand=lambda x: ad_on_selection_button(1))
                        pm.radioButton(label='Translate Y', onCommand=lambda x: ad_on_selection_button(2))
                        pm.radioButton(label='Translate Z', onCommand=lambda x: ad_on_selection_button(3))
                        pm.radioCollection(direction_control_translate, edit=True, select=direction_translateX)

                    with pm.rowLayout(nc=3, columnAttach=[(1, 'right', 0), (2, 'left', 1 * percentage),
                                                          (3, 'left', 1 * percentage)],
                                      cw3=(40 * percentage, 20 * percentage, 20 * percentage)):
                        # pm.text("Fk/Ik Controller Attr Name:")
                        pm.textFieldGrp('Fk_Ik_Attr_Name', l="Fk/Ik Controller Attr Name:",
                                        cw2=(30 * percentage, 10 * percentage), tx='FkIk',
                                        cat=[(1, 'right', 2), (2, 'both', 5)],

                                        )
                        pm.floatFieldGrp('Fk_Value_On', l="Fk Value On:", cal=(1, "left"),
                                         cw2=(11 * percentage, 5 * percentage), precision=1)
                        pm.floatFieldGrp('Ik_Value_On', l="Ik Value On:", cal=(1, "left"),
                                         cw2=(11 * percentage, 5 * percentage), precision=1, value1=1)

                    with pm.rowLayout(nc=4, columnAttach=[(1, 'right', 0), (2, 'left', 1 * percentage),
                                                          (3, 'left', 1 * percentage), (4, 'left', 1 * percentage),
                                                          ],
                                      cw4=(52 * percentage, 15 * percentage, 12 * percentage, 12 * percentage
                                           )):

                        # pm.text('Ik_Snap', l="Elbow/Knee Snap Ctrl Name:")

                        pm.textFieldButtonGrp('Ik_Snap_Ctrl_Name', l="Elbow/Knee Snap Ctrl Name:", cal=(1, "right"),
                              cw3=(30 * percentage, 16 * percentage, 6 * percentage),
                              cat=[(1, 'right', 1), (2, 'both', 5)],
                              bl="<<",
                              bc=partial(ad_adding_object_sel_to_textfield, 'Ik_Snap_Ctrl_Name'),
                                               tx='wristIk_ctrl')

                        pm.textFieldGrp('Ik_Snap_Attr_Name', l='Attr:', cw2=(4 * percentage, 9 * percentage),
                                        tx='iKSnap')
                        pm.floatFieldGrp('Ik_Snap_Off', l="Off:", cal=(1, "right"),
                                         cw2=(4 * percentage, 5 * percentage), precision=1)
                        pm.floatFieldGrp('Ik_Snap_On', l="On:", cal=(1, "right"),
                                         cw2=(4 * percentage, 5 * percentage), precision=1, value1=1)

                    pm.separator(h=5, st="in", w=layout)

                    with pm.rowLayout('ik_ball_layout', nc=3,
                                      columnAttach=[(1, 'right', 0), (2, 'left', 1 * percentage)],
                                      cw2=(52 * percentage, 20 * percentage)):
                        # pm.text('Ik_Ball_Toe_Wiggle_Name', l="Ik Ball Toe Wiggle Name:")
                        pm.textFieldButtonGrp('Ik_Toe_Wiggle_Ctrl', l="Ik Ball Toe Wiggle Name:",
                                              cal=(1, "right"),
                                              cw3=(30 * percentage, 16 * percentage, 6 * percentage),
                                              cat=[(1, 'right', 1), (2, 'both', 5)],
                                              bl="<<",
                                              bc=partial(ad_adding_object_sel_to_textfield, 'Ik_Toe_Wiggle_Ctrl'),
                                              tx='wristIk_ctrl')
                        pm.textFieldGrp('Ik_Toe_Wiggle_Attr_Name', l='Attr Toe Wiggle:',
                                        cw2=(14 * percentage, 12 * percentage),
                                        tx='toeWiggle')
                    with pm.rowLayout('ik_ball_rotation_layout', nc=5,
                                      columnAttach=[(1, 'right', 0), (2, 'left', 1 * percentage),
                                                    (3, 'left', 1 * percentage), (4, 'left', 1 * percentage),
                                                    (5, 'left', 1 * percentage)],
                                      cw5=(30 * percentage, 16 * percentage, 16 * percentage, 18 * percentage,
                                           16 * percentage)):
                        pm.text('Rotation_Toe_Wiggle', l="Rotation Toe Wiggle:")
                        radio_collection_rotate_ball_ik_ctrl = pm.radioCollection()
                        ball_ik_ctrl_rotateX = pm.radioButton(label='Rotate X',
                                                              onCommand=lambda x: ad_on_selection_button(1))
                        pm.radioButton(label='Rotate Y', onCommand=lambda x: ad_on_selection_button(2))
                        pm.radioButton(label='Rotate Z', onCommand=lambda x: ad_on_selection_button(3))
                        pm.radioCollection(radio_collection_rotate_ball_ik_ctrl, edit=True, select=ball_ik_ctrl_rotateX)
                        pm.checkBox('Reverse_Wiggle_Value', l='Reverse')

                    pm.radioCollection(direction_control, edit=True, select=direction1)

                pm.separator(h=5, st="in", w=layout)

                with pm.frameLayout(collapsable=True, l='Additional Attributes', mh=5):
                    with pm.rowLayout(nc=2, cw2=(49 * percentage, 49 * percentage), cl2=('center', 'center'),
                                      columnAttach=[(1, 'both', 2 * percentage), (2, 'both', 2 * percentage)]
                                      ):
                        pm.button(l="Add Object And Set Default Attribute Value", bgc=(0, 0, 0.5),
                                  c=ad_additional_attr_adding)

                        # create button to delete last pair of text fields
                        pm.button(l="Delete", bgc=(0.5, 0, 0), c=ad_additional_attr_deleting)
                        pm.setParent(u=True)
                        pm.rowColumnLayout("row_column_add_object", nc=5,
                                           cw=[(1, 37 * percentage), (2, 22 * percentage), (3, 25 * percentage),
                                               (4, 7 * percentage), (5, 7 * percentage)])
                        pm.setParent(u=True)

                pm.separator(h=5, st="in", w=layout)
                with pm.frameLayout(collapsable=True, l='Setup', mh=5):
                    pm.text(l='Select Leg/Arm Ctrl Setup :')
                    with pm.rowLayout(nc=2, cw2=(49 * percentage, 49 * percentage), cl2=('center', 'center'),
                                      columnAttach=[(1, 'both', 2 * percentage), (2, 'both', 2 * percentage)]
                                      ):
                        pm.button("run_setup", bgc=(0, 0.5, 0), l="Run Setup",
                                  c=partial(ad_run_setup))
                        pm.button("delete_setup", bgc=(0.5, 0, 0), l="Delete Setup",
                                  c=partial(ad_delete_setup))

                pm.separator(h=10, st="in", w=layout)
                with pm.rowLayout(nc=3, cw3=(32 * percentage, 32 * percentage, 32 * percentage),
                                  cl3=('left', 'center', 'right'),
                                  columnAttach=[(1, 'both', 2 * percentage), (2, 'both', 2 * percentage),
                                                (3, 'both', 2 * percentage)]):
                    pm.text(l='Adien Dendra | 08/2020', al='left')
                    pm.text(l='<a href="http://projects.adiendendra.com/">find out how to use it! >> </a>', hl=True,
                            al='center')
                    pm.text(l='Version 1.0', al='right')

                pm.separator(h=1, st="none", w=layout)
            pm.setParent(u=True)
    pm.showWindow()


# def action_checkbox_button(*args):
#     if on_selector == 1:
#         value = 1
#     else:
#         value = 0
#
#     return value
# def ad_action_checkbox(selector, *args):
#     row=[]
#     if selector == 1:
#         row = 1
#     elif selector == 0:
#         row = 0
#     else:
#         pass
#     return row


def ad_action_translate_rotate_radio_button(object, *args):
    """
    query object with value on shape selector status

    """
    value_translate, axis_translate, value_rotate, axis_rotate = [], [], [], []
    if on_selector == 1:
        axis_translate = 'translateX'
        axis_rotate = 'rotateX'
        value_translate = pm.getAttr('%s.%s' % (object, axis_translate))
        value_rotate = pm.getAttr('%s.%s' % (object, axis_rotate))
    elif on_selector == 2:
        axis_translate = 'translateY'
        axis_rotate = 'rotateY'
        value_translate = pm.getAttr('%s.%s' % (object, axis_translate))
        value_rotate = pm.getAttr('%s.%s' % (object, axis_rotate))
    elif on_selector == 3:
        axis_translate = 'translateZ'
        axis_rotate = 'rotateZ'
        value_translate = pm.getAttr('%s.%s' % (object, axis_translate))
        value_rotate = pm.getAttr('%s.%s' % (object, axis_rotate))
    else:
        pass

    return value_translate, axis_translate, value_rotate, axis_rotate


def ad_on_selection_button(on):
    """
    Save the current shape selection
    into global variable

    """
    global on_selector
    on_selector = on


def ad_defining_object_text_field(define_object, label, add_feature=False, *args, **kwargs):
    if not add_feature:
        pm.textFieldButtonGrp(define_object, label=label, cal=(1, "right"),
                              cw3=(30 * percentage, 54 * percentage, 15 * percentage),
                              cat=[(1, 'right', 2), (2, 'both', 2), (3, 'left', 2)],
                              bl="Get Object",
                              bc=partial(ad_adding_object_sel_to_textfield, define_object))
    else:
        pm.textFieldButtonGrp(define_object, label=label, cal=(1, "right"),
                              cw3=(25 * percentage, 54 * percentage, 15 * percentage),
                              cat=[(1, 'right', 2), (2, 'both', 2), (3, 'left', 2)],
                              bl="Get Object",
                              bc=partial(ad_adding_object_sel_to_textfield, define_object), **kwargs)

def ad_enabling_disabling_ui(object, value, *args):
    for item in object:
        objectType = pm.objectTypeUI(item)
        if objectType == 'rowGroupLayout':
            pm.textFieldButtonGrp(item, edit=True, enable=value, tx='')
        elif objectType == 'rowColumnLayout':
            pm.rowColumnLayout(item, edit=True, enable=value)
        elif objectType == 'checkBox':
            pm.checkBox(item, edit=True, enable=value)
        elif objectType == 'rowLayout':
            if value:
                pm.rowLayout(item, edit=True, enable=False)
            else:
                pm.rowLayout(item, edit=True, enable=True)
        else:
            pass


def ad_clearing_all_text_field(*args):
    for object in args:
        if object:
            pm.textFieldButtonGrp(object, edit=True, tx='')
        else:
            pass


def ad_additional_attr_adding(*args):
    child_array = pm.rowColumnLayout("row_column_add_object", q=True, ca=True)
    if child_array:
        current_number = len(child_array) / 5 + 1
        current_default_value = "default_value" + str(current_number)
        current_attr = "attribute" + str(current_number)
        current_object = "object" + str(current_number)
        current_collection_fk_ik = 'fk_ik_choose' + str(current_number)
        current_fk = "fk_add_setup" + str(current_number)
        current_ik = "ik_add_setup" + str(current_number)

    else:
        current_default_value = "default_value1"
        current_attr = "attribute1"
        current_object = "object1"
        current_collection_fk_ik = 'fk_ik_choose1'
        current_fk = "fk_add_setup1"
        current_ik = "ik_add_setup1"

    pm.textFieldButtonGrp(current_object, l="Object:", cal=(1, "right"),
                          cw3=(8 * percentage, 22 * percentage, 7 * percentage), p="row_column_add_object",
                          cat=[(3, 'left', 2)],
                          bl="<<",
                          bc=partial(ad_adding_object_sel_to_textfield, current_object))
    pm.textFieldGrp(current_attr, l="Attr:", cal=(1, "right"), cw2=(6 * percentage, 14 * percentage),
                    p="row_column_add_object")
    pm.floatFieldGrp(current_default_value, l="Set Default Value:", cal=(1, "right"),
                     cw2=(16 * percentage, 6 * percentage),
                     p="row_column_add_object", precision=1)

    fk_ik_choose_additional = pm.radioCollection(current_collection_fk_ik, p='row_column_add_object')
    pm.radioButton(current_fk, label='Fk', p='row_column_add_object')
    ik_choose_additional = pm.radioButton(current_ik, label='Ik', p='row_column_add_object')
    pm.radioCollection(fk_ik_choose_additional, edit=True, select=ik_choose_additional)


def ad_additional_attr_deleting(*args):
    """
    delete add_text_field_grp
    """
    child_array = pm.rowColumnLayout("row_column_add_object", q=True, ca=True)

    if child_array:
        child_array_num = len(child_array)
        delete_default_value = "default_value" + str(child_array_num / 5)
        delete_attr = "attribute" + str(child_array_num / 5)
        delete_object = "object" + str(child_array_num / 5)
        delete_fk = "fk_add_setup" + str(child_array_num / 5)
        delete_ik = "ik_add_setup" + str(child_array_num / 5)
        delete_collection_fk_ik = "fk_ik_choose" + str(child_array_num / 5)

        pm.deleteUI(delete_default_value)
        pm.deleteUI(delete_attr)
        pm.deleteUI(delete_object)
        pm.deleteUI(delete_fk)
        pm.deleteUI(delete_ik)
        pm.deleteUI(delete_collection_fk_ik)

    else:
        pass


def ad_adding_object_sel_to_textfield(text_input, *args):
    """
    select and add object
    """
    sel = pm.ls(sl=True, l=True, tr=True)
    if len(sel) == 1:
        object_selection = sel[0]
        pm.textFieldButtonGrp(text_input, e=True, tx=object_selection)
    else:
        pm.error("please select one object!")


def ad_query_define_textfield_object(object_define, *args):
    text = []
    if (pm.textFieldButtonGrp(object_define, q=True, en=True)):
        if (pm.textFieldButtonGrp(object_define, q=True, tx=True)):
            text = pm.textFieldButtonGrp(object_define, q=True, tx=True)
            if pm.ls(text):
                text = pm.textFieldButtonGrp(object_define, q=True, tx=True)
            else:
                pm.error('%s has wrong input object name.' % object_define, "There is no object with name '%s'!" % text)

        else:
            pm.error('%s can not be empty!' % object_define)

    else:
        pass
    return text, object_define


def ad_additional_setup(Middle_Limb_Joint_Define, Lower_Limb_Joint_Define, End_Limb_Joint_Define, fkIk_setup_ctrl):
    if pm.rowLayout('ik_ball_layout', q=True, enable=True):
        # ball_toe_wiggle_name = pm.textField('Ik_Toe_Wiggle_Ctrl', q=True, tx=True)
        # pm.addAttr(fkIk_setup_ctrl[0], ln='Ik_Toe_Wiggle_Ctrl', dt='string')
        # pm.setAttr('%s.Ik_Toe_Wiggle_Ctrl' % fkIk_setup_ctrl[0], ball_toe_wiggle_name, l=True)

        toe_wiggle_attr_name = pm.textFieldGrp('Ik_Toe_Wiggle_Attr_Name', q=True, tx=True)
        pm.addAttr(fkIk_setup_ctrl[0], ln='Ik_Toe_Wiggle_Attr_Name', dt='string')
        pm.setAttr('%s.Ik_Toe_Wiggle_Attr_Name' % fkIk_setup_ctrl[0], toe_wiggle_attr_name, l=True)

    if pm.rowLayout('ik_ball_rotation_layout', q=True, enable=True):
        pm.addAttr(fkIk_setup_ctrl[0], ln='Rotation_Wiggle', dt='string')
        pm.setAttr('%s.Rotation_Wiggle' % fkIk_setup_ctrl[0],
                   ad_action_translate_rotate_radio_button(End_Limb_Joint_Define[0])[3], l=True)

        reverse_wiggle_value = pm.checkBox('Reverse_Wiggle_Value', q=True, value=True)
        pm.addAttr(fkIk_setup_ctrl[0], ln='Reverse_Wiggle_Value', at='bool')
        pm.setAttr('%s.Reverse_Wiggle_Value' % fkIk_setup_ctrl[0], reverse_wiggle_value, l=True)

    translate_fk_ctrl = pm.checkBox('Translate_Fk', q=True, value=True)
    pm.addAttr(fkIk_setup_ctrl[0], ln='Translate_Fk_Ctrl_Exists', at='bool')
    pm.setAttr('%s.Translate_Fk_Ctrl_Exists' % fkIk_setup_ctrl[0], translate_fk_ctrl, l=True)

    fk_ik_attr_name = pm.textFieldGrp('Fk_Ik_Attr_Name', q=True, tx=True)
    pm.addAttr(fkIk_setup_ctrl[0], ln='Fk_Ik_Attr_Name', dt='string')
    pm.setAttr('%s.Fk_Ik_Attr_Name' % fkIk_setup_ctrl[0], fk_ik_attr_name, l=True)

    value_fk_attr = pm.floatFieldGrp('Fk_Value_On', q=True, value1=True)
    pm.addAttr(fkIk_setup_ctrl[0], ln='Fk_Value_On', at='float')
    pm.setAttr('%s.Fk_Value_On' % fkIk_setup_ctrl[0], value_fk_attr, l=True)

    value_ik_attr = pm.floatFieldGrp('Ik_Value_On', q=True, value1=True)
    pm.addAttr(fkIk_setup_ctrl[0], ln='Ik_Value_On', at='float')
    pm.setAttr('%s.Ik_Value_On' % fkIk_setup_ctrl[0], value_ik_attr, l=True)

    # ik_snap_ctrl_name = pm.textField('Ik_Snap_Ctrl_Name', q=True, tx=True)
    # pm.addAttr(fkIk_setup_ctrl[0], ln='Ik_Snap_Ctrl_Name', dt='string')
    # pm.setAttr('%s.Ik_Snap_Ctrl_Name' % fkIk_setup_ctrl[0], ik_snap_ctrl_name, l=True)

    ik_snap_ctrl_attr = pm.textFieldGrp('Ik_Snap_Attr_Name', q=True, tx=True)
    pm.addAttr(fkIk_setup_ctrl[0], ln='Ik_Snap_Attr_Name', dt='string')
    pm.setAttr('%s.Ik_Snap_Attr_Name' % fkIk_setup_ctrl[0], ik_snap_ctrl_attr, l=True)

    ik_snap_min_value = pm.floatFieldGrp('Ik_Snap_Off', q=True, value1=True)
    pm.addAttr(fkIk_setup_ctrl[0], ln='Ik_Snap_Off', at='float')
    pm.setAttr('%s.Ik_Snap_Off' % fkIk_setup_ctrl[0], ik_snap_min_value, l=True)

    ik_snap_max_value = pm.floatFieldGrp('Ik_Snap_On', q=True, value1=True)
    pm.addAttr(fkIk_setup_ctrl[0], ln='Ik_Snap_On', at='float')
    pm.setAttr('%s.Ik_Snap_On' % fkIk_setup_ctrl[0], ik_snap_max_value, l=True)

    pm.addAttr(fkIk_setup_ctrl[0], ln='Middle_Translate_Aim_Joint', at='float')
    pm.setAttr('%s.Middle_Translate_Aim_Joint' % fkIk_setup_ctrl[0],
               ad_action_translate_rotate_radio_button(Middle_Limb_Joint_Define[0])[0], l=True)

    pm.addAttr(fkIk_setup_ctrl[0], ln='Lower_Translate_Aim_Joint', at='float')
    pm.setAttr('%s.Lower_Translate_Aim_Joint' % fkIk_setup_ctrl[0],
               ad_action_translate_rotate_radio_button(Lower_Limb_Joint_Define[0])[0], l=True)

    pm.addAttr(fkIk_setup_ctrl[0], ln='Aim_Axis', dt='string')
    pm.setAttr('%s.Aim_Axis' % fkIk_setup_ctrl[0],
               ad_action_translate_rotate_radio_button(Lower_Limb_Joint_Define[0])[1], l=True)


def ad_run_setup(*args):
    # query objects
    FkIk_Arm_Setup_Controller = ad_query_define_textfield_object('FkIk_Arm_Setup_Controller')
    FkIk_Leg_Setup_Controller = ad_query_define_textfield_object('FkIk_Leg_Setup_Controller')
    Upper_Limb_Joint_Define = ad_query_define_textfield_object('Upper_Limb_Joint')
    Middle_Limb_Joint_Define = ad_query_define_textfield_object('Middle_Limb_Joint')
    Lower_Limb_Joint_Define = ad_query_define_textfield_object('Lower_Limb_Joint')
    End_Limb_Joint_Define = ad_query_define_textfield_object('End_Limb_Joint')
    Upper_Limb_Fk_Ctrl_Define = ad_query_define_textfield_object('Upper_Limb_Fk_Ctrl')
    Middle_Limb_Fk_Ctrl_Define = ad_query_define_textfield_object('Middle_Limb_Fk_Ctrl')
    Lower_Limb_Fk_Ctrl_Define = ad_query_define_textfield_object('Lower_Limb_Fk_Ctrl')
    End_Limb_Fk_Ctrl_Define = ad_query_define_textfield_object('End_Limb_Fk_Ctrl')
    Upper_Limb_Ik_Ctrl_Define = ad_query_define_textfield_object('Upper_Limb_Ik_Ctrl')
    Pole_Vector_Ik_Ctrl_Define = ad_query_define_textfield_object('Pole_Vector_Ik_Ctrl')
    Lower_Limb_Ik_Ctrl_Define = ad_query_define_textfield_object('Lower_Limb_Ik_Ctrl')
    End_Limb_Ik_Ctrl_Define = ad_query_define_textfield_object('End_Limb_Ik_Ctrl')
    Ik_Snap_Ctrl_Name_Define = ad_query_define_textfield_object('Ik_Snap_Ctrl_Name')

    label_list = [FkIk_Arm_Setup_Controller[1], FkIk_Leg_Setup_Controller[1],
                  Upper_Limb_Joint_Define[1], Middle_Limb_Joint_Define[1], Lower_Limb_Joint_Define[1],
                  Upper_Limb_Fk_Ctrl_Define[1], Middle_Limb_Fk_Ctrl_Define[1], Lower_Limb_Fk_Ctrl_Define[1],
                  Upper_Limb_Ik_Ctrl_Define[1], Pole_Vector_Ik_Ctrl_Define[1], Lower_Limb_Ik_Ctrl_Define[1],
                  Ik_Snap_Ctrl_Name_Define[1],
                  End_Limb_Joint_Define[1], End_Limb_Fk_Ctrl_Define[1], End_Limb_Ik_Ctrl_Define[1],
                  ]
    object_list = [FkIk_Arm_Setup_Controller[0], FkIk_Leg_Setup_Controller[0],
                   Upper_Limb_Joint_Define[0], Middle_Limb_Joint_Define[0], Lower_Limb_Joint_Define[0],
                   Upper_Limb_Fk_Ctrl_Define[0], Middle_Limb_Fk_Ctrl_Define[0], Lower_Limb_Fk_Ctrl_Define[0],
                   Upper_Limb_Ik_Ctrl_Define[0], Pole_Vector_Ik_Ctrl_Define[0], Lower_Limb_Ik_Ctrl_Define[0],
                   Ik_Snap_Ctrl_Name_Define[0],
                   End_Limb_Joint_Define[0], End_Limb_Fk_Ctrl_Define[0], End_Limb_Ik_Ctrl_Define[0],
                   ]

    if pm.rowLayout('ik_ball_layout', q=True, enable=True):
        Ik_Toe_Wiggle_Ctrl_Define_1 = ad_query_define_textfield_object('Ik_Toe_Wiggle_Ctrl')[1]
        Ik_Toe_Wiggle_Ctrl_Define_0 = ad_query_define_textfield_object('Ik_Toe_Wiggle_Ctrl')[0]

        label_list.append(Ik_Toe_Wiggle_Ctrl_Define_1)
        object_list.append(Ik_Toe_Wiggle_Ctrl_Define_0)

    # addding attribute
    if pm.objExists('%s.%s' % (FkIk_Arm_Setup_Controller[0], Upper_Limb_Joint_Define[1])):
        pm.warning('please delete the setup first!')
    else:
        if (pm.textFieldButtonGrp(FkIk_Arm_Setup_Controller[1], q=True, en=True)):
            for item_label, object_label in zip(label_list[:12], object_list[:12]):
                pm.addAttr(FkIk_Arm_Setup_Controller[0], ln=item_label, at='message')
                if pm.textFieldButtonGrp(item_label, q=True, en=True):
                    pm.connectAttr(object_label + '.message', '%s.%s' % (FkIk_Arm_Setup_Controller[0], item_label))

            ad_additional_setup(Middle_Limb_Joint_Define, Lower_Limb_Joint_Define, End_Limb_Joint_Define,
                                fkIk_setup_ctrl=FkIk_Arm_Setup_Controller)

        else:
            for item_label, object_label in zip(label_list, object_list):
                pm.addAttr(FkIk_Leg_Setup_Controller[0], ln=item_label, at='message')
                if pm.textFieldButtonGrp(item_label, q=True, en=True):
                    pm.connectAttr(object_label + '.message', '%s.%s' % (FkIk_Leg_Setup_Controller[0], item_label))

            ad_additional_setup(Middle_Limb_Joint_Define, Lower_Limb_Joint_Define, End_Limb_Joint_Define,
                                fkIk_setup_ctrl=FkIk_Leg_Setup_Controller)

    if pm.rowColumnLayout("row_column_add_object", q=True, ca=True):
        child_define_object = pm.rowColumnLayout("row_column_add_object", q=True, ca=True)
        number_of_object = (len(child_define_object) / 5)
        if number_of_object:
            for current_number in range(1, number_of_object + 1):
                current_object = "object" + str(current_number)
                current_attr = "attribute" + str(current_number)
                current_default_value = "default_value" + str(current_number)
                current_collection_fk_ik = 'fk_ik_choose' + str(current_number)
                current_fk = "fk_add_setup" + str(current_number)
                current_ik = "ik_add_setup" + str(current_number)

                object = pm.textFieldButtonGrp(current_object, q=True, tx=True)
                attribute = pm.textFieldGrp(current_attr, q=True, tx=True)
                default_value = pm.floatFieldGrp(current_default_value, q=True, value1=True)
                radio_collection = pm.radioCollection(current_collection_fk_ik, q=True, select=True)

                if radio_collection == current_fk:
                    object_compile_name = '_DOTFK_AT_' + attribute
                    value_compile_name = '_DOTFK_VA_' + attribute

                else:
                    object_compile_name = '_DOTIK_AT_' + attribute
                    value_compile_name = '_DOTIK_VA_' + attribute


                # attribute_compile_name = object + '_DOT_' + attribute
                if object and attribute:
                    if (pm.textFieldButtonGrp(FkIk_Arm_Setup_Controller[1], q=True, en=True)):
                        if not pm.objExists(FkIk_Arm_Setup_Controller[0] + '.' + object_compile_name):
                            pm.addAttr(FkIk_Arm_Setup_Controller[0], ln=object_compile_name, at='message')
                            pm.connectAttr(object + '.message', '%s.%s' % (FkIk_Arm_Setup_Controller[0],
                                                                           object_compile_name))

                            pm.addAttr(FkIk_Arm_Setup_Controller[0], ln=value_compile_name, at='float')
                            pm.setAttr('%s.%s' % (FkIk_Arm_Setup_Controller[0], value_compile_name), default_value,
                                       l=True)
                        else:
                            pm.warning("Line # " + str(number_of_object) + " same attribute! skipped this attribute")

                    else:
                        if not pm.objExists(FkIk_Arm_Setup_Controller[0] + '.' + object_compile_name):
                            pm.addAttr(FkIk_Leg_Setup_Controller[0], ln=object_compile_name, at='message')
                            pm.connectAttr(object + '.message', '%s.%s' % (FkIk_Leg_Setup_Controller[0],
                                                                           object_compile_name))

                            pm.addAttr(FkIk_Leg_Setup_Controller[0], ln=value_compile_name, at='float')
                            pm.setAttr('%s.%s' % (FkIk_Leg_Setup_Controller[0], value_compile_name), default_value,
                                       l=True)
                        else:
                            pm.warning("Line # " + str(number_of_object) + " same attribute! skipped this attribute")

                else:
                    pm.warning("Line # " + str(number_of_object) + " is empty! skipped this attribute")


def ad_delete_setup(*args):
    sel = pm.ls(sl=1)
    if sel:
        object_text_field_list = ['FkIk_Arm_Setup_Controller', 'FkIk_Leg_Setup_Controller',
                                  'Upper_Limb_Joint', 'Middle_Limb_Joint', 'Lower_Limb_Joint',
                                  'Upper_Limb_Fk_Ctrl', 'Middle_Limb_Fk_Ctrl', 'Lower_Limb_Fk_Ctrl',
                                  'Upper_Limb_Ik_Ctrl', 'Pole_Vector_Ik_Ctrl', 'Lower_Limb_Ik_Ctrl',
                                  'End_Limb_Joint', 'End_Limb_Fk_Ctrl', 'End_Limb_Ik_Ctrl',
                                  'Middle_Translate_Aim_Joint', 'Ik_Snap_Ctrl_Name', 'Ik_Snap_Attr_Name',
                                  'Ik_Snap_Off', 'Ik_Snap_On',
                                  'Lower_Translate_Aim_Joint', 'Aim_Axis', 'Translate_Fk_Ctrl_Exists',
                                  'Fk_Ik_Attr_Name',
                                  'Fk_Value_On', 'Ik_Value_On', 'Ik_Toe_Wiggle_Ctrl', 'Ik_Toe_Wiggle_Attr_Name',
                                  'Rotation_Wiggle',
                                  'Reverse_Wiggle_Value']

        if pm.objExists(sel[0] + '.' + 'FkIk_Arm_Setup_Controller'):
            for item in object_text_field_list:
                if pm.attributeQuery(item, n=sel[0], ex=True):
                    list_attr = pm.listAttr('%s.%s' % (sel[0], item), l=True)
                    if list_attr:
                        pm.setAttr('%s.%s' % (sel[0], list_attr[0]), l=False)
                    pm.deleteAttr('%s.%s' % (sel[0], item))

            list_attribute_additional = pm.listAttr(sel[0])
            if filter(lambda x: '_DOTFK_AT_' in x or '_DOTFK_VA_' in x or '_DOTIK_AT_' in x or '_DOTIK_VA_' in x, list_attribute_additional):
                filtering = filter(lambda x: '_DOTFK_AT_' in x or '_DOTFK_VA_' in x or '_DOTIK_AT_' in x or '_DOTIK_VA_' in x, list_attribute_additional)
                for item in filtering:
                    list_attr_layout = pm.listAttr('%s.%s' % (sel[0], item), l=True)
                    if list_attr_layout:
                        pm.setAttr('%s.%s' % (sel[0], list_attr_layout[0]), l=False)
                    pm.deleteAttr('%s.%s' % (sel[0], item))
        else:
            pm.warning(
                'There is no setup added! Either you have selected wrong controller object or the setup already deleted!')
    else:
        pm.warning('Please select either arm or leg setup to clean up the setup!')
