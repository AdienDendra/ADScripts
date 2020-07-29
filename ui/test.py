import pymel.core as pm
import maya.cmds as mc


def display_ui():
    adien_snap_fkIk = 'AdienSnapFkIk'
    pm.window(adien_snap_fkIk, exists=True)

    if pm.window(adien_snap_fkIk, exists=True):
        pm.deleteUI(adien_snap_fkIk)

    with pm.window(adien_snap_fkIk, title='Adien Fk/Ik Snap', width=275, height=50):
        with pm.columnLayout(w=505, h=300):
            mc.separator(h=5, st="single")
            mc.textFieldButtonGrp('zbw_tfbg_baseObj', cal=(1, "right"), cw3=(120, 300, 85),
                                  label="Fk/Ik Arm Controller:", w=500, bl="Get Object",
                                  bc=partial(zbw_mmAddBase, "zbw_tfbg_baseObj", "clear"))
            mc.separator(h=2, st="single")
            mc.textFieldButtonGrp('zbw_tfbg_baseObj', cal=(1, "right"), cw3=(120, 300, 85),
                                  label="Fk/Ik Leg Controller:", w=500, bl="Get Object",
                                  bc=partial(zbw_mmAddBase, "zbw_tfbg_baseObj", "clear"))
            mc.separator(h=2, st="single")
            mc.textFieldButtonGrp('zbw_tfbg_baseObj', cal=(1, "right"), cw3=(120, 300, 85), label="Upper Limb Joint:",
                                  w=500, bl="Get Object", bc=partial(zbw_mmAddBase, "zbw_tfbg_baseObj", "clear"))
            mc.separator(h=2, st="single")
            mc.textFieldButtonGrp('zbw_tfbg_baseObj', cal=(1, "right"), cw3=(120, 300, 85), label="Middle Limb Joint:",
                                  w=500, bl="Get Object", bc=partial(zbw_mmAddBase, "zbw_tfbg_baseObj", "clear"))
            mc.separator(h=2, st="single")
            mc.textFieldButtonGrp('zbw_tfbg_baseObj', cal=(1, "right"), cw3=(120, 300, 85), label="Lower Limb Joint:",
                                  w=500, bl="Get Object", bc=partial(zbw_mmAddBase, "zbw_tfbg_baseObj", "clear"))

            # button to create new message/obj field groups
            mc.separator(h=20, st="single")
            mc.button(w=150, l="add new message attr/obj", c=zbw_mmAddMObjs)
            mc.separator(h=20, st="single")

            mc.setParent(u=True)
            mc.rowColumnLayout("mmRCLayout", nc=2, co=(2, "left", 30))

            # back up to the 2nd columnLayout
            mc.setParent(u=True)
    pm.showWindow()


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

