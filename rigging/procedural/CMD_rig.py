from __builtin__ import reload

import maya.cmds as mc

from rigging.library.module import biped_module as cbm, face_module as cfm
from rigging.library.module.body import expand_skeleton_module as esm
from rigging.library.module.face import blendshape_module as bsm
from rigging.tools import AD_utils as au

reload(cbm)
reload(cfm)
reload(esm)
reload(au)
reload(bsm)

# load Plug-ins
matrix_node = mc.pluginInfo('matrixNodes.mll', query=True, loaded=True)
quat_node = mc.pluginInfo('quatNodes.mll', query=True, loaded=True)

if not matrix_node:
    mc.loadPlugin( 'matrixNodes.mll' )

if not quat_node:
    mc.loadPlugin( 'quatNodes.mll' )

# build Spine
prefix_spine = 'spine'
prefix_spine_setup = 'spineSetup'

# build Clavicle
prefix_clav = 'clavicle'

# build Arm
prefix_arm = 'arm'
prefix_upperArm = 'upperArm'
prefix_forearm = 'forearm'
prefix_wrist = 'wrist'
prefix_elbow = 'elbow'
prefix_hand = 'hand'
prefix_arm_setup = 'armSetup'
prefix_finger_setup = 'fingerSetup'
prefix_palm = 'palm'

# build Leg`
prefix_leg = 'leg'
prefix_upperLeg = 'upperLeg'
prefix_lowerLeg = 'lowerLeg'
prefix_ankle = 'ankle'
prefix_knee  = 'knee'
prefix_ball = 'ball'
prefix_toe = 'toe'
prefix_leg_setup = 'legSetup'
prefix_foot = 'foot'

# build arm finger
prefix_thumb = 'thumb'
prefix_index = 'index'
prefix_middle = 'middle'
prefix_ring = 'ring'
prefix_pinky = 'pinky'

sj_prefix_value = ''
ss_prefix_value = 'Scale'
sFk_prefix_value = 'Fk'
sIk_prefix_value = 'Ik'
sAdd_prefix_value = 'Expand'

fk = 'Fk'
ik = 'Ik'
dtl = 'Dtl'
suffix_controller= 'ctrl'
suffix_joint = 'jnt'

# FACE
prefix_jaw_jnt = 'jaw'
prefix_head_low_jnt = 'headLow'
prefix_mouth_jnt = 'mouth'

cheek_low_prefix = 'cheekLow'
cheek_mid_prefix = 'cheekMid'
cheek_up_prefix = 'cheekUp'
cheek_in_up_prefix = 'cheekInUp'
cheek_in_low_prefix = 'cheekInLow'
cheek_out_up_prefix = 'cheekOutUp'
cheek_out_low_prefix = 'cheekOutLow'

jaw_prefix= 'jaw'
jaw_tip_prefix= 'jawTip'

head_prefix = 'head'
neck_prefix = 'neck'
neck_inbetween_prefix= 'neckInBtw'
head_up_prefix = 'headUp'
head_low_prefix = 'headLow'

columella_prefix = 'columella'
eye_prefix= 'eye'
eye_aim_prefix = 'eyeAim'
pupil_prefix= 'pupil'
iris_prefix= 'iris'

mentolabial_prefix= 'mentolabial'
chin_prefix= 'chin'
ear_prefix= 'ear'

brow_tw_prefix= 'browTw'
brow_in_prefix= 'browIn'
brow_mid_prefix= 'browMid'
brow_out_prefix= 'browOut'
brows_prefix= 'brow'
brow_tip_prefix= 'browTip'
brow_center_prefix= 'browCenter'

# ======================================================================================================================
#                                                         BIPED BODY CMD
# ======================================================================================================================

def biped(clavicle_left=True,
          clavicle_right=True,
          arm_left=True,
          arm_right=True,
          leg_left=True,
          leg_right=True,
          foot_left = True,
          foot_right=True,
          detail_spine_deformer=True,
          detail_arm_deformer=True,
          detail_leg_deformer=True,
          number_arm_detail_ctrl=5,
          number_leg_detail_ctrl=5,
          left_side='LFT',
          right_side='RGT',
          thumb_left=True,
          index_left=True,
          middle_left=True,
          ring_left=True,
          pinky_left=True,
          thumb_right=True,
          index_right=True,
          middle_right=True,
          ring_right=True,
          pinky_right=True,
          size=1.0):


    ## CHECK IF THE RIG EXIST IN THE SCENE
    if mc.objExists('anim_ctrl'):
        mc.error('Please rid off the old base and including the nodes before run the script!')

    print('------------------------------')
    print('Biped base script is running...')
    print('------------------------------')

    # RUN THE RIG BUILD
    cbm.build_rig(clavicle_left=clavicle_left, clavicle_right=clavicle_right, arm_left=arm_left, arm_right=arm_right,
                  prefix_spine=prefix_spine,
                  prefix_spine_setup=prefix_spine_setup,
                  prefix_upperArm=prefix_upperArm, prefix_forearm=prefix_forearm, prefix_clav=prefix_clav,
                  prefix_arm=prefix_arm,
                  prefix_wrist=prefix_wrist, prefix_elbow=prefix_elbow, prefix_hand=prefix_hand,
                  prefix_arm_setup=prefix_arm_setup,
                  leg_left=leg_left, leg_right=leg_right, foot_right=foot_right, foot_left=foot_left,
                  prefix_upperLeg=prefix_upperLeg,
                  prefix_lowerLeg=prefix_lowerLeg, prefix_leg=prefix_leg, prefix_ankle=prefix_ankle,
                  prefix_knee=prefix_knee,
                  prefix_ball=prefix_ball, prefix_toe=prefix_toe, prefix_foot=prefix_foot, prefix_leg_setup=prefix_leg_setup,
                  detail_leg_def=detail_leg_deformer, num_leg_dtl_ctrl=number_leg_detail_ctrl - 2,
                  prefix_thumb=prefix_thumb, prefix_index=prefix_index, prefix_middle=prefix_middle,
                  prefix_ring=prefix_ring,
                  prefix_finger_setup=prefix_finger_setup, prefix_pinky=prefix_pinky, prefix_palm=prefix_palm,
                  detail_spine_deformer=detail_spine_deformer, detail_arm_deformer=detail_arm_deformer,
                  number_arm_detail_ctrl=number_arm_detail_ctrl - 2,
                  thumb_arm_LFT=thumb_left, index_arm_LFT=index_left, middle_arm_LFT=middle_left, ring_arm_LFT=ring_left,
                  pinky_arm_LFT=pinky_left,
                  thumb_arm_RGT=thumb_right, index_arm_RGT=index_right, middle_arm_RGT=middle_right,
                  ring_arm_RGT=ring_right,
                  pinky_arm_RGT=pinky_right,
                  scale=size, side_LFT=left_side, side_RGT=right_side, sj_prefix_value=sj_prefix_value,
                  ss_prefix_value=ss_prefix_value,
                  sFk_prefix_value=sFk_prefix_value, sIk_prefix_value=sIk_prefix_value, sAdd_prefix_value=sAdd_prefix_value,
                  fk=fk, ik=ik, detail=dtl, suffix_joint=suffix_joint)
    print('------------------------------')
    print('Biped base is done!')


# ======================================================================================================================
#                                                         HEAD AND FACE CMD
# ======================================================================================================================

def Head(# LIP
         crvUpLip='lipUp_crv',
         crvLowLip='lipLow_crv',
         crvUpLipRoll='lipUpRoll_crv',
         crvLowLipRoll='lipLowRoll_crv',
         offsetJnt02BindLipPosToCheek=1,
         directionLip0105=20,
         directionLip0204=15,

         # NOSE
         crvNose='nose_crv',
         noseExpressionFollowMouthValue=1,
         offsetJnt02BindNosePos=0,
         offsetJnt04BindNosePos=0,

         # LID SETUP
         crvUpLidLFT='lidUpLFT_crv',
         crvLowLidLFT='lidLowLFT_crv',
         crvUpLidRGT='lidUpRGT_crv',
         crvLowLidRGT='lidLowRGT_crv',
         directionLid01=0,
         directionLid02=0,
         directionLid03=30,
         directionLid04=50,
         directionLid05=60,
         offsetJnt02LidPos=1,
         offsetJnt04LidPos=1,

         # LID FOLLOWING THE EYE AIM
         lowLidFollowingToDown=30,
         upLidFollowingToDownLowLidFollowingToUp=20,
         upLidAndLowLidToLeftRight=40,
         upLidFollowingToUp=20,

         # EYEBALL, MOUTH AND EYE AIM
         eyeballCtrlDirection=29,
         positionMouthCtrl=1,
         positionEyeAimCtrl=2,

         # LID OUT
         crvUpLidOutLFT='lidOutUpLFT_crv',
         crvLowLidOutLFT='lidOutLowLFT_crv',
         crvUpLidOutRGT='lidOutUpRGT_crv',
         crvLowLidOutRGT='lidOutLowRGT_crv',
         directionCtrlLidOut01=0,
         directionCtrlLidOut02=0,
         directionCtrlLidOut03=30,
         directionCtrlLidOut04=40,
         directionCtrlLidOut05=50,
         offsetJnt02BindLidOutPos=1,
         offsetJnt04BindLidOutPos=1,

         # BROW
         browInGrpRotOffset=0,
         browMidGrpRotOffset=30,
         browOutGrpRotOffset=45,
         browTipGrpRotOffset=65,

         # BULGE DEFORMER
         bulgeMesh='headBulge_geo',
         addSetBulge=['browGeoBulge_grp', 'lashesGeoBulge_grp'],

         # UTILS
         sideLFT='LFT',
         sideRGT='RGT',
         scale=1.0,
         faceCurvesGrp='faceCurves_grp'
         ):

    # # CHECK IF THE RIG EXIST IN THE SCENE
    # if mc.objExists('head_ctrl'):
    #     mc.error('Please rid off the old base and including the nodes before run the script!')
    print ('----------------------------------------')
    print ('head and face base script is running...')
    print ('----------------------------------------')
    if mc.objExists('neck01_jnt'):
        mc.error('%s%s%s' % ('Please remove the',' neck01_jnt ', 'joint first!'))

    # RUN THE RIG BUILD
    faceRig = cfm.BuildRig(crvUpLip=crvUpLip,
                           crvLowLip=crvLowLip,
                           crvUpLipRoll=crvUpLipRoll,
                           crvLowLipRoll=crvLowLipRoll,
                           crvNose=crvNose,
                           positionMouthCtrl=positionMouthCtrl,

                           offsetJnt02BindLipPosCheek=offsetJnt02BindLipPosToCheek,
                           offsetJnt02BindLipPosNose=offsetJnt02BindNosePos,
                           offsetJnt04BindLipPosNose=offsetJnt04BindNosePos,
                           scale=scale,
                           directionLip01Cheek=directionLip0105,
                           directionLip02Cheek=directionLip0204,
                           sideLFT=sideLFT,
                           sideRGT=sideRGT,
                           suffixController=suffix_controller,

                           cheekLowPrefix=cheek_low_prefix,
                           cheekMidPrefix=cheek_mid_prefix,
                           cheekUpPrefix=cheek_up_prefix,
                           cheekInUpPrefix=cheek_in_up_prefix,
                           cheekInLowPrefix= cheek_in_low_prefix,
                           cheekOutUpPrefix=cheek_out_up_prefix,
                           cheekOutLowPrefix=cheek_out_low_prefix,
                           jawPrefix=jaw_prefix,
                           jawTipPrefix=jaw_tip_prefix,
                           headPrefix=head_prefix,
                           neckPrefix=neck_prefix,
                           neckInBtwPrefix=neck_inbetween_prefix,
                           headUpPrefix=head_up_prefix,
                           headLowPrefix=head_low_prefix,

                           columellaPrefix=columella_prefix,

                           offsetLidPos02=offsetJnt02LidPos,
                           offsetLidPos04=offsetJnt04LidPos,
                           crvUpLidLFT=crvUpLidLFT,
                           crvLowLidLFT=crvLowLidLFT,
                           crvUpLidRGT=crvUpLidRGT,
                           crvLowLidRGT=crvLowLidRGT,
                           lowLidFolDown=lowLidFollowingToDown,
                           upLidFolDownLowLidFolUp=upLidFollowingToDownLowLidFollowingToUp,
                           upLidLRLowLidLR=upLidAndLowLidToLeftRight,
                           upLidFolUp=upLidFollowingToUp,

                           eyePrefix=eye_prefix,
                           pupilPrefix= pupil_prefix,
                           irisPrefix= iris_prefix,
                           directionLid01=directionLid01,
                           directionLid02=directionLid02,
                           directionLid03=directionLid03,
                           directionLid04=directionLid04,
                           directionLid05=directionLid05,
                           positionEyeAimCtrl=positionEyeAimCtrl,
                           eyeCtrlDirection=eyeballCtrlDirection,
                           eyeAimPrefix=eye_aim_prefix,
                           noseFollowMouthValue=noseExpressionFollowMouthValue,

                           crvUpLidOutLFT=crvUpLidOutLFT,
                           crvLowLidOutLFT=crvLowLidOutLFT,
                           offsetJnt02BindLipPosLidOut=offsetJnt02BindLidOutPos,
                           offsetJnt04BindLipPosLidOut = offsetJnt04BindLidOutPos,
                           crvUpLidOutRGT=crvUpLidOutRGT,
                           crvLowLidOutRGT=crvLowLidOutRGT,
                           directionCtrlLidOut01=directionCtrlLidOut01,
                           directionCtrlLidOut02=directionCtrlLidOut02,
                           directionCtrlLidOut03=directionCtrlLidOut03,
                           directionCtrlLidOut04=directionCtrlLidOut04,
                           directionCtrlLidOut05=directionCtrlLidOut05,

                           mentolabialPrefix=mentolabial_prefix,
                           chinPrefix=chin_prefix,
                           earPrefix=ear_prefix,

                           browTwPrefix=brow_tw_prefix,
                           browInPrefix=brow_in_prefix,
                           browMidPrefix=brow_mid_prefix,
                           browOutPrefix=brow_out_prefix,
                           browsPrefix=brows_prefix,
                           browTipPrefix=brow_tip_prefix,
                           browCenterPrefix=brow_center_prefix,

                           browInGrpRotOffset= browInGrpRotOffset,
                           browMidGrpRotOffset= browMidGrpRotOffset,
                           browOutGrpRotOffset=  browOutGrpRotOffset,
                           browTipGrpRotOffset=browTipGrpRotOffset,

                           bulgeMesh=bulgeMesh,
                           addSetBulge=addSetBulge,
                           faceCurvesGrp=faceCurvesGrp,
                           suffixJoint=suffix_joint
                           )
    if mc.objExists('spine04%s_jnt' % sj_prefix_value):
        mc.parent(faceRig['neckJntGrp'], 'spine04%s_jnt' % sj_prefix_value)
        mc.parentConstraint('spine04%s_jnt' % sj_prefix_value, faceRig['neckCtrlZroGrp'], mo=1)
        mc.scaleConstraint('spine04%s_jnt' % sj_prefix_value, faceRig['neckCtrlZroGrp'])
    else:
        mc.parent(faceRig['neckJntGrp'], 'faceJoint_grp')

    print ('------------------------------')
    print ('Facial base is done!')

# ======================================================================================================================
#                                                   FACIAL BLENDSHAPE CMD
# ======================================================================================================================
def Blendshape(faceBsnName='face_bsn',
               squashStretchBshPrefix='head',
               rollUpBshPrefix='rollLipUp',
               rollLowBshPrefix='rollLipLow',
               cheekOutPrefix = 'cheekOut',
               sideLFT='LFT',
               sideRGT='RGT',
               bshSuffix='grp'):

    if faceBsnName:
        print('------------------------------')
        print('Add facial blendshape..............')

        au.add_attribute(objects=['%s_%s' % (prefix_mouth_jnt, suffix_controller)], long_name=['bshSetup'],
                         nice_name=[' '], at="enum",
                         en='Bsh Setup', channel_box=True)

        controllerUpRollBsh = au.add_attribute(objects=['%s_%s' % (prefix_mouth_jnt, suffix_controller)],
                                               long_name=['rollLipUpBsh'],
                                               attributeType="float", dv=0, keyable=True)

        controllerLowRollBsh = au.add_attribute(objects=['%s_%s' % (prefix_mouth_jnt, suffix_controller)],
                                                long_name=['rollLipLowBsh'],
                                                attributeType="float", dv=0, keyable=True)

        headLowSquashStretch = au.add_attribute(objects=['%s_%s' % (prefix_mouth_jnt, suffix_controller)],
                                                long_name=['squashStretchBsh'],
                                                attributeType="float", dv=0, keyable=True)

        cheekOutLFT = au.add_attribute(objects=['%s_%s' % (prefix_mouth_jnt, suffix_controller)],
                                       long_name=['cheekOutLFT' + '_' + 'Bsh'],
                                       attributeType="float", dv=0, min=0, keyable=True)
        cheekOutRGT = au.add_attribute(objects=['%s_%s' % (prefix_mouth_jnt, suffix_controller)],
                                       long_name=['cheekOutRGT' + '_' + 'Bsh'],
                                       attributeType="float", dv=0, min=0, keyable=True)
        bsm.blendshape(bsnName=faceBsnName,
                       prefixSquashStretch=squashStretchBshPrefix,
                       prefixRollLow=rollLowBshPrefix,
                       prefixRollUp=rollUpBshPrefix,
                       prefixCheekOut=cheekOutPrefix,
                       suffixBsh=bshSuffix,
                       mouthCtrl='%s_%s' % (prefix_mouth_jnt, suffix_controller),
                       controllerUpRollBshAttr=controllerUpRollBsh,
                       controllerLowRollBshAttr=controllerLowRollBsh,
                       squashStretchAttr=headLowSquashStretch,
                       cheekOutAttrLFT= cheekOutLFT,
                       cheekOutAttrRGT=cheekOutRGT,
                       sideLFT = sideLFT,
                       sideRGT = sideRGT
                       )
        print('Facial blendshape is done!')


# ======================================================================================================================
#                                                EXPAND BODY JOINT CMD
# ======================================================================================================================


def add_expand_joint(number_arm_detail_ctrl= 5,
                     number_leg_detail_ctrl = 5,
                     spine_expand_joint=True,
                     neck_expand_joint= False,
                     clavicle_expand_joint=False,
                     ball_expand_joint=True,
                     upperArm_expand_joint=True,
                     upperLeg_expand_joint=True,
                     elbow_expand_joint=True,
                     knee_expand_joint=True,
                     wrist_expand_joint=True,
                     ankle_expand_joint=True,
                     thumb_expand_joint=True,
                     index_expand_joint=True,
                     middle_expand_joint=True,
                     ring_expand_joint=True,
                     pinky_expand_joint=True,
                     left_side='LFT',
                     right_side='RGT'):
    print('------------------------------')
    print('Adding joint deform...........')

    esm.JointExpand(number_arm_detail_ctrl=number_arm_detail_ctrl,
                    number_leg_detail_ctrl=number_leg_detail_ctrl,
                    spine_expand_joint=spine_expand_joint,
                    neck_expand_joint=neck_expand_joint,
                    clavicle_expand_joint=clavicle_expand_joint,
                    ball_expand_joint=ball_expand_joint,
                    upperArm_expand_joint=upperArm_expand_joint,
                    upperLeg_expand_joint=upperLeg_expand_joint,
                    elbow_expand_joint=elbow_expand_joint,
                    knee_expand_joint=knee_expand_joint,
                    wrist_expand_joint=wrist_expand_joint,
                    ankle_expand_joint=ankle_expand_joint,
                    left_side=left_side,
                    right_side=right_side,

                    prefix_spine=prefix_spine,
                    prefix_arm_setup=prefix_arm_setup,
                    prefix_clav=prefix_clav,
                    prefix_upperArm=prefix_upperArm,
                    prefix_elbow=prefix_elbow,
                    prefix_wrist=prefix_wrist,
                    prefix_leg_setup=prefix_leg_setup,
                    prefix_ball=prefix_ball,
                    prefix_upperLeg=prefix_upperLeg,
                    prefix_knee=prefix_knee,
                    prefix_ankle=prefix_ankle,
                    sAdd_prefix_value=sAdd_prefix_value,
                    dtl=dtl,
                    sj_prefix_value=sj_prefix_value,
                    prefix_forearm=prefix_forearm,
                    fk=fk,
                    prefix_lower_leg=prefix_lowerLeg,
                    prefix_FkIk_spine_setup=prefix_spine_setup,
                    neck_prefix=neck_prefix,

                    upArm_joint_LFT_grp=prefix_arm + 'Joint' + left_side + '_grp',
                    elbow_joint_LFT_grp=prefix_arm + 'Joint' + left_side + '_grp',
                    wrist_joint_LFT_grp=prefix_arm + 'Joint' + left_side + '_grp',
                    upArm_joint_RGT_grp=prefix_arm + 'Joint' + right_side + '_grp',
                    elbow_joint_RGT_grp=prefix_arm + 'Joint' + right_side + '_grp',
                    wrist_joint_RGT_grp=prefix_arm + 'Joint' + right_side + '_grp',
                    upLeg_joint_LFT_grp=prefix_leg + 'Joint' + left_side + '_grp',
                    knee_joint_LFT_grp=prefix_leg + 'Joint' + left_side + '_grp',
                    ankle_joint_LFT_grp=prefix_leg + 'Joint' + left_side + '_grp',
                    ball_joint_LFT_grp=prefix_leg + 'Joint' + left_side + '_grp',
                    upLeg_joint_RGT_grp=prefix_leg + 'Joint' + right_side + '_grp',
                    knee_joint_RGT_grp=prefix_leg + 'Joint' + right_side + '_grp',
                    ankle_joint_RGT_grp=prefix_leg + 'Joint' + right_side + '_grp',
                    ball_joint_RGT_grp=prefix_leg + 'Joint' + right_side + '_grp',
                    neck_joint_grp=prefix_spine + 'Joint_grp',
                    spine_joint_grp=prefix_spine + 'Joint_grp',

                    prefix_thumb=prefix_thumb,
                    prefix_index=prefix_index,
                    prefix_middle=prefix_middle,
                    prefix_ring=prefix_ring,
                    prefix_pinky=prefix_pinky,
                    thumb_joint_LFT_grp=prefix_arm + 'Joint' + left_side + '_grp',
                    index_joint_LFT_grp=prefix_arm + 'Joint' + left_side + '_grp',
                    middle_joint_LFT_grp=prefix_arm + 'Joint' + left_side + '_grp',
                    ring_joint_LFT_grp=prefix_arm + 'Joint' + left_side + '_grp',
                    pinky_joint_LFT_grp=prefix_arm + 'Joint' + left_side + '_grp',
                    thumb_joint_RGT_grp=prefix_arm + 'Joint' + right_side + '_grp',
                    index_joint_RGT_grp=prefix_arm + 'Joint' + right_side + '_grp',
                    middle_joint_RGT_grp=prefix_arm + 'Joint' + right_side + '_grp',
                    ring_joint_RGT_grp=prefix_arm + 'Joint' + right_side + '_grp',
                    pinky_joint_RGT_grp=prefix_arm + 'Joint' + right_side + '_grp',
                    thumb_expand_joint=thumb_expand_joint,
                    index_expand_joint=index_expand_joint,
                    middle_expand_joint=middle_expand_joint,
                    ring_expand_joint=ring_expand_joint,
                    pinky_expand_joint=pinky_expand_joint,
                    )

    print('------------------------------')
    print('Adding joint deform is done!')