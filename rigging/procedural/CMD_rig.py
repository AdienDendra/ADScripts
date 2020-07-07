from __builtin__ import reload

import maya.cmds as mc
from rigging.library.utils import core as cr
from rigging.library.module import biped_module as cbm, face_module as cfm
from rigging.library.module.body import expand_skeleton_module as esm
from rigging.library.base.face import blendshape as bsm
from rigging.tools import AD_utils as au

reload(cbm)
reload(cfm)
reload(esm)
reload(au)
reload(bsm)
reload(cr)

# load Plug-ins
cr.load_matrix_quad_plugin()

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

def face_biped(# LIP
         crv_up_lip_template='lipUpTmp_crv',
         crv_low_lip_template='lipLowTmp_crv',
         crv_up_lip_roll_template='lipUpRollTmp_crv',
         crv_low_lip_roll_template='lipLowRollTmp_crv',
         offset_jnt02_bind_lip_pos_to_cheek=1,
         lip_0105_direction=20,
         lip_0204_direction=15,

         # NOSE
         crv_nose_template='nose_crv',
         nose_expression_follow_mouth_value=1,
         offset_jnt02_bind_nose_pos=1,
         offset_jnt04_bind_nose_pos=1,

         # LID SETUP
         curve_up_lid_template_LFT='lidUpTmpLFT_crv',
         curve_low_lid_template_LFT='lidLowTmpLFT_crv',
         curve_up_lid_template_RGT='lidUpTmpRGT_crv',
         curve_low_lid_template_RGT='lidLowTmpRGT_crv',
         lid01_direction=0,
         lid02_direction=0,
         lid03_direction=30,
         lid04_direction=50,
         lid05_direction=60,
         offset_jnt02_lid_position=1,
         offset_jnt04_lid_position=1,

         # LID FOLLOWING THE EYE AIM
         low_lid_following_to_down=30,
         up_lid_following_to_down_low_lid_following_to_up=20,
         up_lid_and_low_lid_to_left_right=40,
         up_lid_following_to_up=20,

         # EYEBALL, MOUTH AND EYE AIM
         eyeball_ctrl_direction=29,
         mouth_ctrl_position=1,
         eye_aim_ctrl_position=2,

         # LID OUT
         curve_up_lid_out_template_LFT='lidOutUpTmpLFT_crv',
         curve_low_lid_out_template_LFT='lidOutLowTmpLFT_crv',
         curve_up_lid_out_template_RGT='lidOutUpTmpRGT_crv',
         curve_low_lid_out_template_RGT='lidOutLowTmpRGT_crv',
         lid01_out_ctrl_direction=0,
         lid02_out_ctrl_direction=0,
         lid03_out_ctrl_direction=30,
         lid04_out_ctrl_direction=40,
         lid05_out_ctrl_direction=50,
         offset_jnt02_bind_lid_out_position=1,
         offset_jnt04_bind_lid_out_position=1,

         # BROW
         brow_in_rotate_grp_offset=0,
         brow_mid_rotate_grp_offset=30,
         brow_out_rotate_grp_offset=45,
         brow_tip_rotate_grp_offset=65,

         # BULGE DEFORMER
         bulge_mesh='headBulge_geo',
         add_set_bulge=['bodyPartGeoBulge_grp'],

         # UTILS
         side_LFT='LFT',
         side_RGT='RGT',
         scale=1.0,
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
    faceRig = cfm.build_rig(curve_up_template_lip=crv_up_lip_template,
                            curve_low_template_lip=crv_low_lip_template,
                            curve_up_template_lip_roll=crv_up_lip_roll_template,
                            curve_low_template_lip_roll=crv_low_lip_roll_template,
                            curve_template_nose=crv_nose_template,
                            position_mouth_ctrl=mouth_ctrl_position,

                            offset_jnt02_bind_lip_cheek_position=offset_jnt02_bind_lip_pos_to_cheek,
                            offset_jnt02_bind_lip_nose_position=offset_jnt02_bind_nose_pos,
                            offset_jnt04_bind_lip_nose_position=offset_jnt04_bind_nose_pos,
                            scale=scale,
                            lip01_cheek_direction=lip_0105_direction,
                            lip02_cheek_direction=lip_0204_direction,
                            side_LFT=side_LFT,
                            side_RGT=side_RGT,
                            suffix_controller=suffix_controller,

                            cheek_low_prefix=cheek_low_prefix,
                            cheek_mid_prefix=cheek_mid_prefix,
                            cheek_up_prefix=cheek_up_prefix,
                            cheek_in_up_prefix=cheek_in_up_prefix,
                            cheek_in_low_prefix= cheek_in_low_prefix,
                            cheek_out_up_prefix=cheek_out_up_prefix,
                            cheek_out_low_prefix=cheek_out_low_prefix,
                            jaw_prefix=jaw_prefix,
                            jaw_tip_prefix=jaw_tip_prefix,
                            head_prefix=head_prefix,
                            neck_prefix=neck_prefix,
                            neck_in_btw_prefix=neck_inbetween_prefix,
                            head_up_prefix=head_up_prefix,
                            head_low_prefix=head_low_prefix,

                            columella_prefix=columella_prefix,

                            lid02_position_offset=offset_jnt02_lid_position,
                            lid04_position_offset=offset_jnt04_lid_position,
                            curve_up_lid_template_LFT=curve_up_lid_template_LFT,
                            curve_low_lid_template_LFT=curve_low_lid_template_LFT,
                            curve_up_lid_template_RGT=curve_up_lid_template_RGT,
                            curve_low_lid_template_RGT=curve_low_lid_template_RGT,
                            low_lid_following_down=low_lid_following_to_down,
                            up_lid_following_down_low_lid_following_up=up_lid_following_to_down_low_lid_following_to_up,
                            up_lid_LR_low_lid_LR=up_lid_and_low_lid_to_left_right,
                            up_lid_following_up=up_lid_following_to_up,

                            eye_prefix=eye_prefix,
                            pupil_prefix= pupil_prefix,
                            iris_prefix= iris_prefix,
                            lid01_direction=lid01_direction,
                            lid02_direction=lid02_direction,
                            lid03_direction=lid03_direction,
                            lid04_direction=lid04_direction,
                            lid05_direction=lid05_direction,
                            position_eye_aim_ctrl=eye_aim_ctrl_position,
                            eye_ctrl_direction=eyeball_ctrl_direction,
                            eye_aim_prefix=eye_aim_prefix,
                            nose_follow_mouth_value=nose_expression_follow_mouth_value,

                            curve_up_lid_out_LFT=curve_up_lid_out_template_LFT,
                            curve_low_lid_out_LFT=curve_low_lid_out_template_LFT,
                            jnt02_bind_lip_lid_out_position_offset=offset_jnt02_bind_lid_out_position,
                            jnt04_bind_lip_lid_out_position_offset= offset_jnt04_bind_lid_out_position,
                            curve_up_lid_out_RGT=curve_up_lid_out_template_RGT,
                            curve_low_lid_out_RGT=curve_low_lid_out_template_RGT,
                            lid01_out_ctrl_direction=lid01_out_ctrl_direction,
                            lid02_out_ctrl_direction=lid02_out_ctrl_direction,
                            lid03_out_ctrl_direction=lid03_out_ctrl_direction,
                            lid04_out_ctrl_direction=lid04_out_ctrl_direction,
                            lid05_out_ctrl_direction=lid05_out_ctrl_direction,

                            mentolabial_prefix=mentolabial_prefix,
                            chin_prefix=chin_prefix,
                            ear_prefix=ear_prefix,

                            brow_tweak_prefix=brow_tw_prefix,
                            brow_in_prefix=brow_in_prefix,
                            brow_mid_prefix=brow_mid_prefix,
                            brow_out_prefix=brow_out_prefix,
                            brows_prefix=brows_prefix,
                            brow_tip_prefix=brow_tip_prefix,
                            brow_center_prefix=brow_center_prefix,

                            brow_in_rotation_grp_offset= brow_in_rotate_grp_offset,
                            brow_mid_rotation_grp_offset= brow_mid_rotate_grp_offset,
                            brow_out_rotation_grp_offset=  brow_out_rotate_grp_offset,
                            brow_tip_rotation_grp_offset=brow_tip_rotate_grp_offset,

                            bulge_mesh=bulge_mesh,
                            add_set_bulge=add_set_bulge,
                            suffix_joint=suffix_joint
                            )


    print ('------------------------------')
    print ('Facial base is done!')

# ======================================================================================================================
#                                                   FACIAL BLENDSHAPE CMD
# ======================================================================================================================
def blendshape(face_blendshape_node_name='face_bsn',
               squash_stretch_bsh_prefix='head',
               roll_up_lip_bsh_prefix='rollLipUp',
               roll_low_lip_bsh_prefix='rollLipLow',
               cheek_out_prefix ='cheekOut',
               side_LFT='LFT',
               side_RGT='RGT',
               bshSuffix='grp'):

    if face_blendshape_node_name:
        print('------------------------------')
        print('Add facial blendshape..............')

        au.add_attribute(objects=['%s_%s' % (prefix_mouth_jnt, suffix_controller)], long_name=['bshSetup'],
                         nice_name=[' '], at="enum",
                         en='Bsh Setup', channel_box=True)

        controller_up_roll_bsh = au.add_attribute(objects=['%s_%s' % (prefix_mouth_jnt, suffix_controller)],
                                                  long_name=['rollLipUpBsh'],
                                                  attributeType="float", dv=0, keyable=True)

        controller_low_roll_bsh = au.add_attribute(objects=['%s_%s' % (prefix_mouth_jnt, suffix_controller)],
                                                   long_name=['rollLipLowBsh'],
                                                   attributeType="float", dv=0, keyable=True)

        head_low_squash_stretch = au.add_attribute(objects=['%s_%s' % (prefix_mouth_jnt, suffix_controller)],
                                                   long_name=['squashStretchBsh'],
                                                   attributeType="float", dv=0, keyable=True)

        cheek_out_LFT = au.add_attribute(objects=['%s_%s' % (prefix_mouth_jnt, suffix_controller)],
                                         long_name=['cheekOutLFT' + '_' + 'Bsh'],
                                         attributeType="float", dv=0, min=0, keyable=True)
        cheek_out_RGT = au.add_attribute(objects=['%s_%s' % (prefix_mouth_jnt, suffix_controller)],
                                         long_name=['cheekOutRGT' + '_' + 'Bsh'],
                                         attributeType="float", dv=0, min=0, keyable=True)
        bsm.BuildTwoSide(blendshape_node_name=face_blendshape_node_name,
                       squash_stretch_prefix=squash_stretch_bsh_prefix,
                       roll_low_prefix=roll_low_lip_bsh_prefix,
                       roll_up_prefix=roll_up_lip_bsh_prefix,
                       cheek_out_prefix=cheek_out_prefix,
                       blendshape_suffix=bshSuffix,
                       mouth_ctrl='%s_%s' % (prefix_mouth_jnt, suffix_controller),
                       controller_roll_up_bsh_attr=controller_up_roll_bsh,
                       controller_roll_low_bsh_attr=controller_low_roll_bsh,
                       squash_stretch_attr=head_low_squash_stretch,
                       cheek_out_attr_LFT= cheek_out_LFT,
                       cheek_out_attr_RGT=cheek_out_RGT,
                       side_LFT= side_LFT,
                       side_RGT= side_RGT
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
                    suffix_parent_joint='skn',
                    suffix_duplicate_expand_joint='jnt'
                    )

    print('------------------------------')
    print('Adding joint deform is done!')