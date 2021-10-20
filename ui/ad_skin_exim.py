from functools import partial
import json
import re
from collections import OrderedDict
from string import digits
import os

import maya.OpenMaya as om
import pymel.core as pm
import maya.mel as mm
import maya.cmds as cmds


layout = 350
percentage = 0.01 * layout
on_selector = 0
method_radio_button =1

def ad_show_ui():
    adien_skin = 'AD_ExportImportSkin_Tool'
    pm.window(adien_skin, exists=True)
    if pm.window(adien_skin, exists=True):
        pm.deleteUI(adien_skin)
    with pm.window(adien_skin, title='AD Export/Import Skin Tool', width=350, height=80):
        # CREATE TAB
        with pm.columnLayout('Exim Tool', rowSpacing=1 * percentage, w=layout,
                             co=('both', 1 * percentage)):
            pm.separator(h=5, st="in", w=layout)
            with pm.rowLayout(nc=1):
                pm.textFieldButtonGrp('Path', label='Path:', cal=(1, "right"),
                                      cw3=(10 * percentage, 70 * percentage, 10 * percentage),
                                      cat=[(1, 'right', 2), (2, 'both', 2), (3, 'left', 2)],
                                      bl="Get Path",
                                      bc=partial(ad_get_path_button))

            # ad_defining_object_text_field(define_object='Static_Joint', label="Static Joint:")
            with pm.rowLayout(nc=3, cw3=(10 * percentage, 43.5 * percentage, 43.5 * percentage),
                                  cat=[(1, 'right', 2), (2, 'both', 1), (3, 'both', 1)]):
                pm.text(l='')
                pm.button('export_skin_weight', l="Export Skin Weight", bgc=(1, 1, 0),
                          c=partial(ad_export_skin_button))

                # create button to delete last pair of text fields
                pm.button("import_skin_weight", l="Import Skin Weight", bgc=(0, 0.5, 0),
                          c=''
                          )
            pm.separator(h=10, st="in", w=layout)
            with pm.rowLayout(nc=2, cw2=(49 * percentage, 49 * percentage), cl2=('center', 'center'),
                              columnAttach=[(1, 'both', 2 * percentage), (2, 'both', 2 * percentage)]):
                pm.text(l='Adien Dendra | 11/2020', al='left')
                pm.text(
                    l='<a href="https://youtu.be/IqMGcvEzJCk">find out how to use it! >> </a>',
                    hl=True,
                    al='right')
    pm.showWindow()

def ad_get_path_button(*args):
    set = pm.fileDialog2(fileMode=2, dialogStyle=2, okc='Set',fileFilter='*.json',
                          cap='Set The Path')
    if set:
        pm.textFieldButtonGrp('Path', e=True, tx=set[0])
    else:
        pass

    return set

def ad_export_skin_button(*args):
    selection = pm.ls(sl=1)
    object_path = pm.textFieldButtonGrp('Path', q=True, tx=True)
    if object_path :
        if selection:
            for item in selection:
                get_shape = item.getShape()
                if get_shape:
                    node_type =  pm.nodeType(get_shape)
                    if node_type == 'mesh' or node_type == 'nurbsSurface':
                        ad_export_skin_selected(item)
                    else:
                        om.MGlobal_displayWarning('The object type is not mesh. Skip object to export!')
                else:
                    pass
            pm.confirmDialog(title='Progress', message='Exporting weight has done.')

        else:
            om.MGlobal_displayError('Select the minimum one object mesh or nurbsSurface which has a skin weight!')
    else:
        om.MGlobal_displayError('Set the path first!')


def ad_export_skin_selected(item):
    path = pm.textFieldButtonGrp('Path', q=True, tx=True)
    # Export skin weight values into selected geometries
    suffix = 'SkinWeight'
    # Check whether the specified path exists or not

    directory_sel = '%s/%s' % (path, item)
    directory_exists = os.path.exists(directory_sel)

    if not directory_exists:
        # Create a new directory because it does not exist
        os.mkdir('%s/%s' % (path, item))
        directory = directory_sel
    else:
        directory = directory_sel

    # file_path = '%s/%s%s.json' % (directory, item, suffix)

    file_path = ad_increment_file(directory, item, suffix)

    ad_export_skin(item, file_path[0])

    # for file in sorted(current_file_exists):
    if file_path[1] > 11:
        os.remove('%s/%s' % (directory, (file_path[0][2])))

    # if len(numb) > 10:
    #     print
    # os.remove('%s/%s.%s.%03d.json' % (directory_path, object_name, suffix, new_num))
    # print num_list[2]
    else:
        pass


def ad_increment_file(directory_path, object_name, suffix):
    """
    increment the version update skin weight and deleting the older one
    """
    current_file_exists = os.listdir(directory_path)
    # prefix = 'SkinWeight'
    current_file_exists = filter(lambda x: '.json' in x, current_file_exists)
    num_list = [0]
    for file in current_file_exists:
        i = os.path.splitext(file)[0]
        try:
            num = re.findall('[0-9]+$', i)[0]
            num_list.append(int(num))
        except IndexError:
            pass
    num_list = sorted(num_list)
    print num_list
    new_num = num_list[-1] + 1
    total_file = len(num_list)

    save_name = '%s/%s.%s.%03d.json' % (directory_path, object_name, suffix, new_num)

    print "Saving %s" % save_name
    return save_name, total_file, current_file_exists

def ad_export_skin(item, path):
    skin = mm.eval('findRelatedSkinCluster( "%s" )' % item)
    if skin:
        print(path)
        method = cmds.getAttr('%s.skinningMethod' % skin)
        components = cmds.getAttr('%s.useComponents' % skin)
        influence = cmds.skinCluster(skin, q=True, inf=True)
        skin_set = cmds.listConnections('%s.message' % skin, d=True, s=False)[0]

        # fid = open(fn, 'w')
        weight_dict = {}

        # shape_dict[str(item)] = {'influences': influence, 'name': skin, 'set': skin_set, 'skinningMethod': method,
        #                                 'useComponents': components}
        weight_dict['influences'] = influence
        weight_dict['name'] = skin
        weight_dict['set'] = skin_set
        weight_dict['skinningMethod'] = method
        weight_dict['useComponents'] = components

        for range in xrange(pm.polyEvaluate(item, v=True)):
            current_vertex = '%s.vtx[%d]' % (item, range)
            skin_value = pm.skinPercent(skin, current_vertex, q=True, v=True)
            weight_dict[range] = skin_value

        # write the json file

        file = open("%s" % (path), "w")
        json.dump(weight_dict, file, indent=4)

    else:
        print('%s has no related skinCluster node.' % item)




def ad_exporting_skin_selected(item):
    path = 'C:\Users\Raizel Dendra\Documents\maya\projects\default\scenes'
    # Export skin weight values into selected geometries
    suffix = 'Weight'
    # Check whether the specified path exists or not

    file_path = '%s/%s%s' % (path, item, suffix)
    return file_path

    # ad_export_skin(item, file_path)


    # # all item shape in the list
    # for item in list:
    #     # get transform name
    #     item_parent = item.getParent()
    #
    #     # get cv number, x value, y value, z value and color on each item
    #     cvs, xvalue, yvalue, zvalue, color = [], [], [], [], []
    #     for cv in pm.PyNode(item).cv:
    #         # for cv in object_curve.getShape().cv:
    #         x = pm.getAttr(str(cv) + '.xValue')
    #         y = pm.getAttr(str(cv) + '.yValue')
    #         z = pm.getAttr(str(cv) + '.zValue')
    #         xvalue.append(x)
    #         yvalue.append(y)
    #         zvalue.append(z)
    #
    #         # get the number cv
    #         cv = cv.split('.')[-1]
    #         cvs.append(cv)
    #
    #     if pm.getAttr('%s.overrideEnabled' % item):
    #         color_number = pm.getAttr('%s.overrideColor' % item)
    #         color.append(color_number)
    #     shape_dict[str(item_parent)] = {'cv': cvs, 'xValue': xvalue, 'yValue': yvalue, 'zValue': zvalue,
    #                                     'overrideColor': color}
    #
    #     om.MGlobal.displayInfo("Object '%s' is saved!." % (item.getParent()))
    #
    # om.MGlobal.displayInfo("---------------- File path saved: '%s'" % file_name)
    #
    # # write the json file
    # file = open("%s" % (file_name), "w")
    # json.dump(shape_dict, file, indent=4)




