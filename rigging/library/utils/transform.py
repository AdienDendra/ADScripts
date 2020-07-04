"""
add object group parent

"""
import re
from __builtin__ import reload
from string import digits

import maya.cmds as mc

from rigging.tools import AD_utils as au

reload(au)


def create_parent_transform(parent_list, object, match_position, prefix, suffix, side=''):
    list_relatives = mc.listRelatives(object, ap=1)
    try:
        patterns = [r'\d+']
        prefix_number = au.prefix_name(prefix)
        for p in patterns:
            prefix_number = re.findall(p, prefix_number)[0]
    except:
        prefix_number = ''
    # get the prefix without number
    prefix_no_number = str(prefix).translate(None, digits)

    if side in prefix_no_number:
        prefix_new_name = prefix_no_number.replace(side, '')
    else:
        prefix_new_name = prefix_no_number

    group = au.group_parent(groups=parent_list, prefix=au.prefix_name(prefix_new_name), number=prefix_number,
                            suffix=au.suffix_name(suffix).title(),
                            side=side)

    if match_position:
        au.match_position(match_position, group[0])
        au.match_scale(match_position, group[0])

    if list_relatives == None:
        au.parent_object(group[-1], object)
    else:
        # parent group offset to list relatives
        au.parent_object(list_relatives, group[0])
        # parent obj to grp offset
        au.parent_object(group[-1], object)

    return group


def create_parent_transform_two(parent_list, object, match_pos, prefix, suffix, side=''):
    list_relatives = mc.listRelatives(object, ap=1)

    group = au.group_parent(parent_list, '%s' % au.prefix_name(prefix), au.suffix_name(suffix).title(), side)

    if match_pos:
        au.match_position(match_pos, group[0])
        au.match_scale(match_pos, group[0])

    if list_relatives == None:
        au.parent_object(group[-1], object)
    else:
        # parent group offset to list relatives
        au.parent_object(list_relatives, group[0])
        # parent obj to grp offset
        au.parent_object(group[-1], object)

    return group


def bind_translate_reverse(control, input_2X, input_2Y, input_2Z, joint_bind_target, side_RGT, side_LFT, side):
    control_new = replace_position_LFT_RGT(crv=control, side_RGT=side_RGT, side_LFT=side_LFT)
    mdn_reverse = mc.createNode('multiplyDivide', n=au.prefix_name(control_new) + 'Trans' + side + '_mdn')
    mc.connectAttr(control + '.translate', mdn_reverse + '.input1')

    mc.setAttr(mdn_reverse + '.input2X', input_2X)
    mc.setAttr(mdn_reverse + '.input2Y', input_2Y)
    mc.setAttr(mdn_reverse + '.input2Z', input_2Z)

    # CONNECT TO OBJECT
    mc.connectAttr(mdn_reverse + '.output', joint_bind_target + '.translate')

    return mdn_reverse


def bind_rotate_reverse(control, input_2X, input_2Y, input_2Z, joint_bind_target, side_RGT, side_LFT, side):
    control_new = replace_position_LFT_RGT(crv=control, side_RGT=side_RGT, side_LFT=side_LFT)
    mdn_reverse = mc.createNode('multiplyDivide', n=au.prefix_name(control_new) + 'Rot' + side + '_mdn')
    mc.connectAttr(control + '.rotate', mdn_reverse + '.input1')

    mc.setAttr(mdn_reverse + '.input2X', input_2X)
    mc.setAttr(mdn_reverse + '.input2Y', input_2Y)
    mc.setAttr(mdn_reverse + '.input2Z', input_2Z)

    # CONNECT TO OBJECT
    mc.connectAttr(mdn_reverse + '.output', joint_bind_target + '.rotate')

    return mdn_reverse


def replace_position_LFT_RGT(crv, side_RGT, side_LFT):
    if side_RGT in crv:
        crv_new_name = crv.replace(side_RGT, '')
    elif side_LFT in crv:
        crv_new_name = crv.replace(side_LFT, '')
    else:
        crv_new_name = crv

    return crv_new_name
