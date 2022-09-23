"""
listing the joint
"""
from __future__ import absolute_import

import maya.OpenMaya as om
import maya.cmds as cmds

from rigging.library.utils import controller as rlu_controller
from rigging.tools import utils as rt_utils


def hierarchy(top_joint, with_end_joints=True):
    list_joint = cmds.listRelatives(top_joint, type='joint', ad=True)
    list_joint.append(top_joint)
    list_joint.reverse()

    complete_joint = list_joint[:]

    if not with_end_joints:
        complete_joint = [j for j in list_joint if cmds.listRelatives(j, c=1, type='joint')]

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
    for i, v in enumerate(cmds.ls('%s.cv[0:*]' % crv, fl=True)):
        # create joint
        cmds.select(cl=1)
        joint = cmds.joint(n='%s%02d%s' % (rt_utils.prefix_name(crv), (i + 1), '_jnt'), rad=0.1)
        pos = cmds.xform(v, q=1, ws=1, t=1)
        cmds.xform(joint, ws=1, t=pos)
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
            new_transform = rlu_controller.Control(match_obj_first_position=i, prefix=rt_utils.prefix_name(i) + 'Jnt',
                                                   shape=rlu_controller.CUBE,
                                                   groups_ctrl=['Zro'], ctrl_size=2.0,
                                                   ctrl_color='blue', gimbal=False, lock_channels=['r', 's', 'v'],
                                                   connection=['parent'])
            motion_path = cmds.pathAnimation(new_transform.parent_control[0], fractionMode=True, fa='z', ua='x',
                                             wut='objectrotation',
                                             wuo=world_up_loc,
                                             c=curve,
                                             n=rt_utils.prefix_name(i) + '_mpt')

            transform.append(new_transform.parent_control[0])
            controls.append(new_transform.control)
            new_transform = new_transform.control

        else:
            new_transform = cmds.createNode('transform', n=rt_utils.prefix_name(i) + 'Jnt_grp')
            cmds.parent(i, new_transform)
            motion_path = cmds.pathAnimation(new_transform, fractionMode=True, fa='z', ua='x',
                                             wut='objectrotation',
                                             wuo=world_up_loc,
                                             c=curve,
                                             n=rt_utils.prefix_name(i) + '_mpt')
            transform.append(new_transform)
            controls.append(newJnt[0])

        cmds.cutKey(motion_path + '.u', time=())
        cmds.setAttr(motion_path + '.u', ranges)
        motion_paths.append(motion_path)

        cmds.setAttr(i + '.translate', 0, 0, 0, type='double3')
        cmds.setAttr(i + '.rotate', 0, 0, 0, type='double3')

        joints.append(i)

        if delete_group:
            cmds.parent(joints[n], w=True)
            cmds.delete(new_transform + '.tx', icn=1)
            cmds.delete(new_transform + '.ty', icn=1)
            cmds.delete(new_transform + '.tz', icn=1)
            cmds.delete(new_transform + '.rx', icn=1)
            cmds.delete(new_transform + '.ry', icn=1)
            cmds.delete(new_transform + '.rz', icn=1)
            cmds.xform(new_transform, ws=True, ro=(0, 0, 0))
            cmds.delete(motion_path)
            cmds.delete(new_transform)

            if n > 0:
                cmds.parent(joints[n], joints[n - 1])

            cmds.joint(joints[0], e=True, oj='xyz', sao='yup', ch=True, zso=True)

    if spline_ik:
        if not delete_group:
            cmds.error('Spline Ik cannot be created. Please delGrp set to True in order to remove group parent joints!')
        else:
            ikHdl = cmds.ikHandle(sj=joints[0], ee=joints[-1], c=curve, sol='ikSplineSolver', ccv=False,
                                  n=rt_utils.prefix_name(curve) + '_ikh')

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
        cmds.select(cl=1)

        new_jnt = cmds.joint(n=rt_utils.prefix_name(curve) + str(i + 1).zfill(2) + '_jnt')
        if ctrl:

            new_transform = rlu_controller.Control(match_obj_first_position=new_jnt,
                                                   prefix=rt_utils.prefix_name(curve) + str(i + 1).zfill(2) + 'Jnt',
                                                   shape=rlu_controller.CUBE,
                                                   groups_ctrl=['Zro'], ctrl_size=2.0,
                                                   ctrl_color='blue', gimbal=False, lock_channels=['r', 's', 'v'],
                                                   connection=['parent'])
            motion_path = cmds.pathAnimation(new_transform.parent_control[0], fractionMode=True, fa='z', ua='x',
                                             wut='objectrotation',
                                             wuo=worldUp_locator,
                                             c=curve,
                                             n=rt_utils.prefix_name(curve) + str(i + 1).zfill(2) + '_mpt')
            transform.append(new_transform.parent_control[0])
            controls.append(new_transform.control)
            new_transform = new_transform.control

        else:
            new_transform = cmds.createNode('transform',
                                            n=rt_utils.prefix_name(curve) + str(i + 1).zfill(2) + 'Jnt_grp')
            cmds.parent(new_jnt, new_transform)
            cmds.xform(new_jnt, ws=1, t=(0, 0, 0), ro=(0, 0, 0))
            motion_path = cmds.pathAnimation(new_transform, fractionMode=True, fa='z', ua='x',
                                             wut='objectrotation',
                                             wuo=world_up_loc,
                                             c=curve,
                                             n=rt_utils.prefix_name(curve) + str(i + 1).zfill(2) + '_mpt')
            transform.append(new_transform)
            controls.append(new_jnt)

        joints.append(new_jnt)

        cmds.cutKey(motion_path + '.u', time=())
        cmds.setAttr(motion_path + '.u', ranges)
        motion_paths.append(motion_path)

        if delete_group:
            cmds.parent(joints[i], w=True)
            cmds.delete(new_transform + '.tx', icn=1)
            cmds.delete(new_transform + '.ty', icn=1)
            cmds.delete(new_transform + '.tz', icn=1)
            cmds.delete(new_transform + '.rx', icn=1)
            cmds.delete(new_transform + '.ry', icn=1)
            cmds.delete(new_transform + '.rz', icn=1)
            cmds.xform(new_transform, ws=True, ro=(0, 0, 0))
            cmds.delete(motion_path)
            cmds.delete(new_transform)

            if i > 0:
                cmds.parent(joints[i], joints[i - 1])

            cmds.joint(joints[0], e=True, oj='xyz', sao='yup', ch=True, zso=True)

    if spline_ik:
        if not delete_group:
            cmds.error('Spline Ik cannot be created. Please delGrp set to True in order to remove group parent joints!')
        else:
            ik_hdl = cmds.ikHandle(sj=joints[0], ee=joints[-1], c=curve, sol='ikSplineSolver', ccv=False,
                                   n=rt_utils.prefix_name(curve) + '_ikh')
    if del_worldUp_loc:
        cmds.delete(worldUp_locator)

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
