from __builtin__ import reload

import maya.cmds as mc

from rigging.library.utils import template_skeleton as ts

reload (ts)


class listSkeletonDuplicate:
    def __init__(self,
                 value_prefix,
                 key_prefix,
                 suffix,
                 side_LFT,
                 side_RGT,
                 origin_prefix='',
                 ):

        hide = mc.ls(type='joint')
        mc.hide(hide)

        # DUPLICATE SKELETON
        sj = ts.list_skeleton_dic(obj_duplicate='rootTmp_jnt',
                                  value_prefix=value_prefix,
                                  key_prefix=key_prefix,
                                  oriPrefix=origin_prefix,

                                  suffix=suffix)

        # ROOT, SPINE AND PELVIS
        self.root = sj['%s%s%s_%s' % ('root', origin_prefix, key_prefix, suffix)]
        self.spine_list = [sj['%s%s%s_%s' % ('spine01', origin_prefix, key_prefix, suffix)],
                           sj['%s%s%s_%s' % ('spine02', origin_prefix, key_prefix, suffix)],
                           sj['%s%s%s_%s' % ('spine03', origin_prefix, key_prefix, suffix)],
                           sj['%s%s%s_%s' % ('spine04', origin_prefix, key_prefix, suffix)]]

        self.pelvis = sj['%s%s%s_%s' % ('pelvis', origin_prefix, key_prefix, suffix)]

        # ARM LFT SIDE
        self.clav_LFT = sj['%s%s%s%s_%s' % ('clav', origin_prefix, key_prefix, side_LFT, suffix)]
        self.upArm_LFT = sj['%s%s%s%s_%s' % ('upArm', origin_prefix, key_prefix, side_LFT, suffix)]
        self.forearm_LFT = sj['%s%s%s%s_%s' % ('forearm', origin_prefix, key_prefix, side_LFT, suffix)]
        self.wrist_LFT = sj['%s%s%s%s_%s' % ('wrist', origin_prefix, key_prefix, side_LFT, suffix)]
        self.hand_LFT = sj['%s%s%s%s_%s' % ('hand', origin_prefix, key_prefix, side_LFT, suffix)]

        self.thumb1_LFT = sj['%s%s%s%s_%s' % ('thumb01', origin_prefix, key_prefix, side_LFT, suffix)]
        self.index1_LFT = sj['%s%s%s%s_%s' % ('index01', origin_prefix, key_prefix, side_LFT, suffix)]
        self.middle1_LFT = sj['%s%s%s%s_%s' % ('middle01', origin_prefix, key_prefix, side_LFT, suffix)]
        self.ring1_LFT = sj['%s%s%s%s_%s' % ('ring01', origin_prefix, key_prefix, side_LFT, suffix)]
        self.pinky1_LFT = sj['%s%s%s%s_%s' % ('pinky01', origin_prefix, key_prefix, side_LFT, suffix)]

        self.thumb2_LFT = sj['%s%s%s%s_%s' % ('thumb02', origin_prefix, key_prefix, side_LFT, suffix)]
        self.index2_LFT = sj['%s%s%s%s_%s' % ('index02', origin_prefix, key_prefix, side_LFT, suffix)]
        self.middle2_LFT = sj['%s%s%s%s_%s' % ('middle02', origin_prefix, key_prefix, side_LFT, suffix)]
        self.ring2_LFT   = sj['%s%s%s%s_%s' % ('ring02', origin_prefix, key_prefix, side_LFT, suffix)]
        self.pinky2_LFT  = sj['%s%s%s%s_%s' % ('pinky02', origin_prefix, key_prefix, side_LFT, suffix)]

        self.thumb3_LFT  = sj['%s%s%s%s_%s' % ('thumb03', origin_prefix, key_prefix, side_LFT, suffix)]
        self.index3_LFT  = sj['%s%s%s%s_%s' % ('index03', origin_prefix, key_prefix, side_LFT, suffix)]
        self.middle3_LFT = sj['%s%s%s%s_%s' % ('middle03', origin_prefix, key_prefix, side_LFT, suffix)]
        self.ring3_LFT   = sj['%s%s%s%s_%s' % ('ring03', origin_prefix, key_prefix, side_LFT, suffix)]
        self.pinky3_LFT  = sj['%s%s%s%s_%s' % ('pinky03', origin_prefix, key_prefix, side_LFT, suffix)]

        self.thumb4_LFT  = sj['%s%s%s%s_%s' % ('thumb04', origin_prefix, key_prefix, side_LFT, suffix)]
        self.index4_LFT  = sj['%s%s%s%s_%s' % ('index04', origin_prefix, key_prefix, side_LFT, suffix)]
        self.middle4_LFT = sj['%s%s%s%s_%s' % ('middle04', origin_prefix, key_prefix, side_LFT, suffix)]
        self.ring4_LFT   = sj['%s%s%s%s_%s' % ('ring04', origin_prefix, key_prefix, side_LFT, suffix)]
        self.pinky4_LFT  = sj['%s%s%s%s_%s' % ('pinky04', origin_prefix, key_prefix, side_LFT, suffix)]

        self.index5_LFT  = sj['%s%s%s%s_%s' % ('index05', origin_prefix, key_prefix, side_LFT, suffix)]
        self.middle5_LFT = sj['%s%s%s%s_%s' % ('middle05', origin_prefix, key_prefix, side_LFT, suffix)]
        self.ring5_LFT   = sj['%s%s%s%s_%s' % ('ring05', origin_prefix, key_prefix, side_LFT, suffix)]
        self.pinky5_LFT  = sj['%s%s%s%s_%s' % ('pinky05', origin_prefix, key_prefix, side_LFT, suffix)]

        self.palm_LFT    = sj['%s%s%s%s_%s' % ('palm', origin_prefix, key_prefix, side_LFT, suffix)]


        # ARM RGT SIDE
        self.clav_RGT    = sj['%s%s%s%s_%s' % ('clav', origin_prefix, key_prefix, side_RGT, suffix)]
        self.upArm_RGT   = sj['%s%s%s%s_%s' % ('upArm', origin_prefix, key_prefix, side_RGT, suffix)]
        self.forearm_RGT = sj['%s%s%s%s_%s' % ('forearm', origin_prefix, key_prefix, side_RGT, suffix)]
        self.wrist_RGT   = sj['%s%s%s%s_%s' % ('wrist', origin_prefix, key_prefix, side_RGT, suffix)]
        self.hand_RGT    = sj['%s%s%s%s_%s' % ('hand', origin_prefix, key_prefix, side_RGT, suffix)]

        self.thumb1_RGT  = sj['%s%s%s%s_%s' % ('thumb01', origin_prefix, key_prefix, side_RGT, suffix)]
        self.index1_RGT  = sj['%s%s%s%s_%s' % ('index01', origin_prefix, key_prefix, side_RGT, suffix)]
        self.middle1_RGT = sj['%s%s%s%s_%s' % ('middle01', origin_prefix, key_prefix, side_RGT, suffix)]
        self.ring1_RGT   = sj['%s%s%s%s_%s' % ('ring01', origin_prefix, key_prefix, side_RGT, suffix)]
        self.pinky1_RGT  = sj['%s%s%s%s_%s' % ('pinky01', origin_prefix, key_prefix, side_RGT, suffix)]

        self.thumb2_RGT  = sj['%s%s%s%s_%s' % ('thumb02', origin_prefix, key_prefix, side_RGT, suffix)]
        self.index2_RGT  = sj['%s%s%s%s_%s' % ('index02', origin_prefix, key_prefix, side_RGT, suffix)]
        self.middle2_RGT = sj['%s%s%s%s_%s' % ('middle02', origin_prefix, key_prefix, side_RGT, suffix)]
        self.ring2_RGT   = sj['%s%s%s%s_%s' % ('ring02', origin_prefix, key_prefix, side_RGT, suffix)]
        self.pinky2_RGT  = sj['%s%s%s%s_%s' % ('pinky02', origin_prefix, key_prefix, side_RGT, suffix)]

        self.thumb3_RGT  = sj['%s%s%s%s_%s' % ('thumb03', origin_prefix, key_prefix, side_RGT, suffix)]
        self.index3_RGT  = sj['%s%s%s%s_%s' % ('index03', origin_prefix, key_prefix, side_RGT, suffix)]
        self.middle3_RGT = sj['%s%s%s%s_%s' % ('middle03', origin_prefix, key_prefix, side_RGT, suffix)]
        self.ring3_RGT   = sj['%s%s%s%s_%s' % ('ring03', origin_prefix, key_prefix, side_RGT, suffix)]
        self.pinky3_RGT  = sj['%s%s%s%s_%s' % ('pinky03', origin_prefix, key_prefix, side_RGT, suffix)]

        self.thumb4_RGT  = sj['%s%s%s%s_%s' % ('thumb04', origin_prefix, key_prefix, side_RGT, suffix)]
        self.index4_RGT  = sj['%s%s%s%s_%s' % ('index04', origin_prefix, key_prefix, side_RGT, suffix)]
        self.middle4_RGT = sj['%s%s%s%s_%s' % ('middle04', origin_prefix, key_prefix, side_RGT, suffix)]
        self.ring4_RGT   = sj['%s%s%s%s_%s' % ('ring04', origin_prefix, key_prefix, side_RGT, suffix)]
        self.pinky4_RGT  = sj['%s%s%s%s_%s' % ('pinky04', origin_prefix, key_prefix, side_RGT, suffix)]

        self.index5_RGT  = sj['%s%s%s%s_%s' % ('index05', origin_prefix, key_prefix, side_RGT, suffix)]
        self.middle5_RGT = sj['%s%s%s%s_%s' % ('middle05', origin_prefix, key_prefix, side_RGT, suffix)]
        self.ring5_RGT   = sj['%s%s%s%s_%s' % ('ring05', origin_prefix, key_prefix, side_RGT, suffix)]
        self.pinky5_RGT  = sj['%s%s%s%s_%s' % ('pinky05', origin_prefix, key_prefix, side_RGT, suffix)]

        self.palm_RGT    = sj['%s%s%s%s_%s' % ('palm', origin_prefix, key_prefix, side_RGT, suffix)]

        # LEG LFT SIDE
        self.upLeg_LFT   = sj['%s%s%s%s_%s' % ('upLeg', origin_prefix, key_prefix, side_LFT, suffix)]
        self.lowLeg_LFT  = sj['%s%s%s%s_%s' % ('lowLeg', origin_prefix, key_prefix, side_LFT, suffix)]
        self.ankle_LFT   = sj['%s%s%s%s_%s' % ('ankle', origin_prefix, key_prefix, side_LFT, suffix)]
        self.ball_LFT    = sj['%s%s%s%s_%s' % ('ball', origin_prefix, key_prefix, side_LFT, suffix)]
        self.toe_LFT     = sj['%s%s%s%s_%s' % ('toe', origin_prefix, key_prefix, side_LFT, suffix)]
        self.heel_LFT    = sj['%s%s%s%s_%s' % ('heel', origin_prefix, key_prefix, side_LFT, suffix)]
        self.footIn_LFT  = sj['%s%s%s%s_%s' % ('footIn', origin_prefix, key_prefix, side_LFT, suffix)]
        self.footOut_LFT = sj['%s%s%s%s_%s' % ('footOut', origin_prefix, key_prefix, side_LFT, suffix)]

        # LEG RGT SIDE
        self.upLeg_RGT   = sj['%s%s%s%s_%s' % ('upLeg', origin_prefix, key_prefix, side_RGT, suffix)]
        self.lowLeg_RGT  = sj['%s%s%s%s_%s' % ('lowLeg', origin_prefix, key_prefix, side_RGT, suffix)]
        self.ankle_RGT   = sj['%s%s%s%s_%s' % ('ankle', origin_prefix, key_prefix, side_RGT, suffix)]
        self.ball_RGT    = sj['%s%s%s%s_%s' % ('ball', origin_prefix, key_prefix, side_RGT, suffix)]
        self.toe_RGT     = sj['%s%s%s%s_%s' % ('toe', origin_prefix, key_prefix, side_RGT, suffix)]
        self.heel_RGT    = sj['%s%s%s%s_%s' % ('heel', origin_prefix, key_prefix, side_RGT, suffix)]
        self.footIn_RGT  = sj['%s%s%s%s_%s' % ('footIn', origin_prefix, key_prefix, side_RGT, suffix)]
        self.footOut_RGT = sj['%s%s%s%s_%s' % ('footOut', origin_prefix, key_prefix, side_RGT, suffix)]

        # NECK AND HEAD
        self.neck = sj['%s%s%s_%s' % ('neck', origin_prefix, key_prefix, suffix)]
        self.neckIn_Btw = sj['%s%s%s_%s' % ('neckInBtw', origin_prefix, key_prefix, suffix)]
        self.head = sj['%s%s%s_%s' % ('head', origin_prefix, key_prefix, suffix)]
        self.head_tip = sj['%s%s%s_%s' % ('headTip', origin_prefix, key_prefix, suffix)]

        self.head_up = sj['%s%s%s_%s' % ('headUp', origin_prefix, key_prefix, suffix)]
        self.head_low = sj['%s%s%s_%s' % ('headLow', origin_prefix, key_prefix, suffix)]
        self.jaw = sj['%s%s%s_%s' % ('jaw', origin_prefix, key_prefix, suffix)]
        self.jaw_tip = sj['%s%s%s_%s' % ('jawTip', origin_prefix, key_prefix, suffix)]
        self.mouth = sj['%s%s%s_%s' % ('mouth', origin_prefix, key_prefix, suffix)]

        self.mentolabial = sj['%s%s%s_%s' % ('mentolabial', origin_prefix, key_prefix, suffix)]
        self.chin = sj['%s%s%s_%s' % ('chin', origin_prefix, key_prefix, suffix)]
        self.brow_center = sj['%s%s%s_%s' % ('browCenter', origin_prefix, key_prefix, suffix)]

        # CHEEK IN LFT SIDE
        self.cheek_in_up_LFT = sj['%s%s%s%s_%s' % ('cheekInUp', origin_prefix, key_prefix, side_LFT, suffix)]
        self.cheek_in_low_LFT = sj['%s%s%s%s_%s' % ('cheekInLow', origin_prefix, key_prefix, side_LFT, suffix)]

        # CHEEK MID LFT SIDE
        self.cheek_up_LFT = sj['%s%s%s%s_%s' % ('cheekUp', origin_prefix, key_prefix, side_LFT, suffix)]
        self.cheek_mid_LFT = sj['%s%s%s%s_%s' % ('cheekMid', origin_prefix, key_prefix, side_LFT, suffix)]
        self.cheek_low_LFT = sj['%s%s%s%s_%s' % ('cheekLow', origin_prefix, key_prefix, side_LFT, suffix)]

        # CHEEK OUT LFT SIDE
        self.cheek_out_up_LFT = sj['%s%s%s%s_%s' % ('cheekOutUp', origin_prefix, key_prefix, side_LFT, suffix)]
        self.cheek_out_low_LFT = sj['%s%s%s%s_%s' % ('cheekOutLow', origin_prefix, key_prefix, side_LFT, suffix)]

        # CHEEK IN RGT SIDE
        self.cheek_in_up_RGT = sj['%s%s%s%s_%s' % ('cheekInUp', origin_prefix, key_prefix, side_RGT, suffix)]
        self.cheek_in_low_RGT = sj['%s%s%s%s_%s' % ('cheekInLow', origin_prefix, key_prefix, side_RGT, suffix)]

        # CHEEK MID RGT SIDE
        self.cheek_up_RGT = sj['%s%s%s%s_%s' % ('cheekUp', origin_prefix, key_prefix, side_RGT, suffix)]
        self.cheek_mid_RGT = sj['%s%s%s%s_%s' % ('cheekMid', origin_prefix, key_prefix, side_RGT, suffix)]
        self.cheek_low_RGT = sj['%s%s%s%s_%s' % ('cheekLow', origin_prefix, key_prefix, side_RGT, suffix)]

        # CHEEK OUT RGT SIDE
        self.cheek_out_up_RGT = sj['%s%s%s%s_%s' % ('cheekOutUp', origin_prefix, key_prefix, side_RGT, suffix)]
        self.cheek_out_low_RGT = sj['%s%s%s%s_%s' % ('cheekOutLow', origin_prefix, key_prefix, side_RGT, suffix)]

        # BROW LFT SIDE
        self.brow_tweak_LFT = sj['%s%s%s%s_%s' % ('browTw', origin_prefix, key_prefix, side_LFT, suffix)]
        self.brow_in_LFT = sj['%s%s%s%s_%s' % ('browIn', origin_prefix, key_prefix, side_LFT, suffix)]
        self.brow_mid_LFT = sj['%s%s%s%s_%s' % ('browMid', origin_prefix, key_prefix, side_LFT, suffix)]
        self.brow_out_LFT = sj['%s%s%s%s_%s' % ('browOut', origin_prefix, key_prefix, side_LFT, suffix)]
        self.brow_tip_LFT = sj['%s%s%s%s_%s' % ('browTip', origin_prefix, key_prefix, side_LFT, suffix)]

        # BROW RGT SIDE
        self.brow_tweak_RGT = sj['%s%s%s%s_%s' % ('browTw', origin_prefix, key_prefix, side_RGT, suffix)]
        self.brow_in_RGT = sj['%s%s%s%s_%s' % ('browIn', origin_prefix, key_prefix, side_RGT, suffix)]
        self.brow_mid_RGT = sj['%s%s%s%s_%s' % ('browMid', origin_prefix, key_prefix, side_RGT, suffix)]
        self.brow_out_RGT = sj['%s%s%s%s_%s' % ('browOut', origin_prefix, key_prefix, side_RGT, suffix)]
        self.brow_tip_RGT = sj['%s%s%s%s_%s' % ('browTip', origin_prefix, key_prefix, side_RGT, suffix)]

        # NOSE
        self.nose = sj['%s%s%s_%s' % ('nose', origin_prefix, key_prefix, suffix)]
        self.nose_up = sj['%s%s%s_%s' % ('noseUp', origin_prefix, key_prefix, suffix)]
        self.columella = sj['%s%s%s_%s' % ('columella', origin_prefix, key_prefix, suffix)]

        # EYEAIM
        self.eye_LFT = sj['%s%s%s%s_%s' % ('eye', origin_prefix, key_prefix, side_LFT, suffix)]
        self.eye_RGT = sj['%s%s%s%s_%s' % ('eye', origin_prefix, key_prefix, side_RGT, suffix)]

        # EYEBALL
        self.eyeball_LFT = sj['%s%s%s%s_%s' % ('eyeball', origin_prefix, key_prefix, side_LFT, suffix)]
        self.eyeball_RGT = sj['%s%s%s%s_%s' % ('eyeball', origin_prefix, key_prefix, side_RGT, suffix)]

        # PUPIL AND IRIS
        self.pupil_LFT = sj['%s%s%s%s_%s' % ('pupil', origin_prefix, key_prefix, side_LFT, suffix)]
        self.iris_LFT = sj['%s%s%s%s_%s' % ('iris', origin_prefix, key_prefix, side_LFT, suffix)]

        self.pupil_RGT = sj['%s%s%s%s_%s' % ('pupil', origin_prefix, key_prefix, side_RGT, suffix)]
        self.iris_RGT = sj['%s%s%s%s_%s' % ('iris', origin_prefix, key_prefix, side_RGT, suffix)]

        # EAR
        self.ear_LFT = sj['%s%s%s%s_%s' % ('ear', origin_prefix, key_prefix, side_LFT, suffix)]
        self.ear_RGT = sj['%s%s%s%s_%s' % ('ear', origin_prefix, key_prefix, side_RGT, suffix)]

        # TEETH
        self.upper_teeth = sj['%s%s%s_%s' % ('upperTeeth', origin_prefix, key_prefix, suffix)]
        self.lower_teeth = sj['%s%s%s_%s' % ('lowerTeeth', origin_prefix, key_prefix, suffix)]

        # TOUNGE
        self.tongue01 = sj['%s%s%s_%s' % ('tongue01', origin_prefix, key_prefix, suffix)]
        self.tongue02 = sj['%s%s%s_%s' % ('tongue02', origin_prefix, key_prefix, suffix)]
        self.tongue03 = sj['%s%s%s_%s' % ('tongue03', origin_prefix, key_prefix, suffix)]
        self.tongue04 = sj['%s%s%s_%s' % ('tongue04', origin_prefix, key_prefix, suffix)]

        # BULGE
        self.cheek_bulge_LFT = sj['%s%s%s%s_%s' % ('cheekBulge', origin_prefix, key_prefix, side_LFT, suffix)]
        self.cheek_bulge_RGT = sj['%s%s%s%s_%s' % ('cheekBulge', origin_prefix, key_prefix, side_RGT, suffix)]

        # DETAILS
        # mc.parent(self.root, 'tmpJnt_grp')
