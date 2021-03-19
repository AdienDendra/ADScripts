# class Lr_PathLine():
#     def __init__(self, curve_attach, curve):
#         lr_load_matrix_quad_plugin()
#         lr_motion_path(curve_attach=curve_attach, curve=curve, bind_joint='', group_joint='', world_up_loc='', fa='z', ua='x')

# class Lr_MotionPaths():
#     def __init__(self, curve='', world_up_loc='', set_value_length =1, controller=False):
#         # load Plug-ins
#         lr_load_matrix_quad_plugin()
#
#         # all_grp = mc.group(empty=True, n=lr_prefix_name(curve) + 'MotionLoop' + '_grp')
#         # setup_grp = mc.group(empty=True, n=lr_prefix_name(curve) + 'Setup' + '_grp')
#         # grp_jnt = mc.group(empty=True, n=lr_prefix_name(curve) + 'Joints' + '_grp')
#         # grp_crv = mc.group(empty=True, n=lr_prefix_name(curve) + 'Crv' + '_grp')
#         #
#         # create_ik = lr_joint_on_curve(curve=curve, world_up_loc=world_up_loc, delete_group=False,
#         #                               ctrl=controller)
#         # arc_length = mc.arclen(curve)
#         #
#         # value_length = arc_length/set_value_length
#         #
#         #
#         # ctrl = Lr_Control(match_obj_first_position=create_ik['joints'][0], prefix=lr_prefix_name(curve),
#         #                   shape=STAR,
#         #                   groups_ctrl=['Zro'], ctrl_size=10.0,
#         #                   ctrl_color='blue', lock_channels=['r', 's', 'v'])
#
#         attribute_speed = lr_add_attribute(objects=[ctrl.control], long_name=['speed'], min=0, dv=0, max=50, at="float",
#                                            keyable=True)
#
#         lr_change_position(ctrl.control, 'xy')
#
#         for i, ctrls in zip(create_ik['motionPath'], create_ik['ctrl']):
#
#             motion_path_uvalue = mc.getAttr(i + '.u')
#
#             mult_timing = mc.shadingNode('multDoubleLinear', asUtility=1, n=lr_prefix_name(i) + 'TimeMult' + '_mdl')
#             mc.connectAttr(ctrl.control + '.%s' % attribute_speed, mult_timing + '.input1')
#             mc.connectAttr('time1.outTime', mult_timing + '.input2')
#
#             add_speed = mc.shadingNode('addDoubleLinear', asUtility=1, n=lr_prefix_name(i) + 'SpeedAdd' + '_adl')
#             mc.setAttr(add_speed + '.input2', (((motion_path_uvalue/value_length) * 1000)))
#
#             mult_offset = mc.shadingNode('multiplyDivide', asUtility=1, n=lr_prefix_name(i) + 'SpeedOffset' + '_mdn')
#             mc.setAttr(mult_offset + '.operation', 2)
#             mc.setAttr(mult_offset + '.input2X', 1000)
#             mc.connectAttr(add_speed + '.output', mult_offset + '.input1X')
#
#             condition_speed = mc.shadingNode('condition', asUtility=1, n=lr_prefix_name(i) + 'Speed' + '_cnd')
#             mc.setAttr(condition_speed + '.operation', 2)
#             mc.connectAttr(mult_timing + '.output', condition_speed + '.firstTerm')
#
#             add_value = mc.shadingNode('plusMinusAverage', asUtility=1, n=lr_prefix_name(i) + 'Speed' + '_pma')
#             mc.connectAttr(mult_offset + '.outputX', add_value + '.input1D[0]')
#             mc.setAttr(add_value + '.input1D[1]', 1)
#
#             mc.connectAttr(mult_offset + '.outputX', condition_speed + '.colorIfTrueR')
#             mc.connectAttr(add_value + '.output1D', condition_speed + '.colorIfFalseR')
#
#             mc.setDrivenKeyframe(i + '.u', cd=condition_speed + '.outColorR', dv=0, v=0)
#             mc.setDrivenKeyframe(i + '.u', cd=condition_speed + '.outColorR', dv=1, v=1)
#
#             mc.keyTangent(i + '_uValue', edit=True, inTangentType='linear', outTangentType='linear')
#
#             mc.setAttr(i + '_uValue' + '.preInfinity', 3)
#             mc.setAttr(i + '_uValue' + '.postInfinity', 3)
#
#             if controller:
#                 pos_offset_attr = lr_add_attribute(objects=[ctrls], long_name=['posOffset'], dv=0, min=0, at="float",
#                                                    keyable=True)
#
#                 obj_offset = mc.shadingNode('plusMinusAverage', asUtility=1, n=lr_prefix_name(i) + 'ObjSpeed' + '_pma')
#                 mc.connectAttr(mult_timing + '.output', obj_offset + '.input1D[0]')
#                 mc.connectAttr(obj_offset + '.output1D', add_speed + '.input1')
#
#                 obj_condition = mc.shadingNode('condition', asUtility=1, n=lr_prefix_name(i) + 'ObjSpeed' + '_cnd')
#                 mc.setAttr(obj_condition + '.operation', 4)
#                 mc.connectAttr(mult_timing + '.output', obj_condition + '.firstTerm')
#
#                 mc.setDrivenKeyframe(obj_condition + '.colorIfTrueR', cd=ctrls + '.%s' % pos_offset_attr, dv=0, v=0)
#                 mc.setDrivenKeyframe(obj_condition + '.colorIfTrueR', cd=ctrls + '.%s' % pos_offset_attr, dv=1, v=-1)
#
#                 mc.keyTangent(obj_condition + '_colorIfTrueR', edit=True, inTangentType='spline', outTangentType='spline')
#
#                 mc.setAttr(obj_condition + '_colorIfTrueR' + '.preInfinity', 1)
#                 mc.setAttr(obj_condition + '_colorIfTrueR' + '.postInfinity', 1)
#
#                 mc.setDrivenKeyframe(obj_condition + '.colorIfFalseR', cd=ctrls + '.%s' % pos_offset_attr, dv=0, v=0)
#                 mc.setDrivenKeyframe(obj_condition + '.colorIfFalseR', cd=ctrls + '.%s' % pos_offset_attr, dv=1, v=1)
#
#                 mc.keyTangent(obj_condition + '_colorIfFalseR', edit=True, inTangentType='spline', outTangentType='spline')
#
#                 mc.setAttr(obj_condition + '_colorIfFalseR' + '.preInfinity', 1)
#                 mc.setAttr(obj_condition + '_colorIfFalseR' + '.postInfinity', 1)
#
#                 mc.connectAttr(obj_condition + '.outColorR', obj_offset + '.input1D[1]')
#
#             else:
#                 mc.connectAttr(mult_timing + '.output', add_speed + '.input1')
#
#             mc.setAttr(i + '.u', lock=True)
#
#         decompose = mc.shadingNode('decomposeMatrix', asUtility=1, n=lr_prefix_name(curve) + 'Scale' + 'dmt')
#         mc.connectAttr(grp_crv + '.worldMatrix[0]', decompose + '.inputMatrix')
#
#         for i in create_ik['joints']:
#             mc.connectAttr(decompose + '.outputScale', i + '.scale')
#             lr_lock_attr(['t', 'r', 's'], i)
#
#         mc.parent(create_ik['joints'], grp_jnt)
#         # mc.parent(createIk['wUpLocGrp'], grpJnt)
#
#         mc.parent(curve, grp_crv)
#
#         mc.parent(grp_jnt, grp_crv, setup_grp)
#         mc.parent(ctrl.parent_control[0], setup_grp, all_grp)
#
#         # mc.setAttr(createIk['wUpLoc']+'.visibility', 0)
#         lr_lock_attr(['t', 'r', 's'], curve)
#         lr_lock_attr(['t', 'r', 's'], grp_jnt)
#         lr_lock_attr(['t', 'r', 's'], setup_grp)
#
#         mc.select(cl=1)
