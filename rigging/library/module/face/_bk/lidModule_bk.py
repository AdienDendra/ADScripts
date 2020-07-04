from __builtin__ import reload

import maya.cmds as mc
from rigLib.rig.face import lid as el
from rigLib.utils import controller as ct, transform as tf

from rigging.tools import AD_utils as au

reload(el)
reload(ct)
reload(au)
reload(tf)

class Lid:
    def __init__(self,
                 faceUtilsGrp,
                 crvUpLid,
                 crvLowLid,
                 offsetLidPos02,
                 offsetLidPos04,
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
                 headUpCtrlGimbal
                 ):
        # CREATE GROUP FOR LID STUFF
        lidGrp = mc.group(em=1, n='lid' + side + '_grp')

        # world up object lid
        worldUpObject = mc.spaceLocator(n='eyeWorldObj'+side+'_loc')[0]
        mc.delete(mc.parentConstraint(eyeJnt, worldUpObject))
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
        mc.delete(mc.parentConstraint(eyeJnt, self.eyeMoveGrp))

        self.eyeMoveAll= mc.group(em=1, n='eyeMoveAll' + side + '_grp')
        mc.parent(self.eyeMoveAll, self.eyeMoveOffset)

        mc.parent(self.eyeMoveGrp, lidGrp)

        # LID UP LFT
        self.upLid = el.Build(crv=crvUpLid,
                              worldUpObject=worldUpObject,
                              eyeballJnt=eyeJnt,
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
                              controllerLidLow=False)

        self.lowLid = el.Build(crv=crvLowLid,
                               worldUpObject=worldUpObject,
                               eyeballJnt=eyeJnt,
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
                               controllerLidLow=True)

        # BLINK SETUP
        blink = self.blinkSetup(sideRGT=sideRGT, sideLFT=sideLFT, eyeJnt=eyeJnt, prefixEye=prefixEye,
                                prefixEyeAim=prefixEyeAim, crvUp=crvUpLid,
                                crvLow=crvLowLid, scale=scale, side=side, upLid=self.upLid,
                                lowLid=self.lowLid, positionEyeAimCtrl=positionEyeAimCtrl,
                                worldUpAimObject=worldUpAimObject,
                                eyeAimMainCtrl=eyeAimMainCtrl,
                                controllerBind03OffsetCtrlUp=self.upLid.controllerBind03OffsetCtrl,
                                controllerBind03OffsetCtrlLow=self.lowLid.controllerBind03OffsetCtrl,
                                jointBind03GrpAllUp=self.upLid.jointBind03GrpAll,
                                jointBind03GrpAllLow=self.lowLid.jointBind03GrpAll,
                                jointBind03GrpOffsetLow=self.upLid.jointBind03GrpOffset,
                                jointBind03GrpOffsetUp=self.lowLid.jointBind03GrpOffset)

        # # connect the eyeball to eyeball up grp bind
        # au.connectAttrTransRot(self.eyeController, self.eyelidUp.eyeOffsetBind01[1])
        # au.connectAttrTransRot(self.eyeController, self.eyelidUp.eyeOffsetBind03[1])
        # au.connectAttrTransRot(self.eyeController, self.eyelidUp.eyeOffsetBind05[1])
        #
        # # connect the eyeball to eyeball down grp bind
        # au.connectAttrTransRot(self.eyeController, self.eyelidDown.eyeOffsetBind01[1])
        # au.connectAttrTransRot(self.eyeController, self.eyelidDown.eyeOffsetBind03[1])
        # au.connectAttrTransRot(self.eyeController, self.eyelidDown.eyeOffsetBind05[1])
        # reverse = mc.createNode('reverse', n='eyelidFollow'+ side + '_rev')
        # mc.connectAttr(self.eyeController + '.' + self.eyelidFollow, reverse + '.inputX')

        self.lidOnOffFollow(eyeController=self.eyeController, targetUp=self.upLid.eyeOffsetBind01[1])
        self.lidOnOffFollow(eyeController=self.eyeController, targetUp=self.upLid.eyeOffsetBind03[1])
        self.lidOnOffFollow(eyeController=self.eyeController, targetUp=self.upLid.eyeOffsetBind05[1])

        self.lidOnOffFollow(eyeController=self.eyeController, targetUp=self.lowLid.eyeOffsetBind01[1])
        self.lidOnOffFollow(eyeController=self.eyeController, targetUp=self.lowLid.eyeOffsetBind03[1])
        self.lidOnOffFollow(eyeController=self.eyeController, targetUp=self.lowLid.eyeOffsetBind05[1])

        # parent contraint eye move
        au.connect_attr_translate(self.eyeController, self.eyeMoveOffset)

        # CONNECT SCALE EYE CTRL TO JOINT CTR
        for up, low in zip (self.upLid.allJointCenter, self.lowLid.allJointCenter):
            au.connect_attr_scale(self.eyeController, up)
            au.connect_attr_scale(self.eyeController, low)

    # ==================================================================================================================
    #                                                  CORNER CONTROLLER
    # ==================================================================================================================
        # controller in corner
        lidCornerCtrlIn = self.cornerCtrl(matchPosOne=self.upLid.jnt01,
                                          matchPosTwo=self.lowLid.jnt01,
                                          prefix='cornerLidIn',
                                          scale=scale,
                                          side=side)

        # controller in corner
        lidCornerCtrlOut = self.cornerCtrl(matchPosOne=self.upLid.jnt05,
                                           matchPosTwo=self.lowLid.jnt05,
                                           prefix='cornerLidOut',
                                           scale=scale,
                                           side=side)

        pos = mc.xform(lidCornerCtrlOut[0], ws=1, q=1, t=1)[0]
        if pos > 0:
            # parent constraint corner grp bind jnt
            au.connectAttrTransRot(lidCornerCtrlIn[0], self.upLid.jointBind01Grp[1])
            au.connectAttrTransRot(lidCornerCtrlIn[0], self.lowLid.jointBind01Grp[1])
            au.connectAttrTransRot(lidCornerCtrlOut[0], self.upLid.jointBind05Grp[1])
            au.connectAttrTransRot(lidCornerCtrlOut[0], self.lowLid.jointBind05Grp[1])
        else:
            self.cornerReverseNode(sideRGT, sideLFT, lidCornerCtrl=lidCornerCtrlOut[0], side=side, lidCornerName='lidCornerOut',
                                   targetUp=self.upLid.jointBind05Grp[1], targetLow=self.lowLid.jointBind05Grp[1])

            self.cornerReverseNode(sideRGT, sideLFT, lidCornerCtrl=lidCornerCtrlIn[0], side=side, lidCornerName='lidCornerIn',
                                   targetUp=self.upLid.jointBind01Grp[1], targetLow=self.lowLid.jointBind01Grp[1])

    # ==================================================================================================================
    #                                              PARENT TO GROUP
    # ==================================================================================================================
        mc.parent(self.upLid.controllerBindGrpZro01, lidCornerCtrlIn[0])
        mc.parent(self.lowLid.controllerBindGrpZro01, lidCornerCtrlIn[0])
        mc.parent(self.upLid.controllerBindGrpZro05, lidCornerCtrlOut[0])
        mc.parent(self.lowLid.controllerBindGrpZro05, lidCornerCtrlOut[0])

        mc.parent(self.upLid.grpDrvCtrl, self.lowLid.grpDrvCtrl, lidCornerCtrlIn[1],
                  lidCornerCtrlOut[1], self.eyeCtrl.control)

        mc.parent(self.upLid.jointGrp, self.upLid.locatorGrp,
                  self.upLid.curvesGrp, self.upLid.jointGrp,
                  self.lowLid.jointGrp, self.lowLid.locatorGrp,
                  self.lowLid.curvesGrp, self.lowLid.jointGrp, self.eyeMoveAll)

        mc.parent(self.upLid.bindJntGrp, self.lowLid.bindJntGrp, lidGrp)

        mc.parent(self.eyeCtrl.parent_control[0], headUpCtrlGimbal)
        mc.parent(lidGrp, faceUtilsGrp)

    def lidOnOffFollow(self, eyeController, targetUp):

        transRev = mc.createNode('multiplyDivide', n=au.prefix_name(targetUp) + 'Trans' + '_mdn')
        rotRev = mc.createNode('multiplyDivide', n=au.prefix_name(targetUp) + 'Rot' + '_mdn')

        mc.connectAttr(eyeController + '.translate', transRev + '.input1')
        mc.connectAttr(self.eyeController + '.' + self.lidFollow, transRev + '.input2X')
        mc.connectAttr(self.eyeController + '.' + self.lidFollow, transRev + '.input2Y')
        mc.connectAttr(self.eyeController + '.' + self.lidFollow, transRev + '.input2Z')

        mc.connectAttr(eyeController + '.rotate', rotRev + '.input1')
        mc.connectAttr(self.eyeController + '.' + self.lidFollow, rotRev + '.input2X')
        mc.connectAttr(self.eyeController + '.' + self.lidFollow, rotRev + '.input2Y')
        mc.connectAttr(self.eyeController + '.' + self.lidFollow, rotRev + '.input2Z')

        mc.connectAttr(transRev + '.output', targetUp + '.translate')
        mc.connectAttr(rotRev + '.output', targetUp + '.rotate')


    def cornerReverseNode(self, sideRGT, sideLFT, lidCornerCtrl, side, lidCornerName='', targetUp='', targetLow=''):
        if sideRGT in lidCornerName:
            newName = lidCornerName.replace(sideRGT, '')
        elif sideLFT in lidCornerName:
            newName = lidCornerName.replace(sideLFT, '')
        else:
            newName = lidCornerName

        transRev = mc.createNode('multiplyDivide', n=newName + 'Trans' + side + '_mdn')
        rotRev = mc.createNode('multiplyDivide', n=newName+ 'Rot' + side + '_mdn')
        mc.connectAttr(lidCornerCtrl + '.translate', transRev + '.input1')
        mc.setAttr(transRev + '.input2X', -1)

        mc.connectAttr(lidCornerCtrl + '.rotate', rotRev + '.input1')
        mc.setAttr(rotRev + '.input2Y', -1)
        mc.setAttr(rotRev + '.input2Z', -1)

        mc.connectAttr(transRev + '.output', targetUp + '.translate')
        mc.connectAttr(rotRev + '.output', targetUp + '.rotate')
        mc.connectAttr(transRev + '.output', targetLow + '.translate')
        mc.connectAttr(rotRev + '.output', targetLow + '.rotate')

    def cornerCtrl(self,matchPosOne, matchPosTwo, prefix, scale, side):
        cornerCtrl = ct.Control(match_obj_first_position=matchPosOne, match_obj_second_position=matchPosTwo,
                                prefix=prefix,
                                shape=ct.CIRCLEPLUS, groups_ctrl=['Zro', 'Offset'],
                                ctrl_size=scale * 1.0,
                                ctrl_color='blue', lock_channels=['v', 's'], side=side)

        # check position
        pos = mc.xform(cornerCtrl.control, ws=1, q=1, t=1)[0]

        # flipping the controller
        if pos < 0:
            mc.setAttr(cornerCtrl.parent_control[0] + '.scaleX', -1)

        self.control = cornerCtrl.control
        self.parentControlZro = cornerCtrl.parent_control[0]
        self.parentControlOffset = cornerCtrl.parent_control[1]

        return cornerCtrl.control, cornerCtrl.parent_control[0]

    def blinkSetup(self, sideRGT, sideLFT, eyeJnt, prefixEye, prefixEyeAim, crvUp, crvLow, scale,
                   side, upLid, lowLid, positionEyeAimCtrl, worldUpAimObject, eyeAimMainCtrl,
                   controllerBind03OffsetCtrlUp, controllerBind03OffsetCtrlLow, jointBind03GrpAllUp, jointBind03GrpAllLow,
                   jointBind03GrpOffsetLow, jointBind03GrpOffsetUp):

        # ==============================================================================================================
        #                                             EYE CONTROLLER
        # ==============================================================================================================

        eyeGrp = tf.create_parent_transform(parent_list=['Zro', 'Offset'], object=eyeJnt, match_position=eyeJnt,
                                            prefix='eye',
                                            suffix='_jnt', side=side)

        self.eyeCtrl = ct.Control(match_obj_first_position=eyeJnt,
                                  prefix=prefixEye,
                                  shape=ct.JOINTPLUS, groups_ctrl=['Zro', 'Offset'],
                                  ctrl_size=scale * 2.5,
                                  ctrl_color='turquoiseBlue', lock_channels=['v'], side=side,
                                  connection=['connectMatrixAll'])

        self.eyeController = self.eyeCtrl.control

        # ADD ATTRIBUTE
        au.add_attribute(objects=[self.eyeCtrl.control], long_name=['lidDegree'], nice_name=[' '], at="enum",
                         en='Lid Degree', channel_box=True)

        self.lidPos = au.add_attribute(objects=[self.eyeCtrl.control], long_name=['lidPos'],
                                       attributeType="float", min=0, max=1, dv=0.5, keyable=True)

        self.eyeAimFollow = au.add_attribute(objects=[self.eyeCtrl.control], long_name=['eyeAimFollow'],
                                             attributeType="float", min=0.00001, max=2, dv=1, keyable=True)

        self.lidFollow = au.add_attribute(objects=[self.eyeCtrl.control], long_name=['lidFollow'],
                                          attributeType="float", min=0, max=1, dv=1, keyable=True)

        # ==============================================================================================================
        #                                             EYE AIM
        # ==============================================================================================================
        if mc.xform(eyeJnt, q=1, ws=1, t=1)[0] > 0:
            ctrlColor ='red'
        else:
            ctrlColor='yellow'

        self.eyeAimCtrl = ct.Control(match_obj_first_position=eyeJnt,
                                     prefix=prefixEyeAim,
                                     shape=ct.LOCATOR, groups_ctrl=['Zro', 'Offset'],
                                     ctrl_size=scale * 1.0,
                                     ctrl_color=ctrlColor, lock_channels=['v', 'r', 's'], side=side)

        eyeAimCtrl = self.eyeAimCtrl.control

        getAttribute = mc.getAttr(self.eyeAimCtrl.parent_control[0] + '.translateZ')
        mc.setAttr(self.eyeAimCtrl.parent_control[0] + '.translateZ', getAttribute + (positionEyeAimCtrl * scale))

        mc.aimConstraint(self.eyeAimCtrl.control, eyeGrp[1], mo=1, weight=1, aimVector=(0, 0, 1), upVector=(0, 1, 0),
                         worldUpType="object", worldUpObject=worldUpAimObject)

        # PARENT EYE AIM TO EYE AIM MAIN CTRL
        mc.parent(self.eyeAimCtrl.parent_control[0], eyeAimMainCtrl)

        # EXPRESSION UP AND LOW FOLLOW LID CTRL
        expressionLidCtrl= "$range = {5}.{1}; " \
                            "$a = 20 /$range; " \
                            "$b = 30 /$range; " \
                            "$c = 80 /$range;" \
                            "{2}.translateX = {3}.translateX /$c + {0}.translateX /$c;" \
                           "{2}.translateY = {3}.translateY /$a + {0}.translateY /$a;" \
                           "{4}.translateX = {3}.translateX /$c + {0}.translateX /$c;" \
                           "{4}.translateY = -{3}.translateY /$b - {0}.translateY /$b;"\
            \
            .format(eyeAimCtrl,  # 0
                    self.eyeAimFollow,  # 1
                    controllerBind03OffsetCtrlUp,  # 2
                    eyeAimMainCtrl,  # 3
                    controllerBind03OffsetCtrlLow,
                    self.eyeCtrl.control
                    )

        mc.expression(s=expressionLidCtrl, n="%s%s%s" % ('lidCtrl', side, '_expr'), ae=0)

        # EXPRESSION UP AND LOW FOLLOW LID BIND
        expressionLidBind = "$range = {7}.{1}; " \
                               "$a = 30 /$range; " \
                               "$b = 8 /$range; " \
                               "$d = 12 /$range; " \
                               "$c = 60 /$range;" \
                               "if ({0}.translateY >= 0) " \
                               "{8} " \
                               "{2}.translateY = {0}.translateY /$b; " \
                               "{3}.translateY = {0}.translateY /$b;" \
                               "{9} " \
                               "else if ({0}.translateY < 0)" \
                               "{8}" \
                               "{2}.translateY = {0}.translateY /$d; " \
                               "{3}.translateY = {0}.translateY /$a;" \
                               "{9} " \
                               "{2}.translateX = {0}.translateX /$c; " \
                               "{3}.translateX = {0}.translateX /$c; " \
                               "if ({6}.translateY >= 0) " \
                               "{8}" \
                               "{4}.translateY = {6}.translateY /$b; " \
                               "{5}.translateY = {6}.translateY /$b;" \
                               "{9} " \
                               "else if ({6}.translateY < 0) " \
                               "{8}" \
                               "{4}.translateY = {6}.translateY /$d; " \
                               "{5}.translateY = {6}.translateY /$a;" \
                               "{9} " \
                               "{4}.translateX = {6}.translateX /$c; " \
                               "{5}.translateX = {6}.translateX /$c;" \
            \
            .format(eyeAimCtrl,
                    self.eyeAimFollow,
                    jointBind03GrpAllUp,
                    jointBind03GrpAllLow,
                    jointBind03GrpOffsetUp,
                    jointBind03GrpOffsetLow,
                    eyeAimMainCtrl,
                    self.eyeCtrl.control,
                    "{",
                    "}")

        mc.expression(s=expressionLidBind, n="%s%s%s" % ('lidBind', side, '_expr'), ae=0)

        # ==============================================================================================================
        #                                                   BLINK
        # ==============================================================================================================
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
        crvUpNewName = self.replacePosLFTRGT(crv=crvUp, sideRGT=sideRGT, sideLFT=sideLFT)

        # wire deform up on mid curves
        stickyMidwireDefUp = mc.wire(curveBlinkUp, dds=(0, 100 * scale), wire=curveBlinkBindMid)
        stickyMidwireDefUp[0] = mc.rename(stickyMidwireDefUp[0], (au.prefix_name(crvUpNewName) + 'Blink' + side + '_wireNode'))
        mc.setAttr(stickyMidwireDefUp[0]+'.scale[0]', 0)

        # SET TO LOW CURVE
        mc.setAttr(blinkBsn +'.%s' % upLid.deformCrv, 0)
        mc.setAttr(blinkBsn +'.%s' % lowLid.deformCrv, 1)

        mc.select(cl=1)
        # replace position LFT and RGT
        crvLowNewName = self.replacePosLFTRGT(crv=crvLow, sideRGT=sideRGT, sideLFT=sideLFT)

        stickyMidwireDefLow = mc.wire(curveBlinkLow, dds=(0, 100 * scale), wire=curveBlinkBindMid)
        stickyMidwireDefLow[0] = mc.rename(stickyMidwireDefLow[0], (au.prefix_name(crvLowNewName) + 'Blink' + side + '_wireNode'))
        mc.setAttr(stickyMidwireDefLow[0] + '.scale[0]', 0)

        # SET KEYFRAME
        mc.setDrivenKeyframe(blinkBsn +'.%s' % upLid.deformCrv,
                             cd='%s.%s' % (self.eyeCtrl.control, self.lidPos),
                             dv=0, v=1, itt='linear', ott='linear')

        mc.setDrivenKeyframe(blinkBsn +'.%s' % upLid.deformCrv,
                             cd='%s.%s' % (self.eyeCtrl.control, self.lidPos),
                             dv=1, v=0, itt='linear', ott='linear')

        mc.setDrivenKeyframe(blinkBsn + '.%s' % lowLid.deformCrv,
                             cd='%s.%s' % (self.eyeCtrl.control, self.lidPos),
                             dv=0, v=0, itt='linear', ott='linear')

        mc.setDrivenKeyframe(blinkBsn + '.%s' % lowLid.deformCrv,
                             cd='%s.%s' % (self.eyeCtrl.control, self.lidPos),
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

    def replacePosLFTRGT(self, crv, sideRGT, sideLFT):
        if sideRGT in crv:
            crvNewName = crv.replace(sideRGT, '')
        elif sideLFT in crv:
            crvNewName = crv.replace(sideLFT, '')
        else:
            crvNewName = crv

        return crvNewName