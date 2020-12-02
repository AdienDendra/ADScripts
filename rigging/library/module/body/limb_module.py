from __builtin__ import reload

import maya.cmds as mc

from rigging.library.base.body import limb_part_detail as dl, limb as lm, hand as hn
from rigging.library.module import base_module as gm, template_single_module as ds
from rigging.library.module.body import hand_module as hm, foot_module as fm
from rigging.library.utils import controller as ct, softIk_setup as rs, adding_attr_message as am, snap_joint as sl
from rigging.library.utils import pole_vector as pv
from rigging.tools import AD_utils as au

reload(gm)
reload(pv)
reload(ct)
reload(au)
reload(lm)
reload(hn)
reload(dl)
reload(ds)
reload(rs)
reload(hm)
reload(fm)
reload(am)
reload(sl)


class Limb:
    def __init__(self,
                 limb=None,
                 prefix=None,
                 prefix_upper_limb=None,
                 prefix_upper_limb_fk=None,
                 prefix_middle_limb_fk=None,
                 prefix_lower_limb_fk=None,
                 prefix_upper_limb_ik=None,
                 prefix_pole_vector_ik=None,
                 prefix_middle_limb_ik=None,
                 prefix_lower_limb_ik=None,
                 prefix_end_limb_ik=None,
                 prefix_limb_setup=None,
                 side=None,
                 upper_limb_jnt=None,
                 middle_limb_jnt=None,
                 lower_limb_jnt=None,
                 end_limb_jnt=None,
                 lower_limb_scale_jnt=None,
                 end_limb_scale_jnt=None,
                 upper_limb_fk_jnt=None,
                 middle_limb_fk_jnt=None,
                 lower_limb_fk_jnt=None,
                 upper_limb_ik_jnt=None,
                 middle_limb_ik_jnt=None,
                 lower_limb_ik_jnt=None,
                 end_limb_ik_jnt=None,
                 world=None,
                 upper_limb_twist_help_driver_jnt=None,
                 middle_limb_twist_help_driver_jnt=None,
                 clav_jnt=None,
                 pelvis_gimbal_ctrl=None,
                 parallel_axis=None,
                 tip_pos=None,
                 prefix_upper_limb_detail=None,
                 prefix_middle_limb_detail=None,
                 root_gimbal_ctrl=None,
                 singleModule=True,
                 size=1.0,
                 side_LFT=None,
                 side_RGT=None,

                 arm=None,
                 base_controller=None,
                 detail_limb_deformer=None,
                 number_detail_ctrl=None,
                 left_side=True,
                 end_limb=True,
                 game_bind_joint=None,
                 limb_bind_joint_parent_upper=None,
                 limb_bind_joint_parent_lower=None):

        """
        ###############################################################################################

        HOW TO CALL SINGLE MODULE:
        @:param > arm, True/False. True means arm, False means leg
        @:param > baseController, variable, module anim controller,
        @:param > detailLimbDeformer, True/False, True means has deformer, False means doesn't has
        @:param > numDtlCtrl, integer, number of detail/deformer controller
        @:param > leftSide, True/False, True means left side, False means right side
        @:param > size, float, can fill it in any number, use it if need it
        @:param > endLimb, True/False, True if add hand or leg, False is not

        ################################################################################################
        """

        if not mc.objExists('anim_ctrl'):
            mc.error('Please create the module controller first!')

            # single module
        if singleModule:
            if arm:
                if left_side:
                    if mc.objExists('upArmLFT_skn'):
                        mc.error('please clean up the left arm first!')
                    else:
                        self.joint_driver(arm=True)
                        self.single_module_arm(base_controller=base_controller, upper_limb_jnt=self.sj.upArm_LFT,
                                               middle_limb_jnt=self.sj.forearm_LFT, lower_limb_jnt=self.sj.wrist_LFT,
                                               upper_limb_fk_jnt=self.sFk.upArm_LFT,
                                               middle_limb_fk_jnt=self.sFk.forearm_LFT,
                                               lower_limb_fk_jnt=self.sFk.wrist_LFT,
                                               upper_limb_ik_jnt=self.sIk.upArm_LFT,
                                               middle_limb_ik_jnt=self.sIk.forearm_LFT,
                                               lower_limb_ik_jnt=self.sIk.wrist_LFT, end_limb_ik_jnt=self.sIk.hand_LFT,
                                               upper_limb_twist_help_driver_jnt=self.sTwistHelp.upArm_LFT,
                                               middle_limb_twist_help_driver_jnt=self.sTwistHelp.forearm_LFT,
                                               detail_limb_deformer=detail_limb_deformer,
                                               number_detail_ctrl=number_detail_ctrl, clav_jnt=self.sj.clav_LFT,
                                               parallel_axis='x', tip_pos='+',
                                               size=size, side='LFT',
                                               side_LFT=side_LFT,
                                               side_RGT=side_RGT)
                        if end_limb:
                            hm.Hand(parent=True, arm_object=self.part_control_grp, thumb_finger_base=self.sj.thumb1_LFT,
                                    thumb_finger_up=self.sj.thumb2_LFT, thumb_finger_mid=self.sj.thumb3_LFT,
                                    index_finger_base=self.sj.index1_LFT, index_finger_up=self.sj.index2_LFT,
                                    index_finger_mid=self.sj.index3_LFT, index_finger_low=self.sj.index4_LFT,
                                    middle_finger_base=self.sj.middle1_LFT,
                                    middle_finger_up=self.sj.middle2_LFT, middle_finger_mid=self.sj.middle3_LFT,
                                    middle_finger_low=self.sj.middle4_LFT,
                                    ring_finger_base=self.sj.ring1_LFT, ring_finger_up=self.sj.ring2_LFT,
                                    ring_finger_mid=self.sj.ring3_LFT, ring_finger_low=self.sj.ring4_LFT,
                                    pinky_finger_base=self.sj.pinky1_LFT,
                                    pinky_finger_up=self.sj.pinky2_LFT, pinky_finger_mid=self.sj.pinky3_LFT,
                                    pinky_finger_low=self.sj.pinky4_LFT,
                                    palm_jnt=self.sj.palm_LFT,
                                    wrist_jnt=self.sj.wrist_LFT,
                                    hand_jnt=self.sj.hand_LFT,
                                    side='LFT', size=size,
                                    single_module=singleModule)

                        # else:
                        #

                        mc.delete(self.sIk.hand_LFT, self.sIk.palm_LFT, self.sIk.thumb1_LFT,
                                  self.sFk.hand_LFT, self.sFk.palm_LFT, self.sFk.thumb1_LFT,
                                  self.sTwistHelp.hand_LFT, self.sTwistHelp.palm_LFT, self.sTwistHelp.thumb1_LFT)
                        mc.delete(self.sj.hand_LFT, self.sj.palm_LFT, self.sj.thumb1_LFT)

                        mc.delete(self.sj.root, self.ss.root, self.sFk.root, self.sIk.root, self.sTwistHelp.root,
                                  self.sAdd.root,
                                  )

                else:
                    if mc.objExists('upArmRGT_skn'):
                        mc.error('please clean up the right arm first!')
                    else:
                        self.joint_driver(arm=True)
                        self.single_module_arm(base_controller=base_controller, upper_limb_jnt=self.sj.upArm_RGT,
                                               middle_limb_jnt=self.sj.forearm_RGT, lower_limb_jnt=self.sj.wrist_RGT,
                                               upper_limb_fk_jnt=self.sFk.upArm_RGT,
                                               middle_limb_fk_jnt=self.sFk.forearm_RGT,
                                               lower_limb_fk_jnt=self.sFk.wrist_RGT,
                                               upper_limb_ik_jnt=self.sIk.upArm_RGT,
                                               middle_limb_ik_jnt=self.sIk.forearm_RGT,
                                               lower_limb_ik_jnt=self.sIk.wrist_RGT, end_limb_ik_jnt=self.sIk.hand_RGT,
                                               upper_limb_twist_help_driver_jnt=self.sTwistHelp.upArm_RGT,
                                               middle_limb_twist_help_driver_jnt=self.sTwistHelp.forearm_RGT,
                                               detail_limb_deformer=detail_limb_deformer,
                                               number_detail_ctrl=number_detail_ctrl, clav_jnt=self.sj.clav_RGT,
                                               parallel_axis='x',
                                               tip_pos='-',
                                               size=size, side='RGT',
                                               side_LFT=side_LFT,
                                               side_RGT=side_RGT)

                        if end_limb:
                            hm.Hand(parent=True, arm_object=self.part_control_grp, thumb_finger_base=self.sj.thumb1_RGT,
                                    thumb_finger_up=self.sj.thumb2_RGT, thumb_finger_mid=self.sj.thumb3_RGT,
                                    index_finger_base=self.sj.index1_RGT, index_finger_up=self.sj.index2_RGT,
                                    index_finger_mid=self.sj.index3_RGT, index_finger_low=self.sj.index4_RGT,
                                    middle_finger_base=self.sj.middle1_RGT,
                                    middle_finger_up=self.sj.middle2_RGT,
                                    middle_finger_mid=self.sj.middle3_RGT,
                                    middle_finger_low=self.sj.middle4_RGT,
                                    ring_finger_base=self.sj.ring1_RGT, ring_finger_up=self.sj.ring2_RGT,
                                    ring_finger_mid=self.sj.ring3_RGT, ring_finger_low=self.sj.ring4_RGT,
                                    pinky_finger_base=self.sj.pinky1_RGT,
                                    pinky_finger_up=self.sj.pinky2_RGT,
                                    pinky_finger_mid=self.sj.pinky3_RGT,
                                    pinky_finger_low=self.sj.pinky4_RGT,
                                    palm_jnt=self.sj.palm_RGT,
                                    wrist_jnt=self.sj.wrist_RGT,
                                    hand_jnt=self.sj.hand_RGT,
                                    side='RGT', size=size,
                                    single_module=singleModule)

                        # else:
                        mc.delete(self.sIk.hand_RGT, self.sIk.palm_RGT, self.sIk.thumb1_RGT,
                                  self.sFk.hand_RGT, self.sFk.palm_RGT, self.sFk.thumb1_RGT,
                                  self.sTwistHelp.hand_RGT, self.sTwistHelp.palm_RGT, self.sTwistHelp.thumb1_RGT)

                        mc.delete(self.sj.hand_RGT, self.sj.palm_RGT, self.sj.thumb1_RGT)
                        mc.delete(self.sj.root, self.ss.root, self.sFk.root, self.sIk.root, self.sTwistHelp.root,
                                  self.sAdd.root,
                                  )
            else:
                if left_side:
                    if mc.objExists('upLegLFT_skn'):
                        mc.error('please clean up the left leg first!')
                    else:
                        self.joint_driver(arm=False)
                        legLFT = self.single_module_leg(base_controller, upper_limb_jnt=self.sj.upLeg_LFT,
                                                        middle_limb_jnt=self.sj.lowLeg_LFT,
                                                        lower_limb_jnt=self.sj.ankle_LFT, end_limb_jnt=self.sj.ball_LFT,
                                                        lower_limb_scale_jnt=self.ss.ankle_LFT,
                                                        end_limb_scale_jnt=self.ss.ball_LFT,
                                                        upper_limb_fk_jnt=self.sFk.upLeg_LFT,
                                                        middle_limb_fk_jnt=self.sFk.lowLeg_LFT,
                                                        lower_limb_fk_jnt=self.sFk.ankle_LFT,
                                                        upper_limb_ik_jnt=self.sIk.upLeg_LFT,
                                                        middle_limb_ik_jnt=self.sIk.lowLeg_LFT,
                                                        lower_limb_ik_jnt=self.sIk.ankle_LFT,
                                                        end_limb_ik_jnt=self.sIk.ball_LFT,
                                                        upper_limb_twist_help_driver_jnt=self.sTwistHelp.upLeg_LFT,
                                                        middle_limb_twist_help_driver_jnt=self.sTwistHelp.lowLeg_LFT,
                                                        detail_limb_deformer=detail_limb_deformer,
                                                        number_detail_ctrl=number_detail_ctrl,
                                                        parallel_axis='y', tip_pos='-',
                                                        side='LFT', size=size,
                                                        side_LFT=side_LFT,
                                                        side_RGT=side_RGT)
                        if end_limb:
                            mc.delete(legLFT[0], legLFT[1])
                            fm.Foot(leg=True, foot=True, upper_limb_jnt=self.sj.upLeg_LFT,
                                    ball_fk_jnt=self.sFk.ball_LFT,
                                    ball_ik_jnt=self.sIk.ball_LFT, toe_ik_jnt=self.sIk.toe_LFT,
                                    ball_jnt=self.sj.ball_LFT,
                                    heel_jnt=self.sj.heel_LFT, lower_limb_jnt=self.sj.ankle_LFT,
                                    in_tilt_jnt=self.sj.footIn_LFT,
                                    out_tilt_jnt=self.sj.footOut_LFT, lower_gimbal_fk_ctrl=self.lower_limb_fk_gimbal,
                                    lower_limb_ik_hdl=self.lower_limb_ik_hdl, end_limb_ik_hdl=self.end_limb_ik_hdl,
                                    controller_FkIk_limb_setup=self.FkIk_limb_setup_controller, prefix_ball_fk='ballFk',
                                    prefix_toe_ik='toeIk',
                                    ball_scale_jnt=self.ss.ball_LFT,
                                    controller_lower_limb_ik=self.lower_limb_ik_control,
                                    position_soft_jnt=self.pos_soft_jnt,
                                    part_joint_grp_module=self.part_joint_grp, side='LFT', scale=size,
                                    single_module=singleModule,
                                    lower_limb_ik_gimbal=self.lower_limb_ik_gimbal,
                                    position_lower_limb_jnt=self.pos_lower_limb_jnt,
                                    lower_limb_ik_control=self.lower_limb_ik_control)

                            mc.delete(self.ss.heel_LFT, self.ss.toe_LFT, self.ss.footIn_LFT, self.ss.footOut_LFT,
                                      self.sj.heel_LFT, self.sj.toe_LFT, self.sj.footIn_LFT, self.sj.footOut_LFT,
                                      self.sIk.heel_LFT, self.sIk.toe_LFT, self.sIk.footIn_LFT, self.sIk.footOut_LFT)
                        else:
                            mc.delete(self.sj.ball_LFT)

                        mc.delete(self.sj.root, self.ss.root, self.sFk.root, self.sIk.root, self.sTwistHelp.root,
                                  self.sAdd.root, self.sTwistHelp.ball_LFT
                                  )

                else:
                    if mc.objExists('upLegRGT_skn'):
                        mc.error('please clean up the right leg first!')
                    else:
                        self.joint_driver(arm=False)
                        legRGT = self.single_module_leg(base_controller, upper_limb_jnt=self.sj.upLeg_RGT,
                                                        middle_limb_jnt=self.sj.lowLeg_RGT,
                                                        lower_limb_jnt=self.sj.ankle_RGT, end_limb_jnt=self.sj.ball_RGT,
                                                        lower_limb_scale_jnt=self.ss.ankle_RGT,
                                                        end_limb_scale_jnt=self.ss.ball_RGT,
                                                        upper_limb_fk_jnt=self.sFk.upLeg_RGT,
                                                        middle_limb_fk_jnt=self.sFk.lowLeg_RGT,
                                                        lower_limb_fk_jnt=self.sFk.ankle_RGT,
                                                        upper_limb_ik_jnt=self.sIk.upLeg_RGT,
                                                        middle_limb_ik_jnt=self.sIk.lowLeg_RGT,
                                                        lower_limb_ik_jnt=self.sIk.ankle_RGT,
                                                        end_limb_ik_jnt=self.sIk.ball_RGT,
                                                        upper_limb_twist_help_driver_jnt=self.sTwistHelp.upLeg_RGT,
                                                        middle_limb_twist_help_driver_jnt=self.sTwistHelp.lowLeg_RGT,
                                                        detail_limb_deformer=detail_limb_deformer,
                                                        number_detail_ctrl=number_detail_ctrl,
                                                        parallel_axis='y', tip_pos='-',
                                                        side='RGT', size=size,
                                                        side_LFT=side_LFT,
                                                        side_RGT=side_RGT)
                        if end_limb:
                            mc.delete(legRGT[0], legRGT[1])
                            fm.Foot(leg=True, foot=True, upper_limb_jnt=self.sj.upLeg_RGT,
                                    ball_fk_jnt=self.sFk.ball_RGT,
                                    ball_ik_jnt=self.sIk.ball_RGT, toe_ik_jnt=self.sIk.toe_RGT,
                                    ball_jnt=self.sj.ball_RGT,
                                    heel_jnt=self.sj.heel_RGT, lower_limb_jnt=self.sj.ankle_RGT,
                                    in_tilt_jnt=self.sj.footIn_RGT,
                                    out_tilt_jnt=self.sj.footOut_RGT, lower_gimbal_fk_ctrl=self.lower_limb_fk_gimbal,
                                    lower_limb_ik_hdl=self.lower_limb_ik_hdl, end_limb_ik_hdl=self.end_limb_ik_hdl,
                                    controller_FkIk_limb_setup=self.FkIk_limb_setup_controller, prefix_ball_fk='ballFk',
                                    prefix_toe_ik='toeIk',
                                    ball_scale_jnt=self.ss.ball_RGT,
                                    controller_lower_limb_ik=self.lower_limb_ik_control,
                                    position_soft_jnt=self.pos_soft_jnt,
                                    part_joint_grp_module=self.part_joint_grp, side='RGT', scale=size,
                                    single_module=singleModule,
                                    lower_limb_ik_gimbal=self.lower_limb_ik_gimbal,
                                    position_lower_limb_jnt=self.pos_lower_limb_jnt,
                                    lower_limb_ik_control=self.lower_limb_ik_control)

                            mc.delete(self.ss.heel_RGT, self.ss.toe_RGT, self.ss.footIn_RGT, self.ss.footOut_RGT,
                                      self.sj.heel_RGT, self.sj.toe_RGT, self.sj.footIn_RGT, self.sj.footOut_RGT,
                                      self.sIk.heel_RGT, self.sIk.toe_RGT, self.sIk.footIn_RGT, self.sIk.footOut_RGT)

                        else:
                            mc.delete(self.sj.ball_RGT)

                        mc.delete(self.sj.root, self.ss.root, self.sFk.root, self.sIk.root, self.sTwistHelp.root,
                                  self.sAdd.root, self.sTwistHelp.ball_RGT
                                  )
        else:
            if limb:
                self.module(arm, prefix, base_controller, prefix_upper_limb, prefix_upper_limb_fk,
                            prefix_middle_limb_fk,
                            prefix_lower_limb_fk, prefix_upper_limb_ik, prefix_pole_vector_ik, prefix_middle_limb_ik,
                            prefix_lower_limb_ik,
                            prefix_end_limb_ik, prefix_limb_setup, side, upper_limb_jnt, middle_limb_jnt,
                            lower_limb_jnt,
                            end_limb_jnt,
                            lower_limb_scale_jnt, end_limb_scale_jnt, upper_limb_fk_jnt, middle_limb_fk_jnt,
                            lower_limb_fk_jnt,
                            upper_limb_ik_jnt,
                            middle_limb_ik_jnt, lower_limb_ik_jnt, end_limb_ik_jnt, world,
                            upper_limb_twist_help_driver_jnt,
                            middle_limb_twist_help_driver_jnt,
                            clav_jnt, pelvis_gimbal_ctrl, detail_limb_deformer, number_detail_ctrl, parallel_axis,
                            tip_pos,
                            prefix_upper_limb_detail, prefix_middle_limb_detail, size, root_gimbal_ctrl, side_LFT,
                            side_RGT, game_bind_joint, limb_bind_joint_parent_upper, limb_bind_joint_parent_lower
                            )

                self.run_soft_ik = rs.run_soft_ik_joint(prefix=prefix, side=side,
                                                        lower_limb_ik_gimbal=self.lower_limb_ik_gimbal,
                                                        foot_reverse_joint_or_position_soft_jnt=self.pos_soft_jnt,
                                                        position_lower_limb_jnt=self.pos_lower_limb_jnt,
                                                        lowerLimbIkControl=self.lower_limb_ik_control)

            else:
                mc.delete(upper_limb_jnt)

    def module(self, arm, prefix, base_controller, prefix_upper_limb, prefix_upper_limb_fk, prefix_middle_limb_fk,
               prefix_lower_limb_fk, prefix_upper_limb_ik, prefix_pole_vector_ik, prefix_middle_limb_ik,
               prefix_lower_limb_ik,
               prefix_end_limb_ik, prefix_limb_setup, side, upper_limb_jnt, middle_limb_jnt, lower_limb_jnt,
               end_limb_jnt,
               lower_limb_scale_jnt, end_limb_scale_jnt, upper_limb_fk_jnt, middle_limb_fk_jnt, lower_limb_fk_jnt,
               upper_limb_ik_jnt,
               middle_limb_ik_jnt, lower_limb_ik_jnt, end_limb_ik_jnt, world, upper_limb_twist_help_driver_jnt,
               middle_limb_twist_help_driver_jnt,
               clav_jnt, pelvis_gimbal_ctrl, detail_limb_deformer, number_detail_ctrl, parallel_axis, tip_pos,
               prefix_upper_limb_detail, prefix_middle_limb_detail, size, root_gimbal_ctrl, side_LFT, side_RGT,
               game_bind_joint=None, limb_bind_joint_parent_upper=None, limb_bind_joint_parent_lower=None
               ):

        getValueTxLimbJnt = mc.xform(upper_limb_ik_jnt, ws=1, q=1, t=1)[0]

        ### GENERAL LIMB SETUP
        # limb position
        # create limb pole vector position
        ikh_vect_pos = mc.ikHandle(sj=upper_limb_ik_jnt, ee=lower_limb_ik_jnt, sol='ikRPsolver')
        loc_poleVector_position = pv.create_poleVec_locator(ikh_vect_pos[0], constraint=False, length=4 * size)

        # ==============================================================================================================
        #                                               IMPORT LIMB MODULE
        # ==============================================================================================================
        build_limb = lm.Build(
            arm=arm,
            prefix=prefix,
            prefix_upper_limb_dtl=prefix_upper_limb_detail,
            prefix_middle_limb_dtl=prefix_middle_limb_detail,
            prefix_upper_limb_fk=prefix_upper_limb_fk,
            prefix_middle_limb_fk=prefix_middle_limb_fk,
            prefix_lower_limb_fk=prefix_lower_limb_fk,
            prefix_upper_limb_ik=prefix_upper_limb_ik,
            prefix_pole_vector_ik=prefix_pole_vector_ik,
            prefix_middle_limb_ik=prefix_middle_limb_ik,
            prefix_lower_limb_ik=prefix_lower_limb_ik,
            prefix_end_limb_ik=prefix_end_limb_ik,
            prefix_limb_setup=prefix_limb_setup,
            side=side,
            upper_limb_jnt=upper_limb_jnt,
            middle_limb_jnt=middle_limb_jnt,
            lower_limb_jnt=lower_limb_jnt,
            upper_limb_fk_jnt=upper_limb_fk_jnt,
            middle_limb_fk_jnt=middle_limb_fk_jnt,
            lower_limb_fk_jnt=lower_limb_fk_jnt,
            upper_limb_ik_jnt=upper_limb_ik_jnt,
            middle_limb_ik_jnt=middle_limb_ik_jnt,
            pole_vector_ik_jnt=loc_poleVector_position[0],
            lower_limb_ik_jnt=lower_limb_ik_jnt,
            end_limb_ik_jnt=end_limb_ik_jnt,
            detail_limb_deformer=detail_limb_deformer,
            number_joints=number_detail_ctrl,
            scale=size)

        # delete locator pole vector pos
        mc.delete(loc_poleVector_position)

        self.prefix = prefix

        self.parent_cons_elm = None

        # build part of group hierarchy
        part = gm.Part(prefix=prefix, side=side)
        mc.parent(part.top_grp, base_controller.body_part_grp)

        self.part = part

        # instance the objects
        self.FkIk_limb_setup_controller_grp_zro = build_limb.controller_FkIk_limb_setup.parent_control[0]
        self.FkIk_limb_setup_controller = build_limb.controller_FkIk_limb_setup.control

        # Fk
        self.upper_limb_fk_controller_grp_zro = build_limb.controller_upper_limb_fk.parent_control[0]
        self.middle_limb_fk_controller_grp_zro = build_limb.controller_middle_limb_fk.parent_control[0]
        self.lower_limb_fk_controller_grp_zro = build_limb.controller_lower_limb_fk.parent_control[0]

        self.upper_limb_fk_gimbal = build_limb.controller_upper_limb_fk.control_gimbal
        self.middle_limb_fk_gimbal = build_limb.controller_middle_limb_fk.control_gimbal
        self.lower_limb_fk_gimbal = build_limb.controller_lower_limb_fk.control_gimbal

        self.upper_limb_fk_control = build_limb.controller_upper_limb_fk.control
        self.middle_limb_fk_control = build_limb.controller_middle_limb_fk.control
        self.lower_limb_fk_control = build_limb.controller_lower_limb_fk.control

        # Ik
        self.upper_limb_ik_controller_grp_zro = build_limb.controller_upper_limb_ik.parent_control[0]
        self.poleVector_ik_controller_grp_zro = build_limb.controller_pole_vector_ik.parent_control[0]
        self.lower_limb_ik_controller_grp_zro = build_limb.controller_lower_limb_ik.parent_control[0]
        self.poleVector_ik_control = build_limb.controller_pole_vector_ik.control

        self.upper_limb_ik_gimbal = build_limb.controller_upper_limb_ik.control_gimbal
        self.lower_limb_ik_gimbal = build_limb.controller_lower_limb_ik.control_gimbal
        self.upper_limb_ik_control = build_limb.controller_upper_limb_ik.control
        self.lower_limb_ik_control = build_limb.controller_lower_limb_ik.control

        # limb ikh
        self.lower_limb_ik_hdl = build_limb.lower_limb_ik_hdl[0]
        self.end_limb_ik_hdl = build_limb.end_limb_ik_hdl[0]

        ##### CONNECT MESSAGE ATTRIBUTE TO FK/IK CONTROLLER ATTRIBUTE
        # ADD MESSAGE ATTRIBUTE
        message = am.MessageAttribute(fkik_ctrl=self.FkIk_limb_setup_controller)

        # add joint reference
        message.add_joint_reference(upper_limb_jnt, middle_limb_jnt, lower_limb_jnt, side_LFT, side_RGT, side)

        if arm:
            self.shoulder_fk_locator = build_limb.shoulder_fk
            self.hip_fk_locator = build_limb.hip_fk
            self.world_fk_locator = build_limb.world_fk

            self.shoulder_ik_locator = build_limb.shoulder_ik
            self.hip_ik_locator = build_limb.hip_ik
            self.world_ik_locator = build_limb.world_ik

            ### FOLLOW ORIENTATION
            # constraining follow Fk
            mc.parent(self.shoulder_fk_locator, clav_jnt)
            mc.parent(self.hip_fk_locator, root_gimbal_ctrl)
            mc.parent(self.world_fk_locator, part.utils_grp)

            # constraining follow Ik
            pac_clavicle_constraint = au.parent_constraint(clav_jnt, self.upper_limb_ik_controller_grp_zro)

            mc.parent(self.shoulder_ik_locator, clav_jnt)
            mc.parent(self.hip_ik_locator, root_gimbal_ctrl)
            mc.parent(self.world_ik_locator, part.utils_grp)

            # rename constraint
            au.constraint_rename(pac_clavicle_constraint)

            # connect fk ik arm controller
            message.connect_message_to_attribute(object_target=self.FkIk_limb_setup_controller,
                                                 fkik_ctrl=self.FkIk_limb_setup_controller,
                                                 object_connector=message.fk_ik_arm_ctrl)
        else:
            self.hip_fk_locator = build_limb.hip_fk
            self.world_fk_locator = build_limb.world_fk

            self.hip_ik_locator = build_limb.hip_ik
            self.world_ik_locator = build_limb.world_ik
            ### FOLLOW ORIENTATION
            # constraining follow Fk
            mc.parent(self.hip_fk_locator, pelvis_gimbal_ctrl)
            mc.parent(self.world_fk_locator, part.utils_grp)

            # constraining follow Ik
            pac_pelvis_constraint = au.parent_constraint(pelvis_gimbal_ctrl, self.upper_limb_ik_controller_grp_zro)

            mc.parent(self.hip_ik_locator, pelvis_gimbal_ctrl)
            mc.parent(self.world_ik_locator, part.utils_grp)

            # parent scale joint to joint driver
            mc.parent(lower_limb_scale_jnt, lower_limb_jnt)
            # connect scale
            self.foot_scale(self.FkIk_limb_setup_controller, lower_limb_scale_jnt)

            # connect attribute translate and rotate
            mc.connectAttr(end_limb_jnt + '.translate', end_limb_scale_jnt + '.translate')
            mc.connectAttr(end_limb_jnt + '.rotate', end_limb_scale_jnt + '.rotate')

            # set to world
            mc.setAttr(self.lower_limb_ik_control + '.follow', 1)

            # rename constraint
            au.constraint_rename(pac_pelvis_constraint)

            # connect fk ik arm controller
            message.connect_message_to_attribute(object_target=self.FkIk_limb_setup_controller,
                                                 fkik_ctrl=self.FkIk_limb_setup_controller,
                                                 object_connector=message.fk_ik_leg_ctrl)

        # connect middle ref joint
        message.connect_message_to_attribute(object_target=message.middle_ref_joint,
                                             fkik_ctrl=self.FkIk_limb_setup_controller,
                                             object_connector=message.middle_ref_message_jnt)
        # connect lower ref joint
        message.connect_message_to_attribute(object_target=message.lower_ref_joint,
                                             fkik_ctrl=self.FkIk_limb_setup_controller,
                                             object_connector=message.lower_ref_message_jnt)

        # connect upper limb snap jnt
        message.connect_message_to_attribute(object_target=upper_limb_jnt,
                                             fkik_ctrl=self.FkIk_limb_setup_controller,
                                             object_connector=message.upper_limb_jnt)

        # connect middle limb joint
        message.connect_message_to_attribute(object_target=middle_limb_jnt,
                                             fkik_ctrl=self.FkIk_limb_setup_controller,
                                             object_connector=message.middle_limb_jnt)
        # connect lower limb joint
        message.connect_message_to_attribute(object_target=lower_limb_jnt,
                                             fkik_ctrl=self.FkIk_limb_setup_controller,
                                             object_connector=message.lower_limb_jnt)

        # connect upper limb fk ctrl
        message.connect_message_to_attribute(object_target=self.upper_limb_fk_control,
                                             fkik_ctrl=self.FkIk_limb_setup_controller,
                                             object_connector=message.upper_limb_fk_ctrl)
        # connect middle limb fk ctrl
        message.connect_message_to_attribute(object_target=self.middle_limb_fk_control,
                                             fkik_ctrl=self.FkIk_limb_setup_controller,
                                             object_connector=message.middle_limb_fk_ctrl)
        # connect lower limb fk ctrl
        message.connect_message_to_attribute(object_target=self.lower_limb_fk_control,
                                             fkik_ctrl=self.FkIk_limb_setup_controller,
                                             object_connector=message.lower_limb_fk_ctrl)
        # connect upper limb ik ctrl
        message.connect_message_to_attribute(object_target=self.upper_limb_ik_control,
                                             fkik_ctrl=self.FkIk_limb_setup_controller,
                                             object_connector=message.upper_limb_ik_ctrl)
        # connect pole vector ctrl
        message.connect_message_to_attribute(object_target=self.poleVector_ik_control,
                                             fkik_ctrl=self.FkIk_limb_setup_controller,
                                             object_connector=message.poleVector_ctrl)
        # connect lower limb ik ctrl
        message.connect_message_to_attribute(object_target=self.lower_limb_ik_control,
                                             fkik_ctrl=self.FkIk_limb_setup_controller,
                                             object_connector=message.lower_limb_ik_ctrl)

        # control combine detail
        self.ctrl_combine_detail = build_limb.ctrl_mid_middle_limb.control

        # control group in part
        self.part_control_grp = part.control_grp

        # parent setup to part group
        # controller
        mc.parent(self.FkIk_limb_setup_controller_grp_zro, part.control_grp)
        mc.parent(build_limb.ctrl_mid_middle_limb.parent_control[0], part.control_grp)

        # joint
        self.part_joint_grp = part.joint_grp
        mc.parent(build_limb.pos_upper_limb_jnt, part.joint_grp)
        mc.parent(build_limb.position_softIk_jnt, part.joint_grp)

        # non-trans
        mc.parent(build_limb.curve_poleVector_ik, part.non_transform_grp)

        ### FK SETUP
        # parent lower to middle limb control group
        mc.parent(self.lower_limb_fk_controller_grp_zro, self.middle_limb_fk_gimbal)

        # parent middle limb to upper limb control group
        mc.parent(self.middle_limb_fk_controller_grp_zro, self.upper_limb_fk_gimbal)

        # parent all limb to part control group
        mc.parent(self.upper_limb_fk_controller_grp_zro, part.control_grp)

        # connect scale module to decompose matrix
        mc.connectAttr(base_controller.anim_control + '.worldMatrix[0]', build_limb.scale_decompose + '.inputMatrix')

        # stretch FK middle limb
        mc.connectAttr(build_limb.upper_stretch_limb_fk + '.output',
                       self.middle_limb_fk_controller_grp_zro + '.translateY')

        # stretch FK wrist
        mc.connectAttr(build_limb.middle_stretch_limb_fk + '.output',
                       self.lower_limb_fk_controller_grp_zro + '.translateY')

        ### IK SETUP
        # parent joint IK driver to joint grp
        mc.parent(upper_limb_ik_jnt, part.joint_grp)

        # parent upper limb to part control group
        mc.parent(self.upper_limb_ik_controller_grp_zro, part.control_grp)

        # parent elbow to part control group
        mc.parent(self.poleVector_ik_controller_grp_zro, part.control_grp)

        # parent wrist to part control group
        mc.parent(self.lower_limb_ik_controller_grp_zro, part.control_grp)

        # point constraint the stretching the limb
        pt_upper_limb_ik_constraint = mc.pointConstraint(self.upper_limb_ik_gimbal, build_limb.pos_upper_limb_jnt, mo=1)

        # aim constraining for stretching the limb
        aim_lower_limb_ik_constraint = mc.aimConstraint(self.lower_limb_ik_gimbal, build_limb.pos_upper_limb_jnt, mo=1,
                                                        aim=(0.0, 1.0, 0.0),
                                                        u=(-1.0, 0.0, 0.0), wut='objectrotation', wu=(0.0, 1.0, 0.0),
                                                        wuo=part.joint_grp)

        # ELBOW FOLLOWING LIMB
        elbow_follow_constraint = \
            mc.parentConstraint(self.lower_limb_ik_control, world, self.poleVector_ik_controller_grp_zro, mo=1)[0]
        mc.connectAttr(build_limb.controller_pole_vector_ik.control + '.follow',
                       elbow_follow_constraint + '.%sW0' % self.lower_limb_ik_control)

        elbow_cons_reverse = mc.shadingNode('reverse', asUtility=1,
                                            n='%s%s%s_rev' % (prefix_pole_vector_ik, 'Follow', side))
        mc.connectAttr(build_limb.controller_pole_vector_ik.control + '.follow', elbow_cons_reverse + '.inputX')
        mc.connectAttr(elbow_cons_reverse + '.outputX', elbow_follow_constraint + '.%sW1' % world)

        # set ikRPsolver
        mc.setAttr("ikRPsolver.tolerance", 1e-09)

        # constraining the controller Fk/Ik
        pac_lower_limb_constraint = mc.parentConstraint(lower_limb_jnt, self.FkIk_limb_setup_controller_grp_zro, mo=1)

        ## IMPORT DETAIL LIMB MODULE
        self.pos_lower_limb_jnt = build_limb.pos_lower_limb_jnt
        self.pos_soft_jnt = build_limb.position_softIk_jnt

        # ==============================================================================================================
        #                                             LIMB DETAIL
        # ==============================================================================================================
        # divided value in every index
        num = (1.0 / (number_detail_ctrl + 1))

        # ==============================================================================================================
        #                                               UPPER LIMB DETAIL
        # ==============================================================================================================
        detail_upper_limb = dl.CreateDetail(
            limb_bind_joint_parent=limb_bind_joint_parent_upper,
            detail_limb_deformer=detail_limb_deformer,
            base=upper_limb_jnt,
            tip=middle_limb_jnt,
            parallel_axis=parallel_axis,
            tip_pos=tip_pos,
            ctrl_tip=ct.SQUARE,
            ctrl_mid=ct.SQUARE,
            ctrl_base=ct.SQUARE,
            ctrl_details=ct.CIRCLEPLUS,
            ctrl_color='lightPink',
            prefix=prefix_upper_limb_detail,
            side=side,
            scale=size,
            volume_pos_min=2,
            volume_pos_max=0,
            number_joints=number_detail_ctrl,
            game_bind_joint=game_bind_joint)

        # set grp and ctrl follicle upper limb
        self.set_grp_follicle_upper_limb = detail_upper_limb.follicle_set_grp
        self.set_grp_follicle_twist_upper_limb = detail_upper_limb.follicle_grp_twist
        self.set_grp_follicle_offset_upper_limb = detail_upper_limb.follicle_grp_offset
        self.ctrl_follicle_upper_limb = detail_upper_limb.follicle_ctrl
        self.follicle_joint_upper_limb = detail_upper_limb.follicle_joint_limb

        # parent main grp to still grp
        mc.parent(detail_upper_limb.grp_no_transform_zro, part.non_transform_grp)
        mc.parent(detail_upper_limb.grp_transform_zro, part.control_grp)

        # scale connect
        mc.connectAttr(base_controller.scale_matrix_node + '.outputScale', detail_upper_limb.grp_transform + '.scale')

        # parent contraint detail jnt driver to grp offset middle limb
        pac_mid_dtl_upper_limb_constraint = mc.parentConstraint(middle_limb_jnt,
                                                                detail_upper_limb.ctrl_down.parent_control[1],
                                                                mo=1)

        if arm:
            # parent constraint detail bind to grp transform detail
            pac_detail_limb_constraint = mc.parentConstraint(clav_jnt, detail_upper_limb.grp_transform, mo=1)
            au.constraint_rename(pac_detail_limb_constraint)
        else:
            pac_detail_limb_constraint = mc.parentConstraint(pelvis_gimbal_ctrl, detail_upper_limb.grp_transform, mo=1)
            au.constraint_rename(pac_detail_limb_constraint)

        ### TWIST UPPER LIMB SETUP
        # create multi matrix
        mult_matrix_ctrl_up = mc.shadingNode('multMatrix', asUtility=1,
                                             n='%s%s%s_mmtx' % (prefix_upper_limb_detail, 'CtrlUp', side))
        mult_matrix_ctrl_down = mc.shadingNode('multMatrix', asUtility=1,
                                               n='%s%s%s_mmtx' % (prefix_upper_limb_detail, 'CtrlDown', side))

        mc.connectAttr(detail_upper_limb.ctrl_up.parent_control[2] + '.worldMatrix[0]',
                       mult_matrix_ctrl_up + '.matrixIn[0]')
        mc.connectAttr(detail_upper_limb.ctrl_down.parent_control[0] + '.worldInverseMatrix[0]',
                       mult_matrix_ctrl_up + '.matrixIn[1]')

        mc.connectAttr(detail_upper_limb.ctrl_down.parent_control[2] + '.worldMatrix[0]',
                       mult_matrix_ctrl_down + '.matrixIn[0]')
        mc.connectAttr(detail_upper_limb.ctrl_up.parent_control[0] + '.worldInverseMatrix[0]',
                       mult_matrix_ctrl_down + '.matrixIn[1]')

        # create decompose matrix
        decompose_matrix_ctrl_up = mc.shadingNode('decomposeMatrix', asUtility=1,
                                                  n='%s%s%s_dmtx' % (prefix_upper_limb_detail, 'CtrlUp', side))
        decompose_matrix_ctrl_down = mc.shadingNode('decomposeMatrix', asUtility=1,
                                                    n='%s%s%s_dmtx' % (prefix_upper_limb_detail, 'CtrlDown', side))

        mc.connectAttr(mult_matrix_ctrl_up + '.matrixSum', decompose_matrix_ctrl_up + '.inputMatrix')
        mc.connectAttr(mult_matrix_ctrl_down + '.matrixSum', decompose_matrix_ctrl_down + '.inputMatrix')

        # create quat to euler
        quat_ctrl_up = mc.shadingNode('quatToEuler', asUtility=1,
                                      n='%s%s%s_qte' % (prefix_upper_limb_detail, 'CtrlUp', side))
        quat_ctrl_down = mc.shadingNode('quatToEuler', asUtility=1,
                                        n='%s%s%s_qte' % (prefix_upper_limb_detail, 'CtrlDown', side))

        # set rotation order to zxy
        mc.setAttr(quat_ctrl_up + '.inputRotateOrder', 2)
        mc.setAttr(quat_ctrl_down + '.inputRotateOrder', 2)

        mc.connectAttr(decompose_matrix_ctrl_up + '.outputQuatY', quat_ctrl_up + '.inputQuatY')
        mc.connectAttr(decompose_matrix_ctrl_up + '.outputQuatW', quat_ctrl_up + '.inputQuatW')

        mc.connectAttr(decompose_matrix_ctrl_down + '.outputQuatY', quat_ctrl_down + '.inputQuatY')
        mc.connectAttr(decompose_matrix_ctrl_down + '.outputQuatW', quat_ctrl_down + '.inputQuatW')

        # REVERSING TWIST WHEN THE LIMB AS A POSE
        for twist, offset in zip(self.set_grp_follicle_twist_upper_limb, self.set_grp_follicle_offset_upper_limb):
            reverseTwistNode = mc.createNode('multDoubleLinear', n='%s_mdl' % (au.prefix_name(twist)))
            mc.connectAttr(twist + '.rotateY', reverseTwistNode + '.input1')
            mc.connectAttr(self.FkIk_limb_setup_controller + '.%s%s' % (prefix, 'MultTwist'),
                           reverseTwistNode + '.input2')
            mc.connectAttr(reverseTwistNode + '.output', offset + '.rotateY')

        ctrl_up_mdl_node = []
        ctrl_down_mdl_node = []
        sum_up_down_matrix_node = []

        for i in range(len(self.set_grp_follicle_twist_upper_limb)):
            value = num * i
            # ctrl up mult double linear
            ctrl_up_mdl = mc.shadingNode('multDoubleLinear', asUtility=1,
                                         n='%s%s%s%s_mdl' % (
                                             prefix_upper_limb_detail, str(i + 1).zfill(2), 'MultCtrlUp', side))

            mc.setAttr(ctrl_up_mdl + '.input2', value)
            ctrl_up_mdl_node.append(ctrl_up_mdl)

            # ctrl down mult double linear
            ctrl_down_mdl = mc.shadingNode('multDoubleLinear', asUtility=1,
                                           n='%s%s%s%s_mdl' % (
                                               prefix_upper_limb_detail, str(i + 1).zfill(2), 'MultCtrlDown', side))
            mc.setAttr(ctrl_down_mdl + '.input2', value)
            ctrl_down_mdl_node.append(ctrl_down_mdl)

            # connect quatCtrlDown and quatCtrlUp to respective multiply node
            mc.connectAttr(quat_ctrl_up + '.outputRotateY', ctrl_up_mdl + '.input1')
            mc.connectAttr(quat_ctrl_down + '.outputRotateY', ctrl_down_mdl + '.input1')

            # create matrix node for twist upper limb
            sum_up_down_matrix = mc.shadingNode('plusMinusAverage', asUtility=1,
                                                n='%s%s%s%s_pma' % (
                                                    prefix_upper_limb_detail, str(i + 1).zfill(2), 'SumUpDown', side))
            sum_up_down_matrix_node.append(sum_up_down_matrix)

        for up, down, pma, twist in zip(ctrl_up_mdl_node[::-1], ctrl_down_mdl_node, sum_up_down_matrix_node,
                                        self.set_grp_follicle_twist_upper_limb):
            mc.connectAttr(up + '.output', pma + '.input1D[0]')
            mc.connectAttr(down + '.output', pma + '.input1D[1]')
            mc.connectAttr(pma + '.output1D', twist + '.rotateY')

        # ==============================================================================================================
        #                                        TWIST ROTATE UPPER LIMB
        # ==============================================================================================================
        # parent joint to joint grp
        mc.parent(upper_limb_twist_help_driver_jnt, part.joint_grp)

        upper_limb_twist_help_joint = mc.xform(upper_limb_twist_help_driver_jnt, q=1, ws=True, t=1)
        middle_limb_twist_help_joint = mc.xform(middle_limb_twist_help_driver_jnt, q=1, ws=True, t=1)

        # create curve for ik spline
        curve_ik_spline_detail = mc.curve(d=1, p=[upper_limb_twist_help_joint, middle_limb_twist_help_joint])
        self.limb_detail_hdl = mc.ikHandle(sj=upper_limb_twist_help_driver_jnt, ee=middle_limb_twist_help_driver_jnt,
                                           sol='ikSplineSolver',
                                           n='%s%s_hdl' % (prefix_upper_limb + 'TwistHelp', side), ccv=False,
                                           c=curve_ik_spline_detail, ns=1, rootOnCurve=True)
        detail_hdl_curve = mc.rename(curve_ik_spline_detail, '%s%s_crv' % (prefix_upper_limb + 'TwistHelp', side))

        # skin the spline curve
        mc.skinCluster(upper_limb_jnt, middle_limb_jnt, detail_hdl_curve, tsb=True, mi=1)

        # parent to part grp
        grp_curve_ikh = mc.group(empty=True, n=prefix_upper_limb + 'TwistHelp' + side + '_grp')
        mc.parent(self.limb_detail_hdl[0], upper_limb_twist_help_driver_jnt, grp_curve_ikh)
        mc.parent(grp_curve_ikh, detail_upper_limb.grp_transform)
        mc.parent(detail_hdl_curve, part.non_transform_grp)

        # constraint twist help joint to zro controller up limb grp
        pac_detail_upper_limb_constraint = mc.parentConstraint(upper_limb_twist_help_driver_jnt,
                                                               detail_upper_limb.ctrl_up.parent_control[0])

        # hide the curve spline Ik
        mc.hide(detail_hdl_curve, self.limb_detail_hdl[0], upper_limb_twist_help_driver_jnt,
                middle_limb_twist_help_driver_jnt)

        # ==============================================================================================================
        #                                               MIDDLE LIMB DETAIL
        # ==============================================================================================================
        detail_lower_limb = dl.CreateDetail(
            limb_bind_joint_parent=limb_bind_joint_parent_lower,
            detail_limb_deformer=detail_limb_deformer,
            base=middle_limb_jnt,
            tip=lower_limb_jnt,
            parallel_axis=parallel_axis,
            tip_pos=tip_pos,
            ctrl_tip=ct.SQUARE,
            ctrl_mid=ct.SQUARE,
            ctrl_base=ct.SQUARE,
            ctrl_details=ct.CIRCLEPLUS,
            ctrl_color='turquoiseBlue',
            prefix=prefix_middle_limb_detail,
            side=side,
            scale=size,
            volume_pos_min=0,
            volume_pos_max=2,
            number_joints=number_detail_ctrl,
            game_bind_joint=game_bind_joint)

        # set grp and ctrl follicle middle limb
        self.set_grp_follicle_middle_limb = detail_lower_limb.follicle_set_grp
        self.set_grp_follicle_twist_middle_limb = detail_lower_limb.follicle_grp_twist
        self.ctrl_follicle_middle_limb = detail_lower_limb.follicle_ctrl
        self.follicle_joint_lower_limb = detail_lower_limb.follicle_joint_limb

        # parent main grp to still grp
        mc.parent(detail_lower_limb.grp_no_transform_zro, part.non_transform_grp)
        mc.parent(detail_lower_limb.grp_transform_zro, part.control_grp)

        # scale connect
        mc.connectAttr(base_controller.scale_matrix_node + '.outputScale', detail_lower_limb.grp_transform + '.scale')

        # constraining middle limb bind dtl to middle limb grp transform
        pac_mid_limb_constraint = mc.parentConstraint(middle_limb_jnt, detail_lower_limb.grp_transform, mo=1)

        # constraining wrist to middle limb down ctrl detail
        pac_low_limb_constraint = mc.parentConstraint(lower_limb_jnt, detail_lower_limb.ctrl_down.parent_control[1])

        ### TWIST MIDDLE LIMB SETUP
        # create multi matrix
        multi_matrix_ctrl_lower_limb = mc.shadingNode('multMatrix', asUtility=1,
                                                      n='%s%s%s_mmtx' % (prefix_middle_limb_detail, 'CtrlDown', side))

        mc.connectAttr(detail_lower_limb.ctrl_down.parent_control[2] + '.worldMatrix[0]',
                       multi_matrix_ctrl_lower_limb + '.matrixIn[0]')
        mc.connectAttr(detail_lower_limb.ctrl_up.parent_control[0] + '.worldInverseMatrix[0]',
                       multi_matrix_ctrl_lower_limb + '.matrixIn[1]')

        # create decompose matrix
        decompose_matrix_ctrl_lower_limb = mc.shadingNode('decomposeMatrix', asUtility=1,
                                                          n='%s%s%s_dmtx' % (
                                                              prefix_middle_limb_detail, 'CtrlDown', side))
        mc.connectAttr(multi_matrix_ctrl_lower_limb + '.matrixSum', decompose_matrix_ctrl_lower_limb + '.inputMatrix')

        # create quat to euler
        quat_ctrl_lower_limb = mc.shadingNode('quatToEuler', asUtility=1,
                                              n='%s%s%s_qte' % (prefix_middle_limb_detail, 'CtrlDown', side))

        # set rotation order to zxy
        mc.setAttr(quat_ctrl_lower_limb + '.inputRotateOrder', 2)

        mc.connectAttr(decompose_matrix_ctrl_lower_limb + '.outputQuatY', quat_ctrl_lower_limb + '.inputQuatY')
        mc.connectAttr(decompose_matrix_ctrl_lower_limb + '.outputQuatW', quat_ctrl_lower_limb + '.inputQuatW')

        ctrl_lower_bind_mdl_node = []
        for i in range(len(self.set_grp_follicle_twist_middle_limb)):
            value = num * i
            # ctrl down mult double linear
            ctrl_lower_limb_mdl = mc.shadingNode('multDoubleLinear', asUtility=1,
                                                 n='%s%s%s%s_mdl' % (
                                                     prefix_middle_limb_detail, str(i + 1).zfill(2), 'MultCtrlDown',
                                                     side))
            mc.setAttr(ctrl_lower_limb_mdl + '.input2', value)
            ctrl_lower_bind_mdl_node.append(ctrl_lower_limb_mdl)

            # connect quatCtrlDown  to respective multiply node
            mc.connectAttr(quat_ctrl_lower_limb + '.outputRotateY', ctrl_lower_limb_mdl + '.input1')

        for down, twist in zip(ctrl_lower_bind_mdl_node, self.set_grp_follicle_twist_middle_limb):
            mc.connectAttr(down + '.output', twist + '.rotateY')

        # ==============================================================================================================
        #                                               SCALE LIMB
        # ==============================================================================================================
        # upper limb
        self.limb_part_scale(prefix=prefix, controller=self.FkIk_limb_setup_controller,
                             group_scale=self.set_grp_follicle_twist_upper_limb)

        # middle limb
        self.limb_part_scale(prefix=prefix, controller=self.FkIk_limb_setup_controller,
                             group_scale=self.set_grp_follicle_twist_middle_limb)

        # ==============================================================================================================
        #                                               COMBINED DETAIL
        # ==============================================================================================================
        # parent constraint from middle limb bind to limb detail combine
        pac_ctrl_mid_limb_constraint = mc.parentConstraint(middle_limb_jnt,
                                                           build_limb.ctrl_mid_middle_limb.parent_control[0])

        # point ccnstraint to respective module upper limb detail and middle limb detail combine
        pt_ctrl_down_constraint = mc.pointConstraint(self.ctrl_combine_detail,
                                                     detail_upper_limb.ctrl_down.parent_control[2])
        pt_ctrl_up_constraint = mc.pointConstraint(self.ctrl_combine_detail,
                                                   detail_lower_limb.ctrl_up.parent_control[2])
        au.constraint_rename(pac_ctrl_mid_limb_constraint)
        au.constraint_rename(pt_ctrl_down_constraint)
        au.constraint_rename(pt_ctrl_up_constraint)

        ### CONNECT ROLL
        # disconnect from detail roll to plus minus average
        mc.disconnectAttr(detail_upper_limb.ctrl_down.parent_control[2] + '.twist',
                          detail_upper_limb.sum_top_pma + '.input1D[0]')
        mc.disconnectAttr(detail_lower_limb.ctrl_up.parent_control[2] + '.twist',
                          detail_lower_limb.sum_end_pma + '.input1D[0]')

        # connect attribute from respective control module to add double linear control
        mc.connectAttr(detail_upper_limb.ctrl_down.parent_control[2] + '.twist',
                       build_limb.adl_upper_limb_combine + '.input1')
        mc.connectAttr(detail_lower_limb.ctrl_up.parent_control[2] + '.twist',
                       build_limb.adl_middle_limb_combine + '.input1')

        # connect output of adl combine node to plus minus average upper limb and middle limb roll node
        mc.connectAttr(build_limb.adl_upper_limb_combine + '.output', detail_upper_limb.sum_top_pma + '.input1D[0]')
        mc.connectAttr(build_limb.adl_middle_limb_combine + '.output', detail_lower_limb.sum_end_pma + '.input1D[0]')

        if detail_limb_deformer:
            ### CONNECT VOLUME POSITION
            # volume position combined
            if tip_pos == '-':
                # v upper limb LFT
                self.combine_volume_detail(detail_upper_limb.combine_vol_position_adl, self.ctrl_combine_detail,
                                           number_detail_ctrl,
                                           min_mult=1, mid_mult=-1, max_mult=-1)
                # detail middle limb LFT
                self.combine_volume_detail(detail_lower_limb.combine_vol_position_adl, self.ctrl_combine_detail,
                                           number_detail_ctrl,
                                           min_mult=1, mid_mult=1, max_mult=-1)

            if tip_pos == '+':
                # v upper limb LFT
                self.combine_volume_detail(detail_upper_limb.combine_vol_position_adl, self.ctrl_combine_detail,
                                           number_detail_ctrl,
                                           min_mult=-1, mid_mult=1, max_mult=1)
                # detail middle limb LFT
                self.combine_volume_detail(detail_lower_limb.combine_vol_position_adl, self.ctrl_combine_detail,
                                           number_detail_ctrl,
                                           min_mult=-1, mid_mult=-1, max_mult=1)

            #### CONNECT VOLUME
            # connect to multdouble linear volume detail to volume add double linear detail
            # upper limb
            mc.connectAttr(build_limb.volume_pos_mdl_upper_limb + '.output',
                           detail_upper_limb.volume_reverse_adl + '.input1')

            # middle limb
            mc.connectAttr(build_limb.volume_pos_mdl_middle_limb + '.output',
                           detail_lower_limb.volume_reverse_adl + '.input1')

            ### CONNECT MULTIPLIER VOLUME
            for ua, fa in zip(detail_upper_limb.combine_mult_all, detail_lower_limb.combine_mult_all):
                mc.connectAttr(self.ctrl_combine_detail + '.volumeMultiplier', ua + '.input2')
                mc.connectAttr(self.ctrl_combine_detail + '.volumeMultiplier', fa + '.input2')

            ### CONNECT SINE SETUP
            mc.connectAttr(self.ctrl_combine_detail + '.amplitude',
                           detail_upper_limb.combine_sine_amplitude + '.input1')
            mc.connectAttr(self.ctrl_combine_detail + '.amplitude',
                           detail_lower_limb.combine_sine_amplitude + '.input1')
            mc.connectAttr(self.ctrl_combine_detail + '.wide', detail_upper_limb.combine_sine_wide + '.input1')
            mc.connectAttr(self.ctrl_combine_detail + '.wide', detail_lower_limb.combine_sine_wide + '.input1')
            mc.connectAttr(self.ctrl_combine_detail + '.sineRotate', detail_upper_limb.combine_sine_rotate + '.input1')
            mc.connectAttr(self.ctrl_combine_detail + '.sineRotate', detail_lower_limb.combine_sine_rotate + '.input1')
            mc.connectAttr(self.ctrl_combine_detail + '.offset', detail_upper_limb.combine_sine_offset + '.input1')
            mc.connectAttr(self.ctrl_combine_detail + '.offset', detail_lower_limb.combine_sine_offset + '.input1')
            mc.connectAttr(self.ctrl_combine_detail + '.twist', detail_upper_limb.combine_sine_twist + '.input1')
            mc.connectAttr(self.ctrl_combine_detail + '.twist', detail_lower_limb.combine_sine_twist + '.input1')
            mc.connectAttr(self.ctrl_combine_detail + '.sineLength', detail_upper_limb.combine_sine_length + '.input1')
            mc.connectAttr(self.ctrl_combine_detail + '.sineLength', detail_lower_limb.combine_sine_length + '.input1')

            # constraint upper limb Dtl Jnt to grp surface
            pac_twist_help_constraint = mc.parentConstraint(upper_limb_twist_help_driver_jnt,
                                                            detail_upper_limb.grp_surface,
                                                            mo=1)
            au.constraint_rename(pac_twist_help_constraint)

        # connect the visibility-switch for the controller
        # switch on/off detail module ctrl
        mc.connectAttr(self.ctrl_combine_detail + '.detailBaseCtrlVis',
                       detail_upper_limb.ctrl_up.parent_control[0] + '.visibility')
        mc.connectAttr(self.ctrl_combine_detail + '.detailBaseCtrlVis',
                       detail_upper_limb.ctrl_down.parent_control[0] + '.visibility')
        mc.connectAttr(self.ctrl_combine_detail + '.detailBaseCtrlVis',
                       detail_lower_limb.ctrl_up.parent_control[0] + '.visibility')
        mc.connectAttr(self.ctrl_combine_detail + '.detailBaseCtrlVis',
                       detail_lower_limb.ctrl_down.parent_control[0] + '.visibility')

        # rename constraint
        au.constraint_rename([pt_upper_limb_ik_constraint[0], aim_lower_limb_ik_constraint[0], elbow_follow_constraint,
                              pac_lower_limb_constraint[0],
                              pac_mid_limb_constraint[0], pac_low_limb_constraint[0],
                              pac_mid_dtl_upper_limb_constraint[0],
                              pac_detail_upper_limb_constraint[0]])

    # ==================================================================================================================
    #                                               FUNCTION LIMB MODULE
    # ==================================================================================================================
    def single_module_arm(self, base_controller, upper_limb_jnt, middle_limb_jnt, lower_limb_jnt, upper_limb_fk_jnt,
                          middle_limb_fk_jnt, lower_limb_fk_jnt, upper_limb_ik_jnt, middle_limb_ik_jnt,
                          lower_limb_ik_jnt,
                          end_limb_ik_jnt, upper_limb_twist_help_driver_jnt, middle_limb_twist_help_driver_jnt,
                          detail_limb_deformer, number_detail_ctrl, clav_jnt, parallel_axis, tip_pos,
                          side, size, side_RGT, side_LFT
                          ):

        self.module(arm=True, prefix='arm', base_controller=base_controller, prefix_upper_limb='upperArm',
                    prefix_upper_limb_fk='upperArmFk', prefix_middle_limb_fk='forearmFk',
                    prefix_lower_limb_fk='wristFk', prefix_upper_limb_ik='upperArmIk',
                    prefix_pole_vector_ik='elbowIk', prefix_middle_limb_ik='forearmIk',
                    prefix_lower_limb_ik='wristIk', prefix_end_limb_ik='handIk',
                    prefix_limb_setup='armSetup', side=side, upper_limb_jnt=upper_limb_jnt,
                    middle_limb_jnt=middle_limb_jnt, lower_limb_jnt=lower_limb_jnt, end_limb_jnt=None,
                    lower_limb_scale_jnt=None, end_limb_scale_jnt=None, upper_limb_fk_jnt=upper_limb_fk_jnt,
                    middle_limb_fk_jnt=middle_limb_fk_jnt, lower_limb_fk_jnt=lower_limb_fk_jnt,
                    upper_limb_ik_jnt=upper_limb_ik_jnt, middle_limb_ik_jnt=middle_limb_ik_jnt,
                    lower_limb_ik_jnt=lower_limb_ik_jnt, end_limb_ik_jnt=end_limb_ik_jnt,
                    upper_limb_twist_help_driver_jnt=upper_limb_twist_help_driver_jnt,
                    middle_limb_twist_help_driver_jnt=middle_limb_twist_help_driver_jnt,
                    world=base_controller.body_part_grp, detail_limb_deformer=detail_limb_deformer,
                    number_detail_ctrl=number_detail_ctrl - 2, clav_jnt=clav_jnt, pelvis_gimbal_ctrl=None,
                    root_gimbal_ctrl=None, parallel_axis=parallel_axis, tip_pos=tip_pos,
                    prefix_upper_limb_detail='upperArmDtl', prefix_middle_limb_detail='forearmDtl', size=size,
                    side_LFT=side_LFT, side_RGT=side_RGT)

        self.run_soft_ik_arm = rs.run_soft_ik_joint(prefix='arm', side=side,
                                                    lower_limb_ik_gimbal=self.lower_limb_ik_gimbal,
                                                    foot_reverse_joint_or_position_soft_jnt=self.pos_soft_jnt,
                                                    position_lower_limb_jnt=self.pos_lower_limb_jnt,
                                                    lowerLimbIkControl=self.lower_limb_ik_control)

        mc.parent(upper_limb_jnt, self.part.joint_grp)
        mc.parent(self.shoulder_ik_locator, self.shoulder_fk_locator, self.hip_fk_locator, self.hip_ik_locator,
                  self.part.utils_grp)

    def single_module_leg(self, base_controller, upper_limb_jnt, middle_limb_jnt, lower_limb_jnt, end_limb_jnt,
                          lower_limb_scale_jnt,
                          upper_limb_fk_jnt, end_limb_scale_jnt, middle_limb_fk_jnt, lower_limb_fk_jnt,
                          upper_limb_ik_jnt, middle_limb_ik_jnt,
                          lower_limb_ik_jnt, end_limb_ik_jnt, upper_limb_twist_help_driver_jnt,
                          middle_limb_twist_help_driver_jnt,
                          detail_limb_deformer, number_detail_ctrl, parallel_axis, tip_pos,
                          side, size, side_LFT, side_RGT
                          ):

        self.module(arm=False, prefix='leg', side=side, base_controller=base_controller,
                    prefix_upper_limb='upperLeg', prefix_upper_limb_fk='upperLegFk', prefix_middle_limb_fk='lowerLegFk',
                    prefix_lower_limb_fk='ankleFk', prefix_upper_limb_ik='upperLegIk', prefix_pole_vector_ik='kneeIk',
                    prefix_middle_limb_ik='lowerLeg', prefix_lower_limb_ik='ankleIk', prefix_end_limb_ik='ballIk',
                    prefix_limb_setup='legSetup', upper_limb_jnt=upper_limb_jnt, middle_limb_jnt=middle_limb_jnt,
                    lower_limb_jnt=lower_limb_jnt, end_limb_jnt=end_limb_jnt, lower_limb_scale_jnt=lower_limb_scale_jnt,
                    end_limb_scale_jnt=end_limb_scale_jnt, upper_limb_fk_jnt=upper_limb_fk_jnt,
                    middle_limb_fk_jnt=middle_limb_fk_jnt,
                    lower_limb_fk_jnt=lower_limb_fk_jnt, upper_limb_ik_jnt=upper_limb_ik_jnt,
                    middle_limb_ik_jnt=middle_limb_ik_jnt,
                    lower_limb_ik_jnt=lower_limb_ik_jnt, end_limb_ik_jnt=end_limb_ik_jnt,
                    upper_limb_twist_help_driver_jnt=upper_limb_twist_help_driver_jnt,
                    middle_limb_twist_help_driver_jnt=middle_limb_twist_help_driver_jnt,
                    world=base_controller.body_part_grp,
                    detail_limb_deformer=detail_limb_deformer, number_detail_ctrl=number_detail_ctrl - 2, clav_jnt=None,
                    pelvis_gimbal_ctrl=self.sj.pelvis, root_gimbal_ctrl=None, parallel_axis=parallel_axis,
                    tip_pos=tip_pos,
                    prefix_upper_limb_detail='upperLegDtl',
                    prefix_middle_limb_detail='lowerLegDtl', size=size,
                    side_LFT=side_LFT, side_RGT=side_RGT)

        run_soft_ik_leg = rs.run_soft_ik_joint(prefix='leg', side=side, lower_limb_ik_gimbal=self.lower_limb_ik_gimbal,
                                               foot_reverse_joint_or_position_soft_jnt=self.pos_soft_jnt,
                                               position_lower_limb_jnt=self.pos_lower_limb_jnt,
                                               lowerLimbIkControl=self.lower_limb_ik_control)

        mc.parent(upper_limb_jnt, self.part.joint_grp)

        return run_soft_ik_leg

    def combine_volume_detail(self, combine_vol_position_adl, controller, number_detail_ctrl, min_mult=1, mid_mult=1,
                              max_mult=1):
        # min
        mc.setDrivenKeyframe(combine_vol_position_adl + '.input1',
                             cd=controller + '.volumePosition',
                             dv=number_detail_ctrl * -0.5, v=number_detail_ctrl * 0.5 * min_mult, itt='linear',
                             ott='linear')
        # mid
        mc.setDrivenKeyframe(combine_vol_position_adl + '.input1',
                             cd=controller + '.volumePosition',
                             dv=0, v=number_detail_ctrl * 0.5 * mid_mult, itt='linear', ott='linear')
        # max
        mc.setDrivenKeyframe(combine_vol_position_adl + '.input1',
                             cd=controller + '.volumePosition',
                             dv=number_detail_ctrl * 0.5, v=number_detail_ctrl * 0.5 * max_mult, itt='linear',
                             ott='linear')

    def limb_part_scale(self, prefix, controller, group_scale):
        # LIMB SCALE
        for i in group_scale:
            mc.connectAttr(controller + '.%s%s' % (prefix, 'ScaleX'), i + '.scaleX')
            mc.connectAttr(controller + '.%s%s' % (prefix, 'ScaleY'), i + '.scaleY')
            mc.connectAttr(controller + '.%s%s' % (prefix, 'ScaleZ'), i + '.scaleZ')

    def foot_scale(self, controller, ankle_jnt):
        mc.connectAttr(controller + '.footScaleX', ankle_jnt + '.scaleX')
        mc.connectAttr(controller + '.footScaleY', ankle_jnt + '.scaleY')
        mc.connectAttr(controller + '.footScaleZ', ankle_jnt + '.scaleZ')

    def joint_driver(self, arm):
        if arm:
            skel = ds.all_skeleton(sj_prefix_value='ModArm', ss_prefix_value='ModArmScl',
                                   sFk_prefix_value='ModArmFk', sIk_prefix_value='ModArmIk',
                                   sAdd_prefix_value='ModArmShape')
        else:
            skel = ds.all_skeleton(sj_prefix_value='ModLeg', ss_prefix_value='ModLegScl',
                                   sFk_prefix_value='ModLegFk', sIk_prefix_value='ModLegIk',
                                   sAdd_prefix_value='ModLegShape')
        self.sj = skel['sj']
        self.sFk = skel['sFk']
        self.sIk = skel['sIk']
        self.ss = skel['ss']
        self.sTwistHelp = skel['sTwistHelp']
        self.sAdd = skel['sAdd']
