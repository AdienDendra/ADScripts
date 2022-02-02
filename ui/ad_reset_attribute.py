import ast
from functools import partial

import maya.OpenMaya as om
import maya.cmds as mc
import maya.mel as mel

MENU_NAME = "markingMenu"
STRING_NAME = '_adNote'


class markingMenu():
    def __init__(self):
        self.removeOld()
        self.build()

    def build(self):
        mc.popupMenu(MENU_NAME, mm=1, b=2, aob=1, ctl=1, alt=1, sh=0, p="viewPanes", pmo=1, pmc=self.buildMarkingMenu)

    def removeOld(self):
        if mc.popupMenu(MENU_NAME, ex=1):
            mc.deleteUI(MENU_NAME)

    def buildMarkingMenu(self, menu, parent):
        # Radial positioned
        mc.menuItem(p=menu, l="Delete All Default Attrs", rp="SE", c=partial(ad_delete_all_default_attrs))
        mc.menuItem(p=menu, l="Delete Default Attr", rp="SW", c=partial(ad_delete_default_attr))
        mc.menuItem(p=menu, l="Set Default Attr", rp="NW", c=partial(ad_set_default_attr))
        mc.menuItem(p=menu, l="Reset to Default", rp="NE", c=partial(ad_reset_to_default))


markingMenu()


# delete the all of _adNote attribute in the scene
def ad_delete_all_default_attrs(*args):
    # create confirm dialog
    confirm_dialog = mc.confirmDialog(title='Confirm', message='Are you sure to delete all default attributes?',
                                      button=['Yes', 'No'], defaultButton='Yes',
                                      cancelButton='No', dismissString='No')
    # condition of dialog
    if confirm_dialog == 'Yes':
        # listing all object in the scene
        transform_listing = mc.ls()
        # selection all the object nurbsCurve and joint
        for object in transform_listing:
            try:
                # query the object selection whether it has shape
                object_type = mc.objectType(mc.listRelatives(object, s=1))
            except:
                pass
            else:
                # if it has a shape check whether it curves object
                if object_type == 'nurbsCurve':
                    ad_delete_attr(object)

            # condition if it's joint
            if mc.nodeType(object) == 'joint':
                ad_delete_attr(object)
            else:
                pass
    else:
        om.MGlobal.displayInfo("Cancel Delete All Default Attr!")


# delete the _adNote attribute with selection
def ad_delete_default_attr(*args):
    selection = mc.ls(sl=1)
    for object in selection:
        if not object:
            om.MGlobal.displayWarning('Please select at least one object to Delete Default Attr!')
        else:
            ad_delete_attr(object)


# deleting the node network
def ad_delete_attr(selection):
    # get the node name
    attribute = mc.attributeQuery(STRING_NAME, node=selection, exists=True)
    # if the node exists delete the node and attribute _adNet on object
    if attribute:
        # mc.delete(node)
        mc.deleteAttr('%s.%s' % (selection, STRING_NAME))
        om.MGlobal.displayInfo("Delete Default Attr %s!" % selection)
    else:
        om.MGlobal.displayInfo('There is no attr value %s has been set! Skipped delete!' % selection)


# reset the value attr
def ad_reset_to_default(*args):
    selection = mc.ls(sl=1)
    if not selection:
        om.MGlobal.displayWarning('Please select at least one object to Reset to Default!')
    else:
        for object in selection:
            # query the _adNote attribute in the object selection
            attr_note = mc.attributeQuery(STRING_NAME, node=object, exists=True)
            # if the _adNote attribute exists
            if attr_note:
                get_dic = mc.getAttr('%s.%s' % (object, STRING_NAME))
                # evaluate a dictionary display
                dict_encode = ast.literal_eval(get_dic)
                # condition if the attribute object not selected
                if ad_channel_attr() == []:
                    for (key, value) in dict_encode.items():
                        mc.setAttr('%s.%s' % (object, key), value)

                # when the specific the attribute reset
                for attr in ad_channel_attr():
                    mc.setAttr('%s.%s' % (object, attr), dict_encode.get(attr))

            else:
                om.MGlobal.displayWarning("Reset %s skipped! Please set the 'Define Attr Value' first!" % object)


# channel attr on the selection object
def ad_channel_attr():
    # get the currently selected attributes from the main channel box.
    channelBox = mel.eval('global string $gChannelBoxName; $temp=$gChannelBoxName;')  # fetch maya's main channelbox
    attrs = mc.channelBox(channelBox, q=1, sma=1)
    if not attrs:
        return []
    print attrs
    return attrs


# set the default attribute from marking menu
def ad_set_default_attr(*args):
    selection = mc.ls(sl=1)
    if selection:
        # for every node in selection
        for item in selection:
            node_name = item + '.' + STRING_NAME
            # get the value and key to storing in dic
            key_value_dic = ad_get_attr_value(item)
            mc.setAttr(node_name, key_value_dic, type='string')
    else:
        om.MGlobal.displayWarning('Please select at least one object to Define Attr Value!')


# get attribute name and that value
def ad_get_attr_value(selection):
    # storing dictionary
    dic = {}
    # query _adNote in selection object
    attr_note = mc.attributeQuery(STRING_NAME, node=selection, exists=True)
    if attr_note:
        pass
    else:
        # add string extra attribute on selection object
        mc.addAttr(selection, ln=STRING_NAME, dt='string')
        mc.setAttr(selection + '.' + STRING_NAME, e=True, k=True)
    # get all animatable attribute in the scene of the selection object
    for attr in mc.listAnimatable(selection):
        # Sort out the actual name of just the attribute.
        attr = mc.ls(attr, sn=True)[0]
        attr = attr.partition('.')[2]
        # get the value.
        get_value = mc.getAttr('%s.%s' % (selection, attr))
        # storing into dic
        dic[attr] = get_value

    return dic
