import maya.OpenMaya as om
import pymel.core as pm
import ad_controller_shp as ac
import json
from collections import OrderedDict

from xml.dom.minidom import Document
from xml.dom.minidom import parse
import pickle


# def ad_export_ctrl_bin(path, file_name):
#     file = open("%s/%s_ADCtrl.txt" % (path, file_name), "wb")
#     selection = pm.ls(type="nurbsCurve")
#
#     # instance_query_shapes = pm.listRelatives(selection, s=1)
#     # if not pm.objectType(target_shapes[0]) == 'nurbsCurve':
#     data ={}
#     objects =[]
#     color =[]
#     cv=[]
#     vector=[]
#     for item in selection:
#         print item
#         # create object element
#         object = item.getParent()
#         serial_data = ad_lib_query_controller(object)
#         # 'curve' : dfa, fddasf, dfada
#
#         # data.update(serial_data)
#         # objects.append(object)
#         # color.append(serial_data['color'])
#         # cv.append(serial_data['cv'])
#         # vector.append(serial_data['vector'])
#
#         data['curve_%s' % object] = object
#         data['shape_%s' % object] = item
#         data['color_%s' % object] = serial_data['color']
#         data['cv_%s' % object] = serial_data['cv']
#         data['vector_%s' % object] = serial_data['vector']
#
#     # data ={'object' : objects,
#     #        'color': color,
#     #        'cv': cv,
#     #        'vector': vector}
#     print data
#     pickle.dump(data, file)
#     file.close()
#
# def ad_import_ctrl_bin(path):
#     file = open(path, "rb")
#     load_file = pickle.load(file)
#     file.close()
#
#     print load_file
#     # selection = pm.ls(sl=1)
#     # all_curves = pm.ls(type="nurbsCurve")
#     #
#     # if selection:
#     #     for item in selection:
#     #         print item
#     #         # if load_file['curve_%s' % item] == item:
#     #         #     curve_shape = load_file['shape_%s' % item]
#     #         #     color = load_file['color_%s' % item]
#     #         #     pm.setAttr(curve_shape+'.overrideEnabled', 1)
#     #         #     pm.setAttr(curve_shape+'.overrideColor', color[0])
#     #         # else:
#     #         #     om.MGlobal.displayWarning('Load file %s skipped! Due to name issue.' % item )
#     #
#     #         # print item
#     #         # print load_file['curve_%s' % item]
#     # else:
#     #     for item in all_curves:
#     #         print item


# def ad_save_xml_file(path, file_name):
#     doc = Document()
#
#     root_node = doc.createElement("nurbs_curve_ADController")
#     doc.appendChild(root_node)
#
#     # Selection:
#     selection = pm.ls(type="nurbsCurve", v=True)
#
#     # instance_query_shapes = pm.listRelatives(selection, s=1)
#     # if not pm.objectType(target_shapes[0]) == 'nurbsCurve':
#
#     for item in selection:
#         # create object element
#         object = item.getParent()
#         object_node = doc.createElement("object")
#         root_node.appendChild(object_node)
#
#         #object_translation = pm.xform(object, query=True, worldSpace=True, rotatePivot=True)
#
#         query_vector_cv = ad_lib_query_vector_cv(object)
#
#         # set attributes
#
#         object_node.setAttribute("name", str(object))
#         object_node.setAttribute("cv", str(query_vector_cv[0]))
#         object_node.setAttribute("vector", str(query_vector_cv[1]))
#
#         # object_node.setAttribute("translateY", str(object_translation[1]))
#         # object_node.setAttribute("translateZ", str(object_translation[2]))
#
#     xml_file = open("%s/%s_ADCtrl.xml" % (path, file_name), "w")
#     xml_file.write(doc.toprettyxml())
#     xml_file.close()
#
#     print
#     print doc.toprettyxml()
#
# def ad_load_xml_file(path):
#     dom = parse(path)
#     # dom = parse("C:/Temp/test.xml")
#
#     # visit every object node
#     names, cvs, vectors = [],[],[]
#     for node in dom.getElementsByTagName('object'):
#
#         # # method 1: using keys
#         # attrs = node.attributes.keys()
#         # for a in attrs:
#         #     pair = node.attributes[a]
#         #     print (str(pair.name) + " = " + str(pair.value))
#         # print
#
#         # method 2: by attribute name
#
#         name =  node.getAttribute("name")
#         cv =  node.getAttribute("cv")
#         vector = node.getAttribute("vector")
#         # print name
#         # print cv
#         # print vector
#
#
#
#         # print str(node.getAttribute("translateZ"))
#         names.append(name)
#         cvs.append(cv)
#         vectors.append(vector)
#
#     return {'name': names,
#             'cv': cvs,
#             'vector': vectors}

# def ad_load_controller(path):
#     names = ad_load_xml_file(path)['name']
#     cvs = ad_load_xml_file(path)['cv']
#     vectors = ad_load_xml_file(path)['vector']
#
#     # print name
#     # print cv
#     # print vectors
#     new_list = map(str, cvs)
#     print new_list
#     print(type(new_list))
#
#     # for cv in cvs:
#     #     print eval(cv)
#     # x = [cv.encode('UTF8') for cv in cvs]
#     # print x
#     # print(type(x))
#
#     # for cv in list(cvs):
#
#         # for cnv in list(cv):
#         #     print cnv
#
#     # for name, cv, vector in zip (names, cvs, vectors):
#     #     print name
#     #     print cv
#     #     print vector
#     #     for cvvf in cv:
#     #         print cvvf
#     #     # for c, vec in zip(cv, vector):
#     #     #     print c
#     #     #     print vec
#     #         #pm.move((vec[0]), (vec[1]), (vec[2]), c)
#     #
#     #     #load_vector = ad_lib_load_vector_cv(name, cv, vector)
#
#     #print load_vector

# def ad_lib_load_vector_cv(ctrl_shape, cvs, vector_position):
#     object_curve = pm.PyNode(ctrl_shape)
#     # for cv in vector_position:
#     #     print cv
#
#         # for c, vec in zip(cv, vector_pos):
#         #     print c
#         #     print vec
#
#             #pm.move(float(vec[0]), float(vec[1]), float(vec[2]), c)
#     #
#     # pm.setAttr(cv)
#     # for cv in object_curve.getShape().cv:
#     #     vector = pm.dt.Vector(vector_position)
#     #     # position_ws = pm.xform(cv, q=True, ws=True, t=True)
#     #     # position_os = pm.xform(cv, q=True, os=True, t=True)
#     #     #
#     #     # vector_ws = pm.dt.Vector(position_ws[0], position_ws[1], position_ws[2])
#     #     # vector_os = pm.dt.Vector(position_os[0], position_os[1], position_os[2])
#     #     #
#     #     # final_position = vector_ws + (vector_os * value)
#     #
#     #     print pm.move((vector[0]), (vector[1]), (vector[2]), cv)
#     # object_curve = pm.PyNode(ctrl_shape)
#     # position_object = pm.xform(object_curve, q=True, ws=True, t=True)
#     # vector_optimums = []
#     # cvs = []
#     # for cv in object_curve.getShape().cv:
#     #     position_os = pm.xform(cv, q=True, os=True, t=True)
#     #     vector_ws = pm.dt.Vector(position_object[0], position_object[1], position_object[2])
#     #     vector_os = pm.dt.Vector(position_os[0], position_os[1], position_os[2])
#     #     # vector_multiply = vector_os * (current_value * 0.2)
#     #     vector_optimum = vector_os + vector_ws
#     #     cvs.append(cv)
#     #     vector_optimums.append(vector_optimum)
#     #
#     # # print cvs
#     # # print vector_optimums
#     # return cvs, vector_optimums

def ad_lib_save_json_controller(file_name):
    # list = pm.ls(type='nurbsCurve')
    shape_dict = OrderedDict()
    selection = pm.ls(sl=1)
    list = []
    if selection:
        for item in selection:
            try:
                object= pm.objectType(item.getShape())
            except Exception:
                om.MGlobal.displayWarning("Object '%s' is skipped! It is not nurbsCurve." % (item))
            else:
                if object == 'nurbsCurve':
                    list.append(item.getShape())
    else:
        list = pm.ls(type='nurbsCurve')
    for item in list:
        item_parent = item.getParent()
        object_curve = pm.PyNode(item_parent)
        cvs, xvalue, yvalue, zvalue, color =[], [], [], [], []
        for cv in object_curve.getShape().cv:
            x = pm.getAttr(cv + '.xValue')
            y = pm.getAttr(cv + '.yValue')
            z = pm.getAttr(cv + '.zValue')
            xvalue.append(x)
            yvalue.append(y)
            zvalue.append(z)
            cv = cv.split('.')[-1]
            cvs.append(cv)
        if pm.getAttr('%s.overrideEnabled' % item):
            color_number = pm.getAttr('%s.overrideColor' % item)
            color.append(color_number)
        shape_dict[item_parent.nodeName()] = {'cv': cvs, 'xValue': xvalue, 'yValue': yvalue, 'zValue': zvalue, 'overrideColor':color}

    file = open("%s" % (file_name), "w")
    json.dump(shape_dict, file, indent=4)


def ad_lib_load_json_controller(file_name):
    file = open("%s" % (file_name))
    shape_dict = json.load(file)
    keys = shape_dict.keys()
    select = pm.ls(sl=1)
    scene = pm.ls(type='nurbsCurve')
    list = []
    if select:
        for item in select:
            if item in keys:
                list.append(item)
            else:
                om.MGlobal.displayWarning(
                    "Object '%s' is skipped! There is no saving curve in the library." % (item))
    else:
        for item in scene:
            item = item.getParent()
            if item in keys:
                list.append(item)
            else:
                om.MGlobal.displayWarning(
                    "Object '%s' is skipped! There is no saving curve in the library." % (item))

    for name in list:
        name = name.nodeName()
        value = shape_dict.get(name)
        name = pm.PyNode(name)
        shape_name = name.getShape()
        for cv, x, y, z in zip(value['cv'], value['xValue'], value['yValue'],
                               value['zValue']):
            pm.setAttr('%s.%s.xValue' % (shape_name, cv), x)
            pm.setAttr('%s.%s.yValue' % (shape_name, cv), y)
            pm.setAttr('%s.%s.zValue' % (shape_name, cv), z)

        for color in value['overrideColor']:
            pm.setAttr('%s.overrideColor' % shape_name, color)

# def ad_load_json_controller(file_name):
#     file = open("%s" % (file_name))
#     shape_dict = json.load(file)
#     keys = shape_dict.keys()
#     select = pm.ls(sl=1)
#     list = []
#     if select:
#         for item in select:
#             if item in keys:
#                 list.append(item)
#             else:
#                 om.MGlobal.displayWarning(
#                     "Object '%s' is skipped! Due to there is no saving curve in library." % (item))
#
#     for name in list:
#         name = name.nodeName()
#         value = shape_dict.get(name)
#         name = pm.PyNode(name)
#         shape_name = name.getShape()
#         for cv, x, y, z in zip(value['cv'], value['xValue'], value['yValue'],
#                                value['zValue']):
#             pm.setAttr('%s.%s.xValue' % (shape_name, cv), x)
#             pm.setAttr('%s.%s.yValue' % (shape_name, cv), y)
#             pm.setAttr('%s.%s.zValue' % (shape_name, cv), z)
#
#         for color in value['overrideColor']:
#             pm.setAttr('%s.overrideColor' % shape_name, color)

# def ad_save_x_json_controller(file_name):
#     list = pm.ls(type='nurbsCurve')
#     shape_dict = OrderedDict()
#     for item in list:
#         item_parent = item.getParent()
#         object_curve = pm.PyNode(item_parent)
#         # cvs, xvalue, yvalue, zvalue, color =[], [], [], [], []
#
#         if pm.getAttr('%s.overrideEnabled' % item):
#             color_number = pm.getAttr('%s.overrideColor' % item)
#             # color.append(color_number)
#             shape_dict[item.nodeName()] = {'overrideColor': color_number}
#
#         for cv in object_curve.getShape().cv:
#             x = pm.getAttr(cv + '.xValue')
#             y = pm.getAttr(cv + '.yValue')
#             z = pm.getAttr(cv + '.zValue')
#             # xvalue.append(x)
#             # yvalue.append(y)
#             # zvalue.append(z)
#             # cv = cv.split('.')[-1]
#             # cvs.append(cv)
#             cv = str(cv)
#             shape_dict[cv] = {'xValue': x, 'yValue': y, 'zValue': z}
#
#         #print(json.dumps(shapeDict, indent=4))
#     file = open("%s" % (file_name), "w")
#     json.dump(shape_dict, file, indent=4)

# def ad_loadc_json_controller(file_name):
#     file = open("%s" % (file_name))
#     shape_dict = json.load(file)
#     for name, value in shape_dict.iteritems():
#         name = pm.PyNode(name)
#         shape_name = name.getShape()
#         # pm.setAttr(shape_name+'.xValue',
#         print name, value
#         for color, cv, x, y, z in zip(value['cv'], value['overrideColor'], value['xValue'], value['yValue'],
#                                       value['zValue']):
#             pm.setAttr(shape_name + '.{0}.xValue'.format(cv), x)
#             pm.setAttr(shape_name + '.{0}.yValue'.format(cv), y)
#             pm.setAttr(shape_name + '.{0}.zValue'.format(cv), z)

        #print(json.dumps(shapeDict, indent=4))
    # file = open("%s" % (file_name), "w")
    # json.dump(shapeDict, file, indent=4)

# def ad_lib_query_controller(ctrl_shape):
#     object_curve = pm.PyNode(ctrl_shape)
#     position_object = pm.xform(object_curve, q=True, ws=True, t=True)
#
#     vector_optimums, cvs,color =[], [],[]
#     for cv in object_curve.getShape().cv:
#         position_os = pm.xform(cv, q=True, os=True, t=True)
#         vector_ws = pm.dt.Vector(position_object[0], position_object[1], position_object[2])
#         vector_os = pm.dt.Vector(position_os[0], position_os[1], position_os[2])
#         #vector_multiply = vector_os * (current_value * 0.2)
#         vector_optimum = vector_os + vector_ws
#         cvs.append(cv)
#         vector_optimums.append(vector_optimum)
#
#     if pm.getAttr('%s.overrideEnabled' % ctrl_shape.getShape()):
#         color_number = pm.getAttr('%s.overrideColor' % ctrl_shape.getShape())
#         color.append(color_number)
#
#     # print cvs
#     # print vector_optimums
#     return {'cv' : cvs,
#             'vector' : vector_optimums,
#             'color': color}


# def ad_lib_query_vector(ctrl_shape):
#     x = ad_lib_query_controller(ctrl_shape)
#     z=[]
#     for item in x[0]:
#         item = item
#         z.append(item)
#
#     print z


def ad_lib_mirror_controller(object_origin, object_target, key_position):
    object_curve_origin = pm.PyNode(object_origin)
    object_curve_target = pm.PyNode(object_target)

    # if len(object_curve_origin.getShape().cv) == len(object_curve_target.getShape().cv):
    for vtx_origin, vtx_target in zip(object_curve_origin.getShape().cv, object_curve_target.getShape().cv):
        position_ws_vtx_origin = pm.xform(vtx_origin, q=True, ws=True, t=True)
        vector_ws_vtx_origin = pm.dt.Vector(position_ws_vtx_origin[0], position_ws_vtx_origin[1], position_ws_vtx_origin[2])
        vector_mirror = ad_lib_vector_reverse_position(vector_ws_vtx_origin[0], vector_ws_vtx_origin[1], vector_ws_vtx_origin[2])[key_position]

        pm.move((vector_mirror[0]), (vector_mirror[1]), (vector_mirror[2]), vtx_target)

# def ad_lib_rotation_controller(object, x, y, z):
#     shape = object.getShape()
#     points = pm.ls('%s.cv[0:*]' % shape)
#     pm.rotate(points,(x, y, z), r=True, ocp=True, os=True, fo=True)

# def ad_lib_rotation_controller(object, matrix_rotation_position):
#     object_curve = pm.PyNode(object)
#
#     for vtx in object_curve.getShape().cv:
#         split = vtx.split('.')[-1]
#         # target_position = matrix_rotation_position
#         # print ('ini target:', target_position)
#         position_vtx = pm.xform(vtx, q=True, os=True, t=True)
#         vector_ws_pos = pm.dt.Vector(position_vtx[0], position_vtx[1], position_vtx[2])
#
#         matrix_ws = pm.xform(vtx, q=True, ws=True, m=True)
#         print (split, 'matrix', matrix_ws)
#         print (split, 'xform', position_vtx)
#         print (split, 'vector', vector_ws_pos)

        # pm.xform(vtx, ws=True, m=matrix_ws)

        # jumlah = target_position +  matrix_ws
        # print ('ini jumlah:', jumlah)

    #     # matrix_rotation =  matrix_rotation_position
    #
    #     hatspot_x = matrix_ws.__getitem__(0)
    #     hatspot_y = matrix_ws.__getitem__(1)
    #     hatspot_z = matrix_ws.__getitem__(2)
    #     hatspot_position = matrix_ws.__getitem__(3)
    #
    #     hatspot_rot_x = matrix_rotation_position.__getitem__(0)
    #     hatspot_rot_y = matrix_rotation_position.__getitem__(1)
    #     hatspot_rot_z = matrix_rotation_position.__getitem__(2)
    #     hatspot_rot_position = matrix_rotation_position.__getitem__(3)
    #
    #     # matrixes_x = hatspot_x + hatspot_rot_x
    #     # matrixes_y = hatspot_y + hatspot_rot_y
    #     # matrixes_z = hatspot_z + hatspot_rot_z
    #     # matrixes_position = hatspot_position + hatspot_rot_position
    #
    #     matrixes_x = hatspot_rot_x
    #     matrixes_y = hatspot_rot_y
    #     matrixes_z = hatspot_rot_z
    #     matrixes_position = hatspot_rot_position
    #
    #     # print hatspot_x
    #     # print hatspot_y
    #     # print hatspot_z
    #     # print hatspot_position
    #
    #
    # #     # replacing matrix value
    #     matrix_ws.__setitem__(0, matrixes_x)
    #     matrix_ws.__setitem__(1, matrixes_y)
    #     matrix_ws.__setitem__(2, matrixes_z)
    #     matrix_ws.__setitem__(3, matrixes_position)
    # #
    #     pm.xform(vtx, ws=True, m=matrix_ws)

        # pm.move((matrix_rotation[0]), (matrix_rotation[1]), (matrix_rotation[2]), vtx)
# def ad_lib_rotation_controller_x(object, matrix_rotation_position):
#     object_curve = pm.PyNode(object)
#     position_ws = pm.xform(object_curve, q=True, ws=True, t=True)
#     #rotation_ws = pm.xform(object_curve, q=True, ws=True, ro=True)
#
#     for vtx in object_curve.getShape().cv:
#         position_vtx = pm.xform(vtx, q=True, ws=True, t=True)
#         vector_ws_pos = pm.dt.Vector(position_ws[0], position_ws[1], position_ws[2])
#         #vector_ws_rot = pm.dt.Vector(rotation_ws[0], rotation_ws[1], rotation_ws[2])
#         vector_ws_vtx = pm.dt.Vector(position_vtx[0], position_vtx[1], position_vtx[2])
#         vector_pos_vtx = (vector_ws_pos - vector_ws_vtx)
#         #vector_rot_vtx = (vector_ws_rot - vector_ws_vtx)
#         x = pm.dt.Matrix(matrix_rotation_position)
#         print x
#         print vector_pos_vtx
#         print x*vector_pos_vtx
#         matrix_rotation = ((x * (vector_pos_vtx))) + (vector_ws_pos)
#         # print matrix_rotation
#         # matrix_rotation = ((matrix_rotation_position * vector_ws_vtx))
#
#         # pm.move((matrix_rotation[0]), (matrix_rotation[1]), (matrix_rotation[2]), vtx)

def ad_lib_rotation_controller_x(object, matrix_rotation_position):
    object_curve = pm.PyNode(object)
    position_ws = pm.xform(object_curve, q=True, ws=True, t=True)
    #rotation_ws = pm.xform(object_curve, q=True, ws=True, ro=True)

    for vtx in object_curve.getShape().cv:
        position_vtx = pm.xform(vtx, q=True, ws=True, t=True)
        vector_ws_pos = pm.dt.Vector(position_ws[0], position_ws[1], position_ws[2])
        #vector_ws_rot = pm.dt.Vector(rotation_ws[0], rotation_ws[1], rotation_ws[2])
        vector_ws_vtx = pm.dt.Vector(position_vtx[0], position_vtx[1], position_vtx[2])
        vector_pos_vtx = (vector_ws_pos - vector_ws_vtx)
        #vector_rot_vtx = (vector_ws_rot - vector_ws_vtx)
        x = pm.dt.Matrix(matrix_rotation_position)
        print x
        print vector_pos_vtx
        print x*vector_pos_vtx
        matrix_rotation = ((x * (vector_pos_vtx))) + (vector_ws_pos)
        # print matrix_rotation
        # matrix_rotation = ((matrix_rotation_position * vector_ws_vtx))

        # pm.move((matrix_rotation[0]), (matrix_rotation[1]), (matrix_rotation[2]), vtx)

def ad_lib_vector_reverse_position(vector_origin_0, vector_origin_1, vector_origin_2):
    # position_origin = pm.xform(object_curve_origin, q=True, ws=True, t=True)
    vector_position_origin_x = pm.dt.Vector(vector_origin_0*-1.0, vector_origin_1, vector_origin_2)
    vector_position_origin_y = pm.dt.Vector(vector_origin_0, vector_origin_1*-1.0, vector_origin_2)
    vector_position_origin_z = pm.dt.Vector(vector_origin_0, vector_origin_1,vector_origin_2* -1.0)

    return {'x': vector_position_origin_x,
            'y': vector_position_origin_y,
            'z': vector_position_origin_z}

def ad_lib_flaten_list(nested_list):
    flat_list = []
    for sub_list in nested_list:
        for element in sub_list:
            flat_list.append(element)

    return flat_list

def ad_lib_matrix_rotation_x(value):
    value_float = float(value)
    matrix = pm.dt.Matrix([1.0, 0.0, 0.0, 0.0,
                           0.0, pm.dt.cos(pm.dt.radians(value_float)), -1 * (pm.dt.sin(pm.dt.radians(value_float))),
                           0.0,
                           0.0, pm.dt.sin(pm.dt.radians(value_float)), pm.dt.cos(pm.dt.radians(value_float)), 0.0,
                           0.0, 0.0, 0.0, 1.0])
    return matrix


def ad_lib_matrix_rotation_y(value):
    value_float = float(value)
    matrix = pm.dt.Matrix([pm.dt.cos(pm.dt.radians(value_float)), 0.0, pm.dt.sin(pm.dt.radians(value_float)), 0.0,
                           0.0, 1.0, 0.0, 0.0,
                           -1 * (pm.dt.sin(pm.dt.radians(value_float))), 0.0, pm.dt.cos(pm.dt.radians(value_float)),
                           0.0,
                           0.0, 0.0, 0.0, 1.0])
    return matrix


def ad_lib_matrix_rotation_z(value):
    value_float = float(value)
    matrix = pm.dt.Matrix(
        [pm.dt.cos(pm.dt.radians(value_float)), -1 * (pm.dt.sin(pm.dt.radians(value_float))), 0.0, 0.0,
         pm.dt.sin(pm.dt.radians(value_float)), pm.dt.cos(pm.dt.radians(value_float)), 0.0, 0.0,
         0.0, 0.0, 1.0, 0.0,
         0.0, 0.0, 0.0, 1.0])
    return matrix

def ad_list_connections_object(object):
    # list connection
    if len(object) > 1:
        om.MGlobal.displayError('Objects selected are multiple. Select a single object only!')
    else:
        select = []
        for item in object:
            source = pm.listConnections(object, p=True, d=False, s=True, c=True)
            if source:
                for node_source in source:
                    # print node_source
                    connection_source_object = node_source[1].split('.')[0]
                    connection_source_transform = node_source[1].split('.')[1]
                    node_source_type = pm.nodeType(connection_source_object)

                    connection_destination_object = node_source[0].split('.')[0]
                    connection_destination_transform = node_source[0].split('.')[1]

                    if node_source_type == 'parentConstraint':
                        object_select = pm.listConnections(connection_source_object + '.target[0].targetParentMatrix',
                                                           d=0, s=1)
                        om.MGlobal.displayInfo("------ >>> %s %s is connected to Parent Constraint from %s %s!" %
                                               (item, connection_destination_transform, object_select[0],
                                                connection_source_transform[10:]))
                    elif node_source_type == 'pointConstraint':
                        object_select = pm.listConnections(connection_source_object + '.target[0].targetParentMatrix',
                                                           d=0, s=1)
                        om.MGlobal.displayInfo("------ >>> %s %s is connected to Point Constraint from %s %s!" %
                                               (item, connection_destination_transform, object_select[0],
                                                connection_source_transform[10:]))
                    elif node_source_type == 'orientConstraint':
                        object_select = pm.listConnections(connection_source_object + '.target[0].targetParentMatrix',
                                                           d=0, s=1)
                        om.MGlobal.displayInfo("------ >>> %s %s is connected to Orient Constraint from %s %s!" %
                                               (item, connection_destination_transform, object_select[0],
                                                connection_source_transform[10:]))
                    elif node_source_type == 'scaleConstraint':
                        object_select = pm.listConnections(connection_source_object + '.target[0].targetParentMatrix',
                                                           d=0, s=1)
                        om.MGlobal.displayInfo("------ >>> %s %s is connected to Scale Constraint from %s %s!" %
                                               (item, connection_destination_transform, object_select[0],
                                                connection_source_transform[10:]))
                    elif node_source_type == 'aimConstraint':
                        object_select = pm.listConnections(connection_source_object + '.target[0].targetParentMatrix',
                                                           d=0, s=1)
                        om.MGlobal.displayInfo("------ >>> %s %s is connected to Aim Constraint from %s %s!" %
                                               (item, connection_destination_transform, object_select[0],
                                                connection_source_transform[10:]))
                    elif node_source_type == 'transform':
                        object_select = connection_source_object
                        om.MGlobal.displayInfo("------ >>> %s %s is connected to Direct Connection from %s %s!" % (
                            connection_destination_object,
                            connection_destination_transform,
                            connection_source_object,
                            connection_source_transform))
                    else:
                        object_select = om.MGlobal.displayWarning(
                            "Skip the target! The object %s %s doesn't have any constraint or direct connection! "
                            "It's connected with another node. " %
                            (connection_destination_object, connection_destination_transform))

                    select.append(object_select)
                try:
                    pm.select(select)
                except:
                    pass
            else:
                om.MGlobal.displayWarning('There is no connection to the transform object selected!')


def ad_lib_pivot_controller(controller, parent_constraint_node, suffix):
    # pm.select(cl=1)
    joint = pm.joint(n='instance_pivot')
    pm.setAttr(joint + '.drawStyle', 2)
    controller_rs = ad_lib_ctrl_shape(ac.ARROW3D, size_ctrl=0.8)
    ad_lib_ctrl_color(ctrl=[controller_rs], color=20)
    pm.rename(controller_rs, ad_lib_main_name(controller) + 'Pivot' + suffix)

    # parent relatives
    shape_ctrl = pm.listRelatives(controller_rs, s=True)[0]
    pm.parent(shape_ctrl, joint, r=True, s=True)
    pm.delete(controller_rs)

    joint_new_name = pm.rename(joint, ad_lib_main_name(controller) + 'Pivot' + suffix)
    ad_lib_xform_position_rotation(origin=controller, target=joint_new_name)
    pm.parent(joint_new_name, controller)

    # connect pivot
    pm.connectAttr(joint + '.translate', controller + '.rotatePivot')
    pm.connectAttr(joint + '.translate', controller + '.scalePivot')

    # create decompose matrix
    decompose_matrix = pm.createNode('decomposeMatrix', n=ad_lib_main_name(joint_new_name) + '_dmtx')
    pm.connectAttr(joint_new_name + '.inverseMatrix', decompose_matrix + '.inputMatrix')
    pm.connectAttr(decompose_matrix + '.outputTranslate', parent_constraint_node + '.target[0].targetOffsetTranslate')

    ad_lib_lock_hide_attr(lock_hide_channel=['r', 's', 'v', 'radius'], ctrl=joint_new_name, hide_object=True, cb=0)

    return joint_new_name


def ad_lib_parent_constraint(obj_base, obj_target, mo=1):
    par_constraint = pm.parentConstraint(obj_base, obj_target, mo=mo)
    split = par_constraint.split('_')
    x = '_'.join(split[:-1])
    n = x.replace(x, x + '_pac')
    new_name = [pm.rename(par_constraint, n)]
    return new_name


def ad_lib_orient_constraint(obj_base, obj_target, mo=1):
    orient_constraint = pm.orientConstraint(obj_base, obj_target, mo=mo)
    split = orient_constraint.split('_')
    x = '_'.join(split[:-1])
    n = x.replace(x, x + '_oc')
    new_name = [pm.rename(orient_constraint, n)]
    return new_name


def ad_lib_point_constraint(obj_base, obj_target, mo=1):
    point_constraint = pm.pointConstraint(obj_base, obj_target, mo=mo)
    split = point_constraint.split('_')
    x = '_'.join(split[:-1])
    n = x.replace(x, x + '_pc')
    new_name = [pm.rename(point_constraint, n)]
    return new_name


def ad_lib_scale_constraint(obj_base, obj_target, mo=1):
    scale_constraint = pm.scaleConstraint(obj_base, obj_target, mo=mo)
    split = scale_constraint.split('_')
    x = '_'.join(split[:-1])
    n = x.replace(x, x + '_sc')
    new_name = [pm.rename(scale_constraint, n)]

    return new_name


def ad_lib_query_textfield_object(object_define, *args):
    text = []
    if pm.textField(object_define, q=True, en=True):
        if pm.textField(object_define, q=True, tx=True):
            text = pm.textField(object_define, q=True, tx=True)
        else:
            pm.error("'%s' can not be empty!" % object_define)
    else:
        pass
    return text, object_define


def ad_lib_query_list_textfield_object(object_define, *args):
    listing_object = []
    if pm.textField(object_define, q=True, en=True):
        if pm.textField(object_define, q=True, tx=True):
            text = pm.textField(object_define, q=True, tx=True)
            listing = text.split(',')
            set_duplicate = set([x for x in listing if listing.count(x) > 1])
            if set_duplicate:
                for item in list(set_duplicate):
                    pm.error("'%s' is duplicate object!" % item)
            else:
                for item in listing:
                    listing_object.append(item)
        else:
            pm.error("'%s' can not be empty!" % object_define)
    else:
        pass

    return listing_object, object_define


def ad_lib_prefix(prefix_text):
    if pm.textField(prefix_text, q=True, en=True):
        return ad_lib_query_textfield_object(object_define=prefix_text)[0]
    else:
        return ''


def ad_lib_match_position_target_to_ctrl(selection, target, manipulated_position,
                                         manipulated_rotation):
    if '.' in str(selection[0]):
        cls = pm.cluster(selection)
        pm.pointConstraint(cls, target[0], mo=0)
        pm.delete(cls)

        # set attribute rotate jnt
        if manipulated_rotation != (0, 0, 0):
            pm.setAttr(target[0] + '.rotateX', list(manipulated_rotation)[0])
            pm.setAttr(target[0] + '.rotateY', list(manipulated_rotation)[1])
            pm.setAttr(target[0] + '.rotateZ', list(manipulated_rotation)[2])

        # set attribute translate jnt
        if manipulated_position != (0, 0, 0):
            pm.setAttr(target[0] + '.translateX', list(manipulated_position)[0])
            pm.setAttr(target[0] + '.translateY', list(manipulated_position)[1])
            pm.setAttr(target[0] + '.translateZ', list(manipulated_position)[2])
    else:
        for object, tgt in zip(selection, target):
            # query and match
            ad_lib_xform_position_rotation(origin=object, target=tgt)


def ad_lib_xform_position_rotation(origin, target):
    origin_position = pm.xform(origin, ws=True, q=True, t=True)
    origin_rotation = pm.xform(origin, ws=True, q=True, ro=True)

    # match position
    target_position = pm.xform(target, ws=True, t=origin_position)
    target_rotation = pm.xform(target, ws=True, ro=origin_rotation)

    return {'origin_position': origin_position,
            'origin_rotation': origin_rotation,
            'target_position': target_position,
            'target_rotation': target_rotation
            }


def ad_lib_main_name(main_name):
    if '_' in main_name:
        get_prefix_name = main_name.split('_')[:-1]
        joining = '_'.join(get_prefix_name)
        return joining
    else:
        return main_name


def ad_lib_get_suffix_main(main_name):
    if '_' in main_name:
        get_suffix_name = main_name.split('_')[-1]
        # joining = '_'.join(get_prefix_name)
    else:
        get_suffix_name = ''
    return get_suffix_name


def ad_lib_defining_object_text_field(define_object, tx='', *args, **kwargs):
    pm.textField(define_object, tx=tx, **kwargs)


def ad_lib_display(object, target, long_name='display', default_vis=1, k=True, cb=False):
    # create attr
    if not pm.objExists(object + '.' + long_name):
        pm.addAttr(object, ln=long_name, at='bool')
    else:
        pass
    pm.setAttr('%s.%s' % (object, long_name), default_vis, e=True, k=k, cb=cb)
    pm.connectAttr('%s.%s' % (object, long_name), target + '.visibility')


def ad_lib_group_parent(groups, name, suffix, prefix_2, prefix_number):
    # create group hierarchy
    grps = []
    for number, group in enumerate(groups):
        grps.append(pm.createNode('transform', n="%s%s%s%s%s_%s" % (
            name, group.title(), suffix.title(), prefix_number, prefix_2, 'grp')))

        if number > 0:
            pm.parent(grps[number], grps[number - 1])

    return grps


def ad_lib_replacing_controller(list_controller):
    instance_controller = list_controller.pop(0)
    for target in list_controller:
        target_shapes = pm.listRelatives(target, s=1)
        instance_query_shapes = pm.listRelatives(instance_controller, s=1)
        if not pm.objectType(target_shapes[0]) == 'nurbsCurve':
            om.MGlobal.displayWarning("%s is not curve type object! Replacing is skipped." % target)

        elif not pm.objectType(instance_query_shapes[0]) == 'nurbsCurve':
            om.MGlobal.displayError("%s is not curve type object!" % instance_controller)

        else:
            instance_shapes = pm.duplicate(instance_controller.getShape(), addShape=True)[0]
            pm.parent(instance_shapes, target, r=True, s=True)

            list_attribute_target_shapes = pm.listAttr(target_shapes, ud=1)
            list_attribute_instance_shapes = pm.listAttr(instance_shapes, ud=1)

            for list_attr_ins_shape in list_attribute_instance_shapes:
                pm.setAttr('%s.%s' % (instance_shapes, list_attr_ins_shape), e=True, l=False)
                pm.deleteAttr('%s.%s' % (instance_shapes, list_attr_ins_shape))

            for attr_tgt_shape in list_attribute_target_shapes:
                get_type_attr = pm.attributeQuery(attr_tgt_shape, n=target_shapes[0], attributeType=True)
                keyable = pm.getAttr('%s.%s' % (target_shapes[0], attr_tgt_shape), k=True)
                channel_box = pm.getAttr('%s.%s' % (target_shapes[0], attr_tgt_shape), cb=True)
                lock = pm.getAttr('%s.%s' % (target_shapes[0], attr_tgt_shape), l=True)

                value_attr = pm.getAttr('%s.%s' % (target_shapes[0], attr_tgt_shape))
                if get_type_attr == 'long' or get_type_attr == 'double':
                    try:
                        range = pm.attributeQuery(attr_tgt_shape, n=target_shapes[0], range=True)
                        pm.addAttr(instance_shapes, ln=attr_tgt_shape, at=get_type_attr, min=range[0], max=range[1])
                    except:
                        pm.addAttr(instance_shapes, ln=attr_tgt_shape, at=get_type_attr)

                    pm.setAttr('%s.%s' % (instance_shapes, attr_tgt_shape), value_attr)
                    pm.setAttr('%s.%s' % (instance_shapes, attr_tgt_shape), e=True, k=keyable, cb=channel_box, l=lock)

                elif get_type_attr == 'typed':
                    pm.addAttr(instance_shapes, ln=attr_tgt_shape, dt="string")
                    if value_attr:
                        pm.setAttr('%s.%s' % (instance_shapes, attr_tgt_shape), value_attr, type='string')
                    pm.setAttr('%s.%s' % (instance_shapes, attr_tgt_shape), e=True, k=keyable, cb=channel_box,
                               l=lock)

                else:
                    pm.addAttr(instance_shapes, ln=attr_tgt_shape, at=get_type_attr)
                    pm.setAttr('%s.%s' % (instance_shapes, attr_tgt_shape), value_attr)
                    pm.setAttr('%s.%s' % (instance_shapes, attr_tgt_shape), e=True, k=keyable, cb=channel_box,
                               l=lock)
            try:
                # connection replace to instance
                list_connections = pm.listConnections(target_shapes, c=True, plugs=True)
                for connection, attr_tgt_shape in zip(list_connections, list_attribute_target_shapes):
                    spliting = connection[0].split('.')
                    new_instance_shape = connection[0].replace(str(spliting[0]), str(instance_shapes))
                    pm.disconnectAttr(connection[0], connection[1])
                    pm.connectAttr(new_instance_shape, connection[1])
            except:
                pass

            # rename the shape
            replacing = instance_shapes.name().replace(str(instance_shapes), str(target_shapes[0]))
            pm.delete(target_shapes)
            instance_shapes.rename(replacing)
            pm.select(cl=1)

    return instance_controller, list_controller


def ad_lib_replacing_color(source, target):
    if not source:
        om.MGlobal.displayError("No curves selected")
        return False

    for obj in target:
        shapeNodes = pm.listRelatives(obj, shapes=True)
        sourceNode = pm.listRelatives(source, shapes=True)[0]
        for shape in shapeNodes:
            try:
                pm.setAttr("{0}.overrideEnabled".format(shape), True)
                pm.setAttr("{0}.overrideEnabled".format(sourceNode), True)
                color_source = pm.getAttr("{0}.overrideColor".format(sourceNode))
                pm.setAttr("{0}.overrideColor".format(shape), color_source)
            except:
                om.MGlobal.displayWarning("Failed to override color: {0}".format(shape))
    return True


# def ad_scaling_controllers(size_obj, ctrl_shape):
#     points = mc.ls('%s.cv[0:*]' % ctrl_shape, fl=True)
#     mc.scale(size_obj, size_obj, size_obj, points, ocp=True, r=True)

# def ad_lib_scaling_controller(current_value, ctrl_shape):
#     # hat = pm.PyNode("PartyHat")
#     # # birdy = pm.PyNode('Birdy')
#     # birdy_likes_his_hat_here = pm.dt.Matrix([
#     #     [0.99, -0.13, 0.022, 0.0],
#     #     [0.13, 0.97, -0.16, 0.0],
#     #     [0, 0.167, 0.985, 0.0],
#     #     [12.13, 83.57, -15.185, 1.0],
#     # ])
#     # hat_spot=pm.PyNode('hat_spot')
#     hat_spot_mtx = pm.dt.Matrix(pm.xform(ctrl_shape, ws=True, q=True, m=True))
#
#     # query matrix value
#     hatspot_x = hat_spot_mtx.__getitem__(0)
#     hatspot_y = hat_spot_mtx.__getitem__(1)
#     hatspot_z = hat_spot_mtx.__getitem__(2)
#     hatspot_position = hat_spot_mtx.__getitem__(3)
#
#     # replacing matrix value
#     hat_spot_mtx.__setitem__(0, hatspot_x*current_value)
#     hat_spot_mtx.__setitem__(1, hatspot_y*current_value)
#     hat_spot_mtx.__setitem__(2, hatspot_z*current_value)
#     hat_spot_mtx.__setitem__(3, hatspot_position)
#
#     # set the hat position
#     pm.xform(ctrl_shape, ws=True, m=hat_spot_mtx)

def ad_lib_scaling_controller(current_value, ctrl_shape):
    object_curve = pm.PyNode(ctrl_shape)
    position_object = pm.xform(object_curve, q=True, ws=True, t=True)
    # rotation_object = pm.xform(object_curve, q=True, ws=True, ro=True)
    # print rotation_object
    #rotation = object_curve.getRotation()
    # print rotation_x
    # rotate_matrix_x_0 = ad_matrix_rotation_x(rotation_x[0])
    # rotate_matrix_y_0 = ad_matrix_rotation_x(rotation_x[0])
    # rotate_matrix_z_0 = ad_matrix_rotation_x(rotation_x[0])

    for cv in object_curve.getShape().cv:
        position_ws = pm.xform(cv, q=True, ws=True, t=True)
        position_os = pm.xform(cv, q=True, os=True, t=True)
        #vector_position_ws = pm.dt.Vector(position_object[0], position_object[1], position_object[2])
        # vector_ro = pm.dt.Vector(rotation_object[0], rotation_object[1], rotation_object[2])
        vector_ws = pm.dt.Vector(position_ws[0], position_ws[1], position_ws[2])
        vector_os = pm.dt.Vector(position_os[0], position_os[1], position_os[2])
        # print 'vector pos:', vector_position_ws
        # print 'vector ws:', vector_ws
        # print 'vector os:', vector_os
        # vex = vector_ws - vector_os
        # print 'vector os-ws:', vex
        final_position = vector_ws + (vector_os * (current_value * 0.2))
        # add = vector_position_ws - (vex)
        # print 'vector pos -(os-ws):', add
        # vexcv = vector_ws + add

        # print 'vector ws -(os-ws):', add
        # print 'vector multiply:', vector_multiply
        # vector_optimum = vector_os + vector_multiply + vector_position_ws
        # vector_optimum = vector_ws + vector_multiply)
        # print 'vector vec ws + vec os*(current value*0.2):', vector_optimum
        # pm.move((vector_optimum[0]), (vector_optimum[1]), (vector_optimum[2]), cv)

    # pm.setAttr('%s.xValue' % cv, vector_multiply[0])
        # pm.setAttr('%s.yValue' % cv, vector_multiply[1])
        # pm.setAttr('%s.zValue' % cv, vector_multiply[2])

        #pm.move((final_position[0]), (final_position[1]), (final_position[2]), cv)

def scaling_object(value, object):
    object_curve = pm.PyNode(object)
    for cv in object_curve.getShape().cv:
        position_ws = pm.xform(cv, q=True, ws=True, t=True)
        position_os = pm.xform(cv, q=True, os=True, t=True)

        vector_ws = pm.dt.Vector(position_ws[0], position_ws[1], position_ws[2])
        vector_os = pm.dt.Vector(position_os[0], position_os[1], position_os[2])

        final_position = vector_ws + (vector_os * value)

        pm.move((final_position[0]), (final_position[1]), (final_position[2]), cv)


def ad_lib_attr_value(channel):
    attr_lock_list = []
    for lc in channel:
        if lc in ['t', 'r', 's']:
            for axis in ['x', 'y', 'z']:
                at = lc + axis
                attr_lock_list.append(at)
        else:
            attr_lock_list.append(lc)
    return attr_lock_list


def ad_lib_hide_unhide_attr(channel, ctrl):
    attr_lock_list = ad_lib_attr_value(channel)
    for at in attr_lock_list:
        query_object_hide = pm.getAttr(ctrl + '.' + at, k=True)
        if query_object_hide:
            pm.setAttr(ctrl + '.' + at, k=False)
        else:
            pm.setAttr(ctrl + '.' + at, k=True)
    return attr_lock_list


def ad_lib_lock_unlock_attr(channel, ctrl):
    attr_lock_list = ad_lib_attr_value(channel)
    for at in attr_lock_list:
        query_object_lock = pm.getAttr(ctrl + '.' + at, l=True)
        if query_object_lock:
            pm.setAttr(ctrl + '.' + at, l=False)
        else:
            pm.setAttr(ctrl + '.' + at, l=True)
    return attr_lock_list


def ad_lib_lock_hide_attr(lock_hide_channel, ctrl, hide_object, **kwargs):
    attr_lock_list = ad_lib_attr_value(lock_hide_channel)
    for at in attr_lock_list:
        if hide_object:
            pm.setAttr(ctrl + '.' + at, l=1, k=0, **kwargs)
        else:
            pm.setAttr(ctrl + '.' + at, l=0, k=1, **kwargs)

    return attr_lock_list


def ad_lib_ctrl_color_list(color):
    selection = pm.ls(selection=True)
    if not selection:
        om.MGlobal.displayError("No curves selected")
        return False
    else:
        for obj in selection:
            shapeNodes = pm.listRelatives(obj, shapes=True)[0]
            if not pm.objectType(shapeNodes) == 'nurbsCurve':
                pass
            else:
                try:
                    pm.setAttr("{0}.overrideEnabled".format(shapeNodes), True)
                    pm.setAttr("{0}.overrideColor".format(shapeNodes), color)
                except:
                    om.MGlobal.displayWarning("Failed to override color: {0}".format(shapeNodes))
    return True


def ad_lib_ctrl_color(ctrl, color):
    list_relatives = []
    for item in ctrl:
        list_relatives = pm.listRelatives(item, s=1)[0]
        pm.setAttr(list_relatives + '.ove', 1)
        pm.setAttr(list_relatives + '.ovc', color)

    return list_relatives


def ad_lib_ctrl_shape(shape, size_ctrl, tag_number):
    scale_shape = [[size_ctrl * i for i in j] for j in shape]
    create_curve = pm.curve(d=1, p=scale_shape)
    ad_lib_tagging_controller_code(create_curve, tag_number)
    pm.addAttr(create_curve, ln='AD_Controller', at='bool')
    pm.setAttr(create_curve + '.AD_Controller', 1)

    return create_curve

def ad_lib_tagging_controller_code(ctrl, tag_number):
    #attributes = pm.attributeQuery('AD_Controller_Tag', n=ctrl, ex=True)
    pm.addAttr(ctrl, ln='AD_Controller_Tag', at='long')
    pm.setAttr(ctrl + '.AD_Controller_Tag', tag_number, l=True)

def ad_lib_tagging(ctrl):
    attributes = pm.attributeQuery('AD_Controller', n=ctrl, ex=True)
    if attributes:
        pm.setAttr(ctrl + '.AD_Controller', 1)
    else:
        pm.addAttr(ctrl, ln='AD_Controller', at='bool')
        pm.setAttr(ctrl + '.AD_Controller', 1)


def ad_lib_untagging(ctrl):
    attributes = pm.attributeQuery('AD_Controller', n=ctrl, ex=True)
    if attributes:
        pm.setAttr(ctrl + '.AD_Controller', 0)
    else:
        pm.addAttr(ctrl, ln='AD_Controller', at='bool')
        pm.setAttr(ctrl + '.AD_Controller', 0)
