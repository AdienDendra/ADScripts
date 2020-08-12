from functools import partial

import pymel.core as pm
import maya.cmds as mc

layout = 500

# class UI:
def UI():
    adien_snap_fkIk = 'AdienFkIkSnapSetup'
    pm.window(adien_snap_fkIk, exists=True)
    percentage = 0.01*layout
    if pm.window(adien_snap_fkIk, exists=True):
        pm.deleteUI(adien_snap_fkIk)
    with pm.window(adien_snap_fkIk, title='Adien Fk/Ik Snap Setup', width=600, height=5000):
        with pm.scrollLayout('scroll'):
            with pm.columnLayout(rowSpacing=1*percentage, w=layout, co=('both',1*percentage), adj=1):
                with pm.frameLayout(collapsable=True, l= 'Define Objects', mh=5):
                    with pm.rowColumnLayout(nc=2, rowSpacing=(2, 1*percentage), co=(1*percentage,'both',1*percentage), cw=[(1, 5*percentage), (2, 93*percentage)]):
                        direction_control = pm.radioCollection()
                        direction0 = pm.radioButton(label='', cc=arm_enable_field)
                        mc.textFieldButtonGrp("arm_setup_ctrl", label="Fk/Ik Arm Setup Controller:",
                                                                cal=(1, "right"), cw3=(28*percentage, 50*percentage, 15*percentage), w=93*percentage, bl="Get Object",
                                                                bc='')

                        direction1 = pm.radioButton(label='', cc=leg_enable_field)
                        mc.textFieldButtonGrp('leg_setup_ctrl', label="Fk/Ik Leg Setup Controller:",
                                              cal=(1, "left"), cw3=(28 * percentage, 50 * percentage, 15 * percentage),
                                              w=93 * percentage, bl="Get Object",
                                              bc='', enable=False)
                        direction_control = pm.radioCollection(direction_control, edit=True, select=direction0)

                    mc.textFieldButtonGrp(label="Upper Limb Joint:", cal=(1, "right"),
                                          cw3=(33*percentage, 50*percentage, 15*percentage), w=98*percentage, bl="Get Object",
                                                            bc='')
                    mc.textFieldButtonGrp(label="Middle Limb Joint:",cal=(1, "right"),
                                          cw3=(33*percentage, 50*percentage, 15*percentage), w=98*percentage, bl="Get Object",
                                                            bc='')
                    mc.textFieldButtonGrp(label="Lower Limb Joint:",cal=(1, "right"),
                                          cw3=(33*percentage, 50*percentage, 15*percentage), w=98*percentage, bl="Get Object",
                                                            bc='')
                    mc.textFieldButtonGrp(label="Upper Limb Fk Ctrl:",cal=(1, "right"),
                                          cw3=(33*percentage, 50*percentage, 15*percentage), w=98*percentage, bl="Get Object",
                                                            bc='')
                    mc.textFieldButtonGrp(label="Middle Limb Fk Ctrl:",cal=(1, "right"),
                                          cw3=(33*percentage, 50*percentage, 15*percentage), w=98*percentage, bl="Get Object",
                                                            bc='')
                    mc.textFieldButtonGrp(label="Lower Limb Fk Ctrl:",cal=(1, "right"),
                                          cw3=(33*percentage, 50*percentage, 15*percentage), w=98*percentage, bl="Get Object",
                                                            bc='')
                    with pm.rowColumnLayout(nc=2, rowSpacing=(2, 1*percentage), co=(1*percentage,'both',1*percentage), cw=[(1, 5*percentage), (2, 93*percentage)]):
                        pm.checkBox(label='', cc=upperLimb_ik_enable_field, value=True)
                        mc.textFieldButtonGrp('upperLimb_ik_ctrl', label="Upper Limb Ik Ctrl:",cal=(1, "right"),
                                              cw3=(28 * percentage, 50 * percentage, 15 * percentage),
                                              w=93 * percentage, bl="Get Object",
                                                                bc='')
                    mc.textFieldButtonGrp(label="Pole Vector Ik Ctrl:",cal=(1, "right"),
                                          cw3=(33*percentage, 50*percentage, 15*percentage), w=98*percentage, bl="Get Object",
                                                            bc='')
                    mc.textFieldButtonGrp(label="Lower Limb Ik Ctrl:",cal=(1, "right"),
                                          cw3=(33*percentage, 50*percentage, 15*percentage), w=98*percentage, bl="Get Object",
                                                            bc='')
                pm.separator(h=10, st="in", w=layout)

                with pm.frameLayout(collapsable=True, l= 'Additional Attributes', mh=5):
                    # with pm.rowColumnLayout(nc=2, rowSpacing=(2, 1*percentage), co=(1*percentage,'both',1*percentage), cw=[(1, 49*percentage), (2, 49*percentage)]):
                    with pm.rowLayout(nc=2, cw2=(49*percentage,49*percentage), cl2=('center','center'),
                                      columnAttach=[(1, 'both', 2*percentage), (2, 'both', 2*percentage)]
                                      ):

                        pm.button(l="Add Object | Set Attribute Value", bgc=(0,0,0.5),  c=add_object_attributes)
                        # create button to delete last pair of text fields
                        pm.button("delete_last_button", bgc=(0.5, 0, 0), l="Delete",
                                    c=zbw_mmDeleteLast)

                        pm.setParent(u=True)
                        pm.rowColumnLayout("row_column_add_object", nc=2, co=(2, "left", 30))

                        # back up to the 2nd columnLayout
                        pm.setParent(u=True)

                pm.separator(h=10, st="in", w=layout)
                with pm.frameLayout(collapsable=True, l='Setup', mh=5):
                    pm.text(l='Select Leg/Arm Ctrl Setup :')
                    with pm.rowLayout(nc=2, cw2=(49*percentage,49*percentage), cl2=('center','center'),
                                      columnAttach=[(1, 'both', 2*percentage), (2, 'both', 2*percentage)]
                                      ):
                        pm.button("run_setup", bgc=(0, 0.5, 0), l="Run Setup",
                                  c='')
                        pm.button("delete_setup", bgc=(0.5, 0, 0), l="Delete Setup",
                                  c='')

                pm.separator(h=10, st="in", w=layout)
                pm.text(l='<a href="http://projects.adiendendra.com/">find out how to use it! >> </a>', hl=True, al='center')

            # # back up to the 2nd columnLayout
            mc.setParent(u=True)
    pm.showWindow()

def arm_enable_field(value, *args):
    mc.textFieldButtonGrp("arm_setup_ctrl", edit=True, enable=value)

def leg_enable_field(value, *args):
    mc.textFieldButtonGrp("leg_setup_ctrl", edit=True, enable=value)

def upperLimb_ik_enable_field(value, *args):
    mc.textFieldButtonGrp("upperLimb_ik_ctrl", edit=True, enable=value)

def add_object_attributes( *args):
    percentage = 0.01*layout
    delete_rowColumn()
    child_array = pm.rowColumnLayout("row_column_add_object", q=True, ca=True)
    if child_array:
        currentNum = len(child_array) / 2 + 1
        currentTFG = "attr" + str(currentNum)
        currentTFBG = "obj" + str(currentNum)
    else:
        currentTFG = "attr1"
        currentTFBG = "obj1"
        
    mc.textFieldButtonGrp(currentTFBG, l="Attribute:", cal=(1, "left"), cw3=(10*percentage, 43*percentage, 15*percentage), p="row_column_add_object", bl="Get Object",
                            bc=partial(zbw_mmAddTarget, currentTFBG))
    mc.textFieldGrp(currentTFG, l="Default Value:", cal=(1, "right"), cw2=(15*percentage, 8*percentage), p="row_column_add_object")

def delete_rowColumn():
    if (pm.text("mmTextConfirm", q=True, ex=True)):
        pm.deleteUI("mmTextConfirm")
        pm.deleteUI("mmConfirmSep")

def zbw_mmAddTarget(currentTFBG, *args):
    """
    uses the selected item to add full path into the textField of the UI target obj
    """
    # check selection is one object
    sel = mc.ls(sl=True, l=True)
    if len(sel) == 1:
        targetObj = sel[0]
        # add selected to textField
        mc.textFieldButtonGrp(currentTFBG, e=True, tx=targetObj)
    else:
        mc.error("please select one object to send out message attr")

def zbw_mmDeleteLast(*args):
    """
    deletes the last pair of attr, obj text fields in the UI
    """
    children = pm.rowColumnLayout("row_column_add_object", q=True, ca=True)

    if children:
        numChildren = len(children)
        lastTFG = "attr" + str(numChildren / 2)
        lastTFBG = "obj" + str(numChildren / 2)
        pm.deleteUI(lastTFG)
        pm.deleteUI(lastTFBG)

    else:
        pass

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


# mc.checkBox(label='', cc=arm_enable_field, value=True)
# mc.textFieldButtonGrp("arm_setup_ctrl", label="Fk/Ik Arm Setup Controller:",
#                                         cal=(1, "right"), cw3=(190, 270, 50), w=490, bl="Get Object",
#                                         bc='', adj=True, ip=1)
#
# mc.checkBox(label='', cc=leg_enable_field, value=True)
# mc.textFieldButtonGrp('leg_setup_ctrl', label="Fk/Ik Leg Setup Controller:",
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
#     mc.textFieldGrp(currentTFG, l="addedAttr (ln)", cal=(1, "left"), cw2=(100, 150), p="row_column_add_object")
#     mc.textFieldButtonGrp(currentTFBG, l="messageObj", cal=(1, "left"), cw3=(75, 150, 50), p="row_column_add_object", bl="get",
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
#         mc.textFieldButtonGrp(currentTFBG, e=True, tx=targetObj)
#     else:
#         mc.error("please select one object to send out message attr")

