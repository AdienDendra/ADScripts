from __future__ import absolute_import

import maya.cmds as cmds

from rigging.library.module import tmpModule as rlm_tmpModule, baseModule as rlm_baseModule
from rigging.library.module.face import lidOutModule as rlmf_lidOutModule, noseModule as rlmf_noseModule, \
    browModule as rlmf_browModule, \
    lipModule as rlmf_lipModule, cheekModule as rlmf_cheekModule, lidModule as rlmf_lidModule, \
    chinModule as rlmf_chinModule, \
    earModule as rlmf_earModule, bulgeModule as rlmf_bulgeModule, headModule as rlmf_headModule
from rigging.library.utils import controller as rlu_controller, transform as rlu_transform
from rigging.tools import utils as rt_utils


def build_rig(
        offset_jnt02_bind_lip_cheek_position,
        offset_jnt02_bind_lip_nose_position,
        offset_jnt04_bind_lip_nose_position,
        lip01_cheek_direction,
        lip02_cheek_direction,
        scale,
        side_LFT,
        side_RGT,
        suffix_controller,

        cheek_low_prefix,
        cheek_mid_prefix,
        cheek_up_prefix,
        cheek_in_up_prefix,
        cheek_in_low_prefix,

        cheek_out_up_prefix,
        cheek_out_low_prefix,
        curve_up_template_lip,
        curve_low_template_lip,
        curve_up_template_lip_roll,
        curve_low_template_lip_roll,
        position_mouth_ctrl,
        curve_template_nose,

        jaw_prefix,
        jaw_tip_prefix,
        head_prefix,
        neck_prefix,
        neck_in_btw_prefix,
        head_up_prefix,
        head_low_prefix,
        columella_prefix,

        curve_up_lid_template_LFT,
        curve_low_lid_template_LFT,
        curve_up_lid_template_RGT,
        curve_low_lid_template_RGT,
        eye_prefix,
        eye_aim_prefix,
        lid01_direction,
        lid02_direction,
        lid03_direction,
        lid04_direction,
        lid05_direction,
        position_eye_aim_ctrl,

        eye_ctrl_direction,

        lid02_position_offset,
        lid04_position_offset,
        nose_follow_mouth_value,

        curve_up_lid_out_LFT,
        curve_low_lid_out_LFT,
        curve_up_lid_out_RGT,
        curve_low_lid_out_RGT,
        jnt02_bind_lip_lid_out_position_offset,
        jnt04_bind_lip_lid_out_position_offset,
        lid01_out_ctrl_direction,
        lid02_out_ctrl_direction,
        lid03_out_ctrl_direction,
        lid04_out_ctrl_direction,
        lid05_out_ctrl_direction,
        pupil_prefix,
        iris_prefix,

        mentolabial_prefix,
        chin_prefix,

        ear_prefix,

        brow_tweak_prefix,
        brow_in_prefix,
        brow_mid_prefix,
        brow_out_prefix,
        brows_prefix,
        brow_tip_prefix,
        brow_center_prefix,
        brow_in_rotation_grp_offset,
        brow_mid_rotation_grp_offset,
        brow_out_rotation_grp_offset,
        brow_tip_rotation_grp_offset,

        low_lid_following_down,
        up_lid_following_down_low_lid_following_up,
        up_lid_LR_low_lid_LR,
        up_lid_following_up,

        bulge,
        bulge_mesh,
        add_set_bulge,
        follicle_mesh,
        game_bind_joint):
    # FINGER POSITION
    BaseF = 'Base'
    UpF = 'Up'
    MidF = 'Mid'
    LowF = 'Low'

    # global base_controller
    if not cmds.objExists('animGmbl_ctrl'):
        base_controller = rlm_baseModule.Base(scale=scale)
        face_non_transform_grp = base_controller.face_non_transform_grp
        face_controller_grp = base_controller.face_controller_grp
        face_joint_grp = base_controller.face_joint_grp

    else:
        face_non_transform_grp = 'faceNonTransform_grp'
        face_controller_grp = 'faceCtrl_grp'
        face_joint_grp = 'faceJoint_grp'

    # ======================================================================================================================
    #                                              DUPLICATE JOINTS AS DRIVER
    # ======================================================================================================================
    sj = rlm_tmpModule.listSkeletonDuplicate(value_prefix='',
                                             key_prefix='Ori',
                                             suffix='skn',
                                             side_LFT=side_LFT,
                                             side_RGT=side_RGT
                                             )
    sGame = []
    if game_bind_joint:
        sGame = rlm_tmpModule.listSkeletonDuplicate(value_prefix='',
                                                    key_prefix='Game',
                                                    suffix='bind',
                                                    side_LFT=side_LFT,
                                                    side_RGT=side_RGT
                                                    )
        # unhide the joint skn
        for item in sGame.list_joint.values():
            cmds.setAttr(item + '.visibility', 1)
            cmds.setAttr(item + '.segmentScaleCompensate', 0)

        bind_game = sorted(sGame.list_joint.values())
        bind_sj = sorted(sj.list_joint.values())

        # constraining the skn to game joint
        for skin_joint, game in zip(bind_sj, bind_game):
            constraint = rt_utils.parent_scale_constraint(skin_joint, game, mo=1)
            cmds.parent(constraint[0], constraint[1], 'additional_grp')

        cmds.parent(sGame.neck, world=True)
        cmds.delete(sGame.root)

        if cmds.objExists('spine04_bind'):
            cmds.parent(sGame.neck, 'spine04_bind')
        # else:
        #     mc.parent(sGame.neck, world=True)

    cmds.parent(sj.neck, world=True)
    cmds.delete(sj.root)

    # ROTATE EYE JNT
    cmds.setAttr(sj.eyeball_LFT + '.rotateY', eye_ctrl_direction)
    cmds.setAttr(sj.eyeball_RGT + '.rotateY', eye_ctrl_direction * -1)
    cmds.makeIdentity(sj.eyeball_LFT, apply=True)
    cmds.makeIdentity(sj.eyeball_RGT, apply=True)

    # JOINT DQ BASE
    cmds.select(cl=1)
    jntDQBase = cmds.joint(n='headDQBase_skn', radius=0.2 * scale)
    cmds.delete(cmds.parentConstraint(sj.head, jntDQBase))
    cmds.makeIdentity(jntDQBase, apply=1, translate=1, rotate=1)
    parentDQ_grp = rlu_transform.create_parent_transform(parent_list=['', 'Offset'], object=jntDQBase,
                                                         match_position=sj.head,
                                                         prefix=jntDQBase, suffix='_skn')

    # mc.parent((jntDQBase, face_non_transform_grp))

    print('5%  | skeleton duplicated is done!')

    # ==================================================================================================================
    #                                                     HEAD PARAMETERS
    # ==================================================================================================================

    head = rlmf_headModule.Head(face_anim_ctrl_grp=face_controller_grp,
                                face_utils_grp=face_non_transform_grp,
                                neck_jnt=sj.neck,
                                neck_in_btw_jnt=sj.neckIn_Btw,
                                head_jnt=sj.head,
                                jaw_jnt=sj.jaw,
                                jaw_tip_jnt=sj.jaw_tip,
                                head_up_jnt=sj.head_up,
                                head_low_jnt=sj.head_low,
                                jaw_prefix=jaw_prefix,
                                jaw_tip_prefix=jaw_tip_prefix,
                                head_prefix=head_prefix,
                                neck_prefix=neck_prefix,
                                neck_in_btw_prefix=neck_in_btw_prefix,
                                head_up_prefix=head_up_prefix,
                                head_low_prefix=head_low_prefix,
                                eye_aim_prefix=eye_aim_prefix,
                                eye_jnt_LFT=sj.eye_LFT,
                                eye_jnt_RGT=sj.eye_RGT,
                                position_eye_aim_ctrl=position_eye_aim_ctrl,
                                upper_teeth_jnt=sj.upper_teeth,
                                lower_teeth_jnt=sj.lower_teeth,
                                tongue01_jnt=sj.tongue01,
                                tongue02_jnt=sj.tongue02,
                                tongue03_jnt=sj.tongue03,
                                tongue04_jnt=sj.tongue04,
                                scale=scale,
                                suffix_controller=suffix_controller,
                                )

    print('10% | head is done!')
    # ==================================================================================================================
    #                                                     LIP PARAMETERS
    # ==================================================================================================================
    lip = rlmf_lipModule.Lip(face_anim_ctrl_grp=face_controller_grp,
                             face_utils_grp=face_non_transform_grp,
                             curve_up_lip_template=curve_up_template_lip,
                             curve_low_lip_template=curve_low_template_lip,
                             curve_up_lip_roll_template=curve_up_template_lip_roll,
                             curve_low_lip_roll_template=curve_low_template_lip_roll,
                             offset_jnt02_bind_position=offset_jnt02_bind_lip_cheek_position,
                             scale=scale,
                             lip01_cheek_direction=lip01_cheek_direction,
                             lip02_cheek_direction=lip02_cheek_direction,
                             side_LFT=side_LFT,
                             side_RGT=side_RGT,
                             jaw_jnt=sj.jaw,
                             head_low_jnt=sj.head_low,
                             mouth_jnt=sj.mouth,
                             position_mouth_ctrl=position_mouth_ctrl,
                             suffix_controller=suffix_controller,
                             jaw_ctrl=head.jaw_ctrl,
                             prefix_upLip_follow=head.attr_upLip_follow,
                             prefix_degree_follow=head.attr_degree_follow,
                             headLow_normal_rotationGrp=head.headLow_normal_rotationGrp,
                             base_module_nonTransform=face_non_transform_grp,
                             game_bind_joint=game_bind_joint
                             )

    print('15% | lip is done!')
    # ==================================================================================================================
    #                                                     NOSE PARAMETERS
    # ==================================================================================================================
    if game_bind_joint:
        nose = rlmf_noseModule.Nose(face_utils_grp=face_non_transform_grp,
                                    columella_jnt=sj.columella,
                                    nose_jnt=sj.nose,
                                    nose_up_jnt=sj.nose_up,
                                    columella_prefix=columella_prefix,
                                    curve_template_nose=curve_template_nose,
                                    offset_jnt02_bind_position=offset_jnt02_bind_lip_nose_position,
                                    offset_jnt04_bind_position=offset_jnt04_bind_lip_nose_position,
                                    ctrl01_direction=0,
                                    ctrl02_direction=0,
                                    ctrl03_direction=0,
                                    ctrl04_direction=0,
                                    ctrl05_direction=0,
                                    ctrl_color='lightPink',
                                    shape=rlu_controller.JOINT,
                                    scale=scale,
                                    head_ctrl_gimbal=head.head_ctrl_gimbal,
                                    head_up_ctrl_gimbal=head.head_up_ctrl_gimbal,
                                    head_jnt=sj.head,
                                    position_mouth_ctrl=position_mouth_ctrl,
                                    side_LFT=side_LFT,
                                    side_RGT=side_RGT,
                                    lip_corner_ctrl_LFT=lip.corner_lip_ctrl_LFT,
                                    lip_corner_ctrl_RGT=lip.corner_lip_ctrl_RGT,
                                    nostril_attr_ctrl_LFT=lip.nostril_attr_ctrl_LFT,
                                    nostril_attr_ctrl_RGT=lip.nostril_attr_ctrl_RGT,
                                    up_lip_controller_all=lip.up_lip_controller_all,
                                    mouth_ctrl=lip.mouth_ctrl,
                                    nose_follow_mouth_value=nose_follow_mouth_value,
                                    jaw_ctrl=head.jaw_ctrl,
                                    suffix_controller=suffix_controller,
                                    base_module_nonTransform=face_non_transform_grp,
                                    mouth_ctrl_nose_follow=lip.mouth_ctrl_nose_follow,
                                    game_bind_joint=game_bind_joint,
                                    parent_sgame_joint=sGame.head
                                    )

        print('25% | nose is done!')
    else:
        nose = rlmf_noseModule.Nose(face_utils_grp=face_non_transform_grp,
                                    columella_jnt=sj.columella,
                                    nose_jnt=sj.nose,
                                    nose_up_jnt=sj.nose_up,
                                    columella_prefix=columella_prefix,
                                    curve_template_nose=curve_template_nose,
                                    offset_jnt02_bind_position=offset_jnt02_bind_lip_nose_position,
                                    offset_jnt04_bind_position=offset_jnt04_bind_lip_nose_position,
                                    ctrl01_direction=0,
                                    ctrl02_direction=0,
                                    ctrl03_direction=0,
                                    ctrl04_direction=0,
                                    ctrl05_direction=0,
                                    ctrl_color='lightPink',
                                    shape=rlu_controller.JOINT,
                                    scale=scale,
                                    head_ctrl_gimbal=head.head_ctrl_gimbal,
                                    head_up_ctrl_gimbal=head.head_up_ctrl_gimbal,
                                    head_jnt=sj.head,
                                    position_mouth_ctrl=position_mouth_ctrl,
                                    side_LFT=side_LFT,
                                    side_RGT=side_RGT,
                                    lip_corner_ctrl_LFT=lip.corner_lip_ctrl_LFT,
                                    lip_corner_ctrl_RGT=lip.corner_lip_ctrl_RGT,
                                    nostril_attr_ctrl_LFT=lip.nostril_attr_ctrl_LFT,
                                    nostril_attr_ctrl_RGT=lip.nostril_attr_ctrl_RGT,
                                    up_lip_controller_all=lip.up_lip_controller_all,
                                    mouth_ctrl=lip.mouth_ctrl,
                                    nose_follow_mouth_value=nose_follow_mouth_value,
                                    jaw_ctrl=head.jaw_ctrl,
                                    suffix_controller=suffix_controller,
                                    base_module_nonTransform=face_non_transform_grp,
                                    mouth_ctrl_nose_follow=lip.mouth_ctrl_nose_follow,
                                    )

        print('25% | nose is done!')
    # ==================================================================================================================
    #                                                     CHEEK PARAMETERS
    # ==================================================================================================================

    leftCheek = rlmf_cheekModule.Cheek(face_anim_ctrl_grp=face_controller_grp,
                                       face_utils_grp=face_non_transform_grp,
                                       cheek_low_jnt=sj.cheek_low_LFT,
                                       cheek_low_prefix=cheek_low_prefix,
                                       cheek_mid_jnt=sj.cheek_mid_LFT,
                                       cheek_mid_prefix=cheek_mid_prefix,
                                       cheek_up_jnt=sj.cheek_up_LFT,
                                       cheek_up_prefix=cheek_up_prefix,
                                       cheek_in_up_jnt=sj.cheek_in_up_LFT,
                                       cheek_in_up_prefix=cheek_in_up_prefix,
                                       cheek_in_low_jnt=sj.cheek_in_low_LFT,
                                       cheek_in_low_prefix=cheek_in_low_prefix,
                                       cheek_out_up_jnt=sj.cheek_out_up_LFT,
                                       cheek_out_up_prefix=cheek_out_up_prefix,
                                       cheek_out_low_jnt=sj.cheek_out_low_LFT,
                                       cheek_out_low_prefix=cheek_out_low_prefix,
                                       scale=scale,
                                       side=side_LFT,
                                       side_LFT=side_LFT,
                                       side_RGT=side_RGT,
                                       lip_drive_ctrl=lip.up_lip_controller_all,
                                       mouth_ctrl=lip.mouth_ctrl,
                                       mouth_cheek_in_up_attr=lip.cheek_in_up_attr,
                                       head_low_jnt=sj.head_low,
                                       head_up_jnt=sj.head_up,
                                       jaw_jnt=sj.jaw,
                                       corner_lip_ctrl=lip.corner_lip_ctrl_LFT,
                                       corner_lip_ctrl_attr_cheek_low=lip.cheek_low_attr_ctrl_LFT,
                                       corner_lip_ctrl_attr_cheek_mid=lip.cheek_mid_attr_ctrl_LFT,
                                       low_lip_drive_ctrl=lip.low_reset_mouth_ctrl_grp_offset,
                                       nostril_drive_ctrl_attr_cheek_up=nose.pull_forward_LFT,
                                       nostril_drive_ctrl_attr_cheek_up_two=nose.push_upward_LFT,
                                       nostril_drive_ctrl=nose.controller_nose01_LFT,
                                       corner_lip_ctrl_attr_cheek_out_up=lip.cheek_out_up_attr_ctrl_LFT,
                                       corner_lip_ctrl_attr_cheek_out_low=lip.cheek_out_low_attr_ctrl_LFT,
                                       head_up_ctrl=head.head_up_ctrl,
                                       head_low_ctrl=head.head_low_ctrl,
                                       suffix_controller=suffix_controller,
                                       )

    print('30% | left cheek is done!')

    rightCheek = rlmf_cheekModule.Cheek(face_anim_ctrl_grp=face_controller_grp,
                                        face_utils_grp=face_non_transform_grp,
                                        cheek_low_jnt=sj.cheek_low_RGT,
                                        cheek_low_prefix=cheek_low_prefix,
                                        cheek_mid_jnt=sj.cheek_mid_RGT,
                                        cheek_mid_prefix=cheek_mid_prefix,
                                        cheek_up_jnt=sj.cheek_up_RGT,
                                        cheek_up_prefix=cheek_up_prefix,
                                        cheek_in_up_jnt=sj.cheek_in_up_RGT,
                                        cheek_in_up_prefix=cheek_in_up_prefix,
                                        cheek_in_low_jnt=sj.cheek_in_low_RGT,
                                        cheek_in_low_prefix=cheek_in_low_prefix,
                                        cheek_out_up_jnt=sj.cheek_out_up_RGT,
                                        cheek_out_up_prefix=cheek_out_up_prefix,
                                        cheek_out_low_jnt=sj.cheek_out_low_RGT,
                                        cheek_out_low_prefix=cheek_out_low_prefix,
                                        scale=scale,
                                        side=side_RGT,
                                        side_LFT=side_LFT,
                                        side_RGT=side_RGT,
                                        lip_drive_ctrl=lip.up_lip_controller_all,
                                        mouth_ctrl=lip.mouth_ctrl,
                                        mouth_cheek_in_up_attr=lip.cheek_in_up_attr,
                                        head_low_jnt=sj.head_low,
                                        head_up_jnt=sj.head_up,
                                        jaw_jnt=sj.jaw,
                                        corner_lip_ctrl=lip.corner_lip_ctrl_RGT,
                                        corner_lip_ctrl_attr_cheek_low=lip.cheek_low_attr_ctrl_RGT,
                                        corner_lip_ctrl_attr_cheek_mid=lip.cheek_mid_attr_ctrl_RGT,
                                        low_lip_drive_ctrl=lip.low_reset_mouth_ctrl_grp_offset,
                                        nostril_drive_ctrl_attr_cheek_up=nose.pull_forward_RGT,
                                        nostril_drive_ctrl_attr_cheek_up_two=nose.push_upward_RGT,
                                        nostril_drive_ctrl=nose.controller_nose01_RGT,
                                        corner_lip_ctrl_attr_cheek_out_up=lip.cheek_out_up_attr_ctrl_RGT,
                                        corner_lip_ctrl_attr_cheek_out_low=lip.cheek_out_low_attr_ctrl_RGT,
                                        head_up_ctrl=head.head_up_ctrl,
                                        head_low_ctrl=head.head_low_ctrl,
                                        suffix_controller=suffix_controller,
                                        )

    print('40% | right cheek is done!')

    # ==================================================================================================================
    #                                                     EARS PARAMETERS
    # ==================================================================================================================
    earLeft = rlmf_earModule.Ear(scale=scale,
                                 ear_jnt=sj.ear_LFT,
                                 ear_prefix=ear_prefix,
                                 head_ctrl_gimbal=head.head_ctrl_gimbal,
                                 side=side_LFT,
                                 side_LFT=side_LFT,
                                 side_RGT=side_RGT,
                                 suffix_controller=suffix_controller)

    earRight = rlmf_earModule.Ear(scale=scale,
                                  ear_jnt=sj.ear_RGT,
                                  ear_prefix=ear_prefix,
                                  head_ctrl_gimbal=head.head_ctrl_gimbal,
                                  side=side_RGT,
                                  side_LFT=side_LFT,
                                  side_RGT=side_RGT,
                                  suffix_controller=suffix_controller)
    # ==================================================================================================================
    #                                                     CHIN PARAMETERS
    # ==================================================================================================================
    chin = rlmf_chinModule.Chin(mentolabial_jnt=sj.mentolabial,
                                mentolabial_prefix=mentolabial_prefix,
                                chin_jnt=sj.chin,
                                chin_prefix=chin_prefix,
                                scale=scale,
                                face_anim_ctrl_grp=face_controller_grp,
                                face_utils_grp=face_non_transform_grp,
                                lower_lip_bind_jnt=lip.low_bind_jnt,
                                jaw_jnt=sj.jaw,
                                suffix_controller=suffix_controller)

    print('50% | chin is done!')

    # ==================================================================================================================
    #                                                     EYELID PARAMETERS
    # ==================================================================================================================
    if game_bind_joint:
        leftEyelid = rlmf_lidModule.Lid(
            face_utils_grp=face_non_transform_grp,
            curve_up_lid_template=curve_up_lid_template_LFT,
            curve_low_lid_template=curve_low_lid_template_LFT,
            offset_lid02_position=lid02_position_offset,
            offset_lid04_position=lid04_position_offset,
            eyeball_jnt=sj.eyeball_LFT,
            eye_jnt=sj.eye_LFT,
            suffix_controller=suffix_controller,
            prefix_eye=eye_prefix,
            prefix_eye_aim=eye_aim_prefix,
            scale=scale,
            side=side_LFT,
            side_LFT=side_LFT,
            side_RGT=side_RGT,
            lid01_direction=lid01_direction,
            lid02_direction=lid02_direction,
            lid03_direction=lid03_direction,
            lid04_direction=lid04_direction,
            lid05_direction=lid05_direction,
            position_eye_aim_ctrl=position_eye_aim_ctrl,
            eye_aim_main_ctrl=head.eyeAimMainCtrl,
            head_up_ctrl_gimbal=head.head_up_ctrl_gimbal,
            corner_lip=lip.corner_lip_ctrl_LFT,
            corner_lip_lid_attr=lip.lid_attr_ctrl_LFT,
            low_lid_following_down=low_lid_following_down,
            upLid_following_down_lowLid_following_up=up_lid_following_down_low_lid_following_up,
            upLid_LR_lowLid_LR=up_lid_LR_low_lid_LR,
            upLid_following_up=up_lid_following_up,
            upper_head_gimbal_ctrl=head.head_up_ctrl_gimbal,
            pupil_jnt=sj.pupil_LFT,
            iris_jnt=sj.iris_LFT,
            pupil_prefix=pupil_prefix,
            iris_prefix=iris_prefix,
            eye_ctrl_direction=eye_ctrl_direction,
            base_module_nonTransform=face_non_transform_grp,
            game_bind_joint=game_bind_joint,
            parent_sgame_joint=sGame.eye_LFT
        )

        print('60% | left eyelid is done!')

        rightEyelid = rlmf_lidModule.Lid(
            face_utils_grp=face_non_transform_grp,
            curve_up_lid_template=curve_up_lid_template_RGT,
            curve_low_lid_template=curve_low_lid_template_RGT,
            offset_lid02_position=lid02_position_offset,
            offset_lid04_position=lid04_position_offset,
            eyeball_jnt=sj.eyeball_RGT,
            eye_jnt=sj.eye_RGT,
            suffix_controller=suffix_controller,
            prefix_eye=eye_prefix,
            prefix_eye_aim=eye_aim_prefix,
            scale=scale,
            side=side_RGT,
            side_LFT=side_LFT,
            side_RGT=side_RGT,
            lid01_direction=lid01_direction,
            lid02_direction=lid02_direction,
            lid03_direction=lid03_direction,
            lid04_direction=lid04_direction,
            lid05_direction=lid05_direction,
            position_eye_aim_ctrl=position_eye_aim_ctrl,
            eye_aim_main_ctrl=head.eyeAimMainCtrl,
            head_up_ctrl_gimbal=head.head_up_ctrl_gimbal,
            corner_lip=lip.corner_lip_ctrl_RGT,
            corner_lip_lid_attr=lip.lid_attr_ctrl_RGT,
            low_lid_following_down=low_lid_following_down,
            upLid_following_down_lowLid_following_up=up_lid_following_down_low_lid_following_up,
            upLid_LR_lowLid_LR=up_lid_LR_low_lid_LR,
            upLid_following_up=up_lid_following_up,
            upper_head_gimbal_ctrl=head.head_up_ctrl_gimbal,
            pupil_jnt=sj.pupil_RGT,
            iris_jnt=sj.iris_RGT,
            pupil_prefix=pupil_prefix,
            iris_prefix=iris_prefix,
            eye_ctrl_direction=eye_ctrl_direction,
            base_module_nonTransform=face_non_transform_grp,
            game_bind_joint=game_bind_joint,
            parent_sgame_joint=sGame.eye_RGT
        )

        print('70% | right eyelid is done!')

    else:
        leftEyelid = rlmf_lidModule.Lid(
            face_utils_grp=face_non_transform_grp,
            curve_up_lid_template=curve_up_lid_template_LFT,
            curve_low_lid_template=curve_low_lid_template_LFT,
            offset_lid02_position=lid02_position_offset,
            offset_lid04_position=lid04_position_offset,
            eyeball_jnt=sj.eyeball_LFT,
            eye_jnt=sj.eye_LFT,
            suffix_controller=suffix_controller,
            prefix_eye=eye_prefix,
            prefix_eye_aim=eye_aim_prefix,
            scale=scale,
            side=side_LFT,
            side_LFT=side_LFT,
            side_RGT=side_RGT,
            lid01_direction=lid01_direction,
            lid02_direction=lid02_direction,
            lid03_direction=lid03_direction,
            lid04_direction=lid04_direction,
            lid05_direction=lid05_direction,
            position_eye_aim_ctrl=position_eye_aim_ctrl,
            eye_aim_main_ctrl=head.eyeAimMainCtrl,
            head_up_ctrl_gimbal=head.head_up_ctrl_gimbal,
            corner_lip=lip.corner_lip_ctrl_LFT,
            corner_lip_lid_attr=lip.lid_attr_ctrl_LFT,
            low_lid_following_down=low_lid_following_down,
            upLid_following_down_lowLid_following_up=up_lid_following_down_low_lid_following_up,
            upLid_LR_lowLid_LR=up_lid_LR_low_lid_LR,
            upLid_following_up=up_lid_following_up,
            upper_head_gimbal_ctrl=head.head_up_ctrl_gimbal,
            pupil_jnt=sj.pupil_LFT,
            iris_jnt=sj.iris_LFT,
            pupil_prefix=pupil_prefix,
            iris_prefix=iris_prefix,
            eye_ctrl_direction=eye_ctrl_direction,
            base_module_nonTransform=face_non_transform_grp
        )

        print('60% | left eyelid is done!')

        rightEyelid = rlmf_lidModule.Lid(
            face_utils_grp=face_non_transform_grp,
            curve_up_lid_template=curve_up_lid_template_RGT,
            curve_low_lid_template=curve_low_lid_template_RGT,
            offset_lid02_position=lid02_position_offset,
            offset_lid04_position=lid04_position_offset,
            eyeball_jnt=sj.eyeball_RGT,
            eye_jnt=sj.eye_RGT,
            suffix_controller=suffix_controller,
            prefix_eye=eye_prefix,
            prefix_eye_aim=eye_aim_prefix,
            scale=scale,
            side=side_RGT,
            side_LFT=side_LFT,
            side_RGT=side_RGT,
            lid01_direction=lid01_direction,
            lid02_direction=lid02_direction,
            lid03_direction=lid03_direction,
            lid04_direction=lid04_direction,
            lid05_direction=lid05_direction,
            position_eye_aim_ctrl=position_eye_aim_ctrl,
            eye_aim_main_ctrl=head.eyeAimMainCtrl,
            head_up_ctrl_gimbal=head.head_up_ctrl_gimbal,
            corner_lip=lip.corner_lip_ctrl_RGT,
            corner_lip_lid_attr=lip.lid_attr_ctrl_RGT,
            low_lid_following_down=low_lid_following_down,
            upLid_following_down_lowLid_following_up=up_lid_following_down_low_lid_following_up,
            upLid_LR_lowLid_LR=up_lid_LR_low_lid_LR,
            upLid_following_up=up_lid_following_up,
            upper_head_gimbal_ctrl=head.head_up_ctrl_gimbal,
            pupil_jnt=sj.pupil_RGT,
            iris_jnt=sj.iris_RGT,
            pupil_prefix=pupil_prefix,
            iris_prefix=iris_prefix,
            eye_ctrl_direction=eye_ctrl_direction,
            base_module_nonTransform=face_non_transform_grp,
        )

        print('70% | right eyelid is done!')

    # ==================================================================================================================
    #                                                     EYELID OUT PARAMETERS
    # ==================================================================================================================
    if game_bind_joint:
        leftLidOut = rlmf_lidOutModule.LidOut(face_utils_grp=face_non_transform_grp,
                                              curve_up_template=curve_up_lid_out_LFT,
                                              curve_low_template=curve_low_lid_out_LFT,
                                              offset_jnt02_bind_position=jnt02_bind_lip_lid_out_position_offset,
                                              offset_jnt04_bind_position=jnt04_bind_lip_lid_out_position_offset,
                                              ctrl01_direction=lid01_out_ctrl_direction,
                                              ctrl02_direction=lid02_out_ctrl_direction,
                                              ctrl03_direction=lid03_out_ctrl_direction,
                                              ctrl04_direction=lid04_out_ctrl_direction,
                                              ctrl05_direction=lid05_out_ctrl_direction,
                                              ctrl_color='blue',
                                              shape=rlu_controller.JOINT,
                                              scale=scale,
                                              side_RGT=side_RGT,
                                              side_LFT=side_LFT,
                                              side=side_LFT,
                                              eyeball_jnt=sj.eyeball_LFT,
                                              head_up_jnt=sj.head_up,
                                              eye_ctrl=leftEyelid.eyeball_controller,
                                              corner_lip=lip.corner_lip_ctrl_LFT,
                                              corner_lip_attr=lip.lid_out_attr_ctrl_LFT,
                                              ctrl_bind01_up=leftEyelid.up_lid_bind01_ctrl,
                                              ctrl_bind02_up=leftEyelid.up_lid_bind02_ctrl,
                                              ctrl_bind03_up=leftEyelid.up_lid_bind03_ctrl,
                                              ctrl_bind04_up=leftEyelid.up_lid_bind04_ctrl,
                                              ctrl_bind05_up=leftEyelid.up_lid_bind05_ctrl,
                                              ctrl_bind01_low=leftEyelid.low_lid_bind01_ctrl,
                                              ctrl_bind02_low=leftEyelid.low_lid_bind02_ctrl,
                                              ctrl_bind03_low=leftEyelid.low_lid_bind03_ctrl,
                                              ctrl_bind04_low=leftEyelid.low_lid_bind04_ctrl,
                                              ctrl_bind05_low=leftEyelid.low_lid_bind05_ctrl,
                                              lid_out_follow=leftEyelid.lid_out_up03_follow_attr,
                                              close_lid_up_attr=leftEyelid.upLid_closer,
                                              close_lid_low_attr=leftEyelid.lowLid_closer,
                                              eyeball_ctrl=leftEyelid.eyeball_controller,
                                              lid_corner_in_ctrl=leftEyelid.lid_corner_in_ctrl,
                                              lid_corner_out_ctrl=leftEyelid.lid_corner_out_ctrl,
                                              wire_up_bind01_grp_offset=leftEyelid.up_lid_bind01_grp_offset,
                                              wire_low_bind01_grp_offset=leftEyelid.low_lid_bind01_grp_offset,
                                              wire_up_bind05_grp_offset=leftEyelid.up_lid_bind05_grp_offset,
                                              wire_low_bind05_grp_offset=leftEyelid.low_lid_bind05_grp_offset,
                                              lid_out_on_off_follow_trans_mdn=leftEyelid.lid_out_eye_ctrl_trans,
                                              lid_out_on_off_follow_rot_mdn=leftEyelid.lid_out_eye_ctrl_rotate,
                                              eye_ctrl_direction=eye_ctrl_direction,
                                              suffix_controller=suffix_controller,
                                              base_module_nonTransform=face_non_transform_grp,
                                              game_bind_joint=game_bind_joint,
                                              parent_sgame_joint=sGame.head_up
                                              )

        print('80% | left lid out is done!')

        rightLidOut = rlmf_lidOutModule.LidOut(face_utils_grp=face_non_transform_grp,
                                               curve_up_template=curve_up_lid_out_RGT,
                                               curve_low_template=curve_low_lid_out_RGT,
                                               offset_jnt02_bind_position=jnt02_bind_lip_lid_out_position_offset,
                                               offset_jnt04_bind_position=jnt04_bind_lip_lid_out_position_offset,
                                               ctrl01_direction=lid01_out_ctrl_direction,
                                               ctrl02_direction=lid02_out_ctrl_direction,
                                               ctrl03_direction=lid03_out_ctrl_direction,
                                               ctrl04_direction=lid04_out_ctrl_direction,
                                               ctrl05_direction=lid05_out_ctrl_direction,
                                               ctrl_color='blue',
                                               shape=rlu_controller.JOINT,
                                               scale=scale,
                                               side_RGT=side_RGT,
                                               side_LFT=side_LFT,
                                               side=side_RGT,
                                               eyeball_jnt=sj.eyeball_RGT,
                                               head_up_jnt=sj.head_up,
                                               eye_ctrl=rightEyelid.eyeball_controller,
                                               corner_lip=lip.corner_lip_ctrl_RGT,
                                               corner_lip_attr=lip.lid_out_attr_ctrl_RGT,
                                               eyeball_ctrl=rightEyelid.eyeball_controller,
                                               ctrl_bind01_up=rightEyelid.up_lid_bind01_ctrl,
                                               ctrl_bind02_up=rightEyelid.up_lid_bind02_ctrl,
                                               ctrl_bind03_up=rightEyelid.up_lid_bind03_ctrl,
                                               ctrl_bind04_up=rightEyelid.up_lid_bind04_ctrl,
                                               ctrl_bind05_up=rightEyelid.up_lid_bind05_ctrl,
                                               ctrl_bind01_low=rightEyelid.low_lid_bind01_ctrl,
                                               ctrl_bind02_low=rightEyelid.low_lid_bind02_ctrl,
                                               ctrl_bind03_low=rightEyelid.low_lid_bind03_ctrl,
                                               ctrl_bind04_low=rightEyelid.low_lid_bind04_ctrl,
                                               ctrl_bind05_low=rightEyelid.low_lid_bind05_ctrl,
                                               lid_out_follow=rightEyelid.lid_out_up03_follow_attr,
                                               close_lid_up_attr=rightEyelid.upLid_closer,
                                               close_lid_low_attr=rightEyelid.lowLid_closer,
                                               lid_corner_in_ctrl=rightEyelid.lid_corner_in_ctrl,
                                               lid_corner_out_ctrl=rightEyelid.lid_corner_out_ctrl,
                                               wire_up_bind01_grp_offset=rightEyelid.up_lid_bind01_grp_offset,
                                               wire_low_bind01_grp_offset=rightEyelid.low_lid_bind01_grp_offset,
                                               wire_up_bind05_grp_offset=rightEyelid.up_lid_bind05_grp_offset,
                                               wire_low_bind05_grp_offset=rightEyelid.low_lid_bind05_grp_offset,
                                               lid_out_on_off_follow_trans_mdn=rightEyelid.lid_out_eye_ctrl_trans,
                                               lid_out_on_off_follow_rot_mdn=rightEyelid.lid_out_eye_ctrl_rotate,
                                               eye_ctrl_direction=eye_ctrl_direction,
                                               suffix_controller=suffix_controller,
                                               base_module_nonTransform=face_non_transform_grp,
                                               game_bind_joint=game_bind_joint,
                                               parent_sgame_joint=sGame.head_up
                                               )
        print('90% | right lid out is done!')
    else:
        leftLidOut = rlmf_lidOutModule.LidOut(face_utils_grp=face_non_transform_grp,
                                              curve_up_template=curve_up_lid_out_LFT,
                                              curve_low_template=curve_low_lid_out_LFT,
                                              offset_jnt02_bind_position=jnt02_bind_lip_lid_out_position_offset,
                                              offset_jnt04_bind_position=jnt04_bind_lip_lid_out_position_offset,
                                              ctrl01_direction=lid01_out_ctrl_direction,
                                              ctrl02_direction=lid02_out_ctrl_direction,
                                              ctrl03_direction=lid03_out_ctrl_direction,
                                              ctrl04_direction=lid04_out_ctrl_direction,
                                              ctrl05_direction=lid05_out_ctrl_direction,
                                              ctrl_color='blue',
                                              shape=rlu_controller.JOINT,
                                              scale=scale,
                                              side_RGT=side_RGT,
                                              side_LFT=side_LFT,
                                              side=side_LFT,
                                              eyeball_jnt=sj.eyeball_LFT,
                                              head_up_jnt=sj.head_up,
                                              eye_ctrl=leftEyelid.eyeball_controller,
                                              corner_lip=lip.corner_lip_ctrl_LFT,
                                              corner_lip_attr=lip.lid_out_attr_ctrl_LFT,
                                              ctrl_bind01_up=leftEyelid.up_lid_bind01_ctrl,
                                              ctrl_bind02_up=leftEyelid.up_lid_bind02_ctrl,
                                              ctrl_bind03_up=leftEyelid.up_lid_bind03_ctrl,
                                              ctrl_bind04_up=leftEyelid.up_lid_bind04_ctrl,
                                              ctrl_bind05_up=leftEyelid.up_lid_bind05_ctrl,
                                              ctrl_bind01_low=leftEyelid.low_lid_bind01_ctrl,
                                              ctrl_bind02_low=leftEyelid.low_lid_bind02_ctrl,
                                              ctrl_bind03_low=leftEyelid.low_lid_bind03_ctrl,
                                              ctrl_bind04_low=leftEyelid.low_lid_bind04_ctrl,
                                              ctrl_bind05_low=leftEyelid.low_lid_bind05_ctrl,
                                              lid_out_follow=leftEyelid.lid_out_up03_follow_attr,
                                              close_lid_up_attr=leftEyelid.upLid_closer,
                                              eyeball_ctrl=leftEyelid.eyeball_controller,
                                              lid_corner_in_ctrl=leftEyelid.lid_corner_in_ctrl,
                                              lid_corner_out_ctrl=leftEyelid.lid_corner_out_ctrl,
                                              wire_up_bind01_grp_offset=leftEyelid.up_lid_bind01_grp_offset,
                                              wire_low_bind01_grp_offset=leftEyelid.low_lid_bind01_grp_offset,
                                              wire_up_bind05_grp_offset=leftEyelid.up_lid_bind05_grp_offset,
                                              wire_low_bind05_grp_offset=leftEyelid.low_lid_bind05_grp_offset,
                                              lid_out_on_off_follow_trans_mdn=leftEyelid.lid_out_eye_ctrl_trans,
                                              lid_out_on_off_follow_rot_mdn=leftEyelid.lid_out_eye_ctrl_rotate,
                                              eye_ctrl_direction=eye_ctrl_direction,
                                              suffix_controller=suffix_controller,
                                              base_module_nonTransform=face_non_transform_grp
                                              )

        print('80% | left lid out is done!')

        rightLidOut = rlmf_lidOutModule.LidOut(face_utils_grp=face_non_transform_grp,
                                               curve_up_template=curve_up_lid_out_RGT,
                                               curve_low_template=curve_low_lid_out_RGT,
                                               offset_jnt02_bind_position=jnt02_bind_lip_lid_out_position_offset,
                                               offset_jnt04_bind_position=jnt04_bind_lip_lid_out_position_offset,
                                               ctrl01_direction=lid01_out_ctrl_direction,
                                               ctrl02_direction=lid02_out_ctrl_direction,
                                               ctrl03_direction=lid03_out_ctrl_direction,
                                               ctrl04_direction=lid04_out_ctrl_direction,
                                               ctrl05_direction=lid05_out_ctrl_direction,
                                               ctrl_color='blue',
                                               shape=rlu_controller.JOINT,
                                               scale=scale,
                                               side_RGT=side_RGT,
                                               side_LFT=side_LFT,
                                               side=side_RGT,
                                               eyeball_jnt=sj.eyeball_RGT,
                                               head_up_jnt=sj.head_up,
                                               eye_ctrl=rightEyelid.eyeball_controller,
                                               corner_lip=lip.corner_lip_ctrl_RGT,
                                               corner_lip_attr=lip.lid_out_attr_ctrl_RGT,
                                               eyeball_ctrl=rightEyelid.eyeball_controller,
                                               ctrl_bind01_up=rightEyelid.up_lid_bind01_ctrl,
                                               ctrl_bind02_up=rightEyelid.up_lid_bind02_ctrl,
                                               ctrl_bind03_up=rightEyelid.up_lid_bind03_ctrl,
                                               ctrl_bind04_up=rightEyelid.up_lid_bind04_ctrl,
                                               ctrl_bind05_up=rightEyelid.up_lid_bind05_ctrl,
                                               ctrl_bind01_low=rightEyelid.low_lid_bind01_ctrl,
                                               ctrl_bind02_low=rightEyelid.low_lid_bind02_ctrl,
                                               ctrl_bind03_low=rightEyelid.low_lid_bind03_ctrl,
                                               ctrl_bind04_low=rightEyelid.low_lid_bind04_ctrl,
                                               ctrl_bind05_low=rightEyelid.low_lid_bind05_ctrl,
                                               lid_out_follow=rightEyelid.lid_out_up03_follow_attr,
                                               close_lid_up_attr=rightEyelid.upLid_closer,
                                               lid_corner_in_ctrl=rightEyelid.lid_corner_in_ctrl,
                                               lid_corner_out_ctrl=rightEyelid.lid_corner_out_ctrl,
                                               wire_up_bind01_grp_offset=rightEyelid.up_lid_bind01_grp_offset,
                                               wire_low_bind01_grp_offset=rightEyelid.low_lid_bind01_grp_offset,
                                               wire_up_bind05_grp_offset=rightEyelid.up_lid_bind05_grp_offset,
                                               wire_low_bind05_grp_offset=rightEyelid.low_lid_bind05_grp_offset,
                                               lid_out_on_off_follow_trans_mdn=rightEyelid.lid_out_eye_ctrl_trans,
                                               lid_out_on_off_follow_rot_mdn=rightEyelid.lid_out_eye_ctrl_rotate,
                                               eye_ctrl_direction=eye_ctrl_direction,
                                               suffix_controller=suffix_controller,
                                               base_module_nonTransform=face_non_transform_grp,
                                               )
        print('90% | right lid out is done!')

    # ==================================================================================================================
    #                                                     BROWS PARAMETERS
    # ==================================================================================================================

    brows = rlmf_browModule.Brows(brow_tweak_jnt_LFT=sj.brow_tweak_LFT,
                                  brow_in_jnt_LFT=sj.brow_in_LFT,
                                  brow_mid_jnt_LFT=sj.brow_mid_LFT,
                                  brow_out_jnt_LFT=sj.brow_out_LFT,
                                  brow_tip_jnt_LFT=sj.brow_tip_LFT,
                                  brow_tweak_jnt_RGT=sj.brow_tweak_RGT,
                                  brow_in_jnt_RGT=sj.brow_in_RGT,
                                  brow_mid_jnt_RGT=sj.brow_mid_RGT,
                                  brow_out_jnt_RGT=sj.brow_out_RGT,
                                  brow_tip_jnt_RGT=sj.brow_tip_RGT,
                                  brow_center_jnt=sj.brow_center,
                                  brow_tweak_prefix=brow_tweak_prefix,
                                  brow_in_prefix=brow_in_prefix,
                                  brow_mid_prefix=brow_mid_prefix,
                                  brow_out_prefix=brow_out_prefix,
                                  brows_prefix=brows_prefix,
                                  brow_tip_prefix=brow_tip_prefix,
                                  brow_center_prefix=brow_center_prefix,
                                  scale=scale,
                                  side_RGT=side_RGT,
                                  side_LFT=side_LFT,
                                  brow_in_rotate_grp_offset=brow_in_rotation_grp_offset,
                                  brow_mid_rotate_grp_offset=brow_mid_rotation_grp_offset,
                                  brow_out_rotate_grp_offset=brow_out_rotation_grp_offset,
                                  brow_tip_rotate_grp_offset=brow_tip_rotation_grp_offset,
                                  head_up_ctrl_gimbal=head.head_up_ctrl_gimbal,
                                  suffix_controller=suffix_controller)
    # ==================================================================================================================
    #                                                     BULGE PARAMETERS
    # ==================================================================================================================
    if bulge:
        bulge = rlmf_bulgeModule.Bulge(face_utils_grp=face_non_transform_grp,
                                       face_anim_ctrl_grp=face_controller_grp,
                                       cheek_bulge_jnt_LFT=sj.cheek_bulge_LFT,
                                       cheek_bulge_prefix=cheek_mid_prefix,
                                       cheek_bulge_jnt_RGT=sj.cheek_bulge_RGT,
                                       brow_in_bulge_prefix=brow_in_prefix,
                                       brow_out_bulge_prefix=brow_out_prefix,
                                       corner_mouth_bulge_prefix='cornerMouth',
                                       nose_bulge_prefix='nose',
                                       chin_bulge_prefix=chin_prefix,
                                       brow_in_bulge_jnt_LFT=sj.brow_in_LFT,
                                       brow_in_bulge_jnt_RGT=sj.brow_in_RGT,
                                       brow_out_bulge_jnt_LFT=sj.brow_out_LFT,
                                       brow_out_bulge_jnt_RGT=sj.brow_out_RGT,
                                       corner_mouth_bulge_jnt_LFT=lip.corner_lip_ctrl_LFT,
                                       corner_mouth_bulge_jnt_RGT=lip.corner_lip_ctrl_RGT,
                                       nose_bulge_jnt=nose.controller_nose03,
                                       chin_bulge_jnt=sj.chin,
                                       bulge_mesh=bulge_mesh,
                                       side_LFT=side_LFT,
                                       side_RGT=side_RGT,
                                       head_up_ctrl_gimbal=head.head_up_ctrl_gimbal,
                                       head_low_ctrl_gimbal=head.head_low_ctrl_gimbal,
                                       nose_drv03_ctrl=nose.controller_nose03,
                                       chin_ctrl=chin.chin_ctrl,
                                       corner_mouth_ctrl_LFT=lip.corner_lip_ctrl_LFT,
                                       corner_mouth_ctrl_RGT=lip.corner_lip_ctrl_RGT,
                                       scale=scale,
                                       add_set=add_set_bulge,
                                       follicle_mesh=follicle_mesh)

        print('100% | brows is done!')

    # ==================================================================================================================
    #                                         SETUP VISIBILITY CONTROLLER
    # ==================================================================================================================
    setupCtrl = rlu_controller.Control(prefix='setup', match_obj_first_position=sj.head,
                                       shape=rlu_controller.SETUP, groups_ctrl=[''], ctrl_size=scale * 0.12,
                                       ctrl_color='blue', lock_channels=['v', 't', 's', 'r']
                                       )
    # # HAIR VIS
    # hairVis = au.connect_part_object(obj_base_connection='hairVis', target_connection='visibility', obj_name=setupCtrl.control,
    #                                  target_name=['hair_geo', 'hairMainGeoCtrl_grp'], channel_box=True, select_obj=False)

    # MAIN CHEEK VIS
    mainCheekCtrlVis = rt_utils.connect_part_object(obj_base_connection='mainCheekCtrlVis',
                                                    target_connection='visibility',
                                                    obj_name=setupCtrl.control,
                                                    target_name=[leftCheek.cheek_low_ctrl_grp,
                                                                 leftCheek.cheek_mid_ctrl_grp,
                                                                 leftCheek.cheek_out_up_ctrl_grp,
                                                                 leftCheek.cheek_out_low_ctrl_grp,
                                                                 rightCheek.cheek_low_ctrl_grp,
                                                                 rightCheek.cheek_mid_ctrl_grp,
                                                                 rightCheek.cheek_out_up_ctrl_grp,
                                                                 rightCheek.cheek_out_low_ctrl_grp],
                                                    channel_box=True, select_obj=False)

    # SECONDARY CHEEK VIS
    secondaryCheekCtrlVis = rt_utils.connect_part_object(obj_base_connection='secondaryCheekCtrlVis',
                                                         target_connection='visibility', obj_name=setupCtrl.control,
                                                         target_name=[leftCheek.cheek_up_ctrl_grp,
                                                                      leftCheek.cheek_in_up_ctrl_grp,
                                                                      leftCheek.cheek_in_low_ctrl_grp,
                                                                      rightCheek.cheek_up_ctrl_grp,
                                                                      rightCheek.cheek_in_up_ctrl_grp,
                                                                      rightCheek.cheek_in_low_ctrl_grp],
                                                         channel_box=True, select_obj=False)

    # CHIN VIS
    chinCtrlVis = rt_utils.connect_part_object(obj_base_connection='chinCtrlVis', target_connection='visibility',
                                               obj_name=setupCtrl.control,
                                               target_name=[chin.chin_ctrl_grp,
                                                            chin.mentolabial_ctrl_grp],
                                               channel_box=True, select_obj=False)

    # LIP VIS
    mouthCtrlVis = rt_utils.connect_part_object(obj_base_connection='mouthCtrlVis', target_connection='visibility',
                                                obj_name=setupCtrl.control,
                                                target_name=[lip.controller_grp], channel_box=True, select_obj=False)

    # NOSE VIS
    noseCtrlVis = rt_utils.connect_part_object(obj_base_connection='noseCtrlVis', target_connection='visibility',
                                               obj_name=setupCtrl.control,
                                               target_name=[nose.nose_controller_grp, nose.nose_ctrl_grp_zro,
                                                            nose.nose_up_controller_grp], channel_box=True,
                                               select_obj=False)

    # EYE VIS
    eyeCtrlVis = rt_utils.connect_part_object(obj_base_connection='eyeCtrlVis', target_connection='visibility',
                                              obj_name=setupCtrl.control,
                                              target_name=[leftEyelid.eyeball_ctrl.parent_control[0],
                                                           leftEyelid.upLid.ctrl_0204_grp,
                                                           leftEyelid.lowLid.ctrl_0204_grp,
                                                           rightEyelid.eyeball_ctrl.parent_control[0],
                                                           rightEyelid.upLid.ctrl_0204_grp,
                                                           rightEyelid.lowLid.ctrl_0204_grp], channel_box=True,
                                              select_obj=False)
    # BROW VIS
    browCtrlVis = rt_utils.connect_part_object(obj_base_connection='browCtrlVis', target_connection='visibility',
                                               obj_name=setupCtrl.control,
                                               target_name=[brows.brow_all_ctrl], channel_box=True, select_obj=False)
    if bulge:
        # BULGE VIS
        bulgeCtrlVis = rt_utils.connect_part_object(obj_base_connection='bulgeCtrlVis', target_connection='visibility',
                                                    obj_name=setupCtrl.control,
                                                    target_name=[bulge.cheek_bulge_ctrl_LFT_grp,
                                                                 bulge.cheek_bulge_ctrl_RGT_grp,
                                                                 bulge.brow_in_bulge_ctrl_LFT_grp,
                                                                 bulge.brow_in_bulge_ctrl_RGT_grp,
                                                                 bulge.brow_out_bulge_ctrl_LFT_grp,
                                                                 bulge.brow_out_bulge_ctrl_RGT_grp,
                                                                 bulge.corner_mouth_bulge_ctrl_LFT_grp,
                                                                 bulge.corner_mouth_bulge_ctrl_RGT_grp,
                                                                 bulge.nose_bulge_ctrl_grp,
                                                                 bulge.chin_bulge_ctrl_grp], channel_box=True,
                                                    select_obj=False)
        cmds.setAttr(bulgeCtrlVis, 0)

    cmds.setAttr(mainCheekCtrlVis, 0)
    cmds.setAttr(secondaryCheekCtrlVis, 0)
    cmds.setAttr(chinCtrlVis, 0)

    # ==================================================================================================================
    #                                               CLEAN UP SET
    # ==================================================================================================================

    # PARENT TO GRP GENERAL MODULE
    cmds.parent(head.neck_ctrl_grp, setupCtrl.parent_control[0], 'faceAnim_grp')
    cmds.parent(head.world_up_grp, 'faceUtils_grp')

    # CONSTRAINT NECK JOINT AND CONTROLLER WITH SPINE 04 SKIN JOINT

    if cmds.objExists('spine04_skn'):
        cmds.parent(head.neck_jnt_grp, 'spine04_skn')
        rt_utils.parent_scale_constraint('spine04_skn', head.neck_ctrl_grp, mo=1)
    else:
        cmds.parent(head.neck_jnt_grp, face_joint_grp)

    # BRING ALL JOINT UNDER THE FACE JOINT HIERARCHY
    # JOINT lidUpMoveZroRGT AND lidLowMoveZroRGT AND lidUpMoveZroLFT AND lidLowMoveZroLFT
    cmds.setAttr(leftEyelid.up_lid_move_grp + '.inheritsTransform', 0)
    cmds.setAttr(leftEyelid.low_lid_move_grp + '.inheritsTransform', 0)
    cmds.setAttr(rightEyelid.up_lid_move_grp + '.inheritsTransform', 0)
    cmds.setAttr(rightEyelid.low_lid_move_grp + '.inheritsTransform', 0)

    # parent to eye joint
    cmds.parent(leftEyelid.up_lid_move_grp, leftEyelid.low_lid_move_grp, sj.eye_LFT)
    cmds.parent(rightEyelid.up_lid_move_grp, rightEyelid.low_lid_move_grp, sj.eye_RGT)

    # snap position
    cmds.delete(cmds.parentConstraint(sj.eye_LFT, leftEyelid.up_lid_move_grp, mo=0))
    cmds.delete(cmds.parentConstraint(sj.eye_LFT, leftEyelid.low_lid_move_grp, mo=0))
    cmds.delete(cmds.parentConstraint(sj.eye_RGT, rightEyelid.up_lid_move_grp, mo=0))
    cmds.delete(cmds.parentConstraint(sj.eye_RGT, rightEyelid.low_lid_move_grp, mo=0))

    # PARENT eyeWorldObjRGT_loc AND eyeWorldObjLFT_loc to face util
    cmds.parent(leftEyelid.world_up_object, rightEyelid.world_up_object, 'faceUtils_grp')

    # CHEEK PART
    cmds.setAttr(leftCheek.cheek_joint_grp + '.inheritsTransform', 0)
    cmds.setAttr(rightCheek.cheek_joint_grp + '.inheritsTransform', 0)

    cmds.parent(leftCheek.cheek_joint_grp, rightCheek.cheek_joint_grp, sj.head)

    cmds.setAttr(leftCheek.cheek_joint_grp + '.translate', 0, 0, 0, type="double3")
    cmds.setAttr(leftCheek.cheek_joint_grp + '.rotate', 0, 0, 0, type="double3")
    cmds.setAttr(rightCheek.cheek_joint_grp + '.translate', 0, 0, 0, type="double3")
    cmds.setAttr(rightCheek.cheek_joint_grp + '.rotate', 0, 0, 0, type="double3")

    # JOINT lipUpJntCtr_grp AND lipLowJntCtr_grp
    for joint, ctrl, joint_low, ctrl_low in zip(lip.upLip_all_joint, lip.uplip_controller, lip.lowLip_all_joint,
                                                lip.lowLip_controller):
        constraining_up = rt_utils.parent_scale_constraint(ctrl, joint)
        constraining_low = rt_utils.parent_scale_constraint(ctrl_low, joint_low)
        if game_bind_joint:
            cmds.parent(joint, sGame.head_up)
            cmds.parent(joint_low, sGame.jaw)
            cmds.parent(constraining_up[0], constraining_up[1], constraining_low[0], constraining_low[1],
                        'additional_grp')
            cmds.setAttr(joint + '.segmentScaleCompensate', 0)
            cmds.setAttr(joint_low + '.segmentScaleCompensate', 0)

        else:
            cmds.parent(joint, sj.head_up)
            cmds.parent(joint_low, sj.jaw)

    # PARENT DQ JOINT TO NECK JOINT
    cmds.setAttr(parentDQ_grp[0] + '.inheritsTransform', 0)
    cmds.parent(parentDQ_grp[0], sj.neck)
    cmds.delete(cmds.parentConstraint(sj.head, parentDQ_grp[0], mo=0))

    # CHIN JOINT
    cmds.setAttr(chin.group_driver + '.inheritsTransform', 0)
    cmds.parent(chin.group_driver, sj.jaw)
    cmds.setAttr(chin.group_driver + '.translate', 0, 0, 0, type="double3")
    cmds.setAttr(chin.group_driver + '.rotate', 0, 0, 0, type="double3")

    if not game_bind_joint:
        # UNHIDE SKIN JOINT
        unhide = cmds.ls('*skn')
        for i in unhide:
            try:
                if i + '.visibility' == 1:
                    pass
                else:
                    cmds.setAttr(i + '.visibility', 1)
            except:
                pass
        # CREATE SET LINEAR JOINT SKIN
        sets_LN = cmds.sets(sj.neck, n='FACE_SKIN_LN')
        cmds.setAttr(sj.neck + '.visibility', 1)

        # CREATE SETS
        for i in (sj.head, sj.head_up, sj.head_low, sj.jaw, sj.mentolabial, sj.chin, sj.brow_center,
                  sj.cheek_in_up_LFT, sj.cheek_in_low_LFT, sj.cheek_up_LFT, sj.cheek_mid_LFT, sj.cheek_low_LFT,
                  sj.cheek_out_up_LFT,
                  sj.cheek_out_low_LFT, sj.cheek_in_up_RGT, sj.cheek_in_low_RGT, sj.cheek_up_RGT, sj.cheek_mid_RGT,
                  sj.cheek_low_RGT,
                  sj.cheek_out_up_RGT, sj.cheek_out_low_RGT, sj.brow_in_LFT, sj.brow_mid_LFT, sj.brow_out_LFT,
                  sj.brow_tip_LFT,
                  sj.brow_in_RGT, sj.brow_mid_RGT, sj.brow_out_RGT, sj.brow_tip_RGT, sj.nose_up, sj.columella,
                  sj.eye_LFT,
                  sj.eye_RGT,
                  sj.ear_LFT, sj.ear_RGT, sj.neckIn_Btw):
            cmds.sets(i, add=sets_LN)
            cmds.setAttr(i + '.visibility', 1)

        for i in list(set(nose.all_joint + lip.all_up_lip_joint + lip.all_low_lip_joint + leftLidOut.lid_out_up_jnt +
                          leftLidOut.lid_out_low_jnt + rightLidOut.lid_out_up_jnt + rightLidOut.lid_out_low_jnt)):
            cmds.sets(i, add=sets_LN)
            cmds.setAttr(i + '.visibility', 1)

        # SETS DQ JOINT SKIN
        sets_DQ = cmds.sets(jntDQBase, n='FACE_SKIN_DQ')
        cmds.setAttr(jntDQBase + '.visibility', 1)

        for i in list(set(leftEyelid.up_lid_all_jnt + leftEyelid.low_lid_all_jnt +
                          rightEyelid.up_lid_all_jnt + rightEyelid.low_lid_all_jnt)):
            cmds.sets(i, add=sets_DQ)
