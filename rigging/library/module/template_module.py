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
        self.cheekInUp_LFT = sj['%s%s%s%s_%s' % ('cheekInUp', origin_prefix, key_prefix, side_LFT, suffix)]
        self.cheekInLow_LFT = sj['%s%s%s%s_%s' % ('cheekInLow', origin_prefix, key_prefix, side_LFT, suffix)]

        # CHEEK MID LFT SIDE
        self.cheekUp_LFT = sj['%s%s%s%s_%s' % ('cheekUp', origin_prefix, key_prefix, side_LFT, suffix)]
        self.cheekMid_LFT = sj['%s%s%s%s_%s' % ('cheekMid', origin_prefix, key_prefix, side_LFT, suffix)]
        self.cheekLow_LFT = sj['%s%s%s%s_%s' % ('cheekLow', origin_prefix, key_prefix, side_LFT, suffix)]

        # CHEEK OUT LFT SIDE
        self.cheekOutUp_LFT = sj['%s%s%s%s_%s' % ('cheekOutUp', origin_prefix, key_prefix, side_LFT, suffix)]
        self.cheekOutLow_LFT = sj['%s%s%s%s_%s' % ('cheekOutLow', origin_prefix, key_prefix, side_LFT, suffix)]

        # CHEEK IN RGT SIDE
        self.cheekInUp_RGT = sj['%s%s%s%s_%s' % ('cheekInUp', origin_prefix, key_prefix, side_RGT, suffix)]
        self.cheekInLow_RGT = sj['%s%s%s%s_%s' % ('cheekInLow', origin_prefix, key_prefix, side_RGT, suffix)]

        # CHEEK MID RGT SIDE
        self.cheekUp_RGT = sj['%s%s%s%s_%s' % ('cheekUp', origin_prefix, key_prefix, side_RGT, suffix)]
        self.cheekMid_RGT = sj['%s%s%s%s_%s' % ('cheekMid', origin_prefix, key_prefix, side_RGT, suffix)]
        self.cheekLow_RGT = sj['%s%s%s%s_%s' % ('cheekLow', origin_prefix, key_prefix, side_RGT, suffix)]

        # CHEEK OUT RGT SIDE
        self.cheekOutUp_RGT = sj['%s%s%s%s_%s' % ('cheekOutUp', origin_prefix, key_prefix, side_RGT, suffix)]
        self.cheekOutLow_RGT = sj['%s%s%s%s_%s' % ('cheekOutLow', origin_prefix, key_prefix, side_RGT, suffix)]

        # BROW LFT SIDE
        self.browTw_LFT = sj['%s%s%s%s_%s' % ('browTw', origin_prefix, key_prefix, side_LFT, suffix)]
        self.browIn_LFT = sj['%s%s%s%s_%s' % ('browIn', origin_prefix, key_prefix, side_LFT, suffix)]
        self.browMid_LFT = sj['%s%s%s%s_%s' % ('browMid', origin_prefix, key_prefix, side_LFT, suffix)]
        self.browOut_LFT = sj['%s%s%s%s_%s' % ('browOut', origin_prefix, key_prefix, side_LFT, suffix)]
        self.browTip_LFT = sj['%s%s%s%s_%s' % ('browTip', origin_prefix, key_prefix, side_LFT, suffix)]

        # BROW RGT SIDE
        self.browTw_RGT = sj['%s%s%s%s_%s' % ('browTw', origin_prefix, key_prefix, side_RGT, suffix)]
        self.browIn_RGT = sj['%s%s%s%s_%s' % ('browIn', origin_prefix, key_prefix, side_RGT, suffix)]
        self.browMid_RGT = sj['%s%s%s%s_%s' % ('browMid', origin_prefix, key_prefix, side_RGT, suffix)]
        self.browOut_RGT = sj['%s%s%s%s_%s' % ('browOut', origin_prefix, key_prefix, side_RGT, suffix)]
        self.browTip_RGT = sj['%s%s%s%s_%s' % ('browTip', origin_prefix, key_prefix, side_RGT, suffix)]

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
        self.cheekBulge_LFT = sj['%s%s%s%s_%s' % ('cheekBulge', origin_prefix, key_prefix, side_LFT, suffix)]
        self.cheekBulge_RGT = sj['%s%s%s%s_%s' % ('cheekBulge', origin_prefix, key_prefix, side_RGT, suffix)]

        # DETAILS
        # mc.parent(self.root, 'tmpJnt_grp')

# class listFaceSkeletonDuplicate:
#     # HEAD PART AND FACE
#     def __init__(self, objDuplicate,
#                  valuePrefix,
#                  keyPrefix,
#                  suffix,
#                  sideLFT,
#                  sideRGT,
#                  oriPrefix='',
#                  ):
#
#         hide = mc.ls(type='joint')
#         mc.hide(hide)
#
#         # DUPLICATE SKELETON
#         sj = dt.listSkeletonDic(objDuplicate=objDuplicate,
#                                 valuePrefix=valuePrefix,
#                                 keyPrefix=keyPrefix,
#                                 oriPrefix=oriPrefix,
#                                 suffix=suffix)
#
#         # NECK AND HEAD
#         self.neck       = sj['%s%s%s_%s' % ('neck', oriPrefix, keyPrefix, suffix)]
#         self.neckInBtw  = sj['%s%s%s_%s' % ('neckInBtw', oriPrefix, keyPrefix, suffix)]
#         self.head       = sj['%s%s%s_%s' % ('head', oriPrefix, keyPrefix, suffix)]
#         self.headTip    = sj['%s%s%s_%s' % ('headTip', oriPrefix, keyPrefix, suffix)]
#
#         self.headUp      = sj['%s%s%s_%s' % ('headUp', oriPrefix, keyPrefix, suffix)]
#         self.headLow     = sj['%s%s%s_%s' % ('headLow', oriPrefix, keyPrefix, suffix)]
#         self.jaw         = sj['%s%s%s_%s' % ('jaw', oriPrefix, keyPrefix, suffix)]
#         self.jawTip      = sj['%s%s%s_%s' % ('jawTip', oriPrefix, keyPrefix, suffix)]
#         self.mouth       = sj['%s%s%s_%s' % ('mouth', oriPrefix, keyPrefix, suffix)]
#
#         self.mentolabial  = sj['%s%s%s_%s' % ('mentolabial', oriPrefix, keyPrefix, suffix)]
#         self.chin         = sj['%s%s%s_%s' % ('chin', oriPrefix, keyPrefix, suffix)]
#         self.browCenter   = sj['%s%s%s_%s' % ('browCenter', oriPrefix, keyPrefix, suffix)]
#
#         # CHEEK IN LFT SIDE
#         self.cheekInUpLFT    = sj['%s%s%s%s_%s' % ('cheekInUp', oriPrefix, keyPrefix, sideLFT, suffix)]
#         self.cheekInLowLFT   = sj['%s%s%s%s_%s' % ('cheekInLow', oriPrefix, keyPrefix, sideLFT, suffix)]
#
#         # CHEEK MID LFT SIDE
#         self.cheekUpLFT     = sj['%s%s%s%s_%s' % ('cheekUp', oriPrefix, keyPrefix, sideLFT, suffix)]
#         self.cheekMidLFT    = sj['%s%s%s%s_%s' % ('cheekMid', oriPrefix, keyPrefix, sideLFT, suffix)]
#         self.cheekLowLFT    = sj['%s%s%s%s_%s' % ('cheekLow', oriPrefix, keyPrefix, sideLFT, suffix)]
#
#         # CHEEK OUT LFT SIDE
#         self.cheekOutUpLFT    = sj['%s%s%s%s_%s' % ('cheekOutUp', oriPrefix, keyPrefix, sideLFT, suffix)]
#         self.cheekOutLowLFT   = sj['%s%s%s%s_%s' % ('cheekOutLow', oriPrefix, keyPrefix, sideLFT, suffix)]
#
#         # CHEEK IN RGT SIDE
#         self.cheekInUpRGT     = sj['%s%s%s%s_%s' % ('cheekInUp', oriPrefix, keyPrefix, sideRGT, suffix)]
#         self.cheekInLowRGT    = sj['%s%s%s%s_%s' % ('cheekInLow', oriPrefix, keyPrefix, sideRGT, suffix)]
#
#         # CHEEK MID RGT SIDE
#         self.cheekUpRGT     = sj['%s%s%s%s_%s' % ('cheekUp', oriPrefix, keyPrefix, sideRGT, suffix)]
#         self.cheekMidRGT    = sj['%s%s%s%s_%s' % ('cheekMid', oriPrefix, keyPrefix, sideRGT, suffix)]
#         self.cheekLowRGT    = sj['%s%s%s%s_%s' % ('cheekLow', oriPrefix, keyPrefix, sideRGT, suffix)]
#
#         # CHEEK OUT RGT SIDE
#         self.cheekOutUpRGT    = sj['%s%s%s%s_%s' % ('cheekOutUp', oriPrefix, keyPrefix, sideRGT, suffix)]
#         self.cheekOutLowRGT  = sj['%s%s%s%s_%s' % ('cheekOutLow', oriPrefix, keyPrefix, sideRGT, suffix)]
#
#         # BROW LFT SIDE
#         self.browTwLFT     = sj['%s%s%s%s_%s' % ('browTw', oriPrefix, keyPrefix, sideLFT, suffix)]
#         self.browInLFT     = sj['%s%s%s%s_%s' % ('browIn', oriPrefix, keyPrefix, sideLFT, suffix)]
#         self.browMidLFT    = sj['%s%s%s%s_%s' % ('browMid', oriPrefix, keyPrefix, sideLFT, suffix)]
#         self.browOutLFT   = sj['%s%s%s%s_%s' % ('browOut', oriPrefix, keyPrefix, sideLFT, suffix)]
#         self.browTipLFT   = sj['%s%s%s%s_%s' % ('browTip', oriPrefix, keyPrefix, sideLFT, suffix)]
#
#         # BROW RGT SIDE
#         self.browTwRGT    = sj['%s%s%s%s_%s' % ('browTw', oriPrefix, keyPrefix, sideRGT, suffix)]
#         self.browInRGT     = sj['%s%s%s%s_%s' % ('browIn', oriPrefix, keyPrefix, sideRGT, suffix)]
#         self.browMidRGT    = sj['%s%s%s%s_%s' % ('browMid', oriPrefix, keyPrefix, sideRGT, suffix)]
#         self.browOutRGT   = sj['%s%s%s%s_%s' % ('browOut', oriPrefix, keyPrefix, sideRGT, suffix)]
#         self.browTipRGT   = sj['%s%s%s%s_%s' % ('browTip', oriPrefix, keyPrefix, sideRGT, suffix)]
#
#         # NOSE
#         self.nose    = sj['%s%s%s_%s' % ('nose', oriPrefix, keyPrefix, suffix)]
#         self.noseUp    = sj['%s%s%s_%s' % ('noseUp', oriPrefix, keyPrefix, suffix)]
#         self.columella  = sj['%s%s%s_%s' % ('columella', oriPrefix, keyPrefix, suffix)]
#
#         # EYEAIM
#         self.eyeLFT = sj['%s%s%s%s_%s' % ('eye', oriPrefix, keyPrefix, sideLFT, suffix)]
#         self.eyeRGT = sj['%s%s%s%s_%s' % ('eye', oriPrefix, keyPrefix, sideRGT, suffix)]
#
#         # EYEBALL
#         self.eyeballLFT = sj['%s%s%s%s_%s' % ('eyeball', oriPrefix, keyPrefix, sideLFT, suffix)]
#         self.eyeballRGT = sj['%s%s%s%s_%s' % ('eyeball', oriPrefix, keyPrefix, sideRGT, suffix)]
#
#         # PUPIL AND IRIS
#         self.pupilLFT = sj['%s%s%s%s_%s' % ('pupil', oriPrefix, keyPrefix, sideLFT, suffix)]
#         self.irisLFT = sj['%s%s%s%s_%s' % ('iris', oriPrefix, keyPrefix, sideLFT, suffix)]
#
#         self.pupilRGT = sj['%s%s%s%s_%s' % ('pupil', oriPrefix, keyPrefix, sideRGT, suffix)]
#         self.irisRGT = sj['%s%s%s%s_%s' % ('iris', oriPrefix, keyPrefix, sideRGT, suffix)]
#
#         # EAR
#         self.earLFT = sj['%s%s%s%s_%s' % ('ear', oriPrefix, keyPrefix, sideLFT, suffix)]
#         self.earRGT = sj['%s%s%s%s_%s' % ('ear', oriPrefix, keyPrefix, sideRGT, suffix)]
#
#         # TEETH
#         self.upperTeeth = sj['%s%s%s_%s' % ('upperTeeth', oriPrefix, keyPrefix, suffix)]
#         self.lowerTeeth = sj['%s%s%s_%s' % ('lowerTeeth', oriPrefix, keyPrefix, suffix)]
#
#         # TOUNGE
#         self.tongue01 = sj['%s%s%s_%s' % ('tongue01', oriPrefix, keyPrefix, suffix)]
#         self.tongue02 = sj['%s%s%s_%s' % ('tongue02', oriPrefix, keyPrefix, suffix)]
#         self.tongue03 = sj['%s%s%s_%s' % ('tongue03', oriPrefix, keyPrefix, suffix)]
#         self.tongue04 = sj['%s%s%s_%s' % ('tongue04', oriPrefix, keyPrefix, suffix)]
#
#         # BULGE
#         self.cheekBulgeLFT =  sj['%s%s%s%s_%s' % ('cheekBulge', oriPrefix, keyPrefix, sideLFT, suffix)]
#         self.cheekBulgeRGT =  sj['%s%s%s%s_%s' % ('cheekBulge', oriPrefix, keyPrefix, sideRGT, suffix)]
#
#
#         mc.parent(self.neck, world=True)
