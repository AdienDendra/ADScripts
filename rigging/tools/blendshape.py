import maya.cmds as mc


def connect_blendshape(blendshapeName):
    list_ctrl = mc.ls(sl=1)
    print(list_ctrl)

    combine_multiply = []
    for i in list_ctrl:
        # create mult double linear node
        sufixName = suffix_name(i)
        multiplier = mc.createNode('multDoubleLinear', n=prefix_name(i) + '_mdl')
        mc.connectAttr(i + '.translateX', multiplier + '.input1')
        mc.setAttr(multiplier + '.input2', 0.1)

        # if not (queryTheNameObject(selCtrl)+'_'+ sufixName):
        combine_multiplier = mc.createNode('multDoubleLinear', n=prefix_name(i) + 'CombineMult' + '_mdl')
        mc.connectAttr(multiplier + '.output', combine_multiplier + '.input1')

        mc.connectAttr(combine_multiplier + '.output', blendshapeName + '.%s_ply' % prefix_name(i))

        combine_multiply.append(combine_multiplier)

    # main controller
    name_main_ctrl = query_the_name_object(list_ctrl) + '_' + suffix_name(list_ctrl[0])

    # list connection
    if not mc.listConnections(name_main_ctrl + '.translateX', d=1):
        multiplier_main = mc.createNode('multDoubleLinear', n=prefix_name(name_main_ctrl) + '_mdl')
        mc.connectAttr(multiplier_main + '.output', blendshapeName + '.%s_ply' % prefix_name(name_main_ctrl))

        mc.connectAttr(name_main_ctrl + '.translateX', multiplier_main + '.input1')
        mc.setAttr(multiplier_main + '.input2', 0.1)

        condition_main = mc.createNode('condition', n=prefix_name(name_main_ctrl) + '_cnd')
        mc.setAttr(condition_main + '.operation', 3)
        mc.connectAttr(multiplier_main + '.output', condition_main + '.firstTerm')

        mc.setDrivenKeyframe(condition_main + '.colorIfTrueR',
                             cd=multiplier_main + '.output',
                             dv=0, v=1, itt='linear', ott='linear')

        mc.setDrivenKeyframe(condition_main + '.colorIfTrueR',
                             cd=multiplier_main + '.output',
                             dv=1, v=0, itt='linear', ott='linear')

        mc.setDrivenKeyframe(condition_main + '.colorIfFalseR',
                             cd=multiplier_main + '.output',
                             dv=0, v=0, itt='linear', ott='linear')

        mc.setDrivenKeyframe(condition_main + '.colorIfFalseR',
                             cd=multiplier_main + '.output',
                             dv=1, v=1, itt='linear', ott='linear')

        # connect from condition to mdl also from mdl to object blendshape
        for i in combine_multiply:
            mc.connectAttr(condition_main + '.outColorR', i + '.input2')

    else:
        destination_mult = mc.listConnections(name_main_ctrl, d=1, type='multDoubleLinear')[0]
        destination_condition = mc.listConnections(destination_mult, d=1, type='condition')[0]

        for i in combine_multiply:
            mc.connectAttr(destination_condition + '.outColorR', i + '.input2')


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
