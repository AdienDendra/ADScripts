import maya.cmds as mc
import maya.mel as mel
from functools import partial
import maya.OpenMaya as om

MENU_NAME = "markingMenu"

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
        transform_listing = mc.ls(type='transform')
        ad_delete_node(transform_listing)
    else:
        om.MGlobal.displayInfo("Cancel delete Define Attr Value!")


# delete the _adNet node with selection
def ad_delete_default_attr(*args):
    selection = mc.ls(sl=1)
    if not selection:
        om.MGlobal.displayWarning('Please select at least one object to Delete Attr Value!')
    else:
        ad_delete_node(selection)

# deleting the node network
def ad_delete_node(selection):
    for object in selection:
        # get the node name
        node = ad_reset_delete_query_attr(object)
        # if the node exists delete the node and attribute _adNet on object
        if node:
            mc.delete(node)
            mc.deleteAttr('%s._adNet' % object)
            om.MGlobal.displayInfo("Delete Define Attr Value %s" % object)
        else:
            pass


# reset the value attr
def ad_reset_to_default(*args):
    selection = mc.ls(sl=1)
    if not selection:
        om.MGlobal.displayWarning('Please select at least one object to Reset Attr Value!')
    else:
        for object in selection:
            # get the node name
            node = ad_reset_delete_query_attr(object)
            # if the node exists
            if node:
                # query all the attribute in node
                list_attributes = mc.listAttr(node, ud=1)
                # get the value on every attribute then set to the selection object
                for attribute in list_attributes:
                    get_value = mc.getAttr('%s.%s' % (node, attribute))
                    mc.setAttr('%s.%s' % (object, attribute), get_value)
                # else:
                #     om.MGlobal.displayWarning("Reset %s skipped! Please set the 'Define Attr Value' first!" % object)
            else:
                om.MGlobal.displayWarning("Reset %s skipped! Please set the 'Define Attr Value' first!" % object)

# query the node for reset and delete function
def ad_reset_delete_query_attr(selection):

    attr_node = mc.attributeQuery("_adNet", node=selection, exists=True)
    # check the connection exists
    if attr_node:
        # query the source node name
        node = mc.listConnections(selection + '._adNet', s=True)[0]
        return node

    else:
        om.MGlobal.displayInfo('There is no Define Attr Value exists to %s. Skipped the job!' % selection)


# define attr value to marking menu
def ad_set_default_attr(*args):
    selection = mc.ls(sl=1)
    if selection:
        # For every node in selection #
        for item in selection:
            key_value_message = ad_get_attr_value(item)
            node_name = item+'_adNet'
            for (key, value) in key_value_message.items():
                if mc.objExists(node_name):
                    pass
                else:
                    # create node
                    network_node = mc.createNode('network', n=node_name)
                    mc.connectAttr(network_node+'.message', item+'._adNet')

                # get the value and add to attr
                ad_add_attr_node(node_name, attribute_name=key, attribute_type='double',
                                 setAttr=True, attr=key, value=value)
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
    ad_add_attr_node(selection, attribute_name='_adNet', attribute_type='message')

    # If no channels are selected:
    if ad_channel_attr() == []:
        for attr in mc.listAnimatable(selection):
            # Sort out the actual name of just the attribute.
            attr = mc.ls(attr, sn=True)[0]
            # print attr
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
