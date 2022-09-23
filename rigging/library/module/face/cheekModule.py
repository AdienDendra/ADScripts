from __future__ import absolute_import

import maya.cmds as cmds

from rigging.library.base.face import cheek as rlbf_cheek
from rigging.library.utils import transform as rlu_transform
from rigging.tools import utils as rt_utils


class Cheek:
    def __init__(self,
                 face_anim_ctrl_grp,
                 face_utils_grp,
                 cheek_low_jnt,
                 cheek_low_prefix,
                 cheek_mid_jnt,
                 cheek_mid_prefix,
                 cheek_up_jnt,
                 cheek_up_prefix,
                 cheek_in_up_jnt,
                 cheek_in_up_prefix,
                 cheek_in_low_jnt,
                 cheek_in_low_prefix,
                 cheek_out_up_jnt,
                 cheek_out_up_prefix,
                 cheek_out_low_jnt,
                 cheek_out_low_prefix,
                 scale,
                 side,
                 side_RGT,
                 side_LFT,
                 head_low_jnt,
                 head_up_jnt,
                 jaw_jnt,
                 corner_lip_ctrl,
                 corner_lip_ctrl_attr_cheek_low,
                 corner_lip_ctrl_attr_cheek_mid,
                 lip_drive_ctrl,
                 mouth_ctrl,
                 mouth_cheek_in_up_attr,
                 low_lip_drive_ctrl,
                 nostril_drive_ctrl_attr_cheek_up,
                 nostril_drive_ctrl_attr_cheek_up_two,
                 nostril_drive_ctrl,
                 corner_lip_ctrl_attr_cheek_out_up,
                 corner_lip_ctrl_attr_cheek_out_low,
                 head_up_ctrl,
                 head_low_ctrl,
                 suffix_controller,
                 ):

        self.position = cmds.xform(corner_lip_ctrl, ws=1, q=1, t=1)[0]
        self.nostril = cmds.xform(nostril_drive_ctrl, ws=1, q=1, t=1)[0]
        self.side_RGT = side_RGT
        self.side_LFT = side_LFT
        # group cheek driver
        group_driver = cmds.group(em=1, n='cheekJoint' + side + '_grp')
        setup_driver_grp = cmds.group(em=1, n='cheekSetup' + side + '_grp')
        ctrl_driver_grp = cmds.group(em=1, n='cheekCtrlAll' + side + '_grp')

        cmds.hide(setup_driver_grp)
        grp_cheek_all = cmds.group(em=1, n='cheek' + side + '_grp')
        cmds.parent(group_driver, setup_driver_grp, grp_cheek_all)
        cmds.parent(ctrl_driver_grp, face_anim_ctrl_grp)
        cmds.parent(grp_cheek_all, face_utils_grp)
        self.cheek_joint_grp = group_driver

        cheek = rlbf_cheek.Build(
            cheek_low_jnt=cheek_low_jnt,
            cheek_low_prefix=cheek_low_prefix,
            cheek_mid_jnt=cheek_mid_jnt,
            cheek_mid_prefix=cheek_mid_prefix,
            cheek_up_jnt=cheek_up_jnt,
            cheek_up_prefix=cheek_up_prefix,
            cheek_in_up_jnt=cheek_in_up_jnt,
            cheek_in_up_prefix=cheek_in_up_prefix,
            cheek_in_low_jnt=cheek_in_low_jnt,
            cheek_in_low_prefix=cheek_in_low_prefix,
            cheek_out_up_jnt=cheek_out_up_jnt,
            cheek_out_up_prefix=cheek_out_up_prefix,
            cheek_out_low_jnt=cheek_out_low_jnt,
            cheek_out_low_prefix=cheek_out_low_prefix,
            scale=scale,
            side=side,
            suffix_controller=suffix_controller)

        cmds.parent(cheek.cheek_low_jnt_grp[0], cheek.cheek_mid_jnt_grp[0],
                    cheek.cheek_up_jnt_grp[0], cheek.cheek_in_up_jnt_grp[0],
                    cheek.cheek_in_low_jnt_grp[0],
                    cheek.cheek_out_up_jnt_grp[0],
                    cheek.cheek_out_low_jnt_grp[0], group_driver)

        cmds.parent(cheek.cheek_low_ctrl_grp, cheek.cheek_mid_ctrl_grp,
                    cheek.cheek_up_ctrl_grp, cheek.cheek_in_up_ctrl_grp,
                    cheek.cheek_in_low_ctrl_grp,
                    cheek.cheek_out_up_ctrl_grp,
                    cheek.cheek_out_low_ctrl_grp, ctrl_driver_grp)

        self.cheek_low_ctrl_grp = cheek.cheek_low_ctrl_grp
        self.cheek_mid_ctrl_grp = cheek.cheek_mid_ctrl_grp
        self.cheek_out_up_ctrl_grp = cheek.cheek_out_up_ctrl_grp
        self.cheek_out_low_ctrl_grp = cheek.cheek_out_low_ctrl_grp

        self.cheek_up_ctrl_grp = cheek.cheek_up_ctrl_grp
        self.cheek_in_up_ctrl_grp = cheek.cheek_in_up_ctrl_grp
        self.cheek_in_low_ctrl_grp = cheek.cheek_in_low_ctrl_grp

        # ==================================================================================================================
        #                                                       SET DRIVER
        # ==================================================================================================================
        # CHEEK OUT UP
        cheek_out_up_set = self.set_driver_cheek(expression_mid_out_area=True, name_expression='OutUp',
                                                 attribute_offset=corner_lip_ctrl_attr_cheek_out_up,
                                                 object_prefix=cheek_out_up_prefix, object_joint=cheek_out_up_jnt,
                                                 side=side, scale=scale, constraint=[head_up_jnt], w=[1.0],
                                                 group_driver_jnt=cheek.cheek_out_up_jnt_grp[0],
                                                 controller=corner_lip_ctrl,
                                                 cheek_joint_grp_offset=cheek.cheek_out_up_jnt_grp[1],
                                                 cheek_joint_grp=cheek.cheek_out_up_jnt_grp[0],
                                                 cheek_ctrl_grp=cheek.cheek_out_up_ctrl_grp,
                                                 cheek_ctrl_grp_offset=cheek.cheek_out_up_ctrl_grp_offset,
                                                 cheek_ctrl=cheek.cheek_out_up_ctrl, cheek_jnt=cheek_out_up_jnt,
                                                 value_div_tx=12.0, value_div_ty=12.0, range_one_tz=24.0,
                                                 range_two_tz=24.0,
                                                 range_one_ty=72.0, range_two_ty=16.0, multiplier_tz=1.0
                                                 )

        # CHEEK OUT LOW
        cheek_out_low_set = self.set_driver_cheek(expression_mid_out_area=True, name_expression='OutLow',
                                                  attribute_offset=corner_lip_ctrl_attr_cheek_out_low,
                                                  object_prefix=cheek_out_low_prefix, object_joint=cheek_out_low_jnt,
                                                  side=side, scale=scale, constraint=[head_low_jnt, jaw_jnt],
                                                  w=[1.0, 0.5], interp_type=2,
                                                  group_driver_jnt=cheek.cheek_out_low_jnt_grp[0],
                                                  controller=corner_lip_ctrl,
                                                  cheek_joint_grp_offset=cheek.cheek_out_low_jnt_grp[1],
                                                  cheek_joint_grp=cheek.cheek_out_low_jnt_grp[0],
                                                  cheek_ctrl_grp=cheek.cheek_out_low_ctrl_grp,
                                                  cheek_ctrl_grp_offset=cheek.cheek_out_low_ctrl_grp_offset,
                                                  cheek_ctrl=cheek.cheek_out_low_ctrl, cheek_jnt=cheek_out_low_jnt,
                                                  value_div_tx=3.0, value_div_ty=3.0, range_one_tz=6.0,
                                                  range_two_tz=6.0,
                                                  range_one_ty=18.0, range_two_ty=4.0, multiplier_tz=1.0
                                                  )

        # CHEEK UP
        cheek_up_set = self.set_driver_cheek(expression_mid_up_area=True, name_expression='Up',
                                             attribute_offset=nostril_drive_ctrl_attr_cheek_up,
                                             attribute_offset_two=nostril_drive_ctrl_attr_cheek_up_two,
                                             object_prefix=cheek_up_prefix, object_joint=cheek_up_jnt,
                                             side=side, scale=scale, constraint=[head_up_jnt], w=[1.0],
                                             group_driver_jnt=cheek.cheek_up_jnt_grp[0],
                                             controller=nostril_drive_ctrl,
                                             cheek_joint_grp_offset=cheek.cheek_up_jnt_grp[1],
                                             cheek_joint_grp=cheek.cheek_up_jnt_grp[0],
                                             cheek_ctrl_grp=cheek.cheek_up_ctrl_grp,
                                             cheek_ctrl_grp_offset=cheek.cheek_up_ctrl_grp_offset,
                                             cheek_ctrl=cheek.cheek_up_ctrl, cheek_jnt=cheek_up_jnt,
                                             range_one_tz=0.75, range_two_tz=4.5)

        # CHEEK MID
        cheek_mid_set = self.set_driver_cheek(expression_mid_out_area=True, name_expression='Mid',
                                              attribute_offset=corner_lip_ctrl_attr_cheek_mid,
                                              object_prefix=cheek_mid_prefix, object_joint=cheek_mid_jnt,
                                              side=side, scale=scale, constraint=[head_up_jnt, head_low_jnt, jaw_jnt],
                                              w=[0.7, 0.2, 0.1], interp_type=2,
                                              group_driver_jnt=cheek.cheek_mid_jnt_grp[0],
                                              controller=corner_lip_ctrl,
                                              cheek_joint_grp_offset=cheek.cheek_mid_jnt_grp[1],
                                              cheek_joint_grp=cheek.cheek_mid_jnt_grp[0],
                                              cheek_ctrl_grp=cheek.cheek_mid_ctrl_grp,
                                              cheek_ctrl_grp_offset=cheek.cheek_mid_ctrl_grp_offset,
                                              cheek_ctrl=cheek.cheek_mid_ctrl, cheek_jnt=cheek_mid_jnt,
                                              value_div_tx=1.5, value_div_ty=1.5, range_one_tz=4.0, range_two_tz=4.0,
                                              range_one_ty=18.0, range_two_ty=3.0, multiplier_tz=1.0
                                              )

        # CHEEK LOW
        cheek_low_set = self.set_driver_cheek(expression_mid_out_area=True, name_expression='Low',
                                              attribute_offset=corner_lip_ctrl_attr_cheek_low,
                                              object_prefix=cheek_low_prefix, object_joint=cheek_low_jnt,
                                              side=side, scale=scale, constraint=[head_low_jnt, jaw_jnt], w=[0.4, 0.6],
                                              interp_type=2,
                                              group_driver_jnt=cheek.cheek_low_jnt_grp[0],
                                              controller=corner_lip_ctrl,
                                              cheek_joint_grp_offset=cheek.cheek_low_jnt_grp[1],
                                              cheek_joint_grp=cheek.cheek_low_jnt_grp[0],
                                              cheek_ctrl_grp=cheek.cheek_low_ctrl_grp,
                                              cheek_ctrl_grp_offset=cheek.cheek_low_ctrl_grp_offset,
                                              cheek_ctrl=cheek.cheek_low_ctrl, cheek_jnt=cheek_low_jnt,
                                              value_div_tx=0.85, value_div_ty=0.85, range_one_tz=3.0, range_two_tz=3.0,
                                              range_one_ty=9.0, range_two_ty=2.0, multiplier_tz=0.5
                                              )
        # CHEEK IN UP
        cheek_in_up = self.set_driver_cheek(expression_in_area=True, name_expression='InUp',
                                            object_prefix=cheek_in_up_prefix, object_joint=cheek_in_up_jnt,
                                            side=side, scale=scale, constraint=[head_low_jnt, jaw_jnt], w=[0.8, 0.2],
                                            interp_type=2,
                                            group_driver_jnt=cheek.cheek_in_up_jnt_grp[0],
                                            controller=corner_lip_ctrl,
                                            cheek_joint_grp_offset=cheek.cheek_in_up_jnt_grp[1],
                                            cheek_joint_grp=cheek.cheek_in_up_jnt_grp[0],
                                            cheek_ctrl_grp=cheek.cheek_in_up_ctrl_grp,
                                            cheek_ctrl_grp_offset=cheek.cheek_in_up_ctrl_grp_offset,
                                            cheek_ctrl=cheek.cheek_in_up_ctrl, cheek_jnt=cheek_in_up_jnt,
                                            value_div_tx=2.0, value_div_ty=2.5, value_div_tz=2.0,
                                            lip_drive_ctrl=lip_drive_ctrl, mouth_ctrl=mouth_ctrl,
                                            mouth_cheek_in_up_attr=mouth_cheek_in_up_attr
                                            )

        # CHEEK IN LOW
        chek_in_low = self.set_driver_cheek(cheek_in_low=True, object_prefix=cheek_in_low_prefix,
                                            object_joint=cheek_in_low_jnt,
                                            side=side, scale=scale,
                                            constraint=[cheek_low_jnt, low_lip_drive_ctrl, jaw_jnt],
                                            w=[0.25, 0.75, 1.0], interp_type=2,
                                            group_driver_jnt=cheek.cheek_in_low_jnt_grp[0],
                                            cheek_joint_grp_offset=cheek.cheek_in_low_jnt_grp[1],
                                            cheek_joint_grp=cheek.cheek_in_low_jnt_grp[0],
                                            cheek_ctrl_grp=cheek.cheek_in_low_ctrl_grp,
                                            cheek_ctrl_grp_offset=cheek.cheek_in_low_ctrl_grp_offset,
                                            cheek_ctrl=cheek.cheek_in_low_ctrl, cheek_jnt=cheek_in_low_jnt,
                                            )

        # SCALE CONSTRAINT SET GRP
        cmds.scaleConstraint(head_up_ctrl, head_low_ctrl, cheek_out_up_set, mo=1)
        cmds.scaleConstraint(head_low_ctrl, cheek_out_low_set, mo=1)
        cmds.scaleConstraint(head_up_ctrl, cheek_up_set, mo=1)
        cmds.scaleConstraint(head_up_ctrl, head_low_ctrl, cheek_mid_set, mo=1)
        cmds.scaleConstraint(head_low_ctrl, cheek_low_set, mo=1)
        cmds.scaleConstraint(head_low_ctrl, cheek_in_up, mo=1)
        cmds.scaleConstraint(head_low_ctrl, chek_in_low, mo=1)

        cmds.parent(cheek_out_up_set, cheek_out_low_set, cheek_up_set, cheek_mid_set, cheek_low_set, cheek_in_up,
                    chek_in_low, setup_driver_grp)

    # ==================================================================================================================
    #                                       FUNCTION SETUP FOR PART CHEEK JOINTS
    # ==================================================================================================================

    def set_driver_cheek(self, name_expression='', attribute_offset='', attribute_offset_two='', object_prefix='',
                         object_joint='',
                         side='', scale=None, group_driver_jnt='', cheek_in_low=None,
                         value_div_tx=None, value_div_ty=None, value_div_tz=None,
                         range_one_tz=None, range_two_tz=None, range_one_ty=None, range_two_ty=None,
                         expression_mid_out_area=None, expression_in_area=None, expression_mid_up_area=None,
                         constraint=[], w=[], interp_type=1, controller='', cheek_joint_grp_offset='',
                         cheek_joint_grp='',
                         cheek_ctrl_grp='', cheek_ctrl_grp_offset='', cheek_ctrl='', cheek_jnt='',
                         lip_drive_ctrl='', mouth_ctrl='', mouth_cheek_in_up_attr='', multiplier_tz=None
                         ):

        if self.position < 0:
            multiplier = -1
        else:
            multiplier = 1

        if self.nostril < 0:
            operator = 2
        else:
            operator = 1

        # mc.select(cl=1)
        parent_driver = cmds.group(em=1, n=rt_utils.prefix_name(object_prefix) + side + '_set')
        driver = cmds.spaceLocator(n=rt_utils.prefix_name(object_prefix) + 'Drv' + side + '_set')[0]
        cmds.parent(driver, parent_driver)
        cmds.delete(cmds.parentConstraint(object_joint, parent_driver, mo=0))

        cmds.setAttr(driver + '.localScaleX', 0.5 * scale)
        cmds.setAttr(driver + '.localScaleY', 0.5 * scale)
        cmds.setAttr(driver + '.localScaleZ', 0.5 * scale)

        const_interp = None
        for cons, value in zip(constraint, w):
            const_interp = cmds.parentConstraint(cons, parent_driver, mo=1, w=value)
            # constraint rename
            const_interp = rt_utils.constraint_rename(const_interp)

        # SET INTERPOLATION
        cmds.setAttr(const_interp[0] + '.interpType', interp_type)
        rt_utils.connect_attr_object(parent_driver, group_driver_jnt)

        # CORNER LIP FOR REVERSE
        # CREATE MULTIPLIER CONTROLLER
        controller_news = rlu_transform.reposition_side(object=controller, side_RGT=self.side_RGT,
                                                        side_LFT=self.side_LFT)
        controller_new = rlu_transform.reorder_number(prefix=controller_news, side_RGT=self.side_RGT,
                                                      side_LFT=self.side_LFT)

        driver_new = rlu_transform.reposition_side(object=driver, side_RGT=self.side_RGT, side_LFT=self.side_LFT)

        lip_drive_ctrl_new = rlu_transform.reposition_side(object=lip_drive_ctrl, side_RGT=self.side_RGT,
                                                           side_LFT=self.side_LFT)

        mouth_ctrl_new = rlu_transform.reposition_side(object=mouth_ctrl, side_RGT=self.side_RGT,
                                                       side_LFT=self.side_LFT)

        new_cheek_joint_grp_offset = rlu_transform.reposition_side(object=cheek_joint_grp_offset,
                                                                   side_RGT=self.side_RGT, side_LFT=self.side_LFT)

        if expression_mid_up_area:
            range_mid_up_z = controller + '.%s' % attribute_offset
            range_mid_up = controller + '.%s' % attribute_offset_two

            # DIVIDED FOR RANGE
            ctrl_drv_range_mdn = cmds.createNode('multiplyDivide', n=rt_utils.prefix_name(
                controller_new[0]) + 'Range' + name_expression + 'Ctrl' + side + '_mdn')
            cmds.setAttr(ctrl_drv_range_mdn + '.operation', 2)
            cmds.setAttr(ctrl_drv_range_mdn + '.input1X', 2)
            cmds.setAttr(ctrl_drv_range_mdn + '.input1Y', 2)
            cmds.connectAttr(range_mid_up, ctrl_drv_range_mdn + '.input2X')
            cmds.connectAttr(range_mid_up_z, ctrl_drv_range_mdn + '.input2Y')

            # DIVIDED BY CONTROLLER
            ctrl_drv_tx_mdn = self.mult_or_div_connect_attr(name=controller_new[0], prefix='Tx',
                                                            name_expression=name_expression,
                                                            side=side, input2X=ctrl_drv_range_mdn + '.outputX',
                                                            input1X=controller + '.translateX', operation=2)

            ctrl_drv_ty_mdn = self.mult_or_div_connect_attr(name=controller_new[0], prefix='Ty',
                                                            name_expression=name_expression,
                                                            side=side, input2X=ctrl_drv_range_mdn + '.outputX',
                                                            input1X=controller + '.translateY', operation=2)

            # ADD OR SUBTRACT FROM SET GRP
            ctrl_drv_tx_pma = self.pma_expr(name=new_cheek_joint_grp_offset, prefix='Tx',
                                            name_expression=name_expression, side=side,
                                            operation=operator, input0=driver + '.translateX',
                                            input1=ctrl_drv_tx_mdn + '.outputX')

            ctrl_drv_ty_pma = self.pma_expr(name=new_cheek_joint_grp_offset, prefix='Ty',
                                            name_expression=name_expression, side=side,
                                            operation=1, input0=driver + '.translateY',
                                            input1=ctrl_drv_ty_mdn + '.outputX')

            # TRANSLATE Z
            corner_lip_drv_tz_range_mdl = self.mdl_set_attr(name=controller_new[0], prefix='TzRange',
                                                            name_expression=name_expression, side=side,
                                                            input1=range_mid_up, input2Set=2)

            # DIVIDED BY CONTROLLER
            ctrl_drv_tz_mdn = self.mult_or_div_connect_attr(name=controller_new[0], prefix='Tz',
                                                            name_expression=name_expression,
                                                            side=side, input2X=corner_lip_drv_tz_range_mdl + '.output',
                                                            input1X=controller + '.translateZ', operation=2)

            # ADD WITH SET CONTROLLER
            ctrl_drv_tz_driver_pma = self.pma_expr(name=driver_new, prefix='Tz', name_expression=name_expression,
                                                   side=side,
                                                   operation=1, input0=ctrl_drv_tz_mdn + '.outputX',
                                                   input1=driver + '.translateZ')

            # MULT RANGE NORMAL
            corner_lip_drv_tz_range_one_mdl = self.mdl_set_attr(name=controller_new[0], prefix='TzRangeOne',
                                                                name_expression=name_expression, side=side,
                                                                input1=ctrl_drv_range_mdn + '.outputX',
                                                                input2Set=range_one_tz)
            corner_lip_drv_tz_range_two_mdl = self.mdl_set_attr(name=controller_new[0], prefix='TzRangeTwo',
                                                                name_expression=name_expression, side=side,
                                                                input1=ctrl_drv_range_mdn + '.outputX',
                                                                input2Set=range_two_tz)

            # MULT RANGE Z
            corner_lip_drv_tz_range_z_one_mdl = self.mdl_connect_attr(name=controller_new[0], prefix='TzRangeZOne',
                                                                      name_expression=name_expression,
                                                                      side=side,
                                                                      input1=corner_lip_drv_tz_range_one_mdl + '.output',
                                                                      input2=ctrl_drv_range_mdn + '.outputY')

            corner_lip_drv_tz_range_z_two_mdl = self.mdl_connect_attr(name=controller_new[0], prefix='TzRangeZTwo',
                                                                      name_expression=name_expression,
                                                                      side=side,
                                                                      input1=corner_lip_drv_tz_range_two_mdl + '.output',
                                                                      input2=ctrl_drv_range_mdn + '.outputY')

            # DIVIDE RANGE Z AND RANGE NORMAL
            ctrl_drv_tz_range_one_mdn = self.mult_or_div_connect_attr(name=controller_new[0], prefix='TzRangeOneMul',
                                                                      name_expression=name_expression,
                                                                      side=side,
                                                                      input2X=corner_lip_drv_tz_range_z_one_mdl + '.output',
                                                                      input1X=controller + '.translateY', operation=2)

            ctrl_drv_tz_range_two_mdn = self.mult_or_div_connect_attr(name=controller_new[0], prefix='TzRangeTwoMul',
                                                                      name_expression=name_expression,
                                                                      side=side,
                                                                      input2X=corner_lip_drv_tz_range_z_two_mdl + '.output',
                                                                      input1X=controller + '.translateY', operation=2)

            # ADD WITH SET CONTROLLER
            ctrl_drv_tz_range_pma = cmds.createNode('plusMinusAverage',
                                                    n=rt_utils.prefix_name(new_cheek_joint_grp_offset)
                                                      + 'TzRange' + name_expression + 'Grp' + side + '_pma')
            cmds.connectAttr(ctrl_drv_tz_range_one_mdn + '.outputX', ctrl_drv_tz_range_pma + '.input2D[0].input2Dx')
            cmds.connectAttr(ctrl_drv_tz_range_two_mdn + '.outputX', ctrl_drv_tz_range_pma + '.input2D[0].input2Dy')
            cmds.connectAttr(ctrl_drv_tz_driver_pma + '.output1D', ctrl_drv_tz_range_pma + '.input2D[1].input2Dx')
            cmds.connectAttr(ctrl_drv_tz_driver_pma + '.output1D', ctrl_drv_tz_range_pma + '.input2D[1].input2Dy')

            # CREATE CONDITION FOR TY AND TZ CONTROLLER
            ctrl_drv_tz_range_cnd = cmds.createNode('condition', n=rt_utils.prefix_name(
                new_cheek_joint_grp_offset) + 'Tz' + name_expression + 'Ctrl' + side + '_cnd')
            cmds.setAttr(ctrl_drv_tz_range_cnd + '.operation', 2)
            cmds.connectAttr(controller + '.translateY', ctrl_drv_tz_range_cnd + '.firstTerm')
            cmds.connectAttr(ctrl_drv_tz_range_pma + '.output2D.output2Dx', ctrl_drv_tz_range_cnd + '.colorIfTrueR')
            cmds.connectAttr(ctrl_drv_tz_range_pma + '.output2D.output2Dy', ctrl_drv_tz_range_cnd + '.colorIfFalseR')

            # CONNECT TO OBJECT SET TARGET
            cmds.connectAttr(ctrl_drv_tx_pma + '.output1D', cheek_joint_grp_offset + '.translateX')
            cmds.connectAttr(ctrl_drv_ty_pma + '.output1D', cheek_joint_grp_offset + '.translateY')
            cmds.connectAttr(ctrl_drv_tz_range_cnd + '.outColorR', cheek_joint_grp_offset + '.translateZ')

            # CONNECT ROTATE TO OBJECT
            rt_utils.connect_attr_rotate(controller, cheek_joint_grp_offset)

        if expression_mid_out_area:
            corner_lip_drv_tx_mdl = self.mdl_set_attr(name=controller_new[0], prefix='Tx',
                                                      name_expression=name_expression, side=side,
                                                      input1=controller + '.translateX',
                                                      input2Set=multiplier)

            range_mid_out = controller + '.%s' % attribute_offset

            # CREATE MULTIPLY FOR CONTROLLER
            corner_lip_drv_trans_low_xmdn = self.mult_or_div_connect_attr(name=controller_new[0], prefix='TransX',
                                                                          name_expression=name_expression,
                                                                          side=side, input2X=range_mid_out,
                                                                          input1X=corner_lip_drv_tx_mdl + '.output',
                                                                          operation=1)

            corner_lip_drv_trans_low_ymdn = self.mult_or_div_connect_attr(name=controller_new[0], prefix='TransY',
                                                                          name_expression=name_expression,
                                                                          side=side, input2X=range_mid_out,
                                                                          input1X=controller + '.translateY',
                                                                          operation=1)

            # CREATE DIVIDED FOR CONTROLLER TO THE VALUE
            corner_lip_drv_div_trans_x_low_mdn = self.mult_or_div_set_attr(name=controller_new[0], prefix='DivTransX',
                                                                           name_expression=name_expression,
                                                                           side=side, input2XSet=value_div_tx,
                                                                           input1X=corner_lip_drv_trans_low_xmdn + '.outputX',
                                                                           operation=2)

            corner_lip_drv_div_trans_y_low_mdn = self.mult_or_div_set_attr(name=controller_new[0], prefix='DivTransY',
                                                                           name_expression=name_expression,
                                                                           side=side, input2XSet=value_div_ty,
                                                                           input1X=corner_lip_drv_trans_low_ymdn + '.outputX',
                                                                           operation=2)

            # CREATE PLUS MINUS AVERAGE CHEEK LOW TX AND TY SET AND CONTROLLER
            cheek_low_corner_lip_drv_tx_ty_pma = cmds.createNode('plusMinusAverage',
                                                                 n=rt_utils.prefix_name(new_cheek_joint_grp_offset)
                                                                   + 'TxTy' + name_expression + 'Grp' + side + '_pma')

            cmds.connectAttr(corner_lip_drv_div_trans_x_low_mdn + '.outputX',
                             cheek_low_corner_lip_drv_tx_ty_pma + '.input2D[0].input2Dx')
            cmds.connectAttr(corner_lip_drv_div_trans_y_low_mdn + '.outputX',
                             cheek_low_corner_lip_drv_tx_ty_pma + '.input2D[0].input2Dy')
            cmds.connectAttr(driver + '.translateX', cheek_low_corner_lip_drv_tx_ty_pma + '.input2D[1].input2Dx')
            cmds.connectAttr(driver + '.translateY', cheek_low_corner_lip_drv_tx_ty_pma + '.input2D[1].input2Dy')

            # CONNECTION TY
            corner_lip_drv_ty_mdl = self.mdl_connect_attr(name=controller_new[0], prefix='TyTrans',
                                                          name_expression=name_expression, side=side,
                                                          input1=controller + '.translateY',
                                                          input2=range_mid_out)

            # CREATE DIVIDED FOR TY CONTROLLER TO THE VALUE
            corner_lip_drv_ty_div_trans_low_one_mdn = self.mult_or_div_set_attr(name=controller_new[0],
                                                                                prefix='DivTyTransOne',
                                                                                name_expression=name_expression,
                                                                                side=side, input2XSet=range_one_ty,
                                                                                input1X=corner_lip_drv_ty_mdl + '.output',
                                                                                operation=2)

            corner_lip_drv_ty_div_trans_low_two_mdn = self.mult_or_div_set_attr(name=controller_new[0],
                                                                                prefix='DivTyTransTwo',
                                                                                name_expression=name_expression,
                                                                                side=side, input2XSet=range_two_ty,
                                                                                input1X=corner_lip_drv_ty_mdl + '.output',
                                                                                operation=2)

            # CONNECTION TZ
            corner_lip_drv_tz_mdl = self.mdl_connect_attr(name=controller_new[0], prefix='TzTrans',
                                                          name_expression=name_expression, side=side,
                                                          input1=controller + '.translateZ',
                                                          input2=range_mid_out)

            # CREATE DIVIDED FOR TZ CONTROLLER TO THE VALUE
            corner_lip_drv_tz_div_trans_low_one_mdn = self.mult_or_div_set_attr(name=controller_new[0],
                                                                                prefix='DivTzTransOne',
                                                                                name_expression=name_expression,
                                                                                side=side, input2XSet=range_one_tz,
                                                                                input1X=corner_lip_drv_tz_mdl + '.output',
                                                                                operation=2)

            corner_lip_drv_tz_div_trans_low_two_mdn = self.mult_or_div_set_attr(name=controller_new[0],
                                                                                prefix='DivTzTransTwo',
                                                                                name_expression=name_expression,
                                                                                side=side, input2XSet=range_two_tz,
                                                                                input1X=corner_lip_drv_tz_mdl + '.output',
                                                                                operation=2)

            # CREATE PLUS MINUS FOR CONDITION
            cheek_low_corner_lip_drv_tz_pma = cmds.createNode('plusMinusAverage',
                                                              n=rt_utils.prefix_name(new_cheek_joint_grp_offset)
                                                                + 'Tz' + name_expression + 'Grp' + side + '_pma')
            cmds.connectAttr(corner_lip_drv_tz_div_trans_low_one_mdn + '.outputX',
                             cheek_low_corner_lip_drv_tz_pma + '.input2D[0].input2Dx')
            cmds.connectAttr(corner_lip_drv_tz_div_trans_low_two_mdn + '.outputX',
                             cheek_low_corner_lip_drv_tz_pma + '.input2D[0].input2Dy')
            cmds.connectAttr(corner_lip_drv_ty_div_trans_low_one_mdn + '.outputX',
                             cheek_low_corner_lip_drv_tz_pma + '.input2D[1].input2Dx')
            cmds.connectAttr(corner_lip_drv_ty_div_trans_low_two_mdn + '.outputX',
                             cheek_low_corner_lip_drv_tz_pma + '.input2D[1].input2Dy')

            cmds.connectAttr(driver + '.translateZ', cheek_low_corner_lip_drv_tz_pma + '.input2D[2].input2Dx')
            cmds.connectAttr(driver + '.translateZ', cheek_low_corner_lip_drv_tz_pma + '.input2D[3].input2Dy')

            # CREATE CONDITION FOR TY AND TZ CONTROLLER
            corner_lip_drv_ty_div_trans_low_cnd = cmds.createNode('condition',
                                                                  n=rt_utils.prefix_name(controller_new[
                                                                                             0]) + 'DivTyTrans' + name_expression + 'Ctrl' + side + '_cnd')
            cmds.setAttr(corner_lip_drv_ty_div_trans_low_cnd + '.operation', 4)
            cmds.connectAttr(controller + '.translateY', corner_lip_drv_ty_div_trans_low_cnd + '.firstTerm')
            cmds.connectAttr(cheek_low_corner_lip_drv_tz_pma + '.output2D.output2Dx',
                             corner_lip_drv_ty_div_trans_low_cnd + '.colorIfTrueR')
            cmds.connectAttr(cheek_low_corner_lip_drv_tz_pma + '.output2D.output2Dy',
                             corner_lip_drv_ty_div_trans_low_cnd + '.colorIfFalseR')

            # CREATE MULTIPLY Z CONTROLLER
            corner_lip_drv_tz_mult_mdl = self.mdl_set_attr(name=controller_new[0], prefix='MultTz',
                                                           name_expression=name_expression, side=side,
                                                           input1=corner_lip_drv_ty_div_trans_low_cnd + '.outColorR',
                                                           input2Set=multiplier_tz)

            # CONNECT TRANSLATE TO OBJECT
            cmds.connectAttr(cheek_low_corner_lip_drv_tx_ty_pma + '.output2Dx', cheek_joint_grp_offset + '.translateX')
            cmds.connectAttr(cheek_low_corner_lip_drv_tx_ty_pma + '.output2Dy', cheek_joint_grp_offset + '.translateY')

            cmds.connectAttr(corner_lip_drv_tz_mult_mdl + '.output', cheek_joint_grp_offset + '.translateZ')

            # CONNECT ROTATE TO OBJECT
            rt_utils.connect_attr_rotate(controller, cheek_joint_grp_offset)

        if expression_in_area:
            corner_lip_drv_tx_mdl = self.mdl_set_attr(name=controller_new[0], prefix='Tx',
                                                      name_expression=name_expression, side=side,
                                                      input1=controller + '.translateX',
                                                      input2Set=multiplier)

            # CREATE DIVIDE CONTROLLER
            corner_lip_drv_trans_mdn = cmds.createNode('multiplyDivide', n=rt_utils.prefix_name(
                controller_new[0]) + 'Trans' + name_expression + 'Ctrl' + side + '_mdn')
            cmds.setAttr(corner_lip_drv_trans_mdn + '.operation', 2)
            cmds.connectAttr(corner_lip_drv_tx_mdl + '.output', corner_lip_drv_trans_mdn + '.input1X')
            cmds.connectAttr(controller + '.translateY', corner_lip_drv_trans_mdn + '.input1Y')
            cmds.connectAttr(controller + '.translateZ', corner_lip_drv_trans_mdn + '.input1Z')

            cmds.setAttr(corner_lip_drv_trans_mdn + '.input2X', value_div_tx)
            cmds.setAttr(corner_lip_drv_trans_mdn + '.input2Y', value_div_ty)
            cmds.setAttr(corner_lip_drv_trans_mdn + '.input2Z', value_div_tz)

            # CREATE PLUS MINUS AVERAGE DRIVER AND CONTROLLER
            cheek_in_up_corner_lip_drv_pma = cmds.createNode('plusMinusAverage', n=rt_utils.prefix_name(driver_new) +
                                                                                   (rt_utils.prefix_name(
                                                                                       (controller_new[0])[
                                                                                           0].capitalize() +
                                                                                       rt_utils.prefix_name(
                                                                                           (controller_new[0])[1:]))) +
                                                                                   name_expression + 'Ctrl' + side + '_pma')

            cmds.connectAttr(driver + '.translate', cheek_in_up_corner_lip_drv_pma + '.input3D[0]')
            cmds.connectAttr(corner_lip_drv_trans_mdn + '.output', cheek_in_up_corner_lip_drv_pma + '.input3D[1]')

            # CREATE DIVIDE LIP DRIVE CTRL
            lip_up_drv_all_ctrl_trans_mdn = cmds.createNode('multiplyDivide', n=rt_utils.prefix_name(
                lip_drive_ctrl_new) + 'Trans' + name_expression + 'Ctrl' + side + '_mdn')
            cmds.setAttr(lip_up_drv_all_ctrl_trans_mdn + '.operation', 2)
            cmds.connectAttr(lip_drive_ctrl + '.translate', lip_up_drv_all_ctrl_trans_mdn + '.input1')

            cmds.setAttr(lip_up_drv_all_ctrl_trans_mdn + '.input2X', 2)
            cmds.setAttr(lip_up_drv_all_ctrl_trans_mdn + '.input2Y', 2)
            cmds.setAttr(lip_up_drv_all_ctrl_trans_mdn + '.input2Z', 2)

            # CREATE DIVIDE MOUTH CTRL
            mouth_ctrl_mul_attr = cmds.createNode('multiplyDivide',
                                                  n=rt_utils.prefix_name(
                                                      mouth_ctrl_new) + 'MulAttr' + name_expression + 'Ctrl' + side + '_mdn')
            cmds.setAttr(mouth_ctrl_mul_attr + '.operation', 2)
            cmds.connectAttr(mouth_ctrl + '.%s' % mouth_cheek_in_up_attr, mouth_ctrl_mul_attr + '.input2X')
            cmds.connectAttr(mouth_ctrl + '.%s' % mouth_cheek_in_up_attr, mouth_ctrl_mul_attr + '.input2Y')
            cmds.connectAttr(mouth_ctrl + '.%s' % mouth_cheek_in_up_attr, mouth_ctrl_mul_attr + '.input2Z')

            cmds.setAttr(mouth_ctrl_mul_attr + '.input1X', 25)
            cmds.setAttr(mouth_ctrl_mul_attr + '.input1Y', 25)
            cmds.setAttr(mouth_ctrl_mul_attr + '.input1Z', 25)

            mouth_ctrl_trans_mdn = cmds.createNode('multiplyDivide',
                                                   n=rt_utils.prefix_name(
                                                       mouth_ctrl_new) + 'Trans' + name_expression + 'Ctrl' + side + '_mdn')
            cmds.setAttr(mouth_ctrl_trans_mdn + '.operation', 2)
            cmds.connectAttr(mouth_ctrl + '.translate', mouth_ctrl_trans_mdn + '.input1')
            cmds.connectAttr(mouth_ctrl_mul_attr + '.output', mouth_ctrl_trans_mdn + '.input2')

            # CREATE PLUS MINUS LIP DRIVE CTRL AND MOUTH CTRL
            lip_up_drv_all_mouth_ctrl_trans_pma = cmds.createNode('plusMinusAverage',
                                                                  n=rt_utils.prefix_name(lip_drive_ctrl_new) +
                                                                    rt_utils.prefix_name(
                                                                        mouth_ctrl_new.capitalize()) + name_expression + 'Ctrl' + side + '_pma')
            cmds.connectAttr(lip_up_drv_all_ctrl_trans_mdn + '.output',
                             lip_up_drv_all_mouth_ctrl_trans_pma + '.input3D[0]')
            cmds.connectAttr(mouth_ctrl_trans_mdn + '.output', lip_up_drv_all_mouth_ctrl_trans_pma + '.input3D[1]')

            # CREATE PLUS MINUS LIP DRIVE CTRL AND MOUTH CTRL
            cheek_in_up_corner_lip_up_drv_all_mouth_pma = cmds.createNode('plusMinusAverage',
                                                                          n=rt_utils.prefix_name(
                                                                              new_cheek_joint_grp_offset)
                                                                            + name_expression + 'Grp' + side + '_pma')

            cmds.connectAttr(cheek_in_up_corner_lip_drv_pma + '.output3D',
                             cheek_in_up_corner_lip_up_drv_all_mouth_pma + '.input3D[0]')
            cmds.connectAttr(lip_up_drv_all_mouth_ctrl_trans_pma + '.output3D',
                             cheek_in_up_corner_lip_up_drv_all_mouth_pma + '.input3D[1]')

            # CONNECT TRANSLATE AND ROTATE
            cmds.connectAttr(cheek_in_up_corner_lip_up_drv_all_mouth_pma + '.output3D',
                             cheek_joint_grp_offset + '.translate')
            rt_utils.connect_attr_rotate(driver, cheek_joint_grp_offset)

        # connect attribute cheek  joint parent to cheek parent controller
        rt_utils.connect_attr_object(cheek_joint_grp, cheek_ctrl_grp)
        rt_utils.connect_attr_translate_rotate(cheek_joint_grp_offset, cheek_ctrl_grp_offset)

        # connect attribute cheek controller to cheek  joint
        if not cheek_in_low:
            if self.position < 0:
                self.reverse_node(cheek_ctrl, cheek_jnt, object_prefix, side)
                rt_utils.connect_attr_scale(cheek_ctrl, cheek_jnt)

            else:
                rt_utils.connect_attr_object(cheek_ctrl, cheek_jnt)
        else:
            reverse_trans = cmds.createNode('multiplyDivide',
                                            n=rt_utils.prefix_name(object_prefix) + 'ReverseTrans' + side + '_mdn')
            reverse_rotation = cmds.createNode('multiplyDivide',
                                               n=rt_utils.prefix_name(object_prefix) + 'ReverseRot' + side + '_mdn')

            if self.position < 0:
                cmds.setAttr(reverse_trans + '.input2X', -1)
                cmds.setAttr(reverse_trans + '.input2Y', -1)
                cmds.setAttr(reverse_trans + '.input2Z', 1)
                cmds.setAttr(reverse_rotation + '.input2X', -1)
                cmds.setAttr(reverse_rotation + '.input2Y', -1)
                cmds.setAttr(reverse_rotation + '.input2Z', 1)

            else:
                cmds.setAttr(reverse_trans + '.input2X', 1)
                cmds.setAttr(reverse_trans + '.input2Y', -1)
                cmds.setAttr(reverse_trans + '.input2Z', 1)
                cmds.setAttr(reverse_rotation + '.input2X', -1)
                cmds.setAttr(reverse_rotation + '.input2Y', 1)
                cmds.setAttr(reverse_rotation + '.input2Z', -1)

            cmds.connectAttr(cheek_ctrl + '.translate', reverse_trans + '.input1')
            cmds.connectAttr(reverse_trans + '.output', cheek_jnt + '.translate')
            cmds.connectAttr(cheek_ctrl + '.rotate', reverse_rotation + '.input1')
            cmds.connectAttr(reverse_rotation + '.output', cheek_jnt + '.rotate')

            rt_utils.connect_attr_scale(cheek_ctrl, cheek_jnt)

        return parent_driver

    def mdl_connect_attr(self, name, prefix, name_expression, side, input1, input2):
        connect_drv_mdl = cmds.createNode('multDoubleLinear', n=rt_utils.prefix_name(
            name) + prefix + name_expression + 'Ctrl' + side + '_mdl')
        cmds.connectAttr(input1, connect_drv_mdl + '.input1')
        cmds.connectAttr(input2, connect_drv_mdl + '.input2')

        return connect_drv_mdl

    def mdl_set_attr(self, name, prefix, name_expression, side, input1, input2Set):
        corner_lip_range_mdl = cmds.createNode('multDoubleLinear', n=rt_utils.prefix_name(
            name) + prefix + name_expression + 'Ctrl' + side + '_mdl')
        cmds.connectAttr(input1, corner_lip_range_mdl + '.input1')
        cmds.setAttr(corner_lip_range_mdl + '.input2', input2Set)

        return corner_lip_range_mdl

    def mult_or_div_connect_attr(self, name, prefix, name_expression, side, input2X, input1X, operation=2):
        ctrl_drv_mdn = cmds.createNode('multiplyDivide',
                                       n=rt_utils.prefix_name(name) + prefix + name_expression + 'Ctrl' + side + '_mdn')
        cmds.setAttr(ctrl_drv_mdn + '.operation', operation)
        cmds.connectAttr(input1X, ctrl_drv_mdn + '.input1X')
        cmds.connectAttr(input2X, ctrl_drv_mdn + '.input2X')

        return ctrl_drv_mdn

    def mult_or_div_set_attr(self, name, prefix, name_expression, side, input2XSet, input1X, operation=2):
        ctrl_drv_mdn = cmds.createNode('multiplyDivide',
                                       n=rt_utils.prefix_name(name) + prefix + name_expression + 'Ctrl' + side + '_mdn')
        cmds.setAttr(ctrl_drv_mdn + '.operation', operation)
        cmds.connectAttr(input1X, ctrl_drv_mdn + '.input1X')
        cmds.setAttr(ctrl_drv_mdn + '.input2X', input2XSet)

        return ctrl_drv_mdn

    def pma_expr(self, name, prefix, name_expression, side, operation, input0, input1):
        ctrlDrvPMA = cmds.createNode('plusMinusAverage', n=rt_utils.prefix_name(name)
                                                           + prefix + name_expression + 'Grp' + side + '_pma')
        cmds.setAttr(ctrlDrvPMA + '.operation', operation)
        cmds.connectAttr(input0, ctrlDrvPMA + '.input1D[0]')
        cmds.connectAttr(input1, ctrlDrvPMA + '.input1D[1]')

        return ctrlDrvPMA

    def reverse_node(self, object, target_jnt, object_prefix, side):

        transMdn = cmds.createNode('multiplyDivide', n=rt_utils.prefix_name(object_prefix) + 'Trans' + side + '_mdn')
        cmds.connectAttr(object + '.translate', transMdn + '.input1')
        cmds.setAttr(transMdn + '.input2X', -1)
        cmds.connectAttr(transMdn + '.output', target_jnt + '.translate')

        rotMdn = cmds.createNode('multiplyDivide', n=rt_utils.prefix_name(object_prefix) + 'Rot' + side + '_mdn')
        cmds.connectAttr(object + '.rotate', rotMdn + '.input1')
        cmds.setAttr(rotMdn + '.input2Y', -1)
        cmds.setAttr(rotMdn + '.input2Z', -1)
        cmds.connectAttr(rotMdn + '.output', target_jnt + '.rotate')
