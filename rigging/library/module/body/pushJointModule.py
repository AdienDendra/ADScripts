from __future__ import absolute_import

import maya.cmds as cmds

from rigging.library.base.body import pushJoint as rlbb_pushJoint
from rigging.tools import utils as rt_utils


class PushJoint:
    def __init__(self,
                 prefix_spine,
                 spine_expand_joint,
                 spine_joint_grp,
                 number_arm_detail_ctrl,
                 number_leg_detail_ctrl,
                 neck_expand_joint,
                 clavicle_expand_joint,
                 ball_expand_joint,
                 upperArm_expand_joint,
                 upperLeg_expand_joint,
                 elbow_expand_joint,
                 knee_expand_joint,
                 wrist_expand_joint,
                 ankle_expand_joint,
                 left_side,
                 right_side,

                 prefix_arm_setup,
                 prefix_clav,
                 prefix_upperArm,
                 prefix_elbow,
                 prefix_wrist,
                 prefix_leg_setup,
                 prefix_ball,
                 prefix_upperLeg,
                 prefix_knee,
                 prefix_ankle,
                 sAdd_prefix_value,
                 dtl,
                 sj_prefix_value,
                 prefix_forearm,
                 fk,
                 prefix_lower_leg,

                 upArm_joint_LFT_grp,
                 elbow_joint_LFT_grp,
                 wrist_joint_LFT_grp,
                 upArm_joint_RGT_grp,
                 elbow_joint_RGT_grp,
                 wrist_joint_RGT_grp,
                 upLeg_joint_LFT_grp,
                 knee_joint_LFT_grp,
                 ankle_joint_LFT_grp,
                 ball_joint_LFT_grp,
                 upLeg_joint_RGT_grp,
                 knee_joint_RGT_grp,
                 ankle_joint_RGT_grp,
                 ball_joint_RGT_grp,
                 neck_joint_grp,
                 prefix_FkIk_spine_setup,
                 neck_prefix,

                 prefix_thumb,
                 prefix_index,
                 prefix_middle,
                 prefix_ring,
                 prefix_pinky,
                 thumb_joint_LFT_grp,
                 index_joint_LFT_grp,
                 middle_joint_LFT_grp,
                 ring_joint_LFT_grp,
                 pinky_joint_LFT_grp,
                 thumb_joint_RGT_grp,
                 index_joint_RGT_grp,
                 middle_joint_RGT_grp,
                 ring_joint_RGT_grp,
                 pinky_joint_RGT_grp,
                 thumb_expand_joint,
                 index_expand_joint,
                 middle_expand_joint,
                 ring_expand_joint,
                 pinky_expand_joint,
                 suffix_parent_joint,
                 suffix_duplicate_expand_joint,
                 size
                 ):
        self.prefix_spine = prefix_spine
        self.prefix_arm_setup = prefix_arm_setup
        self.prefix_clav = prefix_clav
        self.prefix_upperArm = prefix_upperArm
        self.prefix_elbow = prefix_elbow
        self.prefix_wrist = prefix_wrist
        self.prefix_leg_setup = prefix_leg_setup
        self.prefix_ball = prefix_ball
        self.prefix_upperLeg = prefix_upperLeg
        self.prefix_knee = prefix_knee
        self.prefix_ankle = prefix_ankle
        self.sAdd_prefix_value = sAdd_prefix_value
        self.dtl = dtl
        self.sj_prefix_value = sj_prefix_value
        self.prefix_forearm = prefix_forearm
        self.fk = fk
        self.prefix_lowerLeg = prefix_lower_leg
        self.prefix_FkIk_spine_setup = prefix_FkIk_spine_setup
        self.neck_prefix = neck_prefix
        self.prefix_thumb = prefix_thumb
        self.prefix_index = prefix_index
        self.prefix_middle = prefix_middle
        self.prefix_ring = prefix_ring
        self.prefix_pinky = prefix_pinky

        # ==================================================================================================================
        #                                     EXPAND JOINT LEFT AND RIGHT CALL
        # ==================================================================================================================
        if cmds.objExists('%sSetup_ctrl' % (self.prefix_spine)):
            self.spine_expand(spine_expand_joint=spine_expand_joint, spine_joint_grp=spine_joint_grp, multiply=1,
                              suffix_parent_joint=suffix_parent_joint,
                              suffix_duplicate_expand_joint=suffix_duplicate_expand_joint,
                              scale=size)

        if cmds.objExists('%s%s_ctrl' % (self.prefix_arm_setup, left_side)):
            self.arm_expand(upperArm_expand_joint=upperArm_expand_joint, side=left_side,
                            upArm_joint_grp=upArm_joint_LFT_grp,
                            elbow_expand_joint=elbow_expand_joint, number_arm_detail_ctrl=number_arm_detail_ctrl,
                            elbow_joint_grp=elbow_joint_LFT_grp, wrist_expand_joint=wrist_expand_joint,
                            wrist_joint_grp=wrist_joint_LFT_grp,
                            multiply=1, suffix_parent_joint=suffix_parent_joint,
                            suffix_duplicate_expand_joint=suffix_duplicate_expand_joint,
                            scale=size)
            self.finger_expand(side=left_side, thumb_joint_grp=thumb_joint_LFT_grp,
                               thumb_expand_joint=thumb_expand_joint,
                               index_joint_grp=index_joint_LFT_grp, index_expand_joint=index_expand_joint,
                               middle_joint_grp=middle_joint_LFT_grp, middle_expand_joint=middle_expand_joint,
                               ring_joint_grp=ring_joint_LFT_grp,
                               ring_expand_joint=ring_expand_joint, pinky_joint_grp=pinky_joint_LFT_grp,
                               pinky_expand_joint=pinky_expand_joint,
                               multiply=1, suffix_parent_joint=suffix_parent_joint,
                               suffix_duplicate_expand_joint=suffix_duplicate_expand_joint,
                               scale=size)

        if cmds.objExists('%s%s_ctrl' % (self.prefix_arm_setup, right_side)):
            self.arm_expand(upperArm_expand_joint=upperArm_expand_joint, side=right_side,
                            upArm_joint_grp=upArm_joint_RGT_grp,
                            elbow_expand_joint=elbow_expand_joint, number_arm_detail_ctrl=number_arm_detail_ctrl,
                            elbow_joint_grp=elbow_joint_RGT_grp, wrist_expand_joint=wrist_expand_joint,
                            wrist_joint_grp=wrist_joint_RGT_grp,
                            multiply=-1, suffix_parent_joint=suffix_parent_joint,
                            suffix_duplicate_expand_joint=suffix_duplicate_expand_joint,
                            scale=size)
            self.finger_expand(side=right_side, thumb_joint_grp=thumb_joint_RGT_grp,
                               thumb_expand_joint=thumb_expand_joint,
                               index_joint_grp=index_joint_RGT_grp, index_expand_joint=index_expand_joint,
                               middle_joint_grp=middle_joint_RGT_grp, middle_expand_joint=middle_expand_joint,
                               ring_joint_grp=ring_joint_RGT_grp,
                               ring_expand_joint=ring_expand_joint, pinky_joint_grp=pinky_joint_RGT_grp,
                               pinky_expand_joint=pinky_expand_joint,
                               multiply=-1, suffix_parent_joint=suffix_parent_joint,
                               suffix_duplicate_expand_joint=suffix_duplicate_expand_joint,
                               scale=size)

        if cmds.objExists('%s%s_ctrl' % (self.prefix_leg_setup, left_side)):
            self.leg_expand(side=left_side, upperLeg_expand_joint=upperLeg_expand_joint,
                            upLeg_joint_grp=upLeg_joint_LFT_grp,
                            knee_expand_joint=knee_expand_joint, number_leg_detail_ctrl=number_leg_detail_ctrl,
                            knee_joint_grp=knee_joint_LFT_grp,
                            ankle_expand_joint=ankle_expand_joint, ankle_joint_grp=ankle_joint_LFT_grp,
                            ball_expand_joint=ball_expand_joint,
                            ball_joint_grp=ball_joint_LFT_grp, multiply=1, suffix_parent_joint=suffix_parent_joint,
                            suffix_duplicate_expand_joint=suffix_duplicate_expand_joint,
                            scale=size)

        if cmds.objExists('%s%s_ctrl' % (self.prefix_leg_setup, right_side)):
            self.leg_expand(side=right_side, upperLeg_expand_joint=upperLeg_expand_joint,
                            upLeg_joint_grp=upLeg_joint_RGT_grp,
                            knee_expand_joint=knee_expand_joint, number_leg_detail_ctrl=number_leg_detail_ctrl,
                            knee_joint_grp=knee_joint_RGT_grp,
                            ankle_expand_joint=ankle_expand_joint, ankle_joint_grp=ankle_joint_RGT_grp,
                            ball_expand_joint=ball_expand_joint,
                            ball_joint_grp=ball_joint_RGT_grp, multiply=-1, suffix_parent_joint=suffix_parent_joint,
                            suffix_duplicate_expand_joint=suffix_duplicate_expand_joint,
                            scale=size)

        # # ==================================================================================================================
        # #                                        ADDITIONAL NECK PARAMETERS
        # # ==================================================================================================================
        # if mc.objExists('%s_ctrl' % self.neck_prefix):
        #     if not mc.objExists('%s_ctrl.%sExpand' % (self.prefix_FkIk_spine_setup, self.neck_prefix)):
        #         au.add_attribute(objects=['%s_ctrl' % self.prefix_FkIk_spine_setup], long_name=['cornerExpand'],
        #                          nice_name=[' '], at="enum",
        #                          en='Corner Expand', cb=True)
        #         au.add_attribute(objects=['%s_ctrl' % self.prefix_FkIk_spine_setup], long_name=['neckExpand'],
        #                          attributeType="float", min=0, dv=0.5, cb=True)
        #
        #     # print('85% adding attribute neck is done!')
        #
        #     # UPPERLEG
        #     self.add_neck_joint(add_joint=neck_expand_joint,
        #                         joint_grp=neck_joint_grp,
        #                         rotation='X',
        #                         rotation_pair_blend=2,
        #                         offset_translation_position='X',
        #                         offset_value=0.5, position_name='Out',
        #                         )

    # ==================================================================================================================
    #                                            EXPAND JOINT COMPILE
    # ==================================================================================================================
    def spine_expand(self, spine_expand_joint, spine_joint_grp, multiply, suffix_parent_joint,
                     suffix_duplicate_expand_joint, scale):

        if cmds.objExists('spine01_skn'):
            if cmds.objExists('spine%sOutLeft01_grp' % (self.sAdd_prefix_value)):
                print('object spine expand joint already made!')
            else:
                if spine_expand_joint:
                    # SPINE OUT LEFT
                    self.add_spine_joint(rotation='Z', joint_grp=spine_joint_grp, rotation_pair_blend=1,
                                         offset_translation_position='X',
                                         offset_value=multiply * 1.5 * scale, position_name='OutLeft',
                                         add_joint=spine_expand_joint,
                                         prefix=self.prefix_spine, suffix_parent_joint=suffix_parent_joint,
                                         suffix_duplicate_expand_joint=suffix_duplicate_expand_joint)
                    # SPINE OUT RIGHT
                    self.add_spine_joint(rotation='Z', joint_grp=spine_joint_grp, rotation_pair_blend=1,
                                         offset_translation_position='X',
                                         offset_value=multiply * -1.5 * scale, position_name='OutRight',
                                         add_joint=spine_expand_joint,
                                         prefix=self.prefix_spine, suffix_parent_joint=suffix_parent_joint,
                                         suffix_duplicate_expand_joint=suffix_duplicate_expand_joint)
                    # SPINE OUT FRONT
                    self.add_spine_joint(rotation='X', joint_grp=spine_joint_grp, rotation_pair_blend=1,
                                         offset_translation_position='Z',
                                         offset_value=multiply * 1.5 * scale, position_name='Front',
                                         add_joint=spine_expand_joint,
                                         prefix=self.prefix_spine, suffix_parent_joint=suffix_parent_joint,
                                         suffix_duplicate_expand_joint=suffix_duplicate_expand_joint)
                    # SPINE OUT RIGHT
                    self.add_spine_joint(rotation='X', joint_grp=spine_joint_grp, rotation_pair_blend=1,
                                         offset_translation_position='Z',
                                         offset_value=multiply * -1.5 * scale, position_name='Back',
                                         add_joint=spine_expand_joint,
                                         prefix=self.prefix_spine, suffix_parent_joint=suffix_parent_joint,
                                         suffix_duplicate_expand_joint=suffix_duplicate_expand_joint)

                    print('spine add joint expand is done!')

    def arm_expand(self, upperArm_expand_joint, side, upArm_joint_grp, elbow_expand_joint, number_arm_detail_ctrl,
                   elbow_joint_grp, wrist_expand_joint, wrist_joint_grp, multiply, suffix_parent_joint,
                   suffix_duplicate_expand_joint, scale):

        if cmds.objExists('upArm%s_skn' % (side)):
            # UPPERARM UP
            if cmds.objExists('upArm%sUp%s_grp' % (self.sAdd_prefix_value, side)):
                print('object upArm %s Expand joint already made!' % side)
            else:
                if upperArm_expand_joint:
                    # UPPERARM UP
                    self.add_joint_attribute(prefix_setup=self.prefix_arm_setup,
                                             prefix_expand_joint=self.prefix_upperArm, side=side, position_name='Up')

                    self.add_upperArm_joint(add_joint=upperArm_expand_joint, side=side, joint_grp=upArm_joint_grp,
                                            rotation='Z', rotation_pair_blend=1, offset_translation_position='X',
                                            offset_value=multiply * -0.5 * scale, position_name='Up',
                                            suffix_parent_joint=suffix_parent_joint,
                                            suffix_duplicate_expand_joint=suffix_duplicate_expand_joint)
                    # UPPERARM DOWN
                    self.add_joint_attribute(prefix_setup=self.prefix_arm_setup,
                                             prefix_expand_joint=self.prefix_upperArm, side=side, position_name='Down')

                    self.add_upperArm_joint(add_joint=upperArm_expand_joint, side=side, joint_grp=upArm_joint_grp,
                                            rotation='Z', rotation_pair_blend=1, offset_translation_position='X',
                                            offset_value=multiply * 0.5 * scale, position_name='Down',
                                            suffix_parent_joint=suffix_parent_joint,
                                            suffix_duplicate_expand_joint=suffix_duplicate_expand_joint)
                    # UPPERARM FRONT
                    self.add_joint_attribute(prefix_setup=self.prefix_arm_setup,
                                             prefix_expand_joint=self.prefix_upperArm, side=side, position_name='Front')
                    self.add_upperArm_joint(add_joint=upperArm_expand_joint, side=side, joint_grp=upArm_joint_grp,
                                            rotation='X', rotation_pair_blend=1, offset_translation_position='Z',
                                            offset_value=multiply * 0.5 * scale, position_name='Front',
                                            suffix_parent_joint=suffix_parent_joint,
                                            suffix_duplicate_expand_joint=suffix_duplicate_expand_joint)
                    # UPPERARM BACK
                    self.add_joint_attribute(prefix_setup=self.prefix_arm_setup,
                                             prefix_expand_joint=self.prefix_upperArm, side=side, position_name='Back')
                    self.add_upperArm_joint(add_joint=upperArm_expand_joint, side=side, joint_grp=upArm_joint_grp,
                                            rotation='X', rotation_pair_blend=1, offset_translation_position='Z',
                                            offset_value=multiply * -0.5 * scale, position_name='Back',
                                            suffix_parent_joint=suffix_parent_joint,
                                            suffix_duplicate_expand_joint=suffix_duplicate_expand_joint)

                    print("{} upper arm add joint expand is done!".format(side))

            if cmds.objExists('forearm%sFront%s_grp' % (self.sAdd_prefix_value, side)):
                print('object forearm %s expand joint already made!' % side)
            else:
                if elbow_expand_joint:
                    # ELBOW FRONT
                    self.add_joint_attribute(prefix_setup=self.prefix_arm_setup,
                                             prefix_expand_joint=self.prefix_elbow, side=side, position_name='Front')
                    self.add_elbow_joint(add_joint=elbow_expand_joint, side=side,
                                         number_arm_detail_ctrl=number_arm_detail_ctrl,
                                         joint_grp=elbow_joint_grp,
                                         rotation='X', rotation_pair_blend=1, offset_translation_position='Z',
                                         offset_value=multiply * 0.5 * scale, position_name='Front',
                                         suffix_parent_joint=suffix_parent_joint,
                                         suffix_duplicate_expand_joint=suffix_duplicate_expand_joint)

                    # ELBOW BACK
                    self.add_joint_attribute(prefix_setup=self.prefix_arm_setup,
                                             prefix_expand_joint=self.prefix_elbow, side=side, position_name='Back')
                    self.add_elbow_joint(add_joint=elbow_expand_joint, side=side,
                                         number_arm_detail_ctrl=number_arm_detail_ctrl,
                                         joint_grp=elbow_joint_grp,
                                         rotation='X', rotation_pair_blend=1, offset_translation_position='Z',
                                         offset_value=multiply * -0.5 * scale, position_name='Back',
                                         suffix_parent_joint=suffix_parent_joint,
                                         suffix_duplicate_expand_joint=suffix_duplicate_expand_joint)

                    # ELBOW UP
                    self.add_joint_attribute(prefix_setup=self.prefix_arm_setup,
                                             prefix_expand_joint=self.prefix_elbow, side=side, position_name='Up')
                    self.add_elbow_joint(add_joint=elbow_expand_joint, side=side,
                                         number_arm_detail_ctrl=number_arm_detail_ctrl,
                                         joint_grp=elbow_joint_grp,
                                         rotation='Z', rotation_pair_blend=1, offset_translation_position='X',
                                         offset_value=multiply * -0.5 * scale, position_name='Up',
                                         suffix_parent_joint=suffix_parent_joint,
                                         suffix_duplicate_expand_joint=suffix_duplicate_expand_joint)

                    # ELBOW DOWN
                    self.add_joint_attribute(prefix_setup=self.prefix_arm_setup,
                                             prefix_expand_joint=self.prefix_elbow, side=side, position_name='Down')
                    self.add_elbow_joint(add_joint=elbow_expand_joint, side=side,
                                         number_arm_detail_ctrl=number_arm_detail_ctrl,
                                         joint_grp=elbow_joint_grp,
                                         rotation='Z', rotation_pair_blend=1, offset_translation_position='X',
                                         offset_value=multiply * 0.5 * scale, position_name='Down',
                                         suffix_parent_joint=suffix_parent_joint,
                                         suffix_duplicate_expand_joint=suffix_duplicate_expand_joint)

                    print('{} elbow add joint expand is done!'.format(side))

            if cmds.objExists('wrist%sUp%s_grp' % (self.sAdd_prefix_value, side)):
                print('object wrist %s expand joint already made!' % side)
            else:
                if wrist_expand_joint:
                    # WRIST UP
                    self.add_joint_attribute(prefix_setup=self.prefix_arm_setup,
                                             prefix_expand_joint=self.prefix_wrist, side=side, position_name='Up')
                    self.add_wrist_joint(add_joint=wrist_expand_joint, side=side,
                                         number_arm_detail_ctrl=number_arm_detail_ctrl,
                                         joint_grp=wrist_joint_grp,
                                         rotation='Z', rotation_pair_blend=1, offset_translation_position='X',
                                         offset_value=multiply * -0.5 * scale, position_name='Up',
                                         suffix_parent_joint=suffix_parent_joint,
                                         suffix_duplicate_expand_joint=suffix_duplicate_expand_joint)

                    # WRIST DOWN
                    self.add_joint_attribute(prefix_setup=self.prefix_arm_setup,
                                             prefix_expand_joint=self.prefix_wrist, side=side, position_name='Down')
                    self.add_wrist_joint(add_joint=wrist_expand_joint, side=side,
                                         number_arm_detail_ctrl=number_arm_detail_ctrl,
                                         joint_grp=wrist_joint_grp,
                                         rotation='Z', rotation_pair_blend=1, offset_translation_position='X',
                                         offset_value=multiply * 0.5 * scale, position_name='Down',
                                         suffix_parent_joint=suffix_parent_joint,
                                         suffix_duplicate_expand_joint=suffix_duplicate_expand_joint)
                    # WRIST FRONT
                    self.add_joint_attribute(prefix_setup=self.prefix_arm_setup,
                                             prefix_expand_joint=self.prefix_wrist, side=side, position_name='Front')
                    self.add_wrist_joint(add_joint=wrist_expand_joint, side=side,
                                         number_arm_detail_ctrl=number_arm_detail_ctrl,
                                         joint_grp=wrist_joint_grp,
                                         rotation='X', rotation_pair_blend=1, offset_translation_position='Z',
                                         offset_value=multiply * 0.5 * scale, position_name='Front',
                                         suffix_parent_joint=suffix_parent_joint,
                                         suffix_duplicate_expand_joint=suffix_duplicate_expand_joint)
                    # WRIST BACK
                    self.add_joint_attribute(prefix_setup=self.prefix_arm_setup,
                                             prefix_expand_joint=self.prefix_wrist, side=side, position_name='Back')
                    self.add_wrist_joint(add_joint=wrist_expand_joint, side=side,
                                         number_arm_detail_ctrl=number_arm_detail_ctrl,
                                         joint_grp=wrist_joint_grp,
                                         rotation='X', rotation_pair_blend=1, offset_translation_position='Z',
                                         offset_value=multiply * -0.5 * scale, position_name='Back',
                                         suffix_parent_joint=suffix_parent_joint,
                                         suffix_duplicate_expand_joint=suffix_duplicate_expand_joint)

                    print('{} wrist add joint expand is done!'.format(side))

    def finger_expand(self, side, thumb_joint_grp, thumb_expand_joint, index_joint_grp, index_expand_joint,
                      middle_joint_grp, middle_expand_joint, ring_joint_grp, ring_expand_joint, pinky_joint_grp,
                      pinky_expand_joint, multiply, suffix_parent_joint, suffix_duplicate_expand_joint, scale):
        # FINGER UP
        if cmds.objExists('thumb02%s_skn' % (side)):
            if cmds.objExists('thumb%sUp02%s_grp' % (self.sAdd_prefix_value, side)):
                print('object thumb %s expand joint already made!' % side)
            else:
                if thumb_expand_joint:
                    self.add_finger_joint(side=side, rotation='Z', joint_grp=thumb_joint_grp, rotation_pair_blend=1,
                                          offset_translation_position='X',
                                          offset_value=multiply * -0.25 * scale, position_name='Up',
                                          add_joint=thumb_expand_joint,
                                          thumb=True,
                                          prefix=self.prefix_thumb, suffix_parent_joint=suffix_parent_joint,
                                          suffix_duplicate_expand_joint=suffix_duplicate_expand_joint)
                    self.add_finger_joint(side=side, rotation='Z', joint_grp=thumb_joint_grp, rotation_pair_blend=1,
                                          offset_translation_position='X',
                                          offset_value=multiply * 0.25 * scale, position_name='Down',
                                          add_joint=thumb_expand_joint,
                                          thumb=True,
                                          prefix=self.prefix_thumb, suffix_parent_joint=suffix_parent_joint,
                                          suffix_duplicate_expand_joint=suffix_duplicate_expand_joint)

                    print('{} thumb add joint expand is done!'.format(side))

        if cmds.objExists('index02%s_skn' % (side)):
            if cmds.objExists('index%sUp02%s_grp' % (self.sAdd_prefix_value, side)):
                print('object index %s expand joint already made!' % side)
            else:
                if index_expand_joint:
                    self.add_finger_joint(side=side, rotation='Z', joint_grp=index_joint_grp, rotation_pair_blend=1,
                                          offset_translation_position='X',
                                          offset_value=multiply * -0.25 * scale, position_name='Up',
                                          add_joint=index_expand_joint,
                                          thumb=False,
                                          prefix=self.prefix_index, suffix_parent_joint=suffix_parent_joint,
                                          suffix_duplicate_expand_joint=suffix_duplicate_expand_joint)
                    self.add_finger_joint(side=side, rotation='Z', joint_grp=index_joint_grp, rotation_pair_blend=1,
                                          offset_translation_position='X',
                                          offset_value=multiply * 0.25 * scale, position_name='Down',
                                          add_joint=index_expand_joint,
                                          thumb=False,
                                          prefix=self.prefix_index, suffix_parent_joint=suffix_parent_joint,
                                          suffix_duplicate_expand_joint=suffix_duplicate_expand_joint)
                    print('{} index add joint expand is done!'.format(side))

        if cmds.objExists('middle02%s_skn' % (side)):
            if cmds.objExists('middle%sUp02%s_grp' % (self.sAdd_prefix_value, side)):
                print('object middle %s expand joint already made!' % side)
            else:
                if middle_expand_joint:
                    self.add_finger_joint(side=side, rotation='Z', joint_grp=middle_joint_grp, rotation_pair_blend=1,
                                          offset_translation_position='X',
                                          offset_value=multiply * -0.25 * scale, position_name='Up',
                                          add_joint=middle_expand_joint,
                                          thumb=False,
                                          prefix=self.prefix_middle, suffix_parent_joint=suffix_parent_joint,
                                          suffix_duplicate_expand_joint=suffix_duplicate_expand_joint)
                    self.add_finger_joint(side=side, rotation='Z', joint_grp=middle_joint_grp, rotation_pair_blend=1,
                                          offset_translation_position='X',
                                          offset_value=multiply * 0.25 * scale, position_name='Down',
                                          add_joint=middle_expand_joint,
                                          thumb=False,
                                          prefix=self.prefix_middle, suffix_parent_joint=suffix_parent_joint,
                                          suffix_duplicate_expand_joint=suffix_duplicate_expand_joint)
                    print('{} middle add joint expand is done!'.format(side))

        if cmds.objExists('ring02%s_skn' % (side)):
            if cmds.objExists('ring%sUp02%s_grp' % (self.sAdd_prefix_value, side)):
                print('object ring %s expand joint already made!' % side)
            else:
                if ring_expand_joint:
                    self.add_finger_joint(side=side, rotation='Z', joint_grp=ring_joint_grp, rotation_pair_blend=1,
                                          offset_translation_position='X',
                                          offset_value=multiply * -0.25 * scale, position_name='Up',
                                          add_joint=ring_expand_joint,
                                          thumb=False,
                                          prefix=self.prefix_ring, suffix_parent_joint=suffix_parent_joint,
                                          suffix_duplicate_expand_joint=suffix_duplicate_expand_joint)
                    self.add_finger_joint(side=side, rotation='Z', joint_grp=ring_joint_grp, rotation_pair_blend=1,
                                          offset_translation_position='X',
                                          offset_value=multiply * 0.25 * scale, position_name='Down',
                                          add_joint=ring_expand_joint,
                                          thumb=False,
                                          prefix=self.prefix_ring, suffix_parent_joint=suffix_parent_joint,
                                          suffix_duplicate_expand_joint=suffix_duplicate_expand_joint)
                    print('{} ring add joint expand is done!'.format(side))

        if cmds.objExists('pinky02%s_skn' % (side)):
            if cmds.objExists('pinky%sUp02%s_grp' % (self.sAdd_prefix_value, side)):
                print('object pinky %s expand joint already made!' % side)
            else:
                if pinky_expand_joint:
                    self.add_finger_joint(side=side, rotation='Z', joint_grp=pinky_joint_grp, rotation_pair_blend=1,
                                          offset_translation_position='X',
                                          offset_value=multiply * -0.25 * scale, position_name='Up',
                                          add_joint=pinky_expand_joint,
                                          thumb=False,
                                          prefix=self.prefix_pinky, suffix_parent_joint=suffix_parent_joint,
                                          suffix_duplicate_expand_joint=suffix_duplicate_expand_joint)
                    self.add_finger_joint(side=side, rotation='Z', joint_grp=pinky_joint_grp, rotation_pair_blend=1,
                                          offset_translation_position='X',
                                          offset_value=multiply * 0.25 * scale, position_name='Down',
                                          add_joint=pinky_expand_joint,
                                          thumb=False,
                                          prefix=self.prefix_pinky, suffix_parent_joint=suffix_parent_joint,
                                          suffix_duplicate_expand_joint=suffix_duplicate_expand_joint)
                    print('{} pinky add joint expand is done!'.format(side))

    def leg_expand(self, side, upperLeg_expand_joint, upLeg_joint_grp, knee_expand_joint, number_leg_detail_ctrl,
                   knee_joint_grp,
                   ankle_expand_joint, ankle_joint_grp, ball_expand_joint, ball_joint_grp, multiply,
                   suffix_parent_joint,
                   suffix_duplicate_expand_joint, scale):
        if cmds.objExists('upLeg%s_skn' % (side)):
            if cmds.objExists('upLeg%sOut%s_grp' % (self.sAdd_prefix_value, side)):
                print('object upLeg %s expand joint already made!' % side)
            else:
                if upperLeg_expand_joint:
                    # UPPERLEG OUT
                    self.add_joint_attribute(prefix_setup=self.prefix_leg_setup,
                                             prefix_expand_joint=self.prefix_upperLeg, side=side, position_name='Out')
                    self.add_upperLeg_joint(add_joint=upperLeg_expand_joint, side=side, joint_grp=upLeg_joint_grp,
                                            rotation='Z', rotation_pair_blend=1, offset_translation_position='X',
                                            offset_value=multiply * -0.5 * scale, position_name='Out',
                                            suffix_parent_joint=suffix_parent_joint,
                                            suffix_duplicate_expand_joint=suffix_duplicate_expand_joint)

                    # UPPERLEG FRONT
                    self.add_joint_attribute(prefix_setup=self.prefix_leg_setup,
                                             prefix_expand_joint=self.prefix_upperLeg, side=side, position_name='Front')
                    self.add_upperLeg_joint(add_joint=upperLeg_expand_joint, side=side, joint_grp=upLeg_joint_grp,
                                            rotation='X', rotation_pair_blend=1, offset_translation_position='Z',
                                            offset_value=multiply * 0.5 * scale, position_name='Front',
                                            suffix_parent_joint=suffix_parent_joint,
                                            suffix_duplicate_expand_joint=suffix_duplicate_expand_joint)

                    # UPPERLEG BACK
                    self.add_joint_attribute(prefix_setup=self.prefix_leg_setup,
                                             prefix_expand_joint=self.prefix_upperLeg, side=side, position_name='Back')
                    self.add_upperLeg_joint(add_joint=upperLeg_expand_joint, side=side, joint_grp=upLeg_joint_grp,
                                            rotation='X', rotation_pair_blend=1, offset_translation_position='Z',
                                            offset_value=multiply * -0.5 * scale, position_name='Back',
                                            suffix_parent_joint=suffix_parent_joint,
                                            suffix_duplicate_expand_joint=suffix_duplicate_expand_joint)

                    print('{} upper leg add joint expand is done!'.format(side))

            if cmds.objExists('lowLeg%sFront%s_grp' % (self.sAdd_prefix_value, side)):
                print('object lowLeg %s expand joint already made!' % side)
            else:
                if knee_expand_joint:
                    # KNEE FRONT
                    self.add_joint_attribute(prefix_setup=self.prefix_leg_setup,
                                             prefix_expand_joint=self.prefix_knee, side=side, position_name='Front')
                    self.add_knee_joint(add_joint=knee_expand_joint, side=side,
                                        number_leg_detail_ctrl=number_leg_detail_ctrl,
                                        joint_grp=knee_joint_grp,
                                        rotation='X', rotation_pair_blend=1, offset_translation_position='Z',
                                        offset_value=multiply * 0.5 * scale, position_name='Front',
                                        suffix_parent_joint=suffix_parent_joint,
                                        suffix_duplicate_expand_joint=suffix_duplicate_expand_joint)
                    # KNEE BACK
                    self.add_joint_attribute(prefix_setup=self.prefix_leg_setup,
                                             prefix_expand_joint=self.prefix_knee, side=side, position_name='Back')
                    self.add_knee_joint(add_joint=knee_expand_joint, side=side,
                                        number_leg_detail_ctrl=number_leg_detail_ctrl,
                                        joint_grp=knee_joint_grp,
                                        rotation='X', rotation_pair_blend=1, offset_translation_position='Z',
                                        offset_value=multiply * -0.5 * scale, position_name='Back',
                                        suffix_parent_joint=suffix_parent_joint,
                                        suffix_duplicate_expand_joint=suffix_duplicate_expand_joint)

                    # KNEE OUT
                    self.add_joint_attribute(prefix_setup=self.prefix_leg_setup,
                                             prefix_expand_joint=self.prefix_knee, side=side, position_name='Out')
                    self.add_knee_joint(add_joint=knee_expand_joint, side=side,
                                        number_leg_detail_ctrl=number_leg_detail_ctrl,
                                        joint_grp=knee_joint_grp,
                                        rotation='Z', rotation_pair_blend=1, offset_translation_position='X',
                                        offset_value=multiply * -0.5 * scale, position_name='Out',
                                        suffix_parent_joint=suffix_parent_joint,
                                        suffix_duplicate_expand_joint=suffix_duplicate_expand_joint)
                    # KNEE IN
                    self.add_joint_attribute(prefix_setup=self.prefix_leg_setup,
                                             prefix_expand_joint=self.prefix_knee, side=side, position_name='In')
                    self.add_knee_joint(add_joint=knee_expand_joint, side=side,
                                        number_leg_detail_ctrl=number_leg_detail_ctrl,
                                        joint_grp=knee_joint_grp,
                                        rotation='Z', rotation_pair_blend=1, offset_translation_position='X',
                                        offset_value=multiply * 0.5 * scale, position_name='In',
                                        suffix_parent_joint=suffix_parent_joint,
                                        suffix_duplicate_expand_joint=suffix_duplicate_expand_joint)

                    print('{} knee add joint expand is done!'.format(side))

            if cmds.objExists('ankle%sFront%s_grp' % (self.sAdd_prefix_value, side)):
                print('object ankle %s expand joint already made!' % side)
            else:
                if ankle_expand_joint:
                    # ANKLE FRONT
                    self.add_joint_attribute(prefix_setup=self.prefix_leg_setup,
                                             prefix_expand_joint=self.prefix_ankle, side=side, position_name='Front')
                    self.add_ankle_joint(add_joint=ankle_expand_joint, side=side,
                                         number_leg_detail_ctrl=number_leg_detail_ctrl,
                                         joint_grp=ankle_joint_grp,
                                         rotation='X', rotation_pair_blend=1, offset_translation_position='Z',
                                         offset_value=multiply * 0.5 * scale, position_name='Front',
                                         suffix_parent_joint=suffix_parent_joint,
                                         suffix_duplicate_expand_joint=suffix_duplicate_expand_joint)
                    # ANKLE BACK
                    self.add_joint_attribute(prefix_setup=self.prefix_leg_setup,
                                             prefix_expand_joint=self.prefix_ankle, side=side, position_name='Back')
                    self.add_ankle_joint(add_joint=ankle_expand_joint, side=side,
                                         number_leg_detail_ctrl=number_leg_detail_ctrl,
                                         joint_grp=ankle_joint_grp,
                                         rotation='X', rotation_pair_blend=1, offset_translation_position='Z',
                                         offset_value=multiply * -0.5 * scale, position_name='Back',
                                         suffix_parent_joint=suffix_parent_joint,
                                         suffix_duplicate_expand_joint=suffix_duplicate_expand_joint)
                    # ANKLE OUT
                    self.add_joint_attribute(prefix_setup=self.prefix_leg_setup,
                                             prefix_expand_joint=self.prefix_ankle, side=side, position_name='Out')
                    self.add_ankle_joint(add_joint=ankle_expand_joint, side=side,
                                         number_leg_detail_ctrl=number_leg_detail_ctrl,
                                         joint_grp=ankle_joint_grp,
                                         rotation='Z', rotation_pair_blend=1, offset_translation_position='X',
                                         offset_value=multiply * -0.5 * scale, position_name='Out',
                                         suffix_parent_joint=suffix_parent_joint,
                                         suffix_duplicate_expand_joint=suffix_duplicate_expand_joint)
                    # ANKLE IN
                    self.add_joint_attribute(prefix_setup=self.prefix_leg_setup,
                                             prefix_expand_joint=self.prefix_ankle, side=side, position_name='In')
                    self.add_ankle_joint(add_joint=ankle_expand_joint, side=side,
                                         number_leg_detail_ctrl=number_leg_detail_ctrl,
                                         joint_grp=ankle_joint_grp,
                                         rotation='Z', rotation_pair_blend=1, offset_translation_position='X',
                                         offset_value=multiply * 0.5 * scale, position_name='In',
                                         suffix_parent_joint=suffix_parent_joint,
                                         suffix_duplicate_expand_joint=suffix_duplicate_expand_joint)

                    print('{} ankle add joint expand is done!'.format(side))

        if cmds.objExists('ball%s_skn' % (side)):
            if cmds.objExists('ball%sUp%s_grp' % (self.sAdd_prefix_value, side)):
                print('object ball %s expand joint already made!' % side)
            else:
                if ball_expand_joint:
                    # BALL UP
                    self.add_joint_attribute(prefix_setup=self.prefix_leg_setup,
                                             prefix_expand_joint=self.prefix_ball, side=side, position_name='Up')
                    self.add_ball_joint(add_joint=ball_expand_joint, side=side, joint_grp=ball_joint_grp,
                                        rotation='X',
                                        rotation_pair_blend=1,
                                        offset_translation_position='Z',
                                        offset_value=multiply * 0.5 * scale, position_name='Up',
                                        suffix_parent_joint=suffix_parent_joint,
                                        suffix_duplicate_expand_joint=suffix_duplicate_expand_joint)
                    # BALL DOWN
                    self.add_joint_attribute(prefix_setup=self.prefix_leg_setup,
                                             prefix_expand_joint=self.prefix_ball, side=side, position_name='Down')
                    self.add_ball_joint(add_joint=ball_expand_joint, side=side, joint_grp=ball_joint_grp,
                                        rotation='X',
                                        rotation_pair_blend=1,
                                        offset_translation_position='Z',
                                        offset_value=multiply * -0.5 * scale, position_name='Down',
                                        suffix_parent_joint=suffix_parent_joint,
                                        suffix_duplicate_expand_joint=suffix_duplicate_expand_joint)
                    # BALL OUT
                    self.add_joint_attribute(prefix_setup=self.prefix_leg_setup,
                                             prefix_expand_joint=self.prefix_ball, side=side, position_name='Out')
                    self.add_ball_joint(add_joint=ball_expand_joint, side=side, joint_grp=ball_joint_grp,
                                        rotation='Y',
                                        rotation_pair_blend=1,
                                        offset_translation_position='X',
                                        offset_value=multiply * -0.5 * scale, position_name='Out',
                                        suffix_parent_joint=suffix_parent_joint,
                                        suffix_duplicate_expand_joint=suffix_duplicate_expand_joint)
                    # BALL IN
                    self.add_joint_attribute(prefix_setup=self.prefix_leg_setup,
                                             prefix_expand_joint=self.prefix_ball, side=side, position_name='In')
                    self.add_ball_joint(add_joint=ball_expand_joint, side=side, joint_grp=ball_joint_grp,
                                        rotation='Y',
                                        rotation_pair_blend=1,
                                        offset_translation_position='X',
                                        offset_value=multiply * 0.5 * scale, position_name='In',
                                        suffix_parent_joint=suffix_parent_joint,
                                        suffix_duplicate_expand_joint=suffix_duplicate_expand_joint)

                    print('{} ball add joint expand is done!'.format(side))

    # ==================================================================================================================
    #                                            EXPAND JOINT FUNCTIONS
    # ==================================================================================================================

    def add_spine_joint(self, rotation, joint_grp, rotation_pair_blend, offset_translation_position,
                        offset_value, position_name, add_joint, prefix, suffix_parent_joint,
                        suffix_duplicate_expand_joint):

        if cmds.objExists('%sSetup_ctrl' % (prefix)):
            if not cmds.objExists('%s%s_grp' % (prefix, self.sAdd_prefix_value)):
                if not cmds.objExists('%sSetup_ctrl' % (prefix) + '.' + 'cornerExpand'):
                    rt_utils.add_attr_transform_shape(obj='%sSetup_ctrl' % (prefix), attr_name='cornerExpand',
                                                      attr_type="enum", en='Corner Expand', channel_box=True,
                                                      niceName=' ')

                rt_utils.add_attr_transform_shape(obj='%sSetup_ctrl' % (prefix),
                                                  attr_name='%s%s%s%s' % (prefix, '01', position_name, 'Expand'),
                                                  attr_type="float", min=0, dv=0.5, max=1.0, channel_box=True)
                rt_utils.add_attr_transform_shape(obj='%sSetup_ctrl' % (prefix),
                                                  attr_name='%s%s%s%s' % (prefix, '02', position_name, 'Expand'),
                                                  attr_type="float", min=0, dv=0.5, max=1.0, channel_box=True)
                rt_utils.add_attr_transform_shape(obj='%sSetup_ctrl' % (prefix),
                                                  attr_name='%s%s%s%s' % (prefix, '03', position_name, 'Expand'),
                                                  attr_type="float", min=0, dv=0.5, max=1.0, channel_box=True)

            rlbb_pushJoint.Build(add_joint=add_joint,
                                 fk_ik_setup='%sSetup_ctrl' % (prefix),
                                 controller_expand_name=prefix + '01',
                                 joint_driver_matrix='%s01%s_%s' % (prefix, self.sj_prefix_value, suffix_parent_joint),
                                 joint_add_target='%s01%s_%s' % (
                                 prefix, self.sAdd_prefix_value, suffix_duplicate_expand_joint),
                                 joint_driver_inverse_matrix='root_%s' % suffix_parent_joint,
                                 point_grp_driver=['%s01%s_%s' % (prefix, self.sj_prefix_value, suffix_parent_joint)],
                                 scale_driver=['%s01%s_%s' % (prefix, self.sj_prefix_value, suffix_parent_joint)],
                                 joint_grp=joint_grp,
                                 rotation=rotation,
                                 side='',
                                 rotation_pair_blend=rotation_pair_blend,
                                 offset_translation_position=offset_translation_position,
                                 offset_value=offset_value,
                                 position_name=position_name,
                                 )

            rlbb_pushJoint.Build(add_joint=add_joint,
                                 fk_ik_setup='%sSetup_ctrl' % (prefix),
                                 controller_expand_name=prefix + '02',
                                 joint_driver_matrix='%s02%s_%s' % (prefix, self.sj_prefix_value, suffix_parent_joint),
                                 joint_add_target='%s02%s_%s' % (
                                 prefix, self.sAdd_prefix_value, suffix_duplicate_expand_joint),
                                 joint_driver_inverse_matrix='%s01%s_%s' % (
                                 prefix, self.sj_prefix_value, suffix_parent_joint),
                                 point_grp_driver=['%s02%s_%s' % (prefix, self.sj_prefix_value, suffix_parent_joint)],
                                 scale_driver=['%s02%s_%s' % (prefix, self.sj_prefix_value, suffix_parent_joint)],
                                 joint_grp=joint_grp,
                                 rotation=rotation,
                                 side='',
                                 rotation_pair_blend=rotation_pair_blend,
                                 offset_translation_position=offset_translation_position,
                                 offset_value=offset_value,
                                 position_name=position_name,
                                 )

            rlbb_pushJoint.Build(add_joint=add_joint,
                                 fk_ik_setup='%sSetup_ctrl' % (prefix),
                                 controller_expand_name=prefix + '03',
                                 joint_driver_matrix='%s03%s_%s' % (prefix, self.sj_prefix_value, suffix_parent_joint),
                                 joint_add_target='%s03%s_%s' % (
                                 prefix, self.sAdd_prefix_value, suffix_duplicate_expand_joint),
                                 joint_driver_inverse_matrix='%s02%s_%s' % (
                                 prefix, self.sj_prefix_value, suffix_parent_joint),
                                 point_grp_driver=['%s03%s_%s' % (prefix, self.sj_prefix_value, suffix_parent_joint)],
                                 scale_driver=['%s03%s_%s' % (prefix, self.sj_prefix_value, suffix_parent_joint)],
                                 joint_grp=joint_grp,
                                 rotation=rotation,
                                 side='',
                                 rotation_pair_blend=rotation_pair_blend,
                                 offset_translation_position=offset_translation_position,
                                 offset_value=offset_value,
                                 position_name=position_name,
                                 )
        else:
            print('Expand joint', 'spine%s_%s' % (self.sAdd_prefix_value, suffix_parent_joint), 'is already added!')

    def add_joint_attribute(self, prefix_setup, prefix_expand_joint, position_name, side):

        if cmds.objExists('%s%s%s' % (prefix_setup, side, '_ctrl')):
            if not cmds.objExists('%s%s_ctrl' % (prefix_setup, side) + '.' + 'cornerExpand'):
                rt_utils.add_attr_transform_shape(obj='%s%s_ctrl' % (prefix_setup, side), attr_name='cornerExpand',
                                                  niceName=' ', attr_type="enum",
                                                  en='Corner Expand', channel_box=True)

            if not cmds.objExists(
                    '%s%s_ctrl' % (prefix_setup, side) + '.' + prefix_expand_joint + position_name + 'Expand'):
                rt_utils.add_attr_transform_shape(obj='%s%s_ctrl' % (prefix_setup, side),
                                                  attr_name=prefix_expand_joint + position_name + 'Expand',
                                                  attr_type="float", min=0, dv=0.5, max=1.0, channel_box=True)
        else:
            return

    def add_upperArm_joint(self, add_joint, side, rotation, joint_grp, rotation_pair_blend,
                           offset_translation_position,
                           offset_value, position_name, suffix_parent_joint, suffix_duplicate_expand_joint
                           ):

        if cmds.objExists('%s%s%s' % (self.prefix_arm_setup, side, '_ctrl')):
            if not cmds.objExists('upArm%s%s_grp' % (self.sAdd_prefix_value, side)):
                rlbb_pushJoint.Build(add_joint=add_joint,
                                     fk_ik_setup='%s%s_ctrl' % (self.prefix_arm_setup, side),
                                     controller_expand_name=self.prefix_upperArm,
                                     joint_driver_matrix='%s%s01%s_%s' % (
                                     self.prefix_upperArm, self.dtl, side, suffix_parent_joint),
                                     joint_add_target='upArm%s%s_%s' % (
                                     self.sAdd_prefix_value, side, suffix_duplicate_expand_joint),
                                     joint_driver_inverse_matrix='clav%s%s_%s' % (
                                     self.sj_prefix_value, side, suffix_parent_joint),
                                     point_grp_driver=[
                                         '%s%s01%s_%s' % (self.prefix_upperArm, self.dtl, side, suffix_parent_joint)],
                                     scale_driver=[
                                         '%s%s01%s_%s' % (self.prefix_upperArm, self.dtl, side, suffix_parent_joint)],
                                     side=side,
                                     joint_grp=joint_grp,
                                     rotation=rotation,
                                     rotation_pair_blend=rotation_pair_blend,
                                     offset_translation_position=offset_translation_position,
                                     offset_value=offset_value,
                                     position_name=position_name,
                                     )
            else:
                print('Additional joint',
                      'upArm%s%s%s_%s' % (self.sAdd_prefix_value, position_name, side, suffix_parent_joint),
                      'is already added!')

    def add_elbow_joint(self, add_joint, side, number_arm_detail_ctrl, rotation, joint_grp, rotation_pair_blend,
                        offset_translation_position,
                        offset_value, position_name, suffix_parent_joint, suffix_duplicate_expand_joint
                        ):

        if cmds.objExists('%s%s%s' % (self.prefix_arm_setup, side, '_ctrl')):
            if not cmds.objExists('forearm%s%s_grp' % (self.sAdd_prefix_value, side)):
                rlbb_pushJoint.Build(add_joint=add_joint,
                                     fk_ik_setup='%s%s_ctrl' % (self.prefix_arm_setup, side),
                                     controller_expand_name=self.prefix_elbow,
                                     joint_driver_matrix='forearm%s%s_%s' % (
                                     self.sj_prefix_value, side, suffix_parent_joint),
                                     joint_add_target='forearm%s%s_%s' % (
                                     self.sAdd_prefix_value, side, suffix_duplicate_expand_joint),
                                     joint_driver_inverse_matrix='upArm%s%s_%s' % (
                                     self.sj_prefix_value, side, suffix_parent_joint),
                                     point_grp_driver=['%s%s%02d%s_%s' % (
                                     self.prefix_upperArm, self.dtl, number_arm_detail_ctrl, side, suffix_parent_joint),
                                                       '%s%s01%s_%s' % (
                                                       self.prefix_forearm, self.dtl, side, suffix_parent_joint)],
                                     scale_driver=['%s%s%02d%s_%s' % (
                                     self.prefix_upperArm, self.dtl, number_arm_detail_ctrl, side, suffix_parent_joint),
                                                   '%s%s01%s_%s' % (
                                                   self.prefix_forearm, self.dtl, side, suffix_parent_joint)],
                                     side=side,
                                     joint_grp=joint_grp,
                                     rotation=rotation,
                                     rotation_pair_blend=rotation_pair_blend,
                                     offset_translation_position=offset_translation_position,
                                     offset_value=offset_value,
                                     position_name=position_name,
                                     constraint_method=True
                                     )
            else:
                print('Expand joint', 'forearm%s%s_%s' % (self.sAdd_prefix_value, side, suffix_parent_joint),
                      'is already added!')

    def add_wrist_joint(self, add_joint, side, number_arm_detail_ctrl, rotation, joint_grp, rotation_pair_blend,
                        offset_translation_position,
                        offset_value, position_name, suffix_parent_joint, suffix_duplicate_expand_joint
                        ):

        if cmds.objExists('%s%s%s' % (self.prefix_arm_setup, side, '_ctrl')):
            if not cmds.objExists('wrist%s%s_grp' % (self.sAdd_prefix_value, side)):
                rlbb_pushJoint.Build(add_joint=add_joint,
                                     fk_ik_setup='%s%s_ctrl' % (self.prefix_arm_setup, side),
                                     controller_expand_name=self.prefix_wrist,
                                     joint_driver_matrix='wrist%s%s_%s' % (
                                     self.sj_prefix_value, side, suffix_parent_joint),
                                     joint_add_target='wrist%s%s_%s' % (
                                     self.sAdd_prefix_value, side, suffix_duplicate_expand_joint),
                                     joint_driver_inverse_matrix='forearm%s%s_%s' % (
                                     self.sj_prefix_value, side, suffix_parent_joint),
                                     point_grp_driver=['%s%s%02d%s_ctrl' % (
                                     self.prefix_forearm, self.dtl, number_arm_detail_ctrl, side),
                                                       'wrist%s%s_%s' % (
                                                       self.sj_prefix_value, side, suffix_parent_joint)],
                                     scale_driver=['%s%s%02d%s_ctrl' % (
                                     self.prefix_forearm, self.dtl, number_arm_detail_ctrl, side),
                                                   'wrist%s%s_%s' % (self.sj_prefix_value, side, suffix_parent_joint)],
                                     side=side,
                                     joint_grp=joint_grp,
                                     rotation=rotation,
                                     rotation_pair_blend=rotation_pair_blend,
                                     offset_translation_position=offset_translation_position,
                                     offset_value=offset_value,
                                     position_name=position_name,
                                     constraint_method=True
                                     )
            else:
                print('Expand joint', 'wrist%s%s_%s' % (self.sAdd_prefix_value, side, suffix_parent_joint),
                      'is already added!')

    def add_upperLeg_joint(self, add_joint, side, rotation, joint_grp, rotation_pair_blend,
                           offset_translation_position,
                           offset_value, position_name, suffix_parent_joint, suffix_duplicate_expand_joint
                           ):

        if cmds.objExists('%s%s%s' % (self.prefix_leg_setup, side, '_ctrl')):
            if not cmds.objExists('upLeg%s%s_grp' % (self.sAdd_prefix_value, side)):
                rlbb_pushJoint.Build(add_joint=add_joint,
                                     fk_ik_setup='%s%s_ctrl' % (self.prefix_leg_setup, side),
                                     controller_expand_name=self.prefix_upperLeg,
                                     joint_driver_matrix='%s%s01%s_%s' % (
                                     self.prefix_upperLeg, self.dtl, side, suffix_parent_joint,),
                                     joint_add_target='upLeg%s%s_%s' % (
                                     self.sAdd_prefix_value, side, suffix_duplicate_expand_joint),
                                     joint_driver_inverse_matrix='%s%sCtrlOffset%s_grp' % (
                                     self.prefix_upperLeg, self.fk, side),
                                     point_grp_driver=[
                                         '%s%s01%s_%s' % (self.prefix_upperLeg, self.dtl, side, suffix_parent_joint,)],
                                     scale_driver=[
                                         '%s%s01%s_%s' % (self.prefix_upperLeg, self.dtl, side, suffix_parent_joint,)],
                                     side=side,
                                     joint_grp=joint_grp,
                                     rotation=rotation,
                                     rotation_pair_blend=rotation_pair_blend,
                                     offset_translation_position=offset_translation_position,
                                     offset_value=offset_value,
                                     position_name=position_name,
                                     )
            else:
                print('Expand joint', 'upLeg%s%s_%s' % (self.sAdd_prefix_value, side, suffix_parent_joint),
                      'is already added!')

    def add_knee_joint(self, add_joint, side, number_leg_detail_ctrl, rotation, joint_grp, rotation_pair_blend,
                       offset_translation_position,
                       offset_value, position_name, suffix_parent_joint, suffix_duplicate_expand_joint
                       ):

        if cmds.objExists('%s%s%s' % (self.prefix_leg_setup, side, '_ctrl')):
            if not cmds.objExists('lowLeg%s%s_grp' % (self.sAdd_prefix_value, side)):
                rlbb_pushJoint.Build(add_joint=add_joint,
                                     fk_ik_setup='%s%s_ctrl' % (self.prefix_leg_setup, side),
                                     controller_expand_name=self.prefix_knee,
                                     joint_driver_matrix='lowLeg%s%s_%s' % (
                                     self.sj_prefix_value, side, suffix_parent_joint),
                                     joint_add_target='lowLeg%s%s_%s' % (
                                     self.sAdd_prefix_value, side, suffix_duplicate_expand_joint),
                                     joint_driver_inverse_matrix='upLeg%s%s_%s' % (
                                     self.sj_prefix_value, side, suffix_parent_joint),
                                     point_grp_driver=['%s%s%02d%s_%s' % (
                                     self.prefix_upperLeg, self.dtl, number_leg_detail_ctrl, side,
                                     suffix_parent_joint,),
                                                       '%s%s01%s_%s' % (
                                                       self.prefix_lowerLeg, self.dtl, side, suffix_parent_joint,)],
                                     scale_driver=['%s%s%02d%s_%s' % (
                                     self.prefix_upperLeg, self.dtl, number_leg_detail_ctrl, side,
                                     suffix_parent_joint,),
                                                   '%s%s01%s_%s' % (
                                                   self.prefix_lowerLeg, self.dtl, side, suffix_parent_joint,)],
                                     side=side,
                                     joint_grp=joint_grp,
                                     rotation=rotation,
                                     rotation_pair_blend=rotation_pair_blend,
                                     offset_translation_position=offset_translation_position,
                                     offset_value=offset_value,
                                     position_name=position_name,
                                     constraint_method=True
                                     )
            else:
                print('Expand joint', 'lowLeg%s%s_%s' % (self.sAdd_prefix_value, side, suffix_parent_joint),
                      'is already added!')

    def add_ankle_joint(self, add_joint, side, number_leg_detail_ctrl, rotation, joint_grp, rotation_pair_blend,
                        offset_translation_position,
                        offset_value, position_name, suffix_parent_joint, suffix_duplicate_expand_joint
                        ):

        if cmds.objExists('%s%s%s' % (self.prefix_leg_setup, side, '_ctrl')):
            if not cmds.objExists('ankle%s%s_grp' % (self.sAdd_prefix_value, side)):
                rlbb_pushJoint.Build(add_joint=add_joint,
                                     fk_ik_setup='%s%s_ctrl' % (self.prefix_leg_setup, side),
                                     controller_expand_name=self.prefix_ankle,
                                     joint_driver_matrix='ankle%s%s_%s' % (
                                     self.sj_prefix_value, side, suffix_parent_joint),
                                     joint_add_target='ankle%s%s_%s' % (
                                     self.sAdd_prefix_value, side, suffix_duplicate_expand_joint),
                                     joint_driver_inverse_matrix='lowLeg%s%s_%s' % (
                                     self.sj_prefix_value, side, suffix_parent_joint),
                                     point_grp_driver=['%s%s%02d%s_%s' % (
                                     self.prefix_lowerLeg, self.dtl, number_leg_detail_ctrl, side,
                                     suffix_parent_joint,),
                                                       'ankle%s%s_%s' % (
                                                       self.sj_prefix_value, side, suffix_parent_joint)],
                                     scale_driver=['%s%s%02d%s_%s' % (
                                     self.prefix_lowerLeg, self.dtl, number_leg_detail_ctrl, side,
                                     suffix_parent_joint,),
                                                   'ankle%s%s_%s' % (self.sj_prefix_value, side, suffix_parent_joint)],
                                     side=side,
                                     joint_grp=joint_grp,
                                     rotation=rotation,
                                     rotation_pair_blend=rotation_pair_blend,
                                     offset_translation_position=offset_translation_position,
                                     offset_value=offset_value,
                                     position_name=position_name,
                                     constraint_method=True
                                     )
            else:
                print('Expand joint', 'ankle%s%s_%s' % (self.sAdd_prefix_value, side, suffix_parent_joint),
                      'is already added!')

    def add_ball_joint(self, add_joint, side, rotation, joint_grp, rotation_pair_blend,
                       offset_translation_position,
                       offset_value, position_name, suffix_parent_joint, suffix_duplicate_expand_joint
                       ):

        if cmds.objExists('%s%s%s' % (self.prefix_leg_setup, side, '_ctrl')):
            if not cmds.objExists('ball%s%s_grp' % (self.sAdd_prefix_value, side)):
                rlbb_pushJoint.Build(add_joint=add_joint,
                                     fk_ik_setup='%s%s_ctrl' % (self.prefix_leg_setup, side),
                                     controller_expand_name=self.prefix_ball,
                                     joint_driver_matrix='ballScale%s%s_%s' % (
                                     self.sj_prefix_value, side, suffix_parent_joint),
                                     joint_add_target='ball%s%s_%s' % (
                                     self.sAdd_prefix_value, side, suffix_duplicate_expand_joint),
                                     joint_driver_inverse_matrix='ankle%s%s_%s' % (
                                     self.sj_prefix_value, side, suffix_parent_joint),
                                     point_grp_driver=['ballScale%s_%s' % (side, suffix_parent_joint)],
                                     scale_driver=['ballScale%s_%s' % (side, suffix_parent_joint)],
                                     side=side,
                                     joint_grp=joint_grp,
                                     rotation=rotation,
                                     rotation_pair_blend=rotation_pair_blend,
                                     offset_translation_position=offset_translation_position,
                                     offset_value=offset_value,
                                     position_name=position_name,
                                     )
            else:
                print('Expand joint', 'ball%s%s_%s' % (self.sAdd_prefix_value, side, suffix_parent_joint),
                      'is already added!')

    def add_neck_joint(self, add_joint, rotation, joint_grp, rotation_pair_blend, offset_translation_position,
                       offset_value, position_name, suffix_parent_joint, suffix_duplicate_expand_joint):

        if cmds.objExists('%s%s' % (self.prefix_FkIk_spine_setup, '_ctrl')):
            if not cmds.objExists('neck%s_grp' % (self.sAdd_prefix_value)):
                rlbb_pushJoint.Build(add_joint=add_joint,
                                     fk_ik_setup='%s_ctrl' % (self.prefix_FkIk_spine_setup),
                                     controller_expand_name=self.neck_prefix,
                                     joint_driver_matrix='%sGmbl_ctrl' % self.neck_prefix,
                                     joint_add_target='neck%s_%s' % (
                                     self.sAdd_prefix_value, suffix_duplicate_expand_joint),
                                     joint_driver_inverse_matrix='spine%s04_%s' % (
                                     self.sj_prefix_value, suffix_parent_joint),
                                     point_grp_driver=['%sGmbl_ctrl' % self.neck_prefix],
                                     scale_driver=['%sGmbl_ctrl' % self.neck_prefix],
                                     side='',
                                     joint_grp=joint_grp,
                                     rotation=rotation,
                                     rotation_pair_blend=rotation_pair_blend,
                                     offset_translation_position=offset_translation_position,
                                     offset_value=offset_value,
                                     position_name=position_name,
                                     )
            else:
                print('Expand joint', 'neck%s_%s' % (self.sAdd_prefix_value, suffix_parent_joint), 'is already added!')

    def add_finger_joint(self, side, rotation, joint_grp, rotation_pair_blend,
                         offset_translation_position,
                         offset_value, position_name, add_joint, prefix, thumb, suffix_parent_joint,
                         suffix_duplicate_expand_joint):

        if cmds.objExists('%sBase%s_ctrl' % (prefix, side)):
            if not cmds.objExists('%sBase%s%s_grp' % (prefix, self.sAdd_prefix_value, side)):
                if not cmds.objExists('%sBase%s_ctrl' % (prefix, side) + '.' + 'cornerExpand'):
                    rt_utils.add_attr_transform_shape(obj='%sBase%s_ctrl' % (prefix, side), attr_name='cornerExpand',
                                                      attr_type="enum", en='Corner Expand', channel_box=True,
                                                      niceName=' ')

                rt_utils.add_attr_transform_shape(obj='%sBase%s_ctrl' % (prefix, side),
                                                  attr_name='%s02%s%s' % (prefix, position_name, 'Expand'),
                                                  attr_type="float", min=0, dv=0.5, max=1.0, channel_box=True)
                rt_utils.add_attr_transform_shape(obj='%sBase%s_ctrl' % (prefix, side),
                                                  attr_name='%s03%s%s' % (prefix, position_name, 'Expand'),
                                                  attr_type="float", min=0, dv=0.5, max=1.0, channel_box=True)
                if not thumb:
                    rt_utils.add_attr_transform_shape(obj='%sBase%s_ctrl' % (prefix, side),
                                                      attr_name='%s04%s%s' % (prefix, position_name, 'Expand'),
                                                      attr_type="float", min=0, dv=0.5, max=1.0, channel_box=True)

            rlbb_pushJoint.Build(add_joint=add_joint,
                                 fk_ik_setup='%sBase%s_ctrl' % (prefix, side),
                                 controller_expand_name=prefix + '02',
                                 joint_driver_matrix='%s02%s%s_%s' % (
                                 prefix, self.sj_prefix_value, side, suffix_parent_joint),
                                 joint_add_target='%s02%s%s_%s' % (
                                 prefix, self.sAdd_prefix_value, side, suffix_duplicate_expand_joint),
                                 joint_driver_inverse_matrix='%s01%s%s_%s' % (
                                 prefix, self.sj_prefix_value, side, suffix_parent_joint),
                                 point_grp_driver=[
                                     '%s02%s%s_%s' % (prefix, self.sj_prefix_value, side, suffix_parent_joint)],
                                 scale_driver=[
                                     '%s02%s%s_%s' % (prefix, self.sj_prefix_value, side, suffix_parent_joint)],
                                 side=side,
                                 joint_grp=joint_grp,
                                 rotation=rotation,
                                 rotation_pair_blend=rotation_pair_blend,
                                 offset_translation_position=offset_translation_position,
                                 offset_value=offset_value,
                                 position_name=position_name,
                                 )

            rlbb_pushJoint.Build(add_joint=add_joint,
                                 fk_ik_setup='%sBase%s_ctrl' % (prefix, side),
                                 controller_expand_name=prefix + '03',
                                 joint_driver_matrix='%s03%s%s_%s' % (
                                 prefix, self.sj_prefix_value, side, suffix_parent_joint),
                                 joint_add_target='%s03%s%s_%s' % (
                                 prefix, self.sAdd_prefix_value, side, suffix_duplicate_expand_joint),
                                 joint_driver_inverse_matrix='%s02%s%s_%s' % (
                                 prefix, self.sj_prefix_value, side, suffix_parent_joint),
                                 point_grp_driver=[
                                     '%s03%s%s_%s' % (prefix, self.sj_prefix_value, side, suffix_parent_joint)],
                                 scale_driver=[
                                     '%s03%s%s_%s' % (prefix, self.sj_prefix_value, side, suffix_parent_joint)],
                                 side=side,
                                 joint_grp=joint_grp,
                                 rotation=rotation,
                                 rotation_pair_blend=rotation_pair_blend,
                                 offset_translation_position=offset_translation_position,
                                 offset_value=offset_value,
                                 position_name=position_name,
                                 )
            if not thumb:
                rlbb_pushJoint.Build(add_joint=add_joint,
                                     fk_ik_setup='%sBase%s_ctrl' % (prefix, side),
                                     controller_expand_name=prefix + '04',
                                     joint_driver_matrix='%s04%s%s_%s' % (
                                     prefix, self.sj_prefix_value, side, suffix_parent_joint),
                                     joint_add_target='%s04%s%s_%s' % (
                                     prefix, self.sAdd_prefix_value, side, suffix_duplicate_expand_joint),
                                     joint_driver_inverse_matrix='%s03%s%s_%s' % (
                                     prefix, self.sj_prefix_value, side, suffix_parent_joint),
                                     point_grp_driver=[
                                         '%s04%s%s_%s' % (prefix, self.sj_prefix_value, side, suffix_parent_joint)],
                                     scale_driver=[
                                         '%s04%s%s_%s' % (prefix, self.sj_prefix_value, side, suffix_parent_joint)],
                                     side=side,
                                     joint_grp=joint_grp,
                                     rotation=rotation,
                                     rotation_pair_blend=rotation_pair_blend,
                                     offset_translation_position=offset_translation_position,
                                     offset_value=offset_value,
                                     position_name=position_name,
                                     )
        else:
            print('Expand joint', '%s%s%s_%s' % (prefix, self.sAdd_prefix_value, side, suffix_parent_joint),
                  'is already added!')
