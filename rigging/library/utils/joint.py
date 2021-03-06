"""
listing the joint
"""
from __builtin__ import reload

import maya.OpenMaya as om
import maya.cmds as mc

from rigging.library.utils import controller as ct
from rigging.library.utils import transform as tf
from rigging.tools import AD_utils as au

reload(au)
reload(ct)
reload(tf)


def hierarchy(top_joint, with_end_joints=True):
    list_joint = mc.listRelatives(top_joint, type='joint', ad=True)
    list_joint.append(top_joint)
    list_joint.reverse()

    complete_joint = list_joint[:]

    if not with_end_joints:
        complete_joint = [j for j in list_joint if mc.listRelatives(j, c=1, type='joint')]

    return complete_joint


def get_u_param(pnt=[], crv=None):
    point = om.MPoint(pnt[0], pnt[1], pnt[2])
    curveFn = om.MFnNurbsCurve(get_dag_path(crv))
    param_utill = om.MScriptUtil()
    param_ptr = param_utill.asDoublePtr()
    isOnCurve = curveFn.isPointOnCurve(point)
    if isOnCurve == True:

        curveFn.getParamAtPoint(point, param_ptr, 0.001, om.MSpace.kObject)
    else:
        point = curveFn.closestPoint(point, param_ptr, 0.001, om.MSpace.kObject)
        curveFn.getParamAtPoint(point, param_ptr, 0.001, om.MSpace.kObject)

    param = param_utill.getDouble(param_ptr)
    return param


def get_dag_path(object_name):
    if isinstance(object_name, list) == True:
        o_node_list = []
        for o in object_name:
            selection_list = om.MSelectionList()
            selection_list.add(o)
            o_node = om.MDagPath()
            selection_list.getDagPath(0, o_node)
            o_node_list.append(o_node)
        return o_node_list
    else:
        selection_list = om.MSelectionList()
        selection_list.add(object_name)
        o_node = om.MDagPath()
        selection_list.getDagPath(0, o_node)
        return o_node


def create_joint_lid(crv):
    all_joint = []
    all_locator = []
    ranges = []
    for i, v in enumerate(mc.ls('%s.cv[0:*]' % crv, fl=True)):
        # create joint
        mc.select(cl=1)
        joint = mc.joint(n='%s%02d%s' % (au.prefix_name(crv), (i + 1), '_jnt'), rad=0.1)
        pos = mc.xform(v, q=1, ws=1, t=1)
        mc.xform(joint, ws=1, t=pos)
        all_joint.append(joint)

        ranges.append(i)

    length = len(ranges)
    return all_joint, all_locator, ranges, length


def joint_on_curve(curve='', world_up_loc='', spline_ik=None, delete_group=True, ctrl=False):
    newJnt = create_joint_lid(curve)

    num = (1.0 / (int(newJnt[3]) - 1))
    transform = []
    controls = []
    motion_paths = []
    joints = []
    ikHdl = None

    for n, i in enumerate(newJnt[0]):
        ranges = num * n
        if ctrl:
            new_transform = ct.Control(match_obj_first_position=i, prefix=au.prefix_name(i) + 'Jnt', shape=ct.CUBE,
                                       groups_ctrl=['Zro'], ctrl_size=2.0,
                                       ctrl_color='blue', gimbal=False, lock_channels=['r', 's', 'v'],
                                       connection=['parent'])
            motion_path = mc.pathAnimation(new_transform.parent_control[0], fractionMode=True, fa='z', ua='x',
                                           wut='objectrotation',
                                           wuo=world_up_loc,
                                           c=curve,
                                           n=au.prefix_name(i) + '_mpt')

            transform.append(new_transform.parent_control[0])
            controls.append(new_transform.control)
            new_transform = new_transform.control

        else:
            new_transform = mc.createNode('transform', n=au.prefix_name(i) + 'Jnt_grp')
            mc.parent(i, new_transform)
            motion_path = mc.pathAnimation(new_transform, fractionMode=True, fa='z', ua='x',
                                           wut='objectrotation',
                                           wuo=world_up_loc,
                                           c=curve,
                                           n=au.prefix_name(i) + '_mpt')
            transform.append(new_transform)
            controls.append(newJnt[0])

        mc.cutKey(motion_path + '.u', time=())
        mc.setAttr(motion_path + '.u', ranges)
        motion_paths.append(motion_path)

        mc.setAttr(i + '.translate', 0, 0, 0, type='double3')
        mc.setAttr(i + '.rotate', 0, 0, 0, type='double3')

        joints.append(i)

        if delete_group:
            mc.parent(joints[n], w=True)
            mc.delete(new_transform + '.tx', icn=1)
            mc.delete(new_transform + '.ty', icn=1)
            mc.delete(new_transform + '.tz', icn=1)
            mc.delete(new_transform + '.rx', icn=1)
            mc.delete(new_transform + '.ry', icn=1)
            mc.delete(new_transform + '.rz', icn=1)
            mc.xform(new_transform, ws=True, ro=(0, 0, 0))
            mc.delete(motion_path)
            mc.delete(new_transform)

            if n > 0:
                mc.parent(joints[n], joints[n - 1])

            mc.joint(joints[0], e=True, oj='xyz', sao='yup', ch=True, zso=True)

    if spline_ik:
        if not delete_group:
            mc.error('Spline Ik cannot be created. Please delGrp set to True in order to remove group parent joints!')
        else:
            ikHdl = mc.ikHandle(sj=joints[0], ee=joints[-1], c=curve, sol='ikSplineSolver', ccv=False,
                                n=au.prefix_name(curve) + '_ikh')

        return {'joints': transform,
                'motionPath': motion_paths,
                'ctrl': controls,
                'ikHdl': ikHdl,
                'curve': curve}

    return {'joints': transform,
            'motionPath': motion_paths,
            'ctrl': controls,
            'ikHdl': ikHdl,
            'wUpLoc': newJnt[1],
            'curve': curve}


def joint_on_crv_with_num_jnt(curve='', world_up_loc='', number_of_jnt=None, spline_ik=None, delete_group=True,
                              ctrl=False, del_worldUp_loc=True):
    num = (1.0 / (number_of_jnt - 1))
    transform = []
    controls = []
    motion_paths = []
    joints = []
    ik_hdl = None
    worldUp_locator_grp = []
    worldUp_locator = None
    for i in range(0, number_of_jnt):
        ranges = num * i
        mc.select(cl=1)

        new_jnt = mc.joint(n=au.prefix_name(curve) + str(i + 1).zfill(2) + '_jnt')
        if ctrl:

            new_transform = ct.Control(match_obj_first_position=new_jnt,
                                       prefix=au.prefix_name(curve) + str(i + 1).zfill(2) + 'Jnt', shape=ct.CUBE,
                                       groups_ctrl=['Zro'], ctrl_size=2.0,
                                       ctrl_color='blue', gimbal=False, lock_channels=['r', 's', 'v'],
                                       connection=['parent'])
            motion_path = mc.pathAnimation(new_transform.parent_control[0], fractionMode=True, fa='z', ua='x',
                                           wut='objectrotation',
                                           wuo=worldUp_locator,
                                           c=curve,
                                           n=au.prefix_name(curve) + str(i + 1).zfill(2) + '_mpt')
            transform.append(new_transform.parent_control[0])
            controls.append(new_transform.control)
            new_transform = new_transform.control

        else:
            new_transform = mc.createNode('transform', n=au.prefix_name(curve) + str(i + 1).zfill(2) + 'Jnt_grp')
            mc.parent(new_jnt, new_transform)
            mc.xform(new_jnt, ws=1, t=(0, 0, 0), ro=(0, 0, 0))
            motion_path = mc.pathAnimation(new_transform, fractionMode=True, fa='z', ua='x',
                                           wut='objectrotation',
                                           wuo=world_up_loc,
                                           c=curve,
                                           n=au.prefix_name(curve) + str(i + 1).zfill(2) + '_mpt')
            transform.append(new_transform)
            controls.append(new_jnt)

        joints.append(new_jnt)

        mc.cutKey(motion_path + '.u', time=())
        mc.setAttr(motion_path + '.u', ranges)
        motion_paths.append(motion_path)

        if delete_group:
            mc.parent(joints[i], w=True)
            mc.delete(new_transform + '.tx', icn=1)
            mc.delete(new_transform + '.ty', icn=1)
            mc.delete(new_transform + '.tz', icn=1)
            mc.delete(new_transform + '.rx', icn=1)
            mc.delete(new_transform + '.ry', icn=1)
            mc.delete(new_transform + '.rz', icn=1)
            mc.xform(new_transform, ws=True, ro=(0, 0, 0))
            mc.delete(motion_path)
            mc.delete(new_transform)

            if i > 0:
                mc.parent(joints[i], joints[i - 1])

            mc.joint(joints[0], e=True, oj='xyz', sao='yup', ch=True, zso=True)

    if spline_ik:
        if not delete_group:
            mc.error('Spline Ik cannot be created. Please delGrp set to True in order to remove group parent joints!')
        else:
            ik_hdl = mc.ikHandle(sj=joints[0], ee=joints[-1], c=curve, sol='ikSplineSolver', ccv=False,
                                 n=au.prefix_name(curve) + '_ikh')
    if del_worldUp_loc:
        mc.delete(worldUp_locator)

        return {'joints': transform,
                'motionPath': motion_paths,
                'ctrl': controls,
                'ikHdl': ik_hdl,
                'curve': curve}

    return {'joints': transform,
            'motionPath': motion_paths,
            'ctrl': controls,
            'ikHdl': ik_hdl,
            'wUpLoc': worldUp_locator,
            'wUpLocGrp': worldUp_locator_grp,
            'curve': curve}
