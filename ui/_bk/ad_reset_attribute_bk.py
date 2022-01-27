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
        menu = mc.popupMenu(MENU_NAME, mm=1, b=2, aob=1, ctl=1, alt=1, sh=0, p="viewPanes", pmo=1, pmc=self.buildMarkingMenu)

    def removeOld(self):
        if mc.popupMenu(MENU_NAME, ex=1):
            mc.deleteUI(MENU_NAME)

    def buildMarkingMenu(self, menu):

        # Radial positioned
        mc.menuItem(p=menu, l="Delete All Define Value", rp="SE", c=partial(ad_delete_all_define_value))
        mc.menuItem(p=menu, l="Delete Define Value", rp="SW", c=partial(ad_delete_define_value))
        mc.menuItem(p=menu, l="Define Attr Value", rp="NW", c=partial(ad_define_attr_value))
        mc.menuItem(p=menu, l="Reset Attr Value", rp="NE", c=partial(ad_reset_attr_value))

markingMenu()


# def ad_create_attr_t_r_s(object):
#     for item in object:
#         # condition if attribute t in AD attribute is exist
#         if mc.attributeQuery('AD_trans', node= item, exists=True):
#             pass
#         # otherwise
#         else:
#             mc.addAttr(item, longName='AD_trans', at='double3')
#             mc.addAttr(item, longName='tX', attributeType='double', parent='AD_trans')
#             mc.addAttr(item, longName='tY', attributeType='double', parent='AD_trans')
#             mc.addAttr(item, longName='tZ', attributeType='double', parent='AD_trans')
#
#         # condition if attribute r in AD attribute is exist
#         if mc.attributeQuery('AD_rot', node= item, exists=True):
#             pass
#         # otherwise
#         else:
#             mc.addAttr(item, longName='AD_rot', at='double3')
#             mc.addAttr(item, longName='rX', attributeType='double', parent='AD_rot')
#             mc.addAttr(item, longName='rY', attributeType='double', parent='AD_rot')
#             mc.addAttr(item, longName='rZ', attributeType='double', parent='AD_rot')
#
#        # condition if attribute s in AD attribute is exist
#         if mc.attributeQuery('AD_scl', node= item, exists=True):
#             pass
#         # otherwise
#         else:
#             mc.addAttr(item, longName='AD_scl', at='double3')
#             mc.addAttr(item, longName='sX', attributeType='double', parent='AD_scl')
#             mc.addAttr(item, longName='sY', attributeType='double', parent='AD_scl')
#             mc.addAttr(item, longName='sZ', attributeType='double', parent='AD_scl')
#
#         # query the attribute and value
#         for (key, value) in ad_query_attr(['t','r','s'], item).items():
#             # condition if the attribute object keyable (hide)
#             if mc.getAttr(item + '.' + key, k=True):
#                 # condition if the attribute object locked
#                 lock = mc.getAttr(item + '.' + key, l=True)
#                 if lock:
#                     # if it's locked skip it
#                     attr_locked_query = mc.getAttr('%s.%s' % (item, key[:-1] + key[-1].upper()), l=True)
#                     if attr_locked_query:
#                         pass
#                     # otherwise set  the value attribute AD as attribute object value
#                     else:
#                         mc.setAttr('%s.%s' % (item, key[:-1] + key[-1].upper()), l=True)
#
#                 # if  attribute object not locked or keyable
#                 else:
#                     # check if the AD attribute locked
#                     attr_locked_query = mc.getAttr('%s.%s' % (item, key[:-1] + key[-1].upper()), l=True)
#                     if attr_locked_query:
#                         mc.setAttr('%s.%s' % (item, key[:-1]+ key[-1].upper()), l=False)
#
#                     # if not then set the value attribute AD as attribute object value
#                     else:
#                         mc.setAttr('%s.%s' % (item, key[:-1]+ key[-1].upper()), value)
#
#             # if it's not keyable then lock the AD attribute
#             else:
#                 mc.setAttr('%s.%s' % (item, key[:-1] + key[-1].upper()), l=True)
#
#
# # def ad_add_attr():
# #
#
# def ad_query_attr(channel, ctrl):
#     # query value with attribute
#     attr_list = ad_attr_axis(channel)
#     dic = OrderedDict()
#     for at in attr_list:
#         attr_value = mc.getAttr(ctrl + '.' + at)
#         # attribute : value
#         dic[at] = attr_value
#     return dic
#
# def ad_attr_axis(channel):
#     # get the axis x, y, z attribute
#     attr_list = []
#     for lc in channel:
#         if lc in ['t', 'r', 's']:
#             for axis in ['x', 'y', 'z']:
#                 at = lc + axis
#                 attr_list.append(at)
#         else:
#             attr_list.append(lc)
#     return attr_list


# delete the _adNet node all in the scene
def ad_delete_all_define_value(*args):
    confirm_dialog = mc.confirmDialog(title='Confirm', message='Are you sure to delete all define values?',
                                      button=['Yes', 'No'], defaultButton='Yes',
                       cancelButton='No', dismissString='No')
    if confirm_dialog == 'Yes':
        transform_listing = mc.ls(type='transform')
        ad_delete_node(transform_listing)
    else:
        om.MGlobal.displayInfo("Cancel delete Define Attr Value!")


# delete the _adNet node with selection
def ad_delete_define_value(*args):
    selection = mc.ls(sl=1)
    if not selection:
        pass
    else:
        ad_delete_node(selection)
        # for object in selection:
        #     node = ad_reset_delete_query_attr(object)
        #     if node:
        #         for object_sel, node in zip (object, node):
        #             mc.delete(node)
        #             mc.deleteAttr('%s._adNet' % object_sel)
        #     else:
        #         pass

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
def ad_reset_attr_value(*args):
    selection = mc.ls(sl=1)
    if not selection:
        pass
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
    # selection = mc.ls(sl=1)
    # if not selection:
    #     pass
    # else:
    #     # check the attribute exists
    # items, source_connections =[],[]
    # for item in selection:
    # node_name = item + '_adNet'
    # source_connections=[]
    attr_node = mc.attributeQuery("_adNet", node=selection, exists=True)
    # check the connection exists
    if attr_node:
        # query the source node name
        node = mc.listConnections(selection + '._adNet', s=True)[0]
        return node

    else:
        om.MGlobal.displayInfo('There is no Define Attr Value exists to %s. Skipped the job!' % selection)
        # pass
        # om.MGlobal.displayWarning("Reset or delete %s is skipped! Please set the 'Define Attr Value' first!" % selection)
    # return selection, source_connections

# define attr value to marking menu
def ad_define_attr_value(*args):
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
        om.MGlobal.displayWarning('Please select at least one object to define!')

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
    # From here: http://forums.cgsociety.org/showthread.php?f=89&t=892246&highlight=main+channelbox
    channelBox = mel.eval('global string $gChannelBoxName; $temp=$gChannelBoxName;')  # fetch maya's main channelbox
    attrs = mc.channelBox(channelBox, q=1, sma=1)
    # attrs = mc.ls(attrs, l=True)
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
# else:
    for attr in ad_channel_attr():
        # get the value.
        get_value = mc.getAttr('%s.%s' % (selection, attr))
        # storing into dic
        dic[attr] = get_value
    return dic

# def exampleFunction(*args):
#     '''Example function to demonstrate how to pass functions to menuItems'''
#     print "example function"
#
#
# def rebuildMarkingMenu(*args):
#     '''This function assumes that this file has been imported in the userSetup.py
#     and all it does is reload the module and initialize the markingMenu class which
#     rebuilds our marking menu'''
#     mc.evalDeferred("""
# reload(markingMenu)
# markingMenu.markingMenu()
# """)
