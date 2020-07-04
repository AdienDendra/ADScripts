import generalModule as gm
import maya.cmds as mc
from rigLib.rig import arm as ar
from rigLib.rig.body import limb_part_detail as rl, hand as hn
from rigLib.utils import pole_vector as pv, controller as ct

from rigging.tools import AD_utils as au

reload(gm)
reload(pv)
reload(ct)
reload(au)
reload(ar)
reload(hn)
reload(rl)

generalScale = 1.0

class Arm:
    def __init__(self,
                 arm,
                 prefix,
                 base,
                 prefixUpperArmFk,
                 prefixForearmFk,
                 prefixWristFk,
                 prefixUpperArmIk,
                 prefixElbowIk,
                 prefixForearmIk,
                 prefixWristIk,
                 prefixHandIk,
                 prefixArmSetup,
                 side,
                 rootJnt,
                 clavJnt,
                 upperArmJnt,
                 forearmJnt,
                 wristJnt,
                 upperArmFkJnt,
                 forearmFkJnt,
                 wristFkJnt,
                 upperArmIkJnt,
                 forearmIkJnt,
                 wristIkJnt,
                 handIKJnt,
                 clavicleShapeJoint,
                 upperArmShapeJoint,
                 elbowShapeJoint,
                 wristShapeJoint,
                 world,
                 upperArmDtlJnt,
                 forearmDtlJnt,
                 upperArmDtlBind,
                 forearmDtlBind,
                 detailArmDeformer,
                 numDtlCtrl,
                 parallelAxis,
                 tipPos,
                 prefixUpperArmDtl,
                 prefixForearmDtl,
                 size=generalScale):

        if arm:
            getValueTxWristJnt = mc.xform(upperArmIkJnt, ws=1, q=1, t=1)[0]

        ### GENERAL ARM SETUP
            # arm position

            # create arm pole vector position
            ikhVectPos = mc.ikHandle(sj=upperArmIkJnt, ee=wristIkJnt, sol='ikRPsolver')
            locPVPos = pv.create_poleVec_locator(ikhVectPos[0], constraint=False, length=3 * size)

        ### IMPORT ARM MODULE
            buildArm= ar.Build(
                prefix=prefix,
                prefixUpperArmDtl=prefixUpperArmDtl,
                prefixForearmDtl=prefixForearmDtl,
                prefixUpperArmFk=prefixUpperArmFk,
                prefixForearmFk=prefixForearmFk,
                prefixWristFk=prefixWristFk,
                prefixUpperArmIk=prefixUpperArmIk,
                prefixElbowIk=prefixElbowIk,
                prefixForearmIk=prefixForearmIk,
                prefixWristIk=prefixWristIk,
                prefixHandIk=prefixHandIk,
                prefixArmSetup=prefixArmSetup,
                side=side,
                upperArmJnt=upperArmJnt,
                forearmJnt= forearmJnt,
                wristJnt = wristJnt,
                upperArmFkJnt=upperArmFkJnt,
                forearmFkJnt=forearmFkJnt,
                wristFkJnt=wristFkJnt,
                upperArmIkJnt=upperArmIkJnt,
                forearmIkJnt=forearmIkJnt,
                elbowIKJnt=locPVPos[0],
                wristIkJnt=wristIkJnt,
                handIKJnt=handIKJnt,
                detailArmDeformer=detailArmDeformer,
                numJoint=numDtlCtrl,
                clavicleShapeJoint=clavicleShapeJoint,
                upperArmShapeJoint=upperArmShapeJoint,
                elbowShapeJoint=elbowShapeJoint,
                wristShapeJoint=wristShapeJoint,
                scale=size)

            # delete locator pole vector pos
            mc.delete(locPVPos)

            self.prefix = prefix

            self.parentConsElm = None

            # instance the objects
            self.fkIkArmSetupControllerGrpZro   = buildArm.controllerFKIKArmSetup.parentControl[0]
            self.fkIkArmSetupController         = buildArm.controllerFKIKArmSetup.control

            # Fk
            self.upperArmFkControllerGrpZro = buildArm.controllerUpperArmFk.parentControl[0]
            self.forearmFkControllerGrpZro  = buildArm.controllerForeArmFk.parentControl[0]
            self.wristFkControllerGrpZro    = buildArm.controllerWristFk.parentControl[0]

            self.upperArmFkGimbal   = buildArm.controllerUpperArmFk.controlGimbal
            self.forearmFkGimbal    = buildArm.controllerForeArmFk.controlGimbal

            # Ik
            self.upperArmIkControllerGrpZro = buildArm.controllerUpperArmIk.parentControl[0]
            self.elbowIkControllerGrpZro    = buildArm.controllerElbowIk.parentControl[0]
            self.wristIkControllerGrpZro    = buildArm.controllerWristIk.parentControl[0]

            self.upperArmIkGimbal = buildArm.controllerUpperArmIk.controlGimbal
            self.wristIkGimbal    = buildArm.controllerWristIk.controlGimbal
            self.upperArmIk       = buildArm.controllerUpperArmIk.control
            self.wristIk          = buildArm.controllerWristIk.control

            # locator
            self.shoulderFkLoc = buildArm.shoulderFkLoc
            self.hipFkLoc      = buildArm.hipFkLoc
            self.worldFkLoc    = buildArm.worldFkLoc

            self.shoulderIkLoc = buildArm.shoulderIkLoc
            self.hipIkLoc      = buildArm.hipIkLoc
            self.worldIkLoc    = buildArm.worldIkLoc

            self.ctrlCombineDtl = buildArm.ctrlMidForearm.control

            # build part of group hierarchy
            part = gm.Part(prefix=prefix, side=side, baseObj= base)

            # control group in part
            self.partControlGrp = part.controlGrp

            # parent setup to part group
            # controller
            mc.parent(self.fkIkArmSetupControllerGrpZro, part.controlGrp)
            mc.parent(buildArm.ctrlMidForearm.parentControl[0], part.controlGrp)

            # joint
            mc.parent(buildArm.posUpperArmJnt, part.jointGrp)
            mc.parent(buildArm.posElbowJnt, part.jointGrp)
            mc.parent(buildArm.posSoftJnt, part.jointGrp)
            mc.parent(buildArm.posArmJnt, part.jointGrp)

            # locator
            mc.parent(buildArm.shoulderFkLoc, part.locGrp)
            mc.parent(buildArm.hipFkLoc, part.locGrp)
            mc.parent(buildArm.worldFkLoc, part.locGrp)

            mc.parent(buildArm.shoulderIkLoc, part.locGrp)
            mc.parent(buildArm.hipIkLoc, part.locGrp)
            mc.parent(buildArm.worldIkLoc, part.locGrp)

            # non-trans
            mc.parent(buildArm.curveElbowIk, part.nonTransform)

        ### FK SETUP
            # parent joint FK driver to joint grp
            mc.parent(upperArmFkJnt, base.jntGrp)

            # parent wrist to foreArm control group
            mc.parent(self.wristFkControllerGrpZro, self.forearmFkGimbal)

            # parent foreArm to upperArm control group
            mc.parent(self.forearmFkControllerGrpZro, self.upperArmFkGimbal)

            # parent all arm to part control group
            mc.parent(self.upperArmFkControllerGrpZro, part.controlGrp)

            # connect scale module to decompose matrix
            mc.connectAttr(base.animControl +'.worldMatrix[0]', buildArm.scaleDecompose + '.inputMatrix')

            # stretch FK foreArm
            mc.connectAttr(buildArm.upperArmAddOffset + '.output',
                           buildArm.controllerForeArmFk.parentControl[0] + '.translateY')

            # stretch FK wrist
            mc.connectAttr(buildArm.forearmAddOffset + '.output',
                           self.wristFkControllerGrpZro + '.translateY')

        ### IK SETUP
            # parent joint IK driver to joint grp
            mc.parent(upperArmIkJnt, base.jntGrp)

            # parent upperArm to part control group
            mc.parent(self.upperArmIkControllerGrpZro, part.controlGrp)

            # parent elbow to part control group
            mc.parent(self.elbowIkControllerGrpZro, part.controlGrp)

            # parent wrist to part control group
            mc.parent(self.wristIkControllerGrpZro, part.controlGrp)

            # point constraint the stretching the arm
            mc.pointConstraint(self.upperArmIkGimbal,  buildArm.posUpperArmJnt, mo=1)

            # aim constraining for stretching the arm
            mc.aimConstraint(self.wristIkGimbal, buildArm.posUpperArmJnt, mo=1, aim=(0.0,1.0,0.0),
                             u=(-1.0,0.0,0.0), wut='objectrotation', wu= (0.0,1.0,0.0), wuo=part.jointGrp)

            # ELBOW FOLLOWING ARM
            elbowFollowConst = mc.parentConstraint(self.wristIk, world, self.elbowIkControllerGrpZro, mo=1)[0]
            mc.connectAttr(buildArm.controllerElbowIk.control+'.follow', elbowFollowConst+'.%sW0' % self.wristIk)

            elbowConsRev = mc.shadingNode('reverse', asUtility=1, n='%s%s%s_rev' % (prefixElbowIk, 'Follow', side))
            mc.connectAttr(buildArm.controllerElbowIk.control+'.follow', elbowConsRev+'.inputX')
            mc.connectAttr(elbowConsRev+'.outputX', elbowFollowConst+'.%sW1' % world)

            # set ikRPsolver
            mc.setAttr("ikRPsolver.tolerance", 1e-09)

            # constraining the controller Fk/Ik
            mc.parentConstraint(wristJnt, self.fkIkArmSetupControllerGrpZro, mo=1)

            ## IMPORT DETAIL ARM MODULE
            # parenting all joints to joint grp
            mc.parent(upperArmDtlJnt, upperArmDtlBind, base.jntGrp)
            mc.parent(forearmDtlBind, base.jntGrp)

            # constraint from arm driver to arm bind
            mc.parentConstraint(upperArmJnt, upperArmDtlBind, mo=1)
            mc.parentConstraint(forearmJnt, forearmDtlBind, mo=1)

        ######################################################## FOLLOW ORIENTATION #######################################
            # constraining follow Fk
            mc.parentConstraint(clavJnt, self.shoulderFkLoc, mo=1)
            mc.parentConstraint(rootJnt, self.hipFkLoc, mo=1)
            mc.parentConstraint(base.animControl, self.worldFkLoc, mo=1)

            # constraining follow Ik
            mc.parentConstraint(clavJnt, self.upperArmIkControllerGrpZro, mo=1)

            mc.parentConstraint(clavJnt, self.shoulderIkLoc, mo=1)
            mc.parentConstraint(rootJnt, self.hipIkLoc, mo=1)
            mc.parentConstraint(base.animControl, self.worldIkLoc, mo=1)


        ######################################################## DETAIL ####################################################
        # DETAIL SETUP
            # spline ik detail driver
            # get attibute upperArm jnt
            upperArmDtlJoint = mc.xform(upperArmDtlJnt, q=1, ws=True, t=1)
            forearmDtlJoint  = mc.xform(forearmDtlJnt, q=1, ws=True, t=1)

            # create curve for ik spline
            curveIkSplineDtl  = mc.curve(d=1, p=[upperArmDtlJoint, forearmDtlJoint])
            self.armDetailHdl = mc.ikHandle(sj=upperArmDtlJnt, ee=forearmDtlJnt, sol='ikSplineSolver',
                                            n='%s%s_hdl' % (prefixUpperArmIk+'Dtl', side), ccv=False, c=curveIkSplineDtl, ns=1, rootOnCurve=True)
            dtlHdlCrv = mc.rename(curveIkSplineDtl, '%s%s_crv' % (prefixUpperArmIk + 'Dtl', side))

            # hide the curve spline Ik
            mc.hide(dtlHdlCrv)

            # skin the spline curve
            mc.skinCluster(upperArmDtlBind, forearmDtlBind, dtlHdlCrv, tsb=True, mi=1)

            # parent to part grp
            mc.parent(self.armDetailHdl[0], part.utilsGrp)
            mc.parent(dtlHdlCrv, part.nonTransform)

            # divided value in every index
            num = (1.0 / (numDtlCtrl + 1))

        # UPPERARM DETAIL
            dtlUpperArm = rl.CreateDetail(
                         detail_limb_deformer=detailArmDeformer,
                         base=upperArmDtlJnt,
                         tip=forearmDtlBind,
                         parallel_axis=parallelAxis,
                         tip_pos=tipPos,
                         ctrl_tip=ct.SQUARE,
                         ctrl_mid=ct.SQUARE,
                         ctrl_base=ct.SQUARE,
                         ctrl_details=ct.CIRCLEPLUS,
                         prefix=prefixUpperArmDtl,
                         side=side,
                         scale=size,
                         volume_pos_min=2,
                         volume_pos_max=0,
                         number_joints=numDtlCtrl)

            # set grp follicle upperArm
            self.setGrpFollUpperArm = dtlUpperArm.follicle_set_grp

            self.setGrpFollTwistUpperArm = dtlUpperArm.follicle_grp_twist

            # parent main grp to still grp
            mc.parent(dtlUpperArm.grp_no_transform_zro, base.stillGrp)
            mc.parent(dtlUpperArm.grp_transform_zro, part.controlGrp)

            # scale connect
            mc.connectAttr(base.scaleMatrixNode +'.outputScale', dtlUpperArm.grp_transform + '.scale')

            # parent constraint detail bind to grp transform detail
            mc.parentConstraint(upperArmDtlBind, dtlUpperArm.grp_transform, mo=1)

            # parent contraint detail jnt driver to grp offset upperArm
            mc.parentConstraint(upperArmDtlJnt, dtlUpperArm.ctrl_up.parentControl[1])

            # parent contraint detail jnt driver to grp offset forearm
            mc.parentConstraint(forearmDtlBind, dtlUpperArm.ctrl_down.parentControl[1], mo=1)

            #connect attribute to twist grp
            ctrlTwistMdl = mc.shadingNode('multDoubleLinear', asUtility=1, n='%s%s%s_mdl' % (prefixUpperArmDtl, 'MultCtrlTwist', side))

            mc.connectAttr(upperArmDtlJnt + '.rotateX', ctrlTwistMdl + '.input1')
            mc.connectAttr(buildArm.controllerFKIKArmSetup.control + '.upperArmMultTwist', ctrlTwistMdl + '.input2')

            mc.connectAttr(ctrlTwistMdl +'.output', dtlUpperArm.ctrl_up.parentControl[2] + '.rotateY')

            ### TWIST UPPERARM SETUP
            # create multi matrix
            multMtxCtrlUp   = mc.shadingNode('multMatrix', asUtility=1, n='%s%s%s_mmtx' % (prefixUpperArmDtl, 'CtrlUp', side))
            multMtxCtrlDown = mc.shadingNode('multMatrix', asUtility=1, n='%s%s%s_mmtx' % (prefixUpperArmDtl, 'CtrlDown', side))

            mc.connectAttr(dtlUpperArm.ctrl_up.control + '.worldMatrix[0]', multMtxCtrlUp + '.matrixIn[0]')
            mc.connectAttr(dtlUpperArm.ctrl_down.parentControl[0] + '.worldInverseMatrix[0]', multMtxCtrlUp + '.matrixIn[1]')

            mc.connectAttr(dtlUpperArm.ctrl_down.control + '.worldMatrix[0]', multMtxCtrlDown + '.matrixIn[0]')
            mc.connectAttr(dtlUpperArm.ctrl_up.parentControl[0] + '.worldInverseMatrix[0]', multMtxCtrlDown + '.matrixIn[1]')

            # create decompose matrix
            decomposeMtxCtrlUp   = mc.shadingNode('decomposeMatrix', asUtility=1, n='%s%s%s_dmtx' % (prefixUpperArmDtl, 'CtrlUp', side))
            decomposeMtxCtrlDown = mc.shadingNode('decomposeMatrix', asUtility=1, n='%s%s%s_dmtx' % (prefixUpperArmDtl, 'CtrlDown', side))

            mc.connectAttr(multMtxCtrlUp+'.matrixSum', decomposeMtxCtrlUp+'.inputMatrix')
            mc.connectAttr(multMtxCtrlDown+'.matrixSum', decomposeMtxCtrlDown+'.inputMatrix')

            # create quat to euler
            quatCtrlUp   = mc.shadingNode('quatToEuler', asUtility=1, n='%s%s%s_qte' % (prefixUpperArmDtl, 'CtrlUp', side))
            quatCtrlDown = mc.shadingNode('quatToEuler', asUtility=1, n='%s%s%s_qte' % (prefixUpperArmDtl, 'CtrlDown', side))

            mc.connectAttr(decomposeMtxCtrlUp+'.outputQuatY', quatCtrlUp+'.inputQuatY')
            mc.connectAttr(decomposeMtxCtrlUp+'.outputQuatW', quatCtrlUp+'.inputQuatW')

            mc.connectAttr(decomposeMtxCtrlDown+'.outputQuatY', quatCtrlDown+'.inputQuatY')
            mc.connectAttr(decomposeMtxCtrlDown+'.outputQuatW', quatCtrlDown+'.inputQuatW')

            ctrlUpMdlNode       = []
            ctrlDownMdlNode     = []
            sumUpDownMatrixNode = []

            for i in range(len(self.setGrpFollTwistUpperArm)):
                value = num*i
                # ctrl up mult double linear
                ctrlUpMdl = mc.shadingNode('multDoubleLinear', asUtility=1, n='%s%s%s%s_mdl' % (prefixUpperArmDtl,
                                                                                                str(i + 1).zfill(2) , 'MultCtrlUp', side))
                mc.setAttr(ctrlUpMdl+'.input2', value)
                ctrlUpMdlNode.append(ctrlUpMdl)

                # ctrl down mult double linear
                ctrlDownMdl = mc.shadingNode('multDoubleLinear', asUtility=1, n='%s%s%s%s_mdl' % (prefixUpperArmDtl,
                                                                                                  str(i + 1).zfill(2) , 'MultCtrlDown', side))
                mc.setAttr(ctrlDownMdl + '.input2', value)
                ctrlDownMdlNode.append(ctrlDownMdl)

                # connect quatCtrlDown and quatCtrlUp to respective multiply node
                mc.connectAttr(quatCtrlUp+'.outputRotateY', ctrlUpMdl+'.input1')
                mc.connectAttr(quatCtrlDown + '.outputRotateY', ctrlDownMdl + '.input1')

                # create matrix node for twist upperArm
                sumUpDownMatrix = mc.shadingNode('plusMinusAverage', asUtility=1,
                                                 n='%s%s%s%s_pma' % (prefixUpperArmDtl, str(i + 1).zfill(2), 'SumUpDown', side))
                sumUpDownMatrixNode.append(sumUpDownMatrix)

            for up, down, pma, twst in zip (ctrlUpMdlNode[::-1], ctrlDownMdlNode, sumUpDownMatrixNode, self.setGrpFollTwistUpperArm):
                mc.connectAttr(up+'.output', pma+'.input1D[0]')
                mc.connectAttr(down+'.output', pma+'.input1D[1]')
                mc.connectAttr(pma + '.output1D', twst + '.rotateY')

        # FOREARM DETAIL
            dtlForearm = rl.CreateDetail(
                detail_limb_deformer=detailArmDeformer,
                base=forearmDtlBind,
                tip=wristJnt,
                parallel_axis=parallelAxis,
                tip_pos=tipPos,
                ctrl_tip=ct.SQUARE,
                ctrl_mid=ct.SQUARE,
                ctrl_base=ct.SQUARE,
                ctrl_details=ct.CIRCLEPLUS,
                prefix=prefixForearmDtl,
                side=side,
                scale=size,
                volume_pos_min=0,
                volume_pos_max=2,
                number_joints=numDtlCtrl)

            # set grp follicle forearm
            self.setGrpFollForearm = dtlForearm.follicle_set_grp

            self.setGrpFollTwistForearm = dtlForearm.follicle_grp_twist

            # parent main grp to still grp
            mc.parent(dtlForearm.grp_no_transform_zro, base.stillGrp)
            mc.parent(dtlForearm.grp_transform_zro, part.controlGrp)

            # scale connect
            mc.connectAttr(base.scaleMatrixNode +'.outputScale', dtlForearm.grp_transform + '.scale')

            # constraining forearm bind dtl to forearm grp transform
            mc.parentConstraint(forearmDtlBind, dtlForearm.grp_transform, mo=1)

            # constraining wrist to forearm down ctrl detail
            mc.parentConstraint(wristJnt, dtlForearm.ctrl_down.parentControl[1])

            ### TWIST FOREARM SETUP
            # create multi matrix
            multMtxCtrlFaDown = mc.shadingNode('multMatrix', asUtility=1, n='%s%s%s_mmtx' % (prefixForearmDtl, 'CtrlDown', side))
            mc.connectAttr(dtlForearm.ctrl_down.control + '.worldMatrix[0]', multMtxCtrlFaDown + '.matrixIn[0]')
            mc.connectAttr(dtlForearm.ctrl_up.parentControl[0] + '.worldInverseMatrix[0]', multMtxCtrlFaDown + '.matrixIn[1]')

            # create decompose matrix
            decomposeMtxCtrlFaDown = mc.shadingNode('decomposeMatrix', asUtility=1,
                                                    n='%s%s%s_dmtx' % (prefixForearmDtl, 'CtrlDown', side))
            mc.connectAttr(multMtxCtrlFaDown + '.matrixSum', decomposeMtxCtrlFaDown + '.inputMatrix')

            # create quat to euler
            quatCtrlFaDown = mc.shadingNode('quatToEuler', asUtility=1, n='%s%s%s_qte' % (prefixForearmDtl, 'CtrlDown', side))

            mc.connectAttr(decomposeMtxCtrlFaDown + '.outputQuatY', quatCtrlFaDown + '.inputQuatY')
            mc.connectAttr(decomposeMtxCtrlFaDown + '.outputQuatW', quatCtrlFaDown + '.inputQuatW')

            ctrlDownFaMdlNode = []
            for i in range(len(self.setGrpFollTwistForearm)):
                value = num*i
                # ctrl down mult double linear
                ctrlDownFaMdl = mc.shadingNode('multDoubleLinear', asUtility=1, n='%s%s%s%s_mdl' % (prefixForearmDtl, str(i + 1).zfill(2) ,
                                                                                                'MultCtrlDown', side))
                mc.setAttr(ctrlDownFaMdl + '.input2', value)
                ctrlDownFaMdlNode.append(ctrlDownFaMdl)

                # connect quatCtrlDown  to respective multiply node
                mc.connectAttr(quatCtrlFaDown + '.outputRotateY', ctrlDownFaMdl + '.input1')

            for down, twst in zip (ctrlDownFaMdlNode, self.setGrpFollTwistForearm):
                mc.connectAttr(down+'.output',  twst + '.rotateY')

            ######################################################## SCALE ARM #######################################
            # SCALE ARM
            # upperArm
            self.armPartScale(controller=self.fkIkArmSetupController, groupScale=self.setGrpFollTwistUpperArm)

            # forearm
            self.armPartScale(controller=self.fkIkArmSetupController, groupScale=self.setGrpFollTwistForearm)

        ##################################################### COMBINE DETAIL ###############################################

            # parent constraint from forearmbind to arm detail combine
            mc.parentConstraint(forearmDtlBind, buildArm.ctrlMidForearm.parentControl[0])

            # point ccnstraint to respective module upperArm detail and forearm detail combine
            mc.pointConstraint(self.ctrlCombineDtl, dtlUpperArm.ctrl_down.parentControl[2])
            mc.pointConstraint(self.ctrlCombineDtl, dtlForearm.ctrl_up.parentControl[2])

            if detailArmDeformer:
                ### CONNECT ROLL
                # disconnect from detail roll to plus minus average
                mc.disconnectAttr(dtlUpperArm.ctrl_down.control + '.twist', dtlUpperArm.sum_top_pma + '.input1D[0]')
                mc.disconnectAttr(dtlForearm.ctrl_up.control + '.twist', dtlForearm.sum_end_pma + '.input1D[0]')

                # connect attribute from respective control module to add double linear control
                mc.connectAttr(dtlUpperArm.ctrl_down.control + '.twist', buildArm.adlUpperArmCombine + '.input1')
                mc.connectAttr(dtlForearm.ctrl_up.control + '.twist', buildArm.adlforearmCombine + '.input1')

                # connect output of adl combine node to plus minus average upperArm and forearm roll node
                mc.connectAttr(buildArm.adlUpperArmCombine +'.output', dtlUpperArm.sum_top_pma + '.input1D[0]')
                mc.connectAttr(buildArm.adlforearmCombine + '.output', dtlForearm.sum_end_pma + '.input1D[0]')

                ### CONNECT VOLUME POSITION
                # volume position combined
                if getValueTxWristJnt > 0:
                    # v upperArm LFT
                    self.combineVolumeDetail(dtlUpperArm.combine_vol_position_adl, self.ctrlCombineDtl, numDtlCtrl,
                                             minMult=-1, midMult=1, maxMult=1)
                    # detail forearm LFT
                    self.combineVolumeDetail(dtlForearm.combine_vol_position_adl, self.ctrlCombineDtl, numDtlCtrl,
                                             minMult=-1, midMult=-1, maxMult=1)
                else:
                    # detail upperArm RGT
                    self.combineVolumeDetail(dtlUpperArm.combine_vol_position_adl, self.ctrlCombineDtl, numDtlCtrl,
                                             minMult=1, midMult=-1, maxMult=-1)
                    # detail forearm RGT
                    self.combineVolumeDetail(dtlForearm.combine_vol_position_adl, self.ctrlCombineDtl, numDtlCtrl,
                                             minMult=1, midMult=1, maxMult=-1)

                #### CONNECT VOLUME
                # connect to multdouble linear volume detail to volume add double linear detail
                # upperArm
                mc.connectAttr(buildArm.volumePosMdlUa + '.output', dtlUpperArm.volume_reverse_adl + '.input1')

                # forearm
                mc.connectAttr(buildArm.volumePosMdlFa + '.output', dtlForearm.volume_reverse_adl + '.input1')

                ### CONNECT MULTIPLIER VOLUME
                for ua, fa in zip (dtlUpperArm.combine_mult_all, dtlForearm.combine_mult_all):
                    mc.connectAttr(self.ctrlCombineDtl+'.volumeMultiplier', ua+'.input2')
                    mc.connectAttr(self.ctrlCombineDtl+'.volumeMultiplier', fa+'.input2')

                ### CONNECT SINE SETUP
                mc.connectAttr(self.ctrlCombineDtl +'.amplitude', dtlUpperArm.combine_sine_amplitude + '.input1')
                mc.connectAttr(self.ctrlCombineDtl +'.amplitude', dtlForearm.combine_sine_amplitude + '.input1')
                mc.connectAttr(self.ctrlCombineDtl +'.wide', dtlUpperArm.combine_sine_wide + '.input1')
                mc.connectAttr(self.ctrlCombineDtl +'.wide', dtlForearm.combine_sine_wide + '.input1')
                mc.connectAttr(self.ctrlCombineDtl +'.sineRotate', dtlUpperArm.combine_sine_rotate + '.input1')
                mc.connectAttr(self.ctrlCombineDtl +'.sineRotate', dtlForearm.combine_sine_rotate + '.input1')
                mc.connectAttr(self.ctrlCombineDtl +'.offset', dtlUpperArm.combine_sine_offset + '.input1')
                mc.connectAttr(self.ctrlCombineDtl +'.offset', dtlForearm.combine_sine_offset + '.input1')
                mc.connectAttr(self.ctrlCombineDtl +'.twist', dtlUpperArm.combine_sine_twist + '.input1')
                mc.connectAttr(self.ctrlCombineDtl +'.twist', dtlForearm.combine_sine_twist + '.input1')
                mc.connectAttr(self.ctrlCombineDtl +'.sineLength', dtlUpperArm.combine_sine_length + '.input1')
                mc.connectAttr(self.ctrlCombineDtl +'.sineLength', dtlForearm.combine_sine_length + '.input1')

            # connect the visibility-switch for the controller
            # switch on/off detail module ctrl
            mc.connectAttr(self.ctrlCombineDtl +'.detailBaseCtrlVis', dtlUpperArm.ctrl_up.parentControl[0] + '.visibility')
            mc.connectAttr(self.ctrlCombineDtl +'.detailBaseCtrlVis', dtlUpperArm.ctrl_down.parentControl[0] + '.visibility')
            mc.connectAttr(self.ctrlCombineDtl +'.detailBaseCtrlVis', dtlForearm.ctrl_up.parentControl[0] + '.visibility')
            mc.connectAttr(self.ctrlCombineDtl +'.detailBaseCtrlVis', dtlForearm.ctrl_down.parentControl[0] + '.visibility')

    def combineVolumeDetail(self, combineVolPosAdl, controller, numDtlCtrl, minMult=1, midMult= 1, maxMult=1):
        # min
        mc.setDrivenKeyframe(combineVolPosAdl + '.input1',
                             cd=controller + '.volumePosition',
                             dv=numDtlCtrl * -0.5, v=numDtlCtrl * 0.5 * minMult, itt='linear', ott='linear')
        # mid
        mc.setDrivenKeyframe(combineVolPosAdl + '.input1',
                             cd=controller + '.volumePosition',
                             dv=0, v=numDtlCtrl * 0.5 * midMult, itt='linear', ott='linear')
        # max
        mc.setDrivenKeyframe(combineVolPosAdl + '.input1',
                             cd=controller + '.volumePosition',
                             dv=numDtlCtrl * 0.5, v=numDtlCtrl * 0.5 * maxMult, itt='linear', ott='linear')

    def armPartScale(self, controller, groupScale):
        # ARM SCALE
        for i in groupScale:
            mc.connectAttr(controller + '.size', i + '.scaleX')
            mc.connectAttr(controller + '.size', i + '.scaleY')
            mc.connectAttr(controller + '.size', i + '.scaleZ')
