import maya.cmds as mc

from rigLib.base import general_module as gm, template_module as sd
from rigLib.base.body import spine_module as sm, foot_module as fm, clavicle_module as cm, hand_module as hm, \
    limb_module as lm
from rigLib.rig.body import expand_skeleton as aj

from rigLib.utils import template_skeleton as dt

reload(gm)
reload(sm)
reload(cm)
reload(aj)
reload(lm)
reload(hm)
reload(fm)
reload(dt)
reload(sd)

def BuildRig(clavicleLeft, clavicleRight, armLeft, armRight, handLeft, handRight, prefixSpine, prefixUpperArm, prefixForearm,
             prefixClav, prefixArm, prefixSpineSetup, prefixWrist,
             prefixElbow, prefixHand, prefixArmSetup, detailSpineDef, detailArmDef, numArmDtlCtrl,
             legLeft, legRight, footRight, footLeft, prefixUpperLeg, prefixLowerLeg,
             prefixLeg, prefixAnkle, prefixFoot,
             prefixKnee, prefixBall, prefixToe, prefixLegSetup, detailLegDef, numLegDtlCtrl,
             prefixThumb, prefixIndex,
             thumbArm, indexArm, middleArm, ringArm, pinkyArm, prefixFingerSetup,
             prefixMiddle, prefixRing, prefixPinky,
             scale, sideLFT, sideRGT, clavicleShapeJoint, upperArmShapeJoint, elbowShapeJoint, wristShapeJoint,
             upperLegShapeJoint, kneeShapeJoint, ankleShapeJoint, ballShapeJoint):

    Fk = 'Fk'
    Ik = 'Ik'
    Dtl = 'Dtl'

    # FINGER POSITION
    BaseF = 'Base'
    UpF = 'Up'
    MidF = 'Mid'
    LowF = 'Low'

    # CREATE BASE RIG
    base = gm.Base(scale=scale)

# ======================================================================================================================
#                                              DUPLICATE JOINTS AS DRIVER
# ======================================================================================================================
    sj = sd.listSkeletonDuplicate(objDuplicate='root_tmpJnt',
                                  value_prefix='Driver',
                                  key_prefix='Ori',
                                  suffix='jnt'
                                  )

    ss = sd.listSkeletonDuplicate(objDuplicate='root_tmpJnt',
                                  value_prefix='DriverScale',
                                  key_prefix='Scl',
                                  suffix='jnt'
                                  )

    sFk = sd.listSkeletonDuplicate(objDuplicate='root_tmpJnt',
                                   value_prefix='FkDriver',
                                   key_prefix='Fk',
                                   suffix='jnt'
                                   )

    sIk = sd.listSkeletonDuplicate(objDuplicate='root_tmpJnt',
                                   value_prefix='IkDriver',
                                   key_prefix='Ik',
                                   suffix='jnt'
                                   )

    sDtlJnt = sd.listSkeletonDuplicate(objDuplicate='root_tmpJnt',
                                       value_prefix='DriverDtl',
                                       key_prefix='DtlKey',
                                       suffix='jnt'
                                       )

    sDtlBind = sd.listSkeletonDuplicate(objDuplicate='root_tmpJnt',
                                        value_prefix='DriverDtl',
                                        key_prefix='DtlBind',
                                        suffix='bind'
                                        )
    print '5%  | skeleton duplicated is done!'

# ======================================================================================================================
#                                                     SPINE PARAMETERS
# ======================================================================================================================
    sm.Spine(prefix=prefixSpine,
             prefix_spine_setup=prefixSpineSetup,
             detail_spine_deformer=detailSpineDef,
             base_controller=base,
             size=scale,
             spine_jnt= sj.spine_list,
             pelvis_jnt= sj.pelvis,
             root_jnt= sj.root,
             parentJnt = sj.root,
             )

    print '10% | spine is done!'

# ======================================================================================================================
#                                                  LEFT CLAVICLE PARAMETERS
# ======================================================================================================================
    cm.Clavicle(clavicle=clavicleLeft,
                prefix=prefixClav,
                side=sideLFT,
                base_controller=base,
                clavicle_jnt=sj.clav_LFT,
                scale_jnt=ss.clav_LFT,
                parentScaleJnt=sj.clav_LFT,
                parent_jnt=sj.spine_list[-1],
                size=scale
                )

    print '15% | clavicle left is done!'

# ======================================================================================================================
#                                                   RIGHT CLAVICLE PARAMETERS
# ======================================================================================================================
    cm.Clavicle(clavicle=clavicleRight,
                prefix=prefixClav,
                side=sideRGT,
                base_controller=base,
                clavicle_jnt=sj.clav_RGT,
                scale_jnt=ss.clav_RGT,
                parentScaleJnt=sj.clav_RGT,
                parent_jnt=sj.spine_list[-1],
                size=scale
                )

    print '20% | clavicle right is done!'

# ======================================================================================================================
#                                                   LEFT ARM PARAMETERS
# ======================================================================================================================
    armLFT = lm.Limb(limb=armLeft,
                     arm=True,
                     prefix=prefixArm,
                     side=sideLFT,
                     base_controller=base,
                     prefix_upper_limb=prefixUpperArm,
                     prefixPoleVecLimb=prefixElbow,
                     prefixLowerLimb=prefixWrist,
                     prefixBaseOrTipLimb=prefixClav,
                     prefix_upper_limb_fk=prefixUpperArm + Fk,
                     prefix_middle_limb_fk=prefixForearm + Fk,
                     prefix_lower_limb_fk=prefixWrist + Fk,
                     prefix_upper_limb_ik=prefixUpperArm + Ik,
                     prefix_poleVector_ik=prefixElbow + Ik,
                     prefix_middle_limb_ik=prefixForearm + Ik,
                     prefix_lower_limb_ik=prefixWrist + Ik,
                     prefix_end_limb_ik=prefixHand + Ik,
                     prefix_limb_setup=prefixArmSetup,
                     pelvisJnt=None,
                     rootJnt=sj.root,
                     clav_jnt=sj.clav_LFT,
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
                     baseOrTipShapeJoint=clavicleShapeJoint,
                     upperLimbShapeJoint=upperArmShapeJoint,
                     middleLimbShapeJoint=elbowShapeJoint,
                     lowerLimbShapeJoint=wristShapeJoint,
                     upper_limb_twist_help_driver_jnt=sDtlJnt.upArm_LFT,
                     middle_limb_twist_help_driver_jnt=sDtlJnt.forearm_LFT,
                     upperLimbDtlBind= sDtlBind.upArm_LFT,
                     middleLimbDtlBind= sDtlBind.forearm_LFT,
                     world=base.body_part_grp,
                     detail_limb_deformer=detailArmDef,
                     number_detail_ctrl=numArmDtlCtrl,
                     parallel_axis='x',
                     tip_pos='+',
                     prefix_upper_limb_detail=prefixUpperArm + Dtl,
                     prefix_middle_limb_detail=prefixForearm + Dtl,
                     size=scale
                     )
    print '25% | arm left is done!'

# ======================================================================================================================
#                                                   RIGHT ARM PARAMETERS
# ======================================================================================================================
    armRGT = lm.Limb(limb=armRight,
                     arm=True,
                     prefix=prefixArm,
                     side=sideRGT,
                     base_controller=base,
                     prefix_upper_limb=prefixUpperArm,
                     prefixPoleVecLimb=prefixElbow,
                     prefixLowerLimb=prefixWrist,
                     prefixBaseOrTipLimb=prefixClav,
                     prefix_upper_limb_fk=prefixUpperArm + Fk,
                     prefix_middle_limb_fk=prefixForearm + Fk,
                     prefix_lower_limb_fk=prefixWrist + Fk,
                     prefix_upper_limb_ik=prefixUpperArm + Ik,
                     prefix_poleVector_ik=prefixElbow + Ik,
                     prefix_middle_limb_ik=prefixForearm + Ik,
                     prefix_lower_limb_ik=prefixWrist + Ik,
                     prefix_end_limb_ik=prefixHand + Ik,
                     prefix_limb_setup=prefixArmSetup,
                     pelvisJnt=None,
                     rootJnt=sj.root,
                     clav_jnt=sj.clav_RGT,
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
                     baseOrTipShapeJoint=clavicleShapeJoint,
                     upperLimbShapeJoint=upperArmShapeJoint,
                     middleLimbShapeJoint=elbowShapeJoint,
                     lowerLimbShapeJoint=wristShapeJoint,
                     upper_limb_twist_help_driver_jnt=sDtlJnt.upArm_RGT,
                     middle_limb_twist_help_driver_jnt=sDtlJnt.forearm_RGT,
                     upperLimbDtlBind=sDtlBind.upArm_RGT,
                     middleLimbDtlBind=sDtlBind.forearm_RGT,
                     detail_limb_deformer=detailArmDef,
                     number_detail_ctrl= numArmDtlCtrl,
                     parallel_axis='x',
                     tip_pos='-',
                     world=base.body_part_grp,
                     prefix_upper_limb_detail=prefixUpperArm + Dtl,
                     prefix_middle_limb_detail=prefixForearm + Dtl,
                     size=scale
                     )

    print '30% | arm right is done!'

# ======================================================================================================================
#                                                   LEFT HAND PARAMETERS
# ======================================================================================================================
    hm.Hand(parent=armLeft,
            arm_object=armLFT,
            hand=handLeft,
            thumb=thumbArm,
            index=indexArm,
            middle=middleArm,
            ring=ringArm,
            pinky=pinkyArm,
            thumb_finger_base=sj.thumb1_LFT,
            thumb_finger_up=sj.thumb2_LFT,
            thumb_finger_mid=sj.thumb3_LFT,
            prefix_thumb_finger_base=prefixThumb + BaseF,
            prefix_thumb_finger_up=prefixThumb + UpF,
            prefix_thumb_finger_mid=prefixThumb + MidF,
            index_finger_base=sj.index1_LFT,
            index_finger_up=sj.index2_LFT,
            index_finger_mid=sj.index3_LFT,
            index_finger_low=sj.index4_LFT,
            prefix_index_finger_base=prefixIndex + BaseF,
            prefix_index_finger_up=prefixIndex + UpF,
            prefix_index_finger_mid=prefixIndex + MidF,
            prefix_index_finger_low=prefixIndex + LowF,
            middle_finger_base=sj.middle1_LFT,
            middle_finger_up=sj.middle2LFT,
            middle_finger_mid=sj.middle3_LFT,
            middle_finger_low=sj.middle4_LFT,
            prefix_middle_finger_base=prefixMiddle + BaseF,
            prefix_middle_finger_up=prefixMiddle + UpF,
            prefix_middle_finger_mid=prefixMiddle + MidF,
            prefix_middle_finger_low=prefixMiddle + LowF,
            ring_finger_base=sj.ring1_LFT,
            ring_finger_up=sj.ring2_LFT,
            ring_finger_mid=sj.ring3_LFT,
            ring_finger_low=sj.ring4_LFT,
            prefix_ring_finger_base=prefixRing + BaseF,
            prefix_ring_finger_up=prefixRing + UpF,
            prefix_ring_finger_mid=prefixRing + MidF,
            prefix_ring_finger_low=prefixRing + LowF,
            pinky_finger_base=sj.pinky1_LFT,
            pinky_finger_up=sj.pinky2_LFT,
            pinky_finger_mid=sj.pinky3_LFT,
            pinky_finger_low=sj.pinky4_LFT,
            prefix_pinky_finger_base=prefixPinky + BaseF,
            prefix_pinky_finger_up=prefixPinky + UpF,
            prefix_pinky_finger_mid=prefixPinky + MidF,
            prefix_pinky_finger_low=prefixPinky + LowF,
            prefix_finger_setup=prefixFingerSetup,
            wrist_jnt=sj.wrist_LFT,
            hand_jnt=sj.hand_LFT,
            side=sideLFT,
            size=scale)

    print '35% | hand left is done!'

# ======================================================================================================================
#                                                   RIGHT HAND PARAMETERS
# ======================================================================================================================
    hm.Hand(parent=armRight,
            arm_object=armRGT,
            hand=handRight,
            thumb=thumbArm,
            index=indexArm,
            middle=middleArm,
            ring=ringArm,
            pinky=pinkyArm,
            thumb_finger_base= sj.thumb1_RGT,
            thumb_finger_up= sj.thumb2_RGT,
            thumb_finger_mid= sj.thumb3_RGT,
            prefix_thumb_finger_base=prefixThumb + BaseF,
            prefix_thumb_finger_up=prefixThumb + UpF,
            prefix_thumb_finger_mid=prefixThumb + MidF,
            index_finger_base=sj.index1_RGT,
            index_finger_up=sj.index2_RGT,
            index_finger_mid=sj.index3_RGT,
            index_finger_low=sj.index4_RGT,
            prefix_index_finger_base=prefixIndex + BaseF,
            prefix_index_finger_up=prefixIndex + UpF,
            prefix_index_finger_mid=prefixIndex + MidF,
            prefix_index_finger_low=prefixIndex + LowF,
            middle_finger_base=sj.middle1_RGT,
            middle_finger_up=sj.middle2_RGT,
            middle_finger_mid=sj.middle3_RGT,
            middle_finger_low=sj.middle4_RGT,
            prefix_middle_finger_base=prefixMiddle + BaseF,
            prefix_middle_finger_up=prefixMiddle + UpF,
            prefix_middle_finger_mid=prefixMiddle + MidF,
            prefix_middle_finger_low=prefixMiddle + LowF,
            ring_finger_base=sj.ring1_RGT,
            ring_finger_up=sj.ring2_RGT,
            ring_finger_mid=sj.ring3_RGT,
            ring_finger_low=sj.ring4_RGT,
            prefix_ring_finger_base=prefixRing + BaseF,
            prefix_ring_finger_up=prefixRing + UpF,
            prefix_ring_finger_mid=prefixRing + MidF,
            prefix_ring_finger_low=prefixRing + LowF,
            pinky_finger_base=sj.pinky1_RGT,
            pinky_finger_up=sj.pinky2_RGT,
            pinky_finger_mid=sj.pinky3_RGT,
            pinky_finger_low=sj.pinky4_RGT,
            prefix_pinky_finger_base=prefixPinky + BaseF,
            prefix_pinky_finger_up=prefixPinky + UpF,
            prefix_pinky_finger_mid=prefixPinky + MidF,
            prefix_pinky_finger_low=prefixPinky + LowF,
            prefix_finger_setup= prefixFingerSetup,
            wrist_jnt=sj.wrist_RGT,
            hand_jnt=sj.hand_RGT,
            side=sideRGT,
            size=scale)

    print '40% | hand right is done!'

# ======================================================================================================================
#                                                   LEFT LEG PARAMETERS
# ======================================================================================================================
    legLFT = lm.Limb(limb=legLeft,
                     arm=False,
                     prefix=prefixLeg,
                     side=sideLFT,
                     base_controller=base,
                     prefix_upper_limb=prefixUpperLeg,
                     prefixPoleVecLimb=prefixKnee,
                     prefixLowerLimb=prefixLowerLeg,
                     prefixBaseOrTipLimb=prefixBall,
                     prefix_upper_limb_fk=prefixUpperLeg + Fk,
                     prefix_middle_limb_fk=prefixLowerLeg + Fk,
                     prefix_lower_limb_fk=prefixAnkle + Fk,
                     prefix_upper_limb_ik=prefixUpperLeg + Ik,
                     prefix_poleVector_ik=prefixKnee + Ik,
                     prefix_middle_limb_ik=prefixLowerLeg + Ik,
                     prefix_lower_limb_ik=prefixAnkle + Ik,
                     prefix_end_limb_ik=prefixBall + Ik,
                     prefix_limb_setup=prefixLegSetup,
                     pelvisJnt=sj.pelvis,
                     rootJnt=None,
                     clav_jnt=None,
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
                     baseOrTipShapeJoint=ballShapeJoint,
                     upperLimbShapeJoint=upperLegShapeJoint,
                     middleLimbShapeJoint=kneeShapeJoint,
                     lowerLimbShapeJoint=ankleShapeJoint,
                     upper_limb_twist_help_driver_jnt=sDtlJnt.upLeg_LFT,
                     middle_limb_twist_help_driver_jnt=sDtlJnt.lowLeg_LFT,
                     upperLimbDtlBind=sDtlBind.upLeg_LFT,
                     middleLimbDtlBind=sDtlBind.lowLeg_LFT,
                     world=base.body_part_grp,
                     detail_limb_deformer=detailLegDef,
                     number_detail_ctrl=numLegDtlCtrl,
                     parallel_axis='y',
                     tip_pos='-',
                     prefix_upper_limb_detail=prefixUpperLeg + Dtl,
                     prefix_middle_limb_detail=prefixLowerLeg + Dtl,
                     size=scale
                     )

    print '45% | leg left is done!'

# ======================================================================================================================
#                                                   RIGHT LEG PARAMETERS
# ======================================================================================================================
    legRGT = lm.Limb(limb=legRight,
                     arm=False,
                     prefix=prefixLeg,
                     side=sideRGT,
                     base_controller=base,
                     prefix_upper_limb=prefixUpperLeg,
                     prefixPoleVecLimb=prefixKnee,
                     prefixLowerLimb=prefixLowerLeg,
                     prefixBaseOrTipLimb=prefixBall,
                     prefix_upper_limb_fk=prefixUpperLeg + Fk,
                     prefix_middle_limb_fk=prefixLowerLeg + Fk,
                     prefix_lower_limb_fk=prefixAnkle + Fk,
                     prefix_upper_limb_ik=prefixUpperLeg + Ik,
                     prefix_poleVector_ik=prefixKnee + Ik,
                     prefix_middle_limb_ik=prefixLowerLeg + Ik,
                     prefix_lower_limb_ik=prefixAnkle + Ik,
                     prefix_end_limb_ik=prefixBall + Ik,
                     prefix_limb_setup=prefixLegSetup,
                     pelvisJnt=sj.pelvis,
                     rootJnt=None,
                     clav_jnt=None,
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
                     baseOrTipShapeJoint=ballShapeJoint,
                     upperLimbShapeJoint=upperLegShapeJoint,
                     middleLimbShapeJoint=kneeShapeJoint,
                     lowerLimbShapeJoint=ankleShapeJoint,
                     upper_limb_twist_help_driver_jnt=sDtlJnt.upLeg_RGT,
                     middle_limb_twist_help_driver_jnt=sDtlJnt.lowLeg_RGT,
                     upperLimbDtlBind=sDtlBind.upLeg_RGT,
                     middleLimbDtlBind=sDtlBind.lowLeg_RGT,
                     world=base.body_part_grp,
                     detail_limb_deformer=detailLegDef,
                     number_detail_ctrl=numLegDtlCtrl,
                     parallel_axis='y',
                     tip_pos='-',
                     prefix_upper_limb_detail=prefixUpperLeg + Dtl,
                     prefix_middle_limb_detail=prefixLowerLeg + Dtl,
                     size=scale
                     )

    print '50% | leg right is done!'

# ======================================================================================================================
#                                                   LEFT FOOT PARAMETERS
# ======================================================================================================================
    footLFT = fm.Foot(foot=footLeft,
                      prefix=prefixFoot,
                      upper_limb_jnt=sj.upLeg_LFT,
                      ball_fk_jnt=sFk.ball_LFT,
                      ball_ik_jnt=sIk.ball_LFT,
                      toe_ik_jnt=sIk.toe_LFT,
                      ball_jnt=sj.ball_LFT,
                      heel_jnt=sj.heel_LFT,
                      lower_limb_jnt=sj.ankle_LFT,
                      in_tilt_jnt=sj.footIn_LFT,
                      out_tilt_jnt=sj.footOut_LFT,
                      prefix_ball_fk=prefixBall + Fk,
                      prefix_toe_ik=prefixToe + Ik,
                      lower_gimbal_fk_ctrl=legLFT.lower_limb_fk_gimbal,
                      lower_limb_ik_hdl=legLFT.lower_limb_ik_hdl,
                      end_limb_ik_hdl=legLFT.end_limb_ik_hdl,
                      controller_FkIk_limb_setup=legLFT.FkIk_limb_setup_controller,
                      controller_lower_limb_ik=legLFT.lower_limb_ik_control,
                      position_soft_jnt=legLFT.pos_soft_jnt,
                      part_joint_grp_module=legLFT.part_joint_grp,
                      side=sideLFT,
                      scale=scale)

# ======================================================================================================================
#                                                   RIGHT FOOT PARAMETERS
# ======================================================================================================================
    footRGT = fm.Foot(foot=footRight,
                      prefix=prefixFoot,
                      upper_limb_jnt=sj.upLeg_RGT,
                      ball_fk_jnt=sFk.ball_RGT,
                      ball_ik_jnt=sIk.ball_RGT,
                      toe_ik_jnt=sIk.toe_RGT,
                      ball_jnt=sj.ball_RGT,
                      heel_jnt=sj.heel_RGT,
                      lower_limb_jnt=sj.ankle_RGT,
                      in_tilt_jnt=sj.footIn_RGT,
                      out_tilt_jnt=sj.footOut_RGT,
                      prefix_ball_fk=prefixBall + Fk,
                      prefix_toe_ik=prefixToe + Ik,
                      lower_gimbal_fk_ctrl=legRGT.lower_limb_fk_gimbal,
                      lower_limb_ik_hdl=legRGT.lower_limb_ik_hdl,
                      end_limb_ik_hdl=legRGT.end_limb_ik_hdl,
                      controller_FkIk_limb_setup=legRGT.FkIk_limb_setup_controller,
                      controller_lower_limb_ik=legRGT.lower_limb_ik_control,
                      position_soft_jnt=legRGT.pos_soft_jnt,
                      part_joint_grp_module=legRGT.part_joint_grp,
                      side=sideRGT,
                      scale=scale)

# ======================================================================================================================
#                                                   SOFT IK LEG CONDITION
# ======================================================================================================================
    # leftLegSoftIk
    if footLeft:
        runSoftIkJoint(prefix=prefixLeg, side=sideLFT, lowerLimbIkGimbal=legLFT.lower_limb_ik_gimbal,
                       footReverseJointOrPosSoftJnt=footLFT.foot_reverse_joint,
                       posLowerLimbJnt=legLFT.pos_lower_limb_jnt, lowerLimbIkControl=legLFT.lower_limb_ik_control)
    else:
        runSoftIkJoint(prefix=prefixLeg, side=sideLFT, lowerLimbIkGimbal=legLFT.lower_limb_ik_gimbal,
                       footReverseJointOrPosSoftJnt=legLFT.pos_soft_jnt,
                       posLowerLimbJnt=legLFT.pos_lower_limb_jnt, lowerLimbIkControl=legLFT.lower_limb_ik_control)
    # rightLegSoftIk
    if footRight:
        runSoftIkJoint(prefix=prefixLeg, side=sideRGT, lowerLimbIkGimbal=legRGT.lower_limb_ik_gimbal,
                       footReverseJointOrPosSoftJnt=footRGT.foot_reverse_joint,
                       posLowerLimbJnt=legRGT.pos_lower_limb_jnt, lowerLimbIkControl=legRGT.lower_limb_ik_control)
    else:
        runSoftIkJoint(prefix=prefixLeg, side=sideRGT, lowerLimbIkGimbal=legRGT.lower_limb_ik_gimbal,
                       footReverseJointOrPosSoftJnt=legRGT.pos_soft_jnt,
                       posLowerLimbJnt=legRGT.pos_lower_limb_jnt, lowerLimbIkControl=legRGT.lower_limb_ik_control)

# ======================================================================================================================
#                                           ADDITIONAL JOINT LEFT ARM PARAMETERS
# ======================================================================================================================
    if armLeft:
        # SOFT IK
        runSoftIkJoint(prefix=prefixArm, side=sideLFT, lowerLimbIkGimbal=armLFT.lower_limb_ik_gimbal,
                       footReverseJointOrPosSoftJnt=armLFT.pos_soft_jnt,
                       posLowerLimbJnt=armLFT.pos_lower_limb_jnt,
                       lowerLimbIkControl=armLFT.lower_limb_ik_control)
        # # CLAVICLE
        # addJointClavLFT = aj.Build(addJoint=clavicleShapeJoint,
        #                                fkIkSetup=armLFT.fkIkLimbSetupController,
        #                                controllerShapeName=prefixClav,
        #                                jointDriverMatrix=sj.clavLFT,
        #                                jointAddTarget=sDtlJnt.clavLFT,
        #                                jointDriverInverseMatrix=sj.spineList[3],
        #                                pointGrpDriver=sj.clavLFT,
        #                                prefix=prefixClav,
        #                                prefixLimb=prefixArm,
        #                                side=sideLFT,
        #                                skinGrp=module.skinGrp,
        #                                rotation='Z',
        #                                translateOne='X',
        #                                translateTwo='Y',
        #                                rotationOnePos=-1,
        #                                rotationTwoPos=1,
        #                                rotationOneNeg=1,
        #                                rotationTwoNeg=0,
        #                                offsetTranslate=-1.006,
        #                                scaleObjectOne=sj.clavLFT,
        #                                scaleObjectTwo=None,
        #                                )

        # UPPERARM
        aj.Build(add_joint=upperArmShapeJoint, fk_ik_setup=armLFT.FkIk_limb_setup_controller,
                 controller_expand_name=prefixUpperArm,
                 joint_driver_matrix=sDtlJnt.upArm_LFT,
                 joint_add_target=ss.upArm_LFT,
                 joint_driver_inverse_matrix=sj.clav_LFT,
                 point_grp_driver=sDtlJnt.upArm_LFT,
                 prefix=prefixUpperArm,
                 prefixLimb=prefixArm,
                 side=sideLFT,
                 joint_grp=base.additional_grp,
                 rotation='Z',
                 translateOne='X',
                 translateTwo='Y',
                 rotationOnePos=-1,
                 rotationTwoPos=1,
                 rotationOneNeg=1,
                 rotationTwoNeg=0,
                 offsetTranslate=-1.006,
                 scaleObjectOne=sj.clav_LFT,
                 scaleObjectTwo=armLFT.set_grp_follicle_upper_limb[0]
                 )

        # ELBOW
        aj.Build(add_joint=elbowShapeJoint,
                 fk_ik_setup=armLFT.FkIk_limb_setup_controller,
                 controller_expand_name=prefixElbow,
                 joint_driver_matrix=sj.forearm_LFT,
                 joint_add_target=ss.forearm_LFT,
                 joint_driver_inverse_matrix=sj.upArm_LFT,
                 point_grp_driver=armLFT.ctrl_combine_detail,
                 prefix=prefixForearm,
                 prefixLimb=prefixArm,
                 side=sideLFT,
                 joint_grp=base.additional_grp,
                 rotation='X',
                 translateOne='Y',
                 translateTwo='Z',
                 rotationOnePos=-1,
                 rotationTwoPos=-1,
                 rotationOneNeg=-1,
                 rotationTwoNeg=1,
                 offsetTranslate=-1.006,
                 scaleObjectOne=armLFT.set_grp_follicle_upper_limb[-1],
                 scaleObjectTwo=armLFT.set_grp_follicle_middle_limb[0],
                 )

        # WRIST
        aj.Build(add_joint=wristShapeJoint,
                 fk_ik_setup=armLFT.FkIk_limb_setup_controller,
                 controller_expand_name=prefixWrist,
                 joint_driver_matrix=sj.wrist_LFT,
                 joint_add_target=ss.wrist_LFT,
                 joint_driver_inverse_matrix=sj.forearm_LFT,
                 point_grp_driver=sj.wrist_LFT,
                 prefix=prefixWrist,
                 prefixLimb=prefixArm,
                 side=sideLFT,
                 joint_grp=base.additional_grp,
                 rotation='Z',
                 translateOne='Y',
                 translateTwo='X',
                 rotationOnePos=-1,
                 rotationTwoPos=-1,
                 rotationOneNeg=1,
                 rotationTwoNeg=1,
                 offsetTranslate=-1.006,
                 scaleObjectOne=armLFT.set_grp_follicle_middle_limb[-1],
                 scaleObjectTwo=sj.wrist_LFT,
                 )

    print '55% | additional arm left is done!'
# ======================================================================================================================
#                                           ADDITIONAL JOINT RIGHT ARM PARAMETERS
# ======================================================================================================================
    if armRight:
        # SOFT IK
        armRGTSoftIk = runSoftIkJoint(prefix=prefixArm, side=sideRGT, lowerLimbIkGimbal=armRGT.lower_limb_ik_gimbal,
                                      footReverseJointOrPosSoftJnt=armRGT.pos_soft_jnt,
                                      posLowerLimbJnt=armRGT.pos_lower_limb_jnt,
                                      lowerLimbIkControl=armRGT.lower_limb_ik_control)
        # UPPERARM
        aj.Build(add_joint=upperArmShapeJoint,
                 fk_ik_setup=armRGT.FkIk_limb_setup_controller,
                 controller_expand_name=prefixUpperArm,
                 joint_driver_matrix=sDtlJnt.upArm_RGT,
                 joint_add_target=ss.upArm_RGT,
                 joint_driver_inverse_matrix=sj.clav_RGT,
                 point_grp_driver=sDtlJnt.upArm_RGT,
                 prefix=prefixUpperArm,
                 prefixLimb=prefixArm,
                 side=sideRGT,
                 joint_grp=base.additional_grp,
                 rotation='Z',
                 translateOne='X',
                 translateTwo='Y',
                 rotationOnePos=-1,
                 rotationTwoPos=1,
                 rotationOneNeg=1,
                 rotationTwoNeg=0,
                 offsetTranslate=-1.006,
                 scaleObjectOne=sj.clav_RGT,
                 scaleObjectTwo=armRGT.set_grp_follicle_upper_limb[0]
                 )
        # ELBOW
        aj.Build(add_joint=elbowShapeJoint,
                 fk_ik_setup=armRGT.FkIk_limb_setup_controller,
                 controller_expand_name=prefixElbow,
                 joint_driver_matrix=sj.forearm_RGT,
                 joint_add_target=ss.forearm_RGT,
                 joint_driver_inverse_matrix=sj.upArm_RGT,
                 point_grp_driver=armRGT.ctrl_combine_detail,
                 prefix=prefixForearm,
                 prefixLimb=prefixArm,
                 side=sideRGT,
                 joint_grp=base.additional_grp,
                 rotation='X',
                 translateOne='Y',
                 translateTwo='Z',
                 rotationOnePos=-1,
                 rotationTwoPos=-1,
                 rotationOneNeg=-1,
                 rotationTwoNeg=1,
                 offsetTranslate=-1.006,
                 scaleObjectOne=armRGT.set_grp_follicle_upper_limb[-1],
                 scaleObjectTwo=armRGT.set_grp_follicle_middle_limb[0],
                 )

        # WRIST
        aj.Build(add_joint=wristShapeJoint,
                 fk_ik_setup=armRGT.FkIk_limb_setup_controller,
                 controller_expand_name=prefixWrist,
                 joint_driver_matrix=sj.wrist_RGT,
                 joint_add_target=ss.wrist_RGT,
                 joint_driver_inverse_matrix=sj.forearm_RGT,
                 point_grp_driver=sj.wrist_RGT,
                 prefix=prefixWrist,
                 prefixLimb=prefixArm,
                 side=sideRGT,
                 joint_grp=base.additional_grp,
                 rotation='Z',
                 translateOne='Y',
                 translateTwo='X',
                 rotationOnePos=-1,
                 rotationTwoPos=-1,
                 rotationOneNeg=1,
                 rotationTwoNeg=1,
                 offsetTranslate=-1.006,
                 scaleObjectOne=armRGT.set_grp_follicle_middle_limb[-1],
                 scaleObjectTwo=sj.wrist_RGT
                 )
# ======================================================================================================================
#                                                   UNUSED JOINT REMOVE
# ======================================================================================================================
    print '60% | additional arm right is done!'
    # delete unused bones
    # mc.delete(sFk.elbowIkLFT, sFk.elbowIkRGT)
    # mc.delete(sIk.elbowIkLFT, sIk.elbowIkRGT)
    # mc.delete(sj.elbowIkLFT, sj.elbowIkRGT)
    mc.delete(sFk.thumb1_LFT, sFk.thumb1_RGT)
    mc.delete(sIk.thumb1_LFT, sIk.thumb1_RGT)
    mc.delete(sFk.index1_LFT, sFk.index1_RGT)
    mc.delete(sIk.index1_LFT, sIk.index1_RGT)
    mc.delete(sFk.middle1_LFT, sFk.middle1_RGT)
    mc.delete(sIk.middle1_LFT, sIk.middle1_RGT)
    mc.delete(sFk.ring1_LFT, sFk.ring1_RGT)
    mc.delete(sIk.ring1_LFT, sIk.ring1_RGT)
    mc.delete(sFk.pinky1_LFT, sFk.pinky1_RGT)
    mc.delete(sIk.pinky1_LFT, sIk.pinky1_RGT)
    mc.delete(sFk.palm_LFT, sFk.palm_RGT)
    mc.delete(sIk.palm_LFT, sIk.palm_RGT)
    mc.delete(ss.palm_LFT, ss.palm_RGT)
    mc.delete(ss.hand_LFT, ss.hand_RGT)
    mc.delete(ss.thumb1_LFT, ss.thumb1_RGT)
    mc.delete(ss.heel_LFT, ss.heel_RGT)
    mc.delete(ss.footIn_LFT, ss.footIn_RGT)
    mc.delete(ss.footOut_LFT, ss.footOut_RGT)
    mc.delete(sj.heel_LFT, sj.heel_RGT)
    mc.delete(sj.footIn_LFT, sj.footIn_RGT)
    mc.delete(sj.footOut_LFT, sj.footOut_RGT)
    mc.delete(sFk.heel_LFT, sFk.heel_RGT)
    mc.delete(sFk.footIn_LFT, sFk.footIn_RGT)
    mc.delete(sFk.footOut_LFT, sFk.footOut_RGT)
    mc.delete(sIk.heel_LFT, sIk.heel_RGT)
    mc.delete(sIk.footIn_LFT, sIk.footIn_RGT)
    mc.delete(sIk.footOut_LFT, sIk.footOut_RGT)
    mc.delete(sDtlBind.ankle_LFT, sDtlBind.ankle_RGT)
    mc.delete(sDtlJnt.ankle_LFT, sDtlJnt.ankle_RGT)

    # mc.delete(sDtlJnt.elbowIkLFT, sDtlJnt.elbowIkRGT)
    # mc.delete(sDtlBind.elbowIkLFT, sDtlBind.elbowIkRGT)
    mc.delete(sDtlJnt.wrist_LFT, sDtlJnt.wrist_RGT)
    mc.delete(sDtlBind.wrist_LFT, sDtlBind.wrist_RGT)
    mc.delete(ss.root)
    mc.delete(sIk.root)
    mc.delete(sFk.root)
    mc.delete(sDtlBind.root)
    mc.delete(sDtlJnt.root)


    print '65% | clean up!'
    print '70%'
    print '75%'
    print '80%'
    print '85%'
    print '90%'
    print '95%'
    print '100%'
# ======================================================================================================================
#                                                  CTRL BIPED MODULE FUNCTION
# ======================================================================================================================
def runSoftIkJoint(prefix, side, lowerLimbIkGimbal, footReverseJointOrPosSoftJnt, posLowerLimbJnt,
                   lowerLimbIkControl):
        mc.orientConstraint(lowerLimbIkGimbal, footReverseJointOrPosSoftJnt, mo=1)

        # constraint the soft jnt from gimbal control and lower limb distance
        stretchIkPointCons = mc.pointConstraint(lowerLimbIkGimbal, posLowerLimbJnt,
                                                footReverseJointOrPosSoftJnt, mo=1)
        # set the key driver key for stretch setup
        stretchIkRev = mc.shadingNode('reverse', asUtility=1, n='%s%s%s_rev' % (prefix, 'StretchIk', side))

        # connect the attribute stretch from the limb controller
        mc.connectAttr(lowerLimbIkControl + '.stretch', stretchIkRev + '.inputX')
        mc.connectAttr(stretchIkRev + '.outputX', stretchIkPointCons[0] + ('.%sW1' % posLowerLimbJnt))
        mc.connectAttr(lowerLimbIkControl + '.stretch',
                       stretchIkPointCons[0] + ('.%sW0' % lowerLimbIkGimbal))