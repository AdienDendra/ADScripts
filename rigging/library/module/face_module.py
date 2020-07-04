from __builtin__ import reload

import maya.cmds as mc

from rigging.library.module import template_module as tm, base_module as bs
from rigging.library.module.face import lidOut_module as lo, nose_module as nm, brow_module as bm, lip_module as lm, \
    blendshape_module as bsm, cheek_module as cm, lid_module as ld, chin_module as ch, ear_module as er, \
    bulge_module as bl, head_module as hm
from rigging.library.utils import controller as ct
from rigging.tools import AD_utils as au

reload(ct)
reload(hm)
reload(lm)
reload(cm)
reload(tm)
reload(nm)
reload(ld)
reload(lo)
reload(ch)
reload(bm)
reload(bl)
reload(er)
reload(bsm)
reload(au)
reload(bs)


def BuildRig(
             offsetJnt02BindLipPosCheek,
             offsetJnt02BindLipPosNose,
             offsetJnt04BindLipPosNose,
             directionLip01Cheek,
             directionLip02Cheek,
             scale,
             sideLFT,
             sideRGT,
             suffixController,

             cheekLowPrefix,
             cheekMidPrefix,
             cheekUpPrefix,
             cheekInUpPrefix,
             cheekInLowPrefix,

             cheekOutUpPrefix,
             cheekOutLowPrefix,
             crvUpLip,
             crvLowLip,
             crvUpLipRoll,
             crvLowLipRoll,
             positionMouthCtrl,
             crvNose,

             jawPrefix,
             jawTipPrefix,
             headPrefix,
             neckPrefix,
             neckInBtwPrefix,
             headUpPrefix,
             headLowPrefix,
             columellaPrefix,

             crvUpLidLFT,
             crvLowLidLFT,
             crvUpLidRGT,
             crvLowLidRGT,
             eyePrefix,
             eyeAimPrefix,
             directionLid01,
             directionLid02,
             directionLid03,
             directionLid04,
             directionLid05,
             positionEyeAimCtrl,

             eyeCtrlDirection,

             offsetLidPos02,
             offsetLidPos04,
             noseFollowMouthValue,

             crvUpLidOutLFT,
             crvLowLidOutLFT,
             crvUpLidOutRGT,
             crvLowLidOutRGT,
             offsetJnt02BindLipPosLidOut,
             offsetJnt04BindLipPosLidOut,
             directionCtrlLidOut01,
             directionCtrlLidOut02,
             directionCtrlLidOut03,
             directionCtrlLidOut04,
             directionCtrlLidOut05,
             pupilPrefix,
             irisPrefix,

             mentolabialPrefix,
             chinPrefix,

             earPrefix,

             browTwPrefix,
             browInPrefix,
             browMidPrefix,
             browOutPrefix,
             browsPrefix,
             browTipPrefix,
             browCenterPrefix,
             browInGrpRotOffset,
             browMidGrpRotOffset,
             browOutGrpRotOffset,
             browTipGrpRotOffset,

             lowLidFolDown,
             upLidFolDownLowLidFolUp,
             upLidLRLowLidLR,
             upLidFolUp,

             bulgeMesh,
             addSetBulge,
             faceCurvesGrp,
             suffixJoint
            ):

    # FINGER POSITION
    BaseF = 'Base'
    UpF = 'Up'
    MidF = 'Mid'
    LowF = 'Low'

    if not mc.objExists('animGmbl_ctrl'):
        base_controller = bs.Base(scale=scale)
        face_non_transform_grp = base_controller.face_non_transform_grp
        face_controller_grp = base_controller.face_controller_grp
    else:
        face_non_transform_grp = 'faceNonTransform_grp'
        face_controller_grp = 'faceCtrl_grp'

    # # CREATE GENERAL GROUP
    # face_utils_grp = mc.group(em=1, n='faceUtils_grp')
    # mc.setAttr(face_utils_grp + '.it', 0, l=1)
    #
    # face_controller_grp = mc.group(em=1, n='faceAnim_grp')
    # mc.setAttr(face_controller_grp + '.it', 0, l=1)
    # au.lock_hide_attr(['t', 'r', 's'], face_controller_grp)

# ======================================================================================================================
#                                              DUPLICATE JOINTS AS DRIVER
# ======================================================================================================================
    sj = tm.listSkeletonDuplicate(value_prefix='',
                                  key_prefix='Ori',
                                  suffix=suffixJoint,
                                  side_LFT=sideLFT,
                                  side_RGT=sideRGT
                                  )
    mc.parent(sj.neck, world=True)
    mc.delete(sj.root)

    # ROTATE EYE JNT
    mc.setAttr(sj.eyeball_LFT + '.rotateY', eyeCtrlDirection)
    mc.setAttr(sj.eyeball_RGT + '.rotateY', eyeCtrlDirection * -1)
    mc.makeIdentity(sj.eyeball_LFT, apply=True)
    mc.makeIdentity(sj.eyeball_RGT, apply=True)

    # JOINT DQ BASE
    mc.select(cl=1)
    jntDQBase = mc.joint(n='headDQBase_jnt')
    mc.delete(mc.parentConstraint(sj.neck, jntDQBase))
    mc.makeIdentity(jntDQBase, apply=1, translate=1, rotate=1)
    mc.parent((jntDQBase, face_non_transform_grp))

    print ('5%  | skeleton duplicated is done!')

    # ==================================================================================================================
    #                                                     HEAD PARAMETERS
    # ==================================================================================================================

    head = hm.Head(faceAnimCtrlGrp=face_controller_grp,
                   faceUtilsGrp=face_non_transform_grp,
                   neckJnt=sj.neck,
                   neckInBtwJnt=sj.neckIn_Btw,
                   headJnt= sj.head,
                   jawJnt= sj.jaw,
                   jawTipJnt=sj.jaw_tip,
                   headUpJnt=sj.head_up,
                   headLowJnt=sj.head_low,
                   jawPrefix=jawPrefix,
                   jawTipPrefix= jawTipPrefix,
                   headPrefix=headPrefix,
                   neckPrefix=neckPrefix,
                   neckInBtwPrefix=neckInBtwPrefix,
                   headUpPrefix=headUpPrefix,
                   headLowPrefix=headLowPrefix,
                   eyeAimPrefix=eyeAimPrefix,
                   eyeJntLFT=sj.eye_LFT,
                   eyeJntRGT=sj.eye_RGT,
                   positionEyeAimCtrl=positionEyeAimCtrl,
                   upperTeethJnt=sj.upper_teeth,
                   lowerTeethJnt=sj.lower_teeth,
                   tongue01Jnt=sj.tongue01,
                   tongue02Jnt=sj.tongue02,
                   tongue03Jnt=sj.tongue03,
                   tongue04Jnt=sj.tongue04,
                   scale=scale,
                   suffixController=suffixController)

    print ('10% | head is done!')
    # ==================================================================================================================
    #                                                     LIP PARAMETERS
    # ==================================================================================================================
    lip = lm.Lip(faceAnimCtrlGrp=face_controller_grp,
                 faceUtilsGrp=face_non_transform_grp,
                 crvUpLip=crvUpLip,
                 crvLowLip=crvLowLip,
                 crvUpLipRoll=crvUpLipRoll,
                 crvLowLipRoll=crvLowLipRoll,
                 offsetJnt02BindPos=offsetJnt02BindLipPosCheek,
                 scale=scale,
                 directionLip01Cheek=directionLip01Cheek,
                 directionLip02Cheek=directionLip02Cheek,
                 sideLFT=sideLFT,
                 sideRGT=sideRGT,
                 jawJnt=sj.jaw,
                 headLowJnt=sj.head_low,
                 mouthJnt=sj.mouth,
                 positionMouthCtrl=positionMouthCtrl,
                 suffixController=suffixController,
                 jaw_ctrl=head.jawCtrl,
                 prefix_upLip_follow=head.attr_upLip_follow,
                 headLow_normal_rotationGrp=head.headLow_normal_rotationGrp)

    print ('15% | lip is done!')
    # ==================================================================================================================
    #                                                     NOSE PARAMETERS
    # ==================================================================================================================
    nose = nm.Nose(faceUtilsGrp=face_non_transform_grp,
                   columellaJnt=sj.columella,
                   noseJnt=sj.nose,
                   noseUpJnt=sj.nose_up,
                   columellaPrefix=columellaPrefix,
                   crvNose=crvNose,
                   offsetJnt02BindPos=offsetJnt02BindLipPosNose,
                   offsetJnt04BindPos=offsetJnt04BindLipPosNose,
                   directionCtrl01=0,
                   directionCtrl02=0,
                   directionCtrl03=0,
                   directionCtrl04=0,
                   directionCtrl05=0,
                   ctrlColor='lightPink',
                   shape=ct.JOINT,
                   scale=scale,
                   headCtrlGimbal=head.headCtrlGimbal,
                   headUpCtrlGimbal=head.headUpCtrlGimbal,
                   headJnt=sj.head,
                   positionMouthCtrl=positionMouthCtrl,
                   sideLFT=sideLFT,
                   sideRGT=sideRGT,
                   lipCornerCtrlLFT=lip.cornerLipCtrlLFT,
                   lipCornerCtrlRGT=lip.cornerLipCtrlRGT,
                   nostrilAttrCtrlLFT=lip.nostrilCtrlAttrLFT,
                   nostrilAttrCtrlRGT=lip.nostrilCtrlAttrRGT,
                   upLipControllerAll=lip.upLipControllerAll,
                   mouthCtrl=lip.mouthCtrl,
                   noseFollowMouthValue= noseFollowMouthValue,
                   upLipAllCtrlZroGrp=lip.upLipMouthCtrlGrp,
                   jawCtrl = head.jawCtrl,
                   suffixController=suffixController)

    print ('25% | nose is done!')
    # ==================================================================================================================
    #                                                     CHEEK PARAMETERS
    # ==================================================================================================================

    leftCheek = cm.Cheek(faceAnimCtrlGrp=face_controller_grp,
                         faceUtilsGrp=face_non_transform_grp,
                         cheekLowJnt=sj.cheekLow_LFT,
                         cheekLowPrefix=cheekLowPrefix,
                         cheekMidJnt=sj.cheekMid_LFT,
                         cheekMidPrefix=cheekMidPrefix,
                         cheekUpJnt=sj.cheekUp_LFT,
                         cheekUpPrefix=cheekUpPrefix,
                         cheekInUpJnt=sj.cheekInUp_LFT,
                         cheekInUpPrefix=cheekInUpPrefix,
                         cheekInLowJnt=sj.cheekInLow_LFT,
                         cheekInLowPrefix=cheekInLowPrefix,
                         cheekOutUpJnt=sj.cheekOutUp_LFT,
                         cheekOutUpPrefix=cheekOutUpPrefix,
                         cheekOutLowJnt=sj.cheekOutLow_LFT,
                         cheekOutLowPrefix=cheekOutLowPrefix,
                         scale=scale,
                         side=sideLFT,
                         sideLFT=sideLFT,
                         sideRGT=sideRGT,
                         lipDriveCtrl=lip.upLipControllerAll,
                         mouthCtrl=lip.mouthCtrl,
                         mouthCheekInUpAttr=lip.cheekInUpAttr,
                         headLowJnt=sj.head_low,
                         headUpJnt=sj.head_up,
                         jawJnt=sj.jaw,
                         cornerLipCtrl= lip.cornerLipCtrlLFT,
                         cornerLipCtrlAttrCheekLow=lip.cheekLowCtrlAttrLFT,
                         cornerLipCtrlAttrCheekMid=lip.cheekMidCtrlAttrLFT,
                         lowLipDriveCtrl=lip.lowResetMouthOffsetCtrlGrp,
                         nostrilDriveCtrlAttrCheekUp=nose.pullForwardLFT,
                         nostrilDriveCtrlAttrCheekUpTwo=nose.pushUpwardLFT,
                         nostrilDriveCtrl=nose.controllerNose01LFT,
                         cornerLipCtrlAttrCheekOutUp=lip.cheekOutUpCtrlAttrLFT,
                         cornerLipCtrlAttrCheekOutLow=lip.cheekOutLowCtrlAttrLFT,
                         headUpCtrl=head.headUpCtrl,
                         headLowCtrl=head.headLowCtrl,
                         suffixController=suffixController)

    print ('30% | left cheek is done!')

    rightCheek = cm.Cheek(faceAnimCtrlGrp=face_controller_grp,
                          faceUtilsGrp=face_non_transform_grp,
                          cheekLowJnt=sj.cheekLow_RGT,
                          cheekLowPrefix=cheekLowPrefix,
                          cheekMidJnt=sj.cheekMid_RGT,
                          cheekMidPrefix=cheekMidPrefix,
                          cheekUpJnt=sj.cheekUp_RGT,
                          cheekUpPrefix=cheekUpPrefix,
                          cheekInUpJnt=sj.cheekInUp_RGT,
                          cheekInUpPrefix=cheekInUpPrefix,
                          cheekInLowJnt=sj.cheekInLow_RGT,
                          cheekInLowPrefix=cheekInLowPrefix,
                          cheekOutUpJnt=sj.cheekOutUp_RGT,
                          cheekOutUpPrefix=cheekOutUpPrefix,
                          cheekOutLowJnt=sj.cheekOutLow_RGT,
                          cheekOutLowPrefix=cheekOutLowPrefix,
                          scale=scale,
                          side=sideRGT,
                          sideLFT=sideLFT,
                          sideRGT=sideRGT,
                          lipDriveCtrl=lip.upLipControllerAll,
                          mouthCtrl=lip.mouthCtrl,
                          mouthCheekInUpAttr=lip.cheekInUpAttr,
                          headLowJnt=sj.head_low,
                          headUpJnt=sj.head_up,
                          jawJnt=sj.jaw,
                          cornerLipCtrl=lip.cornerLipCtrlRGT,
                          cornerLipCtrlAttrCheekLow=lip.cheekLowCtrlAttrRGT,
                          cornerLipCtrlAttrCheekMid=lip.cheekMidCtrlAttrRGT,
                          lowLipDriveCtrl= lip.lowResetMouthOffsetCtrlGrp,
                          nostrilDriveCtrlAttrCheekUp=nose.pullForwardRGT,
                          nostrilDriveCtrlAttrCheekUpTwo=nose.pushUpwardRGT,
                          nostrilDriveCtrl=nose.controllerNose01RGT,
                          cornerLipCtrlAttrCheekOutUp=lip.cheekOutUpCtrlAttrRGT,
                          cornerLipCtrlAttrCheekOutLow=lip.cheekOutLowCtrlAttrRGT,
                          headUpCtrl=head.headUpCtrl,
                          headLowCtrl=head.headLowCtrl,
                          suffixController=suffixController)

    print ('40% | right cheek is done!')

    # ==================================================================================================================
    #                                                     EARS PARAMETERS
    # ==================================================================================================================
    earLeft = er.Ear(scale=scale,
                     earJnt=sj.ear_LFT,
                     earPrefix=earPrefix,
                     headCtrlGimbal=head.headCtrlGimbal,
                     side=sideLFT,
                     sideLFT=sideLFT,
                     sideRGT=sideRGT,
                     suffixController=suffixController)

    earRight = er.Ear(scale=scale,
                      earJnt=sj.ear_RGT,
                      earPrefix=earPrefix,
                      headCtrlGimbal=head.headCtrlGimbal,
                      side=sideRGT,
                      sideLFT=sideLFT,
                      sideRGT=sideRGT,
                      suffixController=suffixController)
    # ==================================================================================================================
    #                                                     CHIN PARAMETERS
    # ==================================================================================================================
    chin = ch.Chin(mentolabialJnt=sj.mentolabial,
                   mentolabialPrefix=mentolabialPrefix,
                   chinJnt=sj.chin,
                   chinPrefix=chinPrefix,
                   scale=scale,
                   faceAnimCtrlGrp=face_controller_grp,
                   faceUtilsGrp=face_non_transform_grp,
                   lowerLipBindJnt=lip.lowBindJnt,
                   jawJnt= sj.jaw,
                   suffixController=suffixController)

    print ('50% | chin is done!')

    # ==================================================================================================================
    #                                                     EYELID PARAMETERS
    # ==================================================================================================================

    leftEyelid = ld.Lid(
                        faceUtilsGrp=face_non_transform_grp,
                        crvUpLid=crvUpLidLFT,
                        crvLowLid=crvLowLidLFT,
                        offsetLidPos02=offsetLidPos02,
                        offsetLidPos04=offsetLidPos04,
                        eyeballJnt=sj.eyeball_LFT,
                        eyeJnt=sj.eye_LFT,
                        suffixController=suffixController,
                        prefixEye=eyePrefix,
                        prefixEyeAim=eyeAimPrefix,
                        scale=scale,
                        side=sideLFT,
                        sideLFT=sideLFT,
                        sideRGT=sideRGT,
                        directionLid01=directionLid01,
                        directionLid02=directionLid02,
                        directionLid03=directionLid03,
                        directionLid04=directionLid04,
                        directionLid05=directionLid05,
                        positionEyeAimCtrl=positionEyeAimCtrl,
                        eyeAimMainCtrl=head.eyeAimMainCtrl,
                        headUpCtrlGimbal= head.headUpCtrlGimbal,
                        cornerLip=lip.cornerLipCtrlLFT,
                        cornerLipLidAttr=lip.lidAttrLFT,
                        lowLidFolDown=lowLidFolDown,
                        upLidFolDownLowLidFolUp=upLidFolDownLowLidFolUp,
                        upLidLRLowLidLR=upLidLRLowLidLR,
                        upLidFolUp=upLidFolUp,
                        upperHeadGimbalCtrl=head.headUpCtrlGimbal,
                        pupilJnt=sj.pupil_LFT,
                        irisJnt=sj.iris_LFT,
                        pupilPrefix=pupilPrefix,
                        irisPrefix=irisPrefix,
                        eyeCtrlDirection=eyeCtrlDirection
                        )

    print ('60% | left eyelid is done!')

    rightEyelid = ld.Lid(
                         faceUtilsGrp=face_non_transform_grp,
                         crvUpLid=crvUpLidRGT,
                         crvLowLid=crvLowLidRGT,
                         offsetLidPos02=offsetLidPos02,
                         offsetLidPos04=offsetLidPos04,
                         eyeballJnt=sj.eyeball_RGT,
                         eyeJnt=sj.eye_RGT,
                         suffixController=suffixController,
                         prefixEye=eyePrefix,
                         prefixEyeAim=eyeAimPrefix,
                         scale=scale,
                         side=sideRGT,
                         sideLFT=sideLFT,
                         sideRGT=sideRGT,
                         directionLid01=directionLid01,
                         directionLid02=directionLid02,
                         directionLid03=directionLid03,
                         directionLid04=directionLid04,
                         directionLid05=directionLid05,
                         positionEyeAimCtrl=positionEyeAimCtrl,
                         eyeAimMainCtrl=head.eyeAimMainCtrl,
                         headUpCtrlGimbal= head.headUpCtrlGimbal,
                         cornerLip=lip.cornerLipCtrlRGT,
                         cornerLipLidAttr=lip.lidAttrRGT,
                         lowLidFolDown=lowLidFolDown,
                         upLidFolDownLowLidFolUp=upLidFolDownLowLidFolUp,
                         upLidLRLowLidLR=upLidLRLowLidLR,
                         upLidFolUp=upLidFolUp,
                         upperHeadGimbalCtrl=head.headUpCtrlGimbal,
                         pupilJnt=sj.pupil_RGT,
                         irisJnt=sj.iris_RGT,
                         pupilPrefix=pupilPrefix,
                         irisPrefix=irisPrefix,
                         eyeCtrlDirection=eyeCtrlDirection
                         )

    print ('70% | right eyelid is done!')

    # ==================================================================================================================
    #                                                     EYELID OUT PARAMETERS
    # ==================================================================================================================

    leftLidOut = lo.LidOut(faceUtilsGrp=face_non_transform_grp,
                           crvUp=crvUpLidOutLFT,
                           crvLow=crvLowLidOutLFT,
                           offsetJnt02BindPos=offsetJnt02BindLipPosLidOut,
                           offsetJnt04BindPos=offsetJnt04BindLipPosLidOut,
                           directionCtrl01=directionCtrlLidOut01,
                           directionCtrl02=directionCtrlLidOut02,
                           directionCtrl03=directionCtrlLidOut03,
                           directionCtrl04=directionCtrlLidOut04,
                           directionCtrl05=directionCtrlLidOut05,
                           ctrlColor='blue',
                           shape=ct.JOINT,
                           scale=scale,
                           sideRGT=sideRGT,
                           sideLFT=sideLFT,
                           side=sideLFT,
                           eyeballJnt=sj.eyeball_LFT,
                           headUpJnt=sj.head_up,
                           eyeCtrl=leftEyelid.eyeballController,
                           cornerLip=lip.cornerLipCtrlLFT,
                           cornerLipAttr=lip.lidOutAttrLFT,
                           ctrlBindUp01=leftEyelid.upLidControllerBind01,
                           ctrlBindUp02=leftEyelid.upLidControllerBind02,
                           ctrlBindUp03=leftEyelid.upLidControllerBind03,
                           ctrlBindUp04=leftEyelid.upLidControllerBind04,
                           ctrlBindUp05=leftEyelid.upLidControllerBind05,
                           ctrlBindLow01=leftEyelid.lowLidControllerBind01,
                           ctrlBindLow02=leftEyelid.lowLidControllerBind02,
                           ctrlBindLow03=leftEyelid.lowLidControllerBind03,
                           ctrlBindLow04=leftEyelid.lowLidControllerBind04,
                           ctrlBindLow05=leftEyelid.lowLidControllerBind05,
                           lidOutFollow=leftEyelid.lidOutUp03FollowAttr,
                           closeLidAttr=leftEyelid.upLidCloseLid,
                           lidCornerInCtrl=leftEyelid.lidCornerInCtrl,
                           lidCornerOutCtrl=leftEyelid.lidCornerOutCtrl,
                           wireUp01BindOffsetGrp=leftEyelid.upLidBind01GrpOffset,
                           wireLow01BindOffsetGrp=leftEyelid.lowLidBind01GrpOffset,
                           wireUp05BindOffsetGrp=leftEyelid.upLidBind05GrpOffset,
                           wireLow05BindOffsetGrp=leftEyelid.lowLidBind05GrpOffset,
                           lidOutOnOffFollowTransMdn=leftEyelid.LidOutEyeCtrlTrans,
                           lidOutOnOffFollowRotMdn=leftEyelid.LidOutEyeCtrlRot,
                           eyeCtrlDirection=eyeCtrlDirection,
                           suffixController=suffixController)

    print ('80% | left lid out is done!')

    rightLidOut = lo.LidOut(faceUtilsGrp=face_non_transform_grp,
                            crvUp=crvUpLidOutRGT,
                            crvLow=crvLowLidOutRGT,
                            offsetJnt02BindPos=offsetJnt02BindLipPosLidOut,
                            offsetJnt04BindPos=offsetJnt04BindLipPosLidOut,
                            directionCtrl01=directionCtrlLidOut01,
                            directionCtrl02=directionCtrlLidOut02,
                            directionCtrl03=directionCtrlLidOut03,
                            directionCtrl04=directionCtrlLidOut04,
                            directionCtrl05=directionCtrlLidOut05,
                            ctrlColor='blue',
                            shape=ct.JOINT,
                            scale=scale,
                            sideRGT=sideRGT,
                            sideLFT=sideLFT,
                            side=sideRGT,
                            eyeballJnt=sj.eyeball_RGT,
                            headUpJnt=sj.head_up,
                            eyeCtrl=rightEyelid.eyeballController,
                            cornerLip=lip.cornerLipCtrlRGT,
                            cornerLipAttr=lip.lidOutAttrRGT,
                            ctrlBindUp01=rightEyelid.upLidControllerBind01,
                            ctrlBindUp02=rightEyelid.upLidControllerBind02,
                            ctrlBindUp03=rightEyelid.upLidControllerBind03,
                            ctrlBindUp04=rightEyelid.upLidControllerBind04,
                            ctrlBindUp05=rightEyelid.upLidControllerBind05,
                            ctrlBindLow01=rightEyelid.lowLidControllerBind01,
                            ctrlBindLow02=rightEyelid.lowLidControllerBind02,
                            ctrlBindLow03=rightEyelid.lowLidControllerBind03,
                            ctrlBindLow04=rightEyelid.lowLidControllerBind04,
                            ctrlBindLow05=rightEyelid.lowLidControllerBind05,
                            lidOutFollow=rightEyelid.lidOutUp03FollowAttr,
                            closeLidAttr=rightEyelid.upLidCloseLid,
                            lidCornerInCtrl=rightEyelid.lidCornerInCtrl,
                            lidCornerOutCtrl=rightEyelid.lidCornerOutCtrl,
                            wireUp01BindOffsetGrp=rightEyelid.upLidBind01GrpOffset,
                            wireLow01BindOffsetGrp=rightEyelid.lowLidBind01GrpOffset,
                            wireUp05BindOffsetGrp=rightEyelid.upLidBind05GrpOffset,
                            wireLow05BindOffsetGrp=rightEyelid.lowLidBind05GrpOffset,
                            lidOutOnOffFollowTransMdn=rightEyelid.LidOutEyeCtrlTrans,
                            lidOutOnOffFollowRotMdn=rightEyelid.LidOutEyeCtrlRot,
                            eyeCtrlDirection=eyeCtrlDirection,
                            suffixController=suffixController)
    print ('90% | right lid out is done!')

    # ==================================================================================================================
    #                                                     BROWS PARAMETERS
    # ==================================================================================================================

    brows =  bm.Brows(browTwJntLFT=sj.browTw_LFT,
                      browInJntLFT=sj.browIn_LFT,
                      browMidJntLFT=sj.browMid_LFT,
                      browOutJntLFT=sj.browOut_LFT,
                      browTipJntLFT=sj.browTip_LFT,
                      browTwJntRGT=sj.browTw_RGT,
                      browInJntRGT=sj.browIn_RGT,
                      browMidJntRGT=sj.browMid_RGT,
                      browOutJntRGT=sj.browOut_RGT,
                      browTipJntRGT=sj.browTip_RGT,
                      browCenterJnt=sj.brow_center,
                      browTwPrefix=browTwPrefix,
                      browInPrefix=browInPrefix,
                      browMidPrefix=browMidPrefix,
                      browOutPrefix=browOutPrefix,
                      browsPrefix=browsPrefix,
                      browTipPrefix=browTipPrefix,
                      browCenterPrefix=browCenterPrefix,
                      scale=scale,
                      sideRGT=sideRGT,
                      sideLFT=sideLFT,
                      browInGrpRotOffset=browInGrpRotOffset,
                      browMidGrpRotOffset= browMidGrpRotOffset,
                      browOutGrpRotOffset=browOutGrpRotOffset,
                      browTipGrpRotOffset= browTipGrpRotOffset,
                      headUpCtrlGimbal=head.headUpCtrlGimbal,
                      suffixController=suffixController)
    # ==================================================================================================================
    #                                                     BULGE PARAMETERS
    # ==================================================================================================================
    bulge = bl.Bulge(faceUtilsGrp=face_non_transform_grp,
                     faceAnimCtrlGrp=face_controller_grp,
                     cheekBulgeLFTJnt=sj.cheekBulge_LFT,
                     cheekBulgePrefix=cheekMidPrefix,
                     cheekBulgeRGTJnt=sj.cheekBulge_RGT,
                     browInBulgePrefix=browInPrefix,
                     browOutBulgePrefix=browOutPrefix,
                     cornerMouthBulgePrefix='cornerMouth',
                     noseBulgePrefix='nose',
                     chinBulgePrefix=chinPrefix,
                     browInBulgeLFTJnt=sj.browIn_LFT,
                     browInBulgeRGTJnt=sj.browIn_RGT,
                     browOutBulgeLFTJnt=sj.browOut_LFT,
                     browOutBulgeRGTJnt=sj.browOut_RGT,
                     cornerMouthBulgeLFTJnt=lip.cornerLipCtrlLFT,
                     cornerMouthBulgeRGTJnt=lip.cornerLipCtrlRGT,
                     noseBulgeJnt=nose.controllerNose03,
                     chinBulgeJnt=sj.chin,
                     bulgeMesh=bulgeMesh,
                     sideLFT=sideLFT,
                     sideRGT=sideRGT,
                     headUpCtrlGimbal=head.headUpCtrlGimbal,
                     headLowCtrlGimbal=head.headLowCtrlGimbal,
                     noseDrv03ctrl=nose.controllerNose03,
                     chinCtrl=chin.chinCtrl,
                     cornerMouthLFTCtrl=lip.cornerLipCtrlLFT,
                     cornerMouthRGTCtrl=lip.cornerLipCtrlRGT,
                     scale=scale,
                     addSet=addSetBulge)

    print ('100% | brows is done!')

    # ==================================================================================================================
    #                                         SETUP VISIBILITY CONTROLLER
    # ==================================================================================================================
    setupCtrl = ct.Control(prefix='setup', match_obj_first_position=sj.head,
                           shape=ct.SETUP, groups_ctrl=[''], ctrl_size=scale * 0.12,
                           ctrl_color='blue', lock_channels=['v', 't', 's', 'r']
                           )
    # # HAIR VIS
    # hairVis = au.connect_part_object(obj_base_connection='hairVis', target_connection='visibility', obj_name=setupCtrl.control,
    #                                  target_name=['hair_geo', 'hairMainGeoCtrl_grp'], channel_box=True, select_obj=False)

    # MAIN CHEEK VIS
    mainCheekCtrlVis = au.connect_part_object(obj_base_connection='mainCheekCtrlVis', target_connection='visibility', obj_name=setupCtrl.control,
                                              target_name=[leftCheek.cheekLowZroCtrlGrp,
                                                           leftCheek.cheekMidZroCtrlGrp,
                                                           leftCheek.cheekOutUpZroCtrlGrp,
                                                           leftCheek.cheekOutLowZroCtrlGrp,
                                                           rightCheek.cheekLowZroCtrlGrp,
                                                           rightCheek.cheekMidZroCtrlGrp,
                                                           rightCheek.cheekOutUpZroCtrlGrp,
                                                           rightCheek.cheekOutLowZroCtrlGrp],
                                              channel_box=True, select_obj=False)

    # SECONDARY CHEEK VIS
    secondaryCheekCtrlVis = au.connect_part_object(obj_base_connection='secondaryCheekCtrlVis', target_connection='visibility', obj_name=setupCtrl.control,
                                                   target_name=[leftCheek.cheekUpZroCtrlGrp,
                                                                leftCheek.cheekInUpZroCtrlGrp,
                                                                leftCheek.cheekInLowZroCtrlGrp,
                                                                rightCheek.cheekUpZroCtrlGrp,
                                                                rightCheek.cheekInUpZroCtrlGrp,
                                                                rightCheek.cheekInLowZroCtrlGrp],
                                                   channel_box=True, select_obj=False)

    # CHIN VIS
    chinCtrlVis = au.connect_part_object(obj_base_connection='chinCtrlVis', target_connection='visibility', obj_name=setupCtrl.control,
                                         target_name=[chin.chinCtrlGrp,
                                                      chin.mentolabialCtrlGrp],
                                         channel_box=True, select_obj=False)

    # LIP VIS
    mouthCtrlVis = au.connect_part_object(obj_base_connection='mouthCtrlVis', target_connection='visibility', obj_name=setupCtrl.control,
                                          target_name=[lip.controllerGrp], channel_box=True, select_obj=False)

    # NOSE VIS
    noseCtrlVis = au.connect_part_object(obj_base_connection='noseCtrlVis', target_connection='visibility', obj_name=setupCtrl.control,
                                         target_name=[nose.noseControllerGrp, nose.noseCtrlParentZro,
                                                      nose.noseUpControllerGrp], channel_box=True, select_obj=False)

    # EYE VIS
    eyeCtrlVis = au.connect_part_object(obj_base_connection='eyeCtrlVis', target_connection='visibility', obj_name=setupCtrl.control,
                                        target_name=[leftEyelid.eyeballCtrl.parent_control[0],
                                                     leftEyelid.upLid.grp0204Ctrl,
                                                     leftEyelid.lowLid.grp0204Ctrl,
                                                     rightEyelid.eyeballCtrl.parent_control[0],
                                                     rightEyelid.upLid.grp0204Ctrl,
                                                     rightEyelid.lowLid.grp0204Ctrl], channel_box=True, select_obj=False)
    # BROW VIS
    browCtrlVis = au.connect_part_object(obj_base_connection='browCtrlVis', target_connection='visibility', obj_name=setupCtrl.control,
                                         target_name=[brows.browAllCtrl], channel_box=True, select_obj=False)

    # BULGE VIS
    bulgeCtrlVis = au.connect_part_object(obj_base_connection='bulgeCtrlVis', target_connection='visibility', obj_name=setupCtrl.control,
                                          target_name=[bulge.cheekBulgeLFTCtrlGrp,
                                                       bulge.cheekBulgeRGTCtrlGrp,
                                                       bulge.browInBulgeLFTCtrlGrp,
                                                       bulge.browInBulgeRGTCtrlGrp,
                                                       bulge.browOutBulgeLFTCtrlGrp,
                                                       bulge.browOutBulgeRGTCtrlGrp,
                                                       bulge.cornerMouthBulgeLFTCtrlGrp,
                                                       bulge.cornerMouthBulgeRGTCtrlGrp,
                                                       bulge.noseBulgeCtrlGrp,
                                                       bulge.chinBulgeCtrlGrp], channel_box=True, select_obj=False)

    mc.setAttr(mainCheekCtrlVis, 0)
    mc.setAttr(secondaryCheekCtrlVis, 0)
    mc.setAttr(chinCtrlVis, 0)
    mc.setAttr(bulgeCtrlVis, 0)

    # ==================================================================================================================
    #                                               CLEAN UP SET
    # ==================================================================================================================

    # PARENT TO GRP GENERAL MODULE
    if mc.objExists('animGmbl_ctrl'):
        mc.parent(faceCurvesGrp, 'faceNonTransform_grp')
        mc.parent(head.neckCtrlGrp, setupCtrl.parent_control[0], 'faceAnim_grp')
        mc.parent(head.worldUpGrp, 'faceUtils_grp')

    # SETS LN JOINT
    setsLN = mc.sets(sj.neck, n='FACESKINJNT_LN')
    mc.setAttr(sj.neck + '.visibility', 1)

    for i in (sj.head, sj.head_up, sj.head_low, sj.jaw, sj.mentolabial, sj.chin, sj.brow_center,
              sj.cheekInUp_LFT, sj.cheekInLow_LFT, sj.cheekUp_LFT, sj.cheekMid_LFT, sj.cheekLow_LFT, sj.cheekOutUp_LFT,
              sj.cheekOutLow_LFT, sj.cheekInUp_RGT, sj.cheekInLow_RGT, sj.cheekUp_RGT, sj.cheekMid_RGT, sj.cheekLow_RGT,
              sj.cheekOutUp_RGT, sj.cheekOutLow_RGT, sj.browIn_LFT, sj.browMid_LFT, sj.browOut_LFT, sj.browTip_LFT,
              sj.browIn_RGT, sj.browMid_RGT, sj.browOut_RGT, sj.browTip_RGT, sj.nose_up, sj.columella, sj.eye_LFT, sj.eye_RGT,
              sj.ear_LFT, sj.ear_RGT, sj.neckIn_Btw):
        mc.sets(i, add=setsLN)
        mc.setAttr(i + '.visibility', 1)

    for i in list(set(nose.allJoint+ lip.allUpLipJoint + lip.allLowLipJoint+ leftLidOut.lidOutUpJnt+
                      leftLidOut.lidOutLowJnt+ rightLidOut.lidOutUpJnt+ rightLidOut.lidOutLowJnt)):
        mc.sets(i, add=setsLN)
        mc.setAttr(i + '.visibility', 1)


    # SETS DQ JOINT
    setsDQ = mc.sets(jntDQBase, n='FACESKINJNT_DQ')
    mc.setAttr(jntDQBase + '.visibility', 1)

    for i in list(set(leftEyelid.upLidAllJnt+ leftEyelid.lowLidAllJnt+
                   rightEyelid.upLidAllJnt+ rightEyelid.lowLidAllJnt)):
        mc.sets(i, add=setsDQ)
        mc.setAttr(i + '.visibility', 1)

    return {'neckJntGrp' :head.neckJntGrp,
            'neckCtrlZroGrp' : head.neckCtrlGrp,
            'sj': sj}
