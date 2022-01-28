import maya.cmds as mc
import maya.mel as mel
from functools import partial
import maya.OpenMaya as om
import ast

MENU_NAME = "markingMenu"
STRING_NAME ='_adNote'

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

# delete the _adNet node all in the scene
def ad_delete_all_default_attrs(*args):
    confirm_dialog = mc.confirmDialog(title='Confirm', message='Are you sure to delete all default attributes?',
                                      button=['Yes', 'No'], defaultButton='Yes',
                       cancelButton='No', dismissString='No')
    if confirm_dialog == 'Yes':
        transform_listing = mc.ls()
        for object in transform_listing:
            node_type = mc.nodeType(object)
            if node_type == 'nurbsCurve':
                object = mc.listRelatives(object, p=1)[0]
                ad_delete_attr(object)
            elif node_type == 'joint':
                ad_delete_attr(object)
            else:
                pass
    else:
        om.MGlobal.displayInfo("Cancel Delete All Default Attr!")


# delete the _adNet node with selection
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
        om.MGlobal.displayInfo("Delete Default Attr %s" % selection)
    else:
        om.MGlobal.displayInfo('There is no attr value %s has been set! Skipped delete!' % selection)

# reset the value attr
def ad_reset_to_default(*args):
    selection = mc.ls(sl=1)
    if not selection:
        om.MGlobal.displayWarning('Please select at least one object to Reset to Default!')
    else:
        for object in selection:
            # node = ad_reset_delete_query_attr(object)
            attr_note = mc.attributeQuery(STRING_NAME, node=object, exists=True)

            # if the node exists
            if attr_note:
                get_dic = mc.getAttr('%s.%s' % (object, STRING_NAME))
                dict_encode = ast.literal_eval(get_dic)
                for (key, value) in dict_encode.items():
                    mc.setAttr('%s.%s' % (object, key), value)
            else:
                om.MGlobal.displayWarning("Reset %s skipped! Please set the 'Define Attr Value' first!" % object)

# define attr value to marking menu
def ad_set_default_attr(*args):
    selection = mc.ls(sl=1)
    if selection:
        # For every node in selection #
        for item in selection:
            node_name = item+'.'+ STRING_NAME
            key_value_dic = ad_get_attr_value(item)
            mc.setAttr(node_name, key_value_dic, type='string')
    else:
        om.MGlobal.displayWarning('Please select at least one object to Define Attr Value!')

# add and set the attr
def ad_add_attr_node(node, attribute_name, attribute_type, setAttr=False, attr=[], value=[]):
    query_attr = mc.attributeQuery(attribute_name, node=node, exists=True)
    if query_attr:
        pass
    else:
        mc.addAttr(node, ln=attribute_name, at=attribute_type)
    if setAttr:
        mc.setAttr(node+'.'+attr, value)

# channel attr on the object
def ad_channel_attr():
    # Get the currently selected attributes from the main channelbox.
    channelBox = mel.eval('global string $gChannelBoxName; $temp=$gChannelBoxName;')  # fetch maya's main channelbox
    attrs = mc.channelBox(channelBox, q=1, sma=1)
    if not attrs:
        return []
    return attrs

# get attribute name and that value
def ad_get_attr_value(selection):
    # storing dictionary
    dic ={}

    # for node in selection:
    attr_note = mc.attributeQuery(STRING_NAME, node=selection, exists=True)
    if attr_note:
        pass
    else:
        mc.addAttr(selection, ln=STRING_NAME, dt='string')
        mc.setAttr(selection+'.'+STRING_NAME, e=True, k=True)
    # ad_add_attr_node(selection, attribute_name='_adNet', attribute_type='string')

    # If no channels are selected:
    if ad_channel_attr() == []:
        for attr in mc.listAnimatable(selection):
            # Sort out the actual name of just the attribute.
            attr = mc.ls(attr, sn=True)[0]
            attr = attr.partition('.')[2]
            # get the value.
            get_value = mc.getAttr('%s.%s' % (selection, attr))
            # storing into dic
            dic[attr] = get_value
    for attr in ad_channel_attr():
        # get the value.
        get_value = mc.getAttr('%s.%s' % (selection, attr))
        # storing into dic
        dic[attr] = get_value
    return dic