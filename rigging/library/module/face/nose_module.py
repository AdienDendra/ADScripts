from __builtin__ import reload

import maya.cmds as mc

from rigging.library.base.face import wire as wr, nose as ns
from rigging.library.utils import controller as ct
from rigging.library.utils import transform as tf
from rigging.tools import AD_utils as au

reload (ct)
reload (tf)
reload (au)
reload (ns)
reload (wr)

class Nose:
    def __init__(self,
                 faceUtilsGrp,
                 columellaJnt,
                 columellaPrefix,
                 crvNose,
                 offsetJnt02BindPos,
                 offsetJnt04BindPos,
                 directionCtrl01,
                 directionCtrl02,
                 directionCtrl03,
                 directionCtrl04,
                 directionCtrl05,
                 ctrlColor,
                 noseJnt,
                 noseUpJnt,
                 positionMouthCtrl,
                 headCtrlGimbal,
                 headUpCtrlGimbal,
                 headJnt,
                 shape,
                 scale,
                 sideRGT,
                 sideLFT,
                 lipCornerCtrlLFT,
                 lipCornerCtrlRGT,
                 nostrilAttrCtrlLFT,
                 nostrilAttrCtrlRGT,
                 upLipControllerAll,
                 mouthCtrl,
                 noseFollowMouthValue,
                 upLipAllCtrlZroGrp,
                 jawCtrl,
                 suffixController
                 ):


    # ==================================================================================================================
    #                                               NOSE CONTROLLER
    # ==================================================================================================================
        columellaCtrl = ns.Build(columellaJnt, columellaPrefix, suffixController, scale)

        wire = wr.Build(crv=crvNose, posDirectionJnt=noseJnt, scale=scale, sideLFT=sideLFT, sideRGT=sideRGT, side='',
                        offsetJnt02BindPos=offsetJnt02BindPos, offsetJnt04BindPos=offsetJnt04BindPos,
                        directionCtrl01=directionCtrl01, directionCtrl02=directionCtrl02,
                        directionCtrl03=directionCtrl03, directionCtrl04=directionCtrl04, directionCtrl05=directionCtrl05,
                        ctrlColor=ctrlColor, controllerWireLow=False, shape=shape, faceUtilsGrp=faceUtilsGrp, connectWithCornerCtrl=False,
                        suffixController=suffixController)


        self.controllerNose01LFT = wire.controllerBind05
        self.controllerNose01RGT = wire.controllerBind01
        self.controllerNose03 = wire.controllerBind03

        controllerBind01LFT = wire.controllerBind05
        controllerBind01RGT = wire.controllerBind01
        self.allJoint = wire.allJoint
        self.noseControllerGrp = wire.ctrlDriverGrp

        # ADD ATTRIBUTE LFT
        au.add_attribute(objects=[controllerBind01LFT], long_name=['cheekUpSetup'], nice_name=[' '], at="enum",
                         en='Cheek Up Setup', channel_box=True)
        self.pullForwardLFT = au.add_attribute(objects=[controllerBind01LFT], long_name=['pullForward'],
                                               attributeType="float", min=0.001, max=10, dv=1, keyable=True)

        self.pushUpwardLFT = au.add_attribute(objects=[controllerBind01LFT], long_name=['pushUpward'],
                                              attributeType="float", min=0.001, max=10, dv=1, keyable=True)

        # ADD ATTRIBUTE RGT
        au.add_attribute(objects=[controllerBind01RGT], long_name=['cheekUpSetup'], nice_name=[' '], at="enum",
                         en='Cheek Up Setup', channel_box=True)
        self.pullForwardRGT = au.add_attribute(objects=[controllerBind01RGT], long_name=['pullForward'],
                                               attributeType="float", min=0.001, max=10, dv=1, keyable=True)

        self.pushUpwardRGT = au.add_attribute(objects=[controllerBind01RGT], long_name=['pushUpward'],
                                              attributeType="float", min=0.001, max=10, dv=1, keyable=True)


        # ADD NOSE CONTROLLER
        noseController = ct.Control(match_obj_first_position=noseJnt,
                                    prefix='nose',
                                    shape=ct.LOCATOR, groups_ctrl=['Zro', 'Offset'],
                                    ctrl_size=scale * 0.25,
                                    ctrl_color='turquoiseBlue', lock_channels=['v'])

        self.noseCtrl = noseController.control
        self.noseCtrlParentOffset = noseController.parent_control[1]
        self.noseCtrlParentZro = noseController.parent_control[0]

        # ADD ATTRIBUTE NOSE
        au.add_attribute(objects=[noseController.control], long_name=['weightSkinInfluence'], nice_name=[' '], at="enum",
                         en='Weight Influence', channel_box=True)

        self.mouthWeightUD = au.add_attribute(objects=[noseController.control], long_name=['upDown'],
                                              attributeType="float", min=0, dv=1, keyable=True)
        self.mouthWeightSS = au.add_attribute(objects=[noseController.control], long_name=['squashStretch'],
                                              attributeType="float", min=0, dv=1, keyable=True)
        self.mouthWeightLR = au.add_attribute(objects=[noseController.control], long_name=['leftRight'],
                                              attributeType="float", min=0, dv=1, keyable=True)
        # OFFSET POSITION PARENT GRP NOSE
        tZValue = mc.getAttr(self.noseCtrlParentZro+'.translateZ')
        mc.setAttr(self.noseCtrlParentZro+'.translateZ', tZValue+(positionMouthCtrl*0.5*scale))

        # CREATE PMA FOR EXPRESSION
        self.noseCtrlTransPMA = mc.createNode('plusMinusAverage', n='noseWeightToMouthTrans_pma')
        self.noseCtrlRotPMA = mc.createNode('plusMinusAverage', n='noseWeightToMouthRot_pma')
        self.noseCtrlSclPMA = mc.createNode('plusMinusAverage', n='noseWeightToMouthScl_pma')

        # CONNECT ATTRIBUTE NOSE CTRL TO GRP OFFSET JOINT DRIVEN AND CONTROLLER
        mc.connectAttr(self.noseCtrl+'.translate', self.noseCtrlTransPMA +'.input3D[0]')
        mc.connectAttr(self.noseCtrl+'.rotate', self.noseCtrlRotPMA +'.input3D[0]')
        mc.connectAttr(self.noseCtrl+'.scale', self.noseCtrlSclPMA +'.input3D[0]')


        mc.connectAttr(self.noseCtrlRotPMA+'.output3D', wire.wireGrpDrivenOffsetJnt+'.rotate')
        # au.connectAttrRot(self.noseCtrl, noseGrpDrivenOffsetJnt)
        mc.connectAttr(self.noseCtrlSclPMA+'.output3D',  wire.wireGrpDrivenOffsetJnt+'.scale')

        mc.connectAttr(self.noseCtrlTransPMA+'.output3D', wire.wireGrpDrivenOffsetCtrl+'.translate')
        mc.connectAttr(self.noseCtrlRotPMA+'.output3D', wire.wireGrpDrivenOffsetCtrl+'.rotate')
        # au.connectAttrRot(self.noseCtrl, noseGrpDrivenOffsetCtrl)
        mc.connectAttr(self.noseCtrlSclPMA+'.output3D', wire.wireGrpDrivenOffsetCtrl+'.scale')

        mc.connectAttr(self.noseCtrlTransPMA+'.output3D', columellaCtrl.grpColumellaJnt[1]+'.translate')
        mc.connectAttr(self.noseCtrlRotPMA+'.output3D', columellaCtrl.grpColumellaJnt[1]+'.rotate')
        # au.connectAttrRot(self.noseCtrl, columellaCtrl.grpColumellaJnt[1])
        mc.connectAttr(self.noseCtrlSclPMA+'.output3D', columellaCtrl.grpColumellaJnt[1]+'.scale')


        # CONNECT ALL PART NOSE JOINT
        for i in wire.allJoint:
            mc.connectAttr(self.noseCtrlTransPMA + '.output3D', i + '.translate')
            mc.connectAttr(self.noseCtrlRotPMA + '.output3D', i + '.rotate')
            # au.connectAttrRot(self.noseCtrl, i)
            mc.connectAttr(self.noseCtrlSclPMA + '.output3D', i + '.scale')
            # au.connectAttrObject(self.noseCtrl, i)

        # PARENT INTO THE GROUP
        mc.parent(columellaCtrl.columellaParentCtrlZro, wire.wireGrpDrivenOffsetCtrl)
        mc.parent(wire.jointGrp, headJnt)
        mc.parent(wire.ctrlDriverGrp,  self.noseCtrlParentZro, headCtrlGimbal)

        # SET THE VALUE FOR EXPRESSION
        translateXMouth = noseFollowMouthValue*24.0
        translateXLip = noseFollowMouthValue*24.0
        translateXJaw = noseFollowMouthValue*6.0
        translateYMouth = noseFollowMouthValue*12.0
        translateYLip = noseFollowMouthValue*12.0
        translateYJaw = noseFollowMouthValue*(-12.0)

        scaleXMouth = noseFollowMouthValue*48.0
        scaleXLip = noseFollowMouthValue*24.0
        scaleXJaw = noseFollowMouthValue*(-6.0)
        scaleYMouth = noseFollowMouthValue*48.0
        scaleYLip = noseFollowMouthValue*(-24.0)
        scaleYJaw = noseFollowMouthValue*(-6.0)

        rotateYMouth = noseFollowMouthValue*12.0
        rotateYLip = noseFollowMouthValue*24.0
        rotateYJaw = noseFollowMouthValue*0.1

        rotateZMouth = noseFollowMouthValue*12.0
        rotateZLip = noseFollowMouthValue*12.0
        rotateZJaw = noseFollowMouthValue*(-0.1)

        # ADD NOSE UP CONTROLLER
        noseUpController = ct.Control(match_obj_first_position=noseUpJnt,
                                      prefix='noseUp',
                                      shape=ct.JOINT, groups_ctrl=['Zro'],
                                      ctrl_size=scale * 0.05,
                                      ctrl_color='turquoiseBlue', lock_channels=['v'])

        self.noseUpControllerGrp = noseUpController.parent_control[0]

        grpNoseUpJnt = tf.create_parent_transform(parent_list=['Zro'], object=noseUpJnt, match_position=noseUpJnt,
                                                  prefix='noseUp', suffix='_jnt')

        au.connect_attr_object(noseUpController.control, noseUpJnt)
        mc.parent(noseUpController.parent_control[0], headUpCtrlGimbal)

        # ==============================================================================================================
        #                                            NOSTRIL SETUP
        # ==============================================================================================================
        jointBind05Grp = wire.jointBindGrp05
        jointBind01Grp = wire.jointBindGrp01
        getAttrGrpZroBindNostrilLFT = mc.getAttr(jointBind05Grp + '.translate')[0]
        getAttrGrpZroBindNostrilRGT = mc.getAttr(jointBind01Grp + '.translate')[0]
        getAttrlipUpAllCtrlZroGrp = mc.getAttr(upLipAllCtrlZroGrp + '.translate')[0]

        getAttrLipUpAllCtrlZroGrpTy = getAttrlipUpAllCtrlZroGrp[1]
        # NOSTRIL LEFT
        self.nostrilSetup(side=sideLFT, controller=lipCornerCtrlLFT,
                          attributeOffset=nostrilAttrCtrlLFT,
                          noseBindParentZro=jointBind05Grp,
                          getAttrTxCtrlGrpZroNostril=getAttrGrpZroBindNostrilLFT[0],
                          lipUpAllCtrl=upLipControllerAll,
                          mouthCtrl=mouthCtrl, multiplier=1,
                          getAttrTyCtrlGrpZroNostril=getAttrGrpZroBindNostrilLFT[1],
                          getAttrTzCtrlGrpZroNostril=getAttrGrpZroBindNostrilLFT[2],
                          valueMouth=noseFollowMouthValue*24.0,
                          valueMouthThreeTimes=noseFollowMouthValue * 36.0,
                          valueUpperLip=noseFollowMouthValue*12.0,
                          jawCtrl=jawCtrl,
                          valueUpperLipMinHalf=noseFollowMouthValue * (-6.0),
                          valueUpperLipMaxOrMinYHalf=noseFollowMouthValue * 6.0,
                          valueCornerLip=noseFollowMouthValue * 6.0)
        # NOSTRIL RIGHT
        self.nostrilSetup(side=sideRGT, controller=lipCornerCtrlRGT,
                          attributeOffset=nostrilAttrCtrlRGT,
                          noseBindParentZro=jointBind01Grp,
                          getAttrTxCtrlGrpZroNostril=getAttrGrpZroBindNostrilRGT[0],
                          lipUpAllCtrl=upLipControllerAll,
                          mouthCtrl=mouthCtrl, multiplier=-1,
                          getAttrTyCtrlGrpZroNostril=getAttrGrpZroBindNostrilRGT[1],
                          getAttrTzCtrlGrpZroNostril=getAttrGrpZroBindNostrilRGT[2],
                          valueMouth=noseFollowMouthValue*24.0,
                          valueMouthThreeTimes=noseFollowMouthValue * 36.0,
                          valueUpperLip=noseFollowMouthValue*12.0,
                          jawCtrl=jawCtrl,
                          valueUpperLipMinHalf=noseFollowMouthValue * 6.0,
                          valueUpperLipMaxOrMinYHalf=noseFollowMouthValue * (-6.0),
                          valueCornerLip=noseFollowMouthValue * 6.0)

    # ==================================================================================================================
    #                                                   NOSE SETUP
    # ==================================================================================================================

        rangeUD = self.noseCtrl+'.%s'%self.mouthWeightUD
        rangeSS = self.noseCtrl+'.%s'%self.mouthWeightSS
        rangeLR = self.noseCtrl+'.%s'%self.mouthWeightLR

        # TRANSLATE
        self.noseSetup(mouthCtrl, jawCtrl, upLipControllerAll,
                       translateX='translateX', translateY='translateY',
                       rotateXJaw='rotateY', rotateYJaw='rotateX',
                       firstValueX=translateXLip, secondValueX=translateXMouth,
                       firstValueY=translateYLip, secondValueY=translateYMouth,
                       firstOperationX=2, secondOperationX=2,
                       firstOperationY=2, secondOperationY=2,
                       operationSumX=1, operationSumY=1,
                       radValueX=0.0174533, radValueY=0.0174533,
                       ctrlValueJawX=translateXJaw, ctrlValueJawY=translateYJaw,
                       operationSumJawX=1, operationSumJawY=1, prefixX='TransX',
                       prefixY='TransY', divide=True, range=rangeUD,
                       prefix='Trans', targetObject=self.noseCtrlTransPMA,
                       targetX='input3Dx', targetY='input3Dy')
        # SCALE
        self.noseSetup(mouthCtrl, jawCtrl, upLipControllerAll,
                       translateX='translateY', translateY='translateY',
                       rotateXJaw='rotateX', rotateYJaw='rotateX',
                       firstValueX=scaleXLip, secondValueX=scaleXMouth,
                       firstValueY=scaleYLip, secondValueY=scaleYMouth,
                       firstOperationX=2, secondOperationX=2,
                       firstOperationY=2, secondOperationY=2,
                       operationSumX=1, operationSumY=2, radValueX=0.0174533, radValueY=0.0174533,
                       ctrlValueJawX=scaleXJaw, ctrlValueJawY=scaleYJaw,
                       operationSumJawX=1, operationSumJawY=2, prefixX='SclX',
                       prefixY='SclY', divide=True, range=rangeSS,
                       prefix='Scl', targetObject=self.noseCtrlSclPMA,
                       targetX='input3Dx', targetY='input3Dy')
        # ROTATE
        self.noseSetup(mouthCtrl, jawCtrl, upLipControllerAll,
                       translateX='translateX', translateY='translateX',
                       rotateXJaw='rotateY', rotateYJaw='rotateY',
                       firstValueX=rotateYLip, secondValueX=rotateYMouth,
                       firstValueY=rotateZLip, secondValueY=rotateZMouth,
                       firstOperationX=1, secondOperationX=1,
                       firstOperationY=1, secondOperationY=1,
                       operationSumX=1, operationSumY=1, radValueX=rotateYJaw, radValueY=rotateZJaw,
                       ctrlValueJawX=None, ctrlValueJawY=None,
                       operationSumJawX=1, operationSumJawY=1, prefixX='RotY',
                       prefixY='RotZ', divide=False, range=rangeLR,
                       prefix='Rot', targetObject=self.noseCtrlRotPMA,
                       targetX='input3Dy', targetY='input3Dz')

    # ==================================================================================================================
    #                                                 FUNCTION NOSE AND NOSTRIL
    # ==================================================================================================================

    def noseSetup(self,mouthCtrl, jawCtrl, upLipControllerAll, translateX, translateY, rotateXJaw, rotateYJaw, firstValueX, secondValueX, firstValueY,
                  secondValueY, firstOperationX, secondOperationX, firstOperationY, secondOperationY, operationSumX, operationSumY,
                  radValueX, radValueY, ctrlValueJawX, ctrlValueJawY, operationSumJawX, operationSumJawY, prefixX, prefixY, divide, range, prefix,
                  targetObject, targetX, targetY):

        X = self.noseWeight(secondCtrl=mouthCtrl + '.%s' % translateX, firstCtrl=upLipControllerAll + '.%s' % translateX,
                            secondValue=secondValueX, firstValue=firstValueX,
                            secondOperation=secondOperationX, firstOperation=firstOperationX, operationSum=operationSumX,
                            prefix=prefixX)

        jawX = self.noseAdditional(prefix='Jaw' + prefixX, ctrl=jawCtrl + '.%s' % rotateXJaw,
                                   noseWeightPMA=X + '.output1D',
                                   operationSum=operationSumJawX, radValue=radValueX, ctrlValue=ctrlValueJawX, divide=divide)

        Y = self.noseWeight(secondCtrl=mouthCtrl + '.%s' % translateY, firstCtrl=upLipControllerAll + '.%s' % translateY,
                            secondValue=secondValueY, firstValue=firstValueY,
                            secondOperation=secondOperationY, firstOperation=firstOperationY, operationSum=operationSumY,
                            prefix=prefixY)

        jawY = self.noseAdditional(prefix='Jaw' + prefixY, ctrl=jawCtrl + '.%s' % rotateYJaw,
                                   noseWeightPMA=Y + '.output1D',
                                   operationSum=operationSumJawY, radValue=radValueY, ctrlValue=ctrlValueJawY, divide=divide)

        rangeGreat = self.multiplyToRange(range=range, nosePMAX=X + '.output1D',
                                          nosePMAY=Y + '.output1D',
                                          prefix=prefix, nameExpr='Great')

        rangeLess = self.multiplyToRange(range=range, nosePMAX=jawX + '.output1D',
                                         nosePMAY=jawY + '.output1D',
                                         prefix=prefix, nameExpr='Less')

        # CONDITION
        self.conditionNoseWeight(jawCtrl=jawCtrl, rangeGreat=rangeGreat, rangeLess=rangeLess,
                                 targetFirst= targetObject +'.input3D[1]'+'.%s' % targetX,
                                 targetSecond=targetObject + '.input3D[1]'+'.%s' % targetY,
                                 prefix=prefix)

    def nostrilSetup(self, side, controller, attributeOffset, noseBindParentZro,
                     getAttrTxCtrlGrpZroNostril,
                     lipUpAllCtrl, mouthCtrl, multiplier, getAttrTyCtrlGrpZroNostril,
                     getAttrTzCtrlGrpZroNostril,
                     valueMouth, valueMouthThreeTimes, valueUpperLip, jawCtrl, valueCornerLip, valueUpperLipMaxOrMinYHalf, valueUpperLipMinHalf):

        range = controller + '.%s' % attributeOffset
        multRevNostrilTransX = self.mdlSetAttr(name='nostrilWeight', prefix='TransX', nameExpr='', side=side,
                                               input1=controller + '.translateX ', input2Set=multiplier)
        multRevNostrilTransXOut = multRevNostrilTransX + '.output'
        # TRANS X
        transXGreat, transXLess = self.nostril(range, mouthCtrl, lipUpAllCtrl,jawCtrl, valueMouthThreeTimes, valueUpperLip, valueCornerLip,
                    valueUpperLipMinHalf=valueUpperLipMinHalf, side=side, controller= multRevNostrilTransXOut,
                    translate='translateX', rotate='rotateX', prefix='TransX',
                    prefixJaw='JawTransX', getAttrCtrlGrpZroNostril=getAttrTxCtrlGrpZroNostril,  operation=1)

        # TRANS Y
        transYGreat, transYLess = self.nostril(range, mouthCtrl, lipUpAllCtrl, jawCtrl, valueMouth, valueUpperLip, valueCornerLip,
                    valueUpperLipMinHalf=valueUpperLipMaxOrMinYHalf, side=side, controller=controller+'.translateY',
                    translate='translateY', rotate='rotateY', prefix='TransY',
                    prefixJaw='JawTransY', getAttrCtrlGrpZroNostril=getAttrTyCtrlGrpZroNostril,  operation=1)

        # TRANS Z
        transZGreat, transZLess = self.nostril(range, mouthCtrl, lipUpAllCtrl, jawCtrl, valueMouth, valueUpperLip, valueCornerLip,
                    valueUpperLipMinHalf=valueUpperLipMinHalf, side=side, controller=controller+'.translateZ',
                    translate='translateZ', rotate='rotateZ', prefix='TransZ',
                    prefixJaw='JawTransZ', getAttrCtrlGrpZroNostril=getAttrTzCtrlGrpZroNostril,  operation=1)

        self.conditionNostrilWeight(jawCtrl,
                                    rangeGreatX=transXGreat, rangeLessX=transXLess,
                                    rangeGreatY=transYGreat, rangeLessY=transYLess,
                                    rangeGreatZ=transZGreat, rangeLessZ=transZLess,
                                    target=noseBindParentZro, side=side)

    def nostril(self, range, mouthCtrl, lipUpAllCtrl, jawCtrl, valueMouth, valueUpperLip, valueCornerLip, valueUpperLipMinHalf, side, controller,
                translate, rotate, prefix, prefixJaw, getAttrCtrlGrpZroNostril,  operation):

        transNostril = self.noseWeight(thirdCtrl=mouthCtrl + '.%s' % translate,
                                       secondCtrl=lipUpAllCtrl + '.%s' % translate,
                                       firstCtrl=controller,
                                       thirdValue=valueMouth, secondValue=valueUpperLip, firstValue=valueCornerLip,
                                       secondOperation=2, firstOperation=2, operationSum=1, name='nostrilWeight',
                                       side=side,
                                       prefix=prefix, noseTarget=False)

        transJawNostril = self.noseAdditional(name='nostrilWeight', side=side, prefix=prefixJaw,
                                              ctrl=jawCtrl + '.%s'% rotate, noseWeightPMA=transNostril + '.output1D',
                                              operationSum=1, radValue=0.0174533, ctrlValue=valueUpperLipMinHalf,
                                              divide=True)

        rangeTransNostrilGreat = self.multiplyToRange(name='nostrilWeight', side=side, range=range,
                                                      nosePMAX=transNostril + '.output1D', prefix=prefix,
                                                      nameExpr='Great', multRange=False)

        rangeTransNostrilLess = self.multiplyToRange(name='nostrilWeight', side=side, range=range,
                                                     nosePMAX=transJawNostril + '.output1D', prefix=prefix,
                                                     nameExpr='Less', multRange=False)

        addNostrilGreat = self.pmaSetAttr(name='nostrilWeight', valueInput0=getAttrCtrlGrpZroNostril,
                                          input1=rangeTransNostrilGreat + '.outputX',
                                          operation=operation, prefix=prefix, nameExpr='Great', side=side)

        addNostrilLess = self.pmaSetAttr(name='nostrilWeight', valueInput0=getAttrCtrlGrpZroNostril,
                                         input1=rangeTransNostrilLess + '.outputX',
                                         operation=operation, prefix=prefix, nameExpr='Less', side=side)

        return addNostrilGreat, addNostrilLess

    def conditionNostrilWeight(self, jawCtrl, rangeGreatX, rangeLessX, rangeGreatY, rangeLessY, rangeGreatZ, rangeLessZ, target, side, prefix='', nameExpr=''):
        condition = mc.createNode('condition', n='nostrilWeight' + prefix + nameExpr + 'Ctrl' + side+ '_cnd')
        mc.setAttr(condition + '.operation', 3)
        mc.connectAttr(jawCtrl + '.rotateX', condition + '.firstTerm')

        mc.connectAttr(rangeGreatX + '.output1D', condition + '.colorIfTrueR')
        mc.connectAttr(rangeGreatY + '.output1D', condition + '.colorIfTrueG')
        mc.connectAttr(rangeGreatZ + '.output1D', condition + '.colorIfTrueB')

        mc.connectAttr(rangeLessX + '.output1D', condition + '.colorIfFalseR')
        mc.connectAttr(rangeLessY + '.output1D', condition + '.colorIfFalseG')
        mc.connectAttr(rangeLessZ + '.output1D', condition + '.colorIfFalseB')

        mc.connectAttr(condition + '.outColorR', target+'.translateX')
        mc.connectAttr(condition + '.outColorG', target+'.translateY')
        mc.connectAttr(condition + '.outColorB', target+'.translateZ')

        return condition

    def conditionNoseWeight(self, jawCtrl, rangeGreat, rangeLess, targetFirst, targetSecond, prefix='', nameExpr=''):
        condition = mc.createNode('condition', n='noseWeight' + prefix + nameExpr + 'Ctrl' + '_cnd')
        mc.setAttr(condition+'.operation', 3)
        mc.connectAttr(jawCtrl+'.rotateX', condition+'.firstTerm')

        mc.connectAttr(rangeGreat+'.outputX', condition+'.colorIfTrueR')
        mc.connectAttr(rangeGreat+'.outputY', condition+'.colorIfTrueG')

        mc.connectAttr(rangeLess+'.outputX', condition+'.colorIfFalseR')
        mc.connectAttr(rangeLess+'.outputY', condition+'.colorIfFalseG')

        mc.connectAttr(condition+'.outColorR', targetFirst)
        mc.connectAttr(condition+'.outColorG', targetSecond)

        return condition

    def multiplyToRange(self, range, nosePMAX, nosePMAY='', side='',
                      prefix='', nameExpr='Less', name='noseWeight', multRange=True):
        if multRange:
            rangeMult = self.multOrDivConnectTwoAttr(name=name, side=side,
                                                  input1X=nosePMAX,
                                                  input1Y=nosePMAY,
                                                  input2X=range,
                                                  input2Y=range,
                                                  operation=1, prefix=prefix, nameExpr=nameExpr)
        else:
            rangeMult = self.multOrDivConnectAttr(name=name, side=side,
                                                     input1X=nosePMAX,
                                                     input2X=range,
                                                     operation=1, prefix=prefix, nameExpr=nameExpr)
        return rangeMult

    def noseAdditional(self, prefix, ctrl, noseWeightPMA, operationSum, radValue=None, ctrlValue=None, side='',nameExpr='', name='noseWeight',
                       divide=True):

        jawCtrlMUL = self.multOrDivSetAttr(name=name, side=side,
                                           input1X=ctrl, input2XSet=radValue,
                                           operation=1, prefix=prefix+'JawRad', nameExpr=nameExpr)
        if divide:
            jawCtrlDIV = self.multOrDivSetAttr(name=name, side=side,
                                               input1X=jawCtrlMUL + '.outputX', input2XSet=ctrlValue,
                                               operation=2, prefix=prefix+'Jaw', nameExpr=nameExpr)
            jawPMA = self.pmaAttr(name=name, side=side,
                                  input0=noseWeightPMA,
                                  input1=jawCtrlDIV + '.outputX',
                                  operation=operationSum, prefix=prefix, nameExpr=nameExpr)
            return jawPMA

        else:
            jawPMA = self.pmaAttr(name=name, side=side,
                                  input0=noseWeightPMA,
                                  input1=jawCtrlMUL + '.outputX',
                                  operation=operationSum, prefix=prefix, nameExpr=nameExpr)
            return jawPMA

    def noseWeight(self, secondCtrl, firstCtrl, firstValue,
                   secondValue, secondOperation, firstOperation, operationSum,
                   prefix, thirdCtrl='', thirdValue='', nameExpr='', side='', name='noseWeight', noseTarget=True):

        mouthDIV = self.multOrDivSetAttr(name=name, side=side,
                                         input1X=secondCtrl, input2XSet=secondValue,
                                         operation=secondOperation, prefix=prefix + 'Mouth', nameExpr=nameExpr)

        lipUpDIV = self.multOrDivSetAttr(name=name, side=side,
                                         input1X=firstCtrl, input2XSet=firstValue,
                                         operation=firstOperation, prefix=prefix + 'UpLip', nameExpr=nameExpr)

        if not noseTarget:
            cornerLipDIV = self.multOrDivSetAttr(name=name, side=side,
                                             input1X=thirdCtrl, input2XSet=thirdValue,
                                             operation=firstOperation, prefix=prefix + 'CornerLip', nameExpr=nameExpr)

            nosePMA = self.pmaAttr(name=name, side=side,
                                   input0=lipUpDIV + '.outputX',
                                   input1=mouthDIV + '.outputX',
                                   input2= cornerLipDIV + '.outputX',
                                   operation=operationSum, prefix=prefix, nameExpr=nameExpr, inputTwo=True)
        else:
            nosePMA = self.pmaAttr(name=name, side=side,
                                   input0=lipUpDIV + '.outputX',
                                   input1=mouthDIV + '.outputX',
                                   operation=operationSum, prefix=prefix, nameExpr=nameExpr)
        return nosePMA

    def multOrDivConnectTwoAttr(self, name, input1X, input2X, input1Y, input2Y, operation=2, prefix='', nameExpr='', side=''):
        ctrlDrvMDN = mc.createNode('multiplyDivide',
                                   n=au.prefix_name(name) + prefix + nameExpr + 'Ctrl' + side + '_mdn')
        mc.setAttr(ctrlDrvMDN + '.operation', operation)
        mc.connectAttr(input1X , ctrlDrvMDN + '.input1X')
        mc.connectAttr(input1Y , ctrlDrvMDN + '.input1Y')

        mc.connectAttr(input2X, ctrlDrvMDN + '.input2X')
        mc.connectAttr(input2Y, ctrlDrvMDN + '.input2Y')

        return ctrlDrvMDN

    def multOrDivSetTwoAttr(self, name, input1X, input1Y, input2XSet, input2YSet, operation=2, prefix='', nameExpr='', side=''):
        ctrlDrvMDN = mc.createNode('multiplyDivide',
                                   n=au.prefix_name(name) + prefix + nameExpr + 'Ctrl' + side + '_mdn')
        mc.setAttr(ctrlDrvMDN + '.operation', operation)
        mc.connectAttr(input1X , ctrlDrvMDN + '.input1X')
        mc.connectAttr(input1Y , ctrlDrvMDN + '.input1Y')

        mc.setAttr(ctrlDrvMDN + '.input2X', input2XSet)
        mc.setAttr(ctrlDrvMDN + '.input2Y', input2YSet)

        return ctrlDrvMDN

    def multOrDivConnectAttr(self, name, input2X, input1X, operation=2, prefix='', nameExpr='', side=''):
        ctrlDrvMDN = mc.createNode('multiplyDivide',
                                   n=au.prefix_name(name) + prefix + nameExpr + 'Ctrl' + side + '_mdn')
        mc.setAttr(ctrlDrvMDN + '.operation', operation)
        mc.connectAttr(input1X , ctrlDrvMDN + '.input1X')
        mc.connectAttr(input2X, ctrlDrvMDN + '.input2X')

        return ctrlDrvMDN

    def multOrDivSetAttr(self, name, input2XSet, input1X, operation=2, prefix='', nameExpr='', side=''):
        ctrlDrvMDN = mc.createNode('multiplyDivide',
                                   n=au.prefix_name(name) + prefix + nameExpr + 'Ctrl' + side + '_mdn')
        mc.setAttr(ctrlDrvMDN + '.operation', operation)
        mc.connectAttr(input1X , ctrlDrvMDN + '.input1X')
        mc.setAttr(ctrlDrvMDN + '.input2X', input2XSet)

        return ctrlDrvMDN

    def pmaSetAttr(self, name, valueInput0, input1, operation, prefix='', nameExpr='', side=''):
        ctrlDrvPMA = mc.createNode('plusMinusAverage', n=au.prefix_name(name)
                                                         + prefix + nameExpr + 'Ctrl' + side + '_pma')
        mc.setAttr(ctrlDrvPMA + '.operation', operation)
        mc.setAttr(ctrlDrvPMA + '.input1D[0]', valueInput0)
        mc.connectAttr(input1, ctrlDrvPMA + '.input1D[1]')

        return ctrlDrvPMA

    def pmaAttr(self, name, input0, input1, operation, input2='', prefix='', nameExpr='', side='', inputTwo=False):
        ctrlDrvPMA = mc.createNode('plusMinusAverage', n=au.prefix_name(name)
                                                         + prefix + nameExpr + 'Ctrl' + side + '_pma')
        mc.setAttr(ctrlDrvPMA + '.operation', operation)
        mc.connectAttr(input0, ctrlDrvPMA + '.input1D[0]')
        mc.connectAttr(input1, ctrlDrvPMA + '.input1D[1]')
        if inputTwo:
            mc.connectAttr(input2, ctrlDrvPMA + '.input1D[2]')
            return ctrlDrvPMA
        else:
            return ctrlDrvPMA

    def pmaTwoAttr(self, name, input0x, input1x, input2x, input0y, input1y, input2y, operation, prefix='', nameExpr='', side=''):
        ctrlDrvPMA = mc.createNode('plusMinusAverage', n=au.prefix_name(name)
                                                         + prefix + nameExpr + 'Ctrl' + side + '_pma')
        mc.setAttr(ctrlDrvPMA + '.operation', operation)
        mc.connectAttr(input0x, ctrlDrvPMA + '.input2D[0].input2Dx')
        mc.connectAttr(input1x, ctrlDrvPMA + '.input2D[1].input2Dx')
        mc.connectAttr(input2x, ctrlDrvPMA + '.input2D[2].input2Dx')

        mc.connectAttr(input0y, ctrlDrvPMA + '.input2D[0].input2Dy')
        mc.connectAttr(input1y, ctrlDrvPMA + '.input2D[1].input2Dy')
        mc.connectAttr(input2y, ctrlDrvPMA + '.input2D[2].input2Dy')

        return ctrlDrvPMA

    def mdlConnectAttr(self, name, prefix, nameExpr, side, input1, input2):
        connectDrvMDL = mc.createNode('multDoubleLinear', n=au.prefix_name(name) + prefix + nameExpr + 'Ctrl' + side + '_mdl')
        mc.connectAttr(input1, connectDrvMDL + '.input1')
        mc.connectAttr(input2, connectDrvMDL + '.input2')

        return connectDrvMDL

    def mdlSetAttr(self, name, prefix, nameExpr, side, input1, input2Set):
        cornerLipRangeMDL = mc.createNode('multDoubleLinear', n=au.prefix_name(name) + prefix + nameExpr + 'Ctrl' + side + '_mdl')
        mc.connectAttr(input1, cornerLipRangeMDL + '.input1')
        mc.setAttr(cornerLipRangeMDL + '.input2', input2Set)

        return cornerLipRangeMDL