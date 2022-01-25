import maya.cmds as mc
import maya.mel as mel

from collections import OrderedDict

MENU_NAME = "markingMenu"

class markingMenu():

    def __init__(self):

        self._removeOld()
        self._build()

    def _build(self):
        menu = mc.popupMenu(MENU_NAME, mm=1, b=2, aob=1, ctl=1, alt=1, sh=0, p="viewPanes", pmo=1, pmc=self._buildMarkingMenu)

    def _removeOld(self):
        if mc.popupMenu(MENU_NAME, ex=1):
            mc.deleteUI(MENU_NAME)

    def _buildMarkingMenu(self, menu, parent):

        # Radial positioned
        mc.menuItem(p=menu, l="Delete All Value", rp="SW", c="print 'SouthWest'")
        mc.menuItem(p=menu, l="Delete Value", rp="NW", c="mc.circle()")
        mc.menuItem(p=menu, l="Reset Value", rp="SE", c=exampleFunction)
        mc.menuItem(p=menu, l="Assign Value", rp="NE", c="mc.circle()")

        # subMenu = mc.menuItem(p=menu, l="North Sub Menu", rp="N", subMenu=1)
        # mc.menuItem(p=subMenu, l="North Sub Menu Item 1")
        # mc.menuItem(p=subMenu, l="North Sub Menu Item 2")
        #
        # mc.menuItem(p=menu, l="South", rp="S", c="print 'South'")
        # mc.menuItem(p=menu, ob=1, c="print 'South with Options'")
        #
        # # List
        # mc.menuItem(p=menu, l="First menu item")
        # mc.menuItem(p=menu, l="Second menu item")
        # mc.menuItem(p=menu, l="Third menu item")
        # mc.menuItem(p=menu, l="Create poly cube", c="mc.polyCube()")
        #
        # # Rebuild
        # mc.menuItem(p=menu, l="Rebuild Marking Menu", c=rebuildMarkingMenu)

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



def ad_network_node():
    # For every node in selection #
    sel = mc.ls(selection=1)
    for item in sel:
        key_value_message = ad_get_attr_value(item)

        for (key, value) in key_value_message.items():
            if mc.objExists(item+'_net'):
                pass
            else:
                # create node
                network_node = mc.createNode('network', n=item+'_net')
                mc.connectAttr(network_node+'.message', item+'.AD_network')

            # get the value and attr
            add_attr = ad_add_attr_node(item+'_net', attribute_name=key, attribute_type='double')
            if add_attr:
                mc.setAttr(item+'_net'+'.'+add_attr, value)


        # # set value
        # ad_add_message_node(item, attribute_name=, attribute_type):
        # mc.addAttr(item, )
        #

# def ad_attr_query(node, attribute_name):
#     query_attr = mc.attributeQuery(attribute_name, node= node, exists=True)
#     if query_attr:
#         return attribute_name
#     else:
#         return
#
def ad_add_attr_node(node, attribute_name, attribute_type):
    query_attr = mc.attributeQuery(attribute_name, node=node, exists=True)
    if query_attr:
        pass
    else:
        mc.addAttr(node, ln=attribute_name, at=attribute_type)
    # return query_attr

def ad_channel_attr():
    # Get the currently selected attributes from the main channelbox.
    # From here: http://forums.cgsociety.org/showthread.php?f=89&t=892246&highlight=main+channelbox
    channelBox = mel.eval('global string $gChannelBoxName; $temp=$gChannelBoxName;')  # fetch maya's main channelbox
    attrs = mc.channelBox(channelBox, q=1, sma=1)
    # attrs = mc.ls(attrs, l=True)
    if not attrs:
        return []
    return attrs

def ad_get_attr_value(selection):
    # storing dictionary
    dic ={}

    # for node in selection:
    ad_add_attr_node(selection, attribute_name='AD_network', attribute_type='message')

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
