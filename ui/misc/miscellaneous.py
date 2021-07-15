import pymel.core as pm

def ad_lib_matrix_scale(value):
    value_float = float(value)
    matrix = pm.dt.Matrix([1.0+value_float, 0.0, 0.0, 0.0,
                           0.0, 1.0+value_float, 0.0, 0.0,
                           0.0, 0.0, 1.0+value_float, 0.0,
                           0.0, 0.0, 0.0, 1.0])
    return matrix

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

def ad_lib_scaling_controller_matrix(ctrl_shape, current_value):
    object_curve = pm.PyNode(ctrl_shape)
    for cv in object_curve.getShape().cv:

        pm.xform(cv, os=True, m=(ad_lib_matrix_scale(current_value*0.1)))