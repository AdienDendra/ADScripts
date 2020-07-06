from __builtin__ import reload

import maya.cmds as mc

from rigging.library.base.face import wire as wr, nose as ns
from rigging.library.utils import controller as ct
from rigging.library.utils import transform as tf
from rigging.tools import AD_utils as au

reload (ct)
reload (tf)
reload (au)
reload (ns)
reload (wr)

class Nose:
    def __init__(self,
                 face_utils_grp,
                 columella_jnt,
                 # columella_skn,
                 columella_prefix,
                 curve_template_nose,
                 offset_jnt02_bind_position,
                 offset_jnt04_bind_position,
                 ctrl01_direction,
                 ctrl02_direction,
                 ctrl03_direction,
                 ctrl04_direction,
                 ctrl05_direction,
                 ctrl_color,
                 nose_jnt,
                 nose_up_jnt,
                 # nose_up_skin,
                 position_mouth_ctrl,
                 head_ctrl_gimbal,
                 head_up_ctrl_gimbal,
                 head_jnt,
                 shape,
                 scale,
                 side_RGT,
                 side_LFT,
                 lip_corner_ctrl_LFT,
                 lip_corner_ctrl_RGT,
                 nostril_attr_ctrl_LFT,
                 nostril_attr_ctrl_RGT,
                 up_lip_controller_all,
                 mouth_ctrl,
                 nose_follow_mouth_value,
                 up_lip_all_ctrl_grp_ctrl,
                 jaw_ctrl,
                 suffix_controller,
                 base_module_nonTransform,
                 # parent_skin_nose
                 ):


    # ==================================================================================================================
    #                                               NOSE CONTROLLER
    # ==================================================================================================================
        columella_ctrl = ns.Build(columella_jnt, columella_prefix, suffix_controller, scale)

        wire = wr.Build(curve_template=curve_template_nose, position_joint_direction=nose_jnt, scale=scale, side_LFT=side_LFT, side_RGT=side_RGT, side='',
                        offset_jnt02_bind_position=offset_jnt02_bind_position, offset_jnt04_bind_position=offset_jnt04_bind_position,
                        ctrl01_direction=ctrl01_direction, ctrl02_direction=ctrl02_direction,
                        ctrl03_direction=ctrl03_direction, ctrl04_direction=ctrl04_direction, ctrl05_direction=ctrl05_direction,
                        ctrl_color=ctrl_color, wire_low_controller=False, shape=shape, face_utils_grp=face_utils_grp, connect_with_corner_ctrl=False,
                        suffix_controller=suffix_controller, base_module_nonTransform=base_module_nonTransform,
                        # parent_skin=parent_skin_nose
                        )


        self.controller_nose01_LFT = wire.controller_bind05
        self.controller_nose01_RGT = wire.controller_bind01
        self.controller_nose03 = wire.controller_bind03

        controller_bind01_LFT = wire.controller_bind05
        controller_bind01_RGT = wire.controller_bind01
        self.all_joint = wire.all_joint
        self.nose_controller_grp = wire.ctrl_driver_grp

        # ADD ATTRIBUTE LFT
        au.add_attribute(objects=[controller_bind01_LFT], long_name=['cheekUpSetup'], nice_name=[' '], at="enum",
                         en='Cheek Up Setup', channel_box=True)
        self.pull_forward_LFT = au.add_attribute(objects=[controller_bind01_LFT], long_name=['pullForward'],
                                                 attributeType="float", min=0.001, max=10, dv=1, keyable=True)

        self.push_upward_LFT = au.add_attribute(objects=[controller_bind01_LFT], long_name=['pushUpward'],
                                                attributeType="float", min=0.001, max=10, dv=1, keyable=True)

        # ADD ATTRIBUTE RGT
        au.add_attribute(objects=[controller_bind01_RGT], long_name=['cheekUpSetup'], nice_name=[' '], at="enum",
                         en='Cheek Up Setup', channel_box=True)
        self.pull_forward_RGT = au.add_attribute(objects=[controller_bind01_RGT], long_name=['pullForward'],
                                                 attributeType="float", min=0.001, max=10, dv=1, keyable=True)

        self.push_upward_RGT = au.add_attribute(objects=[controller_bind01_RGT], long_name=['pushUpward'],
                                                attributeType="float", min=0.001, max=10, dv=1, keyable=True)


        # ADD NOSE CONTROLLER
        nose_controller = ct.Control(match_obj_first_position=nose_jnt,
                                     prefix='nose',
                                     shape=ct.LOCATOR, groups_ctrl=['Zro', 'Offset'],
                                     ctrl_size=scale * 0.25,
                                     ctrl_color='turquoiseBlue', lock_channels=['v'])

        self.nose_ctrl = nose_controller.control
        self.nose_ctrl_grp_offset = nose_controller.parent_control[1]
        self.nose_ctrl_grp_zro = nose_controller.parent_control[0]

        # ADD ATTRIBUTE NOSE
        au.add_attribute(objects=[nose_controller.control], long_name=['weightSkinInfluence'], nice_name=[' '], at="enum",
                         en='Weight Influence', channel_box=True)

        self.mouth_weight_ud = au.add_attribute(objects=[nose_controller.control], long_name=['upDown'],
                                                attributeType="float", min=0, dv=1, keyable=True)
        self.mouth_weight_ss = au.add_attribute(objects=[nose_controller.control], long_name=['squashStretch'],
                                                attributeType="float", min=0, dv=1, keyable=True)
        self.mouth_weight_lr = au.add_attribute(objects=[nose_controller.control], long_name=['leftRight'],
                                                attributeType="float", min=0, dv=1, keyable=True)
        # OFFSET POSITION PARENT GRP NOSE
        tZ_value = mc.getAttr(self.nose_ctrl_grp_zro + '.translateZ')
        mc.setAttr(self.nose_ctrl_grp_zro + '.translateZ', tZ_value + (position_mouth_ctrl * 0.5 * scale))

        # CREATE PMA FOR EXPRESSION
        self.nose_ctrl_translate_pma = mc.createNode('plusMinusAverage', n='noseWeightToMouthTrans_pma')
        self.nose_ctrl_rotate_pma = mc.createNode('plusMinusAverage', n='noseWeightToMouthRot_pma')
        self.nose_ctrl_scale_pma = mc.createNode('plusMinusAverage', n='noseWeightToMouthScl_pma')

        # CONNECT ATTRIBUTE NOSE CTRL TO GRP OFFSET JOINT DRIVEN AND CONTROLLER
        mc.connectAttr(self.nose_ctrl + '.translate', self.nose_ctrl_translate_pma + '.input3D[0]')
        mc.connectAttr(self.nose_ctrl + '.rotate', self.nose_ctrl_rotate_pma + '.input3D[0]')
        mc.connectAttr(self.nose_ctrl + '.scale', self.nose_ctrl_scale_pma + '.input3D[0]')


        mc.connectAttr(self.nose_ctrl_rotate_pma + '.output3D', wire.wire_driven_jnt_grp_offset + '.rotate')
        # au.connectAttrRot(self.noseCtrl, noseGrpDrivenOffsetJnt)
        mc.connectAttr(self.nose_ctrl_scale_pma + '.output3D', wire.wire_driven_jnt_grp_offset + '.scale')

        mc.connectAttr(self.nose_ctrl_translate_pma + '.output3D', wire.wire_driven_ctrl_grp_offset + '.translate')
        mc.connectAttr(self.nose_ctrl_rotate_pma + '.output3D', wire.wire_driven_ctrl_grp_offset + '.rotate')
        # au.connectAttrRot(self.noseCtrl, noseGrpDrivenOffsetCtrl)
        mc.connectAttr(self.nose_ctrl_scale_pma + '.output3D', wire.wire_driven_ctrl_grp_offset + '.scale')

        mc.connectAttr(self.nose_ctrl_translate_pma + '.output3D', columella_ctrl.columella_jnt_grp[1] + '.translate')
        mc.connectAttr(self.nose_ctrl_rotate_pma + '.output3D', columella_ctrl.columella_jnt_grp[1] + '.rotate')
        # au.connectAttrRot(self.noseCtrl, columellaCtrl.grpColumellaJnt[1])
        mc.connectAttr(self.nose_ctrl_scale_pma + '.output3D', columella_ctrl.columella_jnt_grp[1] + '.scale')


        # CONNECT ALL PART NOSE JOINT
        for i in wire.all_joint:
            mc.connectAttr(self.nose_ctrl_translate_pma + '.output3D', i + '.translate')
            mc.connectAttr(self.nose_ctrl_rotate_pma + '.output3D', i + '.rotate')
            # au.connectAttrRot(self.noseCtrl, i)
            mc.connectAttr(self.nose_ctrl_scale_pma + '.output3D', i + '.scale')
            # au.connectAttrObject(self.noseCtrl, i)

        # PARENT INTO THE GROUP
        mc.parent(columella_ctrl.columella_ctrl_grp_zro, wire.wire_driven_ctrl_grp_offset)
        mc.parent(wire.joint_grp, head_jnt)
        mc.parent(wire.ctrl_driver_grp, self.nose_ctrl_grp_zro, head_ctrl_gimbal)

        # SET THE VALUE FOR EXPRESSION
        translate_x_mouth = nose_follow_mouth_value * 24.0
        translate_x_lip = nose_follow_mouth_value * 24.0
        translate_x_jaw = nose_follow_mouth_value * 6.0
        translate_y_mouth = nose_follow_mouth_value * 12.0
        translate_y_lip = nose_follow_mouth_value * 12.0
        translate_y_jaw = nose_follow_mouth_value * (-12.0)

        scale_x_mouth = nose_follow_mouth_value * 48.0
        scale_x_lip = nose_follow_mouth_value * 24.0
        scale_x_jaw = nose_follow_mouth_value * (-6.0)
        scale_y_mouth = nose_follow_mouth_value * 48.0
        scale_y_lip = nose_follow_mouth_value * (-24.0)
        scale_y_jaw = nose_follow_mouth_value * (-6.0)

        rotate_y_mouth = nose_follow_mouth_value * 12.0
        rotate_y_lip = nose_follow_mouth_value * 24.0
        rotate_y_jaw = nose_follow_mouth_value * 0.1

        rotate_z_mouth = nose_follow_mouth_value * 12.0
        rotate_z_lip = nose_follow_mouth_value * 12.0
        rotate_z_jaw = nose_follow_mouth_value * (-0.1)

        # ADD NOSE UP CONTROLLER
        nose_up_controller = ct.Control(match_obj_first_position=nose_up_jnt,
                                        prefix='noseUp',
                                        shape=ct.JOINT, groups_ctrl=['Zro'],
                                        ctrl_size=scale * 0.05,
                                        ctrl_color='turquoiseBlue', lock_channels=['v'])

        self.nose_up_controller_grp = nose_up_controller.parent_control[0]

        grp_nose_up_jnt = tf.create_parent_transform(parent_list=['Zro'], object=nose_up_jnt, match_position=nose_up_jnt,
                                                     prefix='noseUp', suffix='_jnt')

        au.connect_attr_object(nose_up_controller.control, nose_up_jnt)
        mc.parent(nose_up_controller.parent_control[0], head_up_ctrl_gimbal)

        # ==============================================================================================================
        #                                            NOSTRIL SETUP
        # ==============================================================================================================
        joint_bind05_grp = wire.joint_bind05_grp
        joint_bind01_grp = wire.joint_bind01_grp
        get_attr_grp_zro_bind_nostril_LFT = mc.getAttr(joint_bind05_grp + '.translate')[0]
        get_attr_grp_zro_bind_nostril_RGT = mc.getAttr(joint_bind01_grp + '.translate')[0]
        get_attr_lip_up_all_ctrl_zro_grp = mc.getAttr(up_lip_all_ctrl_grp_ctrl + '.translate')[0]

        get_attr_lip_up_all_ctrl_zro_grp_ty = get_attr_lip_up_all_ctrl_zro_grp[1]
        # NOSTRIL LEFT
        self.nostril_setup(side=side_LFT, controller=lip_corner_ctrl_LFT,
                           attribute_offset=nostril_attr_ctrl_LFT,
                           nose_bind_grp_zro=joint_bind05_grp,
                           getAttr_tx_ctrl_grp_zro_nostril=get_attr_grp_zro_bind_nostril_LFT[0],
                           lip_up_all_ctrl=up_lip_controller_all,
                           mouth_ctrl=mouth_ctrl, multiplier=1,
                           getAttr_ty_ctrl_grp_zro_nostril=get_attr_grp_zro_bind_nostril_LFT[1],
                           getAttr_tz_ctrl_grp_zro_nostril=get_attr_grp_zro_bind_nostril_LFT[2],
                           value_mouth=nose_follow_mouth_value * 24.0,
                           value_mouth_three_times=nose_follow_mouth_value * 36.0,
                           value_upper_lip=nose_follow_mouth_value * 12.0,
                           jaw_ctrl=jaw_ctrl,
                           value_upper_lip_min_half=nose_follow_mouth_value * (-6.0),
                           value_upper_lip_max_or_min_y_half=nose_follow_mouth_value * 6.0,
                           value_corner_lip=nose_follow_mouth_value * 6.0)
        # NOSTRIL RIGHT
        self.nostril_setup(side=side_RGT, controller=lip_corner_ctrl_RGT,
                           attribute_offset=nostril_attr_ctrl_RGT,
                           nose_bind_grp_zro=joint_bind01_grp,
                           getAttr_tx_ctrl_grp_zro_nostril=get_attr_grp_zro_bind_nostril_RGT[0],
                           lip_up_all_ctrl=up_lip_controller_all,
                           mouth_ctrl=mouth_ctrl, multiplier=-1,
                           getAttr_ty_ctrl_grp_zro_nostril=get_attr_grp_zro_bind_nostril_RGT[1],
                           getAttr_tz_ctrl_grp_zro_nostril=get_attr_grp_zro_bind_nostril_RGT[2],
                           value_mouth=nose_follow_mouth_value * 24.0,
                           value_mouth_three_times=nose_follow_mouth_value * 36.0,
                           value_upper_lip=nose_follow_mouth_value * 12.0,
                           jaw_ctrl=jaw_ctrl,
                           value_upper_lip_min_half=nose_follow_mouth_value * 6.0,
                           value_upper_lip_max_or_min_y_half=nose_follow_mouth_value * (-6.0),
                           value_corner_lip=nose_follow_mouth_value * 6.0)

    # ==================================================================================================================
    #                                                   NOSE SETUP
    # ==================================================================================================================

        range_ud = self.nose_ctrl + '.%s' % self.mouth_weight_ud
        range_ss = self.nose_ctrl + '.%s' % self.mouth_weight_ss
        range_lr = self.nose_ctrl + '.%s' % self.mouth_weight_lr

        # TRANSLATE
        self.nose_setup(mouth_ctrl, jaw_ctrl, up_lip_controller_all,
                        translate_x='translateX', translate_y='translateY',
                        rotate_x_jaw='rotateY', rotate_y_jaw='rotateX',
                        first_value_x=translate_x_lip, second_value_x=translate_x_mouth,
                        first_value_y=translate_y_lip, second_value_y=translate_y_mouth,
                        first_operation_x=2, second_operation_x=2,
                        first_operation_y=2, second_operation_y=2,
                        operation_sum_x=1, operation_sum_y=1,
                        radius_value_x=0.0174533, radius_value_y=0.0174533,
                        ctrl_value_jaw_x=translate_x_jaw, ctrl_value_jaw_y=translate_y_jaw,
                        operation_sum_jaw_x=1, operation_sum_jaw_y=1, prefix_x='TransX',
                        prefix_y='TransY', divide=True, range=range_ud,
                        prefix='Trans', target_object=self.nose_ctrl_translate_pma,
                        target_x='input3Dx', target_y='input3Dy')
        # SCALE
        self.nose_setup(mouth_ctrl, jaw_ctrl, up_lip_controller_all,
                        translate_x='translateY', translate_y='translateY',
                        rotate_x_jaw='rotateX', rotate_y_jaw='rotateX',
                        first_value_x=scale_x_lip, second_value_x=scale_x_mouth,
                        first_value_y=scale_y_lip, second_value_y=scale_y_mouth,
                        first_operation_x=2, second_operation_x=2,
                        first_operation_y=2, second_operation_y=2,
                        operation_sum_x=1, operation_sum_y=2, radius_value_x=0.0174533, radius_value_y=0.0174533,
                        ctrl_value_jaw_x=scale_x_jaw, ctrl_value_jaw_y=scale_y_jaw,
                        operation_sum_jaw_x=1, operation_sum_jaw_y=2, prefix_x='SclX',
                        prefix_y='SclY', divide=True, range=range_ss,
                        prefix='Scl', target_object=self.nose_ctrl_scale_pma,
                        target_x='input3Dx', target_y='input3Dy')
        # ROTATE
        self.nose_setup(mouth_ctrl, jaw_ctrl, up_lip_controller_all,
                        translate_x='translateX', translate_y='translateX',
                        rotate_x_jaw='rotateY', rotate_y_jaw='rotateY',
                        first_value_x=rotate_y_lip, second_value_x=rotate_y_mouth,
                        first_value_y=rotate_z_lip, second_value_y=rotate_z_mouth,
                        first_operation_x=1, second_operation_x=1,
                        first_operation_y=1, second_operation_y=1,
                        operation_sum_x=1, operation_sum_y=1, radius_value_x=rotate_y_jaw, radius_value_y=rotate_z_jaw,
                        ctrl_value_jaw_x=None, ctrl_value_jaw_y=None,
                        operation_sum_jaw_x=1, operation_sum_jaw_y=1, prefix_x='RotY',
                        prefix_y='RotZ', divide=False, range=range_lr,
                        prefix='Rot', target_object=self.nose_ctrl_rotate_pma,
                        target_x='input3Dy', target_y='input3Dz')

        # SKIN PARENT AND SCALE CONSTRAINT
        # au.parent_scale_constraint(nose_up_jnt, nose_up_skin)
        # au.parent_scale_constraint(columella_jnt, columella_skn)

    # ==================================================================================================================
    #                                                 FUNCTION NOSE AND NOSTRIL
    # ==================================================================================================================

    def nose_setup(self, mouth_ctrl, jaw_ctrl, upLip_controller_all, translate_x, translate_y, rotate_x_jaw, rotate_y_jaw,
                   first_value_x, second_value_x, first_value_y, second_value_y, first_operation_x, second_operation_x,
                   first_operation_y, second_operation_y, operation_sum_x, operation_sum_y,
                   radius_value_x, radius_value_y, ctrl_value_jaw_x, ctrl_value_jaw_y, operation_sum_jaw_x,
                   operation_sum_jaw_y, prefix_x, prefix_y, divide, range, prefix,
                   target_object, target_x, target_y):

        X = self.nose_weight(second_ctrl=mouth_ctrl + '.%s' % translate_x, first_ctrl=upLip_controller_all + '.%s' % translate_x,
                             second_value=second_value_x, first_value=first_value_x,
                             second_operation=second_operation_x, first_operation=first_operation_x, operation_sum=operation_sum_x,
                             prefix=prefix_x)

        jaw_x = self.nose_additional(prefix='Jaw' + prefix_x, ctrl=jaw_ctrl + '.%s' % rotate_x_jaw,
                                     nose_weight_pma=X + '.output1D',
                                     operation_sum=operation_sum_jaw_x, radius_value=radius_value_x, ctrl_value=ctrl_value_jaw_x, divide=divide)

        Y = self.nose_weight(second_ctrl=mouth_ctrl + '.%s' % translate_y, first_ctrl=upLip_controller_all + '.%s' % translate_y,
                             second_value=second_value_y, first_value=first_value_y,
                             second_operation=second_operation_y, first_operation=first_operation_y, operation_sum=operation_sum_y,
                             prefix=prefix_y)

        jaw_y = self.nose_additional(prefix='Jaw' + prefix_y, ctrl=jaw_ctrl + '.%s' % rotate_y_jaw,
                                     nose_weight_pma=Y + '.output1D',
                                     operation_sum=operation_sum_jaw_y, radius_value=radius_value_y, ctrl_value=ctrl_value_jaw_y, divide=divide)

        range_great = self.multiply_to_range(range=range, nose_pma_x=X + '.output1D',
                                             nose_pma_y=Y + '.output1D',
                                             prefix=prefix, nameExpr='Great')

        range_less = self.multiply_to_range(range=range, nose_pma_x=jaw_x + '.output1D',
                                            nose_pma_y=jaw_y + '.output1D',
                                            prefix=prefix, nameExpr='Less')

        # CONDITION
        self.condition_nose_weight(jaw_ctrl=jaw_ctrl, range_great=range_great, range_less=range_less,
                                   target_first=target_object + '.input3D[1]' + '.%s' % target_x,
                                   target_second=target_object + '.input3D[1]' + '.%s' % target_y,
                                   prefix=prefix)

    def nostril_setup(self, side, controller, attribute_offset, nose_bind_grp_zro,
                      getAttr_tx_ctrl_grp_zro_nostril,
                      lip_up_all_ctrl, mouth_ctrl, multiplier, getAttr_ty_ctrl_grp_zro_nostril,
                      getAttr_tz_ctrl_grp_zro_nostril,
                      value_mouth, value_mouth_three_times, value_upper_lip, jaw_ctrl, value_corner_lip, value_upper_lip_max_or_min_y_half,
                      value_upper_lip_min_half):

        range = controller + '.%s' % attribute_offset
        mult_rev_nostril_trans_x = self.mdl_set_attr(name='nostrilWeight', prefix='TransX', name_expression='', side=side,
                                                     input1=controller + '.translateX ', input2_set=multiplier)
        mult_rev_nostril_trans_x_out = mult_rev_nostril_trans_x + '.output'
        # TRANS X
        trans_x_great, trans_x_less = self.nostril(range, mouth_ctrl, lip_up_all_ctrl, jaw_ctrl, value_mouth_three_times, value_upper_lip, value_corner_lip,
                                                   value_upper_lip_min_half=value_upper_lip_min_half, side=side, controller= mult_rev_nostril_trans_x_out,
                                                   translate='translateX', rotate='rotateX', prefix='TransX',
                                                   prefix_jaw='JawTransX', get_attr_ctrl_grp_zro_nostril=getAttr_tx_ctrl_grp_zro_nostril, operation=1)

        # TRANS Y
        trans_y_great, trans_y_less = self.nostril(range, mouth_ctrl, lip_up_all_ctrl, jaw_ctrl, value_mouth, value_upper_lip, value_corner_lip,
                                                   value_upper_lip_min_half=value_upper_lip_max_or_min_y_half, side=side, controller=controller + '.translateY',
                                                   translate='translateY', rotate='rotateY', prefix='TransY',
                                                   prefix_jaw='JawTransY', get_attr_ctrl_grp_zro_nostril=getAttr_ty_ctrl_grp_zro_nostril, operation=1)

        # TRANS Z
        trans_z_great, trans_z_less = self.nostril(range, mouth_ctrl, lip_up_all_ctrl, jaw_ctrl, value_mouth, value_upper_lip, value_corner_lip,
                                                   value_upper_lip_min_half=value_upper_lip_min_half, side=side, controller=controller + '.translateZ',
                                                   translate='translateZ', rotate='rotateZ', prefix='TransZ',
                                                   prefix_jaw='JawTransZ', get_attr_ctrl_grp_zro_nostril=getAttr_tz_ctrl_grp_zro_nostril, operation=1)

        self.condition_nostril_weight(jaw_ctrl,
                                      range_great_x=trans_x_great, range_less_x=trans_x_less,
                                      range_great_y=trans_y_great, range_less_y=trans_y_less,
                                      range_great_z=trans_z_great, range_less_z=trans_z_less,
                                      target=nose_bind_grp_zro, side=side)

    def nostril(self, range, mouth_ctrl, lip_up_all_ctrl, jaw_ctrl, value_mouth, value_upper_lip,
                value_corner_lip, value_upper_lip_min_half, side, controller,
                translate, rotate, prefix, prefix_jaw, get_attr_ctrl_grp_zro_nostril, operation):

        trans_nostril = self.nose_weight(third_ctrl=mouth_ctrl + '.%s' % translate,
                                         second_ctrl=lip_up_all_ctrl + '.%s' % translate,
                                         first_ctrl=controller,
                                         third_value=value_mouth, second_value=value_upper_lip, first_value=value_corner_lip,
                                         second_operation=2, first_operation=2, operation_sum=1, name='nostrilWeight',
                                         side=side,
                                         prefix=prefix, nose_target=False)

        trans_jaw_nostril = self.nose_additional(name='nostrilWeight', side=side, prefix=prefix_jaw,
                                                 ctrl=jaw_ctrl + '.%s' % rotate, nose_weight_pma=trans_nostril + '.output1D',
                                                 operation_sum=1, radius_value=0.0174533, ctrl_value=value_upper_lip_min_half,
                                                 divide=True)

        range_trans_nostril_great = self.multiply_to_range(name='nostrilWeight', side=side, range=range,
                                                           nose_pma_x=trans_nostril + '.output1D', prefix=prefix,
                                                           nameExpr='Great', mult_range=False)

        range_trans_nostril_less = self.multiply_to_range(name='nostrilWeight', side=side, range=range,
                                                          nose_pma_x=trans_jaw_nostril + '.output1D', prefix=prefix,
                                                          nameExpr='Less', mult_range=False)

        add_nostril_great = self.pma_set_attr(name='nostrilWeight', value_input0=get_attr_ctrl_grp_zro_nostril,
                                              input1=range_trans_nostril_great + '.outputX',
                                              operation=operation, prefix=prefix, name_expression='Great', side=side)

        add_nostril_less = self.pma_set_attr(name='nostrilWeight', value_input0=get_attr_ctrl_grp_zro_nostril,
                                             input1=range_trans_nostril_less + '.outputX',
                                             operation=operation, prefix=prefix, name_expression='Less', side=side)

        return add_nostril_great, add_nostril_less

    def condition_nostril_weight(self, jaw_ctrl, range_great_x, range_less_x, range_great_y, range_less_y,
                                 range_great_z, range_less_z, target, side, prefix='', name_expression=''):
        condition = mc.createNode('condition', n='nostrilWeight' + prefix + name_expression + 'Ctrl' + side + '_cnd')
        mc.setAttr(condition + '.operation', 3)
        mc.connectAttr(jaw_ctrl + '.rotateX', condition + '.firstTerm')

        mc.connectAttr(range_great_x + '.output1D', condition + '.colorIfTrueR')
        mc.connectAttr(range_great_y + '.output1D', condition + '.colorIfTrueG')
        mc.connectAttr(range_great_z + '.output1D', condition + '.colorIfTrueB')

        mc.connectAttr(range_less_x + '.output1D', condition + '.colorIfFalseR')
        mc.connectAttr(range_less_y + '.output1D', condition + '.colorIfFalseG')
        mc.connectAttr(range_less_z + '.output1D', condition + '.colorIfFalseB')

        mc.connectAttr(condition + '.outColorR', target+'.translateX')
        mc.connectAttr(condition + '.outColorG', target+'.translateY')
        mc.connectAttr(condition + '.outColorB', target+'.translateZ')

        return condition

    def condition_nose_weight(self, jaw_ctrl, range_great, range_less, target_first, target_second, prefix='', name_expression=''):
        condition = mc.createNode('condition', n='noseWeight' + prefix + name_expression + 'Ctrl' + '_cnd')
        mc.setAttr(condition+'.operation', 3)
        mc.connectAttr(jaw_ctrl + '.rotateX', condition + '.firstTerm')

        mc.connectAttr(range_great + '.outputX', condition + '.colorIfTrueR')
        mc.connectAttr(range_great + '.outputY', condition + '.colorIfTrueG')

        mc.connectAttr(range_less + '.outputX', condition + '.colorIfFalseR')
        mc.connectAttr(range_less + '.outputY', condition + '.colorIfFalseG')

        mc.connectAttr(condition +'.outColorR', target_first)
        mc.connectAttr(condition +'.outColorG', target_second)

        return condition

    def multiply_to_range(self, range, nose_pma_x, nose_pma_y='', side='',
                          prefix='', nameExpr='Less', name='noseWeight', mult_range=True):
        if mult_range:
            range_mult = self.mult_or_div_connect_two_attr(name=name, side=side,
                                                           input_1X=nose_pma_x,
                                                           input_1Y=nose_pma_y,
                                                           input_2X=range,
                                                           input_2Y=range,
                                                           operation=1, prefix=prefix, name_expression=nameExpr)
        else:
            range_mult = self.mult_or_div_connect_attr(name=name, side=side,
                                                       input1X=nose_pma_x,
                                                       input2X=range,
                                                       operation=1, prefix=prefix, nameExpr=nameExpr)
        return range_mult

    def nose_additional(self, prefix, ctrl, nose_weight_pma, operation_sum, radius_value=None, ctrl_value=None, side='', name_expression='', name='noseWeight',
                        divide=True):

        jaw_ctrl_mul = self.multOrDivSetAttr(name=name, side=side,
                                             input_1X=ctrl, input_2X_set=radius_value,
                                             operation=1, prefix=prefix+'JawRad', name_expression=name_expression)
        if divide:
            jaw_ctrl_div = self.multOrDivSetAttr(name=name, side=side,
                                                 input_1X=jaw_ctrl_mul + '.outputX', input_2X_set=ctrl_value,
                                                 operation=2, prefix=prefix+'Jaw', name_expression=name_expression)
            jaw_pma = self.pma_attr(name=name, side=side,
                                    input0=nose_weight_pma,
                                    input1=jaw_ctrl_div + '.outputX',
                                    operation=operation_sum, prefix=prefix, name_expression=name_expression)
            return jaw_pma

        else:
            jaw_pma = self.pma_attr(name=name, side=side,
                                    input0=nose_weight_pma,
                                    input1=jaw_ctrl_mul + '.outputX',
                                    operation=operation_sum, prefix=prefix, name_expression=name_expression)
            return jaw_pma

    def nose_weight(self, second_ctrl, first_ctrl, first_value,
                    second_value, second_operation, first_operation, operation_sum,
                    prefix, third_ctrl='', third_value='', name_expression='', side='', name='noseWeight', nose_target=True):

        mouth_div = self.multOrDivSetAttr(name=name, side=side,
                                          input_1X=second_ctrl, input_2X_set=second_value,
                                          operation=second_operation, prefix=prefix + 'Mouth', name_expression=name_expression)

        lip_up_div = self.multOrDivSetAttr(name=name, side=side,
                                           input_1X=first_ctrl, input_2X_set=first_value,
                                           operation=first_operation, prefix=prefix + 'UpLip', name_expression=name_expression)

        if not nose_target:
            corner_lip_div = self.multOrDivSetAttr(name=name, side=side,
                                                   input_1X=third_ctrl, input_2X_set=third_value,
                                                   operation=first_operation, prefix=prefix + 'CornerLip', name_expression=name_expression)

            nose_pma = self.pma_attr(name=name, side=side,
                                     input0=lip_up_div + '.outputX',
                                     input1=mouth_div + '.outputX',
                                     input2=corner_lip_div + '.outputX',
                                     operation=operation_sum, prefix=prefix, name_expression=name_expression, input_two=True)
        else:
            nose_pma = self.pma_attr(name=name, side=side,
                                     input0=lip_up_div + '.outputX',
                                     input1=mouth_div + '.outputX',
                                     operation=operation_sum, prefix=prefix, name_expression=name_expression)
        return nose_pma

    def mult_or_div_connect_two_attr(self, name, input_1X, input_2X, input_1Y, input_2Y, operation=2, prefix='', name_expression='', side=''):
        ctrl_drv_mdn = mc.createNode('multiplyDivide',
                                     n=au.prefix_name(name) + prefix + name_expression + 'Ctrl' + side + '_mdn')
        mc.setAttr(ctrl_drv_mdn + '.operation', operation)
        mc.connectAttr(input_1X, ctrl_drv_mdn + '.input1X')
        mc.connectAttr(input_1Y, ctrl_drv_mdn + '.input1Y')

        mc.connectAttr(input_2X, ctrl_drv_mdn + '.input2X')
        mc.connectAttr(input_2Y, ctrl_drv_mdn + '.input2Y')

        return ctrl_drv_mdn

    def mult_or_div_set_two_attr(self, name, input1X, input1Y, input2XSet, input2YSet, operation=2, prefix='', nameExpr='', side=''):
        ctrlDrvMDN = mc.createNode('multiplyDivide',
                                   n=au.prefix_name(name) + prefix + nameExpr + 'Ctrl' + side + '_mdn')
        mc.setAttr(ctrlDrvMDN + '.operation', operation)
        mc.connectAttr(input1X , ctrlDrvMDN + '.input1X')
        mc.connectAttr(input1Y , ctrlDrvMDN + '.input1Y')

        mc.setAttr(ctrlDrvMDN + '.input2X', input2XSet)
        mc.setAttr(ctrlDrvMDN + '.input2Y', input2YSet)

        return ctrlDrvMDN

    def mult_or_div_connect_attr(self, name, input2X, input1X, operation=2, prefix='', nameExpr='', side=''):
        ctrlDrvMDN = mc.createNode('multiplyDivide',
                                   n=au.prefix_name(name) + prefix + nameExpr + 'Ctrl' + side + '_mdn')
        mc.setAttr(ctrlDrvMDN + '.operation', operation)
        mc.connectAttr(input1X , ctrlDrvMDN + '.input1X')
        mc.connectAttr(input2X, ctrlDrvMDN + '.input2X')

        return ctrlDrvMDN

    def multOrDivSetAttr(self, name, input_2X_set, input_1X, operation=2, prefix='', name_expression='', side=''):
        ctrl_drv_mdn = mc.createNode('multiplyDivide',
                                     n=au.prefix_name(name) + prefix + name_expression + 'Ctrl' + side + '_mdn')
        mc.setAttr(ctrl_drv_mdn + '.operation', operation)
        mc.connectAttr(input_1X, ctrl_drv_mdn + '.input1X')
        mc.setAttr(ctrl_drv_mdn + '.input2X', input_2X_set)

        return ctrl_drv_mdn

    def pma_set_attr(self, name, value_input0, input1, operation, prefix='', name_expression='', side=''):
        ctrlDrvPMA = mc.createNode('plusMinusAverage', n=au.prefix_name(name)
                                                         + prefix + name_expression + 'Ctrl' + side + '_pma')
        mc.setAttr(ctrlDrvPMA + '.operation', operation)
        mc.setAttr(ctrlDrvPMA + '.input1D[0]', value_input0)
        mc.connectAttr(input1, ctrlDrvPMA + '.input1D[1]')

        return ctrlDrvPMA

    def pma_attr(self, name, input0, input1, operation, input2='', prefix='', name_expression='', side='', input_two=False):
        ctrl_drv_pma = mc.createNode('plusMinusAverage', n=au.prefix_name(name)
                                                           + prefix + name_expression + 'Ctrl' + side + '_pma')
        mc.setAttr(ctrl_drv_pma + '.operation', operation)
        mc.connectAttr(input0, ctrl_drv_pma + '.input1D[0]')
        mc.connectAttr(input1, ctrl_drv_pma + '.input1D[1]')
        if input_two:
            mc.connectAttr(input2, ctrl_drv_pma + '.input1D[2]')
            return ctrl_drv_pma
        else:
            return ctrl_drv_pma

    def pma_two_attr(self, name, input_0x, input_1x, input_2x, input_0y, input_1y, input_2y, operation, prefix='', name_expression='', side=''):
        ctrlDrvPMA = mc.createNode('plusMinusAverage', n=au.prefix_name(name)
                                                         + prefix + name_expression + 'Ctrl' + side + '_pma')
        mc.setAttr(ctrlDrvPMA + '.operation', operation)
        mc.connectAttr(input_0x, ctrlDrvPMA + '.input2D[0].input2Dx')
        mc.connectAttr(input_1x, ctrlDrvPMA + '.input2D[1].input2Dx')
        mc.connectAttr(input_2x, ctrlDrvPMA + '.input2D[2].input2Dx')

        mc.connectAttr(input_0y, ctrlDrvPMA + '.input2D[0].input2Dy')
        mc.connectAttr(input_1y, ctrlDrvPMA + '.input2D[1].input2Dy')
        mc.connectAttr(input_2y, ctrlDrvPMA + '.input2D[2].input2Dy')

        return ctrlDrvPMA

    def mdl_connect_attr(self, name, prefix, name_expression, side, input1, input2):
        connect_drv_mdl = mc.createNode('multDoubleLinear', n=au.prefix_name(name) + prefix + name_expression + 'Ctrl' + side + '_mdl')
        mc.connectAttr(input1, connect_drv_mdl + '.input1')
        mc.connectAttr(input2, connect_drv_mdl + '.input2')

        return connect_drv_mdl

    def mdl_set_attr(self, name, prefix, name_expression, side, input1, input2_set):
        corner_lip_range_mdl = mc.createNode('multDoubleLinear', n=au.prefix_name(name) + prefix + name_expression + 'Ctrl' + side + '_mdl')
        mc.connectAttr(input1, corner_lip_range_mdl + '.input1')
        mc.setAttr(corner_lip_range_mdl + '.input2', input2_set)

        return corner_lip_range_mdl