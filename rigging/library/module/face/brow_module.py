from __builtin__ import reload

import maya.cmds as mc

from rigging.library.base.face import brow as br
from rigging.library.utils import controller as ct
from rigging.library.utils import transform as tf
from rigging.tools import AD_utils as au

reload (ct)
reload (tf)
reload (au)
reload (br)

class Brows:
    def __init__(self,
                 brow_tweak_jnt_LFT,
                 brow_in_jnt_LFT,
                 brow_mid_jnt_LFT,
                 brow_out_jnt_LFT,
                 brow_tip_jnt_LFT,
                 brow_tweak_jnt_RGT,
                 brow_in_jnt_RGT,
                 brow_mid_jnt_RGT,
                 brow_out_jnt_RGT,
                 brow_tip_jnt_RGT,
                 brow_tweak_skin_LFT,
                 brow_in_skin_LFT,
                 brow_mid_skin_LFT,
                 brow_out_skin_LFT,
                 brow_tip_skin_LFT,
                 brow_tweak_skin_RGT,
                 brow_in_skin_RGT,
                 brow_mid_skin_RGT,
                 brow_out_skin_RGT,
                 brow_tip_skin_RGT,
                 brow_center_jnt,
                 brow_tweak_prefix,
                 brow_in_prefix,
                 brow_mid_prefix,
                 brow_out_prefix,
                 brows_prefix,
                 brow_tip_prefix,
                 brow_center_prefix,
                 scale,
                 side_RGT,
                 side_LFT,
                 brow_in_rotate_grp_offset,
                 brow_mid_rotate_grp_offset,
                 brow_out_rotate_grp_offset,
                 brow_tip_rotate_grp_offset,
                 head_up_ctrl_gimbal,
                 suffix_controller
                 ):

        ctrl_driver_grp = mc.group(em=1, n='browCtrlAll' + '_grp')
        mc.parent(ctrl_driver_grp, head_up_ctrl_gimbal)
        self.brow_all_ctrl = ctrl_driver_grp

        # ==================================================================================================================
        #                                               BROWS CONTROLLER
        # ==================================================================================================================

        left_brow = br.Build(brow_tweak_jnt=brow_tweak_jnt_LFT,
                             brow_in_jnt=brow_in_jnt_LFT,
                             brow_mid_jnt=brow_mid_jnt_LFT,
                             brow_out_jnt=brow_out_jnt_LFT,
                             brow_tip_jnt=brow_tip_jnt_LFT,
                             brow_tweak_skin=brow_tweak_skin_LFT,
                             brow_in_skin=brow_in_skin_LFT,
                             brow_mid_skin=brow_mid_skin_LFT,
                             brow_out_skin=brow_out_skin_LFT,
                             brow_tip_skin=brow_tip_skin_LFT,
                             brow_tw_prefix=brow_tweak_prefix,
                             brow_in_prefix=brow_in_prefix,
                             brow_mid_prefix=brow_mid_prefix,
                             brow_out_prefix=brow_out_prefix,
                             brows_prefix=brows_prefix,
                             brow_tip_prefix=brow_tip_prefix,
                             scale=scale,
                             side_RGT=side_RGT,
                             side_LFT=side_LFT,
                             side=side_LFT,
                             brow_in_rotation_grp_offset=brow_in_rotate_grp_offset,
                             brow_mid_rotation_grp_offset=brow_mid_rotate_grp_offset,
                             brow_out_rotate_grp_offset=brow_out_rotate_grp_offset,
                             brow_tip_rotate_grp_offset=brow_tip_rotate_grp_offset,
                             suffix_controller=suffix_controller)

        right_brow = br.Build(brow_tweak_jnt=brow_tweak_jnt_RGT,
                              brow_in_jnt=brow_in_jnt_RGT,
                              brow_mid_jnt=brow_mid_jnt_RGT,
                              brow_out_jnt=brow_out_jnt_RGT,
                              brow_tip_jnt=brow_tip_jnt_RGT,
                              brow_tweak_skin=brow_tweak_skin_RGT,
                              brow_in_skin=brow_in_skin_RGT,
                              brow_mid_skin=brow_mid_skin_RGT,
                              brow_out_skin=brow_out_skin_RGT,
                              brow_tip_skin=brow_tip_skin_RGT,
                              brow_tw_prefix=brow_tweak_prefix,
                              brow_in_prefix=brow_in_prefix,
                              brow_mid_prefix=brow_mid_prefix,
                              brow_out_prefix=brow_out_prefix,
                              brows_prefix=brows_prefix,
                              brow_tip_prefix=brow_tip_prefix,
                              scale=scale,
                              side_RGT=side_RGT,
                              side_LFT=side_LFT,
                              side=side_RGT,
                              brow_in_rotation_grp_offset=brow_in_rotate_grp_offset,
                              brow_mid_rotation_grp_offset=brow_mid_rotate_grp_offset,
                              brow_out_rotate_grp_offset=brow_out_rotate_grp_offset,
                              brow_tip_rotate_grp_offset=brow_tip_rotate_grp_offset,
                              suffix_controller=suffix_controller)

        center_brow_ctrl = ct.Control(match_obj_first_position=brow_center_jnt,
                                      prefix=brow_center_prefix,
                                      shape=ct.JOINT, groups_ctrl=['', 'Offset'],
                                      ctrl_size=scale * 0.07, suffix=suffix_controller,
                                      ctrl_color='blue', lock_channels=['v'],
                                      )

        brow_center_grp = tf.create_parent_transform(parent_list=['', 'Offset'], object=brow_center_jnt,
                                                     match_position=brow_center_jnt,
                                                     prefix=brow_center_prefix, suffix='_jnt')

        au.connect_attr_object(center_brow_ctrl.control, brow_center_jnt)

        # ==============================================================================================================
        #                                               BROWS CENTER SETUP
        # ==============================================================================================================

        brow_sum_node = self.sum(target_jnt=brow_center_grp[1] + '.translateY', side_RGT=side_RGT, side_LFT=side_LFT)

        brow_in_sum_node = self.sum(target_jnt=brow_sum_node + '.input1D[2]', side_RGT=side_RGT, side_LFT=side_LFT)

        self.divided_two_items(brow_first_ctrl=left_brow.brow_ctrl, brow_second_ctrl=right_brow.brow_ctrl,
                               target_sum0=brow_sum_node + '.input1D[0]',
                               target_sum1=brow_sum_node + '.input1D[1]',
                               side_RGT=side_RGT, side_LFT=side_LFT, side_object_one=side_LFT, side_object_two=side_RGT,
                               add_prefix_first='StCtr',
                               add_prefix_second='NdCtr')

        self.divided_two_items(brow_first_ctrl=left_brow.brow_in_ctrl, brow_second_ctrl=right_brow.brow_in_ctrl,
                               target_sum0=brow_in_sum_node + '.input1D[0]',
                               target_sum1=brow_in_sum_node + '.input1D[1]',
                               side_RGT=side_RGT, side_LFT=side_LFT, side_object_one=side_LFT, side_object_two=side_RGT,
                               object_second_one=left_brow.brow_in_ctrl, attr_second_one=left_brow.brow_center_in_attr,
                               object_second_two=right_brow.brow_in_ctrl,
                               attr_second_two=right_brow.brow_center_in_attr,
                               add_attr=True,
                               add_prefix_first='StIn',
                               add_prefix_second='NdIn')

        mc.connectAttr(brow_center_grp[1] + '.translateY', center_brow_ctrl.parent_control[1] + '.translateY')

        # ==============================================================================================================
        #                                               BROWS SETUP
        # ==============================================================================================================

        brow_LFT_sum = self.sum(target_jnt=left_brow.brow_mid_jnt_grp[2] + '.translateY', side_RGT=side_RGT,
                                side_LFT=side_LFT, side=side_LFT)
        self.divided_two_items(brow_first_ctrl=left_brow.brow_in_ctrl, brow_second_ctrl=left_brow.brow_out_ctrl,
                               target_sum0=brow_LFT_sum + '.input1D[0]',
                               target_sum1=brow_LFT_sum + '.input1D[1]', side_RGT=side_RGT, side_LFT=side_LFT,
                               side_object_one=side_LFT, side_object_two=side_LFT,
                               object_second_one=left_brow.brow_in_ctrl, attr_second_one=left_brow.brow_mid_in_attr,
                               object_second_two=left_brow.brow_out_ctrl, attr_second_two=left_brow.brow_mid_out_attr,
                               add_attr=True,
                               add_prefix_first='StInOut',
                               add_prefix_second='NdInOut')

        mc.connectAttr(left_brow.brow_mid_jnt_grp[2] + '.translateY',
                       left_brow.brow_mid_ctrl_grp_offset + '.translateY')

        brow_RGT_sum = self.sum(target_jnt=right_brow.brow_mid_jnt_grp[2] + '.translateY', side_RGT=side_RGT,
                                side_LFT=side_LFT, side=side_RGT)
        self.divided_two_items(brow_first_ctrl=right_brow.brow_in_ctrl, brow_second_ctrl=right_brow.brow_out_ctrl,
                               target_sum0=brow_RGT_sum + '.input1D[0]',
                               target_sum1=brow_RGT_sum + '.input1D[1]', side_RGT=side_RGT, side_LFT=side_LFT,
                               side_object_one=side_RGT, side_object_two=side_RGT,
                               object_second_one=right_brow.brow_in_ctrl, attr_second_one=right_brow.brow_mid_in_attr,
                               object_second_two=right_brow.brow_out_ctrl, attr_second_two=right_brow.brow_mid_out_attr,
                               add_attr=True,
                               add_prefix_first='StInOut',
                               add_prefix_second='NdInOut')

        mc.connectAttr(right_brow.brow_mid_jnt_grp[2] + '.translateY',
                       right_brow.brow_mid_ctrl_grp_offset + '.translateY')

        # PARENT TO THE GROUP
        mc.parent(center_brow_ctrl.parent_control[0], left_brow.brow_all_ctrl_grp, right_brow.brow_all_ctrl_grp,
                  ctrl_driver_grp)

    def divided_two_items(self, brow_first_ctrl, brow_second_ctrl, target_sum0, target_sum1, side_RGT, side_LFT,
                          side_object_one, side_object_two, object_second_one='', attr_second_one='',
                          object_second_two='',
                          attr_second_two='', add_attr=False, add_prefix_first='',
                          add_prefix_second=''):
        if add_attr:
            item_first_divide = self.divide(object=brow_first_ctrl, side_RGT=side_RGT, side_LFT=side_LFT,
                                            side=side_object_one, target=False, add_prefix=add_prefix_first)
            item_second_divide = self.divide(object=brow_second_ctrl, side_RGT=side_RGT, side_LFT=side_LFT,
                                             side=side_object_two, target=False, add_prefix=add_prefix_second)
            self.multiply(object_first=item_first_divide, object_second=object_second_one, target=target_sum0,
                          side_RGT=side_RGT, side_LFT=side_LFT,
                          side=side_object_one, attr_first='outputY', attr_second=attr_second_one,
                          add_prefix=add_prefix_first)

            self.multiply(object_first=item_second_divide, object_second=object_second_two, target=target_sum1,
                          side_RGT=side_RGT, side_LFT=side_LFT,
                          side=side_object_two, attr_first='outputY', attr_second=attr_second_two,
                          add_prefix=add_prefix_second)

        else:
            item_first_divide = self.divide(object=brow_first_ctrl, target_sum=target_sum0, side_RGT=side_RGT,
                                            side_LFT=side_LFT,
                                            side=side_object_one, add_prefix=add_prefix_first)
            item_second_divide = self.divide(object=brow_second_ctrl, target_sum=target_sum1, side_RGT=side_RGT,
                                             side_LFT=side_LFT,
                                             side=side_object_two, add_prefix=add_prefix_second)

    def divide(self, object, side_RGT, side_LFT, side, add_prefix, input_trans2Y=2, target_sum='', target=True):
        if side_RGT in object:
            new_name = object.replace(side_RGT, '')
        elif side_LFT in object:
            new_name = object.replace(side_LFT, '')
        else:
            new_name = object

        div_node = mc.createNode('multiplyDivide', n=au.prefix_name(new_name) + 'TyDiv' + add_prefix + side + '_mdn')
        mc.connectAttr(object + '.translateY', div_node + '.input1Y')
        mc.setAttr(div_node + '.operation', 2)
        mc.setAttr(div_node + '.input2Y', input_trans2Y)
        if target:
            mc.connectAttr(div_node + '.outputY', target_sum)
        else:
            return div_node

    def multiply(self, object_first, object_second, target, side_RGT, side_LFT, side, attr_first, attr_second,
                 add_prefix):
        if side_RGT in object_first:
            newName = object_first.replace(side_RGT, '')
        elif side_LFT in object_first:
            newName = object_first.replace(side_LFT, '')
        else:
            newName = object_first

        div_node = mc.createNode('multiplyDivide', n=au.prefix_name(newName) + 'TyMul' + add_prefix + side + '_mdn')
        mc.connectAttr(object_first + '.%s' % attr_first, div_node + '.input1Y')
        mc.connectAttr(object_second + '.%s' % attr_second, div_node + '.input2Y')

        mc.connectAttr(div_node + '.outputY', target)
        return div_node

    # connectAttr - f
    # noseWeightTransYCtrl_pma.output1D
    # noseWeightJawTransYCtrl_pma.input1D[0];

    def sum(self, target_jnt, side_RGT, side_LFT, side=''):
        if side_RGT in target_jnt:
            newName = target_jnt.replace(side_RGT, '')
        elif side_LFT in target_jnt:
            newName = target_jnt.replace(side_LFT, '')
        else:
            newName = target_jnt

        sum = mc.createNode('plusMinusAverage', n=au.prefix_name(newName) + 'Ty' + side + '_pma')
        mc.connectAttr(sum + '.output1D', target_jnt)

        return sum
