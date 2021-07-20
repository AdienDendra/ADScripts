"""
DESCRIPTION:
    This file is a GUI for customizing creating controllers. The user can handle
    flexibility the input and call the functionality from ad_controller_lib.py

USAGE:
    You may go to this link to have more detail >>
    http://projects.adiendendra.com/ad-universal-fkik-setup-tutorial/

AUTHOR:
    Adien Dendra

CONTACT:
    adprojects.animation@gmail.com | hello@adiendendra.com

VERSION:
    1.0 - 20 July 2021 - Initial Release

LICENSE:
    Copyright (C) 2021 Adien Dendra - hello@adiendendra.com>
    This is commercial license can not be copied and/or
    distributed without the express permission of Adien Dendra

"""

from functools import partial

import maya.OpenMaya as om
import pymel.core as pm

import ad_controller_lib as al

reload(al)

layout = 400
percentage = 0.01 * layout
on_selector = 0
previous_value = 0

# UI
def ad_show_ui():
    adien_controller = 'AD_Controller'
    shape_controller = 'Shape_Controller'
    pm.window(adien_controller, exists=True)
    if pm.window(adien_controller, exists=True):
        pm.deleteUI(adien_controller)
        if pm.window(shape_controller, exists=True):
            pm.deleteUI(shape_controller)
    # WINDOW LAYOUT
    with pm.window(adien_controller, title='AD Controller', width=layout, height=200):
        # TAB LAYOUT
        with pm.tabLayout('tab', width=layout * 1.027, height=200):
            # LAYOUT CREATE CONTROLLER
            with pm.scrollLayout('Create Controller', p='tab'):
                with pm.columnLayout('Create_Controller_Column', w=layout, co=('both', 1 * percentage), adj=1):
                    # NAMING PREFIX SUFFIX FRAME
                    with pm.frameLayout(collapsable=True, l='Naming', mh=1):
                        with pm.rowColumnLayout(nc=8, rowAttach=(2, 'top', 0),
                                                cs=[(3, 1 * percentage), (5, 1 * percentage),
                                                    (7, 1 * percentage)],
                                                cw=[(1, 12 * percentage), (2, 7 * percentage), (3, 13 * percentage),
                                                    (4, 20 * percentage), (5, 15 * percentage), (6, 9.5 * percentage),
                                                    (8, 8 * percentage)]):
                            # prefix 1 text field
                            pm.checkBox('Prefix_1', label='Prfx 1:', cc=partial(ad_cc_enabling_disabling_ui,
                                                                                ['Prefix_1_Text'], 'L_'), value=False)
                            al.ad_lib_defining_object_text_field(define_object='Prefix_1_Text', tx='L_', enable=False)

                            # name text field
                            pm.checkBox('Name_CheckBox', label='Name:', cc=partial(ad_cc_enabling_disabling_ui,
                                                                                   ['Name_Text'], ''), value=False)
                            al.ad_lib_defining_object_text_field(define_object='Name_Text', enable=False)
                            # prefix 2 text field
                            pm.checkBox('Prefix_2', label='Prefix 2:',
                                        cc=partial(ad_cc_enabling_disabling_ui, ['Prefix_2_Text'], 'LFT'), value=False)
                            al.ad_lib_defining_object_text_field(define_object='Prefix_2_Text', tx='LFT', enable=False)

                            # suffix text field
                            pm.text('Suffix:')
                            pm.textField('Suffix_Main', tx='ctrl')

                    # CONNECTION FRAME
                    with pm.frameLayout(collapsable=True, l='Connection', mh=1):
                        with pm.rowLayout('Connection', nc=3,
                                          cw3=(18.5 * percentage, 32 * percentage, 40 * percentage),
                                          cl3=('right', 'right', 'right'),
                                          columnAttach=[(1, 'both', 0.5 * percentage), (2, 'both', 0.5 * percentage),
                                                        (3, 'both', 0.5 * percentage), ],
                                          rowAttach=[(1, 'top', 0), (3, 'top', 0)]):
                            pm.text('')
                            # constraint channel box
                            ad_cc_channelbox_constraint_connection()
                            # direct connection channel box
                            ad_cc_channelbox_direct_connection()

                        with pm.rowLayout(nc=3, cw3=(19 * percentage, 38 * percentage, 38 * percentage),
                                          cl3=('right', 'right', 'right'), columnAttach=[(2, 'both', 0.15 * percentage),
                                                                                         (3, 'both',
                                                                                          0.15 * percentage)]):
                            pm.text('')
                            # list connection button
                            pm.button("List_Connection", l="List Connection",
                                      c=partial(ad_cc_list_connection_button))

                            # create connection button
                            pm.button('Create_Connection', l="Create Connection",
                                      c=partial(ad_cc_connection_button))

                    # COLOR FRAME
                    with pm.frameLayout(collapsable=True, l='Color', mh=1):
                        with pm.rowLayout('Palette_Port', nc=2, cw2=(18.5 * percentage, 69 * percentage),
                                          cl2=('right', 'left'),
                                          columnAttach=[(1, 'both', 0.5 * percentage), (2, 'both', 0.5 * percentage)]):
                            pm.text('')
                            # color index palette
                            ad_cc_color_index()

                        with pm.rowLayout(nc=3, cw3=(19 * percentage, 38 * percentage, 38 * percentage),
                                          cl3=('right', 'right', 'right'), columnAttach=[(2, 'both', 0.15 * percentage),
                                                                                         (3, 'both',
                                                                                          0.15 * percentage)]):
                            pm.text(label='')
                            # reset color button
                            pm.button('Reset_Color', l="Reset Color", c=partial(ad_cc_reset_color_button))
                            # replace color button
                            pm.button("Replace_Color", l="Replace Color", c=partial(ad_cc_replace_color_button))

                    # CHANNEL FRAME
                    with pm.frameLayout(collapsable=True, l='Channel', mh=1):
                        with pm.rowLayout(nc=4,
                                          cw4=(18.5 * percentage, 32 * percentage, 27 * percentage, 22 * percentage),
                                          cl4=('right', 'left', 'left', 'left'),
                                          columnAttach=[(1, 'both', 0.5 * percentage), (2, 'both', 0.5 * percentage),
                                                        (3, 'both', 0.5 * percentage), (4, 'both', 0.5 * percentage), ],
                                          rowAttach=[(1, 'top', 0), (2, 'top', 0), (3, 'top', 0), (4, 'top', 0)]):
                            pm.text('')
                            # translation channel box
                            ad_cc_channelbox_translation()
                            # rotation channel box
                            ad_cc_channelbox_rotation()
                            # scale channel box
                            ad_cc_channelbox_scale()

                        with pm.rowLayout(nc=3, cw3=(19 * percentage, 38 * percentage, 38 * percentage),
                                          cl3=('right', 'right', 'right'), columnAttach=[(2, 'both', 0.15 * percentage),
                                                                                         (3, 'both',
                                                                                          0.15 * percentage)]):
                            pm.text(label='')
                            # hide unhide button
                            pm.button("Hide_Unhide_Channel", l="Hide/Unhide", c=partial(ad_cc_hide_unhide_button))
                            # lock unlock button
                            pm.button('Lock_Unlock_Channel', l="Lock/Unlock",
                                      c=partial(ad_cc_lock_unlock_button))

                    # RESIZE FRAME
                    with pm.frameLayout(collapsable=True, l='Resize', mh=1):
                        with pm.rowLayout(nc=2, cw2=(18.5 * percentage, 77 * percentage), cl2=('right', 'left'),
                                          columnAttach=[(1, 'both', 0.5 * percentage),
                                                        (2, 'both', 0.5 * percentage)], ):
                            pm.text('')
                            # controller resize slider
                            pm.floatSlider('Controller_Resize', min=0.7, value=1.0, max=1.3, step=0.1,
                                           dragCommand=partial(ad_cc_controller_resize_slider),
                                           changeCommand=partial(ad_cc_controller_resize_reset))
                        with pm.rowLayout(nc=2, cw2=(18.5 * percentage, 77 * percentage), cl2=('right', 'left'),
                                          columnAttach=[(1, 'both', 0), (2, 'both', 0)]):
                            pm.text('')
                            # select controller button
                            pm.button('Select_All_AD_Controller', l="Select All AD Controller",
                                      c=partial(ad_cc_select_all_ad_controller_button))

                    # GROUP AND SHAPE FRAME
                    with pm.frameLayout(collapsable=True, l='Group and Shape', mh=1):
                        with pm.rowColumnLayout(nc=3, cw=[(2, 56 * percentage)], cs=[(3, 1 * percentage)]):
                            pm.checkBox(label='Name List:',
                                        cc=partial(ad_cc_enabling_disabling_ui, ['Parent_Group_Name'],
                                                   'Main,Offset'),
                                        value=True)
                            # parent group text field
                            al.ad_lib_defining_object_text_field(define_object='Parent_Group_Name', tx='Main,Offset',
                                                                 enable=True
                                                                 )
                            # create group button
                            pm.button("Create_Grp_Select", l="Create Group", c=partial(ad_cc_group_button))

                        with pm.rowLayout(nc=2, cw2=(18.5 * percentage, 77 * percentage), cl2=('right', 'left'),
                                          columnAttach=[(1, 'both', 0 * percentage), (2, 'both', 0 * percentage)]):
                            pm.text('')
                            # icon text
                            with pm.rowColumnLayout(nc=9,
                                                    cs=[(2, 0.25 * percentage), (3, 0.25 * percentage),
                                                        (4, 0.25 * percentage), (5, 0.25 * percentage),
                                                        (6, 0.25 * percentage), (7, 0.25 * percentage),
                                                        (8, 0.25 * percentage)]
                                                    ):
                                icon_radio_control = pm.iconTextRadioCollection()
                                circle = pm.iconTextRadioButton(st='iconOnly', image='ad_icons/circle.png',
                                                                onCommand=lambda x: ad_cc_on_selection_ctrl_shape(1))
                                # locator
                                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/locator.png',
                                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(2))
                                # cube
                                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/cube.png',
                                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(3))
                                # circlehalf
                                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/circlehalf.png',
                                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(4))
                                # square
                                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/square.png',
                                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(5))
                                # joint
                                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/joint.png',
                                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(6))
                                # capsule
                                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/capsule.png',
                                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(7))
                                # stickcircle
                                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/stickcircle.png',
                                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(8))
                                # continues
                                pm.iconTextButton(st='iconOnly', hi='ad_icons/continue_hi.png',
                                                  image='ad_icons/continue.png',
                                                  c=partial(ad_cc_shape_controller_ui, circle))

                                pm.iconTextRadioCollection(icon_radio_control, edit=True, select=circle)

                        with pm.rowLayout(nc=2, cw2=(18 * percentage, 80 * percentage), cl2=('right', 'left'),
                                          columnAttach=[(1, 'both', 0.5 * percentage),
                                                        (2, 'both', 0.5 * percentage)]):
                            pm.text('')
                            with pm.rowLayout(nc=3, cw3=(25 * percentage, 25 * percentage, 25 * percentage),
                                              cl3=('center', 'center', 'center'),
                                              columnAttach=[(1, 'both', 0 * percentage),
                                                            (2, 'both', 0 * percentage),
                                                            (3, 'both', 0 * percentage)]):
                                # replace controller button
                                pm.button("Replace_Controller", l="Replace Ctrl",
                                          c=partial(ad_cc_replacing_controller_button))
                                # tag controller button
                                pm.button("Tag_as_AD_Controller", l="Tag as AD Ctrl",
                                          c=partial(ad_cc_tagging_untagging_button, True))
                                # untag controller button
                                pm.button('Untag_AD_Controller', l="Untag AD Ctrl",
                                          c=partial(ad_cc_tagging_untagging_button, False))

                    # ADDITIONAL FRAME
                    with pm.frameLayout(collapsable=True, l='Additional', mh=1):
                        with pm.columnLayout():
                            with pm.rowLayout(nc=2, cw2=(17.5 * percentage, 50 * percentage), cl2=('right', 'left'),
                                              columnAttach=[(1, 'both', 0.5 * percentage),
                                                            (2, 'both', 0.5 * percentage)]):
                                pm.text('')
                                with pm.columnLayout():
                                    with pm.rowColumnLayout(nc=2):
                                        # adding child check box
                                        pm.checkBox('Adding_Ctrl_Child', label='Add Child Ctrl:',
                                                    cc=partial(ad_cc_enabling_disabling_ui, ['Suffix_Child_Ctrl'],
                                                               'Child'),
                                                    value=False)
                                        pm.textField('Suffix_Child_Ctrl', enable=False, tx='Child')

                                    with pm.rowColumnLayout():
                                        # target visibility check box
                                        pm.checkBox('Target_Visibility', label='Add Attribute for Target Visibility',
                                                    value=False)
                                        # add pivot check box
                                        pm.checkBox('Add_Pivot_Ctrl', label='Add Pivot Controller', value=False,
                                                    enable=False)

                    # RUN FRAME
                    with pm.frameLayout(collapsable=True, l='Run', mh=3):
                        with pm.rowLayout(nc=2, cw2=(18.5 * percentage, 77 * percentage), cl2=('right', 'left'),
                                          columnAttach=[(1, 'both', 0), (2, 'both', 0)]):
                            pm.text(label='')
                            # create controller button
                            pm.button('Create_Controller', l="Create Controller With All Defined Above!",
                                      bgc=(0, 0.5, 0),
                                      c=partial(ad_cc_controller_button))

                pm.separator(h=10, st="in", w=layout)

                # link tutorial
                with pm.rowLayout(nc=3, cw3=(38 * percentage, 36 * percentage, 24 * percentage),
                                  cl3=('left', 'center', 'right'),
                                  columnAttach=[(1, 'both', 2 * percentage), (2, 'both', 2 * percentage),
                                                (3, 'both', 2 * percentage)]):
                    pm.text(l='Adien Dendra | 07/2021', al='left')
                    pm.text(
                        l='<a href="http://projects.adiendendra.com/ad-universal-fkik-setup-tutorial/">find out how to use it! >> </a>',
                        hl=True,
                        al='center')
                    pm.text(l='Version 1.0', al='right')

            # LAYOUT CONTROLLER UTILITES
            with pm.scrollLayout('Controller Utilities', p='tab'):
                with pm.columnLayout('Controller_Utilities_Column', w=layout, co=('both', 1 * percentage), adj=1):
                    with pm.frameLayout(collapsable=True, l='Rotate', mh=1):
                        with pm.rowLayout(nc=2, cw2=(18 * percentage, 77 * percentage), cl2=('right', 'left'),
                                          columnAttach=[(1, 'both', 0.5 * percentage), (2, 'both', 0.5 * percentage)]):
                            pm.text('Rotate:')
                            with pm.rowLayout(nc=4, cw4=(
                                    10 * percentage, 21.5 * percentage, 21.5 * percentage, 21.5 * percentage),
                                              cl4=('center', 'center', 'center', 'center'),
                                              columnAttach=[(1, 'both', 0 * percentage), (2, 'both', 0 * percentage),
                                                            (3, 'both', 0 * percentage), (4, 'both', 0 * percentage)]):
                                pm.intField('Degree_Rotate', value=90, min=-360, max=360)

                                pm.button("Rotate_X", l="X", c=partial(ad_cu_rotation_x_button), bgc=(0.5, 0, 0))
                                pm.button("Rotate_Y", l="Y", c=partial(ad_cu_rotation_y_button), bgc=(0, 0.5, 0))
                                pm.button('Rotate_Z', l="Z", c=partial(ad_cu_rotation_z_button), bgc=(0, 0, 0.5))

                    with pm.frameLayout(collapsable=True, l='Mirror', mh=1):
                        with pm.rowColumnLayout(nc=3,
                                                cw=[(1, 42 * percentage), (2, 12 * percentage), (3, 42 * percentage)],
                                                cal=[(1, 'center'), (2, 'center'), (3, 'center')],
                                                columnAttach=[(1, 'both', 0 * percentage), (2, 'both', 0 * percentage),
                                                              (3, 'both', 0 * percentage)]):
                            pm.text(label='From Prefix:')
                            pm.text(label='')
                            pm.text(label='To Prefix:')

                            pm.textFieldButtonGrp('From_Prefix', label='', cal=(1, "right"),
                                                  cw3=(10 * percentage, 13 * percentage, 7 * percentage), bl="<<",
                                                  columnAttach=[(1, 'both', 0 * percentage),
                                                                (2, 'both', 0 * percentage),
                                                                (3, 'both', 0 * percentage)], tx='L_',
                                                  bc=partial(ad_cu_object_sel_to_textfield_mirror, 'From_Prefix'))

                            pm.button("Swap", l="<<-->>",
                                      c=partial(ad_cu_swap_button))

                            pm.textFieldButtonGrp('To_Prefix', label='', cal=(1, "right"),
                                                  cw3=(10 * percentage, 13 * percentage, 7 * percentage),
                                                  columnAttach=[(1, 'both', 0 * percentage),
                                                                (2, 'both', 0 * percentage),
                                                                (3, 'both', 0 * percentage)], bl="<<", tx='R_',
                                                  bc=partial(ad_cu_object_sel_to_textfield_mirror, 'To_Prefix'))
                        with pm.rowLayout(nc=3, cw3=(31.6 * percentage, 31.6 * percentage, 31.6 * percentage),
                                          cl3=('center', 'center', 'center'),
                                          columnAttach=[(1, 'both', 0 * percentage), (2, 'both', 0 * percentage),
                                                        (3, 'both', 0 * percentage)]):
                            pm.button("Mirror_X", l="X",
                                      c=partial(ad_cu_mirror_button, 'x'), bgc=(0.5, 0, 0))
                            pm.button("Mirror_Y", l="Y",
                                      c=partial(ad_cu_mirror_button, 'y'), bgc=(0, 0.5, 0))
                            pm.button('Mirror_Z', l="Z",
                                      c=partial(ad_cu_mirror_button, 'z'), bgc=(0, 0, 0.5))

                    with pm.frameLayout(collapsable=True, l='Save/Load', mh=1):
                        with pm.columnLayout():
                            with pm.rowLayout(nc=1, cw=(1, 95 * percentage), cal=(1, 'right'),
                                              columnAttach=[(1, 'both', 0.25 * percentage), ], ):
                                pm.button('Select_All_AD_Controller', l="Select All AD Controller",
                                          c=partial(ad_cc_select_all_ad_controller_button), bgc=(0.0, 0.5, 0.0))

                            with pm.rowLayout(nc=2, cw2=(47.5 * percentage, 47.5 * percentage), cl2=('right', 'right'),
                                              columnAttach=[(1, 'both', 0.15 * percentage),
                                                            (2, 'both', 0.15 * percentage)]):
                                pm.button("Save", l="Save", c=partial(ad_cu_save_dialog), bgc=(0.5, 0.0, 0.0))
                                pm.button('Load', l="Load", c=partial(ad_cu_load_dialog), bgc=(0.0, 0.0, 0.5))

                pm.separator(h=10, st="in", w=layout)
                with pm.rowLayout(nc=3, cw3=(38 * percentage, 36 * percentage, 24 * percentage),
                                  cl3=('left', 'center', 'right'),
                                  columnAttach=[(1, 'both', 2 * percentage), (2, 'both', 2 * percentage),
                                                (3, 'both', 2 * percentage)]):
                    pm.text(l='Adien Dendra | 07/2021', al='left')
                    pm.text(
                        l='<a href="http://projects.adiendendra.com/ad-universal-fkik-setup-tutorial/">find out how to use it! >> </a>',
                        hl=True,
                        al='center')
                    pm.text(l='Version 1.0', al='right')
    pm.showWindow()


########################################################################################################################
#                                           CREATE CONTROLLER TAB FUNCTION
########################################################################################################################
####### CREATE CONTROLLER UI FUNCTION #######
# NAMING
def ad_cc_enabling_disabling_ui(object, tx, value, *args):
    # query for enabling and disabling layout
    for item in object:
        objectType = pm.objectTypeUI(item)
        if objectType == 'rowGroupLayout':
            pm.textFieldGrp(item, edit=True, enable=value, tx=tx)
        elif objectType == 'field':
            pm.textField(item, edit=True, enable=value, tx=tx)
        elif objectType == 'button':
            pm.button(item, edit=True, enable=value, tx=tx)
        else:
            pass


# CONNECTION
def ad_cc_list_connection_button(*args):
    list_object = pm.ls(sl=1)
    if list_object:
        al.ad_lib_list_connections_object(list_object)
    else:
        om.MGlobal_displayError('Select the minimum one object which has a connection!')


def ad_cc_connection_button(*args):
    list_controller = pm.ls(sl=1)
    if len(list_controller) < 2:
        om.MGlobal_displayError('Select minimum two objects!')
    else:
        instance_controller = list_controller.pop(0)
        for item in list_controller:
            al.ad_lib_connection(ctrl=instance_controller, target=item)


def ad_cc_channelbox_constraint_connection(*args):
    pm.columnLayout()
    pm.checkBox('Point_Cons', label='Point Constraint', value=False,
                cc=partial(ad_cc_connection_uncheck_translate_rotate_constraint,
                           ['Parent_Cons', 'Direct_Trans',
                            'Parent'], ['Add_Pivot_Ctrl'], 'Point_Cons'))
    pm.checkBox('Orient_Cons', label='Orient Constraint', value=False,
                cc=partial(ad_cc_connection_uncheck_translate_rotate_constraint,
                           ['Parent_Cons', 'Direct_Rot',
                            'Parent'], ['Add_Pivot_Ctrl'], 'Orient_Cons'))
    pm.checkBox('Scale_Cons', label='Scale Constraint', value=False,
                cc=partial(ad_cc_connection_uncheck_scale_constraint,
                           ['Direct_Scl', 'Parent'], 'Scale_Cons'))
    pm.checkBox('Parent_Cons', label='Parent Constraint', value=False,
                cc=partial(ad_cc_connection_uncheck_parent_constraint,
                           ['Point_Cons', 'Orient_Cons',
                            'Direct_Trans', 'Direct_Rot',
                            'Parent'], ['Add_Pivot_Ctrl'], 'Parent_Cons'))
    pm.setParent(u=True)


def ad_cc_channelbox_direct_connection(*args):
    pm.columnLayout()
    pm.checkBox('Direct_Trans', label='Direct Connect Translate', value=False,
                cc=partial(ad_cc_connection_uncheck_translate_rotate_constraint,
                           ['Parent_Cons', 'Point_Cons', 'Parent'], ['Add_Pivot_Ctrl'], 'Direct_Trans'))
    pm.checkBox('Direct_Rot', label='Direct Connect Rotate', value=False,
                cc=partial(ad_cc_connection_uncheck_translate_rotate_constraint,
                           ['Parent_Cons', 'Orient_Cons',
                            'Parent'], ['Add_Pivot_Ctrl'], 'Direct_Rot'))
    pm.checkBox('Direct_Scl', label='Direct Connect Scale', value=False,
                cc=partial(ad_cc_connection_uncheck_scale_constraint,
                           ['Scale_Cons', 'Parent'],
                           'Direct_Scl'))
    pm.checkBox('Parent', label='Parent', value=False, cc=partial(ad_cc_connection_uncheck_translate_rotate_constraint,
                                                                  ['Point_Cons', 'Orient_Cons', 'Direct_Trans',
                                                                   'Direct_Rot', 'Parent_Cons',
                                                                   'Direct_Scl', 'Scale_Cons'], ['Add_Pivot_Ctrl'],
                                                                  'Parent'))
    pm.setParent(u=True)


# COLOR
def ad_cc_color_index():
    MAX_OVERRIDE_COLORS = 32
    columns = MAX_OVERRIDE_COLORS / 2
    rows = 2
    cell_width = 19
    color_palette = pm.palettePort('Pallete', dimensions=(columns, rows), transparent=0, width=(columns * cell_width),
                                   height=(rows * cell_width), topDown=True, colorEditable=False)
    for index in range(1, MAX_OVERRIDE_COLORS):
        color_component = pm.colorIndex(index, q=True)
        pm.palettePort(color_palette, edit=True,
                       rgbValue=(index, color_component[0], color_component[1], color_component[2]))

    pm.palettePort(color_palette, edit=True, rgbValue=(0, 0.6, 0.6, 0.6))


def ad_cc_reset_color_button(*args):
    al.ad_lib_ctrl_color_list(0)
    pm.select(cl=True)


def ad_cc_replace_color_button(*args):
    al.ad_lib_ctrl_color_list(ad_cc_set_color())
    pm.select(cl=True)


# CHANNEL
def ad_cc_channelbox_translation(*args):
    pm.columnLayout()
    pm.checkBox('All_Trans', label='All Translation', value=False,
                cc=partial(ad_cc_checkbox_check_channel_translate, ['Trans_X', 'Trans_Y', 'Trans_Z']))
    pm.checkBox('Trans_X', label='Translate X', value=False,
                cc=partial(ad_cc_checkbox_uncheck_all_channel, ['Trans_X']))
    pm.checkBox('Trans_Y', label='Translate Y', value=False,
                cc=partial(ad_cc_checkbox_uncheck_all_channel, ['Trans_Y']))
    pm.checkBox('Trans_Z', label='Translate Z', value=False,
                cc=partial(ad_cc_checkbox_uncheck_all_channel, ['Trans_Z']))
    pm.checkBox('Visibility', label='Visibility', value=False)
    pm.setParent(u=True)


def ad_cc_channelbox_rotation(*args):
    pm.columnLayout()
    pm.checkBox('All_Rot', label='All Rotation', value=False,
                cc=partial(ad_cc_checkbox_check_channel_rotate, ['Rot_X', 'Rot_Y', 'Rot_Z']))
    pm.checkBox('Rot_X', label='Rotate X', value=False, cc=partial(ad_cc_checkbox_uncheck_all_channel, ['Rot_X']))
    pm.checkBox('Rot_Y', label='Rotate Y', value=False, cc=partial(ad_cc_checkbox_uncheck_all_channel, ['Rot_Y']))
    pm.checkBox('Rot_Z', label='Rotate Z', value=False, cc=partial(ad_cc_checkbox_uncheck_all_channel, ['Rot_Z']))
    pm.checkBox('User_Def', label='User Defined', value=False)

    pm.setParent(u=True)


def ad_cc_channelbox_scale(*args):
    pm.columnLayout()
    pm.checkBox('All_Scale', label='All Scale', value=False,
                cc=partial(ad_cc_checkbox_check_channel_scale, ['Scl_X', 'Scl_Y', 'Scl_Z']))
    pm.checkBox('Scl_X', label='Scale X', value=False, cc=partial(ad_cc_checkbox_uncheck_all_channel, ['Scl_X']))
    pm.checkBox('Scl_Y', label='Scale Y', value=False, cc=partial(ad_cc_checkbox_uncheck_all_channel, ['Scl_Y']))
    pm.checkBox('Scl_Z', label='Scale Z', value=False, cc=partial(ad_cc_checkbox_uncheck_all_channel, ['Scl_Z']))
    pm.setParent(u=True)


def ad_cc_hide_unhide_button(*args):
    selection = pm.ls(selection=True)
    if not selection:
        om.MGlobal.displayError("No objects selected")
        return False
    else:
        for item in selection:
            al.ad_lib_hide_unhide(ctrl=item)


def ad_cc_lock_unlock_button(*args):
    selection = pm.ls(selection=True)
    if not selection:
        om.MGlobal.displayError("No objects selected")
        return False
    else:
        for item in selection:
            al.ad_lib_lock_unlock(ctrl=item)


# RESIZE
def ad_cc_controller_resize_slider(*args):
    selection = pm.ls(selection=True)
    if not selection:
        om.MGlobal.displayWarning("No objects selected")
    else:
        for item in selection:
            shape_node = pm.listRelatives(item, s=True)[0]
            if pm.objectType(shape_node) == 'nurbsCurve':
                global previous_value
                current_value = pm.floatSlider('Controller_Resize', q=True, v=True)
                al.ad_lib_scaling_controller(item, current_value)
                previous_value = current_value
            else:
                om.MGlobal.displayError("Object type must be curve")
                return False


def ad_cc_select_all_ad_controller_button(*args):
    list_scene = pm.ls(type='transform')
    list_object = []
    for item in list_scene:
        try:
            shape_node = pm.listRelatives(item, s=True)[0]
            if pm.objectType(shape_node) == 'nurbsCurve':
                pm.listAttr(item + '.AD_Controller')
                attr_true = pm.getAttr(item + '.AD_Controller')
                if attr_true:
                    list_object.append(item)
                else:
                    pass
        except:
            pass

    pm.select(list_object)


# GROUP AND SHAPE
def ad_cc_group_button(*args):
    select = pm.ls(sl=1)
    # grouping controller
    if pm.textField('Parent_Group_Name', q=True, enable=True):
        for item in select:
            name = al.ad_lib_get_number_main_name(item)
            group = al.ad_lib_group_parent(groups=al.ad_lib_query_list_textfield_object('Parent_Group_Name')[0],
                                           name=name[1],
                                           suffix=al.ad_lib_get_suffix_main(item),
                                           prefix_number=name[0], prefix_2=al.ad_lib_prefix('Prefix_2_Text'))
            al.ad_lib_xform_position_rotation(origin=item, target=group[0])
            pm.parent(item, group[-1])
    else:
        pass


def ad_cc_shape_controller_ui(default, *args):
    shape_controller = 'Shape_Controller'
    pm.window(shape_controller, exists=True)
    if pm.window(shape_controller, exists=True):
        pm.deleteUI(shape_controller)
    with pm.window(shape_controller, title='AD Controller Shape'):
        with pm.columnLayout(co=('both', 1 * percentage), adj=1):
            pm.separator(h=7, st="in")
            with pm.rowColumnLayout(nc=10, rowOffset=[(1, 'top', 1), (2, 'top', 3), (3, 'top', 3)]):
                pm.iconTextRadioButton(default, edit=True, select=True)
                # circleplushalf
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/circleplushalf.png',
                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(9))
                # circleplus
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/circleplus.png',
                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(10))
                # stick2circle
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/stick2circle.png',
                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(11))
                # sticksquare
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/sticksquare.png',
                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(12))
                # stick2square
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/stick2square.png',
                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(13))
                # stickstar
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/stickstar.png',
                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(14))
                # circleplusarrow
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/circleplusarrow.png',
                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(15))
                # rectangle
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/rectangle.png',
                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(16))
                # arrow
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/arrow.png',
                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(17))
                # arrow3dflat
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/arrow3dflat.png',
                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(18))
                # arrow2halfcircular
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/arrow2halfcircular.png',
                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(19))
                # arrow2straight
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/arrow2straight.png',
                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(20))
                # arrow2flat
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/arrow2flat.png',
                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(21))
                # arrowhead
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/arrowhead.png',
                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(22))
                # arrow90deg
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/arrow90deg.png',
                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(23))
                # squareplus
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/squareplus.png',
                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(24))
                # jointplus
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/jointplus.png',
                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(25))
                # hand
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/hand.png',
                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(26))
                # arrowcircular
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/arrowcircular.png',
                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(27))
                # plus
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/plus.png',
                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(28))
                # pivot
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/pivot.png',
                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(29))
                # keys
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/keys.png',
                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(30))
                # pyramidcircle
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/pyramidcircle.png',
                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(31))
                # arrow4circular
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/arrow4circular.png',
                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(32))
                # eyes
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/eyes.png',
                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(33))
                # footstep
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/footstep.png',
                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(34))
                # half3dcircle
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/half3dcircle.png',
                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(35))
                # capsulecurve
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/capsulecurve.png',
                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(36))
                # arrow4straight
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/arrow4straight.png',
                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(37))
                # arrow3d
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/arrow3d.png',
                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(38))
                # pyramid
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/pyramid.png',
                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(39))
                # arrow3dcircular
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/arrow3dcircular.png',
                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(40))
                # cylinder
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/cylinder.png',
                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(41))
                # arrow2flathalf
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/arrow2flathalf.png',
                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(42))
                # flag
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/flag.png',
                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(43))
                # world
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/world.png',
                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(44))
                # setup
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/setup.png',
                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(45))
                # star
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/star.png',
                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(46))
                # diamond
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/diamond.png',
                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(47))
                # starsqueeze
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/starsqueeze.png',
                                       onCommand=lambda x: ad_cc_on_selection_ctrl_shape(48))

    pm.showWindow()


def ad_cc_replacing_controller_button(*args):
    list_controller = pm.ls(sl=1)
    if not list_controller:
        om.MGlobal.displayError("No curves selected, you have to select origin and target curve!")
        return False

    else:
        controller_replacing = al.ad_lib_replacing_controller(list_controller)
        al.ad_lib_replacing_color(controller_replacing[0], controller_replacing[1])


def ad_cc_tagging_untagging_button(tagging, *args):
    selection = pm.ls(selection=True)
    if not selection:
        om.MGlobal.displayError("No curves selected")
    else:
        for item in selection:
            try:
                shape_node = item.getShape()
            except:
                pass
            else:
                if pm.objectType(shape_node) == 'nurbsCurve':
                    if tagging:
                        al.ad_lib_tagging(shape_node)
                    else:
                        al.ad_lib_untagging(shape_node)


# RUN
def ad_cc_controller_button(*args):
    select = pm.ls(sl=1)
    child_text_field = al.ad_lib_text_field_query_text('Suffix_Child_Ctrl')
    child_check_box = pm.checkBox('Adding_Ctrl_Child', q=True, value=True)
    # condition the text filed is empty
    if not child_text_field:
        om.MGlobal_displayError("'Add Child Ctrl:' cannot be empty!")

    # condition the text filed is not empty
    else:
        # condition selection object
        if select:
            # query value of manipulation position
            manipulated_position = pm.manipPivot(q=True, p=True)[0]
            # query value of manipulation rotation
            manipulated_rotation = pm.manipPivot(q=True, o=True)[0]

            # create controller shape
            main_controller = al.ad_lib_create_main_ctrl_prefix_suffix_selection(select, on_selector)

            # condition the controller doesn't has an issue
            if main_controller:
                # match position
                al.ad_lib_match_position_target_to_ctrl(selection=select, target=main_controller[0],
                                                        manipulated_position=manipulated_position,
                                                        manipulated_rotation=manipulated_rotation)
                # condition the object select as COMPONENTS
                if '.' in str(select[0]):
                    get_objects = []
                    for item in select:
                        get_object = item.split('.')
                        parent_query = pm.listRelatives(get_object[0], p=True)
                        get_objects.append(parent_query[0])

                    listing = list(set(get_objects))
                    for target in listing:
                        # condition when have child controller
                        if child_check_box:
                            # create child controller
                            child_controller = al.ad_lib_child_ctrl(main_controller=main_controller[0],
                                                                    main_name=main_controller[1],
                                                                    on_selector=on_selector)
                            # add connection
                            al.ad_lib_connection(ctrl=child_controller[0], target=target)

                        # condition when doesn't have child controller
                        else:
                            al.ad_lib_connection(ctrl=main_controller[0], target=target)

                        # add pivot controller
                        if pm.checkBox('Add_Pivot_Ctrl', q=True, value=True):
                            pm.displayWarning("Adding pivot controller is skipped, since it's component mode.")

                        # add visibility to target
                        al.ad_lib_visibility_target(object=main_controller[0][0],
                                                    target=target)

                # condition the object select as TRANSFORM
                else:
                    # condition when have child controller
                    if child_check_box:
                        # create child controller
                        child_controller = al.ad_lib_child_ctrl(main_controller=main_controller[0],
                                                                main_name=main_controller[1], on_selector=on_selector)

                        for target, child_ctrl, main_ctrl in zip(select, child_controller, main_controller[0]):

                            # add connection
                            connection = al.ad_lib_connection(ctrl=child_ctrl, target=target)

                            # add pivot controller
                            if pm.checkBox('Add_Pivot_Ctrl', q=True, value=True):
                                al.ad_lib_pivot_controller(controller=child_ctrl,
                                                           parent_constraint_node=connection[0],
                                                           suffix='_' + al.ad_lib_suffix_main())
                            # add visibility to target
                            al.ad_lib_visibility_target(object=main_ctrl, target=target)

                    # condition when doesn't have child controller
                    else:
                        for target, main_ctrl in zip(select, main_controller[0]):

                            # add connection
                            connection = al.ad_lib_connection(ctrl=main_ctrl, target=target)

                            # add pivot controller
                            if pm.checkBox('Add_Pivot_Ctrl', q=True, value=True):
                                al.ad_lib_pivot_controller(controller=main_ctrl,
                                                           parent_constraint_node=connection[0],
                                                           suffix='_' + al.ad_lib_suffix_main())
                            # add visibility to target
                            al.ad_lib_visibility_target(object=main_ctrl, target=target)
            else:
                pass

        # condition nothing selected object
        else:
            # create controller without selection
            main_controller = al.ad_lib_create_main_ctrl_prefix_suffix(on_selector)

            # condition the controller doesn't has an issue
            if main_controller:
                if child_check_box:
                    # add child controller
                    al.ad_lib_child_ctrl(main_controller=main_controller[0], main_name=main_controller[1],
                                         on_selector=on_selector)
                else:
                    pass

                # add target visibility
                if pm.checkBox('Add_Pivot_Ctrl', q=True, value=True):
                    pm.displayWarning("Adding pivot controller is skipped, since there is no object selection.")

                # add pivot controller
                if pm.checkBox('Add_Pivot_Ctrl', q=True, value=True):
                    pm.displayWarning("Adding pivot controller is skipped, since there is no object selection.")

            else:
                pass

        # continue create group parent with condition when the controller doesn't has an issue
        if main_controller:
            # grouping controller
            if pm.textField('Parent_Group_Name', q=True, enable=True):
                al.ad_lib_main_ctrl_grouping(controller=main_controller[0],
                                             main_name=main_controller[1],
                                             prefix_2=al.ad_lib_prefix('Prefix_2_Text'))

            # set the main controller color
            for item in main_controller[0]:
                al.ad_lib_ctrl_color(ctrl=item, color=ad_cc_set_color())

            # set the main controller hide and unlock
            al.ad_lib_hide_and_lock(main_controller[0], value=True)

        else:
            pass

        pm.select(cl=1)


####### CREATE CONTROLLER FUNCTION #######

def ad_cc_connection_uncheck_translate_rotate_constraint(target, pivot, object, value, *args):
    checkbox_obj = pm.checkBox(object, q=True, value=value)
    for item in target:
        if checkbox_obj == 1:
            pm.checkBox(item, e=True, value=False)
    for pvt in pivot:
        pm.checkBox(pvt, edit=True, enable=False)
        pm.checkBox(pvt, edit=True, value=False)


def ad_cc_connection_uncheck_scale_constraint(target, object, value, *args):
    checkbox_obj = pm.checkBox(object, q=True, value=value)
    for item in target:
        if checkbox_obj == 1:
            pm.checkBox(item, e=True, value=False)


def ad_cc_connection_uncheck_parent_constraint(target, pivot, object, value, *args):
    checkbox_obj = pm.checkBox(object, q=True, value=value)
    for item in target:
        if checkbox_obj == 1:
            pm.checkBox(item, e=True, value=False)
    for pvt in pivot:
        pm.checkBox(pvt, edit=True, enable=value)
        if checkbox_obj == 0:
            pm.checkBox(pvt, e=True, value=False)


#
def ad_cc_set_color(*args):
    controller_color = pm.palettePort('Pallete', query=True, setCurCell=True)
    return controller_color


#
def ad_cc_checkbox_check_channel_translate(objects, value, *args):
    for item in objects:
        all_trans = pm.checkBox('All_Trans', q=True, value=value)
        if all_trans == 1:
            pm.checkBox(item, e=True, value=True)
        else:
            pm.checkBox(item, e=True, value=False)


def ad_cc_checkbox_check_channel_rotate(objects, value, *args):
    for item in objects:
        all_rot = pm.checkBox('All_Rot', q=True, value=value)
        if all_rot == 1:
            pm.checkBox(item, e=True, value=True)
        else:
            pm.checkBox(item, e=True, value=False)


def ad_cc_checkbox_check_channel_scale(objects, value, *args):
    for item in objects:
        all_scale = pm.checkBox('All_Scale', q=True, value=value)
        if all_scale == 1:
            pm.checkBox(item, e=True, value=True)
        else:
            pm.checkBox(item, e=True, value=False)


def ad_cc_checkbox_uncheck_all_channel(*args):
    trans_x = pm.checkBox('Trans_X', q=True, value=True)
    trans_y = pm.checkBox('Trans_Y', q=True, value=True)
    trans_z = pm.checkBox('Trans_Z', q=True, value=True)

    rot_x = pm.checkBox('Rot_X', q=True, value=True)
    rot_y = pm.checkBox('Rot_Y', q=True, value=True)
    rot_z = pm.checkBox('Rot_Z', q=True, value=True)

    scale_x = pm.checkBox('Scl_X', q=True, value=True)
    scale_y = pm.checkBox('Scl_Y', q=True, value=True)
    scale_z = pm.checkBox('Scl_Z', q=True, value=True)

    if trans_x == 0 or trans_y == 0 or trans_z == 0:
        pm.checkBox('All_Trans', e=True, value=False)

    if rot_x == 0 or rot_y == 0 or rot_z == 0:
        pm.checkBox('All_Rot', e=True, value=False)

    if scale_x == 0 or scale_y == 0 or scale_z == 0:
        pm.checkBox('All_Scale', e=True, value=False)


#
def ad_cc_controller_resize_reset(*args):
    pm.floatSlider('Controller_Resize', edit=True, v=1.0)


def ad_cc_on_selection_ctrl_shape(on):
    # save the current shape selection into global variable
    global on_selector
    on_selector = on


########################################################################################################################
#                                           CONTROLLER UTILITIES TAB FUNCTION
########################################################################################################################
####### CONTROLLER UTILITIES UI FUNCTION
# ROTATE
def ad_cu_rotation_x_button(*args):
    al.ad_lib_rotate_controller(x=al.ad_lib_degree_rotation_int_field('Degree_Rotate'), y=0.0, z=0.0)


def ad_cu_rotation_y_button(*args):
    al.ad_lib_rotate_controller(x=0.0, y=al.ad_lib_degree_rotation_int_field('Degree_Rotate'), z=0.0)


def ad_cu_rotation_z_button(*args):
    al.ad_lib_rotate_controller(x=0.0, y=0.0, z=al.ad_lib_degree_rotation_int_field('Degree_Rotate'))


# MIRROR
def ad_cu_mirror_button(key_position, *args):
    selection = pm.ls(selection=True)
    if not selection:
        om.MGlobal.displayWarning("No objects is selected!")
    else:
        for select_obj in selection:
            # get name object even though multiple object
            name = select_obj.nodeName()

            # conversion into string
            string_select = str(name)

            # get sting from the box field
            prefix_text_from_string = str(al.ad_lib_from_to_prefix_text('From_Prefix'))
            prefix_text_to_string = str(al.ad_lib_from_to_prefix_text('To_Prefix'))

            # get shape object
            if pm.objectType(select_obj.getShape()) == 'nurbsCurve':

                # condition text from box in object select
                if prefix_text_from_string in string_select:
                    # replace target name
                    get_target_name = string_select.replace(prefix_text_from_string, prefix_text_to_string)

                    # check the object exists
                    if pm.objExists(get_target_name):

                        # listing in case multiple object
                        list_target = pm.ls(get_target_name)
                        for item_target in list_target:
                            # check the length of cv's and match it
                            if len(item_target.getShape().cv) == len(select_obj.getShape().cv):
                                al.ad_lib_mirror_controller(object_origin=select_obj, object_target=item_target,
                                                            key_position=key_position)
                                if len(list_target) > 1:
                                    om.MGlobal.displayWarning(
                                        "There is more than one '%s' with similar name!" % (item_target))
                                else:
                                    pass
                            else:
                                om.MGlobal.displayWarning(
                                    "Skip the mirroring '%s'! The '%s' cv's number is not similar!" % (
                                        name, item_target))
                    else:
                        om.MGlobal.displayWarning(
                            "Skip the mirroring '%s'! There is no target curve object '%s' in the scene!" % (
                                string_select, get_target_name))
                else:
                    om.MGlobal.displayWarning("Skip the mirroring '%s'! It doesn't have prefix '%s' name" % (
                        string_select, prefix_text_from_string))

            else:
                om.MGlobal.displayWarning("Skip the mirroring '%s'! The object type is not curve." % string_select)


def ad_cu_swap_button(*args):
    from_prefix = pm.textFieldButtonGrp('From_Prefix', q=True, tx=True)
    to_prefix = pm.textFieldButtonGrp('To_Prefix', q=True, tx=True)

    from_prefix, to_prefix = to_prefix, from_prefix

    pm.textFieldButtonGrp('From_Prefix', e=True, tx=from_prefix)
    pm.textFieldButtonGrp('To_Prefix', e=True, tx=to_prefix)


def ad_cu_object_sel_to_textfield_mirror(text_input, *args):
    # delete and add object
    select = pm.ls(sl=True, l=True, tr=True)
    if len(select) == 1:
        object_selection = select[0]
        pm.textFieldButtonGrp(text_input, e=True, tx=object_selection, bl="<<")
    else:
        pm.error("please select one object or one prefix!")


# SAVE/LOAD
def ad_cu_save_dialog(*args):
    if pm.ls(sl=1):
        pm.confirmDialog(icon='warning',
                         title='Save Confirm',
                         message='Only selected controllers \nwill be saved!')
    else:
        pm.confirmDialog(icon='warning',
                         title='Save Confirm',
                         message='There is no object selected.\nAll of the controllers curve in the scene \nwill be saved!')

    save = pm.fileDialog2(fileMode=0, fileFilter='*.json', dialogStyle=2,
                          cap='Save AD Controller')
    # Check Path
    if not save: return
    filePath = save[0]

    # export json file
    al.ad_lib_save_json_controller(filePath)

    return filePath


def ad_cu_load_dialog(*args):
    if pm.ls(sl=1):
        pm.confirmDialog(icon='warning',
                         title='Load Confirm',
                         message='Only selected controllers \nwill be loaded!')

    else:
        pm.confirmDialog(icon='warning',
                         title='Load Confirm',
                         message='There is no object selected.\nAll of the controllers curve in the scene \nwill be loaded!')

    load = pm.fileDialog2(fileMode=1, fileFilter='*.json', okc='Load', dialogStyle=2,
                          cap='Load AD Controller')

    if not load: return
    filePath = load[0]

    # export json file
    al.ad_lib_load_json_controller(filePath)

    return filePath
