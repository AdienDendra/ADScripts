import maya.OpenMaya as om
import pymel.core as pm
import ad_controller_shp as ac


# def ad_scaling_controller(size_obj, ctrl_shape):
#     # shape_node = pm.listRelatives(ctrl_shape, s=True)[0]
#     points = pm.ls('%s.cv[0:*]' % ctrl_shape, fl=True)
#     for point in points:
#         position = pm.pointPosition(point, l=True)
#
#         pm.setAttr('%s.xValue' % point, position[0]*size_obj )
#         pm.setAttr('%s.yValue' % point, position[1]*size_obj )
#         pm.setAttr('%s.zValue' % point, position[2]*size_obj )
# def ad_name_query_shape(obj):
#     for i in obj:
#         objs = i.split('.')[0]
#         return objs

def ad_list_connections_object(object):
    # list connection
    if len(object) > 1:
        om.MGlobal.displayError('Please select one object!')
    else:
        pass

    select=[]
    for item in object:
        source = pm.listConnections(object, p=True, d=False, s=True, c=True)
        if source:
            for node_source in source:
                connection_source_object = node_source[1].split('.')[0]
                connection_source_transform = node_source[1].split('.')[1]
                node_source_type = pm.nodeType(connection_source_object)

                connection_destination_object = node_source[0].split('.')[0]
                connection_destination_transform = node_source[0].split('.')[1]

                if node_source_type == 'parentConstraint':
                    object_select = pm.listConnections(connection_source_object + '.target[0].targetParentMatrix', d=0, s=1)
                    om.MGlobal.displayInfo( "------ >>> %s attribute has parent constraint connection from '%s'!" % (item, source[0]))
                elif node_source_type == 'pointConstraint':
                    object_select = pm.listConnections(connection_source_object + '.target[0].targetParentMatrix', d=0, s=1)
                    om.MGlobal.displayInfo( "------ >>> %s attribute has point constraint connection from '%s'!" % (item, source[0]))
                elif node_source_type == 'orientConstraint':
                    object_select = pm.listConnections(connection_source_object + '.target[0].targetParentMatrix', d=0, s=1)
                    om.MGlobal.displayInfo( "------ >>> %s attribute has orient constraint connection from '%s'!" % (item, source[0]))
                elif node_source_type == 'scaleConstraint':
                    object_select = pm.listConnections(connection_source_object + '.target[0].targetParentMatrix', d=0, s=1)
                    om.MGlobal.displayInfo( "------ >>> %s attribute has scale constraint connection from '%s'!" % (item, source[0]))
                elif node_source_type == 'transform':
                    object_select = connection_source_object
                    om.MGlobal.displayInfo( "------ >>> %s %s attribute has connection from '%s' %s object!" % (
                    connection_destination_object,
                    connection_destination_transform,
                    connection_source_object,
                    connection_source_transform))
                else:
                    object_select = om.MGlobal.displayWarning( 'The object connection is not constraint or direct connection!')

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
    present = pm.PyNode(ctrl_shape)
    for cv in present.getShape().cv:
        position_os = pm.xform(cv, q=True, os=True, t=True)

        vector_os = pm.dt.Vector(position_os[0], position_os[1], position_os[2])
        vector_optimum = vector_os * (current_value * 0.2)
        vector_optimum = vector_os + vector_optimum

        # vector_ws = pm.dt.Vector(position_ws[0], position_ws[1], position_ws[2])
        #
        # sub_vector = vector_ws - vector_os
        # vector_optimum = ((vector_os * (current_value * 1)) + sub_vector)

        # def ad_scaling_controller(size_obj, ctrl_shape):
        # shape_node = pm.listRelatives(ctrl_shape, s=True)[0]
        #     points = pm.ls('%s.cv[0:*]' % ctrl_shape, fl=True)
        #     for point in points:
        # position = pm.pointPosition(cv, l=True)
        #
        pm.setAttr('%s.xValue' % cv, vector_optimum[0])
        pm.setAttr('%s.yValue' % cv, vector_optimum[1])
        pm.setAttr('%s.zValue' % cv, vector_optimum[2])

        # pm.move(vector_os[0] + vector_optimum[0],
        #         vector_os[1] + vector_optimum[1],
        #         vector_os[2] + vector_optimum[2],
        #         cv)


# import pymel.core as pm
# class Test(object):
#     def __init__(self):
#         self.WINDOW_NAME = 'test'
#         self.prevValue = 0
#     def UI(self):
#         with pm.window(self.WINDOW_NAME, widthHeight=(200, 200))  as self.mainWindow:
#             with pm.rowColumnLayout(nc=1):
#                 self.slider = pm.floatSlider( w=500,min=-10, max=10, value=0, step=0.0001, changeCommand=pm.Callback(self.action) , dragCommand=pm.Callback(self.dragSlider))
#     def action(self):
#         print('action')
#         pm.floatSlider(self.slider, edit=True, v=0)
#         self.prevValue = 0
#     def dragSlider(self):
#         value = pm.floatSlider(self.slider, q=True, v=True)
#         deltaValue = (value - self.prevValue)
#         self.scaleAction( deltaValue )
#         self.prevValue = value
#     def scaleAction(self, deltaValue):
#         objList = [pm.PyNode(node) for node in pm.ls(selection=True)]
#         for obj in objList:
#             currentScale = obj.scaleX.get()
#             obj.scale.set([currentScale+deltaValue, currentScale+deltaValue,currentScale+deltaValue])
#             pm.makeIdentity(apply=True, s=1, n=0)
# main = Test()
# main.UI()

#
# def ad_scale_controller(delta_value):
#     objList = [pm.PyNode(node) for node in pm.ls(selection=True)]
#     for obj in objList:
#         currentScale = obj.scaleX.get()
#         obj.scale.set([currentScale+delta_value, currentScale+delta_value, currentScale+delta_value])
#         pm.makeIdentity(apply=True, s=1, n=0)

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


def ad_lib_ctrl_shape(shape, size_ctrl):
    scale_shape = [[size_ctrl * i for i in j] for j in shape]
    create_curve = pm.curve(d=1, p=scale_shape)
    pm.addAttr(create_curve, ln='AD_Controller', at='bool')
    pm.setAttr(create_curve + '.AD_Controller', 1)

    return create_curve


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
