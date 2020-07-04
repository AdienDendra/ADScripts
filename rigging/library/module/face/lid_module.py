import re
from __builtin__ import reload
from string import digits

import maya.cmds as mc

from rigging.library.base.face import lid as el, lid_corner as cl, iris_pupil as ip
from rigging.library.utils import controller as ct
from rigging.library.utils import transform as tf
from rigging.tools import AD_utils as au

reload(el)
reload(ct)
reload(au)
reload(tf)
reload(cl)
reload(ip)

class Lid:
    def __init__(self,
                 faceUtilsGrp,
                 crvUpLid,
                 crvLowLid,
                 offsetLidPos02,
                 offsetLidPos04,
                 eyeballJnt,
                 eyeJnt,
                 prefixEye,
                 prefixEyeAim,
                 scale,
                 side,
                 sideLFT,
                 sideRGT,
                 directionLid01,
                 directionLid02,
                 directionLid03,
                 directionLid04,
                 directionLid05,
                 positionEyeAimCtrl,
                 eyeAimMainCtrl,
                 headUpCtrlGimbal,
                 cornerLip,
                 cornerLipLidAttr,
                 lowLidFolDown,
                 upLidFolDownLowLidFolUp,
                 upLidLRLowLidLR,
                 upLidFolUp,
                 upperHeadGimbalCtrl,

                 pupilJnt,
                 irisJnt,
                 pupilPrefix,
                 irisPrefix,
                 eyeCtrlDirection,
                 suffixController
                 ):

        self.pos = mc.xform(eyeballJnt, ws=1, q=1, t=1)[0]

        # CREATE GROUP FOR LID STUFF
        lidGrp = mc.group(em=1, n='lid' + side + '_grp')

        # world up object lid
        worldUpObject = mc.spaceLocator(n='eyeWorldObj'+side+'_loc')[0]
        mc.delete(mc.parentConstraint(eyeballJnt, worldUpObject))
        value = mc.getAttr(worldUpObject + '.translateY')
        mc.setAttr(worldUpObject + '.translateY', value + (10 * scale))
        # mc.parentConstraint(headUpJoint, worldUpObject, mo=1)
        self.worldUpObject = worldUpObject

        # world up object eye aim
        worldUpAimObject = mc.duplicate(worldUpObject, n='eyeWorldAimObj'+side+'_loc')[0]
        mc.parent(worldUpAimObject, headUpCtrlGimbal)
        mc.hide(worldUpAimObject)
        self.worldUpAimObject = worldUpAimObject

        self.eyeMoveGrp = mc.group(em=1, n='eyeMove' + side + '_grp')
        self.eyeMoveOffset = mc.group(em=1, n='eyeMoveOffset' + side + '_grp', p=self.eyeMoveGrp)
        mc.delete(mc.parentConstraint(eyeballJnt, self.eyeMoveGrp))

        self.eyeMoveAll= mc.group(em=1, n='eyeMoveAll' + side + '_grp')
        mc.parent(self.eyeMoveAll, self.eyeMoveOffset)

        mc.parent(self.eyeMoveGrp, lidGrp)

        # LID UP LFT
        self.upLid = el.Build(crv=crvUpLid,
                              worldUpObject=worldUpObject,
                              eyeballJnt=eyeballJnt,
                              scale=1,
                              offsetLidPos02Jnt=offsetLidPos02,
                              offsetLidPos04Jnt=offsetLidPos04,
                              directionLid01=directionLid01,
                              directionLid02=directionLid02,
                              directionLid03=directionLid03,
                              directionLid04=directionLid04,
                              directionLid05=directionLid05,
                              side=side,
                              sideLFT=sideLFT,
                              sideRGT=sideRGT,
                              ctrlColor='yellow',
                              controllerLidLow=False,
                              upperHeadGimbalCtrl=upperHeadGimbalCtrl,
                              suffixController=suffixController
                              )
        self.lidOutUp01FollowAttr = self.upLid.lidOut01FollowAttr
        self.lidOutUp02FollowAttr = self.upLid.lidOut02FollowAttr
        self.lidOutUp03FollowAttr = self.upLid.lidOut03FollowAttr
        self.lidOutUp04FollowAttr = self.upLid.lidOut04FollowAttr
        self.lidOutUp05FollowAttr = self.upLid.lidOut05FollowAttr
        self.upLidCloseLid = self.upLid.closeLid

        self.upLidControllerBind01 = self.upLid.controllerBind01.control
        self.upLidControllerBind02 = self.upLid.controllerBind02.control
        self.upLidControllerBind03 = self.upLid.controllerBind03.control
        self.upLidControllerBind04 = self.upLid.controllerBind04.control
        self.upLidControllerBind05 = self.upLid.controllerBind05.control

        self.upLidBind01GrpOffset = self.upLid.jointBind01GrpOffset
        self.upLidBind05GrpOffset =  self.upLid.jointBind05GrpOffset
        self.upLidAllJnt = self.upLid.allJoint

        self.lowLid = el.Build(crv=crvLowLid,
                               worldUpObject=worldUpObject,
                               eyeballJnt=eyeballJnt,
                               scale=1,
                               offsetLidPos02Jnt=offsetLidPos02,
                               offsetLidPos04Jnt=offsetLidPos04,
                               directionLid01=directionLid01,
                               directionLid02=directionLid02,
                               directionLid03=directionLid03,
                               directionLid04=directionLid04,
                               directionLid05=directionLid05,
                               side=side,
                               sideLFT=sideLFT,
                               sideRGT=sideRGT,
                               ctrlColor='red',
                               controllerLidLow=True,
                               upperHeadGimbalCtrl=upperHeadGimbalCtrl,
                               suffixController=suffixController
                               )
        self.lidOutLow01FollowAttr = self.lowLid.lidOut01FollowAttr
        self.lidOutLow02FollowAttr = self.lowLid.lidOut02FollowAttr
        self.lidOutLow03FollowAttr = self.lowLid.lidOut03FollowAttr
        self.lidOutLow04FollowAttr = self.lowLid.lidOut04FollowAttr
        self.lidOutLow05FollowAttr = self.lowLid.lidOut05FollowAttr
        self.lowLidCloseLid = self.lowLid.closeLid

        self.lowLidControllerBind01 = self.lowLid.controllerBind01.control
        self.lowLidControllerBind02 = self.lowLid.controllerBind02.control
        self.lowLidControllerBind03 = self.lowLid.controllerBind03.control
        self.lowLidControllerBind04 = self.lowLid.controllerBind04.control
        self.lowLidControllerBind05 = self.lowLid.controllerBind05.control

        self.lowLidBind01GrpOffset = self.lowLid.jointBind01GrpOffset
        self.lowLidBind05GrpOffset =  self.lowLid.jointBind05GrpOffset
        self.lowLidAllJnt = self.lowLid.allJoint

        # BLINK SETUP
        self.blinkSetup(sideRGT=sideRGT, sideLFT=sideLFT, eyeballJnt=eyeballJnt, prefixEye=prefixEye,
                                prefixEyeAim=prefixEyeAim, crvUp=crvUpLid,
                                crvLow=crvLowLid, scale=scale, side=side, upLid=self.upLid,
                                lowLid=self.lowLid, positionEyeAimCtrl=positionEyeAimCtrl,
                                worldUpAimObject=worldUpAimObject, eyeAimJnt=eyeJnt,
                                eyeAimMainCtrl=eyeAimMainCtrl, suffixController=suffixController,
                        eyeCtrlDirection=eyeCtrlDirection)

        # LID BIND FOLLOWING
        self.lidFollowBind(rValueA=lowLidFolDown, rValueB=upLidFolDownLowLidFolUp, rValueC=upLidLRLowLidLR, rValueD=upLidFolUp,
                           eyeAimFollow=self.eyeAimFollow, eyeCtrl=self.eyeballCtrl.control, eyeAimSideCtrl= self.eyeAimCtrl.control,
                           lidUpBindAll03Grp=self.upLid.jointBind03GrpAll, lidLowBindAll03Grp=self.lowLid.jointBind03GrpAll, side=side,
                           eyeAimCtrl=eyeAimMainCtrl, lidLowBindOffset03Grp=self.lowLid.jointBind03GrpOffset,
                           lidUpBindOffset03Grp=self.upLid.jointBind03GrpOffset)

        # LID CTRL FOLLOWING
        self.lidFollowCtrl(eyeAimFollow=self.eyeAimFollow, eyeCtrl=self.eyeballCtrl.control, eyeAimSideCtrl=self.eyeAimCtrl.control,
                           side=side, eyeAimCtrl=eyeAimMainCtrl, lidLowCtrlOffset03Grp=self.lowLid.controllerBind03EyeAimCtrl,
                           lidUpCtrlOffset03Grp=self.upLid.controllerBind03EyeAimCtrl)


        # LID OUT ON OFF FOLLOW
        self.LidOutEyeCtrlTrans = self.lidOutEyeCtrlConnect(side, subPrefix='TransLidOut', sideRGT=sideRGT, sideLFT=sideLFT,
                                                            attribute='translate')
        self.LidOutEyeCtrlRot = self.lidOutEyeCtrlConnect(side, subPrefix='RotLidOut', sideRGT=sideRGT, sideLFT=sideLFT,
                                                          attribute='rotate')

    # ==================================================================================================================
    #                                                  CORNER CONTROLLER
    # ==================================================================================================================
        # controller in corner
        lidCornerCtrl = cl.Build(upLid01=self.upLid.jnt01,
                                   lowLid01=self.lowLid.jnt01,
                                   upLid05=self.upLid.jnt05,
                                   lowLid05=self.lowLid.jnt05,
                                   upLidjointBind01OffsetGrp= self.upLid.jointBind01Grp[1],
                                   lowLidjointBind01OffsetGrp=self.lowLid.jointBind01Grp[1],
                                   upLidjointBind05OffsetGrp=self.upLid.jointBind05Grp[1],
                                   lowLidjointBind05OffsetGrp=self.lowLid.jointBind05Grp[1],
                                   scale=scale, sideRGT=sideRGT, sideLFT=sideLFT,
                                   upLidControllerBindGrpZro01=self.upLid.controllerBindGrpZro01,
                                   lowLidControllerBindGrpZro01=self.lowLid.controllerBindGrpZro01,
                                   upLidControllerBindGrpZro05=self.upLid.controllerBindGrpZro05,
                                   lowLidControllerBindGrpZro05=self.lowLid.controllerBindGrpZro05,
                                   prefixNameIn='cornerLidIn',
                                   prefixNameOut='cornerLidOut',
                                   side=side,
                                   ctrlShape=ct.CIRCLEPLUS,
                                   ctrlColor='blue',
                                   suffixController=suffixController)

        self.lidCornerCtrlInOffset = lidCornerCtrl.lidCornerCtrlInOffset
        self.lidCornerCtrlOutOffset = lidCornerCtrl.lidCornerCtrlOutOffset
        self.lidCornerInCtrl = lidCornerCtrl.inCtrl
        self.lidCornerOutCtrl = lidCornerCtrl.outCtrl

    # ==================================================================================================================
    #                                               CORNER LIP TO LID DOWN
    # ==================================================================================================================
        self.cornerLipToLidDown(rangeGreat=30, rangeLess=10, side=side, cornerLip=cornerLip, lidAttr=cornerLipLidAttr,
                                lidLowCtrlOffset03=self.lowLid.controllerBind03.parent_control[1],
                                lidLowBindCornerLip03=self.lowLid.jointBind03GrpCornerLip)

    # ==================================================================================================================
    #                                               IRIS PUPIL
    # ==================================================================================================================
        irisPupil = ip.Build(pupilJnt=pupilJnt,
                             irisJnt=irisJnt,
                             pupilPrefix=pupilPrefix,
                             irisPrefix=irisPrefix,
                             scale=scale,
                             side=side,
                             eyeballJnt=eyeballJnt,
                             eyeCtrl=self.eyeballController,
                             eyeJntOffsetGrp=self.eyeballGrpOffset,
                             suffixController=suffixController
                             )

    # ==================================================================================================================
    #                                              PARENT TO GROUP
    # ==================================================================================================================

        mc.parent(self.upLid.grpDrvCtrl, self.lowLid.grpDrvCtrl, lidCornerCtrl.inParentGrpZro,
                  lidCornerCtrl.outParentGrpZro, self.upLid.allJointCtrl, self.lowLid.allJointCtrl,
                  self.eyeballCtrl.control)

        mc.parent(self.upLid.locatorGrp, self.upLid.curvesGrp, self.lowLid.locatorGrp, self.lowLid.curvesGrp,  self.eyeMoveAll)

        mc.parent(self.upLid.bindJntGrp, self.lowLid.bindJntGrp, lidGrp)

        mc.parent(self.eyeballCtrl.parent_control[0], self.upLid.grp0204Ctrl, self.lowLid.grp0204Ctrl, headUpCtrlGimbal)
        mc.parent(lidGrp, self.upLid.moveZro, self.lowLid.moveZro, faceUtilsGrp)

    # ==================================================================================================================
    #                                                   FUNCTIONS
    # ==================================================================================================================
    def partLidFollowValueRange(self, rangeValue, side, attrCtrl, prefix, subPrefix, attribute, input1='input1X',
                                input2='input2X', prefixName='eyeAimValueRange'):
        valueRange = mc.createNode('multiplyDivide', n=prefixName + prefix + subPrefix + side + '_mdn')
        mc.setAttr(valueRange + '.operation', 2)
        mc.setAttr(valueRange + '.%s' % input1, rangeValue)
        mc.connectAttr(attrCtrl + '.%s' % attribute, valueRange + '.%s' % input2)

        return valueRange

    def partLidFollowRangeConnected(self, side, attrCtrl, valueRange, prefix, subPrefix, attribute, operation=2, prefixName='eyeAimRange'):
        rangeSide = mc.createNode('multiplyDivide', n=prefixName + prefix + subPrefix + side + '_mdn')
        mc.setAttr(rangeSide + '.operation', operation)
        mc.connectAttr(attrCtrl + '.%s' % attribute, rangeSide + '.input1X')
        mc.connectAttr(valueRange + '.outputX', rangeSide + '.input2X')

        return rangeSide

    def cornerLipToLidDown(self, rangeGreat, rangeLess, side, cornerLip, lidAttr, lidLowCtrlOffset03, lidLowBindCornerLip03):

        if self.pos >0:
            positionValue=1
        else:
            positionValue=-1

        valueRangeGreat = self.partLidFollowValueRange(rangeValue=rangeGreat, side=side, attrCtrl=cornerLip, prefix='',
                                                       subPrefix='rngGreat', attribute=lidAttr, prefixName='eyeCornerLip',
                                                       input1='input2X',
                                                       input2='input1X',
                                                       )

        valueRangeLess = self.partLidFollowValueRange(rangeValue=rangeLess, side=side, attrCtrl=cornerLip, prefix='',
                                                      subPrefix='rngLess', attribute=lidAttr, prefixName='eyeCornerLip',
                                                      input1='input2X',
                                                      input2='input1X',
                                                      )

        # CONNECT THE VALUE RANGE
        multCtrlToRngGreatX = self.partLidFollowRangeConnected(side, attrCtrl=cornerLip, valueRange=valueRangeGreat,
                                                               prefix='', subPrefix='GreatTx', attribute='translateX',
                                                               operation=1, prefixName='eyeCornerLip')

        multCtrlToRngGreatY = self.partLidFollowRangeConnected(side, attrCtrl=cornerLip, valueRange=valueRangeGreat,
                                                               prefix='', subPrefix='GreatTy', attribute='translateY',
                                                               operation=1, prefixName='eyeCornerLip')

        multCtrlToRngLessY = self.partLidFollowRangeConnected(side, attrCtrl=cornerLip, valueRange=valueRangeLess,
                                                              prefix='', subPrefix='LessTy', attribute='translateY',
                                                              operation=1, prefixName='eyeCornerLip')

        # CONNECT NODE MDL WHETHER ON LFT AS POSITIVE OR RIGHT AS NEGATIVE
        posMdl = mc.createNode('multDoubleLinear', n='eyeCornerLipPos' + side + '_mdl')
        mc.setAttr(posMdl+'.input2', positionValue)
        mc.connectAttr(multCtrlToRngGreatX + '.outputX', posMdl + '.input1')

        # CONNECT THE ATTRIBUTE FOR TRANSLATE X
        mc.connectAttr(posMdl + '.output', lidLowCtrlOffset03 + '.translateX')
        mc.connectAttr(posMdl + '.output', lidLowBindCornerLip03 + '.translateX')

        # CREATE CONDITION FOR GREAT AND LESS
        conditionSide = mc.createNode('condition', n='eyeCornerLipBind' + side + '_cnd')
        mc.setAttr(conditionSide + '.operation', 3)
        mc.connectAttr(cornerLip + '.translateY', conditionSide + '.firstTerm')

        mc.connectAttr(multCtrlToRngLessY + '.outputX', conditionSide + '.colorIfTrueR')
        mc.connectAttr(multCtrlToRngGreatY + '.outputX', conditionSide + '.colorIfFalseR')

        mc.connectAttr(conditionSide + '.outColorR', lidLowCtrlOffset03 + '.translateY')
        mc.connectAttr(conditionSide + '.outColorR', lidLowBindCornerLip03 + '.translateY')

        # mc.setAttr(conditionAimSide + '.colorIfTrueG', 0)
        # mc.connectAttr(eyeAimCtrl + '.translateY', conditionAimSide + '.firstTerm')

    def lidOutEyeCtrlConnect(self, side, subPrefix, sideRGT, sideLFT, attribute):
        newTargetUp, numberTargetUp = self.reorderNumber(prefix=self.eyeballController, sideRGT=sideRGT, sideLFT=sideLFT)

        mdn = mc.createNode('multiplyDivide', n=au.prefix_name(newTargetUp) + subPrefix + numberTargetUp + side + '_mdn')
        mc.connectAttr(self.eyeballController + '.%s' % attribute, mdn + '.input1')
        mc.connectAttr(self.eyeballController + '.' + self.lidOutFollow, mdn + '.input2X')
        mc.connectAttr(self.eyeballController + '.' + self.lidOutFollow, mdn + '.input2Y')
        mc.connectAttr(self.eyeballController + '.' + self.lidOutFollow, mdn + '.input2Z')

        return mdn


    # def lidOnOffFollow(self, side, eyeController, targetUp, sideRGT, sideLFT):
    #     newTargetUp, numberTargetUp = self.reorderNumber(prefix=targetUp, sideRGT=sideRGT, sideLFT=sideLFT)
    #
    #     transRev = mc.createNode('multiplyDivide', n=au.prefixName(newTargetUp) + 'Trans' +numberTargetUp+side+ '_mdn')
    #     rotRev = mc.createNode('multiplyDivide', n=au.prefixName(newTargetUp) + 'Rot' +numberTargetUp+side+ '_mdn')
    #
    #     mc.connectAttr(eyeController + '.translate', transRev + '.input1')
    #     mc.connectAttr(self.eyeController + '.' + self.lidFollow, transRev + '.input2X')
    #     mc.connectAttr(self.eyeController + '.' + self.lidFollow, transRev + '.input2Y')
    #     mc.connectAttr(self.eyeController + '.' + self.lidFollow, transRev + '.input2Z')
    #
    #     mc.connectAttr(eyeController + '.rotate', rotRev + '.input1')
    #     mc.connectAttr(self.eyeController + '.' + self.lidFollow, rotRev + '.input2X')
    #     mc.connectAttr(self.eyeController + '.' + self.lidFollow, rotRev + '.input2Y')
    #     mc.connectAttr(self.eyeController + '.' + self.lidFollow, rotRev + '.input2Z')
    #
    #     mc.connectAttr(transRev + '.output', targetUp + '.translate')
    #     mc.connectAttr(rotRev + '.output', targetUp + '.rotate')


    def blinkSetup(self, sideRGT, sideLFT, eyeballJnt, prefixEye, prefixEyeAim, crvUp, crvLow, scale,
                   side, upLid, lowLid, positionEyeAimCtrl, worldUpAimObject, eyeAimMainCtrl, eyeAimJnt, suffixController,
                   eyeCtrlDirection
                   ):

        # ==============================================================================================================
        #                                             EYEBALL CONTROLLER
        # ==============================================================================================================

        eyeballGrp = tf.create_parent_transform(parent_list=['Zro', 'Offset'], object=eyeballJnt, match_position=eyeballJnt,
                                                prefix='eyeball',
                                                suffix='_jnt', side=side)

        self.eyeballCtrl = ct.Control(match_obj_first_position=eyeballJnt,
                                      prefix=prefixEye,
                                      shape=ct.JOINTPLUS, groups_ctrl=['Zro', 'Offset'],
                                      ctrl_size=scale * 0.5,
                                      ctrl_color='turquoiseBlue', lock_channels=['v'], side=side,
                                      suffix=suffixController,
                                      connection=['connectMatrixAll'])

        self.eyeballController = self.eyeballCtrl.control
        self.eyeballGrpOffset = eyeballGrp[1]

        # ADD ATTRIBUTE
        au.add_attribute(objects=[self.eyeballCtrl.control], long_name=['lidDegree'], nice_name=[' '], at="enum",
                         en='Lid Degree', channel_box=True)

        self.lidPos = au.add_attribute(objects=[self.eyeballCtrl.control], long_name=['lidPos'],
                                       attributeType="float", min=0, max=1, dv=0.5, keyable=True)

        self.eyeAimFollow = au.add_attribute(objects=[self.eyeballCtrl.control], long_name=['eyeAimFollow'],
                                             attributeType="float", min=0.001, dv=1, keyable=True)

        # self.lidFollow = au.addAttribute(objects=[self.eyeCtrl.control], longName=['lidFollow'],
        #                                  attributeType="float", min=0, max=1, dv=1, k=True)

        self.lidOutFollow = au.add_attribute(objects=[self.eyeballCtrl.control], long_name=['lidOutFollow'],
                                             attributeType="float", min=0, max=1, dv=0.5, keyable=True)

        # mc.parent(eyeballGrp[0], headUpJnt)

        # ==============================================================================================================
        #                                                   EYE AIM
        # ==============================================================================================================

        if mc.xform(eyeballJnt, q=1, ws=1, t=1)[0] > 0:
            ctrlColor ='red'
        else:
            ctrlColor='yellow'

        self.eyeAimCtrl = ct.Control(match_obj_first_position=eyeAimJnt,
                                     prefix=prefixEyeAim,
                                     shape=ct.LOCATOR, groups_ctrl=['Zro', 'Offset'],
                                     ctrl_size=scale * 0.25, suffix=suffixController,
                                     ctrl_color=ctrlColor, lock_channels=['v', 'r', 's'], side=side)

        getAttribute = mc.getAttr(self.eyeAimCtrl.parent_control[0] + '.translateZ')
        mc.setAttr(self.eyeAimCtrl.parent_control[0] + '.translateZ', getAttribute + (positionEyeAimCtrl * scale))

        aimEyeCons = mc.aimConstraint(self.eyeAimCtrl.control, eyeballGrp[1], mo=1, weight=1, aimVector=(0, 0, 1), upVector=(0, 1, 0),
                         worldUpType="object", worldUpObject=worldUpAimObject)

        # CONSTRAINT RENAME
        au.constraint_rename(aimEyeCons)

        # PARENT EYE AIM TO EYE AIM MAIN CTRL
        mc.parent(self.eyeAimCtrl.parent_control[0], eyeAimMainCtrl)

        # MAKE GRP TRANSFORM EYE JNT
        eyeGrp = tf.create_parent_transform(parent_list=[''], object=eyeAimJnt, match_position=eyeAimJnt,
                                            prefix='eye',
                                            suffix='_jnt', side=side)

        # ROTATE THE EYE GROUP
        if  self.pos >=0:
            mc.setAttr(eyeGrp[0] +'.rotateY', eyeCtrlDirection)

        else:
            mc.setAttr(eyeGrp[0] +'.rotateY', eyeCtrlDirection*-1)


        # CONNECT THE AIM JNT
        au.connect_attr_object(self.eyeballController, eyeAimJnt)


        # ==============================================================================================================
        #                                                   BLINK
        # ==============================================================================================================
        # if blinkOpen:
        #     self.blinkOpen(side=side, crvUp=crvUp, crvLow=crvLow, upLid, lowLid, sideRGT, sideLFT, scale)

    # def blinkOpen(self, side, crvUp, crvLow, upLid, lowLid, sideRGT, sideLFT, scale):
        # CREATE CURVE MID BLINK
        curveBlinkBindMidOld = mc.curve(d=3, ep=[(self.upLid.xformJnt01), (self.upLid.xformJnt05)])
        curveBlinkBindMidReb = mc.rebuildCurve(curveBlinkBindMidOld, ch=0, rpo=1, rt=0, end=1, kr=0, kcp=0,
                                                               kep=1, kt=0, s=8, d=3, tol=0.01)

        curveBlinkBindMid = mc.rename(curveBlinkBindMidReb, ('lidBlink' + side + '_crv'))

        curveBlinkUp = mc.duplicate(crvUp, n='lidBlinkUp'+side+'_crv')[0]
        curveBlinkLow = mc.duplicate(crvLow, n='lidBlinkLow' + side + '_crv')[0]

        blinkBsn = mc.blendShape(upLid.deformCrv, lowLid.deformCrv, curveBlinkBindMid, n=('lidBlink' + side + '_bsn'),
                                 weight=[(0, 1), (1, 0)])[0]

        mc.select(cl=1)
        # replace position LFT and RGT
        crvUpNewName = self.replacePosLFTRGT(object=crvUp, sideRGT=sideRGT, sideLFT=sideLFT)

        # wire deform up on mid curves
        stickyMidwireDefUp = mc.wire(curveBlinkUp, dds=(0, 100 * scale), wire=curveBlinkBindMid)
        stickyMidwireDefUp[0] = mc.rename(stickyMidwireDefUp[0], (au.prefix_name(crvUpNewName) + 'Blink' + side + '_wireNode'))
        mc.setAttr(stickyMidwireDefUp[0]+'.scale[0]', 0)

        # SET TO LOW CURVE
        mc.setAttr(blinkBsn +'.%s' % upLid.deformCrv, 0)
        mc.setAttr(blinkBsn +'.%s' % lowLid.deformCrv, 1)

        mc.select(cl=1)
        # replace position LFT and RGT
        crvLowNewName = self.replacePosLFTRGT(object=crvLow, sideRGT=sideRGT, sideLFT=sideLFT)

        stickyMidwireDefLow = mc.wire(curveBlinkLow, dds=(0, 100 * scale), wire=curveBlinkBindMid)
        stickyMidwireDefLow[0] = mc.rename(stickyMidwireDefLow[0], (au.prefix_name(crvLowNewName) + 'Blink' + side + '_wireNode'))
        mc.setAttr(stickyMidwireDefLow[0] + '.scale[0]', 0)

        # SET KEYFRAME
        mc.setDrivenKeyframe(blinkBsn +'.%s' % upLid.deformCrv,
                             cd='%s.%s' % (self.eyeballCtrl.control, self.lidPos),
                             dv=0, v=1, itt='linear', ott='linear')

        mc.setDrivenKeyframe(blinkBsn +'.%s' % upLid.deformCrv,
                             cd='%s.%s' % (self.eyeballCtrl.control, self.lidPos),
                             dv=0.5, v=0, itt='linear', ott='linear')

        mc.setDrivenKeyframe(blinkBsn + '.%s' % lowLid.deformCrv,
                             cd='%s.%s' % (self.eyeballCtrl.control, self.lidPos),
                             dv=0.5, v=0, itt='linear', ott='linear')

        mc.setDrivenKeyframe(blinkBsn + '.%s' % lowLid.deformCrv,
                             cd='%s.%s' % (self.eyeballCtrl.control, self.lidPos),
                             dv=1, v=1, itt='linear', ott='linear')

        # CONNECT TO BLENDSHAPE BIND CURVE
        upLidBsn = mc.blendShape(curveBlinkUp, crvUp, n=('lidBlinkUp' + side + '_bsn'),
                                 weight=[(0, 1)])[0]

        mc.connectAttr(upLid.controllerBind03Ctrl + '.%s' % upLid.closeLid, upLidBsn + '.%s' % curveBlinkUp)

        lowLidBsn = mc.blendShape(curveBlinkLow, crvLow, n=('lidBlinkLow' + side + '_bsn'),
                                  weight=[(0, 1)])[0]

        mc.connectAttr(lowLid.controllerBind03Ctrl + '.%s' % lowLid.closeLid, lowLidBsn + '.%s' % curveBlinkLow)

        # parent eyeblink crve to face curve grp
        mc.parent(curveBlinkBindMid, mc.listConnections(stickyMidwireDefLow[0] + '.baseWire[0]')[0],
                  mc.listConnections(stickyMidwireDefUp[0] + '.baseWire[0]')[0],'faceCurves_grp')





    # CONNECTION UP AND LOW FOLLOW LID BIND
    def lidFollowBind(self, rValueA, rValueB, rValueC, rValueD, eyeAimFollow, eyeCtrl, eyeAimSideCtrl, lidUpBindAll03Grp, lidLowBindAll03Grp, side,
                      eyeAimCtrl, lidLowBindOffset03Grp, lidUpBindOffset03Grp):

        self.partLidBindFollow(rValueA, rValueB, rValueC, rValueD, eyeAimFollow, eyeCtrl, eyeAimSideCtrl,
                               lidBind03Grp=lidUpBindAll03Grp, prefix='Up',
                               side=side, upLid=True)
        self.partLidBindFollow(rValueA, rValueB, rValueC, rValueD, eyeAimFollow, eyeCtrl, eyeAimSideCtrl,
                               lidBind03Grp=lidLowBindAll03Grp, prefix='Low',
                               side=side, upLid=False)

        self.partLidBindFollow(rValueA, rValueB, rValueC, rValueD, eyeAimFollow, eyeCtrl, eyeAimCtrl,
                               lidBind03Grp=lidUpBindOffset03Grp, prefix='MainUp',
                               side=side, upLid=True)

        self.partLidBindFollow(rValueA, rValueB, rValueC, rValueD, eyeAimFollow, eyeCtrl, eyeAimCtrl,
                               lidBind03Grp=lidLowBindOffset03Grp, prefix='MainLow',
                               side=side, upLid=False)


    def partLidBindFollow(self, rValueA, rValueB, rValueC, rValueD, eyeAimFollow, eyeCtrl, eyeAimCtrl, lidBind03Grp,  side, upLid, prefix='',):
        valueRangeB = self.partLidFollowValueRange(rangeValue=rValueB, side=side, attrCtrl=eyeCtrl, prefix=prefix,
                                                   subPrefix='BBind', attribute=eyeAimFollow)
        valueRangeC = self.partLidFollowValueRange(rangeValue=rValueC, side=side, attrCtrl=eyeCtrl, prefix=prefix,
                                                   subPrefix='CBind', attribute=eyeAimFollow)

        # CREATE CONDITION AIM SIDE
        conditionAimSideGreater = mc.createNode('condition', n='eyeAimBind' +prefix+ side + '_cnd')
        mc.setAttr(conditionAimSideGreater + '.colorIfTrueG', 0)
        mc.connectAttr(eyeAimCtrl + '.translateY', conditionAimSideGreater + '.firstTerm')

        # CREATE DIVIDE RANGE AIM SIDE B
        rangeAimBindB= self.partLidFollowRangeConnected(side, eyeAimCtrl, valueRange=valueRangeB,
                                                        prefix=prefix, subPrefix='BBind', attribute='translateY')
        mc.connectAttr(rangeAimBindB + '.outputX', conditionAimSideGreater + '.colorIfTrueR')
        # mc.connectAttr(rangeAimBindB + '.outputX', conditionAimSideGreater + '.colorIfTrueG')

        # CREATE DIVIDE RANGE AIM SIDE D
        if upLid:
            valueRangeD = self.partLidFollowValueRange(rangeValue=rValueD, side=side, attrCtrl=eyeCtrl, prefix=prefix,
                                                       subPrefix='DBind', attribute=eyeAimFollow)
            mc.setAttr(conditionAimSideGreater + '.operation', 5)
            rangeAimBindD= self.partLidFollowRangeConnected(side, eyeAimCtrl, valueRange=valueRangeD,
                                                            prefix=prefix, subPrefix='DBind', attribute='translateY')
            mc.connectAttr(rangeAimBindD + '.outputX', conditionAimSideGreater + '.colorIfFalseR')

        # CREATE DIVIDE RANGE AIM SIDE A
        else:
            valueRangeA = self.partLidFollowValueRange(rangeValue=rValueA, side=side, attrCtrl=eyeCtrl, prefix=prefix,
                                                       subPrefix='ABind', attribute=eyeAimFollow)
            mc.setAttr(conditionAimSideGreater + '.operation', 3)
            rangeAimBindA= self.partLidFollowRangeConnected(side, eyeAimCtrl, valueRange=valueRangeA,
                                                            prefix=prefix, subPrefix='ABind', attribute='translateY')
            mc.connectAttr(rangeAimBindA + '.outputX', conditionAimSideGreater + '.colorIfFalseR')


        mc.connectAttr(conditionAimSideGreater + '.outColorR', lidBind03Grp + '.translateY')
        # mc.connectAttr(conditionAimSideGreater + '.outColorR', lidLowBind03Grp + '.translateY')

        # CREATE DIVIDE RANGE AIM SIDE C
        rangeAimBindC= self.partLidFollowRangeConnected(side, eyeAimCtrl, valueRange=valueRangeC, prefix=prefix, subPrefix='CBind', attribute='translateX')
        mc.connectAttr(rangeAimBindC + '.outputX', lidBind03Grp + '.translateX')
        # mc.connectAttr(rangeAimBindC + '.outputX', conditionAimSideLessC + '.colorIfTrueG')

        # mc.connectAttr(conditionAimSideGreater + '.outColorG', lidBind03Grp + '.translateX')

        # else:
        #     mc.connectAttr(conditionAimSideGreater + '.outColorR', lidLowBind03Grp + '.translateY')
        #     mc.connectAttr(conditionAimSideGreater + '.outColorG', lidUpBind03Grp + '.translateY')

        # # # CONDITION EXCEPTION AIM SIDE C
        # conditionAimSideLessC = mc.createNode('condition', n='eyeAimBindLess' +prefix+ side + '_cnd')
        # mc.setAttr(conditionAimSideLessC + '.operation', 4)
        # mc.setAttr(conditionAimSideLessC + '.colorIfFalseR', 0)
        # mc.setAttr(conditionAimSideLessC + '.colorIfFalseG', 0)
        # mc.connectAttr(eyeAimCtrl + '.translateY', conditionAimSideLessC + '.firstTerm')
        # else:
        #     mc.connectAttr(conditionAimSideGreater + '.outColorR', lidLowBind03Grp + '.translateX')
        #     mc.connectAttr(conditionAimSideGreater + '.outColorG', lidUpBind03Grp + '.translateX')

    def lidFollowCtrl(self, eyeAimFollow, eyeCtrl, eyeAimSideCtrl, side,
                      eyeAimCtrl, lidLowCtrlOffset03Grp, lidUpCtrlOffset03Grp):

        valueRangeA = self.partLidFollowValueRange(rangeValue=20.0, side=side, attrCtrl=eyeCtrl, prefix='', subPrefix='ACtrl', attribute=eyeAimFollow)
        valueRangeB = self.partLidFollowValueRange(rangeValue=30.0, side=side, attrCtrl=eyeCtrl, prefix='', subPrefix='BCtrl', attribute=eyeAimFollow)
        valueRangeC = self.partLidFollowValueRange(rangeValue=80.0, side=side, attrCtrl=eyeCtrl, prefix='', subPrefix='CCtrl', attribute=eyeAimFollow)

        # CREATE DIVIDE RANGE AIM AND AIM SIDE C
        rangeAimC= self.partLidFollowRangeConnected(side=side, attrCtrl=eyeAimCtrl, valueRange=valueRangeC,
                                                    prefix='Main', subPrefix='CCtrl', attribute='translateX')

        rangeAimSideC= self.partLidFollowRangeConnected(side=side, attrCtrl=eyeAimSideCtrl, valueRange=valueRangeC,
                                                        prefix='', subPrefix='CCtrl', attribute='translateX')

        sumAimSideAndAimC = mc.createNode('plusMinusAverage', n='eyeAimCtrlRangeC' + side + '_pma')
        mc.connectAttr(rangeAimC + '.outputX', sumAimSideAndAimC + '.input1D[0]')
        mc.connectAttr(rangeAimSideC + '.outputX', sumAimSideAndAimC + '.input1D[1]')

        # CREATE DIVIDE RANGE AIM SIDE A
        rangeAimA= self.partLidFollowRangeConnected(side=side, attrCtrl=eyeAimCtrl, valueRange=valueRangeA,
                                                    prefix='Main', subPrefix='ACtrl', attribute='translateY')
        rangeAimSideA= self.partLidFollowRangeConnected(side=side, attrCtrl=eyeAimSideCtrl, valueRange=valueRangeA,
                                                        prefix='', subPrefix='ACtrl', attribute='translateY')

        sumAimSideAndAimA = mc.createNode('plusMinusAverage', n='eyeAimCtrlRangeA' + side + '_pma')
        mc.connectAttr(rangeAimA + '.outputX', sumAimSideAndAimA + '.input1D[0]')
        mc.connectAttr(rangeAimSideA + '.outputX', sumAimSideAndAimA + '.input1D[1]')

        # CREATE DIVIDE RANGE AIM B
        rangeAimB= self.partLidFollowRangeConnected(side=side, attrCtrl=eyeAimCtrl, valueRange=valueRangeB,
                                                    prefix='Main', subPrefix='BCtrl', attribute='translateY')
        rangeAimSideB= self.partLidFollowRangeConnected(side=side, attrCtrl=eyeAimSideCtrl, valueRange=valueRangeB,
                                                        prefix='', subPrefix='BCtrl', attribute='translateY')

        rangeAimBRev = mc.createNode('multDoubleLinear', n='eyeAimCtrlRangeBRev' + side+ '_mdl')
        mc.setAttr(rangeAimBRev + '.input1', -1)
        mc.connectAttr(rangeAimB + '.outputX', rangeAimBRev + '.input2')

        sumAimSideAndAimB = mc.createNode('plusMinusAverage', n='eyeAimCtrlRangeB' + side + '_pma')
        mc.setAttr(sumAimSideAndAimB + '.operation', 2)
        mc.connectAttr(rangeAimBRev + '.output', sumAimSideAndAimB + '.input1D[0]')
        mc.connectAttr(rangeAimSideB + '.outputX', sumAimSideAndAimB + '.input1D[1]')

        mc.connectAttr(sumAimSideAndAimC + '.output1D', lidUpCtrlOffset03Grp + '.translateX')
        mc.connectAttr(sumAimSideAndAimA + '.output1D', lidUpCtrlOffset03Grp + '.translateY')
        mc.connectAttr(sumAimSideAndAimC + '.output1D', lidLowCtrlOffset03Grp + '.translateX')
        mc.connectAttr(sumAimSideAndAimB + '.output1D', lidLowCtrlOffset03Grp + '.translateY')

    def reorderNumber(self, prefix, sideRGT, sideLFT):
        # get the number
        newPrefix = self.replacePosLFTRGT(object=prefix, sideRGT=sideRGT, sideLFT=sideLFT)
        try:
            patterns = [r'\d+']
            prefixNumber = au.prefix_name(newPrefix)
            for p in patterns:
                prefixNumber = re.findall(p, prefixNumber)[0]
        except:
            prefixNumber=''

        # get the prefix without number
        prefixNoNumber = str(newPrefix).translate(None, digits)

        return prefixNoNumber, prefixNumber

    def replacePosLFTRGT(self, object, sideRGT, sideLFT):
        if sideRGT in object:
            crvNewName = object.replace(sideRGT, '')
        elif sideLFT in object:
            crvNewName = object.replace(sideLFT, '')
        else:
            crvNewName = object

        return crvNewName