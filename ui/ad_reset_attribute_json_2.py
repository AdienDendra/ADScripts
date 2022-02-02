import maya.cmds as mc
import maya.mel as mel
from functools import partial
import maya.OpenMaya as om
import os
import json
from collections import OrderedDict
from AL.breed.ui.services import sessionManager


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
        # mc.menuItem(p=menu, l="Delete All Default Attrs", rp="SE", c=partial(ad_delete_all_default_attrs))
        # mc.menuItem(p=menu, l="Delete Default Attr", rp="SW", c=partial(ad_delete_default_attr))
        mc.menuItem(p=menu, l="Set Default Attr", rp="W", c=partial(ad_set_default_attr))
        mc.menuItem(p=menu, l="Reset to Default", rp="E", c=partial(ad_reset_to_default))

markingMenu()


def ad_get_directory():
    dataPath = (
        sessionManager.SessionManager.instance()
            .activeManifest()
            .rigDirectory()
            .asFilepath()
    )
    directory = os.path.join(os.path.dirname(dataPath), "resources", "ctrlAttr")
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def ad_save_json_controller(file_name, object):
    # ordered dictionary
    attr_dict = OrderedDict()

    for obj in object:
        attr_dict[str(obj)] = ad_get_attr_value(obj)

    # # write the json file

    file_names = "%s" % (file_name)
    # print file_names
    if os.path.isfile(file_names):
        file = open(file_names, "r")
        load = json.load(file)
        load.update(attr_dict)
        file = open(file_names, "w")
        json.dump(load, file, indent=4)

    else:
    # if file_names:
        file = open(file_names, "w")
        json.dump(attr_dict, file, indent=4)



def ad_load_json_controller(file_name):
    file = open("%s" % (file_name))
    shape_dict = json.load(file)
    return shape_dict
    # for object in selection:
    #     # for (object_name, attribute) in shape_dict.items():
    #         # print object_name, object
    #         # for object in shape_dict.keys():
    #     for (objects, dictionary) in shape_dict.items():
    #         if object == objects:
    #             pass
    #             # if ad_channel_attr() == []:
    #             #         # print key, value
    #             #     for (key, value) in dictionary.items():
    #             #         mc.setAttr('%s.%s' % (object, key), value)
    #             #     # mc.setAttr('%s.%s' % (shape_dict, key), value)
    #             # else:
    #             #     for attr in ad_channel_attr():
    #             #         # print file_name
    #             #         # pass
    #             #         print attr
    #             #         print dictionary.get(attr)
    #                 # mc.setAttr('%s.%s' % (object, attr), dictionary.get(attr))
    #                 # mc.setAttr('%s.%s' % (shape_dict, attr), shape_dict.get(attr))
    #
    #         # else:
    #         #     om.MGlobal.displayWarning("Reset %s skipped! Please set the 'Define Attr Value' first!" % object)

# reset the value attr
def ad_reset_to_default(*args):

    # when the specific the attribute reset
    # for attr in ad_channel_attr():
    #     return attr
    ad_channel_attr()

    selection = mc.ls(sl=1)
    if not selection:
        om.MGlobal.displayWarning('Please select at least one object to Reset to Default!')
    else:
        import_object = os.path.join(ad_get_directory(), "resetAttr" + ".json")
        json_file = ad_load_json_controller(import_object)

        for object in selection:
            for (key, attribute) in json_file.items():
                if object == key:
                    for (attr, value) in attribute.items():
                        if ad_channel_attr() == []:
                            mc.setAttr('%s.%s' % (object, attr), value)

                        # when the specific the attribute reset
                        for attr in ad_channel_attr():
                            mc.setAttr('%s.%s' % (object, attr), attribute.get(attr))
                else:
                    pass


# set the default attribute from marking menu
def ad_set_default_attr(*args):
    selection = mc.ls(sl=1)
    if selection:
        export_object = os.path.join(ad_get_directory(), 'resetAttr' + ".json")
        objects = []
        for object in selection:
            try:
            # query the object selection whether it has shape
                object_type = mc.objectType(mc.listRelatives(object, s=1))
            except:
                pass
            else:
                if object_type == 'nurbsCurve' or mc.nodeType(object) == 'joint':
                    # for every node in selection
                    objects.append(object)

                    om.MGlobal.displayInfo("---------- Saved attribute value %s" % object)


                else:
                    om.MGlobal.displayInfo("Object '%s' is not nurbCurves or Joint. Skipped save!." % (object))

        om.MGlobal.displayInfo("********** File path: %s" % export_object)
        ad_save_json_controller(export_object, objects)

    else:
        om.MGlobal.displayWarning('Please select at least one object to Define Attr Value!')



# channel attr on the selection object
def ad_channel_attr():
    # get the currently selected attributes from the main channel box.
    channelBox = mel.eval('global string $gChannelBoxName; $temp=$gChannelBoxName;')  # fetch maya's main channelbox
    attrs = mc.channelBox(channelBox, q=1, sma=1)
    if not attrs:
        return []
    return attrs

# get attribute name and that value
def ad_get_attr_value(selection):
    # storing dictionary
    dic = {}

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
