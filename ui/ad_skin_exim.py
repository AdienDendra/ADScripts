from functools import partial
import re
from collections import OrderedDict
from string import digits
import os
import json


import maya.OpenMaya as om
import pymel.core as pm
import maya.mel as mm
import maya.cmds as cmds


layout = 400
percentage = 0.01 * layout
suffix = 'SkinWeight'

def ad_show_ui():
    adien_skin = 'AD_Skin_Tool'
    pm.window(adien_skin, exists=True)
    if pm.window(adien_skin, exists=True):
        pm.deleteUI(adien_skin)
    with pm.window(adien_skin, title='AD Skin Tool', width=400, height=80):
        with pm.columnLayout('Exim Tool', rowSpacing=1 * percentage, w=layout,
                             co=('both', 1 * percentage)):
            pm.separator(h=5, st="in", w=layout)
            with pm.rowLayout(nc=1):
                pm.textFieldButtonGrp('Path', label='Path:', cal=(1, "right"),
                                      cw3=(12 * percentage, 67 * percentage, 17 * percentage),
                                      cat=[(1, 'right', 2), (2, 'both', 1), (3, 'both', 1)],
                                      bl="Get Path",
                                      bc=partial(ad_get_path_button))

            with pm.rowLayout(nc=4, cw4=(12 * percentage, 33 * percentage, 33 * percentage, 18 * percentage) ,
                                  cat=[(1, 'right', 2), (2, 'both', 2), (3, 'both', 2), (4, 'both', 1)]):
                pm.text(l='')
                pm.button('export_skin_weight', l="Export Skin Weight", bgc=(1, 1, 0),
                          c=partial(ad_export_skin_button))

                pm.button("import_skin_weight", l="Import Skin Weight", bgc=(0, 0.5, 0),
                          c=partial(ad_import_skin_button)
                          )

                pm.button("transfer_skin_weight", l="Transfer", c=partial(ad_transfer_button)
                          )
            with pm.rowLayout(nc=2, cw2=(12 * percentage, 67 * percentage, ),
                              cat=[(1, 'right', 2), (2, 'both', 2)]):
                pm.text(l='Progress:')
                pm.progressBar('Progress_Bar', maxValue=100)

            pm.separator(h=1, st="out", w=layout)
            with pm.rowLayout(nc=2, cw2=(34 * percentage, 63* percentage),
                              cl2=('right', 'right'),
                              cat=[(1, 'right', 4 * percentage), (2, 'both', 1 * percentage)]
                              ):
                pm.text(
                    l='<a href="https://adiendendra.gumroad.com/">Adien Dendra</a> | 11/2021',
                    hl=True,
                    al='right')

                pm.text('Object_progress', l='')

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
                        ad_create_directories_export(item)
                    else:
                        om.MGlobal_displayWarning('The object type is not mesh. Skip object to export!')
                else:
                    pass
            pm.progressBar('Progress_Bar', e=True, progress=100)
            pm.confirmDialog(title='Progress', message='Exporting weight has done.')
            pm.progressBar('Progress_Bar', e=True, endProgress=True)
            pm.text('Object_progress', e=True, l='')

        else:
            om.MGlobal_displayError('Select the minimum one object mesh or nurbsSurface which has a skin weight!')
    else:
        om.MGlobal_displayError('Set the path first!')

def ad_import_skin_button(*args):
    selection = pm.ls(sl=1)
    object_path = pm.textFieldButtonGrp('Path', q=True, tx=True)
    if object_path :
        if selection:
            for item in selection:
                get_shape = item.getShape()
                if get_shape:
                    node_type =  pm.nodeType(get_shape)
                    if node_type == 'mesh' or node_type == 'nurbsSurface':
                        ad_read_increment_file_import(item)
                    else:
                        om.MGlobal_displayWarning('The object type is not mesh. Skip object to export!')
                else:
                    pass
            pm.progressBar('Progress_Bar', e=True, progress=100)
            pm.confirmDialog(title='Progress', message='Importing weight has done.')
            pm.progressBar('Progress_Bar', e=True, endProgress=True)
            pm.text('Object_progress', e=True, l='')

        else:
            om.MGlobal_displayError('Select the minimum one object mesh or nurbsSurface which has a skin weight!')
    else:
        om.MGlobal_displayError('Set the path first!')

def ad_transfer_button(*args):
    om.MGlobal.displayInfo('will be released soon!')

# EXPORT

def ad_create_directories_export(item):
    name = item.nodeName()
    object = pm.ls(name)

    if len(object) > 1:
        om.MGlobal.displayWarning('Skin weight %s skipped! Due to duplicate object name' % item)
    else:
        path = pm.textFieldButtonGrp('Path', q=True, tx=True)

        # Check whether the specified path exists or not
        directory_sel = '%s/%s' % (path, item)
        directory_exists = os.path.exists(directory_sel)

        if not directory_exists:
            # Create a new directory because it does not exist
            os.mkdir('%s/%s' % (path, item))
            directory = directory_sel
        else:
            directory = directory_sel

        file_path = ad_increment_data_file(directory, item, suffix, create=True)

        if file_path['total file'] > 10:
            os.remove('%s/%s' % (directory, (file_path['current file exists'][0])))
        else:
            pass

        ad_data_skin_weight_export(item, file_path['file name'])

def ad_increment_data_file(directory_path, object_name, suffix, create):
    """
    increment the version update skin weight and deleting the older one
    """
    save_name, total_file, current_file_exists, get_file_path = [],[],[],[]
    # for export
    if create :
        current_file_exists = os.listdir(directory_path)
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
        new_num = num_list[-1] + 1
        total_file = len(num_list)

        save_name = '%s/%s.%s.%03d.json' % (directory_path, object_name, suffix, new_num)
        pm.text('Object_progress', e=True, l="Export '%s' skin weight" % (object_name))
        om.MGlobal.displayInfo('Export skin weight %s as %s.%s.%03d.json file' % (object_name, object_name, suffix, new_num))

    # for import file
    else:
        get_file_path = sorted(os.listdir('%s/%s' % (directory_path, object_name)))

    return {'file name' : save_name,
            'total file': total_file,
            'current file exists' : current_file_exists,
            'get file path': get_file_path}

def ad_data_skin_weight_export(item, path):
    skin = mm.eval('findRelatedSkinCluster( "%s" )' % item)
    if skin:
        method = cmds.getAttr('%s.skinningMethod' % skin)
        components = cmds.getAttr('%s.useComponents' % skin)
        influence = cmds.skinCluster(skin, q=True, inf=True)
        skin_set = cmds.listConnections('%s.message' % skin, d=True, s=False)[0]

        weight_dict = OrderedDict()
        weight_dict['influences'] = influence
        weight_dict['name'] = skin
        weight_dict['set'] = skin_set
        weight_dict['skinningMethod'] = method
        weight_dict['useComponents'] = components
        vertices = pm.polyEvaluate(item, v=True)
        for range in xrange(vertices):
            current_vertex = '%s.vtx[%d]' % (item, range)
            skin_value = pm.skinPercent(skin, current_vertex, q=True, v=True)
            # value_with_object = zip(influence, skin_value)
            weight_dict[range] = skin_value
            progress = 100.0 / vertices * (range)
            pm.progressBar('Progress_Bar', e=True, progress=progress)


        file = open("%s" % (path), "w")
        json.dump(weight_dict, file, indent=1)

    else:
        om.MGlobal.displayWarning('%s has no related skinCluster node.' % item)


# IMPORT
def ad_read_increment_file_import(item):
    path = pm.textFieldButtonGrp('Path', q=True, tx=True)

    # Check whether the specified path exists or not
    directory_sel = '%s/%s' % (path, item)
    directory_exists = os.path.exists(directory_sel)
    om.MGlobal.displayInfo('Import skin weight from %s' % os.listdir(directory_sel)[0])

    if not directory_exists:
        # Create a new directory because it does not exist
        om.MGlobal.displayWarning("Please check your object selection name. It doesn't match with directories exported!")
    else:
        if not os.listdir(directory_sel):
            om.MGlobal.displayWarning("There is no skin %s exported. Import skipped!" % item)
        else:
            file_path = ad_increment_data_file(path, item, suffix, create=False)

            ad_data_skin_weight_import(file_path['get file path'][-1], path, item)


def ad_data_skin_weight_import(item_version, path, object_name):
    print('Loading %s...' % object_name)
    pm.text('Object_progress', e=True, l="Import '%s' skin weight" % (object_name))

    file = open("%s/%s/%s" % (path, object_name, item_version))
    weight_dict = json.load(file)

    influences = weight_dict['influences']

    for influence in influences:
        if not pm.objExists(influence):
            om.MGlobal.displayWarning('Scene has no %s ' % influence)
    related_skin = mm.eval('findRelatedSkinCluster "%s"' % object_name)
    if related_skin:
        pm.skinCluster(related_skin, e=True, ub=True)

    create_skin = pm.skinCluster(influences[0], object_name, tsb=True)

    for influence in influences[1:]:
        influence_type = pm.objectType(influence)
        if influence_type == 'joint':
            pm.skinCluster(create_skin, e=True, ai=influence, lw=True)
        elif influence_type == 'transform':
            base_influence = pm.duplicate(influence)[0]
            pm.setAttr('%s.v' % base_influence, 0)
            base_influence = pm.rename(base_influence, '%sBase' % base_influence)
            shape = pm.listRelatives(base_influence, s=True, f=True, ni=True)[0]
            pm.skinCluster(create_skin, e=True, lw=True, ug=True, dr=4, ps=0, ns=10, wt=0,
                           ai=influence, bsh=shape)
        else:
            continue

    skin_attribute = pm.rename(create_skin, weight_dict['name'])
    pm.setAttr('%s.skinningMethod' % skin_attribute, weight_dict['skinningMethod'])
    pm.setAttr('%s.useComponents' % skin_attribute, weight_dict['useComponents'])

    skin_set = pm.listConnections('%s.message' % skin_attribute, d=True, s=False)[0]
    pm.rename(skin_set, weight_dict['set'])


    # pm.setAttr('%s.normalizeWeights' % skin_attribute, False)
    # pm.skinPercent(skin_attribute, object_name, nrm=False, prw=100)
    pm.setAttr('%s.normalizeWeights' % skin_attribute, True)

    # vertices = pm.polyEvaluate(object_name, v=True)

    keys = weight_dict.keys()

    number_vertex = [number_vertex for number_vertex in keys if number_vertex.isdigit()]
    # number_vertex = sorted(map(int, number_vertex))
    for vertices in number_vertex:
        tranform_value = zip(influences, weight_dict[str(vertices)])
        pm.progressBar('Progress_Bar', e=True, progress=vertices)
        pm.skinPercent(skin_attribute, object_name +'.vtx[%s]' % vertices, transformValue=tranform_value)

# vertices = len(number_vertex)
    # pm.skinPercent(skin_attribute, object_name+'.vtx[%s]' % number_vertex, transformValue=weight_dict[number_vertex])

    # for value_range in range(0, vertices):
    #     tranform_value = zip(influences, weight_dict[str(value_range)])
    #     pm.skinPercent(skin_attribute, object_name +'.vtx[%s]' % value_range, transformValue=tranform_value)
    #     # if progress % step:
    #     #     continue
    #     progress = 100.0 / vertices * (value_range)
    #     pm.progressBar('Progress_Bar', e=True, progress=progress)
    #


    # length = len(number_vertex)
    #
    # value = []
    # for vertex in number_vertex:
    #     pm.skinPercent(skin_attribute, object_name+'.vtx[%s]' % vertex, transformValue=weight_dict[str(vertex)])


        # # calculation
        # previous_value = int((float(vertex + 1) / float(length)) * 100.00)
        # if previous_value not in value:
        #     value.append(previous_value)



        #om.MGlobal.displayInfo('%s%% done.' % str(value))


    # for percent in value:
    #     for vertex in number_vertex:
    #         pm.skinPercent(skin_attribute, object_name+'.vtx[%s]' % vertex, transformValue=weight_dict[str(vertex)])
    #     om.MGlobal.displayInfo('%s%% done.' % str(percent))


        # if vertex == (vertex - 1):
        #     om.MGlobal.displayInfo('100%% done.')
        # else:
        #
        #     counting = 0
        #     if vertex > 0:
        #         counting = int((float(vertex - 1) / float(vertex))* 100.00)
        #
        #     total_value = int((float(vertex) / float(vertex)) * 100.00)
        #
        #     if not total_value == counting:
        #         om.MGlobal.displayInfo('%s%% done.' % str(total_value))

    # print mynewlist
    # print sorted(map(int, keys))

    # numbers = []
    # for number_vertex in keys:
    #     if number_vertex.isdigit():
    #         numbers.append(number_vertex)
    #         pm.skinPercent(skin_attribute, object_name+'.vtx[%s]' % number_vertex, transformValue=weight_dict[number_vertex])


            # print number_vertex, vertex
            # if number_vertex == vertex:
            #     om.MGlobal.displayInfo('100%% done.')
            # else:
            #     total_value = int((float(number_vertex) / vertex) * 100.00)
            #     om.MGlobal.displayInfo('%s%% done.' % str(total_value))

        #         counting = 0
        #         if number_vertex > 0:
        #             counting = int((float(number_vertex - 1) / vertex) * 100.00)
        #
        #         total_value = int((float(number_vertex) / vertex) * 100.00)
        #
        #         if not total_value == counting:
        #             om.MGlobal.displayInfo('%s%% done.' % str(total_value))
        # else:
        #     pass
        #
        # list_influence = sorted(map(int, numbers))
        # if number_vertex == list_influence[-1]:
        #     om.MGlobal.displayInfo('100%% done.')



#     om.MGlobal.displayInfo('100%% done.')


            # for number_influence, influence in zip (weight_dict[number_vertex], influences):
            #     print number_influence, influence
            #     pm.skinPercent(skin_attribute, object_name+'.vtx[%s]' % number_vertex, transformValue=[])

                # weight_attribute = '%s.weightList[%s].weights[%s]' % (skin_attribute, number_vertex, number_influence)
                # pm.setAttr(weight_attribute, number_vertex)

            # weight_value = weight_dict[item]

    # for number_vertex in xrange(vertex):
    #     for number_influence in xrange(len(influences)):
    #         # print weight_dict[number_vertex]
    #         weight_value = weight_dict[number_vertex][number_influence]
    #         print weight_value

                # if weight_value:

        # # calculation
        # number_vertex = int(number_vertex)
        # if number_vertex == (vertex - 1):
        #     om.MGlobal.displayInfo('100%% done.')
        # else:
        #     counting = 0
        #     if number_vertex > 0:
        #         counting = int((float(number_vertex - 1) / vertex) * 100.00)
        #
        #     total_value = int((float(number_vertex) / vertex) * 100.00)
        #
        #     if not total_value == counting:
        #         om.MGlobal.displayInfo('%s%% done.' % str(total_value))

