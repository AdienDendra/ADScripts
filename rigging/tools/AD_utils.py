import re
from string import digits

import maya.cmds as mc
import pymel.core as pm

# CONTROL FUNCTION
SUFFIXES = {
    'mesh': 'geo',
    'joint': 'jnt',
    'follicle': 'fol',
    'nurbsCurve': 'crv',
    'camera': None

}
GROUP = 'grp'
GIMBAL = 'Gmbl'


# CONNECTING THE FOLLICLE
def connect_follicle_rotation(follicleNode, follicleTransf):
    conn = mc.connectAttr(follicleNode + '.outRotate', follicleTransf + '.rotate')
    return conn


def connect_follicle_translation(follicleNode, follicleTransf):
    conn = mc.connectAttr(follicleNode + '.outTranslate', follicleTransf + '.translate')
    return conn


def dic_connect_follicle(connect, follicleNode, follicleTransf):
    dic = {'rotateConn': connect_follicle_rotation,
           'transConn': connect_follicle_translation,
           }
    for con in connect:
        if con in dic.keys():
            dic[con](follicleNode, follicleTransf)
        else:
            return mc.warning("Your %s key name is wrong. Please check on the key list connection!" % con)
    return dic


########################################## follicle object #####################################################
# CREATE FOLLICLE BASED ON VERTEX OR EDGE OR FACE SELECTED
def create_follicle(snap=None, jntDel=None, scale=None, connectFol=['']):
    """
    :param snap: bool, if True, every vertex has follicle Else, calculate local position of all vertex selected then create one joint
    :param jntDel: bool, delete the joints after create follicle or dont
    :param connectFol: str, list connection. rotateConn or transConn or both
    :return: follicle object transform
    """
    sel = mc.ls(sl=1)

    if not sel:
        return mc.error('please select the object!')

    else:
        if snap:
            obj_sel = joint(True)

        else:
            obj_sel = joint(False)

        obj = name_query_shape(sel)
        type_obj = mc.listRelatives(obj, s=1)[0]

        rename = None
        for i in obj_sel:
            global closest_node
            # If the inputSurface is of type 'nurbsSurface', connect the surface to the closest node
            if mc.objectType(type_obj) == 'nurbsSurface':
                closest_node = mc.createNode('closestPointOnSurface')
                mc.connectAttr((type_obj + '.local'), (closest_node + '.inputSurface'))

            # If the inputSurface is of type 'mesh', connect the surface to the closest node
            elif mc.objectType(type_obj) == 'mesh':
                closest_node = mc.createNode('closestPointOnMesh')
                mc.connectAttr((type_obj + '.outMesh'), (closest_node + '.inMesh'))
            else:
                mc.error('please check your type object. Object must be either nurbs or mesh')

            # query locator position
            xform = mc.xform(i, ws=True, t=True, q=True)

            # set the position of node according to the loc
            mc.setAttr(closest_node + '.inPositionX', xform[0])
            mc.setAttr(closest_node + '.inPositionY', xform[1])
            mc.setAttr(closest_node + '.inPositionZ', xform[2])

            # create follicle
            follicle_node = mc.createNode('follicle')

            # query the transform follicle
            follicle_transform = mc.listRelatives(follicle_node, type='transform', p=True)

            # connecting the shape follicle to transform follicle
            dic_connect_follicle(connectFol, follicle_node, follicle_transform[0])

            # connect the world matrix mesh to the follicle shape
            mc.connectAttr(obj + '.worldMatrix', follicle_node + '.inputWorldMatrix')

            # connect the output mesh of mesh to input mesh follicle
            if mc.objectType(type_obj) == 'nurbsSurface':
                mc.connectAttr((type_obj + '.local'), (follicle_node + '.inputSurface'))

            # If the inputSurface is of type 'mesh', connect the surface to the follicle
            if mc.objectType(type_obj) == 'mesh':
                mc.connectAttr(type_obj + '.outMesh', follicle_node + '.inputMesh')

            # # connect the output mesh of mesh to input mesh follicle
            # mc.connectAttr(objMesh + '.outMesh', follicleNode + '.inputMesh')

            # turn off the simulation follicle
            mc.setAttr(follicle_node + '.simulationMethod', 0)

            # get u and v output closest point on mesh node
            par_u = mc.getAttr(closest_node + '.result.parameterU')
            par_v = mc.getAttr(closest_node + '.result.parameterV')

            # connect output closest point on mesh node to follicle
            mc.setAttr(follicle_node + '.parameterU', par_u)
            mc.setAttr(follicle_node + '.parameterV', par_v)

            # parent constraint locator to follicle
            # mc.parent(follicleTransform[0], objLoc, mo=1)

            # rename follicle
            rename = mc.rename(follicle_transform, '%s_%s' % (prefix_name(i), 'fol'))

            mc.delete(closest_node)

            if scale:
                scale_constraint(scale, rename, mo=1)

            if not jntDel:
                continue
            else:
                mc.delete(i)

        return rename


############################################ follicle based on selection ######################################
# CREATE FOLLICLE BASED ON OBJECT (JOINT OR TRANSFORM) SELECTED
def create_follicle_selection(obj_select, obj_mesh, connect=None, prefix=None, suffix=None, scale=None, connect_follicle=['']):
    obj_mesh = mc.listRelatives(obj_mesh, s=1)[0]

    closest_node = None
    # If the inputSurface is of type 'nurbsSurface', connect the surface to the closest node
    if mc.objectType(obj_mesh) == 'nurbsSurface':
        closest_node = mc.createNode('closestPointOnSurface')
        mc.connectAttr((obj_mesh + '.local'), (closest_node + '.inputSurface'))

    # If the inputSurface is of type 'mesh', connect the surface to the closest node
    elif mc.objectType(obj_mesh) == 'mesh':
        closest_node = mc.createNode('closestPointOnMesh')
        mc.connectAttr((obj_mesh + '.outMesh'), (closest_node + '.inMesh'))
    else:
        mc.error('please check your type object. Object must be either nurbs or mesh')

    # query object selection
    xform = mc.xform(obj_select, ws=True, t=True, q=True)

    # set the position of node according to the loc
    mc.setAttr(closest_node + '.inPositionX', xform[0])
    mc.setAttr(closest_node + '.inPositionY', xform[1])
    mc.setAttr(closest_node + '.inPositionZ', xform[2])

    # create follicle
    follicle_node = mc.createNode('follicle')

    # query the transform follicle
    follicle_transform = mc.listRelatives(follicle_node, type='transform', p=True)

    # connecting the shape follicle to transform follicle
    dic_connect_follicle(connect_follicle, follicle_node, follicle_transform[0])

    # connect the world matrix mesh to the follicle shape
    mc.connectAttr(obj_mesh + '.worldMatrix[0]', follicle_node + '.inputWorldMatrix')

    # connect the output mesh of mesh to input mesh follicle
    if mc.objectType(obj_mesh) == 'nurbsSurface':
        mc.connectAttr((obj_mesh + '.local'), (follicle_node + '.inputSurface'))

    # If the inputSurface is of type 'mesh', connect the surface to the follicle
    if mc.objectType(obj_mesh) == 'mesh':
        mc.connectAttr(obj_mesh + '.outMesh', follicle_node + '.inputMesh')

    # turn off the simulation follicle
    mc.setAttr(follicle_node + '.simulationMethod', 0)

    # get u and v output closest point on mesh node
    par_u = mc.getAttr(closest_node + '.result.parameterU')
    par_v = mc.getAttr(closest_node + '.result.parameterV')

    # connect output closest point on mesh node to follicle
    mc.setAttr(follicle_node + '.parameterU', par_u)
    mc.setAttr(follicle_node + '.parameterV', par_v)

    # deleting node
    mc.delete(closest_node)

    # rename follicle
    if prefix or suffix:
        follicle_transform = mc.rename(follicle_transform, '%s_%s' % (prefix_name(prefix), suffix))
    else:
        follicle_transform = mc.rename(follicle_transform, '%s_%s' % (prefix_name(obj_select), 'fol'))

    if scale:
        scale_constraint(scale, follicle_transform, mo=1)

    # listing the shape of follicle
    follicle_shape = mc.listRelatives(follicle_transform, s=1)[0]

    if connect:
        connection(connect, follicle_transform, obj_select)
    else:
        return follicle_transform, follicle_shape

    return follicle_transform, follicle_shape


################################## follicle multiple object #####################################################
# APPENDING RESULT OF CREATEFOLLICLESET FUNCTION
def follicle_set(obj_select, obj_mesh, prefix=None, suffix=None, connect_follicle=['']):
    grps = []
    grps.extend(create_follicle_selection(obj_select, obj_mesh, prefix=prefix, suffix=suffix,
                                          connect_follicle=connect_follicle))
    return {'folTrans': grps[0],
            'folShape': grps[1]}


############################################ follicle based on u and v value ######################################
# CREATE FOLLICLE BASED ON POSITION OF VALUE V AND U
def create_follicle_UV(prefix='follicle', suffix='', input_surface=[], connect_follicle=[''], scale_grp='', uVal=0.5,
                       vVal=0.5, hide=0):
    # Create a follicle
    follicle_shape = mc.createNode('follicle')

    # Get the transform of the follicle
    follicle_translation = mc.listRelatives(follicle_shape, type='transform', p=True)

    # If the inputSurface is of type 'nurbsSurface', connect the surface to the follicle
    if mc.objectType(input_surface[0]) == 'nurbsSurface':
        mc.connectAttr((input_surface[0] + '.local'), (follicle_shape + '.inputSurface'))

    # If the inputSurface is of type 'mesh', connect the surface to the follicle
    elif mc.objectType(input_surface[0]) == 'mesh':
        mc.connectAttr((input_surface[0] + '.outMesh'), (follicle_shape + '.inputMesh'))

    else:
        mc.error('please check your type object. Object must be either nurbs or mesh')

    # Connect the worldMatrix of the surface into the follicleShape
    mc.connectAttr((input_surface[0] + '.worldMatrix[0]'), (follicle_shape + '.inputWorldMatrix'))

    # connecting the shape follicle to transform follicle
    dic_connect_follicle(connect_follicle, follicle_shape, follicle_translation[0])

    # Set the uValue and vValue for the current follicle
    mc.setAttr((follicle_shape + '.parameterU'), uVal)
    mc.setAttr((follicle_shape + '.parameterV'), vVal)

    # If it was set to be hidden, hide the follicle
    if hide:
        mc.setAttr((follicle_shape + '.visibility'), 1)

    # If a scale-group was defined and exists
    if scale_grp and mc.objExists(scale_grp):
        # Connect the scale-group to the follicle
        mc.connectAttr((scale_grp + '.scale'), (follicle_translation + '.scale'))

    follicle_translation = mc.rename(follicle_translation, '%s_%s' % (prefix_name(prefix), suffix))

    follicle_shape = mc.listRelatives(follicle_translation, s=1)[0]

    # Return the follicle and it's shape
    return follicle_translation, follicle_shape


###################################### locator and joint ####################################################################
# CREATE JOINT BASED ON VERTEX OR EDGE OR FACE SELECTED
def joint(snap=None, poly_constraint=False, delete_constraint=True):
    sel = mc.ls(sl=1, fl=1)
    jnts = []
    if snap:
        for number, i in enumerate(sel):
            mc.select(cl=1)
            obj_name = name_query_shape(sel)
            jnt = mc.joint()
            name_jnt = '%s%02d_%s' % (prefix_name(obj_name), number + 1, 'jnt')
            rnm = mc.rename(jnt, name_jnt)
            if poly_constraint:
                pm.select(i, rnm, r=True)
                # pm.mel.eval('doCreatePointOnPolyConstraintArgList 2 {   "0" ,"0" ,"0" ,"1" ,"" ,"1" ,"0" ,"0" ,"0" ,"0" };')
                pm.runtime.PointOnPolyConstraint()
                if delete_constraint:
                    cons = mc.listRelatives(rnm, ad=1)
                    mc.delete(cons)

            else:
                cls = mc.cluster(i)
                mc.parentConstraint(cls, rnm, mo=0)
                jnts.append(rnm)
                mc.delete(cls)

    else:
        mc.select(cl=1)
        obj_name = name_query_shape(sel)
        jnt = mc.joint()
        cls = mc.cluster(sel)
        name_jnt = '%s_%s' % (prefix_name(obj_name), 'jnt')
        rnm = mc.rename(jnt, name_jnt)
        mc.parentConstraint(cls, rnm, mo=0)
        mc.delete(cls)
        jnts.append(rnm)

    return jnts


# CREATE LOCATOR BASED ON VERTEX OR EDGE OR FACE SELECTED
def locator(snap=None, poly_constraint=False, delete_constraint=True):
    sel = mc.ls(sl=1, fl=1)
    locs = []
    if snap:
        for number, i in enumerate(sel):
            mc.select(cl=1)
            obj_name = name_query_shape(sel)
            loc = mc.spaceLocator()
            name_locator = '%s%02d_%s' % (prefix_name(obj_name), number + 1, 'loc')
            rnm = mc.rename(loc, name_locator)
            if poly_constraint:
                pm.select(i, rnm, r=True)
                # pm.mel.eval('doCreatePointOnPolyConstraintArgList 2 {   "0" ,"0" ,"0" ,"1" ,"" ,"1" ,"0" ,"0" ,"0" ,"0" };')
                pm.runtime.PointOnPolyConstraint()
                if delete_constraint:
                    cons = mc.listRelatives(rnm, ad=1)[1::2]
                    mc.delete(cons)

            else:
                cls = mc.cluster(i)
                mc.parentConstraint(cls, rnm, mo=0)
                mc.delete(cls)

            locs.append(rnm)

    else:
        mc.select(cl=1)
        obj_name = name_query_shape(sel)
        loc = mc.spaceLocator()
        cls = mc.cluster(sel)
        nameLoc = '%s_%s' % (prefix_name(obj_name), 'loc')
        rnm = mc.rename(loc, nameLoc)
        mc.parentConstraint(cls, rnm, mo=0)
        mc.delete(cls)
        locs.append(rnm)

    return locs


def connect_mesh(obj_origin, obj_target):
    obj_shape = mc.listRelatives(obj_origin, s=1)[0]
    obj_tgt_shape = mc.listRelatives(obj_target, s=1)[-1]
    connect_mesh = mc.connectAttr('%s.outMesh' % (obj_shape), '%s.inMesh' % (obj_tgt_shape))
    return connect_mesh


################################################# query joint connection of skin ####################################

def query_skin_name(obj):
    # get the skincluster name
    relatives = mc.listRelatives(obj, type="shape")
    skin_cluster = mc.listConnections(relatives, type="skinCluster")
    if not skin_cluster:
        return mc.error("Please add your skin cluster before run the script!")
    else:
        for obj in skin_cluster:
            return obj


########################################################################################################################

def group_null(name):
    grp = mc.createNode('transform', name=name)
    return grp


# GET VALUE OF POINT OF VERTEX CURVE
def get_transform_shape_position(shape):
    # if a transform get the shape
    if mc.nodeType(shape) == 'transform':
        shape_node = mc.listRelatives(shape, s=True)[0]

    if mc.nodeType(shape) == 'nurbCurve':
        shape_node = shape

    # get cv list
    points = mc.ls('%s.cv[0:*]' % shape_node, fl=True)

    # get point position
    point_position = []

    for point in points:
        point_position.append(mc.pointPosition(point, l=True))

    return point_position


def scale_curve(size_obj, shape):
    scaleShp = [[size_obj * i for i in j] for j in shape]
    return scaleShp


def controller(shape):
    createCrv = mc.curve(d=1, p=shape)
    return createCrv


def name_query_shape(obj):
    for i in obj:
        objs = i.split('.')[0]
        return objs


def check_duplicate_name():
    # def renameDuplicates():
    # Find all objects that have the same shortname as another
    # We can indentify them because they have | in the name
    duplicates = [f for f in mc.ls() if '|' in f]
    # Sort them by hierarchy so that we don't rename a parent before a child.
    duplicates.sort(key=lambda obj: obj.count('|'), reverse=True)

    # if we have duplicates, rename them
    if duplicates:
        for name in duplicates:
            # extract the module name
            m = re.compile("[^|]*$").search(name)
            shortname = m.group(0)

            # extract the numeric suffix
            m2 = re.compile(".*[^0-9]").match(shortname)
            if m2:
                strip_suffix = m2.group(0)
            else:
                strip_suffix = shortname

            # rename, adding '#' as the suffix, which tells maya to find the next available number
            newname = mc.rename(name, (strip_suffix + "#"))
            print("renamed %s to %s" % (name, newname))

        return "Renamed %s objects with duplicated name." % len(duplicates)
    else:
        return "No Duplicates"


def rename_object(object):
    for obj in object:
        split_name = obj.split('|')[-1]
        list_relatives = mc.listRelatives(obj, c=1) or []
        if len(list_relatives) == 1:
            child = list_relatives[0]
            obj_type = mc.objectType(child)
        else:
            obj_type = mc.objectType(obj)

        suffix = SUFFIXES.get(obj_type, GROUP)

        if not suffix:
            continue

        if '_' in split_name:
            continue

        if split_name.endswith('_' + suffix):
            continue

        new_name = "%s_%s" % (split_name, suffix)
        mc.rename(split_name, new_name)
        index = object.index(obj)
        object[index] = obj.replace(split_name, new_name)

    return object


def prefix_named(obj):
    if '|' in obj:
        objs = obj.split('|')[-1:]
        for l in objs:
            get_prefix_name = l.split('_')[0]
    else:
        for i in obj:
            get_prefix_name = i.split('_')[0]
    return get_prefix_name


def prefix_names(obj):
    objs = obj.split('|')[0]
    for l in objs:
        get_prefix_name = l.split('_')[0]
        return get_prefix_name


def prefix_name_no_split(obj):
    for i in obj:
        get_prefix_name = i.split('_')[0]
    return get_prefix_name


# def prefix_name(obj):
#     if '_' in obj:
#         get_prefix_name = obj.split('_')[0]
#         return get_prefix_name
#     else:
#         return obj

def prefix_name(obj):
    if '_' in obj:
        get_prefix_name = obj.split('_')[:-1]
        joining = '_'.join(get_prefix_name)
        return joining
    else:
        print obj

def suffix_name(obj):
    objs = obj.split('|')[-1:]
    for l in objs:
        get_len = l.split('_')
        if len(get_len) > 1:
            get_suffix_name = get_len[1]
            return get_suffix_name
        else:
            get_suffix_no = l.replace(l, '')
            return get_suffix_no


def suffix_name_zero(obj):
    objs = obj.split('|')[-1:]
    for l in objs:
        get_suffix_no = l.replace(l, '')
        return get_suffix_no


def obj_duplicate_then_rename(obj_duplicate='', value_prefix='', key_prefix='',
                              suffix='', selection=False, **kwargs):
    list_rename = []
    list_rename_origin = []
    if selection:
        select_obj = mc.ls(sl=1)
        duplicate = mc.duplicate(select_obj, rc=True)
        for i in duplicate:
            rename_origin = mc.rename(i, '%s%s_%s' % (prefix_name(i), key_prefix, suffix))
            rename = mc.rename(rename_origin, '%s%s_%s' % (prefix_name(i), value_prefix, suffix))
            list_rename.append(rename)
            list_rename_origin.append(rename_origin)
    else:
        duplicate = mc.duplicate(obj_duplicate, rc=True)
        for i in duplicate:
            replace_tmp = i.replace('Tmp', key_prefix)
            rename_origin = mc.rename(i, '%s_%s' % (prefix_name(replace_tmp), suffix))

            replace_key_prefix = rename_origin.replace(key_prefix, value_prefix)
            rename = mc.rename(rename_origin, replace_key_prefix)

            list_rename.append(rename)
            list_rename_origin.append(rename_origin)

    return list_rename_origin, list_rename


def group_parent(groups, prefix, suffix, number='', side=''):
    # create group hierarchy
    grps = []
    for i in range(len(groups)):
        grps.append(mc.createNode('transform', n="%s%s%s%s%s_%s" % (prefix, suffix, groups[i], number, side, GROUP)))

        if i > 0:
            parent_object(grps[i - 1], grps[i])

    return grps


def group_object(grp_name_list, obj_base, match_pos=None, side=''):
    list_relatives = mc.listRelatives(obj_base, ap=1)

    cGrp = group_parent(grp_name_list, '%s' % prefix_name(obj_base), suffix_name(obj_base).title(), side)

    if match_pos:
        match_position(match_pos, cGrp[0])
        match_scale(match_pos, cGrp[0])

    if list_relatives == None:
        parent_object(cGrp[-1], obj_base)
    else:
        # parent group offset to list relatives
        parent_object(list_relatives, cGrp[0])
        # parent obj to grp offset
        parent_object(cGrp[-1], obj_base)

    return cGrp


def group_object_outside(add_suffix, obj_base):
    # create group hierarchy
    grps = []
    for i in obj_base:
        grps.append(mc.createNode('transform', n="%s%s_%s" % (prefix_name(i), add_suffix, GROUP)))

    for i, item in enumerate(obj_base):
        match_position(item, grps[i])

        if i > 0:
            parent_object(grps[i - 1], grps[i])

    return grps


def group_follow_object(grp_name_list, obj_base, suffix_name):
    grps = []
    for i in obj_base:
        origin_grp = group_parent(grp_name_list, '%s' % prefix_name(i), suffix_name.title())

        match_position(obj_base, origin_grp[0])

        match_scale(obj_base, origin_grp[0])

        grps.append(origin_grp)

    return grps[0]


def parent_under_list(obj, obj_target):
    lR = mc.listRelatives(obj_target, c=1, f=1)

    for i in lR:
        parent_object(obj, i)
    parent_object(obj_target, obj)
    return lR


def match_position(obj_base, obj_target):
    mc.delete(parent_constraint(obj_base, obj_target, mo=0))


def match_scale(obj_base, obj_target):
    mc.delete(scale_constraint(obj_base, obj_target, mo=0))


def parent_or_connect_attr_object(grp_name_list, obj_base, obj_target, match_postion):
    get_translation = get_attribute_translate(obj_base)
    get_rotation = get_attribute_rotate(obj_base)
    get_scale = get_attribute_scale(obj_base)

    if get_translation == True and get_rotation == True and get_scale == True:
        connect_attr_translate(obj_target, obj_base)
        connect_attr_rotate(obj_target, obj_base)
        connect_attr_scale(obj_target, obj_base)
    else:
        group_object(grp_name_list, obj_base, match_postion)
        connect_attr_translate(obj_target, obj_base)
        connect_attr_rotate(obj_target, obj_base)
        connect_attr_scale(obj_target, obj_base)

    return get_translation, get_rotation, get_scale


def get_attribute_translate(obj):
    obj_translate = mc.getAttr('%s.translate' % obj)[0]
    if obj_translate[0] == 0.0000 and obj_translate[1] == 0.00000 and obj_translate[2] == 0.00000:
        return True
    else:
        return False


def get_attribute_rotate(obj):
    obj_rotate = mc.getAttr('%s.rotate' % obj)[0]
    if obj_rotate[0] == 0.00000 and obj_rotate[1] == 0.00000 and obj_rotate[2] == 0.00000:
        return True
    else:
        return False


def get_attribute_scale(obj):
    obj_scale = mc.getAttr('%s.scale' % obj)[0]
    if obj_scale[0] == 1.00000 and obj_scale[1] == 1.00000 and obj_scale[2] == 1.0000:
        return True
    else:
        return False


def parent_object(objBase, objTgt):
    parent_object = mc.parent(objTgt, objBase)
    return parent_object


def parent_constraint(obj_base, obj_target, mo=1):
    par_constraint = mc.parentConstraint(obj_base, obj_target, mo=mo)[0]
    split = par_constraint.split('_')
    x = '_'.join(split[:-1])
    n = x.replace(x, x + '_pac')
    new_name = [mc.rename(par_constraint, n)]
    return new_name


def orient_constraint(obj_base, obj_target, mo=1):
    orient_constraint = mc.orientConstraint(obj_base, obj_target, mo=mo)[0]
    split = orient_constraint.split('_')
    x = '_'.join(split[:-1])
    n = x.replace(x, x + '_oc')
    new_name = [mc.rename(orient_constraint, n)]
    return new_name


def point_constraint(obj_base, obj_target, mo=1):
    point_constraint = mc.pointConstraint(obj_base, obj_target, mo=mo)[0]
    split = point_constraint.split('_')
    x = '_'.join(split[:-1])
    n = x.replace(x, x + '_pc')
    new_name = [mc.rename(point_constraint, n)]
    return new_name


def scale_constraint(obj_base, obj_target, mo=1):
    scale_constraint = mc.scaleConstraint(obj_base, obj_target, mo=mo)[0]
    split = scale_constraint.split('_')
    x = '_'.join(split[:-1])
    n = x.replace(x, x + '_sc')
    new_name = [mc.rename(scale_constraint, n)]

    return new_name


def parent_scale_constraint(obj_base, obj_target, mo=0):
    par_cons = parent_constraint(obj_base, obj_target, mo=mo)
    scl_cons = scale_constraint(obj_base, obj_target)
    return par_cons, scl_cons


def constraint_rename(constraint):
    name_list = []
    if len(constraint) > 1:
        for i in constraint:
            type = mc.nodeType(i)
            if type == 'parentConstraint' or type == 'pointConstraint' or type == 'orientConstraint' or type == 'scaleConstraint' \
                    or type == 'poleVectorConstraint' or type == 'aimConstraint':
                split = i.split('_')
                x = '_'.join(split[:-1])
                if type == 'parentConstraint':
                    n = x.replace(x, x + '_pac')
                    new_name = [mc.rename(i, n)]
                    name_list.append(new_name)
                if type == 'pointConstraint':
                    n = x.replace(x, x + '_pc')
                    new_name = [mc.rename(i, n)]
                    name_list.append(new_name)
                if type == 'orientConstraint':
                    n = x.replace(x, x + '_oc')
                    new_name = [mc.rename(i, n)]
                    name_list.append(new_name)
                if type == 'scaleConstraint':
                    n = x.replace(x, x + '_sc')
                    new_name = [mc.rename(i, n)]
                    name_list.append(new_name)
                if type == 'poleVectorConstraint':
                    n = x.replace(x, x + '_pvc')
                    new_name = [mc.rename(i, n)]
                    name_list.append(new_name)
                if type == 'aimConstraint':
                    n = x.replace(x, x + '_aim')
                    new_name = [mc.rename(i, n)]
                    name_list.append(new_name)
            else:
                print(type)
                mc.error('The object(s) is not a constraint node!')
    else:
        type = mc.nodeType(constraint)
        if type == 'parentConstraint' or type == 'pointConstraint' or type == 'orientConstraint' or type == 'scaleConstraint' \
                or type == 'poleVectorConstraint' or type == 'aimConstraint':
            split = constraint[0].split('_')
            x = '_'.join(split[:-1])
            if type == 'parentConstraint':
                n = x.replace(x, x + '_pac')
                name_list = [mc.rename(constraint, n)]
            if type == 'pointConstraint':
                n = x.replace(x, x + '_pc')
                name_list = [mc.rename(constraint, n)]
            if type == 'orientConstraint':
                n = x.replace(x, x + '_oc')
                name_list = [mc.rename(constraint, n)]
            if type == 'scaleConstraint':
                n = x.replace(x, x + '_sc')
                name_list = [mc.rename(constraint, n)]
            if type == 'poleVectorConstraint':
                n = x.replace(x, x + '_pvc')
                name_list = [mc.rename(constraint, n)]
            if type == 'aimConstraint':
                n = x.replace(x, x + '_aim')
                name_list = [mc.rename(constraint, n)]
        else:
            print(type)
            mc.error('The object(s) is not a constraint node!')
    return name_list


def connect_matrix_offset(obj_base, obj_target):
    matrix_node = mc.pluginInfo('matrixNodes.mll', query=True, loaded=True)
    if not matrix_node:
        mc.loadPlugin('matrixNodes.mll')

    if mc.objExists(obj_base + '.offsetMtx'):
        mc.deleteAttr(obj_base + '.offsetMtx')

    list_relatives = mc.listRelatives(obj_base, f=1, ap=1)[0]
    split = list_relatives.split('|')
    first_parent = filter(None, split)[0]

    prefix = prefix_name(obj_target)
    multiply_matrix = mc.createNode('multMatrix', n=prefix + '_mmtx')

    multiply_matrix_offset = mc.createNode('multMatrix')

    decompose_matrix = mc.createNode('decomposeMatrix', n=prefix + '_dmtx')

    mc.addAttr(obj_base, ln='offsetMtx', at='matrix')

    mc.connectAttr(obj_base + '.worldMatrix[0]', multiply_matrix + '.matrixIn[0]')
    mc.connectAttr(first_parent + '.worldInverseMatrix[0]', multiply_matrix + '.matrixIn[1]')

    mc.connectAttr(multiply_matrix + '.matrixSum', multiply_matrix_offset + '.matrixIn[0]')
    mc.connectAttr(obj_target + '.worldMatrix[0]', multiply_matrix_offset + '.matrixIn[1]')
    mc.connectAttr(multiply_matrix_offset + '.matrixSum', obj_base + '.offsetMtx')

    mc.disconnectAttr(multiply_matrix_offset + '.matrixSum', obj_base + '.offsetMtx')
    mc.disconnectAttr(multiply_matrix + '.matrixSum', multiply_matrix_offset + '.matrixIn[0]')
    mc.disconnectAttr(obj_target + '.worldMatrix[0]', multiply_matrix_offset + '.matrixIn[1]')
    mc.delete(multiply_matrix_offset)

    mc.disconnectAttr(obj_base + '.worldMatrix[0]', multiply_matrix + '.matrixIn[0]')
    mc.connectAttr(obj_base + '.offsetMtx', multiply_matrix + '.matrixIn[0]')
    mc.connectAttr(obj_base + '.worldMatrix[0]', multiply_matrix + '.matrixIn[2]')

    mc.connectAttr(multiply_matrix + '.matrixSum', decompose_matrix + '.inputMatrix')

    return decompose_matrix


def connect_matrix(obj_base, obj_target):
    list_relatives = mc.listRelatives(obj_base, f=1, ap=1)[0]
    split = list_relatives.split('|')
    first_parent = filter(None, split)[0]

    prefix = prefix_name(obj_target)
    multiply_matrix = mc.createNode('multMatrix', n=prefix + '_mmtx')

    decompose_matrix = mc.createNode('decomposeMatrix', n=prefix + '_dmtx')

    mc.connectAttr(obj_base + '.worldMatrix[0]', multiply_matrix + '.matrixIn[0]')
    mc.connectAttr(first_parent + '.worldInverseMatrix[0]', multiply_matrix + '.matrixIn[1]')

    mc.connectAttr(multiply_matrix + '.matrixSum', decompose_matrix + '.inputMatrix')

    return decompose_matrix


def connect_matrix_translation_offset(obj_base, obj_target):
    matrix = connect_matrix_offset(obj_base, obj_target)
    mc.connectAttr(matrix + '.outputTranslate', obj_target + '.translate')


def connect_matrix_rotation_offset(obj_base, obj_target):
    matrix = connect_matrix_offset(obj_base, obj_target)
    mc.connectAttr(matrix + '.outputRotate', obj_target + '.rotate')


def connect_matrix_scale_offset(obj_base, obj_target):
    matrix = connect_matrix_offset(obj_base, obj_target)
    mc.connectAttr(matrix + '.outputScale', obj_target + '.scale')


def connect_matrix_trans_rot_offset(obj_base, obj_target):
    matrix = connect_matrix_offset(obj_base, obj_target)
    mc.connectAttr(matrix + '.outputTranslate', obj_target + '.translate')
    mc.connectAttr(matrix + '.outputRotate', obj_target + '.rotate')


def connect_matrix_all_offset(obj_base, obj_target):
    matrix = connect_matrix_offset(obj_base, obj_target)
    mc.connectAttr(matrix + '.outputTranslate', obj_target + '.translate')
    mc.connectAttr(matrix + '.outputRotate', obj_target + '.rotate')
    mc.connectAttr(matrix + '.outputScale', obj_target + '.scale')


def connect_matrix_translation(obj_base, obj_target):
    matrix = connect_matrix(obj_base, obj_target)
    mc.connectAttr(matrix + '.outputTranslate', obj_target + '.translate')


def connect_matrix_rotation(obj_base, obj_target):
    matrix = connect_matrix(obj_base, obj_target)
    mc.connectAttr(matrix + '.outputRotate', obj_target + '.rotate')


def connect_matrix_scale(obj_base, obj_target):
    matrix = connect_matrix(obj_base, obj_target)
    mc.connectAttr(matrix + '.outputScale', obj_target + '.scale')


def connect_matrix_trans_rot(obj_base, obj_target):
    matrix = connect_matrix(obj_base, obj_target)
    mc.connectAttr(matrix + '.outputTranslate', obj_target + '.translate')
    mc.connectAttr(matrix + '.outputRotate', obj_target + '.rotate')


def connect_matrix_all(obj_base, obj_target):
    matrix = connect_matrix(obj_base, obj_target)
    mc.connectAttr(matrix + '.outputTranslate', obj_target + '.translate')
    mc.connectAttr(matrix + '.outputRotate', obj_target + '.rotate')
    mc.connectAttr(matrix + '.outputScale', obj_target + '.scale')


def connect_attr_translate(objBase, objTgt):
    list_relatives = mc.listRelatives(objTgt, ap=1)
    if list_relatives == True:
        translate_attr = mc.connectAttr(objBase + '.translate', list_relatives + '.translate')
    else:
        translate_attr = mc.connectAttr(objBase + '.translate', objTgt + '.translate')
    return translate_attr


def connect_attr_rotate(obj_base, obj_target):
    list_relatives = mc.listRelatives(obj_target, ap=1)
    if list_relatives == True:
        rotate_attr = mc.connectAttr(obj_base + '.rotate', list_relatives + '.rotate')
    else:
        rotate_attr = mc.connectAttr(obj_base + '.rotate', obj_target + '.rotate')
    return rotate_attr


def connect_part_object(obj_base_connection, target_connection, obj_name='', target_name=[''], channel_box=False,
                        keyable=False, select_obj=True):
    if select_obj:
        sel = mc.ls(sl=1)
        if isinstance(obj_base_connection, str) and sel:
            for i in range(len(sel)):
                if i > 0:
                    if not mc.objExists('%s.%s' % (sel[0], obj_base_connection)):
                        add_attr_transform(sel[0], obj_base_connection, 'long', edit=True, channel_box=channel_box,
                                           keyable=keyable, dv=1, min=0, max=1)
                        mc.connectAttr(sel[0] + ('.%s' % obj_base_connection), sel[i - 0] + ('.%s' % target_connection))
                    else:
                        mc.connectAttr(sel[0] + ('.%s' % obj_base_connection), sel[i - 0] + ('.%s' % target_connection))
        else:
            return mc.error('Please select at least two objects and the attribute name must be string!')
    else:
        for i in target_name:
            if not mc.objExists('%s.%s' % (obj_name, obj_base_connection)):
                add_attr_transform(obj_name, obj_base_connection, 'long', edit=True, channel_box=channel_box,
                                   keyable=keyable, dv=1, min=0, max=1)
                mc.connectAttr(obj_name + ('.%s' % obj_base_connection), i + ('.%s' % target_connection))
            else:
                mc.connectAttr(obj_name + ('.%s' % obj_base_connection), i + ('.%s' % target_connection))
        return obj_name + '.%s' % obj_base_connection


def connect_attr_scale(obj_base, obj_target):
    list_relatives = mc.listRelatives(obj_target, ap=1)
    if list_relatives == True:
        attr = mc.connectAttr(obj_base + '.scaleX', list_relatives + '.scaleX')
        attr = mc.connectAttr(obj_base + '.scaleY', list_relatives + '.scaleY')
        attr = mc.connectAttr(obj_base + '.scaleZ', list_relatives + '.scaleZ')

    else:
        attr = mc.connectAttr(obj_base + '.scaleX', obj_target + '.scaleX')
        attr = mc.connectAttr(obj_base + '.scaleY', obj_target + '.scaleY')
        attr = mc.connectAttr(obj_base + '.scaleZ', obj_target + '.scaleZ')
    return attr


def connect_attr_object(objBase, objTgt):
    connect_attr_translate(objBase, objTgt)
    connect_attr_rotate(objBase, objTgt)
    connect_attr_scale(objBase, objTgt)
    return


def connect_attr_translate_rotate(objBase, objTgt):
    connect_attr_translate(objBase, objTgt)
    connect_attr_rotate(objBase, objTgt)


def connection(connect, ctrl, obj):
    dic = {'parentCons': parent_constraint,
           'pointCons': point_constraint,
           'orientCons': orient_constraint,
           'scaleCons': scale_constraint,
           'parent': parent_object,
           'connectAttr': connect_attr_object,
           'connectTrans': connect_attr_translate,
           'connectOrient': connect_attr_rotate,
           'connectScale': connect_attr_scale,
           'connectMatrixAllOffset': connect_matrix_all_offset,
           'connectMatrixTransRotOffset': connect_matrix_trans_rot_offset,
           'connectMatrixTransOffset': connect_matrix_translation_offset,
           'connectMatrixRotOffset': connect_matrix_rotation_offset,
           'connectMatrixSclOffset': connect_matrix_scale_offset,
           'connectMatrixAll': connect_matrix_all,
           'connectMatrixTransRot': connect_matrix_trans_rot,
           'connectMatrixTrans': connect_matrix_translation,
           'connectMatrixRot': connect_matrix_rotation,
           'connectMatrixScl': connect_matrix_scale
           }
    rs = {}
    for con in connect:
        if con in dic.keys():
            rs[con] = dic[con](ctrl, obj)
        else:
            return mc.error("Your %s key name is wrong. Please check on the key list connection!" % con)
    return rs


def add_attr_message(obj_target, obj):
    mc.addAttr(obj_target, ln='root', at='message')
    attr = mc.connectAttr('%s.message' % obj, '%s.root' % obj_target)
    return attr


# add attribute on shape
def add_attr_transform_shape(obj, attr_name, attr_type, keyable=False, edit=False, channel_box=False, **kwargs):
    if mc.nodeType(obj) == "transform":
        try:
            list_relatives = mc.listRelatives(obj, shapes=True)[0]
            mc.addAttr(list_relatives, ln=attr_name, at=attr_type, **kwargs)
            mc.setAttr('%s.%s' % (list_relatives, attr_name), e=edit, k=keyable, cb=channel_box)
            return list_relatives
        except IndexError:
            return mc.warning("Could not find shape in %s" % obj)
    else:
        return


# add attribute on transform
def add_attr_transform(obj, attr_name, attr_type, edit=False, keyable=False, channel_box=False, **kwargs):
    if mc.nodeType(obj) == "transform":
        mc.addAttr(obj, ln=attr_name, at=attr_type, **kwargs)
        mc.setAttr('%s.%s' % (obj, attr_name), e=edit, k=keyable, cb=channel_box)
        return attr_name
    else:
        mc.error('object is not transform')


# GENERAL FUNCTION: ADD ATTRIBUTE(S) ON MULTIPLE OBJECTS
def add_attribute(objects=[], long_name='', nice_name='', separator=False, keyable=False, channel_box=False, **kwargs):
    # For each object
    for obj in objects:
        # For each attribute
        for x in range(0, len(long_name)):
            # See if a niceName was defined
            attr_nice = '' if not nice_name else nice_name[x]
            # If the attribute does not exists
            if not mc.attributeQuery(long_name[x], node=obj, exists=True):
                # Add the attribute
                mc.addAttr(obj, longName=long_name[x], niceName=attr_nice, **kwargs)
                # If lock was set to True
                mc.setAttr((obj + '.' + long_name[x]), k=keyable, e=1, cb=channel_box) if separator else mc.setAttr(
                    (obj + '.' + long_name[x]), k=keyable, e=1, cb=channel_box)
    return long_name[0]


def set_color(ctrl, color):
    color_dic = {
        'gray': 0,
        'black': 1,
        'darkGray': 2,
        'lightGray': 3,
        'darkRed': 4,
        'darkBlue': 5,
        'blue': 6,
        'darkGreen': 7,
        'darkPurple': 8,
        'purple': 9,
        'brown': 10,
        'darkBrown': 11,
        'dullRed': 12,
        'red': 13,
        'green': 14,
        'navy': 15,
        'white': 16,
        'yellow': 17,
        'turquoiseBlue': 18,
        'turquoiseGreen': 19,
        'lightPink': 20,
        'lightBrown': 21,
        'lightYellow': 22,
        'dullGreen': 23,
        'chocholate': 24,
        'dullYellow': 25,
        'greenYellow': 26,
        'greenBlue': 27,
        'blueGreen': 28,
        'lightNavy': 29,
        'violet': 30,
        'ruby': 31
    }
    if color in color_dic.keys():
        list_relatives = mc.listRelatives(ctrl, s=1)[0]
        mc.setAttr(list_relatives + '.ove', 1)
        mc.setAttr(list_relatives + '.ovc', color_dic[color])
        return list_relatives
    else:
        return mc.warning("Could not find %s name color. Please check color name!" % color)


def lock_hide_attr_object(obj, attr_name):
    mc.setAttr('%s.%s' % (obj, attr_name), l=True, k=False)


def lock_hide_attr(lock_channel, ctrl):
    attr_lock_list = []
    for lc in lock_channel:
        if lc in ['t', 'r', 's']:
            for axis in ['x', 'y', 'z']:
                at = lc + axis
                attr_lock_list.append(at)
        else:
            attr_lock_list.append(lc)
    for at in attr_lock_list:
        mc.setAttr(ctrl + '.' + at, l=1, k=0)
    return attr_lock_list


def lock_attr(lock_channel, ctrl):
    attrLockList = []
    for lc in lock_channel:
        if lc in ['t', 'r', 's']:
            for axis in ['x', 'y', 'z']:
                at = lc + axis
                attrLockList.append(at)
        else:
            attrLockList.append(lc)

    for at in attrLockList:
        mc.setAttr(ctrl + '.' + at, l=1)

    return attrLockList


def joint_on_crv_sub(curve='', number_of_jnt=None, del_poc=None, spline_ik=None):
    num = (1.0 / number_of_jnt)
    joints = []
    point_on_crv = []
    for i in range(0, number_of_jnt + 1):
        ranges = num * i
        pointCurve_node = mc.shadingNode('pointOnCurveInfo', asUtility=1,
                                         n=prefix_name(curve) + str(i + 1).zfill(2) + '_poc')
        point_on_crv.append(pointCurve_node)
        mc.connectAttr(curve + '.worldSpace[0]', pointCurve_node + '.inputCurve')
        mc.setAttr(pointCurve_node + '.parameter', ranges)
        jnts = mc.joint(n=prefix_name(curve) + str(i + 1).zfill(2) + '_jnt')
        mc.connectAttr(pointCurve_node + '.result.position', jnts + '.translate')
        mc.disconnectAttr(pointCurve_node + '.result.position', jnts + '.translate')

        joints.append(jnts)
        if i > 0:
            mc.parent(joints[i], joints[i - 1])

        mc.joint(joints[0], e=True, oj='xyz', sao='yup', ch=True, zso=True)

    ik_hdl = None
    if spline_ik:
        ik_hdl = mc.ikHandle(sj=joints[0], ee=joints[-1], c=curve, sol='ikSplineSolver', ccv=False,
                             n=prefix_name(curve) + '_ikh')
    if del_poc:
        mc.delete(point_on_crv)

    return {'joints': joints,
            'poc': point_on_crv,
            'ikHdl': ik_hdl,
            'curve': curve}
