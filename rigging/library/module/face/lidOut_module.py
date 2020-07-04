from __builtin__ import reload

import maya.cmds as mc

from rigging.library.base.face import wire as wr, lid_corner as cl
from rigging.library.utils import controller as ct
from rigging.tools import AD_utils as au

reload (wr)
reload (ct)
reload (au)
reload (cl)

class LidOut:
    def __init__(self,
                 faceUtilsGrp,
                 crvUp,
                 crvLow,
                 offsetJnt02BindPos,
                 offsetJnt04BindPos,
                 directionCtrl01,
                 directionCtrl02,
                 directionCtrl03,
                 directionCtrl04,
                 directionCtrl05,
                 ctrlColor,
                 shape,
                 scale,
                 sideRGT,
                 sideLFT,
                 side,
                 eyeballJnt,
                 headUpJnt,
                 eyeCtrl,
                 cornerLip,
                 cornerLipAttr,
                 ctrlBindUp01,
                 ctrlBindUp02,
                 ctrlBindUp03,
                 ctrlBindUp04,
                 ctrlBindUp05,
                 ctrlBindLow01,
                 ctrlBindLow02,
                 ctrlBindLow03,
                 ctrlBindLow04,
                 ctrlBindLow05,
                 lidOutFollow,
                 closeLidAttr,
                 lidCornerInCtrl,
                 lidCornerOutCtrl,
                 wireUp01BindOffsetGrp,
                 wireLow01BindOffsetGrp,
                 wireUp05BindOffsetGrp,
                 wireLow05BindOffsetGrp,
                 lidOutOnOffFollowTransMdn,
                 lidOutOnOffFollowRotMdn,
                 eyeCtrlDirection,
                 suffixController
                 ):

    # ==================================================================================================================
    #                                               LID OUT CONTROLLER
    # ==================================================================================================================
        self.pos = mc.xform(eyeballJnt, ws=1, q=1, t=1)[0]

        wireUp = wr.Build(crv=crvUp, posDirectionJnt=eyeballJnt, scale=scale, sideLFT=sideLFT, sideRGT=sideRGT, side=side,
                          offsetJnt02BindPos=offsetJnt02BindPos, offsetJnt04BindPos=offsetJnt04BindPos,
                          directionCtrl01=directionCtrl01, directionCtrl02=directionCtrl02,
                          directionCtrl03=directionCtrl03, directionCtrl04=directionCtrl04,
                          directionCtrl05=directionCtrl05, suffixController=suffixController,
                          ctrlColor=ctrlColor, controllerWireLow=False, shape=shape, faceUtilsGrp=faceUtilsGrp,
                          connectWithCornerCtrl=True)

        wireLow = wr.Build(crv=crvLow, posDirectionJnt=eyeballJnt, scale=scale, sideLFT=sideLFT, sideRGT=sideRGT, side=side,
                           offsetJnt02BindPos=offsetJnt02BindPos, offsetJnt04BindPos=offsetJnt04BindPos,
                           directionCtrl01=directionCtrl01, directionCtrl02=directionCtrl02,
                           directionCtrl03=directionCtrl03, directionCtrl04=directionCtrl04,
                           directionCtrl05=directionCtrl05, suffixController=suffixController,
                           ctrlColor=ctrlColor, controllerWireLow=True, shape=shape, faceUtilsGrp=faceUtilsGrp,
                           connectWithCornerCtrl=True)

        self.lidOutUpJnt = wireUp.allJoint
        self.lidOutLowJnt = wireLow.allJoint

        # PARENT INTO THE GROUP
        # mc.parent(wireUp.grpDrvCtrl, wireUp.wireGrpDrivenOffsetCtrl)
        # mc.parent(wireLow.grpDrvCtrl, wireLow.wireGrpDrivenOffsetCtrl)
        #
        # mc.parent(wireUp.jointGrp, wireUp.setupDriverGrp)
        # mc.parent(wireLow.jointGrp, wireLow.setupDriverGrp)
        #
        # mc.parent(wireUp.bindJntGrp, wireUp.wireGrpDrivenOffsetJnt)
        # mc.parent(wireLow.bindJntGrp, wireLow.wireGrpDrivenOffsetJnt)
        #
        # mc.parent(wireUp.curvesGrp, wireUp.locatorGrp, wireUp.setupDriverGrp)
        # mc.parent(wireLow.curvesGrp, wireLow.locatorGrp, wireLow.setupDriverGrp)
        # CONNECT OFFSET CORNER LID TO CORNER LID OUT GRP
        # au.connectAttrTransRot(wireUp01BindOffsetGrp, wireUp.jointBindCorner01)
        # au.connectAttrTransRot(wireLow01BindOffsetGrp, wireLow.jointBindCorner01)
        # au.connectAttrTransRot(wireUp05BindOffsetGrp, wireUp.jointBindCorner05)
        # au.connectAttrTransRot(wireLow05BindOffsetGrp, wireLow.jointBindCorner05)


    # ==================================================================================================================
    #                                                  CORNER CONTROLLER
    # ==================================================================================================================
        # controller in corner
        lidCornerCtrl = cl.Build(upLid01=wireUp.jnt01,
                                 lowLid01=wireLow.jnt01,
                                 upLid05=wireUp.jnt05,
                                 lowLid05=wireLow.jnt05,
                                 upLidjointBind01OffsetGrp=wireUp.jointBindGrpAll01,
                                 lowLidjointBind01OffsetGrp=wireLow.jointBindGrpAll01,
                                 upLidjointBind05OffsetGrp=wireUp.jointBindGrpAll05,
                                 lowLidjointBind05OffsetGrp=wireLow.jointBindGrpAll05,
                                 scale=scale, sideRGT=sideRGT, sideLFT=sideLFT,
                                 upLidControllerBindGrpZro01=wireUp.controllerBindZro01,
                                 lowLidControllerBindGrpZro01=wireLow.controllerBindZro01,
                                 upLidControllerBindGrpZro05=wireUp.controllerBindZro05,
                                 lowLidControllerBindGrpZro05=wireLow.controllerBindZro05,
                                 prefixNameIn='cornerOutLidIn',
                                 prefixNameOut='cornerOutLidOut',
                                 side=side,
                                 ctrlShape=ct.JOINT,
                                 ctrlColor='red',
                                 lidOut=True,
                                 suffixController=suffixController)


        # ADJUSTING LID CORNER CONTROLLER TO LID OUT CORNER CONTROLLER
        self.lidInCornerFollowAttr = au.add_attribute(objects=[lidCornerInCtrl],
                                                      long_name=['lidOutFollow'],
                                                      attributeType="float", min=0, dv=1, keyable=True)
        self.cornerMultiplyLidFollow(wire=au.prefix_name(wireUp.prefixNameCrv), side=side,
                                     bindGrpSource=wireUp01BindOffsetGrp, bindGrpDestination=wireUp.jointBindCorner01,
                                     subPrefix='Bind01',
                                     ctrlCornerLid=lidCornerInCtrl,
                                     attribute=self.lidInCornerFollowAttr)

        self.cornerMultiplyLidFollow(wire=au.prefix_name(wireLow.prefixNameCrv), side=side,
                                     bindGrpSource=wireLow01BindOffsetGrp, bindGrpDestination=wireLow.jointBindCorner01,
                                     subPrefix='Bind01',
                                     ctrlCornerLid=lidCornerInCtrl,
                                     attribute=self.lidInCornerFollowAttr)

        self.lidOutCornerFollowAttr = au.add_attribute(objects=[lidCornerOutCtrl],
                                                       long_name=['lidOutFollow'],
                                                       attributeType="float", min=0, dv=1, keyable=True)

        self.cornerMultiplyLidFollow(wire=au.prefix_name(wireUp.prefixNameCrv), side=side,
                                     bindGrpSource=wireUp05BindOffsetGrp, bindGrpDestination=wireUp.jointBindCorner05,
                                     subPrefix='Bind05',
                                     ctrlCornerLid=lidCornerOutCtrl,
                                     attribute=self.lidOutCornerFollowAttr)

        self.cornerMultiplyLidFollow(wire=au.prefix_name(wireLow.prefixNameCrv), side=side,
                                     bindGrpSource=wireLow05BindOffsetGrp, bindGrpDestination=wireLow.jointBindCorner05,
                                     subPrefix='Bind05',
                                     ctrlCornerLid=lidCornerOutCtrl,
                                     attribute=self.lidOutCornerFollowAttr)

        # CONNECT LID CONTROL TO LID OUT CORNER
        # au.connectAttrTransRot(lidCornerInCtrl, lidCornerCtrl.lidCornerCtrlInOffset)
        # au.connectAttrTransRot(lidCornerOutCtrl, lidCornerCtrl.lidCornerCtrlOutOffset)

        self.cornerMultiplyLidFollow(wire=au.prefix_name(wireUp.prefixNameCrv), side=side,
                                     bindGrpSource=lidCornerInCtrl, bindGrpDestination=lidCornerCtrl.lidCornerCtrlInOffset,
                                     subPrefix='Ctrl',
                                     ctrlCornerLid=lidCornerInCtrl,
                                     attribute=self.lidInCornerFollowAttr)

        self.cornerMultiplyLidFollow(wire=au.prefix_name(wireLow.prefixNameCrv), side=side,
                                     bindGrpSource=lidCornerOutCtrl, bindGrpDestination=lidCornerCtrl.lidCornerCtrlOutOffset,
                                     subPrefix='Ctrl',
                                     ctrlCornerLid=lidCornerOutCtrl,
                                     attribute=self.lidOutCornerFollowAttr)

    # ==================================================================================================================
    #                                               LIP TO LOWER LID OUT
    # ==================================================================================================================
        # CONNECT THE BIND LID OUT TO CONTROLLER BIND LID OUT 03
        au.connect_attr_translate(wireLow.jointBindGrp03, wireLow.controllerBindZro03)

        ## CREATE FOLLOWING LID
        self.pos = mc.xform(wireLow.jointBindGrp03, ws=1, q=1, t=1)[0]

        if self.pos < 0:
            multiplier = -1
        else:
            multiplier = 1

        # MULTIPLY BY MULTIPLIER
        mdl = mc.createNode('multDoubleLinear', n=au.prefix_name(wireLow.prefixNameCrv) + 'Reverse' + side + '_mdl')
        mc.connectAttr(cornerLip+'.translateX', mdl+'.input1')
        mc.setAttr(mdl + '.input2', multiplier)

        # CREATE CONDITION
        cnd = mc.createNode('condition', n=au.prefix_name(wireLow.prefixNameCrv) + side + '_cnd')
        mc.setAttr(cnd+'.operation', 3)
        mc.setAttr(cnd + '.colorIfTrueR', 20)
        mc.setAttr(cnd + '.colorIfFalseR', 50)
        mc.connectAttr(cornerLip+'.translateY', cnd+'.firstTerm')

        # CREATE PMA FOR SUM
        transJnt03 = mc.xform(wireLow.jnt03, ws=1, q=1, t=1)
        pma = mc.createNode('plusMinusAverage', n=au.prefix_name(wireLow.prefixNameCrv) + side + '_pma')
        mc.setAttr(pma + '.input3D[0].input3Dx', transJnt03[0])
        mc.setAttr(pma + '.input3D[0].input3Dy', transJnt03[1])
        mc.setAttr(pma + '.input3D[0].input3Dz', transJnt03[2])

        # CONNECT THE ATTRIBUTE TO MDN
        mult = self.multiplyDivide(wireLowName=wireLow.prefixNameCrv+'Mult', side=side, object1X=mdl+'.output',
                            object1Y=cornerLip+'.translateY', object1Z=cornerLip+'.translateY',
                            object2X=cornerLip+'.%s'%cornerLipAttr, object2Y=cornerLip+'.%s'%cornerLipAttr,
                                   object2Z=cornerLip+'.%s'%cornerLipAttr, setAttr=False, scale=scale)

        div = self.multiplyDivide(wireLowName=wireLow.prefixNameCrv+'Div', side=side, object1X=mult + '.outputX',
                                  object1Y=mult + '.outputY', object1Z=mult + '.outputZ', operation=2,
                                  valueX=20, valueY=20, valueZ=20, setAttr=True, scale=scale)

        mc.connectAttr(cnd + '.outColorR', div + '.input2Y')
        mc.connectAttr(div + '.output', pma + '.input3D[1]')

        # CONNECT TO OBJECT
        mc.connectAttr(pma+'.output3D', wireLow.jointBindGrp03+'.translate')

    # ==================================================================================================================
    #                                         ADD FOLLOWING ATTR CONTROLLER
    # ==================================================================================================================
        # UP LID
        self.allCtrlConnectingLidOut(wire=au.prefix_name(wireUp.prefixNameCrv), side=side, ctrlBind01=ctrlBindUp01,
                                     ctrlBind02=ctrlBindUp02,
                                     ctrlBind03=ctrlBindUp03, ctrlBind04=ctrlBindUp04, ctrlBind05=ctrlBindUp05,
                                     lidOutFollow=lidOutFollow, drvBindOffset01=wireUp.jointBindOffset01,
                                     drvBindOffset02=wireUp.jointBindOffset02, drvBindOffset03=wireUp.jointBindOffset03,
                                     drvBindOffset04=wireUp.jointBindOffset04, drvBindOffset05=wireUp.jointBindOffset05,
                                     closeLidAttr=closeLidAttr, upLid=True)
        # LOW LID
        self.allCtrlConnectingLidOut(wire=au.prefix_name(wireLow.prefixNameCrv), side=side, ctrlBind01=ctrlBindLow01,
                                     ctrlBind02=ctrlBindLow02,
                                     ctrlBind03=ctrlBindLow03, ctrlBind04=ctrlBindLow04, ctrlBind05=ctrlBindLow05,
                                     lidOutFollow=lidOutFollow, drvBindOffset01=wireLow.jointBindOffset01,
                                     drvBindOffset02=wireLow.jointBindOffset02, drvBindOffset03=wireLow.jointBindOffset03,
                                     drvBindOffset04=wireLow.jointBindOffset04, drvBindOffset05=wireLow.jointBindOffset05,
                                     closeLidAttr=closeLidAttr, upLid=False)

        # PARENT TO GROUP
        mc.parent(wireUp.jointGrp, wireLow.jointGrp, headUpJnt)
        mc.parent(wireUp.ctrlDriverGrp, wireLow.ctrlDriverGrp, lidCornerCtrl.inParentGrpZro,
                  lidCornerCtrl.outParentGrpZro, eyeCtrl)

    # ==================================================================================================================
    #                                         ROTATE THE OFFSET LID OUT BIND GRP
    # ==================================================================================================================

        for up, low in zip(wireUp.parentLocGrpOffset, wireLow.parentLocGrpOffset):
            # ROTATE THE EYE GROUP
            if self.pos >= 0:
                mc.setAttr(up + '.rotateY', eyeCtrlDirection)
                mc.setAttr(low + '.rotateY', eyeCtrlDirection)

            else:
                mc.setAttr(up+ '.rotateY', eyeCtrlDirection * -1)
                mc.setAttr(low + '.rotateY', eyeCtrlDirection * -1)

    # ==================================================================================================================
    #                               CONNECT EYE CONTROLLER TO EVERY JOINT LID OUT CURVE
    # ==================================================================================================================
        for up, low in zip(wireUp.allJoint, wireLow.allJoint):
            mc.connectAttr(lidOutOnOffFollowTransMdn+'.output', up+'.translate')
            mc.connectAttr(lidOutOnOffFollowTransMdn+'.output', low+'.translate')
            mc.connectAttr(lidOutOnOffFollowRotMdn+'.output', up+'.rotate')
            mc.connectAttr(lidOutOnOffFollowRotMdn+'.output', low+'.rotate')
            au.connect_attr_scale(eyeCtrl, up)
            au.connect_attr_scale(eyeCtrl, low)


    # ==================================================================================================================
    #                                                   FUNCTION
    # ==================================================================================================================
    def cornerMultiplyLidFollow(self, wire, side, bindGrpSource, bindGrpDestination, subPrefix, ctrlCornerLid, attribute):
        trans = mc.createNode('multiplyDivide', n=wire + 'TransCorner' + subPrefix + side + '_mdn')
        rot = mc.createNode('multiplyDivide', n=wire + 'RotCorner' + subPrefix + side + '_mdn')

        mc.connectAttr(bindGrpSource + '.translate', trans + '.input1')
        mc.connectAttr(ctrlCornerLid + '.%s' % attribute, trans + '.input2X')
        mc.connectAttr(ctrlCornerLid + '.%s' % attribute, trans + '.input2Y')
        mc.connectAttr(ctrlCornerLid + '.%s' % attribute, trans + '.input2Z')

        mc.connectAttr(trans+'.output', bindGrpDestination+'.translate')

        mc.connectAttr(bindGrpSource + '.rotate', rot + '.input1')
        mc.connectAttr(ctrlCornerLid + '.%s' % attribute, rot + '.input2X')
        mc.connectAttr(ctrlCornerLid + '.%s' % attribute, rot + '.input2Y')
        mc.connectAttr(ctrlCornerLid + '.%s' % attribute, rot + '.input2Z')

        mc.connectAttr(rot+'.output', bindGrpDestination+'.rotate')

    def allCtrlConnectingLidOut(self, wire, side, ctrlBind01, ctrlBind02, ctrlBind03, ctrlBind04, ctrlBind05,
                                lidOutFollow, drvBindOffset01, drvBindOffset02, drvBindOffset03,
                                drvBindOffset04, drvBindOffset05, closeLidAttr, upLid):
        if self.pos > 0:
            self.connectingLidToLidOut(wire=wire, side=side, ctrlBind=ctrlBind01, numCtrl='01',
                                       lidOutFollowAttr=lidOutFollow,
                                       middleBindCtrl=False, drvBindOffset=drvBindOffset01, closeLidAttr=None,
                                       upLid=upLid, reverseTx=True)
            self.connectingLidToLidOut(wire=wire, side=side, ctrlBind=ctrlBind02, numCtrl='02',
                                       lidOutFollowAttr=lidOutFollow,
                                       middleBindCtrl=False, drvBindOffset=drvBindOffset02, closeLidAttr=None,
                                       upLid=upLid, reverseTx=True)
            self.connectingLidToLidOut(wire=wire, side=side, ctrlBind=ctrlBind04, numCtrl='04',
                                       lidOutFollowAttr=lidOutFollow,
                                       middleBindCtrl=False, drvBindOffset=drvBindOffset04, closeLidAttr=None,
                                       upLid=upLid, reverseTx=False)
            self.connectingLidToLidOut(wire=wire, side=side, ctrlBind=ctrlBind05, numCtrl='05',
                                       lidOutFollowAttr=lidOutFollow,
                                       middleBindCtrl=False, drvBindOffset=drvBindOffset05, closeLidAttr=None,
                                       upLid=upLid, reverseTx=False)
        else:
            self.connectingLidToLidOut(wire=wire, side=side, ctrlBind=ctrlBind01, numCtrl='01',
                                       lidOutFollowAttr=lidOutFollow,
                                       middleBindCtrl=False, drvBindOffset=drvBindOffset01, closeLidAttr=None,
                                       upLid=upLid, reverseTx=False)
            self.connectingLidToLidOut(wire=wire, side=side, ctrlBind=ctrlBind02, numCtrl='02',
                                       lidOutFollowAttr=lidOutFollow,
                                       middleBindCtrl=False, drvBindOffset=drvBindOffset02, closeLidAttr=None,
                                       upLid=upLid, reverseTx=False)
            self.connectingLidToLidOut(wire=wire, side=side, ctrlBind=ctrlBind04, numCtrl='04',
                                       lidOutFollowAttr=lidOutFollow,
                                       middleBindCtrl=False, drvBindOffset=drvBindOffset04, closeLidAttr=None,
                                       upLid=upLid, reverseTx=True)
            self.connectingLidToLidOut(wire=wire, side=side, ctrlBind=ctrlBind05, numCtrl='05',
                                       lidOutFollowAttr=lidOutFollow,
                                       middleBindCtrl=False, drvBindOffset=drvBindOffset05, closeLidAttr=None,
                                       upLid=upLid, reverseTx=True)

        self.connectingLidToLidOut(wire=wire, side=side, ctrlBind=ctrlBind03, numCtrl='03', lidOutFollowAttr=lidOutFollow,
                                   middleBindCtrl=True, drvBindOffset=drvBindOffset03, closeLidAttr=closeLidAttr, upLid=upLid,
                                   reverseTx = False)

    def connectingLidToLidOut(self, wire, side, ctrlBind, numCtrl, lidOutFollowAttr, middleBindCtrl, drvBindOffset, closeLidAttr, upLid, reverseTx):

        if middleBindCtrl:
            if upLid:
                mdlCloseLid = self.closeLid(wire, side, ctrlBind, numCtrl=numCtrl, subPrefix='RevCloseLid',
                                            attribute=closeLidAttr, value=-0.125)
                mdlTy = self.closeLid(wire, side, ctrlBind, numCtrl=numCtrl, subPrefix='RevTy', attribute='translateY',
                                      value=1)

            else:
                mdlCloseLid = self.closeLid(wire, side, ctrlBind, numCtrl=numCtrl, subPrefix='RevCloseLid',
                                            attribute=closeLidAttr, value=0.125)
                mdlTy = self.closeLid(wire, side, ctrlBind, numCtrl=numCtrl, subPrefix='RevTy', attribute='translateY',
                                      value=-1)

            mdnTy = self.multiplyDivideLid(wireLowName=wire, side=side, object1X=mdlCloseLid + '.output', object2X=ctrlBind + '.%s' % lidOutFollowAttr,
                                           object1Y=mdlTy + '.output', object2Y=ctrlBind + '.%s' % lidOutFollowAttr, subPrefix='Ty', numCtrl=numCtrl, twoAttr=True)

            cndCloseLid = self.condition(wire, subPrefix='CloseLid', objCondition=ctrlBind + '.%s' % closeLidAttr,
                                         objFirst=mdnTy+'.outputX', side=side, numCtrl=numCtrl, operation=5)

            cndTy = self.condition(wire, subPrefix='Ty', objCondition=ctrlBind + '.translateY',
                                   objFirst=mdnTy+'.outputY', side=side, numCtrl=numCtrl,  operation=3)

            pma = self.plusMinusAvg(wire, subPrefix='CloseLidTy', side=side, objectFirst=cndCloseLid+'.outColorR',
                                    objectSecond=cndTy+'.outColorR', numCtrl=numCtrl, )
            mc.connectAttr(pma+'.output1D',  drvBindOffset+'.translateY')

        else:
            if upLid:
                mdlTy = self.closeLid(wire, side, ctrlBind, numCtrl=numCtrl, subPrefix='RevTy', attribute='translateY',
                                      value=1)

            else:
                mdlTy = self.closeLid(wire, side, ctrlBind, numCtrl=numCtrl, subPrefix='RevTy', attribute='translateY',
                                      value=-1)

            mdnTyDirect = self.multiplyDivideLid(wireLowName=wire, subPrefix='DirectTy', side=side, object1X=mdlTy + '.output',
                                                 object2X=ctrlBind + '.%s' % lidOutFollowAttr, numCtrl=numCtrl, twoAttr=False)

            cndTyDirect = self.condition(wire, subPrefix='Ty', objCondition=ctrlBind + '.translateY',
                                   objFirst=mdnTyDirect+'.outputX', side=side, numCtrl=numCtrl,  operation=3)

            mc.connectAttr(cndTyDirect+'.outColorR',  drvBindOffset+'.translateY')

        if reverseTx:
            revTx = self.closeLid(wire, side, ctrlBind, numCtrl=numCtrl, subPrefix='RevTx',
                                  attribute='translateX',
                                  value=-1)

            mdnTx = self.multiplyDivideLid(wireLowName=wire, subPrefix='Tx', side=side, object1X=revTx + '.output',
                                           object2X=ctrlBind + '.%s' % lidOutFollowAttr, numCtrl=numCtrl, twoAttr=False)
        else:
            mdnTx = self.multiplyDivideLid(wireLowName=wire, subPrefix='Tx', side=side, object1X=ctrlBind + '.translateX',
                                           object2X=ctrlBind + '.%s' % lidOutFollowAttr, numCtrl=numCtrl, twoAttr=False)

        mc.connectAttr(mdnTx + '.outputX', drvBindOffset + '.translateX')

    def closeLid(self, wire, side, ctrlBind03, subPrefix, numCtrl, attribute, value):
        mdl = mc.createNode('multDoubleLinear', n=wire +subPrefix +numCtrl+ side+'_mdl')
        mc.setAttr(mdl+'.input2', value)
        mc.connectAttr(ctrlBind03 +'.%s' % attribute, mdl + '.input1')
        return mdl

    def plusMinusAvg(self, wire, subPrefix, side, objectFirst, numCtrl, objectSecond):
        pma = mc.createNode('plusMinusAverage', n=wire +subPrefix+numCtrl + side+'_pma')
        mc.connectAttr(objectFirst, pma+'.input1D[0]')
        mc.connectAttr(objectSecond, pma+'.input1D[1]')
        return pma

    def condition(self, wire, subPrefix, objCondition, objFirst, side, numCtrl, operation):
        cnd = mc.createNode('condition', n=wire +subPrefix+ numCtrl+side + '_cnd')
        mc.connectAttr(objCondition, cnd+'.firstTerm')
        mc.connectAttr(objFirst, cnd+'.colorIfTrueR')
        mc.setAttr(cnd+'.operation', operation)
        mc.setAttr(cnd+'.colorIfFalseR', 0)
        return cnd

    def multiplyDivideLid(self,wireLowName, side, object1X, object2X, numCtrl, subPrefix, object1Y=None, object2Y=None, operation=1, twoAttr=True):
        mdn = mc.createNode('multiplyDivide', n=wireLowName + subPrefix+ numCtrl+side + '_mdn')
        mc.connectAttr(object1X, mdn+'.input1X')
        mc.connectAttr(object2X, mdn + '.input2X')
        mc.setAttr(mdn+'.operation', operation)
        if twoAttr:
            mc.connectAttr(object1Y, mdn + '.input1Y')
            mc.connectAttr(object2Y, mdn + '.input2Y')

        return mdn

    def multiplyDivide(self,wireLowName, side, scale, object1X, object1Y, object1Z, operation=1, valueX=None,
                       valueY=None, valueZ=None, object2X=None, object2Y=None, object2Z=None, setAttr=True):

        mdn = mc.createNode('multiplyDivide', n=au.prefix_name(wireLowName) + side + '_mdn')
        mc.connectAttr(object1X, mdn+'.input1X')
        mc.connectAttr(object1Y, mdn+'.input1Y')
        mc.connectAttr(object1Z, mdn+'.input1Z')
        mc.setAttr(mdn+'.operation', operation)

        if setAttr:
            mc.setAttr(mdn+'.input2X', valueX*scale)
            mc.setAttr(mdn+'.input2Y', valueY*scale)
            mc.setAttr(mdn+'.input2Z', valueZ*scale)
        else:
            mc.connectAttr(object2X, mdn + '.input2X')
            mc.connectAttr(object2Y, mdn + '.input2Y')
            mc.connectAttr(object2Z, mdn + '.input2Z')

        return mdn



