import maya.cmds as mc

from rigging.library.module import base_module as gm, template_module as sd
from rigging.library.module.body import clavicle_module as cm
from rigging.library.module.body import spine_module as sm, foot_module as fm, hand_module as hm, \
    limb_module as lm
from rigging.library.utils import template_skeleton as ts
from rigging.tools import AD_utils as au

reload(gm)
reload(sm)
reload(cm)
reload(lm)
reload(hm)
reload(fm)
reload(ts)
reload(sd)
reload(au)

def build_rig(clavicle_left, clavicle_right, arm_left, arm_right, prefix_spine, prefix_upperArm, prefix_forearm,
              prefix_clav, prefix_arm, prefix_spine_setup, prefix_wrist,
              prefix_elbow, prefix_hand, prefix_arm_setup, detail_spine_deformer, detail_arm_deformer, number_arm_detail_ctrl,
              leg_left, leg_right, foot_right, foot_left, prefix_upperLeg, prefix_lowerLeg,
              prefix_leg, prefix_ankle, prefix_foot,
              prefix_knee, prefix_ball, prefix_toe, prefix_leg_setup, detail_leg_def, num_leg_dtl_ctrl,
              prefix_thumb, prefix_index, prefix_palm,
              thumb_arm_LFT, index_arm_LFT, middle_arm_LFT, ring_arm_LFT, pinky_arm_LFT, prefix_finger_setup,
              thumb_arm_RGT, index_arm_RGT, middle_arm_RGT, ring_arm_RGT, pinky_arm_RGT, prefix_middle, prefix_ring, prefix_pinky,
              scale, side_LFT, side_RGT, sj_prefix_value, ss_prefix_value, sFk_prefix_value, sIk_prefix_value, sAdd_prefix_value, fk, ik, detail,
              suffix_joint
              ):

    # CREATE BASE RIG
    base = gm.Base(scale=scale)

    # FINGER POSITION
    BaseF = 'Base'
    UpF = 'Up'
    MidF = 'Mid'
    LowF = 'Low'
# ======================================================================================================================
#                                              DUPLICATE JOINTS AS DRIVER
# ======================================================================================================================
    sj = sd.listSkeletonDuplicate(value_prefix=sj_prefix_value,
                                  key_prefix='Ori',
                                  suffix=suffix_joint,
                                  side_LFT=side_LFT,
                                  side_RGT=side_RGT
                                  )

    ss = sd.listSkeletonDuplicate(value_prefix=ss_prefix_value,
                                  key_prefix='Scl',
                                  suffix=suffix_joint,
                                  side_LFT=side_LFT,
                                  side_RGT=side_RGT
                                  )

    sFk = sd.listSkeletonDuplicate(value_prefix=sFk_prefix_value,
                                   key_prefix=fk,
                                   suffix=suffix_joint,
                                   side_LFT=side_LFT,
                                   side_RGT=side_RGT
                                   )

    sIk = sd.listSkeletonDuplicate(value_prefix=sIk_prefix_value,
                                   key_prefix=ik,
                                   suffix=suffix_joint,
                                   side_LFT=side_LFT,
                                   side_RGT=side_RGT
                                   )
    sTwistHelp = sd.listSkeletonDuplicate(value_prefix='TwistHelpDriver',
                                          key_prefix='DtlKey',
                                          suffix=suffix_joint,
                                          side_LFT=side_LFT,
                                          side_RGT=side_RGT
                                          )

    sAdd = sd.listSkeletonDuplicate(value_prefix=sAdd_prefix_value,
                                    key_prefix='Scl',
                                    suffix=suffix_joint,
                                    side_LFT=side_LFT,
                                    side_RGT=side_RGT
                                    )

    sSkn= sd.listSkeletonDuplicate(value_prefix='',
                                   key_prefix='Skin',
                                   suffix='skn',
                                   side_LFT=side_LFT,
                                   side_RGT=side_RGT
                                   )

    # parent skin into skin group
    mc.parent(sSkn.root, base.skin_grp)

    print ('5%  | skeleton duplicated is done!')

# ======================================================================================================================
#                                                     SPINE PARAMETERS
# ======================================================================================================================
    spine = sm.Spine(prefix=prefix_spine,
                     prefix_spine_setup=prefix_spine_setup,
                     detail_spine_deformer=detail_spine_deformer,
                     base_controller=base,
                     size=scale,
                     spine_jnt= sj.spine_list,
                     pelvis_jnt= sj.pelvis,
                     root_jnt= sj.root,
                     skin_root_jnt=sSkn.root,
                     skin_pelvis_jnt=sSkn.pelvis,
                     skin_spine_jnt= sSkn.spine_list,
                     single_module=False,
                     )

    print ('10% | spine is done!')

# ======================================================================================================================
#                                                  LEFT CLAVICLE PARAMETERS
# ======================================================================================================================
    clavLFT = cm.Clavicle(clavicle=clavicle_left,
                          skin_joint_clavicle=sSkn.clav_LFT,
                          prefix=prefix_clav,
                          side=side_LFT,
                          base_controller=base,
                          clavicle_jnt=sj.clav_LFT,
                          scale_jnt=ss.clav_LFT,
                          parent_jnt=sj.spine_list[-1],
                          size=scale,
                          single_module=False
                          )

    print ('15% | left clavicle is done!')

# ======================================================================================================================
#                                                   RIGHT CLAVICLE PARAMETERS
# ======================================================================================================================
    clavRGT = cm.Clavicle(clavicle=clavicle_right,
                          skin_joint_clavicle=sSkn.clav_RGT,
                          prefix=prefix_clav,
                          side=side_RGT,
                          base_controller=base,
                          clavicle_jnt=sj.clav_RGT,
                          scale_jnt=ss.clav_RGT,
                          parent_jnt=sj.spine_list[-1],
                          size=scale,
                          single_module=False
                          )

    print ('20% | right clavicle is done!')

# ======================================================================================================================
#                                                   LEFT ARM PARAMETERS
# ======================================================================================================================
    armLFT = lm.Limb(limb=arm_left,
                     arm=True,
                     prefix=prefix_arm,
                     side=side_LFT,
                     base_controller=base,
                     prefix_upper_limb=prefix_upperArm,
                     prefix_upper_limb_fk=prefix_upperArm + fk,
                     prefix_middle_limb_fk=prefix_forearm + fk,
                     prefix_lower_limb_fk=prefix_wrist + fk,
                     prefix_upper_limb_ik=prefix_upperArm + ik,
                     prefix_poleVector_ik=prefix_elbow + ik,
                     prefix_middle_limb_ik=prefix_forearm + ik,
                     prefix_lower_limb_ik=prefix_wrist + ik,
                     prefix_end_limb_ik=prefix_hand + ik,
                     prefix_limb_setup=prefix_arm_setup,
                     upper_limb_jnt=sj.upArm_LFT,
                     middle_limb_jnt=sj.forearm_LFT,
                     lower_limb_jnt=sj.wrist_LFT,
                     end_limb_jnt=None,
                     lower_limb_scale_jnt=None,
                     end_limb_scale_jnt=None,
                     upper_limb_fk_jnt=sFk.upArm_LFT,
                     middle_limb_fk_jnt=sFk.forearm_LFT,
                     lower_limb_fk_jnt=sFk.wrist_LFT,
                     upper_limb_ik_jnt=sIk.upArm_LFT,
                     middle_limb_ik_jnt=sIk.forearm_LFT,
                     lower_limb_ik_jnt=sIk.wrist_LFT,
                     end_limb_ik_jnt=sIk.hand_LFT,
                     upper_limb_twist_help_driver_jnt=sTwistHelp.upArm_LFT,
                     middle_limb_twist_help_driver_jnt=sTwistHelp.forearm_LFT,
                     world=base.body_part_grp,
                     detail_limb_deformer=detail_arm_deformer,
                     number_detail_ctrl=number_arm_detail_ctrl,
                     clav_jnt=sj.clav_LFT,
                     pelvis_gimbal_ctrl=None,
                     root_gimbal_ctrl= spine.root_gimbal_controller,
                     parallel_axis='x',
                     tip_pos='+',
                     prefix_upper_limb_detail=prefix_upperArm + detail,
                     prefix_middle_limb_detail=prefix_forearm + detail,
                     size=scale,
                     singleModule=False,
                     skin_upper_limb_jnt=sSkn.upArm_LFT,
                     skin_middle_limb_jnt=sSkn.forearm_LFT,
                     skin_lower_limb_jnt=sSkn.wrist_LFT,
                     )
    print ('25% | left arm is done!')

# ======================================================================================================================
#                                                   RIGHT ARM PARAMETERS
# ======================================================================================================================
    armRGT = lm.Limb(limb=arm_right,
                     arm=True,
                     prefix=prefix_arm,
                     side=side_RGT,
                     base_controller=base,
                     prefix_upper_limb=prefix_upperArm,
                     prefix_upper_limb_fk=prefix_upperArm + fk,
                     prefix_middle_limb_fk=prefix_forearm + fk,
                     prefix_lower_limb_fk=prefix_wrist + fk,
                     prefix_upper_limb_ik=prefix_upperArm + ik,
                     prefix_poleVector_ik=prefix_elbow + ik,
                     prefix_middle_limb_ik=prefix_forearm + ik,
                     prefix_lower_limb_ik=prefix_wrist + ik,
                     prefix_end_limb_ik=prefix_hand + ik,
                     prefix_limb_setup=prefix_arm_setup,
                     upper_limb_jnt=sj.upArm_RGT,
                     middle_limb_jnt=sj.forearm_RGT,
                     lower_limb_jnt=sj.wrist_RGT,
                     end_limb_jnt=None,
                     lower_limb_scale_jnt=None,
                     end_limb_scale_jnt=None,
                     upper_limb_fk_jnt=sFk.upArm_RGT,
                     middle_limb_fk_jnt=sFk.forearm_RGT,
                     lower_limb_fk_jnt=sFk.wrist_RGT,
                     upper_limb_ik_jnt=sIk.upArm_RGT,
                     middle_limb_ik_jnt=sIk.forearm_RGT,
                     lower_limb_ik_jnt=sIk.wrist_RGT,
                     end_limb_ik_jnt=sIk.hand_RGT,
                     upper_limb_twist_help_driver_jnt=sTwistHelp.upArm_RGT,
                     middle_limb_twist_help_driver_jnt=sTwistHelp.forearm_RGT,
                     detail_limb_deformer=detail_arm_deformer,
                     number_detail_ctrl= number_arm_detail_ctrl,
                     clav_jnt=sj.clav_RGT,
                     pelvis_gimbal_ctrl=None,
                     root_gimbal_ctrl=spine.root_gimbal_controller,
                     parallel_axis='x',
                     tip_pos='-',
                     world=base.body_part_grp,
                     prefix_upper_limb_detail=prefix_upperArm + detail,
                     prefix_middle_limb_detail=prefix_forearm + detail,
                     size=scale,
                     singleModule=False,
                     skin_upper_limb_jnt=sSkn.upArm_RGT,
                     skin_middle_limb_jnt=sSkn.forearm_RGT,
                     skin_lower_limb_jnt=sSkn.wrist_RGT,
                     )

    print ('30% | right arm is done!')

# ======================================================================================================================
#                                                   LEFT HAND PARAMETERS
# ======================================================================================================================
    handLFT = hm.Hand(parent=arm_left,
                      arm_object=armLFT,
                      thumb=thumb_arm_LFT,
                      index=index_arm_LFT,
                      middle=middle_arm_LFT,
                      ring=ring_arm_LFT,
                      pinky=pinky_arm_LFT,
                      thumb_finger_base=sj.thumb1_LFT,
                      thumb_finger_up=sj.thumb2_LFT,
                      thumb_finger_mid=sj.thumb3_LFT,
                      skin_thumb_finger_base=sSkn.thumb1_LFT,
                      skin_thumb_finger_up=sSkn.thumb2_LFT,
                      skin_thumb_finger_mid=sSkn.thumb3_LFT,
                      skin_thumb_finger_end=sSkn.thumb4_LFT,
                      prefix_thumb_finger_base=prefix_thumb + BaseF,
                      prefix_thumb_finger_up=prefix_thumb + UpF,
                      prefix_thumb_finger_mid=prefix_thumb + MidF,
                      index_finger_base=sj.index1_LFT,
                      index_finger_up=sj.index2_LFT,
                      index_finger_mid=sj.index3_LFT,
                      index_finger_low=sj.index4_LFT,
                      skin_index_finger_base=sSkn.index1_LFT,
                      skin_index_finger_up=sSkn.index2_LFT,
                      skin_index_finger_mid=sSkn.index3_LFT,
                      skin_index_finger_low=sSkn.index4_LFT,
                      skin_index_finger_end=sSkn.index5_LFT,
                      prefix_index_finger_base=prefix_index + BaseF,
                      prefix_index_finger_up=prefix_index + UpF,
                      prefix_index_finger_mid=prefix_index + MidF,
                      prefix_index_finger_low=prefix_index + LowF,
                      middle_finger_base=sj.middle1_LFT,
                      middle_finger_up=sj.middle2_LFT,
                      middle_finger_mid=sj.middle3_LFT,
                      middle_finger_low=sj.middle4_LFT,
                      skin_middle_finger_base=sSkn.middle1_LFT,
                      skin_middle_finger_up=sSkn.middle2_LFT,
                      skin_middle_finger_mid=sSkn.middle3_LFT,
                      skin_middle_finger_low=sSkn.middle4_LFT,
                      skin_middle_finger_end=sSkn.middle5_LFT,
                      prefix_middle_finger_base=prefix_middle + BaseF,
                      prefix_middle_finger_up=prefix_middle + UpF,
                      prefix_middle_finger_mid=prefix_middle + MidF,
                      prefix_middle_finger_low=prefix_middle + LowF,
                      ring_finger_base=sj.ring1_LFT,
                      ring_finger_up=sj.ring2_LFT,
                      ring_finger_mid=sj.ring3_LFT,
                      ring_finger_low=sj.ring4_LFT,
                      skin_ring_finger_base=sSkn.ring1_LFT,
                      skin_ring_finger_up=sSkn.ring2_LFT,
                      skin_ring_finger_mid=sSkn.ring3_LFT,
                      skin_ring_finger_low=sSkn.ring4_LFT,
                      skin_ring_finger_end=sSkn.ring5_LFT,
                      prefix_ring_finger_base=prefix_ring + BaseF,
                      prefix_ring_finger_up=prefix_ring + UpF,
                      prefix_ring_finger_mid=prefix_ring + MidF,
                      prefix_ring_finger_low=prefix_ring + LowF,
                      pinky_finger_base=sj.pinky1_LFT,
                      pinky_finger_up=sj.pinky2_LFT,
                      pinky_finger_mid=sj.pinky3_LFT,
                      pinky_finger_low=sj.pinky4_LFT,
                      skin_pinky_finger_base=sSkn.pinky1_LFT,
                      skin_pinky_finger_up=sSkn.pinky2_LFT,
                      skin_pinky_finger_mid=sSkn.pinky3_LFT,
                      skin_pinky_finger_low=sSkn.pinky4_LFT,
                      skin_pinky_finger_end=sSkn.pinky5_LFT,
                      prefix_pinky_finger_base=prefix_pinky + BaseF,
                      prefix_pinky_finger_up=prefix_pinky + UpF,
                      prefix_pinky_finger_mid=prefix_pinky + MidF,
                      prefix_pinky_finger_low=prefix_pinky + LowF,
                      prefix_finger_setup=prefix_finger_setup,
                      prefix_palm=prefix_palm,
                      palm_jnt=sj.palm_LFT,
                      skin_palm_jnt=sSkn.palm_LFT,
                      wrist_jnt=sj.wrist_LFT,
                      hand_jnt=sj.hand_LFT,
                      skin_hand_jnt=sSkn.hand_LFT,
                      side=side_LFT,
                      size=scale)

    print ('35% | left hand is done!')

# ======================================================================================================================
#                                                   RIGHT HAND PARAMETERS
# ======================================================================================================================
    handRGT = hm.Hand(parent=arm_right,
                      arm_object=armRGT,
                      thumb=thumb_arm_RGT,
                      index=index_arm_RGT,
                      middle=middle_arm_RGT,
                      ring=ring_arm_RGT,
                      pinky=pinky_arm_RGT,
                      thumb_finger_base= sj.thumb1_RGT,
                      thumb_finger_up= sj.thumb2_RGT,
                      thumb_finger_mid= sj.thumb3_RGT,
                      skin_thumb_finger_base=sSkn.thumb1_RGT,
                      skin_thumb_finger_up=sSkn.thumb2_RGT,
                      skin_thumb_finger_mid=sSkn.thumb3_RGT,
                      skin_thumb_finger_end=sSkn.thumb4_RGT,
                      prefix_thumb_finger_base=prefix_thumb + BaseF,
                      prefix_thumb_finger_up=prefix_thumb + UpF,
                      prefix_thumb_finger_mid=prefix_thumb + MidF,
                      index_finger_base=sj.index1_RGT,
                      index_finger_up=sj.index2_RGT,
                      index_finger_mid=sj.index3_RGT,
                      index_finger_low=sj.index4_RGT,
                      skin_index_finger_base=sSkn.index1_RGT,
                      skin_index_finger_up=sSkn.index2_RGT,
                      skin_index_finger_mid=sSkn.index3_RGT,
                      skin_index_finger_low=sSkn.index4_RGT,
                      skin_index_finger_end=sSkn.index5_RGT,
                      prefix_index_finger_base=prefix_index + BaseF,
                      prefix_index_finger_up=prefix_index + UpF,
                      prefix_index_finger_mid=prefix_index + MidF,
                      prefix_index_finger_low=prefix_index + LowF,
                      middle_finger_base=sj.middle1_RGT,
                      middle_finger_up=sj.middle2_RGT,
                      middle_finger_mid=sj.middle3_RGT,
                      middle_finger_low=sj.middle4_RGT,
                      skin_middle_finger_base=sSkn.middle1_RGT,
                      skin_middle_finger_up=sSkn.middle2_RGT,
                      skin_middle_finger_mid=sSkn.middle3_RGT,
                      skin_middle_finger_low=sSkn.middle4_RGT,
                      skin_middle_finger_end=sSkn.middle5_RGT,
                      prefix_middle_finger_base=prefix_middle + BaseF,
                      prefix_middle_finger_up=prefix_middle + UpF,
                      prefix_middle_finger_mid=prefix_middle + MidF,
                      prefix_middle_finger_low=prefix_middle + LowF,
                      ring_finger_base=sj.ring1_RGT,
                      ring_finger_up=sj.ring2_RGT,
                      ring_finger_mid=sj.ring3_RGT,
                      ring_finger_low=sj.ring4_RGT,
                      skin_ring_finger_base=sSkn.ring1_RGT,
                      skin_ring_finger_up=sSkn.ring2_RGT,
                      skin_ring_finger_mid=sSkn.ring3_RGT,
                      skin_ring_finger_low=sSkn.ring4_RGT,
                      skin_ring_finger_end=sSkn.ring5_RGT,
                      prefix_ring_finger_base=prefix_ring + BaseF,
                      prefix_ring_finger_up=prefix_ring + UpF,
                      prefix_ring_finger_mid=prefix_ring + MidF,
                      prefix_ring_finger_low=prefix_ring + LowF,
                      pinky_finger_base=sj.pinky1_RGT,
                      pinky_finger_up=sj.pinky2_RGT,
                      pinky_finger_mid=sj.pinky3_RGT,
                      pinky_finger_low=sj.pinky4_RGT,
                      skin_pinky_finger_base=sSkn.pinky1_RGT,
                      skin_pinky_finger_up=sSkn.pinky2_RGT,
                      skin_pinky_finger_mid=sSkn.pinky3_RGT,
                      skin_pinky_finger_low=sSkn.pinky4_RGT,
                      skin_pinky_finger_end=sSkn.pinky5_RGT,
                      prefix_pinky_finger_base=prefix_pinky + BaseF,
                      prefix_pinky_finger_up=prefix_pinky + UpF,
                      prefix_pinky_finger_mid=prefix_pinky + MidF,
                      prefix_pinky_finger_low=prefix_pinky + LowF,
                      prefix_finger_setup= prefix_finger_setup,
                      prefix_palm=prefix_palm,
                      palm_jnt=sj.palm_RGT,
                      skin_palm_jnt=sSkn.palm_RGT,
                      wrist_jnt=sj.wrist_RGT,
                      hand_jnt=sj.hand_RGT,
                      skin_hand_jnt=sSkn.hand_RGT,
                      side=side_RGT,
                      size=scale)

    print ('45% | right hand is done!')

# ======================================================================================================================
#                                                   LEFT LEG PARAMETERS
# ======================================================================================================================
    legLFT = lm.Limb(limb=leg_left,
                     endLimb=foot_left,
                     arm=False,
                     prefix=prefix_leg,
                     side=side_LFT,
                     base_controller=base,
                     prefix_upper_limb=prefix_upperLeg,
                     prefix_upper_limb_fk=prefix_upperLeg + fk,
                     prefix_middle_limb_fk=prefix_lowerLeg + fk,
                     prefix_lower_limb_fk=prefix_ankle + fk,
                     prefix_upper_limb_ik=prefix_upperLeg + ik,
                     prefix_poleVector_ik=prefix_knee + ik,
                     prefix_middle_limb_ik=prefix_lowerLeg + ik,
                     prefix_lower_limb_ik=prefix_ankle + ik,
                     prefix_end_limb_ik=prefix_ball + ik,
                     prefix_limb_setup=prefix_leg_setup,
                     upper_limb_jnt=sj.upLeg_LFT,
                     middle_limb_jnt=sj.lowLeg_LFT,
                     lower_limb_jnt=sj.ankle_LFT,
                     end_limb_jnt=sj.ball_LFT,
                     lower_limb_scale_jnt=ss.ankle_LFT,
                     end_limb_scale_jnt=ss.ball_LFT,
                     upper_limb_fk_jnt=sFk.upLeg_LFT,
                     middle_limb_fk_jnt=sFk.lowLeg_LFT,
                     lower_limb_fk_jnt=sFk.ankle_LFT,
                     upper_limb_ik_jnt=sIk.upLeg_LFT,
                     middle_limb_ik_jnt=sIk.lowLeg_LFT,
                     lower_limb_ik_jnt=sIk.ankle_LFT,
                     end_limb_ik_jnt=sIk.ball_LFT,
                     upper_limb_twist_help_driver_jnt=sTwistHelp.upLeg_LFT,
                     middle_limb_twist_help_driver_jnt=sTwistHelp.lowLeg_LFT,
                     world=base.body_part_grp,
                     detail_limb_deformer=detail_leg_def,
                     number_detail_ctrl=num_leg_dtl_ctrl,
                     clav_jnt=None,
                     pelvis_gimbal_ctrl=spine.pelvis_gimbal_controller,
                     root_gimbal_ctrl=None,
                     parallel_axis='y',
                     tip_pos='-',
                     prefix_upper_limb_detail=prefix_upperLeg + detail,
                     prefix_middle_limb_detail=prefix_lowerLeg + detail,
                     size=scale,
                     singleModule=False,
                     skin_upper_limb_jnt=sSkn.upLeg_LFT,
                     skin_middle_limb_jnt=sSkn.lowLeg_LFT,
                     skin_lower_limb_jnt=sSkn.ankle_LFT,
                     )

    print('55% | left leg is done!')

    # ======================================================================================================================
#                                                   RIGHT LEG PARAMETERS
# ======================================================================================================================
    legRGT = lm.Limb(limb=leg_right,
                     endLimb=foot_right,
                     arm=False,
                     prefix=prefix_leg,
                     side=side_RGT,
                     base_controller=base,
                     prefix_upper_limb=prefix_upperLeg,
                     prefix_upper_limb_fk=prefix_upperLeg + fk,
                     prefix_middle_limb_fk=prefix_lowerLeg + fk,
                     prefix_lower_limb_fk=prefix_ankle + fk,
                     prefix_upper_limb_ik=prefix_upperLeg + ik,
                     prefix_poleVector_ik=prefix_knee + ik,
                     prefix_middle_limb_ik=prefix_lowerLeg + ik,
                     prefix_lower_limb_ik=prefix_ankle + ik,
                     prefix_end_limb_ik=prefix_ball + ik,
                     prefix_limb_setup=prefix_leg_setup,
                     upper_limb_jnt=sj.upLeg_RGT,
                     middle_limb_jnt=sj.lowLeg_RGT,
                     lower_limb_jnt=sj.ankle_RGT,
                     end_limb_jnt=sj.ball_RGT,
                     lower_limb_scale_jnt=ss.ankle_RGT,
                     end_limb_scale_jnt=ss.ball_RGT,
                     upper_limb_fk_jnt=sFk.upLeg_RGT,
                     middle_limb_fk_jnt=sFk.lowLeg_RGT,
                     lower_limb_fk_jnt=sFk.ankle_RGT,
                     upper_limb_ik_jnt=sIk.upLeg_RGT,
                     middle_limb_ik_jnt=sIk.lowLeg_RGT,
                     lower_limb_ik_jnt=sIk.ankle_RGT,
                     end_limb_ik_jnt=sIk.ball_RGT,
                     upper_limb_twist_help_driver_jnt=sTwistHelp.upLeg_RGT,
                     middle_limb_twist_help_driver_jnt=sTwistHelp.lowLeg_RGT,
                     world=base.body_part_grp,
                     detail_limb_deformer=detail_leg_def,
                     number_detail_ctrl=num_leg_dtl_ctrl,
                     clav_jnt=None,
                     pelvis_gimbal_ctrl=spine.pelvis_gimbal_controller,
                     root_gimbal_ctrl=None,
                     parallel_axis='y',
                     tip_pos='-',
                     prefix_upper_limb_detail=prefix_upperLeg + detail,
                     prefix_middle_limb_detail=prefix_lowerLeg + detail,
                     size=scale,
                     singleModule=False,
                     skin_upper_limb_jnt=sSkn.upLeg_RGT,
                     skin_middle_limb_jnt=sSkn.lowLeg_RGT,
                     skin_lower_limb_jnt=sSkn.ankle_RGT,
                     )


    print('65% | right leg is done!')

# ======================================================================================================================
#                                                   LEFT FOOT PARAMETERS
# ======================================================================================================================
    if leg_left:
        footLFT = fm.Foot(foot=foot_left,
                          leg=legLFT,
                          prefix=prefix_foot,
                          upper_limb_jnt=sj.upLeg_LFT,
                          ball_fk_jnt=sFk.ball_LFT,
                          ball_ik_jnt=sIk.ball_LFT,
                          toe_ik_jnt=sIk.toe_LFT,
                          ball_jnt=sj.ball_LFT,
                          heel_jnt=sj.heel_LFT,
                          lower_limb_jnt=sj.ankle_LFT,
                          in_tilt_jnt=sj.footIn_LFT,
                          out_tilt_jnt=sj.footOut_LFT,
                          prefix_ball_fk=prefix_ball + fk,
                          prefix_toe_ik=prefix_toe + ik,
                          lower_gimbal_fk_ctrl=legLFT.lower_limb_fk_gimbal,
                          lower_limb_ik_hdl=legLFT.lower_limb_ik_hdl,
                          end_limb_ik_hdl=legLFT.end_limb_ik_hdl,
                          controller_FkIk_limb_setup=legLFT.FkIk_limb_setup_controller,
                          controller_lower_limb_ik=legLFT.lower_limb_ik_control,
                          position_soft_jnt=legLFT.pos_soft_jnt,
                          part_joint_grp_module=legLFT.part_joint_grp,
                          ankle_scale_jnt=ss.ankle_LFT,
                          skin_ankle_jnt=sSkn.ankle_LFT,
                          ball_scale_jnt=ss.ball_LFT,
                          skin_ball_jnt=sSkn.ball_LFT,
                          skin_toe_jnt=sSkn.toe_LFT,
                          skin_heel_jnt=sSkn.heel_LFT,
                          skin_foot_in_jnt=sSkn.footIn_LFT,
                          skin_foot_out_jnt=sSkn.footOut_LFT,
                          side=side_LFT,
                          scale=scale)

    print('75% | left foot is done!')
# ======================================================================================================================
#                                                   RIGHT FOOT PARAMETERS
# ======================================================================================================================
    if leg_right:
        footRGT = fm.Foot(foot=foot_right,
                          leg=legRGT,
                          prefix=prefix_foot,
                          upper_limb_jnt=sj.upLeg_RGT,
                          ball_fk_jnt=sFk.ball_RGT,
                          ball_ik_jnt=sIk.ball_RGT,
                          toe_ik_jnt=sIk.toe_RGT,
                          ball_jnt=sj.ball_RGT,
                          heel_jnt=sj.heel_RGT,
                          lower_limb_jnt=sj.ankle_RGT,
                          in_tilt_jnt=sj.footIn_RGT,
                          out_tilt_jnt=sj.footOut_RGT,
                          prefix_ball_fk=prefix_ball + fk,
                          prefix_toe_ik=prefix_toe + ik,
                          lower_gimbal_fk_ctrl=legRGT.lower_limb_fk_gimbal,
                          lower_limb_ik_hdl=legRGT.lower_limb_ik_hdl,
                          end_limb_ik_hdl=legRGT.end_limb_ik_hdl,
                          controller_FkIk_limb_setup=legRGT.FkIk_limb_setup_controller,
                          controller_lower_limb_ik=legRGT.lower_limb_ik_control,
                          position_soft_jnt=legRGT.pos_soft_jnt,
                          part_joint_grp_module=legRGT.part_joint_grp,
                          ankle_scale_jnt=ss.ankle_RGT,
                          skin_ankle_jnt=sSkn.ankle_RGT,
                          ball_scale_jnt=ss.ball_RGT,
                          skin_ball_jnt=sSkn.ball_RGT,
                          skin_toe_jnt=sSkn.toe_RGT,
                          skin_heel_jnt=sSkn.heel_RGT,
                          skin_foot_in_jnt=sSkn.footIn_RGT,
                          skin_foot_out_jnt=sSkn.footOut_RGT,
                          side=side_RGT,
                          scale=scale)

    print('85% | right foot is done!')


    # ==================================================================================================================
    #                                                     CLEAN UP SET
    # ==================================================================================================================
    # UNHIDE AND SEGMENT SCALE
    unhide = mc.ls('*skn')
    for i in unhide:
        mc.setAttr(i + '.visibility', 1)
        mc.setAttr(i + '.segmentScaleCompensate', 0)
    mc.setAttr(sSkn.neck + '.visibility', 0)

    # PARENT TO GENERAL MODULE
    if mc.objExists('anim_grp'):
        mc.parent(base.anim_control, 'anim_grp')

    mc.delete(sAdd.neck, sj.neck)
    # PARENT TO ADD JOINT TO SKELETON GROUP
    selection =[sAdd.spine_list[0], sAdd.upLeg_LFT, sAdd.upLeg_RGT]
    list_relatives = mc.listRelatives(selection, c=1, ad=1)
    list_object = []
    for obj in list_relatives:
        list_object.append(obj)
        list_object.extend(selection)
        while '' in list_object:
            list_object.remove('')

    mc.parent(list(set(list_object)), base.skeleton_grp)

    # # mc.parent(sAdd.clavLFT, sAdd.upArmLFT, sAdd.forearmLFT, sAdd.wristLFT, module.skeletonGrp)
    # # mc.parent(sAdd.clavRGT, sAdd.upArmRGT, sAdd.forearmRGT, sAdd.wristRGT, module.skeletonGrp)
    # # mc.parent(sAdd.upLegLFT, sAdd.lowLegLFT, sAdd.ankleLFT, sAdd.ballLFT, module.skeletonGrp)
    # # mc.parent(sAdd.upLegRGT, sAdd.lowLegRGT, sAdd.ankleRGT, sAdd.ballRGT, module.skeletonGrp)
    # # mc.parent(sAdd.thumb1LFT, sAdd.thumb1RGT, sAdd.palmLFT, sAdd.palmRGT, sAdd.handLFT, sAdd.handRGT,
    # #           sAdd.thumb2LFT, sAdd.thumb2RGT, sAdd.index1LFT, sAdd.index1RGT,
    # #           sAdd.index2LFT, sAdd.index2RGT, sAdd.middle1LFT, sAdd.middle1RGT, sAdd.middle2LFT, sAdd.middle2RGT,
    # #           sAdd.ring1LFT, sAdd.ring1RGT, sAdd.pinky1LFT, sAdd.pinky1RGT,
    # #           sAdd.ring2LFT, sAdd.ring2RGT, sAdd.pinky2LFT, sAdd.pinky2RGT, sAdd.thumb3LFT, sAdd.thumb3RGT,
    # #           sAdd.index3LFT, sAdd.index3RGT, sAdd.middle3LFT, sAdd.middle3RGT,
    # #           sAdd.ring3LFT, sAdd.ring3RGT, sAdd.pinky3LFT, sAdd.pinky3RGT, sAdd.index4LFT, sAdd.index4RGT,
    # #           sAdd.middle4LFT, sAdd.middle4RGT,
    # #           sAdd.ring4LFT, sAdd.ring4RGT, sAdd.pinky4LFT, sAdd.pinky4RGT, module.skeletonGrp)
    #
    # mc.parent(sAdd.neck, module.skeletonGrp)
    #
    # # DELETE ITEMS UNDER WRIST FK AND IK
    # list = [sFk.wristLFT, sFk.wristRGT, sIk.wristLFT, sIk.wristRGT]
    # listLRFkIk = mc.listRelatives(list, ad=1, c=1)
    # for i in listLRFkIk:
    #     mc.delete(i)
    #
    #
    # # delete unused bones
    # mc.delete(sFk.thumb1LFT, sFk.thumb1RGT)
    # mc.delete(sIk.thumb1LFT, sIk.thumb1RGT)
    # mc.delete(sFk.handLFT, sFk.handRGT)
    # mc.delete(sIk.index1LFT, sIk.index1RGT)
    # mc.delete(sIk.middle1LFT, sIk.middle1RGT)
    # mc.delete(sIk.ring1LFT, sIk.ring1RGT)
    # mc.delete(sIk.pinky1LFT, sIk.pinky1RGT)
    # mc.delete(sFk.palmLFT, sFk.palmRGT)
    # mc.delete(sIk.palmLFT, sIk.palmRGT)
    #
    # mc.delete(ss.upArmLFT, ss.upArmRGT)
    # mc.delete(ss.heelLFT, ss.heelRGT)
    # mc.delete(ss.footInLFT, ss.footInRGT)
    # mc.delete(ss.footOutLFT, ss.footOutRGT)
    # mc.delete(ss.toeLFT, ss.toeRGT)
    #
    #
    # mc.delete(sj.heelLFT, sj.heelRGT)
    # mc.delete(sj.footInLFT, sj.footInRGT)
    # mc.delete(sj.footOutLFT, sj.footOutRGT)
    #
    # mc.delete(sFk.heelLFT, sFk.heelRGT)
    # mc.delete(sFk.footInLFT, sFk.footInRGT)
    # mc.delete(sFk.footOutLFT, sFk.footOutRGT)
    # mc.delete(sIk.heelLFT, sIk.heelRGT)
    # mc.delete(sIk.footInLFT, sIk.footInRGT)
    # mc.delete(sIk.footOutLFT, sIk.footOutRGT)
    #
    # mc.delete(sAdd.palmLFT, sAdd.palmRGT)
    # mc.delete(sAdd.heelLFT, sAdd.heelRGT)
    # mc.delete(sAdd.footInLFT, sAdd.footInRGT)
    # mc.delete(sAdd.footOutLFT, sAdd.footOutRGT)
    # mc.delete(sAdd.toeLFT, sAdd.toeRGT)
    # mc.delete(sTwistHelpJnt.wristLFT, sTwistHelpJnt.wristRGT)
    # mc.delete(sTwistHelpJnt.ankleLFT, sTwistHelpJnt.ankleRGT)
    # mc.delete(sAdd.thumb1LFT, sAdd.thumb1RGT, sAdd.thumb4LFT, sAdd.thumb4RGT, sAdd.index5LFT, sAdd.index5RGT, sAdd.middle5LFT, sAdd.middle5RGT,
    #           sAdd.ring5LFT, sAdd.ring5RGT, sAdd.pinky5LFT, sAdd.pinky5RGT)
    #
    # mc.delete(sj.neck)
    #
    #
    # mc.delete(sAdd.handLFT, sAdd.handRGT)
    # mc.delete(sAdd.head)
    mc.delete(ss.root)
    mc.delete(sIk.root)
    mc.delete(sFk.root)
    mc.delete(sAdd.root)
    mc.delete(sTwistHelp.root)
    #
    # print('100% | clean up!')