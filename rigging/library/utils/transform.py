"""
add object group parent

"""
from __future__ import absolute_import

import re

import maya.cmds as cmds

from rigging.tools import pythonVersion as rt_pythonVersion, utils as rt_utils


def reorder_number(prefix, side_RGT, side_LFT):
    # get the number
    new_prefix = reposition_side(object=prefix, side_RGT=side_RGT, side_LFT=side_LFT)
    try:
        patterns = [r'\d+']
        prefix_number = rt_utils.prefix_name(new_prefix)
        for p in patterns:
            prefix_number = re.findall(p, prefix_number)[0]
    except:
        prefix_number = ''

    # get the prefix without number
    prefix_no_number = rt_pythonVersion.translation_string(new_prefix)

    return prefix_no_number, prefix_number


def create_parent_transform(parent_list, object, match_position, prefix, suffix, side=''):
    list_relatives = cmds.listRelatives(object, ap=1)
    try:
        patterns = [r'\d+']
        prefix_number = rt_utils.prefix_name(prefix)
        for p in patterns:
            prefix_number = re.findall(p, prefix_number)[0]
    except:
        prefix_number = ''

    # get the prefix without number
    prefix_no_number = rt_pythonVersion.translation_string(prefix)

    if side in prefix_no_number:
        prefix_new_name = prefix_no_number.replace(side, '')
    else:
        prefix_new_name = prefix_no_number

    group = rt_utils.group_parent(groups=parent_list, prefix=rt_utils.prefix_name(prefix_new_name),
                                  number=prefix_number,
                                  suffix=rt_utils.suffix_name(suffix).title(),
                                  side=side)

    if match_position:
        rt_utils.match_position(match_position, group[0])
        rt_utils.match_scale(match_position, group[0])

    if list_relatives == None:
        rt_utils.parent_object(group[-1], object)
    else:
        # parent group offset to list relatives
        rt_utils.parent_object(list_relatives, group[0])
        # parent obj to grp offset
        rt_utils.parent_object(group[-1], object)

    # print (group)
    return group


def create_parent_transform_two(parent_list, object, match_pos, prefix, suffix, side=''):
    list_relatives = cmds.listRelatives(object, ap=1)

    group = rt_utils.group_parent(parent_list, '%s' % rt_utils.prefix_name(prefix),
                                  rt_utils.suffix_name(suffix).title(), side)

    if match_pos:
        rt_utils.match_position(match_pos, group[0])
        rt_utils.match_scale(match_pos, group[0])

    if list_relatives == None:
        rt_utils.parent_object(group[-1], object)
    else:
        # parent group offset to list relatives
        rt_utils.parent_object(list_relatives, group[0])
        # parent obj to grp offset
        rt_utils.parent_object(group[-1], object)
    # print (group)
    return group


def bind_translate_reverse(control, input_2X, input_2Y, input_2Z, joint_bind_target, side_RGT, side_LFT, side):
    control_new = reposition_side(object=control, side_RGT=side_RGT, side_LFT=side_LFT)
    mdn_reverse = cmds.createNode('multiplyDivide', n=rt_utils.prefix_name(control_new) + 'Trans' + side + '_mdn')
    cmds.connectAttr(control + '.translate', mdn_reverse + '.input1')

    cmds.setAttr(mdn_reverse + '.input2X', input_2X)
    cmds.setAttr(mdn_reverse + '.input2Y', input_2Y)
    cmds.setAttr(mdn_reverse + '.input2Z', input_2Z)

    # CONNECT TO OBJECT
    cmds.connectAttr(mdn_reverse + '.output', joint_bind_target + '.translate')

    return mdn_reverse


def bind_rotate_reverse(control, input_2X, input_2Y, input_2Z, joint_bind_target, side_RGT, side_LFT, side):
    control_new = reposition_side(object=control, side_RGT=side_RGT, side_LFT=side_LFT)
    mdn_reverse = cmds.createNode('multiplyDivide', n=rt_utils.prefix_name(control_new) + 'Rot' + side + '_mdn')
    cmds.connectAttr(control + '.rotate', mdn_reverse + '.input1')

    cmds.setAttr(mdn_reverse + '.input2X', input_2X)
    cmds.setAttr(mdn_reverse + '.input2Y', input_2Y)
    cmds.setAttr(mdn_reverse + '.input2Z', input_2Z)

    # CONNECT TO OBJECT
    cmds.connectAttr(mdn_reverse + '.output', joint_bind_target + '.rotate')

    return mdn_reverse


def reposition_side(object, side_RGT, side_LFT):
    if side_RGT in object:
        obj_new_name = object.replace(side_RGT, '')
    elif side_LFT in object:
        obj_new_name = object.replace(side_LFT, '')