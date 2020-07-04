import re
from __builtin__ import reload

import maya.cmds as mc

from rigging.library.base.face import lip as lp, lip_corner as lc
from rigging.library.utils import controller as ct
from rigging.library.utils import transform as tf
from rigging.tools import AD_utils as au

reload (ct)
reload (tf)
reload (au)
reload (lp)
reload (lc)

class Lip:
    def __init__(self,
                 faceAnimCtrlGrp,
                 faceUtilsGrp,
                 crvUpLip,
                 crvLowLip,
                 crvUpLipRoll,
                 crvLowLipRoll,
                 offsetJnt02BindPos,
                 scale,
                 directionLip01Cheek,
                 directionLip02Cheek,
                 sideLFT,
                 sideRGT,
                 jawJnt,
                 headLowJnt,
                 mouthJnt,
                 positionMouthCtrl,
                 suffixController,
                 jaw_ctrl,
                 prefix_upLip_follow,
                 headLow_normal_rotationGrp
                 ):

        self.crvUpLip= crvUpLip
        self.crvLowLip = crvLowLip

    # ==============================================================================================================
    #                                          LIP UP AND LOW CONTROLLER
    # ==============================================================================================================

        # UP LIP
        upLip = lp.Build(crvLip=crvUpLip,
                         crvLipRoll=crvUpLipRoll,
                         offsetJnt02BindPos=offsetJnt02BindPos,
                         scale=scale,
                         directionLip01Cheek=directionLip01Cheek,
                         directionLip02Cheek=directionLip02Cheek,
                         sideLFT = sideLFT,
                         sideRGT = sideRGT,
                         mouthJnt=mouthJnt,
                         ctrlColor='yellow',
                         controllerLowLip=False,
                         suffixController=suffixController)

        # UP LIP FOLLOW JAW
        # CONTROLLER
        self.upLip_follow_jaw(jaw_ctrl=jaw_ctrl, prefix_upLip_follow=prefix_upLip_follow, name='Ctrl', jaw_jnt=jawJnt,
                              headLow_normal_rotationGrp=headLow_normal_rotationGrp,
                              crv_up_lip=crvUpLip, mouth_lip_grp=upLip.mouthCtrlGrp, mouth_offset_lip_grp=upLip.mouthOffsetCtrlGrp)
        # SETUP
        self.upLip_follow_jaw(jaw_ctrl=jaw_ctrl, prefix_upLip_follow=prefix_upLip_follow, name='Setup', jaw_jnt=jawJnt,
                              headLow_normal_rotationGrp=headLow_normal_rotationGrp,
                              crv_up_lip=crvUpLip, mouth_lip_grp=upLip.resetAllMouthCtrlGrp, mouth_offset_lip_grp=upLip.resetAllMouthOffsetCtrlGrp)


        # LOW LIP
        lowLip = lp.Build(crvLip=crvLowLip,
                          crvLipRoll=crvLowLipRoll,
                          offsetJnt02BindPos=offsetJnt02BindPos,
                          scale=scale,
                          directionLip01Cheek=directionLip01Cheek,
                          directionLip02Cheek=directionLip02Cheek,
                          sideLFT=sideLFT,
                          sideRGT=sideRGT,
                          mouthJnt=mouthJnt,
                          ctrlColor='red',
                          controllerLowLip=True,
                          suffixController=suffixController)

        self.lowBindJnt = lowLip.jntMid
        self.allUpLipJoint = upLip.allJoint
        self.allLowLipJoint = lowLip.allJoint

    # =================================================================================================================
    #                                             CORNER LIP CONTROLLER
    # =================================================================================================================

        # CONTROLLER RGT CORNER
        cornerLipCtrlRGT = lc.Build(
                 matchPosOne=lowLip.jnt01RGT,
                 matchPosTwo=upLip.jnt01RGT,
                 prefix='cornerLipDrv',
                 scale=scale,
                 sticky=True,
                 side=sideRGT,
                 suffixController=suffixController)

        self.cornerLipCtrlRGT = cornerLipCtrlRGT.control
        self.cheekMidCtrlAttrRGT = cornerLipCtrlRGT.cheekMidCtrl
        self.cheekLowCtrlAttrRGT = cornerLipCtrlRGT.cheekLowCtrl
        self.cheekOutUpCtrlAttrRGT = cornerLipCtrlRGT.cheekOutUpCtrl
        self.cheekOutLowCtrlAttrRGT = cornerLipCtrlRGT.cheekOutLowCtrl
        self.nostrilCtrlAttrRGT = cornerLipCtrlRGT.nostrilCtrl
        self.lidOutAttrRGT = cornerLipCtrlRGT.lidOutCtrl
        self.lidAttrRGT = cornerLipCtrlRGT.lidCtrl

        # CONTROLLER LFT CORNER
        cornerLipCtrlLFT = lc.Build(
                 matchPosOne=lowLip.jnt01LFT,
                 matchPosTwo=upLip.jnt01LFT,
                 prefix='cornerLipDrv',
                 scale=scale,
                 sticky=True,
                 side=sideLFT,
                 suffixController=suffixController)

        self.cornerLipCtrlLFT = cornerLipCtrlLFT.control
        self.cheekMidCtrlAttrLFT = cornerLipCtrlLFT.cheekMidCtrl
        self.cheekLowCtrlAttrLFT = cornerLipCtrlLFT.cheekLowCtrl
        self.cheekOutUpCtrlAttrLFT = cornerLipCtrlLFT.cheekOutUpCtrl
        self.cheekOutLowCtrlAttrLFT = cornerLipCtrlLFT.cheekOutLowCtrl
        self.nostrilCtrlAttrLFT = cornerLipCtrlLFT.nostrilCtrl
        self.lidOutAttrLFT = cornerLipCtrlLFT.lidOutCtrl
        self.lidAttrLFT = cornerLipCtrlLFT.lidCtrl

        # CREATE LOCATOR SET CORNER
        self.cornerLipLocSet01RGT = mc.spaceLocator(n='cornerLipDrv01' + sideRGT + '_set')[0]
        self.cornerLipLocSet01LFT = mc.spaceLocator(n='cornerLipDrv01' + sideLFT + '_set')[0]

        # PARENT LOCATOR SET TO GROUP
        cornerSetGrp = mc.createNode('transform', n='cornerLipDrvSet_grp')
        mc.parent(self.cornerLipLocSet01RGT, self.cornerLipLocSet01LFT, cornerSetGrp)

        # MATCH POSITION
        # PARENT CONSTRAINT CORNER LOCATOR SET
        mc.parentConstraint(lowLip.locatorSet01RGT, upLip.locatorSet01RGT, self.cornerLipLocSet01RGT)
        mc.parentConstraint(lowLip.locatorSet01LFT, upLip.locatorSet01LFT, self.cornerLipLocSet01LFT)

        # CONNECT CORNER LOCATOR TO CONTROLLER CORNER PARENT ZRO
        au.connectAttrTransRot(self.cornerLipLocSet01RGT, cornerLipCtrlRGT.parentControlZro)
        au.connectAttrTransRot(self.cornerLipLocSet01LFT, cornerLipCtrlLFT.parentControlZro)

        # CONNECT ALL MOUTH CTRL GRP (CENTER) TO CONTROLLER CORNER PARENT OFFSET
        au.connect_attr_scale(upLip.mouthCtrlGrp, cornerLipCtrlRGT.parentControlOffset)
        au.connect_attr_scale(upLip.mouthCtrlGrp, cornerLipCtrlLFT.parentControlOffset)

        # ==============================================================================================================
        #                                       LIP ALL CONTROLLER (CENTER)
        # ==============================================================================================================
        # ASSIGN ALL CONTROLLER LIP
        self.upLipControllerAll = upLip.controllerAll
        self.lowLipControllerAll = lowLip.controllerAll
        self.lowResetMouthOffsetCtrlGrp = lowLip.resetMouthOffsetCtrlGrp
        self.upLipControllerAllZroGrp= upLip.controllerAllZroGrp
        self.upLipMouthCtrlGrp =upLip.mouthCtrlGrp

        # LOW LIP
        self.upAndLowLipSetup(cornerLipCtrlRGT=cornerLipCtrlRGT, cornerLipCtrlLFT=cornerLipCtrlLFT, sideLFT=sideLFT,
                              sideRGT=sideRGT, prefixBind='LowBind', prefixCtrl='LowCtrl', lip=lowLip,
                              conditionLowLip=True)

        # UP LIP
        self.upAndLowLipSetup(cornerLipCtrlRGT=cornerLipCtrlRGT, cornerLipCtrlLFT=cornerLipCtrlLFT, sideLFT=sideLFT,
                              sideRGT=sideRGT, prefixBind='upBind', prefixCtrl='upCtrl', lip=upLip,
                              conditionLowLip=False)

        # PARENT CONSTRAINT SET LOCATOR
        self.parentConstraintSetLocator(lip=upLip, upLip=upLip, lowLip=lowLip, conditionLowLip=False,
                                        jawJnt=jawJnt, headLowJnt=headLowJnt)

        self.parentConstraintSetLocator(lip=lowLip, upLip=upLip, lowLip=lowLip, conditionLowLip=True,
                                        jawJnt=jawJnt, headLowJnt=headLowJnt)

        # CONNECT ALL CONTROLLER TO ALL RESET GRP
        trans = self.reverseLowLid(control=lowLip.controllerAll, input2X=1, input2Y=-1, input2Z=1,
                                   jointBindTarget=lowLip.resetMouthOffsetCtrlGrp,
                                   name='Trans', connect='translate')

        rot = self.reverseLowLid(control=lowLip.controllerAll, input2X=-1, input2Y=1, input2Z=-1,
                                   jointBindTarget=lowLip.resetMouthOffsetCtrlGrp,
                                   name='Rot', connect='rotate')

        # au.connectAttrRot(lowLip.controllerAll, lowLip.resetMouthOffsetCtrlGrp)
        au.connectAttrTransRot(upLip.controllerAll, upLip.resetMouthOffsetCtrlGrp)

        # CREATE JAW FOLLOW LOW LIP
        cornerAdjustLFT, jawFollowingLFT = self.multiplyLipAndJaw(side=sideLFT, cornerAdjustCtrl='%s.%s' % (cornerLipCtrlLFT.control, cornerLipCtrlLFT.jawUDCtrl),
                                                                  jawFollowingCtrl='%s.%s' % (cornerLipCtrlLFT.control, cornerLipCtrlLFT.jawFollowCtrl))

        cornerAdjustRGT, jawFollowingRGT = self.multiplyLipAndJaw(side=sideRGT, cornerAdjustCtrl='%s.%s' % (cornerLipCtrlRGT.control, cornerLipCtrlRGT.jawUDCtrl),
                                                                  jawFollowingCtrl='%s.%s' % (cornerLipCtrlRGT.control, cornerLipCtrlRGT.jawFollowCtrl))

        # UP LIP
        self.upLipJaw(side=sideLFT, multCornerAdjust=cornerAdjustLFT, multJawFollowing=jawFollowingLFT,
                      locatorSet01=upLip.locatorSet01LFT, resetMouthOffsetCtrlGrp=upLip.resetMouthOffsetCtrlGrp, nameW='W0', W0=True)

        self.upLipJaw(side=sideLFT, multCornerAdjust=cornerAdjustLFT, multJawFollowing=jawFollowingLFT,
                      locatorSet01=upLip.locatorSet01LFT, resetMouthOffsetCtrlGrp=lowLip.resetMouthOffsetCtrlGrp, nameW='W1', W0=False)

        self.upLipJaw(side=sideRGT, multCornerAdjust=cornerAdjustRGT, multJawFollowing=jawFollowingRGT,
                      locatorSet01=upLip.locatorSet01RGT, resetMouthOffsetCtrlGrp=upLip.resetMouthOffsetCtrlGrp, nameW='W0',W0=True)

        self.upLipJaw(side=sideRGT, multCornerAdjust=cornerAdjustRGT, multJawFollowing=jawFollowingRGT,
                      locatorSet01=upLip.locatorSet01RGT, resetMouthOffsetCtrlGrp=lowLip.resetMouthOffsetCtrlGrp, nameW='W1',W0=False)

        # LOW LIP
        self.lowLipJaw(side=sideLFT, multCornerAdjust=cornerAdjustLFT, multJawFollowing=jawFollowingLFT,
                       locatorSet01=lowLip.locatorSet01LFT, resetMouthOffsetCtrlGrp=upLip.resetMouthOffsetCtrlGrp, nameW='W0',W0=True)

        self.lowLipJaw(side=sideLFT, multCornerAdjust=cornerAdjustLFT, multJawFollowing=jawFollowingLFT,
                       locatorSet01=lowLip.locatorSet01LFT, resetMouthOffsetCtrlGrp=lowLip.resetMouthOffsetCtrlGrp,nameW='W1', W0=False)

        self.lowLipJaw(side=sideRGT, multCornerAdjust=cornerAdjustRGT, multJawFollowing=jawFollowingRGT,
                       locatorSet01=lowLip.locatorSet01RGT, resetMouthOffsetCtrlGrp=upLip.resetMouthOffsetCtrlGrp, nameW='W0',W0=True)

        self.lowLipJaw(side=sideRGT, multCornerAdjust=cornerAdjustRGT, multJawFollowing=jawFollowingRGT,
                       locatorSet01=lowLip.locatorSet01RGT, resetMouthOffsetCtrlGrp=lowLip.resetMouthOffsetCtrlGrp,nameW='W1', W0=False)

    # ==================================================================================================================
    #                                                   STICKY LIP
    # ==================================================================================================================

        xformCornerLipRight = mc.xform(self.cornerLipLocSet01RGT, ws=1, q=1, t=1)
        xformCornerLipLeft = mc.xform(self.cornerLipLocSet01LFT, ws=1, q=1, t=1)

        stickyLipBindCrv = mc.curve(ep=[(xformCornerLipRight), (xformCornerLipLeft)],
                                    degree=3, n='lipBindSticky_crv')
        mc.rebuildCurve(stickyLipBindCrv, ch=0, rpo=1, rt=0, end=1, kr=0, kcp=0,
                        kep=1, kt=0, s=2, d=3, tol=0.01)

        # STICKY BLENDSHAPE BIND UP AND LOW LIP
        mc.blendShape(upLip.deformCrv, lowLip.deformCrv, stickyLipBindCrv, n=('lipSticky' + '_bsn'),
                      weight=[(0, 0.5), (1, 0.5)])

        # STICKY BLENDSHAPE STICKY TO LOW BIND MID
        mc.blendShape(stickyLipBindCrv, lowLip.bindStickyMidCrv, n=au.prefix_name(crvLowLip) + 'BindStickyMid' + '_bsn',
                      weight=[(0, 1)])

        # STICKY BLENDSHAPE STICKY TO UP BIND MID
        mc.blendShape(stickyLipBindCrv, upLip.bindStickyMidCrv, n=au.prefix_name(crvUpLip) + 'BindStickyMid' + '_bsn',
                      weight=[(0, 1)])

        # SET KEYFRAME FOR CONSTRAINT
        # LOW LIP SET
        self.setValueSticky(constraint=lowLip.clsConstraint, offsetValue=0.65,
                            attributeRGT=cornerLipCtrlRGT.stickyCtrl, attributeLFT=cornerLipCtrlLFT.stickyCtrl,
                            controllerRGT=cornerLipCtrlRGT.control, controllerLFT=cornerLipCtrlLFT.control,
                            lipStickyOriginLocName='%sStickyOrigin' % au.prefix_name(crvLowLip),
                            lipStickyMidLocName='%sStickyMid' % au.prefix_name(crvLowLip))
        # UP LIP SET
        self.setValueSticky(constraint=upLip.clsConstraint, offsetValue=0.65,
                            attributeRGT=cornerLipCtrlRGT.stickyCtrl, attributeLFT=cornerLipCtrlLFT.stickyCtrl,
                            controllerRGT=cornerLipCtrlRGT.control, controllerLFT=cornerLipCtrlLFT.control,
                            lipStickyOriginLocName='%sStickyOrigin' % au.prefix_name(crvUpLip),
                            lipStickyMidLocName='%sStickyMid' % au.prefix_name(crvUpLip))

    # ==================================================================================================================
    #                                                   MOUTH AIM
    # ==================================================================================================================

        self.mouthController = ct.Control(match_obj_first_position=None,
                                          prefix='mouth',
                                          shape=ct.LOCATOR, groups_ctrl=['Zro', 'Offset'],
                                          ctrl_size=scale * 0.25,
                                          ctrl_color='lightPink', lock_channels=['v', 's', 'r'])
        self.mouthCtrl = self.mouthController.control
        self.mouthCtrlParentOffset = self.mouthController.parent_control[1]
        self.mouthCtrlParentZro = self.mouthController.parent_control[0]

        # ADD ATTRIBUTE CONTROLLER ROLL
        au.add_attribute(objects=[self.mouthController.control], long_name=['rollSetup'], nice_name=[' '], at="enum",
                         en='Add Setup', channel_box=True)

        self.controllerUpRoll = au.add_attribute(objects=[self.mouthController.control], long_name=['rollLipUpSkin'],
                                                 attributeType="float", dv=0, keyable=True)

        self.controllerLowRoll = au.add_attribute(objects=[self.mouthController.control], long_name=['rollLipLowSkin'],
                                                  attributeType="float", dv=0, keyable=True)

        self.cheekInUpAttr = au.add_attribute(objects=[self.mouthController.control], long_name=['cheekInUp'],
                                              attributeType="float", dv=1, min=0.001, keyable=True)

        # CONNECT ROLL ATTRIBUTE CONTROLLER MID TO MDL LIP ROLL
        mc.connectAttr(self.mouthController.control + '.%s' % self.controllerLowRoll, lowLip.mdlLipRoll + '.input1')
        mc.setAttr(lowLip.mdlLipRoll + '.input2', 10)

        mc.connectAttr(self.mouthController.control + '.%s' % self.controllerUpRoll, upLip.mdlLipRoll + '.input1')
        mc.setAttr(upLip.mdlLipRoll + '.input2', -10)

        # CONNECT ROLL ATTRIBUTE CONTROLLER MID TO CONDITION ROLL ROLL
        for low, up, in zip (lowLip.condition, upLip.condition):
            mc.connectAttr(self.mouthController.control + '.%s' % self.controllerLowRoll, low + '.firstTerm')
            mc.connectAttr(self.mouthController.control + '.%s' % self.controllerUpRoll, up + '.firstTerm')

        # SET THE POSITION CONTROLLER
        mc.delete(mc.pointConstraint(upLip.controllerBindMid.control, lowLip.controllerBindMid.control,
                                     self.mouthController.parent_control[0]))
        tZValue = mc.getAttr(self.mouthController.parent_control[0] + '.translateZ')
        mc.setAttr(self.mouthController.parent_control[0] + '.translateZ', tZValue + (positionMouthCtrl * scale))

        # AIM LOC OBJECT LOOK UP
        locatorAim =  mc.spaceLocator(n='mouthAim_loc')[0]
        grpLocatorAim = tf.create_parent_transform(parent_list=[''], object=locatorAim,
                                                   match_position=locatorAim, prefix=au.prefix_name(locatorAim),
                                                   suffix='_loc')

        mc.delete(mc.parentConstraint(self.mouthController.control, grpLocatorAim[0]))
        tYLocValue = mc.getAttr(grpLocatorAim[0] + '.translateY')
        mc.setAttr(grpLocatorAim[0]+'.translateY', tYLocValue+(10*scale))
        mc.hide(grpLocatorAim[0])

        # AIM CONSTRAINT TO THE MOUTH JOINT
        mc.aimConstraint(self.mouthController.control, mouthJnt, mo=1, aimVector=(0, 0, 1), upVector=(0, 1, 0),
                         worldUpType='object', worldUpObject=locatorAim)

        # CONNECT ATTRIBUTE THE MOUTH AIM JOINT
        au.connect_attr_translate(self.mouthController.control, locatorAim)

        # PARENT CONSTRAINT HEAD LOW TO LOCATOR AIM GRP
        mc.parentConstraint(headLowJnt, grpLocatorAim[0], mo=1)
        mc.scaleConstraint(headLowJnt, grpLocatorAim[0], mo=1)

        # PARENT CONSTRAINT HEAD LOW TO PARENT MOUTH CONTROLLER
        mc.parentConstraint(headLowJnt, self.mouthController.parent_control[0], mo=1)
        mc.scaleConstraint(headLowJnt, self.mouthController.parent_control[0], mo=1)

    # ==================================================================================================================
    #                                                   PARENT GROUP
    # ==================================================================================================================
        self.lip = mc.createNode('transform', n='lip_grp')
        self.controllerGrp = mc.createNode('transform', n='lipCtrlAll_grp')
        self.setupGrp = mc.createNode('transform', n='lipSetup_grp')
        mc.hide(self.setupGrp)

        mc.parent(self.setupGrp, self.lip)
        mc.parent(upLip.stickyGrp, lowLip.stickyGrp, upLip.utilsGrp, lowLip.utilsGrp, stickyLipBindCrv, cornerSetGrp,
                  grpLocatorAim[0], self.setupGrp)
        mc.parent(self.mouthController.parent_control[0], cornerLipCtrlLFT.parentControlZro,
                  cornerLipCtrlRGT.parentControlZro, upLip.ctrlGrp, lowLip.ctrlGrp, self.controllerGrp)

        mc.parent(self.controllerGrp, faceAnimCtrlGrp)
        mc.parent(self.lip, faceUtilsGrp)


    # ==================================================================================================================
    #                                                   FUNCTIONS
    # ==================================================================================================================
    def upLip_follow_jaw(self, jaw_ctrl, prefix_upLip_follow, name, jaw_jnt, headLow_normal_rotationGrp, crv_up_lip, mouth_offset_lip_grp, mouth_lip_grp):

        # UPPERLIP FOLLOWING JAW
        upLipX_follow_jaw = mc.createNode('transform', n=au.prefix_name(crv_up_lip) + 'DrvUp%sJawRotX_grp' % name)
        upLipYZ_follow_jaw = mc.group(em=1, n=crv_up_lip + 'DrvUp%sJawRotYZ_grp' % name, p=upLipX_follow_jaw)
        mc.delete(mc.pointConstraint(jaw_jnt, upLipX_follow_jaw, mo=0))
        mc.transformLimits(upLipX_follow_jaw, rx=(-45, 0), erx=(0, 1))

        # REPARENTING THE GROUP
        mc.parent(upLipX_follow_jaw, mouth_lip_grp)
        mc.parent(mouth_offset_lip_grp, upLipYZ_follow_jaw)

        # CONSTRAINT THE GROUP
        oc_upperLipX = mc.orientConstraint(jaw_jnt, upLipX_follow_jaw, mo=1, skip=('y', 'z'))
        oc_upperLipYZ = mc.orientConstraint(jaw_jnt, headLow_normal_rotationGrp, upLipYZ_follow_jaw, mo=1, skip='x')


        oc_upperLipX = au.constraint_rename(oc_upperLipX)[0]
        oc_upperLipYZ = au.constraint_rename(oc_upperLipYZ)[0]
        # mc.setAttr(oc_upperLipYZ+'.interpType', 2)

        # CREATE REVERSE
        reverse_follow_jaw = mc.createNode('reverse', n=au.prefix_name(crv_up_lip) + 'DrvUp%sJawRotXY_rev' % name)
        mc.connectAttr(jaw_ctrl+'.%s' % prefix_upLip_follow, reverse_follow_jaw+'.inputX')

        # CONNECT TO OBJECT
        mc.connectAttr(jaw_ctrl+'.%s' % prefix_upLip_follow, oc_upperLipYZ+'.%sW0' % jaw_jnt)
        mc.connectAttr(reverse_follow_jaw+'.outputX', oc_upperLipYZ+'.%sW1' % headLow_normal_rotationGrp)

    def reverseLowLid(self, control, input2X, input2Y, input2Z, jointBindTarget, name, connect):
        mdnReverse = mc.createNode('multiplyDivide', n=au.prefix_name(control) + 'ReverseAllMouth' + name + '_mdn')
        mc.connectAttr(control + '.%s' %connect, mdnReverse + '.input1')

        mc.setAttr(mdnReverse + '.input2X', input2X)
        mc.setAttr(mdnReverse + '.input2Y', input2Y)
        mc.setAttr(mdnReverse + '.input2Z', input2Z)

        # CONNECT TO OBJECT
        mc.connectAttr(mdnReverse + '.output', jointBindTarget + '.%s' %connect)

        return mdnReverse

    def multiplyLipAndJaw(self, side, cornerAdjustCtrl, jawFollowingCtrl):
        multCornerAdjust = mc.createNode('multDoubleLinear', n='cornerAdjust' + side + '_mdl')
        mc.setAttr(multCornerAdjust + '.input2', 0.1)
        mc.connectAttr(cornerAdjustCtrl, multCornerAdjust + '.input1')

        multJawFollowing = mc.createNode('multDoubleLinear', n='jawFollowing' + side + '_mdl')
        mc.setAttr(multJawFollowing + '.input2', 0.1)
        mc.connectAttr(jawFollowingCtrl, multJawFollowing + '.input1')

        return multCornerAdjust, multJawFollowing

    def jawFollowingSubstract1(self, side, multJawFollowing, nameW,  name):
        sumBothAdjustAndFollow = mc.createNode('plusMinusAverage', n=name + nameW + side + '_pma')
        mc.setAttr(sumBothAdjustAndFollow + '.operation', 2)
        mc.setAttr(sumBothAdjustAndFollow + '.input1D[0]', 1.0)
        mc.connectAttr(multJawFollowing + '.output', sumBothAdjustAndFollow + '.input1D[1]')

        return sumBothAdjustAndFollow

    def upLipJaw(self, side, multCornerAdjust, multJawFollowing, locatorSet01, resetMouthOffsetCtrlGrp, nameW, W0=True):

        multBothAdjustAndFollow = mc.createNode('multDoubleLinear', n='upLipJawFolCornerAdjust' + nameW + side + '_mdl')
        mc.connectAttr(multCornerAdjust + '.output', multBothAdjustAndFollow + '.input1')
        mc.connectAttr(multJawFollowing + '.output', multBothAdjustAndFollow + '.input2')

        if W0:
            sumBothAdjustAndFollow = self.jawFollowingSubstract1(side, multJawFollowing,  nameW, name='upLipJawFolSum')
            valueMinW0 = mc.createNode('plusMinusAverage', n='upLipValueJawFolCornerAdjustW0' + side + '_pma')
            mc.connectAttr(multBothAdjustAndFollow + '.output', valueMinW0 + '.input1D[0]')
            mc.connectAttr(sumBothAdjustAndFollow + '.output1D', valueMinW0 + '.input1D[1]')

            mc.connectAttr(valueMinW0 + '.output1D',
                           '%s_pac.%sW0' % (locatorSet01, resetMouthOffsetCtrlGrp))

        else:
            valueMinW1 = mc.createNode('plusMinusAverage', n='upLipValueJawFolCornerAdjustW1' + side + '_pma')
            mc.setAttr(valueMinW1 + '.operation', 2)
            mc.connectAttr(multJawFollowing + '.output', valueMinW1 + '.input1D[0]')
            mc.connectAttr(multBothAdjustAndFollow + '.output', valueMinW1 + '.input1D[1]')

            mc.connectAttr(valueMinW1 + '.output1D',
                           '%s_pac.%sW1' % (locatorSet01, resetMouthOffsetCtrlGrp))

    def lowLipJaw(self, side, multCornerAdjust, multJawFollowing, locatorSet01, resetMouthOffsetCtrlGrp, nameW, W0=True):

        valueCornerLip = self.jawFollowingSubstract1(side, multJawFollowing, nameW, name='lowLipValueJawFol')
        multBothAdjustAndFollow = mc.createNode('multDoubleLinear', n='lowLipJawFolCornerAdjust'+nameW  + side + '_mdl')
        mc.connectAttr(multCornerAdjust + '.output', multBothAdjustAndFollow + '.input1')
        mc.connectAttr(valueCornerLip + '.output1D', multBothAdjustAndFollow + '.input2')

        if W0:
            subtractBothAdjustAndFollow = self.jawFollowingSubstract1(side, multJawFollowing, nameW, name='lowLipJawFolSubtract')
            valueMinW0 = mc.createNode('plusMinusAverage', n='lowLipValueJawFolCornerAdjustW0' + side + '_pma')
            mc.setAttr(valueMinW0 + '.operation', 2)
            mc.connectAttr(subtractBothAdjustAndFollow + '.output1D', valueMinW0 + '.input1D[0]')
            mc.connectAttr(multBothAdjustAndFollow + '.output', valueMinW0 + '.input1D[1]')

            mc.connectAttr(valueMinW0 + '.output1D',
                           '%s_pac.%sW0' % (locatorSet01, resetMouthOffsetCtrlGrp))

        else:
            valueMinW1 = mc.createNode('plusMinusAverage', n='lowLipValueJawFolCornerAdjustW1' + side + '_pma')
            mc.connectAttr(multJawFollowing + '.output', valueMinW1 + '.input1D[0]')
            mc.connectAttr(multBothAdjustAndFollow + '.output', valueMinW1 + '.input1D[1]')

            mc.connectAttr(valueMinW1 + '.output1D',
                           '%s_pac.%sW1' % (locatorSet01, resetMouthOffsetCtrlGrp))

    def parentConstraintSetLocator(self, lip, upLip, lowLip, conditionLowLip, jawJnt, headLowJnt):
        # parent constraint 01 set locator
        rightCons = mc.parentConstraint(upLip.resetMouthOffsetCtrlGrp, lowLip.resetMouthOffsetCtrlGrp, lip.locatorSet01RGT, mo=1)[0]
        mc.setAttr(rightCons+'.interpType', 2)

        leftCons = mc.parentConstraint(upLip.resetMouthOffsetCtrlGrp, lowLip.resetMouthOffsetCtrlGrp, lip.locatorSet01LFT, mo=1)[0]
        mc.setAttr(leftCons+'.interpType', 2)

        # PARENT CONSTRAINT MID LOCATOR
        pacMidLocCons = mc.parentConstraint(lip.resetMouthOffsetCtrlGrp, lip.locatorSetMid, mo=1)

        # SET THE VALUE
        mc.setAttr(rightCons + '.%sW0' % upLip.resetMouthOffsetCtrlGrp, 0.5)
        mc.setAttr(rightCons + '.%sW1' % lowLip.resetMouthOffsetCtrlGrp, 0.5)
        mc.setAttr(leftCons + '.%sW0' % upLip.resetMouthOffsetCtrlGrp, 0.5)
        mc.setAttr(leftCons + '.%sW1' % lowLip.resetMouthOffsetCtrlGrp, 0.5)

        if conditionLowLip:
            pacResetAllCtrlCons = mc.parentConstraint(jawJnt, lip.resetAllMouthCtrlGrp, mo=1)
            sclResetAllCtrlCons = mc.scaleConstraint(jawJnt, lip.resetAllMouthCtrlGrp, mo=1)
            pacMouthCtrlCons = mc.parentConstraint(jawJnt, lip.mouthCtrlGrp, mo=1)
            sclMouthCtrlCons = mc.scaleConstraint(jawJnt, lip.mouthCtrlGrp, mo=1)

            # rename constraint
            au.constraint_rename([pacResetAllCtrlCons[0], sclResetAllCtrlCons[0], pacMouthCtrlCons[0], sclMouthCtrlCons[0]])

        else:
            # parent constraint mouth reset grp and mouth ctrl all grp
            consMouthReset = mc.parentConstraint(headLowJnt, jawJnt, lip.resetAllMouthCtrlGrp, mo=1)[0]
            consMouthResetScl = mc.scaleConstraint(headLowJnt, lip.resetAllMouthCtrlGrp, mo=1)[0]
            consMouthCtrl = mc.parentConstraint(headLowJnt, jawJnt,  lip.mouthCtrlGrp, mo=1)[0]
            consMouthCtrlScl = mc.scaleConstraint(headLowJnt, lip.mouthCtrlGrp, mo=1)[0]

            # condition low head joint
            cndLowHead = mc.createNode('condition', n=au.prefix_name(self.crvUpLip) + 'DrvLowHead' + '_cnd')
            mc.connectAttr(jawJnt + '.rotateX', cndLowHead + '.firstTerm')
            mc.setAttr(cndLowHead + '.operation', 4)

            mc.connectAttr(cndLowHead + '.outColorR', consMouthReset + '.%sW0' % headLowJnt)
            mc.connectAttr(cndLowHead + '.outColorR', consMouthCtrl + '.%sW0' % headLowJnt)

            # condition jaw joint
            cndJaw = mc.createNode('condition', n=au.prefix_name(self.crvUpLip) + 'DrvJaw' + '_cnd')
            mc.connectAttr(jawJnt + '.rotateX', cndJaw + '.firstTerm')
            mc.setAttr(cndJaw + '.operation', 3)

            mc.connectAttr(cndJaw + '.outColorR', consMouthReset + '.%sW1' % jawJnt)
            mc.connectAttr(cndJaw + '.outColorR', consMouthCtrl + '.%sW1' % jawJnt)

            # rename constraint
            au.constraint_rename([consMouthReset, consMouthResetScl, consMouthCtrl, consMouthCtrlScl])

        # constraint rename
        au.constraint_rename([rightCons, leftCons, pacMidLocCons[0]])

    def upAndLowLipSetup(self, cornerLipCtrlRGT, cornerLipCtrlLFT, sideLFT, sideRGT,
                         prefixBind, prefixCtrl,
                         lip, conditionLowLip=True):
        # CONNECT CORNER CONTROLLER TO OFFSET BIND JNT
        self.reverseDirectionCornerOffsetGrpBind(cornerCtrl=cornerLipCtrlRGT, prefix=prefixBind, side=sideRGT,
                                                 jntBindGrpOffset=lip.jointBind01GrpRGT[1], sideRGT=True)

        self.reverseDirectionCornerOffsetGrpBind(cornerCtrl=cornerLipCtrlLFT, prefix=prefixBind, side=sideLFT,
                                                 jntBindGrpOffset=lip.jointBind01GrpLFT[1], sideRGT=False)

        # CONNECT ROTATION LOCATOR OFFSET LOWLIP OF JAW ROTATION
        for i in lip.parentLocGrpOffset:
            au.connect_attr_rotate(lip.locatorSetMid, i)

        mc.parentConstraint(lip.resetMouthOffsetCtrlGrp, lip.locatorSetMid, mo=1)

        # CONNECT SET LOCATOR TO JOINT BIND GRP ZRO AND CONTROLLER BIND GRP ZRO
        au.connectAttrTransRot(lip.locatorSetMid, lip.controllerBindMid.parent_control[0])
        au.connectAttrTransRot(lip.locatorSetMid, lip.jointBindGrpMid[0])

        # CONNECT SET LOCATOR TO JOINT BIND GRP ZRO AND CONTROLLER BIND GRP ZRO
        au.connectAttrTransRot(lip.locatorSet01RGT, lip.controllerBind01RGT.parent_control[0])
        au.connectAttrTransRot(lip.locatorSet01RGT, lip.jointBind01GrpRGT[0])

        au.connectAttrTransRot(lip.locatorSet01LFT, lip.controllerBind01LFT.parent_control[0])
        au.connectAttrTransRot(lip.locatorSet01LFT, lip.jointBind01GrpLFT[0])

        # CONNECT CORNER CONTROLLER TO CONTROLLER 01 OFFSET GRP
        self.reverseDirectionCornerCtrl(cornerCtrl=cornerLipCtrlRGT, prefix=prefixCtrl, side=sideRGT,
                                        ctrlBindGrpOffset=lip.controllerBind01RGT.parent_control[2], conditionLowLip=conditionLowLip)

        self.reverseDirectionCornerCtrl(cornerCtrl=cornerLipCtrlLFT, prefix=prefixCtrl, side=sideLFT,
                                        ctrlBindGrpOffset=lip.controllerBind01LFT.parent_control[2], conditionLowLip=conditionLowLip)

    def setValueSticky(self, offsetValue, constraint, attributeRGT, attributeLFT, controllerRGT, controllerLFT, lipStickyOriginLocName,
                       lipStickyMidLocName):
        lenCons = len(constraint)
        consRight = constraint[0:((lenCons-1) / 2)]
        consLeft = constraint[((lenCons+1) / 2):]
        consLeft = consLeft[::-1]

        listPart = len(constraint[0:((lenCons+1) / 2)])
        stickyValue = 10
        result = stickyValue / float(listPart)


        # RIGHT SIDE
        self.setKeyframeSticky(result=result, constraintSide=consRight, lipStickyOriginLocName=lipStickyOriginLocName,
                               controller=controllerRGT, attribute=attributeRGT, offsetValue=offsetValue,
                               lipStickyMidLocName=lipStickyMidLocName)

        # LEFT SIDE
        self.setKeyframeSticky(result=result, constraintSide=consLeft, lipStickyOriginLocName=lipStickyOriginLocName,
                               controller=controllerLFT, attribute=attributeLFT, offsetValue=offsetValue,
                               lipStickyMidLocName=lipStickyMidLocName)

        # MID
        midCons = constraint[((lenCons - 1) / 2)]
        # MID RIGHT
        self.setKeyframeStickyMid(result=result, midCons=midCons, lipStickyOriginLocName=lipStickyOriginLocName,
                                  controller=controllerRGT, attribute=attributeRGT, offsetValue=offsetValue,
                                 lipStickyMidLocName=lipStickyMidLocName)
        # MID LEFT
        self.setKeyframeStickyMid(result=result, midCons=midCons, lipStickyOriginLocName=lipStickyOriginLocName,
                                  controller=controllerLFT, attribute=attributeLFT, offsetValue=offsetValue,
                                 lipStickyMidLocName=lipStickyMidLocName)


    def setKeyframeStickyMid(self, result, midCons, lipStickyOriginLocName, controller, attribute, offsetValue,
                          lipStickyMidLocName):

        prefix = self.getNumberOfList(midCons)
        driverVal = float(prefix)

        mc.setDrivenKeyframe(midCons + '.%s%s%sW0' % (lipStickyOriginLocName, prefix, '_loc'),
                             cd='%s.%s' % (controller, attribute),
                             dv=((driverVal-1) * result) * offsetValue, v=0.5, itt='auto', ott='auto')
        mc.setDrivenKeyframe(midCons + '.%s%s%sW0' % (lipStickyOriginLocName, prefix, '_loc'),
                             cd='%s.%s' % (controller, attribute),
                             dv=((driverVal-1) * result) + result, v=0, itt='auto', ott='auto')

        mc.setDrivenKeyframe(midCons + '.%s%s%sW1' % (lipStickyMidLocName, prefix, '_loc'),
                             cd='%s.%s' % (controller, attribute),
                             dv=((driverVal-1) * result) * offsetValue, v=0, itt='auto', ott='auto')
        mc.setDrivenKeyframe(midCons + '.%s%s%sW1' % (lipStickyMidLocName, prefix, '_loc'),
                             cd='%s.%s' % (controller, attribute),
                             dv=((driverVal-1) * result) + result, v=0.5, itt='auto', ott='auto')


    def setKeyframeSticky(self, result, constraintSide, lipStickyOriginLocName, controller, attribute, offsetValue,
                          lipStickyMidLocName):

        for n, i in enumerate(constraintSide):
            prefix = self.getNumberOfList(i)

            mc.setDrivenKeyframe(i + '.%s%s%sW0' % (lipStickyOriginLocName, prefix, '_loc'),
                                 cd='%s.%s' % (controller, attribute),
                                 dv=(float(n) * result) * offsetValue, v=1, itt='auto', ott='auto')
            mc.setDrivenKeyframe(i + '.%s%s%sW0' % (lipStickyOriginLocName, prefix, '_loc'),
                                 cd='%s.%s' % (controller, attribute),
                                 dv=(float(n) * result) + result, v=0, itt='auto', ott='auto')

            mc.setDrivenKeyframe(i + '.%s%s%sW1' % (lipStickyMidLocName, prefix, '_loc'),
                                 cd='%s.%s' % (controller, attribute),
                                 dv=(float(n) * result) * offsetValue, v=0, itt='auto', ott='auto')
            mc.setDrivenKeyframe(i + '.%s%s%sW1' % (lipStickyMidLocName, prefix, '_loc'),
                                 cd='%s.%s' % (controller, attribute),
                                 dv=(float(n) * result) + result, v=1, itt='auto', ott='auto')

    def getNumberOfList(self, object):
        patterns = [r'\d+']
        prefix = au.prefix_name(object)
        for p in patterns:
            prefix = re.findall(p, prefix)[0]
        return prefix

    def reverseDirectionCornerOffsetGrpBind(self, cornerCtrl, prefix, side, jntBindGrpOffset, sideRGT):
        mdnReverseTrans = mc.createNode('multiplyDivide', n='cornerLip' + prefix + 'ReverseTrans' + side + '_mdn')
        mdnReverseRot = mc.createNode('multiplyDivide', n='cornerLip' + prefix + 'ReverseRot' + side + '_mdn')

        if sideRGT:
            mc.setAttr(mdnReverseTrans + '.input2X', -1)
            mc.setAttr(mdnReverseRot + '.input2Z', -1)

            # CONNECT TRANSLATE
            mc.connectAttr(cornerCtrl.control+'.translate', mdnReverseTrans+'.input1')
            mc.connectAttr(mdnReverseTrans+'.output', jntBindGrpOffset+'.translate')

            # CONNECT ROTATE
            mc.connectAttr(cornerCtrl.control+'.rotate', mdnReverseRot+'.input1')
            mc.connectAttr(mdnReverseRot+'.output', jntBindGrpOffset+'.rotate')

        else:
            au.connectAttrTransRot(cornerCtrl.control, jntBindGrpOffset)

    def reverseDirectionCornerCtrl(self, cornerCtrl, prefix, side, ctrlBindGrpOffset, conditionLowLip):
        # CHECK POSITION
        pos = mc.xform(cornerCtrl.control, ws=1, q=1, t=1)[0]

        if conditionLowLip:
            # ADD NODE FOR DRIVING BIND CONTROLLER 01 OFFSET
            mdnReverseTrans = mc.createNode('multiplyDivide', n='cornerLip'+prefix + 'ReverseTrans' + side + '_mdn')
            mdnReverseRot = mc.createNode('multiplyDivide', n='cornerLip'+prefix + 'ReverseRot' + side + '_mdn')

            mc.setAttr(mdnReverseTrans + '.input2X', 1)
            mc.setAttr(mdnReverseTrans + '.input2Y', -1)
            mc.setAttr(mdnReverseTrans + '.input2Z', 1)

            mc.setAttr(mdnReverseRot + '.input2X', -1)
            mc.setAttr(mdnReverseRot + '.input2Y', 1)
            mc.setAttr(mdnReverseRot + '.input2Z', -1)

            mc.connectAttr(cornerCtrl.control + '.rotate', mdnReverseRot + '.input1')
            mc.connectAttr(cornerCtrl.control + '.translate', mdnReverseTrans + '.input1')

            # CONNECTING LIP CORNER CONTROL TO BIND CONTROLLER PARENT GRP OFFSET
            mc.connectAttr(mdnReverseRot + '.output', ctrlBindGrpOffset + '.rotate')
            mc.connectAttr(mdnReverseTrans + '.output', ctrlBindGrpOffset + '.translate')

        else:
            au.connectAttrTransRot(cornerCtrl.control, ctrlBindGrpOffset)