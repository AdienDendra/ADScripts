from __future__ import absolute_import

import re

import maya.cmds as cmds

from rigging.library.base.face import lip as rlbf_lip, lipCorner as rlbf_lipCorner
from rigging.library.utils import controller as rlu_controller, transform as rlu_transform
from rigging.tools import utils as rt_utils


class Lip:
    def __init__(self,
                 face_anim_ctrl_grp,
                 face_utils_grp,
                 curve_up_lip_template,
                 curve_low_lip_template,
                 curve_up_lip_roll_template,
                 curve_low_lip_roll_template,
                 offset_jnt02_bind_position,
                 scale,
                 lip01_cheek_direction,
                 lip02_cheek_direction,
                 side_LFT,
                 side_RGT,
                 jaw_jnt,
                 head_low_jnt,
                 mouth_jnt,
                 position_mouth_ctrl,
                 suffix_controller,
                 jaw_ctrl,
                 prefix_upLip_follow,
                 prefix_degree_follow,
                 headLow_normal_rotationGrp,
                 base_module_nonTransform,
                 game_bind_joint,
                 ):

        # ==============================================================================================================
        #                                          LIP UP AND LOW CONTROLLER
        # ==============================================================================================================

        # UP LIP
        upLip = rlbf_lip.Build(curve_lip_template=curve_up_lip_template,
                               curve_lip_roll_template=curve_up_lip_roll_template,
                               offset_jnt02_bind_position=offset_jnt02_bind_position,
                               scale=scale,
                               lip01_cheek_direction=lip01_cheek_direction,
                               lip02_cheek_direction=lip02_cheek_direction,
                               side_LFT=side_LFT,
                               side_RGT=side_RGT,
                               mouth_jnt=mouth_jnt,
                               ctrl_color='yellow',
                               low_lip_controller=False,
                               suffix_controller=suffix_controller,
                               base_module_nonTransform=base_module_nonTransform,
                               game_bind_joint=game_bind_joint
                               )

        # LOW LIP
        lowLip = rlbf_lip.Build(curve_lip_template=curve_low_lip_template,
                                curve_lip_roll_template=curve_low_lip_roll_template,
                                offset_jnt02_bind_position=offset_jnt02_bind_position,
                                scale=scale,
                                lip01_cheek_direction=lip01_cheek_direction,
                                lip02_cheek_direction=lip02_cheek_direction,
                                side_LFT=side_LFT,
                                side_RGT=side_RGT,
                                mouth_jnt=mouth_jnt,
                                ctrl_color='red',
                                low_lip_controller=True,
                                suffix_controller=suffix_controller,
                                base_module_nonTransform=base_module_nonTransform,
                                game_bind_joint=game_bind_joint
                                )

        self.low_bind_jnt = lowLip.jnt_mid
        self.all_up_lip_joint = upLip.all_joint
        self.all_low_lip_joint = lowLip.all_joint

        self.upLip_all_joint = upLip.all_joint
        self.uplip_controller = upLip.controller

        self.lowLip_all_joint = lowLip.all_joint
        self.lowLip_controller = lowLip.controller

        # ================================================================================================================
        #                                               ASSIGN CURVE
        # =================================================================================================================
        curve_up_lip = upLip.curve_lip
        curve_low_lip = lowLip.curve_lip
        self.curve_up_lip = curve_up_lip
        self.curve_low_lip = curve_low_lip
        # ================================================================================================================
        #                                               UP LIP FOLLOW JAW
        # =================================================================================================================
        # CONTROLLER
        self.upLip_follow_jaw(jaw_ctrl=jaw_ctrl, prefix_degree_follow=prefix_degree_follow,
                              prefix_upLip_follow=prefix_upLip_follow, name='Ctrl', jaw_jnt=jaw_jnt,
                              headLow_normal_rotationGrp=headLow_normal_rotationGrp,
                              crv_up_lip=curve_up_lip, mouth_lip_grp=upLip.mouth_ctrl_grp,
                              mouth_offset_lip_grp=upLip.mouth_ctrl_grp_offset)
        # SETUP
        self.upLip_follow_jaw(jaw_ctrl=jaw_ctrl, prefix_degree_follow=prefix_degree_follow,
                              prefix_upLip_follow=prefix_upLip_follow, name='Setup', jaw_jnt=jaw_jnt,
                              headLow_normal_rotationGrp=headLow_normal_rotationGrp,
                              crv_up_lip=curve_up_lip, mouth_lip_grp=upLip.reset_all_mouth_ctrl_grp,
                              mouth_offset_lip_grp=upLip.reset_all_mouth_ctrl_grp_offset)

        # ================================================================================================================
        #                                             CORNER LIP CONTROLLER
        # =================================================================================================================

        # CONTROLLER RGT CORNER
        corner_lip_ctrl_RGT = rlbf_lipCorner.Build(
            match_pos_one=lowLip.jnt01_RGT,
            match_pos_two=upLip.jnt01_RGT,
            prefix='cornerLipDrv',
            scale=scale,
            sticky=True,
            side=side_RGT,
            suffix_controller=suffix_controller)

        self.corner_lip_ctrl_RGT = corner_lip_ctrl_RGT.control
        self.cheek_mid_attr_ctrl_RGT = corner_lip_ctrl_RGT.cheek_mid_ctrl
        self.cheek_low_attr_ctrl_RGT = corner_lip_ctrl_RGT.cheek_low_ctrl
        self.cheek_out_up_attr_ctrl_RGT = corner_lip_ctrl_RGT.cheek_out_up_ctrl
        self.cheek_out_low_attr_ctrl_RGT = corner_lip_ctrl_RGT.cheek_out_low_ctrl
        self.nostril_attr_ctrl_RGT = corner_lip_ctrl_RGT.nostril_ctrl
        self.lid_out_attr_ctrl_RGT = corner_lip_ctrl_RGT.lid_out_ctrl
        self.lid_attr_ctrl_RGT = corner_lip_ctrl_RGT.lid_ctrl

        # CONTROLLER LFT CORNER
        corner_lip_ctrl_LFT = rlbf_lipCorner.Build(
            match_pos_one=lowLip.jnt01_LFT,
            match_pos_two=upLip.jnt01_LFT,
            prefix='cornerLipDrv',
            scale=scale,
            sticky=True,
            side=side_LFT,
            suffix_controller=suffix_controller)

        self.corner_lip_ctrl_LFT = corner_lip_ctrl_LFT.control
        self.cheek_mid_attr_ctrl_LFT = corner_lip_ctrl_LFT.cheek_mid_ctrl
        self.cheek_low_attr_ctrl_LFT = corner_lip_ctrl_LFT.cheek_low_ctrl
        self.cheek_out_up_attr_ctrl_LFT = corner_lip_ctrl_LFT.cheek_out_up_ctrl
        self.cheek_out_low_attr_ctrl_LFT = corner_lip_ctrl_LFT.cheek_out_low_ctrl
        self.nostril_attr_ctrl_LFT = corner_lip_ctrl_LFT.nostril_ctrl
        self.lid_out_attr_ctrl_LFT = corner_lip_ctrl_LFT.lid_out_ctrl
        self.lid_attr_ctrl_LFT = corner_lip_ctrl_LFT.lid_ctrl

        # CREATE LOCATOR SET CORNER
        self.corner_lip_loc_set01_RGT = cmds.spaceLocator(n='cornerLipDrv01' + side_RGT + '_set')[0]
        self.corner_lip_loc_set01_LFT = cmds.spaceLocator(n='cornerLipDrv01' + side_LFT + '_set')[0]

        # PARENT LOCATOR SET TO GROUP
        corner_set_grp = cmds.createNode('transform', n='cornerLipDrvSet_grp')
        cmds.parent(self.corner_lip_loc_set01_RGT, self.corner_lip_loc_set01_LFT, corner_set_grp)

        # MATCH POSITION
        # PARENT CONSTRAINT CORNER LOCATOR SET
        cmds.parentConstraint(lowLip.locator_set01_RGT, upLip.locator_set01_RGT, self.corner_lip_loc_set01_RGT)
        cmds.parentConstraint(lowLip.locator_set01_LFT, upLip.locator_set01_LFT, self.corner_lip_loc_set01_LFT)

        # CONNECT CORNER LOCATOR TO CONTROLLER CORNER PARENT ZRO
        rt_utils.connect_attr_translate_rotate(self.corner_lip_loc_set01_RGT, corner_lip_ctrl_RGT.control_grp_zro)
        rt_utils.connect_attr_translate_rotate(self.corner_lip_loc_set01_LFT, corner_lip_ctrl_LFT.control_grp_zro)

        # CONNECT ALL MOUTH CTRL GRP (CENTER) TO CONTROLLER CORNER PARENT OFFSET
        rt_utils.connect_attr_scale(upLip.mouth_ctrl_grp, corner_lip_ctrl_RGT.control_grp_offset)
        rt_utils.connect_attr_scale(upLip.mouth_ctrl_grp, corner_lip_ctrl_LFT.control_grp_offset)

        # ==============================================================================================================
        #                                       LIP ALL CONTROLLER (CENTER)
        # ==============================================================================================================
        # ASSIGN ALL CONTROLLER LIP
        self.up_lip_controller_all = upLip.controller_all
        self.low_lip_controller_all = lowLip.controller_all
        self.low_reset_mouth_ctrl_grp_offset = lowLip.reset_mouth_ctrl_grp_offset
        self.up_lip_controller_all_grp_zro = upLip.controller_all_grp_zro
        self.up_lip_mouth_ctrl_grp = upLip.mouth_ctrl_grp

        # LOW LIP
        self.up_and_low_lip_setup(corner_lip_ctrl_RGT=corner_lip_ctrl_RGT, corner_lip_ctrl_LFT=corner_lip_ctrl_LFT,
                                  side_LFT=side_LFT,
                                  side_RGT=side_RGT, prefix_bind='LowBind', prefix_ctrl='LowCtrl', lip=lowLip,
                                  condition_low_lip=True)

        # UP LIP
        self.up_and_low_lip_setup(corner_lip_ctrl_RGT=corner_lip_ctrl_RGT, corner_lip_ctrl_LFT=corner_lip_ctrl_LFT,
                                  side_LFT=side_LFT,
                                  side_RGT=side_RGT, prefix_bind='upBind', prefix_ctrl='upCtrl', lip=upLip,
                                  condition_low_lip=False)

        # PARENT CONSTRAINT SET LOCATOR
        self.parent_constraint_set_locator(lip=upLip, up_lip=upLip, low_lip=lowLip, condition_low_lip=False,
                                           jaw_jnt=jaw_jnt, head_low_jnt=head_low_jnt)

        self.parent_constraint_set_locator(lip=lowLip, up_lip=upLip, low_lip=lowLip, condition_low_lip=True,
                                           jaw_jnt=jaw_jnt, head_low_jnt=head_low_jnt)

        # CONNECT ALL CONTROLLER TO ALL RESET GRP
        trans = self.reverse_low_lid(control=lowLip.controller_all, input_2X=1, input_2Y=-1, input_2Z=1,
                                     joint_bind_target=lowLip.reset_mouth_ctrl_grp_offset,
                                     name='Trans', connect='translate')

        rot = self.reverse_low_lid(control=lowLip.controller_all, input_2X=-1, input_2Y=1, input_2Z=-1,
                                   joint_bind_target=lowLip.reset_mouth_ctrl_grp_offset,
                                   name='Rot', connect='rotate')

        rt_utils.connect_attr_translate_rotate(upLip.controller_all, upLip.reset_mouth_ctrl_grp_offset)

        # CREATE JAW FOLLOW LOW LIP
        corner_adjust_LFT, jaw_following_LFT = self.multiply_lip_and_jaw(side=side_LFT, corner_adjust_ctrl='%s.%s' % (
            corner_lip_ctrl_LFT.control, corner_lip_ctrl_LFT.jaw_ud_ctrl),
                                                                         jaw_following_ctrl='%s.%s' % (
                                                                             corner_lip_ctrl_LFT.control,
                                                                             corner_lip_ctrl_LFT.jaw_following_ctrl))

        corner_adjust_RGT, jaw_following_RGT = self.multiply_lip_and_jaw(side=side_RGT, corner_adjust_ctrl='%s.%s' % (
            corner_lip_ctrl_RGT.control, corner_lip_ctrl_RGT.jaw_ud_ctrl),
                                                                         jaw_following_ctrl='%s.%s' % (
                                                                             corner_lip_ctrl_RGT.control,
                                                                             corner_lip_ctrl_RGT.jaw_following_ctrl))
        # UP LIP
        self.up_lip_jaw(side=side_LFT, mult_corner_adjust=corner_adjust_LFT, mult_jaw_following=jaw_following_LFT,
                        locator_set01=upLip.locator_set01_LFT,
                        reset_mouth_ctrl_grp_offset=upLip.reset_mouth_ctrl_grp_offset, name_w='W0', W0=True)

        self.up_lip_jaw(side=side_LFT, mult_corner_adjust=corner_adjust_LFT, mult_jaw_following=jaw_following_LFT,
                        locator_set01=upLip.locator_set01_LFT,
                        reset_mouth_ctrl_grp_offset=lowLip.reset_mouth_ctrl_grp_offset, name_w='W1', W0=False)

        self.up_lip_jaw(side=side_RGT, mult_corner_adjust=corner_adjust_RGT, mult_jaw_following=jaw_following_RGT,
                        locator_set01=upLip.locator_set01_RGT,
                        reset_mouth_ctrl_grp_offset=upLip.reset_mouth_ctrl_grp_offset, name_w='W0', W0=True)

        self.up_lip_jaw(side=side_RGT, mult_corner_adjust=corner_adjust_RGT, mult_jaw_following=jaw_following_RGT,
                        locator_set01=upLip.locator_set01_RGT,
                        reset_mouth_ctrl_grp_offset=lowLip.reset_mouth_ctrl_grp_offset, name_w='W1', W0=False)

        # LOW LIP
        self.low_lip_jaw(side=side_LFT, mult_corner_adjust=corner_adjust_LFT, mult_jaw_following=jaw_following_LFT,
                         locator_set01=lowLip.locator_set01_LFT,
                         reset_mouth_ctrl_grp_offset=upLip.reset_mouth_ctrl_grp_offset, name_w='W0', W0=True)

        self.low_lip_jaw(side=side_LFT, mult_corner_adjust=corner_adjust_LFT, mult_jaw_following=jaw_following_LFT,
                         locator_set01=lowLip.locator_set01_LFT,
                         reset_mouth_ctrl_grp_offset=lowLip.reset_mouth_ctrl_grp_offset, name_w='W1', W0=False)

        self.low_lip_jaw(side=side_RGT, mult_corner_adjust=corner_adjust_RGT, mult_jaw_following=jaw_following_RGT,
                         locator_set01=lowLip.locator_set01_RGT,
                         reset_mouth_ctrl_grp_offset=upLip.reset_mouth_ctrl_grp_offset, name_w='W0', W0=True)

        self.low_lip_jaw(side=side_RGT, mult_corner_adjust=corner_adjust_RGT, mult_jaw_following=jaw_following_RGT,
                         locator_set01=lowLip.locator_set01_RGT,
                         reset_mouth_ctrl_grp_offset=lowLip.reset_mouth_ctrl_grp_offset, name_w='W1', W0=False)

        # ==================================================================================================================
        #                                                   STICKY LIP
        # ==================================================================================================================

        xform_corner_lip_right = cmds.xform(self.corner_lip_loc_set01_RGT, ws=1, q=1, t=1)
        xform_corner_lip_left = cmds.xform(self.corner_lip_loc_set01_LFT, ws=1, q=1, t=1)

        sticky_lip_bind_crv = cmds.curve(ep=[(xform_corner_lip_right), (xform_corner_lip_left)],
                                         degree=3, n='lipBindSticky_crv')
        cmds.rebuildCurve(sticky_lip_bind_crv, ch=0, rpo=1, rt=0, end=1, kr=0, kcp=0,
                          kep=1, kt=0, s=8, d=3, tol=0.01)

        # STICKY BLENDSHAPE BIND UP AND LOW LIP
        cmds.blendShape(upLip.deform_curve, lowLip.deform_curve, sticky_lip_bind_crv, n=('lipSticky' + '_bsn'),
                        weight=[(0, 0.5), (1, 0.5)])

        # STICKY BLENDSHAPE STICKY TO LOW BIND MID
        cmds.blendShape(sticky_lip_bind_crv, lowLip.bind_sticky_mid_crv,
                        n=rt_utils.prefix_name(curve_low_lip) + 'BindStickyMid' + '_bsn',
                        weight=[(0, 1)])

        # STICKY BLENDSHAPE STICKY TO UP BIND MID
        cmds.blendShape(sticky_lip_bind_crv, upLip.bind_sticky_mid_crv,
                        n=rt_utils.prefix_name(curve_up_lip) + 'BindStickyMid' + '_bsn',
                        weight=[(0, 1)])

        # SET KEYFRAME FOR CONSTRAINT
        # LOW LIP SET
        self.set_value_sticky(constraint=lowLip.cluster_constraint, offset_value=0.5,
                              attribute_RGT=corner_lip_ctrl_RGT.sticky_ctrl,
                              attribute_LFT=corner_lip_ctrl_LFT.sticky_ctrl,
                              controller_RGT=corner_lip_ctrl_RGT.control, controller_LFT=corner_lip_ctrl_LFT.control,
                              lip_sticky_origin_locator_name='%sStickyOrigin' % rt_utils.prefix_name(curve_low_lip),
                              lip_sticky_mid_locator_name='%sStickyMid' % rt_utils.prefix_name(curve_low_lip))
        # UP LIP SET
        self.set_value_sticky(constraint=upLip.cluster_constraint, offset_value=0.5,
                              attribute_RGT=corner_lip_ctrl_RGT.sticky_ctrl,
                              attribute_LFT=corner_lip_ctrl_LFT.sticky_ctrl,
                              controller_RGT=corner_lip_ctrl_RGT.control, controller_LFT=corner_lip_ctrl_LFT.control,
                              lip_sticky_origin_locator_name='%sStickyOrigin' % rt_utils.prefix_name(curve_up_lip),
                              lip_sticky_mid_locator_name='%sStickyMid' % rt_utils.prefix_name(curve_up_lip))

        # ==================================================================================================================
        #                                                   MOUTH AIM
        # ==================================================================================================================

        self.mouth_controller = rlu_controller.Control(match_obj_first_position=None,
                                                       prefix='mouth',
                                                       shape=rlu_controller.LOCATOR, groups_ctrl=['Zro', 'Offset'],
                                                       ctrl_size=scale * 0.25,
                                                       ctrl_color='lightPink', lock_channels=['v', 's', 'r'])
        self.mouth_ctrl = self.mouth_controller.control
        self.mouth_ctrl_grp_offset = self.mouth_controller.parent_control[1]
        self.mouth_ctrl_grp_zro = self.mouth_controller.parent_control[0]

        # ADD ATTRIBUTE CONTROLLER ROLL
        rt_utils.add_attribute(objects=[self.mouth_controller.control], long_name=['rollSetup'], nice_name=[' '],
                               at="enum",
                               en='Add Setup', channel_box=True)

        self.controller_up_roll = rt_utils.add_attribute(objects=[self.mouth_controller.control],
                                                         long_name=['rollLipUpSkin'],
                                                         attributeType="float", dv=0, keyable=True)

        self.controller_low_roll = rt_utils.add_attribute(objects=[self.mouth_controller.control],
                                                          long_name=['rollLipLowSkin'],
                                                          attributeType="float", dv=0, keyable=True)

        self.cheek_in_up_attr = rt_utils.add_attribute(objects=[self.mouth_controller.control], long_name=['cheekInUp'],
                                                       attributeType="float", dv=1, min=0.001, keyable=True)

        self.nose_follow = rt_utils.add_attribute(objects=[self.mouth_controller.control], long_name=['noseFollow'],
                                                  attributeType="float", dv=1, min=0, keyable=True)

        self.mouth_ctrl_nose_follow = '%s.%s' % (self.mouth_ctrl, self.nose_follow)

        # CONNECT ROLL ATTRIBUTE CONTROLLER MID TO MDL LIP ROLL
        cmds.connectAttr(self.mouth_controller.control + '.%s' % self.controller_low_roll,
                         lowLip.lip_roll_mdl + '.input1')
        cmds.setAttr(lowLip.lip_roll_mdl + '.input2', 10)

        cmds.connectAttr(self.mouth_controller.control + '.%s' % self.controller_up_roll,
                         upLip.lip_roll_mdl + '.input1')
        cmds.setAttr(upLip.lip_roll_mdl + '.input2', -10)

        # CONNECT ROLL ATTRIBUTE CONTROLLER MID TO CONDITION ROLL ROLL
        for low, up, in zip(lowLip.condition, upLip.condition):
            cmds.connectAttr(self.mouth_controller.control + '.%s' % self.controller_low_roll, low + '.firstTerm')
            cmds.connectAttr(self.mouth_controller.control + '.%s' % self.controller_up_roll, up + '.firstTerm')

        # SET THE POSITION CONTROLLER
        cmds.delete(cmds.pointConstraint(upLip.controller_bind_mid.control, lowLip.controller_bind_mid.control,
                                         self.mouth_controller.parent_control[0]))
        tZ_value = cmds.getAttr(self.mouth_controller.parent_control[0] + '.translateZ')
        cmds.setAttr(self.mouth_controller.parent_control[0] + '.translateZ', tZ_value + (position_mouth_ctrl * scale))

        # AIM LOC OBJECT LOOK UP
        locator_aim = cmds.spaceLocator(n='mouthAim_loc')[0]
        locator_aim_grp = rlu_transform.create_parent_transform(parent_list=[''], object=locator_aim,
                                                                match_position=locator_aim,
                                                                prefix=rt_utils.prefix_name(locator_aim),
                                                                suffix='_loc')

        cmds.delete(cmds.parentConstraint(self.mouth_controller.control, locator_aim_grp[0]))
        tY_locator_value = cmds.getAttr(locator_aim_grp[0] + '.translateY')
        cmds.setAttr(locator_aim_grp[0] + '.translateY', tY_locator_value + (10 * scale))
        cmds.hide(locator_aim_grp[0])

        # AIM CONSTRAINT TO THE MOUTH JOINT
        cmds.aimConstraint(self.mouth_controller.control, mouth_jnt, mo=1, aimVector=(0, 0, 1), upVector=(0, 1, 0),
                           worldUpType='object', worldUpObject=locator_aim)

        # CONNECT ATTRIBUTE THE MOUTH AIM JOINT
        rt_utils.connect_attr_translate(self.mouth_controller.control, locator_aim)

        # PARENT CONSTRAINT HEAD LOW TO LOCATOR AIM GRP
        cmds.parentConstraint(head_low_jnt, locator_aim_grp[0], mo=1)
        cmds.scaleConstraint(head_low_jnt, locator_aim_grp[0], mo=1)

        # PARENT CONSTRAINT HEAD LOW TO PARENT MOUTH CONTROLLER
        cmds.parentConstraint(head_low_jnt, self.mouth_controller.parent_control[0], mo=1)
        cmds.scaleConstraint(head_low_jnt, self.mouth_controller.parent_control[0], mo=1)

        # ==================================================================================================================
        #                                                   PARENT GROUP
        # ==================================================================================================================
        self.lip = cmds.createNode('transform', n='lip_grp')
        self.controller_grp = cmds.createNode('transform', n='lipCtrlAll_grp')
        self.setup_grp = cmds.createNode('transform', n='lipSetup_grp')
        cmds.hide(self.setup_grp)

        cmds.parent(self.setup_grp, self.lip)
        cmds.parent(upLip.sticky_grp, lowLip.sticky_grp, upLip.utils_grp, lowLip.utils_grp, sticky_lip_bind_crv,
                    corner_set_grp,
                    locator_aim_grp[0], self.setup_grp)
        cmds.parent(self.mouth_controller.parent_control[0], corner_lip_ctrl_LFT.control_grp_zro,
                    corner_lip_ctrl_RGT.control_grp_zro, upLip.ctrl_grp, lowLip.ctrl_grp, self.controller_grp)

        cmds.parent(self.controller_grp, face_anim_ctrl_grp)
        cmds.parent(self.lip, face_utils_grp)

    # ==================================================================================================================
    #                                                   FUNCTIONS
    # ==================================================================================================================
    def upLip_follow_jaw(self, jaw_ctrl, prefix_upLip_follow, prefix_degree_follow, name, jaw_jnt,
                         headLow_normal_rotationGrp, crv_up_lip,
                         mouth_offset_lip_grp, mouth_lip_grp):

        # UPPERLIP FOLLOWING JAW
        upLipX_follow_jaw = cmds.createNode('transform',
                                            n=rt_utils.prefix_name(crv_up_lip) + 'DrvUp%sJawRotX_grp' % name)
        upLipYZ_follow_jaw = cmds.group(em=1, n=crv_up_lip + 'DrvUp%sJawRotYZ_grp' % name, p=upLipX_follow_jaw)
        cmds.delete(cmds.pointConstraint(jaw_jnt, upLipX_follow_jaw, mo=0))
        cmds.transformLimits(upLipX_follow_jaw, rx=(-45, 0), erx=(0, 1))

        # REPARENTING THE GROUP
        cmds.parent(upLipX_follow_jaw, mouth_lip_grp)
        cmds.parent(mouth_offset_lip_grp, upLipYZ_follow_jaw)

        # CONSTRAINT THE GROUP
        oc_upperLipX = cmds.orientConstraint(jaw_jnt, headLow_normal_rotationGrp, upLipX_follow_jaw, mo=1,
                                             skip=('y', 'z'))
        oc_upperLipYZ = cmds.orientConstraint(jaw_jnt, headLow_normal_rotationGrp, upLipYZ_follow_jaw, mo=1, skip='x')

        oc_upperLipX = rt_utils.constraint_rename(oc_upperLipX)[0]
        oc_upperLipYZ = rt_utils.constraint_rename(oc_upperLipYZ)[0]

        # CREATE MULTIPLY DIVIDE NODE
        scaling_value = cmds.createNode('multiplyDivide',
                                        n=rt_utils.prefix_name(crv_up_lip) + 'DrvUp%sJawRotXY_rev_mdn' % name)
        cmds.setAttr(scaling_value + '.operation', 2)
        cmds.connectAttr(jaw_ctrl + '.%s' % prefix_degree_follow, scaling_value + '.input1X')
        cmds.setAttr(scaling_value + '.input2X', 10)

        # CREATE CONDITION
        condition = cmds.createNode('condition', n=rt_utils.prefix_name(crv_up_lip) + 'DrvUp%sJawRotXY_cnd' % name)
        cmds.setAttr(condition + '.operation', 2)
        cmds.connectAttr(scaling_value + '.outputX', condition + '.colorIfTrueR')
        cmds.setAttr(condition + '.colorIfFalseR', 0)
        cmds.connectAttr(jaw_ctrl + '.%s' % prefix_upLip_follow, condition + '.firstTerm')

        # CREATE REVERSE
        reverse_follow_jaw_XY = cmds.createNode('reverse',
                                                n=rt_utils.prefix_name(crv_up_lip) + 'DrvUp%sJawRotXY_rev' % name)
        # mc.connectAttr(jaw_ctrl + '.%s' % prefix_upLip_follow, reverse_follow_jaw_XY + '.inputX')

        cmds.setDrivenKeyframe(reverse_follow_jaw_XY + '.inputX', cd=condition + '.outColorR', dv=0, v=0, itt='linear',
                               ott='linear')
        cmds.setDrivenKeyframe(reverse_follow_jaw_XY + '.inputX', cd=condition + '.outColorR', dv=1, v=1, itt='linear',
                               ott='linear')

        cmds.setDrivenKeyframe(oc_upperLipYZ + '.%sW0' % jaw_jnt, cd=condition + '.outColorR', dv=0, v=0, itt='linear',
                               ott='linear')
        cmds.setDrivenKeyframe(oc_upperLipYZ + '.%sW0' % jaw_jnt, cd=condition + '.outColorR', dv=1, v=1, itt='linear',
                               ott='linear')

        # CONNECT REVERSE TO CONSTRAINT
        cmds.connectAttr(reverse_follow_jaw_XY + '.outputX', oc_upperLipYZ + '.%sW1' % headLow_normal_rotationGrp)

        # CONNECT UPPER LIP FOLLOWING JAW CONSTRAINT
        # CREATE REVERSE
        reverse_follow_jaw_X = cmds.createNode('reverse',
                                               n=rt_utils.prefix_name(crv_up_lip) + 'DrvUp%sJawRotX_rev' % name)
        cmds.connectAttr(jaw_ctrl + '.%s' % prefix_upLip_follow, reverse_follow_jaw_X + '.inputX')

        # CONNECT TO OBJECT
        cmds.connectAttr(jaw_ctrl + '.%s' % prefix_upLip_follow, oc_upperLipX + '.%sW0' % jaw_jnt)
        cmds.connectAttr(reverse_follow_jaw_X + '.outputX', oc_upperLipX + '.%sW1' % headLow_normal_rotationGrp)

    def reverse_low_lid(self, control, input_2X, input_2Y, input_2Z, joint_bind_target, name, connect):
        mdn_reverse = cmds.createNode('multiplyDivide',
                                      n=rt_utils.prefix_name(control) + 'ReverseAllMouth' + name + '_mdn')
        cmds.connectAttr(control + '.%s' % connect, mdn_reverse + '.input1')

        cmds.setAttr(mdn_reverse + '.input2X', input_2X)
        cmds.setAttr(mdn_reverse + '.input2Y', input_2Y)
        cmds.setAttr(mdn_reverse + '.input2Z', input_2Z)

        # CONNECT TO OBJECT
        cmds.connectAttr(mdn_reverse + '.output', joint_bind_target + '.%s' % connect)

        return mdn_reverse

    def multiply_lip_and_jaw(self, side, corner_adjust_ctrl, jaw_following_ctrl):
        multCornerAdjust = cmds.createNode('multDoubleLinear', n='cornerAdjust' + side + '_mdl')
        cmds.setAttr(multCornerAdjust + '.input2', 0.1)
        cmds.connectAttr(corner_adjust_ctrl, multCornerAdjust + '.input1')

        multJawFollowing = cmds.createNode('multDoubleLinear', n='jawFollowing' + side + '_mdl')
        cmds.setAttr(multJawFollowing + '.input2', 0.1)
        cmds.connectAttr(jaw_following_ctrl, multJawFollowing + '.input1')

        return multCornerAdjust, multJawFollowing

    def jaw_following_subtract(self, side, mult_jaw_following, name_w, name):
        sum_both_adjust_and_follow = cmds.createNode('plusMinusAverage', n=name + name_w + side + '_pma')
        cmds.setAttr(sum_both_adjust_and_follow + '.operation', 2)
        cmds.setAttr(sum_both_adjust_and_follow + '.input1D[0]', 1.0)
        cmds.connectAttr(mult_jaw_following + '.output', sum_both_adjust_and_follow + '.input1D[1]')

        return sum_both_adjust_and_follow

    def up_lip_jaw(self, side, mult_corner_adjust, mult_jaw_following, locator_set01, reset_mouth_ctrl_grp_offset,
                   name_w, W0=True):

        mult_both_adjust_and_follow = cmds.createNode('multDoubleLinear',
                                                      n='upLipJawFolCornerAdjust' + name_w + side + '_mdl')
        cmds.connectAttr(mult_corner_adjust + '.output', mult_both_adjust_and_follow + '.input1')
        cmds.connectAttr(mult_jaw_following + '.output', mult_both_adjust_and_follow + '.input2')

        if W0:
            sum_both_adjust_and_follow = self.jaw_following_subtract(side, mult_jaw_following, name_w,
                                                                     name='upLipJawFolSum')
            value_min_w0 = cmds.createNode('plusMinusAverage', n='upLipValueJawFolCornerAdjustW0' + side + '_pma')
            cmds.connectAttr(mult_both_adjust_and_follow + '.output', value_min_w0 + '.input1D[0]')
            cmds.connectAttr(sum_both_adjust_and_follow + '.output1D', value_min_w0 + '.input1D[1]')

            cmds.connectAttr(value_min_w0 + '.output1D',
                             '%s_pac.%sW0' % (locator_set01, reset_mouth_ctrl_grp_offset))

        else:
            value_min_w1 = cmds.createNode('plusMinusAverage', n='upLipValueJawFolCornerAdjustW1' + side + '_pma')
            cmds.setAttr(value_min_w1 + '.operation', 2)
            cmds.connectAttr(mult_jaw_following + '.output', value_min_w1 + '.input1D[0]')
            cmds.connectAttr(mult_both_adjust_and_follow + '.output', value_min_w1 + '.input1D[1]')

            cmds.connectAttr(value_min_w1 + '.output1D',
                             '%s_pac.%sW1' % (locator_set01, reset_mouth_ctrl_grp_offset))

    def low_lip_jaw(self, side, mult_corner_adjust, mult_jaw_following, locator_set01, reset_mouth_ctrl_grp_offset,
                    name_w, W0=True):

        value_corner_lip = self.jaw_following_subtract(side, mult_jaw_following, name_w, name='lowLipValueJawFol')
        mult_both_adjust_and_follow = cmds.createNode('multDoubleLinear',
                                                      n='lowLipJawFolCornerAdjust' + name_w + side + '_mdl')
        cmds.connectAttr(mult_corner_adjust + '.output', mult_both_adjust_and_follow + '.input1')
        cmds.connectAttr(value_corner_lip + '.output1D', mult_both_adjust_and_follow + '.input2')

        if W0:
            subtract_both_adjust_and_follow = self.jaw_following_subtract(side, mult_jaw_following, name_w,
                                                                          name='lowLipJawFolSubtract')
            value_min_w0 = cmds.createNode('plusMinusAverage', n='lowLipValueJawFolCornerAdjustW0' + side + '_pma')
            cmds.setAttr(value_min_w0 + '.operation', 2)
            cmds.connectAttr(subtract_both_adjust_and_follow + '.output1D', value_min_w0 + '.input1D[0]')
            cmds.connectAttr(mult_both_adjust_and_follow + '.output', value_min_w0 + '.input1D[1]')

            cmds.connectAttr(value_min_w0 + '.output1D',
                             '%s_pac.%sW0' % (locator_set01, reset_mouth_ctrl_grp_offset))

        else:
            value_min_w1 = cmds.createNode('plusMinusAverage', n='lowLipValueJawFolCornerAdjustW1' + side + '_pma')
            cmds.connectAttr(mult_jaw_following + '.output', value_min_w1 + '.input1D[0]')
            cmds.connectAttr(mult_both_adjust_and_follow + '.output', value_min_w1 + '.input1D[1]')

            cmds.connectAttr(value_min_w1 + '.output1D',
                             '%s_pac.%sW1' % (locator_set01, reset_mouth_ctrl_grp_offset))

    def parent_constraint_set_locator(self, lip, up_lip, low_lip, condition_low_lip, jaw_jnt, head_low_jnt):
        # parent constraint 01 set locator
        right_constraint = \
        cmds.parentConstraint(up_lip.reset_mouth_ctrl_grp_offset, low_lip.reset_mouth_ctrl_grp_offset,
                              lip.locator_set01_RGT, mo=1)[0]
        cmds.setAttr(right_constraint + '.interpType', 2)

        left_constraint = cmds.parentConstraint(up_lip.reset_mouth_ctrl_grp_offset, low_lip.reset_mouth_ctrl_grp_offset,
                                                lip.locator_set01_LFT, mo=1)[0]
        cmds.setAttr(left_constraint + '.interpType', 2)

        # PARENT CONSTRAINT MID LOCATOR
        pac_mid_loc_constraint = cmds.parentConstraint(lip.reset_mouth_ctrl_grp_offset, lip.locator_set_mid, mo=1)

        # SET THE VALUE
        cmds.setAttr(right_constraint + '.%sW0' % up_lip.reset_mouth_ctrl_grp_offset, 0.5)
        cmds.setAttr(right_constraint + '.%sW1' % low_lip.reset_mouth_ctrl_grp_offset, 0.5)
        cmds.setAttr(left_constraint + '.%sW0' % up_lip.reset_mouth_ctrl_grp_offset, 0.5)
        cmds.setAttr(left_constraint + '.%sW1' % low_lip.reset_mouth_ctrl_grp_offset, 0.5)

        if condition_low_lip:
            pac_reset_all_ctrl_cons = rt_utils.parent_scale_constraint(jaw_jnt, lip.reset_all_mouth_ctrl_grp, mo=1)
            pac_mouth_ctrl_cons = rt_utils.parent_scale_constraint(jaw_jnt, lip.mouth_ctrl_grp, mo=1)
        else:
            cons_mouth_reset = rt_utils.parent_scale_constraint(head_low_jnt, lip.reset_all_mouth_ctrl_grp, mo=1)[0]
            cons_mouth_ctrl = rt_utils.parent_scale_constraint(head_low_jnt, lip.mouth_ctrl_grp, mo=1)[0]

        # constraint rename
        rt_utils.constraint_rename([right_constraint, left_constraint, pac_mid_loc_constraint[0]])

    def up_and_low_lip_setup(self, corner_lip_ctrl_RGT, corner_lip_ctrl_LFT, side_LFT, side_RGT,
                             prefix_bind, prefix_ctrl,
                             lip, condition_low_lip=True):
        # CONNECT CORNER CONTROLLER TO OFFSET BIND JNT
        self.reverse_corner_bind_grp_offset_direction(corner_ctrl=corner_lip_ctrl_RGT, prefix=prefix_bind,
                                                      side=side_RGT,
                                                      jnt_bind_grp_offset=lip.joint_bind01_RGT_grp[1], side_RGT=True)

        self.reverse_corner_bind_grp_offset_direction(corner_ctrl=corner_lip_ctrl_LFT, prefix=prefix_bind,
                                                      side=side_LFT,
                                                      jnt_bind_grp_offset=lip.joint_bind01_LFT_grp[1], side_RGT=False)

        # CONNECT ROTATION LOCATOR OFFSET LOWLIP OF JAW ROTATION
        for item in lip.locator_group_offset:
            rt_utils.connect_attr_rotate(lip.locator_set_mid, item)

        cmds.parentConstraint(lip.reset_mouth_ctrl_grp_offset, lip.locator_set_mid, mo=1)

        # CONNECT SET LOCATOR TO JOINT BIND GRP ZRO AND CONTROLLER BIND GRP ZRO
        rt_utils.connect_attr_translate_rotate(lip.locator_set_mid, lip.controller_bind_mid.parent_control[0])
        rt_utils.connect_attr_translate_rotate(lip.locator_set_mid, lip.joint_bind_mid_grp[0])

        # CONNECT SET LOCATOR TO JOINT BIND GRP ZRO AND CONTROLLER BIND GRP ZRO
        rt_utils.connect_attr_translate_rotate(lip.locator_set01_RGT, lip.controller_bind01_RGT.parent_control[0])
        rt_utils.connect_attr_translate_rotate(lip.locator_set01_RGT, lip.joint_bind01_RGT_grp[0])

        rt_utils.connect_attr_translate_rotate(lip.locator_set01_LFT, lip.controller_bind01_LFT.parent_control[0])
        rt_utils.connect_attr_translate_rotate(lip.locator_set01_LFT, lip.joint_bind01_LFT_grp[0])

        # CONNECT CORNER CONTROLLER TO CONTROLLER 01 OFFSET GRP
        self.reverse_corner_ctrl_direction(corner_ctrl=corner_lip_ctrl_RGT, prefix=prefix_ctrl, side=side_RGT,
                                           ctrl_bind_grp_offset=lip.controller_bind01_RGT.parent_control[2],
                                           condition_low_lip=condition_low_lip)

        self.reverse_corner_ctrl_direction(corner_ctrl=corner_lip_ctrl_LFT, prefix=prefix_ctrl, side=side_LFT,
                                           ctrl_bind_grp_offset=lip.controller_bind01_LFT.parent_control[2],
                                           condition_low_lip=condition_low_lip)

    def set_value_sticky(self, offset_value, constraint, attribute_RGT, attribute_LFT, controller_RGT, controller_LFT,
                         lip_sticky_origin_locator_name,
                         lip_sticky_mid_locator_name):
        len_constraint = len(constraint)
        constraint_right = constraint[0:int((len_constraint - 1) / 2)]
        constraint_left = constraint[int((len_constraint + 1) / 2):]
        constraint_left = constraint_left[::-1]

        list_part = len(constraint[0:int((len_constraint + 1) / 2)])
        sticky_value = 10
        result = sticky_value / float(list_part)

        # RIGHT SIDE
        self.set_keyframe_sticky(result=result, constraint_side=constraint_right,
                                 lip_sticky_origin_locator_name=lip_sticky_origin_locator_name,
                                 controller=controller_RGT, attribute=attribute_RGT, offset_value=offset_value,
                                 lip_sticky_mid_locator_name=lip_sticky_mid_locator_name)

        # LEFT SIDE
        self.set_keyframe_sticky(result=result, constraint_side=constraint_left,
                                 lip_sticky_origin_locator_name=lip_sticky_origin_locator_name,
                                 controller=controller_LFT, attribute=attribute_LFT, offset_value=offset_value,
                                 lip_sticky_mid_locator_name=lip_sticky_mid_locator_name)

        # MID
        mid_constraint = constraint[int((len_constraint - 1) / 2)]

        # MID RIGHT
        self.set_keyframe_sticky_mid(result=result, mid_cons=mid_constraint,
                                     lip_sticky_origin_locator_name=lip_sticky_origin_locator_name,
                                     controller=controller_RGT, attribute=attribute_RGT, offset_value=offset_value,
                                     lip_sticky_mid_locator_name=lip_sticky_mid_locator_name)
        # MID LEFT
        self.set_keyframe_sticky_mid(result=result, mid_cons=mid_constraint,
                                     lip_sticky_origin_locator_name=lip_sticky_origin_locator_name,
                                     controller=controller_LFT, attribute=attribute_LFT, offset_value=offset_value,
                                     lip_sticky_mid_locator_name=lip_sticky_mid_locator_name)

    def set_keyframe_sticky_mid(self, result, mid_cons, lip_sticky_origin_locator_name, controller, attribute,
                                offset_value,
                                lip_sticky_mid_locator_name):

        prefix = self.get_number_of_list(mid_cons)
        driverVal = float(prefix)

        cmds.setDrivenKeyframe(mid_cons + '.%s%s%sW0' % (lip_sticky_origin_locator_name, prefix, '_loc'),
                               cd='%s.%s' % (controller, attribute),
                               dv=((driverVal - 2) * result) * (offset_value * 1.05), v=0.5, itt='auto', ott='auto')
        cmds.setDrivenKeyframe(mid_cons + '.%s%s%sW0' % (lip_sticky_origin_locator_name, prefix, '_loc'),
                               cd='%s.%s' % (controller, attribute),
                               dv=((driverVal - 2) * result) + result, v=0, itt='auto', ott='auto')

        cmds.setDrivenKeyframe(mid_cons + '.%s%s%sW1' % (lip_sticky_mid_locator_name, prefix, '_loc'),
                               cd='%s.%s' % (controller, attribute),
                               dv=((driverVal - 2) * result) * (offset_value * 1.05), v=0, itt='auto', ott='auto')
        cmds.setDrivenKeyframe(mid_cons + '.%s%s%sW1' % (lip_sticky_mid_locator_name, prefix, '_loc'),
                               cd='%s.%s' % (controller, attribute),
                               dv=((driverVal - 2) * result) + result, v=0.5, itt='auto', ott='auto')

    def set_keyframe_sticky(self, result, constraint_side, lip_sticky_origin_locator_name, controller, attribute,
                            offset_value,
                            lip_sticky_mid_locator_name):

        for n, i in enumerate(constraint_side):
            prefix = self.get_number_of_list(i)

            cmds.setDrivenKeyframe(i + '.%s%s%sW0' % (lip_sticky_origin_locator_name, prefix, '_loc'),
                                   cd='%s.%s' % (controller, attribute),
                                   dv=(float(n) * result) * offset_value, v=1, itt='auto', ott='auto')
            cmds.setDrivenKeyframe(i + '.%s%s%sW0' % (lip_sticky_origin_locator_name, prefix, '_loc'),
                                   cd='%s.%s' % (controller, attribute),
                                   dv=(float(n) * result) + result, v=0, itt='auto', ott='auto')

            cmds.setDrivenKeyframe(i + '.%s%s%sW1' % (lip_sticky_mid_locator_name, prefix, '_loc'),
                                   cd='%s.%s' % (controller, attribute),
                                   dv=(float(n) * result) * offset_value, v=0, itt='auto', ott='auto')
            cmds.setDrivenKeyframe(i + '.%s%s%sW1' % (lip_sticky_mid_locator_name, prefix, '_loc'),
                                   cd='%s.%s' % (controller, attribute),
                                   dv=(float(n) * result) + result, v=1, itt='auto', ott='auto')

    def get_number_of_list(self, object):
        patterns = [r'\d+']
        prefix = rt_utils.prefix_name(object)
        for p in patterns:
            prefix = re.findall(p, prefix)[0]
        return prefix

    def reverse_corner_bind_grp_offset_direction(self, corner_ctrl, prefix, side, jnt_bind_grp_offset, side_RGT):
        mdn_reverse_trans = cmds.createNode('multiplyDivide', n='cornerLip' + prefix + 'ReverseTrans' + side + '_mdn')
        mdn_reverse_rotate = cmds.createNode('multiplyDivide', n='cornerLip' + prefix + 'ReverseRot' + side + '_mdn')

        if side_RGT:
            cmds.setAttr(mdn_reverse_trans + '.input2X', -1)
            cmds.setAttr(mdn_reverse_rotate + '.input2Z', -1)

            # CONNECT TRANSLATE
            cmds.connectAttr(corner_ctrl.control + '.translate', mdn_reverse_trans + '.input1')
            cmds.connectAttr(mdn_reverse_trans + '.output', jnt_bind_grp_offset + '.translate')

            # CONNECT ROTATE
            cmds.connectAttr(corner_ctrl.control + '.rotate', mdn_reverse_rotate + '.input1')
            cmds.connectAttr(mdn_reverse_rotate + '.output', jnt_bind_grp_offset + '.rotate')

        else:
            rt_utils.connect_attr_translate_rotate(corner_ctrl.control, jnt_bind_grp_offset)

    def reverse_corner_ctrl_direction(self, corner_ctrl, prefix, side, ctrl_bind_grp_offset, condition_low_lip):
        # CHECK POSITION
        pos = cmds.xform(corner_ctrl.control, ws=1, q=1, t=1)[0]

        if condition_low_lip:
            # ADD NODE FOR DRIVING BIND CONTROLLER 01 OFFSET
            mdn_reverse_trans = cmds.createNode('multiplyDivide',
                                                n='cornerLip' + prefix + 'ReverseTrans' + side + '_mdn')
            mdn_reverse_rotate = cmds.createNode('multiplyDivide',
                                                 n='cornerLip' + prefix + 'ReverseRot' + side + '_mdn')

            cmds.setAttr(mdn_reverse_trans + '.input2X', 1)
            cmds.setAttr(mdn_reverse_trans + '.input2Y', -1)
            cmds.setAttr(mdn_reverse_trans + '.input2Z', 1)

            cmds.setAttr(mdn_reverse_rotate + '.input2X', -1)
            cmds.setAttr(mdn_reverse_rotate + '.input2Y', 1)
            cmds.setAttr(mdn_reverse_rotate + '.input2Z', -1)

            cmds.connectAttr(corner_ctrl.control + '.rotate', mdn_reverse_rotate + '.input1')
            cmds.connectAttr(corner_ctrl.control + '.translate', mdn_reverse_trans + '.input1')

            # CONNECTING LIP CORNER CONTROL TO BIND CONTROLLER PARENT GRP OFFSET
            cmds.connectAttr(mdn_reverse_rotate + '.output', ctrl_bind_grp_offset + '.rotate')
            cmds.connectAttr(mdn_reverse_trans + '.output', ctrl_bind_grp_offset + '.translate')

        else:
            rt_utils.connect_attr_translate_rotate(corner_ctrl.control, ctrl_bind_grp_offset)
