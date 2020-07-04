import math
import os
from __builtin__ import reload

import maya.OpenMaya as om
import maya.cmds as mc
import pymel.core as pm

from rigging.tools import AD_utils as ut

reload(ut)


def list_of_floats_matrix(axis_x, axis_y, axis_z, obj):
    obj_target = pm.ls(obj)
    getMatrix = obj_target[0].getMatrix()

    translate = []
    for i in getMatrix:
        translate.extend(i)

    listing = [list(vector_obj(axis_x)), 0.0,
               list(vector_obj(axis_y)), 0.0,
               list(vector_obj(axis_z)), 0.0,
               translate[-4:]]

    # listing[0], listing[2] = listing[2], listing[0]

    flat = []
    for a in listing:
        if isinstance(a, list):
            flat.extend(a)
        else:
            flat.append(a)

    return flat


def listing_float_matrix(obj, obj_shape, translation=False):
    obj_target = pm.ls(obj, obj_shape)
    get_matrix = obj_target[0].getMatrix()
    get_matrix_shape = obj_target[1].getMatrix()

    translate = []
    for i in get_matrix_shape:
        translate.extend(i)

    flat = []
    for a in get_matrix:
        flat.extend(a)

    if not translation:
        del flat[-4:]
        flat.extend(translate[-4:])
    else:
        return flat

    return flat


def decompose_matrix(obj_selection, obj, translation=False):
    listOfFloats = listing_float_matrix(obj_selection, obj, translation=translation)

    # create MMatrix from list
    mm = om.MMatrix()
    om.MScriptUtil.createMatrixFromList(listOfFloats, mm)

    # create MTransformationMatrix from MMatrix
    mt = om.MTransformationMatrix(mm)

    # translation is easy to obtain
    translate = mt.translation(om.MSpace.kWorld)

    # rotation needs to go past Quaternion representation due to API limitation
    rotate = mt.rotation().asEulerRotation()

    # rotation in degrees
    rotation = rotate * (180 / math.pi)

    # for scale we need to utilize MScriptUtil to deal with the native double pointers
    scale_util = om.MScriptUtil()
    scale_util.createFromList([0, 0, 0], 3)
    scaleVec = scale_util.asDoublePtr()
    mt.getScale(scaleVec, om.MSpace.kWorld)
    scale = [om.MScriptUtil.getDoubleArrayItem(scaleVec, i) for i in range(0, 3)]

    translate = mc.move(translate.x, translate.y, translate.z, obj)

    rotation = mc.rotate(rotation.x, rotation.y, rotation.z, obj)

    # scale = mc.scale(scale.x, scale.y, scale.z, obj)

    return {'rotation': rotation,
            'translation': translate,
            'scale': scale}


def decompose_matrix_axis(axis_x, axis_y, axis_z, obj):
    list_of_floats = list_of_floats_matrix(axis_x, axis_y, axis_z, obj)

    # create MMatrix from list
    mm = om.MMatrix()
    om.MScriptUtil.createMatrixFromList(list_of_floats, mm)

    # create MTransformationMatrix from MMatrix
    mt = om.MTransformationMatrix(mm)

    # translation is easy to obtain
    translate = mt.translation(om.MSpace.kWorld)

    # rotation needs to go past Quaternion representation due to API limitation
    rotate = mt.rotation().asEulerRotation()

    # rotation in degrees
    rotation = rotate * (180 / math.pi)

    # for scale we need to utilize MScriptUtil to deal with the native double pointers
    scale_util = om.MScriptUtil()
    scale_util.createFromList([0, 0, 0], 3)
    scale_vector = scale_util.asDoublePtr()
    mt.getScale(scale_vector, om.MSpace.kWorld)
    scale = [om.MScriptUtil.getDoubleArrayItem(scale_vector, i) for i in range(0, 3)]

    translate = mc.move(translate.x, translate.y, translate.z, obj)

    rotation = mc.rotate(rotation.x, rotation.y, rotation.z, obj)

    # scale = mc.scale(scale.x, scale.y, scale.z, obj)

    return {'rotation': rotation,
            'translation': translate,
            'scale': scale}


def split_evenly(obj_base, obj_tip, prefix, side=None, split=1, base_tip=False):
    base_xform = mc.xform(obj_base, q=1, ws=1, t=1)
    tip_xform = mc.xform(obj_tip, q=1, ws=1, t=1)

    base_vector = om.MVector(base_xform[0], base_xform[1], base_xform[2])
    tip_vector = om.MVector(tip_xform[0], tip_xform[1], tip_xform[2])

    split_vector = (tip_vector - base_vector)
    segment_vector = (split_vector / (split + 1.0))

    segment_location = (base_vector + segment_vector)

    list = []
    new_list = []
    for i in range(0, split):
        segment = mc.duplicate(obj_base)
        new_name = mc.rename(segment, str('%s%01d%s_%s' % (prefix, (i + 1), side, 'ref')))
        list.append(new_name)
        mc.move(segment_location.x, segment_location.y, segment_location.z, new_name)
        segment_location = segment_location + segment_vector
    if base_tip:
        base = mc.duplicate(obj_base)
        tip = mc.duplicate(obj_tip)
        list.insert(0, base[0])
        list.insert(split + 1, tip[0])
        for i in list:
            new_name = mc.rename(i, '%s%s%s_%s' % (prefix, str(list.index(i) + 1).zfill(2), side, 'splt'))
            new_list.append(new_name)
    else:
        for i in list:
            new_name = mc.rename(i, '%s%s%s_%s' % (prefix, str(list.index(i) + 1).zfill(2), side, 'splt'))
            new_list.append(new_name)

    return new_list


def vector_obj(string, multiply=1.0):
    """
    Convert string to vector.
        args:
            string = string to be converted ('x', 'y', '+z', etc..)

        return: vector
    """

    if isinstance(string, str) == False:
        try:
            string = str(string)
        except:
            return None

    if string == '+x' or string == 'x':
        return pm.dt.Vector(multiply, 0, 0)
    elif string == '+y' or string == 'y':
        return pm.dt.Vector(0, multiply, 0)
    elif string == '+z' or string == 'z':
        return pm.dt.Vector(0, 0, multiply)
    elif string == '-x':
        return pm.dt.Vector(multiply * -1, 0, 0)
    elif string == '-y':
        return pm.dt.Vector(0, multiply * -1, 0)
    elif string == '-z':
        return pm.dt.Vector(0, 0, multiply * -1)
    else:
        return None


def create_data_folder():
    # wfn = mc.file( q = True , sn = True )
    query_file_path = pm.sceneName()
    tmp_array = query_file_path.split('/')
    tmp_array[-2] = 'data'

    data_field = '/'.join(tmp_array[0:-1])

    if not os.path.isdir(data_field):
        os.mkdir(data_field)

    return data_field


def get_selection(sel_type='transform', num=1):
    """
    Get user selection util.
        args:
            selType = Type of object to filter(string)
            num = Number of return object to expect
        return:
            PyNode, list of PyNode
    """

    # if num == 0:
    # return

    if sel_type == 'any':
        sels = pm.ls(sl=True)
    else:
        sels = pm.ls(sl=True, type=sel_type)

    if sels:
        if num == 'inf':
            return sels
        elif num == 1:
            return sels[0]
        else:
            return sels[:num]


def get_vector(obj=None):
    if not obj:
        obj = get_selection()

    m = obj.worldMatrix.get()
    return {'x': pm.dt.Vector(m[0][0], m[0][1], m[0][2]),
            'y': pm.dt.Vector(m[1][0], m[1][1], m[1][2]),
            'z': pm.dt.Vector(m[2][0], m[2][1], m[2][2]),
            't': pm.dt.Vector(m[3][0], m[3][1], m[3][2])}


def str_vector(vec):
    """
    Convert vector to string.
        args:
            vec = vector to convert. list(x, y, z) or pm.dt.Vector

        return: vector (str)
    """

    if isinstance(vec, pm.dt.Vector) == False:
        try:
            vec = pm.dt.Vector(vec)
        except:
            return
    vec.normalize()

    if vec == pm.dt.Vector(1, 0, 0):
        return '+x'
    elif vec == pm.dt.Vector(0, 1, 0):
        return '+y'
    elif vec == pm.dt.Vector(0, 0, 1):
        return '+z'
    elif vec == pm.dt.Vector(-1, 0, 0):
        return '-x'
    elif vec == pm.dt.Vector(0, -1, 0):
        return '-y'
    elif vec == pm.dt.Vector(0, 0, -1):
        return '-z'
    else:
        return ''


def str_vec(vec):
    """
    Convert vector to string.
        args:
            vec = vector to convert. list(x, y, z) or pm.dt.Vector

        return: vector (str)
    """

    if isinstance(vec, pm.dt.Vector) == False:
        try:
            vec = pm.dt.Vector(vec)
        except:
            return
    vec.normalize()

    if vec == pm.dt.Vector(1, 0, 0):
        return '+x'
    elif vec == pm.dt.Vector(0, 1, 0):
        return '+y'
    elif vec == pm.dt.Vector(0, 0, 1):
        return '+z'
    elif vec == pm.dt.Vector(-1, 0, 0):
        return '-x'
    elif vec == pm.dt.Vector(0, -1, 0):
        return '-y'
    elif vec == pm.dt.Vector(0, 0, -1):
        return '-z'
    else:
        return ''


def convert_to_matrix(obj):
    pos = mc.xform(get_selection(obj), q=1, ws=1, t=1, r=1)
    # poleVecPos = getPoleVecPos(rootJointPos, midJointPos, endJointPos, length)
    return pos


def cross_axis(a, b):
    aVec = vector_obj(a)
    bVec = vector_obj(b)
    cross = aVec.cross(bVec)
    crossStr = str_vector(cross)
    return crossStr


def direction_pivot(obj, aim_axis='', up_axis=''):
    # Aim axis positive and up axis positive
    if (aim_axis == '+y' and up_axis == '+x'):
        decompose_matrix_axis('y', 'x', 'z', obj)

    elif (aim_axis == '+y' and up_axis == '+z'):
        decompose_matrix_axis('z', 'x', 'y', obj)

    elif (aim_axis == '+x' and up_axis == '+y'):
        decompose_matrix_axis('x', 'y', 'z', obj)

    elif (aim_axis == '+x' and up_axis == '+z'):
        decompose_matrix_axis('x', '-z', 'y', obj)

    elif (aim_axis == '+z' and up_axis == '+x'):
        decompose_matrix_axis('y', 'z', 'x', obj)

    elif (aim_axis == '+z' and up_axis == '+y'):
        decompose_matrix_axis('-z', 'y', 'x', obj)

    # Aim axis negative and up axis negative
    elif (aim_axis == '-y' and up_axis == '-x'):
        decompose_matrix_axis('-y', '-x', '-z', obj)

    elif (aim_axis == '-y' and up_axis == '-z'):
        decompose_matrix_axis('z', '-x', '-y', obj)

    elif (aim_axis == '-x' and up_axis == '-y'):
        decompose_matrix_axis('-x', '-y', 'z', obj)

    elif (aim_axis == '-x' and up_axis == '-z'):
        decompose_matrix_axis('-x', '-z', 'y', obj)

    elif (aim_axis == '-z' and up_axis == '-x'):
        decompose_matrix_axis('-y', 'z', '-x', obj)

    elif (aim_axis == '-z' and up_axis == '-y'):
        decompose_matrix_axis('-z', '-y', '-x', obj)

    # Aim axis positive and up axis negative
    elif (aim_axis == '+y' and up_axis == '-x'):
        decompose_matrix_axis('-y', 'x', 'z', obj)

    elif (aim_axis == '+y' and up_axis == '-z'):
        decompose_matrix_axis('-z', 'x', 'y', obj)

    elif (aim_axis == '+x' and up_axis == '-y'):
        decompose_matrix_axis('x', '-y', 'z', obj)

    elif (aim_axis == '+x' and up_axis == '-z'):
        decompose_matrix_axis('x', 'z', 'y', obj)

    elif (aim_axis == '+z' and up_axis == '-x'):
        decompose_matrix_axis('-y', '-z', 'x', obj)

    elif (aim_axis == '+z' and up_axis == '-y'):
        decompose_matrix_axis('z', '-y', 'x', obj)

    # Aim axis negative and up axis positive
    elif (aim_axis == '-y' and up_axis == '+x'):
        decompose_matrix_axis('y', '-x', 'z', obj)

    elif (aim_axis == '-y' and up_axis == '+z'):
        decompose_matrix_axis('-z', '-x', 'y', obj)

    elif (aim_axis == '-x' and up_axis == '+y'):
        decompose_matrix_axis('-x', 'y', 'z', obj)

    elif (aim_axis == '-x' and up_axis == '+z'):
        decompose_matrix_axis('-x', 'z', 'y', obj)

    elif (aim_axis == '-z' and up_axis == '+x'):
        decompose_matrix_axis('y', '-z', 'x', obj)

    elif (aim_axis == '-z' and up_axis == '+y'):
        decompose_matrix_axis('z', 'y', 'x', obj)

    else:
        return mc.warning(
            'Some pivot direction might be not working. Please check naming the value %s as aim axis and %s as '
            'up axis?' % (aim_axis, up_axis))

    # If it is joint then freezing the rotation
    if mc.nodeType(obj) == 'joint':
        mc.makeIdentity(obj, apply=True, r=True, n=1)
    else:
        return obj
