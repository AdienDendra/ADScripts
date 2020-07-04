import re
from __builtin__ import reload
from string import digits

import maya.cmds as mc

from rigging.library.base.face import cheek as ck
from rigging.tools import AD_utils as au

reload (au)
reload (ck)

class Cheek:
    def __init__(self,
                 faceAnimCtrlGrp,
                 faceUtilsGrp,
                 cheekLowJnt,
                 cheekLowPrefix,
                 cheekMidJnt,
                 cheekMidPrefix,
                 cheekUpJnt,
                 cheekUpPrefix,
                 cheekInUpJnt,
                 cheekInUpPrefix,
                 cheekInLowJnt,
                 cheekInLowPrefix,
                 cheekOutUpJnt,
                 cheekOutUpPrefix,
                 cheekOutLowJnt,
                 cheekOutLowPrefix,
                 scale,
                 side,
                 sideRGT,
                 sideLFT,
                 headLowJnt,
                 headUpJnt,
                 jawJnt,
                 cornerLipCtrl,
                 cornerLipCtrlAttrCheekLow,
                 cornerLipCtrlAttrCheekMid,
                 lipDriveCtrl,
                 mouthCtrl,
                 mouthCheekInUpAttr,
                 lowLipDriveCtrl,
                 nostrilDriveCtrlAttrCheekUp,
                 nostrilDriveCtrlAttrCheekUpTwo,
                 nostrilDriveCtrl,

                 cornerLipCtrlAttrCheekOutUp,
                 cornerLipCtrlAttrCheekOutLow,
                 headUpCtrl,
                 headLowCtrl,
                 suffixController
                 ):

        self.pos = mc.xform(cornerLipCtrl, ws=1, q=1, t=1)[0]
        self.nostril = mc.xform(nostrilDriveCtrl, ws=1, q=1, t=1)[0]
        self.sideRGT = sideRGT
        self.sideLFT = sideLFT
        # group cheek driver
        groupDriver = mc.group(em=1, n='cheekJoint'+side+'_grp')
        setupDriverGrp = mc.group(em=1, n='cheekSetup'+side+'_grp')
        ctrlDriverGrp = mc.group(em=1, n='cheekCtrlAll'+side+'_grp')

        mc.hide(setupDriverGrp)
        grpCheekAll = mc.group(em=1, n='cheek'+side+'_grp')
        mc.parent(groupDriver, setupDriverGrp, grpCheekAll)
        mc.parent(ctrlDriverGrp, faceAnimCtrlGrp)
        mc.parent(grpCheekAll, faceUtilsGrp)

        cheek = ck.Build(
                         cheekLowJnt=cheekLowJnt,
                         cheekLowPrefix=cheekLowPrefix,
                         cheekMidJnt=cheekMidJnt,
                         cheekMidPrefix=cheekMidPrefix,
                         cheekUpJnt=cheekUpJnt,
                         cheekUpPrefix=cheekUpPrefix,
                         cheekInUpJnt=cheekInUpJnt,
                         cheekInUpPrefix=cheekInUpPrefix,
                         cheekInLowJnt=cheekInLowJnt,
                         cheekInLowPrefix=cheekInLowPrefix,
                         cheekOutUpJnt=cheekOutUpJnt,
                         cheekOutUpPrefix=cheekOutUpPrefix,
                         cheekOutLowJnt=cheekOutLowJnt,
                         cheekOutLowPrefix=cheekOutLowPrefix,
                         scale=scale,
                         side=side,
                         suffixController=suffixController)

        mc.parent(cheek.cheekLowJnt[0], cheek.cheekMidJnt[0],
                  cheek.cheekUpJnt[0], cheek.cheekInUpJnt[0],
                  cheek.cheekInLowJnt[0],
                  cheek.cheekOutUpJnt[0],
                  cheek.cheekOutLowJnt[0], groupDriver)

        mc.parent(cheek.cheekLowParentCtrlZro, cheek.cheekMidParentCtrlZro,
                  cheek.cheekUpParentCtrlZro, cheek.cheekInUpParentCtrlZro,
                  cheek.cheekInLowParentCtrlZro,
                  cheek.cheekOutUpParentCtrlZro,
                  cheek.cheekOutLowParentCtrlZro, ctrlDriverGrp)

        self.cheekLowZroCtrlGrp = cheek.cheekLowParentCtrlZro
        self.cheekMidZroCtrlGrp = cheek.cheekMidParentCtrlZro
        self.cheekOutUpZroCtrlGrp = cheek.cheekOutUpParentCtrlZro
        self.cheekOutLowZroCtrlGrp = cheek.cheekOutLowParentCtrlZro

        self.cheekUpZroCtrlGrp = cheek.cheekUpParentCtrlZro
        self.cheekInUpZroCtrlGrp = cheek.cheekInUpParentCtrlZro
        self.cheekInLowZroCtrlGrp = cheek.cheekInLowParentCtrlZro


    # ==================================================================================================================
    #                                                       SET DRIVER
    # ==================================================================================================================
        # CHEEK OUT UP
        cheekOutUpSet = self.setDriverCheek(expressionMidOutArea=True, nameExpr='OutUp', attributeOffset=cornerLipCtrlAttrCheekOutUp,
                                            objectPrefix=cheekOutUpPrefix, objectJoint= cheekOutUpJnt,
                                            side=side, scale=scale, constraint=[headUpJnt], w=[1.0],
                                            groupDriverJnt=cheek.cheekOutUpJnt[0],
                                            controller=cornerLipCtrl, cheekJointParentOffset=cheek.cheekOutUpJnt[1],
                                            cheekJointParentZro=cheek.cheekOutUpJnt[0],
                                            cheekParentCtrlZro=cheek.cheekOutUpParentCtrlZro,
                                            cheekParentCtrlOffset=cheek.cheekOutUpParentCtrlOffset,
                                            cheekCtrl=cheek.cheekOutUpCtrl, cheekJnt=cheekOutUpJnt,
                                            valueDivTx=12.0, valueDivTy=12.0, tzRangeOne=24.0, tzRangeTwo=24.0,
                                            tyRangeOne=72.0, tyRangeTwo=16.0, multiplierTz=1.0
                                            )

        # CHEEK OUT LOW
        cheekOutLowSet = self.setDriverCheek(expressionMidOutArea=True, nameExpr='OutLow', attributeOffset=cornerLipCtrlAttrCheekOutLow,
                                             objectPrefix=cheekOutLowPrefix, objectJoint= cheekOutLowJnt,
                                             side=side, scale=scale, constraint=[headLowJnt, jawJnt], w=[1.0, 0.5], interpType=2,
                                             groupDriverJnt=cheek.cheekOutLowJnt[0],
                                             controller=cornerLipCtrl, cheekJointParentOffset=cheek.cheekOutLowJnt[1],
                                             cheekJointParentZro=cheek.cheekOutLowJnt[0],
                                             cheekParentCtrlZro=cheek.cheekOutLowParentCtrlZro,
                                             cheekParentCtrlOffset=cheek.cheekOutLowParentCtrlOffset,
                                             cheekCtrl=cheek.cheekOutLowCtrl, cheekJnt=cheekOutLowJnt,
                                             valueDivTx=3.0, valueDivTy=3.0, tzRangeOne=6.0, tzRangeTwo=6.0,
                                             tyRangeOne=18.0, tyRangeTwo=4.0, multiplierTz=1.0
                                             )

        # CHEEK UP
        cheekUpSet = self.setDriverCheek(expressionMidUpArea=True, nameExpr='Up', attributeOffset=nostrilDriveCtrlAttrCheekUp,
                                         attributeOffsetTwo=nostrilDriveCtrlAttrCheekUpTwo,
                                         objectPrefix=cheekUpPrefix, objectJoint= cheekUpJnt,
                                         side=side, scale=scale, constraint=[headUpJnt], w=[1.0],
                                         groupDriverJnt=cheek.cheekUpJnt[0],
                                         controller=nostrilDriveCtrl, cheekJointParentOffset=cheek.cheekUpJnt[1],
                                         cheekJointParentZro=cheek.cheekUpJnt[0],
                                         cheekParentCtrlZro=cheek.cheekUpParentCtrlZro,
                                         cheekParentCtrlOffset=cheek.cheekUpParentCtrlOffset,
                                         cheekCtrl=cheek.cheekUpCtrl, cheekJnt=cheekUpJnt,
                                         tzRangeOne = 0.75, tzRangeTwo = 4.5)

        # CHEEK MID
        cheekMidSet = self.setDriverCheek(expressionMidOutArea=True, nameExpr='Mid', attributeOffset=cornerLipCtrlAttrCheekMid,
                                          objectPrefix=cheekMidPrefix, objectJoint= cheekMidJnt,
                                          side=side, scale=scale, constraint=[headUpJnt,headLowJnt,jawJnt],
                                          w=[0.7, 0.2, 0.1], interpType=2,
                                          groupDriverJnt=cheek.cheekMidJnt[0],
                                          controller=cornerLipCtrl, cheekJointParentOffset=cheek.cheekMidJnt[1],
                                          cheekJointParentZro=cheek.cheekMidJnt[0],
                                          cheekParentCtrlZro=cheek.cheekMidParentCtrlZro,
                                          cheekParentCtrlOffset=cheek.cheekMidParentCtrlOffset,
                                          cheekCtrl=cheek.cheekMidCtrl, cheekJnt=cheekMidJnt,
                                          valueDivTx = 1.5, valueDivTy = 1.5, tzRangeOne = 4.0, tzRangeTwo = 4.0,
                                          tyRangeOne = 18.0, tyRangeTwo = 3.0, multiplierTz=1.0
                                          )

        # CHEEK LOW
        cheekLowSet = self.setDriverCheek(expressionMidOutArea=True, nameExpr='Low', attributeOffset=cornerLipCtrlAttrCheekLow,
                                          objectPrefix=cheekLowPrefix, objectJoint= cheekLowJnt,
                                          side=side, scale=scale, constraint=[headLowJnt,jawJnt], w=[0.4,0.6],
                                          interpType=2,
                                          groupDriverJnt=cheek.cheekLowJnt[0],
                                          controller=cornerLipCtrl, cheekJointParentOffset=cheek.cheekLowJnt[1],
                                          cheekJointParentZro=cheek.cheekLowJnt[0],
                                          cheekParentCtrlZro=cheek.cheekLowParentCtrlZro,
                                          cheekParentCtrlOffset=cheek.cheekLowParentCtrlOffset,
                                          cheekCtrl=cheek.cheekLowCtrl, cheekJnt=cheekLowJnt,
                                          valueDivTx=0.85, valueDivTy=0.85, tzRangeOne=3.0, tzRangeTwo=3.0,
                                          tyRangeOne=9.0, tyRangeTwo=2.0, multiplierTz=0.5
                                          )
        # CHEEK IN UP
        cheekInUp = self.setDriverCheek(expressionInArea=True, nameExpr='InUp',
                                        objectPrefix=cheekInUpPrefix, objectJoint=cheekInUpJnt,
                                        side=side, scale=scale, constraint=[headLowJnt,jawJnt], w=[0.8, 0.2],
                                        interpType=2,
                                        groupDriverJnt=cheek.cheekInUpJnt[0],
                                        controller=cornerLipCtrl, cheekJointParentOffset=cheek.cheekInUpJnt[1],
                                        cheekJointParentZro=cheek.cheekInUpJnt[0],
                                        cheekParentCtrlZro=cheek.cheekInUpParentCtrlZro,
                                        cheekParentCtrlOffset=cheek.cheekInUpParentCtrlOffset,
                                        cheekCtrl=cheek.cheekInUpCtrl, cheekJnt=cheekInUpJnt,
                                        valueDivTx = 2.0, valueDivTy = 2.5, valueDivTz= 2.0,
                                        lipDriveCtrl=lipDriveCtrl, mouthCtrl=mouthCtrl, mouthCheekInUpAttr=mouthCheekInUpAttr
                                        )

        # CHEEK IN LOW
        chekInLow = self.setDriverCheek(cheekInLow=True, objectPrefix=cheekInLowPrefix, objectJoint=cheekInLowJnt,
                                        side=side, scale=scale, constraint=[cheekLowJnt, lowLipDriveCtrl, jawJnt],
                                        w=[0.25, 0.75, 1.0], interpType=2,
                                        groupDriverJnt=cheek.cheekInLowJnt[0],
                                        cheekJointParentOffset=cheek.cheekInLowJnt[1],
                                        cheekJointParentZro=cheek.cheekInLowJnt[0],
                                        cheekParentCtrlZro=cheek.cheekInLowParentCtrlZro,
                                        cheekParentCtrlOffset=cheek.cheekInLowParentCtrlOffset,
                                        cheekCtrl=cheek.cheekInLowCtrl, cheekJnt=cheekInLowJnt,
                                        )

        # SCALE CONSTRAINT SET GRP
        mc.scaleConstraint(headUpCtrl, headLowCtrl, cheekOutUpSet, mo=1)
        mc.scaleConstraint(headLowCtrl, cheekOutLowSet, mo=1)
        mc.scaleConstraint(headUpCtrl, cheekUpSet, mo=1)
        mc.scaleConstraint(headUpCtrl, headLowCtrl, cheekMidSet, mo=1)
        mc.scaleConstraint(headLowCtrl, cheekLowSet, mo=1)
        mc.scaleConstraint(headLowCtrl, cheekInUp, mo=1)
        mc.scaleConstraint(headLowCtrl, chekInLow, mo=1)

        mc.parent(cheekOutUpSet, cheekOutLowSet, cheekUpSet, cheekMidSet, cheekLowSet, cheekInUp, chekInLow, setupDriverGrp)
    # ==================================================================================================================
    #                                       FUNCTION SETUP FOR PART CHEEK JOINTS
    # ==================================================================================================================

    def setDriverCheek(self, nameExpr='', attributeOffset='', attributeOffsetTwo='', objectPrefix='', objectJoint='',
                       side='', scale=None, groupDriverJnt='', cheekInLow=None,
                       valueDivTx=None, valueDivTy=None, valueDivTz=None,
                       tzRangeOne=None, tzRangeTwo=None, tyRangeOne=None, tyRangeTwo=None,
                       expressionMidOutArea=None, expressionInArea=None, expressionMidUpArea=None,
                       constraint=[], w=[], interpType=1, controller='', cheekJointParentOffset='', cheekJointParentZro='',
                       cheekParentCtrlZro='', cheekParentCtrlOffset='', cheekCtrl='', cheekJnt='',
                       lipDriveCtrl='', mouthCtrl='', mouthCheekInUpAttr='', multiplierTz=None
                       ):

        if self.pos < 0:
            multiplier = -1
        else:
            multiplier = 1

        if self.nostril<0:
            operator = 2
        else:
            operator = 1

        # mc.select(cl=1)
        parentDriver = mc.group(em=1, n=au.prefix_name(objectPrefix) + side + '_set')
        driver = mc.spaceLocator(n=au.prefix_name(objectPrefix) + 'Drv' + side + '_set')[0]
        mc.parent(driver, parentDriver)
        mc.delete(mc.parentConstraint(objectJoint, parentDriver, mo=0))

        mc.setAttr(driver+'.localScaleX', 0.5*scale)
        mc.setAttr(driver+'.localScaleY', 0.5*scale)
        mc.setAttr(driver+'.localScaleZ', 0.5*scale)

        constInterp = None
        for cons, value in zip(constraint, w):
            constInterp = mc.parentConstraint(cons, parentDriver, mo=1, w=value)
            # constraint rename
            constInterp = au.constraint_rename(constInterp)

        # SET INTERPOLATION
        mc.setAttr(constInterp[0]+'.interpType', interpType)

        # mc.parentConstraint(parentDriver, groupDriverJnt, mo=1)
        # mc.scaleConstraint(parentDriver, groupDriverJnt, mo=1)
        au.connect_attr_object(parentDriver, groupDriverJnt)
        # mc.connectAttr(driver+'.translate', groupDriverJnt+'.translate')
        # mc.connectAttr(driver+'.rotate', groupDriverJnt+'.rotate')
        # mc.connectAttr(driver+'.scale', groupDriverJnt+'.scale')
        # au.connectAttrObject(driver, groupDriverJnt)

        # CORNER LIP FOR REVERSE
        # CREATE MULTIPLIER CONTROLLER
        controllerNews = self.replacePosLFTRGT(controller)
        controllerNew = self.reorderNumber(controllerNews)

        driverNew = self.replacePosLFTRGT(driver)
        lipDriveCtrlNew = self.replacePosLFTRGT(lipDriveCtrl)
        mouthCtrlNew = self.replacePosLFTRGT(mouthCtrl)
        newCheekJointParentOffset = self.replacePosLFTRGT(cheekJointParentOffset)

        if expressionMidUpArea:

            rangeMidUpZ = controller +'.%s' % attributeOffset
            rangeMidUp = controller +'.%s' % attributeOffsetTwo

            # DIVIDED FOR RANGE
            ctrlDrvRangeMDN = mc.createNode('multiplyDivide', n=au.prefix_name(controllerNew[0]) + 'Range' + nameExpr + 'Ctrl' + side + '_mdn')
            mc.setAttr(ctrlDrvRangeMDN + '.operation', 2)
            mc.setAttr(ctrlDrvRangeMDN + '.input1X', 2)
            mc.setAttr(ctrlDrvRangeMDN + '.input1Y', 2)
            mc.connectAttr(rangeMidUp, ctrlDrvRangeMDN + '.input2X')
            mc.connectAttr(rangeMidUpZ, ctrlDrvRangeMDN + '.input2Y')

            # DIVIDED BY CONTROLLER
            ctrlDrvTxMDN = self.multOrDivConnectAttr(name=controllerNew[0], prefix='Tx', nameExpr=nameExpr,
                                                     side=side, input2X=ctrlDrvRangeMDN+'.outputX',
                                                     input1X=controller+'.translateX', operation=2)

            ctrlDrvTyMDN = self.multOrDivConnectAttr(name=controllerNew[0], prefix='Ty', nameExpr=nameExpr,
                                                     side=side, input2X=ctrlDrvRangeMDN+'.outputX',
                                                     input1X=controller+'.translateY', operation=2)

            # ADD OR SUBTRACT FROM SET GRP
            ctrlDrvTxPMA= self.pmaExpr(name=newCheekJointParentOffset, prefix='Tx', nameExpr=nameExpr, side=side,
                                       operation=operator, input0=driver+'.translateX', input1=ctrlDrvTxMDN+ '.outputX')

            ctrlDrvTyPMA= self.pmaExpr(name=newCheekJointParentOffset, prefix='Ty', nameExpr=nameExpr, side=side,
                                       operation=1, input0=driver+'.translateY', input1=ctrlDrvTyMDN+ '.outputX')

            # TRANSLATE Z
            cornerLipDrvTzRangeMDL = self.mdlSetAttr(name=controllerNew[0], prefix='TzRange',
                                                        nameExpr=nameExpr, side=side, input1=rangeMidUp, input2Set=2)

            # DIVIDED BY CONTROLLER
            ctrlDrvTzMDN = self.multOrDivConnectAttr(name=controllerNew[0], prefix='Tz', nameExpr=nameExpr,
                                                     side=side, input2X=cornerLipDrvTzRangeMDL+'.output',
                                                     input1X=controller+'.translateZ', operation=2)

            # ADD WITH SET CONTROLLER
            ctrlDrvTzDriverPMA= self.pmaExpr(name=driverNew, prefix='Tz', nameExpr=nameExpr, side=side,
                                       operation=1, input0=ctrlDrvTzMDN+'.outputX', input1=driver+ '.translateZ')

            # MULT RANGE NORMAL
            cornerLipDrvTzRangeOneMDL = self.mdlSetAttr(name=controllerNew[0], prefix='TzRangeOne',
                                                        nameExpr=nameExpr, side=side, input1=ctrlDrvRangeMDN + '.outputX',
                                                        input2Set=tzRangeOne)
            cornerLipDrvTzRangeTwoMDL = self.mdlSetAttr(name=controllerNew[0], prefix='TzRangeTwo',
                                                        nameExpr=nameExpr, side=side, input1=ctrlDrvRangeMDN + '.outputX',
                                                        input2Set=tzRangeTwo)

            # MULT RANGE Z
            cornerLipDrvTzRangeZOneMDL = self.mdlConnectAttr(name=controllerNew[0], prefix='TzRangeZOne', nameExpr=nameExpr,
                                                             side=side,
                                                             input1=cornerLipDrvTzRangeOneMDL+'.output',
                                                             input2=ctrlDrvRangeMDN + '.outputY')

            cornerLipDrvTzRangeZTwoMDL = self.mdlConnectAttr(name=controllerNew[0], prefix='TzRangeZTwo',nameExpr=nameExpr,
                                                             side=side,
                                                             input1=cornerLipDrvTzRangeTwoMDL + '.output',
                                                             input2=ctrlDrvRangeMDN + '.outputY')

            # DIVIDE RANGE Z AND RANGE NORMAL
            ctrlDrvTzRangeOneMDN = self.multOrDivConnectAttr(name=controllerNew[0], prefix='TzRangeOneMul', nameExpr=nameExpr,
                                                             side=side, input2X=cornerLipDrvTzRangeZOneMDL+'.output',
                                                             input1X=controller+'.translateY', operation=2)

            ctrlDrvTzRangeTwoMDN = self.multOrDivConnectAttr(name=controllerNew[0], prefix='TzRangeTwoMul', nameExpr=nameExpr,
                                                             side=side, input2X=cornerLipDrvTzRangeZTwoMDL+'.output',
                                                             input1X=controller+'.translateY', operation=2)

            # ADD WITH SET CONTROLLER
            ctrlDrvTzRangePMA = mc.createNode('plusMinusAverage', n=au.prefix_name(newCheekJointParentOffset)
                                                                    +'TzRange'+nameExpr+'Grp'+side+'_pma')
            mc.connectAttr(ctrlDrvTzRangeOneMDN+'.outputX',ctrlDrvTzRangePMA +'.input2D[0].input2Dx')
            mc.connectAttr(ctrlDrvTzRangeTwoMDN+'.outputX',ctrlDrvTzRangePMA +'.input2D[0].input2Dy')
            mc.connectAttr(ctrlDrvTzDriverPMA+'.output1D',ctrlDrvTzRangePMA +'.input2D[1].input2Dx')
            mc.connectAttr(ctrlDrvTzDriverPMA+'.output1D',ctrlDrvTzRangePMA +'.input2D[1].input2Dy')

            # CREATE CONDITION FOR TY AND TZ CONTROLLER
            ctrlDrvTzRangeCND = mc.createNode('condition', n=au.prefix_name(newCheekJointParentOffset) + 'Tz' + nameExpr + 'Ctrl' + side + '_cnd')
            mc.setAttr(ctrlDrvTzRangeCND + '.operation', 2)
            mc.connectAttr(controller + '.translateY', ctrlDrvTzRangeCND + '.firstTerm')
            mc.connectAttr(ctrlDrvTzRangePMA + '.output2D.output2Dx', ctrlDrvTzRangeCND + '.colorIfTrueR')
            mc.connectAttr(ctrlDrvTzRangePMA + '.output2D.output2Dy', ctrlDrvTzRangeCND + '.colorIfFalseR')

            # CONNECT TO OBJECT SET TARGET
            mc.connectAttr(ctrlDrvTxPMA+'.output1D', cheekJointParentOffset+'.translateX')
            mc.connectAttr(ctrlDrvTyPMA+'.output1D', cheekJointParentOffset+'.translateY')
            mc.connectAttr(ctrlDrvTzRangeCND + '.outColorR', cheekJointParentOffset + '.translateZ')

            # CONNECT ROTATE TO OBJECT
            au.connect_attr_rotate(controller, cheekJointParentOffset)

        if expressionMidOutArea:

            cornerLipDrvTxMDL = self.mdlSetAttr(name=controllerNew[0], prefix='Tx',
                                                    nameExpr=nameExpr, side=side, input1=controller + '.translateX',
                                                    input2Set=multiplier)

            rangeMidOut = controller +'.%s' % attributeOffset

            # CREATE MULTIPLY FOR CONTROLLER
            cornerLipDrvTransLowXMDN = self.multOrDivConnectAttr(name=controllerNew[0], prefix='TransX', nameExpr=nameExpr,
                                                                 side=side, input2X=rangeMidOut,
                                                                 input1X=cornerLipDrvTxMDL + '.output', operation=1)

            cornerLipDrvTransLowYMDN = self.multOrDivConnectAttr(name=controllerNew[0], prefix='TransY', nameExpr=nameExpr,
                                                                 side=side, input2X=rangeMidOut,
                                                                 input1X=controller + '.translateY', operation=1)

            # CREATE DIVIDED FOR CONTROLLER TO THE VALUE
            cornerLipDrvDivTransXLowMDN = self.multOrDivSetAttr(name=controllerNew[0], prefix='DivTransX', nameExpr=nameExpr,
                                                            side=side, input2XSet=valueDivTx,
                                                            input1X=cornerLipDrvTransLowXMDN + '.outputX', operation=2)

            cornerLipDrvDivTransYLowMDN = self.multOrDivSetAttr(name=controllerNew[0], prefix='DivTransY', nameExpr=nameExpr,
                                                            side=side, input2XSet=valueDivTy,
                                                            input1X=cornerLipDrvTransLowYMDN + '.outputX', operation=2)

            # CREATE PLUS MINUS AVERAGE CHEEK LOW TX AND TY SET AND CONTROLLER
            cheekLowCornerLipDrvTxTyPMA = mc.createNode('plusMinusAverage', n=au.prefix_name(newCheekJointParentOffset)
                                                                    +'TxTy'+nameExpr+'Grp'+side+'_pma')

            mc.connectAttr(cornerLipDrvDivTransXLowMDN +'.outputX', cheekLowCornerLipDrvTxTyPMA + '.input2D[0].input2Dx')
            mc.connectAttr(cornerLipDrvDivTransYLowMDN + '.outputX', cheekLowCornerLipDrvTxTyPMA + '.input2D[0].input2Dy')
            mc.connectAttr(driver +'.translateX', cheekLowCornerLipDrvTxTyPMA + '.input2D[1].input2Dx')
            mc.connectAttr(driver + '.translateY', cheekLowCornerLipDrvTxTyPMA + '.input2D[1].input2Dy')

            # CONNECTION TY
            cornerLipDrvTyMDL = self.mdlConnectAttr(name=controllerNew[0], prefix='TyTrans',
                                            nameExpr=nameExpr, side=side, input1=controller + '.translateY',
                                            input2=rangeMidOut)

            # CREATE DIVIDED FOR TY CONTROLLER TO THE VALUE
            cornerLipDrvTyDivTransLowOneMDN = self.multOrDivSetAttr(name=controllerNew[0], prefix='DivTyTransOne',
                                                             nameExpr=nameExpr,
                                                             side=side, input2XSet=tyRangeOne,
                                                             input1X=cornerLipDrvTyMDL + '.output', operation=2)

            cornerLipDrvTyDivTransLowTwoMDN = self.multOrDivSetAttr(name=controllerNew[0], prefix='DivTyTransTwo',
                                                                nameExpr=nameExpr,
                                                                side=side, input2XSet=tyRangeTwo,
                                                                input1X=cornerLipDrvTyMDL + '.output', operation=2)

            # CONNECTION TZ
            cornerLipDrvTzMDL = self.mdlConnectAttr(name=controllerNew[0], prefix='TzTrans',
                                                nameExpr=nameExpr, side=side, input1=controller + '.translateZ',
                                                input2=rangeMidOut)

            # CREATE DIVIDED FOR TZ CONTROLLER TO THE VALUE
            cornerLipDrvTzDivTransLowOneMDN = self.multOrDivSetAttr(name=controllerNew[0], prefix='DivTzTransOne',
                                                                nameExpr=nameExpr,
                                                                side=side, input2XSet=tzRangeOne,
                                                                input1X=cornerLipDrvTzMDL + '.output', operation=2)

            cornerLipDrvTzDivTransLowTwoMDN = self.multOrDivSetAttr(name=controllerNew[0], prefix='DivTzTransTwo',
                                                                nameExpr=nameExpr,
                                                                side=side, input2XSet=tzRangeTwo,
                                                                input1X=cornerLipDrvTzMDL + '.output', operation=2)

            # CREATE PLUS MINUS FOR CONDITION
            cheekLowCornerLipDrvTzPMA = mc.createNode('plusMinusAverage', n=au.prefix_name(newCheekJointParentOffset)
                                                                            + 'Tz' + nameExpr + 'Grp' + side + '_pma')
            mc.connectAttr(cornerLipDrvTzDivTransLowOneMDN + '.outputX', cheekLowCornerLipDrvTzPMA + '.input2D[0].input2Dx')
            mc.connectAttr(cornerLipDrvTzDivTransLowTwoMDN + '.outputX', cheekLowCornerLipDrvTzPMA + '.input2D[0].input2Dy')
            mc.connectAttr(cornerLipDrvTyDivTransLowOneMDN + '.outputX', cheekLowCornerLipDrvTzPMA + '.input2D[1].input2Dx')
            mc.connectAttr(cornerLipDrvTyDivTransLowTwoMDN + '.outputX', cheekLowCornerLipDrvTzPMA + '.input2D[1].input2Dy')

            mc.connectAttr(driver + '.translateZ', cheekLowCornerLipDrvTzPMA + '.input2D[2].input2Dx')
            mc.connectAttr(driver + '.translateZ', cheekLowCornerLipDrvTzPMA + '.input2D[3].input2Dy')

            # CREATE CONDITION FOR TY AND TZ CONTROLLER
            cornerLipDrvTyDivTransLowCND = mc.createNode('condition',
                                                         n=au.prefix_name(controllerNew[0]) + 'DivTyTrans' + nameExpr + 'Ctrl' + side + '_cnd')
            mc.setAttr(cornerLipDrvTyDivTransLowCND+'.operation', 4)
            mc.connectAttr(controller + '.translateY', cornerLipDrvTyDivTransLowCND + '.firstTerm')
            mc.connectAttr(cheekLowCornerLipDrvTzPMA + '.output2D.output2Dx', cornerLipDrvTyDivTransLowCND + '.colorIfTrueR')
            mc.connectAttr(cheekLowCornerLipDrvTzPMA + '.output2D.output2Dy', cornerLipDrvTyDivTransLowCND + '.colorIfFalseR')

            # CREATE MULTIPLY Z CONTROLLER
            cornerLipDrvTzMultMDL = self.mdlSetAttr(name=controllerNew[0], prefix='MultTz',
                                                nameExpr=nameExpr, side=side,
                                                input1=cornerLipDrvTyDivTransLowCND + '.outColorR',
                                                    input2Set=multiplierTz)

            # CONNECT TRANSLATE TO OBJECT
            mc.connectAttr(cheekLowCornerLipDrvTxTyPMA + '.output2Dx', cheekJointParentOffset + '.translateX')
            mc.connectAttr(cheekLowCornerLipDrvTxTyPMA + '.output2Dy', cheekJointParentOffset + '.translateY')

            mc.connectAttr(cornerLipDrvTzMultMDL + '.output', cheekJointParentOffset + '.translateZ')

            # CONNECT ROTATE TO OBJECT
            au.connect_attr_rotate(controller, cheekJointParentOffset)

        if expressionInArea:
            cornerLipDrvTxMDL = self.mdlSetAttr(name=controllerNew[0], prefix='Tx',
                                                        nameExpr=nameExpr, side=side, input1=controller + '.translateX',
                                                        input2Set=multiplier)

            # CREATE DIVIDE CONTROLLER
            cornerLipDrvTransMDN= mc.createNode('multiplyDivide', n=au.prefix_name(controllerNew[0]) + 'Trans' + nameExpr + 'Ctrl' + side + '_mdn')
            mc.setAttr(cornerLipDrvTransMDN + '.operation', 2)
            mc.connectAttr(cornerLipDrvTxMDL + '.output', cornerLipDrvTransMDN + '.input1X')
            mc.connectAttr(controller +'.translateY', cornerLipDrvTransMDN + '.input1Y')
            mc.connectAttr(controller +'.translateZ', cornerLipDrvTransMDN + '.input1Z')

            mc.setAttr(cornerLipDrvTransMDN + '.input2X', valueDivTx)
            mc.setAttr(cornerLipDrvTransMDN + '.input2Y', valueDivTy)
            mc.setAttr(cornerLipDrvTransMDN + '.input2Z', valueDivTz)

            # CREATE PLUS MINUS AVERAGE DRIVER AND CONTROLLER
            cheekInUpCornerLipDrvPMA = mc.createNode('plusMinusAverage', n=au.prefix_name(driverNew) +
                                                                           (au.prefix_name((controllerNew[0])[0].capitalize() +
                                                                                           au.prefix_name((controllerNew[0])[1:]))) +
                                                                           nameExpr +'Ctrl' + side + '_pma')

            mc.connectAttr(driver +'.translate', cheekInUpCornerLipDrvPMA + '.input3D[0]')
            mc.connectAttr(cornerLipDrvTransMDN + '.output', cheekInUpCornerLipDrvPMA + '.input3D[1]')

            # CREATE DIVIDE LIP DRIVE CTRL
            lipUpDrvAllCtrlTransMDN= mc.createNode('multiplyDivide', n=au.prefix_name(lipDriveCtrlNew) + 'Trans' + nameExpr + 'Ctrl' + side + '_mdn')
            mc.setAttr(lipUpDrvAllCtrlTransMDN + '.operation', 2)
            mc.connectAttr(lipDriveCtrl +'.translate', lipUpDrvAllCtrlTransMDN + '.input1')

            mc.setAttr(lipUpDrvAllCtrlTransMDN + '.input2X', 2)
            mc.setAttr(lipUpDrvAllCtrlTransMDN + '.input2Y', 2)
            mc.setAttr(lipUpDrvAllCtrlTransMDN + '.input2Z', 2)

            # CREATE DIVIDE MOUTH CTRL
            mouthCtrlMulAttr= mc.createNode('multiplyDivide',
                                            n=au.prefix_name(mouthCtrlNew) + 'MulAttr' + nameExpr + 'Ctrl' + side + '_mdn')
            mc.setAttr(mouthCtrlMulAttr + '.operation', 2)
            mc.connectAttr(mouthCtrl + '.%s' % mouthCheekInUpAttr, mouthCtrlMulAttr+ '.input2X')
            mc.connectAttr(mouthCtrl + '.%s' % mouthCheekInUpAttr, mouthCtrlMulAttr + '.input2Y')
            mc.connectAttr(mouthCtrl + '.%s' % mouthCheekInUpAttr, mouthCtrlMulAttr + '.input2Z')

            mc.setAttr(mouthCtrlMulAttr + '.input1X', 25)
            mc.setAttr(mouthCtrlMulAttr + '.input1Y', 25)
            mc.setAttr(mouthCtrlMulAttr + '.input1Z', 25)

            mouthCtrlTransMDN = mc.createNode('multiplyDivide',
                                              n=au.prefix_name(mouthCtrlNew) + 'Trans' + nameExpr + 'Ctrl' + side + '_mdn')
            mc.setAttr(mouthCtrlTransMDN + '.operation', 2)
            mc.connectAttr(mouthCtrl + '.translate', mouthCtrlTransMDN + '.input1')
            mc.connectAttr(mouthCtrlMulAttr+'.output', mouthCtrlTransMDN + '.input2')

            # CREATE PLUS MINUS LIP DRIVE CTRL AND MOUTH CTRL
            lipUpDrvAllMouthCtrlTransPMA = mc.createNode('plusMinusAverage',
                                                         n=au.prefix_name(lipDriveCtrlNew) +
                                                           au.prefix_name(mouthCtrlNew.capitalize()) + nameExpr + 'Ctrl' + side + '_pma')
            mc.connectAttr(lipUpDrvAllCtrlTransMDN + '.output', lipUpDrvAllMouthCtrlTransPMA + '.input3D[0]')
            mc.connectAttr(mouthCtrlTransMDN + '.output', lipUpDrvAllMouthCtrlTransPMA + '.input3D[1]')

            # CREATE PLUS MINUS LIP DRIVE CTRL AND MOUTH CTRL
            cheekInUpCornerLipLipUpDrvAllMouthPMA = mc.createNode('plusMinusAverage',
                                                                  n=au.prefix_name(newCheekJointParentOffset)
                                                                  +nameExpr+'Grp' +side+'_pma')

            mc.connectAttr(cheekInUpCornerLipDrvPMA + '.output3D', cheekInUpCornerLipLipUpDrvAllMouthPMA + '.input3D[0]')
            mc.connectAttr(lipUpDrvAllMouthCtrlTransPMA + '.output3D', cheekInUpCornerLipLipUpDrvAllMouthPMA + '.input3D[1]')

            # CONNECT TRANSLATE AND ROTATE
            mc.connectAttr(cheekInUpCornerLipLipUpDrvAllMouthPMA + '.output3D', cheekJointParentOffset + '.translate')
            au.connect_attr_rotate(driver, cheekJointParentOffset)


        # connect attribute cheek  joint parent to cheek parent controller
        au.connect_attr_object(cheekJointParentZro, cheekParentCtrlZro)
        # au.connectAttrScale(cheekJointParentZro, cheekParentCtrlOffset)
        au.connectAttrTransRot(cheekJointParentOffset, cheekParentCtrlOffset)

        # connect attribute cheek controller to cheek  joint
        if not cheekInLow:
            if self.pos < 0:
                self.reverseNode(cheekCtrl, cheekJnt, objectPrefix, side)
                au.connect_attr_scale(cheekCtrl, cheekJnt)

            else:
                # au.connectAttrTransRot(cheekCtrl, cheekJnt)
                au.connect_attr_object(cheekCtrl, cheekJnt)
        else:
            reverseTrans = mc.createNode('multiplyDivide', n=au.prefix_name(objectPrefix) + 'ReverseTrans' + side + '_mdn')
            reverseRot = mc.createNode('multiplyDivide', n=au.prefix_name(objectPrefix) + 'ReverseRot' + side + '_mdn')

            if self.pos<0:
                mc.setAttr(reverseTrans + '.input2X', -1)
                mc.setAttr(reverseTrans + '.input2Y', -1)
                mc.setAttr(reverseTrans + '.input2Z', 1)
                mc.setAttr(reverseRot + '.input2X', -1)
                mc.setAttr(reverseRot + '.input2Y', -1)
                mc.setAttr(reverseRot + '.input2Z', 1)

            else:
                mc.setAttr(reverseTrans + '.input2X', 1)
                mc.setAttr(reverseTrans + '.input2Y', -1)
                mc.setAttr(reverseTrans + '.input2Z', 1)
                mc.setAttr(reverseRot + '.input2X', -1)
                mc.setAttr(reverseRot + '.input2Y', 1)
                mc.setAttr(reverseRot + '.input2Z', -1)

            mc.connectAttr(cheekCtrl +'.translate', reverseTrans + '.input1')
            mc.connectAttr(reverseTrans + '.output', cheekJnt + '.translate')
            mc.connectAttr(cheekCtrl +'.rotate', reverseRot + '.input1')
            mc.connectAttr(reverseRot + '.output', cheekJnt + '.rotate')

            # au.connectAttrRot(cheekCtrl, cheekJnt)
            au.connect_attr_scale(cheekCtrl, cheekJnt)

        return parentDriver

    def reorderNumber(self, prefix):
        # get the number
        try:
            patterns = [r'\d+']
            prefixNumber = au.prefix_name(prefix)
            for p in patterns:
                prefixNumber = re.findall(p, prefixNumber)[0]
        except:
            prefixNumber=''

        # get the prefix without number
        prefixNoNumber = str(prefix).translate(None, digits)

        return prefixNoNumber, prefixNumber

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

    def multOrDivConnectAttr(self, name, prefix, nameExpr, side, input2X, input1X, operation=2):
        ctrlDrvMDN = mc.createNode('multiplyDivide',
                                   n=au.prefix_name(name) + prefix + nameExpr + 'Ctrl' + side + '_mdn')
        mc.setAttr(ctrlDrvMDN + '.operation', operation)
        mc.connectAttr(input1X , ctrlDrvMDN + '.input1X')
        mc.connectAttr(input2X, ctrlDrvMDN + '.input2X')

        return ctrlDrvMDN

    def multOrDivSetAttr(self, name, prefix, nameExpr, side, input2XSet, input1X, operation=2):
        ctrlDrvMDN = mc.createNode('multiplyDivide',
                                   n=au.prefix_name(name) + prefix + nameExpr + 'Ctrl' + side + '_mdn')
        mc.setAttr(ctrlDrvMDN + '.operation', operation)
        mc.connectAttr(input1X , ctrlDrvMDN + '.input1X')
        mc.setAttr(ctrlDrvMDN + '.input2X', input2XSet)

        return ctrlDrvMDN

    def pmaExpr(self, name, prefix, nameExpr, side, operation, input0, input1):
        ctrlDrvPMA = mc.createNode('plusMinusAverage', n=au.prefix_name(name)
                                                         + prefix + nameExpr + 'Grp' + side + '_pma')
        mc.setAttr(ctrlDrvPMA + '.operation', operation)
        mc.connectAttr(input0, ctrlDrvPMA + '.input1D[0]')
        mc.connectAttr(input1, ctrlDrvPMA + '.input1D[1]')

        return ctrlDrvPMA

    def reverseNode(self, object, targetJnt, objectPrefix, side):

        transMdn = mc.createNode('multiplyDivide', n=au.prefix_name(objectPrefix) + 'Trans' + side + '_mdn')
        mc.connectAttr(object+'.translate', transMdn+'.input1')
        mc.setAttr(transMdn+'.input2X', -1)
        mc.connectAttr(transMdn+'.output', targetJnt +'.translate')

        rotMdn = mc.createNode('multiplyDivide', n=au.prefix_name(objectPrefix) + 'Rot' + side + '_mdn')
        mc.connectAttr(object+'.rotate', rotMdn+'.input1')
        mc.setAttr(rotMdn+'.input2Y', -1)
        mc.setAttr(rotMdn+'.input2Z', -1)
        mc.connectAttr(rotMdn+'.output', targetJnt+'.rotate')

    def replacePosLFTRGT(self, object):
        if self.sideRGT in object:
            newName = object.replace(self.sideRGT, '')
        elif self.sideLFT in object:
            newName = object.replace(self.sideLFT, '')
        else:
            newName = object

        return newName
