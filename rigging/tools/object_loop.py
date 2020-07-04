from __builtin__ import reload

import maya.cmds as mc

import rigging.tools.AD_utils as au
from rigging.library.utils import joint as jn, controller as ct
from rigging.library.utils import rotation_controller as rc

reload (ct)
reload (au)
reload(rc)
reload (jn)

# load Plug-ins
matrix_node = mc.pluginInfo('matrixNodes.mll', query=True, loaded=True)
quat_node = mc.pluginInfo('quatNodes.mll', query=True, loaded=True)

if not matrix_node:
    mc.loadPlugin( 'matrixNodes.mll' )

if not quat_node:
    mc.loadPlugin( 'quatNodes.mll' )


def loop(curve='', world_up_loc='', controller=False):
    all_grp = mc.group(empty=True, n=au.prefix_name(curve) + 'MotionLoop' + '_grp')
    setup_grp = mc.group(empty=True, n=au.prefix_name(curve) + 'Setup' + '_grp')
    grp_jnt = mc.group(empty=True, n=au.prefix_name(curve) + 'Joints' + '_grp')
    grp_crv = mc.group(empty=True, n=au.prefix_name(curve) + 'Crv' + '_grp')

    create_ik = jn.joint_on_curve(curve=curve, world_up_loc=world_up_loc, delete_group=False, delWUpLoc=False,
                                 ctrl=controller)

    ctrl = ct.Control(match_obj_first_position=create_ik['joints'][0], prefix=au.prefix_name(curve),
                      shape=ct.STICKCIRCLE,
                      groups_ctrl=['Zro'], ctrl_size=10.0,
                      ctrl_color='blue', gimbal=False, lock_channels=['r', 's', 'v'])

    attribute_speed = au.add_attribute(objects=[ctrl.control], long_name=['speed'], min=0, dv=0, max=50, at="float",
                                       keyable=True)

    rc.change_position(ctrl.control, 'xy')

    for i, ctrls in zip(create_ik['motionPath'], create_ik['ctrl']):

        motion_path_uvalue = mc.getAttr(i + '.u')

        mult_timing = mc.shadingNode('multDoubleLinear', asUtility=1, n=au.prefix_name(i) + 'TimeMult' + '_mdl')
        mc.connectAttr(ctrl.control +'.%s' % attribute_speed, mult_timing + '.input1')
        mc.connectAttr('time1.outTime', mult_timing + '.input2')

        add_speed = mc.shadingNode('addDoubleLinear', asUtility=1, n=au.prefix_name(i) + 'SpeedAdd' + '_adl')
        mc.setAttr(add_speed + '.input2', motion_path_uvalue * 1000)

        mult_offset = mc.shadingNode('multiplyDivide', asUtility=1, n=au.prefix_name(i) + 'SpeedOffset' + '_mdn')
        mc.setAttr(mult_offset + '.operation', 2)
        mc.setAttr(mult_offset + '.input2X', 1000)
        mc.connectAttr(add_speed + '.output', mult_offset + '.input1X')

        condition_speed = mc.shadingNode('condition', asUtility=1, n=au.prefix_name(i) + 'Speed' + '_cnd')
        mc.setAttr(condition_speed + '.operation', 2)
        mc.connectAttr(mult_timing + '.output', condition_speed + '.firstTerm')

        add_value = mc.shadingNode('plusMinusAverage', asUtility=1, n=au.prefix_name(i) + 'Speed' + '_pma')
        mc.connectAttr(mult_offset + '.outputX', add_value + '.input1D[0]')
        mc.setAttr(add_value + '.input1D[1]', 1)

        mc.connectAttr(mult_offset + '.outputX', condition_speed + '.colorIfTrueR')
        mc.connectAttr(add_value + '.output1D', condition_speed + '.colorIfFalseR')

        mc.setDrivenKeyframe(i +'.u', cd=condition_speed + '.outColorR', dv=0, v=0)
        mc.setDrivenKeyframe(i +'.u', cd=condition_speed + '.outColorR', dv=1, v=1)

        mc.keyTangent(i+'_uValue', edit=True,  inTangentType='linear', outTangentType='linear')

        mc.setAttr(i+'_uValue'+'.preInfinity', 3)
        mc.setAttr(i+'_uValue'+'.postInfinity', 3)

        if controller:
            pos_offset_attr = au.add_attribute(objects=[ctrls], long_name=['posOffset'], dv=0, min=0, at="float", keyable=True)

            obj_offset = mc.shadingNode('plusMinusAverage', asUtility=1, n=au.prefix_name(i) + 'ObjSpeed' + '_pma')
            mc.connectAttr(mult_timing + '.output', obj_offset + '.input1D[0]')
            mc.connectAttr(obj_offset + '.output1D', add_speed + '.input1')

            obj_condition = mc.shadingNode('condition', asUtility=1, n=au.prefix_name(i) + 'ObjSpeed' + '_cnd')
            mc.setAttr(obj_condition + '.operation', 4)
            mc.connectAttr(mult_timing + '.output', obj_condition + '.firstTerm')

            mc.setDrivenKeyframe(obj_condition + '.colorIfTrueR', cd=ctrls + '.%s' % pos_offset_attr, dv=0, v=0)
            mc.setDrivenKeyframe(obj_condition + '.colorIfTrueR', cd=ctrls + '.%s' % pos_offset_attr, dv=1, v=-1)

            mc.keyTangent(obj_condition + '_colorIfTrueR', edit=True, inTangentType='spline', outTangentType='spline')

            mc.setAttr(obj_condition + '_colorIfTrueR' + '.preInfinity', 1)
            mc.setAttr(obj_condition + '_colorIfTrueR' + '.postInfinity', 1)

            mc.setDrivenKeyframe(obj_condition + '.colorIfFalseR', cd=ctrls + '.%s' % pos_offset_attr, dv=0, v=0)
            mc.setDrivenKeyframe(obj_condition + '.colorIfFalseR', cd=ctrls + '.%s' % pos_offset_attr, dv=1, v=1)

            mc.keyTangent(obj_condition + '_colorIfFalseR', edit=True, inTangentType='spline', outTangentType='spline')

            mc.setAttr(obj_condition + '_colorIfFalseR' + '.preInfinity', 1)
            mc.setAttr(obj_condition + '_colorIfFalseR' + '.postInfinity', 1)

            mc.connectAttr(obj_condition + '.outColorR', obj_offset + '.input1D[1]')

        else:
            mc.connectAttr(mult_timing + '.output', add_speed + '.input1')

        mc.setAttr(i+'.u', lock=True)

    decompose = mc.shadingNode('decomposeMatrix', asUtility=1, n=au.prefix_name(curve) + 'Scale' + 'dmt')
    mc.connectAttr(grp_crv + '.worldMatrix[0]', decompose + '.inputMatrix')

    for i in create_ik['joints']:
        mc.connectAttr(decompose + '.outputScale', i + '.scale')
        au.lock_attr(['t', 'r', 's'], i)

    mc.parent(create_ik['joints'], grp_jnt)
    # mc.parent(createIk['wUpLocGrp'], grpJnt)

    mc.parent(curve, grp_crv)

    mc.parent(grp_jnt, grp_crv, setup_grp)
    mc.parent(ctrl.parent_control[0], setup_grp, all_grp)

    # mc.setAttr(createIk['wUpLoc']+'.visibility', 0)
    au.lock_attr(['t', 'r', 's'], curve)
    au.lock_attr(['t', 'r', 's'], grp_jnt)
    au.lock_attr(['t', 'r', 's'], setup_grp)

    mc.select(cl=1)


# # NOT USED #
# def loopAuto(curve='', numberOfJnt=None):
#     allGrp = mc.group(empty=True, n=au.prefixName(curve) + 'MotionLoop' + '_grp')
#     setupGrp = mc.group(empty=True, n=au.prefixName(curve) + 'Setup' + '_grp')
#     grpJnt = mc.group(empty=True, n=au.prefixName(curve) + 'Joints' + '_grp')
#     grpCrv = mc.group(empty=True, n=au.prefixName(curve) + 'Crv' + '_grp')
#
#     createIk = jn.jointOnCrv(curve=curve, numberOfJnt=numberOfJnt, delGrp=False,  delWUpLoc= False)
#
#     ctrl = ct.Control(matchPos=createIk['joints'][0], prefix=au.prefixName(curve), shape=ct.STICKCIRCLE,
#                       groupsCtrl=['Zro'], ctrlSize=10.0,
#                       ctrlColor='blue', gimbal=False, lockChannels=['r','s','v'])
#
#     au.addAttribute(objects=[ctrl.control], longName=['speed'], min=0, dv=1, at="float", k=True)
#
#     for i in createIk['motionPath']:
#         motionPathUvalue = mc.getAttr(i+'.u')
#
#         addSpeed = mc.shadingNode('addDoubleLinear', asUtility=1, n=au.prefixName(i) + 'SpeedAdd' + '_adl')
#         mc.connectAttr('time1.outTime', addSpeed + '.input1')
#         mc.setAttr(addSpeed + '.input2', motionPathUvalue*1000)
#
#         mc.setDrivenKeyframe(addSpeed + '.input2', cd=ctrl.control+'.speed', dv=0, v=0)
#         mc.setDrivenKeyframe(addSpeed + '.input2', cd=ctrl.control+'.speed', dv=1, v=motionPathUvalue*1000)
#         mc.setAttr(addSpeed+'_'+'input2'+'.postInfinity', 1)
#
#         multSpeed = mc.shadingNode('multiplyDivide', asUtility=1, n=au.prefixName(i) + 'Speed' + '_mdn')
#         mc.connectAttr(ctrl.control+'.speed', multSpeed+'.input2X')
#         mc.setAttr(multSpeed+'.input1X', 1000)
#         mc.setAttr(multSpeed+'.operation',2)
#
#         multOffset = mc.shadingNode('multiplyDivide', asUtility=1, n=au.prefixName(i) + 'SpeedOffset' + '_mdn')
#         mc.setAttr(multOffset+'.operation', 2)
#         mc.connectAttr(multSpeed+'.outputX', multOffset+'.input2X')
#         mc.connectAttr(addSpeed+'.output', multOffset+'.input1X')
#
#
#         conditionSpeed  = mc.shadingNode('condition', asUtility=1, n=au.prefixName(i) + 'Speed' + '_cnd')
#         mc.setAttr(conditionSpeed+'.operation',0)
#         mc.connectAttr(ctrl.control+'.speed', conditionSpeed+'.firstTerm')
#         mc.connectAttr(multOffset+'.outputX', conditionSpeed+'.colorIfFalseR')
#         mc.setAttr(conditionSpeed+'.colorIfTrueR', motionPathUvalue)
#
#
#         # addValue = mc.shadingNode('plusMinusAverage', asUtility=1, n=au.prefixName(i) + 'Speed' + '_pma')
#         # mc.connectAttr(multOffset+'.outputX', addValue+'.input1D[0]')
#         # mc.setAttr(addValue+'.input1D[1]', 1)
#
#         # mc.connectAttr(multOffset+'.outputX', conditionSpeed+'.colorIfTrueR')
#         # mc.connectAttr(addValue+'.output1D', conditionSpeed+'.colorIfFalseR')
#
#         mc.setDrivenKeyframe(i+'.u', cd=conditionSpeed+'.outColorR', dv=0, v=0)
#         mc.setDrivenKeyframe(i+'.u', cd=conditionSpeed+'.outColorR', dv=1, v=1)
#
#         mc.keyTangent(i+'_uValue', edit=True,  inTangentType='linear', outTangentType='linear')
#
#         mc.setAttr(i+'_uValue'+'.preInfinity', 3)
#         mc.setAttr(i+'_uValue'+'.postInfinity', 3)
#
#         mc.setAttr(i+'.u', lock=True)
#
#     decompose = mc.shadingNode('decomposeMatrix', asUtility=1, n=au.prefixName(curve) + 'Scale' + 'dmt')
#     mc.connectAttr(grpCrv + '.worldMatrix[0]', decompose + '.inputMatrix')
#
#     for i in createIk['joints']:
#         mc.connectAttr(decompose+'.outputScale', i+'.scale')
#         au.lockAttr(['t', 'r','s'], i)
#
#     mc.parent(createIk['joints'], grpJnt)
#     mc.parent(curve, grpCrv)
#
#     mc.parent(grpJnt, grpCrv, setupGrp)
#     mc.parent(ctrl.parentControl[0], setupGrp, allGrp)
#
#     mc.setAttr(createIk['wUpLoc']+'.visibility', 0)
#     au.lockAttr(['t', 'r', 's'], curve)
#     au.lockAttr(['t', 'r', 's'], grpJnt)
#     au.lockAttr(['t', 'r', 's'], setupGrp)
#
#     mc.select(cl=1)
#
# # ORIGINAL #
# def loopAutoSub(curve='', numberOfJnt=None):
#     allGrp = mc.group(empty=True, n=au.prefixName(curve) + 'MotionLoop' + '_grp')
#     setupGrp = mc.group(empty=True, n=au.prefixName(curve) + 'Setup' + '_grp')
#     grpJnt = mc.group(empty=True, n=au.prefixName(curve) + 'Joints' + '_grp')
#     grpCrv = mc.group(empty=True, n=au.prefixName(curve) + 'Crv' + '_grp')
#
#     createIk = jn.jointOnCrv(curve=curve, numberOfJnt=numberOfJnt, delGrp=False,  delWUpLoc= False)
#
#     ctrl = ct.Control(matchPos=createIk['joints'][0], prefix=au.prefixName(curve), shape=ct.STICKCIRCLE,
#                       groupsCtrl=['Zro'], ctrlSize=10.0,
#                       ctrlColor='blue', gimbal=False, lockChannels=['r','s','v'])
#
#     au.addAttribute(objects=[ctrl.control], longName=['speed'], dv=1, at="float", k=True)
#
#     for i in createIk['motionPath']:
#         motionPathUvalue = mc.getAttr(i+'.u')
#
#         addSpeed = mc.shadingNode('addDoubleLinear', asUtility=1, n=au.prefixName(i) + 'SpeedAdd' + '_adl')
#         mc.connectAttr('time1.outTime', addSpeed + '.input1')
#         mc.setAttr(addSpeed + '.input2', motionPathUvalue*1000)
#
#         multSpeed = mc.shadingNode('multiplyDivide', asUtility=1, n=au.prefixName(i) + 'Speed' + '_mdn')
#         mc.connectAttr(ctrl.control+'.speed', multSpeed+'.input1X')
#         mc.connectAttr(addSpeed+'.output', multSpeed+'.input2X')
#
#         conditionSpeed  = mc.shadingNode('condition', asUtility=1, n=au.prefixName(i) + 'Speed' + '_cnd')
#         mc.setAttr(conditionSpeed+'.operation',2)
#         mc.connectAttr(multSpeed+'.outputX', conditionSpeed+'.firstTerm')
#
#         multOffset = mc.shadingNode('multiplyDivide', asUtility=1, n=au.prefixName(i) + 'SpeedOffset' + '_mdn')
#         mc.setAttr(multOffset+'.operation', 2)
#         mc.setAttr(multOffset+'.input2X', 1000)
#         mc.connectAttr(multSpeed+'.outputX', multOffset+'.input1X')
#
#         addValue = mc.shadingNode('plusMinusAverage', asUtility=1, n=au.prefixName(i) + 'Speed' + '_pma')
#         mc.connectAttr(multOffset+'.outputX', addValue+'.input1D[0]')
#         mc.setAttr(addValue+'.input1D[1]', 1)
#
#         mc.connectAttr(multOffset+'.outputX', conditionSpeed+'.colorIfTrueR')
#         mc.connectAttr(addValue+'.output1D', conditionSpeed+'.colorIfFalseR')
#
#         mc.setDrivenKeyframe(i+'.u', cd=conditionSpeed+'.outColorR', dv=0, v=0)
#         mc.setDrivenKeyframe(i+'.u', cd=conditionSpeed+'.outColorR', dv=1, v=1)
#
#         mc.keyTangent(i+'_uValue', edit=True,  inTangentType='linear', outTangentType='linear')
#
#         mc.setAttr(i+'_uValue'+'.preInfinity', 3)
#         mc.setAttr(i+'_uValue'+'.postInfinity', 3)
#
#         mc.setAttr(i+'.u', lock=True)
#
#     decompose = mc.shadingNode('decomposeMatrix', asUtility=1, n=au.prefixName(curve) + 'Scale' + 'dmt')
#     mc.connectAttr(grpCrv + '.worldMatrix[0]', decompose + '.inputMatrix')
#
#     for i in createIk['joints']:
#         mc.connectAttr(decompose+'.outputScale', i+'.scale')
#         au.lockAttr(['t', 'r','s'], i)
#
#     mc.parent(createIk['joints'], grpJnt)
#     mc.parent(curve, createIk['wUpLoc'], grpCrv)
#
#     mc.parent(grpJnt, grpCrv, setupGrp)
#     mc.parent(ctrl.parentControl[0], setupGrp, allGrp)
#
#     mc.setAttr(createIk['wUpLoc']+'.visibility', 0)
#     au.lockAttr(['t', 'r', 's'], curve)
#     au.lockAttr(['t', 'r', 's'], grpJnt)
#     au.lockAttr(['t', 'r', 's'], setupGrp)
#
#     mc.select(cl=1)


