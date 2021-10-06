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

import json
import re
from collections import OrderedDict
from string import digits

import maya.OpenMaya as om
import pymel.core as pm



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
                            ad_lib_defining_object_text_field(define_object='Prefix_1_Text', tx='L_', enable=False)

                            # name text field
                            pm.checkBox('Name_CheckBox', label='Name:', cc=partial(ad_cc_enabling_disabling_ui,
                                                                                   ['Name_Text'], ''), value=False)
                            ad_lib_defining_object_text_field(define_object='Name_Text', enable=False)
                            # prefix 2 text field
                            pm.checkBox('Prefix_2', label='Prefix 2:',
                                        cc=partial(ad_cc_enabling_disabling_ui, ['Prefix_2_Text'], 'LFT'), value=False)
                            ad_lib_defining_object_text_field(define_object='Prefix_2_Text', tx='LFT', enable=False)

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
                            ad_lib_defining_object_text_field(define_object='Parent_Group_Name', tx='Main,Offset',
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
        ad_lib_list_connections_object(list_object)
    else:
        om.MGlobal_displayError('Select the minimum one object which has a connection!')


def ad_cc_connection_button(*args):
    list_controller = pm.ls(sl=1)
    if len(list_controller) < 2:
        om.MGlobal_displayError('Select minimum two objects!')
    else:
        instance_controller = list_controller.pop(0)
        for item in list_controller:
            ad_lib_connection(ctrl=instance_controller, target=item)


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
    ad_lib_ctrl_color_list(0)
    pm.select(cl=True)


def ad_cc_replace_color_button(*args):
    ad_lib_ctrl_color_list(ad_cc_set_color())
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
            ad_lib_hide_unhide(ctrl=item)


def ad_cc_lock_unlock_button(*args):
    selection = pm.ls(selection=True)
    if not selection:
        om.MGlobal.displayError("No objects selected")
        return False
    else:
        for item in selection:
            ad_lib_lock_unlock(ctrl=item)


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
                ad_lib_scaling_controller(item, current_value)
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
            name = ad_lib_get_number_main_name(item)
            group = ad_lib_group_parent(groups=ad_lib_query_list_textfield_object('Parent_Group_Name')[0],
                                           name=name[1],
                                           suffix=ad_lib_get_suffix_main(item),
                                           prefix_number=name[0], prefix_2=ad_lib_prefix('Prefix_2_Text'))
            ad_lib_xform_position_rotation(origin=item, target=group[0])
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
        controller_replacing = ad_lib_replacing_controller(list_controller)
        ad_lib_replacing_color(controller_replacing[0], controller_replacing[1])


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
                        ad_lib_tagging(shape_node)
                    else:
                        ad_lib_untagging(shape_node)


# RUN
def ad_cc_controller_button(*args):
    select = pm.ls(sl=1)
    child_text_field = ad_lib_text_field_query_text('Suffix_Child_Ctrl')
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
            main_controller = ad_lib_create_main_ctrl_prefix_suffix_selection(select, on_selector)

            # condition the controller doesn't has an issue
            if main_controller:
                # match position
                ad_lib_match_position_target_to_ctrl(selection=select, target=main_controller[0],
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
                            child_controller = ad_lib_child_ctrl(main_controller=main_controller[0],
                                                                    main_name=main_controller[1],
                                                                    on_selector=on_selector)
                            # add connection
                            ad_lib_connection(ctrl=child_controller[0], target=target)

                        # condition when doesn't have child controller
                        else:
                            ad_lib_connection(ctrl=main_controller[0], target=target)

                        # add pivot controller
                        if pm.checkBox('Add_Pivot_Ctrl', q=True, value=True):
                            pm.displayWarning("Adding pivot controller is skipped, since it's component mode.")

                        # add visibility to target
                        ad_lib_visibility_target(object=main_controller[0][0],
                                                    target=target)

                # condition the object select as TRANSFORM
                else:
                    # condition when have child controller
                    if child_check_box:
                        # create child controller
                        child_controller = ad_lib_child_ctrl(main_controller=main_controller[0],
                                                                main_name=main_controller[1], on_selector=on_selector)

                        for target, child_ctrl, main_ctrl in zip(select, child_controller, main_controller[0]):

                            # add connection
                            connection = ad_lib_connection(ctrl=child_ctrl, target=target)

                            # add pivot controller
                            if pm.checkBox('Add_Pivot_Ctrl', q=True, value=True):
                                ad_lib_pivot_controller(controller=child_ctrl,
                                                           parent_constraint_node=connection[0],
                                                           suffix='_' + ad_lib_suffix_main())
                            # add visibility to target
                            ad_lib_visibility_target(object=main_ctrl, target=target)

                    # condition when doesn't have child controller
                    else:
                        for target, main_ctrl in zip(select, main_controller[0]):

                            # add connection
                            connection = ad_lib_connection(ctrl=main_ctrl, target=target)

                            # add pivot controller
                            if pm.checkBox('Add_Pivot_Ctrl', q=True, value=True):
                                ad_lib_pivot_controller(controller=main_ctrl,
                                                           parent_constraint_node=connection[0],
                                                           suffix='_' + ad_lib_suffix_main())
                            # add visibility to target
                            ad_lib_visibility_target(object=main_ctrl, target=target)
            else:
                pass

        # condition nothing selected object
        else:
            # create controller without selection
            main_controller = ad_lib_create_main_ctrl_prefix_suffix(on_selector)

            # condition the controller doesn't has an issue
            if main_controller:
                if child_check_box:
                    # add child controller
                    ad_lib_child_ctrl(main_controller=main_controller[0], main_name=main_controller[1],
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
                ad_lib_main_ctrl_grouping(controller=main_controller[0],
                                             main_name=main_controller[1],
                                             prefix_2=ad_lib_prefix('Prefix_2_Text'))

            # set the main controller color
            for item in main_controller[0]:
                ad_lib_ctrl_color(ctrl=item, color=ad_cc_set_color())

            # set the main controller hide and unlock
            ad_lib_hide_and_lock(main_controller[0], value=True)

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
    ad_lib_rotate_controller(x=ad_lib_degree_rotation_int_field('Degree_Rotate'), y=0.0, z=0.0)


def ad_cu_rotation_y_button(*args):
    ad_lib_rotate_controller(x=0.0, y=ad_lib_degree_rotation_int_field('Degree_Rotate'), z=0.0)


def ad_cu_rotation_z_button(*args):
    ad_lib_rotate_controller(x=0.0, y=0.0, z=ad_lib_degree_rotation_int_field('Degree_Rotate'))


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
            prefix_text_from_string = str(ad_lib_from_to_prefix_text('From_Prefix'))
            prefix_text_to_string = str(ad_lib_from_to_prefix_text('To_Prefix'))

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
                                ad_lib_mirror_controller(object_origin=select_obj, object_target=item_target,
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
    ad_lib_save_json_controller(filePath)

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
    ad_lib_load_json_controller(filePath)

    return filePath

########################################################################################################################
#                                                    LIBRARY                                                           #
########################################################################################################################

"""
DESCRIPTION:
    Module library for ad_controller.py.

USAGE:
    -

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


def ad_lib_save_json_controller(file_name):
    if pm.ls(type='nurbsCurve'):
        # ordered dictionary
        shape_dict = OrderedDict()
        selection = pm.ls(sl=1)
        list = []
        # checking the naming
        if selection:
            for item in selection:
                try:
                    # get type and get the shape
                    object = pm.objectType(item.getShape())
                except:
                    pass
                else:
                    if object == 'nurbsCurve':
                        om.MGlobal.displayInfo("Object '%s' is saved!." % (item))
                        list.append(item.getShape())
                    else:
                        om.MGlobal.displayWarning("Object '%s' is skipped! It is not nurbsCurve." % (item))

        else:
            list = pm.ls(type='nurbsCurve')

        # all item shape in the list
        for item in list:
            # get transform name
            item_parent = item.getParent()
            print item_parent
            # get node
            object_curve = pm.PyNode(item_parent)

            # get cv number, x value, y value, z value and color on each item
            cvs, xvalue, yvalue, zvalue, color = [], [], [], [], []

            for cv in object_curve.getShape().cv:
                x = pm.getAttr(cv + '.xValue')
                y = pm.getAttr(cv + '.yValue')
                z = pm.getAttr(cv + '.zValue')
                xvalue.append(x)
                yvalue.append(y)
                zvalue.append(z)

                # get the number cv
                cv = cv.split('.')[-1]
                cvs.append(cv)

            if pm.getAttr('%s.overrideEnabled' % item):
                color_number = pm.getAttr('%s.overrideColor' % item)
                color.append(color_number)
            shape_dict[str(item_parent)] = {'cv': cvs, 'xValue': xvalue, 'yValue': yvalue, 'zValue': zvalue,
                                            'overrideColor': color}

            om.MGlobal.displayInfo("Object '%s' is saved!." % (item.getParent()))

        om.MGlobal.displayInfo("---------------- File path saved: '%s'" % file_name)

        # write the json file
        file = open("%s" % (file_name), "w")
        json.dump(shape_dict, file, indent=4)

    else:
        return om.MGlobal.displayWarning("No write in the file save as there is no curve object exists in the scene")


def ad_lib_load_json_controller(file_name):
    # get all the nurbs object in the scene
    scene = pm.ls(type='nurbsCurve')

    # query the curve exist in the scene
    if scene:
        # load the file
        file = open("%s" % (file_name))
        shape_dict = json.load(file)

        # get key in dictionary
        keys = shape_dict.keys()

        # object selection
        select = pm.ls(sl=1)

        list = []
        # object select (if any)
        if select:
            for item in select:
                try:
                    # query the object selection whether it has shape
                    object = pm.objectType(item.getShape())
                except:
                    pass
                else:
                    # if it has a shape check whether it curves object
                    if object == 'nurbsCurve':
                        # check item in keys dictionary
                        if item in keys:
                            om.MGlobal.displayInfo("Object '%s' is loaded!." % (item))
                            list.append(item)
                        else:
                            om.MGlobal.displayWarning(
                                "Object '%s' is skipped! There is no saving curve in the library." % (item))
                    else:
                        om.MGlobal.displayWarning("Object '%s' is skipped! It is not nurbsCurve." % (item))

        # if there is no object select in the scene
        else:
            for item in scene:
                # get transform on each item
                item = item.getParent()
                if item in keys:
                    # match the cvs
                    # print len (item)
                    # if len(item_target.getShape().cv) == len(select_obj.getShape().cv)
                    # om.MGlobal.displayInfo("Object '%s' is loaded!." % (item))
                    list.append(item)
                else:
                    om.MGlobal.displayWarning(
                        "Object '%s' is skipped! There is no saving curve in the library." % (item))

        for name in list:
            # get name on query items
            name = str(name)
            # get the value of dictionary
            value = shape_dict.get(name)
            # get the node
            name = pm.PyNode(name)
            # get shape of from the string name
            shape_name = name.getShape()

            # checking the number or cv's
            if len(name.getShape().cv) == len(value['cv']):
                # set all the things up
                for cv, x, y, z in zip(value['cv'], value['xValue'], value['yValue'],
                                       value['zValue']):
                    pm.setAttr('%s.%s.xValue' % (shape_name, cv), x)
                    pm.setAttr('%s.%s.yValue' % (shape_name, cv), y)
                    pm.setAttr('%s.%s.zValue' % (shape_name, cv), z)

                for color in value['overrideColor']:
                    pm.setAttr('%s.overrideColor' % shape_name, color)
            else:
                om.MGlobal.displayWarning(
                    "Object '%s' is skipped! The number of cv's is doesn't match with data!." % (name))

        om.MGlobal.displayInfo("---------------- File path loaded: '%s'" % file_name)
    else:
        return om.MGlobal.displayWarning("Loaded is failed as there is no curve object exists in the scene!")


def ad_lib_mirror_controller(object_origin, object_target, key_position):
    # object select node
    object_curve_origin = pm.PyNode(object_origin)
    # object target node
    object_curve_target = pm.PyNode(object_target)

    for vtx_origin, vtx_target in zip(object_curve_origin.getShape().cv, object_curve_target.getShape().cv):
        # query the position
        position_ws_vtx_origin = pm.xform(vtx_origin, q=True, ws=True, t=True)
        # get the vector on each select object
        vector_ws_vtx_origin = pm.dt.Vector(position_ws_vtx_origin[0], position_ws_vtx_origin[1],
                                            position_ws_vtx_origin[2])
        # get the vector mirror value multiply by reverse
        vector_mirror = \
            ad_lib_vector_reverse_position(vector_ws_vtx_origin[0], vector_ws_vtx_origin[1], vector_ws_vtx_origin[2])[
                key_position]
        # move each vertex
        pm.move((vector_mirror[0]), (vector_mirror[1]), (vector_mirror[2]), vtx_target)


def ad_lib_average_position(vertices):
    result = [0, 0, 0]
    vertices = pm.PyNode(vertices)
    for vtx in vertices.getShape().cv:
        pos_tmp = pm.pointPosition(vtx)
        result[0] += pos_tmp[0]
        result[1] += pos_tmp[1]
        result[2] += pos_tmp[2]

    # geting amount of all vertices
    vtxCount = len(vertices.getShape().cv)

    # getting average of x y z values
    result[0] /= vtxCount
    result[1] /= vtxCount
    result[2] /= vtxCount

    return result[0], result[1], result[2]


def ad_lib_rotate_controller(x, y, z):
    selection = pm.ls(selection=True)
    if not selection:
        om.MGlobal.displayWarning("No objects selected")
    else:
        # item object in selection
        for item in selection:
            try:
                # query the shape object
                shape = item.getShape()
            except:
                pass
            else:
                # if the object shape nurbs type
                if pm.objectType(shape) == 'nurbsCurve':
                    points = pm.ls('%s.cv[0:*]' % shape)
                    pm.rotate(points, (x, y, z), r=True,
                              p=ad_lib_average_position(item), os=True, fo=True)

                else:
                    om.MGlobal.displayWarning("Skip the rotating '%s'! The object type is not curve." % item)


def ad_lib_vector_reverse_position(vector_origin_0, vector_origin_1, vector_origin_2):
    # reverse the vector x y z
    vector_position_origin_x = pm.dt.Vector(vector_origin_0 * -1.0, vector_origin_1, vector_origin_2)
    vector_position_origin_y = pm.dt.Vector(vector_origin_0, vector_origin_1 * -1.0, vector_origin_2)
    vector_position_origin_z = pm.dt.Vector(vector_origin_0, vector_origin_1, vector_origin_2 * -1.0)

    return {'x': vector_position_origin_x,
            'y': vector_position_origin_y,
            'z': vector_position_origin_z}


def ad_lib_from_to_prefix_text(prefix):
    text_field = pm.textFieldButtonGrp(prefix, q=True, tx=True)
    return text_field


def ad_lib_degree_rotation_int_field(int_name):
    value = pm.intField(int_name, q=True, value=True)
    return value


def ad_lib_list_connections_object(object):
    # list connection
    if len(object) > 1:
        om.MGlobal.displayError('Objects selected are multiple. Select a single object only!')
    else:
        select = []
        for item in object:
            # query the source connection
            source = pm.listConnections(object, p=True, d=False, s=True, c=True)
            if source:
                for node_source in source:
                    connection_source_object = node_source[1].split('.')[0]
                    connection_source_transform = node_source[1].split('.')[1]

                    # query node type
                    node_source_type = pm.nodeType(connection_source_object)

                    connection_destination_object = node_source[0].split('.')[0]
                    connection_destination_transform = node_source[0].split('.')[1]

                    if node_source_type == 'parentConstraint':
                        object_select = pm.listConnections(connection_source_object + '.target[0].targetParentMatrix',
                                                           d=0, s=1)
                        om.MGlobal.displayInfo("------ >>> %s %s is connected to Parent Constraint from %s %s!" %
                                               (item, connection_destination_transform, object_select[0],
                                                connection_source_transform[10:]))
                    elif node_source_type == 'pointConstraint':
                        object_select = pm.listConnections(connection_source_object + '.target[0].targetParentMatrix',
                                                           d=0, s=1)
                        om.MGlobal.displayInfo("------ >>> %s %s is connected to Point Constraint from %s %s!" %
                                               (item, connection_destination_transform, object_select[0],
                                                connection_source_transform[10:]))
                    elif node_source_type == 'orientConstraint':
                        object_select = pm.listConnections(connection_source_object + '.target[0].targetParentMatrix',
                                                           d=0, s=1)
                        om.MGlobal.displayInfo("------ >>> %s %s is connected to Orient Constraint from %s %s!" %
                                               (item, connection_destination_transform, object_select[0],
                                                connection_source_transform[10:]))
                    elif node_source_type == 'scaleConstraint':
                        object_select = pm.listConnections(connection_source_object + '.target[0].targetParentMatrix',
                                                           d=0, s=1)
                        om.MGlobal.displayInfo("------ >>> %s %s is connected to Scale Constraint from %s %s!" %
                                               (item, connection_destination_transform, object_select[0],
                                                connection_source_transform[10:]))
                    elif node_source_type == 'aimConstraint':
                        object_select = pm.listConnections(connection_source_object + '.target[0].targetParentMatrix',
                                                           d=0, s=1)
                        om.MGlobal.displayInfo("------ >>> %s %s is connected to Aim Constraint from %s %s!" %
                                               (item, connection_destination_transform, object_select[0],
                                                connection_source_transform[10:]))
                    elif node_source_type == 'transform':
                        object_select = connection_source_object
                        om.MGlobal.displayInfo("------ >>> %s %s is connected to Direct Connection from %s %s!" % (
                            connection_destination_object,
                            connection_destination_transform,
                            connection_source_object,
                            connection_source_transform))
                    else:
                        object_select = om.MGlobal.displayWarning(
                            "Skip the target! The object %s %s doesn't have any constraint or direct connection! "
                            "It's connected with another node. " %
                            (connection_destination_object, connection_destination_transform))

                    select.append(object_select)
                try:
                    pm.select(select)
                except:
                    pass
            else:
                om.MGlobal.displayWarning('There is no connection to the transform object selected!')


def ad_lib_pivot_controller(controller, parent_constraint_node, suffix):
    joint = pm.joint(n='instance_pivot')
    pm.setAttr(joint + '.drawStyle', 2)
    controller_rs = ad_lib_shape_controller(LOCATOR, size_ctrl=0.8, tag_number=2)
    ad_lib_ctrl_color(ctrl=controller_rs, color=20)
    pm.rename(controller_rs, ad_lib_main_name(controller) + 'Pivot' + suffix)

    # parent relatives
    shape_ctrl = pm.listRelatives(controller_rs, s=True)[0]
    pm.parent(shape_ctrl, joint, r=True, s=True)
    pm.delete(controller_rs)

    # create joint for connection
    joint_new_name = pm.rename(joint, ad_lib_main_name(controller) + 'Pivot' + suffix)
    ad_lib_xform_position_rotation(origin=controller, target=joint_new_name)
    pm.parent(joint_new_name, controller)

    # connect pivot
    pm.connectAttr(joint + '.translate', controller + '.rotatePivot')
    pm.connectAttr(joint + '.translate', controller + '.scalePivot')

    # create decompose matrix
    decompose_matrix = pm.createNode('decomposeMatrix', n=ad_lib_main_name(joint_new_name) + '_dmtx')
    pm.connectAttr(joint_new_name + '.inverseMatrix', decompose_matrix + '.inputMatrix')
    pm.connectAttr(decompose_matrix + '.outputTranslate', parent_constraint_node + '.target[0].targetOffsetTranslate')

    # lock attribute
    ad_lib_lock_hide_attr(lock_hide_channel=['r', 's', 'v', 'radius'], ctrl=joint_new_name, hide_object=True, cb=0)

    return joint_new_name


def ad_lib_parent_constraint(obj_base, obj_target, mo=1):
    par_constraint = pm.parentConstraint(obj_base, obj_target, mo=mo)
    split = par_constraint.split('_')
    x = '_'.join(split[:-1])
    n = x.replace(x, x + '_pac')
    new_name = [pm.rename(par_constraint, n)]
    return new_name


def ad_lib_orient_constraint(obj_base, obj_target, mo=1):
    orient_constraint = pm.orientConstraint(obj_base, obj_target, mo=mo)
    split = orient_constraint.split('_')
    x = '_'.join(split[:-1])
    n = x.replace(x, x + '_oc')
    new_name = [pm.rename(orient_constraint, n)]
    return new_name


def ad_lib_point_constraint(obj_base, obj_target, mo=1):
    point_constraint = pm.pointConstraint(obj_base, obj_target, mo=mo)
    split = point_constraint.split('_')
    x = '_'.join(split[:-1])
    n = x.replace(x, x + '_pc')
    new_name = [pm.rename(point_constraint, n)]
    return new_name


def ad_lib_scale_constraint(obj_base, obj_target, mo=1):
    scale_constraint = pm.scaleConstraint(obj_base, obj_target, mo=mo)
    split = scale_constraint.split('_')
    x = '_'.join(split[:-1])
    n = x.replace(x, x + '_sc')
    new_name = [pm.rename(scale_constraint, n)]

    return new_name


def ad_lib_text_field_query_enabled(object_define):
    name_text_enable = pm.textField(object_define, q=True, enable=True)

    return name_text_enable


def ad_lib_text_field_query_text(object_define):
    name_text_enable = pm.textField(object_define, q=True, tx=True)
    if name_text_enable:
        return name_text_enable
    else:
        return ''


def ad_lib_suffix_main():
    suffix = pm.textField('Suffix_Main', q=True, tx=True)
    if suffix:
        add_space = suffix.lower()
        return add_space
    else:
        om.MGlobal_displayError("'Suffix:' cannot be empty!")


def ad_lib_main_ctrl_grouping(controller, main_name, prefix_2):
    grouping_controller = []
    for object_controller, name in zip(controller, main_name):
        # get main name and number
        ad_main_name = ad_lib_get_number_main_name(name)
        group_controller = ad_lib_group_parent(groups=ad_lib_query_list_textfield_object('Parent_Group_Name')[0],
                                               name=ad_main_name[1],
                                               suffix=ad_lib_suffix_main(),
                                               prefix_number=ad_main_name[0], prefix_2=prefix_2)

        ad_lib_xform_position_rotation(origin=object_controller, target=group_controller[0])
        pm.parent(object_controller, group_controller[-1])
        grouping_controller.append(group_controller)
        pm.select(cl=1)

    return grouping_controller


def ad_lib_child_ctrl(main_controller, main_name, on_selector):
    child_text_field = ad_lib_text_field_query_text('Suffix_Child_Ctrl')
    controller_childs = []
    for controller, name in zip(main_controller, main_name):
        # get main name and number
        ad_main_name = ad_lib_get_number_main_name(name)

        # object_main_shape = pm.listRelatives(controller, shapes=1)[0]
        object_main_shape = controller.getShape()
        controller_shape = ad_lib_controller_shape(size_ctrl=0.8, on_selector=on_selector)
        controller_child = pm.rename(controller_shape,
                                     ad_main_name[1] + child_text_field.title() + ad_main_name[0] +
                                     ad_lib_prefix('Prefix_2_Text') + '_' + ad_lib_suffix_main())

        controller_child_shape = controller_child.getShape()

        ad_lib_xform_position_rotation(origin=controller, target=controller_child)
        pm.parent(controller_child, controller)
        ad_lib_display(object=object_main_shape, target=controller_child_shape,
                       long_name=child_text_field + 'Ctrl',
                       default_vis=0,
                       k=False, cb=True)
        # set color
        ad_lib_ctrl_color(ctrl=controller_child, color=16)

        controller_childs.append(controller_child)

    return controller_childs


def ad_lib_connection(ctrl, target):
    connection = []
    if ad_lib_query_lock_unlock_hide_unhide_channel('Point_Cons'):
        connection = ad_lib_point_constraint(obj_base=ctrl, obj_target=target)
    if ad_lib_query_lock_unlock_hide_unhide_channel('Orient_Cons'):
        connection = ad_lib_orient_constraint(obj_base=ctrl, obj_target=target)
    if ad_lib_query_lock_unlock_hide_unhide_channel('Scale_Cons'):
        connection = ad_lib_scale_constraint(obj_base=ctrl, obj_target=target)
    if ad_lib_query_lock_unlock_hide_unhide_channel('Parent_Cons'):
        connection = ad_lib_parent_constraint(obj_base=ctrl, obj_target=target)
    if ad_lib_query_lock_unlock_hide_unhide_channel('Parent'):
        connection = pm.parent(target, ctrl)
    if ad_lib_query_lock_unlock_hide_unhide_channel('Direct_Trans'):
        connection = pm.connectAttr(ctrl + '.translate', target + '.translate')
    if ad_lib_query_lock_unlock_hide_unhide_channel('Direct_Rot'):
        connection = pm.connectAttr(ctrl + '.rotate', target + '.rotate')
    if ad_lib_query_lock_unlock_hide_unhide_channel('Direct_Scl'):
        connection = pm.connectAttr(ctrl + '.scale', target + '.scale')
    return connection


def ad_lib_hide_unhide(ctrl):
    if ad_lib_query_lock_unlock_hide_unhide_channel("Trans_X"):
        ad_lib_hide_unhide_attr(channel=['tx'], ctrl=ctrl)
    if ad_lib_query_lock_unlock_hide_unhide_channel("Trans_Y"):
        ad_lib_hide_unhide_attr(channel=['ty'], ctrl=ctrl)
    if ad_lib_query_lock_unlock_hide_unhide_channel("Trans_Z"):
        ad_lib_hide_unhide_attr(channel=['tz'], ctrl=ctrl)
    if ad_lib_query_lock_unlock_hide_unhide_channel('Rot_X'):
        ad_lib_hide_unhide_attr(channel=['rx'], ctrl=ctrl)
    if ad_lib_query_lock_unlock_hide_unhide_channel('Rot_Y'):
        ad_lib_hide_unhide_attr(channel=['ry'], ctrl=ctrl)
    if ad_lib_query_lock_unlock_hide_unhide_channel('Rot_Z'):
        ad_lib_hide_unhide_attr(channel=['rz'], ctrl=ctrl)
    if ad_lib_query_lock_unlock_hide_unhide_channel('Scl_X'):
        ad_lib_hide_unhide_attr(channel=['sx'], ctrl=ctrl)
    if ad_lib_query_lock_unlock_hide_unhide_channel('Scl_Y'):
        ad_lib_hide_unhide_attr(channel=['sy'], ctrl=ctrl)
    if ad_lib_query_lock_unlock_hide_unhide_channel('Scl_Z'):
        ad_lib_hide_unhide_attr(channel=['sz'], ctrl=ctrl)
    if ad_lib_query_lock_unlock_hide_unhide_channel('Visibility'):
        ad_lib_hide_unhide_attr(channel=['v'], ctrl=ctrl)
    if ad_lib_query_lock_unlock_hide_unhide_channel('User_Def'):
        list_attribute = ad_lib_query_user_defined_channel(ctrl)
        ad_lib_hide_unhide_attr(channel=list_attribute, ctrl=ctrl)


def ad_lib_lock_unlock(ctrl):
    if ad_lib_query_lock_unlock_hide_unhide_channel("Trans_X"):
        ad_lib_lock_unlock_attr(channel=['tx'], ctrl=ctrl)
    if ad_lib_query_lock_unlock_hide_unhide_channel("Trans_Y"):
        ad_lib_lock_unlock_attr(channel=['ty'], ctrl=ctrl)
    if ad_lib_query_lock_unlock_hide_unhide_channel("Trans_Z"):
        ad_lib_lock_unlock_attr(channel=['tz'], ctrl=ctrl)
    if ad_lib_query_lock_unlock_hide_unhide_channel('Rot_X'):
        ad_lib_lock_unlock_attr(channel=['rx'], ctrl=ctrl)
    if ad_lib_query_lock_unlock_hide_unhide_channel('Rot_Y'):
        ad_lib_lock_unlock_attr(channel=['ry'], ctrl=ctrl)
    if ad_lib_query_lock_unlock_hide_unhide_channel('Rot_Z'):
        ad_lib_lock_unlock_attr(channel=['rz'], ctrl=ctrl)
    if ad_lib_query_lock_unlock_hide_unhide_channel('Scl_X'):
        ad_lib_lock_unlock_attr(channel=['sx'], ctrl=ctrl)
    if ad_lib_query_lock_unlock_hide_unhide_channel('Scl_Y'):
        ad_lib_lock_unlock_attr(channel=['sy'], ctrl=ctrl)
    if ad_lib_query_lock_unlock_hide_unhide_channel('Scl_Z'):
        ad_lib_lock_unlock_attr(channel=['sz'], ctrl=ctrl)
    if ad_lib_query_lock_unlock_hide_unhide_channel('Visibility'):
        ad_lib_lock_unlock_attr(channel=['v'], ctrl=ctrl)
    if ad_lib_query_lock_unlock_hide_unhide_channel('User_Def'):
        list_attribute = ad_lib_query_user_defined_channel(ctrl)
        ad_lib_lock_unlock_attr(channel=list_attribute, ctrl=ctrl)


def ad_lib_hide_and_lock(ctrl, value):
    for item in ctrl:
        if ad_lib_query_lock_unlock_hide_unhide_channel("Trans_X"):
            ad_lib_lock_hide_attr(lock_hide_channel=['tx'], ctrl=item,
                                  hide_object=value)
        if ad_lib_query_lock_unlock_hide_unhide_channel("Trans_Y"):
            ad_lib_lock_hide_attr(lock_hide_channel=['ty'], ctrl=item,
                                  hide_object=value)
        if ad_lib_query_lock_unlock_hide_unhide_channel("Trans_Z"):
            ad_lib_lock_hide_attr(lock_hide_channel=['tz'], ctrl=item,
                                  hide_object=value)
        if ad_lib_query_lock_unlock_hide_unhide_channel('Rot_X'):
            ad_lib_lock_hide_attr(lock_hide_channel=['rx'], ctrl=item,
                                  hide_object=value)
        if ad_lib_query_lock_unlock_hide_unhide_channel('Rot_Y'):
            ad_lib_lock_hide_attr(lock_hide_channel=['ry'], ctrl=item,
                                  hide_object=value)
        if ad_lib_query_lock_unlock_hide_unhide_channel('Rot_Z'):
            ad_lib_lock_hide_attr(lock_hide_channel=['rz'], ctrl=item,
                                  hide_object=value)
        if ad_lib_query_lock_unlock_hide_unhide_channel('Scl_X'):
            ad_lib_lock_hide_attr(lock_hide_channel=['sx'], ctrl=item,
                                  hide_object=value)
        if ad_lib_query_lock_unlock_hide_unhide_channel('Scl_Y'):
            ad_lib_lock_hide_attr(lock_hide_channel=['sy'], ctrl=item,
                                  hide_object=value)
        if ad_lib_query_lock_unlock_hide_unhide_channel('Scl_Z'):
            ad_lib_lock_hide_attr(lock_hide_channel=['sz'], ctrl=item,
                                  hide_object=value)
        if ad_lib_query_lock_unlock_hide_unhide_channel('Visibility'):
            ad_lib_lock_hide_attr(lock_hide_channel=['v'], ctrl=item,
                                  hide_object=value)


def ad_lib_query_lock_unlock_hide_unhide_channel(channel_name):
    value = pm.checkBox(channel_name, q=True, value=True)
    return value


def ad_lib_query_list_textfield_object(object_define, *args):
    listing_object = []
    if pm.textField(object_define, q=True, en=True):
        if pm.textField(object_define, q=True, tx=True):
            text = pm.textField(object_define, q=True, tx=True)
            listing = text.split(',')
            set_duplicate = set([x for x in listing if listing.count(x) > 1])
            if set_duplicate:
                for item in list(set_duplicate):
                    om.MGlobal.displayError("'%s' is duplicate object!" % item)
            else:
                for item in listing:
                    listing_object.append(item)
        else:
            om.MGlobal.displayError("'%s' can not be empty!" % object_define)
    else:
        pass

    return listing_object, object_define


def ad_lib_prefix(prefix_text):
    text = pm.textField(prefix_text, q=True, tx=True)
    if pm.textField(prefix_text, q=True, en=True):
        if text:
            return text
        else:
            return ''
    else:
        return ''


def ad_lib_match_position_target_to_ctrl(selection, target, manipulated_position,
                                         manipulated_rotation):
    objects = []
    if '.' in str(selection[0]):
        cls = pm.cluster(selection)
        pm.pointConstraint(cls, target[0], mo=0)
        pm.delete(cls)

        # set attribute rotate jnt
        if manipulated_rotation != (0, 0, 0):
            pm.setAttr(target[0] + '.rotateX', list(manipulated_rotation)[0])
            pm.setAttr(target[0] + '.rotateY', list(manipulated_rotation)[1])
            pm.setAttr(target[0] + '.rotateZ', list(manipulated_rotation)[2])

        # set attribute translate jnt
        if manipulated_position != (0, 0, 0):
            pm.setAttr(target[0] + '.translateX', list(manipulated_position)[0])
            pm.setAttr(target[0] + '.translateY', list(manipulated_position)[1])
            pm.setAttr(target[0] + '.translateZ', list(manipulated_position)[2])
    else:
        for object, tgt in zip(selection, target):
            # query and match
            ad_lib_xform_position_rotation(origin=object, target=tgt)
            objects.append(object.nodeName())

    return objects


def ad_lib_xform_position_rotation(origin, target):
    origin_position = pm.xform(origin, ws=True, q=True, t=True)
    origin_rotation = pm.xform(origin, ws=True, q=True, ro=True)

    # match position
    target_position = pm.xform(target, ws=True, t=origin_position)
    target_rotation = pm.xform(target, ws=True, ro=origin_rotation)

    return {'origin_position': origin_position,
            'origin_rotation': origin_rotation,
            'target_position': target_position,
            'target_rotation': target_rotation
            }


def ad_lib_main_name(main_name):
    if '_' in main_name:
        get_prefix_name = main_name.split('_')[:-1]
        joining = '_'.join(get_prefix_name)
        return joining
    else:
        return main_name


def ad_lib_get_suffix_main(main_name):
    if '_' in main_name:
        get_suffix_name = main_name.split('_')[-1]
    else:
        get_suffix_name = ''
    return get_suffix_name


def ad_lib_defining_object_text_field(define_object, tx='', *args, **kwargs):
    pm.textField(define_object, tx=tx, **kwargs)


def ad_lib_visibility_target(object, target):
    check_box = pm.checkBox('Target_Visibility', q=True, value=True)
    if check_box:
        ad_lib_display(object=object, target=target)
    else:
        pass


def ad_lib_display(object, target, long_name='display', default_vis=1, k=True, cb=False):
    # create attr
    if not pm.objExists(object + '.' + long_name):
        pm.addAttr(object, ln=long_name, at='bool')
    else:
        pass
    pm.setAttr('%s.%s' % (object, long_name), default_vis, e=True, k=k, cb=cb)
    pm.connectAttr('%s.%s' % (object, long_name), target + '.visibility')


def ad_lib_group_parent(groups, name, suffix, prefix_2, prefix_number):
    # create group hierarchy
    grps = []
    for number, group in enumerate(groups):
        grps.append(pm.createNode('transform', n="%s%s%s%s%s_%s" % (
            name, group.title(), suffix.title(), prefix_number, prefix_2, 'grp')))

        if number > 0:
            pm.parent(grps[number], grps[number - 1])

    return grps


def ad_lib_excute_main_ctrl(Prefix_1_Text, Prefix_2_Text, main_name_for_grp, main_name,
                            suffix_text_field, controller_shape):
    main_name_for_grp.append(ad_lib_prefix(Prefix_1_Text) + main_name + suffix_text_field)
    controller_shape_prefix_suffix = pm.rename(controller_shape,
                                               ad_lib_prefix(
                                                   Prefix_1_Text) + main_name + ad_lib_prefix(
                                                   Prefix_2_Text) + suffix_text_field)

    return controller_shape_prefix_suffix


def ad_lib_create_main_ctrl_prefix_suffix_selection(selection, on_selector):
    name_text_enable = ad_lib_text_field_query_enabled('Name_Text')
    name_text_field = ad_lib_text_field_query_text('Name_Text')
    suffix_text_field = ad_lib_text_field_query_text('Suffix_Main')

    controller_shape_prefix_suffix_app = []
    main_name_for_grp = []

    # suffix condition
    if suffix_text_field:
        suffix_text_field = '_' + suffix_text_field
        # condition for selection by vertex
        if '.' in str(selection[0]):
            get_first_object = selection[0].split('Shape')[0]
            query_name_object_select = ad_lib_main_name(get_first_object)
            controller_shape = ad_lib_controller_shape(size_ctrl=1.0, on_selector=on_selector)
            if name_text_enable:
                if name_text_field:
                    controller_shape_prefix_suffix = \
                        ad_lib_excute_main_ctrl(Prefix_1_Text='Prefix_1_Text',
                                                Prefix_2_Text='Prefix_2_Text',
                                                main_name_for_grp=main_name_for_grp,
                                                main_name=name_text_field,
                                                suffix_text_field=suffix_text_field,
                                                controller_shape=controller_shape)
                    controller_shape_prefix_suffix_app.append(controller_shape_prefix_suffix)

                else:
                    controller_shape_prefix_suffix = \
                        ad_lib_excute_main_ctrl(Prefix_1_Text='Prefix_1_Text',
                                                Prefix_2_Text='Prefix_2_Text',
                                                main_name_for_grp=main_name_for_grp,
                                                main_name=query_name_object_select,
                                                suffix_text_field=suffix_text_field,
                                                controller_shape=controller_shape)
                    controller_shape_prefix_suffix_app.append(controller_shape_prefix_suffix)


            else:
                controller_shape_prefix_suffix = \
                    ad_lib_excute_main_ctrl(Prefix_1_Text='Prefix_1_Text',
                                            Prefix_2_Text='Prefix_2_Text',
                                            main_name_for_grp=main_name_for_grp,
                                            main_name=query_name_object_select,
                                            suffix_text_field=suffix_text_field,
                                            controller_shape=controller_shape)
                controller_shape_prefix_suffix_app.append(controller_shape_prefix_suffix)

        # selection by object
        else:
            for number, object in enumerate(selection):
                query_name_object_select = ad_lib_main_name(object)
                controller_shape = ad_lib_controller_shape(size_ctrl=1.0, on_selector=on_selector)
                # condition enable the name text
                if name_text_enable:
                    # condition the name is not empty
                    if name_text_field:
                        # condition selection more than one object
                        if len(selection) > 1:
                            main_name_for_grp.append(
                                '%s%s%02d%s' % (
                                    ad_lib_prefix('Prefix_1_Text'), name_text_field, number + 1, suffix_text_field))
                            controller_shape_prefix_suffix = pm.rename(controller_shape,
                                                                       '%s%s%02d%s%s' % (
                                                                           ad_lib_prefix('Prefix_1_Text'),
                                                                           name_text_field,
                                                                           number + 1,
                                                                           ad_lib_prefix('Prefix_2_Text'),
                                                                           suffix_text_field))
                        else:
                            controller_shape_prefix_suffix = \
                                ad_lib_excute_main_ctrl(Prefix_1_Text='Prefix_1_Text',
                                                        Prefix_2_Text='Prefix_2_Text',
                                                        main_name_for_grp=main_name_for_grp,
                                                        main_name=name_text_field,
                                                        suffix_text_field=suffix_text_field,
                                                        controller_shape=controller_shape)
                        controller_shape_prefix_suffix_app.append(controller_shape_prefix_suffix)

                    else:
                        controller_shape_prefix_suffix = \
                            ad_lib_excute_main_ctrl(Prefix_1_Text='Prefix_1_Text',
                                                    Prefix_2_Text='Prefix_2_Text',
                                                    main_name_for_grp=main_name_for_grp,
                                                    main_name=query_name_object_select,
                                                    suffix_text_field=suffix_text_field,
                                                    controller_shape=controller_shape)

                        controller_shape_prefix_suffix_app.append(controller_shape_prefix_suffix)
                else:
                    controller_shape_prefix_suffix = \
                        ad_lib_excute_main_ctrl(Prefix_1_Text='Prefix_1_Text',
                                                Prefix_2_Text='Prefix_2_Text',
                                                main_name_for_grp=main_name_for_grp,
                                                main_name=query_name_object_select,
                                                suffix_text_field=suffix_text_field,
                                                controller_shape=controller_shape)

                    controller_shape_prefix_suffix_app.append(controller_shape_prefix_suffix)

                    pm.select(cl=1)

        return controller_shape_prefix_suffix_app, main_name_for_grp

    else:
        return om.MGlobal.displayError("'Suffix:' can not be empty!")


def ad_lib_create_main_ctrl_prefix_suffix(on_selector):
    name_text_enable = ad_lib_text_field_query_enabled('Name_Text')
    name_text_field = ad_lib_text_field_query_text('Name_Text')
    suffix_text_field = ad_lib_text_field_query_text('Suffix_Main')

    controller_shape_prefix_suffix_app = []
    main_name_for_grp = []

    if suffix_text_field:
        suffix_text_field = '_' + suffix_text_field

        # condition the name field is enabled
        if name_text_enable:
            # condition if the text is exist
            if name_text_field:
                # create controller shape
                controller_shape = ad_lib_controller_shape(size_ctrl=1.0, on_selector=on_selector)
                # create the name prefix, name, and suffix
                controller_shape_prefix_suffix = pm.rename(controller_shape,
                                                           ad_lib_prefix('Prefix_1_Text') + name_text_field +
                                                           ad_lib_prefix('Prefix_2_Text') + suffix_text_field)
                controller_shape_prefix_suffix_app.append(controller_shape_prefix_suffix)
                main_name_for_grp.append(ad_lib_prefix('Prefix_1_Text') + name_text_field + suffix_text_field)

                pm.select(cl=1)

            else:
                return om.MGlobal.displayError("'Name:' without selection object can not be empty!")

        else:
            controller_shape = ad_lib_controller_shape(size_ctrl=1.0, on_selector=on_selector)
            controller_shape_prefix_suffix = \
                ad_lib_excute_main_ctrl(Prefix_1_Text='Prefix_1_Text',
                                        Prefix_2_Text='Prefix_2_Text',
                                        main_name_for_grp=main_name_for_grp,
                                        main_name=controller_shape,
                                        suffix_text_field=suffix_text_field,
                                        controller_shape=controller_shape)

            controller_shape_prefix_suffix_app.append(controller_shape_prefix_suffix)
            pm.select(cl=1)

        return controller_shape_prefix_suffix_app, main_name_for_grp

    else:
        return om.MGlobal.displayError("'Suffix:' can not be empty!")


def ad_lib_replacing_controller(list_controller):
    instance_controller = list_controller.pop(0)
    for target in list_controller:
        target_shapes = pm.listRelatives(target, s=1)
        instance_query_shapes = pm.listRelatives(instance_controller, s=1)
        if not pm.objectType(target_shapes[0]) == 'nurbsCurve':
            om.MGlobal.displayWarning("%s is not curve type object! Replacing is skipped." % target)

        elif not pm.objectType(instance_query_shapes[0]) == 'nurbsCurve':
            om.MGlobal.displayError("%s is not curve type object!" % instance_controller)

        else:
            instance_shapes = pm.duplicate(instance_controller.getShape(), addShape=True)[0]
            pm.parent(instance_shapes, target, r=True, s=True)

            list_attribute_target_shapes = pm.listAttr(target_shapes, ud=1)
            list_attribute_instance_shapes = pm.listAttr(instance_shapes, ud=1)

            for list_attr_ins_shape in list_attribute_instance_shapes:
                pm.setAttr('%s.%s' % (instance_shapes, list_attr_ins_shape), e=True, l=False)
                pm.deleteAttr('%s.%s' % (instance_shapes, list_attr_ins_shape))

            for attr_tgt_shape in list_attribute_target_shapes:
                get_type_attr = pm.attributeQuery(attr_tgt_shape, n=target_shapes[0], attributeType=True)
                keyable = pm.getAttr('%s.%s' % (target_shapes[0], attr_tgt_shape), k=True)
                channel_box = pm.getAttr('%s.%s' % (target_shapes[0], attr_tgt_shape), cb=True)
                lock = pm.getAttr('%s.%s' % (target_shapes[0], attr_tgt_shape), l=True)

                value_attr = pm.getAttr('%s.%s' % (target_shapes[0], attr_tgt_shape))
                if get_type_attr == 'long' or get_type_attr == 'double':
                    try:
                        range = pm.attributeQuery(attr_tgt_shape, n=target_shapes[0], range=True)
                        pm.addAttr(instance_shapes, ln=attr_tgt_shape, at=get_type_attr, min=range[0], max=range[1])
                    except:
                        pm.addAttr(instance_shapes, ln=attr_tgt_shape, at=get_type_attr)

                    pm.setAttr('%s.%s' % (instance_shapes, attr_tgt_shape), value_attr)
                    pm.setAttr('%s.%s' % (instance_shapes, attr_tgt_shape), e=True, k=keyable, cb=channel_box, l=lock)

                elif get_type_attr == 'typed':
                    pm.addAttr(instance_shapes, ln=attr_tgt_shape, dt="string")
                    if value_attr:
                        pm.setAttr('%s.%s' % (instance_shapes, attr_tgt_shape), value_attr, type='string')
                    pm.setAttr('%s.%s' % (instance_shapes, attr_tgt_shape), e=True, k=keyable, cb=channel_box,
                               l=lock)

                else:
                    pm.addAttr(instance_shapes, ln=attr_tgt_shape, at=get_type_attr)
                    pm.setAttr('%s.%s' % (instance_shapes, attr_tgt_shape), value_attr)
                    pm.setAttr('%s.%s' % (instance_shapes, attr_tgt_shape), e=True, k=keyable, cb=channel_box,
                               l=lock)
            try:
                # connection replace to instance
                list_connections = pm.listConnections(target_shapes, c=True, plugs=True)
                for connection, attr_tgt_shape in zip(list_connections, list_attribute_target_shapes):
                    spliting = connection[0].split('.')
                    new_instance_shape = connection[0].replace(str(spliting[0]), str(instance_shapes))
                    pm.disconnectAttr(connection[0], connection[1])
                    pm.connectAttr(new_instance_shape, connection[1])
            except:
                pass

            # rename the shape
            replacing = instance_shapes.name().replace(str(instance_shapes), str(target_shapes[0]))
            pm.delete(target_shapes)
            instance_shapes.rename(replacing)
            pm.select(cl=1)

    return instance_controller, list_controller


def ad_lib_replacing_color(source, target):
    if not source:
        om.MGlobal.displayError("No curves selected")
        return False

    for obj in target:
        shapeNodes = pm.listRelatives(obj, shapes=True)
        sourceNode = pm.listRelatives(source, shapes=True)[0]
        for shape in shapeNodes:
            try:
                pm.setAttr("{0}.overrideEnabled".format(shape), True)
                pm.setAttr("{0}.overrideEnabled".format(sourceNode), True)
                color_source = pm.getAttr("{0}.overrideColor".format(sourceNode))
                pm.setAttr("{0}.overrideColor".format(shape), color_source)
            except:
                om.MGlobal.displayWarning("Failed to override color: {0}".format(shape))
    return True


def ad_lib_scaling_controller(object, value):
    object_curve = pm.PyNode(object)
    position = ad_lib_average_position(object)

    for cv in object_curve.getShape().cv:
        pm.scale(cv, value, value, value,
                 p=(position[0], position[1], position[2]),
                 r=True)


def ad_lib_attr_value(channel):
    attr_lock_list = []
    for lc in channel:
        if lc in ['t', 'r', 's']:
            for axis in ['x', 'y', 'z']:
                at = lc + axis
                attr_lock_list.append(at)
        else:
            attr_lock_list.append(lc)
    return attr_lock_list


def ad_lib_hide_unhide_attr(channel, ctrl):
    attr_lock_list = ad_lib_attr_value(channel)
    for at in attr_lock_list:
        query_object_hide = pm.getAttr(ctrl + '.' + at, k=True)
        if query_object_hide:
            pm.setAttr(ctrl + '.' + at, k=False)
        else:
            pm.setAttr(ctrl + '.' + at, k=True)
    return attr_lock_list


def ad_lib_lock_unlock_attr(channel, ctrl):
    attr_lock_list = ad_lib_attr_value(channel)
    for at in attr_lock_list:
        query_object_lock = pm.getAttr(ctrl + '.' + at, l=True)
        if query_object_lock:
            pm.setAttr(ctrl + '.' + at, l=False)
        else:
            pm.setAttr(ctrl + '.' + at, l=True)
    return attr_lock_list


def ad_lib_lock_hide_attr(lock_hide_channel, ctrl, hide_object, **kwargs):
    attr_lock_list = ad_lib_attr_value(lock_hide_channel)
    for at in attr_lock_list:
        if hide_object:
            pm.setAttr(ctrl + '.' + at, l=1, k=0, **kwargs)
        else:
            pm.setAttr(ctrl + '.' + at, l=0, k=1, **kwargs)

    return attr_lock_list


def ad_lib_ctrl_color_list(color):
    selection = pm.ls(selection=True)
    if not selection:
        om.MGlobal.displayError("No curves selected")
        return False
    else:
        for obj in selection:
            shapeNodes = pm.listRelatives(obj, shapes=True)[0]
            if not pm.objectType(shapeNodes) == 'nurbsCurve':
                pass
            else:
                try:
                    pm.setAttr("{0}.overrideEnabled".format(shapeNodes), True)
                    pm.setAttr("{0}.overrideColor".format(shapeNodes), color)
                except:
                    om.MGlobal.displayWarning("Failed to override color: {0}".format(shapeNodes))
    return True


def ad_lib_query_user_defined_channel(ctrl):
    list_attr = pm.listAttr(ctrl, ud=1)
    if 'AD_Controller' in list_attr:
        list_attr.remove('AD_Controller')
        return list_attr
    else:
        return list_attr


def ad_lib_ctrl_color(ctrl, color):
    # list_relatives = []
    # for item in ctrl:
    list_relatives = ctrl.getShape()
    pm.setAttr(list_relatives + '.ove', 1)
    pm.setAttr(list_relatives + '.ovc', color)

    return list_relatives


def ad_lib_get_number_main_name(main_name):
    try:
        patterns = [r'\d+']
        name_number = ad_lib_main_name(main_name)
        for p in patterns:
            name_number = re.findall(p, name_number)[0]
    except:
        name_number = ''

    # get the prefix without number
    ad_main_name = str(ad_lib_main_name(main_name)).translate(None, digits)

    return name_number, ad_main_name


def ad_lib_shape_controller(shape, size_ctrl, tag_number):
    scale_shape = [[size_ctrl * i for i in j] for j in shape]
    curve = pm.curve(d=1, p=scale_shape)
    create_curve = curve.getShape()
    pm.addAttr(create_curve, ln='AD_Controller', at='bool')
    pm.setAttr(create_curve + '.AD_Controller', 1)
    ad_lib_tagging_controller_code(create_curve, tag_number)

    return curve


def ad_lib_tagging_controller_code(ctrl, tag_number):
    pm.addAttr(ctrl, ln='AD_Controller_Tag', at='long')
    pm.setAttr(ctrl + '.AD_Controller_Tag', tag_number, l=True)


def ad_lib_tagging(ctrl):
    attributes = pm.attributeQuery('AD_Controller', n=ctrl, ex=True)
    if attributes:
        pm.setAttr(ctrl + '.AD_Controller', 1)
    else:
        pm.addAttr(ctrl, ln='AD_Controller', at='bool')
        pm.setAttr(ctrl + '.AD_Controller', 1)


def ad_lib_untagging(ctrl):
    attributes = pm.attributeQuery('AD_Controller', n=ctrl, ex=True)
    if attributes:
        pm.setAttr(ctrl + '.AD_Controller', 0)
    else:
        pm.addAttr(ctrl, ln='AD_Controller', at='bool')
        pm.setAttr(ctrl + '.AD_Controller', 0)


def ad_lib_controller_shape(size_ctrl, on_selector, *args):
    control_shape = []
    if on_selector == 1:
        control_shape = ad_lib_shape_controller(CIRCLE, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 2:
        control_shape = ad_lib_shape_controller(LOCATOR, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 3:
        control_shape = ad_lib_shape_controller(CUBE, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 4:
        control_shape = ad_lib_shape_controller(CIRCLEHALF, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 5:
        control_shape = ad_lib_shape_controller(SQUARE, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 6:
        control_shape = ad_lib_shape_controller(JOINT, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 7:
        control_shape = ad_lib_shape_controller(CAPSULE, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 8:
        control_shape = ad_lib_shape_controller(STICKCIRCLE, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 9:
        control_shape = ad_lib_shape_controller(CIRCLEPLUSHALF, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 10:
        control_shape = ad_lib_shape_controller(CIRCLEPLUS, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 11:
        control_shape = ad_lib_shape_controller(STICK2CIRCLE, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 12:
        control_shape = ad_lib_shape_controller(STICKSQUARE, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 13:
        control_shape = ad_lib_shape_controller(STICK2SQUARE, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 14:
        control_shape = ad_lib_shape_controller(STICKSTAR, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 15:
        control_shape = ad_lib_shape_controller(CIRCLEPLUSARROW, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 16:
        control_shape = ad_lib_shape_controller(RECTANGLE, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 17:
        control_shape = ad_lib_shape_controller(ARROW, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 18:
        control_shape = ad_lib_shape_controller(ARROW3DFLAT, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 19:
        control_shape = ad_lib_shape_controller(ARROW2HALFCIRCULAR, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 20:
        control_shape = ad_lib_shape_controller(ARROW2STRAIGHT, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 21:
        control_shape = ad_lib_shape_controller(ARROW2FLAT, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 22:
        control_shape = ad_lib_shape_controller(ARROWHEAD, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 23:
        control_shape = ad_lib_shape_controller(ARROW90DEG, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 24:
        control_shape = ad_lib_shape_controller(SQUAREPLUS, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 25:
        control_shape = ad_lib_shape_controller(JOINTPLUS, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 26:
        control_shape = ad_lib_shape_controller(HAND, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 27:
        control_shape = ad_lib_shape_controller(ARROWCIRCULAR, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 28:
        control_shape = ad_lib_shape_controller(PLUS, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 29:
        control_shape = ad_lib_shape_controller(PIVOT, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 30:
        control_shape = ad_lib_shape_controller(KEYS, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 31:
        control_shape = ad_lib_shape_controller(PYRAMIDCIRCLE, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 32:
        control_shape = ad_lib_shape_controller(ARROW4CIRCULAR, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 33:
        control_shape = ad_lib_shape_controller(EYES, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 34:
        control_shape = ad_lib_shape_controller(FOOTSTEP, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 35:
        control_shape = ad_lib_shape_controller(HALF3DCIRCLE, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 36:
        control_shape = ad_lib_shape_controller(CAPSULECURVE, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 37:
        control_shape = ad_lib_shape_controller(ARROW4STRAIGHT, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 38:
        control_shape = ad_lib_shape_controller(ARROW3D, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 39:
        control_shape = ad_lib_shape_controller(PYRAMID, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 40:
        control_shape = ad_lib_shape_controller(ARROW3DCIRCULAR, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 41:
        control_shape = ad_lib_shape_controller(CYLINDER, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 42:
        control_shape = ad_lib_shape_controller(ARROW2FLATHALF, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 43:
        control_shape = ad_lib_shape_controller(FLAG, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 44:
        control_shape = ad_lib_shape_controller(WORLD, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 45:
        control_shape = ad_lib_shape_controller(SETUP, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 46:
        control_shape = ad_lib_shape_controller(STAR, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 47:
        control_shape = ad_lib_shape_controller(DIAMOND, size_ctrl=size_ctrl, tag_number=on_selector)
    elif on_selector == 48:
        control_shape = ad_lib_shape_controller(STARSQUEEZE, size_ctrl=size_ctrl, tag_number=on_selector)
    else:
        pass
    return control_shape


CIRCLEPLUS = [[1.1300200000000005, -4.996003610813204e-16, 0.0], [1.00412, 1.1102230246251565e-16, 0.0],
              [0.99176, -8.326672684688674e-17, -0.15708], [0.9549800000000004, -2.498001805406602e-16, -0.31029],
              [0.8946800000000001, -2.220446049250313e-16, -0.45586], [0.8123499999999997, 0.0, -0.59021],
              [0.7100200000000002, -1.3877787807814457e-16, -0.71002],
              [0.5902100000000001, -3.885780586188048e-16, -0.81235],
              [0.45586000000000004, -5.551115123125783e-17, -0.89468],
              [0.3102900000000001, -1.5265566588595902e-16, -0.95498], [0.15708, -1.3877787807814457e-17, -0.99176],
              [0.0, 0.0, -1.00412], [0.0, 0.0, -1.13002], [0.0, 0.0, -1.00412],
              [-0.15708, 1.3877787807814457e-17, -0.99176], [-0.3102900000000001, 1.5265566588595902e-16, -0.95498],
              [-0.45586000000000004, 5.551115123125783e-17, -0.89468],
              [-0.5902100000000001, 3.885780586188048e-16, -0.81235],
              [-0.7100200000000002, 1.3877787807814457e-16, -0.71002], [-0.8123499999999997, 0.0, -0.59021],
              [-0.8946800000000001, 2.220446049250313e-16, -0.45586],
              [-0.9549800000000004, 2.498001805406602e-16, -0.31029], [-0.99176, 8.326672684688674e-17, -0.15708],
              [-1.00412, -1.1102230246251565e-16, 0.0], [-1.1300200000000005, 4.996003610813204e-16, 0.0],
              [-1.00412, -1.1102230246251565e-16, 0.0], [-0.99176, 8.326672684688674e-17, 0.15708],
              [-0.9549800000000004, 2.498001805406602e-16, 0.31029],
              [-0.8946800000000001, 2.220446049250313e-16, 0.45586], [-0.8123499999999997, 0.0, 0.59021],
              [-0.7100200000000002, 1.3877787807814457e-16, 0.71002],
              [-0.5902100000000001, 3.885780586188048e-16, 0.81235],
              [-0.45586000000000004, 5.551115123125783e-17, 0.89468],
              [-0.3102900000000001, 1.5265566588595902e-16, 0.95498], [-0.15708, 1.3877787807814457e-17, 0.99176],
              [0.0, 0.0, 1.00412], [0.0, 0.0, 1.13002], [0.0, 0.0, 1.00412],
              [0.15708, -1.3877787807814457e-17, 0.99176], [0.3102900000000001, -1.5265566588595902e-16, 0.95498],
              [0.45586000000000004, -5.551115123125783e-17, 0.89468],
              [0.5902100000000001, -3.885780586188048e-16, 0.81235],
              [0.7100200000000002, -1.3877787807814457e-16, 0.71002], [0.8123499999999997, 0.0, 0.59021],
              [0.8946800000000001, -2.220446049250313e-16, 0.45586],
              [0.9549800000000004, -2.498001805406602e-16, 0.31029], [0.99176, -8.326672684688674e-17, 0.15708],
              [1.00412, 1.1102230246251565e-16, 0.0], [1.1300200000000005, -4.996003610813204e-16, 0.0],
              [1.00412, 1.1102230246251565e-16, 0.0]]
CIRCLEPLUSHALF = [[1.1300200000000005, -4.996003610813204e-16, 0.0], [1.00412, 1.1102230246251565e-16, 0.0],
                  [0.99176, -8.326672684688674e-17, -0.15708], [0.9549800000000004, -2.498001805406602e-16, -0.31029],
                  [0.8946800000000001, -2.220446049250313e-16, -0.45586], [0.8123499999999997, 0.0, -0.59021],
                  [0.7100200000000002, -1.3877787807814457e-16, -0.71002],
                  [0.5902100000000001, -3.885780586188048e-16, -0.81235],
                  [0.45586000000000004, -5.551115123125783e-17, -0.89468],
                  [0.3102900000000001, -1.5265566588595902e-16, -0.95498], [0.15708, -1.3877787807814457e-17, -0.99176],
                  [0.0, 0.0, -1.00412], [0.0, 0.0, -1.13002], [0.0, 0.0, -1.00412],
                  [-0.15708, 1.3877787807814457e-17, -0.99176], [-0.3102900000000001, 1.5265566588595902e-16, -0.95498],
                  [-0.45586000000000004, 5.551115123125783e-17, -0.89468],
                  [-0.5902100000000001, 3.885780586188048e-16, -0.81235],
                  [-0.7100200000000002, 1.3877787807814457e-16, -0.71002], [-0.8123499999999997, 0.0, -0.59021],
                  [-0.8946800000000001, 2.220446049250313e-16, -0.45586],
                  [-0.9549800000000004, 2.498001805406602e-16, -0.31029], [-0.99176, 8.326672684688674e-17, -0.15708],
                  [-1.00412, -1.1102230246251565e-16, 0.0], [-1.1300200000000005, 4.996003610813204e-16, 0.0],
                  [-1.00412, -1.1102230246251565e-16, 0.0], [1.00412, 1.1102230246251565e-16, 0.0],
                  [1.1300200000000005, -4.996003610813204e-16, 0.0], [1.00412, 1.1102230246251565e-16, 0.0]]
CIRCLE = [[1.006715677346795, 3.694760765503359e-15, -0.0006702548752642523],
          [0.9942995854608142, 3.5088838630265848e-15, -0.15846311195050422],
          [0.957352671256412, 3.462414637407381e-15, -0.312368406275037],
          [0.8967790190942225, 3.230068509311403e-15, -0.4585990289160014],
          [0.8140753908601714, 3.462414637407381e-15, -0.5935587331944481],
          [0.7112809990565734, 3.485649250216984e-15, -0.7139124523578334],
          [0.5909272798931885, 3.4391800245977835e-15, -0.8167068441614338],
          [0.45596757561474005, 3.485649250216984e-15, -0.8994104723954812],
          [0.309736952973776, 3.5088838630265848e-15, -0.9599841245576726],
          [0.15583165864924373, 3.5030752098241864e-15, -0.9969310387620735],
          [-0.001961198425996145, 3.5088838630265848e-15, -1.009347130648053],
          [-0.15975405550123625, 3.51469251622898e-15, -0.9969310387620735],
          [-0.31365934982576843, 3.578587701455366e-15, -0.9599841245576726],
          [-0.45988997246673363, 3.578587701455366e-15, -0.8994104723954812],
          [-0.59484967674518, 3.2533031221210005e-15, -0.8167068441614338],
          [-0.7152033959085659, 3.4159454117881866e-15, -0.7139124523578334],
          [-0.8179977877121639, 3.6482915398841665e-15, -0.5935587331944481],
          [-0.9007014159462143, 3.3694761861689905e-15, -0.4585990289160014],
          [-0.9612750681084048, 3.3230069605498e-15, -0.312368406275037],
          [-0.9982219823128072, 3.4159454117881866e-15, -0.15846311195050422],
          [-1.0106380741987873, 3.462414637407381e-15, -0.0006702548752642523],
          [-0.9982219823128072, 3.4159454117881866e-15, 0.1571226021999758],
          [-0.9612750681084048, 3.3230069605498e-15, 0.31102789652450846],
          [-0.9007014159462143, 3.3694761861689905e-15, 0.45725851916547183],
          [-0.8179977877121639, 3.6482915398841665e-15, 0.5922182234439195],
          [-0.7152033959085659, 3.4159454117881866e-15, 0.7125719426073052],
          [-0.59484967674518, 3.2533031221210005e-15, 0.8153663344109039],
          [-0.45988997246673363, 3.578587701455366e-15, 0.8980699626449535],
          [-0.31365934982576843, 3.578587701455366e-15, 0.9586436148071452],
          [-0.15975405550123625, 3.51469251622898e-15, 0.9955905290115455],
          [-0.001961198425996145, 3.5088838630265848e-15, 1.008006620897526],
          [0.15583165864924373, 3.5030752098241864e-15, 0.9955905290115455],
          [0.309736952973776, 3.5088838630265848e-15, 0.9586436148071452],
          [0.45596757561474005, 3.485649250216984e-15, 0.8980699626449535],
          [0.5909272798931885, 3.4391800245977835e-15, 0.8153663344109039],
          [0.7112809990565734, 3.485649250216984e-15, 0.7125719426073052],
          [0.8140753908601714, 3.462414637407381e-15, 0.5922182234439195],
          [0.8967790190942225, 3.230068509311403e-15, 0.45725851916547183],
          [0.957352671256412, 3.462414637407381e-15, 0.31102789652450846],
          [0.9942995854608142, 3.5088838630265848e-15, 0.1571226021999758],
          [1.006715677346795, 3.694760765503359e-15, -0.0006702548752642523]]
CIRCLEHALF = [[1.006715677346795, 3.694760765503359e-15, -0.0006702548752642523],
              [0.9942995854608142, 3.5088838630265848e-15, -0.15846311195050422],
              [0.957352671256412, 3.462414637407381e-15, -0.312368406275037],
              [0.8967790190942225, 3.230068509311403e-15, -0.4585990289160014],
              [0.8140753908601714, 3.462414637407381e-15, -0.5935587331944481],
              [0.7112809990565734, 3.485649250216984e-15, -0.7139124523578334],
              [0.5909272798931885, 3.4391800245977835e-15, -0.8167068441614338],
              [0.45596757561474005, 3.485649250216984e-15, -0.8994104723954812],
              [0.309736952973776, 3.5088838630265848e-15, -0.9599841245576726],
              [0.15583165864924373, 3.5030752098241864e-15, -0.9969310387620735],
              [-0.001961198425996145, 3.5088838630265848e-15, -1.009347130648053],
              [-0.15975405550123625, 3.51469251622898e-15, -0.9969310387620735],
              [-0.31365934982576843, 3.578587701455366e-15, -0.9599841245576726],
              [-0.45988997246673363, 3.578587701455366e-15, -0.8994104723954812],
              [-0.59484967674518, 3.2533031221210005e-15, -0.8167068441614338],
              [-0.7152033959085659, 3.4159454117881866e-15, -0.7139124523578334],
              [-0.8179977877121639, 3.6482915398841665e-15, -0.5935587331944481],
              [-0.9007014159462143, 3.3694761861689905e-15, -0.4585990289160014],
              [-0.9612750681084048, 3.3230069605498e-15, -0.312368406275037],
              [-0.9982219823128072, 3.4159454117881866e-15, -0.15846311195050422],
              [-1.0106380741987873, 3.462414637407381e-15, -0.0006702548752642523],
              [1.006715677346795, 3.694760765503359e-15, -0.0006702548752642523]]
SQUAREPLUS = [[-1.12558, 0.0, 0.0], [-1.0, 0.0, 0.0], [-1.0, 0.0, -1.0], [0.0, 0.0, -1.0], [0.0, 0.0, -1.12558],
              [0.0, 0.0, -1.0], [1.0, 0.0, -1.0], [1.0, 0.0, 0.0], [1.12558, 0.0, 0.0], [1.0, 0.0, 0.0],
              [1.0, 0.0, 1.0], [0.0, 0.0, 1.0], [0.0, 0.0, 1.12558], [0.0, 0.0, 1.0], [-1.0, 0.0, 1.0],
              [-1.0, 0.0, 0.0], [-1.12558, 0.0, 0.0], [-1.0, 0.0, 0.0]]
SQUARE = [[-1.0, 0.0, -1.0], [-1.0, 0.0, 1.0],
          [1.0, 0.0, 1.0], [1.0, 0.0, -1.0], [-1.0, 0.0, -1.0]]  #
CAPSULE = [[-2.011490000000007, 0.0, 0.0], [-1.977020000000007, -2.7755575615628914e-17, -0.26179],
           [-1.875970000000007, -5.551115123125783e-17, -0.50574],
           [-1.7152300000000071, 5.551115123125783e-17, -0.71523],
           [-1.5057400000000072, -2.7755575615628914e-17, -0.8759700000000001],
           [-1.261790000000007, -8.326672684688674e-17, -0.9770199999999998],
           [-1.000000000000007, 2.220446049250313e-16, -1.01149], [0.9999999999999929, 2.220446049250313e-16, -1.01149],
           [1.2617899999999929, -8.326672684688674e-17, -0.9770199999999998],
           [1.505739999999993, -2.7755575615628914e-17, -0.8759700000000001],
           [1.715229999999993, 5.551115123125783e-17, -0.71523], [1.8759699999999928, -5.551115123125783e-17, -0.50574],
           [1.977019999999993, -2.7755575615628914e-17, -0.26179], [2.0114899999999927, 0.0, 0.0],
           [1.977019999999993, 2.7755575615628914e-17, 0.26179], [1.8759699999999928, 5.551115123125783e-17, 0.50574],
           [1.715229999999993, -5.551115123125783e-17, 0.71523],
           [1.505739999999993, 2.7755575615628914e-17, 0.8759700000000001],
           [1.2617899999999929, 8.326672684688674e-17, 0.9770199999999998],
           [0.9999999999999929, -2.220446049250313e-16, 1.01149], [-1.000000000000007, -2.220446049250313e-16, 1.01149],
           [-1.261790000000007, 8.326672684688674e-17, 0.9770199999999998],
           [-1.5057400000000072, 2.7755575615628914e-17, 0.8759700000000001],
           [-1.7152300000000071, -5.551115123125783e-17, 0.71523], [-1.875970000000007, 5.551115123125783e-17, 0.50574],
           [-1.977020000000007, 2.7755575615628914e-17, 0.26179], [-2.011490000000007, 0.0, 0.0]]
STICKCIRCLE = [[1.3793950895567024, -3.44631117065615e-17, 0.0], [1.383213207759879, 0.04857391353114386, 0.0],
               [1.3945682292129031, 0.09594962086194145, 0.0], [1.4131807794131042, 0.14096616572573542, 0.0],
               [1.4385976508339267, 0.18250605011184037, 0.0], [1.4701855946026443, 0.21955731748835713, 0.0],
               [1.5071747787563459, 0.25120113615761036, 0.0], [1.548646371597353, 0.2766614658344029, 0.0],
               [1.5935884165937675, 0.2953050576460113, 0.0], [1.6408834157349044, 0.30667870406588055, 0.0],
               [1.6893766210763885, 0.310503030591339, 0.0], [1.6893766210763885, 0.310503030591339, 0.0],
               [1.7378698264178718, 0.3066787040658806, 0.0], [1.7851648255590074, 0.29530505764601134, 0.0],
               [1.8301068705554226, 0.2766614658344029, 0.0], [1.8715784633964316, 0.25120113615761047, 0.0],
               [1.9085676475501336, 0.219557317488357, 0.0], [1.940155591318851, 0.18250605011184062, 0.0],
               [1.965572462739672, 0.14096616572573528, 0.0], [1.9841850129398715, 0.09594962086194124, 0.0],
               [1.995540034392897, 0.04857391353114411, 0.0], [1.9993581525960722, 0.0, 0.0],
               [1.9993581525960722, 0.0, 0.0], [1.995540034392897, -0.04857391353114392, 0.0],
               [1.984185012939871, -0.09594962086194118, 0.0], [1.965572462739672, -0.14096616572573528, 0.0],
               [1.9401555913188497, -0.18250605011184026, 0.0], [1.9085676475501334, -0.21955731748835688, 0.0],
               [1.8715784633964316, -0.25120113615761036, 0.0], [1.8301068705554226, -0.27666146583440276, 0.0],
               [1.785164825559008, -0.29530505764601134, 0.0], [1.7378698264178718, -0.30667870406588055, 0.0],
               [1.6893766210763885, -0.310503030591339, 0.0], [1.6893766210763885, -0.310503030591339, 0.0],
               [1.6408834157349044, -0.3066787040658804, 0.0], [1.5935884165937675, -0.29530505764601106, 0.0],
               [1.548646371597353, -0.2766614658344029, 0.0], [1.5071747787563454, -0.25120113615761025, 0.0],
               [1.4701855946026452, -0.219557317488357, 0.0], [1.4385976508339267, -0.18250605011184032, 0.0],
               [1.4131807794131042, -0.14096616572573542, 0.0], [1.3945682292129031, -0.09594962086194135, 0.0],
               [1.383213207759879, -0.04857391353114392, 0.0], [1.3793950895567024, -3.44631117065615e-17, 0.0],
               [0.0034473407341919934, 0.0, 0.0]]
STICK2SQUARE = [[-1.37962, 0.0, 0.0], [-1.38011, 0.31012, 0.0], [-1.69023, 0.31012, 0.0],
                [-1.69023, 0.31012, 0.0], [-2.00035, 0.31012, 0.0], [-2.00035, 0.0, 0.0], [-2.00035, 0.0, 0.0],
                [-2.00035, -0.31012, 0.0], [-1.69023, -0.31012, 0.0], [-1.69023, -0.31012, 0.0],
                [-1.38011, -0.31012, 0.0], [-1.37962, 0.0, 0.0], [0.0, 0.0, 0.0], [1.37962, 0.0, 0.0],
                [1.38011, 0.31012, 0.0], [1.69023, 0.31012, 0.0], [1.69023, 0.31012, 0.0], [2.00035, 0.31012, 0.0],
                [2.00035, 0.0, 0.0], [2.00035, 0.0, 0.0], [2.00035, -0.31012, 0.0], [1.69023, -0.31012, 0.0],
                [1.69023, -0.31012, 0.0], [1.38011, -0.31012, 0.0], [1.37962, 0.0, 0.0]]

STICKSQUARE = [[2.8399564837671026e-15, 0.0, 0.0], [1.3800105877892714, -2.524080871237907e-16, 0.0],
               [1.3800105877892714, -0.3098272227100781, 0.0], [2.000361849527144, -0.30982722271007784, 0.0],
               [2.000361849527145, 0.3107409180836937, 0.0], [1.3800105877892714, 0.31074091808369364, 0.0],
               [1.3800105877892714, -2.524080871237907e-16, 0.0]]
STICK2CIRCLE = [[-1.37962, 0.0, 0.0], [-1.38343, 0.04855, 0.0], [-1.39478, 0.09591, 0.0], [-1.41339, 0.14091, 0.0],
                [-1.4388, 0.18244, 0.0], [-1.47037, 0.21947, 0.0], [-1.50735, 0.2511, 0.0], [-1.54881, 0.27655, 0.0],
                [-1.59373, 0.29519, 0.0], [-1.64101, 0.30656, 0.0], [-1.68948, 0.31038, 0.0], [-1.68948, 0.31038, 0.0],
                [-1.73795, 0.30656, 0.0], [-1.78523, 0.29519, 0.0], [-1.83015, 0.27655, 0.0], [-1.87161, 0.2511, 0.0],
                [-1.90858, 0.21947, 0.0], [-1.94016, 0.18244, 0.0], [-1.96556, 0.14091, 0.0], [-1.98417, 0.09591, 0.0],
                [-1.99552, 0.04855, 0.0], [-1.99934, 0.0, 0.0], [-1.99934, 0.0, 0.0], [-1.99552, -0.04855, 0.0],
                [-1.98417, -0.09591, 0.0], [-1.96556, -0.14091, 0.0], [-1.94016, -0.18244, 0.0],
                [-1.90858, -0.21947, 0.0],
                [-1.87161, -0.2511, 0.0], [-1.83015, -0.27655, 0.0], [-1.78523, -0.29519, 0.0],
                [-1.73795, -0.30656, 0.0],
                [-1.68948, -0.31038, 0.0], [-1.68948, -0.31038, 0.0], [-1.64101, -0.30656, 0.0],
                [-1.59373, -0.29519, 0.0],
                [-1.54881, -0.27655, 0.0], [-1.50735, -0.2511, 0.0], [-1.47037, -0.21947, 0.0],
                [-1.4388, -0.18244, 0.0],
                [-1.41339, -0.14091, 0.0], [-1.39478, -0.09591, 0.0], [-1.38343, -0.04855, 0.0], [-1.37962, 0.0, 0.0],
                [0.0, 0.0, 0.0], [1.37962, 0.0, 0.0], [1.38343, 0.04855, 0.0], [1.39478, 0.09591, 0.0],
                [1.41339, 0.14091, 0.0], [1.4388, 0.18244, 0.0], [1.47037, 0.21947, 0.0], [1.50735, 0.2511, 0.0],
                [1.54881, 0.27655, 0.0], [1.59373, 0.29519, 0.0], [1.64101, 0.30656, 0.0], [1.68948, 0.31038, 0.0],
                [1.68948, 0.31038, 0.0], [1.73795, 0.30656, 0.0], [1.78523, 0.29519, 0.0], [1.83015, 0.27655, 0.0],
                [1.87161, 0.2511, 0.0], [1.90858, 0.21947, 0.0], [1.94016, 0.18244, 0.0], [1.96556, 0.14091, 0.0],
                [1.98417, 0.09591, 0.0], [1.99552, 0.04855, 0.0], [1.99934, 0.0, 0.0], [1.99934, 0.0, 0.0],
                [1.99552, -0.04855, 0.0], [1.98417, -0.09591, 0.0], [1.96556, -0.14091, 0.0], [1.94016, -0.18244, 0.0],
                [1.90858, -0.21947, 0.0], [1.87161, -0.2511, 0.0], [1.83015, -0.27655, 0.0], [1.78523, -0.29519, 0.0],
                [1.73795, -0.30656, 0.0], [1.68948, -0.31038, 0.0], [1.68948, -0.31038, 0.0], [1.64101, -0.30656, 0.0],
                [1.59373, -0.29519, 0.0], [1.54881, -0.27655, 0.0], [1.50735, -0.2511, 0.0], [1.47037, -0.21947, 0.0],
                [1.4388, -0.18244, 0.0], [1.41339, -0.14091, 0.0], [1.39478, -0.09591, 0.0], [1.38343, -0.04855, 0.0],
                [1.37962, 0.0, 0.0]]

RECTANGLE = [[-1.4910668771146764, 0.0, -0.9940445847431187], [1.4910668771146764, 0.0, -0.9940445847431187],
             [1.4910668771146764, 0.0, 0.9940445847431187], [-1.4910668771146764, 0.0, 0.9940445847431187],
             [-1.4910668771146764, 0.0, -0.9940445847431187]]
ARROW = [[-0.9983087545713453, 0.0, -0.3975562882738118], [0.20582257977725307, 0.0, -0.3975562882738118],
         [0.20582257977725307, 0.0, -0.7951123794385018], [1.0009349592157541, 0.0, 0.0],
         [0.20582257977725307, 0.0, 0.7951123794385018], [0.20582257977725307, 0.0, 0.3975562882738118],
         [-0.9983087545713453, 0.0, 0.3975562882738118], [-0.9983087545713453, 0.0, -0.3975562882738118]]
ARROWCIRCULAR = [[-0.7000356, 0.0, 0.7000356], [-0.80110437, 0.0, 0.58087227], [-0.88155639, 0.0, 0.44819412],
                 [-0.9414530400000001, 0.0, 0.30282549000000003], [-0.9767831699999999, 0.0, 0.15827823],
                 [-0.9899973600000002, 0.0, 0.0021554049], [-0.9781780800000001, 0.0, -0.14967645],
                 [-0.9369165300000001, 0.0, -0.31648518], [-0.8816666099999999, 0.0, -0.44797632],
                 [-0.803088, 0.0, -0.5781002700000001], [-0.7032276900000001, 0.0, -0.69682833],
                 [-0.59164281, 0.0, -0.79325763], [-0.45802812000000004, 0.0, -0.87651762],
                 [-0.31100454, 0.0, -0.9387625500000001], [-0.15359025, 0.0, -0.97755306],
                 [0.0027721055999999997, 0.0, -0.98999604], [0.15012987, 0.0, -0.9781064700000001],
                 [0.31076067, 0.0, -0.93884373], [0.44531553, 0.0, -0.88300608], [0.57991857, 0.0, -0.80178846],
                 [0.70253106, 0.0, -0.6975309], [0.7957326299999999, 0.0, -0.5882784600000001],
                 [0.8782583699999998, 0.0, -0.45466047], [0.9398165700000001, 0.0, -0.30782796],
                 [0.97708149, 0.0, -0.15647841], [0.98999967, 0.0, 0.0005587527000000001],
                 [0.97836321, 0.0, 0.14849538], [0.94122468, 0.0, 0.30352971],
                 [0.8828107199999998, 0.0, 0.44570459999999995], [0.8024372399999999, 0.0, 0.57901173],
                 [0.70110645, 0.0, 0.6989631], [0.5853929400000001, 0.0, 0.79783803],
                 [0.45298638, 0.0, 0.8791176900000001], [0.30485433, 0.0, 0.9407927100000001],
                 [0.13497198, 0.0, 0.9803818200000001], [0.0, 0.0, 0.9899999999999999],
                 [0.20467359, 0.19567185, 0.9899999999999999], [-0.33, 0.0, 0.9899999999999999],
                 [0.20467359, -0.19567185, 0.9899999999999999], [0.0, 0.0, 0.9899999999999999],
                 [0.20467359, 0.0, 0.7943281500000001], [-0.33, 0.0, 0.9899999999999999], [0.20467359, 0.0, 1.18567185],
                 [0.0, 0.0, 0.9899999999999999]]
ARROW2HALFCIRCULAR = [[-1.000689920099012, 0.0, 0.5229957143185117],
                      [-1.0654162009368167, 0.0647260096091361, 0.08206631880509213],
                      [-0.9359639104898756, 0.0647260096091361, 0.08206631880509213],
                      [-1.000689920099012, 0.0, 0.5229957143185117],
                      [-0.9359639104898756, 0.0647260096091361, 0.08206631880509213],
                      [-0.9359639104898756, -0.0647260096091361, 0.08206631880509213],
                      [-1.000689920099012, 0.0, 0.5229957143185117],
                      [-0.9359639104898756, -0.0647260096091361, 0.08206631880509213],
                      [-1.0654162009368167, -0.0647260096091361, 0.08206631880509213],
                      [-1.000689920099012, 0.0, 0.5229957143185117],
                      [-1.0654162009368167, 0.0647260096091361, 0.08206631880509213],
                      [-1.0654162009368167, -0.0647260096091361, 0.08206631880509213],
                      [-1.000689920099012, 0.0, 0.5229957143185117], [-1.000689920099012, 0.0, -0.0007416924911552399],
                      [-0.9756191692935681, 0.0, -0.2232511831846876], [-0.90166406175881, 0.0, -0.43460314011484735],
                      [-0.7825328358595425, 0.0, -0.6241993030340791], [-0.6241993030340834, 0.0, -0.7825328358595391],
                      [-0.4346031401148514, 0.0, -0.9016640617588073], [-0.22325118318469103, 0.0, -0.9756191692935652],
                      [-0.0007416924911588084, 0.0, -1.0006899200990096],
                      [0.5229957143185071, 0.0, -1.0006899200990096],
                      [0.08206631880508854, 0.0647260096091361, -0.935963910489872],
                      [0.08206631880508854, 0.0647260096091361, -1.065416200936811],
                      [0.5229957143185071, 0.0, -1.0006899200990096],
                      [0.08206631880508854, 0.0647260096091361, -1.065416200936811],
                      [0.08206631880508854, -0.0647260096091361, -1.065416200936811],
                      [0.5229957143185071, 0.0, -1.0006899200990096],
                      [0.08206631880508854, -0.0647260096091361, -0.935963910489872],
                      [0.08206631880508854, -0.0647260096091361, -1.065416200936811],
                      [0.08206631880508854, -0.0647260096091361, -0.935963910489872],
                      [0.08206631880508854, 0.0647260096091361, -0.935963910489872]]
ARROW2STRAIGHT = [[-0.7677315461266506, -0.10046175256545777, -0.10046175256545777],
                  [-0.7677315461266506, -0.10046175256545777, 0.10046175256545777],
                  [-0.7677315461266506, 0.10046175256545777, 0.10046175256545777],
                  [-0.7677315461266506, 0.10046175256545777, -0.10046175256545777],
                  [-0.7677315461266506, -0.10046175256545777, -0.10046175256545777], [-0.9996431901055894, 0.0, 0.0],
                  [-0.7677315461266506, -0.10046175256545777, 0.10046175256545777],
                  [-0.7677315461266506, 0.10046175256545777, 0.10046175256545777], [-0.9996431901055894, 0.0, 0.0],
                  [-0.7677315461266506, 0.10046175256545777, -0.10046175256545777], [-0.9996431901055894, 0.0, 0.0],
                  [0.0, 0.0, 0.0], [0.9996431901055894, 0.0, 0.0],
                  [0.7677315461266506, 0.10046175256545777, 0.10046175256545777],
                  [0.7677315461266506, 0.10046175256545777, -0.10046175256545777], [0.9996431901055894, 0.0, 0.0],
                  [0.7677315461266506, 0.10046175256545777, -0.10046175256545777],
                  [0.7677315461266506, -0.10046175256545777, -0.10046175256545777], [0.9996431901055894, 0.0, 0.0],
                  [0.7677315461266506, -0.10046175256545777, -0.10046175256545777],
                  [0.7677315461266506, -0.10046175256545777, 0.10046175256545777], [0.9996431901055894, 0.0, 0.0],
                  [0.7677315461266506, -0.10046175256545777, 0.10046175256545777],
                  [0.7677315461266506, 0.10046175256545777, 0.10046175256545777]]
JOINTPLUS = [[0.0, 0.0, 1.5066180003875274], [0.0, 0.0, 1.001092], [0.0, 0.383101, 0.924889],
             [0.0, 0.7078790000000001, 0.7078790000000001], [0.0, 0.924889, 0.383101], [0.0, 1.001092, 0.0],
             [0.0, 1.5066180003875274, 0.0], [0.0, 1.001092, 0.0], [0.0, 0.924889, -0.383101],
             [0.0, 0.7078790000000001, -0.7078790000000001], [0.0, 0.383101, -0.924889], [0.0, 0.0, -1.001092],
             [0.0, 0.0, -1.5066180003875274], [0.0, 0.0, -1.001092], [0.0, -0.383101, -0.924889],
             [0.0, -0.7078790000000001, -0.7078790000000001], [0.0, -0.924889, -0.383101], [0.0, -1.001092, 0.0],
             [0.0, -1.5066180003875274, 0.0], [0.0, -1.001092, 0.0], [0.0, -0.924889, 0.383101],
             [0.0, -0.7078790000000001, 0.7078790000000001], [0.0, -0.383101, 0.924889], [0.0, 0.0, 1.001092],
             [-0.383101, 0.0, 0.924889], [-0.7078790000000001, 0.0, 0.7078790000000001], [-0.924889, 0.0, 0.383101],
             [-1.001092, 0.0, 0.0], [-1.5066180003875274, 0.0, 0.0], [-1.001092, 0.0, 0.0], [-0.924889, 0.0, -0.383101],
             [-0.7078790000000001, 0.0, -0.7078790000000001], [-0.383101, 0.0, -0.924889], [0.0, 0.0, -1.001092],
             [0.383101, 0.0, -0.924889], [0.7078790000000001, 0.0, -0.7078790000000001], [0.924889, 0.0, -0.383101],
             [1.001092, 0.0, 0.0], [1.5066180003875274, 0.0, 0.0], [1.001092, 0.0, 0.0], [0.924889, 0.383101, 0.0],
             [0.7078790000000001, 0.7078790000000001, 0.0], [0.383101, 0.924889, 0.0], [0.0, 1.001092, 0.0],
             [-0.383101, 0.924889, 0.0], [-0.7078790000000001, 0.7078790000000001, 0.0], [-0.924889, 0.383101, 0.0],
             [-1.001092, 0.0, 0.0], [-0.924889, -0.383101, 0.0], [-0.7078790000000001, -0.7078790000000001, 0.0],
             [-0.383101, -0.924889, 0.0], [0.0, -1.001092, 0.0], [0.383101, -0.924889, 0.0],
             [0.7078790000000001, -0.7078790000000001, 0.0], [0.924889, -0.383101, 0.0], [1.001092, 0.0, 0.0],
             [0.924889, 0.0, 0.383101], [0.7078790000000001, 0.0, 0.7078790000000001], [0.383101, 0.0, 0.924889],
             [0.0, 0.0, 1.001092], [0.0, 0.0, 0.0], [0.0, 0.0, -1.001092], [0.0, 0.0, 0.0], [1.001092, 0.0, 0.0],
             [0.0, 0.0, 0.0], [-1.001092, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, -1.001092, 0.0], [0.0, 0.0, 0.0],
             [0.0, 1.001092, 0.0]]
JOINT = [[0.0, 1.0, 0.0], [0.0, 0.9238800000000001, 0.38268300000000005], [0.0, 0.7071070000000002, 0.7071070000000002],
         [0.0, 0.38268300000000005, 0.9238800000000001], [0.0, 0.0, 1.0],
         [0.0, -0.38268300000000005, 0.9238800000000001], [0.0, -0.7071070000000002, 0.7071070000000002],
         [0.0, -0.9238800000000001, 0.38268300000000005], [0.0, -1.0, 0.0],
         [0.0, -0.9238800000000001, -0.38268300000000005], [0.0, -0.7071070000000002, -0.7071070000000002],
         [0.0, -0.38268300000000005, -0.9238800000000001], [0.0, 0.0, -1.0],
         [0.0, 0.38268300000000005, -0.9238800000000001], [0.0, 0.7071070000000002, -0.7071070000000002],
         [0.0, 0.9238800000000001, -0.38268300000000005], [0.0, 1.0, 0.0],
         [0.38268300000000005, 0.9238800000000001, 0.0], [0.7071070000000002, 0.7071070000000002, 0.0],
         [0.9238800000000001, 0.38268300000000005, 0.0], [1.0, 0.0, 0.0],
         [0.9238800000000001, -0.38268300000000005, 0.0], [0.7071070000000002, -0.7071070000000002, 0.0],
         [0.38268300000000005, -0.9238800000000001, 0.0], [0.0, -1.0, 0.0],
         [-0.38268300000000005, -0.9238800000000001, 0.0], [-0.7071070000000002, -0.7071070000000002, 0.0],
         [-0.9238800000000001, -0.38268300000000005, 0.0], [-1.0, 0.0, 0.0],
         [-0.9238800000000001, 0.38268300000000005, 0.0], [-0.7071070000000002, 0.7071070000000002, 0.0],
         [-0.38268300000000005, 0.9238800000000001, 0.0], [0.0, 1.0, 0.0],
         [0.0, 0.9238800000000001, -0.38268300000000005], [0.0, 0.7071070000000002, -0.7071070000000002],
         [0.0, 0.38268300000000005, -0.9238800000000001], [0.0, 0.0, -1.0],
         [-0.38268300000000005, 0.0, -0.9238800000000001], [-0.7071070000000002, 0.0, -0.7071070000000002],
         [-0.9238800000000001, 0.0, -0.38268300000000005], [-1.0, 0.0, 0.0],
         [-0.9238800000000001, 0.0, 0.38268300000000005], [-0.7071070000000002, 0.0, 0.7071070000000002],
         [-0.38268300000000005, 0.0, 0.9238800000000001], [0.0, 0.0, 1.0],
         [0.38268300000000005, 0.0, 0.9238800000000001], [0.7071070000000002, 0.0, 0.7071070000000002],
         [0.9238800000000001, 0.0, 0.38268300000000005], [1.0, 0.0, 0.0],
         [0.9238800000000001, 0.0, -0.38268300000000005], [0.7071070000000002, 0.0, -0.7071070000000002],
         [0.38268300000000005, 0.0, -0.9238800000000001], [0.0, 0.0, -1.0]]
ARROWHEAD = [[-0.9965308, 0.0, 0.0], [0.9893078, 0.0, -0.6619462], [0.9893078, 0.0, 0.6619462], [-0.9965308, 0.0, 0.0],
             [0.9893078, 0.6619462, 0.0], [0.9893078, -0.6619462, 0.0], [-0.9965308, 0.0, 0.0]]
CAPSULECURVE = [[1.4701282511443427e-05, 0.024104395106453284, 0.9827271919977267],
                [0.37529096696204384, -0.006035694684618571, 0.9808448166191278],
                [0.7214198380448003, -0.08421316285244652, 0.9682833786876395],
                [1.0289431881645748, -0.19358653359353253, 0.9374965509871606],
                [1.295325813037938, -0.3220413016780118, 0.883443984249744],
                [1.5038343826132077, -0.46052418798054645, 0.8030118720530239],
                [1.6533906335540134, -0.6013132470234531, 0.6958784228518357],
                [1.769440917417077, -0.7376897657933987, 0.5648903350539239],
                [1.8717654570092466, -0.8620884881598586, 0.40763522367688265],
                [1.952614262038154, -0.9613107027391492, 0.22041669237670533],
                [1.9846734675782491, -1.0048650832170405, 1.4722488994796753e-05],
                [1.952614262038154, -0.9613107027391492, -0.22038724739871604],
                [1.8717654570092463, -0.8620884881598586, -0.40760577869889353],
                [1.7694409174170775, -0.7376897657933987, -0.5648608900759344],
                [1.6533906335540134, -0.6013132470234531, -0.6958489778738464],
                [1.5038343826132086, -0.46052418798054645, -0.8029824270750358],
                [1.2953258130379386, -0.3220413016780118, -0.8834145392717544],
                [1.0289431881645752, -0.19358653359353253, -0.9374671060091715],
                [0.721419838044801, -0.08421316285244652, -0.9682539337096506],
                [0.3752909669620435, -0.006035694684618571, -0.9808153716411377],
                [1.470128251135586e-05, 0.024104395106453284, -0.9826977470197367],
                [1.4722488994797996e-05, 0.2289362812759886, -0.9649098254951565],
                [1.4722488994797996e-05, 0.42507348608784046, -0.9011814286691986],
                [1.4722488994943935e-05, 0.6036741032943762, -0.7980661673571863],
                [1.4722488994797996e-05, 0.7569341621220902, -0.6600701747978316],
                [1.4722488994783405e-05, 0.8781528268657098, -0.49322651665986167],
                [1.4722488994812589e-05, 0.9620342079125997, -0.30482492820833007],
                [1.4722488994808945e-05, 1.0049124055030938, -0.10310064398365336],
                [1.4722488994808945e-05, 1.0049124055030938, 0.10313008896164305],
                [1.4722488994827183e-05, 0.9620342079125997, 0.30485437318631986],
                [1.4722488994768813e-05, 0.8781528268657098, 0.4932559616378514],
                [1.4722488994797996e-05, 0.7569341621220902, 0.660099619775822],
                [1.4722488994885564e-05, 0.6036741032943762, 0.7980956123351769],
                [1.4722488994943935e-05, 0.42507348608784046, 0.9012108736471891],
                [1.4722488994797996e-05, 0.2289362812759886, 0.9649392704731464],
                [1.4701282511443427e-05, 0.024104395106453284, 0.9827271919977267],
                [-0.37526152198405377, -0.006035694684618571, 0.9808448166191277],
                [-0.7213903930668109, -0.08421421445880345, 0.9682833786876398],
                [-1.0289137431865845, -0.19358548198717548, 0.9374965509871607],
                [-1.2952974733906448, -0.3220413016780118, 0.8834439842497442],
                [-1.5038048763597265, -0.46052313637418935, 0.8030118720530242],
                [-1.6533645717068794, -0.6013142986298099, 0.6958784228518357],
                [-1.7694116574713543, -0.7376866109743286, 0.5648903350539239],
                [-1.8717415664008819, -0.8620947977979996, 0.4076352236768826],
                [-1.9525814124516527, -0.9613022898882949, 0.22041669237670547],
                [-1.9846734675782491, -1.0049124055030938, 1.4722488994563253e-05],
                [-1.9525814124516532, -0.9613022898882949, -0.22038724739871604],
                [-1.871741566400882, -0.8620947977979996, -0.40760577869889325],
                [-1.7694116574713552, -0.7376866109743286, -0.5648608900759344],
                [-1.65336457170688, -0.6013142986298099, -0.6958489778738467],
                [-1.5038048763597271, -0.46052313637418935, -0.8029824270750353],
                [-1.2952974733906457, -0.3220413016780118, -0.8834145392717546],
                [-1.0289137431865854, -0.19358548198717548, -0.9374671060091717],
                [-0.7213903930668114, -0.08421421445880345, -0.968253933709651],
                [-0.37526152198405377, -0.006035694684618571, -0.9808153716411377],
                [1.470128251135586e-05, 0.024104395106453284, -0.9826977470197367]]
ARROW2FLAT = [[-2.0, 0.0, 0.0], [-1.001811723544654, 0.0, -0.7645152427204828],
              [-1.001811723544654, 0.0, -0.3822576213602414], [1.001811723544654, 0.0, -0.3822576213602414],
              [1.001811723544654, 0.0, -0.7645152427204828], [2.0, 0.0, 0.0],
              [1.001811723544654, 0.0, 0.7645152427204828], [1.001811723544654, 0.0, 0.3822576213602414],
              [-1.001811723544654, 0.0, 0.3822576213602414], [-1.001811723544654, 0.0, 0.7645152427204828],
              [-2.0, 0.0, 0.0]]
HAND = [[-0.9487813957526796, 0.0, -0.17213807611376986], [-0.8706457830016472, 0.0, -0.19108008841949656],
        [-0.7925101702506145, 0.0, -0.19108008841949656], [-0.7259502432622356, 0.0, -0.17754999430454338],
        [-0.6159817608107826, 0.0, -0.11260598055519606], [-0.5320581987196735, 0.0, -0.023308036309348544],
        [-0.4105140305055684, 0.0, 0.11469776892949939], [-0.3584237639498809, 0.0, 0.1336397812352263],
        [-0.2976515733840776, 0.0, 0.10657979209733279], [-0.2600307543435803, 0.0, 0.05245981382154558],
        [-0.34684807818722774, 0.0, -0.26955399719178375], [-0.4307714273608358, 0.0, -0.5320359117385525],
        [-0.4539227988861424, 0.0, -0.6294518328165669], [-0.4510288242161035, 0.0, -0.7322796720853545],
        [-0.4220897162682216, 0.0, -0.8242836749725946], [-0.367105475042495, 0.0, -0.8892276887219421],
        [-0.2976515733840776, 0.0, -0.913581619218442], [-0.21372822421046894, 0.0, -0.8892276887219421],
        [-0.1616377447372802, 0.0, -0.8567555823012631], [-0.10665350351155417, 0.0, -0.7755758139795951],
        [-0.06613870980101866, 0.0, -0.6646297987866273], [-0.03141186543056021, 0.0, -0.19649200661027008],
        [-0.005366604402215865, 0.0, -0.13425405150231612], [0.029360325135242935, 0.0, -0.0963700268908624],
        [0.07855682993839308, 0.0, -0.12072415647937573], [0.10749593788627537, 0.0, -0.1613140406402096],
        [0.12485936007150464, 0.0, -0.2803780326653441], [0.10460196321623677, 0.0, -0.7566338016738681],
        [0.13643504583415766, 0.0, -0.8784036532483829], [0.17984360129723057, 0.0, -0.943347666997729],
        [0.24929750295564845, 0.0, -0.9893496684413504], [0.32743311570668115, 0.0, -1.0055856221056827],
        [0.3853113316024455, 0.0, -0.9812316916091826], [0.437401598158134, 0.0, -0.9216995960506098],
        [0.47791639186866863, 0.0, -0.8378137690875495], [0.4808103665387071, 0.0, -0.7079257415888551],
        [0.43161386173555744, 0.0, -0.48603391029493265], [0.3505844872319869, 0.0, -0.1559021224494362],
        [0.34773141186027134, 0.0, -0.090958108700089], [0.37172503485570596, 0.0, -0.03413207178290858],
        [0.4315241799451456, 0.0, -0.055780142730028716], [0.48697707100313475, 0.0, -0.10178214417364903],
        [0.5999808833060665, 0.0, -0.3047319631618443], [0.6384503175141507, 0.0, -0.43191393201914524],
        [0.7043342397199287, 0.0, -0.5374478299293263], [0.7504395023176991, 0.0, -0.5942738668465063],
        [0.8371656969037973, 0.0, -0.6267457741751735], [0.9248847150142013, 0.0, -0.6186277973430071],
        [0.9727825777026927, 0.0, -0.5753318545407803], [0.9877073288324265, 0.0, -0.5212118762649933],
        [0.9790256177398133, 0.0, -0.4021478842398583], [0.7916497514184305, 0.0, -0.090958108700089],
        [0.7110961694805066, 0.0, 0.14446381670878639], [0.6444569130862319, 0.0, 0.48271358138644893],
        [0.5676276903823536, 0.0, 0.7181355067953251], [0.5068554998165513, 0.0, 0.8047273923997791],
        [0.41425043955032803, 0.0, 0.8913194770962454], [0.30717571885141315, 0.0, 0.9535574322041992],
        [0.1740558648746544, 0.0, 0.9887353981742606], [0.06119340775316383, 0.0, 0.9995594336478213],
        [-0.07192644622359484, 0.0, 0.9887353981742606], [-0.18189514159254816, 0.0, 0.94273339673064],
        [-0.27739417652880966, 0.0, 0.8777893829812926], [-0.448134849546065, 0.0, 0.7018995531309915],
        [-0.5581035449150187, 0.0, 0.5016555936921762], [-0.6073000497181686, 0.0, 0.3717677652854955],
        [-0.6680720273664706, 0.0, 0.27976376239825423], [-0.760677300550195, 0.0, 0.21211369000751384],
        [-0.873539757671686, 0.0, 0.15799371173172663], [-0.9632510561853711, 0.0, 0.0741078847686657],
        [-1.0008718752258674, 0.0, -0.0016601246358389147], [-1.0124473480710208, 0.0, -0.06931003775296891],
        [-0.9864022147931756, 0.0, -0.1288421333115426], [-0.9487813957526796, 0.0, -0.17213807611376986]]
STICKSTAR = [[1.5026404303079492, 4.822388555347645e-16, 0.0], [1.3931184648598856, 0.07994481219566418, 0.0],
             [1.5283878621098932, 0.09557439305127306, 0.0], [1.4728261774803988, 0.21866534994656678, 0.0],
             [1.5983281552834228, 0.16551468622480187, 0.0], [1.611546928642261, 0.29837306256708057, 0.0],
             [1.6939025483346948, 0.191262118026743, 0.0], [1.7714363396226298, 0.29837306256708046, 0.0],
             [1.7894773806569912, 0.16551468622480187, 0.0], [1.9101570907844916, 0.21866534994656678, 0.0],
             [1.859417234559497, 0.09557439305127333, 0.0], [1.9898652302269224, 0.07994481219566443, 0.0],
             [1.8851637878193908, 2.3839445307561785e-16, 0.0], [1.9898652302269224, -0.07994481219566436, 0.0],
             [1.8594172345594975, -0.0955743930512727, 0.0], [1.9101570907844911, -0.21866534994656653, 0.0],
             [1.7894773806569912, -0.16551468622480167, 0.0], [1.7714363396226298, -0.29837306256708046, 0.0],
             [1.6939025483346943, -0.19126211802674328, 0.0], [1.611546928642261, -0.29837306256708046, 0.0],
             [1.5983281552834232, -0.1655146862248017, 0.0], [1.4728261774803988, -0.21866534994656678, 0.0],
             [1.5283878621098927, -0.0955743930512731, 0.0], [1.393118464859886, -0.079944812195664, 0.0],
             [1.5026404303079492, 4.822388555347645e-16, 0.0], [0.0, 0.0, 0.0]]
CUBE = [[-1.0, 1.0, 1.0], [-1.0, 1.0, -1.0], [1.0, 1.0, -1.0], [1.0, 1.0, 1.0], [-1.0, 1.0, 1.0], [-1.0, -1.0, 1.0],
        [-1.0, -1.0, -1.0], [-1.0, 1.0, -1.0], [-1.0, 1.0, 1.0], [-1.0, -1.0, 1.0], [1.0, -1.0, 1.0], [1.0, 1.0, 1.0],
        [1.0, 1.0, -1.0], [1.0, -1.0, -1.0], [1.0, -1.0, 1.0], [1.0, -1.0, -1.0], [-1.0, -1.0, -1.0]]
CIRCLEPLUSARROW = [[1.5005433070921637, -2.2106052322164817e-15, -5.506441071105041e-16],
                   [1.5005433070921637, -2.2106052322164817e-15, -0.25711860643024165],
                   [1.9964888797557958, -3.546476676340752e-15, -8.86619169085188e-16],
                   [1.500543307092164, -2.2106052322164817e-15, 0.25711860643024115],
                   [1.5005433070921637, -2.2106052322164817e-15, -5.506441071105041e-16],
                   [0.49967246117096653, -8.875965938610025e-16, -2.2189914846525062e-16],
                   [0.48223854140490247, -8.566277312469993e-16, 0.12899913152528397],
                   [0.43242449099440083, -7.681402021020757e-16, 0.24925885092125685],
                   [0.3535395215715452, -6.280123471419064e-16, 0.3528056171261176],
                   [0.24999238116257858, -4.4407567607610044e-16, 0.4316912102224799],
                   [0.12973291123600997, -2.304519441693915e-16, 0.4815043874900733],
                   [0.000733626208459907, -1.303181932960636e-18, 0.4989425482359905],
                   [-0.12826547654925963, 2.2784525652721017e-16, 0.4815043874900734],
                   [-0.2485251959452329, 4.414694315806022e-16, 0.43169121022248014],
                   [-0.35207196215009384, 6.254054379263856e-16, 0.3528056171261179],
                   [-0.43095755524645685, 7.655344007532551e-16, 0.24925885092125724],
                   [-0.4807707325140479, 8.540203788847974e-16, 0.12899913152528442],
                   [-0.4982088932599652, 8.849967749923685e-16, 2.2124919374809213e-16],
                   [-0.480770732514048, 8.540203788847974e-16, -0.12899913152528397],
                   [-0.43095755524645707, 7.655344007532551e-16, -0.24925885092125685],
                   [-0.3520719621500942, 6.254054379263856e-16, -0.3528056171261176],
                   [-0.24852519594523328, 4.414694315806022e-16, -0.4316912102224799],
                   [-0.12826547654926007, 2.2784525652721017e-16, -0.4815043874900733],
                   [0.0007336262084594638, -1.303181932960636e-18, -0.4989425482359905],
                   [0.12973291123600952, -2.304519441693915e-16, -0.4815043874900734],
                   [0.2499923811625782, -4.4407567607610044e-16, -0.43169121022248014],
                   [0.3535395215715449, -6.280123471419064e-16, -0.3528056171261179],
                   [0.4324244909944006, -7.681402021020757e-16, -0.24925885092125724],
                   [0.48223854140490235, -8.566277312469993e-16, -0.12899913152528442],
                   [0.49967246117096653, -8.875965938610025e-16, -2.2189914846525062e-16]]
LOCATOR = [[0.0, 1.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 0.0, -1.0], [0.0, 0.0, 0.0],
           [1.0, 0.0, 0.0], [-1.0, 0.0, 0.0]]

PLUS = [[-0.24960000000000004, -0.9984000000000002, 0.0], [-0.24960000000000004, -0.24960000000000004, 0.0],
        [-0.9984000000000002, -0.24960000000000004, 0.0], [-0.9984000000000002, 0.24960000000000004, 0.0],
        [-0.24960000000000004, 0.24960000000000004, 0.0], [-0.24960000000000004, 0.9984000000000002, 0.0],
        [0.24960000000000004, 0.9984000000000002, 0.0], [0.24960000000000004, 0.24960000000000004, 0.0],
        [0.9984000000000002, 0.24960000000000004, 0.0], [0.9984000000000002, -0.24960000000000004, 0.0],
        [0.24960000000000004, -0.24960000000000004, 0.0], [0.24960000000000004, -0.9984000000000002, 0.0],
        [-0.24960000000000004, -0.9984000000000002, 0.0]]

PIVOT = [[0.025399151999999998, 0.8127734760000002, 0.043992648],
         [-0.025399187999999996, 0.8127734760000002, 0.043992648], [0.0, 0.999022752, 0.0],
         [0.025399151999999998, 0.8127734760000002, 0.043992648], [0.050798339999999984, 0.8127734760000002, 0.0],
         [0.0, 0.999022752, 0.0], [0.050798339999999984, 0.8127734760000002, 0.0],
         [0.025399187999999996, 0.8127734760000002, -0.043992648], [0.0, 0.999022752, 0.0],
         [0.025399187999999996, 0.8127734760000002, -0.043992648],
         [-0.025399151999999998, 0.8127734760000002, -0.043992684000000004], [0.0, 0.999022752, 0.0],
         [-0.025399151999999998, 0.8127734760000002, -0.043992684000000004],
         [-0.050798339999999984, 0.8127734760000002, -8.069328000000001e-09], [0.0, 0.999022752, 0.0],
         [-0.050798339999999984, 0.8127734760000002, -8.069328000000001e-09],
         [-0.025399187999999996, 0.8127734760000002, 0.043992648], [0.0, 0.999022752, 0.0], [0.0, 0.0, 0.0],
         [-5.545690306973938e-17, 0.0, 0.999022752], [-0.04399264800000003, 0.025399188000000003, 0.8127734760000002],
         [-4.5117991342991107e-17, 0.05079834, 0.8127734760000002], [-5.545690306973938e-17, 0.0, 0.999022752],
         [0.04399264799999995, 0.025399152000000005, 0.8127734760000002],
         [-4.5117991342991107e-17, 0.05079834, 0.8127734760000002],
         [0.04399264799999995, 0.025399152000000005, 0.8127734760000002],
         [0.04399264799999995, -0.025399188000000003, 0.8127734760000002], [-5.545690306973938e-17, 0.0, 0.999022752],
         [0.04399264799999995, -0.025399188000000003, 0.8127734760000002],
         [-8.069328045117989e-09, -0.05079834, 0.8127734760000002], [-5.545690306973938e-17, 0.0, 0.999022752],
         [-8.069328045117989e-09, -0.05079834, 0.8127734760000002],
         [-0.04399268400000003, -0.025399152000000005, 0.8127734760000002], [-5.545690306973938e-17, 0.0, 0.999022752],
         [-0.04399268400000003, -0.025399152000000005, 0.8127734760000002],
         [-0.04399264800000003, 0.025399188000000003, 0.8127734760000002], [-5.545690306973938e-17, 0.0, 0.999022752],
         [-1.1279497336147414e-17, 0.0, 0.20319336], [-1.1279497336147414e-17, 0.20319336, 0.20319336],
         [0.0, 0.20319336, 0.0], [0.20319335999999993, 0.20319336, 0.0], [0.20319335999999993, 0.0, 0.0],
         [0.0, 0.0, 0.0], [-1.1279497336147414e-17, 0.0, 0.20319336], [0.20319335999999993, 0.0, 0.20319336],
         [0.20319335999999993, 0.0, 0.0], [0.9990227519999998, 0.0, 0.0], [0.8127734759999999, 0.05079834, 0.0],
         [0.8127734759999999, 0.025399152000000005, -0.043992648], [0.9990227519999998, 0.0, 0.0],
         [0.8127734759999999, 0.025399152000000005, -0.043992648],
         [0.8127734759999999, -0.025399188000000003, -0.043992648], [0.9990227519999998, 0.0, 0.0],
         [0.8127734759999999, -0.05079834, 8.069328000000001e-09],
         [0.8127734759999999, -0.025399188000000003, -0.043992648],
         [0.8127734759999999, -0.05079834, 8.069328000000001e-09],
         [0.8127734759999999, -0.025399152000000005, 0.043992684000000004], [0.9990227519999998, 0.0, 0.0],
         [0.8127734759999999, -0.025399152000000005, 0.043992684000000004],
         [0.8127734759999999, 0.025399188000000003, 0.043992648], [0.8127734759999999, 0.05079834, 0.0],
         [0.9990227519999998, 0.0, 0.0], [0.8127734759999999, 0.025399188000000003, 0.043992648]]

KEYS = [[1.0067333322740324, -5.560094081777596e-16, 0.051158268804933654],
        [1.0067333322740324, -5.619382689031837e-16, -0.055646591010074124],
        [0.8708208476226745, -4.8649168400620835e-16, -0.05564659101007413],
        [0.8708208476226745, -4.96195112190023e-16, -0.23044801322144906],
        [0.7005087670872546, -4.0165291559890433e-16, -0.2304480132214491],
        [0.7005087670872546, -3.9194948741508976e-16, -0.05564659101007414],
        [0.6851020144126563, -3.833970216380676e-16, -0.055646591010074145],
        [0.6851020144126563, -3.931004498218822e-16, -0.2304480132214491],
        [0.5147900358243169, -2.9855830982276166e-16, -0.2304480132214491],
        [0.5147900358243169, -2.888548816389471e-16, -0.05564659101007415],
        [-0.502327626159787, 2.7580649802684014e-16, -0.05478809463771496],
        [-0.5135850306748563, 2.7608189732845997e-16, -0.1624009870197954],
        [-0.5388349779515244, 2.8579810398554117e-16, -0.2398688410653333],
        [-0.590727061848281, 3.111472560190443e-16, -0.3021399534239294],
        [-0.6654719093499736, 3.5086360547156906e-16, -0.3341222820612273],
        [-0.7464952698059619, 3.953844231860334e-16, -0.34234013434474525],
        [-0.8275163874261596, 4.408163607583431e-16, -0.3341222820612273],
        [-0.9022641913932128, 4.84085103142251e-16, -0.3021399534239294],
        [-0.954151381830062, 5.163450210307778e-16, -0.23986884106533332],
        [-0.979410402396974, 5.346669238986936e-16, -0.16240098701979544],
        [-0.990652412902755, 5.453922734142655e-16, -0.08161037175061389],
        [-0.9934869495536366, 5.514960430295294e-16, -5.5149604302952936e-17],
        [-0.8983910178771607, 4.987071965818272e-16, -4.987071965818272e-17],
        [-0.8966478247325261, 4.945131862079727e-16, -0.058120642781171974],
        [-0.8897341814611911, 4.874814040233038e-16, -0.11565753657432247],
        [-0.8742003007761021, 4.757957958175675e-16, -0.17082793276723834],
        [-0.8422904565136706, 4.556204767019737e-16, -0.21517572874719998],
        [-0.7963217019396568, 4.2883831905943157e-16, -0.2379526437235843],
        [-0.7464950659117983, 4.0085409643542885e-16, -0.24380522177184513],
        [-0.6966670026248021, 3.735188482137073e-16, -0.23795264372358427],
        [-0.6507000830982543, 3.4926645477081037e-16, -0.21517572874719995],
        [-0.6187872823704613, 3.3401308890609187e-16, -0.17082793276723832],
        [-0.603258906827768, 3.2845568108138306e-16, -0.11565753657432244],
        [-0.596335782477864, 3.2780651426630826e-16, -0.05812064278117196],
        [-0.5946416258793765, 3.300924122259111e-16, -3.300924122259111e-17],
        [-0.596335782477864, 3.3425920184847537e-16, 0.05812064278117189],
        [-0.603258906827768, 3.4129624708900695e-16, 0.11565753657432239],
        [-0.6187872823704613, 3.5297879932682253e-16, 0.17082793276723826],
        [-0.6507000830982543, 3.731557596103742e-16, 0.2151757287471999],
        [-0.6966670026248021, 3.9993689859694236e-16, 0.2379526437235842],
        [-0.7464950659117983, 4.279219135089234e-16, 0.24380522177184508],
        [-0.7963217019396568, 4.552563694426666e-16, 0.23795264372358418],
        [-0.8422904565136706, 4.795097815415376e-16, 0.21517572874719987],
        [-0.8742003007761021, 4.947615062382981e-16, 0.17082793276723823],
        [-0.8897341814611911, 5.003219700309276e-16, 0.11565753657432236],
        [-0.8966478247325261, 5.009658737901397e-16, 0.05812064278117188],
        [-0.8983910178771607, 4.987071965818272e-16, -4.987071965818272e-17],
        [-0.9934869495536366, 5.514960430295294e-16, -5.5149604302952936e-17],
        [-0.990652412902755, 5.544528447908405e-16, 0.08161037175061378],
        [-0.979410402396974, 5.526970553998164e-16, 0.16240098701979533],
        [-0.954151381830062, 5.429758120548663e-16, 0.2398688410653332],
        [-0.9022641913932128, 5.176293764372928e-16, 0.3021399534239293],
        [-0.8275163874261596, 4.779113858168106e-16, 0.3341222820612272],
        [-0.7464952698059619, 4.3339181312631394e-16, 0.34234013434474514],
        [-0.6654719093499736, 3.8795863053003663e-16, 0.3341222820612272],
        [-0.590727061848281, 3.446915293140862e-16, 0.3021399534239293],
        [-0.5388349779515244, 3.124288950096297e-16, 0.23986884106533324],
        [-0.5135850306748563, 2.941120288295828e-16, 0.16240098701979536],
        [-0.502327626159787, 2.8167286420829365e-16, 0.05089096355753708],
        [1.0067333322740324, -5.560094081777596e-16, 0.051158268804933654]]
PYRAMIDCIRCLE = [[-0.9902241019566351, 1.9981786991344e-05, -3.869999999949771e-05],
                 [-0.9902241019566356, 1.8833686176021325e-05, -0.5163241881992721],
                 [-0.9902241019566351, 0.1973972338943525, -0.4765480402814756],
                 [-0.9902241019566351, 0.365088572556557, -0.3651076521972373],
                 [-0.9902241019566349, 0.4765295285985649, -0.19741533251706658],
                 [-0.9902241019566349, 0.5163052634561648, -3.869999999949771e-05],
                 [-0.9902241019566351, 1.9981786991344e-05, -3.869999999949771e-05],
                 [-0.9902241019566349, 0.5163052634561648, -3.869999999949771e-05],
                 [-0.9902241019566348, 0.4765295285985649, 0.19733793251706785],
                 [-0.9902241019566349, 0.365088572556557, 0.36503025219723795],
                 [-0.9902241019566348, 0.1973972338943525, 0.4764706402814762],
                 [-0.9902241019566349, 1.8833686176021325e-05, 0.5162467881992723],
                 [-0.9902241019566351, 1.9981786991344e-05, -3.869999999949771e-05],
                 [-0.9902241019566349, 1.8833686176021325e-05, 0.5162467881992723],
                 [-0.9902241019566349, -0.19735453379657072, 0.4764706402814762],
                 [-0.9902241019566351, -0.36505273958453655, 0.36503025219723795],
                 [-0.9902241019566351, -0.4764836272842618, 0.19733793251706785],
                 [-0.9902241019566356, -0.5163052634561645, -3.869999999949771e-05],
                 [-0.9902241019566351, 1.9981786991344e-05, -3.869999999949771e-05],
                 [-0.9902241019566356, -0.5163052634561645, -3.869999999949771e-05],
                 [-0.9902241019566356, -0.4764836272842618, -0.19741533251706658],
                 [-0.9902241019566356, -0.36505273958453655, -0.3651076521972373],
                 [-0.9902241019566356, -0.19735453379657072, -0.4765480402814756],
                 [-0.9902241019566356, 1.8833686176021325e-05, -0.5163241881992721],
                 [-0.9902241019566351, 1.9981786991344e-05, -3.869999999949771e-05],
                 [0.6468922464746323, 3.829376938011746e-05, -3.870000000012305e-05],
                 [0.6468922464746327, 0.2752168017955173, -3.870000000012305e-05],
                 [1.000373904254263, 3.869999999950286e-05, -3.870000000039136e-05],
                 [0.6468922464746323, -0.27514021425675667, -3.870000000012305e-05],
                 [0.6468922464746323, 3.829376938011746e-05, -3.870000000012305e-05],
                 [0.6468922464746327, 3.829376938011746e-05, 0.2751398080261369],
                 [1.000373904254263, 3.869999999950286e-05, -3.870000000039136e-05],
                 [0.6468922464746323, 3.829376938011746e-05, -0.2752172080261368],
                 [0.6468922464746327, 0.2752168017955173, -3.870000000012305e-05],
                 [0.6468922464746327, 3.829376938011746e-05, 0.2751398080261369],
                 [0.6468922464746323, -0.27514021425675667, -3.870000000012305e-05],
                 [0.6468922464746323, 3.829376938011746e-05, -0.2752172080261368],
                 [0.6468922464746323, 3.829376938011746e-05, -3.870000000012305e-05]]
ARROW4CIRCULAR = [[0.3134548529969644, 0.3832924032745859, -0.3152986673102934],
                  [0.31529866731029377, 0.3360222346721657, -0.630051319606781],
                  [0.31529866731029377, 0.26741051513098685, -0.8995830490055129],
                  [0.31529866731029377, 0.16902509695021153, -1.1523042060144555],
                  [0.31529866731029377, 0.05481977223390687, -1.3555011930861403],
                  [0.9458966776920379, 0.05481977223390687, -1.3555011930861403],
                  [0.6379820525300844, -0.07707309391199758, -1.586],
                  [0.31529866731029377, -0.22800029347081213, -1.7906659390182778],
                  [0.0, -0.3832924032745861, -1.9947875348653963], [-0.315, -0.23158419276007058, -1.787312632016371],
                  [-0.6338416639291067, -0.0771, -1.5861142119019576],
                  [-0.9458966776920379, 0.05481977223390687, -1.3555011930861403],
                  [-0.31529866731029377, 0.05481977223390687, -1.3555011930861403],
                  [-0.31529866731029377, 0.17136948133962632, -1.1481330702808925],
                  [-0.31529866731029377, 0.2684826102045054, -0.8967985751634485],
                  [-0.31529866731029377, 0.3395997142304458, -0.615921829602235],
                  [-0.31529866731029377, 0.38329240327458575, -0.31345485299696424],
                  [-0.6468311448639844, 0.3317735553459869, -0.31529866731029355],
                  [-0.8952044545971494, 0.26888620855474804, -0.3152986673102934],
                  [-1.1462395875226201, 0.17243363621956603, -0.3152986673102934],
                  [-1.3555011930861405, 0.05481977223390682, -0.3152986673102934],
                  [-1.3555011930861405, 0.05481977223390675, -0.9458966776920376],
                  [-1.5794075978981437, -0.08325140921828043, -0.6241637505377394],
                  [-1.7906659390182778, -0.2280002934708122, -0.3152986673102934],
                  [-2.0011356568392564, -0.383292403274586, 3.72291864215378e-16],
                  [-1.7906659390182778, -0.22800029347081213, 0.3152986673102942],
                  [-1.5794075978981437, -0.0732123014891907, 0.6469953548248211],
                  [-1.3555011930861405, 0.05481977223390677, 0.9458966776920382],
                  [-1.3555011930861405, 0.05481977223390679, 0.31529866731029405],
                  [-1.1462395875226201, 0.17243363621956623, 0.3152986673102944],
                  [-0.8951267420642444, 0.2689059745685519, 0.3152986673102942],
                  [-0.6145240176516689, 0.33980159787571057, 0.31529866731029405],
                  [-0.3134548529969644, 0.383292403274586, 0.3152986673102942],
                  [-0.31529866731029377, 0.33668042603781845, 0.6274516664408013],
                  [-0.31529866731029377, 0.2662865553887662, 0.9025016614369844],
                  [-0.31529866731029377, 0.16938493976562197, 1.1516639223194294],
                  [-0.31529866731029377, 0.0548197722339067, 1.3555011930861407],
                  [-0.9458966776920379, 0.0548197722339067, 1.3555011930861407],
                  [-0.611659128232076, -0.08911177890080542, 1.5863890452295863],
                  [-0.3250522659510998, -0.22342927607336366, 1.7875026861904622],
                  [0.0, -0.3832924032745861, 1.9947875348653978],
                  [0.31697860954336565, -0.2272130317244209, 1.7902824297044364],
                  [0.630413527586237, -0.08032249142918448, 1.5799318095062895],
                  [0.9458966776920379, 0.0548197722339067, 1.3555011930861407],
                  [0.31529866731029377, 0.0548197722339067, 1.3555011930861407],
                  [0.31529866731029377, 0.17733898644879728, 1.1335004760959282],
                  [0.31529866731029377, 0.26910633775121745, 0.8943354257509196],
                  [0.31529866731029377, 0.3389856162802023, 0.618347474270624],
                  [0.3134548529969644, 0.383292403274586, 0.3152986673102942],
                  [0.6159218296022356, 0.339599714230446, 0.3152986673102944],
                  [0.8994708726536662, 0.2674535949046621, 0.3152986673102942],
                  [1.119668320999891, 0.1826649979974522, 0.3152986673102942],
                  [1.3555011930861405, 0.05481977223390679, 0.31529866731029405],
                  [1.3555011930861405, 0.05481977223390677, 0.9458966776920382],
                  [1.5794075978981437, -0.0939955047730545, 0.601237877569438],
                  [1.7965738063530432, -0.25039248406639897, 0.26983447039648545],
                  [1.9947875348653963, -0.383292403274586, 3.72291864215378e-16],
                  [1.7906659390182778, -0.22644992843934572, -0.31860685604802624],
                  [1.5794075978981437, -0.08262092406001126, -0.6255088531181608],
                  [1.3555011930861405, 0.05481977223390675, -0.9458966776920376],
                  [1.3555011930861405, 0.05481977223390682, -0.3152986673102934],
                  [1.1424462022750939, 0.17389429395761305, -0.31529866731029327],
                  [0.8973729721457943, 0.2682614673663029, -0.3152986673102932],
                  [0.613805007782004, 0.3399054961534004, -0.3152986673102931],
                  [0.3134548529969644, 0.3832924032745859, -0.3152986673102934]]

EYES = [[-0.996894836779463, 1.3906153718464233e-19, 0.0003131387435231618],
        [-0.9779046862830135, -1.3031587756074232e-17, -0.029344526881150915],
        [-0.8540636916862537, -3.3863468879513145e-17, -0.07625375291362389],
        [-0.7247174892730308, -6.897770185067077e-17, -0.15532397617577703],
        [-0.59818022017501, -1.1061828092086404e-16, -0.24909022436778408],
        [-0.4700550171607693, -1.4961745762625203e-16, -0.3369085632068548],
        [-0.3302644699860779, -1.7999358482151247e-16, -0.40530952076562166],
        [-0.17839721530566477, -2.00483566938041e-16, -0.4514488586780347],
        [0.0, -2.0989864959690573e-16, -0.47264974005509747],
        [0.09815676844799598, -2.0329620066863198e-16, -0.4577823467885443],
        [0.18966349338574628, -1.8646338229048928e-16, -0.4198782095008449],
        [0.2684536563569048, -1.5980713320215343e-16, -0.3598536727701827],
        [0.32847819308756704, -1.2481744814829054e-16, -0.28106390648498875],
        [0.3663815370033373, -8.418029897471799e-17, -0.18955718154723844],
        [0.3796506825185912, -4.058976106925533e-17, -0.09140001641327788],
        [0.3663815370033373, 3.0005302066681345e-18, 0.006756593360332264],
        [0.32847819308756704, 4.363774984582333e-17, 0.09826347697246843],
        [0.2684536563569048, 7.86274348996862e-17, 0.17705324325766236],
        [0.18966349338574628, 1.0528386015197862e-16, 0.23707817667428915],
        [0.09815676844799598, 1.2211632620220816e-16, 0.2749815205900593],
        [0.0, 1.2800883438550624e-16, 0.2882502694193487],
        [-0.09815676844799598, 1.2211632620220816e-16, 0.2749815205900593],
        [-0.18966349338574628, 1.0528386015197862e-16, 0.23707817667428915],
        [-0.2684536563569048, 7.86274348996862e-17, 0.17705324325766236],
        [-0.32847819308756704, 4.363774984582333e-17, 0.09826347697246843],
        [-0.3663815370033373, 3.0005302066681345e-18, 0.006756593360332264],
        [-0.3796506825185912, -4.058976106925533e-17, -0.09140001641327788],
        [-0.3663815370033373, -8.418029897471799e-17, -0.18955718154723844],
        [-0.32847819308756704, -1.2481744814829054e-16, -0.28106390648498875],
        [-0.2684536563569048, -1.5980713320215343e-16, -0.3598536727701827],
        [-0.18966349338574628, -1.8646338229048928e-16, -0.4198782095008449],
        [-0.09815676844799598, -2.0329620066863198e-16, -0.4577823467885443],
        [0.0, -2.0989864959690573e-16, -0.47264974005509747],
        [0.17939924405219784, -1.9981608170659866e-16, -0.44994581555823515],
        [0.3352746137187433, -1.76878653741448e-16, -0.3982953195398901],
        [0.47406313214690166, -1.4805999208621979e-16, -0.333401462593989],
        [0.591667033322545, -1.1573566769525567e-16, -0.2606135549529145],
        [0.7046769143423693, -8.054744586233878e-17, -0.18137672358563706],
        [0.8305156194567618, -4.654586444087502e-17, -0.10481196887578118],
        [0.9728945425503481, -1.5701563914635083e-17, -0.03535677869754229],
        [0.9963311460237925, -1.1124841939351364e-19, -0.00025050917006309235],
        [0.9753996144166807, 1.4811583606045237e-17, 0.03335272120447614],
        [0.8425399644151587, 4.276327196541161e-17, 0.09629432784428545],
        [0.7151982161809665, 7.876748524515908e-17, 0.17736860859950473],
        [0.5936710908156112, 1.1551317261810818e-16, 0.2601125405796479],
        [0.47406313214690166, 1.4805999208621979e-16, 0.333401462593989],
        [0.3352746137187433, 1.76878653741448e-16, 0.3982953195398901],
        [0.17939924405219784, 1.9981625787055523e-16, 0.44994621224419973],
        [0.0, 2.098974164492097e-16, 0.4726469632533453],
        [-0.17939924405219784, 1.9981625787055523e-16, 0.44994621224419973],
        [-0.3352746137187433, 1.76878653741448e-16, 0.3982953195398901],
        [-0.4760671896399677, 1.469475167004825e-16, 0.33089639072765636],
        [-0.6031907605936401, 1.0972830061227418e-16, 0.24708616687471788],
        [-0.7227134317799647, 7.164764277644031e-17, 0.1613361486549755],
        [-0.8420389500418923, 3.87583605767573e-17, 0.08727606912548774],
        [-0.9748986000434142, 1.4144080758207196e-17, 0.031849638416080066],
        [-0.996894836779463, 1.3906153718464233e-19, 0.0003131387435231618]]
FOOTSTEP = [[1.8141528266464267e-07, 0.0, -1.0009962891086175], [1.8141528266464267e-07, 0.0, -1.0009962891086175],
            [0.059981083061113154, 0.0, -0.9909683863143098], [0.12578881149423723, 0.0, -0.9612501531285806],
            [0.18529988391370153, 0.0, -0.9082987466515058], [0.24117603634867768, 0.0, -0.8288697481751847],
            [0.2696151063442304, 0.0, -0.6859755567350875], [0.2582891527526564, 0.0, -0.5309451333592511],
            [0.2578807082493332, 0.0, -0.3490291456710222], [0.2818911065724362, 0.0, -0.20041814775493091],
            [0.3537683675439619, 0.0, 0.0769157374603213], [0.38796532456092925, 0.0, 0.24787266144030523],
            [0.3992785290177175, 0.0, 0.3719006611710087], [0.3869477547289503, 0.0, 0.5309708167274245],
            [0.34958051286191083, 0.0, 0.6562650924090487], [0.3018803333460585, 0.0, 0.7616957640997051],
            [0.24463671815776006, 0.0, 0.8481539223924083], [0.18675328527928428, 0.0, 0.9130542699562232],
            [0.12607684750236117, 0.0, 0.9588765491371432], [0.06341201688902849, 0.0, 0.9911304435747172],
            [0.0022078074290886648, 0.0, 1.000006674526706], [-0.061117281987194134, 0.0, 0.9914411447113498],
            [-0.12445545579328864, 0.0, 0.959834623006788], [-0.18618959956725697, 0.0, 0.913455631606888],
            [-0.24507879752328005, 0.0, 0.8476502812749702], [-0.30183227930759104, 0.0, 0.7618271108791054],
            [-0.35021713458045906, 0.0, 0.6541410055005932], [-0.3846785180966878, 0.0, 0.5385769078836924],
            [-0.39922858621854074, 0.0, 0.3716548490097024], [-0.3888744000117519, 0.0, 0.25034624433552294],
            [-0.37162482064654745, 0.0, 0.09189965832248183], [-0.3498577978555696, 0.0, -0.0669797082470693],
            [-0.33509666072448513, 0.0, -0.2122493448361651], [-0.3178891062850562, 0.0, -0.39713210340807037],
            [-0.3055427497204394, 0.0, -0.5218167528526091], [-0.28665939234194204, 0.0, -0.6805949496652965],
            [-0.2434110218172249, 0.0, -0.8229196797516275], [-0.19034298436636835, 0.0, -0.901323081162958],
            [-0.12456830924565193, 0.0, -0.9618196144823475], [-0.06333138172833025, 0.0, -0.9903857036355812],
            [7.956130598055217e-05, 0.0, -1.0009830677836546]]
HALF3DCIRCLE = [[-1.0054025599999894, 0.0, 1.4592640000000002e-10], [-0.9925726399999896, 0.0, -0.15714640000000002],
                [-0.9551923199999894, 0.0, -0.31032112000000006], [-0.8948531199999894, 0.0, -0.45599280000000003],
                [-0.8129740799999894, 0.0, -0.5907356800000001], [-0.7109268799999894, 0.0, -0.71092688],
                [-0.5907356799999894, 0.0, -0.81297408], [-0.4559927999999894, 0.0, -0.8948531200000001],
                [-0.3103211199999894, 0.0, -0.9551923200000001], [-0.15714639999998936, 0.0, -0.9925728],
                [1.0658141036401503e-14, 0.0, -1.0054022400000002],
                [1.0658141036401503e-14, 0.15714592000000002, -0.9925728],
                [1.0658141036401503e-14, 0.31032128000000003, -0.9551923200000001],
                [1.0658141036401503e-14, 0.45599264000000006, -0.8948531200000001],
                [1.0658141036401503e-14, 0.5907356800000001, -0.81297408],
                [1.0658141036401503e-14, 0.71092688, -0.71092688],
                [1.0658141036401503e-14, 0.8129742400000002, -0.5907356800000001],
                [1.0658141036401503e-14, 0.8948531200000001, -0.45599280000000003],
                [1.0658141036401503e-14, 0.9551923200000001, -0.31032112000000006],
                [1.0658141036401503e-14, 0.9925726400000002, -0.15714640000000002],
                [1.0658141036401503e-14, 1.00540256, 0.0],
                [1.0658141036401503e-14, 0.9925726400000002, 0.15714640000000002],
                [1.0658141036401503e-14, 0.9551923200000001, 0.31032112000000006],
                [1.0658141036401503e-14, 0.8948531200000001, 0.45599280000000003],
                [1.0658141036401503e-14, 0.8129742400000002, 0.5907356800000001],
                [1.0658141036401503e-14, 0.71092688, 0.71092688],
                [1.0658141036401503e-14, 0.5907356800000001, 0.81297408],
                [1.0658141036401503e-14, 0.45599264000000006, 0.8948531200000001],
                [1.0658141036401503e-14, 0.31032128000000003, 0.9551923200000001],
                [1.0658141036401503e-14, 0.15714592000000002, 0.9925728], [1.0658141036401503e-14, 0.0, 1.00540256],
                [-0.15714639999998936, 0.0, 0.9925726400000002], [-0.3103211199999894, 0.0, 0.9551923200000001],
                [-0.4559927999999894, 0.0, 0.8948531200000001], [-0.5907356799999894, 0.0, 0.81297408],
                [-0.7109268799999894, 0.0, 0.71092688], [-0.8129740799999894, 0.0, 0.5907356800000001],
                [-0.8948531199999894, 0.0, 0.45599280000000003], [-0.9551923199999894, 0.0, 0.31032112000000006],
                [-0.9925726399999896, 0.0, 0.15714640000000002], [-1.0054025599999894, 0.0, 1.4592640000000002e-10],
                [-0.9925727999999894, 0.15714592000000002, 0.0], [-0.9551923199999894, 0.31032128000000003, 0.0],
                [-0.8948531199999894, 0.45599264000000006, 0.0], [-0.8129740799999894, 0.5907356800000001, 0.0],
                [-0.7109268799999894, 0.71092688, 0.0], [-0.5907356799999894, 0.8129742400000002, 0.0],
                [-0.4559927999999894, 0.8948531200000001, 0.0], [-0.3103211199999894, 0.9551923200000001, 0.0],
                [-0.15714639999998936, 0.9925726400000002, 0.0], [1.0658141036401503e-14, 1.00540256, 0.0],
                [0.15714640000001068, 0.9925726400000002, 0.0], [0.3103211200000107, 0.9551923200000001, 0.0],
                [0.4559928000000107, 0.8948531200000001, 0.0], [0.5907356800000108, 0.8129742400000002, 0.0],
                [0.7109268800000107, 0.71092688, 0.0], [0.8129740800000107, 0.5907356800000001, 0.0],
                [0.8948531200000107, 0.45599264000000006, 0.0], [0.9551923200000108, 0.31032128000000003, 0.0],
                [0.9925728000000107, 0.15714592000000002, 0.0], [1.0054025600000107, 0.0, 1.4592720000000002e-10],
                [0.9925726400000109, 0.0, 0.15714640000000002], [0.9551923200000108, 0.0, 0.31032112000000006],
                [0.8948531200000107, 0.0, 0.45599280000000003], [0.8129740800000107, 0.0, 0.5907356800000001],
                [0.7109268800000107, 0.0, 0.71092688], [0.5907356800000108, 0.0, 0.81297408],
                [0.4559928000000107, 0.0, 0.8948531200000001], [0.3103211200000107, 0.0, 0.9551923200000001],
                [0.15714640000001068, 0.0, 0.9925726400000002], [1.0658141036401503e-14, 0.0, 1.00540256],
                [0.15714640000001068, 0.0, 0.9925726400000002], [0.3103211200000107, 0.0, 0.9551923200000001],
                [0.4559928000000107, 0.0, 0.8948531200000001], [0.5907356800000108, 0.0, 0.81297408],
                [0.7109268800000107, 0.0, 0.71092688], [0.8129740800000107, 0.0, 0.5907356800000001],
                [0.8948531200000107, 0.0, 0.45599280000000003], [0.9551923200000108, 0.0, 0.31032112000000006],
                [0.9925726400000109, 0.0, 0.15714640000000002], [1.0054025600000107, 0.0, 1.4592720000000002e-10],
                [0.9925726400000109, 0.0, -0.15714640000000002], [0.9551923200000108, 0.0, -0.31032112000000006],
                [0.8948531200000107, 0.0, -0.45599280000000003], [0.8129740800000107, 0.0, -0.5907356800000001],
                [0.7109268800000107, 0.0, -0.71092688], [0.5907356800000108, 0.0, -0.81297408],
                [0.4559928000000107, 0.0, -0.8948531200000001], [0.3103211200000107, 0.0, -0.9551923200000001],
                [0.15714640000001068, 0.0, -0.9925728], [1.0658141036401503e-14, 0.0, -1.0054022400000002]]
ARROW4STRAIGHT = [[-0.9983883971657876, 0.0, 0.0], [-0.5990330382994733, 0.0, -0.3993553588663152],
                  [-0.5990330382994733, 0.0, -0.1996776794331576], [-0.1996776794331576, 0.0, -0.1996776794331576],
                  [-0.1996776794331576, 0.0, -0.5990330382994733], [-0.3993553588663152, 0.0, -0.5990330382994733],
                  [0.0, 0.0, -0.9983883971657876], [0.3993553588663152, 0.0, -0.5990330382994733],
                  [0.1996776794331576, 0.0, -0.5990330382994733], [0.1996776794331576, 0.0, -0.1996776794331576],
                  [0.5990330382994733, 0.0, -0.1996776794331576], [0.5990330382994733, 0.0, -0.3993553588663152],
                  [0.9983883971657876, 0.0, 0.0], [0.5990330382994733, 0.0, 0.3993553588663152],
                  [0.5990330382994733, 0.0, 0.1996776794331576], [0.1996776794331576, 0.0, 0.1996776794331576],
                  [0.1996776794331576, 0.0, 0.5990330382994733], [0.3993553588663152, 0.0, 0.5990330382994733],
                  [0.0, 0.0, 0.9983883971657876], [-0.3993553588663152, 0.0, 0.5990330382994733],
                  [-0.1996776794331576, 0.0, 0.5990330382994733], [-0.1996776794331576, 0.0, 0.1996776794331576],
                  [-0.5990330382994733, 0.0, 0.1996776794331576], [-0.5990330382994733, 0.0, 0.3993553588663152],
                  [-0.9983883971657876, 0.0, 0.0]]
ARROW3D = [[0.0, 1.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 0.0, -1.0], [0.0, 0.0, 0.0],
           [0.0, 0.0, 0.0], [-2.9349871510930825e-06, 0.0, -0.8325912952423096], [0.08, 0.0, -0.8322415349953303],
           [-2.9349871775177957e-06, 0.0, -0.832591317545347], [-0.08, 0.0, -0.8322415349953303], [0.0, 0.0, -1.0],
           [0.08, 0.0, -0.8322415349953303], [-2.9349871775177957e-06, 0.0, -0.832591317545347],
           [-2.9349871816685955e-06, 0.08, -0.8322415349953303], [0.0, 0.0, -1.0],
           [-2.9349871816685955e-06, -0.08, -0.8322415349953303], [-2.9349871775177957e-06, 0.0, -0.832591317545347],
           [-2.1316282072803006e-14, 0.0, 0.0], [-2.9349871775177957e-06, 0.0, 0.832591317545347],
           [-0.08, 0.0, 0.8322415349953303], [0.0, 0.0, 1.0], [0.08, 0.0, 0.8322415349953303],
           [-2.9349871775177957e-06, 0.0, 0.832591317545347], [-2.9349871816685955e-06, -0.08, 0.8322415349953303],
           [0.0, 0.0, 1.0], [-2.9349871816685955e-06, 0.08, 0.8322415349953303],
           [-2.9349871775177957e-06, 0.0, 0.832591317545347], [-2.1316282072803006e-14, 0.0, 0.0],
           [0.8325883825581697, 0.0, 0.0], [0.8322386000081496, 0.0, 0.08], [1.0, 0.0, 0.0],
           [0.8322386000081496, 0.0, -0.08], [0.8325883825581697, 0.0, 0.0], [0.8322386000081496, 0.08, 0.0],
           [1.0, 0.0, 0.0], [0.8322386000081496, -0.08, 0.0], [0.8325883825581697, 0.0, 0.0],
           [-2.1316282072803006e-14, 0.0, 0.0], [-0.8325350924734789, 0.0, 0.0], [-0.8323036300415579, 0.0, 0.08],
           [-1.0, 0.0, 0.0], [-0.8323036300415579, 0.0, -0.08], [-0.8325350924734789, 0.0, 0.0],
           [-0.8323036300415579, 0.08, 0.0], [-1.0, 0.0, 0.0], [-0.8323036300415579, -0.08, 0.0],
           [-0.8325350924734789, 0.0, 0.0], [-2.1316282072803006e-14, 0.0, 0.0],
           [-2.9349871775177957e-06, 0.832591317545347, 0.0], [-0.08, 0.8322415349953303, 0.0], [0.0, 1.0, 0.0],
           [0.08, 0.8322415349953303, 0.0], [-2.9349871775177957e-06, 0.832591317545347, 0.0],
           [-2.9349871816685955e-06, 0.8322415349953303, 0.08], [0.0, 1.0, 0.0],
           [-2.9349871816685955e-06, 0.8322415349953303, -0.08], [-2.9349871775177957e-06, 0.832591317545347, 0.0],
           [-2.1316282072803006e-14, 0.0, 0.0], [-2.9349871775177957e-06, -0.832591317545347, 0.0],
           [-0.08, -0.8322415349953303, 0.0], [0.0, -1.0, 0.0], [0.08, -0.8322415349953303, 0.0],
           [-2.9349871775177957e-06, -0.832591317545347, 0.0], [-2.9349871816685955e-06, -0.8322415349953303, -0.08],
           [0.0, -1.0, 0.0], [-2.9349871816685955e-06, -0.8322415349953303, 0.08],
           [-2.9349871775177957e-06, -0.832591317545347, 0.0]]

ARROW3DFLAT = [[0.14316906937233417, 0.0, -0.6805927362478895], [-2.1316282072803006e-14, 0.0, -0.6806627028155027],
               [-0.14316906937237553, 0.0, -0.6805927362478895], [-2.1316282072803006e-14, 0.0, -0.9818754000000001],
               [0.14316906937233417, 0.0, -0.6805927362478895], [-2.1316282072803006e-14, 0.0, -0.6806627028155027],
               [-2.1316282072803006e-14, 0.1431690693723543, -0.6805927362478895],
               [-2.1316282072803006e-14, 0.0, -0.9818754000000001],
               [-2.1316282072803006e-14, -0.1431690693723543, -0.6805927362478895],
               [-2.1316282072803006e-14, 0.0, -0.6806627028155027], [-2.1316282072803006e-14, 0.0, 0.0],
               [-2.1316282072803006e-14, 0.0, 0.6806627028155027], [-0.14316906937237553, 0.0, 0.6805927362478895],
               [-2.1316282072803006e-14, 0.0, 0.9818754000000001], [0.14316906937233417, 0.0, 0.6805927362478895],
               [-2.1316282072803006e-14, 0.0, 0.6806627028155027],
               [-2.1316282072803006e-14, -0.1431690693723543, 0.6805927362478895],
               [-2.1316282072803006e-14, 0.0, 0.9818754000000001],
               [-2.1316282072803006e-14, 0.1431690693723543, 0.6805927362478895],
               [-2.1316282072803006e-14, 0.0, 0.6806627028155027], [-2.1316282072803006e-14, 0.0, 0.0],
               [0.6806627028154805, 0.0, 0.0], [0.6805927362478625, 0.0, 0.1431690693723543],
               [0.9818753999999787, 0.0, 0.0], [0.6805927362478625, 0.0, -0.1431690693723543],
               [0.6806627028154805, 0.0, 0.0], [0.6805927362478625, 0.1431690693723543, 0.0],
               [0.9818753999999787, 0.0, 0.0], [0.6805927362478625, -0.1431690693723543, 0.0],
               [0.6806627028154805, 0.0, 0.0], [-2.1316282072803006e-14, 0.0, 0.0], [-0.6806627028155267, 0.0, 0.0],
               [-0.6805927362479137, 0.0, 0.1431690693723543], [-0.9818754000000214, 0.0, 0.0],
               [-0.6805927362479137, 0.0, -0.1431690693723543], [-0.6806627028155267, 0.0, 0.0],
               [-0.6805927362479137, 0.1431690693723543, 0.0], [-0.9818754000000214, 0.0, 0.0],
               [-0.6805927362479137, -0.1431690693723543, 0.0], [-0.6806627028155267, 0.0, 0.0],
               [-2.1316282072803006e-14, 0.0, 0.0], [-2.1316282072803006e-14, 0.6806627028155027, 0.0],
               [-0.14316906937237553, 0.6805927362478895, 0.0], [-2.1316282072803006e-14, 0.9818754000000001, 0.0],
               [0.14316906937233417, 0.6805927362478895, 0.0], [-2.1316282072803006e-14, 0.6806627028155027, 0.0],
               [-2.1316282072803006e-14, 0.6805927362478895, 0.1431690693723543],
               [-2.1316282072803006e-14, 0.9818754000000001, 0.0],
               [-2.1316282072803006e-14, 0.6805927362478895, -0.1431690693723543],
               [-2.1316282072803006e-14, 0.6806627028155027, 0.0], [-2.1316282072803006e-14, 0.0, 0.0],
               [-2.1316282072803006e-14, -0.6806627028155027, 0.0], [-0.14316906937237553, -0.6805927362478895, 0.0],
               [-2.1316282072803006e-14, -0.9818754000000001, 0.0], [0.14316906937233417, -0.6805927362478895, 0.0],
               [-2.1316282072803006e-14, -0.6806627028155027, 0.0],
               [-2.1316282072803006e-14, -0.6805927362478895, -0.1431690693723543],
               [-2.1316282072803006e-14, -0.9818754000000001, 0.0],
               [-2.1316282072803006e-14, -0.6805927362478895, 0.1431690693723543],
               [-2.1316282072803006e-14, -0.6806627028155027, 0.0]]
PYRAMID = [[1.0, 0.0, 1.0], [-1.0, 0.0, 1.0], [-1.0, 0.0, -1.0], [1.0, 0.0, -1.0], [1.0, 0.0, 1.0], [0.0, 2.0, 0.0],
           [-1.0, 0.0, 1.0], [-1.0, 0.0, -1.0], [0.0, 2.0, 0.0], [1.0, 0.0, -1.0], [1.0, 0.0, 1.0], [0.0, 2.0, 0.0],
           [-1.0, 0.0, 1.0]]
PYRAMIDARROW = [[-0.4544466599999999, 0.7240772800000002, -2.7963900884031385e-16],
                [-0.45444666, 0.7240772800000002, 0.1279999999999997],
                [-0.2507998199999999, 0.9956064000000002, -1.8920164457625202e-16],
                [-0.4544466599999998, 0.7240772800000002, -0.12800000000000025],
                [-0.4544466599999999, 0.7240772800000002, -2.7963900884031385e-16],
                [-0.99750462, 0.0, -5.20805189199501e-16],
                [-0.45444665999999967, 0.5120000000000001, -0.5120000000000002],
                [-0.45444665999999967, 0.6025096000000001, -0.42149040000000015],
                [-0.25079981999999956, 0.7040000000000002, -0.7040000000000002],
                [-0.45444665999999967, 0.4214904, -0.6025096000000002],
                [-0.45444665999999967, 0.5120000000000001, -0.5120000000000002],
                [-0.99750462, 0.0, -5.20805189199501e-16], [-0.45444665999999956, 0.0, -0.7240772800000003],
                [-0.45444665999999956, 0.12800000000000003, -0.7240772800000003],
                [-0.25079981999999945, 0.0, -0.9956064000000001],
                [-0.45444665999999956, -0.12800000000000003, -0.7240772800000003],
                [-0.45444665999999956, 0.0, -0.7240772800000003], [-0.99750462, 0.0, -5.20805189199501e-16],
                [-0.45444665999999967, -0.5120000000000001, -0.5120000000000002],
                [-0.45444665999999967, -0.4214904, -0.6025096000000002],
                [-0.25079981999999956, -0.7040000000000002, -0.7040000000000002],
                [-0.45444665999999967, -0.6025096000000001, -0.42149040000000015],
                [-0.45444665999999967, -0.5120000000000001, -0.5120000000000002],
                [-0.99750462, 0.0, -5.20805189199501e-16],
                [-0.4544466599999999, -0.7240772800000002, -2.7963900884031385e-16],
                [-0.4544466599999998, -0.7240772800000002, -0.12800000000000025],
                [-0.2507998199999999, -0.9956064000000002, -1.8920164457625202e-16],
                [-0.45444666, -0.7240772800000002, 0.1279999999999997],
                [-0.4544466599999999, -0.7240772800000002, -2.7963900884031385e-16],
                [-0.99750462, 0.0, -5.20805189199501e-16],
                [-0.4544466600000001, -0.5120000000000001, 0.5119999999999996],
                [-0.4544466600000001, -0.6025096000000001, 0.4214903999999996],
                [-0.25079982000000023, -0.7040000000000002, 0.7039999999999997],
                [-0.4544466600000001, -0.4214904, 0.6025095999999995],
                [-0.4544466600000001, -0.5120000000000001, 0.5119999999999996],
                [-0.99750462, 0.0, -5.20805189199501e-16], [-0.4544466600000002, 0.0, 0.7240772799999996],
                [-0.4544466600000002, -0.12800000000000003, 0.7240772799999996],
                [-0.25079982000000034, 0.0, 0.9956063999999997],
                [-0.4544466600000002, 0.12800000000000003, 0.7240772799999996],
                [-0.4544466600000002, 0.0, 0.7240772799999996], [-0.99750462, 0.0, -5.20805189199501e-16],
                [-0.4544466600000001, 0.5120000000000001, 0.5119999999999996],
                [-0.4544466600000001, 0.4214904, 0.6025095999999995],
                [-0.25079982000000023, 0.7040000000000002, 0.7039999999999997],
                [-0.4544466600000001, 0.6025096000000001, 0.4214903999999996],
                [-0.4544466600000001, 0.5120000000000001, 0.5119999999999996],
                [-0.99750462, 0.0, -5.20805189199501e-16], [0.66759672995456, 0.0, 2.1827235824367521e-16],
                [0.66759672995456, 0.17459374007912917, 2.1827235824367521e-16],
                [0.99750462, 0.0, 3.651568878356729e-16],
                [0.66759672995456, -0.17459374007912917, 2.1827235824367521e-16],
                [0.66759672995456, 0.0, 2.1827235824367521e-16], [0.66759672995456, 0.0, 0.1745937400791294],
                [0.66759672995456, 0.17459374007912917, 2.1827235824367521e-16],
                [0.66759672995456, 0.0, -0.1745937400791288],
                [0.66759672995456, -0.17459374007912917, 2.1827235824367521e-16],
                [0.66759672995456, 0.0, 0.1745937400791294], [0.99750462, 0.0, 3.651568878356729e-16],
                [0.66759672995456, 0.0, -0.1745937400791288], [0.66759672995456, 0.0, 2.1827235824367521e-16]]
ARROW3DCIRCULAR = [[0.0003813370824446932, 0.0, -0.7502096087120079], [0.0003813370824446932, 0.0, -1.0002794745607002],
                   [0.2589960902471867, 0.0, -0.9653289599000894], [0.5001029519641302, 0.0, -0.8654574322617011],
                   [0.7076911990723125, 0.0, -0.7073102482605979], [0.8658395083878118, 0.0, -0.49972137597775085],
                   [0.9657091605022066, 0.0, -0.2586148893656064], [1.000668552643055, 0.0, 5.32935778092305e-08],
                   [0.9657091605022066, 0.0, 0.25861474199881085], [0.8658395083878118, 0.0, 0.49972160371575436],
                   [0.7076911990723125, 0.0, 0.7073098508239365], [0.5001029519641302, 0.0, 0.8654581601394361],
                   [0.2589960902471867, 0.0, 0.9653278122538305], [0.0003813370824446932, 0.0, 1.0002872043946793],
                   [-0.25823341608229733, 0.0, 0.9653278122538305], [-0.49934027779924084, 0.0, 0.8654581601394361],
                   [-0.7069285249074229, 0.0, 0.7073098508239365], [-0.8650768342229228, 0.0, 0.49972160371575436],
                   [-0.9649464863373172, 0.0, 0.25861474199881085], [-0.9999058784781653, 0.0, 5.32935778092305e-08],
                   [-1.2646565959412366, 0.0, -1.1165931231123493e-08], [-0.8697631435089268, 0.0, -0.7897869160305514],
                   [-0.47486969107661703, 0.0, -1.1165931231123493e-08],
                   [-0.7498340120705466, 0.0, 3.7213960400226666e-08], [-0.7236145617411098, 0.0, 0.19396117874255828],
                   [-0.6487122601378474, 0.0, 0.37479107496040004], [-0.5301011219274226, 0.0, 0.5304823228090028],
                   [-0.37440974904388646, 0.0, 0.6490935860543612], [-0.19357985282604473, 0.0, 0.7239958876576232],
                   [0.0003813370824446932, 0.0, 0.7502153379870602], [0.19434252699093413, 0.0, 0.7239958876576232],
                   [0.3751724232087759, 0.0, 0.6490935860543612], [0.5308637960923118, 0.0, 0.5304823228090028],
                   [0.6494749343027368, 0.0, 0.37479107496040004], [0.7243772359059995, 0.0, 0.19396117874255828],
                   [0.7505966862354357, 0.0, 3.7213960400226666e-08], [0.7243772359059995, 0.0, -0.19396132610935363],
                   [0.6494749343027368, 0.0, -0.37479097225732944], [0.5308637960923118, 0.0, -0.5304827202456643],
                   [0.3751724232087759, 0.0, -0.6490931082464917], [0.19434252699093413, 0.0, -0.7239966601990835],
                   [0.0003813370824446932, 0.0, -0.7502096087120079]]
CYLINDER = [[0.9971251003039016, 0.022666678770549883, -7.879453482702045e-08],
            [0.9622763437846297, 0.022666678770549883, -0.2578535257594705],
            [0.8627223089552045, 0.022666678770549883, -0.49824958595307595],
            [0.7050740507334028, 0.022666678770549883, -0.7052271674411453],
            [0.4981417665856296, 0.022666678770549883, -0.8629085575274855],
            [0.2577974059860588, 0.022666678770549883, -0.9624858069856578],
            [0.0, 0.022666678770549883, -0.997333464340516], [0.0, 2.017333321229451, -0.997333464340516],
            [0.2577974059860588, 2.017333321229451, -0.9624858069856578],
            [0.4981417665856296, 2.017333321229451, -0.8629085575274855],
            [0.7050740507334028, 2.017333321229451, -0.7052271674411453],
            [0.8627223089552045, 2.017333321229451, -0.49824958595307595],
            [0.9622763437846297, 2.017333321229451, -0.2578535257594705],
            [0.9971251003039016, 2.017333321229451, -7.879453482702045e-08],
            [0.9971251003039016, 0.022666678770549883, -7.879453482702045e-08],
            [0.9622763437846297, 0.022666678770549883, 0.2578530733151209],
            [0.8627223089552045, 0.022666678770549883, 0.4982494659531668],
            [0.7050740507334028, 0.022666678770549883, 0.7052263825523549],
            [0.4981417665856296, 0.022666678770549883, 0.8629089361942364],
            [0.2577974059860588, 0.022666678770549883, 0.9624845234302069],
            [0.0, 0.022666678770549883, 0.9973408243405157],
            [-0.2577974059860588, 0.022666678770549883, 0.9624845234302069],
            [-0.4981417665856296, 0.022666678770549883, 0.8629089361942364],
            [-0.7050740507334028, 0.022666678770549883, 0.7052263825523549],
            [-0.8627223089552045, 0.022666678770549883, 0.4982494659531668],
            [-0.9622763437846297, 0.022666678770549883, 0.2578530733151209],
            [-0.9971251003039016, 0.022666678770549883, -7.879453482702045e-08],
            [-0.9971251003039016, 2.017333321229451, -7.879453482702045e-08],
            [-0.9622763437846297, 2.017333321229451, -0.2578535257594705],
            [-0.8627223089552045, 2.017333321229451, -0.49824958595307595],
            [-0.7050740507334028, 2.017333321229451, -0.7052271674411453],
            [-0.4981417665856296, 2.017333321229451, -0.8629085575274855],
            [-0.2577974059860588, 2.017333321229451, -0.9624858069856578], [0.0, 2.017333321229451, -0.997333464340516],
            [0.0, 0.022666678770549883, -0.997333464340516],
            [-0.2577974059860588, 0.022666678770549883, -0.9624858069856578],
            [-0.4981417665856296, 0.022666678770549883, -0.8629085575274855],
            [-0.7050740507334028, 0.022666678770549883, -0.7052271674411453],
            [-0.8627223089552045, 0.022666678770549883, -0.49824958595307595],
            [-0.9622763437846297, 0.022666678770549883, -0.2578535257594705],
            [-0.9971251003039016, 0.022666678770549883, -7.879453482702045e-08],
            [-0.9971251003039016, 2.017333321229451, -7.879453482702045e-08],
            [-0.9622763437846297, 2.017333321229451, 0.2578530733151209],
            [-0.8627223089552045, 2.017333321229451, 0.4982494659531668],
            [-0.7050740507334028, 2.017333321229451, 0.7052263825523549],
            [-0.4981417665856296, 2.017333321229451, 0.8629089361942364],
            [-0.2577974059860588, 2.017333321229451, 0.9624845234302069], [0.0, 2.017333321229451, 0.9973408243405157],
            [0.0, 0.022666678770549883, 0.9973408243405157], [0.0, 2.017333321229451, 0.9973408243405157],
            [0.2577974059860588, 2.017333321229451, 0.9624845234302069],
            [0.4981417665856296, 2.017333321229451, 0.8629089361942364],
            [0.7050740507334028, 2.017333321229451, 0.7052263825523549],
            [0.8627223089552045, 2.017333321229451, 0.4982494659531668],
            [0.9622763437846297, 2.017333321229451, 0.2578530733151209],
            [0.9971251003039016, 2.017333321229451, -7.879453482702045e-08]]
ARROW2FLATHALF = [[-0.8657258484, 0.0, -0.49474053999999995], [-0.8668724432000001, 0.0, -0.5023629799999999],
                  [-1.1196, 0.0, 0.0], [-0.9952077128, 0.0, 0.0], [-0.9605735088, 0.0, 0.25473714],
                  [-0.8582392076, 0.0, 0.49801262], [-0.7070662128, 0.0, 0.69530468],
                  [-0.5025291011999999, 0.0, 0.8520666000000001], [-0.257301496, 0.0, 0.9549068200000002],
                  [-0.000905622048, 0.0, 0.9893671199999998], [0.2525185648, 0.0, 0.9555495599999999],
                  [0.49186117920000005, 0.0, 0.85830738], [0.7037181112, 0.0, 0.6996742199999999],
                  [0.8563576576000002, 0.0, 0.50046808], [0.9604258460000001, 0.0, 0.25582298],
                  [0.9963097724000001, 0.0, 0.0], [1.1196, 0.0, 0.0], [0.8708, 0.0, -0.49474053999999995],
                  [0.622, 0.0, 0.0], [0.7464057224, 0.0, 0.0], [0.7203194156000001, 0.0, 0.19186734],
                  [0.6457974712, 0.0, 0.37074505999999996], [0.5277886456, 0.0, 0.52475556],
                  [0.375860294, 0.0, 0.6398349999999999], [0.1929762464, 0.0, 0.71618008], [0.0, 0.0, 0.74211648],
                  [-0.1929762464, 0.0, 0.71618008], [-0.3697493928, 0.0, 0.64337896], [-0.5255281732, 0.0, 0.5264679],
                  [-0.6425722768, 0.0, 0.37495416], [-0.7203194156000001, 0.0, 0.19186734], [-0.7464057224, 0.0, 0.0],
                  [-0.622, 0.0, 0.0], [-0.8657258484, 0.0, -0.49474053999999995]]
FLAG = [[0.0, 0.0, 9.085762267363806e-16], [0.0, 0.0, -1.0025065712610746],
        [0.35803806116466985, 0.0, -0.2864304489317349], [0.0, 0.0, -0.2864304489317349]]
ARROW90DEG = [[-0.49971699999999997, 0.0, 0.8684004000000001], [0.0034143800000000003, 0.0, 1.1195948],
              [0.00300986, 0.0, 0.9869488000000001], [0.249144, 0.0, 0.9559998000000001],
              [0.4935256, 0.0, 0.8570612000000001], [0.7037182, 0.0, 0.6996742], [0.8557572000000001, 0.0, 0.5012516],
              [0.9604258, 0.0, 0.255823], [0.9963098000000001, 0.0, 0.0], [1.1196, 0.0, 0.0],
              [0.8708, 0.0, -0.49474060000000003], [0.622, 0.0, 0.0], [0.7464058, 0.0, 0.0],
              [0.7182930000000001, 0.0, 0.1967314], [0.6430624, 0.0, 0.3743146],
              [0.5277885999999999, 0.0, 0.5247556000000001], [0.3719422, 0.0, 0.6414706],
              [0.199078, 0.0, 0.7136330000000001], [0.0, 0.0, 0.7421164], [0.0018968760000000002, 0.0, 0.6219972],
              [-0.49971699999999997, 0.0, 0.8684004000000001]]
WORLD = [[2.249819018465117e-06, 4.4954081543323836e-21, -0.9995246068942343],
         [-0.14364550934591647, 4.4954081543323836e-21, -0.8558768477293006],
         [-0.071821629763449, 4.4954081543323836e-21, -0.8558768477293006],
         [-0.07182162976344904, 4.4954081543323836e-21, -0.7122290885643646],
         [-0.088386409295832, 2.0846451730833405e-17, -0.7108157938106947],
         [-0.1061349197992234, 3.424365103258661e-17, -0.7088070525039724],
         [-0.12501357709855218, 4.497229342741604e-17, -0.7063385569153456],
         [-0.14346314528846507, 4.5393406538715825e-17, -0.7035113744664869],
         [-0.16174000089634305, 4.438578325514239e-17, -0.6998018603824748],
         [-0.17978550363873633, 4.204809138186353e-17, -0.6949578325308288],
         [-0.1977083608059601, 4.1243774524624774e-17, -0.6897328753554542],
         [-0.21555724337727425, 4.14225688486721e-17, -0.6842437171243055],
         [-0.23332973449821515, 4.2521704366388776e-17, -0.6785201391792451],
         [-0.25090703521792, 4.110606733572579e-17, -0.6722116297263254],
         [-0.26830200524946435, 4.048648655099494e-17, -0.6654334932404337],
         [-0.2855187684402299, 4.031687187935323e-17, -0.6582016936643575],
         [-0.30254880350042124, 3.987962028811478e-17, -0.6505416471727158],
         [-0.3193930681286763, 3.9383551536911306e-17, -0.6424878958416353],
         [-0.3360558301637971, 3.8798026965829384e-17, -0.634059768877937],
         [-0.3524512734001972, 3.828035662596862e-17, -0.6251207556479854],
         [-0.3686199003548641, 3.771530917600967e-17, -0.6157856020439431],
         [-0.38456488141059475, 3.711548796341085e-17, -0.6060669447951867],
         [-0.400232558958288, 3.649364150355613e-17, -0.5959065280382044],
         [-0.4156433972813192, 3.5847798846401436e-17, -0.585367121368167],
         [-0.4308011482177873, 3.5179663496699165e-17, -0.5744615036379386],
         [-0.44561771917015786, 3.448426697901553e-17, -0.563095619040009],
         [-0.46013820332983396, 3.376583309756324e-17, -0.5513603654680082],
         [-0.4743666884032504, 3.3025127486903226e-17, -0.5392670202284431],
         [-0.4882347416719026, 3.225933955264423e-17, -0.5267616317911085],
         [-0.5017849672351886, 3.1472900139070075e-17, -0.5139179908469292],
         [-0.515020932440063, 3.06664316539793e-17, -0.5007459415445104],
         [-0.5278091698623874, 2.9833164232413545e-17, -0.48713832513880045],
         [-0.5402563551042172, 2.898108925919669e-17, -0.4732230675449835],
         [-0.5523640315881179, 2.811060335110381e-17, -0.45900681245112573],
         [-0.5640305971829108, 2.7217796546904837e-17, -0.4444261563025453],
         [-0.575335915144953, 2.630801027836206e-17, -0.4295682118477999],
         [-0.586282388353527, 2.538165165114628e-17, -0.4144396485464787],
         [-0.5967470656639576, 2.443464667161036e-17, -0.39897388036939935],
         [-0.6068427740228688, 2.347298219445621e-17, -0.3832687067753213],
         [-0.616570806773389, 2.2496975894361343e-17, -0.36732931371226707],
         [-0.6258216887939452, 2.1503730556440226e-17, -0.351108385558242],
         [-0.6346977037597139, 2.0497956717099997e-17, -0.3346828524172],
         [-0.6431989454573126, 1.9479904720662045e-17, -0.31805680272159],
         [-0.6511810563271991, 1.8446217836868905e-17, -0.3011754142121688],
         [-0.6587791612576919, 1.7401937024917046e-17, -0.28412101412302465],
         [-0.6659911581316683, 1.6347237826023767e-17, -0.2668964692050228],
         [-0.6726813860842611, 1.5279727602981525e-17, -0.24946270427708261],
         [-0.6789766296861943, 1.420344118373564e-17, -0.23188561315928177],
         [-0.6848728058528742, 1.3118517279535426e-17, -0.2141674611548622],
         [-0.6902325390487584, 1.2023209262116127e-17, -0.19627972377070854],
         [-0.6951747516141558, 1.0920771206732719e-17, -0.17827554402085524],
         [-0.6996942786706174, 9.81133652885942e-18, -0.1601571007479005],
         [-0.7036521720993594, 8.693906843663924e-18, -0.14190808909888047],
         [-0.7071956003928191, 7.571451299693695e-18, -0.12357699894669062],
         [-0.710318998133277, 6.44414006335067e-18, -0.10516660931991012],
         [-0.7139779529651757, 4.4954081543323836e-21, -0.07182311068925219],
         [-0.8558579024987216, 4.4954081543323836e-21, -0.07182311068925318],
         [-0.8558579024987216, 4.4954081543323836e-21, -0.14364699027171945],
         [-0.9995056616636551, 4.4954081543323836e-21, 7.688932141024849e-07],
         [-0.8558579024987216, 4.4954081543323836e-21, 0.1436485280581486],
         [-0.8558579024987216, 4.4954081543323836e-21, 0.0718246484756814],
         [-0.7122101433337859, 4.4954081543323836e-21, 0.0718246484756814],
         [-0.7101034965548036, -6.087697272171461e-18, 0.09949382574139899],
         [-0.7082609933364074, -7.217868082009019e-18, 0.11795091574685157],
         [-0.7048089309836327, -8.341556908886927e-18, 0.13630214693710566],
         [-0.7009373282025825, -9.459935799123431e-18, 0.15456666028111893],
         [-0.6966367036059375, -1.0572642193592239e-17, 0.17273853473902004],
         [-0.6917842782426681, -1.1676757680586674e-17, 0.19077010903069605],
         [-0.686532600584519, -1.2773838463269016e-17, 0.208686797882472],
         [-0.6808727724137313, -1.3863494389121935e-17, 0.22648222962020387],
         [-0.6746618705338245, -1.4941788450243546e-17, 0.24409210802551007],
         [-0.668061885450966, -1.6011214612727595e-17, 0.26155716265560613],
         [-0.6610601472264738, -1.7071237447790272e-17, 0.2788686492948676],
         [-0.653550871247968, -1.81181045706513e-17, 0.295965286849302],
         [-0.6456625847485462, -1.9154291160145213e-17, 0.3128874980568981],
         [-0.6373804162987747, -2.0179121203326025e-17, 0.32962424278842917],
         [-0.6286012846154017, -2.1188270255756177e-17, 0.34610489750671675],
         [-0.6194466195350301, -2.2184630432609215e-17, 0.36237669403689604],
         [-0.6098978896256366, -2.3167290157661624e-17, 0.37842474520947295],
         [-0.5998806484292324, -2.413223153555778e-17, 0.39418343381369686],
         [-0.5895058557948166, -2.508270659171159e-17, 0.4097058694549865],
         [-0.5787561849228763, -2.601769893300259e-17, 0.4249754531740134],
         [-0.5675471789092137, -2.6932185200998734e-17, 0.43991014730186906],
         [-0.555979224718831, -2.782949910597824e-17, 0.45456439545903937],
         [-0.5440281932445771, -2.870813647823441e-17, 0.4689136326900169],
         [-0.5316547599209588, -2.956445893308094e-17, 0.4828984396636322],
         [-0.5189553441601219, -3.04024733037141e-17, 0.4965842529318597],
         [-0.5059169129756561, -3.1221073975967847e-17, 0.5099530164451239],
         [-0.4924410227809405, -3.2012547273253943e-17, 0.5228787563047644],
         [-0.47865734876644245, -3.278364463613709e-17, 0.5354717319026262],
         [-0.4645472659737015, -3.3532665829235916e-17, 0.5477041762877382],
         [-0.45008843570187157, -3.4256186129132005e-17, 0.5595201594822365],
         [-0.4353580459528023, -3.4958609557437374e-17, 0.5709916046171855],
         [-0.4203406343995568, -3.563827146809781e-17, 0.5820913259594315],
         [-0.40499041061826413, -3.6289303114448846e-17, 0.5927234796024944],
         [-0.3893961769426973, -3.691794129828541e-17, 0.6029899202492878],
         [-0.37354047471344276, -3.752201320383706e-17, 0.6128551631253922],
         [-0.35742192509874365, -3.809924288992922e-17, 0.6222820392907339],
         [-0.3410954702265476, -3.8653832360352056e-17, 0.6313391726749704],
         [-0.32454901917886597, -3.918391779948583e-17, 0.6399961248591096],
         [-0.3077464896456647, -3.968265207379642e-17, 0.6481410736665159],
         [-0.29076569459111473, -4.0157922848708783e-17, 0.6559028344491882],
         [-0.27359496184751014, -4.0607417017327386e-17, 0.6632436313047645],
         [-0.2562376775958344, -4.10289917814683e-17, 0.6701284696832173],
         [-0.2387306173770215, -4.142622454112497e-17, 0.6766157729601012],
         [-0.2210608959521123, -4.1796211619078793e-17, 0.6826581204877552],
         [-0.20322769420629688, -4.2135178501536966e-17, 0.6881938697779854],
         [-0.185273761676981, -4.244885506307234e-17, 0.693316596783907],
         [-0.1671896739899633, -4.273404065583344e-17, 0.6979740309593714],
         [-0.14899003192378396, -4.2989807641487775e-17, 0.7021510228207365],
         [-0.1307000956866102, -4.321936016851491e-17, 0.7058999000837464],
         [-0.11231314915482549, -4.34192438423744e-17, 0.709164248204342],
         [-0.09383953019484811, -4.3585653831766976e-17, 0.7110124576717894],
         [-0.07182162976344943, 4.4954081543323836e-21, 0.7131249160686077],
         [-0.07182162976344943, 4.4954081543323836e-21, 0.8561838026611327],
         [-0.14364550934591674, 4.4954081543323836e-21, 0.8561838026611327],
         [2.249819017971722e-06, 4.4954081543323836e-21, 0.9998315618260656],
         [0.14365000898395247, 4.4954081543323836e-21, 0.8561838026611327],
         [0.07182612940148543, 4.4954081543323836e-21, 0.8561838026611327],
         [0.07182612940148543, 4.4954081543323836e-21, 0.7131249160686077],
         [0.09232083450553186, -4.3599039927352754e-17, 0.7112732254161431],
         [0.11079918269794695, -4.343375234838748e-17, 0.7094011900887],
         [0.1291884393001287, -4.323543623750627e-17, 0.706162442214306],
         [0.1474948338640772, -4.301075279399389e-17, 0.7024930831196047],
         [0.1656995660937379, -4.2755898344792564e-17, 0.6983309941094709],
         [0.1837846383385905, -4.247141882159778e-17, 0.6936850909250928],
         [0.20176127113327005, -4.216257850250993e-17, 0.6886413457521513],
         [0.21961388354134048, -4.1827078311952345e-17, 0.6831622118371197],
         [0.23728288350866575, -4.145741300376667e-17, 0.6771251192085517],
         [0.25481206208438073, -4.106371923580243e-17, 0.6706956120520611],
         [0.27218045261861523, -4.0643650424946294e-17, 0.6638353677571813],
         [0.2893586016056411, -4.019547615953293e-17, 0.6565161265567881],
         [0.3063666222763842, -3.972387325320081e-17, 0.6488142666138033],
         [0.32317209651097223, -3.922523300930867e-17, 0.6406708534395305],
         [0.339731055644015, -3.869692234186699e-17, 0.6320428854768434],
         [0.3560926054939187, -3.814614407463974e-17, 0.6230479937643268],
         [0.37222646494855166, -3.757034428649845e-17, 0.6136444696045714],
         [0.3880938235437077, -3.6967647079408015e-17, 0.6038016772581842],
         [0.4037309563377685, -3.6342980760639236e-17, 0.5936001020903284],
         [0.4190949085494181, -3.569296651756439e-17, 0.5829845638998766],
         [0.4341338764953483, -3.5015339507127356e-17, 0.5719180750092004],
         [0.448911067167519, -3.431654980922522e-17, 0.5605059731973865],
         [0.46338530599337024, -3.359402941446065e-17, 0.5487063196779216],
         [0.4775051187044391, -3.284590736554943e-17, 0.5364885594146181],
         [0.49132980570942875, -3.2077523459593323e-17, 0.5239398979422069],
         [0.5048084106839476, -3.1286053765402596e-17, 0.5110142170958144],
         [0.5178780570629408, -3.046954636132539e-17, 0.49767963900359674],
         [0.5306298839314281, -2.9634453739276995e-17, 0.4840415413746517],
         [0.5430208106482807, -2.8778949846680915e-17, 0.47007010284058737],
         [0.5549910459715933, -2.7901490617731014e-17, 0.4557401062617147],
         [0.5666223746094745, -2.7007178851966142e-17, 0.4411348867297319],
         [0.5778622280471271, -2.6093997688563706e-17, 0.4262215078864688],
         [0.5886393783723654, -2.516037872225527e-17, 0.4109743480468314],
         [0.5990644468463835, -2.42119022416345e-17, 0.39548455105284286],
         [0.6090952111055409, -2.324738651593775e-17, 0.3797328238929749],
         [0.6186662072784886, -2.2265703732692736e-17, 0.3637007448415196],
         [0.627877172356834, -2.127122630353832e-17, 0.34745968732313603],
         [0.6366808614641742, -2.026279712540406e-17, 0.3309905807522763],
         [0.6449904356921378, -1.9238942346359936e-17, 0.31427009606888806],
         [0.652927817545072, -1.8204086835430034e-17, 0.29736978957530297],
         [0.6604516561462216, -1.715754848071208e-17, 0.280278189502196],
         [0.6674847982101083, -1.6098514334581373e-17, 0.2629818594900687],
         [0.674143715405849, -1.50303989394191e-17, 0.24553821602796122],
         [0.6804045691358974, -1.3952659666794092e-17, 0.2279443931617514],
         [0.6860798685037115, -1.2864068559293838e-17, 0.21015687591052856],
         [0.6913656243657678, -1.1767894533321676e-17, 0.19224897435954677],
         [0.6963078955666434, -1.066296532535281e-17, 0.1742394069382137],
         [0.7005347458787325, -9.55304272027608e-18, 0.15605599426428968],
         [0.7043918301579966, -8.436053328319361e-18, 0.1377793594104616],
         [0.7086930922042123, -7.294423440342042e-18, 0.1196237269495816],
         [0.7097304006221763, -6.204756528444624e-18, 0.10077802993805608],
         [0.7131083084219872, 4.4954081543323836e-21, 0.07182464847568246],
         [0.8567560675869216, 4.4954081543323836e-21, 0.07182464847568246],
         [0.8567560675869216, 4.4954081543323836e-21, 0.14364852805814995],
         [1.000403826751859, 4.4954081543323836e-21, 7.688932151231638e-07],
         [0.8567560675869216, 4.4954081543323836e-21, -0.14364699027171945],
         [0.8567560675869216, 4.4954081543323836e-21, -0.07182311068925219],
         [0.7131083084219872, 4.4954081543323836e-21, -0.07182311068925219],
         [0.708722590618041, 6.508670168317373e-18, -0.10528631250836548],
         [0.7064419060540527, 7.58793699591616e-18, -0.12339333471294958],
         [0.7036523274518477, 8.696114566406692e-18, -0.1419543469692213],
         [0.7001433111365613, 9.802727257137853e-18, -0.16027156582054655],
         [0.6951538953132701, 1.0921201461136248e-17, -0.17826955387725682],
         [0.6900873760985506, 1.2026081083442728e-17, -0.19624127298397945],
         [0.6849307255678295, 1.311781142375181e-17, -0.21418727467184395],
         [0.6789878621119937, 1.4203495165434265e-17, -0.23189051791029433],
         [0.6726814857263902, 1.5279923315569483e-17, -0.24946360155208466],
         [0.665991453020398, 1.634739005093202e-17, -0.2668974094780641],
         [0.6587832574887375, 1.740207731293927e-17, -0.28412359700934114],
         [0.6511861166414, 1.8446349383593318e-17, -0.30117835756224465],
         [0.6432015496809596, 1.9480041140217602e-17, -0.3180586151640961],
         [0.6347008744402949, 2.0498090251450923e-17, -0.3346849466164433],
         [0.625825052884126, 2.1503862445310485e-17, -0.35111058337460604],
         [0.6165742058291214, 2.2497106567100608e-17, -0.3673315323406521],
         [0.6068459404370045, 2.3473110543324713e-17, -0.38327078135569387],
         [0.5967501342401732, 2.443477284610771e-17, -0.3989758955306308],
         [0.5862855161506727, 2.5381775974444852e-17, -0.4144417019657607],
         [0.5753389608145881, 2.6308132054075142e-17, -0.429570206403751],
         [0.5640335739026898, 2.7217915563604288e-17, -0.4444280983668205],
         [0.5523669490867575, 2.811071963628483e-17, -0.4590087068777064],
         [0.5402592292888047, 2.898120297731666e-17, -0.473224925332833],
         [0.5278119969813545, 2.9833275272132993e-17, -0.48714014067374223],
         [0.5150237132057961, 3.0666540199875267e-17, -0.5007477133234475],
         [0.5017876916487845, 3.1473005163888797e-17, -0.5139197060634855],
         [0.4882374155153429, 3.2259441314071075e-17, -0.5267632938489574],
         [0.4743693220473693, 3.302522649932876e-17, -0.5392686372669097],
         [0.46014081229572595, 3.37659304770838e-17, -0.5513619540248029],
         [0.4456202893407636, 3.4484361262685875e-17, -0.563097158891264],
         [0.43080366805496506, 3.517975337078781e-17, -0.5744629778810559],
         [0.4156458793198201, 3.584788621773989e-17, -0.5853685432471336],
         [0.4002350021157505, 3.6493725493083256e-17, -0.5959078929708035],
         [0.38456728994320033, 3.7115568286743994e-17, -0.6060682560924087],
         [0.3686222754871191, 3.771538527312899e-17, -0.6157868587625557],
         [0.35245361721991325, 3.828042876140546e-17, -0.6251219580702674],
         [0.3360581526944811, 3.879809969884935e-17, -0.6340609323222048],
         [0.31939533440484036, 3.9383621751893485e-17, -0.6424889470086936],
         [0.30255103999403216, 3.987968178912845e-17, -0.6505426390180186],
         [0.28552099890769184, 4.031692760241432e-17, -0.6582026679594813],
         [0.26830429006238105, 4.048650017295732e-17, -0.6654346056094138],
         [0.2509092589550268, 4.1106139793236354e-17, -0.6722125677539225],
         [0.2333317288380462, 4.252187942178411e-17, -0.6785204431140072],
         [0.21555938310462627, 4.142247794831148e-17, -0.6842444761639082],
         [0.1977105982940524, 4.1243678058398196e-17, -0.689733951999861],
         [0.17978777606106444, 4.2048113803532293e-17, -0.6949590108787613],
         [0.16174217253160061, 4.438642454105753e-17, -0.6998027165032189],
         [0.1434651010536516, 4.5393681464816715e-17, -0.7035110337630863],
         [0.12501521300043517, 4.497068025544718e-17, -0.7063358327147998],
         [0.10613646184823812, 3.424160006334484e-17, -0.7089322732981522],
         [0.0883883748395849, 2.084429443409713e-17, -0.7108334068614973],
         [0.07182612940148561, 4.4954081543323836e-21, -0.7122290885643646],
         [0.07182612940148564, 4.4954081543323836e-21, -0.8558768477293006],
         [0.14365000898395272, 4.4954081543323836e-21, -0.8558768477293006],
         [2.2498190184895382e-06, 4.4954081543323836e-21, -0.9995246068942343]]

SETUP = [[0.388453, 4.3419999999999996e-10, 0.0640551],
         [0.3849475437658911, 5.429815840160516e-09, -0.06545923386732505],
         [0.33373654860537233, -3.296759258867726e-09, -0.1986090011667963], [0.229441, 5.43855e-10, -0.315191],
         [0.120118, -2.75026e-10, -0.37044], [0.000135984, 1.45413e-10, -0.389548], [-0.120446, 0.0, -0.37046],
         [-0.228922, 0.0, -0.315143], [-0.315161, 0.0, -0.228959], [-0.370454, 0.0, -0.120373],
         [-0.389545, 0.0, 2.1800700000000003e-07], [-0.370453, 0.0, 0.120373], [-0.315161, 0.0, 0.22896],
         [-0.228922, 0.0, 0.315143], [-0.120445, 0.0, 0.37046], [0.000136324, 1.34338e-10, 0.389548],
         [0.120118, -2.53931e-10, 0.37044], [0.229441, 5.013519999999999e-10, 0.315191],
         [0.314213, -1.16457e-09, 0.228864], [0.372449, 4.75637e-09, 0.120562],
         [0.388453, 4.3419999999999996e-10, 0.0640551], [0.388453, 4.3419999999999996e-10, 0.0640551],
         [1.0014, 0.0, -0.0362538], [0.963591, 0.0, -0.27497], [0.734694, 0.0, -0.238716], [0.624968, 0.0, -0.454066],
         [0.78884, 0.0, -0.617938], [0.617938, 0.0, -0.78884], [0.454066, 0.0, -0.624968], [0.238716, 0.0, -0.734694],
         [0.27497, 0.0, -0.963591], [0.0362538, 0.0, -1.0014], [-2.3022399999999998e-08, 0.0, -0.772503],
         [-0.238716, 0.0, -0.734694], [-0.343929, 0.0, -0.941185], [-0.559278, 0.0, -0.831459],
         [-0.454066, 0.0, -0.624968], [-0.624968, 0.0, -0.454066], [-0.831459, 0.0, -0.559278],
         [-0.941185, 0.0, -0.343929], [-0.734694, 0.0, -0.238716], [-0.772503, 0.0, 0.0], [-1.0014, 0.0, 0.0362538],
         [-0.963591, 0.0, 0.27497], [-0.734694, 0.0, 0.238716], [-0.624968, 0.0, 0.454066], [-0.788841, 0.0, 0.617938],
         [-0.617938, 0.0, 0.78884], [-0.454066, 0.0, 0.624968], [-0.238717, 0.0, 0.734694], [-0.27497, 0.0, 0.963592],
         [-0.0362538, 0.0, 1.001401], [0.0, 0.0, 0.772503], [0.238717, 0.0, 0.734694], [0.343929, 0.0, 0.941185],
         [0.559279, 0.0, 0.83146], [0.454066, 0.0, 0.624968], [0.624968, 0.0, 0.454066], [0.83146, 0.0, 0.559279],
         [0.941186, 0.0, 0.343929], [0.734694, 0.0, 0.238717], [0.772503, -8.63339e-09, 5.1800300000000004e-08]]
STAR = [[1.7004453639835406e-15, -0.7200345985899305, -7.942952889804963e-16],
        [0.26058532048278865, -0.9725674676653387, 1.9656927610124178e-16],
        [0.3643968933013128, -0.6218672562759475, 1.4280045265640082e-15],
        [0.71275394524471, -0.7127549886850846, 8.41175905342258e-16],
        [0.6310585453961821, -0.3552056041810745, 1.3750926261939013e-15],
        [0.9725664242249659, -0.26058566829624585, 6.602336936254819e-16],
        [0.7292258877101586, 0.009191289120243706, 5.81414120642293e-16],
        [0.9725664242249655, 0.2605842770424157, 1.4292380934217856e-15],
        [0.6310585453961821, 0.37358985723204086, 1.1369890745284183e-15],
        [0.7127539452447106, 0.712753597431252, 5.697625877670944e-16],
        [0.3643968933013135, 0.6402498345164203, -5.297357871299572e-16],
        [0.26058532048278943, 0.9725674676653387, 9.316470112006479e-16],
        [7.679430676054701e-16, 0.7384138272094085, -1.4292380934217856e-15],
        [-0.2605853204827893, 0.9725674676653387, 8.63793681806856e-16],
        [-0.36439689330131175, 0.6402498345164231, -6.675665889151998e-17],
        [-0.7127539452447099, 0.712753597431252, 4.3405592897951015e-16],
        [-0.6310585453961812, 0.37358985723204086, 7.930617221227221e-16],
        [-0.9725664242249659, 0.2605842770424157, 9.316470112006479e-16],
        [-0.7292258877101601, 0.009191289120240195, -5.297357871299572e-16],
        [-0.9725664242249659, -0.2605856682962476, 7.054692465546765e-16],
        [-0.6310585453961819, -0.3552056041810745, 1.1634450247134728e-15],
        [-0.71275394524471, -0.7127549886850846, 6.828514700900795e-16],
        [-0.36439689330131286, -0.6218672562759475, 4.226784195319719e-16],
        [-0.26058532048278743, -0.9725674676653387, 1.4292380934217856e-15],
        [1.7004453639835406e-15, -0.7200345985899305, -7.942952889804963e-16]]
DIAMOND = [[0.0, 1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0], [-1.0, 0.0, 0.0], [0.0, 0.0, -1.0],
           [0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [0.0, -1.0, 0.0], [0.0, 0.0, -1.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0],
           [-1.0, 0.0, 0.0], [0.0, -1.0, 0.0], [1.0, 0.0, 0.0]]
STARSQUEEZE = [[0.06, 0.0, -0.9], [0.0, 0.0, -1.22], [-0.06, 0.0, -0.9], [-0.09, 0.0, -0.81],
               [-0.16, 0.0, -0.61], [-0.23, 0.0, -0.48], [-0.33, 0.0, -0.33], [-0.48, 0.0, -0.23],
               [-0.62, 0.0, -0.16], [-0.8, 0.0, -0.09], [-0.91, 0.0, -0.06], [-1.19, 0.0, 0.0], [-0.91, 0.0, 0.06],
               [-0.8, 0.0, 0.09], [-0.62, 0.0, 0.16], [-0.48, 0.0, 0.23], [-0.33, 0.0, 0.33], [-0.23, 0.0, 0.48],
               [-0.16, 0.0, 0.62], [-0.09, 0.0, 0.8], [-0.06, 0.0, 0.91], [0.0, 0.0, 1.19], [0.06, 0.0, 0.91],
               [0.09, 0.0, 0.8], [0.16, 0.0, 0.62], [0.23, 0.0, 0.48], [0.33, 0.0, 0.33], [0.48, 0.0, 0.23],
               [0.62, 0.0, 0.16], [0.8, 0.0, 0.09], [0.91, 0.0, 0.06], [1.19, 0.0, 0.0], [0.91, 0.0, -0.06],
               [0.8, 0.0, -0.09], [0.62, 0.0, -0.16], [0.48, 0.0, -0.23], [0.33, 0.0, -0.33], [0.23, 0.0, -0.48],
               [0.16, 0.0, -0.61], [0.1, 0.0, -0.77], [0.06, 0.0, -0.9], [0.06, 0.0, -0.9], [0.06, 0.0, -0.9],
               [0.06, 0.0, -0.9]]

ad_show_ui()