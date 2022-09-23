from __future__ import absolute_import

import maya.cmds as cmds


def connect_blendshape(blendshapeName):
    list_ctrl = cmds.ls(sl=1)
    print(list_ctrl)

    combine_multiply = []
    for i in list_ctrl:
        # create mult double linear node
        sufixName = suffix_name(i)
        multiplier = cmds.createNode('multDoubleLinear', n=prefix_name(i) + '_mdl')
        cmds.connectAttr(i + '.translateX', multiplier + '.input1')
        cmds.setAttr(multiplier + '.input2', 0.1)

        # if not (queryTheNameObject(selCtrl)+'_'+ sufixName):
        combine_multiplier = cmds.createNode('multDoubleLinear', n=prefix_name(i) + 'CombineMult' + '_mdl')
        cmds.connectAttr(multiplier + '.output', combine_multiplier + '.input1')

        cmds.connectAttr(combine_multiplier + '.output', blendshapeName + '.%s_ply' % prefix_name(i))

        combine_multiply.append(combine_multiplier)

    # main controller
    name_main_ctrl = query_the_name_object(list_ctrl) + '_' + suffix_name(list_ctrl[0])

    # list connection
    if not cmds.listConnections(name_main_ctrl + '.translateX', d=1):
        multiplier_main = cmds.createNode('multDoubleLinear', n=prefix_name(name_main_ctrl) + '_mdl')
        cmds.connectAttr(multiplier_main + '.output', blendshapeName + '.%s_ply' % prefix_name(name_main_ctrl))

        cmds.connectAttr(name_main_ctrl + '.translateX', multiplier_main + '.input1')
        cmds.setAttr(multiplier_main + '.input2', 0.1)

        condition_main = cmds.createNode('condition', n=prefix_name(name_main_ctrl) + '_cnd')
        cmds.setAttr(condition_main + '.operation', 3)
        cmds.connectAttr(multiplier_main + '.output', condition_main + '.firstTerm')

        cmds.setDrivenKeyframe(condition_main + '.colorIfTrueR',
                               cd=multiplier_main + '.output',
                               dv=0, v=1, itt='linear', ott='linear')

        cmds.setDrivenKeyframe(condition_main + '.colorIfTrueR',
                               cd=multiplier_main + '.output',
                               dv=1, v=0, itt='linear', ott='linear')

        cmds.setDrivenKeyframe(condition_main + '.colorIfFalseR',
                               cd=multiplier_main + '.output',
                               dv=0, v=0, itt='linear', ott='linear')

        cmds.setDrivenKeyframe(condition_main + '.colorIfFalseR',
                               cd=multiplier_main + '.output',
                               dv=1, v=1, itt='linear', ott='linear')

        # connect from condition to mdl also from mdl to object blendshape
        for i in combine_multiply:
            cmds.connectAttr(condition_main + '.outColorR', i + '.input2')

    else:
        destination_mult = cmds.listConnections(name_main_ctrl, d=1, type='multDoubleLinear')[0]
        destination_condition = cmds.listConnections(destination_mult, d=1, type='condition')[0]

        for i in combine_multiply:
            cmds.connectAttr(destination_condition + '.outColorR', i + '.input2')


def prefix_name(obj):
    if '_' in obj:
        get_prefix_name = obj.split('_')[0]
        return get_prefix_name
    else:
        return obj


def query_the_name_object(list_controller):
    s = []
    for x in zip(*list_controller):
        if len(set(x)) == 1:
            s.append(x[0])

    return ''.join(s)


def suffix_name(obj):
    objs = obj.split('|')[-1:]
    for l in objs:
        get_length = l.split('_')
        if len(get_length) > 1:
            getSufN = get_length[1]
            return getSufN
        else:
            get_suffix_number = l.replace(l, '')
            return get_suffix_number
