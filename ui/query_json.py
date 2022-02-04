import maya.cmds as mc
import urlparse
import os
import json
from urlparse import urlparse

def query_data():
    import_object =os.path.join("D:/", "bindPose.json")
    file = open("%s" % (import_object))
    shape_dict = json.load(file)
    # for (key, value) in shape_dict.items():
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
            # print object_name
            # print value

            new_dic[object_name] =value

    return new_dic
def selection_object():
    selection = [u'dwayne_santa01_base_rig:spine_M_pelvis_ctrl',
                 u'dwayne_santa01_base_rig:spine_M_chest_ctrl', u'dwayne_santa01_base_rig:spine_M_mid_ctrl',
                 u'dwayne_santa01_base_rig:godnode_M_body_ctrl',
                 u'dwayne_santa01_base_rig:spine_M_hip_ctrl', u'dwayne_santa01_base_rig:leg_L_thighFK_ctrl',
                 u'dwayne_santa01_base_rig:arm_L_elbowFK_ctrl', u'dwayne_santa01_base_rig:arm_L_shoulderFK_ctrl']
    data = query_data()
    # print data
    # new_data = {item.split(':')[1]:data.get(item.split(':')[1]) for item.split(':')[1] in selection}

    for item in selection:
        object_name = item.split(':')[1]
        # print split_naming
        new_data = data.get(str(object_name))
        for (key, value) in new_data.items():
            print value[0]
            # mc.setAttr('%s.%s'% (object_name,key), value)

    # a = {"a":1,"b":2,"c":3,"f":4,"d":5}
    # b= ["b","c"]
    #
    # out = {item:a.get(item)for item in b}

        # if split_naming in data.keys():
        #     print True

        # print data
        # print data.keys()
        # if item in data.keys()

            # for (attr, attr_value) in value.items():
            #     print attr, attr_value[0]

            # print os.path.split(split_path[0])[0]
            # for item in split_path[0]:
            #     print item.split('#')

def ad_changing_indent():
    import_object =os.path.join("D:/", "bindPose.json")
    file = open(import_object, "r")
    load = json.load(file)
    file = open(import_object, "w")
    json.dump(load, file, indent=4)