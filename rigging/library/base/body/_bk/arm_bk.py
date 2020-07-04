"""
creating arm module base
"""
import maya.cmds as mc
from rigLib.utils import rotation_controller as rc, controller as ct, transform as tf

from rigging.tools import AD_utils as au

reload (ct)
reload (tf)
reload (au)
reload (rc)

class Build:
    def __init__(self,
                 prefix,
                 prefixUpperArmDtl,
                 prefixForearmDtl,
                 prefixUpperArmFk,
                 prefixForearmFk,
                 prefixWristFk,
                 prefixUpperArmIk,
                 prefixElbowIk,
                 prefixForearmIk,
                 prefixWristIk,
                 prefixHandIk,
                 prefixArmSetup,
                 upperArmJnt,
                 forearmJnt,
                 wristJnt,
                 upperArmFkJnt,
                 forearmFkJnt,
                 wristFkJnt,
                 upperArmIkJnt,
                 forearmIkJnt,
                 elbowIKJnt,
                 wristIkJnt,
                 handIKJnt,
                 detailArmDeformer,
                 clavicleShapeJoint,
                 upperArmShapeJoint,
                 elbowShapeJoint,
                 wristShapeJoint,
                 numJoint,
                 scale,
                 side):

    ################################################# FK ###############################################################
    ### CREATE CONTROL FK
        self.controllerUpperArmFk = ct.Control(match_obj_first_position=upperArmFkJnt, prefix='%s%s' % (prefixUpperArmFk, side), shape=ct.CIRCLEPLUS,
                                               groups_ctrl=['Zro', 'Offset'], ctrl_size=scale,
                                               ctrl_color='yellow', gimbal=True, lock_channels=['v', 's'], connection=['parentCons'])

        self.controllerForeArmFk  = ct.Control(match_obj_first_position=forearmFkJnt, prefix='%s%s' % (prefixForearmFk, side), shape=ct.CIRCLEPLUS,
                                               groups_ctrl=['Zro', 'Offset'], ctrl_size=scale,
                                               ctrl_color='yellow', gimbal=True, lock_channels=['v', 's'], connection=['parentCons'])

        self.controllerWristFk    = ct.Control(match_obj_first_position=wristFkJnt, prefix='%s%s' % (prefixWristFk, side), shape=ct.CIRCLEPLUS,
                                               groups_ctrl=['Zro', 'Offset'], ctrl_size=scale,
                                               ctrl_color='yellow', gimbal=True, lock_channels=['v', 's'], connection=['parentCons'])


        ### ADD ATTRIBUTE FOR FK CONTROLLER
        au.add_attribute(objects=[self.controllerUpperArmFk.control], long_name=['stretch'],
                         at="float", dv=0, keyable=True)

        au.add_attribute(objects=[self.controllerUpperArmFk.control], long_name=['follow'],
                         at="enum", en='shoulder:hip:world:', keyable=True)

        au.add_attribute(objects=[self.controllerForeArmFk.control], long_name=['stretch'],
                         at="float", dv=0, keyable=True)

        ### FK ARM SETUP
        ## create node for stretch upperarm
        # offset value
        upperArmStretchOffset = mc.createNode('multDoubleLinear', n='%s%s%s_mdl' % (prefixUpperArmFk, 'StretchOffset', side))
        au.add_attribute(objects=[upperArmStretchOffset], long_name=['offset'],
                         attributeType="float", dv=0.1, keyable=True)
        mc.connectAttr(upperArmStretchOffset + '.offset', upperArmStretchOffset + '.input1')

        # stretch value
        upperArmStretch = mc.createNode('multDoubleLinear', n='%s%s%s_mdl' % (prefixUpperArmFk , 'Stretch', side))
        forearmGrpTY = mc.getAttr('%s.translateY' % forearmFkJnt)

        au.add_attribute(objects=[upperArmStretch], long_name=['offset'],
                         attributeType="float", dv=forearmGrpTY, keyable=True)
        mc.connectAttr(upperArmStretch + '.offset', upperArmStretch + '.input1')

        # adding value
        self.upperArmAddOffset = mc.createNode('addDoubleLinear', n='%s%s%s_adl' % (prefixUpperArmFk, 'AddOffset', side))
        au.add_attribute(objects=[self.upperArmAddOffset], long_name=['offset'],
                         attributeType="float", dv=forearmGrpTY, keyable=True)

        mc.connectAttr(self.upperArmAddOffset + '.offset', self.upperArmAddOffset + '.input1')

        # connecting each other
        mc.connectAttr(self.controllerUpperArmFk.control + '.stretch', upperArmStretchOffset + '.input2')
        mc.connectAttr(upperArmStretchOffset + '.output', upperArmStretch + '.input2')
        mc.connectAttr(upperArmStretch + '.output', self.upperArmAddOffset + '.input2')

        ## create node for stretch forearm
        # offset value
        forearmStretchOffset = mc.createNode('multDoubleLinear', n='%s%s%s_mdl' % (prefixForearmFk , 'StretchOffset', side))
        au.add_attribute(objects=[forearmStretchOffset], long_name=['offset'],
                         attributeType="float", dv=0.1, keyable=True)
        mc.connectAttr(forearmStretchOffset + '.offset', forearmStretchOffset + '.input1')

        # stretch value
        forearmStretch = mc.createNode('multDoubleLinear', n='%s%s%s_mdl' % (prefixForearmFk , 'Stretch', side))
        forearmGrpTY = mc.getAttr('%s.translateY' % wristFkJnt)

        au.add_attribute(objects=[forearmStretch], long_name=['offset'],
                         attributeType="float", dv=forearmGrpTY, keyable=True)
        mc.connectAttr(forearmStretch + '.offset', forearmStretch + '.input1')

        # adding value
        self.forearmAddOffset = mc.createNode('addDoubleLinear', n='%s%s%s_adl' % (prefixForearmFk , 'AddOffset', side))
        au.add_attribute(objects=[self.forearmAddOffset], long_name=['offset'],
                         attributeType="float", dv=forearmGrpTY, keyable=True)
        mc.connectAttr(self.forearmAddOffset + '.offset', self.forearmAddOffset + '.input1')

        # connecting each other
        mc.connectAttr(self.controllerForeArmFk.control + '.stretch', forearmStretchOffset + '.input2')
        mc.connectAttr(forearmStretchOffset + '.output', forearmStretch + '.input2')
        mc.connectAttr(forearmStretch + '.output', self.forearmAddOffset + '.input2')



    ################################################# IK ###############################################################

        ### CREATE CONTROL IK
        self.controllerUpperArmIk = ct.Control(match_obj_first_position=upperArmIkJnt, prefix='%s%s' % (prefixUpperArmIk, side), shape=ct.CUBE,
                                               groups_ctrl=['Zro', 'Offset'], ctrl_size=scale * 0.65,
                                               ctrl_color='red', gimbal=True, lock_channels=['v', 'r', 's'],
                                               connection=['pointCons'])

        self.controllerElbowIk = ct.Control(match_obj_first_position=elbowIKJnt, prefix='%s%s' % (prefixElbowIk, side), shape=ct.PYRAMID,
                                            groups_ctrl=['Zro', 'Offset'], ctrl_size=scale * 0.25,
                                            ctrl_color='red', gimbal=False, lock_channels=['v', 'r', 's'],
                                            connection=['pointCons'])

        self.controllerWristIk = ct.Control(match_obj_first_position=wristIkJnt, prefix='%s%s' % (prefixWristIk, side), shape=ct.CUBE,
                                            groups_ctrl=['Zro', 'Offset'], ctrl_size=scale * 0.65,
                                            ctrl_color='red', gimbal=True, lock_channels=['v', 's']
                                            )

        ### ADD ATTRIBUTE FOR IK CONTROLLER

        au.add_attribute(objects=[self.controllerWristIk.control], long_name=['armIkSetup'], nice_name=[' '], at="enum",
                         en='Arm Ik Setup', channel_box=True)

        au.add_attribute(objects=[self.controllerWristIk.control], long_name=['follow'],
                         at="enum", en='shoulder:hip:world:', keyable=True)

        au.add_attribute(objects=[self.controllerWristIk.control], long_name=['stretch'],
                         at="float", min=0, max=1, dv=0, keyable=True)

        au.add_attribute(objects=[self.controllerWristIk.control], long_name=['softIk'],
                         at="float", min=0, max=1, dv=0, keyable=True)

        au.add_attribute(objects=[self.controllerWristIk.control], long_name=['slideForearm'],
                         at="float", min=-10, max=10, dv=0, keyable=True)

        au.add_attribute(objects=[self.controllerWristIk.control], long_name=['elbowSnap'],
                         at="float", min=0, max=1, dv=0, keyable=True)

        au.add_attribute(objects=[self.controllerWristIk.control], long_name=['twist'],
                         at="float", dv=0, keyable=True)

        au.add_attribute(objects=[self.controllerElbowIk.control], long_name=['follow'],
                         at="float", min=0, max=1, dv=0, keyable=True)

    #### IK ARM SETUP
        # IK HANDLE AND POLE VECTOR
        self.wristIkHdl = mc.ikHandle(sj=upperArmIkJnt, ee=wristIkJnt, sol='ikRPsolver',
                                      n='%s%s_hdl' % (prefixWristIk, side))
        self.handIkHdl = mc.ikHandle(sj=wristIkJnt, ee=handIKJnt, sol='ikSCsolver', n='%s%s_hdl' % (prefixHandIk, side))

        mc.poleVectorConstraint(self.controllerElbowIk.control, self.wristIkHdl[0])


    # IK STRETCH, ELBOW SNAP, SLIDE JOINT AND SOFT IK SETUP
        # create joints for distance
        # upperArm distance
        mc.select(cl=1)
        self.posUpperArmJnt = mc.joint(n='%s%s%s_jnt' % (prefixUpperArmIk, 'Dist', side))
        mc.delete(mc.pointConstraint(upperArmIkJnt, self.posUpperArmJnt))

        # elbow distance
        mc.select(cl=1)
        self.posElbowJnt = mc.joint(n='%s%s%s_jnt' % (prefixElbowIk, 'Dist', side))
        mc.delete(mc.parentConstraint(elbowIKJnt, self.posElbowJnt))
        mc.makeIdentity(self.posElbowJnt, a=1, r=1, n=2, pn=1)

        # wrist distance
        mc.select(cl=1)
        self.posWristJnt = mc.joint(n='%s%s%s_jnt' % (prefixWristIk, 'Dist', side))
        mc.delete(mc.pointConstraint(wristIkJnt, self.posWristJnt))

        # aiming the pos upperArm joint to wrist joint
        mc.delete(mc.aimConstraint(self.posUpperArmJnt, self.posWristJnt, o=(0, 0, 0), w=1.0, aim=(0, -1, 0), u=(-1, 0, 0),
                                   wut='vector', wu=(0, 1, 0)))
        mc.makeIdentity(self.posWristJnt, a=1, r=1, n=2, pn=1)

        # aiming the pos wrist joint to upperArm joint
        mc.delete(mc.aimConstraint(self.posWristJnt, self.posUpperArmJnt, o=(0, 0, 0), w=1.0, aim=(0, 1, 0), u=(-1, 0, 0),
                                   wut='vector', wu=(0, 1, 0)))
        mc.makeIdentity(self.posUpperArmJnt, a=1, r=1, n=2, pn=1)

        # softIk distance
        mc.select(cl=1)
        self.posSoftJnt = mc.duplicate(self.posWristJnt, name='%s%s%s_jnt' % ('softIk', 'Dist', side))[0]

        # arm distance
        mc.select(cl=1)
        self.posArmJnt = mc.duplicate(self.posWristJnt, name='%s%s%s_jnt' % (prefix, 'Dist', side))[0]


        # create distance node length of arm
        self.distanceMainIk = mc.shadingNode('distanceBetween', asUtility=1, n='%s%s%s_dist' % (prefix, 'CtrlIkStretch', side))
        mc.connectAttr(self.posUpperArmJnt + '.worldMatrix[0]', self.distanceMainIk + '.inMatrix1')
        mc.connectAttr(self.posArmJnt + '.worldMatrix[0]', self.distanceMainIk + '.inMatrix2')
        mc.connectAttr(self.posUpperArmJnt + '.rotatePivotTranslate', self.distanceMainIk + '.point1')
        mc.connectAttr(self.posArmJnt + '.rotatePivotTranslate', self.distanceMainIk + '.point2')

        # create distance node from wrist to soft ik jnt
        self.distanceWrSb = mc.shadingNode('distanceBetween', asUtility=1, n='%s%s%s_dist' % (prefix, 'SoftIkStretch', side))
        mc.connectAttr(self.posWristJnt + '.worldMatrix[0]', self.distanceWrSb + '.inMatrix1')
        mc.connectAttr(self.posSoftJnt + '.worldMatrix[0]', self.distanceWrSb + '.inMatrix2')
        mc.connectAttr(self.posWristJnt + '.rotatePivotTranslate', self.distanceWrSb + '.point1')
        mc.connectAttr(self.posSoftJnt + '.rotatePivotTranslate', self.distanceWrSb + '.point2')

        # create distance node from upperArm to elbow jnt
        self.distanceUaEb = mc.shadingNode('distanceBetween', asUtility=1,
                                           n='%s%s%s_dist' % (prefixUpperArmIk, 'Snap', side))
        mc.connectAttr(self.posUpperArmJnt + '.worldMatrix[0]', self.distanceUaEb + '.inMatrix1')
        mc.connectAttr(self.posElbowJnt + '.worldMatrix[0]', self.distanceUaEb + '.inMatrix2')
        mc.connectAttr(self.posUpperArmJnt + '.rotatePivotTranslate', self.distanceUaEb + '.point1')
        mc.connectAttr(self.posElbowJnt + '.rotatePivotTranslate', self.distanceUaEb + '.point2')

        # create distance node from elbow to soft ik jnt
        self.distanceEbSb = mc.shadingNode('distanceBetween', asUtility=1,
                                           n='%s%s%s_dist' % (prefixForearmIk, 'Snap', side))
        mc.connectAttr(self.posElbowJnt + '.worldMatrix[0]', self.distanceEbSb + '.inMatrix1')
        mc.connectAttr(self.posSoftJnt + '.worldMatrix[0]', self.distanceEbSb + '.inMatrix2')
        mc.connectAttr(self.posElbowJnt + '.rotatePivotTranslate', self.distanceEbSb + '.point1')
        mc.connectAttr(self.posSoftJnt + '.rotatePivotTranslate', self.distanceEbSb + '.point2')

        # parent and constraining the handle and some setup
        mc.parent(self.posWristJnt, self.posUpperArmJnt)
        mc.parent(self.wristIkHdl[0], self.handIkHdl[0], self.posSoftJnt)

        # get attribute value distance
        distanceMainIk = mc.getAttr(self.distanceMainIk + '.distance')

    ### SETTER VALUE FOR THE ATTRIBUTES
        # get value of tx wrist ik jnt
        getValueTxWristJnt = mc.xform(upperArmIkJnt, ws=1, q=1, t=1)[0]

        # get attribute of total length joint
        lengthUpperArm = mc.getAttr(forearmIkJnt + '.translateY')
        lengthForearm = mc.getAttr(wristIkJnt + '.translateY')

        if getValueTxWristJnt > 0:
            lengthUpperArm *= 1
            lengthForearm *= 1
        else:
            lengthUpperArm *= -1
            lengthForearm *= -1

        # sum and offset by adding 1
        jntIkFaWrSum = (lengthForearm + lengthUpperArm)
        subtractIkJntDist = (jntIkFaWrSum - (mc.getAttr(self.distanceMainIk + '.distance')))

        divFaValue = lengthUpperArm/jntIkFaWrSum
        divWrValue = lengthForearm/jntIkFaWrSum

    ## CREATE SCALE IK NODES
        # decompose matrix soft Ik and slide
        self.scaleDecompose = mc.shadingNode('decomposeMatrix', asUtility=1, n='%s%s%s_dmtx' % (prefix, 'SoftSlideIkScale', side))
        self.scaleSoftSlideMdn = mc.shadingNode('multiplyDivide', asUtility=1, n='%s%s%s_mdn' % (prefix, 'SoftSlideIkScale', side))
        mc.setAttr(self.scaleSoftSlideMdn + '.operation', 2)
        mc.connectAttr(self.distanceMainIk + '.distance', self.scaleSoftSlideMdn + '.input1X')
        mc.connectAttr(self.scaleDecompose + '.outputScaleY', self.scaleSoftSlideMdn + '.input2X')

        # decompose matrix stretch
        self.scaleStretchSlideMdn = mc.shadingNode('multiplyDivide', asUtility=1, n='%s%s%s_mdn' % (prefix, 'StretchIkScale', side))
        mc.setAttr(self.scaleStretchSlideMdn + '.operation', 2)
        mc.connectAttr(self.distanceWrSb + '.distance', self.scaleStretchSlideMdn + '.input1X')
        mc.connectAttr(self.scaleDecompose + '.outputScaleY', self.scaleStretchSlideMdn + '.input2X')

        # decompose matrix snap forearm
        self.scaleElbowSnapFaMdn = mc.shadingNode('multiplyDivide', asUtility=1, n='%s%s%s_mdn' % (prefix, 'SnapFaIkScale', side))
        mc.setAttr(self.scaleElbowSnapFaMdn + '.operation', 2)
        mc.connectAttr(self.distanceUaEb + '.distance', self.scaleElbowSnapFaMdn + '.input1X')
        mc.connectAttr(self.scaleDecompose + '.outputScaleY', self.scaleElbowSnapFaMdn + '.input2X')

        # decompose matrix snap wrist
        self.scaleElbowSnapWrMdn = mc.shadingNode('multiplyDivide', asUtility=1, n='%s%s%s_mdn' % (prefix, 'SnapWrIkScale', side))
        mc.setAttr(self.scaleElbowSnapWrMdn + '.operation', 2)
        mc.connectAttr(self.distanceEbSb + '.distance', self.scaleElbowSnapWrMdn + '.input1X')
        mc.connectAttr(self.scaleDecompose + '.outputScaleY', self.scaleElbowSnapWrMdn + '.input2X')

    ## SOFT IK SETUP
        # ik orient constraint
        mc.orientConstraint(self.controllerWristIk.control_gimbal, self.posSoftJnt, mo=1)

        # multiplier subtract sum joint with distance
        distDiv = mc.shadingNode('multiplyDivide', asUtility=1, n='%s%s%s_mdn' % (prefix, 'SoftIkMulSubtDist', side))
        mc.setAttr(distDiv + '.operation', 1)
        mc.setAttr(distDiv + '.input1X', subtractIkJntDist)
        mc.connectAttr(self.controllerWristIk.control + '.softIk', distDiv + '.input2X')

        # create condition node
        softIkCond = mc.shadingNode('condition', asUtility=1, n='%s%s%s_cnd' % (prefix, 'SoftIk', side))
        mc.setAttr(softIkCond + '.operation', 2)

        # connect the distance arm to soft ik condition node
        mc.connectAttr(self.scaleSoftSlideMdn + '.outputX', softIkCond + '.firstTerm')
        mc.connectAttr(self.scaleSoftSlideMdn + '.outputX', softIkCond + '.colorIfFalseR')

        # create pma for soft ik subtract between total length to soft ik
        softIkPmaSubt = mc.shadingNode('plusMinusAverage', asUtility=1, n='%s%s%s_pma' % (prefix, 'SoftIkSubtLength', side))
        mc.setAttr(softIkPmaSubt + '.operation', 2)
        mc.setAttr(softIkPmaSubt +'.input1D[0]', jntIkFaWrSum)
        mc.connectAttr(distDiv+'.outputX', softIkPmaSubt+'.input1D[1]')
        mc.connectAttr(softIkPmaSubt + '.output1D', softIkCond + '.secondTerm')

        # create pma for soft ik subtract between distance to soft ik
        softIkPmaDist = mc.shadingNode('plusMinusAverage', asUtility=1, n='%s%s%s_pma' % (prefix, 'SoftIkSubtDist', side))
        mc.setAttr(softIkPmaDist + '.operation', 2)
        mc.connectAttr(softIkPmaSubt + '.output1D', softIkPmaDist + '.input1D[1]')
        mc.connectAttr(self.scaleSoftSlideMdn + '.outputX', softIkPmaDist + '.input1D[0]')

        # create add double liniear for avoiding infitity number
        softIkaddDl = mc.shadingNode('addDoubleLinear', asUtility=1, n='%s%s%s_adl' % (prefix, 'SoftIkOffset', side))
        mc.connectAttr(self.controllerWristIk.control+'.softIk', softIkaddDl + '.input1')
        mc.setAttr(softIkaddDl + '.input2', 0.001)

        # create mdn total distance to soft ik value
        softIkDivDist = mc.shadingNode('multiplyDivide', asUtility=1, n='%s%s%s_mdn' % (prefix, 'SoftIkDivDist', side))
        mc.setAttr(softIkDivDist + '.operation', 2)
        mc.connectAttr(softIkPmaDist + '.output1D', softIkDivDist + '.input1X')
        mc.connectAttr(softIkaddDl + '.output', softIkDivDist + '.input2X')

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
        mc.setAttr(softIkPmaExp + '.input1D[0]', jntIkFaWrSum)
        mc.connectAttr(softIkMulExp + '.outputX', softIkPmaExp + '.input1D[1]')

        # create condition calcluation with exponent node
        softIkCondExp = mc.shadingNode('condition', asUtility=1, n='%s%s%s_cnd' % (prefix, 'SoftIkExp', side))
        mc.setAttr(softIkCondExp + '.operation', 2)
        # connect the controler wrist to soft ik exp condition node
        mc.connectAttr(self.controllerWristIk.control + '.softIk', softIkCondExp + '.firstTerm')
        mc.connectAttr(softIkPmaExp+ '.output1D', softIkCondExp + '.colorIfTrueR')
        mc.setAttr(softIkCondExp + '.colorIfFalseR', jntIkFaWrSum)

        # connect to the condition soft ik
        mc.connectAttr(softIkCondExp + '.outColorR', softIkCond + '.colorIfTrueR')

        # connect to position wrist distance
        mc.connectAttr(softIkCond + '.outColorR', self.posWristJnt + '.translateY')

    ## STRETCH IK SETUP
        # constraint the soft jnt from gimbal control and wrist distance
        stretchIkPointCons = mc.pointConstraint(self.controllerWristIk.control_gimbal, self.posWristJnt, self.posSoftJnt)
        # set the key driver key for stretch setup
        stretchIkRev = mc.shadingNode('reverse', asUtility=1, n='%s%s%s_rev' % (prefix, 'StretchIk', side))

        # connect the attribute stretch from the arm controller
        mc.connectAttr(self.controllerWristIk.control+'.stretch', stretchIkRev+'.inputX')
        mc.connectAttr(stretchIkRev+'.outputX', stretchIkPointCons[0]+('.%sW1' % self.posWristJnt))
        mc.connectAttr(self.controllerWristIk.control +'.stretch', stretchIkPointCons[0] + ('.%sW0' % self.controllerWristIk.control_gimbal))

        # parent constraint the arm distance from controller gimbal
        mc.parentConstraint(self.controllerWristIk.control_gimbal, self.posArmJnt)

        # create node for multiplying with the distance arm (upperArm and forearm)
        # multiplier reverse stretch
        stretchIkMultiplier = mc.shadingNode('multiplyDivide', asUtility=1, n='%s%s%s_mdn' % (prefix, 'StretchIkMulRev', side))
        mc.setAttr(stretchIkMultiplier + '.operation', 1)

        # connect distance to multiplier
        mc.connectAttr(self.controllerWristIk.control + '.stretch', stretchIkMultiplier + '.input1X')

        if getValueTxWristJnt > 0:
            mc.setAttr(stretchIkMultiplier + ".input2X", 1)
        else:
            mc.setAttr(stretchIkMultiplier + ".input2X", -1)

        # upperArm
        stretchIkUaMulDist = mc.shadingNode('multiplyDivide', asUtility=1, n='%s%s%s_mdn' % (prefix, 'StretchIkUaMulDist', side))
        mc.setAttr(stretchIkUaMulDist + '.operation', 1)
        mc.connectAttr(self.scaleStretchSlideMdn + '.outputX', stretchIkUaMulDist + '.input1X')
        mc.setAttr(stretchIkUaMulDist + '.input2X', divFaValue)

        # forearm
        stretchIkFaMulDist = mc.shadingNode('multiplyDivide', asUtility=1, n='%s%s%s_mdn' % (prefix, 'StretchIkFaMulDist', side))
        mc.setAttr(stretchIkFaMulDist + '.operation', 1)
        mc.connectAttr(self.scaleStretchSlideMdn + '.outputX', stretchIkFaMulDist + '.input1X')
        mc.setAttr(stretchIkFaMulDist + '.input2X', divWrValue)

        # multiply by the control stretch
        # upperArm
        stretchIkUaMulSet = mc.shadingNode('multiplyDivide', asUtility=1, n='%s%s%s_mdn' % (prefix, 'StretchIkUaMulSet', side))
        mc.setAttr(stretchIkUaMulSet + '.operation', 1)
        mc.connectAttr(stretchIkMultiplier + '.outputX', stretchIkUaMulSet + '.input1X')
        mc.connectAttr(stretchIkUaMulDist + '.outputX', stretchIkUaMulSet + '.input2X')

        # forearm
        stretchIkFaMulSet = mc.shadingNode('multiplyDivide', asUtility=1, n='%s%s%s_mdn' % (prefix, 'StretchIkFaMulSet', side))
        mc.setAttr(stretchIkFaMulSet + '.operation', 1)
        mc.connectAttr(stretchIkMultiplier + '.outputX', stretchIkFaMulSet + '.input1X')
        mc.connectAttr(stretchIkFaMulDist + '.outputX', stretchIkFaMulSet + '.input2X')

        # adding respectively by it's joint length
        # upperArm
        stretchIkUaSum = mc.shadingNode('plusMinusAverage', asUtility=1, n='%s%s%s_pma' % (prefix, 'StretchIkUaSum', side))
        if getValueTxWristJnt > 0:
            mc.setAttr(stretchIkUaSum+'.operation', 1)
        else:
            mc.setAttr(stretchIkUaSum + '.operation', 2)

        mc.connectAttr(stretchIkUaMulSet+ '.outputX', stretchIkUaSum + '.input1D[0]')
        mc.setAttr(stretchIkUaSum + '.input1D[1]', lengthUpperArm)

        # forearm
        stretchIkFaSum = mc.shadingNode('plusMinusAverage', asUtility=1, n='%s%s%s_pma' % (prefix, 'StretchIkFaSum', side))
        if getValueTxWristJnt > 0:
            mc.setAttr(stretchIkFaSum + '.operation', 1)
        else:
            mc.setAttr(stretchIkFaSum + '.operation', 2)

        mc.connectAttr(stretchIkFaMulSet+ '.outputX', stretchIkFaSum + '.input1D[0]')
        mc.setAttr(stretchIkFaSum + '.input1D[1]', lengthForearm)

    ## SLIDE FOREARM IK SETUP
        # setRange for slide forearm
        slideIkSetR = mc.shadingNode('setRange', asUtility=1, n='%s%s%s_str' % (prefix, 'SlideIkFa', side))
        mc.connectAttr(self.controllerWristIk.control + '.slideForearm', slideIkSetR + '.valueX')
        mc.setAttr(slideIkSetR + '.minX', -1)
        mc.setAttr(slideIkSetR + '.maxX', 1)
        mc.setAttr(slideIkSetR + '.oldMinX', -10)
        mc.setAttr(slideIkSetR + '.oldMaxX', 10)

        # clamp for maximum value of slide
        slideIkClamp = mc.shadingNode('clamp', asUtility=1, n='%s%s%s_clm' % (prefix, 'SlideIkDist', side))
        mc.connectAttr(self.scaleSoftSlideMdn + '.outputX', slideIkClamp + '.minR')
        mc.setAttr(slideIkClamp + '.maxR', distanceMainIk)

        # condition if stretch on when slide on max
        slideIkMaxCon = mc.shadingNode('condition', asUtility=1, n='%s%s%s_cnd' % (prefix, 'SlideIkStretchOn', side))
        mc.setAttr(slideIkMaxCon + '.operation', 2)
        mc.connectAttr(self.controllerWristIk.control + '.stretch', slideIkMaxCon + '.firstTerm')
        mc.connectAttr(self.scaleSoftSlideMdn + '.outputX', slideIkMaxCon + '.colorIfTrueR')
        mc.connectAttr(slideIkClamp + '.outputR', slideIkMaxCon + '.colorIfFalseR')

        # create pma for result condition subtract to total value joint - distance
        slideIkPmaDiffJnt = mc.shadingNode('plusMinusAverage', asUtility=1, n='%s%s%s_pma' % (prefix, 'SlideIkSubtrJntDist', side))
        mc.setAttr(slideIkPmaDiffJnt + '.operation', 2)
        mc.connectAttr(slideIkMaxCon + '.outColorR', slideIkPmaDiffJnt + '.input1D[0]')
        mc.setAttr(slideIkPmaDiffJnt + '.input1D[1]', subtractIkJntDist)

        # create mdn for multiplying result slideIkPmaDiffJnt to divide forearm joint and total joints
        slideIkFaMulSet = mc.shadingNode('multiplyDivide', asUtility=1, n='%s%s%s_mdn' % (prefix, 'SlideIkFaMulSet', side))
        mc.setAttr(slideIkFaMulSet + '.operation', 1)
        mc.connectAttr(slideIkPmaDiffJnt + '.output1D', slideIkFaMulSet + '.input1X')
        mc.setAttr(slideIkFaMulSet + '.input2X', divFaValue)

        # create mdn for multiplying result slideIkPmaDiffJnt to divide wrist joint and total joints
        slideIkWrMulSet = mc.shadingNode('multiplyDivide', asUtility=1, n='%s%s%s_mdn' % (prefix, 'SlideIkWrMulSet', side))
        mc.setAttr(slideIkWrMulSet + '.operation', 1)
        mc.connectAttr(slideIkPmaDiffJnt + '.output1D', slideIkWrMulSet + '.input1X')
        mc.setAttr(slideIkWrMulSet + '.input2X', divWrValue)

        # create mdn for multiplying result slideIkFaMulSet to output slideIkSetR
        slideIkFaMulSetR = mc.shadingNode('multiplyDivide', asUtility=1, n='%s%s%s_mdn' % (prefix, 'SlideIkFaMulSetR', side))
        mc.setAttr(slideIkFaMulSetR + '.operation', 1)
        mc.connectAttr(slideIkFaMulSet + '.outputX', slideIkFaMulSetR + '.input1X')
        mc.connectAttr(slideIkSetR + '.outValueX', slideIkFaMulSetR + '.input2X')

        # create mdn for multiplying result slideIkWrMulSet to output slideIkSetR
        slideIkWrMulSetR = mc.shadingNode('multiplyDivide', asUtility=1, n='%s%s%s_mdn' % (prefix, 'SlideIkWrMulSetR', side))
        mc.setAttr(slideIkWrMulSetR + '.operation', 1)
        mc.connectAttr(slideIkWrMulSet + '.outputX', slideIkWrMulSetR + '.input1X')
        mc.connectAttr(slideIkSetR + '.outValueX', slideIkWrMulSetR + '.input2X')

        # create condition for both forearm and wrist sliding
        slideIkFaWrCon = mc.shadingNode('condition', asUtility=1, n='%s%s%s_cnd' % (prefix, 'SlideIk', side))
        mc.setAttr(slideIkFaWrCon + '.operation', 4)
        mc.connectAttr(slideIkSetR + '.outValueX', slideIkFaWrCon + '.firstTerm')
        mc.connectAttr(slideIkFaMulSetR + '.outputX', slideIkFaWrCon + '.colorIfTrueR')
        mc.connectAttr(slideIkWrMulSetR+ '.outputX', slideIkFaWrCon + '.colorIfFalseR')

        # create pma for result forearm condition sum to slideIkFaWrCon
        slideIkFaPmaStretch = mc.shadingNode('plusMinusAverage', asUtility=1, n='%s%s%s_pma' % (prefix, 'SlideIkFaSumStretch', side))
        if getValueTxWristJnt > 0:
            mc.setAttr(slideIkFaPmaStretch+'.operation', 1)
        else:
            mc.setAttr(slideIkFaPmaStretch + '.operation', 2)

        mc.connectAttr(stretchIkUaSum + '.output1D', slideIkFaPmaStretch + '.input1D[0]')
        mc.connectAttr(slideIkFaWrCon + '.outColorR', slideIkFaPmaStretch + '.input1D[1]')

        # create pma for result wrist condition sum to slideIkFaWrCon
        slideIkWrPmaStretch = mc.shadingNode('plusMinusAverage', asUtility=1, n='%s%s%s_pma' % (prefix, 'SlideIkWrSumStretch', side))
        if getValueTxWristJnt > 0:
            mc.setAttr(slideIkWrPmaStretch + '.operation', 2)
        else:
            mc.setAttr(slideIkWrPmaStretch + '.operation', 1)

        mc.connectAttr(stretchIkFaSum + '.output1D', slideIkWrPmaStretch + '.input1D[0]')
        mc.connectAttr(slideIkFaWrCon + '.outColorR', slideIkWrPmaStretch + '.input1D[1]')

    ## SLIDE COMBINE TO STRETCH ON/OFF
        # create pma for sum to total value joint - distance
        slideIkPmaSumDiffJnt = mc.shadingNode('plusMinusAverage', asUtility=1, n='%s%s%s_pma' % (prefix, 'SlideIkSumJntDist', side))
        mc.setAttr(slideIkPmaSumDiffJnt + '.operation', 1)
        mc.connectAttr(self.scaleSoftSlideMdn + '.outputX', slideIkPmaSumDiffJnt + '.input1D[0]')
        mc.setAttr(slideIkPmaSumDiffJnt + '.input1D[1]', subtractIkJntDist)

        # create mdn to multiply result slideIkPmaSumDiffJnt to divide forearm joint and total joints
        slideIkFaMulSumPma = mc.shadingNode('multiplyDivide', asUtility=1, n='%s%s%s_mdn' % (prefix, 'SlideIkFaMulSumPma', side))
        mc.setAttr(slideIkFaMulSumPma + '.operation', 1)
        mc.connectAttr(slideIkPmaSumDiffJnt + '.output1D', slideIkFaMulSumPma + '.input1X')
        mc.setAttr(slideIkFaMulSumPma + '.input2X', divFaValue)

        # create mdn to multiply result slideIkPmaSumDiffJnt to divide wrist joint and total joints
        slideIkWrMulSumPma = mc.shadingNode('multiplyDivide', asUtility=1, n='%s%s%s_mdn' % (prefix, 'SlideIkWrMulSumPma', side))
        mc.setAttr(slideIkWrMulSumPma + '.operation', 1)
        mc.connectAttr(slideIkPmaSumDiffJnt + '.output1D', slideIkWrMulSumPma + '.input1X')
        mc.setAttr(slideIkWrMulSumPma + '.input2X', divWrValue)

        # create condition for forearm to distance
        slideIkFaDistCon = mc.shadingNode('condition', asUtility=1, n='%s%s%s_cnd' % (prefix, 'SlideIkFaDist', side))
        mc.setAttr(slideIkFaDistCon + '.operation', 4)
        mc.connectAttr(self.scaleSoftSlideMdn + '.outputX', slideIkFaDistCon + '.firstTerm')
        mc.setAttr(slideIkFaDistCon+'.secondTerm', distanceMainIk)
        mc.connectAttr(slideIkFaMulSumPma + '.outputX', slideIkFaDistCon + '.colorIfTrueR')
        mc.setAttr(slideIkFaDistCon + '.colorIfFalseR', lengthUpperArm)

        # create condition for wrist to distance
        slideIkWrDistCon = mc.shadingNode('condition', asUtility=1, n='%s%s%s_cnd' % (prefix, 'SlideIkWrDist', side))
        mc.setAttr(slideIkWrDistCon + '.operation', 4)
        mc.connectAttr(self.scaleSoftSlideMdn + '.outputX', slideIkWrDistCon + '.firstTerm')
        mc.setAttr(slideIkWrDistCon + '.secondTerm', distanceMainIk)
        mc.connectAttr(slideIkWrMulSumPma + '.outputX', slideIkWrDistCon + '.colorIfTrueR')
        mc.setAttr(slideIkWrDistCon + '.colorIfFalseR', lengthForearm)

        # create condition forearm slide to stretch min
        slideIkFaStretchCon = mc.shadingNode('condition', asUtility=1, n='%s%s%s_cnd' % (prefix, 'SlideIkFaStretch', side))
        mc.setAttr(slideIkFaStretchCon + '.operation', 0)
        mc.connectAttr(slideIkSetR+ '.outValueX', slideIkFaStretchCon + '.firstTerm')
        mc.setAttr(slideIkFaStretchCon + '.colorIfTrueR', lengthUpperArm)
        mc.connectAttr(slideIkFaDistCon + '.outColorR', slideIkFaStretchCon + '.colorIfFalseR')

        # create condition wrist slide to stretch min
        slideIkWrStretchCon = mc.shadingNode('condition', asUtility=1, n='%s%s%s_cnd' % (prefix, 'SlideIkWrStretch', side))
        mc.setAttr(slideIkWrStretchCon + '.operation', 0)
        mc.connectAttr(slideIkSetR + '.outValueX', slideIkWrStretchCon + '.firstTerm')
        mc.setAttr(slideIkWrStretchCon + '.colorIfTrueR', lengthForearm)
        mc.connectAttr(slideIkWrDistCon + '.outColorR', slideIkWrStretchCon + '.colorIfFalseR')

        # connect condition forearm to pma stretchIkUaSum
        mc.connectAttr(slideIkFaStretchCon+'.outColorR', stretchIkUaSum+'.input1D[1]')

        # connect condition wrist to pma stretchIkFaSum
        mc.connectAttr(slideIkWrStretchCon + '.outColorR', stretchIkFaSum + '.input1D[1]')

    ## ELBOW SNAP IK SETUP
        # parent constraint elbow distance position
        mc.parentConstraint(self.controllerElbowIk.control, self.posElbowJnt, mo=1)

        # snap upperArm forearm to elbow
        elbowSnapUaBta = mc.shadingNode('blendTwoAttr', asUtility=1, n='%s%s%s_bta' % (prefix, 'ElbowSnapIkFa', side))
        elbowMultFaRev = mc.shadingNode('multDoubleLinear', asUtility=1, n='%s%s%s_mdl' % (prefix, 'ElbowSnapIkFaRev', side))
        if getValueTxWristJnt > 0 :
            mc.setAttr(elbowMultFaRev + '.input2', 1)
        else:
            mc.setAttr(elbowMultFaRev + '.input2', -1)

        mc.connectAttr(self.controllerWristIk.control+'.elbowSnap', elbowSnapUaBta+'.attributesBlender')
        mc.connectAttr(slideIkFaPmaStretch + '.output1D', elbowSnapUaBta + '.input[0]')
        mc.connectAttr(self.scaleElbowSnapFaMdn +'.outputX', elbowMultFaRev + '.input1')
        mc.connectAttr(elbowMultFaRev + '.output', elbowSnapUaBta + '.input[1]')

        # snap forearm wrist to elbow
        elbowSnapFaBta = mc.shadingNode('blendTwoAttr', asUtility=1, n='%s%s%s_bta' % (prefix, 'ElbowSnapIkWr', side))
        elbowMultWrRev = mc.shadingNode('multDoubleLinear', asUtility=1, n='%s%s%s_mdl' % (prefix, 'ElbowSnapIkWrRev', side))
        if getValueTxWristJnt > 0:
            mc.setAttr(elbowMultWrRev + '.input2', 1)
        else:
            mc.setAttr(elbowMultWrRev + '.input2', -1)

        mc.connectAttr(self.controllerWristIk.control + '.elbowSnap', elbowSnapFaBta + '.attributesBlender')
        mc.connectAttr(slideIkWrPmaStretch + '.output1D', elbowSnapFaBta + '.input[0]')
        mc.connectAttr(self.scaleElbowSnapWrMdn + '.outputX', elbowMultWrRev + '.input1')
        mc.connectAttr(elbowMultWrRev + '.output', elbowSnapFaBta + '.input[1]')

        # connect to respective joints
        mc.connectAttr(elbowSnapUaBta + '.output', forearmIkJnt + '.translateY')
        mc.connectAttr(elbowSnapFaBta + '.output', wristIkJnt + '.translateY')

    # ADD TWIST ATTRIBUTE
        mc.connectAttr('%s.twist' % self.controllerWristIk.control, '%s.twist' % self.wristIkHdl[0])

    ## CREATE CURVE FOR ELBOW CONTROLLER
        self.curveElbowIk = mc.curve(d=1, p=[(0, 0, 0), (0, 0, 0)], k=[0, 1],  n=('%s%s_crv' % (prefixElbowIk, side)))
        self.clusterBase, self.clusterBaseHdl =mc.cluster('%s.cv[0]' % self.curveElbowIk, n='%s01%s_cls' % (prefixElbowIk,side),
                                                          wn=(forearmIkJnt, forearmIkJnt))
        self.clusterElbow, self.clusterElbowHdl =mc.cluster('%s.cv[1]' % self.curveElbowIk, n='%s02%s_cls' % (prefixElbowIk, side),
                                                            wn=(self.controllerElbowIk.control, self.controllerElbowIk.control))

        # LOCK CURVE
        mc.setAttr('%s.template' % self.curveElbowIk, 1)
        mc.setAttr('%s.template' % self.curveElbowIk, lock=1)

        ########################################### BLEND FOLLOW ARM ###################################################
        ## FK
        # create locator
        self.shoulderFkLoc = mc.spaceLocator( n='%s%s_loc' % ('ShoulderFkFol', side))
        self.hipFkLoc = mc.spaceLocator(n='%s%s_loc' % ('HipFkFol', side))
        self.worldFkLoc = mc.spaceLocator(n='%s%s_loc' % ('WorldFkFol', side))

        # match locator position to upperarm
        mc.delete(mc.parentConstraint(upperArmFkJnt, self.shoulderFkLoc))
        mc.delete(mc.parentConstraint(upperArmFkJnt, self.hipFkLoc))
        mc.delete(mc.parentConstraint(upperArmFkJnt, self.worldFkLoc))

    # constraining the locators to arm
        self.blendArmFkPoint = mc.pointConstraint(self.shoulderFkLoc, self.controllerUpperArmFk.parent_control[0], mo=1)
        self.blendArmFkRotation = mc.orientConstraint(self.shoulderFkLoc, self.hipFkLoc, self.worldFkLoc,
                                                      self.controllerUpperArmFk.parent_control[0], mo=1)

        # create condition
        shoulderFolFkCnd = mc.shadingNode('condition', asUtility=1, n='%s%s%s_cnd' % (prefix, 'ShoulderFkFollow', side))
        mc.setAttr(shoulderFolFkCnd + '.secondTerm', 0)
        mc.setAttr(shoulderFolFkCnd + '.colorIfTrueR', 1)
        mc.setAttr(shoulderFolFkCnd + '.colorIfFalseR', 0)
        mc.connectAttr(self.controllerUpperArmFk.control+'.follow', shoulderFolFkCnd+'.firstTerm')

        hipFolFkCnd = mc.shadingNode('condition', asUtility=1, n='%s%s%s_cnd' % (prefix, 'HipFkFollow', side))
        mc.setAttr(hipFolFkCnd + '.secondTerm', 1)
        mc.setAttr(hipFolFkCnd + '.colorIfTrueR', 1)
        mc.setAttr(hipFolFkCnd + '.colorIfFalseR', 0)
        mc.connectAttr(self.controllerUpperArmFk.control + '.follow', hipFolFkCnd + '.firstTerm')

        worldFolFkCnd = mc.shadingNode('condition', asUtility=1, n='%s%s%s_cnd' % (prefix, 'WorldFkFollow', side))
        mc.setAttr(worldFolFkCnd + '.secondTerm', 2)
        mc.setAttr(worldFolFkCnd + '.colorIfTrueR', 1)
        mc.setAttr(worldFolFkCnd + '.colorIfFalseR', 0)
        mc.connectAttr(self.controllerUpperArmFk.control + '.follow', worldFolFkCnd + '.firstTerm')

        # connect to orient constraint
        mc.connectAttr(shoulderFolFkCnd + '.outColorR', ('%s.%sW0' % (self.blendArmFkRotation[0], self.shoulderFkLoc[0])))
        mc.connectAttr(hipFolFkCnd + '.outColorR', ('%s.%sW1' % (self.blendArmFkRotation[0], self.hipFkLoc[0])))
        mc.connectAttr(worldFolFkCnd + '.outColorR', ('%s.%sW2' % (self.blendArmFkRotation[0], self.worldFkLoc[0])))

        ## IK
        # create locator
        self.shoulderIkLoc = mc.spaceLocator(n='%s%s_loc' % ('ShoulderIkFol', side))
        self.hipIkLoc = mc.spaceLocator(n='%s%s_loc' % ('HipIkFol', side))
        self.worldIkLoc = mc.spaceLocator(n='%s%s_loc' % ('WorldIkFol', side))

        # match locator position to upperarm
        mc.delete(mc.parentConstraint(wristIkJnt, self.shoulderIkLoc))
        mc.delete(mc.parentConstraint(wristIkJnt, self.hipIkLoc))
        mc.delete(mc.parentConstraint(wristIkJnt, self.worldIkLoc))

        self.blendArmIkParent = mc.parentConstraint(self.shoulderIkLoc, self.hipIkLoc, self.worldIkLoc,
                                                    self.controllerWristIk.parent_control[0], mo=1)

        # create condition
        shoulderFolIkCnd = mc.shadingNode('condition', asUtility=1, n='%s%s%s_cnd' % (prefix, 'ShoulderIkFollow', side))
        mc.setAttr(shoulderFolIkCnd + '.secondTerm', 0)
        mc.setAttr(shoulderFolIkCnd + '.colorIfTrueR', 1)
        mc.setAttr(shoulderFolIkCnd + '.colorIfFalseR', 0)
        mc.connectAttr(self.controllerWristIk.control + '.follow', shoulderFolIkCnd + '.firstTerm')

        hipFolIkCnd = mc.shadingNode('condition', asUtility=1, n='%s%s%s_cnd' % (prefix, 'HipIkFollow', side))
        mc.setAttr(hipFolIkCnd + '.secondTerm', 1)
        mc.setAttr(hipFolIkCnd + '.colorIfTrueR', 1)
        mc.setAttr(hipFolIkCnd + '.colorIfFalseR', 0)
        mc.connectAttr(self.controllerWristIk.control + '.follow', hipFolIkCnd + '.firstTerm')

        worldFolIkCnd = mc.shadingNode('condition', asUtility=1, n='%s%s%s_cnd' % (prefix, 'WorldIkFollow', side))
        mc.setAttr(worldFolIkCnd + '.secondTerm', 2)
        mc.setAttr(worldFolIkCnd + '.colorIfTrueR', 1)
        mc.setAttr(worldFolIkCnd + '.colorIfFalseR', 0)
        mc.connectAttr(self.controllerWristIk.control + '.follow', worldFolIkCnd + '.firstTerm')

        # connect to orient constraint
        mc.connectAttr(shoulderFolIkCnd + '.outColorR', ('%s.%sW0' % (self.blendArmIkParent[0], self.shoulderIkLoc[0])))
        mc.connectAttr(hipFolIkCnd + '.outColorR', ('%s.%sW1' % (self.blendArmIkParent[0], self.hipIkLoc[0])))
        mc.connectAttr(worldFolIkCnd + '.outColorR', ('%s.%sW2' % (self.blendArmIkParent[0], self.worldIkLoc[0])))

        ################################################# GENERAL #########################################################

        ### CREATE CONTROL FK/IK SETUP
        self.controllerFKIKArmSetup = ct.Control(match_obj_first_position=wristFkJnt, prefix='%s%s' % (prefixArmSetup, side),
                                                 shape=ct.STICKCIRCLE,
                                                 groups_ctrl=['Zro'], ctrl_size=scale,
                                                 ctrl_color='navy', lock_channels=['v', 't', 'r', 's'])

        ### FK/IK SETUP VISIBILITY ATTRIBUTE CONTROLLER
        au.add_attr_transform(self.controllerFKIKArmSetup.control, 'FkIk', 'long', keyable=True, min=0, max=1, dv=0)

        # create reverse node for FK on/off
        armSetupRevs = mc.createNode('reverse', n=('%s%s_rev' % ('armFkIk', side)))

        # set on/off attribute FK
        au.connect_part_object(obj_base_connection='FkIk', target_connection='inputX', obj_name=self.controllerFKIKArmSetup.control,
                               target_name=[armSetupRevs], select_obj=False)

        au.connect_part_object(obj_base_connection='outputX', target_connection='visibility', obj_name=armSetupRevs,
                               target_name=[self.controllerUpperArmFk.parent_control[0]], select_obj=False)

        # set on/off attribute IK
        au.connect_part_object(obj_base_connection='FkIk', target_connection='visibility', obj_name=self.controllerFKIKArmSetup.control,
                               target_name=[self.controllerUpperArmIk.parent_control[0],
                                            self.controllerElbowIk.parent_control[0],
                                            self.controllerWristIk.parent_control[0],
                                            self.curveElbowIk],
                               select_obj=False)

        # EXTRA ATTRIBUTES

        au.add_attribute(objects=[self.controllerFKIKArmSetup.control], long_name=['upperArmMultTwist'],
                         at="float", min=0, max=1, dv=0.5, channel_box=True)

        au.add_attribute(objects=[self.controllerFKIKArmSetup.control], long_name=['size'],
                         attributeType="float", dv=1, keyable=True)

        if clavicleShapeJoint or upperArmShapeJoint or elbowShapeJoint or wristShapeJoint:
            au.add_attribute(objects=[self.controllerFKIKArmSetup.control], long_name=['cornerLimbShape'], nice_name=[' '], at="enum",
                             en='Corner Limb Shape', channel_box=True)

        if clavicleShapeJoint:
            au.add_attribute(objects=[self.controllerFKIKArmSetup.control], long_name=['clavicleShape'],
                             attributeType="float", min=0, max=1, dv=0.5, channel_box=True)

        if upperArmShapeJoint:
            au.add_attribute(objects=[self.controllerFKIKArmSetup.control], long_name=['upperArmShape'],
                             attributeType="float", min=0, max=1, dv=0.5, channel_box=True)

        if elbowShapeJoint:
            au.add_attribute(objects=[self.controllerFKIKArmSetup.control], long_name=['elbowShape'],
                             attributeType="float", min=0, max=1, dv=0.5, channel_box=True)

        if wristShapeJoint:
            au.add_attribute(objects=[self.controllerFKIKArmSetup.control], long_name=['wristShape'],
                             attributeType="float", min=0, max=1, dv=0.5, channel_box=True)


    ############################################# FK/ IK BLEND ####################################################

        upperArmBlendCons = mc.parentConstraint(upperArmFkJnt, upperArmIkJnt, upperArmJnt)
        forearmBlendCons  = mc.parentConstraint(forearmFkJnt, forearmIkJnt, forearmJnt)
        wristBlendCons    = mc.parentConstraint(wristFkJnt, wristIkJnt, wristJnt)

        # set on/off attribute Fk/Ik upperarm
        au.connect_part_object(obj_base_connection='outputX', target_connection='%sW0' % upperArmFkJnt, obj_name=armSetupRevs,
                               target_name=upperArmBlendCons, select_obj=False)
        au.connect_part_object(obj_base_connection='FkIk', target_connection='%sW1' % upperArmIkJnt, obj_name=self.controllerFKIKArmSetup.control,
                               target_name=upperArmBlendCons, select_obj=False)

        # set on/off attribute Fk/Ik forearm
        au.connect_part_object(obj_base_connection='outputX', target_connection='%sW0' % forearmFkJnt, obj_name=armSetupRevs,
                               target_name=forearmBlendCons, select_obj=False)
        au.connect_part_object(obj_base_connection='FkIk', target_connection='%sW1' % forearmIkJnt, obj_name=self.controllerFKIKArmSetup.control,
                               target_name=forearmBlendCons, select_obj=False)

        # set on/off attribute Fk/Ik wrist
        au.connect_part_object(obj_base_connection='outputX', target_connection='%sW0' % wristFkJnt, obj_name=armSetupRevs,
                               target_name=wristBlendCons, select_obj=False)
        au.connect_part_object(obj_base_connection='FkIk', target_connection='%sW1' % wristIkJnt, obj_name=self.controllerFKIKArmSetup.control,
                               target_name=wristBlendCons, select_obj=False)

        ######################################################## DETAIL ####################################################

        ## MID COMBINE DETAIL
        # create controller
        self.ctrlMidForearm = ct.Control(match_obj_first_position=forearmJnt, prefix=prefix + 'DtlCombine' + side, groups_ctrl=['Zro'],
                                         ctrl_size=scale * 0.75, ctrl_color='blue', shape=ct.ARROW3DFLAT)

        # print self.ctrlMidForearm.control

        if detailArmDeformer:
            # add attribute
            au.add_attribute(objects=[self.ctrlMidForearm.control],
                             long_name=['twistSep'], nice_name=[' '], at="enum", en='Twist', channel_box=True)

            au.add_attribute(objects=[self.ctrlMidForearm.control], long_name=['roll'], at="float", keyable=True)

            # Add attributes: Volume attributes
            au.add_attribute(objects=[self.ctrlMidForearm.control], long_name=['volumeSep'], nice_name=[' '], at="enum",
                             en='Volume', channel_box=True)

            au.add_attribute(objects=[self.ctrlMidForearm.control], long_name=['volume'], at="float", min=-1, max=1, keyable=True)
            au.add_attribute(objects=[self.ctrlMidForearm.control], long_name=['volumeMultiplier'], at="float", min=1, dv=1,
                             keyable=True)

            au.add_attribute(objects=[self.ctrlMidForearm.control], long_name=['volumePosition'], dv=0,
                             min= numJoint*-0.5,
                             max= numJoint*0.5, at="float", keyable=True)

            # Add attributes: Sine attributes
            au.add_attribute(objects=[self.ctrlMidForearm.control], long_name=['sineSep'], nice_name=[' '],
                             attributeType='enum',
                             en="Sine:", channel_box=True)

            au.add_attribute(objects=[self.ctrlMidForearm.control], long_name=['amplitude'], attributeType="float", keyable=True)
            au.add_attribute(objects=[self.ctrlMidForearm.control], long_name=['wide'], attributeType="float", keyable=True)
            au.add_attribute(objects=[self.ctrlMidForearm.control], long_name=['sineRotate'], attributeType="float", keyable=True)
            au.add_attribute(objects=[self.ctrlMidForearm.control], long_name=['offset'], attributeType="float", keyable=True)
            au.add_attribute(objects=[self.ctrlMidForearm.control], long_name=['twist'], attributeType="float", keyable=True)
            au.add_attribute(objects=[self.ctrlMidForearm.control], long_name=['sineLength'], min=0.1, dv=1,
                             attributeType="float",
                             keyable=True)

            # ROLL
            self.adlUpperArmCombine = mc.createNode('addDoubleLinear', n=(prefixUpperArmDtl + 'RollCombine' + side + '_adl'))
            mc.connectAttr(self.ctrlMidForearm.control + '.roll', self.adlUpperArmCombine + '.input2')

            self.adlforearmCombine  = mc.createNode('addDoubleLinear', n=(prefixForearmDtl + 'RollCombine' + side + '_adl'))
            mc.connectAttr(self.ctrlMidForearm.control + '.roll', self.adlforearmCombine + '.input2')

        ## VOLUME POSITION
            ## upperArm
            # condition
            volumePosCndUa = mc.shadingNode('condition', asUtility=1,
                                            n='%s%s%s_cnd' % (prefixUpperArmDtl, 'CombineVolumePos', side))
            mc.setAttr(volumePosCndUa + '.operation', 2)
            mc.connectAttr(self.ctrlMidForearm.control + '.volumePosition', volumePosCndUa + '.firstTerm')
            mc.connectAttr(self.ctrlMidForearm.control + '.volumePosition', volumePosCndUa + '.colorIfFalseR')
            mc.connectAttr(self.ctrlMidForearm.control + '.volumePosition', volumePosCndUa + '.colorIfTrueR')

            # add double linear
            self.volumePosMdlUa = mc.shadingNode('multDoubleLinear', asUtility=1,
                                                 n='%s%s%s_mdl' % (prefixUpperArmDtl, 'CombineVolumePos', side))
            mc.connectAttr(self.ctrlMidForearm.control + '.volume', self.volumePosMdlUa + '.input2')

            # connect using keyframe inbetween
            # min
            mc.setDrivenKeyframe(self.volumePosMdlUa + '.input1',
                                       cd=volumePosCndUa + '.outColorR',
                                       dv=0, v=1, itt='linear', ott='linear')
            # max
            mc.setDrivenKeyframe(self.volumePosMdlUa + '.input1',
                                       cd=volumePosCndUa + '.outColorR',
                                       dv=numJoint * 0.5, v=0, itt='linear', ott='linear')

            ## forearm
            # condition
            volumePosCndFa = mc.shadingNode('condition', asUtility=1,
                                            n='%s%s%s_cnd' % (prefixForearmDtl, 'CombineVolumePos', side))
            mc.setAttr(volumePosCndFa + '.operation', 4)
            mc.connectAttr(self.ctrlMidForearm.control + '.volumePosition', volumePosCndFa + '.firstTerm')
            mc.connectAttr(self.ctrlMidForearm.control + '.volumePosition', volumePosCndFa + '.colorIfFalseR')
            mc.connectAttr(self.ctrlMidForearm.control + '.volumePosition', volumePosCndFa + '.colorIfTrueR')

            # add double linear
            self.volumePosMdlFa = mc.shadingNode('multDoubleLinear', asUtility=1,
                                                 n='%s%s%s_mdl' % (prefixForearmDtl, 'CombineVolumePos', side))
            mc.connectAttr(self.ctrlMidForearm.control + '.volume', self.volumePosMdlFa + '.input2')

            # connect using keyframe inbetween
            # min
            mc.setDrivenKeyframe(self.volumePosMdlFa + '.input1',
                                       cd=volumePosCndFa + '.outColorR',
                                       dv=numJoint * -0.5, v=0, itt='linear', ott='linear')
            # max
            mc.setDrivenKeyframe(self.volumePosMdlFa + '.input1',
                                       cd=volumePosCndFa + '.outColorR',
                                       dv=0, v=1, itt='linear', ott='linear')

    # Add attributes: Extra attributes
        au.add_attribute(objects=[self.ctrlMidForearm.control], long_name=['extraSep'], nice_name=[' '], at="enum",
                         en='Extra',
                         channel_box=True)
        au.add_attribute(objects=[self.ctrlMidForearm.control], long_name=['detailBaseCtrlVis'], at="long", min=0, max=1, dv=0,
                         channel_box=True)

        # lock and hide attribute
        au.lock_hide_attr(['r', 's', 'v'], self.ctrlMidForearm.control)

    # adjusting the controller direction
        if getValueTxWristJnt > 0:
                rc.change_position(self.controllerFKIKArmSetup.control, 'xz')
                rc.change_position(self.controllerFKIKArmSetup.control, '-')
                rc.change_position(self.controllerElbowIk.control, 'yz')
                rc.change_position(self.controllerElbowIk.control, '-')

        else:
            rc.change_position(self.controllerFKIKArmSetup.control, 'xz')
            rc.change_position(self.controllerElbowIk.control, 'yz')