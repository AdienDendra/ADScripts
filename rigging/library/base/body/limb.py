"""
creating limb module base
"""
from __future__ import absolute_import

import maya.cmds as cmds

from rigging.library.utils import rotationController as rlu_rotationController, controller as rlu_controller
from rigging.tools import utils as rt_utils


class Build:
    def __init__(self,
                 arm,
                 prefix,
                 prefix_upper_limb_dtl,
                 prefix_middle_limb_dtl,
                 prefix_upper_limb_fk,
                 prefix_middle_limb_fk,
                 prefix_lower_limb_fk,
                 prefix_upper_limb_ik,
                 prefix_pole_vector_ik,
                 prefix_middle_limb_ik,
                 prefix_lower_limb_ik,
                 prefix_end_limb_ik,
                 prefix_limb_setup,
                 side,
                 upper_limb_jnt,
                 middle_limb_jnt,
                 lower_limb_jnt,
                 upper_limb_fk_jnt,
                 middle_limb_fk_jnt,
                 lower_limb_fk_jnt,
                 upper_limb_ik_jnt,
                 middle_limb_ik_jnt,
                 pole_vector_ik_jnt,
                 lower_limb_ik_jnt,
                 end_limb_ik_jnt,
                 detail_limb_deformer,
                 number_joints,
                 scale
                 ):
        # ==================================================================================================================
        #                                                 FK CONTROLLER
        # ==================================================================================================================
        ### CREATE CONTROL FK
        self.controller_upper_limb_fk = rlu_controller.Control(match_obj_first_position=upper_limb_fk_jnt,
                                                               prefix='%s' % prefix_upper_limb_fk, side=side,
                                                               shape=rlu_controller.CIRCLEPLUS,
                                                               groups_ctrl=['Zro', 'Offset'], ctrl_size=scale,
                                                               ctrl_color='yellow', gimbal=True,
                                                               lock_channels=['v', 's'],
                                                               connection=['parent'])

        self.controller_middle_limb_fk = rlu_controller.Control(match_obj_first_position=middle_limb_fk_jnt,
                                                                prefix='%s' % (prefix_middle_limb_fk), side=side,
                                                                shape=rlu_controller.CIRCLEPLUS,
                                                                groups_ctrl=['Zro', 'Offset'], ctrl_size=scale,
                                                                ctrl_color='yellow', gimbal=True,
                                                                lock_channels=['v', 's'],
                                                                connection=['parent'])

        self.controller_lower_limb_fk = rlu_controller.Control(match_obj_first_position=lower_limb_fk_jnt,
                                                               prefix='%s' % (prefix_lower_limb_fk), side=side,
                                                               shape=rlu_controller.CIRCLEPLUS,
                                                               groups_ctrl=['Zro', 'Offset'], ctrl_size=scale,
                                                               ctrl_color='yellow', gimbal=True,
                                                               lock_channels=['v', 's'],
                                                               connection=['parent'])

        ### ADD ATTRIBUTE FOR FK CONTROLLER
        rt_utils.add_attribute(objects=[self.controller_upper_limb_fk.control], long_name=['stretch'],
                               at="float", dv=0, keyable=True)
        if arm:
            rt_utils.add_attribute(objects=[self.controller_upper_limb_fk.control], long_name=['follow'],
                                   at="enum", en='shoulder:hip:world:', keyable=True)
        else:
            rt_utils.add_attribute(objects=[self.controller_upper_limb_fk.control], long_name=['follow'],
                                   at="enum", en='hip:world:', keyable=True)

        rt_utils.add_attribute(objects=[self.controller_middle_limb_fk.control], long_name=['stretch'],
                               at="float", dv=0, keyable=True)

        ### FK LIMB SETUP
        self.upper_stretch_limb_fk = self.limb_stretch_fk(limb_fk_controller=self.controller_upper_limb_fk.control,
                                                          prefix_limb_fk=prefix_upper_limb_fk,
                                                          side=side, down_limb_fk_jnt=middle_limb_jnt)

        self.middle_stretch_limb_fk = self.limb_stretch_fk(limb_fk_controller=self.controller_middle_limb_fk.control,
                                                           prefix_limb_fk=prefix_middle_limb_fk,
                                                           side=side, down_limb_fk_jnt=lower_limb_jnt)

        # ==================================================================================================================
        #                                                IK CONTROLLER
        # ==================================================================================================================
        ### CREATE CONTROL IK
        self.controller_upper_limb_ik = rlu_controller.Control(match_obj_first_position=upper_limb_ik_jnt,
                                                               prefix='%s' % (prefix_upper_limb_ik), side=side,
                                                               shape=rlu_controller.CUBE,
                                                               groups_ctrl=['Zro', 'Offset'], ctrl_size=scale * 0.65,
                                                               ctrl_color='red', gimbal=True,
                                                               lock_channels=['v', 'r', 's'],
                                                               connection=['pointCons'])

        self.controller_pole_vector_ik = rlu_controller.Control(match_obj_first_position=pole_vector_ik_jnt,
                                                                prefix='%s' % (prefix_pole_vector_ik), side=side,
                                                                shape=rlu_controller.JOINT,
                                                                groups_ctrl=['Zro', 'Offset'], ctrl_size=scale * 0.25,
                                                                ctrl_color='red', gimbal=False,
                                                                lock_channels=['v', 'r', 's'],
                                                                connection=['pointCons'])

        self.controller_lower_limb_ik = rlu_controller.Control(match_obj_first_position=lower_limb_ik_jnt,
                                                               prefix='%s' % (prefix_lower_limb_ik), side=side,
                                                               shape=rlu_controller.CUBE,
                                                               groups_ctrl=['Zro', 'Offset'], ctrl_size=scale * 0.65,
                                                               ctrl_color='red', gimbal=True, lock_channels=['v', 's']
                                                               )

        ### ADD ATTRIBUTE FOR IK CONTROLLER
        if arm:
            rt_utils.add_attribute(objects=[self.controller_pole_vector_ik.control], long_name=['follow'],
                                   at="long", min=0, max=1, dv=0, keyable=True)

            self.limb_add_attr_ik(controller=self.controller_lower_limb_ik.control, follow='shoulder:hip:world:',
                                  prefix=prefix)
        else:
            rt_utils.add_attribute(objects=[self.controller_pole_vector_ik.control], long_name=['follow'],
                                   at="long", min=0, max=1, dv=1, keyable=True)

            self.limb_add_attr_ik(controller=self.controller_lower_limb_ik.control, follow='hip:world:',
                                  prefix=prefix)
        # ==================================================================================================================
        #                                                  IK LIMB SETUP
        # ==================================================================================================================

        # IK HANDLE AND POLE VECTOR
        self.lower_limb_ik_hdl = cmds.ikHandle(sj=upper_limb_ik_jnt, ee=lower_limb_ik_jnt, sol='ikRPsolver',
                                               n='%s%s_hdl' % (prefix_lower_limb_ik, side))
        self.end_limb_ik_hdl = cmds.ikHandle(sj=lower_limb_ik_jnt, ee=end_limb_ik_jnt, sol='ikSCsolver',
                                             n='%s%s_hdl' % (prefix_end_limb_ik, side))

        poleVector_lower_constraint = cmds.poleVectorConstraint(self.controller_pole_vector_ik.control,
                                                                self.lower_limb_ik_hdl[0])
        cmds.hide(self.end_limb_ik_hdl[0])
        # constraint rename
        rt_utils.constraint_rename(poleVector_lower_constraint)

        # IK STRETCH, ELBOW SNAP, SLIDE JOINT AND SOFT IK SETUP
        # create joints for distance
        # upper limb distance
        cmds.select(cl=1)
        self.pos_upper_limb_jnt = cmds.joint(n='%s%s%s_jnt' % (prefix_upper_limb_ik, 'Dist', side), radius=0.2 * scale)
        cmds.hide(self.pos_upper_limb_jnt)
        cmds.delete(cmds.pointConstraint(upper_limb_ik_jnt, self.pos_upper_limb_jnt))

        # elbow distance
        cmds.select(cl=1)
        self.pos_pole_vector_jnt = cmds.joint(n='%s%s%s_jnt' % (prefix_pole_vector_ik, 'Dist', side),
                                              radius=0.2 * scale)
        cmds.delete(cmds.parentConstraint(pole_vector_ik_jnt, self.pos_pole_vector_jnt))
        cmds.makeIdentity(self.pos_pole_vector_jnt, a=1, r=1, n=2, pn=1)
        cmds.hide(self.pos_pole_vector_jnt)

        # wrist distance
        cmds.select(cl=1)
        self.pos_lower_limb_jnt = cmds.joint(n='%s%s%s_jnt' % (prefix_lower_limb_ik, 'Dist', side), radius=0.2 * scale)
        cmds.hide(self.pos_lower_limb_jnt)
        cmds.delete(cmds.pointConstraint(lower_limb_ik_jnt, self.pos_lower_limb_jnt))

        # aiming the pos upper limb joint to wrist joint
        cmds.delete(
            cmds.aimConstraint(self.pos_upper_limb_jnt, self.pos_lower_limb_jnt, o=(0, 0, 0), w=1.0, aim=(0, -1, 0),
                               u=(-1, 0, 0),
                               wut='vector', wu=(0, 1, 0)))
        cmds.makeIdentity(self.pos_lower_limb_jnt, a=1, r=1, n=2, pn=1)

        # aiming the pos wrist joint to upper limb joint
        cmds.delete(
            cmds.aimConstraint(self.pos_lower_limb_jnt, self.pos_upper_limb_jnt, o=(0, 0, 0), w=1.0, aim=(0, 1, 0),
                               u=(-1, 0, 0),
                               wut='vector', wu=(0, 1, 0)))
        cmds.makeIdentity(self.pos_upper_limb_jnt, a=1, r=1, n=2, pn=1)

        # softIk distance
        cmds.select(cl=1)
        self.position_softIk_jnt = \
            cmds.duplicate(self.pos_lower_limb_jnt, name='%s%s%s_jnt' % (prefix, 'SoftIkDist', side))[0]

        # limb distance
        cmds.select(cl=1)
        self.position_limb_jnt = cmds.duplicate(self.pos_lower_limb_jnt, name='%s%s%s_jnt' % (prefix, 'Dist', side))[0]
        cmds.hide(self.position_limb_jnt)

        # create distance node length of limb
        distance_main_ik = self.limb_distance(prefix=prefix, pos_up_jnt=self.pos_upper_limb_jnt,
                                              pos_low_jnt=self.position_limb_jnt,
                                              dist_between_name='CtrlIkStretch', side=side)

        # create distance node from lower limb to soft ik jnt
        distance_lower_softIk = self.limb_distance(prefix=prefix, pos_up_jnt=self.pos_lower_limb_jnt,
                                                   pos_low_jnt=self.position_softIk_jnt,
                                                   dist_between_name='SoftIkStretch', side=side)

        # create distance node from upper limb to pole vector jnt
        distance_upper_poleVector = self.limb_distance(prefix=prefix_upper_limb_ik, pos_up_jnt=self.pos_upper_limb_jnt,
                                                       pos_low_jnt=self.pos_pole_vector_jnt,
                                                       dist_between_name='Snap', side=side)

        # create distance node from pole vector to soft ik jnt
        distance_poleVector_softIk = self.limb_distance(prefix=prefix_middle_limb_ik,
                                                        pos_up_jnt=self.pos_pole_vector_jnt,
                                                        pos_low_jnt=self.position_softIk_jnt,
                                                        dist_between_name='Snap', side=side)

        # parent and constraining the handle and some setup
        cmds.parent(self.pos_lower_limb_jnt, self.pos_upper_limb_jnt)
        cmds.parent(self.lower_limb_ik_hdl[0], self.end_limb_ik_hdl[0], self.position_softIk_jnt)

        # get attribute value distance
        distance_main_ik_value = cmds.getAttr(distance_main_ik + '.distance')

        ### SETTER VALUE FOR THE ATTRIBUTES
        # get value of tx wrist ik jnt
        get_value_tx_upper_limb_jnt = cmds.xform(upper_limb_ik_jnt, ws=1, q=1, t=1)[0]

        # get attribute of total length joint
        length_upper_limb = cmds.getAttr(middle_limb_ik_jnt + '.translateY')
        length_middle_limb = cmds.getAttr(lower_limb_ik_jnt + '.translateY')

        if get_value_tx_upper_limb_jnt > 0:
            length_upper_limb *= 1
            length_middle_limb *= 1
        else:
            length_upper_limb *= -1
            length_middle_limb *= -1

        # sum and offset by adding 1
        jnt_ik_mid_lower_sum = (length_middle_limb + length_upper_limb)
        subtract_ik_jnt_dist = (jnt_ik_mid_lower_sum - distance_main_ik_value)

        div_mid_value = length_upper_limb / jnt_ik_mid_lower_sum
        div_lower_value = length_middle_limb / jnt_ik_mid_lower_sum

        ## CREATE GENERAL SCALE IK NODES
        # decompose matrix soft Ik and slide
        self.scale_decompose = cmds.shadingNode('decomposeMatrix', asUtility=1,
                                                n='%s%s%s_dmtx' % (prefix, 'SoftSlideIkScale', side))
        self.scale_soft_slide_mdn = cmds.shadingNode('multiplyDivide', asUtility=1,
                                                     n='%s%s%s_mdn' % (prefix, 'SoftSlideIkScale', side))
        cmds.setAttr(self.scale_soft_slide_mdn + '.operation', 2)
        cmds.connectAttr(distance_main_ik + '.distance', self.scale_soft_slide_mdn + '.input1X')
        cmds.connectAttr(self.scale_decompose + '.outputScaleY', self.scale_soft_slide_mdn + '.input2X')

        # decompose matrix stretch
        self.scale_stretch_slide_mdn = cmds.shadingNode('multiplyDivide', asUtility=1,
                                                        n='%s%s%s_mdn' % (prefix, 'StretchIkScale', side))
        cmds.setAttr(self.scale_stretch_slide_mdn + '.operation', 2)
        cmds.connectAttr(distance_lower_softIk + '.distance', self.scale_stretch_slide_mdn + '.input1X')
        cmds.connectAttr(self.scale_decompose + '.outputScaleY', self.scale_stretch_slide_mdn + '.input2X')

        # decompose matrix snap middle limb
        self.scale_poleVector_snap_middle_mdn = cmds.shadingNode('multiplyDivide', asUtility=1,
                                                                 n='%s%s%s_mdn' % (prefix, 'SnapUrIkScale', side))
        cmds.setAttr(self.scale_poleVector_snap_middle_mdn + '.operation', 2)
        cmds.connectAttr(distance_upper_poleVector + '.distance', self.scale_poleVector_snap_middle_mdn + '.input1X')
        cmds.connectAttr(self.scale_decompose + '.outputScaleY', self.scale_poleVector_snap_middle_mdn + '.input2X')

        # decompose matrix snap lower limb
        self.scale_poleVector_snap_lower_mdn = cmds.shadingNode('multiplyDivide', asUtility=1,
                                                                n='%s%s%s_mdn' % (prefix, 'SnapLrIkScale', side))
        cmds.setAttr(self.scale_poleVector_snap_lower_mdn + '.operation', 2)
        cmds.connectAttr(distance_poleVector_softIk + '.distance', self.scale_poleVector_snap_lower_mdn + '.input1X')
        cmds.connectAttr(self.scale_decompose + '.outputScaleY', self.scale_poleVector_snap_lower_mdn + '.input2X')

        ## SOFT IK SETUP
        ### UPDATE REVISE
        # create pma for soft ik subtract scale and it self
        soft_ik_subtract_scale = cmds.shadingNode('plusMinusAverage', asUtility=1,
                                                  n='%s%s%s_pma' % (prefix, 'SoftIkSubtScale', side))
        cmds.setAttr(soft_ik_subtract_scale + '.operation', 2)
        cmds.setAttr(soft_ik_subtract_scale + '.input1D[1]', jnt_ik_mid_lower_sum)
        cmds.connectAttr(self.scale_soft_slide_mdn + '.outputX', soft_ik_subtract_scale + '.input1D[0]')

        # multiply by the 10
        soft_ik_multiply_dist = cmds.shadingNode('multiplyDivide', asUtility=1,
                                                 n='%s%s%s_mdn' % (prefix, 'SoftIkMulDist', side))
        cmds.setAttr(soft_ik_multiply_dist + '.operation', 1)
        cmds.setAttr(soft_ik_multiply_dist + '.input2X', 10)
        cmds.connectAttr(soft_ik_subtract_scale + '.output1D', soft_ik_multiply_dist + '.input1X')

        # clamp for maximum value of soft ik
        soft_ik_clamp = cmds.shadingNode('clamp', asUtility=1, n='%s%s%s_clm' % (prefix, 'SoftIkDist', side))
        cmds.connectAttr(soft_ik_multiply_dist + '.outputX', soft_ik_clamp + '.inputR')
        cmds.setAttr(soft_ik_clamp + '.minR', 1)
        cmds.setAttr(soft_ik_clamp + '.maxR', 1000)

        # multiply distance scale
        soft_ik_dist_multiply_scale = cmds.shadingNode('multiplyDivide', asUtility=1,
                                                       n='%s%s%s_mdn' % (prefix, 'SoftIkMulScale', side))
        cmds.setAttr(soft_ik_dist_multiply_scale + '.operation', 1)
        cmds.connectAttr(self.scale_soft_slide_mdn + '.outputX', soft_ik_dist_multiply_scale + '.input1X')
        cmds.connectAttr(soft_ik_clamp + '.outputR', soft_ik_dist_multiply_scale + '.input2X')

        ### END OF REVISE
        # multiplier subtract sum joint with distance
        soft_ik_distance_divide = cmds.shadingNode('multiplyDivide', asUtility=1,
                                                   n='%s%s%s_mdn' % (prefix, 'SoftIkMulSubtDist', side))
        cmds.setAttr(soft_ik_distance_divide + '.operation', 1)
        cmds.setAttr(soft_ik_distance_divide + '.input1X', subtract_ik_jnt_dist)
        cmds.connectAttr(self.controller_lower_limb_ik.control + '.softIk', soft_ik_distance_divide + '.input2X')

        # create condition node
        soft_ik_condition = cmds.shadingNode('condition', asUtility=1, n='%s%s%s_cnd' % (prefix, 'SoftIk', side))
        cmds.setAttr(soft_ik_condition + '.operation', 2)

        # connect the distance limb to soft ik condition node
        cmds.connectAttr(self.scale_soft_slide_mdn + '.outputX', soft_ik_condition + '.firstTerm')
        cmds.connectAttr(self.scale_soft_slide_mdn + '.outputX', soft_ik_condition + '.colorIfFalseR')

        # create pma for soft ik subtract between total length to soft ik
        soft_ik_subtract_pma = cmds.shadingNode('plusMinusAverage', asUtility=1,
                                                n='%s%s%s_pma' % (prefix, 'SoftIkSubtLength', side))
        cmds.setAttr(soft_ik_subtract_pma + '.operation', 2)
        cmds.setAttr(soft_ik_subtract_pma + '.input1D[0]', jnt_ik_mid_lower_sum)
        cmds.connectAttr(soft_ik_distance_divide + '.outputX', soft_ik_subtract_pma + '.input1D[1]')
        cmds.connectAttr(soft_ik_subtract_pma + '.output1D', soft_ik_condition + '.secondTerm')

        # create pma for soft ik subtract between distance to soft ik
        soft_ik_distance_pma = cmds.shadingNode('plusMinusAverage', asUtility=1,
                                                n='%s%s%s_pma' % (prefix, 'SoftIkSubtDist', side))
        cmds.setAttr(soft_ik_distance_pma + '.operation', 2)
        cmds.connectAttr(soft_ik_subtract_pma + '.output1D', soft_ik_distance_pma + '.input1D[1]')
        cmds.connectAttr(soft_ik_dist_multiply_scale + '.outputX', soft_ik_distance_pma + '.input1D[0]')

        # create add double liniear for avoiding infitity number
        soft_ik_add_adl = cmds.shadingNode('addDoubleLinear', asUtility=1,
                                           n='%s%s%s_adl' % (prefix, 'SoftIkOffset', side))
        cmds.connectAttr(self.controller_lower_limb_ik.control + '.softIk', soft_ik_add_adl + '.input1')
        cmds.setAttr(soft_ik_add_adl + '.input2', 0.001)

        # create mdn total distance to soft ik value
        soft_ik_distance_div = cmds.shadingNode('multiplyDivide', asUtility=1,
                                                n='%s%s%s_mdn' % (prefix, 'SoftIkDivDist', side))
        cmds.setAttr(soft_ik_distance_div + '.operation', 2)
        cmds.connectAttr(soft_ik_distance_pma + '.output1D', soft_ik_distance_div + '.input1X')
        cmds.connectAttr(soft_ik_add_adl + '.output', soft_ik_distance_div + '.input2X')

        # create mdn for softIkDivDist multiply by -1
        soft_ik_multiply_reverse = cmds.shadingNode('multiplyDivide', asUtility=1,
                                                    n='%s%s%s_mdn' % (prefix, 'SoftIkRev', side))
        cmds.setAttr(soft_ik_multiply_reverse + '.operation', 1)
        cmds.connectAttr(soft_ik_distance_div + '.outputX', soft_ik_multiply_reverse + '.input1X')
        cmds.setAttr(soft_ik_multiply_reverse + '.input2X', -1)

        # create mdn for softIkMulRev power with exponent
        soft_ik_exponent = cmds.shadingNode('multiplyDivide', asUtility=1, n='%s%s%s_mdn' % (prefix, 'SoftIkExp', side))
        cmds.setAttr(soft_ik_exponent + '.operation', 3)
        cmds.setAttr(soft_ik_exponent + '.input1X', 2.718282)
        cmds.connectAttr(soft_ik_multiply_reverse + '.outputX', soft_ik_exponent + '.input2X')

        # create mdn for softIK multiply by exponent
        soft_ik_multiply_exponent = cmds.shadingNode('multiplyDivide', asUtility=1,
                                                     n='%s%s%s_mdn' % (prefix, 'SoftIkMulExp', side))
        cmds.setAttr(soft_ik_multiply_exponent + '.operation', 1)
        cmds.connectAttr(soft_ik_exponent + '.outputX', soft_ik_multiply_exponent + '.input1X')
        cmds.connectAttr(soft_ik_distance_divide + '.outputX', soft_ik_multiply_exponent + '.input2X')

        # create pma for multiply exponent subtracted by total length soft ik
        soft_ik_pma_exponent = cmds.shadingNode('plusMinusAverage', asUtility=1,
                                                n='%s%s%s_pma' % (prefix, 'SoftIkSubtExp', side))
        cmds.setAttr(soft_ik_pma_exponent + '.operation', 2)
        cmds.setAttr(soft_ik_pma_exponent + '.input1D[0]', jnt_ik_mid_lower_sum)
        cmds.connectAttr(soft_ik_multiply_exponent + '.outputX', soft_ik_pma_exponent + '.input1D[1]')

        # create condition calcluation with exponent node
        soft_ik_condition_exponent = cmds.shadingNode('condition', asUtility=1,
                                                      n='%s%s%s_cnd' % (prefix, 'SoftIkExp', side))
        cmds.setAttr(soft_ik_condition_exponent + '.operation', 2)
        # connect the controler wrist to soft ik exp condition node
        cmds.connectAttr(self.controller_lower_limb_ik.control + '.softIk', soft_ik_condition_exponent + '.firstTerm')
        cmds.connectAttr(soft_ik_pma_exponent + '.output1D', soft_ik_condition_exponent + '.colorIfTrueR')
        cmds.setAttr(soft_ik_condition_exponent + '.colorIfFalseR', jnt_ik_mid_lower_sum)

        # connect to the condition soft ik
        cmds.connectAttr(soft_ik_condition_exponent + '.outColorR', soft_ik_condition + '.colorIfTrueR')

        # connect to position wrist distance
        cmds.connectAttr(soft_ik_condition + '.outColorR', self.pos_lower_limb_jnt + '.translateY')

        ## STRETCH IK SETUP
        # parent constraint the limb distance from controller gimbal
        cmds.delete(cmds.parentConstraint(self.controller_lower_limb_ik.control_gimbal, self.position_limb_jnt))
        cmds.parent(self.position_limb_jnt, self.controller_lower_limb_ik.control_gimbal)

        # create node for multiplying with the distance limb (upper limb and middle limb)
        # multiplier reverse stretch
        stretch_ik_multiplier = cmds.shadingNode('multiplyDivide', asUtility=1,
                                                 n='%s%s%s_mdn' % (prefix, 'StretchIkMulRev', side))
        cmds.setAttr(stretch_ik_multiplier + '.operation', 1)

        # connect distance to multiplier
        cmds.connectAttr(self.controller_lower_limb_ik.control + '.stretch', stretch_ik_multiplier + '.input1X')

        if get_value_tx_upper_limb_jnt > 0:
            cmds.setAttr(stretch_ik_multiplier + ".input2X", 1)
        else:
            cmds.setAttr(stretch_ik_multiplier + ".input2X", -1)

        stretch_ik_upper_sum = self.limb_stretch_ik(obj_poleVector='StretchIkUr', prefix=prefix, side=side,
                                                    div_value=div_mid_value,
                                                    stretch_ik_multiplier=stretch_ik_multiplier,
                                                    get_value_tx_upper_limb_jnt=get_value_tx_upper_limb_jnt,
                                                    length_limb=length_upper_limb)

        stretch_ik_mid_sum = self.limb_stretch_ik(obj_poleVector='StretchIkMd', prefix=prefix, side=side,
                                                  div_value=div_lower_value,
                                                  stretch_ik_multiplier=stretch_ik_multiplier,
                                                  get_value_tx_upper_limb_jnt=get_value_tx_upper_limb_jnt,
                                                  length_limb=length_middle_limb)

        ## SLIDE MIDDLE LIMB IK SETUP
        # setRange for slide middle limb
        slide_ik_set_range = cmds.shadingNode('setRange', asUtility=1, n='%s%s%s_str' % (prefix, 'SlideIkMd', side))
        cmds.connectAttr(self.controller_lower_limb_ik.control + '.%s' % self.slide_attr,
                         slide_ik_set_range + '.valueX')
        cmds.setAttr(slide_ik_set_range + '.minX', -1)
        cmds.setAttr(slide_ik_set_range + '.maxX', 1)
        cmds.setAttr(slide_ik_set_range + '.oldMinX', -10)
        cmds.setAttr(slide_ik_set_range + '.oldMaxX', 10)

        # clamp for maximum value of slide
        slide_ik_clamp = cmds.shadingNode('clamp', asUtility=1, n='%s%s%s_clm' % (prefix, 'SlideIkDist', side))
        cmds.connectAttr(self.scale_soft_slide_mdn + '.outputX', slide_ik_clamp + '.minR')
        cmds.setAttr(slide_ik_clamp + '.maxR', distance_main_ik_value)
        self.slide_ik_clamp = slide_ik_clamp

        # condition if stretch on when slide on max
        slide_ik_max_con = cmds.shadingNode('condition', asUtility=1,
                                            n='%s%s%s_cnd' % (prefix, 'SlideIkStretchOn', side))
        cmds.setAttr(slide_ik_max_con + '.operation', 2)
        cmds.connectAttr(self.controller_lower_limb_ik.control + '.stretch', slide_ik_max_con + '.firstTerm')
        cmds.connectAttr(self.scale_soft_slide_mdn + '.outputX', slide_ik_max_con + '.colorIfTrueR')
        cmds.connectAttr(slide_ik_clamp + '.outputR', slide_ik_max_con + '.colorIfFalseR')

        # create pma for result condition subtract to total value joint - distance
        slide_ik_pma_difference_jnt = cmds.shadingNode('plusMinusAverage', asUtility=1,
                                                       n='%s%s%s_pma' % (prefix, 'SlideIkSubtrJntDist', side))
        cmds.setAttr(slide_ik_pma_difference_jnt + '.operation', 2)
        cmds.connectAttr(slide_ik_max_con + '.outColorR', slide_ik_pma_difference_jnt + '.input1D[0]')
        cmds.setAttr(slide_ik_pma_difference_jnt + '.input1D[1]', subtract_ik_jnt_dist)

        slide_ik_mid_multiply_set_range = self.limb_slide_setRange_ik(prefix=prefix, side=side,
                                                                      obj_poleVector='SlideIkMd',
                                                                      slide_ik_pma_difference_jnt=slide_ik_pma_difference_jnt,
                                                                      div_value=div_mid_value,
                                                                      slide_ik_setRange=slide_ik_set_range)

        slide_ik_lower_multiply_set_range = self.limb_slide_setRange_ik(prefix=prefix, side=side,
                                                                        obj_poleVector='SlideIkLr',
                                                                        slide_ik_pma_difference_jnt=slide_ik_pma_difference_jnt,
                                                                        div_value=div_lower_value,
                                                                        slide_ik_setRange=slide_ik_set_range)

        # create condition for both middle limb and wrist sliding
        slide_ik_mid_lower_condition = cmds.shadingNode('condition', asUtility=1,
                                                        n='%s%s%s_cnd' % (prefix, 'SlideIk', side))
        cmds.setAttr(slide_ik_mid_lower_condition + '.operation', 4)
        cmds.connectAttr(slide_ik_set_range + '.outValueX', slide_ik_mid_lower_condition + '.firstTerm')
        cmds.connectAttr(slide_ik_mid_multiply_set_range + '.outputX', slide_ik_mid_lower_condition + '.colorIfTrueR')
        cmds.connectAttr(slide_ik_lower_multiply_set_range + '.outputX',
                         slide_ik_mid_lower_condition + '.colorIfFalseR')

        slide_ik_mid_pma_stretch = self.limb_slide_pma_stretch_ik(obj_poleVector='SlideIkMd', prefix=prefix, side=side,
                                                                  get_value_tx_upper_limb_jnt=get_value_tx_upper_limb_jnt,
                                                                  operation_one=1, operation_two=2,
                                                                  stretch_ik_sum=stretch_ik_upper_sum,
                                                                  slide_ik_md_lower_condition=slide_ik_mid_lower_condition)

        slide_ik_lower_pma_stretch = self.limb_slide_pma_stretch_ik(obj_poleVector='SlideIkLr', prefix=prefix,
                                                                    side=side,
                                                                    get_value_tx_upper_limb_jnt=get_value_tx_upper_limb_jnt,
                                                                    operation_one=2, operation_two=1,
                                                                    stretch_ik_sum=stretch_ik_mid_sum,
                                                                    slide_ik_md_lower_condition=slide_ik_mid_lower_condition)

        ## SLIDE MIDDLE LIMB COMBINE TO STRETCH ON/OFF
        # create pma for sum to total value joint - distance
        slide_ik_pma_sum_difference_jnt = cmds.shadingNode('plusMinusAverage', asUtility=1,
                                                           n='%s%s%s_pma' % (prefix, 'SlideIkSumJntDist', side))
        cmds.setAttr(slide_ik_pma_sum_difference_jnt + '.operation', 1)
        cmds.connectAttr(self.scale_soft_slide_mdn + '.outputX', slide_ik_pma_sum_difference_jnt + '.input1D[0]')
        cmds.setAttr(slide_ik_pma_sum_difference_jnt + '.input1D[1]', subtract_ik_jnt_dist)

        # middle limb
        self.limb_slide_combine_ik(obj_poleVector='SlideIkMd', prefix=prefix, side=side,
                                   slide_ik_pma_sum_difference_jnt=slide_ik_pma_sum_difference_jnt,
                                   div_value=div_mid_value, distance_main_ik_value=distance_main_ik_value,
                                   length_limb=length_upper_limb,
                                   slide_ik_setRange=slide_ik_set_range, stretch_ik_sum=stretch_ik_upper_sum)
        # lower limb
        self.limb_slide_combine_ik(obj_poleVector='SlideIkLr', prefix=prefix, side=side,
                                   slide_ik_pma_sum_difference_jnt=slide_ik_pma_sum_difference_jnt,
                                   div_value=div_lower_value, distance_main_ik_value=distance_main_ik_value,
                                   length_limb=length_middle_limb,
                                   slide_ik_setRange=slide_ik_set_range, stretch_ik_sum=stretch_ik_mid_sum)

        ## SNAP IK SETUP
        # parent constraint pole vector distance position
        cmds.delete(cmds.parentConstraint(self.controller_pole_vector_ik.control, self.pos_pole_vector_jnt))
        cmds.parent(self.pos_pole_vector_jnt, self.controller_pole_vector_ik.control)

        # snap upper limb
        self.limb_poleVector_snap_ik(obj_poleVector='Md', get_value_tx_upper_limb_jnt=get_value_tx_upper_limb_jnt,
                                     prefix=prefix, side=side,
                                     slide_ik_pma_stretch=slide_ik_mid_pma_stretch, limb_ik_jnt=middle_limb_ik_jnt,
                                     scale_poleVector_snap_mdn=self.scale_poleVector_snap_middle_mdn)

        # snap middle limb
        self.limb_poleVector_snap_ik(obj_poleVector='Lr', get_value_tx_upper_limb_jnt=get_value_tx_upper_limb_jnt,
                                     prefix=prefix, side=side,
                                     slide_ik_pma_stretch=slide_ik_lower_pma_stretch,
                                     limb_ik_jnt=lower_limb_ik_jnt,
                                     scale_poleVector_snap_mdn=self.scale_poleVector_snap_lower_mdn)

        # ADD TWIST ATTRIBUTE
        cmds.connectAttr('%s.twist' % self.controller_lower_limb_ik.control, '%s.twist' % self.lower_limb_ik_hdl[0])

        ## CREATE CURVE FOR POLE VECTOR CONTROLLER
        self.curve_poleVector_ik = cmds.curve(d=1, p=[(0, 0, 0), (0, 0, 0)], k=[0, 1],
                                              n=('%s%s_crv' % (prefix_pole_vector_ik, side)))
        self.clusterBase, self.clusterBaseHdl = cmds.cluster('%s.cv[0]' % self.curve_poleVector_ik,
                                                             n='%s01%s_cls' % (prefix_pole_vector_ik, side),
                                                             wn=(middle_limb_ik_jnt, middle_limb_ik_jnt))
        self.clusterPoleVector, self.clusterPoleVectorHdl = cmds.cluster('%s.cv[1]' % self.curve_poleVector_ik,
                                                                         n='%s02%s_cls' % (prefix_pole_vector_ik, side),
                                                                         wn=(self.controller_pole_vector_ik.control,
                                                                             self.controller_pole_vector_ik.control))

        # LOCK CURVE
        cmds.setAttr('%s.template' % self.curve_poleVector_ik, 1)
        cmds.setAttr('%s.template' % self.curve_poleVector_ik, lock=1)

        # ==================================================================================================================
        #                                                   BLEND FOLLOW LIMB
        # ==================================================================================================================
        if arm:
            # FK
            self.shoulder_fk = self.limb_follow_fk(prefix_upper_limb_fk=prefix_upper_limb_fk,
                                                   upper_limb_fk_jnt=upper_limb_fk_jnt,
                                                   locator_name='Shoulder', prefix=prefix, side=side, second_term=0)

            shoulder_fk_point_constraint = cmds.pointConstraint(self.shoulder_fk,
                                                                self.controller_upper_limb_fk.parent_control[0],
                                                                mo=1)

            # hip
            self.hip_fk = self.limb_follow_fk(prefix_upper_limb_fk=prefix_upper_limb_fk,
                                              upper_limb_fk_jnt=upper_limb_fk_jnt,
                                              locator_name='Hip', prefix=prefix, side=side, second_term=1)
            # World
            self.world_fk = self.limb_follow_fk(prefix_upper_limb_fk=prefix_upper_limb_fk,
                                                upper_limb_fk_jnt=upper_limb_fk_jnt,
                                                locator_name='World', prefix=prefix, side=side, second_term=2)

            # IK
            # shoulder
            self.shoulder_ik = self.limb_follow_ik(prefix_upper_limb_ik=prefix_upper_limb_ik,
                                                   lower_limb_ik_jnt=lower_limb_ik_jnt,
                                                   locator_name='Shoulder', prefix=prefix, side=side, second_term=0)
            # hip
            self.hip_ik = self.limb_follow_ik(prefix_upper_limb_ik=prefix_upper_limb_ik,
                                              lower_limb_ik_jnt=lower_limb_ik_jnt,
                                              locator_name='Hip', prefix=prefix, side=side, second_term=1)
            # World
            self.world_ik = self.limb_follow_ik(prefix_upper_limb_ik=prefix_upper_limb_ik,
                                                lower_limb_ik_jnt=lower_limb_ik_jnt,
                                                locator_name='World', prefix=prefix, side=side, second_term=2)
            # rename constraint
            rt_utils.constraint_rename(shoulder_fk_point_constraint)
        else:
            # FK
            # hip
            self.hip_fk = self.limb_follow_fk(prefix_upper_limb_fk=prefix_upper_limb_fk,
                                              upper_limb_fk_jnt=upper_limb_fk_jnt,
                                              locator_name='Hip', prefix=prefix, side=side, second_term=0)
            # World
            self.world_fk = self.limb_follow_fk(prefix_upper_limb_fk=prefix_upper_limb_fk,
                                                upper_limb_fk_jnt=upper_limb_fk_jnt,
                                                locator_name='World', prefix=prefix, side=side, second_term=1)

            hip_fk_point_constraint = cmds.pointConstraint(self.hip_fk, self.controller_upper_limb_fk.parent_control[0],
                                                           mo=1)

            # IK
            # hip
            self.hip_ik = self.limb_follow_ik(prefix_upper_limb_ik=prefix_upper_limb_ik,
                                              lower_limb_ik_jnt=lower_limb_ik_jnt,
                                              locator_name='Hip', prefix=prefix, side=side, second_term=0)
            # World
            self.world_ik = self.limb_follow_ik(prefix_upper_limb_ik=prefix_upper_limb_ik,
                                                lower_limb_ik_jnt=lower_limb_ik_jnt,
                                                locator_name='World', prefix=prefix, side=side, second_term=1)
            # rename constraint
            rt_utils.constraint_rename(hip_fk_point_constraint)
        # ==================================================================================================================
        #                                                 FK/IK CTRL SETUP
        # ==================================================================================================================
        ### CREATE CONTROL FK/IK SETUP
        self.controller_FkIk_limb_setup = rlu_controller.Control(match_obj_first_position=lower_limb_fk_jnt,
                                                                 prefix='%s' % (prefix_limb_setup), side=side,
                                                                 shape=rlu_controller.STICKCIRCLE,
                                                                 groups_ctrl=['Zro'], ctrl_size=scale,
                                                                 ctrl_color='navy', lock_channels=['v', 't', 'r', 's'])

        ### FK/IK SETUP VISIBILITY ATTRIBUTE CONTROLLER
        rt_utils.add_attr_transform(self.controller_FkIk_limb_setup.control, 'FkIk', 'long', keyable=True, min=0, max=1,
                                    dv=0)
        # create reverse node for FK on/off
        self.limb_setup_reverse = cmds.createNode('reverse', n=('%s%s%s_rev' % (prefix, 'FkIk', side)))

        # set on/off attribute FK
        rt_utils.connect_part_object(obj_base_connection='FkIk', target_connection='inputX',
                                     obj_name=self.controller_FkIk_limb_setup.control,
                                     target_name=[self.limb_setup_reverse], select_obj=False)

        rt_utils.connect_part_object(obj_base_connection='outputX', target_connection='visibility',
                                     obj_name=self.limb_setup_reverse,
                                     target_name=[self.controller_upper_limb_fk.parent_control[0]], select_obj=False)

        # set on/off attribute IK
        rt_utils.connect_part_object(obj_base_connection='FkIk', target_connection='visibility',
                                     obj_name=self.controller_FkIk_limb_setup.control,
                                     target_name=[self.controller_upper_limb_ik.parent_control[0],
                                                  self.controller_pole_vector_ik.parent_control[0],
                                                  self.controller_lower_limb_ik.parent_control[0],
                                                  self.curve_poleVector_ik],
                                     select_obj=False)

        # node setup switch on/off
        # upper limb
        self.limb_switch_FkIk(limb_fk_jnt=upper_limb_fk_jnt, limb_ik_jnt=upper_limb_ik_jnt, limb_jnt=upper_limb_jnt)

        # middle limb
        self.limb_switch_FkIk(limb_fk_jnt=middle_limb_fk_jnt, limb_ik_jnt=middle_limb_ik_jnt, limb_jnt=middle_limb_jnt)

        # lower limb
        self.limb_switch_FkIk(limb_fk_jnt=lower_limb_fk_jnt, limb_ik_jnt=lower_limb_ik_jnt, limb_jnt=lower_limb_jnt)

        # EXTRA ATTRIBUTES
        rt_utils.add_attribute(objects=[self.controller_FkIk_limb_setup.control],
                               long_name=['%s%s' % (prefix, 'MultTwist')],
                               at="float", min=0, max=1, dv=0, channel_box=True)
        if not arm:
            # set foot to ik
            cmds.setAttr(self.controller_FkIk_limb_setup.control + '.FkIk', 1)

            rt_utils.add_attribute(objects=[self.controller_FkIk_limb_setup.control], long_name=['footScale'],
                                   nice_name=[' '], at="enum", en='Foot Scale', channel_box=True)

            #### SCALE FOOT
            rt_utils.add_attribute(objects=[self.controller_FkIk_limb_setup.control], long_name=['footScaleX'],
                                   attributeType="float", dv=1, keyable=True)
            rt_utils.add_attribute(objects=[self.controller_FkIk_limb_setup.control], long_name=['footScaleY'],
                                   attributeType="float", dv=1, keyable=True)
            rt_utils.add_attribute(objects=[self.controller_FkIk_limb_setup.control], long_name=['footScaleZ'],
                                   attributeType="float", dv=1, keyable=True)

        rt_utils.add_attribute(objects=[self.controller_FkIk_limb_setup.control], long_name=[prefix + 'Scale'],
                               nice_name=[' '], at="enum", en=prefix.capitalize() + ' ' + 'Scale', channel_box=True)

        rt_utils.add_attribute(objects=[self.controller_FkIk_limb_setup.control], long_name=[prefix + 'ScaleX'],
                               attributeType="float", dv=1, keyable=True)
        rt_utils.add_attribute(objects=[self.controller_FkIk_limb_setup.control], long_name=[prefix + 'ScaleY'],
                               attributeType="float", dv=1, keyable=True)
        rt_utils.add_attribute(objects=[self.controller_FkIk_limb_setup.control], long_name=[prefix + 'ScaleZ'],
                               attributeType="float", dv=1, keyable=True)

        # ==================================================================================================================
        #                                           ADD ROTATION ORDER FK/IK CTRL
        # ==================================================================================================================
        #### FK
        # Fk controller
        cmds.setAttr(self.controller_upper_limb_fk.control + '.rotateOrder', k=True)
        cmds.setAttr(self.controller_middle_limb_fk.control + '.rotateOrder', k=True)
        cmds.setAttr(self.controller_lower_limb_fk.control + '.rotateOrder', k=True)

        # self.limb_rotation_order(self.controller_upper_limb_fk.control)
        # self.limb_rotation_order(self.controller_middle_limb_fk.control)
        # self.limb_rotation_order(self.controller_lower_limb_fk.control)

        ## Fk gimbal
        cmds.setAttr(self.controller_upper_limb_fk.control_gimbal + '.rotateOrder', k=True)
        cmds.setAttr(self.controller_middle_limb_fk.control_gimbal + '.rotateOrder', k=True)
        cmds.setAttr(self.controller_lower_limb_fk.control_gimbal + '.rotateOrder', k=True)

        # self.limb_rotation_order(self.controller_upper_limb_fk.control_gimbal)
        # self.limb_rotation_order(self.controller_middle_limb_fk.control_gimbal)
        # self.limb_rotation_order(self.controller_lower_limb_fk.control_gimbal)

        #### IK
        # Ik controller
        cmds.setAttr(self.controller_lower_limb_ik.control + '.rotateOrder', k=True)

        # self.limb_rotation_order(self.controller_lower_limb_ik.control)

        # Ik gimbal
        cmds.setAttr(self.controller_lower_limb_ik.control_gimbal + '.rotateOrder', k=True)

        # self.limb_rotation_order(self.controller_lower_limb_ik.control_gimbal)

        # ==================================================================================================================
        #                                                   DETAIL CONTROLLER
        # ==================================================================================================================
        ## MID COMBINE DETAIL
        # create controller
        self.ctrl_mid_middle_limb = rlu_controller.Control(match_obj_first_position=middle_limb_jnt,
                                                           prefix=prefix + 'DtlCombine',
                                                           side=side, groups_ctrl=['Zro'],
                                                           ctrl_size=scale * 0.75, ctrl_color='red',
                                                           shape=rlu_controller.LOCATOR)

        # add attribute
        rt_utils.add_attribute(objects=[self.ctrl_mid_middle_limb.control], long_name=['twistSep'],
                               nice_name=[' '], at="enum", en='Twist', channel_box=True)
        rt_utils.add_attribute(objects=[self.ctrl_mid_middle_limb.control], long_name=['roll'],
                               at="float", keyable=True)
        # ROLL
        self.adl_upper_limb_combine = cmds.createNode('addDoubleLinear',
                                                      n=(prefix_upper_limb_dtl + 'RollCombine' + side + '_adl'))
        cmds.connectAttr(self.ctrl_mid_middle_limb.control + '.roll', self.adl_upper_limb_combine + '.input2')

        self.adl_middle_limb_combine = cmds.createNode('addDoubleLinear',
                                                       n=(prefix_middle_limb_dtl + 'RollCombine' + side + '_adl'))
        cmds.connectAttr(self.ctrl_mid_middle_limb.control + '.roll', self.adl_middle_limb_combine + '.input2')

        if detail_limb_deformer:
            # Add attributes: Volume attributes
            rt_utils.add_attribute(objects=[self.ctrl_mid_middle_limb.control], long_name=['volumeSep'],
                                   nice_name=[' '], at="enum", en='Volume', channel_box=True)
            rt_utils.add_attribute(objects=[self.ctrl_mid_middle_limb.control], long_name=['volume'],
                                   at="float", min=-1, max=1, keyable=True)
            rt_utils.add_attribute(objects=[self.ctrl_mid_middle_limb.control], long_name=['volumeMultiplier'],
                                   at="float", min=1, dv=1, keyable=True)
            rt_utils.add_attribute(objects=[self.ctrl_mid_middle_limb.control], long_name=['volumePosition'],
                                   dv=0, min=number_joints * -0.5, max=number_joints * 0.5, at="float", keyable=True)

            # Add attributes: Sine attributes
            rt_utils.add_attribute(objects=[self.ctrl_mid_middle_limb.control], long_name=['sineSep'], nice_name=[' '],
                                   attributeType='enum', en="Sine:", channel_box=True)
            rt_utils.add_attribute(objects=[self.ctrl_mid_middle_limb.control], long_name=['amplitude'],
                                   attributeType="float", keyable=True)
            rt_utils.add_attribute(objects=[self.ctrl_mid_middle_limb.control], long_name=['wide'],
                                   attributeType="float", keyable=True)
            rt_utils.add_attribute(objects=[self.ctrl_mid_middle_limb.control], long_name=['sineRotate'],
                                   attributeType="float", keyable=True)
            rt_utils.add_attribute(objects=[self.ctrl_mid_middle_limb.control], long_name=['offset'],
                                   attributeType="float", keyable=True)
            rt_utils.add_attribute(objects=[self.ctrl_mid_middle_limb.control], long_name=['twist'],
                                   attributeType="float", keyable=True)
            rt_utils.add_attribute(objects=[self.ctrl_mid_middle_limb.control], long_name=['sineLength'],
                                   min=0.1, dv=1, attributeType="float", keyable=True)

            ## VOLUME POSITION
            ## upper limb
            self.volume_pos_mdl_upper_limb = self.limb_volume_position(prefix_limb_dtl=prefix_upper_limb_dtl, side=side,
                                                                       operation=2, num_joint=number_joints,
                                                                       dv_min=0, dv_max=0.5, v_min=1, v_max=0)

            ## middle limb
            self.volume_pos_mdl_middle_limb = self.limb_volume_position(prefix_limb_dtl=prefix_middle_limb_dtl,
                                                                        side=side, operation=4, num_joint=number_joints,
                                                                        dv_min=-0.5, dv_max=0, v_min=0, v_max=1)

        # Extra attributes
        rt_utils.add_attribute(objects=[self.ctrl_mid_middle_limb.control], long_name=['extraSep'], nice_name=[' '],
                               at="enum",
                               en='Extra',
                               channel_box=True)
        rt_utils.add_attribute(objects=[self.ctrl_mid_middle_limb.control], long_name=['detailBaseCtrlVis'], at="long",
                               min=0,
                               max=1, dv=0,
                               channel_box=True)

        # lock and hide attribute
        rt_utils.lock_hide_attr(['r', 's', 'v'], self.ctrl_mid_middle_limb.control)

        # adjusting the controller direction
        if get_value_tx_upper_limb_jnt > 0:
            rlu_rotationController.change_position(self.controller_FkIk_limb_setup.control, 'xz')
            rlu_rotationController.change_position(self.controller_FkIk_limb_setup.control, '-')
        else:
            rlu_rotationController.change_position(self.controller_FkIk_limb_setup.control, 'xz')

    # ==================================================================================================================
    #                                                   CLASS FUNCTION
    # ==================================================================================================================
    # def limb_rotation_order(self, controller_target):
    #     au.add_attribute(objects=[controller_target], long_name=['rotationOrder'],
    #                      at="enum", en='xyz:yzx:zxy:xzy:yxz:zyx:', keyable=True)
    #
    #     mc.connectAttr(controller_target + '.rotationOrder', controller_target + '.rotateOrder')

    def limb_follow_fk(self, prefix_upper_limb_fk, upper_limb_fk_jnt, locator_name, prefix, side, second_term):
        # create locator
        locator = cmds.spaceLocator(n='%s%s_loc' % (prefix_upper_limb_fk + locator_name, side))
        cmds.hide(locator)

        # match locator position to upper limb
        cmds.delete(cmds.parentConstraint(upper_limb_fk_jnt, locator))

        self.blend_limb_fk_rotation = cmds.orientConstraint(locator, self.controller_upper_limb_fk.parent_control[0])

        # create condition
        part_limb_fol_fk_cnd = cmds.shadingNode('condition', asUtility=1,
                                                n='%s%s%s_cnd' % (prefix, locator_name + 'FkFollow',
                                                                  side))
        cmds.setAttr(part_limb_fol_fk_cnd + '.secondTerm', second_term)
        cmds.setAttr(part_limb_fol_fk_cnd + '.colorIfTrueR', 1)
        cmds.setAttr(part_limb_fol_fk_cnd + '.colorIfFalseR', 0)
        cmds.connectAttr(self.controller_upper_limb_fk.control + '.follow', part_limb_fol_fk_cnd + '.firstTerm')

        # connect to orient constraint
        cmds.connectAttr(part_limb_fol_fk_cnd + '.outColorR',
                         ('%s.%sW%s' % (self.blend_limb_fk_rotation[0], locator[0], second_term)))

        # constraint rename
        rt_utils.constraint_rename(self.blend_limb_fk_rotation)
        return locator

    def limb_follow_ik(self, prefix_upper_limb_ik, lower_limb_ik_jnt, locator_name, prefix, side, second_term):
        # create locator
        locator = cmds.spaceLocator(n='%s%s_loc' % (prefix_upper_limb_ik + locator_name, side))
        cmds.hide(locator)

        # match locator position to upper limb
        cmds.delete(cmds.parentConstraint(lower_limb_ik_jnt, locator))

        self.blend_limb_ik_parent = cmds.parentConstraint(locator,
                                                          self.controller_lower_limb_ik.parent_control[0])

        # create condition
        part_limb_fol_ik_condition = cmds.shadingNode('condition', asUtility=1,
                                                      n='%s%s%s_cnd' % (prefix, locator_name + 'IkFollow', side))
        cmds.setAttr(part_limb_fol_ik_condition + '.secondTerm', second_term)
        cmds.setAttr(part_limb_fol_ik_condition + '.colorIfTrueR', 1)
        cmds.setAttr(part_limb_fol_ik_condition + '.colorIfFalseR', 0)
        cmds.connectAttr(self.controller_lower_limb_ik.control + '.follow', part_limb_fol_ik_condition + '.firstTerm')

        cmds.connectAttr(part_limb_fol_ik_condition + '.outColorR',
                         ('%s.%sW%s' % (self.blend_limb_ik_parent[0], locator[0], second_term)))

        # constraint rename
        rt_utils.constraint_rename(self.blend_limb_ik_parent)
        return locator

    def limb_switch_FkIk(self, limb_fk_jnt, limb_ik_jnt, limb_jnt):

        limb_blend_constraint = cmds.parentConstraint(limb_fk_jnt, limb_ik_jnt, limb_jnt)

        # set on/off attribute Fk/Ik upper limb
        rt_utils.connect_part_object(obj_base_connection='outputX', target_connection='%sW0' % limb_fk_jnt,
                                     obj_name=self.limb_setup_reverse,
                                     target_name=limb_blend_constraint, select_obj=False)
        rt_utils.connect_part_object(obj_base_connection='FkIk', target_connection='%sW1' % limb_ik_jnt,
                                     obj_name=self.controller_FkIk_limb_setup.control,
                                     target_name=limb_blend_constraint, select_obj=False)

        # constraint rename
        rt_utils.constraint_rename(limb_blend_constraint)

    def limb_stretch_fk(self, limb_fk_controller, prefix_limb_fk, side, down_limb_fk_jnt):

        limb_stretch_offset = cmds.createNode('multDoubleLinear',
                                              n='%s%s%s_mdl' % (prefix_limb_fk, 'StretchOffset', side))
        rt_utils.add_attribute(objects=[limb_stretch_offset], long_name=['offset'],
                               attributeType="float", dv=0.1, keyable=True)
        cmds.connectAttr(limb_stretch_offset + '.offset', limb_stretch_offset + '.input1')

        # stretch value
        limb_stretch = cmds.createNode('multDoubleLinear', n='%s%s%s_mdl' % (prefix_limb_fk, 'Stretch', side))
        down_limb_grp_ty = cmds.getAttr('%s.translateY' % down_limb_fk_jnt)

        rt_utils.add_attribute(objects=[limb_stretch], long_name=['offset'],
                               attributeType="float", dv=down_limb_grp_ty, keyable=True)
        cmds.connectAttr(limb_stretch + '.offset', limb_stretch + '.input1')

        # adding value
        limb_add_offset = cmds.createNode('addDoubleLinear',
                                          n='%s%s%s_adl' % (prefix_limb_fk, 'AddOffset', side))
        rt_utils.add_attribute(objects=[limb_add_offset], long_name=['offset'],
                               attributeType="float", dv=down_limb_grp_ty, keyable=True)

        cmds.connectAttr(limb_add_offset + '.offset', limb_add_offset + '.input1')

        # connecting each other
        cmds.connectAttr(limb_fk_controller + '.stretch', limb_stretch_offset + '.input2')
        cmds.connectAttr(limb_stretch_offset + '.output', limb_stretch + '.input2')
        cmds.connectAttr(limb_stretch + '.output', limb_add_offset + '.input2')

        return limb_add_offset

    def limb_stretch_ik(self, obj_poleVector, prefix, side, div_value, stretch_ik_multiplier,
                        get_value_tx_upper_limb_jnt, length_limb):
        # limb
        stretch_ik_mul_distance = cmds.shadingNode('multiplyDivide', asUtility=1,
                                                   n='%s%s%s%s_mdn' % (prefix, obj_poleVector, 'MulDist', side))
        cmds.setAttr(stretch_ik_mul_distance + '.operation', 1)
        cmds.connectAttr(self.scale_stretch_slide_mdn + '.outputX', stretch_ik_mul_distance + '.input1X')
        cmds.setAttr(stretch_ik_mul_distance + '.input2X', div_value)

        # multiply by the control stretch
        stretch_ik_mul_set = cmds.shadingNode('multiplyDivide', asUtility=1,
                                              n='%s%s%s%s_mdn' % (prefix, obj_poleVector, 'MulSet', side))
        cmds.setAttr(stretch_ik_mul_set + '.operation', 1)
        cmds.connectAttr(stretch_ik_multiplier + '.outputX', stretch_ik_mul_set + '.input1X')
        cmds.connectAttr(stretch_ik_mul_distance + '.outputX', stretch_ik_mul_set + '.input2X')

        # adding respectively by it's joint length
        stretch_ik_sum = cmds.shadingNode('plusMinusAverage', asUtility=1,
                                          n='%s%s%s%s_pma' % (prefix, obj_poleVector, 'Sum', side))
        if get_value_tx_upper_limb_jnt > 0:
            cmds.setAttr(stretch_ik_sum + '.operation', 1)
        else:
            cmds.setAttr(stretch_ik_sum + '.operation', 2)

        cmds.connectAttr(stretch_ik_mul_set + '.outputX', stretch_ik_sum + '.input1D[0]')
        cmds.setAttr(stretch_ik_sum + '.input1D[1]', length_limb)

        return stretch_ik_sum

    def limb_slide_setRange_ik(self, prefix, side, obj_poleVector, slide_ik_pma_difference_jnt, div_value,
                               slide_ik_setRange):
        # create mdn for multiplying result slideIkPmaDiffJnt to divide limb joint and total joints
        slide_ik_mul_set = cmds.shadingNode('multiplyDivide', asUtility=1,
                                            n='%s%s%s%s_mdn' % (prefix, obj_poleVector, 'MulSet', side))
        cmds.setAttr(slide_ik_mul_set + '.operation', 1)
        cmds.connectAttr(slide_ik_pma_difference_jnt + '.output1D', slide_ik_mul_set + '.input1X')
        cmds.setAttr(slide_ik_mul_set + '.input2X', div_value)

        # create mdn for multiplying result slideIkFaMulSet to output slideIkSetR
        slide_ik_mul_setRange = cmds.shadingNode('multiplyDivide', asUtility=1,
                                                 n='%s%s%s%s_mdn' % (prefix, obj_poleVector, 'MulSetR', side))
        cmds.setAttr(slide_ik_mul_setRange + '.operation', 1)
        cmds.connectAttr(slide_ik_mul_set + '.outputX', slide_ik_mul_setRange + '.input1X')
        cmds.connectAttr(slide_ik_setRange + '.outValueX', slide_ik_mul_setRange + '.input2X')

        return slide_ik_mul_setRange

    def limb_slide_pma_stretch_ik(self, obj_poleVector, prefix, side, get_value_tx_upper_limb_jnt, operation_one,
                                  operation_two, stretch_ik_sum, slide_ik_md_lower_condition):
        # create pma for result limb condition sum to slideIkMdLrCon
        slide_ik_pma_stretch = cmds.shadingNode('plusMinusAverage', asUtility=1,
                                                n='%s%s%s%s_pma' % (prefix, obj_poleVector, 'SumStretch', side))
        if get_value_tx_upper_limb_jnt > 0:
            cmds.setAttr(slide_ik_pma_stretch + '.operation', operation_one)
        else:
            cmds.setAttr(slide_ik_pma_stretch + '.operation', operation_two)

        cmds.connectAttr(stretch_ik_sum + '.output1D', slide_ik_pma_stretch + '.input1D[0]')
        cmds.connectAttr(slide_ik_md_lower_condition + '.outColorR', slide_ik_pma_stretch + '.input1D[1]')

        return slide_ik_pma_stretch

    def limb_slide_combine_ik(self, obj_poleVector, prefix, side, slide_ik_pma_sum_difference_jnt, div_value,
                              distance_main_ik_value,
                              length_limb, slide_ik_setRange, stretch_ik_sum):

        # create mdn to multiply result slideIkPmaSumDiffJnt to divide limb joint and total joints
        slide_ik_mul_sum_pma = cmds.shadingNode('multiplyDivide', asUtility=1,
                                                n='%s%s%s%s_mdn' % (prefix, obj_poleVector, 'MulSumPma', side))
        cmds.setAttr(slide_ik_mul_sum_pma + '.operation', 1)
        cmds.connectAttr(slide_ik_pma_sum_difference_jnt + '.output1D', slide_ik_mul_sum_pma + '.input1X')
        cmds.setAttr(slide_ik_mul_sum_pma + '.input2X', div_value)

        # create condition for limb to distance
        slide_ik_dist_condition = cmds.shadingNode('condition', asUtility=1,
                                                   n='%s%s%s%s_cnd' % (prefix, obj_poleVector, 'Dist', side))
        cmds.setAttr(slide_ik_dist_condition + '.operation', 4)
        cmds.connectAttr(self.scale_soft_slide_mdn + '.outputX', slide_ik_dist_condition + '.firstTerm')
        cmds.setAttr(slide_ik_dist_condition + '.secondTerm', distance_main_ik_value)
        cmds.connectAttr(slide_ik_mul_sum_pma + '.outputX', slide_ik_dist_condition + '.colorIfTrueR')
        cmds.setAttr(slide_ik_dist_condition + '.colorIfFalseR', length_limb)

        # create condition limb slide to stretch min
        slide_ik_stretch_condiiton = cmds.shadingNode('condition', asUtility=1,
                                                      n='%s%s%s%s_cnd' % (prefix, obj_poleVector, 'MdStretch', side))
        cmds.setAttr(slide_ik_stretch_condiiton + '.operation', 0)
        cmds.connectAttr(slide_ik_setRange + '.outValueX', slide_ik_stretch_condiiton + '.firstTerm')
        cmds.setAttr(slide_ik_stretch_condiiton + '.colorIfTrueR', length_limb)
        cmds.connectAttr(slide_ik_dist_condition + '.outColorR', slide_ik_stretch_condiiton + '.colorIfFalseR')

        # connect condition  limb to pma stretchIkUrSum
        cmds.connectAttr(slide_ik_stretch_condiiton + '.outColorR', stretch_ik_sum + '.input1D[1]')

    def limb_add_attr_ik(self, controller, follow, prefix):
        rt_utils.add_attribute(objects=[controller], long_name=['%s%s' % (prefix, 'IkSetup')], nice_name=[' '],
                               at="enum",
                               en='%s%s' % (prefix.capitalize(), ' Ik Setup'), channel_box=True)

        rt_utils.add_attribute(objects=[controller], long_name=['follow'],
                               at="enum", en=follow, keyable=True)

        rt_utils.add_attribute(objects=[controller], long_name=['stretch'],
                               at="float", min=0, max=1, dv=1, keyable=True)

        rt_utils.add_attribute(objects=[controller], long_name=['softIk'],
                               at="float", min=0, max=20, dv=0, keyable=True)

        self.slide_attr = rt_utils.add_attribute(objects=[controller], long_name=['slide'],
                                                 at="float", min=-10, max=10, dv=0, keyable=True)

        self.ikSnap_attr = rt_utils.add_attribute(objects=[controller], long_name=['ikSnap'],
                                                  at="float", min=0, max=1, dv=0, keyable=True)

        rt_utils.add_attribute(objects=[controller], long_name=['twist'],
                               at="float", dv=0, keyable=True)

    def limb_distance(self, prefix, pos_up_jnt, pos_low_jnt, dist_between_name, side):
        distanceNode = cmds.shadingNode('distanceBetween', asUtility=1,
                                        n='%s%s%s_dist' % (prefix, dist_between_name, side))
        cmds.connectAttr(pos_up_jnt + '.worldMatrix[0]', distanceNode + '.inMatrix1')
        cmds.connectAttr(pos_low_jnt + '.worldMatrix[0]', distanceNode + '.inMatrix2')
        cmds.connectAttr(pos_up_jnt + '.rotatePivotTranslate', distanceNode + '.point1')
        cmds.connectAttr(pos_low_jnt + '.rotatePivotTranslate', distanceNode + '.point2')

        return distanceNode

    def limb_poleVector_snap_ik(self, get_value_tx_upper_limb_jnt, prefix, side, obj_poleVector,
                                slide_ik_pma_stretch,
                                scale_poleVector_snap_mdn, limb_ik_jnt):
        # snaplimb to pole vector
        poleVector_snap_bta = cmds.shadingNode('blendTwoAttr', asUtility=1,
                                               n='%s%s%s%s_bta' % (prefix, 'PoleVecSnapIk', obj_poleVector, side))
        poleVector_mult_rev = cmds.shadingNode('multDoubleLinear', asUtility=1,
                                               n='%s%s%s%s%s_mdl' % (
                                                   prefix, 'PoleVecSnapIk', obj_poleVector, 'Rev', side))
        if get_value_tx_upper_limb_jnt > 0:
            cmds.setAttr(poleVector_mult_rev + '.input2', 1)
        else:
            cmds.setAttr(poleVector_mult_rev + '.input2', -1)

        cmds.connectAttr(self.controller_lower_limb_ik.control + '.%s' % self.ikSnap_attr,
                         poleVector_snap_bta + '.attributesBlender')
        cmds.connectAttr(slide_ik_pma_stretch + '.output1D', poleVector_snap_bta + '.input[0]')
        cmds.connectAttr(scale_poleVector_snap_mdn + '.outputX', poleVector_mult_rev + '.input1')
        cmds.connectAttr(poleVector_mult_rev + '.output', poleVector_snap_bta + '.input[1]')

        cmds.connectAttr(poleVector_snap_bta + '.output', limb_ik_jnt + '.translateY')

    def limb_volume_position(self, prefix_limb_dtl, side, operation, num_joint, dv_min, dv_max, v_min, v_max):
        ## upper limb
        # condition
        volume_pos_condition = cmds.shadingNode('condition', asUtility=1,
                                                n='%s%s%s_cnd' % (prefix_limb_dtl, 'CombineVolumePos', side))
        cmds.setAttr(volume_pos_condition + '.operation', operation)
        cmds.connectAttr(self.ctrl_mid_middle_limb.control + '.volumePosition', volume_pos_condition + '.firstTerm')
        cmds.connectAttr(self.ctrl_mid_middle_limb.control + '.volumePosition', volume_pos_condition + '.colorIfFalseR')
        cmds.connectAttr(self.ctrl_mid_middle_limb.control + '.volumePosition', volume_pos_condition + '.colorIfTrueR')

        # add double linear
        volume_position_mdl = cmds.shadingNode('multDoubleLinear', asUtility=1,
                                               n='%s%s%s_mdl' % (prefix_limb_dtl, 'CombineVolumePos', side))
        cmds.connectAttr(self.ctrl_mid_middle_limb.control + '.volume', volume_position_mdl + '.input2')

        # connect using keyframe inbetween
        # min
        cmds.setDrivenKeyframe(volume_position_mdl + '.input1',
                               cd=volume_pos_condition + '.outColorR',
                               dv=dv_min, v=v_min, itt='linear', ott='linear')
        # max
        cmds.setDrivenKeyframe(volume_position_mdl + '.input1',
                               cd=volume_pos_condition + '.outColorR',
                               dv=num_joint * dv_max, v=v_max, itt='linear', ott='linear')

        return volume_position_mdl
