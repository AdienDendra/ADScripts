from functools import partial

import pymel.core as pm
import maya.cmds as mc

class UI:
    def __init__(self):
        adien_snap_fkIk = 'AdienSnapFkIk'
        pm.window(adien_snap_fkIk, exists=True)

        if pm.window(adien_snap_fkIk, exists=True):
            pm.deleteUI(adien_snap_fkIk)
        with pm.window(adien_snap_fkIk, title='Adien Fk/Ik Setup', width=600, height=900):
            with pm.columnLayout(rs=5, w=530, co=('both',5), h=500, adj=1):
                with pm.rowColumnLayout(nc=2, co=(5,'both',5), cw=[(1,20), (2,500)],adj=1):
                    self.object = pm.checkBox(l='')
                    self.text_field_grp = mc.textFieldButtonGrp('zbw_tfbg_baseObj',  cal=(1, "right"), cw3=(190, 270, 50),
                                          label="Fk/Ik Arm Setup Controller:", w=490, bl="Get Object",
                                          bc='', adj=True, ip=1, it='None', ed=True)


                mc.textFieldButtonGrp('zbw_tfbg_baseObj', cal=(1, "right"), cw3=(190, 270, 50),
                                      label="Fk/Ik Leg Setup Controller: ", w=490, bl="Get Object",
                                      bc='', adj=True, ip=1, it='None')
                mc.textFieldButtonGrp('zbw_tfbg_baseObj', cal=(1, "right"), cw3=(190, 270, 50), label="Upper Limb Joint:",
                                      w=490, bl="Get Object", bc='', adj=True)
                mc.textFieldButtonGrp('zbw_tfbg_baseObj', cal=(1, "right"), cw3=(190, 270, 50), label="Middle Limb Joint:",
                                      w=490, bl="Get Object", bc='', adj=True)
                mc.textFieldButtonGrp('zbw_tfbg_baseObj', cal=(1, "right"), cw3=(190, 270, 50), label="Lower Limb Joint:",
                                      w=490, bl="Get Object", bc='', adj=True)
                mc.textFieldButtonGrp('zbw_tfbg_baseObj', cal=(1, "right"), cw3=(190, 270, 50), label="Upper Limb Fk Ctrl:",
                                      w=490, bl="Get Object", bc='', adj=True)
                mc.textFieldButtonGrp('zbw_tfbg_baseObj', cal=(1, "right"), cw3=(190, 270, 50), label="Middle Limb Fk Ctrl:",
                                      w=490, bl="Get Object", bc='', adj=True)
                mc.textFieldButtonGrp('zbw_tfbg_baseObj', cal=(1, "right"), cw3=(190, 270, 50), label="Lower Limb Fk Ctrl:",
                                      w=490, bl="Get Object", bc='', adj=True)
                mc.textFieldButtonGrp('zbw_tfbg_baseObj', cal=(1, "right"), cw3=(190, 270, 50), label="Upper Limb Ik Ctrl:",
                                      w=490, bl="Get Object", bc='', adj=True, ip=1, it='None')
                mc.textFieldButtonGrp('zbw_tfbg_baseObj', cal=(1, "right"), cw3=(190, 270, 50), label="Pole Vector Ik Ctrl:",
                                      w=490, bl="Get Object", bc='', adj=True)
                mc.textFieldButtonGrp('zbw_tfbg_baseObj', cal=(1, "right"), cw3=(190, 270, 50), label="Lower Limb Ik Ctrl:",
                                      w=490, bl="Get Object", bc='', adj=True)

                # button to create new message/obj field groups
                mc.separator(h=20, st="single")
                mc.button(w=150, l="add new message attr/obj", c=zbw_mmAddMObjs)
                mc.separator(h=20, st="single")

                mc.setParent(u=True)
                mc.rowColumnLayout("mmRCLayout", nc=2, co=(2, "left", 30))

                # back up to the 2nd columnLayout
                mc.setParent(u=True)
        pm.showWindow()

    def query_text_field(self):
        text = pm.textFieldButtonGrp(self.text_field_grp, q=1, ed=self.text_field_edit())
        return text

    def text_field_edit(self):
        if pm.checkBox(self.object, q=1, v=1, ofc=True):
            print 'True'
            return True
        else:
            print'False'
            return False


def zbw_mmAddMObjs(*args):
    """
    adds textFields to the UI for adding target objects for the message attrs
    """
    # delete text confirm dialogue if it exists
    zbw_mmDeleteConfirm()
    # figure out what objects are already parented
    children = cmds.rowColumnLayout("mmRCLayout", q=True, ca=True)
    # figure out where stuff goes (2 column layout, so divide by 2), 1 based
    if children:
        currentNum = len(children) / 2 + 1
        currentTFG = "attr" + str(currentNum)
        currentTFBG = "obj" + str(currentNum)
    # if no objects exist . . .
    else:
        currentTFG = "attr1"
        currentTFBG = "obj1"

    mc.textFieldGrp(currentTFG, l="addedAttr (ln)", cal=(1, "left"), cw2=(100, 150), p="mmRCLayout")
    mc.textFieldButtonGrp(currentTFBG, l="messageObj", cal=(1, "left"), cw3=(75, 150, 50), p="mmRCLayout", bl="get",
                          bc=partial(zbw_mmAddTarget, currentTFBG))


def zbw_mmAddTarget(currentTFBG, *args):
    """
    uses the selected item to add full path into the textField of the UI target obj
    """
    # check selection is one object
    sel = cmds.ls(sl=True, l=True)
    if len(sel) == 1:
        targetObj = sel[0]
        # add selected to textField
        mc.textFieldButtonGrp(currentTFBG, e=True, tx=targetObj)
    else:
        mc.error("please select one object to send out message attr")


display_ui()

