import re
from functools import partial
from string import digits

import maya.OpenMaya as om
import pymel.core as pm

import ad_controller_lib as al
import ad_controller_shp as ac

reload(al)

layout = 400
percentage = 0.01 * layout
on_selector = 0
previous_value = 0


def ad_show_ui():
    adien_controller = 'AD_Controller'
    shape_controller = 'Shape_Controller'
    pm.window(adien_controller, exists=True)
    if pm.window(adien_controller, exists=True):
        pm.deleteUI(adien_controller)
        if pm.window(shape_controller, exists=True):
            pm.deleteUI(shape_controller)
    with pm.window(adien_controller, title='AD Controller', width=layout, height=200):
        with pm.tabLayout('tab', width=layout * 1.01, height=200):
            with pm.scrollLayout('Create Controller', p='tab'):
                with pm.columnLayout('Create_Controller_Column', w=layout, co=('both', 1 * percentage), adj=1):
                    # ADDITIONAL
                    with pm.frameLayout(collapsable=True, l='Naming', mh=1):
                        with pm.rowColumnLayout(nc=8, rowAttach=(2, 'top', 0),
                                                cs=[(3, 1 * percentage), (5, 1 * percentage),
                                                    (7, 1 * percentage)],
                                                cw=[(1, 12 * percentage), (2, 7 * percentage), (3, 13 * percentage),
                                                    (4, 20 * percentage), (5, 15 * percentage), (6, 9.5 * percentage),
                                                    (8, 8 * percentage)]):
                            pm.checkBox('Prefix_1', label='Prfx 1:', cc=partial(ad_enabling_disabling_ui,
                                                                                ['Prefix_1_Text'], 'L_'), value=False)
                            al.ad_lib_defining_object_text_field(define_object='Prefix_1_Text', tx='L_', enable=False)

                            pm.checkBox('Name_CheckBox', label='Name:', cc=partial(ad_enabling_disabling_ui,
                                                                                   ['Name_Text'], ''), value=False)
                            al.ad_lib_defining_object_text_field(define_object='Name_Text', enable=False)
                            pm.checkBox('Prefix_2', label='Prefix 2:',
                                        cc=partial(ad_enabling_disabling_ui, ['Prefix_2_Text'], 'LFT'), value=False)
                            al.ad_lib_defining_object_text_field(define_object='Prefix_2_Text', tx='LFT', enable=False)

                            pm.text('Suffix:')
                            pm.textField('Suffix_Main', tx='ctrl')

                    # CONNECTION
                    with pm.frameLayout(collapsable=True, l='Connection', mh=1):
                        with pm.rowLayout('Connection', nc=3,
                                          cw3=(18.5 * percentage, 32 * percentage, 40 * percentage),
                                          cl3=('right', 'right', 'right'),
                                          columnAttach=[(1, 'both', 0.5 * percentage), (2, 'both', 0.5 * percentage),
                                                        (3, 'both', 0.5 * percentage), ],
                                          rowAttach=[(1, 'top', 0), (3, 'top', 0)]):
                            pm.text('')
                            ad_channelbox_constraint_connection()
                            ad_channelbox_direct_connection()

                        with pm.rowLayout(nc=3, cw3=(19 * percentage, 38 * percentage, 38 * percentage),
                                          cl3=('right', 'right', 'right'), columnAttach=[(2, 'both', 0.15 * percentage),
                                                                                         (3, 'both',
                                                                                          0.15 * percentage)]):
                            pm.text('')
                            pm.button("List_Connection", l="List Connection", c=partial(ad_create_list_connection_button))
                            pm.button('Create_Connection', l="Create Connection",
                                      c=partial(ad_create_connection_button))

                    # pm.separator(h=5, st="in", w=90 * percentage)
                    with pm.frameLayout(collapsable=True, l='Color', mh=1):
                        with pm.rowLayout('Palette_Port', nc=2, cw2=(18.5 * percentage, 69 * percentage),
                                          cl2=('right', 'left'),
                                          columnAttach=[(1, 'both', 0.5 * percentage), (2, 'both', 0.5 * percentage)]):
                            pm.text('')
                            ad_color_index()

                        with pm.rowLayout(nc=3, cw3=(19 * percentage, 38 * percentage, 38 * percentage),
                                          cl3=('right', 'right', 'right'), columnAttach=[(2, 'both', 0.15 * percentage),
                                                                                         (3, 'both',
                                                                                          0.15 * percentage)]):
                            pm.text(label='')
                            pm.button('Reset_Color', l="Reset Color", c=partial(ad_reset_color_button))
                            pm.button("Replace_Color", l="Replace Color", c=partial(ad_replace_color_button))
                    # pm.separator(h=5, st="in", w=90 * percentage)

                    with pm.frameLayout(collapsable=True, l='Channel', mh=1):
                        with pm.rowLayout(nc=4,
                                          cw4=(18.5 * percentage, 32 * percentage, 27 * percentage, 22 * percentage),
                                          cl4=('right', 'left', 'left', 'left'),
                                          columnAttach=[(1, 'both', 0.5 * percentage), (2, 'both', 0.5 * percentage),
                                                        (3, 'both', 0.5 * percentage), (4, 'both', 0.5 * percentage), ],
                                          rowAttach=[(1, 'top', 0), (2, 'top', 0), (3, 'top', 0), (4, 'top', 0)]):
                            pm.text('')
                            ad_channelbox_translation()
                            ad_channelbox_rotation()
                            ad_channelbox_scale()
                        with pm.rowLayout(nc=3, cw3=(19 * percentage, 38 * percentage, 38 * percentage),
                                          cl3=('right', 'right', 'right'), columnAttach=[(2, 'both', 0.15 * percentage),
                                                                                         (3, 'both',
                                                                                          0.15 * percentage)]):
                            pm.text(label='')
                            pm.button("Hide_Unhide_Channel", l="Hide/Unhide", c=partial(ad_hide_unhide_button))
                            pm.button('Lock_Unlock_Channel', l="Lock/Unlock",
                                      c=partial(ad_lock_unlock_button))

                    # pm.separator(h=5, st="in", w=90 * percentage)
                    with pm.frameLayout(collapsable=True, l='Resize', mh=1):
                        with pm.rowLayout(nc=2, cw2=(18.5 * percentage, 77 * percentage), cl2=('right', 'left'),
                                          columnAttach=[(1, 'both', 0.5 * percentage),
                                                        (2, 'both', 0.5 * percentage)], ):
                            pm.text('')
                            pm.floatSlider('Controller_Resize', min=-1.0, value=0.0, max=1.0, step=0.0001,
                                           dragCommand=partial(ad_controller_resize_slider),
                                           changeCommand=partial(ad_controller_resize_reset))
                        with pm.rowLayout(nc=2, cw2=(18.5 * percentage, 77 * percentage), cl2=('right', 'left'),
                                          columnAttach=[(1, 'both', 0), (2, 'both', 0)]):
                            pm.text('')
                            pm.button('Select_All_AD_Controller', l="Select All AD Controller",
                                      c=partial(ad_select_all_ad_controller_button))
                    # GROUP AND SHAPE
                    with pm.frameLayout(collapsable=True, l='Group and Shape', mh=1):
                        with pm.rowColumnLayout(nc=3, cw=[(2, 56 * percentage)], cs=[(3, 1 * percentage)]):
                            pm.checkBox(label='Name List:',
                                        cc=partial(ad_enabling_disabling_ui, ['Parent_Group_Name'],
                                                   'Main,Offset'),
                                        value=True)
                            al.ad_lib_defining_object_text_field(define_object='Parent_Group_Name', tx='Main,Offset',
                                                                 enable=True
                                                                 )
                            pm.button("Create_Grp_Select", l="Create Group", c=partial(ad_create_group_button))

                        with pm.rowLayout(nc=2, cw2=(18.5 * percentage, 77 * percentage), cl2=('right', 'left'),
                                          columnAttach=[(1, 'both', 0 * percentage), (2, 'both', 0 * percentage)]):
                            pm.text('')
                            with pm.rowColumnLayout(nc=9,
                                                    cs=[(2, 0.25 * percentage), (3, 0.25 * percentage),
                                                        (4, 0.25 * percentage), (5, 0.25 * percentage),
                                                        (6, 0.25 * percentage), (7, 0.25 * percentage),
                                                        (8, 0.25 * percentage)]
                                                    ):
                                icon_radio_control = pm.iconTextRadioCollection()
                                circle = pm.iconTextRadioButton(st='iconOnly', image='ad_icons/circle.png',
                                                                onCommand=lambda x: ad_on_selection_ctrl_shape(1))
                                # locator
                                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/locator.png',
                                                       onCommand=lambda x: ad_on_selection_ctrl_shape(2))
                                # cube
                                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/cube.png',
                                                       onCommand=lambda x: ad_on_selection_ctrl_shape(3))
                                # circlehalf
                                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/circlehalf.png',
                                                       onCommand=lambda x: ad_on_selection_ctrl_shape(4))
                                # square
                                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/square.png',
                                                       onCommand=lambda x: ad_on_selection_ctrl_shape(5))
                                # joint
                                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/joint.png',
                                                       onCommand=lambda x: ad_on_selection_ctrl_shape(6))
                                # capsule
                                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/capsule.png',
                                                       onCommand=lambda x: ad_on_selection_ctrl_shape(7))
                                # stickcircle
                                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/stickcircle.png',
                                                       onCommand=lambda x: ad_on_selection_ctrl_shape(8))
                                # continues
                                pm.iconTextButton(st='iconOnly', hi='ad_icons/continue_hi.png',
                                                  image='ad_icons/continue.png',
                                                  c=partial(ad_shape_controller_ui, circle))

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
                                pm.button("Replace_Controller", l="Replace Ctrl",
                                          c=partial(ad_replacing_controller_button))
                                pm.button("Tag_as_AD_Controller", l="Tag as AD Ctrl",
                                          c=partial(ad_tagging_untagging_button, True))
                                pm.button('Untag_AD_Controller', l="Untag AD Ctrl",
                                          c=partial(ad_tagging_untagging_button, False))

                    with pm.frameLayout(collapsable=True, l='Additional', mh=1):
                        with pm.columnLayout():
                            with pm.rowLayout(nc=2, cw2=(17.5 * percentage, 50 * percentage), cl2=('right', 'left'),
                                              columnAttach=[(1, 'both', 0.5 * percentage),
                                                            (2, 'both', 0.5 * percentage)]):
                                pm.text('')
                                with pm.columnLayout():
                                    with pm.rowColumnLayout(nc=2):
                                        pm.checkBox('Adding_Ctrl_Child', label='Add Child Ctrl:',
                                                    cc=partial(ad_enabling_disabling_ui, ['Suffix_Child_Ctrl'],
                                                               'Child'),
                                                    value=False)
                                        pm.textField('Suffix_Child_Ctrl', enable=False, tx='Child')
                                    with pm.rowColumnLayout():
                                        pm.checkBox('Target_Visibility', label='Add Attribute for Target Visibility',
                                                    value=False)
                                        pm.checkBox('Add_Pivot_Ctrl', label='Add Pivot Controller', value=False,
                                                    enable=False)

                    # pm.separator(h=15, st="in", w=90 * percentage)
                    with pm.frameLayout(collapsable=True, l='Run', mh=3):
                        with pm.rowLayout(nc=2, cw2=(18.5 * percentage, 77 * percentage), cl2=('right', 'left'),
                                          columnAttach=[(1, 'both', 0), (2, 'both', 0)]):
                            pm.text(label='')
                            pm.button('Create_Controller', l="Create Controller With All Defined Above!",
                                      bgc=(0, 0.5, 0),
                                      c=partial(ad_create_controller_button))
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
            with pm.scrollLayout('Controller Utilities', p='tab'):
                with pm.columnLayout('Controller_Utilities_Column', w=layout, co=('both', 1 * percentage), adj=1):
                    # pm.separator(h=5, st="in", w=90 * percentage)
                    with pm.frameLayout(collapsable=True, l='Save/Load', mh=1):
                        with pm.columnLayout():
                            with pm.rowLayout(nc=1, cw=(1, 95 * percentage), cal=(1, 'right'),
                                              columnAttach=[(1, 'both', 0.25 * percentage), ], ):
                                pm.button('Select_All_AD_Controller', l="Select All AD Controller",
                                          c=partial(ad_select_all_ad_controller_button), bgc=(0.0, 0.5, 0.0))

                            with pm.rowLayout(nc=2, cw2=(47.5 * percentage, 47.5 * percentage), cl2=('right', 'right'),
                                              columnAttach=[(1, 'both', 0.15 * percentage),
                                                            (2, 'both', 0.15 * percentage)]):
                                pm.button("Save", l="Save", c='', bgc=(0.5, 0.0, 0.0))
                                pm.button('Load', l="Load", c='', bgc=(0.0, 0.0, 0.5))
                    with pm.frameLayout(collapsable=True, l='Rotate', mh=1):
                        with pm.rowLayout(nc=2, cw2=(18 * percentage, 77 * percentage), cl2=('right', 'left'),
                                          columnAttach=[(1, 'both', 0.5 * percentage), (2, 'both', 0.5 * percentage)]):
                            pm.text('Rotate:')
                            with pm.rowLayout(nc=4, cw4=(
                            10 * percentage, 21.5 * percentage, 21.5 * percentage, 21.5 * percentage),
                                              cl4=('center', 'center', 'center', 'center'),
                                              columnAttach=[(1, 'both', 0 * percentage), (2, 'both', 0 * percentage),
                                                            (3, 'both', 0 * percentage), (4, 'both', 0 * percentage)]):
                                pm.intField('Degree_Rotate', value=90)
                                pm.button("Rotate_X", l="X", c='', bgc=(0.5, 0, 0))
                                pm.button("Rotate_Y", l="Y", c='', bgc=(0, 0.5, 0))
                                pm.button('Rotate_Z', l="Z", c='', bgc=(0, 0, 0.5))
                        # pm.separator(h=5, st="in", w=90 * percentage)
                    with pm.frameLayout(collapsable=True, l='Mirror', mh=1):
                        with pm.rowColumnLayout(nc=3,
                                                cw=[(1, 42 * percentage), (2, 11 * percentage), (3, 42 * percentage)],
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
                                                  bc=partial(ad_adding_object_sel_to_textfield, 'From_Prefix'))
                            pm.text(label='>>>')
                            pm.textFieldButtonGrp('To_Prefix', label='', cal=(1, "right"),
                                                  cw3=(10 * percentage, 13 * percentage, 7 * percentage),
                                                  columnAttach=[(1, 'both', 0 * percentage),
                                                                (2, 'both', 0 * percentage),
                                                                (3, 'both', 0 * percentage)], bl="<<", tx='R_',
                                                  bc=partial(ad_adding_object_sel_to_textfield, 'To_Prefix'))
                        with pm.rowLayout(nc=3, cw3=(31.6 * percentage, 31.6 * percentage, 31.6 * percentage),
                                          cl3=('center', 'center', 'center'),
                                          columnAttach=[(1, 'both', 0 * percentage), (2, 'both', 0 * percentage),
                                                        (3, 'both', 0 * percentage)]):
                            pm.button("Mirror_X", l="X", c='', bgc=(0.5, 0, 0))
                            pm.button("Mirror_Y", l="Y", c='', bgc=(0, 0.5, 0))
                            pm.button('Mirror_Z', l="Z", c='', bgc=(0, 0, 0.5))
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


def ad_create_controller_button(*args):
    select = pm.ls(sl=1)

    # create controller
    if select:
        # query value of manipulation position
        manipulated_position = pm.manipPivot(q=True, p=True)[0]
        # query value of manipulation rotation
        manipulated_rotation = pm.manipPivot(q=True, o=True)[0]

        # create controller shape
        controller_shape_prefix_suffix = ad_main_ctrl_prefix_suffix_selection(select)

        # match position
        al.ad_lib_match_position_target_to_ctrl(selection=select, target=controller_shape_prefix_suffix[0],
                                                manipulated_position=manipulated_position,
                                                manipulated_rotation=manipulated_rotation)
        # add child controller
        add_child_ctrl = ad_child_ctrl(main_controller=controller_shape_prefix_suffix[0],
                                       main_name=controller_shape_prefix_suffix[1])

        # if component mode
        get_objects = []
        if '.' in str(select[0]):
            for item in select:
                get_object = item.split('.')
                parent_query = pm.listRelatives(get_object[0], p=True)
                get_objects.append(parent_query[0])

            listing = list(set(get_objects))
            for target in listing:
                # add connection
                if add_child_ctrl:
                    ad_connection(ctrl=add_child_ctrl[0], target=target)

                else:
                    ad_connection(ctrl=controller_shape_prefix_suffix[0][0], target=target)

                if pm.checkBox('Add_Pivot_Ctrl', q=True, value=True):
                    pm.displayWarning("Adding pivot controller is skipped, since it's component mode.")

                # add visibility to target
                ad_visibility_target(object=controller_shape_prefix_suffix[0][0],
                                     target=target)


        # object mode
        else:
            if add_child_ctrl:
                for target, child_ctrl in zip(select, add_child_ctrl):
                    # add connection
                    connection = ad_connection(ctrl=child_ctrl, target=target)
                    # add pivot controller
                    if pm.checkBox('Add_Pivot_Ctrl', q=True, value=True):
                        al.ad_lib_pivot_controller(controller=child_ctrl, parent_constraint_node=connection[0],
                                                   suffix='_' + ad_suffix_main())
            else:
                for ctrl, target, in zip(controller_shape_prefix_suffix[0], select):
                    connection = ad_connection(ctrl=ctrl, target=target)
                    # add pivot controller
                    if pm.checkBox('Add_Pivot_Ctrl', q=True, value=True):
                        al.ad_lib_pivot_controller(controller=ctrl, parent_constraint_node=connection[0],
                                                   suffix='_' + ad_suffix_main())

                    # add visibility to target
                    ad_visibility_target(object=ctrl, target=target)
    else:
        # create controller without selection
        controller_shape_prefix_suffix = ad_main_ctrl_prefix_suffix()
        # add child controller
        ad_child_ctrl(main_controller=controller_shape_prefix_suffix[0], main_name=controller_shape_prefix_suffix[1])

        # add pivot controller
        if pm.checkBox('Add_Pivot_Ctrl', q=True, value=True):
            pm.displayWarning("Adding pivot controller is skipped, since there is no object selection.")

    # grouping controller
    if pm.textField('Parent_Group_Name', q=True, enable=True):
        ad_main_ctrl_grouping(controller=controller_shape_prefix_suffix[0],
                              main_name=controller_shape_prefix_suffix[1],
                              prefix_2=al.ad_lib_prefix('Prefix_2_Text'))

    # controller color
    al.ad_lib_ctrl_color(ctrl=controller_shape_prefix_suffix[0], color=ad_set_color())

    # controller hide and unlock
    ad_hide_and_lock(controller_shape_prefix_suffix[0], value=True)


def ad_create_group_button(*args):
    select = pm.ls(sl=1)
    # grouping controller
    if pm.textField('Parent_Group_Name', q=True, enable=True):
        for item in select:
            name = ad_get_number_main_name(item)
            group = al.ad_lib_group_parent(groups=al.ad_lib_query_list_textfield_object('Parent_Group_Name')[0],
                                           name=name[1],
                                           suffix=al.ad_lib_get_suffix_main(item),
                                           prefix_number=name[0], prefix_2=al.ad_lib_prefix('Prefix_2_Text'))
            al.ad_lib_xform_position_rotation(origin=item, target=group[0])
            pm.parent(item, group[-1])
    else:
        pass


def ad_visibility_target(object, target):
    check_box = pm.checkBox('Target_Visibility', q=True, value=True)
    if check_box:
        al.ad_lib_display(object=object, target=target)
    else:
        pass


def ad_get_number_main_name(main_name):
    try:
        patterns = [r'\d+']
        name_number = al.ad_lib_main_name(main_name)
        for p in patterns:
            name_number = re.findall(p, name_number)[0]
    except:
        name_number = ''

    # get the prefix without number
    ad_main_name = str(al.ad_lib_main_name(main_name)).translate(None, digits)
    return name_number, ad_main_name


def ad_main_ctrl_grouping(controller, main_name, prefix_2):
    grouping_controller = []
    for object_controller, name in zip(controller, main_name):
        ad_main_name = ad_get_number_main_name(name)
        group_controller = al.ad_lib_group_parent(groups=al.ad_lib_query_list_textfield_object('Parent_Group_Name')[0],
                                                  name=ad_main_name[1],
                                                  suffix=ad_suffix_main(),
                                                  prefix_number=ad_main_name[0], prefix_2=prefix_2)

        al.ad_lib_xform_position_rotation(origin=object_controller, target=group_controller[0])
        pm.parent(object_controller, group_controller[-1])
        grouping_controller.append(group_controller)
        pm.select(cl=1)

    return grouping_controller


def ad_suffix_main():
    suffix = pm.textField('Suffix_Main', q=True, tx=True)
    if suffix:
        add_space = suffix.lower()
        return add_space
    else:
        om.MGlobal_displayError('suffix cannot be empty!')


def ad_child_ctrl(main_controller, main_name):
    controller_childs = []
    check_box = pm.checkBox('Adding_Ctrl_Child', q=True, value=True)
    query_name = al.ad_lib_query_textfield_object('Suffix_Child_Ctrl')[0]
    if check_box:
        for controller, name in zip(main_controller, main_name):
            ad_main_name = ad_get_number_main_name(name)

            object_main_shape = pm.listRelatives(controller, shapes=1)[0]
            controller_shape = ad_controller_shape(size_ctrl=0.8)
            controller_child = pm.rename(controller_shape,
                                         ad_main_name[1] + query_name.title() + ad_main_name[0] + al.ad_lib_prefix(
                                             'Prefix_2_Text') + '_' + ad_suffix_main())
            al.ad_lib_xform_position_rotation(origin=controller, target=controller_child)
            pm.parent(controller_child, controller)
            al.ad_lib_display(object=object_main_shape, target=controller_child, long_name=query_name + 'Ctrl',
                              default_vis=0,
                              k=False, cb=True)
            controller_childs.append(controller_child)
    else:
        pass
    # set color
    al.ad_lib_ctrl_color(ctrl=controller_childs, color=16)

    return controller_childs
def ad_create_list_connection_button(*args):
    list_object = pm.ls(sl=1)
    if list_object:
        al.ad_list_connections_object(list_object)
    else:
        om.MGlobal_displayError('Select minimum one object which has connection!')

def ad_create_connection_button(*args):
    list_controller = pm.ls(sl=1)
    if len(list_controller) < 2:
        om.MGlobal_displayError('Select minimum two objects!')
    else:
        instance_controller = list_controller.pop(0)
        for item in list_controller:
            ad_connection(ctrl=instance_controller, target=item)


def ad_connection(ctrl, target):
    connection = []
    if ad_query_lock_unlock_hide_unhide_channel('Point_Cons'):
        connection = al.ad_lib_point_constraint(obj_base=ctrl, obj_target=target)
    if ad_query_lock_unlock_hide_unhide_channel('Orient_Cons'):
        connection = al.ad_lib_orient_constraint(obj_base=ctrl, obj_target=target)
    if ad_query_lock_unlock_hide_unhide_channel('Scale_Cons'):
        connection = al.ad_lib_scale_constraint(obj_base=ctrl, obj_target=target)
    if ad_query_lock_unlock_hide_unhide_channel('Parent_Cons'):
        connection = al.ad_lib_parent_constraint(obj_base=ctrl, obj_target=target)
    if ad_query_lock_unlock_hide_unhide_channel('Parent'):
        connection = pm.parent(target, ctrl)
    if ad_query_lock_unlock_hide_unhide_channel('Direct_Trans'):
        connection = pm.connectAttr(ctrl + '.translate', target + '.translate')
    if ad_query_lock_unlock_hide_unhide_channel('Direct_Rot'):
        connection = pm.connectAttr(ctrl + '.rotate', target + '.rotate')
    if ad_query_lock_unlock_hide_unhide_channel('Direct_Scl'):
        connection = pm.connectAttr(ctrl + '.scale', target + '.scale')

    return connection


def ad_main_ctrl_prefix_suffix_selection(selection):
    controller_shape_prefix_suffix_app = []
    main_name_for_grp = []

    suffix = '_' + ad_suffix_main()
    al.ad_lib_query_textfield_object(object_define='Suffix_Main')
    al.ad_lib_query_textfield_object(object_define='Suffix_Child_Ctrl')
    al.ad_lib_query_list_textfield_object(object_define='Parent_Group_Name')

    if '.' in str(selection[0]):
        get_first_object = selection[0].split('Shape')[0]
        query_name = al.ad_lib_query_textfield_object('Name_Text')[0]
        query_name_object = al.ad_lib_main_name(get_first_object)
        controller_shape = ad_controller_shape(size_ctrl=1.0)
        if pm.textField('Name_Text', q=True, enable=True):
            main_name_for_grp.append(al.ad_lib_prefix('Prefix_1_Text') + query_name + suffix)
            controller_shape_prefix_suffix = pm.rename(controller_shape,
                                                       al.ad_lib_prefix(
                                                           'Prefix_1_Text') + query_name + al.ad_lib_prefix(
                                                           'Prefix_2_Text') + suffix)
            controller_shape_prefix_suffix_app.append(controller_shape_prefix_suffix)


        else:
            main_name_for_grp.append(al.ad_lib_prefix('Prefix_1_Text') + query_name_object + suffix)
            controller_shape_prefix_suffix = pm.rename(controller_shape,
                                                       al.ad_lib_prefix(
                                                           'Prefix_1_Text') + query_name_object + al.ad_lib_prefix(
                                                           'Prefix_2_Text') + suffix)
            controller_shape_prefix_suffix_app.append(controller_shape_prefix_suffix)

    else:
        for number, object in enumerate(selection):
            query_name = al.ad_lib_query_textfield_object('Name_Text')[0]
            query_name_object = al.ad_lib_main_name(object)
            controller_shape = ad_controller_shape(size_ctrl=1.0)
            if pm.textField('Name_Text', q=True, enable=True):
                if len(selection) > 1:
                    main_name_for_grp.append(
                        '%s%s%02d%s' % (al.ad_lib_prefix('Prefix_1_Text'), query_name, number + 1, suffix))
                    controller_shape_prefix_suffix = pm.rename(controller_shape,
                                                               '%s%s%02d%s%s' % (
                                                                   al.ad_lib_prefix('Prefix_1_Text'), query_name,
                                                                   number + 1,
                                                                   al.ad_lib_prefix('Prefix_2_Text'), suffix))
                else:
                    main_name_for_grp.append(al.ad_lib_prefix('Prefix_1_Text') + query_name + suffix)
                    controller_shape_prefix_suffix = pm.rename(controller_shape,
                                                               al.ad_lib_prefix(
                                                                   'Prefix_1_Text') + query_name + al.ad_lib_prefix(
                                                                   'Prefix_2_Text') + suffix)
                controller_shape_prefix_suffix_app.append(controller_shape_prefix_suffix)

            else:
                main_name_for_grp.append(al.ad_lib_prefix('Prefix_1_Text') + query_name_object + suffix)
                controller_shape_prefix_suffix = pm.rename(controller_shape,
                                                           al.ad_lib_prefix(
                                                               'Prefix_1_Text') + query_name_object + al.ad_lib_prefix(
                                                               'Prefix_2_Text') + suffix)
                controller_shape_prefix_suffix_app.append(controller_shape_prefix_suffix)

                pm.select(cl=1)
    # print controller_shape_prefix_suffix_app, main_name_for_grp
    return controller_shape_prefix_suffix_app, main_name_for_grp


def ad_main_ctrl_prefix_suffix():
    controller_shape_prefix_suffix_app = []
    main_name_for_grp = []
    suffix = '_' + ad_suffix_main()
    al.ad_lib_query_textfield_object(object_define='Suffix_Main')
    al.ad_lib_query_textfield_object(object_define='Suffix_Child_Ctrl')
    al.ad_lib_query_list_textfield_object(object_define='Parent_Group_Name')

    if al.ad_lib_query_textfield_object(object_define='Name_Text')[0]:
        query_name = al.ad_lib_query_textfield_object('Name_Text')[0]
        controller_shape = ad_controller_shape(size_ctrl=1.0)
        controller_shape_prefix_suffix = pm.rename(controller_shape,
                                                   al.ad_lib_prefix('Prefix_1_Text') + query_name + al.ad_lib_prefix(
                                                       'Prefix_2_Text') + suffix)
        controller_shape_prefix_suffix_app.append(controller_shape_prefix_suffix)
        main_name_for_grp.append(al.ad_lib_prefix('Prefix_1_Text') + query_name + suffix)

        pm.select(cl=1)

    else:
        controller_shape = ad_controller_shape(size_ctrl=1.0)
        main_name_for_grp.append(al.ad_lib_prefix('Prefix_1_Text') + controller_shape + suffix)
        controller_shape_prefix_suffix = pm.rename(controller_shape,
                                                   al.ad_lib_prefix(
                                                       'Prefix_1_Text') + controller_shape + al.ad_lib_prefix(
                                                       'Prefix_2_Text') + suffix)
        controller_shape_prefix_suffix_app.append(controller_shape_prefix_suffix)
        pm.select(cl=1)

    return controller_shape_prefix_suffix_app, main_name_for_grp


###########

def ad_replacing_controller_button(*args):
    list_controller = pm.ls(sl=1)
    # instance_controller = list_controller.pop(0)
    if not list_controller:
        om.MGlobal.displayError("No curves selected, you have to select origin and target curve!")
        return False

    else:
        controller_replacing = al.ad_lib_replacing_controller(list_controller)
        al.ad_lib_replacing_color(controller_replacing[0], controller_replacing[1])


def ad_hide_unhide_button(*args):
    selection = pm.ls(selection=True)
    if not selection:
        om.MGlobal.displayError("No objects selected")
        return False
    else:
        for item in selection:
            ad_hide_unhide(ctrl=item)


def ad_lock_unlock_button(*args):
    selection = pm.ls(selection=True)
    if not selection:
        om.MGlobal.displayError("No objects selected")
        return False
    else:
        for item in selection:
            ad_lock_unlock(ctrl=item)


def ad_hide_unhide(ctrl):
    if ad_query_lock_unlock_hide_unhide_channel("Trans_X"):
        al.ad_lib_hide_unhide_attr(channel=['tx'], ctrl=ctrl)
    if ad_query_lock_unlock_hide_unhide_channel("Trans_Y"):
        al.ad_lib_hide_unhide_attr(channel=['ty'], ctrl=ctrl)
    if ad_query_lock_unlock_hide_unhide_channel("Trans_Z"):
        al.ad_lib_hide_unhide_attr(channel=['tz'], ctrl=ctrl)
    if ad_query_lock_unlock_hide_unhide_channel('Rot_X'):
        al.ad_lib_hide_unhide_attr(channel=['rx'], ctrl=ctrl)
    if ad_query_lock_unlock_hide_unhide_channel('Rot_Y'):
        al.ad_lib_hide_unhide_attr(channel=['ry'], ctrl=ctrl)
    if ad_query_lock_unlock_hide_unhide_channel('Rot_Z'):
        al.ad_lib_hide_unhide_attr(channel=['rz'], ctrl=ctrl)
    if ad_query_lock_unlock_hide_unhide_channel('Scl_X'):
        al.ad_lib_hide_unhide_attr(channel=['sx'], ctrl=ctrl)
    if ad_query_lock_unlock_hide_unhide_channel('Scl_Y'):
        al.ad_lib_hide_unhide_attr(channel=['sy'], ctrl=ctrl)
    if ad_query_lock_unlock_hide_unhide_channel('Scl_Z'):
        al.ad_lib_hide_unhide_attr(channel=['sz'], ctrl=ctrl)
    if ad_query_lock_unlock_hide_unhide_channel('Visibility'):
        al.ad_lib_hide_unhide_attr(channel=['v'], ctrl=ctrl)
    if ad_query_lock_unlock_hide_unhide_channel('User_Def'):
        list_attribute = ad_query_user_defined_channel(ctrl)
        al.ad_lib_hide_unhide_attr(channel=list_attribute, ctrl=ctrl)


def ad_lock_unlock(ctrl):
    if ad_query_lock_unlock_hide_unhide_channel("Trans_X"):
        al.ad_lib_lock_unlock_attr(channel=['tx'], ctrl=ctrl)
    if ad_query_lock_unlock_hide_unhide_channel("Trans_Y"):
        al.ad_lib_lock_unlock_attr(channel=['ty'], ctrl=ctrl)
    if ad_query_lock_unlock_hide_unhide_channel("Trans_Z"):
        al.ad_lib_lock_unlock_attr(channel=['tz'], ctrl=ctrl)
    if ad_query_lock_unlock_hide_unhide_channel('Rot_X'):
        al.ad_lib_lock_unlock_attr(channel=['rx'], ctrl=ctrl)
    if ad_query_lock_unlock_hide_unhide_channel('Rot_Y'):
        al.ad_lib_lock_unlock_attr(channel=['ry'], ctrl=ctrl)
    if ad_query_lock_unlock_hide_unhide_channel('Rot_Z'):
        al.ad_lib_lock_unlock_attr(channel=['rz'], ctrl=ctrl)
    if ad_query_lock_unlock_hide_unhide_channel('Scl_X'):
        al.ad_lib_lock_unlock_attr(channel=['sx'], ctrl=ctrl)
    if ad_query_lock_unlock_hide_unhide_channel('Scl_Y'):
        al.ad_lib_lock_unlock_attr(channel=['sy'], ctrl=ctrl)
    if ad_query_lock_unlock_hide_unhide_channel('Scl_Z'):
        al.ad_lib_lock_unlock_attr(channel=['sz'], ctrl=ctrl)
    if ad_query_lock_unlock_hide_unhide_channel('Visibility'):
        al.ad_lib_lock_unlock_attr(channel=['v'], ctrl=ctrl)
    if ad_query_lock_unlock_hide_unhide_channel('User_Def'):
        list_attribute = ad_query_user_defined_channel(ctrl)
        al.ad_lib_lock_unlock_attr(channel=list_attribute, ctrl=ctrl)


def ad_hide_and_lock(ctrl, value):
    for item in ctrl:
        if ad_query_lock_unlock_hide_unhide_channel("Trans_X"):
            al.ad_lib_lock_hide_attr(lock_hide_channel=['tx'], ctrl=item,
                                     hide_object=value)
        if ad_query_lock_unlock_hide_unhide_channel("Trans_Y"):
            al.ad_lib_lock_hide_attr(lock_hide_channel=['ty'], ctrl=item,
                                     hide_object=value)
        if ad_query_lock_unlock_hide_unhide_channel("Trans_Z"):
            al.ad_lib_lock_hide_attr(lock_hide_channel=['tz'], ctrl=item,
                                     hide_object=value)
        if ad_query_lock_unlock_hide_unhide_channel('Rot_X'):
            al.ad_lib_lock_hide_attr(lock_hide_channel=['rx'], ctrl=item,
                                     hide_object=value)
        if ad_query_lock_unlock_hide_unhide_channel('Rot_Y'):
            al.ad_lib_lock_hide_attr(lock_hide_channel=['ry'], ctrl=item,
                                     hide_object=value)
        if ad_query_lock_unlock_hide_unhide_channel('Rot_Z'):
            al.ad_lib_lock_hide_attr(lock_hide_channel=['rz'], ctrl=item,
                                     hide_object=value)
        if ad_query_lock_unlock_hide_unhide_channel('Scl_X'):
            al.ad_lib_lock_hide_attr(lock_hide_channel=['sx'], ctrl=item,
                                     hide_object=value)
        if ad_query_lock_unlock_hide_unhide_channel('Scl_Y'):
            al.ad_lib_lock_hide_attr(lock_hide_channel=['sy'], ctrl=item,
                                     hide_object=value)
        if ad_query_lock_unlock_hide_unhide_channel('Scl_Z'):
            al.ad_lib_lock_hide_attr(lock_hide_channel=['sz'], ctrl=item,
                                     hide_object=value)
        if ad_query_lock_unlock_hide_unhide_channel('Visibility'):
            al.ad_lib_lock_hide_attr(lock_hide_channel=['v'], ctrl=item,
                                     hide_object=value)


def ad_query_user_defined_channel(ctrl):
    list_attr = pm.listAttr(ctrl, ud=1)
    if 'AD_Controller' in list_attr:
        list_attr.remove('AD_Controller')
        return list_attr
    else:
        return list_attr


def ad_query_lock_unlock_hide_unhide_channel(channel_name):
    value = pm.checkBox(channel_name, q=True, value=True)
    return value


def ad_select_all_ad_controller_button(*args):
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


def ad_reset_color_button(*args):
    al.ad_lib_ctrl_color_list(0)
    pm.select(cl=True)


def ad_replace_color_button(*args):
    al.ad_lib_ctrl_color_list(ad_set_color())
    pm.select(cl=True)


def ad_set_color(*args):
    controller_color = pm.palettePort('Pallete', query=True, setCurCell=True)
    return controller_color


def ad_controller_shape(size_ctrl, *args):
    control_shape = []
    if on_selector == 1:
        control_shape = al.ad_lib_ctrl_shape(ac.CIRCLE, size_ctrl=size_ctrl)
    elif on_selector == 2:
        control_shape = al.ad_lib_ctrl_shape(ac.LOCATOR, size_ctrl=size_ctrl)
    elif on_selector == 3:
        control_shape = al.ad_lib_ctrl_shape(ac.CUBE, size_ctrl=size_ctrl)
    elif on_selector == 4:
        control_shape = al.ad_lib_ctrl_shape(ac.CIRCLEHALF, size_ctrl=size_ctrl)
    elif on_selector == 5:
        control_shape = al.ad_lib_ctrl_shape(ac.SQUARE, size_ctrl=size_ctrl)
    elif on_selector == 6:
        control_shape = al.ad_lib_ctrl_shape(ac.JOINT, size_ctrl=size_ctrl)
    elif on_selector == 7:
        control_shape = al.ad_lib_ctrl_shape(ac.CAPSULE, size_ctrl=size_ctrl)
    elif on_selector == 8:
        control_shape = al.ad_lib_ctrl_shape(ac.STICKCIRCLE, size_ctrl=size_ctrl)
    elif on_selector == 9:
        control_shape = al.ad_lib_ctrl_shape(ac.CIRCLEPLUSHALF, size_ctrl=size_ctrl)
    elif on_selector == 10:
        control_shape = al.ad_lib_ctrl_shape(ac.CIRCLEPLUS, size_ctrl=size_ctrl)
    elif on_selector == 11:
        control_shape = al.ad_lib_ctrl_shape(ac.STICK2CIRCLE, size_ctrl=size_ctrl)
    elif on_selector == 12:
        control_shape = al.ad_lib_ctrl_shape(ac.STICKSQUARE, size_ctrl=size_ctrl)
    elif on_selector == 13:
        control_shape = al.ad_lib_ctrl_shape(ac.STICK2SQUARE, size_ctrl=size_ctrl)
    elif on_selector == 14:
        control_shape = al.ad_lib_ctrl_shape(ac.STICKSTAR, size_ctrl=size_ctrl)
    elif on_selector == 15:
        control_shape = al.ad_lib_ctrl_shape(ac.CIRCLEPLUSARROW, size_ctrl=size_ctrl)
    elif on_selector == 16:
        control_shape = al.ad_lib_ctrl_shape(ac.RECTANGLE, size_ctrl=size_ctrl)
    elif on_selector == 17:
        control_shape = al.ad_lib_ctrl_shape(ac.ARROW, size_ctrl=size_ctrl)
    elif on_selector == 18:
        control_shape = al.ad_lib_ctrl_shape(ac.ARROW3DFLAT, size_ctrl=size_ctrl)
    elif on_selector == 19:
        control_shape = al.ad_lib_ctrl_shape(ac.ARROW2HALFCIRCULAR, size_ctrl=size_ctrl)
    elif on_selector == 20:
        control_shape = al.ad_lib_ctrl_shape(ac.ARROW2STRAIGHT, size_ctrl=size_ctrl)
    elif on_selector == 21:
        control_shape = al.ad_lib_ctrl_shape(ac.ARROW2FLAT, size_ctrl=size_ctrl)
    elif on_selector == 22:
        control_shape = al.ad_lib_ctrl_shape(ac.ARROWHEAD, size_ctrl=size_ctrl)
    elif on_selector == 23:
        control_shape = al.ad_lib_ctrl_shape(ac.ARROW90DEG, size_ctrl=size_ctrl)
    elif on_selector == 24:
        control_shape = al.ad_lib_ctrl_shape(ac.SQUAREPLUS, size_ctrl=size_ctrl)
    elif on_selector == 25:
        control_shape = al.ad_lib_ctrl_shape(ac.JOINTPLUS, size_ctrl=size_ctrl)
    elif on_selector == 26:
        control_shape = al.ad_lib_ctrl_shape(ac.HAND, size_ctrl=size_ctrl)
    elif on_selector == 27:
        control_shape = al.ad_lib_ctrl_shape(ac.ARROWCIRCULAR, size_ctrl=size_ctrl)
    elif on_selector == 28:
        control_shape = al.ad_lib_ctrl_shape(ac.PLUS, size_ctrl=size_ctrl)
    elif on_selector == 29:
        control_shape = al.ad_lib_ctrl_shape(ac.PIVOT, size_ctrl=size_ctrl)
    elif on_selector == 30:
        control_shape = al.ad_lib_ctrl_shape(ac.KEYS, size_ctrl=size_ctrl)
    elif on_selector == 31:
        control_shape = al.ad_lib_ctrl_shape(ac.PYRAMIDCIRCLE, size_ctrl=size_ctrl)
    elif on_selector == 32:
        control_shape = al.ad_lib_ctrl_shape(ac.ARROW4CIRCULAR, size_ctrl=size_ctrl)
    elif on_selector == 33:
        control_shape = al.ad_lib_ctrl_shape(ac.EYES, size_ctrl=size_ctrl)
    elif on_selector == 34:
        control_shape = al.ad_lib_ctrl_shape(ac.FOOTSTEP, size_ctrl=size_ctrl)
    elif on_selector == 35:
        control_shape = al.ad_lib_ctrl_shape(ac.HALF3DCIRCLE, size_ctrl=size_ctrl)
    elif on_selector == 36:
        control_shape = al.ad_lib_ctrl_shape(ac.CAPSULECURVE, size_ctrl=size_ctrl)
    elif on_selector == 37:
        control_shape = al.ad_lib_ctrl_shape(ac.ARROW4STRAIGHT, size_ctrl=size_ctrl)
    elif on_selector == 38:
        control_shape = al.ad_lib_ctrl_shape(ac.ARROW3D, size_ctrl=size_ctrl)
    elif on_selector == 39:
        control_shape = al.ad_lib_ctrl_shape(ac.PYRAMID, size_ctrl=size_ctrl)
    elif on_selector == 40:
        control_shape = al.ad_lib_ctrl_shape(ac.ARROW3DCIRCULAR, size_ctrl=size_ctrl)
    elif on_selector == 41:
        control_shape = al.ad_lib_ctrl_shape(ac.CYLINDER, size_ctrl=size_ctrl)
    elif on_selector == 42:
        control_shape = al.ad_lib_ctrl_shape(ac.ARROW2FLATHALF, size_ctrl=size_ctrl)
    elif on_selector == 43:
        control_shape = al.ad_lib_ctrl_shape(ac.FLAG, size_ctrl=size_ctrl)
    elif on_selector == 44:
        control_shape = al.ad_lib_ctrl_shape(ac.WORLD, size_ctrl=size_ctrl)
    elif on_selector == 45:
        control_shape = al.ad_lib_ctrl_shape(ac.SETUP, size_ctrl=size_ctrl)
    elif on_selector == 46:
        control_shape = al.ad_lib_ctrl_shape(ac.STAR, size_ctrl=size_ctrl)
    elif on_selector == 47:
        control_shape = al.ad_lib_ctrl_shape(ac.DIAMOND, size_ctrl=size_ctrl)
    elif on_selector == 48:
        control_shape = al.ad_lib_ctrl_shape(ac.STARSQUEEZE, size_ctrl=size_ctrl)
    else:
        pass
    return control_shape


def ad_on_selection_ctrl_shape(on):
    # save the current shape selection into global variable
    global on_selector
    on_selector = on


def ad_shape_controller_ui(default, *args):
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
                                       onCommand=lambda x: ad_on_selection_ctrl_shape(9))
                # circleplus
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/circleplus.png',
                                       onCommand=lambda x: ad_on_selection_ctrl_shape(10))
                # stick2circle
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/stick2circle.png',
                                       onCommand=lambda x: ad_on_selection_ctrl_shape(11))
                # sticksquare
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/sticksquare.png',
                                       onCommand=lambda x: ad_on_selection_ctrl_shape(12))
                # stick2square
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/stick2square.png',
                                       onCommand=lambda x: ad_on_selection_ctrl_shape(13))
                # stickstar
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/stickstar.png',
                                       onCommand=lambda x: ad_on_selection_ctrl_shape(14))
                # circleplusarrow
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/circleplusarrow.png',
                                       onCommand=lambda x: ad_on_selection_ctrl_shape(15))
                # rectangle
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/rectangle.png',
                                       onCommand=lambda x: ad_on_selection_ctrl_shape(16))
                # arrow
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/arrow.png',
                                       onCommand=lambda x: ad_on_selection_ctrl_shape(17))
                # arrow3dflat
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/arrow3dflat.png',
                                       onCommand=lambda x: ad_on_selection_ctrl_shape(18))
                # arrow2halfcircular
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/arrow2halfcircular.png',
                                       onCommand=lambda x: ad_on_selection_ctrl_shape(19))
                # arrow2straight
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/arrow2straight.png',
                                       onCommand=lambda x: ad_on_selection_ctrl_shape(20))
                # arrow2flat
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/arrow2flat.png',
                                       onCommand=lambda x: ad_on_selection_ctrl_shape(21))
                # arrowhead
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/arrowhead.png',
                                       onCommand=lambda x: ad_on_selection_ctrl_shape(22))
                # arrow90deg
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/arrow90deg.png',
                                       onCommand=lambda x: ad_on_selection_ctrl_shape(23))
                # squareplus
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/squareplus.png',
                                       onCommand=lambda x: ad_on_selection_ctrl_shape(24))
                # jointplus
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/jointplus.png',
                                       onCommand=lambda x: ad_on_selection_ctrl_shape(25))
                # hand
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/hand.png',
                                       onCommand=lambda x: ad_on_selection_ctrl_shape(26))
                # arrowcircular
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/arrowcircular.png',
                                       onCommand=lambda x: ad_on_selection_ctrl_shape(27))
                # plus
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/plus.png',
                                       onCommand=lambda x: ad_on_selection_ctrl_shape(28))
                # pivot
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/pivot.png',
                                       onCommand=lambda x: ad_on_selection_ctrl_shape(29))
                # keys
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/keys.png',
                                       onCommand=lambda x: ad_on_selection_ctrl_shape(30))
                # pyramidcircle
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/pyramidcircle.png',
                                       onCommand=lambda x: ad_on_selection_ctrl_shape(31))
                # arrow4circular
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/arrow4circular.png',
                                       onCommand=lambda x: ad_on_selection_ctrl_shape(32))
                # eyes
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/eyes.png',
                                       onCommand=lambda x: ad_on_selection_ctrl_shape(33))
                # footstep
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/footstep.png',
                                       onCommand=lambda x: ad_on_selection_ctrl_shape(34))
                # half3dcircle
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/half3dcircle.png',
                                       onCommand=lambda x: ad_on_selection_ctrl_shape(35))
                # capsulecurve
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/capsulecurve.png',
                                       onCommand=lambda x: ad_on_selection_ctrl_shape(36))
                # arrow4straight
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/arrow4straight.png',
                                       onCommand=lambda x: ad_on_selection_ctrl_shape(37))
                # arrow3d
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/arrow3d.png',
                                       onCommand=lambda x: ad_on_selection_ctrl_shape(38))
                # pyramid
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/pyramid.png',
                                       onCommand=lambda x: ad_on_selection_ctrl_shape(39))
                # arrow3dcircular
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/arrow3dcircular.png',
                                       onCommand=lambda x: ad_on_selection_ctrl_shape(40))
                # cylinder
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/cylinder.png',
                                       onCommand=lambda x: ad_on_selection_ctrl_shape(41))
                # arrow2flathalf
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/arrow2flathalf.png',
                                       onCommand=lambda x: ad_on_selection_ctrl_shape(42))
                # flag
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/flag.png',
                                       onCommand=lambda x: ad_on_selection_ctrl_shape(43))
                # world
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/world.png',
                                       onCommand=lambda x: ad_on_selection_ctrl_shape(44))
                # setup
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/setup.png',
                                       onCommand=lambda x: ad_on_selection_ctrl_shape(45))
                # star
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/star.png',
                                       onCommand=lambda x: ad_on_selection_ctrl_shape(46))
                # diamond
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/diamond.png',
                                       onCommand=lambda x: ad_on_selection_ctrl_shape(47))
                # starsqueeze
                pm.iconTextRadioButton(st='iconOnly', image='ad_icons/starsqueeze.png',
                                       onCommand=lambda x: ad_on_selection_ctrl_shape(48))

    pm.showWindow()


def ad_tagging_untagging_button(tagging, *args):
    selection = pm.ls(selection=True)
    if not selection:
        om.MGlobal.displayError("No curves selected")
    else:
        for item in selection:
            shape_node = pm.listRelatives(item, s=True)[0]
            if pm.objectType(shape_node) == 'nurbsCurve':
                if tagging:
                    al.ad_lib_tagging(item)
                else:
                    al.ad_lib_untagging(item)
            else:
                pass


def ad_adding_object_sel_to_textfield(text_input, *args):
    # elect and add object
    select = pm.ls(sl=True, l=True, tr=True)
    if len(select) == 1:
        object_selection = select[0]
        pm.textFieldButtonGrp(text_input, e=True, tx=object_selection, bl="<<")
    else:
        pm.error("please select one object!")


# def ad_controller_resize_slider(*args):
#     selection = pm.ls(selection=True)
#     if not selection:
#         om.MGlobal.displayWarning("No objects selected")
#     else:
#         for item in selection:
#             shape_node = pm.listRelatives(item, s=True)[0]
#             if pm.objectType(shape_node) == 'nurbsCurve':
#                 global previous_value
#                 currentValue = pm.floatSlider('Controller_Resize', q=True, v=True)
#                 deltaValue = (currentValue - previous_value)
#                 al.ad_lib_scaling_controller(deltaValue, shape_node)
#                 # self.prevValue = value
#                 previous_value = currentValue
#             else:
#                 om.MGlobal.displayError("Object type must be curve")
#                 return False

def ad_controller_resize_slider(*args):
    selection = pm.ls(selection=True)
    if not selection:
        om.MGlobal.displayWarning("No objects selected")
    else:
        for item in selection:
            shape_node = pm.listRelatives(item, s=True)[0]
            if pm.objectType(shape_node) == 'nurbsCurve':
                # global previous_value
                current_value = pm.floatSlider('Controller_Resize', q=True, v=True)
                # delta_value = (current_value - previous_value)
                # deltaValue = (previous_value/currentValue)
                # new_value = deltaValue
                al.ad_lib_scaling_controller(current_value, item)
                # self.prevValue = value
                # previous_value = current_value
            else:
                pass


# def ad_controller_resize_slider(*args):
#     selection = pm.ls(selection=True)
#     if not selection:
#         om.MGlobal.displayWarning("No objects selected")
#     else:
#         for item in selection:
#             shape_node = pm.listRelatives(item, s=True)[0]
#             if pm.objectType(shape_node) == 'nurbsCurve':
#                 global previous_value
#                 current_value = pm.floatSlider('Controller_Resize', q=True, v=True)
#                 delta_value = (current_value - previous_value)
#                 # deltaValue = (previous_value/currentValue)
#                 new_value = delta_value
#                 al.ad_lib_scaling_controller(new_value, item)
#                 # self.prevValue = value
#                 previous_value = current_value
#             else:
#                 pass

def ad_controller_resize_reset(*args):
    pm.floatSlider('Controller_Resize', edit=True, v=0.0)


def ad_enabling_disabling_ui(object, tx, value, *args):
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


def ad_color_index():
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


def ad_channelbox_translation(*args):
    pm.columnLayout()
    pm.checkBox('All_Trans', label='All Translation', value=False,
                cc=partial(ad_checkbox_check_channel_translate, ['Trans_X', 'Trans_Y', 'Trans_Z']))
    pm.checkBox('Trans_X', label='Translate X', value=False,
                cc=partial(ad_checkbox_uncheck_all_channel, ['Trans_X']))
    pm.checkBox('Trans_Y', label='Translate Y', value=False,
                cc=partial(ad_checkbox_uncheck_all_channel, ['Trans_Y']))
    pm.checkBox('Trans_Z', label='Translate Z', value=False,
                cc=partial(ad_checkbox_uncheck_all_channel, ['Trans_Z']))
    pm.checkBox('Visibility', label='Visibility', value=False)
    pm.setParent(u=True)


def ad_channelbox_rotation(*args):
    pm.columnLayout()
    pm.checkBox('All_Rot', label='All Rotation', value=False,
                cc=partial(ad_checkbox_check_channel_rotate, ['Rot_X', 'Rot_Y', 'Rot_Z']))
    pm.checkBox('Rot_X', label='Rotate X', value=False, cc=partial(ad_checkbox_uncheck_all_channel, ['Rot_X']))
    pm.checkBox('Rot_Y', label='Rotate Y', value=False, cc=partial(ad_checkbox_uncheck_all_channel, ['Rot_Y']))
    pm.checkBox('Rot_Z', label='Rotate Z', value=False, cc=partial(ad_checkbox_uncheck_all_channel, ['Rot_Z']))
    pm.checkBox('User_Def', label='User Defined', value=False)

    pm.setParent(u=True)


def ad_channelbox_scale(*args):
    pm.columnLayout()
    pm.checkBox('All_Scale', label='All Scale', value=False,
                cc=partial(ad_checkbox_check_channel_scale, ['Scl_X', 'Scl_Y', 'Scl_Z']))
    pm.checkBox('Scl_X', label='Scale X', value=False, cc=partial(ad_checkbox_uncheck_all_channel, ['Scl_X']))
    pm.checkBox('Scl_Y', label='Scale Y', value=False, cc=partial(ad_checkbox_uncheck_all_channel, ['Scl_Y']))
    pm.checkBox('Scl_Z', label='Scale Z', value=False, cc=partial(ad_checkbox_uncheck_all_channel, ['Scl_Z']))
    pm.setParent(u=True)


def ad_checkbox_check_channel_translate(objects, value, *args):
    for item in objects:
        all_trans = pm.checkBox('All_Trans', q=True, value=value)
        if all_trans == 1:
            pm.checkBox(item, e=True, value=True)
        else:
            pm.checkBox(item, e=True, value=False)


def ad_checkbox_check_channel_rotate(objects, value, *args):
    for item in objects:
        all_rot = pm.checkBox('All_Rot', q=True, value=value)
        if all_rot == 1:
            pm.checkBox(item, e=True, value=True)
        else:
            pm.checkBox(item, e=True, value=False)


def ad_checkbox_check_channel_scale(objects, value, *args):
    for item in objects:
        all_scale = pm.checkBox('All_Scale', q=True, value=value)
        if all_scale == 1:
            pm.checkBox(item, e=True, value=True)
        else:
            pm.checkBox(item, e=True, value=False)


def ad_checkbox_uncheck_all_channel(*args):
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


def ad_channelbox_constraint_connection(*args):
    pm.columnLayout()
    pm.checkBox('Point_Cons', label='Point Constraint', value=False,
                cc=partial(ad_connection_uncheck_translate_rotate_constraint,
                           ['Parent_Cons', 'Direct_Trans',
                            'Parent'], ['Add_Pivot_Ctrl'], 'Point_Cons'))
    pm.checkBox('Orient_Cons', label='Orient Constraint', value=False,
                cc=partial(ad_connection_uncheck_translate_rotate_constraint,
                           ['Parent_Cons', 'Direct_Rot',
                            'Parent'], ['Add_Pivot_Ctrl'], 'Orient_Cons'))
    pm.checkBox('Scale_Cons', label='Scale Constraint', value=False, cc=partial(ad_connection_uncheck_scale_constraint,
                                                                                ['Direct_Scl', 'Parent'], 'Scale_Cons'))
    pm.checkBox('Parent_Cons', label='Parent Constraint', value=False,
                cc=partial(ad_connection_uncheck_parent_constraint,
                           ['Point_Cons', 'Orient_Cons',
                            'Direct_Trans', 'Direct_Rot',
                            'Parent'], ['Add_Pivot_Ctrl'], 'Parent_Cons'))
    pm.setParent(u=True)


def ad_channelbox_direct_connection(*args):
    pm.columnLayout()
    pm.checkBox('Direct_Trans', label='Direct Connect Translate', value=False,
                cc=partial(ad_connection_uncheck_translate_rotate_constraint,
                           ['Parent_Cons', 'Point_Cons', 'Parent'], ['Add_Pivot_Ctrl'], 'Direct_Trans'))
    pm.checkBox('Direct_Rot', label='Direct Connect Rotate', value=False,
                cc=partial(ad_connection_uncheck_translate_rotate_constraint,
                           ['Parent_Cons', 'Orient_Cons',
                            'Parent'], ['Add_Pivot_Ctrl'], 'Direct_Rot'))
    pm.checkBox('Direct_Scl', label='Direct Connect Scale', value=False,
                cc=partial(ad_connection_uncheck_scale_constraint,
                           ['Scale_Cons', 'Parent'],
                           'Direct_Scl'))
    pm.checkBox('Parent', label='Parent', value=False, cc=partial(ad_connection_uncheck_translate_rotate_constraint,
                                                                  ['Point_Cons', 'Orient_Cons', 'Direct_Trans',
                                                                   'Direct_Rot', 'Parent_Cons',
                                                                   'Direct_Scl', 'Scale_Cons'], ['Add_Pivot_Ctrl'],
                                                                  'Parent'))
    pm.setParent(u=True)


def ad_connection_uncheck_translate_rotate_constraint(target, pivot, object, value, *args):
    checkbox_obj = pm.checkBox(object, q=True, value=value)
    for item in target:
        if checkbox_obj == 1:
            pm.checkBox(item, e=True, value=False)
    for pvt in pivot:
        pm.checkBox(pvt, edit=True, enable=False)
        pm.checkBox(pvt, edit=True, value=False)


def ad_connection_uncheck_scale_constraint(target, object, value, *args):
    checkbox_obj = pm.checkBox(object, q=True, value=value)
    for item in target:
        if checkbox_obj == 1:
            pm.checkBox(item, e=True, value=False)


def ad_connection_uncheck_parent_constraint(target, pivot, object, value, *args):
    checkbox_obj = pm.checkBox(object, q=True, value=value)
    for item in target:
        if checkbox_obj == 1:
            pm.checkBox(item, e=True, value=False)
    for pvt in pivot:
        pm.checkBox(pvt, edit=True, enable=value)
        if checkbox_obj == 0:
            pm.checkBox(pvt, e=True, value=False)
