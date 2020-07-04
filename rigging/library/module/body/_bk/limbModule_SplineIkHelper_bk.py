import generalModule as gm
import maya.cmds as mc
from rigLib.rig.body import limb_part_detail as dl, limb as lm, hand as hn
from rigLib.utils import pole_vector as pv, controller as ct

from rigging.tools import AD_utils as au

reload(gm)
reload(pv)
reload(ct)
reload(au)
reload(lm)
reload(hn)
reload(dl)

generalScale = 1.0

class Limb:
    def __init__(self,
                 limb,
                 arm,
                 prefix,
                 base,
                 prefixUpperLimb,
                 prefixPoleVecLimb,
                 prefixLowerLimb,
                 prefixBaseOrTipLimb,
                 prefixUpperLimbFk,
                 prefixMiddleLimbFk,
                 prefixLowerLimbFk,
                 prefixUpperLimbIk,
                 prefixPoleVectorIk,
                 prefixMiddleLimbIk,
                 prefixLowerLimbIk,
                 prefixEndLimbIk,
                 prefixLimbSetup,
                 side,
                 rootJnt,
                 clavJnt,
                 upperLimbJnt,
                 middleLimbJnt,
                 lowerLimbJnt,
                 endLimbJnt,
                 lowerLimbScaleJnt,
                 endLimbScaleJnt,
                 upperLimbFkJnt,
                 middleLimbFkJnt,
                 lowerLimbFkJnt,
                 upperLimbIkJnt,
                 middleLimbIkJnt,
                 lowerLimbIkJnt,
                 endLimbIkJnt,
                 baseOrTipShapeJoint,
                 upperLimbShapeJoint,
                 middleLimbShapeJoint,
                 lowerLimbShapeJoint,
                 pelvisJnt,
                 world,
                 upperLimbDtlJnt,
                 middleLimbDtlJnt,
                 upperLimbDtlBind,
                 middleLimbDtlBind,
                 detailLimbDeformer,
                 numDtlCtrl,
                 parallelAxis,
                 tipPos,
                 prefixUpperLimbDtl,
                 prefixMiddleLimbDtl,
                 size=generalScale):

        if limb:
            getValueTxLimbJnt = mc.xform(upperLimbIkJnt, ws=1, q=1, t=1)[0]

        ### GENERAL LIMB SETUP
            # limb position
            # create limb pole vector position
            ikhVectPos = mc.ikHandle(sj=upperLimbIkJnt, ee=lowerLimbIkJnt, sol='ikRPsolver')
            locPVPos = pv.create_poleVec_locator(ikhVectPos[0], constraint=False, length=4 * size)

        # ==============================================================================================================
        #                                               IMPORT LIMB MODULE
        # ==============================================================================================================
            buildLimb= lm.Build(
                arm=arm,
                prefix=prefix,
                prefixUpperLimb=prefixUpperLimb,
                prefixPoleVecLimb=prefixPoleVecLimb,
                prefixLowerLimb=prefixLowerLimb,
                prefixBaseOrTipLimb=prefixBaseOrTipLimb,
                prefix_upper_limb_dtl=prefixUpperLimbDtl,
                prefix_middle_limb_dtl=prefixMiddleLimbDtl,
                prefix_upper_limb_fk=prefixUpperLimbFk,
                prefix_middle_limb_fk=prefixMiddleLimbFk,
                prefix_lower_limb_fk=prefixLowerLimbFk,
                prefix_upper_limb_ik=prefixUpperLimbIk,
                prefix_pole_vector_ik=prefixPoleVectorIk,
                prefix_middle_limb_ik=prefixMiddleLimbIk,
                prefix_lower_limb_ik=prefixLowerLimbIk,
                prefix_end_limb_ik=prefixEndLimbIk,
                prefix_limb_setup=prefixLimbSetup,
                side=side,
                upper_limb_jnt=upperLimbJnt,
                middle_limb_jnt= middleLimbJnt,
                lower_limb_jnt= lowerLimbJnt,
                upper_limb_fk_jnt=upperLimbFkJnt,
                middle_limb_fk_jnt=middleLimbFkJnt,
                lower_limb_fk_jnt=lowerLimbFkJnt,
                upper_limb_ik_jnt=upperLimbIkJnt,
                middle_limb_ik_jnt=middleLimbIkJnt,
                pole_vector_ik_jnt=locPVPos[0],
                lower_limb_ik_jnt=lowerLimbIkJnt,
                end_limb_ik_jnt=endLimbIkJnt,
                detail_limb_deformer=detailLimbDeformer,
                numJoint=numDtlCtrl,
                baseTipShapeJoint=baseOrTipShapeJoint,
                upperLimbShapeJoint=upperLimbShapeJoint,
                poleVecLimbShapeJoint=middleLimbShapeJoint,
                lowerLimbShapeJoint=lowerLimbShapeJoint,
                scale=size)

            # delete locator pole vector pos
            mc.delete(locPVPos)

            self.prefix = prefix

            self.parentConsElm = None

            # build part of group hierarchy
            part = gm.Part(prefix=prefix, side=side, baseObj=base)

            # instance the objects
            self.fkIkLimbSetupControllerGrpZro   = buildLimb.controller_FkIk_limb_setup.parentControl[0]
            self.fkIkLimbSetupController         = buildLimb.controller_FkIk_limb_setup.control

            # Fk
            self.upperLimbFkControllerGrpZro = buildLimb.controller_upper_limb_fk.parentControl[0]
            self.middleLimbFkControllerGrpZro  = buildLimb.controller_middle_limb_fk.parentControl[0]
            self.lowerLimbFkControllerGrpZro    = buildLimb.controller_lower_limb_fk.parentControl[0]

            self.upperLimbFkGimbal   = buildLimb.controller_upper_limb_fk.controlGimbal
            self.middleLimbFkGimbal    = buildLimb.controller_middle_limb_fk.controlGimbal
            self.lowerLimbFkGimbal    = buildLimb.controller_lower_limb_fk.controlGimbal


            # Ik
            self.upperLimbIkControllerGrpZro = buildLimb.controller_upper_limb_ik.parentControl[0]
            self.poleVecIkControllerGrpZro    = buildLimb.controller_pole_vector_ik.parentControl[0]
            self.lowerLimbIkControllerGrpZro    = buildLimb.controller_lower_limb_ik.parentControl[0]

            self.upperLimbIkGimbal = buildLimb.controller_upper_limb_ik.controlGimbal
            self.lowerLimbIkGimbal = buildLimb.controller_lower_limb_ik.controlGimbal
            self.upperLimbIkControl = buildLimb.controller_upper_limb_ik.control
            self.lowerLimbIkControl = buildLimb.controller_lower_limb_ik.control

            # limb ikh
            self.lowerLimbIkHdl = buildLimb.lower_limb_ik_hdl[0]
            self.endLimbIkHdl = buildLimb.end_limb_ik_hdl[0]

            # locator following
            if arm:
                self.shoulderFkLoc = buildLimb.shoulder_fk
                self.hipFkLoc      = buildLimb.hip_fk
                self.worldFkLoc    = buildLimb.world_fk

                self.shoulderIkLoc = buildLimb.shoulder_ik
                self.hipIkLoc      = buildLimb.hip_ik
                self.worldIkLoc    = buildLimb.world_ik

                ### FOLLOW ORIENTATION
                # constraining follow Fk
                mc.parentConstraint(clavJnt, self.shoulderFkLoc, mo=1)
                mc.parentConstraint(rootJnt, self.hipFkLoc, mo=1)
                mc.parentConstraint(base.animControl, self.worldFkLoc, mo=1)

                # constraining follow Ik
                mc.parentConstraint(clavJnt, self.upperLimbIkControllerGrpZro, mo=1)

                mc.parentConstraint(clavJnt, self.shoulderIkLoc, mo=1)
                mc.parentConstraint(rootJnt, self.hipIkLoc, mo=1)
                mc.parentConstraint(base.animControl, self.worldIkLoc, mo=1)

                mc.parent(self.shoulderFkLoc, part.locGrp)
                mc.parent(self.hipFkLoc, part.locGrp)
                mc.parent(self.worldFkLoc, part.locGrp)

                mc.parent(self.shoulderIkLoc, part.locGrp)
                mc.parent(self.hipIkLoc, part.locGrp)
                mc.parent(self.worldIkLoc, part.locGrp)

            else:
                self.hipFkLoc = buildLimb.hip_fk
                self.worldFkLoc = buildLimb.world_fk

                self.hipIkLoc = buildLimb.hip_ik
                self.worldIkLoc = buildLimb.world_ik
                ### FOLLOW ORIENTATION
                # constraining follow Fk
                mc.parentConstraint(pelvisJnt, self.hipFkLoc, mo=1)
                mc.parentConstraint(base.animControl, self.worldFkLoc, mo=1)

                # constraining follow Ik
                mc.parentConstraint(pelvisJnt, self.upperLimbIkControllerGrpZro, mo=1)

                mc.parentConstraint(pelvisJnt, self.hipIkLoc, mo=1)
                mc.parentConstraint(base.animControl, self.worldIkLoc, mo=1)

                mc.parent(self.hipFkLoc, part.locGrp)
                mc.parent(self.worldFkLoc, part.locGrp)

                mc.parent(self.hipIkLoc, part.locGrp)
                mc.parent(self.worldIkLoc, part.locGrp)

                # parent scale joint to joint driver
                mc.parent(lowerLimbScaleJnt, lowerLimbJnt)
                # connect scale
                self.footScale(self.fkIkLimbSetupController, lowerLimbScaleJnt)

                # connect attribute translate and rotate
                mc.connectAttr(endLimbJnt+'.translate', endLimbScaleJnt+'.translate')
                mc.connectAttr(endLimbJnt+'.rotate', endLimbScaleJnt+'.rotate')



            # control combine detail
            self.ctrlCombineDtl = buildLimb.ctrl_mid_middle_limb.control

            # control group in part
            self.partControlGrp = part.controlGrp

            # parent setup to part group
            # controller
            mc.parent(self.fkIkLimbSetupControllerGrpZro, part.controlGrp)
            mc.parent(buildLimb.ctrl_mid_middle_limb.parentControl[0], part.controlGrp)

            # joint
            self.partJointGrp = part.jointGrp
            mc.parent(buildLimb.pos_upper_limb_jnt, part.jointGrp)
            mc.parent(buildLimb.pos_pole_vector_jnt, part.jointGrp)
            mc.parent(buildLimb.position_softIk_jnt, part.jointGrp)
            mc.parent(buildLimb.position_limb_jnt, part.jointGrp)

            # non-trans
            mc.parent(buildLimb.curve_poleVector_ik, part.nonTransform)

        ### FK SETUP
            # parent joint FK driver to joint grp
            mc.parent(upperLimbFkJnt, base.jntGrp)

            # parent lower to middle limb control group
            mc.parent(self.lowerLimbFkControllerGrpZro, self.middleLimbFkGimbal)

            # parent middle limb to upper limb control group
            mc.parent(self.middleLimbFkControllerGrpZro, self.upperLimbFkGimbal)

            # parent all limb to part control group
            mc.parent(self.upperLimbFkControllerGrpZro, part.controlGrp)

            # connect scale module to decompose matrix
            mc.connectAttr(base.animControl +'.worldMatrix[0]', buildLimb.scale_decompose + '.inputMatrix')

            # stretch FK middle limb
            mc.connectAttr(buildLimb.upper_stretch_limb_fk + '.output',
                           self.middleLimbFkControllerGrpZro + '.translateY')

            # stretch FK wrist
            mc.connectAttr(buildLimb.middle_stretch_limb_fk + '.output',
                           self.lowerLimbFkControllerGrpZro + '.translateY')

        ### IK SETUP
            # parent joint IK driver to joint grp
            mc.parent(upperLimbIkJnt, base.jntGrp)

            # parent upper limb to part control group
            mc.parent(self.upperLimbIkControllerGrpZro, part.controlGrp)

            # parent elbow to part control group
            mc.parent(self.poleVecIkControllerGrpZro, part.controlGrp)

            # parent wrist to part control group
            mc.parent(self.lowerLimbIkControllerGrpZro, part.controlGrp)

            # point constraint the stretching the limb
            mc.pointConstraint(self.upperLimbIkGimbal, buildLimb.pos_upper_limb_jnt, mo=1)

            # aim constraining for stretching the limb
            mc.aimConstraint(self.lowerLimbIkGimbal, buildLimb.pos_upper_limb_jnt, mo=1, aim=(0.0, 1.0, 0.0),
                             u=(-1.0,0.0,0.0), wut='objectrotation', wu= (0.0,1.0,0.0), wuo=part.jointGrp)

            # ELBOW FOLLOWING LIMB
            elbowFollowConst = mc.parentConstraint(self.lowerLimbIkControl, world, self.poleVecIkControllerGrpZro, mo=1)[0]
            mc.connectAttr(buildLimb.controller_pole_vector_ik.control + '.follow', elbowFollowConst + '.%sW0' % self.lowerLimbIkControl)

            elbowConsRev = mc.shadingNode('reverse', asUtility=1, n='%s%s%s_rev' % (prefixPoleVectorIk, 'Follow', side))
            mc.connectAttr(buildLimb.controller_pole_vector_ik.control + '.follow', elbowConsRev + '.inputX')
            mc.connectAttr(elbowConsRev+'.outputX', elbowFollowConst+'.%sW1' % world)

            # set ikRPsolver
            mc.setAttr("ikRPsolver.tolerance", 1e-09)

            # constraining the controller Fk/Ik
            mc.parentConstraint(lowerLimbJnt, self.fkIkLimbSetupControllerGrpZro, mo=1)

        ## IMPORT DETAIL LIMB MODULE
            # parenting all joints to joint grp
            mc.parent(upperLimbDtlJnt, upperLimbDtlBind, base.jntGrp)
            mc.parent(middleLimbDtlBind, base.jntGrp)

            # constraint from limb driver to limb bind
            mc.parentConstraint(upperLimbJnt, upperLimbDtlBind, mo=1)
            mc.parentConstraint(middleLimbJnt, middleLimbDtlBind, mo=1)

            self.posLowerLimbJnt = buildLimb.pos_lower_limb_jnt
            self.posSoftJnt = buildLimb.position_softIk_jnt

        # ==============================================================================================================
        #                                                     DETAIL
        # ==============================================================================================================
        # DETAIL SETUP
            # spline ik detail driver
            # get attibute upper limb jnt
            upperLimbDtlJoint = mc.xform(upperLimbDtlJnt, q=1, ws=True, t=1)
            middleLimbDtlJoint  = mc.xform(middleLimbDtlJnt, q=1, ws=True, t=1)

            # create curve for ik spline
            curveIkSplineDtl  = mc.curve(d=1, p=[upperLimbDtlJoint, middleLimbDtlJoint])
            self.limbDetailHdl = mc.ikHandle(sj=upperLimbDtlJnt, ee=middleLimbDtlJnt, sol='ikSplineSolver',
                                             n='%s%s_hdl' % (prefixUpperLimbIk + 'Dtl', side), ccv=False, c=curveIkSplineDtl, ns=1, rootOnCurve=True)
            dtlHdlCrv = mc.rename(curveIkSplineDtl, '%s%s_crv' % (prefixUpperLimbIk + 'Dtl', side))

            # hide the curve spline Ik
            mc.hide(dtlHdlCrv)

            # skin the spline curve
            mc.skinCluster(upperLimbDtlBind, middleLimbDtlBind, dtlHdlCrv, tsb=True, mi=1)

            # parent to part grp
            mc.parent(self.limbDetailHdl[0], part.utilsGrp)
            mc.parent(dtlHdlCrv, part.nonTransform)

            # divided value in every index
            num = (1.0 / (numDtlCtrl + 1))

        # ==============================================================================================================
        #                                               UPPER LIMB DETAIL
        # ==============================================================================================================
            dtlUpperLimb = dl.CreateDetail(
                         detail_limb_deformer=detailLimbDeformer,
                         base=upperLimbDtlJnt,
                         tip=middleLimbDtlBind,
                         parallel_axis=parallelAxis,
                         tip_pos=tipPos,
                         ctrl_tip=ct.SQUARE,
                         ctrl_mid=ct.SQUARE,
                         ctrl_base=ct.SQUARE,
                         ctrl_details=ct.CIRCLEPLUS,
                         ctrl_color='lightPink',
                         prefix=prefixUpperLimbDtl,
                         side=side,
                         scale=size,
                         volume_pos_min=2,
                         volume_pos_max=0,
                         number_joints=numDtlCtrl)

            # set grp follicle upper limb
            self.setGrpFollUpperLimb = dtlUpperLimb.follicle_set_grp

            self.setGrpFollTwistUpperLimb = dtlUpperLimb.follicle_grp_twist

            # parent main grp to still grp
            mc.parent(dtlUpperLimb.grp_no_transform_zro, base.stillGrp)
            mc.parent(dtlUpperLimb.grp_transform_zro, part.controlGrp)

            # scale connect
            mc.connectAttr(base.scaleMatrixNode +'.outputScale', dtlUpperLimb.grp_transform + '.scale')

            # parent constraint detail bind to grp transform detail
            mc.parentConstraint(upperLimbDtlBind, dtlUpperLimb.grp_transform, mo=1)

            # parent contraint detail jnt driver to grp offset upper limb
            mc.parentConstraint(upperLimbDtlJnt, dtlUpperLimb.ctrl_up.parentControl[1])

            # parent contraint detail jnt driver to grp offset middle limb
            mc.parentConstraint(middleLimbDtlBind, dtlUpperLimb.ctrl_down.parentControl[1], mo=1)

            #connect attribute to twist grp
            ctrlTwistMdl = mc.shadingNode('multDoubleLinear', asUtility=1, n='%s%s%s_mdl' % (prefixUpperLimbDtl, 'MultCtrlTwist', side))

            mc.connectAttr(upperLimbDtlJnt + '.rotateX', ctrlTwistMdl + '.input1')
            mc.connectAttr(buildLimb.controller_FkIk_limb_setup.control + '.%s%s' % (prefix, 'MultTwist'), ctrlTwistMdl + '.input2')

            mc.connectAttr(ctrlTwistMdl +'.output', dtlUpperLimb.ctrl_up.parentControl[2] + '.rotateY')

            ### TWIST UPPER LIMB SETUP
            # create multi matrix
            multMtxCtrlUp   = mc.shadingNode('multMatrix', asUtility=1, n='%s%s%s_mmtx' % (prefixUpperLimbDtl, 'CtrlUp', side))
            multMtxCtrlDown = mc.shadingNode('multMatrix', asUtility=1, n='%s%s%s_mmtx' % (prefixUpperLimbDtl, 'CtrlDown', side))

            mc.connectAttr(dtlUpperLimb.ctrl_up.control + '.worldMatrix[0]', multMtxCtrlUp + '.matrixIn[0]')
            mc.connectAttr(dtlUpperLimb.ctrl_down.parentControl[0] + '.worldInverseMatrix[0]', multMtxCtrlUp + '.matrixIn[1]')

            mc.connectAttr(dtlUpperLimb.ctrl_down.control + '.worldMatrix[0]', multMtxCtrlDown + '.matrixIn[0]')
            mc.connectAttr(dtlUpperLimb.ctrl_up.parentControl[0] + '.worldInverseMatrix[0]', multMtxCtrlDown + '.matrixIn[1]')

            # create decompose matrix
            decomposeMtxCtrlUp   = mc.shadingNode('decomposeMatrix', asUtility=1, n='%s%s%s_dmtx' % (prefixUpperLimbDtl, 'CtrlUp', side))
            decomposeMtxCtrlDown = mc.shadingNode('decomposeMatrix', asUtility=1, n='%s%s%s_dmtx' % (prefixUpperLimbDtl, 'CtrlDown', side))

            mc.connectAttr(multMtxCtrlUp+'.matrixSum', decomposeMtxCtrlUp+'.inputMatrix')
            mc.connectAttr(multMtxCtrlDown+'.matrixSum', decomposeMtxCtrlDown+'.inputMatrix')

            # create quat to euler
            quatCtrlUp   = mc.shadingNode('quatToEuler', asUtility=1, n='%s%s%s_qte' % (prefixUpperLimbDtl, 'CtrlUp', side))
            quatCtrlDown = mc.shadingNode('quatToEuler', asUtility=1, n='%s%s%s_qte' % (prefixUpperLimbDtl, 'CtrlDown', side))

            # set rotation order to zxy
            mc.setAttr(quatCtrlUp+'.inputRotateOrder', 2)
            mc.setAttr(quatCtrlDown + '.inputRotateOrder', 2)

            mc.connectAttr(decomposeMtxCtrlUp+'.outputQuatY', quatCtrlUp+'.inputQuatY')
            mc.connectAttr(decomposeMtxCtrlUp+'.outputQuatW', quatCtrlUp+'.inputQuatW')

            mc.connectAttr(decomposeMtxCtrlDown+'.outputQuatY', quatCtrlDown+'.inputQuatY')
            mc.connectAttr(decomposeMtxCtrlDown+'.outputQuatW', quatCtrlDown+'.inputQuatW')

            ctrlUpMdlNode       = []
            ctrlDownMdlNode     = []
            sumUpDownMatrixNode = []

            for i in range(len(self.setGrpFollTwistUpperLimb)):
                value = num*i
                # ctrl up mult double linear
                ctrlUpMdl = mc.shadingNode('multDoubleLinear', asUtility=1,
                                           n='%s%s%s%s_mdl' % (prefixUpperLimbDtl, str(i + 1).zfill(2) , 'MultCtrlUp', side))

                mc.setAttr(ctrlUpMdl+'.input2', value)
                ctrlUpMdlNode.append(ctrlUpMdl)

                # ctrl down mult double linear
                ctrlDownMdl = mc.shadingNode('multDoubleLinear', asUtility=1,
                                             n='%s%s%s%s_mdl' % (prefixUpperLimbDtl, str(i + 1).zfill(2) , 'MultCtrlDown', side))
                mc.setAttr(ctrlDownMdl + '.input2', value)
                ctrlDownMdlNode.append(ctrlDownMdl)

                # connect quatCtrlDown and quatCtrlUp to respective multiply node
                mc.connectAttr(quatCtrlUp+'.outputRotateY', ctrlUpMdl+'.input1')
                mc.connectAttr(quatCtrlDown + '.outputRotateY', ctrlDownMdl + '.input1')

                # create matrix node for twist upper limb
                sumUpDownMatrix = mc.shadingNode('plusMinusAverage', asUtility=1,
                                                 n='%s%s%s%s_pma' % (prefixUpperLimbDtl, str(i + 1).zfill(2), 'SumUpDown', side))
                sumUpDownMatrixNode.append(sumUpDownMatrix)

            for up, down, pma, twst in zip (ctrlUpMdlNode[::-1], ctrlDownMdlNode, sumUpDownMatrixNode, self.setGrpFollTwistUpperLimb):
                mc.connectAttr(up+'.output', pma+'.input1D[0]')
                mc.connectAttr(down+'.output', pma+'.input1D[1]')
                mc.connectAttr(pma + '.output1D', twst + '.rotateY')

        # ==============================================================================================================
        #                                               MIDDLE LIMB DETAIL
        # ==============================================================================================================
            dtlLowerLimb = dl.CreateDetail(
                detail_limb_deformer=detailLimbDeformer,
                base=middleLimbDtlBind,
                tip=lowerLimbJnt,
                parallel_axis=parallelAxis,
                tip_pos=tipPos,
                ctrl_tip=ct.SQUARE,
                ctrl_mid=ct.SQUARE,
                ctrl_base=ct.SQUARE,
                ctrl_details=ct.CIRCLEPLUS,
                ctrl_color='turquoiseBlue',
                prefix=prefixMiddleLimbDtl,
                side=side,
                scale=size,
                volume_pos_min=0,
                volume_pos_max=2,
                number_joints=numDtlCtrl)

            # set grp follicle middle limb
            self.setGrpFollMiddleLimb = dtlLowerLimb.follicle_set_grp

            self.setGrpFollTwistMiddleLimb = dtlLowerLimb.follicle_grp_twist

            # parent main grp to still grp
            mc.parent(dtlLowerLimb.grp_no_transform_zro, base.stillGrp)
            mc.parent(dtlLowerLimb.grp_transform_zro, part.controlGrp)

            # scale connect
            mc.connectAttr(base.scaleMatrixNode +'.outputScale', dtlLowerLimb.grp_transform + '.scale')

            # constraining middle limb bind dtl to middle limb grp transform
            mc.parentConstraint(middleLimbDtlBind, dtlLowerLimb.grp_transform, mo=1)

            # constraining wrist to middle limb down ctrl detail
            mc.parentConstraint(lowerLimbJnt, dtlLowerLimb.ctrl_down.parentControl[1])

            ### TWIST MIDDLE LIMB SETUP
            # create multi matrix
            multMtxCtrlFaDown = mc.shadingNode('multMatrix', asUtility=1,
                                               n='%s%s%s_mmtx' % (prefixMiddleLimbDtl, 'CtrlDown', side))

            mc.connectAttr(dtlLowerLimb.ctrl_down.control + '.worldMatrix[0]', multMtxCtrlFaDown + '.matrixIn[0]')
            mc.connectAttr(dtlLowerLimb.ctrl_up.parentControl[0] + '.worldInverseMatrix[0]', multMtxCtrlFaDown + '.matrixIn[1]')

            # create decompose matrix
            decomposeMtxCtrlFaDown = mc.shadingNode('decomposeMatrix', asUtility=1,
                                                    n='%s%s%s_dmtx' % (prefixMiddleLimbDtl, 'CtrlDown', side))
            mc.connectAttr(multMtxCtrlFaDown + '.matrixSum', decomposeMtxCtrlFaDown + '.inputMatrix')

            # create quat to euler
            quatCtrlFaDown = mc.shadingNode('quatToEuler', asUtility=1, n='%s%s%s_qte' % (prefixMiddleLimbDtl, 'CtrlDown', side))

            # set rotation order to zxy
            mc.setAttr(quatCtrlFaDown+'.inputRotateOrder', 2)

            mc.connectAttr(decomposeMtxCtrlFaDown + '.outputQuatY', quatCtrlFaDown + '.inputQuatY')
            mc.connectAttr(decomposeMtxCtrlFaDown + '.outputQuatW', quatCtrlFaDown + '.inputQuatW')

            ctrlDownFaMdlNode = []
            for i in range(len(self.setGrpFollTwistMiddleLimb)):
                value = num*i
                # ctrl down mult double linear
                ctrlDownFaMdl = mc.shadingNode('multDoubleLinear', asUtility=1,
                                               n='%s%s%s%s_mdl' % (prefixMiddleLimbDtl, str(i + 1).zfill(2),'MultCtrlDown', side))
                mc.setAttr(ctrlDownFaMdl + '.input2', value)
                ctrlDownFaMdlNode.append(ctrlDownFaMdl)

                # connect quatCtrlDown  to respective multiply node
                mc.connectAttr(quatCtrlFaDown + '.outputRotateY', ctrlDownFaMdl + '.input1')

            for down, twst in zip (ctrlDownFaMdlNode, self.setGrpFollTwistMiddleLimb):
                mc.connectAttr(down+'.output',  twst + '.rotateY')

        # ==============================================================================================================
        #                                               SCALE LIMB
        # ==============================================================================================================
            # upper limb
            self.limbPartScale(prefix=prefix, controller=self.fkIkLimbSetupController, groupScale=self.setGrpFollTwistUpperLimb)

            # middle limb
            self.limbPartScale(prefix=prefix, controller=self.fkIkLimbSetupController, groupScale=self.setGrpFollTwistMiddleLimb)

        # ==============================================================================================================
        #                                               COMBINED DETAIL
        # ==============================================================================================================
            # parent constraint from middle limb bind to limb detail combine
            mc.parentConstraint(middleLimbDtlBind, buildLimb.ctrl_mid_middle_limb.parentControl[0])

            # point ccnstraint to respective module upper limb detail and middle limb detail combine
            mc.pointConstraint(self.ctrlCombineDtl, dtlUpperLimb.ctrl_down.parentControl[2])
            mc.pointConstraint(self.ctrlCombineDtl, dtlLowerLimb.ctrl_up.parentControl[2])

            if detailLimbDeformer:
                ### CONNECT ROLL
                # disconnect from detail roll to plus minus average
                mc.disconnectAttr(dtlUpperLimb.ctrl_down.control + '.twist', dtlUpperLimb.sum_top_pma + '.input1D[0]')
                mc.disconnectAttr(dtlLowerLimb.ctrl_up.control + '.twist', dtlLowerLimb.sum_end_pma + '.input1D[0]')

                # connect attribute from respective control module to add double linear control
                mc.connectAttr(dtlUpperLimb.ctrl_down.control + '.twist', buildLimb.adl_upper_limb_combine + '.input1')
                mc.connectAttr(dtlLowerLimb.ctrl_up.control + '.twist', buildLimb.adl_middle_limb_combine + '.input1')

                # connect output of adl combine node to plus minus average upper limb and middle limb roll node
                mc.connectAttr(buildLimb.adl_upper_limb_combine + '.output', dtlUpperLimb.sum_top_pma + '.input1D[0]')
                mc.connectAttr(buildLimb.adl_middle_limb_combine + '.output', dtlLowerLimb.sum_end_pma + '.input1D[0]')

                ### CONNECT VOLUME POSITION
                # volume position combined
                if tipPos=='-':
                    # v upper limb LFT
                    self.combineVolumeDetail(dtlUpperLimb.combine_vol_position_adl, self.ctrlCombineDtl, numDtlCtrl,
                                             minMult=1, midMult=-1, maxMult=-1)
                    # detail middle limb LFT
                    self.combineVolumeDetail(dtlLowerLimb.combine_vol_position_adl, self.ctrlCombineDtl, numDtlCtrl,
                                             minMult=1, midMult=1, maxMult=-1)

                if tipPos == '+':
                    # v upper limb LFT
                    self.combineVolumeDetail(dtlUpperLimb.combine_vol_position_adl, self.ctrlCombineDtl, numDtlCtrl,
                                             minMult=-1, midMult=1, maxMult=1)
                    # detail middle limb LFT
                    self.combineVolumeDetail(dtlLowerLimb.combine_vol_position_adl, self.ctrlCombineDtl, numDtlCtrl,
                                             minMult=-1, midMult=-1, maxMult=1)

                #### CONNECT VOLUME
                # connect to multdouble linear volume detail to volume add double linear detail
                # upper limb
                mc.connectAttr(buildLimb.volume_pos_mdl_upper_limb + '.output', dtlUpperLimb.volume_reverse_adl + '.input1')

                # middle limb
                mc.connectAttr(buildLimb.volume_pos_mdl_middle_limb + '.output', dtlLowerLimb.volume_reverse_adl + '.input1')

                ### CONNECT MULTIPLIER VOLUME
                for ua, fa in zip (dtlUpperLimb.combine_mult_all, dtlLowerLimb.combine_mult_all):
                    mc.connectAttr(self.ctrlCombineDtl+'.volumeMultiplier', ua+'.input2')
                    mc.connectAttr(self.ctrlCombineDtl+'.volumeMultiplier', fa+'.input2')

                ### CONNECT SINE SETUP
                mc.connectAttr(self.ctrlCombineDtl +'.amplitude', dtlUpperLimb.combine_sine_amplitude + '.input1')
                mc.connectAttr(self.ctrlCombineDtl +'.amplitude', dtlLowerLimb.combine_sine_amplitude + '.input1')
                mc.connectAttr(self.ctrlCombineDtl +'.wide', dtlUpperLimb.combine_sine_wide + '.input1')
                mc.connectAttr(self.ctrlCombineDtl +'.wide', dtlLowerLimb.combine_sine_wide + '.input1')
                mc.connectAttr(self.ctrlCombineDtl +'.sineRotate', dtlUpperLimb.combine_sine_rotate + '.input1')
                mc.connectAttr(self.ctrlCombineDtl +'.sineRotate', dtlLowerLimb.combine_sine_rotate + '.input1')
                mc.connectAttr(self.ctrlCombineDtl +'.offset', dtlUpperLimb.combine_sine_offset + '.input1')
                mc.connectAttr(self.ctrlCombineDtl +'.offset', dtlLowerLimb.combine_sine_offset + '.input1')
                mc.connectAttr(self.ctrlCombineDtl +'.twist', dtlUpperLimb.combine_sine_twist + '.input1')
                mc.connectAttr(self.ctrlCombineDtl +'.twist', dtlLowerLimb.combine_sine_twist + '.input1')
                mc.connectAttr(self.ctrlCombineDtl +'.sineLength', dtlUpperLimb.combine_sine_length + '.input1')
                mc.connectAttr(self.ctrlCombineDtl +'.sineLength', dtlLowerLimb.combine_sine_length + '.input1')

            # connect the visibility-switch for the controller
            # switch on/off detail module ctrl
            mc.connectAttr(self.ctrlCombineDtl +'.detailBaseCtrlVis', dtlUpperLimb.ctrl_up.parentControl[0] + '.visibility')
            mc.connectAttr(self.ctrlCombineDtl +'.detailBaseCtrlVis', dtlUpperLimb.ctrl_down.parentControl[0] + '.visibility')
            mc.connectAttr(self.ctrlCombineDtl +'.detailBaseCtrlVis', dtlLowerLimb.ctrl_up.parentControl[0] + '.visibility')
            mc.connectAttr(self.ctrlCombineDtl +'.detailBaseCtrlVis', dtlLowerLimb.ctrl_down.parentControl[0] + '.visibility')

    # ==================================================================================================================
    #                                               FUNCTION LIMB MODULE
    # ==================================================================================================================
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

    def limbPartScale(self, prefix, controller, groupScale):
        # LIMB SCALE
        for i in groupScale:
            mc.connectAttr(controller + '.%s%s' %(prefix, 'Scale'), i + '.scaleX')
            mc.connectAttr(controller + '.%s%s' %(prefix, 'Scale'), i + '.scaleY')
            mc.connectAttr(controller + '.%s%s' %(prefix, 'Scale'), i + '.scaleZ')

    def footScale(self, controller, ankleJnt):
        mc.connectAttr(controller + '.footScale', ankleJnt + '.scaleX')
        mc.connectAttr(controller + '.footScale', ankleJnt + '.scaleY')
        mc.connectAttr(controller + '.footScale', ankleJnt + '.scaleZ')
