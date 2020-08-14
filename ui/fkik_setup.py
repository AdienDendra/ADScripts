from functools import partial

import pymel.core as pm

layout = 500
percentage = 0.01 * layout
# class UI:
def display_ui():
    adien_snap_fkIk = 'AdienFkIkSnapSetup'
    pm.window(adien_snap_fkIk, exists=True)
    if pm.window(adien_snap_fkIk, exists=True):
        pm.deleteUI(adien_snap_fkIk)
    with pm.window(adien_snap_fkIk, title='Adien Fk/Ik Snap Setup', width=600, height=800):
        with pm.scrollLayout('scroll'):
            with pm.columnLayout(rowSpacing=1 * percentage, w=layout, co=('both', 1 * percentage), adj=1):
                with pm.frameLayout(collapsable=True, l='Define Objects', mh=5):
                    with pm.rowColumnLayout(nc=2, rowSpacing=(2, 1 * percentage),
                                            co=(1 * percentage, 'both', 1 * percentage),
                                            cw=[(1, 5 * percentage), (2, 93 * percentage)]):

                        direction_control = pm.radioCollection()

                        direction0 = pm.radioButton(label='', cc=partial(enable_text_field, 'arm_setup_ctrl'))
                        define_object_text_field(define_object='arm_setup_ctrl', label="Fk/Ik Arm Setup Controller:",
                                                 add_feature=True)

                        direction1 = pm.radioButton(label='', cc=partial(enable_text_field, 'leg_setup_ctrl'))
                        define_object_text_field(define_object='leg_setup_ctrl', label="Fk/Ik Leg Setup Controller:",
                                                 add_feature=True, enable=False)

                        direction_control = pm.radioCollection(direction_control, edit=True, select=direction0)

                    define_object_text_field(define_object='upper_limb_joint', label="Upper Limb Joint:")
                    define_object_text_field(define_object='middle_limb_joint', label="Middle Limb Joint:")
                    define_object_text_field(define_object='lower_limb_joint', label="Lower Limb Joint:")
                    define_object_text_field(define_object='upper_limb_fk_ctrl', label="Upper Limb Fk Ctrl:")
                    define_object_text_field(define_object='middle_limb_fk_ctrl', label="Middle Limb Fk Ctrl:")
                    define_object_text_field(define_object='lower_limb_fk_ctrl', label="Lower Limb Fk Ctrl:")

                    with pm.rowColumnLayout(nc=2, rowSpacing=(2, 1 * percentage),
                                            co=(1 * percentage, 'both', 1 * percentage),
                                            cw=[(1, 5 * percentage), (2, 93 * percentage)]):
                        pm.checkBox(label='', cc=partial(enable_text_field, 'upperLimb_ik_ctrl'), value=True)
                        define_object_text_field(define_object='upperLimb_ik_ctrl', label="Upper Limb Ik Ctrl:",
                                                 add_feature=True)

                    define_object_text_field(define_object='pole_vector_ik_ctrl', label="Pole Vector Ik Ctrl:")
                    define_object_text_field(define_object='lower_limb_ik_ctrl', label="Lower Limb Ik Ctrl:")

                    with pm.rowLayout(nc=1, cw1=(35 * percentage), cl1=('center'),
                                      columnAttach=[(1, 'both', 2 * percentage)]
                                      ):
                        pm.button("clear_all", bgc=(1, 1, 0), l="Clear All!",
                                 c=partial(clear_text_field, 'arm_setup_ctrl', 'leg_setup_ctrl','upper_limb_joint',
                                           'middle_limb_joint','lower_limb_joint', 'upper_limb_fk_ctrl',
                                           'middle_limb_fk_ctrl', 'lower_limb_fk_ctrl', 'upperLimb_ik_ctrl',
                                           'pole_vector_ik_ctrl', 'lower_limb_ik_ctrl'))

                pm.separator(h=10, st="in", w=layout)

                with pm.frameLayout(collapsable=True, l='Additional Attributes', mh=5):
                    # with pm.rowColumnLayout(nc=2, rowSpacing=(2, 1*percentage), co=(1*percentage,'both',1*percentage), cw=[(1, 49*percentage), (2, 49*percentage)]):
                    with pm.rowLayout(nc=2, cw2=(49 * percentage, 49 * percentage), cl2=('center', 'center'),
                                      columnAttach=[(1, 'both', 2 * percentage), (2, 'both', 2 * percentage)]
                                      ):
                        pm.button(l="Add Object | Set Attribute Value", bgc=(0, 0, 0.5), c=add_text_field_grp)
                        # create button to delete last pair of text fields
                        pm.button("delete_last_button", bgc=(0.5, 0, 0), l="Delete",
                                  c=delete_additional_attr)

                        pm.setParent(u=True)
                        pm.rowColumnLayout("row_column_add_object", nc=3)

                        # back up to the 2nd columnLayout
                        pm.setParent(u=True)

                pm.separator(h=10, st="in", w=layout)
                with pm.frameLayout(collapsable=True, l='Setup', mh=5):
                    pm.text(l='Select Leg/Arm Ctrl Setup :')
                    with pm.rowLayout(nc=2, cw2=(49 * percentage, 49 * percentage), cl2=('center', 'center'),
                                      columnAttach=[(1, 'both', 2 * percentage), (2, 'both', 2 * percentage)]
                                      ):
                        pm.button("run_setup", bgc=(0, 0.5, 0), l="Run Setup",
                                  c='')
                        pm.button("delete_setup", bgc=(0.5, 0, 0), l="Delete Setup",
                                  c='')

                pm.separator(h=10, st="in", w=layout)
                pm.text(l='<a href="http://projects.adiendendra.com/">find out how to use it! >> </a>', hl=True,
                        al='center')
                pm.separator(h=1, st="none", w=layout)

            # # back up to the 2nd columnLayout
            pm.setParent(u=True)
    pm.showWindow()

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
    pm.textFieldButtonGrp(object, edit=True, enable=value, tx='')

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
    pm.textFieldGrp(current_default_value, l="Default Value:", cal=(1, "right"), cw2=(17 * percentage, 8 * percentage),
                    p="row_column_add_object")


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



# def zbw_mmAddTarget(currentTFBG, *args):
#     """
#     uses the selected item to add full path into the textField of the UI target obj
#     """
#     # check selection is one object
#     sel = pm.ls(sl=True, l=True)
#     if len(sel) == 1:
#         targetObj = sel[0]
#         # add selected to textField
#         pm.textFieldButtonGrp(currentTFBG, e=True, tx=targetObj)
#     else:
#         pm.error("please select one object to send out message attr")





# def query_text_field(self):
    #     text = pm.textFieldButtonGrp(self.text_field_grp, q=1, ed=self.text_field_edit())
    #     return text
    #
    # def text_field_edit(self):
    #     if pm.checkBox(self.object, q=1, v=1, ofc=True):
    #         print 'True'
    #         return True
    #     else:
    #         print'False'
    #         return False

# pm.checkBox(label='', cc=arm_enable_field, value=True)
# pm.textFieldButtonGrp("arm_setup_ctrl", label="Fk/Ik Arm Setup Controller:",
#                                         cal=(1, "right"), cw3=(190, 270, 50), w=490, bl="Get Object",
#                                         bc='', adj=True, ip=1)
#
# pm.checkBox(label='', cc=leg_enable_field, value=True)
# pm.textFieldButtonGrp('leg_setup_ctrl', label="Fk/Ik Leg Setup Controller:",
#                                         cal=(1, "right"), cw3=(190, 270, 50), w=490, bl="Get Object",
#                                         bc='', adj=True, ip=1)

# def zbw_mmAddMObjs(*args):
#     """
#     adds textFields to the UI for adding target objects for the message attrs
#     """
#     # delete text confirm dialogue if it exists
#     zbw_mmDeleteConfirm()
#     # figure out what objects are already parented
#     children = cmds.rowColumnLayout("row_column_add_object", q=True, ca=True)
#     # figure out where stuff goes (2 column layout, so divide by 2), 1 based
#     if children:
#         currentNum = len(children) / 2 + 1
#         currentTFG = "attr" + str(currentNum)
#         currentTFBG = "obj" + str(currentNum)
#     # if no objects exist . . .
#     else:
#         currentTFG = "attr1"
#         currentTFBG = "obj1"
#
#     pm.textFieldGrp(currentTFG, l="addedAttr (ln)", cal=(1, "left"), cw2=(100, 150), p="row_column_add_object")
#     pm.textFieldButtonGrp(currentTFBG, l="messageObj", cal=(1, "left"), cw3=(75, 150, 50), p="row_column_add_object", bl="get",
#                           bc=partial(zbw_mmAddTarget, currentTFBG))
#
#
# def zbw_mmAddTarget(currentTFBG, *args):
#     """
#     uses the selected item to add full path into the textField of the UI target obj
#     """
#     # check selection is one object
#     sel = cmds.ls(sl=True, l=True)
#     if len(sel) == 1:
#         targetObj = sel[0]
#         # add selected to textField
#         pm.textFieldButtonGrp(currentTFBG, e=True, tx=targetObj)
#     else:
#         pm.error("please select one object to send out message attr")
