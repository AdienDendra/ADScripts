
import re
from __builtin__ import reload

import maya.cmds as mc
from rigLib.rig.face import lip as lp, lip_corner as lc
from rigLib.utils import controller as ct, transform as tf

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
                         controllerLowLip=False)

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
                          controllerLowLip=True)


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
                 side=sideRGT)

        self.cornerLipCtrlRGT = cornerLipCtrlRGT.control
        self.cheekMidCtrlAttrRGT = cornerLipCtrlRGT.cheekMidCtrl
        self.cheekLowCtrlAttrRGT = cornerLipCtrlRGT.cheekLowCtrl
        self.cheekOutUpCtrlAttrRGT = cornerLipCtrlRGT.cheekOutUpCtrl
        self.cheekOutLowCtrlAttrRGT = cornerLipCtrlRGT.cheekOutLowCtrl
        self.nostrilCtrlAttrRGT = cornerLipCtrlRGT.nostrilCtrl


        # CONTROLLER LFT CORNER
        cornerLipCtrlLFT = lc.Build(
                 matchPosOne=lowLip.jnt01LFT,
                 matchPosTwo=upLip.jnt01LFT,
                 prefix='cornerLipDrv',
                 scale=scale,
                 sticky=True,
                 side=sideLFT)

        self.cornerLipCtrlLFT = cornerLipCtrlLFT.control
        self.cheekMidCtrlAttrLFT = cornerLipCtrlLFT.cheekMidCtrl
        self.cheekLowCtrlAttrLFT = cornerLipCtrlLFT.cheekLowCtrl
        self.cheekOutUpCtrlAttrLFT = cornerLipCtrlLFT.cheekOutUpCtrl
        self.cheekOutLowCtrlAttrLFT = cornerLipCtrlLFT.cheekOutLowCtrl
        self.nostrilCtrlAttrLFT = cornerLipCtrlLFT.nostrilCtrl


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
        au.connect_attr_translate_rotate(self.cornerLipLocSet01RGT, cornerLipCtrlRGT.parentControlZro)
        au.connect_attr_translate_rotate(self.cornerLipLocSet01LFT, cornerLipCtrlLFT.parentControlZro)

        # CONNECT ALL MOUTH CTRL GRP (CENTER) TO CONTROLLER CORNER PARENT OFFSET
        au.connect_attr_scale(upLip.mouthCtrlGrp, cornerLipCtrlRGT.parentControlOffset)
        au.connect_attr_scale(upLip.mouthCtrlGrp, cornerLipCtrlLFT.parentControlOffset)

        # CONTROLLER 01 TRANSLATION AND ROTATION CONNECTED BY CORNER CTRL LFT AND RGT
        # au.connectAttrTransRot(self.lipCornerCtrlLFT, upLip.controllerBind01LFT.parentControl[2])
        # au.connectAttrTransRot(self.lipCornerCtrlLFT, downLip.controllerBind01LFT.parentControl[2])
        #
        # au.connectAttrTransRot(self.lipCornerCtrlRGT, upLip.controllerBind01RGT.parentControl[2])
        # au.connectAttrTransRot(self.lipCornerCtrlRGT, downLip.controllerBind01RGT.parentControl[2])

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
        transMult = mc.createNode('multiplyDivide', n=au.prefix_name(self.crvLowLip) + 'ReverseAllMouthTrans' + '_cnd')
        mc.connectAttr(lowLip.controllerAll + '.translate', transMult + '.input1')
        mc.setAttr(transMult + '.input2Y', -1)
        mc.connectAttr(transMult + '.output', lowLip.resetMouthOffsetCtrlGrp + '.translate')
        au.connect_attr_rotate(lowLip.controllerAll, lowLip.resetMouthOffsetCtrlGrp)
        au.connect_attr_translate_rotate(upLip.controllerAll, upLip.resetMouthOffsetCtrlGrp)

        # EXPRESSION CORNER UP AND LOW LIP CONSTRAINT JAW AND LOW HEAD
        expressionJawLip = '{0}_parentConstraint1.{4}W0 = 1-{2}.{6}*0.1-((1-{2}.{6}*0.1)*{2}.{7}*0.1);' \
                           '{0}_parentConstraint1.{5}W1 = {2}.{6}*0.1+((1-{2}.{6}*0.1)*{2}.{7}*0.1);' \
                           '{1}_parentConstraint1.{4}W0 = 1-{3}.{8}*0.1-((1-{3}.{8}*0.1)*{3}.{9}*0.1);' \
                           '{1}_parentConstraint1.{5}W1 = {3}.{8}*0.1+((1-{3}.{8}*0.1)*{3}.{9}*0.1);' \
        \
                           '{10}_parentConstraint1.{4}W0 = 1-{2}.{6}*0.1+{2}.{6}*0.1*{2}.{7}*0.1;' \
                           '{10}_parentConstraint1.{5}W1 = {2}.{6}*0.1-{2}.{6}*0.1*{2}.{7}*0.1;' \
                           '{11}_parentConstraint1.{4}W0 = 1-{3}.{8}*0.1+{3}.{8}*0.1*{3}.{9}*0.1;' \
                           '{11}_parentConstraint1.{5}W1 = {3}.{8}*0.1-{3}.{8}*0.1*{3}.{9}*0.1;' \
            .format(lowLip.locatorSet01RGT,  # 0
                    lowLip.locatorSet01LFT,  # 1
                    cornerLipCtrlRGT.control,  # 2
                    cornerLipCtrlLFT.control,  # 3
                    upLip.resetMouthOffsetCtrlGrp,  # 4
                    lowLip.resetMouthOffsetCtrlGrp,  # 5
                    cornerLipCtrlRGT.jawFollowCtrl,  # 6
                    cornerLipCtrlRGT.jawUDCtrl,  # 7
                    cornerLipCtrlLFT.jawFollowCtrl,  # 8
                    cornerLipCtrlLFT.jawUDCtrl,  # 9
                    upLip.locatorSet01RGT,  # 10
                    upLip.locatorSet01LFT,  # 11
                    )

        mc.expression(s=expressionJawLip, n='jawFollowLowLip_expr', ae=0)

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
                                          ctrl_size=scale * 1.5,
                                          ctrl_color='lightPink', lock_channels=['v', 's', 'r'])
        self.mouthCtrl = self.mouthController.control
        self.mouthCtrlParentOffset = self.mouthController.parent_control[1]
        self.mouthCtrlParentZro = self.mouthController.parent_control[0]

        # ADD ATTRIBUTE CONTROLLER ROLL
        au.add_attribute(objects=[self.mouthController.control], long_name=['rollSetup'], nice_name=[' '], at="enum",
                         en='Add Setup', channel_box=True)

        self.controllerUpRoll = au.add_attribute(objects=[self.mouthController.control], long_name=['rollUpLip'],
                                                 attributeType="float", min=-10, max=10, dv=0, keyable=True)

        self.controllerLowRoll = au.add_attribute(objects=[self.mouthController.control], long_name=['rollLowLip'],
                                                  attributeType="float", min=-10, max=10, dv=0, keyable=True)

        # CONNECT ROLL ATTRIBUTE CONTROLLER MID TO MDL LIP ROLL
        mc.connectAttr(self.mouthController.control + '.%s' % self.controllerLowRoll, lowLip.mdlLipRoll + '.input1')
        mc.setAttr(lowLip.mdlLipRoll + '.input2', 10)

        mc.connectAttr(self.mouthController.control + '.%s' % self.controllerUpRoll, upLip.mdlLipRoll + '.input1')
        mc.setAttr(upLip.mdlLipRoll + '.input2', -10)

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
    def parentConstraintSetLocator(self, lip, upLip, lowLip, conditionLowLip, jawJnt, headLowJnt):
        # parent constraint 01 set locator
        rightCons = \
        mc.parentConstraint(upLip.resetMouthOffsetCtrlGrp, lowLip.resetMouthOffsetCtrlGrp, lip.locatorSet01RGT, mo=1)[0]
        # rightConsScl = \
        # mc.scaleConstraint(upLip.resetMouthOffsetCtrlGrp, downLip.resetMouthOffsetCtrlGrp, lip.locatorSet01RGT, mo=1)[0]

        leftCons = \
        mc.parentConstraint(upLip.resetMouthOffsetCtrlGrp, lowLip.resetMouthOffsetCtrlGrp, lip.locatorSet01LFT, mo=1)[0]
        # leftConsScl = \
        # mc.scaleConstraint(upLip.resetMouthOffsetCtrlGrp, downLip.resetMouthOffsetCtrlGrp, lip.locatorSet01LFT, mo=1)[0]

        # PARENT CONSTRAINT MID LOCATOR
        mc.parentConstraint(lip.resetMouthOffsetCtrlGrp, lip.locatorSetMid, mo=1)
        # mc.scaleConstraint(lip.resetMouthOffsetCtrlGrp, lip.locatorSetMid, mo=1)

        # SET THE VALUE
        mc.setAttr(rightCons + '.%sW0' % upLip.resetMouthOffsetCtrlGrp, 0.5)
        mc.setAttr(rightCons + '.%sW1' % lowLip.resetMouthOffsetCtrlGrp, 0.5)
        mc.setAttr(leftCons + '.%sW0' % upLip.resetMouthOffsetCtrlGrp, 0.5)
        mc.setAttr(leftCons + '.%sW1' % lowLip.resetMouthOffsetCtrlGrp, 0.5)

        if conditionLowLip:
            mc.parentConstraint(jawJnt, lip.resetAllMouthCtrlGrp, mo=1)
            mc.scaleConstraint(jawJnt, lip.resetAllMouthCtrlGrp, mo=1)
            mc.parentConstraint(jawJnt, lip.mouthCtrlGrp, mo=1)
            mc.scaleConstraint(jawJnt, lip.mouthCtrlGrp, mo=1)

        else:
            # parent constraint mouth reset grp and mouth ctrl all grp
            consMouthReset = mc.parentConstraint(headLowJnt, jawJnt, lip.resetAllMouthCtrlGrp, mo=1)[0]
            consMouthResetScl = mc.scaleConstraint(headLowJnt, lip.resetAllMouthCtrlGrp, mo=1)[0]

            consMouthCtrl = mc.parentConstraint(headLowJnt, jawJnt, lip.mouthCtrlGrp, mo=1)[0]
            consMouthCtrlScl = mc.scaleConstraint(headLowJnt, lip.mouthCtrlGrp, mo=1)[0]

            # condition low head joint
            cndLowHead = mc.createNode('condition', n=self.crvUpLip + 'DrvLowHead' + '_cnd')
            mc.connectAttr(jawJnt + '.rotateX', cndLowHead + '.firstTerm')
            mc.setAttr(cndLowHead + '.operation', 4)

            mc.connectAttr(cndLowHead + '.outColorR', consMouthReset + '.%sW0' % headLowJnt)
            mc.connectAttr(cndLowHead + '.outColorR', consMouthCtrl + '.%sW0' % headLowJnt)
            # mc.connectAttr(cndLowHead + '.outColorR', consMouthResetScl + '.%sW0' % headLowJnt)
            # mc.connectAttr(cndLowHead + '.outColorR', consMouthCtrlScl + '.%sW0' % headLowJnt)

            # condition jaw joint
            cndJaw = mc.createNode('condition', n=self.crvUpLip + 'DrvJaw' + '_cnd')
            mc.connectAttr(jawJnt + '.rotateX', cndJaw + '.firstTerm')
            mc.setAttr(cndJaw + '.operation', 3)

            mc.connectAttr(cndJaw + '.outColorR', consMouthReset + '.%sW1' % jawJnt)
            mc.connectAttr(cndJaw + '.outColorR', consMouthCtrl + '.%sW1' % jawJnt)
            # mc.connectAttr(cndJaw + '.outColorR', consMouthResetScl + '.%sW1' % jawJnt)
            # mc.connectAttr(cndJaw + '.outColorR', consMouthCtrlScl + '.%sW1' % jawJnt)


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
        au.connect_attr_translate_rotate(lip.locatorSetMid, lip.controllerBindMid.parentControl[0])
        au.connect_attr_translate_rotate(lip.locatorSetMid, lip.jointBindGrpMid[0])

        # CONNECT SET LOCATOR TO JOINT BIND GRP ZRO AND CONTROLLER BIND GRP ZRO
        au.connect_attr_translate_rotate(lip.locatorSet01RGT, lip.controllerBind01RGT.parentControl[0])
        au.connect_attr_translate_rotate(lip.locatorSet01RGT, lip.jointBind01GrpRGT[0])

        au.connect_attr_translate_rotate(lip.locatorSet01LFT, lip.controllerBind01LFT.parentControl[0])
        au.connect_attr_translate_rotate(lip.locatorSet01LFT, lip.jointBind01GrpLFT[0])

        # CONNECT CORNER CONTROLLER TO CONTROLLER 01 OFFSET GRP
        self.reverseDirectionCornerCtrl(cornerCtrl=cornerLipCtrlRGT, prefix=prefixCtrl, side=sideRGT,
                                        ctrlBindGrpOffset=lip.controllerBind01RGT.parentControl[2], conditionLowLip=conditionLowLip)

        self.reverseDirectionCornerCtrl(cornerCtrl=cornerLipCtrlLFT, prefix=prefixCtrl, side=sideLFT,
                                        ctrlBindGrpOffset=lip.controllerBind01LFT.parentControl[2], conditionLowLip=conditionLowLip)

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
            au.connect_attr_translate_rotate(cornerCtrl.control, jntBindGrpOffset)

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
            au.connect_attr_translate_rotate(cornerCtrl.control, ctrlBindGrpOffset)