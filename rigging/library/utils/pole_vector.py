from __builtin__ import reload

import maya.OpenMaya as om
import maya.cmds as mc

import rigging.tools.AD_utils as au

reload(au)

def get_poleVec_position(root_pos, mid_pos, end_pos, length):
    root_jnt_vector  = om.MVector(root_pos[0], root_pos[1], root_pos[2])
    mid_jnt_vector   = om.MVector(mid_pos[0], mid_pos[1], mid_pos[2])
    end_jnt_vector   = om.MVector(end_pos[0], end_pos[1], end_pos[2])

    line = (end_jnt_vector - root_jnt_vector)
    point = (mid_jnt_vector - root_jnt_vector)

    scale_value  = (line * point) / (line * line)
    projection_vector     = line * scale_value + root_jnt_vector

    root_to_mid_length    = (mid_jnt_vector - root_jnt_vector).length()
    mid_to_end_length     = (end_jnt_vector - mid_jnt_vector).length()
    total_length     = root_to_mid_length + mid_to_end_length

    pole_vector_position      = (mid_jnt_vector - projection_vector).normal() * length + mid_jnt_vector

    return pole_vector_position

def get_ikh_poleVec_position(ikHandle, length):
    ik_jnt_list = mc.ikHandle(ikHandle, q=1, jointList = True)
    ik_jnt_list.append(mc.listRelatives(ik_jnt_list[-1], children=1, type='joint')[0])

    root_joint_position = mc.xform(ik_jnt_list[0], q=1, ws=1, t=1)
    mid_joint_position  = mc.xform(ik_jnt_list[1], q=1, ws=1, t=1)
    end_joint_position  = mc.xform(ik_jnt_list[2], q=1, ws=1, t=1)

    pole_vec_position = get_poleVec_position(root_joint_position, mid_joint_position, end_joint_position, length)

    return pole_vec_position

def create_poleVec_locator(ikHandle, constraint=False, length=1):
    locator     = mc.spaceLocator()
    position = mc.move(get_ikh_poleVec_position(ikHandle, length).x, get_ikh_poleVec_position(ikHandle, length).y,
                       get_ikh_poleVec_position(ikHandle, length).z, locator)
    locator = mc.rename(position, '%s_%s' % (au.prefix_name(ikHandle), 'pv'))

    if constraint:
        poleVector_constraint = mc.poleVectorConstraint(locator, ikHandle)
        au.constraint_rename(poleVector_constraint)

    return locator, ikHandle