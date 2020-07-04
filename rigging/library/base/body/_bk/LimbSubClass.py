"""
creating limb module base
"""
import maya.cmds as mc
from rigLib.utils import rotation_controller as rc, controller as ct, transform as tf

from rigging.tools import AD_utils as au

reload (ct)
reload (tf)
reload (au)
reload (rc)

class Build:
    def __init__(self, prefix, prefixUpperLimb, prefixPoleVecLimb, prefixLowerLimb, prefixBaseOrTipLimb, prefixUpperLimbDtl,
                 prefixMiddleLimbDtl, prefixUpperLimbFk, prefixMiddleLimbFk, prefixLowerLimbFk, prefixUpperLimbIk,
                 prefixPoleVectorIk, prefixMiddleLimbIk, prefixLowerLimbIk, prefixEndLimbIk, prefixLimbSetup, side,
                 upperLimbJnt, middleLimbJnt, lowerLimbJnt, upperLimbFkJnt, middleLimbFkJnt, lowerLimbFkJnt,
                 upperLimbIkJnt, middleLimbIkJnt, poleVectorIkJnt, lowerLimbIkJnt, endLimbIkJnt, detailLimbDeformer,
                 numJoint, baseTipShapeJoint, upperLimbShapeJoint, poleVecLimbShapeJoint, lowerLimbShapeJoint, scale):

    ################################################# FK ###############################################################
    ### CREATE CONTROL FK
        self.controllerUpperLimbFk   = ct.Control(match_obj_first_position=upperLimbFkJnt, prefix='%s%s' % (prefixUpperLimbFk, side),
                                                  shape=ct.CIRCLEPLUS, groups_ctrl=['Zro', 'Offset'], ctrl_size=scale,
                                                  ctrl_color='yellow', gimbal=True, lock_channels=['v', 's'],
                                                  connection=['parentCons'])

        self.controllerMiddleLimbFk  = ct.Control(match_obj_first_position=middleLimbFkJnt, prefix='%s%s' % (prefixMiddleLimbFk, side),
                                                  shape=ct.CIRCLEPLUS, groups_ctrl=['Zro', 'Offset'], ctrl_size=scale,
                                                  ctrl_color='yellow', gimbal=True, lock_channels=['v', 's'],
                                                  connection=['parentCons'])

        self.controllerLowerLimbFk   = ct.Control(match_obj_first_position=lowerLimbFkJnt, prefix='%s%s' % (prefixLowerLimbFk, side),
                                                  shape=ct.CIRCLEPLUS, groups_ctrl=['Zro', 'Offset'], ctrl_size=scale,
                                                  ctrl_color='yellow', gimbal=True, lock_channels=['v', 's'],
                                                  connection=['parentCons'])

    ### ADD ATTRIBUTE FOR FK CONTROLLER
        au.add_attribute(objects=[self.controllerUpperLimbFk.control], long_name=['stretch'],
                         at="float", dv=0, keyable=True)
        # if arm:
        #     au.addAttribute(objects=[self.controllerUpperLimbFk.control], longName=['follow'],
        #                     at="enum", en='shoulder:hip:world:', k=True)
        # else:
        #     au.addAttribute(objects=[self.controllerUpperLimbFk.control], longName=['follow'],
        #                     at="enum", en='hip:world:', k=True)

        au.add_attribute(objects=[self.controllerMiddleLimbFk.control], long_name=['stretch'],
                         at="float", dv=0, keyable=True)

        ### FK LIMB SETUP
        self.upperStretchLimbFk = self.limbStretchFk(upLimbFkController=self.controllerUpperLimbFk.control,
                                                     side=side, downLimbFkJnt=middleLimbFkJnt)

        self.middleStretchLimbFk = self.limbStretchFk(upLimbFkController=self.controllerMiddleLimbFk.control,
                                                      side=side, downLimbFkJnt=lowerLimbFkJnt)


    ################################################# IK ###############################################################
        ### CREATE CONTROL IK
        self.controllerUpperLimbIk = ct.Control(match_obj_first_position=upperLimbIkJnt, prefix='%s%s' % (prefixUpperLimbIk, side), shape=ct.CUBE,
                                                groups_ctrl=['Zro', 'Offset'], ctrl_size=scale * 0.65,
                                                ctrl_color='red', gimbal=True, lock_channels=['v', 'r', 's'],
                                                connection=['pointCons'])

        self.controllerPoleVectorIk = ct.Control(match_obj_first_position=poleVectorIkJnt, prefix='%s%s' % (prefixPoleVectorIk, side), shape=ct.JOINT,
                                                 groups_ctrl=['Zro', 'Offset'], ctrl_size=scale * 0.25,
                                                 ctrl_color='red', gimbal=False, lock_channels=['v', 'r', 's'],
                                                 connection=['pointCons'])

        self.controllerLowerLimbIk = ct.Control(match_obj_first_position=lowerLimbIkJnt, prefix='%s%s' % (prefixLowerLimbIk, side), shape=ct.CUBE,
                                                groups_ctrl=['Zro', 'Offset'], ctrl_size=scale * 0.65,
                                                ctrl_color='red', gimbal=True, lock_channels=['v', 's']
                                                )

        self.limbAddAttrIk(controller=self.controllerLowerLimbIk.control, prefix=prefix, prefixPoleVectorIk=prefixPoleVectorIk)

    # ### ADD ATTRIBUTE FOR IK CONTROLLER
        # if arm:
        #     au.addAttribute(objects=[self.controllerPoleVectorIk.control], longName=['follow'],
        #                     at="long", min=0, max=1, dv=0, k=True)
        #
        #     self.limbAddAttrIk(arm=arm, controller=self.controllerLowerLimbIk.control, follow='shoulder:hip:world:',
        #                        prefix=prefix, prefixPoleVectorIk=prefixPoleVectorIk)
        # else:
        #     au.addAttribute(objects=[self.controllerPoleVectorIk.control], longName=['follow'],
        #                     at="long", min=0, max=1, dv=1, k=True)
        #
        #     self.limbAddAttrIk(arm=arm, controller=self.controllerLowerLimbIk.control, follow='hip:world:',
        #                    prefix=prefix, prefixPoleVectorIk=prefixPoleVectorIk)

    #### IK LIMB SETUP
        # IK HANDLE AND POLE VECTOR
        self.lowerLimbIkHdl = mc.ikHandle(sj=upperLimbIkJnt, ee=lowerLimbIkJnt, sol='ikRPsolver',
                                          n='%s%s_hdl' % (prefixLowerLimbIk, side))
        self.endLimbIkHdl = mc.ikHandle(sj=lowerLimbIkJnt, ee=endLimbIkJnt, sol='ikSCsolver', n='%s%s_hdl' % (prefixEndLimbIk, side))

        mc.poleVectorConstraint(self.controllerPoleVectorIk.control, self.lowerLimbIkHdl[0])
        mc.hide(self.endLimbIkHdl[0])


    # IK STRETCH, ELBOW SNAP, SLIDE JOINT AND SOFT IK SETUP
        # create joints for distance
        # upper limb distance
        mc.select(cl=1)
        self.posUpperLimbJnt = mc.joint(n='%s%s%s_jnt' % (prefixUpperLimbIk, 'Dist', side))
        mc.delete(mc.pointConstraint(upperLimbIkJnt, self.posUpperLimbJnt))

        # elbow distance
        mc.select(cl=1)
        self.posPoleVectorJnt = mc.joint(n='%s%s%s_jnt' % (prefixPoleVectorIk, 'Dist', side))
        mc.delete(mc.parentConstraint(poleVectorIkJnt, self.posPoleVectorJnt))
        mc.makeIdentity(self.posPoleVectorJnt, a=1, r=1, n=2, pn=1)

        # wrist distance
        mc.select(cl=1)
        self.posLowerLimbJnt = mc.joint(n='%s%s%s_jnt' % (prefixLowerLimbIk, 'Dist', side))
        mc.delete(mc.pointConstraint(lowerLimbIkJnt, self.posLowerLimbJnt))

        # aiming the pos upper limb joint to wrist joint
        mc.delete(mc.aimConstraint(self.posUpperLimbJnt, self.posLowerLimbJnt, o=(0, 0, 0), w=1.0, aim=(0, -1, 0), u=(-1, 0, 0),
                                   wut='vector', wu=(0, 1, 0)))
        mc.makeIdentity(self.posLowerLimbJnt, a=1, r=1, n=2, pn=1)

        # aiming the pos wrist joint to upper limb joint
        mc.delete(mc.aimConstraint(self.posLowerLimbJnt, self.posUpperLimbJnt, o=(0, 0, 0), w=1.0, aim=(0, 1, 0), u=(-1, 0, 0),
                                   wut='vector', wu=(0, 1, 0)))
        mc.makeIdentity(self.posUpperLimbJnt, a=1, r=1, n=2, pn=1)

        # softIk distance
        mc.select(cl=1)
        self.posSoftJnt = mc.duplicate(self.posLowerLimbJnt, name='%s%s%s_jnt' % (prefix, 'softIkDist', side))[0]

        # limb distance
        mc.select(cl=1)
        self.posLimbJnt = mc.duplicate(self.posLowerLimbJnt, name='%s%s%s_jnt' % (prefix, 'Dist', side))[0]

        # create distance node length of limb
        distanceMainIk = self.limbDistance(prefix=prefix, posUpJnt=self.posUpperLimbJnt, posLowJnt=self.posLimbJnt,
                                                distBetweenName='CtrlIkStretch', side=side)

        # create distance node from lower limb to soft ik jnt
        distanceLrSb = self.limbDistance(prefix=prefix, posUpJnt=self.posLowerLimbJnt, posLowJnt=self.posSoftJnt,
                                           distBetweenName='SoftIkStretch', side=side)

        # create distance node from upper limb to pole vector jnt
        distanceUaPv = self.limbDistance(prefix=prefixUpperLimbIk, posUpJnt=self.posUpperLimbJnt, posLowJnt=self.posPoleVectorJnt,
                                         distBetweenName='Snap', side=side)

        # create distance node from pole vector to soft ik jnt
        distancePvSb = self.limbDistance(prefix=prefixMiddleLimbIk, posUpJnt=self.posPoleVectorJnt, posLowJnt=self.posSoftJnt,
                                         distBetweenName='Snap', side=side)

        # parent and constraining the handle and some setup
        mc.parent(self.posLowerLimbJnt, self.posUpperLimbJnt)
        mc.parent(self.lowerLimbIkHdl[0], self.endLimbIkHdl[0], self.posSoftJnt)

        # get attribute value distance
        distanceMainIkValue = mc.getAttr(distanceMainIk + '.distance')

    ### SETTER VALUE FOR THE ATTRIBUTES
        # get value of tx wrist ik jnt
        getValueTxUpperLimbJnt = mc.xform(upperLimbIkJnt, ws=1, q=1, t=1)[0]

        # get attribute of total length joint
        lengthUpperLimb = mc.getAttr(middleLimbIkJnt + '.translateY')
        lengthMiddleLimb = mc.getAttr(lowerLimbIkJnt + '.translateY')

        if getValueTxUpperLimbJnt > 0:
            lengthUpperLimb *= 1
            lengthMiddleLimb *= 1
        else:
            lengthUpperLimb *= -1
            lengthMiddleLimb *= -1

        # sum and offset by adding 1
        jntIkMdLrSum = (lengthMiddleLimb + lengthUpperLimb)
        subtractIkJntDist = (jntIkMdLrSum - distanceMainIkValue)

        divMdValue = lengthUpperLimb / jntIkMdLrSum
        divLrValue = lengthMiddleLimb / jntIkMdLrSum

    ## CREATE SCALE IK NODES
        # decompose matrix soft Ik and slide
        self.scaleDecompose = mc.shadingNode('decomposeMatrix', asUtility=1, n='%s%s%s_dmtx' % (prefix, 'SoftSlideIkScale', side))
        self.scaleSoftSlideMdn = mc.shadingNode('multiplyDivide', asUtility=1, n='%s%s%s_mdn' % (prefix, 'SoftSlideIkScale', side))
        mc.setAttr(self.scaleSoftSlideMdn + '.operation', 2)
        mc.connectAttr(distanceMainIk + '.distance', self.scaleSoftSlideMdn + '.input1X')
        mc.connectAttr(self.scaleDecompose + '.outputScaleY', self.scaleSoftSlideMdn + '.input2X')

        # decompose matrix stretch
        self.scaleStretchSlideMdn = mc.shadingNode('multiplyDivide', asUtility=1, n='%s%s%s_mdn' % (prefix, 'StretchIkScale', side))
        mc.setAttr(self.scaleStretchSlideMdn + '.operation', 2)
        mc.connectAttr(distanceLrSb + '.distance', self.scaleStretchSlideMdn + '.input1X')
        mc.connectAttr(self.scaleDecompose + '.outputScaleY', self.scaleStretchSlideMdn + '.input2X')

        # decompose matrix snap middle limb
        self.scalePoleVecSnapMdMdn = mc.shadingNode('multiplyDivide', asUtility=1, n='%s%s%s_mdn' % (prefix, 'SnapUrIkScale', side))
        mc.setAttr(self.scalePoleVecSnapMdMdn + '.operation', 2)
        mc.connectAttr(distanceUaPv + '.distance', self.scalePoleVecSnapMdMdn + '.input1X')
        mc.connectAttr(self.scaleDecompose + '.outputScaleY', self.scalePoleVecSnapMdMdn + '.input2X')

        # decompose matrix snap lower limb
        self.scalePoleVecSnapLrMdn = mc.shadingNode('multiplyDivide', asUtility=1, n='%s%s%s_mdn' % (prefix, 'SnapLrIkScale', side))
        mc.setAttr(self.scalePoleVecSnapLrMdn + '.operation', 2)
        mc.connectAttr(distancePvSb + '.distance', self.scalePoleVecSnapLrMdn + '.input1X')
        mc.connectAttr(self.scaleDecompose + '.outputScaleY', self.scalePoleVecSnapLrMdn + '.input2X')

    ## SOFT IK SETUP
        # multiplier subtract sum joint with distance
        distDiv = mc.shadingNode('multiplyDivide', asUtility=1, n='%s%s%s_mdn' % (prefix, 'SoftIkMulSubtDist', side))
        mc.setAttr(distDiv + '.operation', 1)
        mc.setAttr(distDiv + '.input1X', subtractIkJntDist)
        mc.connectAttr(self.controllerLowerLimbIk.control + '.softIk', distDiv + '.input2X')

        # create condition node
        softIkCond = mc.shadingNode('condition', asUtility=1, n='%s%s%s_cnd' % (prefix, 'SoftIk', side))
        mc.setAttr(softIkCond + '.operation', 2)

        # connect the distance limb to soft ik condition node
        mc.connectAttr(self.scaleSoftSlideMdn + '.outputX', softIkCond + '.firstTerm')
        mc.connectAttr(self.scaleSoftSlideMdn + '.outputX', softIkCond + '.colorIfFalseR')

        # create pma for soft ik subtract between total length to soft ik
        softIkPmaSubt = mc.shadingNode('plusMinusAverage', asUtility=1, n='%s%s%s_pma' % (prefix, 'SoftIkSubtLength', side))
        mc.setAttr(softIkPmaSubt + '.operation', 2)
        mc.setAttr(softIkPmaSubt +'.input1D[0]', jntIkMdLrSum)
        mc.connectAttr(distDiv+'.outputX', softIkPmaSubt+'.input1D[1]')
        mc.connectAttr(softIkPmaSubt + '.output1D', softIkCond + '.secondTerm')

        # create pma for soft ik subtract between distance to soft ik
        softIkPmaDist = mc.shadingNode('plusMinusAverage', asUtility=1, n='%s%s%s_pma' % (prefix, 'SoftIkSubtDist', side))
        mc.setAttr(softIkPmaDist + '.operation', 2)
        mc.connectAttr(softIkPmaSubt + '.output1D', softIkPmaDist + '.input1D[1]')
        mc.connectAttr(self.scaleSoftSlideMdn + '.outputX', softIkPmaDist + '.input1D[0]')

        # create add double liniear for avoiding infitity number
        softIkAddDl = mc.shadingNode('addDoubleLinear', asUtility=1, n='%s%s%s_adl' % (prefix, 'SoftIkOffset', side))
        mc.connectAttr(self.controllerLowerLimbIk.control + '.softIk', softIkAddDl + '.input1')
        mc.setAttr(softIkAddDl + '.input2', 0.001)

        # create mdn total distance to soft ik value
        softIkDivDist = mc.shadingNode('multiplyDivide', asUtility=1, n='%s%s%s_mdn' % (prefix, 'SoftIkDivDist', side))
        mc.setAttr(softIkDivDist + '.operation', 2)
        mc.connectAttr(softIkPmaDist + '.output1D', softIkDivDist + '.input1X')
        mc.connectAttr(softIkAddDl + '.output', softIkDivDist + '.input2X')

        # create mdn for softIkDivDist multiply by -1
        softIkMulRev = mc.shadingNode('multiplyDivide', asUtility=1, n='%s%s%s_mdn' % (prefix, 'SoftIkRev', side))
        mc.setAttr(softIkMulRev + '.operation', 1)
        mc.connectAttr(softIkDivDist + '.outputX', softIkMulRev + '.input1X')
        mc.setAttr(softIkMulRev + '.input2X', -1)

        # create mdn for softIkMulRev power with exponent
        softIkExp = mc.shadingNode('multiplyDivide', asUtility=1, n='%s%s%s_mdn' % (prefix, 'SoftIkExp', side))
        mc.setAttr(softIkExp + '.operation', 3)
        mc.setAttr(softIkExp + '.input1X',  2.718282)
        mc.connectAttr(softIkMulRev + '.outputX', softIkExp + '.input2X')

        # create mdn for softIK multiply by exponent
        softIkMulExp = mc.shadingNode('multiplyDivide', asUtility=1, n='%s%s%s_mdn' % (prefix, 'SoftIkMulExp', side))
        mc.setAttr(softIkMulExp + '.operation', 1)
        mc.connectAttr(softIkExp + '.outputX', softIkMulExp + '.input1X')
        mc.connectAttr(distDiv + '.outputX', softIkMulExp + '.input2X')

        # create pma for multiply exponent subtracted by total length soft ik
        softIkPmaExp = mc.shadingNode('plusMinusAverage', asUtility=1, n='%s%s%s_pma' % (prefix, 'SoftIkSubtExp', side))
        mc.setAttr(softIkPmaExp + '.operation', 2)
        mc.setAttr(softIkPmaExp + '.input1D[0]', jntIkMdLrSum)
        mc.connectAttr(softIkMulExp + '.outputX', softIkPmaExp + '.input1D[1]')

        # create condition calcluation with exponent node
        softIkCondExp = mc.shadingNode('condition', asUtility=1, n='%s%s%s_cnd' % (prefix, 'SoftIkExp', side))
        mc.setAttr(softIkCondExp + '.operation', 2)
        # connect the controler wrist to soft ik exp condition node
        mc.connectAttr(self.controllerLowerLimbIk.control + '.softIk', softIkCondExp + '.firstTerm')
        mc.connectAttr(softIkPmaExp+ '.output1D', softIkCondExp + '.colorIfTrueR')
        mc.setAttr(softIkCondExp + '.colorIfFalseR', jntIkMdLrSum)

        # connect to the condition soft ik
        mc.connectAttr(softIkCondExp + '.outColorR', softIkCond + '.colorIfTrueR')

        # connect to position wrist distance
        mc.connectAttr(softIkCond + '.outColorR', self.posLowerLimbJnt + '.translateY')

    ## STRETCH IK SETUP

        # parent constraint the limb distance from controller gimbal
        mc.parentConstraint(self.controllerLowerLimbIk.control_gimbal, self.posLimbJnt)

        # create node for multiplying with the distance limb (upper limb and middle limb)
        # multiplier reverse stretch
        stretchIkMultiplier = mc.shadingNode('multiplyDivide', asUtility=1, n='%s%s%s_mdn' % (prefix, 'StretchIkMulRev', side))
        mc.setAttr(stretchIkMultiplier + '.operation', 1)

        # connect distance to multiplier
        mc.connectAttr(self.controllerLowerLimbIk.control + '.stretch', stretchIkMultiplier + '.input1X')

        if getValueTxUpperLimbJnt > 0:
            mc.setAttr(stretchIkMultiplier + ".input2X", 1)
        else:
            mc.setAttr(stretchIkMultiplier + ".input2X", -1)

        stretchIkUrSum = self.limbStretchIk(objPv='StretchIkUr', prefix=prefix, side=side, divValue=divMdValue,
                                       stretchIkMultiplier=stretchIkMultiplier, getValueTxUpperLimbJnt=getValueTxUpperLimbJnt,
                                       lengthLimb=lengthUpperLimb)

        stretchIkMdSum = self.limbStretchIk(objPv='StretchIkMd', prefix=prefix, side=side, divValue=divLrValue,
                                       stretchIkMultiplier=stretchIkMultiplier,
                                       getValueTxUpperLimbJnt=getValueTxUpperLimbJnt,
                                       lengthLimb=lengthMiddleLimb)

    ## SLIDE MIDDLE LIMB IK SETUP
        # setRange for slide middle limb
        slideIkSetR = mc.shadingNode('setRange', asUtility=1, n='%s%s%s_str' % (prefix, 'SlideIkMd', side))
        mc.connectAttr(self.controllerLowerLimbIk.control + '.%s%s' % (prefix, 'Slide'), slideIkSetR + '.valueX')
        mc.setAttr(slideIkSetR + '.minX', -1)
        mc.setAttr(slideIkSetR + '.maxX', 1)
        mc.setAttr(slideIkSetR + '.oldMinX', -10)
        mc.setAttr(slideIkSetR + '.oldMaxX', 10)

        # clamp for maximum value of slide
        slideIkClamp = mc.shadingNode('clamp', asUtility=1, n='%s%s%s_clm' % (prefix, 'SlideIkDist', side))
        mc.connectAttr(self.scaleSoftSlideMdn + '.outputX', slideIkClamp + '.minR')
        mc.setAttr(slideIkClamp + '.maxR', distanceMainIkValue)

        # condition if stretch on when slide on max
        slideIkMaxCon = mc.shadingNode('condition', asUtility=1, n='%s%s%s_cnd' % (prefix, 'SlideIkStretchOn', side))
        mc.setAttr(slideIkMaxCon + '.operation', 2)
        mc.connectAttr(self.controllerLowerLimbIk.control + '.stretch', slideIkMaxCon + '.firstTerm')
        mc.connectAttr(self.scaleSoftSlideMdn + '.outputX', slideIkMaxCon + '.colorIfTrueR')
        mc.connectAttr(slideIkClamp + '.outputR', slideIkMaxCon + '.colorIfFalseR')

        # create pma for result condition subtract to total value joint - distance
        slideIkPmaDiffJnt = mc.shadingNode('plusMinusAverage', asUtility=1, n='%s%s%s_pma' % (prefix, 'SlideIkSubtrJntDist', side))
        mc.setAttr(slideIkPmaDiffJnt + '.operation', 2)
        mc.connectAttr(slideIkMaxCon + '.outColorR', slideIkPmaDiffJnt + '.input1D[0]')
        mc.setAttr(slideIkPmaDiffJnt + '.input1D[1]', subtractIkJntDist)

        slideIkMdMulSetR = self.limbSlideSetRIk(prefix=prefix, side=side, objPv='SlideIkMd',
                                                slideIkPmaDiffJnt=slideIkPmaDiffJnt,
                                                divValue=divMdValue, slideIkSetR=slideIkSetR)

        slideIkLrMulSetR = self.limbSlideSetRIk(prefix=prefix, side=side, objPv='SlideIkLr',
                                                slideIkPmaDiffJnt=slideIkPmaDiffJnt,
                                                divValue=divLrValue, slideIkSetR=slideIkSetR)

        # create condition for both middle limb and wrist sliding
        slideIkMdLrCon = mc.shadingNode('condition', asUtility=1, n='%s%s%s_cnd' % (prefix, 'SlideIk', side))
        mc.setAttr(slideIkMdLrCon + '.operation', 4)
        mc.connectAttr(slideIkSetR + '.outValueX', slideIkMdLrCon + '.firstTerm')
        mc.connectAttr(slideIkMdMulSetR + '.outputX', slideIkMdLrCon + '.colorIfTrueR')
        mc.connectAttr(slideIkLrMulSetR + '.outputX', slideIkMdLrCon + '.colorIfFalseR')

        slideIkMdPmaStretch = self.limbSlidePmaStretchIk(objPv='SlideIkMd', prefix=prefix, side=side,
                                                         getValueTxUpperLimbJnt=getValueTxUpperLimbJnt,
                                                         operationOne=1, operationTwo=2, stretchIkSum=stretchIkUrSum,
                                                         slideIkMdLrCon=slideIkMdLrCon)

        slideIkLrPmaStretch = self.limbSlidePmaStretchIk(objPv='SlideIkLr', prefix=prefix, side=side,
                                                         getValueTxUpperLimbJnt=getValueTxUpperLimbJnt,
                                                         operationOne=2, operationTwo=1, stretchIkSum=stretchIkMdSum,
                                                         slideIkMdLrCon=slideIkMdLrCon)

    ## SLIDE COMBINE TO STRETCH ON/OFF
        # create pma for sum to total value joint - distance
        slideIkPmaSumDiffJnt = mc.shadingNode('plusMinusAverage', asUtility=1, n='%s%s%s_pma' % (prefix, 'SlideIkSumJntDist', side))
        mc.setAttr(slideIkPmaSumDiffJnt + '.operation', 1)
        mc.connectAttr(self.scaleSoftSlideMdn + '.outputX', slideIkPmaSumDiffJnt + '.input1D[0]')
        mc.setAttr(slideIkPmaSumDiffJnt + '.input1D[1]', subtractIkJntDist)

        # middle limb
        self.limbSlideCombineIk(objPv='SlideIkMd', prefix=prefix, side=side,
                                slideIkPmaSumDiffJnt=slideIkPmaSumDiffJnt,
                                divValue=divMdValue, distanceMainIkValue=distanceMainIkValue,
                                lengthLimb=lengthUpperLimb,
                                slideIkSetR=slideIkSetR, stretchIkSum=stretchIkUrSum)
        # lower limb
        self.limbSlideCombineIk(objPv='SlideIkLr', prefix=prefix, side=side,
                                slideIkPmaSumDiffJnt=slideIkPmaSumDiffJnt,
                                divValue=divLrValue, distanceMainIkValue=distanceMainIkValue,
                                lengthLimb=lengthMiddleLimb,
                                slideIkSetR=slideIkSetR, stretchIkSum=stretchIkMdSum)


    ## POLE VECTOR SNAP IK SETUP
        # parent constraint pole vector distance position
        mc.parentConstraint(self.controllerPoleVectorIk.control, self.posPoleVectorJnt, mo=1)

        # snap upper limb
        self.limbPoleVectorSnapIk(objPv='Md', getValueTxUpperLimbJnt=getValueTxUpperLimbJnt, prefix=prefix, side=side,
                                  prefixPoleVectorIk=prefixPoleVectorIk, slideIkPmaStretch=slideIkMdPmaStretch, limbIkJnt=middleLimbIkJnt,
                                  scalePoleVecSnapMdn=self.scalePoleVecSnapMdMdn)

        # snap middle limb
        self.limbPoleVectorSnapIk(objPv='Lr', getValueTxUpperLimbJnt=getValueTxUpperLimbJnt, prefix=prefix, side=side,
                              prefixPoleVectorIk=prefixPoleVectorIk, slideIkPmaStretch=slideIkLrPmaStretch,
                              limbIkJnt=lowerLimbIkJnt,
                              scalePoleVecSnapMdn=self.scalePoleVecSnapLrMdn)

    # ADD TWIST ATTRIBUTE
        mc.connectAttr('%s.twist' % self.controllerLowerLimbIk.control, '%s.twist' % self.lowerLimbIkHdl[0])

    ## CREATE CURVE FOR POLE VECTOR CONTROLLER
        self.curvePoleVectorIk = mc.curve(d=1, p=[(0, 0, 0), (0, 0, 0)], k=[0, 1], n=('%s%s_crv' % (prefixPoleVectorIk, side)))
        self.clusterBase, self.clusterBaseHdl =mc.cluster('%s.cv[0]' % self.curvePoleVectorIk, n='%s01%s_cls' % (prefixPoleVectorIk, side),
                                                          wn=(middleLimbIkJnt, middleLimbIkJnt))
        self.clusterPoleVector, self.clusterPoleVectorHdl =mc.cluster('%s.cv[1]' % self.curvePoleVectorIk, n='%s02%s_cls' % (prefixPoleVectorIk, side),
                                                                      wn=(self.controllerPoleVectorIk.control, self.controllerPoleVectorIk.control))

        # LOCK CURVE
        mc.setAttr('%s.template' % self.curvePoleVectorIk, 1)
        mc.setAttr('%s.template' % self.curvePoleVectorIk, lock=1)

        # ########################################### BLEND FOLLOW LIMB ###################################################
        #
        # if arm:
        #     # FK
        #     self.shoulderFk = self.limbFollowFK(prefixUpperLimbFk=prefixUpperLimbFk, upperLimbFkJnt=upperLimbFkJnt,
        #                                     locatorName='Shoulder', prefix=prefix, side=side, secondTerm=0)
        #
        #     mc.pointConstraint(self.shoulderFk, self.controllerUpperLimbFk.parentControl[0],
        #                                                mo=1)
        #     # hip
        #     self.hipFk = self.limbFollowFK(prefixUpperLimbFk=prefixUpperLimbFk, upperLimbFkJnt=upperLimbFkJnt,
        #                                    locatorName='Hip', prefix=prefix, side=side, secondTerm=1)
        #     # World
        #     self.worldFk = self.limbFollowFK(prefixUpperLimbFk=prefixUpperLimbFk, upperLimbFkJnt=upperLimbFkJnt,
        #                                      locatorName='World', prefix=prefix, side=side, secondTerm=2)
        #
        #     # IK
        #     # shoulder
        #     self.shoulderIk = self.limbFollowIk(prefixUpperLimbIk=prefixUpperLimbIk, lowerLimbIkJnt=lowerLimbIkJnt,
        #                                         locatorName='Shoulder', prefix=prefix, side=side, secondTerm=0)
        #     # hip
        #     self.hipIk = self.limbFollowIk(prefixUpperLimbIk=prefixUpperLimbIk, lowerLimbIkJnt=lowerLimbIkJnt,
        #                                    locatorName='Hip', prefix=prefix, side=side, secondTerm=1)
        #     # World
        #     self.worldIk = self.limbFollowIk(prefixUpperLimbIk=prefixUpperLimbIk, lowerLimbIkJnt=lowerLimbIkJnt,
        #                                      locatorName='World', prefix=prefix, side=side, secondTerm=2)
        #
        # else:
        #     # FK
        #     # hip
        #     self.hipFk = self.limbFollowFK(prefixUpperLimbFk=prefixUpperLimbFk, upperLimbFkJnt=upperLimbFkJnt,
        #                                    locatorName='Hip', prefix=prefix, side=side, secondTerm=0)
        #     # World
        #     self.worldFk = self.limbFollowFK(prefixUpperLimbFk=prefixUpperLimbFk, upperLimbFkJnt=upperLimbFkJnt,
        #                                      locatorName='World', prefix=prefix, side=side, secondTerm=1)
        #
        #     mc.pointConstraint(self.hipFk, self.controllerUpperLimbFk.parentControl[0], mo=1)
        #
        #     # IK
        #     # hip
        #     self.hipIk = self.limbFollowIk(prefixUpperLimbIk=prefixUpperLimbIk, lowerLimbIkJnt=lowerLimbIkJnt,
        #                                    locatorName='Hip', prefix=prefix, side=side, secondTerm=0)
        #     # World
        #     self.worldIk = self.limbFollowIk(prefixUpperLimbIk=prefixUpperLimbIk, lowerLimbIkJnt=lowerLimbIkJnt,
        #                                      locatorName='World', prefix=prefix, side=side, secondTerm=1)
        #

    ################################################## FK/IK SETUP #####################################################
        ### CREATE CONTROL FK/IK SETUP
        self.controllerFKIKLimbSetup = ct.Control(match_obj_first_position=lowerLimbFkJnt, prefix='%s%s' % (prefixLimbSetup, side),
                                                  shape=ct.STICKCIRCLE,
                                                  groups_ctrl=['Zro'], ctrl_size=scale,
                                                  ctrl_color='navy', lock_channels=['v', 't', 'r', 's'])

        ### FK/IK SETUP VISIBILITY ATTRIBUTE CONTROLLER
        au.add_attr_transform(self.controllerFKIKLimbSetup.control, 'FkIk', 'long', keyable=True, min=0, max=1, dv=0)

        # create reverse node for FK on/off
        self.limbSetupRevs = mc.createNode('reverse', n=('%s%s%s_rev' % (prefix, 'FkIk', side)))

        # set on/off attribute FK
        au.connect_part_object(obj_base_connection='FkIk', target_connection='inputX', obj_name=self.controllerFKIKLimbSetup.control,
                               target_name=[self.limbSetupRevs], select_obj=False)

        au.connect_part_object(obj_base_connection='outputX', target_connection='visibility', obj_name=self.limbSetupRevs,
                               target_name=[self.controllerUpperLimbFk.parent_control[0]], select_obj=False)

        # set on/off attribute IK
        au.connect_part_object(obj_base_connection='FkIk', target_connection='visibility', obj_name=self.controllerFKIKLimbSetup.control,
                               target_name=[self.controllerUpperLimbIk.parent_control[0],
                                            self.controllerPoleVectorIk.parent_control[0],
                                            self.controllerLowerLimbIk.parent_control[0],
                                            self.curvePoleVectorIk],
                               select_obj=False)

        # EXTRA ATTRIBUTES
        au.add_attribute(objects=[self.controllerFKIKLimbSetup.control], long_name=['%s%s' % (prefix, 'MultTwist')],
                         at="float", min=0, max=1, dv=0.5, channel_box=True)
     #    else:
     #        au.addAttribute(objects=[self.controllerFKIKLimbSetup.control], longName=['%s%s' % (prefix, 'MultTwist')],
     #                        at="float", min=0, max=1, dv=0, cb=True)
     #
     # ############################################### SCALE FOOT ########################################################
     #        au.addAttribute(objects=[self.controllerFKIKLimbSetup.control], longName=['footScale'],
     #                        attributeType="float", dv=1, k=True)

        au.add_attribute(objects=[self.controllerFKIKLimbSetup.control], long_name=[prefix + 'Scale'],
                         attributeType="float", dv=1, keyable=True)

        if baseTipShapeJoint or upperLimbShapeJoint or poleVecLimbShapeJoint or lowerLimbShapeJoint:
            au.add_attribute(objects=[self.controllerFKIKLimbSetup.control], long_name=['cornerLimbShape'],
                             nice_name=[' '], at="enum",
                             en='Corner Limb Shape', channel_box=True)
        if baseTipShapeJoint:
            au.add_attribute(objects=[self.controllerFKIKLimbSetup.control], long_name=[prefixBaseOrTipLimb + 'Shape'],
                             attributeType="float", min=0, max=1, dv=0.5, channel_box=True)
        if upperLimbShapeJoint:
            au.add_attribute(objects=[self.controllerFKIKLimbSetup.control], long_name=[prefixUpperLimb + 'Shape'],
                             attributeType="float", min=0, max=1, dv=0.5, channel_box=True)
        if poleVecLimbShapeJoint:
            au.add_attribute(objects=[self.controllerFKIKLimbSetup.control], long_name=[prefixPoleVecLimb + 'Shape'],
                             attributeType="float", min=0, max=1, dv=0.5, channel_box=True)
        if lowerLimbShapeJoint:
            au.add_attribute(objects=[self.controllerFKIKLimbSetup.control], long_name=[prefixLowerLimb + 'Shape'],
                             attributeType="float", min=0, max=1, dv=0.5, channel_box=True)

    ############################################# FK/ IK BLEND #########################################################
        # upper limb
        self.limbSwitchFkIk(limbFkJnt=upperLimbFkJnt, limbIkJnt=upperLimbIkJnt, limbJnt=upperLimbJnt)

        # middle limb
        self.limbSwitchFkIk(limbFkJnt=middleLimbFkJnt, limbIkJnt=middleLimbIkJnt, limbJnt=middleLimbJnt)

        # lower limb
        self.limbSwitchFkIk(limbFkJnt=lowerLimbFkJnt, limbIkJnt=lowerLimbIkJnt, limbJnt=lowerLimbJnt)

    ######################################################## DETAIL ####################################################
        ## MID COMBINE DETAIL
        # create controller
        self.ctrlMidMiddleLimb = ct.Control(match_obj_first_position=middleLimbJnt, prefix=prefix + 'DtlCombine' + side, groups_ctrl=['Zro'],
                                            ctrl_size=scale * 0.75, ctrl_color='blue', shape=ct.LOCATOR)

        if detailLimbDeformer:
            # add attribute
            au.add_attribute(objects=[self.ctrlMidMiddleLimb.control], long_name=['twistSep'],
                             nice_name=[' '], at="enum", en='Twist', channel_box=True)
            au.add_attribute(objects=[self.ctrlMidMiddleLimb.control], long_name=['roll'],
                             at="float", keyable=True)

            # Add attributes: Volume attributes
            au.add_attribute(objects=[self.ctrlMidMiddleLimb.control], long_name=['volumeSep'],
                             nice_name=[' '], at="enum", en='Volume', channel_box=True)
            au.add_attribute(objects=[self.ctrlMidMiddleLimb.control], long_name=['volume'],
                             at="float", min=-1, max=1, keyable=True)
            au.add_attribute(objects=[self.ctrlMidMiddleLimb.control], long_name=['volumeMultiplier'],
                             at="float", min=1, dv=1, keyable=True)
            au.add_attribute(objects=[self.ctrlMidMiddleLimb.control], long_name=['volumePosition'],
                             dv=0, min= numJoint*-0.5, max= numJoint*0.5, at="float", keyable=True)

            # Add attributes: Sine attributes
            au.add_attribute(objects=[self.ctrlMidMiddleLimb.control], long_name=['sineSep'], nice_name=[' '],
                             attributeType='enum', en="Sine:", channel_box=True)
            au.add_attribute(objects=[self.ctrlMidMiddleLimb.control], long_name=['amplitude'],
                             attributeType="float", keyable=True)
            au.add_attribute(objects=[self.ctrlMidMiddleLimb.control], long_name=['wide'],
                             attributeType="float", keyable=True)
            au.add_attribute(objects=[self.ctrlMidMiddleLimb.control], long_name=['sineRotate'],
                             attributeType="float", keyable=True)
            au.add_attribute(objects=[self.ctrlMidMiddleLimb.control], long_name=['offset'],
                             attributeType="float", keyable=True)
            au.add_attribute(objects=[self.ctrlMidMiddleLimb.control], long_name=['twist'],
                             attributeType="float", keyable=True)
            au.add_attribute(objects=[self.ctrlMidMiddleLimb.control], long_name=['sineLength'],
                             min=0.1, dv=1, attributeType="float", keyable=True)

            # ROLL
            self.adlUpperLimbCombine = mc.createNode('addDoubleLinear', n=(prefixUpperLimbDtl + 'RollCombine' + side + '_adl'))
            mc.connectAttr(self.ctrlMidMiddleLimb.control + '.roll', self.adlUpperLimbCombine + '.input2')

            self.adlMiddleLimbCombine  = mc.createNode('addDoubleLinear', n=(prefixMiddleLimbDtl + 'RollCombine' + side + '_adl'))
            mc.connectAttr(self.ctrlMidMiddleLimb.control + '.roll', self.adlMiddleLimbCombine + '.input2')

        ## VOLUME POSITION
            ## upper limb
            self.volumePosMdlUr = self.limbVolumePosition(prefixLimbDtl=prefixUpperLimbDtl, side=side, operation=2, numJoint=numJoint,
                                    dvMin=0, dvMax=0.5, vMin=1, vMax=0)

            ## middle limb
            self.volumePosMdlMd = self.limbVolumePosition(prefixLimbDtl=prefixMiddleLimbDtl, side=side, operation=4, numJoint=numJoint,
                                    dvMin=-0.5, dvMax=0, vMin=0, vMax=1)


    # Add attributes: Extra attributes
        au.add_attribute(objects=[self.ctrlMidMiddleLimb.control], long_name=['extraSep'], nice_name=[' '], at="enum",
                         en='Extra',
                         channel_box=True)
        au.add_attribute(objects=[self.ctrlMidMiddleLimb.control], long_name=['detailBaseCtrlVis'], at="long", min=0, max=1, dv=0,
                         channel_box=True)

        # lock and hide attribute
        au.lock_hide_attr(['r', 's', 'v'], self.ctrlMidMiddleLimb.control)

    # adjusting the controller direction
        if getValueTxUpperLimbJnt > 0:
                rc.change_position(self.controllerFKIKLimbSetup.control, 'xz')
                rc.change_position(self.controllerFKIKLimbSetup.control, '-')
        else:
            rc.change_position(self.controllerFKIKLimbSetup.control, 'xz')

      ####################################### ADD ROTATION ORDER #######################################################
        #### FK
        # Fk controller
        self.limbRotationOrder(self.controllerUpperLimbFk.control)
        self.limbRotationOrder(self.controllerMiddleLimbFk.control)
        self.limbRotationOrder(self.controllerLowerLimbFk.control)

        ## Fk gimbal
        self.limbRotationOrder(self.controllerUpperLimbFk.control_gimbal)
        self.limbRotationOrder(self.controllerMiddleLimbFk.control_gimbal)
        self.limbRotationOrder(self.controllerLowerLimbFk.control_gimbal)

        #### IK
        # Ik controller
        self.limbRotationOrder(self.controllerLowerLimbIk.control)

        # Ik gimbal
        self.limbRotationOrder(self.controllerLowerLimbIk.control_gimbal)

    ############################################### FUNCTION ###########################################################
    def limbRotationOrder(self, controllerTgt):
        au.add_attribute(objects=[controllerTgt], long_name=['rotationOrder'],
                         at="enum", en='xyz:yzx:zxy:xzy:yxz:zyx:', keyable=True)

        mc.connectAttr(controllerTgt + '.rotationOrder', controllerTgt+'.rotateOrder')


    def limbFollowFK(self, prefixUpperLimbFk, upperLimbFkJnt, locatorName, prefix, side, secondTerm):
        # create locator
        locator = mc.spaceLocator(n='%s%s_loc' % (prefixUpperLimbFk + locatorName, side))

        # match locator position to upper limb
        mc.delete(mc.parentConstraint(upperLimbFkJnt, locator))

        self.blendLimbFkRotation = mc.orientConstraint(locator, self.controllerUpperLimbFk.parent_control[0])

        # create condition
        partLimbFolFkCnd = mc.shadingNode('condition', asUtility=1, n='%s%s%s_cnd' % (prefix, locatorName+'FkFollow',
                                                                                      side))
        mc.setAttr(partLimbFolFkCnd + '.secondTerm', secondTerm)
        mc.setAttr(partLimbFolFkCnd + '.colorIfTrueR', 1)
        mc.setAttr(partLimbFolFkCnd + '.colorIfFalseR', 0)
        mc.connectAttr(self.controllerUpperLimbFk.control + '.follow', partLimbFolFkCnd + '.firstTerm')

        # connect to orient constraint
        mc.connectAttr(partLimbFolFkCnd + '.outColorR',
                       ('%s.%sW%s' % (self.blendLimbFkRotation[0], locator[0], secondTerm)))

        return locator

    def limbFollowIk(self, prefixUpperLimbIk, lowerLimbIkJnt, locatorName, prefix, side, secondTerm):
        # create locator
        locator = mc.spaceLocator(n='%s%s_loc' % (prefixUpperLimbIk + locatorName, side))

        # match locator position to upper limb
        mc.delete(mc.parentConstraint(lowerLimbIkJnt, locator))

        self.blendLimbIkParent = mc.parentConstraint(locator,
                                                     self.controllerLowerLimbIk.parent_control[0])
        # create condition
        partLimbFolIkCnd = mc.shadingNode('condition', asUtility=1, n='%s%s%s_cnd' % (prefix, locatorName+ 'IkFollow', side))
        mc.setAttr(partLimbFolIkCnd + '.secondTerm', secondTerm)
        mc.setAttr(partLimbFolIkCnd + '.colorIfTrueR', 1)
        mc.setAttr(partLimbFolIkCnd + '.colorIfFalseR', 0)
        mc.connectAttr(self.controllerLowerLimbIk.control + '.follow', partLimbFolIkCnd + '.firstTerm')

        mc.connectAttr(partLimbFolIkCnd + '.outColorR',('%s.%sW%s' % (self.blendLimbIkParent[0], locator[0], secondTerm)))

        return locator

    def limbSwitchFkIk(self, limbFkJnt, limbIkJnt, limbJnt):

        limbBlendCons = mc.parentConstraint(limbFkJnt, limbIkJnt, limbJnt)

        # set on/off attribute Fk/Ik upper limb
        au.connect_part_object(obj_base_connection='outputX', target_connection='%sW0' % limbFkJnt, obj_name=self.limbSetupRevs,
                               target_name=limbBlendCons, select_obj=False)
        au.connect_part_object(obj_base_connection='FkIk', target_connection='%sW1' % limbIkJnt,
                               obj_name=self.controllerFKIKLimbSetup.control,
                               target_name=limbBlendCons, select_obj=False)

    def limbStretchFk(self, upLimbFkController, side, downLimbFkJnt):

        limbStretchOffset = mc.createNode('multDoubleLinear',
                                          n='%s%s%s_mdl' % (upLimbFkController, 'StretchOffset', side))
        au.add_attribute(objects=[limbStretchOffset], long_name=['offset'],
                         attributeType="float", dv=0.1, keyable=True)
        mc.connectAttr(limbStretchOffset + '.offset', limbStretchOffset + '.input1')

        # stretch value
        limbStretch = mc.createNode('multDoubleLinear', n='%s%s%s_mdl' % (upLimbFkController, 'Stretch', side))
        downLimbGrpTY = mc.getAttr('%s.translateY' % downLimbFkJnt)

        au.add_attribute(objects=[limbStretch], long_name=['offset'],
                         attributeType="float", dv=downLimbGrpTY, keyable=True)
        mc.connectAttr(limbStretch + '.offset', limbStretch + '.input1')

        # adding value
        limbAddOffset = mc.createNode('addDoubleLinear',
                                      n='%s%s%s_adl' % (upLimbFkController, 'AddOffset', side))
        au.add_attribute(objects=[limbAddOffset], long_name=['offset'],
                         attributeType="float", dv=downLimbGrpTY, keyable=True)

        mc.connectAttr(limbAddOffset + '.offset', limbAddOffset + '.input1')

        # connecting each other
        mc.connectAttr(upLimbFkController + '.stretch', limbStretchOffset + '.input2')
        mc.connectAttr(limbStretchOffset + '.output', limbStretch + '.input2')
        mc.connectAttr(limbStretch + '.output', limbAddOffset + '.input2')

        return limbAddOffset

    def limbStretchIk(self, objPv, prefix, side, divValue, stretchIkMultiplier, getValueTxUpperLimbJnt, lengthLimb):
        # limb
        stretchIkMulDist = mc.shadingNode('multiplyDivide', asUtility=1, n='%s%s%s%s_mdn' % (prefix, objPv, 'MulDist', side))
        mc.setAttr(stretchIkMulDist + '.operation', 1)
        mc.connectAttr(self.scaleStretchSlideMdn + '.outputX', stretchIkMulDist + '.input1X')
        mc.setAttr(stretchIkMulDist + '.input2X', divValue)

        # multiply by the control stretch
        stretchIkMulSet = mc.shadingNode('multiplyDivide', asUtility=1, n='%s%s%s%s_mdn' % (prefix, objPv, 'MulSet', side))
        mc.setAttr(stretchIkMulSet + '.operation', 1)
        mc.connectAttr(stretchIkMultiplier + '.outputX', stretchIkMulSet + '.input1X')
        mc.connectAttr(stretchIkMulDist + '.outputX', stretchIkMulSet + '.input2X')

        # adding respectively by it's joint length
        stretchIkSum = mc.shadingNode('plusMinusAverage', asUtility=1, n='%s%s%s%s_pma' % (prefix, objPv, 'Sum', side))
        if getValueTxUpperLimbJnt > 0:
            mc.setAttr(stretchIkSum + '.operation', 1)
        else:
            mc.setAttr(stretchIkSum + '.operation', 2)

        mc.connectAttr(stretchIkMulSet + '.outputX', stretchIkSum + '.input1D[0]')
        mc.setAttr(stretchIkSum + '.input1D[1]', lengthLimb)

        return stretchIkSum

    def limbSlideSetRIk(self, prefix, side, objPv, slideIkPmaDiffJnt, divValue, slideIkSetR):
        # create mdn for multiplying result slideIkPmaDiffJnt to divide limb joint and total joints
        slideIkMulSet = mc.shadingNode('multiplyDivide', asUtility=1,
                                       n='%s%s%s%s_mdn' % (prefix, objPv, 'MulSet', side))
        mc.setAttr(slideIkMulSet + '.operation', 1)
        mc.connectAttr(slideIkPmaDiffJnt + '.output1D', slideIkMulSet + '.input1X')
        mc.setAttr(slideIkMulSet + '.input2X', divValue)

        # create mdn for multiplying result slideIkFaMulSet to output slideIkSetR
        slideIkMulSetR = mc.shadingNode('multiplyDivide', asUtility=1,
                                        n='%s%s%s%s_mdn' % (prefix, objPv, 'MulSetR', side))
        mc.setAttr(slideIkMulSetR + '.operation', 1)
        mc.connectAttr(slideIkMulSet + '.outputX', slideIkMulSetR + '.input1X')
        mc.connectAttr(slideIkSetR + '.outValueX', slideIkMulSetR + '.input2X')

        return slideIkMulSetR

    def limbSlidePmaStretchIk(self, objPv, prefix, side, getValueTxUpperLimbJnt, operationOne, operationTwo, stretchIkSum, slideIkMdLrCon):
        # create pma for result limb condition sum to slideIkMdLrCon
        slideIkPmaStretch = mc.shadingNode('plusMinusAverage', asUtility=1,
                                           n='%s%s%s%s_pma' % (prefix, objPv, 'SumStretch', side))
        if getValueTxUpperLimbJnt > 0:
            mc.setAttr(slideIkPmaStretch + '.operation', operationOne)
        else:
            mc.setAttr(slideIkPmaStretch + '.operation', operationTwo)

        mc.connectAttr(stretchIkSum + '.output1D', slideIkPmaStretch + '.input1D[0]')
        mc.connectAttr(slideIkMdLrCon + '.outColorR', slideIkPmaStretch + '.input1D[1]')

        return slideIkPmaStretch

    def limbSlideCombineIk(self, objPv, prefix, side, slideIkPmaSumDiffJnt, divValue, distanceMainIkValue,
                           lengthLimb, slideIkSetR, stretchIkSum):

        # create mdn to multiply result slideIkPmaSumDiffJnt to divide limb joint and total joints
        slideIkMulSumPma = mc.shadingNode('multiplyDivide', asUtility=1,
                                          n='%s%s%s%s_mdn' % (prefix, objPv, 'MulSumPma', side))
        mc.setAttr(slideIkMulSumPma + '.operation', 1)
        mc.connectAttr(slideIkPmaSumDiffJnt + '.output1D', slideIkMulSumPma + '.input1X')
        mc.setAttr(slideIkMulSumPma + '.input2X', divValue)

        # create condition for limb to distance
        slideIkDistCon = mc.shadingNode('condition', asUtility=1, n='%s%s%s%s_cnd' % (prefix, objPv, 'Dist', side))
        mc.setAttr(slideIkDistCon + '.operation', 4)
        mc.connectAttr(self.scaleSoftSlideMdn + '.outputX', slideIkDistCon + '.firstTerm')
        mc.setAttr(slideIkDistCon + '.secondTerm', distanceMainIkValue)
        mc.connectAttr(slideIkMulSumPma + '.outputX', slideIkDistCon + '.colorIfTrueR')
        mc.setAttr(slideIkDistCon + '.colorIfFalseR', lengthLimb)

        # create condition limb slide to stretch min
        slideIkStretchCon = mc.shadingNode('condition', asUtility=1,
                                           n='%s%s%s%s_cnd' % (prefix, objPv, 'MdStretch', side))
        mc.setAttr(slideIkStretchCon + '.operation', 0)
        mc.connectAttr(slideIkSetR + '.outValueX', slideIkStretchCon + '.firstTerm')
        mc.setAttr(slideIkStretchCon + '.colorIfTrueR', lengthLimb)
        mc.connectAttr(slideIkDistCon + '.outColorR', slideIkStretchCon + '.colorIfFalseR')

        # connect condition  limb to pma stretchIkUrSum
        mc.connectAttr(slideIkStretchCon + '.outColorR', stretchIkSum + '.input1D[1]')

    def limbAddAttrIk(self, controller, prefix, prefixPoleVectorIk):
        au.add_attribute(objects=[controller], long_name=['%s%s' % (prefix, 'IkSetup')], nice_name=[' '], at="enum",
                         en='%s%s' % (prefix.capitalize(), ' Ik Setup'), channel_box=True)

        # au.addAttribute(objects=[controller], longName=['follow'],
        #                 at="enum", en=follow, k=True)

        au.add_attribute(objects=[controller], long_name=['stretch'],
                         at="float", min=0, max=1, dv=1, keyable=True)

        au.add_attribute(objects=[controller], long_name=['softIk'],
                         at="float", min=0, max=1, dv=0, keyable=True)

        au.add_attribute(objects=[controller], long_name=['%s%s' % (prefix, 'Slide')],
                         at="float", min=-10, max=10, dv=0, keyable=True)

        au.add_attribute(objects=[controller], long_name=['%s%s' % (prefixPoleVectorIk, 'Snap')],
                         at="float", min=0, max=1, dv=0, keyable=True)

        au.add_attribute(objects=[controller], long_name=['twist'],
                         at="float", dv=0, keyable=True)

    def limbDistance(self, prefix, posUpJnt, posLowJnt, distBetweenName, side):
        distanceNode = mc.shadingNode('distanceBetween', asUtility=1,
                                      n='%s%s%s_dist' % (prefix, distBetweenName, side))
        mc.connectAttr(posUpJnt + '.worldMatrix[0]', distanceNode + '.inMatrix1')
        mc.connectAttr(posLowJnt + '.worldMatrix[0]', distanceNode + '.inMatrix2')
        mc.connectAttr(posUpJnt + '.rotatePivotTranslate', distanceNode + '.point1')
        mc.connectAttr(posLowJnt + '.rotatePivotTranslate', distanceNode + '.point2')

        return distanceNode

    def limbPoleVectorSnapIk(self, getValueTxUpperLimbJnt, prefix, side, objPv, prefixPoleVectorIk, slideIkPmaStretch,
                             scalePoleVecSnapMdn, limbIkJnt):
        # snaplimb to pole vector
        poleVecSnapBta = mc.shadingNode('blendTwoAttr', asUtility=1,
                                        n='%s%s%s%s_bta' % (prefix, 'PoleVecSnapIk', objPv, side))
        poleVecMultRev = mc.shadingNode('multDoubleLinear', asUtility=1,
                                        n='%s%s%s%sRev_mdl' % (prefix, 'PoleVecSnapIk', objPv, side))
        if getValueTxUpperLimbJnt > 0:
            mc.setAttr(poleVecMultRev + '.input2', 1)
        else:
            mc.setAttr(poleVecMultRev + '.input2', -1)

        mc.connectAttr(self.controllerLowerLimbIk.control + '.%s%s' % (prefixPoleVectorIk, 'Snap'),
                       poleVecSnapBta + '.attributesBlender')
        mc.connectAttr(slideIkPmaStretch + '.output1D', poleVecSnapBta + '.input[0]')
        mc.connectAttr(scalePoleVecSnapMdn + '.outputX', poleVecMultRev + '.input1')
        mc.connectAttr(poleVecMultRev + '.output', poleVecSnapBta + '.input[1]')

        mc.connectAttr(poleVecSnapBta + '.output', limbIkJnt + '.translateY')

    def limbVolumePosition(self, prefixLimbDtl, side, operation, numJoint, dvMin, dvMax, vMin, vMax):
        ## upper limb
        # condition
        volumePosCnd = mc.shadingNode('condition', asUtility=1,
                                      n='%s%s%s_cnd' % (prefixLimbDtl, 'CombineVolumePos', side))
        mc.setAttr(volumePosCnd + '.operation', operation)
        mc.connectAttr(self.ctrlMidMiddleLimb.control + '.volumePosition', volumePosCnd + '.firstTerm')
        mc.connectAttr(self.ctrlMidMiddleLimb.control + '.volumePosition', volumePosCnd + '.colorIfFalseR')
        mc.connectAttr(self.ctrlMidMiddleLimb.control + '.volumePosition', volumePosCnd + '.colorIfTrueR')

        # add double linear
        volumePosMdl = mc.shadingNode('multDoubleLinear', asUtility=1,
                                      n='%s%s%s_mdl' % (prefixLimbDtl, 'CombineVolumePos', side))
        mc.connectAttr(self.ctrlMidMiddleLimb.control + '.volume', volumePosMdl + '.input2')

        # connect using keyframe inbetween
        # min
        mc.setDrivenKeyframe(volumePosMdl + '.input1',
                             cd=volumePosCnd + '.outColorR',
                             dv=dvMin, v=vMin, itt='linear', ott='linear')
        # max
        mc.setDrivenKeyframe(volumePosMdl + '.input1',
                             cd=volumePosCnd + '.outColorR',
                             dv=numJoint * dvMax, v=vMax, itt='linear', ott='linear')

        return  volumePosMdl

class BuildArm(Build):
    def __init__(self, prefix, prefixUpperLimb, prefixPoleVecLimb, prefixLowerLimb, prefixBaseOrTipLimb,
                 prefixUpperLimbDtl, prefixMiddleLimbDtl, prefixUpperLimbFk, prefixMiddleLimbFk, prefixLowerLimbFk,
                 prefixUpperLimbIk, prefixPoleVectorIk, prefixMiddleLimbIk, prefixLowerLimbIk, prefixEndLimbIk,
                 prefixLimbSetup, side, upperLimbJnt, middleLimbJnt, lowerLimbJnt, upperLimbFkJnt, middleLimbFkJnt,
                 lowerLimbFkJnt, upperLimbIkJnt, middleLimbIkJnt, poleVectorIkJnt, lowerLimbIkJnt, endLimbIkJnt,
                 detailLimbDeformer, numJoint, baseTipShapeJoint, upperLimbShapeJoint, poleVecLimbShapeJoint,
                 lowerLimbShapeJoint, scale):

        Build.__init__(self, prefix, prefixUpperLimb, prefixPoleVecLimb, prefixLowerLimb, prefixBaseOrTipLimb,
                         prefixUpperLimbDtl, prefixMiddleLimbDtl, prefixUpperLimbFk, prefixMiddleLimbFk, prefixLowerLimbFk,
                         prefixUpperLimbIk, prefixPoleVectorIk, prefixMiddleLimbIk, prefixLowerLimbIk, prefixEndLimbIk,
                         prefixLimbSetup, side, upperLimbJnt, middleLimbJnt, lowerLimbJnt, upperLimbFkJnt, middleLimbFkJnt,
                         lowerLimbFkJnt, upperLimbIkJnt, middleLimbIkJnt, poleVectorIkJnt, lowerLimbIkJnt, endLimbIkJnt,
                         detailLimbDeformer, numJoint, baseTipShapeJoint, upperLimbShapeJoint, poleVecLimbShapeJoint,
                         lowerLimbShapeJoint, scale)

        ### ADD ATTRIBUTE FOR FK ARM CONTROLLER
        au.add_attribute(objects=[self.controllerUpperLimbFk.control], long_name=['follow'],
                         at="enum", en='shoulder:hip:world:', keyable=True)

        ### ADD ATTRIBUTE FOR IK CONTROLLER
        au.add_attribute(objects=[self.controllerPoleVectorIk.control], long_name=['follow'],
                         at="long", min=0, max=1, dv=0, keyable=True)

        au.add_attribute(objects=[self.controllerLowerLimbIk.control], long_name=['follow'],
                         at="enum", en='shoulder:hip:world:', keyable=True)


        ### BLEND FOLLOW LIMB
        # FK
        self.shoulderFk = self.limbFollowFK(prefixUpperLimbFk=prefixUpperLimbFk, upperLimbFkJnt=upperLimbFkJnt,
                                        locatorName='Shoulder', prefix=prefix, side=side, secondTerm=0)

        mc.pointConstraint(self.shoulderFk, self.controllerUpperLimbFk.parent_control[0],
                           mo=1)
        # hip
        self.hipFk = self.limbFollowFK(prefixUpperLimbFk=prefixUpperLimbFk, upperLimbFkJnt=upperLimbFkJnt,
                                       locatorName='Hip', prefix=prefix, side=side, secondTerm=1)
        # World
        self.worldFk = self.limbFollowFK(prefixUpperLimbFk=prefixUpperLimbFk, upperLimbFkJnt=upperLimbFkJnt,
                                         locatorName='World', prefix=prefix, side=side, secondTerm=2)

        # IK
        # shoulder
        self.shoulderIk = self.limbFollowIk(prefixUpperLimbIk=prefixUpperLimbIk, lowerLimbIkJnt=lowerLimbIkJnt,
                                            locatorName='Shoulder', prefix=prefix, side=side, secondTerm=0)
        # hip
        self.hipIk = self.limbFollowIk(prefixUpperLimbIk=prefixUpperLimbIk, lowerLimbIkJnt=lowerLimbIkJnt,
                                       locatorName='Hip', prefix=prefix, side=side, secondTerm=1)
        # World
        self.worldIk = self.limbFollowIk(prefixUpperLimbIk=prefixUpperLimbIk, lowerLimbIkJnt=lowerLimbIkJnt,
                                         locatorName='World', prefix=prefix, side=side, secondTerm=2)

        ## EXTRA ATTRIBUTES SET
        mc.setAttr(self.controllerFKIKLimbSetup.control+'.MultTwist', 0.5)
        # au.addAttribute(objects=[self.controllerFKIKLimbSetup.control], longName=['%s%s' % (prefix, 'MultTwist')],
        #                 at="float", min=0, max=1, dv=0.5, cb=True)


class BuildLeg(Build):
    def __init__(self, prefix, prefixUpperLimb, prefixPoleVecLimb, prefixLowerLimb, prefixBaseOrTipLimb,
                 prefixUpperLimbDtl, prefixMiddleLimbDtl, prefixUpperLimbFk, prefixMiddleLimbFk, prefixLowerLimbFk,
                 prefixUpperLimbIk, prefixPoleVectorIk, prefixMiddleLimbIk, prefixLowerLimbIk, prefixEndLimbIk,
                 prefixLimbSetup, side, upperLimbJnt, middleLimbJnt, lowerLimbJnt, upperLimbFkJnt, middleLimbFkJnt,
                 lowerLimbFkJnt, upperLimbIkJnt, middleLimbIkJnt, poleVectorIkJnt, lowerLimbIkJnt, endLimbIkJnt,
                 detailLimbDeformer, numJoint, baseTipShapeJoint, upperLimbShapeJoint, poleVecLimbShapeJoint,
                 lowerLimbShapeJoint, scale):

        Build.__init__(self, prefix, prefixUpperLimb, prefixPoleVecLimb, prefixLowerLimb, prefixBaseOrTipLimb,
                         prefixUpperLimbDtl, prefixMiddleLimbDtl, prefixUpperLimbFk, prefixMiddleLimbFk, prefixLowerLimbFk,
                         prefixUpperLimbIk, prefixPoleVectorIk, prefixMiddleLimbIk, prefixLowerLimbIk, prefixEndLimbIk,
                         prefixLimbSetup, side, upperLimbJnt, middleLimbJnt, lowerLimbJnt, upperLimbFkJnt, middleLimbFkJnt,
                         lowerLimbFkJnt, upperLimbIkJnt, middleLimbIkJnt, poleVectorIkJnt, lowerLimbIkJnt, endLimbIkJnt,
                         detailLimbDeformer, numJoint, baseTipShapeJoint, upperLimbShapeJoint, poleVecLimbShapeJoint,
                         lowerLimbShapeJoint, scale)

        ### ADD ATTRIBUTE FOR FK LEG CONTROLLER
        au.add_attribute(objects=[self.controllerUpperLimbFk.control], long_name=['follow'],
                         at="enum", en='hip:world:', keyable=True)

        ### ADD ATTRIBUTE FOR IK CONTROLLER
        au.add_attribute(objects=[self.controllerPoleVectorIk.control], long_name=['follow'],
                         at="long", min=0, max=1, dv=1, keyable=True)

        au.add_attribute(objects=[self.controllerLowerLimbIk.control], long_name=['follow'],
                         at="enum", en='hip:world:', keyable=True)

        ### BLEND FOLLOW LIMB
        # FK
        # hip
        self.hipFk = self.limbFollowFK(prefixUpperLimbFk=prefixUpperLimbFk, upperLimbFkJnt=upperLimbFkJnt,
                                       locatorName='Hip', prefix=prefix, side=side, secondTerm=0)
        # World
        self.worldFk = self.limbFollowFK(prefixUpperLimbFk=prefixUpperLimbFk, upperLimbFkJnt=upperLimbFkJnt,
                                         locatorName='World', prefix=prefix, side=side, secondTerm=1)

        mc.pointConstraint(self.hipFk, self.controllerUpperLimbFk.parent_control[0], mo=1)

        # IK
        # hip
        self.hipIk = self.limbFollowIk(prefixUpperLimbIk=prefixUpperLimbIk, lowerLimbIkJnt=lowerLimbIkJnt,
                                       locatorName='Hip', prefix=prefix, side=side, secondTerm=0)
        # World
        self.worldIk = self.limbFollowIk(prefixUpperLimbIk=prefixUpperLimbIk, lowerLimbIkJnt=lowerLimbIkJnt,
                                         locatorName='World', prefix=prefix, side=side, secondTerm=1)

        ## EXTRA ATTRIBUTES
        mc.setAttr(self.controllerFKIKLimbSetup.control+'.MultTwist', 0)

        # au.addAttribute(objects=[self.controllerFKIKLimbSetup.control], longName=['%s%s' % (prefix, 'MultTwist')],
        #                 at="float", min=0, max=1, dv=0, cb=True)
        # scale foot
        au.add_attribute(objects=[self.controllerFKIKLimbSetup.control], long_name=['footScale'],
                         attributeType="float", dv=1, keyable=True)
