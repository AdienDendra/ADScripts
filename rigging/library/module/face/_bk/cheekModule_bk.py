from __builtin__ import reload

import maya.cmds as mc
from rigLib.rig.face import cheek as ck
from rigLib.utils import controller as ct, transform as tf

from rigging.tools import AD_utils as au

reload (ct)
reload (tf)
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
                 lowLipDriveCtrl,
                 nostrilDriveCtrlAttrCheekUp,
                 nostrilDriveCtrlAttrCheekUpTwo,
                 nostrilDriveCtrl,

                 cornerLipCtrlAttrCheekOutUp,
                 cornerLipCtrlAttrCheekOutLow,
                 headUpCtrl,
                 headLowCtrl
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
                         side=side)

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
                                            tyRangeOne=72.0, tyRangeTwo=16.0
                                            )

        # CHEEK OUT LOW
        cheekOutLowSet = self.setDriverCheek(expressionMidOutArea=True, nameExpr='OutLow', attributeOffset=cornerLipCtrlAttrCheekOutLow,
                                             objectPrefix=cheekOutLowPrefix, objectJoint= cheekOutLowJnt,
                                             side=side, scale=scale, constraint=[headLowJnt, jawJnt], w=[1.0, 0.5],
                                             groupDriverJnt=cheek.cheekOutLowJnt[0],
                                             controller=cornerLipCtrl, cheekJointParentOffset=cheek.cheekOutLowJnt[1],
                                             cheekJointParentZro=cheek.cheekOutLowJnt[0],
                                             cheekParentCtrlZro=cheek.cheekOutLowParentCtrlZro,
                                             cheekParentCtrlOffset=cheek.cheekOutLowParentCtrlOffset,
                                             cheekCtrl=cheek.cheekOutLowCtrl, cheekJnt=cheekOutLowJnt,
                                             valueDivTx=3.0, valueDivTy=3.0, tzRangeOne=6.0, tzRangeTwo=6.0,
                                             tyRangeOne=18.0, tyRangeTwo=4.0
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
                                          side=side, scale=scale, constraint=[headUpJnt,headLowJnt,jawJnt], w=[0.7, 0.2, 0.1],
                                          groupDriverJnt=cheek.cheekMidJnt[0],
                                          controller=cornerLipCtrl, cheekJointParentOffset=cheek.cheekMidJnt[1],
                                          cheekJointParentZro=cheek.cheekMidJnt[0],
                                          cheekParentCtrlZro=cheek.cheekMidParentCtrlZro,
                                          cheekParentCtrlOffset=cheek.cheekMidParentCtrlOffset,
                                          cheekCtrl=cheek.cheekMidCtrl, cheekJnt=cheekMidJnt,
                                          valueDivTx = 1.5, valueDivTy = 1.5, tzRangeOne = 4.0, tzRangeTwo = 4.0,
                                          tyRangeOne = 18.0, tyRangeTwo = 3.0
                                          )

        # CHEEK LOW
        cheekLowSet = self.setDriverCheek(expressionMidOutArea=True, nameExpr='Low', attributeOffset=cornerLipCtrlAttrCheekLow,
                                          objectPrefix=cheekLowPrefix, objectJoint= cheekLowJnt,
                                          side=side, scale=scale, constraint=[headLowJnt,jawJnt], w=[0.4,0.6],
                                          groupDriverJnt=cheek.cheekLowJnt[0],
                                          controller=cornerLipCtrl, cheekJointParentOffset=cheek.cheekLowJnt[1],
                                          cheekJointParentZro=cheek.cheekLowJnt[0],
                                          cheekParentCtrlZro=cheek.cheekLowParentCtrlZro,
                                          cheekParentCtrlOffset=cheek.cheekLowParentCtrlOffset,
                                          cheekCtrl=cheek.cheekLowCtrl, cheekJnt=cheekLowJnt,
                                          valueDivTx=1.5, valueDivTy=1.1, tzRangeOne=3.0, tzRangeTwo=3.0,
                                          tyRangeOne=9.0, tyRangeTwo=2.0
                                          )
        # CHEEK IN UP
        chekInUp = self.setDriverCheek(expressionInArea=True, nameExpr='InUp',
                                       objectPrefix=cheekInUpPrefix, objectJoint=cheekInUpJnt,
                                       side=side, scale=scale, constraint=[headLowJnt,jawJnt], w=[0.8, 0.2],
                                       groupDriverJnt=cheek.cheekInUpJnt[0],
                                       controller=cornerLipCtrl, cheekJointParentOffset=cheek.cheekInUpJnt[1],
                                       cheekJointParentZro=cheek.cheekInUpJnt[0],
                                       cheekParentCtrlZro=cheek.cheekInUpParentCtrlZro,
                                       cheekParentCtrlOffset=cheek.cheekInUpParentCtrlOffset,
                                       cheekCtrl=cheek.cheekInUpCtrl, cheekJnt=cheekInUpJnt,
                                       valueDivTx = 2.0, valueDivTy = 2.5, valueDivTz= 2.0,
                                       lipDriveCtrl=lipDriveCtrl, mouthCtrl=mouthCtrl
                                       )

        # CHEEK IN LOW
        chekInLow = self.setDriverCheek(cheekInLow=True, objectPrefix=cheekInLowPrefix, objectJoint=cheekInLowJnt,
                                        side=side, scale=scale, constraint=[cheekLowJnt, lowLipDriveCtrl, jawJnt], w=[0.25, 0.75, 1.0],
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
        mc.scaleConstraint(headLowCtrl, chekInUp, mo=1)
        mc.scaleConstraint(headLowCtrl, chekInLow, mo=1)

        mc.parent(cheekOutUpSet, cheekOutLowSet, cheekUpSet, cheekMidSet, cheekLowSet, chekInUp, chekInLow, setupDriverGrp)
    # ==================================================================================================================
    #                                       FUNCTION SETUP FOR PART CHEEK JOINTS
    # ==================================================================================================================

    def setDriverCheek(self, nameExpr='', attributeOffset='', attributeOffsetTwo='', objectPrefix='', objectJoint='',
                       side='', scale=None, groupDriverJnt='', cheekInLow=None,
                       valueDivTx=None, valueDivTy=None, valueDivTz=None,
                       tzRangeOne=None, tzRangeTwo=None, tyRangeOne=None, tyRangeTwo=None,
                       expressionMidOutArea=None, expressionInArea=None, expressionMidUpArea=None,
                       constraint=[], w=[], controller='', cheekJointParentOffset='', cheekJointParentZro='',
                       cheekParentCtrlZro='', cheekParentCtrlOffset='', cheekCtrl='', cheekJnt='',
                       lipDriveCtrl='', mouthCtrl=''
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

        for cons, value in zip(constraint, w):
            mc.parentConstraint(cons, parentDriver, mo=1, w=value)

        # mc.parentConstraint(parentDriver, groupDriverJnt, mo=1)
        # mc.scaleConstraint(parentDriver, groupDriverJnt, mo=1)
        au.connect_attr_object(parentDriver, groupDriverJnt)
        # mc.connectAttr(driver+'.translate', groupDriverJnt+'.translate')
        # mc.connectAttr(driver+'.rotate', groupDriverJnt+'.rotate')
        # mc.connectAttr(driver+'.scale', groupDriverJnt+'.scale')
        # au.connectAttrObject(driver, groupDriverJnt)

        # CORNER LIP FOR REVERSE
        # CREATE MULTIPLIER CONTROLLER
        controllerNew = self.replacePosLFTRGT(controller)
        driverNew = self.replacePosLFTRGT(driver)
        lipDriveCtrlNew = self.replacePosLFTRGT(lipDriveCtrl)
        mouthCtrlNew = self.replacePosLFTRGT(mouthCtrl)
        newCheekJointParentOffset = self.replacePosLFTRGT(cheekJointParentOffset)

        if expressionMidUpArea:
            # expressionUpCheek = "$rangeZ = 2 / {0}.{6}; " \
            #                     "$range = 2 / {0}.{7};" \
            #                     "{1}.translateX = {2}.translateX {3} {0}.translateX /$range;" \
            #                     "{1}.translateY = {2}.translateY + {0}.translateY /$range;" \
            #                     "{1}.rotateX = {2}.rotateX;" \
            #                     "{1}.rotateY = {2}.rotateY;" \
            #                     "{1}.rotateZ = {2}.rotateZ;" \
            #                     "if ({0}.translateY >= 0) " \
            #                     "{1}.translateZ = {2}.translateZ + {0}.translateZ / ($range * 2) + {0}.translateY / ($range * {4} * $rangeZ); " \
            #                     "else " \
            #                     "{1}.translateZ = {2}.translateZ + {0}.translateZ / ($range * 2) + {0}.translateY / ($range * {5} * $rangeZ);" \
            #     .format(controller, cheekJointParentOffset, driver, operator, tzRangeOne, tzRangeTwo, attributeOffset, attributeOffsetTwo)
            #
            # mc.expression(s=expressionUpCheek, n=nameExpr + side + '_expr', ae=0)

            rangeMidUpZ = controller +'.%s' % attributeOffset
            rangeMidUp = controller +'.%s' % attributeOffsetTwo

            # DIVIDED FOR RANGE
            ctrlDrvRangeMDN = mc.createNode('multiplyDivide', n=au.prefix_name(controllerNew) + 'Range' + nameExpr + 'Ctrl' + side + '_mdn')
            mc.setAttr(ctrlDrvRangeMDN + '.operation', 2)
            mc.setAttr(ctrlDrvRangeMDN + '.input1X', 2)
            mc.setAttr(ctrlDrvRangeMDN + '.input1Y', 2)
            mc.connectAttr(rangeMidUp, ctrlDrvRangeMDN + '.input2X')
            mc.connectAttr(rangeMidUpZ, ctrlDrvRangeMDN + '.input2Y')

            # DIVIDED BY CONTROLLER
            ctrlDrvTxTyMDN = mc.createNode('multiplyDivide', n=au.prefix_name(controllerNew) + 'TxTy' + nameExpr + 'Ctrl' + side + '_mdn')
            mc.setAttr(ctrlDrvTxTyMDN + '.operation', 2)
            mc.connectAttr(controller+'.translateX', ctrlDrvTxTyMDN + '.input1X')
            mc.connectAttr(controller+'.translateY', ctrlDrvTxTyMDN + '.input1Y')
            mc.connectAttr(ctrlDrvRangeMDN+'.outputX', ctrlDrvTxTyMDN + '.input2X')
            mc.connectAttr(ctrlDrvRangeMDN+'.outputX', ctrlDrvTxTyMDN + '.input2Y')

            # ADD OR SUBSTRACT FROM SET GRP
            ctrlDrvTxPMA = mc.createNode('plusMinusAverage', n=au.prefix_name(newCheekJointParentOffset)
                                                                    +'Tx'+nameExpr+'Grp'+side+'_pma')
            mc.setAttr(ctrlDrvTxPMA+'.operation', operator)
            mc.connectAttr(driver +'.translateX', ctrlDrvTxPMA + '.input1D[0]')
            mc.connectAttr(ctrlDrvTxTyMDN + '.outputX', ctrlDrvTxPMA + '.input1D[1]')

            ctrlDrvTyPMA = mc.createNode('plusMinusAverage', n=au.prefix_name(newCheekJointParentOffset)
                                                                    +'Ty'+nameExpr+'Grp'+side+'_pma')
            mc.connectAttr(driver +'.translateY', ctrlDrvTyPMA + '.input1D[0]')
            mc.connectAttr(ctrlDrvTxTyMDN + '.outputY', ctrlDrvTyPMA + '.input1D[1]')

            # TRANSLATE Z
            cornerLipDrvTzRangeMDL = mc.createNode('multDoubleLinear', n=au.prefix_name(controllerNew) + 'TzRange' + nameExpr + 'Ctrl' + side + '_mdl')
            mc.connectAttr(rangeMidUp, cornerLipDrvTzRangeMDL + '.input1')
            mc.setAttr(cornerLipDrvTzRangeMDL + '.input2', 2)

            # DIVIDED BY CONTROLLER
            ctrlDrvTzMDN = mc.createNode('multiplyDivide', n=au.prefix_name(controllerNew) + 'Tz' + nameExpr + 'Ctrl' + side + '_mdn')
            mc.setAttr(ctrlDrvTzMDN + '.operation', 2)
            mc.connectAttr(controller+'.translateZ', ctrlDrvTzMDN + '.input1X')
            mc.connectAttr(cornerLipDrvTzRangeMDL+'.output', ctrlDrvTzMDN + '.input2X')

            # ADD WITH SET CONTROLLER
            ctrlDrvTzDriverPMA = mc.createNode('plusMinusAverage', n=au.prefix_name(driverNew)
                                                                    +'Tz'+nameExpr+'Ctrl'+side+'_pma')
            mc.connectAttr(ctrlDrvTzMDN +'.outputX', ctrlDrvTzDriverPMA + '.input1D[0]')
            mc.connectAttr(driver + '.translateZ', ctrlDrvTzDriverPMA + '.input1D[1]')

            # MULT RANGE NORMAL
            cornerLipDrvTzRangeOneMDL = mc.createNode('multDoubleLinear', n=au.prefix_name(controllerNew) + 'TzRangeOne' + nameExpr + 'Ctrl' + side + '_mdl')
            mc.connectAttr(ctrlDrvRangeMDN+'.outputX', cornerLipDrvTzRangeOneMDL + '.input1')
            mc.setAttr(cornerLipDrvTzRangeOneMDL + '.input2', tzRangeOne)

            cornerLipDrvTzRangeTwoMDL = mc.createNode('multDoubleLinear', n=au.prefix_name(controllerNew) + 'TzRangeTwo' + nameExpr + 'Ctrl' + side + '_mdl')
            mc.connectAttr(ctrlDrvRangeMDN+'.outputX', cornerLipDrvTzRangeTwoMDL + '.input1')
            mc.setAttr(cornerLipDrvTzRangeTwoMDL + '.input2', tzRangeTwo)

            # MULT RANGE Z
            cornerLipDrvTzRangeZOneMDL = mc.createNode('multDoubleLinear', n=au.prefix_name(controllerNew) + 'TzRangeZOne' + nameExpr + 'Ctrl' + side + '_mdl')
            mc.connectAttr(cornerLipDrvTzRangeOneMDL+'.output', cornerLipDrvTzRangeZOneMDL + '.input1')
            mc.connectAttr(ctrlDrvRangeMDN + '.outputY', cornerLipDrvTzRangeZOneMDL + '.input2')

            cornerLipDrvTzRangeZTwoMDL = mc.createNode('multDoubleLinear', n=au.prefix_name(controllerNew) + 'TzRangeZTwo' + nameExpr + 'Ctrl' + side + '_mdl')
            mc.connectAttr(cornerLipDrvTzRangeTwoMDL+'.output', cornerLipDrvTzRangeZTwoMDL + '.input1')
            mc.connectAttr(ctrlDrvRangeMDN + '.outputY', cornerLipDrvTzRangeZTwoMDL + '.input2')

            # DIVIDE RANGE Z AND RANGE NORMAL
            ctrlDrvTzRangeOneTwoMDN = mc.createNode('multiplyDivide', n=au.prefix_name(controllerNew) + 'TzRangeOneTwo' + nameExpr + 'Ctrl' + side + '_mdn')
            mc.setAttr(ctrlDrvTzRangeOneTwoMDN + '.operation', 2)
            mc.connectAttr(controller+'.translateY', ctrlDrvTzRangeOneTwoMDN + '.input1X')
            mc.connectAttr(controller+'.translateY', ctrlDrvTzRangeOneTwoMDN + '.input1Y')
            mc.connectAttr(cornerLipDrvTzRangeZOneMDL+'.output', ctrlDrvTzRangeOneTwoMDN + '.input2X')
            mc.connectAttr(cornerLipDrvTzRangeZTwoMDL+'.output', ctrlDrvTzRangeOneTwoMDN + '.input2Y')

            # ADD WITH SET CONTROLLER
            ctrlDrvTzRangePMA = mc.createNode('plusMinusAverage', n=au.prefix_name(newCheekJointParentOffset)
                                                                    +'TzRange'+nameExpr+'Grp'+side+'_pma')
            mc.connectAttr(ctrlDrvTzRangeOneTwoMDN+'.outputX',ctrlDrvTzRangePMA +'.input2D[0].input2Dx')
            mc.connectAttr(ctrlDrvTzRangeOneTwoMDN+'.outputY',ctrlDrvTzRangePMA +'.input2D[0].input2Dy')
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
        #     expressionMidCheek = "$range = {0}.{10}; " \
        #                           "{1}.translateX = {2}.translateX + {0}.translateX * {3} *$range / {4}; " \
        #                           "{1}.translateY = {2}.translateY + {0}.translateY *$range / {5}; " \
        #                           "{1}.rotateX = {2}.rotateX; " \
        #                           "{1}.rotateY = {2}.rotateY;" \
        #                           "{1}.rotateZ = {2}.rotateZ; " \
        #                           "if ({0}.translateY <= 0)" \
        #                           "{1}.translateZ = {2}.translateZ + {0}.translateZ *$range / {6} + {0}.translateY * $range / {8};" \
        #                           "else " \
        #                           "{1}.translateZ = {2}.translateZ + {0}.translateZ *$range / {7} + {0}.translateY * $range / {9};" \
        # \
        #         .format(controller, cheekJointParentOffset, driver, multiplier,
        #                 valueDivTx, valueDivTy, tzRangeOne, tzRangeTwo, tyRangeOne, tyRangeTwo, attributeOffset)
        #
        #     mc.expression(s=expressionMidCheek, n=nameExpr + side + '_expr', ae=0)
            cornerLipDrvTxMDL = mc.createNode('multDoubleLinear', n=au.prefix_name(controllerNew) + 'Tx' + nameExpr + 'Ctrl' + side + '_mdl')
            mc.connectAttr(controller + '.translateX', cornerLipDrvTxMDL + '.input1')
            mc.setAttr(cornerLipDrvTxMDL + '.input2', multiplier)

            rangeMidOut = controller +'.%s' % attributeOffset

            # CREATE MULTIPLY FOR CONTROLLER
            cornerLipDrvTransLowMDN = mc.createNode('multiplyDivide',
                                                    n=au.prefix_name(controllerNew) + 'Trans' + nameExpr + 'Ctrl' + side + '_mdn')
            mc.connectAttr(cornerLipDrvTxMDL + '.output', cornerLipDrvTransLowMDN + '.input1X')
            mc.connectAttr(controller + '.translateY', cornerLipDrvTransLowMDN + '.input1Y')
            mc.connectAttr(rangeMidOut, cornerLipDrvTransLowMDN + '.input2X')
            mc.connectAttr(rangeMidOut, cornerLipDrvTransLowMDN + '.input2Y')

            # CREATE DIVIDED FOR CONTROLLER TO THE VALUE
            cornerLipDrvDivTransLowMDN = mc.createNode('multiplyDivide',
                                                    n=au.prefix_name(controllerNew) + 'DivTrans' + nameExpr + 'Ctrl' +
                                                      side + '_mdn')

            mc.setAttr(cornerLipDrvDivTransLowMDN+'.operation', 2)
            mc.connectAttr(cornerLipDrvTransLowMDN + '.outputX', cornerLipDrvDivTransLowMDN + '.input1X')
            mc.connectAttr(cornerLipDrvTransLowMDN + '.outputY', cornerLipDrvDivTransLowMDN + '.input1Y')
            mc.setAttr(cornerLipDrvDivTransLowMDN+'.input2X', valueDivTx)
            mc.setAttr(cornerLipDrvDivTransLowMDN+'.input2Y', valueDivTy)

            # CREATE PLUS MINUS AVERAGE CHEEK LOW TX AND TY SET AND CONTROLLER
            cheekLowCornerLipDrvTxTyPMA = mc.createNode('plusMinusAverage', n=au.prefix_name(newCheekJointParentOffset)
                                                                    +'TxTy'+nameExpr+'Grp'+side+'_pma')

            mc.connectAttr(cornerLipDrvDivTransLowMDN +'.outputX', cheekLowCornerLipDrvTxTyPMA + '.input2D[0].input2Dx')
            mc.connectAttr(cornerLipDrvDivTransLowMDN + '.outputY', cheekLowCornerLipDrvTxTyPMA + '.input2D[0].input2Dy')
            mc.connectAttr(driver +'.translateX', cheekLowCornerLipDrvTxTyPMA + '.input2D[1].input2Dx')
            mc.connectAttr(driver + '.translateY', cheekLowCornerLipDrvTxTyPMA + '.input2D[1].input2Dy')

            # CONNECTION TY
            cornerLipDrvTyMDL = mc.createNode('multDoubleLinear',
                                              n=au.prefix_name(controllerNew) + 'TyTrans' + nameExpr + 'Ctrl' + side + '_mdl')
            mc.connectAttr(controller + '.translateY', cornerLipDrvTyMDL + '.input1')
            mc.connectAttr(rangeMidOut, cornerLipDrvTyMDL + '.input2')

            # CREATE DIVIDED FOR TY CONTROLLER TO THE VALUE
            cornerLipDrvTyDivTransLowMDN = mc.createNode('multiplyDivide',
                                                         n=au.prefix_name(controllerNew) + 'DivTyTrans' + nameExpr + 'Ctrl' + side + '_mdn')

            mc.setAttr(cornerLipDrvTyDivTransLowMDN+'.operation', 2)
            mc.connectAttr(cornerLipDrvTyMDL + '.output', cornerLipDrvTyDivTransLowMDN + '.input1X')
            mc.connectAttr(cornerLipDrvTyMDL + '.output', cornerLipDrvTyDivTransLowMDN + '.input1Y')
            mc.setAttr(cornerLipDrvTyDivTransLowMDN+'.input2X', tyRangeOne)
            mc.setAttr(cornerLipDrvTyDivTransLowMDN+'.input2Y', tyRangeTwo)

            # CONNECTION TZ
            cornerLipDrvTzMDL = mc.createNode('multDoubleLinear',
                                              n=au.prefix_name(controllerNew) + 'TzTrans' + nameExpr + 'Ctrl' + side + '_mdl')
            mc.connectAttr(controller + '.translateZ', cornerLipDrvTzMDL + '.input1')
            mc.connectAttr(rangeMidOut, cornerLipDrvTzMDL + '.input2')

            # CREATE DIVIDED FOR TZ CONTROLLER TO THE VALUE
            cornerLipDrvTzDivTransLowMDN = mc.createNode('multiplyDivide',
                                                         n=au.prefix_name(
                                                             controllerNew) + 'DivTzTrans'+nameExpr+'Ctrl' + side + '_mdn')
            mc.setAttr(cornerLipDrvTzDivTransLowMDN + '.operation', 2)
            mc.connectAttr(cornerLipDrvTzMDL + '.output', cornerLipDrvTzDivTransLowMDN + '.input1X')
            mc.connectAttr(cornerLipDrvTzMDL + '.output', cornerLipDrvTzDivTransLowMDN + '.input1Y')
            mc.setAttr(cornerLipDrvTzDivTransLowMDN + '.input2X', tzRangeOne)
            mc.setAttr(cornerLipDrvTzDivTransLowMDN + '.input2Y', tzRangeTwo)

            # CREATE PLUS MINUS FOR CONDITION
            cheekLowCornerLipDrvTzPMA = mc.createNode('plusMinusAverage', n=au.prefix_name(newCheekJointParentOffset)
                                                                            + 'Tz' + nameExpr + 'Grp' + side + '_pma')
            mc.connectAttr(cornerLipDrvTzDivTransLowMDN + '.outputX', cheekLowCornerLipDrvTzPMA + '.input2D[0].input2Dx')
            mc.connectAttr(cornerLipDrvTzDivTransLowMDN + '.outputY', cheekLowCornerLipDrvTzPMA + '.input2D[0].input2Dy')
            mc.connectAttr(cornerLipDrvTyDivTransLowMDN + '.outputX', cheekLowCornerLipDrvTzPMA + '.input2D[1].input2Dx')
            mc.connectAttr(cornerLipDrvTyDivTransLowMDN + '.outputY', cheekLowCornerLipDrvTzPMA + '.input2D[1].input2Dy')

            mc.connectAttr(driver + '.translateZ', cheekLowCornerLipDrvTzPMA + '.input2D[2].input2Dx')
            mc.connectAttr(driver + '.translateZ', cheekLowCornerLipDrvTzPMA + '.input2D[3].input2Dy')

            # CREATE CONDITION FOR TY AND TZ CONTROLLER
            cornerLipDrvTyDivTransLowCND = mc.createNode('condition',
                                                         n=au.prefix_name(controllerNew) + 'DivTyTrans' + nameExpr + 'Ctrl' + side + '_cnd')
            mc.setAttr(cornerLipDrvTyDivTransLowCND+'.operation', 4)
            mc.connectAttr(controller + '.translateY', cornerLipDrvTyDivTransLowCND + '.firstTerm')
            mc.connectAttr(cheekLowCornerLipDrvTzPMA + '.output2D.output2Dx', cornerLipDrvTyDivTransLowCND + '.colorIfTrueR')
            mc.connectAttr(cheekLowCornerLipDrvTzPMA + '.output2D.output2Dy', cornerLipDrvTyDivTransLowCND + '.colorIfFalseR')


            # CONNECT TRANSLATE TO OBJECT
            mc.connectAttr(cheekLowCornerLipDrvTxTyPMA + '.output2Dx', cheekJointParentOffset + '.translateX')
            mc.connectAttr(cheekLowCornerLipDrvTxTyPMA + '.output2Dy', cheekJointParentOffset + '.translateY')
            mc.connectAttr(cornerLipDrvTyDivTransLowCND + '.outColorR', cheekJointParentOffset + '.translateZ')

            # CONNECT ROTATE TO OBJECT
            au.connect_attr_rotate(controller, cheekJointParentOffset)

        if expressionInArea:
            # expressionInCheek = "{1}.translateX = {2}.translateX + {0}.translateX * {3} / {4} + {7}.translateX / 2 + {8}.translateX / 2; " \
            #                   "{1}.translateY = {2}.translateY + {0}.translateY  / {5} + {7}.translateY / 2 + {8}.translateY / 2; " \
            #                   "{1}.translateZ = {2}.translateZ + {0}.translateZ / {6} + {7}.translateZ / 2 + {8}.translateZ / 2; " \
            #                   "{1}.rotateX = {2}.rotateX; " \
            #                   "{1}.rotateY = {2}.rotateY;" \
            #                   "{1}.rotateZ = {2}.rotateZ; " \
            #     \
            #     .format(controller, cheekJointParentOffset, driver, multiplier,
            #             valueDivTx, valueDivTy, valueDivTz, lipDriveCtrl, mouthCtrl)
            #
            # mc.expression(s=expressionInCheek, n=nameExpr + side + '_expr', ae=0)

            # # CREATE MULTIPLIER CONTROLLER
            # controllerNew = self.replacePosLFTRGT(controller)
            # driverNew = self.replacePosLFTRGT(driver)
            # lipDriveCtrlNew = self.replacePosLFTRGT(lipDriveCtrl)
            # mouthCtrlNew = self.replacePosLFTRGT(mouthCtrl)
            #
            # cornerLipDrvTxMDL= mc.createNode('multDoubleLinear', n=au.prefixName(controllerNew) + 'TxCtrl' + side + '_mdl')
            # mc.connectAttr(controller +'.translateX', cornerLipDrvTxMDL + '.input1')
            # mc.setAttr(cornerLipDrvTxMDL + '.input2', multiplier)

            cornerLipDrvTxMDL = mc.createNode('multDoubleLinear', n=au.prefix_name(controllerNew) + 'Tx' + nameExpr + 'Ctrl' + side + '_mdl')
            mc.connectAttr(controller + '.translateX', cornerLipDrvTxMDL + '.input1')
            mc.setAttr(cornerLipDrvTxMDL + '.input2', multiplier)

            # CREATE DIVIDE CONTROLLER
            cornerLipDrvTransMDN= mc.createNode('multiplyDivide', n=au.prefix_name(controllerNew) + 'Trans' + nameExpr + 'Ctrl' + side + '_mdn')
            mc.setAttr(cornerLipDrvTransMDN + '.operation', 2)
            mc.connectAttr(cornerLipDrvTxMDL + '.output', cornerLipDrvTransMDN + '.input1X')
            mc.connectAttr(controller +'.translateY', cornerLipDrvTransMDN + '.input1Y')
            mc.connectAttr(controller +'.translateZ', cornerLipDrvTransMDN + '.input1Z')

            mc.setAttr(cornerLipDrvTransMDN + '.input2X', valueDivTx)
            mc.setAttr(cornerLipDrvTransMDN + '.input2Y', valueDivTy)
            mc.setAttr(cornerLipDrvTransMDN + '.input2Z', valueDivTz)

            # CREATE PLUS MINUS AVERAGE DRIVER AND CONTROLLER
            cheekInUpCornerLipDrvPMA = mc.createNode('plusMinusAverage', n=au.prefix_name(driverNew) +
                                                                           (au.prefix_name(controllerNew[0].capitalize() +
                                                                                           au.prefix_name(controllerNew[1:]))) + nameExpr + 'Ctrl' + side + '_pma')
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
            mouthCtrlTransMDN = mc.createNode('multiplyDivide',
                                              n=au.prefix_name(mouthCtrlNew) + 'Trans' + nameExpr + 'Ctrl' + side + '_mdn')
            mc.setAttr(mouthCtrlTransMDN + '.operation', 2)
            mc.connectAttr(mouthCtrl + '.translate', mouthCtrlTransMDN + '.input1')

            mc.setAttr(mouthCtrlTransMDN + '.input2X', 2)
            mc.setAttr(mouthCtrlTransMDN + '.input2Y', 2)
            mc.setAttr(mouthCtrlTransMDN + '.input2Z', 2)

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
