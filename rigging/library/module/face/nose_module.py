from __builtin__ import reload

import maya.cmds as mc

from rigging.library.base.face import wire as wr, nose as ns
from rigging.library.utils import controller as ct
from rigging.library.utils import transform as tf
from rigging.tools import AD_utils as au

reload(ct)
reload(tf)
reload(au)
reload(ns)
reload(wr)


class Nose:
    def __init__(self,
                 face_utils_grp,
                 columella_jnt,
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
                 jaw_ctrl,
                 suffix_controller,
                 base_module_nonTransform,
                 mouth_ctrl_nose_follow
                 ):
        # ==================================================================================================================
        #                                               NOSE CONTROLLER
        # ==================================================================================================================
        columella_ctrl = ns.Build(columella_jnt, columella_prefix, suffix_controller, scale)

        wire = wr.Build(curve_template=curve_template_nose, position_joint_direction=nose_jnt, scale=scale,
                        side_LFT=side_LFT, side_RGT=side_RGT, side='',
                        offset_jnt02_bind_position=offset_jnt02_bind_position,
                        offset_jnt04_bind_position=offset_jnt04_bind_position,
                        ctrl01_direction=ctrl01_direction, ctrl02_direction=ctrl02_direction,
                        ctrl03_direction=ctrl03_direction, ctrl04_direction=ctrl04_direction,
                        ctrl05_direction=ctrl05_direction,
                        ctrl_color=ctrl_color, wire_low_controller=False, shape=shape, face_utils_grp=face_utils_grp,
                        connect_with_corner_ctrl=False,
                        suffix_controller=suffix_controller, base_module_nonTransform=base_module_nonTransform,
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
        au.add_attribute(objects=[nose_controller.control], long_name=['weightSkinInfluence'], nice_name=[' '],
                         at="enum",
                         en='Weight Influence', channel_box=True)

        self.mouth_weight_ss = au.add_attribute(objects=[nose_controller.control], long_name=['squashStretch'],
                                                attributeType="float", min=0, dv=1, keyable=True)

        self.mouth_weight_up_down = au.add_attribute(objects=[nose_controller.control], long_name=['upDown'],
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
        mc.connectAttr(self.nose_ctrl_grp_offset + '.translate', self.nose_ctrl_translate_pma + '.input3D[1]')

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

        # ADD NOSE UP CONTROLLER
        nose_up_controller = ct.Control(match_obj_first_position=nose_up_jnt,
                                        prefix='noseUp',
                                        shape=ct.JOINT, groups_ctrl=['Zro'],
                                        ctrl_size=scale * 0.05,
                                        ctrl_color='turquoiseBlue', lock_channels=['v'])

        self.nose_up_controller_grp = nose_up_controller.parent_control[0]

        grp_nose_up_jnt = tf.create_parent_transform(parent_list=['Zro'], object=nose_up_jnt,
                                                     match_position=nose_up_jnt,
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

        range_ss = self.nose_ctrl + '.%s' % self.mouth_weight_ss
        range_ud = self.nose_ctrl + '.%s' % self.mouth_weight_up_down

        ####### NOSTRIL LEFT
        left_side = self.nostril_setup(side=side_LFT, attribute_offset=nostril_attr_ctrl_LFT,
                                       multiplier=1, nose_follow_mouth_value=nose_follow_mouth_value,
                                       controller_mouth=mouth_ctrl,
                                       controller_corner_lip=lip_corner_ctrl_LFT,
                                       controller_upper_lip=up_lip_controller_all,
                                       value_translateX=get_attr_grp_zro_bind_nostril_LFT[0],
                                       value_translateY=get_attr_grp_zro_bind_nostril_LFT[1],
                                       value_translateZ=get_attr_grp_zro_bind_nostril_LFT[2])

        ####### NOSTRIL RIGHT
        right_side = self.nostril_setup(side=side_RGT, attribute_offset=nostril_attr_ctrl_RGT,
                                        multiplier=-1, nose_follow_mouth_value=nose_follow_mouth_value,
                                        controller_mouth=mouth_ctrl,
                                        controller_corner_lip=lip_corner_ctrl_RGT,
                                        controller_upper_lip=up_lip_controller_all,
                                        value_translateX=get_attr_grp_zro_bind_nostril_RGT[0],
                                        value_translateY=get_attr_grp_zro_bind_nostril_RGT[1],
                                        value_translateZ=get_attr_grp_zro_bind_nostril_RGT[2])

        # CONNECT TO TRANSLATE ATTRIBUTE GRP BIND
        mc.connectAttr(left_side[0] + '.output1D', joint_bind05_grp + '.translateX')
        mc.connectAttr(left_side[1] + '.output1D', joint_bind05_grp + '.translateY')
        mc.connectAttr(left_side[2] + '.output1D', joint_bind05_grp + '.translateZ')

        mc.connectAttr(right_side[0] + '.output1D', joint_bind01_grp + '.translateX')
        mc.connectAttr(right_side[1] + '.output1D', joint_bind01_grp + '.translateY')
        mc.connectAttr(right_side[2] + '.output1D', joint_bind01_grp + '.translateZ')

        ######## SQUASH STRETCH
        squash_stretch_node = self.squash_stretch_jaw_mouth_uplip(range_mouth=nose_follow_mouth_value * -48,
                                                                  mouth_ctrl_nose_follow=mouth_ctrl_nose_follow,
                                                                  input_1X_mouth=mouth_ctrl + '.translateY',
                                                                  range_lip=nose_follow_mouth_value * -24,
                                                                  input_1X_lip=up_lip_controller_all + '.translateY',
                                                                  input_1X_jaw=jaw_ctrl + '.rotateX',
                                                                  range_jaw=nose_follow_mouth_value * -6,
                                                                  )

        sum_squash_stretch = self.squash_stretch_great_less(jaw_ctrl=jaw_ctrl,
                                                            input_1X_great=squash_stretch_node[2] + '.output1D',
                                                            input_2X_great=range_ss,
                                                            input_1Y_great=squash_stretch_node[3] + '.output1D',
                                                            input_2Y_great=range_ss,
                                                            input_1X_less=squash_stretch_node[0] + '.output1D',
                                                            input_2X_less=range_ss,
                                                            input_1Y_less=squash_stretch_node[1] + '.output1D',
                                                            input_2Y_less=range_ss)

        # CONNECT SUM SQUASH STRETCH TO OBJECT
        mc.connectAttr(sum_squash_stretch + '.outColorR', self.nose_ctrl_scale_pma + '.input3D[1].input3Dx')
        mc.connectAttr(sum_squash_stretch + '.outColorG', self.nose_ctrl_scale_pma + '.input3D[1].input3Dy')

        ## OFFSET UP DOWN
        multiply_up_down = self.mdl_set_attr(name='nostrilWeight', prefix='UpDown', name_expression='', side='',
                                             input1=sum_squash_stretch + '.outColorG', input2_set=-0.2)

        multiply_up_down_nose = self.mdl_set_attr_up_down(name='nostrilWeight', prefix='UpDown', name_expression='Nose',
                                                          side='', input1=multiply_up_down + '.output', input2=range_ud)
        # CONNECT TO OFFSET GROUP
        mc.connectAttr(multiply_up_down_nose + '.output', self.nose_ctrl_grp_offset + '.translateY')

    # ==================================================================================================================
    #                                                    FUNCTION
    # ==================================================================================================================
    def squash_stretch_great_less(self, jaw_ctrl, input_1X_great, input_2X_great, input_1Y_great, input_2Y_great,
                                  input_1X_less, input_2X_less, input_1Y_less, input_2Y_less):
        # SQUASH STRETCH
        great = self.connect_attr_XY_value_weight(name='nostrilWeight',
                                                  input_1X=input_1X_great,
                                                  input_2X=input_2X_great,
                                                  input_1Y=input_1Y_great,
                                                  input_2Y=input_2Y_great,
                                                  operation=1,
                                                  prefix='Great')
        less = self.connect_attr_XY_value_weight(name='nostrilWeight',
                                                 input_1X=input_1X_less,
                                                 input_2X=input_2X_less,
                                                 input_1Y=input_1Y_less,
                                                 input_2Y=input_2Y_less,
                                                 operation=1,
                                                 prefix='Less')

        condition = mc.createNode('condition', n='nostrilWeightSquashStretch_cnd')
        mc.setAttr(condition + '.operation', 3)
        mc.connectAttr(jaw_ctrl + '.rotateX', condition + '.firstTerm')
        mc.connectAttr(less + '.outputX', condition + '.colorIfFalseR')
        mc.connectAttr(less + '.outputY', condition + '.colorIfFalseG')
        mc.connectAttr(great + '.outputX', condition + '.colorIfTrueR')
        mc.connectAttr(great + '.outputY', condition + '.colorIfTrueG')

        return condition

    def squash_stretch_jaw_mouth_uplip(self, range_mouth, mouth_ctrl_nose_follow, input_1X_mouth, range_lip,
                                       input_1X_lip, input_1X_jaw, range_jaw):
        mouth_nose_follow = self.connect_value_weight(name='nostrilWeight', input_2X=mouth_ctrl_nose_follow,
                                                      input_1X=input_1X_mouth,
                                                      operation=2, prefix='SquashStretch', name_expression='NoseFollow',
                                                      axis='',
                                                      side='')

        mouth = self.set_value_weight(name='nostrilWeight', input_2X_set=range_mouth,
                                      input_1X=mouth_nose_follow + '.outputX',
                                      operation=2, prefix='SquashStretch', name_expression='Mouth', side='')

        up_lip = self.set_value_weight(name='nostrilWeight', input_2X_set=range_lip, input_1X=input_1X_lip,
                                       operation=2, prefix='SquashStretch', name_expression='UpLip', side='')

        jaw_radian = self.set_value_weight(name='nostrilWeight', input_2X_set=0.0174533, input_1X=input_1X_jaw,
                                           operation=1, prefix='SquashStretch', name_expression='JawRadian', side='')

        jaw = self.set_value_weight(name='nostrilWeight', input_2X_set=range_jaw, input_1X=jaw_radian + '.outputX',
                                    operation=2, prefix='SquashStretch', name_expression='Jaw', side='')

        # SUBTRACT VALUE MULTIPLY
        # SQUASH X
        all_X_combine_value_ctrl = self.add_all_value_controller_squash_stretch(name='nostrilWeight', prefix='SsX',
                                                                                multiply_divide_output_second=mouth + '.outputX',
                                                                                multiply_divide_output_first=up_lip + '.outputX',
                                                                                side='',
                                                                                operation=2)
        # SQUASH Y
        all_Y_combine_value_ctrl = self.add_all_value_controller_squash_stretch(name='nostrilWeight', prefix='SsY',
                                                                                multiply_divide_output_second=mouth + '.outputX',
                                                                                multiply_divide_output_first=up_lip + '.outputX',
                                                                                side='',
                                                                                operation=1)
        # JAW
        jaw_X_combine_value_ctrl = self.add_all_value_controller_squash_stretch(name='nostrilWeight', prefix='JawX',
                                                                                multiply_divide_output_second=jaw + '.outputX',
                                                                                multiply_divide_output_first=all_X_combine_value_ctrl + '.output1D',
                                                                                side='',
                                                                                operation=1)

        jaw_Y_combine_value_ctrl = self.add_all_value_controller_squash_stretch(name='nostrilWeight', prefix='JawY',
                                                                                multiply_divide_output_second=jaw + '.outputX',
                                                                                multiply_divide_output_first=all_Y_combine_value_ctrl + '.output1D',
                                                                                side='',
                                                                                operation=2)

        return jaw_X_combine_value_ctrl, jaw_Y_combine_value_ctrl, all_X_combine_value_ctrl, all_Y_combine_value_ctrl

    def nostril_setup(self, side, attribute_offset,
                      multiplier, nose_follow_mouth_value, controller_mouth,
                      controller_corner_lip, controller_upper_lip, value_translateX, value_translateY,
                      value_translateZ):
        controller_lip_attribute = controller_corner_lip + '.%s' % attribute_offset
        mult_rev_nostril_trans_x = self.mdl_set_attr(name='nostrilWeight', prefix='TransX',
                                                     name_expression='MouthReverse',
                                                     side=side,
                                                     input1=controller_corner_lip + '.translateX ',
                                                     input2_set=multiplier)
        mult_rev_nostril_trans_x_out = mult_rev_nostril_trans_x + '.output'

        # TRANS X
        x_origin = self.set_value_weight_mouth_corner_lip(range_mouth=nose_follow_mouth_value * 36,
                                                          range_corner_lip=nose_follow_mouth_value * 6,
                                                          range_lip=nose_follow_mouth_value * 12,
                                                          input_1X_mouth=controller_mouth + '.translateX',
                                                          input_1X_corner_lip=mult_rev_nostril_trans_x_out,
                                                          input_1X_lip=controller_upper_lip + '.translateX',
                                                          prefix='TransX', side=side,
                                                          corner_lip_nostril_attribute=controller_lip_attribute,
                                                          value_translate=value_translateX,
                                                          axis='X'
                                                          )
        # TRANS Y
        y_origin = self.set_value_weight_mouth_corner_lip(range_mouth=nose_follow_mouth_value * 24,
                                                          range_corner_lip=nose_follow_mouth_value * 6,
                                                          range_lip=nose_follow_mouth_value * 12,
                                                          input_1X_mouth=controller_mouth + '.translateY',
                                                          input_1X_corner_lip=controller_corner_lip + '.translateY',
                                                          input_1X_lip=controller_upper_lip + '.translateY',
                                                          prefix='TransY', side=side,
                                                          corner_lip_nostril_attribute=controller_lip_attribute,
                                                          value_translate=value_translateY,
                                                          axis='Y'
                                                          )

        # TRANS Z
        z_origin = self.set_value_weight_mouth_corner_lip(range_mouth=nose_follow_mouth_value * 24,
                                                          range_corner_lip=nose_follow_mouth_value * 6,
                                                          range_lip=nose_follow_mouth_value * 12,
                                                          input_1X_mouth=controller_mouth + '.translateZ',
                                                          input_1X_corner_lip=controller_corner_lip + '.translateZ',
                                                          input_1X_lip=controller_upper_lip + '.translateZ',
                                                          prefix='TransZ', side=side,
                                                          corner_lip_nostril_attribute=controller_lip_attribute,
                                                          value_translate=value_translateZ,
                                                          axis='Z'
                                                          )

        return x_origin, y_origin, z_origin

    def set_value_weight_mouth_corner_lip(self, range_mouth, range_corner_lip, range_lip, input_1X_mouth,
                                          input_1X_corner_lip, input_1X_lip, prefix, side,
                                          corner_lip_nostril_attribute,
                                          value_translate, axis):
        mouth = self.set_value_weight(name='nostrilWeight', input_2X_set=range_mouth,
                                      input_1X=input_1X_mouth, operation=2, prefix=prefix,
                                      name_expression='Mouth', side=side)
        corner_lip = self.set_value_weight(name='nostrilWeight', input_2X_set=range_corner_lip,
                                           input_1X=input_1X_corner_lip, operation=2, prefix=prefix,
                                           name_expression='CornerLip', side=side)
        up_lip = self.set_value_weight(name='nostrilWeight', input_2X_set=range_lip, input_1X=input_1X_lip,
                                       operation=2, prefix=prefix, name_expression='UpLip', side=side)

        # SUM ALL VALUE MULTIPLY
        all_combine_value_ctrl = self.add_all_value_controller(multiply_divide_output_mouth=mouth,
                                                               multiply_divide_output_corner_lip=corner_lip,
                                                               multiply_divide_output_up_lip=up_lip,
                                                               axis= axis, side=side)

        # MULTIPLY WITH CORNER NOSTRIL ATTRIBUTE
        nostril_attribute_connect = self.connect_value_weight(name='nostrilWeight',
                                                              input_2X=corner_lip_nostril_attribute,
                                                              input_1X=all_combine_value_ctrl + '.output1D',
                                                              operation=1, prefix='CornerAttr', name_expression='',
                                                              axis=axis, side=side)
        # SUM WITH ORIGIN VALUE
        origin_attribute_value = self.set_attribute_value_origin(value_translate=value_translate,
                                                                 nostril_attribute_mdn=nostril_attribute_connect,
                                                                 side=side, axis=axis)

        return origin_attribute_value

    def connect_attr_XY_value_weight(self, name, input_1X, input_2X, input_1Y, input_2Y, operation, prefix):
        ctrl_drv_mdn = mc.createNode('multiplyDivide',
                                     n=name + prefix + 'Ctrl' + '_mdn')
        mc.setAttr(ctrl_drv_mdn + '.operation', operation)
        mc.connectAttr(input_1X, ctrl_drv_mdn + '.input1X')
        mc.connectAttr(input_2X, ctrl_drv_mdn + '.input2X')
        mc.connectAttr(input_1Y, ctrl_drv_mdn + '.input1Y')
        mc.connectAttr(input_2Y, ctrl_drv_mdn + '.input2Y')

        return ctrl_drv_mdn

    def connect_attr_X_value_weight(self, name, input_1X, input_2X, operation, prefix, side):
        ctrl_drv_mdn = mc.createNode('multiplyDivide',
                                     n=name + prefix + 'Ctrl' + side + '_mdn')
        mc.setAttr(ctrl_drv_mdn + '.operation', operation)
        mc.connectAttr(input_1X, ctrl_drv_mdn + '.input1X')
        mc.connectAttr(input_2X, ctrl_drv_mdn + '.input2X')

        return ctrl_drv_mdn

    def set_attribute_value_origin(self, value_translate, nostril_attribute_mdn, axis, side):
        ctrl_drv_pma = mc.createNode('plusMinusAverage', n='nostriWeightSetOrigin' + axis + side + '_pma')
        mc.setAttr(ctrl_drv_pma + '.operation', 1)
        mc.setAttr(ctrl_drv_pma + '.input1D[0]', value_translate)
        mc.connectAttr(nostril_attribute_mdn + '.outputX', ctrl_drv_pma + '.input1D[1]')

        return ctrl_drv_pma

    def add_all_value_controller_squash_stretch(self, name, prefix, multiply_divide_output_second,
                                                multiply_divide_output_first, side, operation):
        ctrl_drv_pma = mc.createNode('plusMinusAverage', n=name + prefix + side + '_pma')
        mc.setAttr(ctrl_drv_pma + '.operation', operation)
        mc.connectAttr(multiply_divide_output_first, ctrl_drv_pma + '.input1D[0]')
        mc.connectAttr(multiply_divide_output_second, ctrl_drv_pma + '.input1D[1]')

        return ctrl_drv_pma

    def add_all_value_controller(self, multiply_divide_output_mouth, multiply_divide_output_corner_lip,
                                 multiply_divide_output_up_lip, axis, side):
        ctrl_drv_pma = mc.createNode('plusMinusAverage', n='nostriWeightCombine' + axis  +'Ctrl'+ side + '_pma')
        mc.setAttr(ctrl_drv_pma + '.operation', 1)
        mc.connectAttr(multiply_divide_output_mouth + '.outputX', ctrl_drv_pma + '.input1D[0]')
        mc.connectAttr(multiply_divide_output_corner_lip + '.outputX', ctrl_drv_pma + '.input1D[1]')
        mc.connectAttr(multiply_divide_output_up_lip + '.outputX', ctrl_drv_pma + '.input1D[2]')

        return ctrl_drv_pma

    def set_value_weight(self, name, input_2X_set, input_1X, operation, prefix, name_expression, side):
        ctrl_drv_mdn = mc.createNode('multiplyDivide', n=name + prefix + name_expression + 'Ctrl' + side + '_mdn')
        mc.setAttr(ctrl_drv_mdn + '.operation', operation)
        mc.connectAttr(input_1X, ctrl_drv_mdn + '.input1X')
        mc.setAttr(ctrl_drv_mdn + '.input2X', input_2X_set)

        return ctrl_drv_mdn

    def connect_value_weight(self, name, input_2X, input_1X, operation, prefix, name_expression, axis, side):
        ctrl_drv_mdn = mc.createNode('multiplyDivide', n=name + prefix + name_expression+ axis + 'Ctrl' + side + '_mdn')
        mc.setAttr(ctrl_drv_mdn + '.operation', operation)
        mc.connectAttr(input_1X, ctrl_drv_mdn + '.input1X')
        mc.connectAttr(input_2X, ctrl_drv_mdn + '.input2X')

        return ctrl_drv_mdn

    def mdl_set_attr_up_down(self, name, prefix, name_expression, side, input1, input2):
        corner_lip_range_mdl = mc.createNode('multDoubleLinear',
                                             n=name + prefix + name_expression + 'Ctrl' + side + '_mdl')
        mc.connectAttr(input1, corner_lip_range_mdl + '.input1')
        mc.connectAttr(input2, corner_lip_range_mdl + '.input2')

        return corner_lip_range_mdl

    def mdl_set_attr(self, name, prefix, name_expression, side, input1, input2_set):
        corner_lip_range_mdl = mc.createNode('multDoubleLinear',
                                             n=name + prefix + name_expression + 'Ctrl' + side + '_mdl')
        mc.connectAttr(input1, corner_lip_range_mdl + '.input1')
        mc.setAttr(corner_lip_range_mdl + '.input2', input2_set)

        return corner_lip_range_mdl
