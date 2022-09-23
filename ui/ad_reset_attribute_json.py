import json
import os
from collections import OrderedDict
from functools import partial

import maya.OpenMaya as om
import maya.cmds as mc

MENU_NAME = "markingMenu"


class ResetAttrMarkingMenu():

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
        mc.menuItem(p=menu, l="Set Attr as Default", rp="W", c=partial(set_default_attr))
        mc.menuItem(p=menu, l="Reset to Default", rp="E", c=partial(reset_to_default))


ResetAttrMarkingMenu()


def get_directory_path(folder):
    file_path = mc.file(q=True, sn=True)
    if file_path:
        path = os.path.dirname(file_path)
        file_name = os.path.basename(file_path)
        raw_name, extension = os.path.splitext(file_name)
        extension = extension.split('.')
        directory = os.path.join(path, folder)
        raw_extension = raw_name + '_' + extension[1]
        if not os.path.exists(directory):
            os.makedirs(directory)
        return directory, raw_extension

    else:
        om.MGlobal_displayError('Save the file first before set the attribute!')


def save_json_file(file_name, object):
    # ordered dictionary
    attr_dict = OrderedDict()

    for obj in object:
        attr_dict[str(obj)] = get_attr_value(obj)
        # condition json file exist
        file_names = "%s" % (file_name)
        if os.path.isfile(file_names):
            file = open(file_names, "r")
            load = json.load(file)
            load.update(attr_dict)
            file = open(file_names, "w")
            json.dump(load, file, indent=4)
        # condition json not exist
        else:
            file = open(file_names, "w")
            json.dump(attr_dict, file, indent=4)


def load_json_file(file_name):
    file = open("%s" % (file_name))
    shape_dict = json.load(file)
    return shape_dict


# reset the value attr
def reset_to_default(*args):
    selection = mc.ls(sl=1)
    if not selection:
        om.MGlobal.displayWarning('Please select at least one object to Reset to Default!')
    else:
        directory = get_directory_path("ad_resetAttr")
        import_object = os.path.join(directory[0], directory[1] + '.json')
        if os.path.exists(import_object):
            json_file = load_json_file(import_object)
            for object in selection:
                for (key, attribute) in json_file.items():
                    if object == key:
                        if query_channel_attr(object) == []:
                            for (attr, value) in attribute.items():
                                mc.setAttr('%s.%s' % (object, attr), value)

                        # when the specific the attribute reset
                        for attr in query_channel_attr(object):
                            mc.setAttr('%s.%s' % (object, attr), attribute.get(attr))

        else:
            om.MGlobal_displayError("There is no file '%s.json' in the directory" % directory[1])


# set the default attribute from marking menu
def set_default_attr(*args):
    selection = mc.ls(sl=1)
    if selection:
        directory = get_directory_path("ad_resetAttr")
        export_object = os.path.join(directory[0], directory[1] + ".json")
        objects = []
        for object in selection:
            if mc.listAnimatable(object):
                try:
                    # query the object selection whether it has shape
                    object_type = mc.objectType(mc.listRelatives(object, s=True))
                except:
                    pass
                else:
                    if object_type == 'nurbsCurve' or mc.nodeType(object) == 'joint':
                        # for every node in selection
                        objects.append(object)

                        om.MGlobal.displayInfo("---------- Saved attribute value %s" % object)

                    else:
                        om.MGlobal.displayInfo("Object '%s' is not nurbCurves or Joint. Skipped save!." % (object))

                save_json_file(export_object, objects)

            else:
                om.MGlobal.displayInfo('Skipped object %s due to not animatable!' % object)

        if objects:
            om.MGlobal.displayInfo("********** File path: %s" % export_object)
        else:
            pass

    else:
        om.MGlobal.displayInfo('Skipped object %s due to not animatable!' % selection)


# channel attr on the selection object
def query_channel_attr(selection):
    # query main channel box
    gChannelBoxName = 'mainChannelBox'
    sma = mc.channelBox(gChannelBoxName, q=True, sma=True)
    sha = mc.channelBox(gChannelBoxName, q=True, sha=True)

    attrs = list()
    if sma:
        attrs.extend(sma)

    if sha:
        attrs.extend(sha)

    if not attrs:
        return []

    longNames = []

    result = [mc.attributeQuery(a, n=selection, ln=1) for a in attrs]
    longNames = longNames + result
    longNames = list(set(longNames))

    return longNames


# get attribute name and that value
def get_attr_value(selection):
    # storing dictionary
    # get all animatable attribute in the scene of the selection object
    dic = {}
    for attr in mc.listAnimatable(selection):
        # Sort out the actual name of just the attribute.
        attr = mc.ls(attr)[0]
        attr = attr.partition('.')[2]
        # get the value.
        get_value = mc.getAttr('%s.%s' % (selection, attr))
        # storing into dic
        dic[attr] = get_value
    return dic
