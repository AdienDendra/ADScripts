import maya.cmds as mc
from rigging.tools import AD_utils as au
from rigLib.base import general_module as gm, template_module as sd
from rigLib.base.body import spine_module as sm, foot_module as fm, clavicle_module as cm, hand_module as hm, \
    limb_module as lm
from rigLib.rig.body import expand_skeleton as aj

from rigLib.utils import template_skeleton as dt

reload(au)
reload(gm)
reload(sm)
reload(cm)
reload(aj)
reload(lm)
reload(hm)
reload(fm)
reload(dt)
reload(sd)


Fk = 'Fk'
Ik = 'Ik'
Dtl = 'Dtl'

# FINGER POSITION
BaseF = 'Base'
UpF = 'Up'
MidF = 'Mid'
LowF = 'Low'
# load Plug-ins
matrixNode = mc.pluginInfo('matrixNodes.mll', query=True, loaded=True)
quatNode = mc.pluginInfo('quatNodes.mll', query=True, loaded=True)

if not matrixNode:
    mc.loadPlugin( 'matrixNodes.mll' )

if not quatNode:
    mc.loadPlugin( 'quatNodes.mll' )

# build Spine
prefixSpine = 'spine'
prefixSpineSetup = 'spineSetup'

# build Clavicle
prefixClav = 'clavicle'

# build Arm
prefixArm = 'arm'
prefixUpperArm = 'upperArm'
prefixForearm = 'forearm'
prefixWrist = 'wrist'
prefixElbow = 'elbow'
prefixHand = 'hand'
prefixArmSetup = 'armSetup'
prefixFingerSetup = 'fingerSetup'

# build Leg`
prefixLeg = 'leg'
prefixUpperLeg = 'upperLeg'
prefixLowerLeg = 'lowerLeg'
prefixAnkle = 'ankle'
prefixKnee  = 'knee'
prefixBall = 'ball'
prefixToe = 'toe'
prefixLegSetup = 'legSetup'
prefixFoot = 'foot'

# build arm finger
prefixThumb = 'thumb'
prefixIndex = 'index'
prefixMiddle = 'middle'
prefixRing ='ring'
prefixPinky = 'pinky'
prefixPalm ='palm'

leftSide = 'LFT'
rightSide = 'RGT'

class BuildRig:
    # def __init__(self):
    #     self.armLFTFkIkLimbSetupController =None
    #     self.armLFTCtrlFollUpperLimb = None
    #     self.ssUpArmLFT = None
    #     self.sjClavLFT = None
    #     self.sjForearmLFT = None
    #     self.ssForearmLFT = None
    #     self.sjUpArmLFT = None
    #     self.sjWristLFT = None
    #     self.ssWristLFT = None
    #
    #     self.armRGTFkIkLimbSetupController = None
    #     self.armRGTCtrlFollUpperLimb = None
    #     self.ssUpArmRGT = None
    #     self.sjClavRGT = None
    #     self.sjForearmRGT = None
    #     self.ssForearmRGT = None
    #     self.sjUpArmRGT = None
    #     self.sjWristRGT = None
    #     self.ssWristRGT = None

    def baseRig(self,
                clavicleLeft=True,
                clavicleRight=True,
                armLeft=True,
                armRight=True,
                handLeft=True,
                handRight=True,
                legLeft=True,
                legRight=True,
                footRight=True,
                footLeft=True,
                detailSpineDef=True,
                detailArmDef=True,
                detailLegDef=True,
                thumbArm=True,
                indexArm=True,
                middleArm=True,
                ringArm=True,
                pinkyArm=True,
                prefixSpine=prefixSpine,
                prefixSpineSetup=prefixSpineSetup,
                prefixUpperArm=prefixUpperArm,
                prefixForearm=prefixForearm,
                prefixClav=prefixClav,
                prefixArm=prefixArm,
                prefixWrist=prefixWrist,
                prefixElbow=prefixElbow,
                prefixHand=prefixHand,
                prefixArmSetup=prefixArmSetup,
                prefixUpperLeg=prefixUpperLeg,
                prefixLowerLeg=prefixLowerLeg,
                prefixLeg=prefixLeg,
                prefixAnkle=prefixAnkle,
                prefixKnee=prefixKnee,
                prefixBall=prefixBall,
                prefixToe=prefixToe,
                prefixFoot=prefixFoot,
                prefixLegSetup=prefixLegSetup,
                prefixThumb=prefixThumb,
                prefixIndex=prefixIndex,
                prefixMiddle=prefixMiddle,
                prefixRing=prefixRing,
                prefixFingerSetup=prefixFingerSetup,
                prefixPalm=prefixPalm,
                prefixPinky=prefixPinky,
                numArmDtlCtrl=3,
                numLegDtlCtrl=3,
                scale=1.0,
                sideLFT=leftSide,
                sideRGT=rightSide):

        # CREATE BASE RIG
        self.base = gm.Base(scale=scale)
        self.baseSkinGrp = self.base.additional_grp

    # ======================================================================================================================
    #                                              DUPLICATE JOINTS AS DRIVER
    # ======================================================================================================================
        self.sj = sd.listSkeletonDuplicate(objDuplicate='rootTmp_jnt',
                                           value_prefix='Driver',
                                           key_prefix='Ori',
                                           suffix='jnt'
                                           )

        self.ss = sd.listSkeletonDuplicate(objDuplicate='rootTmp_jnt',
                                           value_prefix='DriverScale',
                                           key_prefix='Scl',
                                           suffix='jnt'
                                           )

        self.sFk = sd.listSkeletonDuplicate(objDuplicate='rootTmp_jnt',
                                            value_prefix='FkDriver',
                                            key_prefix='Fk',
                                            suffix='jnt'
                                            )

        self.sIk = sd.listSkeletonDuplicate(objDuplicate='rootTmp_jnt',
                                            value_prefix='IkDriver',
                                            key_prefix='Ik',
                                            suffix='jnt'
                                            )

        print '5%  | skeleton duplicated is done!'

    # ======================================================================================================================
    #                                                  SPINE PARAMETERS
    # ======================================================================================================================
        sm.Spine(prefix=prefixSpine,
                 prefix_spine_setup=prefixSpineSetup,
                 detail_spine_deformer=detailSpineDef,
                 base_controller=self.base,
                 size=scale,
                 spine_jnt= self.sj.spine_list,
                 pelvis_jnt= self.sj.pelvis,
                 root_jnt= self.sj.root,
                 parentJnt = self.sj.root,
                 )

        print '10% | spine is done!'

    # ======================================================================================================================
#                                                   LEFT CLAVICLE PARAMETERS
    # ======================================================================================================================
        cm.Clavicle(clavicle=clavicleLeft,
                    prefix=prefixClav,
                    side=sideLFT,
                    base_controller=self.base,
                    clavicle_jnt=self.sj.clav_LFT,
                    scale_jnt=self.ss.clav_LFT,
                    parentScaleJnt=self.sj.clav_LFT,
                    parent_jnt=self.sj.spine_list[-1],
                    size=scale
                    )

        print '15% | clavicle left is done!'

    # ======================================================================================================================
#                                                   RIGHT CLAVICLE PARAMETERS
    # ======================================================================================================================
        cm.Clavicle(clavicle=clavicleRight,
                    prefix=prefixClav,
                    side=sideRGT,
                    base_controller=self.base,
                    clavicle_jnt=self.sj.clav_RGT,
                    scale_jnt=self.ss.clav_RGT,
                    parentScaleJnt=self.sj.clav_RGT,
                    parent_jnt=self.sj.spine_list[-1],
                    size=scale
                    )

        print '20% | clavicle right is done!'

    # ======================================================================================================================
    #                                                   LEFT ARM PARAMETERS
    # ======================================================================================================================
        self.armLFT = lm.Limb(limb=armLeft,
                              arm=True,
                              prefix=prefixArm,
                              side=sideLFT,
                              base_controller=self.base,
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
                              rootJnt=self.sj.root,
                              clav_jnt=self.sj.clav_LFT,
                              upper_limb_jnt=self.sj.upArm_LFT,
                              middle_limb_jnt=self.sj.forearm_LFT,
                              lower_limb_jnt=self.sj.wrist_LFT,
                              end_limb_jnt=None,
                              lower_limb_scale_jnt=None,
                              end_limb_scale_jnt=None,
                              upper_limb_fk_jnt=self.sFk.upArm_LFT,
                              middle_limb_fk_jnt=self.sFk.forearm_LFT,
                              lower_limb_fk_jnt=self.sFk.wrist_LFT,
                              upper_limb_ik_jnt=self.sIk.upArm_LFT,
                              middle_limb_ik_jnt=self.sIk.forearm_LFT,
                              lower_limb_ik_jnt=self.sIk.wrist_LFT,
                              end_limb_ik_jnt=self.sIk.hand_LFT,
                              world=self.base.body_part_grp,
                              detail_limb_deformer=detailArmDef,
                              number_detail_ctrl=numArmDtlCtrl,
                              parallel_axis='x',
                              tip_pos='+',
                              prefix_upper_limb_detail=prefixUpperArm + Dtl,
                              prefix_middle_limb_detail=prefixForearm + Dtl,
                              size=scale
                              )

        self.armLFTFkIkLimbSetupController = self.armLFT.FkIk_limb_setup_controller
        self.armLFTCtrlFollUpperLimb = self.armLFT.ctrl_follicle_upper_limb
        self.armLFTCtrlFollMiddleLimb = self.armLFT.ctrl_follicle_middle_limb

        self.ssUpArmLFT = self.ss.upArm_LFT
        self.sjClavLFT = self.sj.clav_LFT
        self.sjForearmLFT = self.sj.forearm_LFT
        self.ssForearmLFT = self.ss.forearm_LFT
        self.sjUpArmLFT =self.sj.upArm_LFT
        self.sjWristLFT = self.sj.wrist_LFT
        self.ssWristLFT = self.ss.wrist_LFT


        print '25% | arm left is done!'

    # ======================================================================================================================
    #                                                   RIGHT ARM PARAMETERS
    # ======================================================================================================================
        self.armRGT = lm.Limb(limb=armRight,
                              arm=True,
                              prefix=prefixArm,
                              side=sideRGT,
                              base_controller=self.base,
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
                              rootJnt=self.sj.root,
                              clav_jnt=self.sj.clav_RGT,
                              upper_limb_jnt=self.sj.upArm_RGT,
                              middle_limb_jnt=self.sj.forearm_RGT,
                              lower_limb_jnt=self.sj.wrist_RGT,
                              end_limb_jnt=None,
                              lower_limb_scale_jnt=None,
                              end_limb_scale_jnt=None,
                              upper_limb_fk_jnt=self.sFk.upArm_RGT,
                              middle_limb_fk_jnt=self.sFk.forearm_RGT,
                              lower_limb_fk_jnt=self.sFk.wrist_RGT,
                              upper_limb_ik_jnt=self.sIk.upArm_RGT,
                              middle_limb_ik_jnt=self.sIk.forearm_RGT,
                              lower_limb_ik_jnt=self.sIk.wrist_RGT,
                              end_limb_ik_jnt=self.sIk.hand_RGT,
                              detail_limb_deformer=detailArmDef,
                              number_detail_ctrl= numArmDtlCtrl,
                              parallel_axis='x',
                              tip_pos='-',
                              world=self.base.body_part_grp,
                              prefix_upper_limb_detail=prefixUpperArm + Dtl,
                              prefix_middle_limb_detail=prefixForearm + Dtl,
                              size=scale
                              )
        self.armRGTFkIkLimbSetupController = self.armRGT.FkIk_limb_setup_controller
        self.armRGTCtrlFollUpperLimb = self.armRGT.ctrl_follicle_upper_limb
        self.armRGTCtrlFollMiddleLimb = self.armRGT.ctrl_follicle_middle_limb

        self.ssUpArmRGT = self.ss.upArm_RGT
        self.sjClavRGT = self.sj.clav_RGT
        self.sjForearmRGT = self.sj.forearm_RGT
        self.ssForearmRGT = self.ss.forearm_RGT
        self.sjUpArmRGT = self.sj.upArm_RGT
        self.sjWristRGT = self.sj.wrist_RGT
        self.ssWristRGT = self.ss.wrist_RGT

        print '30% | arm right is done!'

    # ======================================================================================================================
    #                                                   LEFT HAND PARAMETERS
    # ======================================================================================================================
        hm.Hand(parent=armLeft,
                arm_object=self.armLFT,
                hand=handLeft,
                thumb=thumbArm,
                index=indexArm,
                middle=middleArm,
                ring=ringArm,
                pinky=pinkyArm,
                thumb_finger_base=self.sj.thumb1_LFT,
                thumb_finger_up=self.sj.thumb2_LFT,
                thumb_finger_mid=self.sj.thumb3_LFT,
                prefix_thumb_finger_base=prefixThumb + BaseF,
                prefix_thumb_finger_up=prefixThumb + UpF,
                prefix_thumb_finger_mid=prefixThumb + MidF,
                index_finger_base=self.sj.index1_LFT,
                index_finger_up=self.sj.index2_LFT,
                index_finger_mid=self.sj.index3_LFT,
                index_finger_low=self.sj.index4_LFT,
                prefix_index_finger_base=prefixIndex + BaseF,
                prefix_index_finger_up=prefixIndex + UpF,
                prefix_index_finger_mid=prefixIndex + MidF,
                prefix_index_finger_low=prefixIndex + LowF,
                middle_finger_base=self.sj.middle1_LFT,
                middle_finger_up=self.sj.middle2LFT,
                middle_finger_mid=self.sj.middle3_LFT,
                middle_finger_low=self.sj.middle4_LFT,
                prefix_middle_finger_base=prefixMiddle + BaseF,
                prefix_middle_finger_up=prefixMiddle + UpF,
                prefix_middle_finger_mid=prefixMiddle + MidF,
                prefix_middle_finger_low=prefixMiddle + LowF,
                ring_finger_base=self.sj.ring1_LFT,
                ring_finger_up=self.sj.ring2_LFT,
                ring_finger_mid=self.sj.ring3_LFT,
                ring_finger_low=self.sj.ring4_LFT,
                prefix_ring_finger_base=prefixRing + BaseF,
                prefix_ring_finger_up=prefixRing + UpF,
                prefix_ring_finger_mid=prefixRing + MidF,
                prefix_ring_finger_low=prefixRing + LowF,
                pinky_finger_base=self.sj.pinky1_LFT,
                pinky_finger_up=self.sj.pinky2_LFT,
                pinky_finger_mid=self.sj.pinky3_LFT,
                pinky_finger_low=self.sj.pinky4_LFT,
                prefix_pinky_finger_base=prefixPinky + BaseF,
                prefix_pinky_finger_up=prefixPinky + UpF,
                prefix_pinky_finger_mid=prefixPinky + MidF,
                prefix_pinky_finger_low=prefixPinky + LowF,
                prefix_finger_setup=prefixFingerSetup,
                prefix_palm=prefixPalm,
                wrist_jnt=self.sj.wrist_LFT,
                hand_jnt=self.sj.hand_LFT,
                palm_jnt=self.sj.palm_LFT,
                side=sideLFT,
                size=scale)

        print '35% | hand left is done!'

    # ======================================================================================================================
    #                                                   RIGHT HAND PARAMETERS
    # ======================================================================================================================
        hm.Hand(parent=armRight,
                arm_object=self.armRGT,
                hand=handRight,
                thumb=thumbArm,
                index=indexArm,
                middle=middleArm,
                ring=ringArm,
                pinky=pinkyArm,
                thumb_finger_base= self.sj.thumb1_RGT,
                thumb_finger_up= self.sj.thumb2_RGT,
                thumb_finger_mid= self.sj.thumb3_RGT,
                prefix_thumb_finger_base=prefixThumb + BaseF,
                prefix_thumb_finger_up=prefixThumb + UpF,
                prefix_thumb_finger_mid=prefixThumb + MidF,
                index_finger_base=self.sj.index1_RGT,
                index_finger_up=self.sj.index2_RGT,
                index_finger_mid=self.sj.index3_RGT,
                index_finger_low=self.sj.index4_RGT,
                prefix_index_finger_base=prefixIndex + BaseF,
                prefix_index_finger_up=prefixIndex + UpF,
                prefix_index_finger_mid=prefixIndex + MidF,
                prefix_index_finger_low=prefixIndex + LowF,
                middle_finger_base=self.sj.middle1_RGT,
                middle_finger_up=self.sj.middle2_RGT,
                middle_finger_mid=self.sj.middle3_RGT,
                middle_finger_low=self.sj.middle4_RGT,
                prefix_middle_finger_base=prefixMiddle + BaseF,
                prefix_middle_finger_up=prefixMiddle + UpF,
                prefix_middle_finger_mid=prefixMiddle + MidF,
                prefix_middle_finger_low=prefixMiddle + LowF,
                ring_finger_base=self.sj.ring1_RGT,
                ring_finger_up=self.sj.ring2_RGT,
                ring_finger_mid=self.sj.ring3_RGT,
                ring_finger_low=self.sj.ring4_RGT,
                prefix_ring_finger_base=prefixRing + BaseF,
                prefix_ring_finger_up=prefixRing + UpF,
                prefix_ring_finger_mid=prefixRing + MidF,
                prefix_ring_finger_low=prefixRing + LowF,
                pinky_finger_base=self.sj.pinky1_RGT,
                pinky_finger_up=self.sj.pinky2_RGT,
                pinky_finger_mid=self.sj.pinky3_RGT,
                pinky_finger_low=self.sj.pinky4_RGT,
                prefix_pinky_finger_base=prefixPinky + BaseF,
                prefix_pinky_finger_up=prefixPinky + UpF,
                prefix_pinky_finger_mid=prefixPinky + MidF,
                prefix_pinky_finger_low=prefixPinky + LowF,
                prefix_finger_setup= prefixFingerSetup,
                prefix_palm=prefixPalm,
                wrist_jnt=self.sj.wrist_RGT,
                hand_jnt=self.sj.hand_RGT,
                palm_jnt=self.sj.palm_RGT,
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
                         base_controller=self.base,
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
                         pelvisJnt=self.sj.pelvis,
                         rootJnt=None,
                         clav_jnt=None,
                         upper_limb_jnt=self.sj.upLeg_LFT,
                         middle_limb_jnt=self.sj.lowLeg_LFT,
                         lower_limb_jnt=self.sj.ankle_LFT,
                         end_limb_jnt=self.sj.ball_LFT,
                         lower_limb_scale_jnt=self.ss.ankle_LFT,
                         end_limb_scale_jnt=self.ss.ball_LFT,
                         upper_limb_fk_jnt=self.sFk.upLeg_LFT,
                         middle_limb_fk_jnt=self.sFk.lowLeg_LFT,
                         lower_limb_fk_jnt=self.sFk.ankle_LFT,
                         upper_limb_ik_jnt=self.sIk.upLeg_LFT,
                         middle_limb_ik_jnt=self.sIk.lowLeg_LFT,
                         lower_limb_ik_jnt=self.sIk.ankle_LFT,
                         end_limb_ik_jnt=self.sIk.ball_LFT,
                         world=self.base.body_part_grp,
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
                         base_controller=self.base,
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
                         pelvisJnt=self.sj.pelvis,
                         rootJnt=None,
                         clav_jnt=None,
                         upper_limb_jnt=self.sj.upLeg_RGT,
                         middle_limb_jnt=self.sj.lowLeg_RGT,
                         lower_limb_jnt=self.sj.ankle_RGT,
                         end_limb_jnt=self.sj.ball_RGT,
                         lower_limb_scale_jnt=self.ss.ankle_RGT,
                         end_limb_scale_jnt=self.ss.ball_RGT,
                         upper_limb_fk_jnt=self.sFk.upLeg_RGT,
                         middle_limb_fk_jnt=self.sFk.lowLeg_RGT,
                         lower_limb_fk_jnt=self.sFk.ankle_RGT,
                         upper_limb_ik_jnt=self.sIk.upLeg_RGT,
                         middle_limb_ik_jnt=self.sIk.lowLeg_RGT,
                         lower_limb_ik_jnt=self.sIk.ankle_RGT,
                         end_limb_ik_jnt=self.sIk.ball_RGT,
                         world=self.base.body_part_grp,
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
                          upper_limb_jnt=self.sj.upLeg_LFT,
                          ball_fk_jnt=self.sFk.ball_LFT,
                          ball_ik_jnt=self.sIk.ball_LFT,
                          toe_ik_jnt=self.sIk.toe_LFT,
                          ball_jnt=self.sj.ball_LFT,
                          heel_jnt=self.sj.heel_LFT,
                          lower_limb_jnt=self.sj.ankle_LFT,
                          in_tilt_jnt=self.sj.footIn_LFT,
                          out_tilt_jnt=self.sj.footOut_LFT,
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
    #                                                  RIGHT FOOT PARAMETERS
    # ======================================================================================================================
        footRGT = fm.Foot(foot=footRight,
                          prefix=prefixFoot,
                          upper_limb_jnt=self.sj.upLeg_RGT,
                          ball_fk_jnt=self.sFk.ball_RGT,
                          ball_ik_jnt=self.sIk.ball_RGT,
                          toe_ik_jnt=self.sIk.toe_RGT,
                          ball_jnt=self.sj.ball_RGT,
                          heel_jnt=self.sj.heel_RGT,
                          lower_limb_jnt=self.sj.ankle_RGT,
                          in_tilt_jnt=self.sj.footIn_RGT,
                          out_tilt_jnt=self.sj.footOut_RGT,
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
    #                                                   SOFT IK ARM AND LEG
    # ======================================================================================================================
        # leftArmSoftIk
        self.runSoftIkJoint(prefix=prefixArm, side=sideLFT, lowerLimbIkGimbal=self.armLFT.lower_limb_ik_gimbal,
                            footReverseJointOrPosSoftJnt=self.armLFT.pos_soft_jnt,
                            posLowerLimbJnt=self.armLFT.pos_lower_limb_jnt,
                            lowerLimbIkControl=self.armLFT.lower_limb_ik_control)
        # rightArmSoftIk
        self.runSoftIkJoint(prefix=prefixArm, side=sideRGT, lowerLimbIkGimbal=self.armRGT.lower_limb_ik_gimbal,
                            footReverseJointOrPosSoftJnt=self.armRGT.pos_soft_jnt,
                            posLowerLimbJnt=self.armRGT.pos_lower_limb_jnt,
                            lowerLimbIkControl=self.armRGT.lower_limb_ik_control)

        # leftLegSoftIk
        if footLeft:
            self.runSoftIkJoint(prefix=prefixLeg, side=sideLFT, lowerLimbIkGimbal=legLFT.lower_limb_ik_gimbal,
                                footReverseJointOrPosSoftJnt=footLFT.foot_reverse_joint,
                                posLowerLimbJnt=legLFT.pos_lower_limb_jnt, lowerLimbIkControl=legLFT.lower_limb_ik_control)
        else:
            self.runSoftIkJoint(prefix=prefixLeg, side=sideLFT, lowerLimbIkGimbal=legLFT.lower_limb_ik_gimbal,
                                footReverseJointOrPosSoftJnt=legLFT.pos_soft_jnt,
                                posLowerLimbJnt=legLFT.pos_lower_limb_jnt, lowerLimbIkControl=legLFT.lower_limb_ik_control)
        # rightLegSoftIk
        if footRight:
            self.runSoftIkJoint(prefix=prefixLeg, side=sideRGT, lowerLimbIkGimbal=legRGT.lower_limb_ik_gimbal,
                                footReverseJointOrPosSoftJnt=footRGT.foot_reverse_joint,
                                posLowerLimbJnt=legRGT.pos_lower_limb_jnt, lowerLimbIkControl=legRGT.lower_limb_ik_control)
        else:
            self.runSoftIkJoint(prefix=prefixLeg, side=sideRGT, lowerLimbIkGimbal=legRGT.lower_limb_ik_gimbal,
                                footReverseJointOrPosSoftJnt=legRGT.pos_soft_jnt,
                                posLowerLimbJnt=legRGT.pos_lower_limb_jnt, lowerLimbIkControl=legRGT.lower_limb_ik_control)

    # ======================================================================================================================
    #                                                   UNUSED JOINT REMOVE
    # ======================================================================================================================
        print '60% | additional arm right is done!'
        # delete unused bones
        # mc.delete(self.sFk.elbowIkLFT, self.sFk.elbowIkRGT)
        # mc.delete(self.sIk.elbowIkLFT, self.sIk.elbowIkRGT)
        # mc.delete(self.sj.elbowIkLFT, self.sj.elbowIkRGT)
        mc.delete(self.sFk.thumb1_LFT, self.sFk.thumb1_RGT)
        mc.delete(self.sIk.thumb1_LFT, self.sIk.thumb1_RGT)
        mc.delete(self.sFk.index1_LFT, self.sFk.index1_RGT)
        mc.delete(self.sIk.index1_LFT, self.sIk.index1_RGT)
        mc.delete(self.sFk.middle1_LFT, self.sFk.middle1_RGT)
        mc.delete(self.sIk.middle1_LFT, self.sIk.middle1_RGT)
        mc.delete(self.sFk.ring1_LFT, self.sFk.ring1_RGT)
        mc.delete(self.sIk.ring1_LFT, self.sIk.ring1_RGT)
        mc.delete(self.sFk.pinky1_LFT, self.sFk.pinky1_RGT)
        mc.delete(self.sIk.pinky1_LFT, self.sIk.pinky1_RGT)
        mc.delete(self.sFk.palm_LFT, self.sFk.palm_RGT)
        mc.delete(self.sIk.palm_LFT, self.sIk.palm_RGT)
        mc.delete(self.ss.palm_LFT, self.ss.palm_RGT)
        mc.delete(self.ss.hand_LFT, self.ss.hand_RGT)
        mc.delete(self.ss.thumb1_LFT, self.ss.thumb1_RGT)
        mc.delete(self.ss.heel_LFT, self.ss.heel_RGT)
        mc.delete(self.ss.footIn_LFT, self.ss.footIn_RGT)
        mc.delete(self.ss.footOut_LFT, self.ss.footOut_RGT)
        mc.delete(self.sj.heel_LFT, self.sj.heel_RGT)
        mc.delete(self.sj.footIn_LFT, self.sj.footIn_RGT)
        mc.delete(self.sj.footOut_LFT, self.sj.footOut_RGT)
        mc.delete(self.sFk.heel_LFT, self.sFk.heel_RGT)
        mc.delete(self.sFk.footIn_LFT, self.sFk.footIn_RGT)
        mc.delete(self.sFk.footOut_LFT, self.sFk.footOut_RGT)
        mc.delete(self.sIk.heel_LFT, self.sIk.heel_RGT)
        mc.delete(self.sIk.footIn_LFT, self.sIk.footIn_RGT)
        mc.delete(self.sIk.footOut_LFT, self.sIk.footOut_RGT)
        # mc.delete(sDtlBind.ankleLFT, sDtlBind.ankleRGT)
        # mc.delete(sDtlJnt.ankleLFT, sDtlJnt.ankleRGT)

        # mc.delete(sDtlJnt.elbowIkLFT, sDtlJnt.elbowIkRGT)
        # mc.delete(sDtlBind.elbowIkLFT, sDtlBind.elbowIkRGT)
        # mc.delete(sDtlJnt.wristLFT, sDtlJnt.wristRGT)
        # mc.delete(sDtlBind.wristLFT, sDtlBind.wristRGT)
        mc.delete(self.ss.root)
        mc.delete(self.sIk.root)
        mc.delete(self.sFk.root)
        # mc.delete(sDtlBind.root)
        # mc.delete(sDtlJnt.root)

        print '65% | clean up!'
        print '70%'
        print '75%'
        print '80%'
        print '85%'
        print '90%'
        print '95%'
        print '100%'

    # ======================================================================================================================
    #                                                CTRL BIPED MODULE FUNCTION
    # ======================================================================================================================
    def runSoftIkJoint(self, prefix, side, lowerLimbIkGimbal, footReverseJointOrPosSoftJnt, posLowerLimbJnt,
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
    # ======================================================================================================================
    #                                                 ADDITIONAL JOINT FUNCTION
    # ======================================================================================================================
# class BuildAddJoint:
    def additionalJoint(self,
                        armLeft=True,
                        armRight=True,
                        clavicleShapeJoint=False,
                        upperArmShapeJoint=True,
                        elbowShapeJoint=False,
                        wristShapeJoint=False,
                        prefixUpperArm=prefixUpperArm,
                        prefixForearm=prefixForearm,
                        prefixWrist=prefixWrist,
                        prefixElbow=prefixElbow,
                        sideLFT = leftSide,
                        sideRGT = rightSide
                        ):

    # ======================================================================================================================
    #                                           ADDITIONAL JOINT LEFT ARM PARAMETERS
    # ======================================================================================================================
        if armLeft:
            if clavicleShapeJoint or upperArmShapeJoint or elbowShapeJoint or wristShapeJoint:
                au.add_attribute(objects=[self.armLFTFkIkLimbSetupController], long_name=['addJoint'],
                                 nice_name=[' '], at="enum",
                                 en='Add Joint', channel_box=True)
            if upperArmShapeJoint:
                self.additionalJointAtribute(self.armLFTFkIkLimbSetupController, prefixUpperArm)
            if elbowShapeJoint:
                self.additionalJointAtribute(self.armLFTFkIkLimbSetupController, prefixElbow)
            if wristShapeJoint:
                self.additionalJointAtribute(self.armLFTFkIkLimbSetupController, prefixWrist)

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
            #                                skinGrp=self.module.skinGrp,
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
            aj.Build(add_joint=upperArmShapeJoint, fk_ik_setup=self.armLFTFkIkLimbSetupController,
                     controller_expand_name=prefixUpperArm,
                     joint_driver_matrix=self.armLFTCtrlFollUpperLimb[0],
                     joint_add_target=self.ss.upArm_LFT,
                     joint_driver_inverse_matrix=self.sj.clav_LFT,
                     point_grp_driver=[self.armLFTCtrlFollUpperLimb[0]],
                     scale_driver=[self.armLFTCtrlFollUpperLimb[0]],
                     prefix=prefixUpperArm,
                     side=sideLFT,
                     joint_grp=self.baseSkinGrp,
                     rotation='Z',
                     translateOne='X',
                     translateTwo='Y',
                     rotationOnePos=-1,
                     rotationTwoPos=1,
                     rotationOneNeg=1,
                     rotationTwoNeg=0,
                     offsetTranslate=-1.006,
                     )

            # ELBOW
            aj.Build(add_joint=elbowShapeJoint,
                     fk_ik_setup=self.armLFTFkIkLimbSetupController,
                     controller_expand_name=prefixElbow,
                     joint_driver_matrix=self.sjForearmLFT,
                     joint_add_target=self.ssForearmLFT,
                     joint_driver_inverse_matrix=self.sjUpArmLFT,
                     point_grp_driver=[self.armLFTCtrlFollUpperLimb[-1], self.armLFTCtrlFollMiddleLimb[0]],
                     scale_driver=[self.armLFTCtrlFollUpperLimb[-1], self.armLFTCtrlFollMiddleLimb[0]],
                     prefix=prefixForearm,
                     side=sideLFT,
                     joint_grp=self.baseSkinGrp,
                     rotation='X',
                     translateOne='Y',
                     translateTwo='Z',
                     rotationOnePos=-1,
                     rotationTwoPos=-1,
                     rotationOneNeg=-1,
                     rotationTwoNeg=1,
                     offsetTranslate=-1.006,
                     )

            # WRIST
            aj.Build(add_joint=wristShapeJoint,
                     fk_ik_setup=self.armLFTFkIkLimbSetupController,
                     controller_expand_name=prefixWrist,
                     joint_driver_matrix=self.sjWristLFT,
                     joint_add_target=self.ssWristLFT,
                     joint_driver_inverse_matrix=self.sjForearmLFT,
                     point_grp_driver=[self.armLFTCtrlFollMiddleLimb[-1], self.sjWristLFT],
                     scale_driver=[self.armLFTCtrlFollMiddleLimb[-1], self.sjWristLFT],
                     prefix=prefixWrist,
                     side=sideLFT,
                     joint_grp=self.baseSkinGrp,
                     rotation='Z',
                     translateOne='Y',
                     translateTwo='X',
                     rotationOnePos=-1,
                     rotationTwoPos=-1,
                     rotationOneNeg=1,
                     rotationTwoNeg=1,
                     offsetTranslate=-1.006
                     )

        print '55% | additional arm left is done!'
    # ======================================================================================================================
    #                                           ADDITIONAL JOINT RIGHT ARM PARAMETERS
    # ======================================================================================================================
        if armRight:
            if clavicleShapeJoint or upperArmShapeJoint or elbowShapeJoint or wristShapeJoint:
                au.add_attribute(objects=[self.armRGTFkIkLimbSetupController], long_name=['addJoint'],
                                 nice_name=[' '], at="enum",
                                 en='Add Joint', channel_box=True)
            if upperArmShapeJoint:
                self.additionalJointAtribute(self.armRGTFkIkLimbSetupController, prefixUpperArm)
            if elbowShapeJoint:
                self.additionalJointAtribute(self.armRGTFkIkLimbSetupController, prefixElbow)
            if wristShapeJoint:
                self.additionalJointAtribute(self.armRGTFkIkLimbSetupController, prefixWrist)

            # UPPERARM
            aj.Build(add_joint=upperArmShapeJoint,
                     fk_ik_setup=self.armRGTFkIkLimbSetupController,
                     controller_expand_name=prefixUpperArm,
                     joint_driver_matrix=self.armRGTCtrlFollUpperLimb[0],
                     joint_add_target=self.ssUpArmRGT,
                     joint_driver_inverse_matrix=self.sjClavRGT,
                     point_grp_driver=[self.armRGTCtrlFollUpperLimb[0]],
                     scale_driver=[self.armRGTCtrlFollUpperLimb[0]],
                     prefix=prefixUpperArm,
                     side=sideRGT,
                     joint_grp=self.baseSkinGrp,
                     rotation='Z',
                     translateOne='X',
                     translateTwo='Y',
                     rotationOnePos=-1,
                     rotationTwoPos=1,
                     rotationOneNeg=1,
                     rotationTwoNeg=0,
                     offsetTranslate=-1.006,
                     )
            # ELBOW
            aj.Build(add_joint=elbowShapeJoint,
                     fk_ik_setup=self.armRGTFkIkLimbSetupController,
                     controller_expand_name=prefixElbow,
                     joint_driver_matrix=self.sjForearmRGT,
                     joint_add_target=self.ssForearmRGT,
                     joint_driver_inverse_matrix=self.sjUpArmRGT,
                     point_grp_driver=[self.armRGTCtrlFollUpperLimb[-1], self.armRGTCtrlFollMiddleLimb[0]],
                     scale_driver=[self.armRGTCtrlFollUpperLimb[-1], self.armRGTCtrlFollMiddleLimb[0]],
                     prefix=prefixForearm,
                     side=sideRGT,
                     joint_grp=self.baseSkinGrp,
                     rotation='X',
                     translateOne='Y',
                     translateTwo='Z',
                     rotationOnePos=-1,
                     rotationTwoPos=-1,
                     rotationOneNeg=-1,
                     rotationTwoNeg=1,
                     offsetTranslate=-1.006,
                     )

            # WRIST
            aj.Build(add_joint=wristShapeJoint,
                     fk_ik_setup=self.armRGTFkIkLimbSetupController,
                     controller_expand_name=prefixWrist,
                     joint_driver_matrix=self.sjWristRGT,
                     joint_add_target=self.ssWristRGT,
                     joint_driver_inverse_matrix=self.sjForearmRGT,
                     point_grp_driver=[self.armRGTCtrlFollMiddleLimb[-1], self.sjWristRGT],
                     scale_driver=[self.armRGTCtrlFollMiddleLimb[-1], self.sjWristRGT],
                     prefix=prefixWrist,
                     side=sideRGT,
                     joint_grp=self.baseSkinGrp,
                     rotation='Z',
                     translateOne='Y',
                     translateTwo='X',
                     rotationOnePos=-1,
                     rotationTwoPos=-1,
                     rotationOneNeg=1,
                     rotationTwoNeg=1,
                     offsetTranslate=-1.006,
                     )

    # ======================================================================================================================
    #                                           ADDITIONAL JOINT FUNCTION
    # ======================================================================================================================
    def additionalJointAtribute(self, controllerFKIKLimbSetup, prefixLimb ):
        au.add_attribute(objects=[controllerFKIKLimbSetup], long_name=[prefixLimb + 'Shape'],
                         attributeType="float", min=0, max=1, dv=0.5, channel_box=True)


