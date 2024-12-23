"""
DESCRIPTION:

	The purpose of this tool is for resetting the attribute of your controller. You can use this tool for any commercial or non-commercial work.

USAGE:
    Drop the script into your Maya script directory :
    C:\Users\Your Name \Documents\maya\version\scripts

	There are two ways to run this script:
	 - Run this code below in Maya python script editor:
	 import ad_reset_attribute

	- Or you can drop that line into your userSetup.py in order to make it run automatically when the maya loads.

	This command is based on the marking menu, this stuff explains how to play this :
	- ALT + CONTROL + MIDDLE MOUSE BUTTON, I set this hotkey as default for showing the menu (you can change it if you don't like the hotkey).

	- SET DEFAULT ATTRIBUTE
	  You have to select at least one controller curve/joint. It will store all of the animatable attribute values of your selected object.

	- RESET TO DEFAULT
     You have to select the controller that you intended to reset the attribute. This is regarding the SET DEFAULT ATTRIBUTE values that you've stored. Also, you can select the spesific attribute for doing reset.

    You can see the demo version 1.0 >>
	https://youtu.be/0ymF2bgHfeI

	And here for version 2.0 >>
	https://youtu.be/uf6weAEbiZ0

AUTHOR:
    Adien Dendra

CONTACT:
    adprojects.animation@gmail.com | hello@adiendendra.com

VERSION:
    1.1 - Initial released - 28 January 2022
	1.2 - Fixing the delete all default attr function - 31 January 2022
	1.3 - Fixing the way get channel box  - 03 February 2022
	2.0 - Changing the system work into database JSON file - 24 March 2022

LICENSE:
    Free license

ADDITIONAL NOTES:

	If you think this is useful and would like to support me to continue developing the upcoming rigging stuff, feel free to buy me a coffe to my paypal >> https://paypal.me/adiendendra :)
	Have fun with the tool!

"""

import json
import os
from collections import OrderedDict
from functools import partial

import maya.OpenMaya as om
import maya.cmds as cmds

MENU_NAME = "markingMenu"


class markingMenu():

    def __init__(self):
        self.removeOld()
        self.build()

    def build(self):
        cmds.popupMenu(MENU_NAME, mm=1, b=2, aob=1, ctl=1, alt=1, sh=0, p="viewPanes", pmo=1, pmc=self.buildMarkingMenu)

    def removeOld(self):
        if cmds.popupMenu(MENU_NAME, ex=1):
            cmds.deleteUI(MENU_NAME)

    def buildMarkingMenu(self, menu, parent):
        # Radial positioned
        cmds.menuItem(p=menu, l="Set Attr as Default", rp="W", c=partial(set_default_attr))
        cmds.menuItem(p=menu, l="Reset to Default", rp="E", c=partial(reset_to_default))


markingMenu()


def get_directory_path(folder):
    file_path = cmds.file(q=True, sn=True)
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

    # for obj in object:
    attr_dict[str(object)] = get_attr_value(object)
    # condition json file exist
    file_names = "%s" % (file_name)
    if os.path.isfile(file_names):
        file = open(file_names, "r")
        load = json.load(file)
        load.update(attr_dict)
        file = open(file_names, "w")
        json.dump(load, file, indent=1)
    # condition json not exist
    else:
        file = open(file_names, "w")
        json.dump(attr_dict, file, indent=1)


def load_json_file(file_name):
    file = open("%s" % (file_name))
    shape_dict = json.load(file)
    return shape_dict


# reset the value attr
def reset_to_default(*args):
    selection = cmds.ls(sl=1)
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
                                cmds.setAttr('%s.%s' % (object, attr), value)

                        # when the specific the attribute reset
                        for attr in query_channel_attr(object):
                            cmds.setAttr('%s.%s' % (object, attr), attribute.get(attr))

        else:
            om.MGlobal_displayError("There is no file '%s.json' in the directory" % directory[1])


# set the default attribute from marking menu
def set_default_attr(*args):
    selection = cmds.ls(sl=1)
    if selection:
        directory = get_directory_path("ad_resetAttr")
        export_object = os.path.join(directory[0], directory[1] + ".json")
        objects = []
        for object in selection:
            if cmds.listAnimatable(object):
                try:
                    # query the object selection whether it has shape
                    object_type = cmds.objectType(cmds.listRelatives(object, s=True))
                except:
                    pass
                else:
                    if object_type == 'nurbsCurve' or cmds.nodeType(object) == 'joint':
                        # for every node in selection
                        objects.append(object)

                        # saving to json file
                        save_json_file(export_object, object)
                        om.MGlobal.displayInfo("---------- Saved attribute value %s" % object)

                    else:
                        om.MGlobal.displayInfo("Object '%s' is not nurbCurves or Joint. Skipped save!." % (object))

            else:
                om.MGlobal.displayInfo('Skipped object %s due to not animatable!' % object)

        if objects:
            om.MGlobal.displayInfo("********** File path: %s" % export_object)

    else:
        om.MGlobal.displayInfo('Select at least one animatable object!')


# channel attr on the selection object
def query_channel_attr(selection):
    # query main channel box
    gChannelBoxName = 'mainChannelBox'
    sma = cmds.channelBox(gChannelBoxName, q=True, sma=True)
    sha = cmds.channelBox(gChannelBoxName, q=True, sha=True)

    attrs = list()
    if sma:
        attrs.extend(sma)

    if sha:
        attrs.extend(sha)

    if not attrs:
        return []

    longNames = []

    result = [cmds.attributeQuery(a, n=selection, ln=1) for a in attrs]
    longNames = longNames + result
    longNames = list(set(longNames))

    return longNames


# get attribute name and that value
def get_attr_value(selection):
    # storing dictionary
    # get all animatable attribute in the scene of the selection object
    dic = {}
    for attr in cmds.listAttr(selection, k=True):
        # get the value.
        get_value = cmds.getAttr('%s.%s' % (selection, attr))
        # storing into dic
        dic[attr] = get_value
    return dic
