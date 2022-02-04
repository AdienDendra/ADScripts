import maya.cmds as mc
from functools import partial
import maya.OpenMaya as om
import os
import json
from urlparse import urlparse
from collections import OrderedDict
from AL.breed.ui.services import sessionManager

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
        mc.menuItem(p=menu, l="Set Attr as Default", rp="W", c=partial(ad_set_default_attr))
        mc.menuItem(p=menu, l="Reset to Default", rp="NE", c=partial(ad_reset_to_default))
        mc.menuItem(p=menu, l="Reset to Bindpose", rp="SE", c=partial(ad_reset_to_bindpose))


markingMenu()

def query_data_bindPose():
    import_object = os.path.join(ad_get_directory("motion", ""), "bindPose" + ".json")
    file = open("%s" % (import_object))
    shape_dict = json.load(file)

    data = shape_dict['data']
    internal = data['internal']
    new_dic ={}
    for item_value in internal.values():
        # print key, value
        values = item_value['values']
        # print values
        for (key, value) in values.items():
            parsed = urlparse(key)
            fragment = parsed.fragment
            split_path = os.path.split(fragment)

            main_object = split_path[0].split('#')
            replacing = main_object[1].replace('/control', '_')

            if 'L/' in replacing:
                split = replacing.split('/')
                object =  split[0]+'_'

            elif 'R/' in replacing:
                split = replacing.split('/')
                object =  split[0] + '_'
            else:
                object = replacing

            second_object = split_path[1].split('@')[0]

            object_name = object+second_object


            new_dic[object_name] =value
    # print new_dic
    return new_dic

def ad_reset_to_bindpose(*args):
    selection = mc.ls(sl=1)
    data = query_data_bindPose()
    # print data
    # new_data = {item.split(':')[1]:data.get(item.split(':')[1]) for item.split(':')[1] in selection}

    for item in selection:
        object_name = item.split(':')[1]
        # print split_naming
        new_data = data.get(str(object_name))
        if ad_channel_attr(item) == []:
            for (key, value) in new_data.items():
                if mc.getAttr('%s.%s' % (item, key), l=True):
                    pass
                else:
                    if key == 'rotateX' or key == 'rotateY' or key =='rotateZ':
                        mc.setAttr('%s.%s' % (item, key), value[0]*57.2958)
                    else:
                        mc.setAttr('%s.%s' % (item, key), value[0])

        # # when the specific the attribute reset
        # print ad_channel_attr()
        # print key
        for attr in ad_channel_attr(item):
            # print new_data
            # print attr
            # print key.get(str(attr))
            # print new_data.get(attr)
            # print new_data.get(attr)
            if attr == 'rotateX' or attr == 'rotateY' or attr == 'rotateZ':
                mc.setAttr('%s.%s' % (item, attr), (new_data.get(attr)[0]*57.2958))
            else:
                mc.setAttr('%s.%s' % (item, attr), new_data.get(attr)[0])



def ad_get_directory(folder, subfolder=''):
    dataPath = (
        sessionManager.SessionManager.instance()
            .activeManifest()
            .rigDirectory()
            .asFilepath()
    )
    directory = os.path.join(os.path.dirname(dataPath), folder, subfolder)
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def ad_save_json_controller(file_name, object):
    # ordered dictionary
    attr_dict = OrderedDict()

    for obj in object:
        # if mc.listAnimatable(obj):
            # print obj
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
        # else:
        #     om.MGlobal.displayInfo('Skipped object %s due to not animatable!' % obj)


def ad_load_json_controller(file_name):
    file = open("%s" % (file_name))
    shape_dict = json.load(file)
    return shape_dict

# reset the value attr
def ad_reset_to_default(*args):

    # ad_channel_attr()

    selection = mc.ls(sl=1)
    if not selection:
        om.MGlobal.displayWarning('Please select at least one object to Reset to Default!')
    else:
        import_object = os.path.join(ad_get_directory("resources", "ctrlAttr"), "resetAttr" + ".json")
        json_file = ad_load_json_controller(import_object)

        for object in selection:
            for (key, attribute) in json_file.items():
                if object == key:
                    if ad_channel_attr(object) == []:
                        for (attr, value) in attribute.items():
                            mc.setAttr('%s.%s' % (object, attr), value)

                    # when the specific the attribute reset
                    for attr in ad_channel_attr(object):
                        mc.setAttr('%s.%s' % (object, attr), attribute.get(attr))

# set the default attribute from marking menu
def ad_set_default_attr(*args):
    selection = mc.ls(sl=1)
    # if mc.listAnimatable(selection):
    if selection:
        export_object = os.path.join(ad_get_directory("resources", "ctrlAttr"), 'resetAttr' + ".json")
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

                ad_save_json_controller(export_object, objects)

            else:
                om.MGlobal.displayInfo('Skipped object %s due to not animatable!' % object)

        if objects:
            om.MGlobal.displayInfo("********** File path: %s" % export_object)
        else:
            pass
        # else:
        #     om.MGlobal.displayWarning('Please select at least one object to Define Attr Value!')
    else:
        om.MGlobal.displayInfo('Skipped object %s due to not animatable!' % selection)




# channel attr on the selection object
def ad_channel_attr(selection):
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
        return  []

    longNames = []

    result = [mc.attributeQuery(a, n=selection, ln=1) for a in attrs]
    longNames = longNames + result
    # print longNames
    longNames = list(set(longNames))


    return longNames

    # ssa = mc.channelBox(gChannelBoxName, q=True, ssa=True)
    # if ssa:
    #     attrs.extend(ssa)

    # getSelectedChannels()
    # channelBox = mel.eval('global string $gChannelBoxName; $temp=$gChannelBoxName;')  # fetch maya's main channelbox
    # attrs = mc.channelBox(channelBox, q=1, sma=1)
    # if not attrs:
    #     return []
    # return attrs

# get attribute name and that value
def ad_get_attr_value(selection):
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


