from functools import partial

import pymel.core as pm

layout = 500
percentage = 0.01 * layout
on_checkbox_selector=0
on_selector = 0

def display_ui():
    adien_snap_fkIk = 'AdienFkIkSnapSetup'
    pm.window(adien_snap_fkIk, exists=True)
    if pm.window(adien_snap_fkIk, exists=True):
        pm.deleteUI(adien_snap_fkIk)
    with pm.window(adien_snap_fkIk, title='Adien Fk/Ik Snap Setup', width=600, height=800):
        with pm.scrollLayout('scroll'):
            with pm.columnLayout(rowSpacing=1 * percentage, w=layout, co=('both', 1 * percentage), adj=1):
                with pm.frameLayout(collapsable=True, l='Select Controller', mh=5):
                    with pm.rowColumnLayout('fkIk_controller_layout', nc=2, rowSpacing=(2, 1 * percentage),
                                            co=(1 * percentage, 'both', 1 * percentage),
                                            cw=[(1, 5 * percentage), (2, 93 * percentage)], ca=True):
                        direction_control = pm.radioCollection()
                        direction0 = pm.radioButton(label='',
                                                    cc=partial(enable_text_field, ['FkIk_Arm_Setup_Controller']))
                        define_object_text_field(define_object='FkIk_Arm_Setup_Controller',
                                                 label="Fk/Ik Arm Setup Controller:",
                                                 add_feature=True, enable=False)

                        direction1 = pm.radioButton(label='',
                                                    cc=partial(enable_text_field, ['FkIk_Leg_Setup_Controller',
                                                                                   'End_Limb_Joint', 'End_Limb_Fk_Ctrl',
                                                                                   'End_Limb_Ik_Ctrl']))
                        define_object_text_field(define_object='FkIk_Leg_Setup_Controller',
                                                 label="Fk/Ik Leg Setup Controller:",
                                                 add_feature=True)
                pm.separator(h=5, st="in", w=layout)
                with pm.frameLayout(collapsable=True, l='Define Objects', mh=5):
                    define_object_text_field(define_object='Upper_Limb_Joint', label="Upper Limb Joint:")
                    define_object_text_field(define_object='Middle_Limb_Joint', label="Middle Limb Joint:")
                    define_object_text_field(define_object='Lower_Limb_Joint', label="Lower Limb Joint:")
                    define_object_text_field(define_object='End_Limb_Joint', label="End Limb Joint:", enable=False)
                    define_object_text_field(define_object='Upper_Limb_Fk_Ctrl', label="Upper Limb Fk Ctrl:")
                    define_object_text_field(define_object='Middle_Limb_Fk_Ctrl', label="Middle Limb Fk Ctrl:")
                    define_object_text_field(define_object='Lower_Limb_Fk_Ctrl', label="Lower Limb Fk Ctrl:")
                    define_object_text_field(define_object='End_Limb_Fk_Ctrl', label="End Limb Fk Ctrl:", enable=False)

                    with pm.rowColumnLayout(nc=2, rowSpacing=(2, 1 * percentage),
                                            co=(1 * percentage, 'both', 1 * percentage),
                                            cw=[(1, 5 * percentage), (2, 93 * percentage)]):
                        pm.checkBox(label='', cc=partial(enable_text_field, ['Upper_Limb_Ik_Ctrl']), value=True)
                        define_object_text_field(define_object='Upper_Limb_Ik_Ctrl', label="Upper Limb Ik Ctrl:",
                                                 add_feature=True)
                    define_object_text_field(define_object='Pole_Vector_Ik_Ctrl', label="Pole Vector Ik Ctrl:")
                    define_object_text_field(define_object='Lower_Limb_Ik_Ctrl', label="Lower Limb Ik Ctrl:")
                    with pm.rowColumnLayout(nc=2, rowSpacing=(2, 1 * percentage),
                                            co=(1 * percentage, 'both', 1 * percentage),
                                            cw=[(1, 5 * percentage), (2, 93 * percentage)]):
                        check_boxes = pm.checkBox('check_box_endlimb_ik', label='',
                                                  cc=partial(enable_text_field, ['End_Limb_Ik_Ctrl']), value=True)
                        define_object_text_field(define_object='End_Limb_Ik_Ctrl', label="End Limb Ik Ctrl:",
                                                 add_feature=True)
                    direction_control = pm.radioCollection(direction_control, edit=True, select=direction1)

                    with pm.rowLayout(nc=1, cw1=(35 * percentage), cl1=('center'),
                                      columnAttach=[(1, 'both', 2 * percentage)]
                                      ):
                        pm.button("clear_all_define_objects", bgc=(1, 1, 0), l="Clear All Define Objects!",
                                  c=partial(clear_text_field, 'Upper_Limb_Joint',
                                            'Middle_Limb_Joint', 'Lower_Limb_Joint', 'End_Limb_Joint',
                                            'Upper_Limb_Fk_Ctrl',
                                            'Middle_Limb_Fk_Ctrl', 'Lower_Limb_Fk_Ctrl', 'End_Limb_Fk_Ctrl',
                                            'Upper_Limb_Ik_Ctrl',
                                            'Pole_Vector_Ik_Ctrl', 'Lower_Limb_Ik_Ctrl', 'End_Limb_Ik_Ctrl'))

                pm.separator(h=5, st="in", w=layout)
                # radio button translate
                with pm.frameLayout(collapsable=True, l='Additional Setup', mh=5):
                    with pm.rowLayout(nc=4, columnAttach=[(1, 'right', 0), (2, 'left', 2 * percentage),
                                                          (3, 'left', 2 * percentage), (4, 'left', 2 * percentage)],
                                      cw4=(33 * percentage, 21.6 * percentage, 21.6 * percentage, 21.6 * percentage)):
                        pm.text('Limb Aim Axis:')
                        direction_control_translate = pm.radioCollection()
                        direction_translateX = pm.radioButton(label='Translate X',
                                                              onCommand=lambda x: selection_radio_button(1))
                        direction_translateY = pm.radioButton(label='Translate Y',
                                                              onCommand=lambda x: selection_radio_button(2))
                        direction_translateZ = pm.radioButton(label='Translate Z',
                                                              onCommand=lambda x: selection_radio_button(3))
                        direction_control_translate = pm.radioCollection(direction_control_translate, edit=True,
                                                                         select=direction_translateX)

                    with pm.rowLayout(nc=2, columnAttach=[(1, 'right', 0), (2, 'left', 2 * percentage)],
                                      cw2=(33 * percentage, 64.8)):
                        pm.text('Ctrl Translate Fk is locked?:')
                        pm.checkBox(label='', onc=lambda x: on_checkbox_button(1), ofc=lambda x: on_checkbox_button(0))

                pm.separator(h=5, st="in", w=layout)

                with pm.frameLayout(collapsable=True, l='Additional Attributes', mh=5):
                    with pm.rowLayout(nc=2, cw2=(49 * percentage, 49 * percentage), cl2=('center', 'center'),
                                      columnAttach=[(1, 'both', 2 * percentage), (2, 'both', 2 * percentage)]
                                      ):
                        pm.button(l="Add Object | Set Attribute Value", bgc=(0, 0, 0.5), c=add_text_field_grp)

                        # create button to delete last pair of text fields
                        pm.button("delete_last_button", bgc=(0.5, 0, 0), l="Delete", c=delete_additional_attr)
                        pm.setParent(u=True)
                        pm.rowColumnLayout("row_column_add_object", nc=3)
                        pm.setParent(u=True)

                pm.separator(h=5, st="in", w=layout)
                with pm.frameLayout(collapsable=True, l='Setup', mh=5):
                    pm.text(l='Select Leg/Arm Ctrl Setup :')
                    with pm.rowLayout(nc=2, cw2=(49 * percentage, 49 * percentage), cl2=('center', 'center'),
                                      columnAttach=[(1, 'both', 2 * percentage), (2, 'both', 2 * percentage)]
                                      ):
                        pm.button("run_setup", bgc=(0, 0.5, 0), l="Run Setup",
                                  c=partial(run_setup))
                        pm.button("delete_setup", bgc=(0.5, 0, 0), l="Delete Setup",
                                  c=partial(delete_setup))

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

def action_translate_checkbox_button(*args):
    if on_checkbox_selector == 1:
        value = 1
    elif on_checkbox_selector == 0:
        value = 0
    else:
        value = pm.error('object has no value!')
    return  value

def on_checkbox_button(on_checkbox, *args):
    global on_checkbox_selector
    on_checkbox_selector = on_checkbox

def action_translate_radio_button(object, *args):
    """
    query object with value on shape selector status
    """
    value_translate, axis = [], []
    if on_selector == 1:
        axis = 'translateX'
        value_translate = pm.getAttr('%s.%s' % (object, axis))
    elif on_selector == 2:
        axis = 'translateY'
        value_translate = pm.getAttr('%s.%s' % (object, axis))
    elif on_selector == 3:
        axis = 'translateZ'
        value_translate = pm.getAttr('%s.%s' % (object, axis))
    else:
        pm.error('object has no value!')

    return value_translate, axis


def selection_radio_button(on):
    """
    Save the current shape selection
    into global variable "shape_selector"
    """
    global on_selector
    on_selector = on

def define_object_text_field(define_object, label, add_feature=False, **kwargs):
    if not add_feature:
        pm.textFieldButtonGrp(define_object, label=label, cal=(1, "right"),
                              cw3=(33 * percentage, 50 * percentage, 15 * percentage), w=98 * percentage,
                              bl="Get Object",
                              bc=partial(add_object, define_object))
    else:
        pm.textFieldButtonGrp(define_object, label=label, cal=(1, "right"),
                              cw3=(28 * percentage, 50 * percentage, 15 * percentage),
                              w=93 * percentage, bl="Get Object",
                              bc=partial(add_object, define_object), **kwargs)

def enable_text_field(object, value, *args):
    for item in object:
        pm.textFieldButtonGrp(item, edit=True, enable=value, tx='')

def clear_text_field(*args):
    for object in args:
        if object:
            pm.textFieldButtonGrp(object, edit=True, tx='')
        else:
            pass

def add_text_field_grp(*args):
    child_array = pm.rowColumnLayout("row_column_add_object", q=True, ca=True)
    if child_array:
        current_number = len(child_array) / 3 + 1
        current_default_value = "default_value" + str(current_number)
        current_attr = "attribute" + str(current_number)
        current_object = "object" + str(current_number)
    else:
        current_default_value = "default_value1"
        current_attr = "attribute1"
        current_object = "object1"

    pm.textFieldButtonGrp(current_object, l="Object:", cal=(1, "left"),
                          cw3=(8 * percentage, 30 * percentage, 5 * percentage), p="row_column_add_object",
                          bl="<<",
                          bc=partial(add_object, current_object))
    pm.textFieldGrp(current_attr, l="Attr:", cal=(1, "right"), cw2=(7 * percentage, 18 * percentage),
                    p="row_column_add_object")
    pm.floatFieldGrp(current_default_value, l="Default Value:", cal=(1, "right"), cw2=(17 * percentage, 8 * percentage),
                     p="row_column_add_object", precision=2)

def delete_additional_attr(*args):
    """
    delete add_text_field_grp
    """
    child_array = pm.rowColumnLayout("row_column_add_object", q=True, ca=True)

    if child_array:
        child_array_num = len(child_array)
        delete_default_value = "default_value" + str(child_array_num / 3)
        delete_attr = "attribute" + str(child_array_num / 3)
        delete_object = "object" + str(child_array_num / 3)

        pm.deleteUI(delete_default_value)
        pm.deleteUI(delete_attr)
        pm.deleteUI(delete_object)

    else:
        pass

def add_object(text_input, *args):
    """
    select and add object
    """
    sel = pm.ls(sl=True, l=True, tr=True)
    if len(sel) == 1:
        object_selection = sel[0]
        pm.textFieldButtonGrp(text_input, e=True, tx=object_selection)
    else:
        pm.error("please select one object!")

def query_define_object(object_define, *args):
    text = []
    if (pm.textFieldButtonGrp(object_define, q=True, en=True)):
        if (pm.textFieldButtonGrp(object_define, q=True, tx=True)):
            text = pm.textFieldButtonGrp(object_define, q=True, tx=True)

        else:
            pm.error('%s can not be empty!' % object_define)
    else:
        pass
    return text, object_define

def run_setup(*args):
    # query objects
    FkIk_Arm_Setup_Controller = query_define_object('FkIk_Arm_Setup_Controller')
    FkIk_Leg_Setup_Controller = query_define_object('FkIk_Leg_Setup_Controller')
    Upper_Limb_Joint_Define = query_define_object('Upper_Limb_Joint')
    Middle_Limb_Joint_Define = query_define_object('Middle_Limb_Joint')
    Lower_Limb_Joint_Define = query_define_object('Lower_Limb_Joint')
    End_Limb_Joint_Define = query_define_object('End_Limb_Joint')
    Upper_Limb_Fk_Ctrl_Define = query_define_object('Upper_Limb_Fk_Ctrl')
    Middle_Limb_Fk_Ctrl_Define = query_define_object('Middle_Limb_Fk_Ctrl')
    Lower_Limb_Fk_Ctrl_Define = query_define_object('Lower_Limb_Fk_Ctrl')
    End_Limb_Fk_Ctrl_Define = query_define_object('End_Limb_Fk_Ctrl')
    Upper_Limb_Ik_Ctrl_Define = query_define_object('Upper_Limb_Ik_Ctrl')
    Pole_Vector_Ik_Ctrl_Define = query_define_object('Pole_Vector_Ik_Ctrl')
    Lower_Limb_Ik_Ctrl_Define = query_define_object('Lower_Limb_Ik_Ctrl')
    End_Limb_Ik_Ctrl_Define = query_define_object('End_Limb_Ik_Ctrl')

    label_list = [FkIk_Arm_Setup_Controller[1], FkIk_Leg_Setup_Controller[1],
                  Upper_Limb_Joint_Define[1], Middle_Limb_Joint_Define[1], Lower_Limb_Joint_Define[1],
                  Upper_Limb_Fk_Ctrl_Define[1], Middle_Limb_Fk_Ctrl_Define[1], Lower_Limb_Fk_Ctrl_Define[1],
                  Upper_Limb_Ik_Ctrl_Define[1], Pole_Vector_Ik_Ctrl_Define[1], Lower_Limb_Ik_Ctrl_Define[1],
                  End_Limb_Joint_Define[1], End_Limb_Fk_Ctrl_Define[1], End_Limb_Ik_Ctrl_Define[1]]

    object_list = [FkIk_Arm_Setup_Controller[0], FkIk_Leg_Setup_Controller[0],
                   Upper_Limb_Joint_Define[0], Middle_Limb_Joint_Define[0], Lower_Limb_Joint_Define[0],
                   Upper_Limb_Fk_Ctrl_Define[0], Middle_Limb_Fk_Ctrl_Define[0], Lower_Limb_Fk_Ctrl_Define[0],
                   Upper_Limb_Ik_Ctrl_Define[0], Pole_Vector_Ik_Ctrl_Define[0], Lower_Limb_Ik_Ctrl_Define[0],
                   End_Limb_Joint_Define[0], End_Limb_Fk_Ctrl_Define[0], End_Limb_Ik_Ctrl_Define[0]]

    # addding attribute
    if pm.objExists('%s.%s' % (FkIk_Arm_Setup_Controller[0], Upper_Limb_Joint_Define[1])):
        pm.warning('please delete the setup first!')
    else:
        if (pm.textFieldButtonGrp(FkIk_Arm_Setup_Controller[1], q=True, en=True)):
            for item_label, object_label in zip(label_list[:-3], object_list[:-3]):
                pm.addAttr(FkIk_Arm_Setup_Controller[0], ln=item_label, at='message')
                if pm.textFieldButtonGrp(item_label, q=True, en=True):
                    pm.connectAttr(object_label + '.message', '%s.%s' % (FkIk_Arm_Setup_Controller[0], item_label))

            pm.addAttr(FkIk_Arm_Setup_Controller[0], ln='Translate_Fk_Ctrl_Exists', at='bool')
            pm.setAttr('%s.Translate_Fk_Ctrl_Exists' % FkIk_Arm_Setup_Controller[0], action_translate_checkbox_button(), l=True)
            # action_translate_checkbox_button(FkIk_Arm_Setup_Controller[0])
            pm.addAttr(FkIk_Arm_Setup_Controller[0], ln='Middle_Translate_Aim_Joint', at='float')
            pm.addAttr(FkIk_Arm_Setup_Controller[0], ln='Lower_Translate_Aim_Joint', at='float')
            pm.addAttr(FkIk_Arm_Setup_Controller[0], ln='Aim_Axis', dt='string')
            pm.setAttr('%s.Middle_Translate_Aim_Joint' % FkIk_Arm_Setup_Controller[0],
                       action_translate_radio_button(Middle_Limb_Joint_Define[0])[0], l=True)
            pm.setAttr('%s.Lower_Translate_Aim_Joint' % FkIk_Arm_Setup_Controller[0],
                       action_translate_radio_button(Lower_Limb_Joint_Define[0])[0], l=True)
            pm.setAttr('%s.Aim_Axis' % FkIk_Arm_Setup_Controller[0],
                       action_translate_radio_button(Lower_Limb_Joint_Define[0])[1], l=True)

        else:
            for item_label, object_label in zip(label_list, object_list):
                pm.addAttr(FkIk_Leg_Setup_Controller[0], ln=item_label, at='message')
                if pm.textFieldButtonGrp(item_label, q=True, en=True):
                    pm.connectAttr(object_label + '.message', '%s.%s' % (FkIk_Leg_Setup_Controller[0], item_label))

            # action_translate_checkbox_button(FkIk_Leg_Setup_Controller[0])
            pm.addAttr(FkIk_Leg_Setup_Controller[0], ln='Translate_Fk_Ctrl_Exists', at='bool')
            pm.setAttr('%s.Translate_Fk_Ctrl_Exists' % FkIk_Leg_Setup_Controller[0], action_translate_checkbox_button(), l=True)
            pm.addAttr(FkIk_Leg_Setup_Controller[0], ln='Middle_Translate_Aim_Joint', at='float')
            pm.addAttr(FkIk_Leg_Setup_Controller[0], ln='Lower_Translate_Aim_Joint', at='float')
            pm.addAttr(FkIk_Leg_Setup_Controller[0], ln='Aim_Axis', dt='string')
            pm.setAttr('%s.Middle_Translate_Aim_Joint' % FkIk_Leg_Setup_Controller[0],
                       action_translate_radio_button(Middle_Limb_Joint_Define[0])[0], l=True)
            pm.setAttr('%s.Lower_Translate_Aim_Joint' % FkIk_Leg_Setup_Controller[0],
                       action_translate_radio_button(Lower_Limb_Joint_Define[0])[0], l=True)
            pm.setAttr('%s.Aim_Axis' % FkIk_Leg_Setup_Controller[0],
                       action_translate_radio_button(Lower_Limb_Joint_Define[0])[1], l=True)

    if pm.rowColumnLayout("row_column_add_object", q=True, ca=True):
        child_define_object = pm.rowColumnLayout("row_column_add_object", q=True, ca=True)
        number_of_object = (len(child_define_object) / 3)
        if number_of_object:
            for current_number in range(1, number_of_object + 1):
                current_object = "object" + str(current_number)
                current_attr = "attribute" + str(current_number)
                current_default_value = "default_value" + str(current_number)

                object = pm.textFieldButtonGrp(current_object, q=True, tx=True)
                attribute = pm.textFieldGrp(current_attr, q=True, tx=True)
                default_value = pm.floatFieldGrp(current_default_value, q=True, value1=True)

                attribute_compile_name = object + '_DOT_' + attribute
                if object and attribute:
                    if (pm.textFieldButtonGrp(FkIk_Arm_Setup_Controller[1], q=True, en=True)):
                        pm.addAttr(FkIk_Arm_Setup_Controller[0], ln=attribute_compile_name, at='float')
                        pm.setAttr('%s.%s' % (FkIk_Arm_Setup_Controller[0], attribute_compile_name), default_value,
                                   l=True)
                    else:
                        pm.addAttr(FkIk_Leg_Setup_Controller[0], ln=attribute_compile_name, at='float')
                        pm.setAttr('%s.%s' % (FkIk_Leg_Setup_Controller[0], attribute_compile_name), default_value,
                                   l=True)
                else:
                    pm.warning("Line # " + str(number_of_object) + " is empty! skipped this attribute")

def delete_setup(*args):
    sel = pm.ls(sl=1)[0]
    if sel:
        object_text_field_list = ['FkIk_Arm_Setup_Controller', 'FkIk_Leg_Setup_Controller',
                                  'Upper_Limb_Joint', 'Middle_Limb_Joint', 'Lower_Limb_Joint',
                                  'Upper_Limb_Fk_Ctrl', 'Middle_Limb_Fk_Ctrl', 'Lower_Limb_Fk_Ctrl',
                                  'Upper_Limb_Ik_Ctrl', 'Pole_Vector_Ik_Ctrl', 'Lower_Limb_Ik_Ctrl',
                                  'End_Limb_Joint', 'End_Limb_Fk_Ctrl', 'End_Limb_Ik_Ctrl', 'Middle_Translate_Aim_Joint',
                                  'Lower_Translate_Aim_Joint', 'Aim_Axis', 'Translate_Fk_Ctrl_Exists']

        if sel+'.'+'FkIk_Arm_Setup_Controller':
            for item in object_text_field_list:
                if pm.attributeQuery(item, n=sel, ex=True):
                    list_attr = pm.listAttr('%s.%s' % (sel, item), l=True)
                    if list_attr:
                        pm.setAttr('%s.%s' % (sel, list_attr[0]), l=False)
                    pm.deleteAttr('%s.%s' % (sel, item))

            list_attribute_additional = pm.listAttr(sel)
            if filter(lambda x: '_DOT_' in x, list_attribute_additional):
                filtering = filter(lambda x: '_DOT_' in x, list_attribute_additional)
                for item in filtering:
                    list_attr_layout = pm.listAttr('%s.%s' % (sel, item), l=True)
                    if list_attr_layout:
                        pm.setAttr('%s.%s' % (sel, list_attr_layout[0]), l=False)
                    pm.deleteAttr('%s.%s' % (sel, item))
        else:
            pm.warning('object already delete!')

    else:
        pm.warning('please select arm or leg setup for delete the setup!')
