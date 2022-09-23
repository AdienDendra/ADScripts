from __future__ import absolute_import

import maya.cmds as cmds

from rigging.library.utils import controller as rlu_controller, transform as rlu_transform
from rigging.tools import utils as rt_utils


class Build:
    def __init__(self,
                 brow_tweak_jnt,
                 brow_in_jnt,
                 brow_mid_jnt,
                 brow_out_jnt,
                 brow_tip_jnt,
                 brow_tw_prefix,
                 brow_in_prefix,
                 brow_mid_prefix,
                 brow_out_prefix,
                 brows_prefix,
                 brow_tip_prefix,
                 scale,
                 side_RGT,
                 side_LFT,
                 side,
                 brow_in_rotation_grp_offset,
                 brow_mid_rotation_grp_offset,
                 brow_out_rotate_grp_offset,
                 brow_tip_rotate_grp_offset,
                 suffix_controller
                 ):
        # create group brow
        self.brow_all_ctrl_grp = cmds.group(em=1, n='browAllCtrl' + side + '_grp')

        # check position
        position_brow_mid = cmds.xform(brow_mid_jnt, ws=1, q=1, t=1)[0]

        brow_tweak_ctrl = rlu_controller.Control(match_obj_first_position=brow_tweak_jnt,
                                                 prefix=brow_tw_prefix,
                                                 shape=rlu_controller.ARROW4STRAIGHT, groups_ctrl=[''],
                                                 ctrl_size=scale * 0.03, suffix=suffix_controller,
                                                 ctrl_color='red', lock_channels=['v'],
                                                 side=side)

        brow_in_ctrl = rlu_controller.Control(match_obj_first_position=brow_in_jnt,
                                              prefix=brow_in_prefix,
                                              shape=rlu_controller.CUBE, groups_ctrl=[''],
                                              ctrl_size=scale * 0.05, suffix=suffix_controller,
                                              ctrl_color='blue', lock_channels=['v'],
                                              side=side)

        brow_mid_ctrl = rlu_controller.Control(match_obj_first_position=brow_mid_jnt,
                                               prefix=brow_mid_prefix,
                                               shape=rlu_controller.CUBE, groups_ctrl=['', 'Offset'],
                                               ctrl_size=scale * 0.05, suffix=suffix_controller,
                                               ctrl_color='blue', lock_channels=['v'], side=side)

        brow_out_ctrl = rlu_controller.Control(match_obj_first_position=brow_out_jnt,
                                               prefix=brow_out_prefix,
                                               shape=rlu_controller.CUBE, groups_ctrl=[''],
                                               ctrl_size=scale * 0.05, suffix=suffix_controller,
                                               ctrl_color='blue', lock_channels=['v'], side=side)

        brow_tip_ctrl = rlu_controller.Control(match_obj_first_position=brow_tip_jnt,
                                               prefix=brow_tip_prefix,
                                               shape=rlu_controller.CUBE, groups_ctrl=[''],
                                               ctrl_size=scale * 0.05, suffix=suffix_controller,
                                               ctrl_color='blue', lock_channels=['v'], side=side)

        brow_main_ctrl = rlu_controller.Control(match_obj_first_position=brow_in_jnt,
                                                match_obj_second_position=brow_out_jnt,
                                                prefix=brows_prefix,
                                                shape=rlu_controller.SQUAREPLUS, groups_ctrl=[''],
                                                ctrl_size=scale * 0.1, suffix=suffix_controller,
                                                ctrl_color='yellow', lock_channels=['v'], side=side)

        # ==================================================================================================================
        #                                            ASSIGNING THE INSTANCE NAME
        # ==================================================================================================================
        self.brow_tweak_ctrl = brow_tweak_ctrl.control
        self.brow_tweak_ctrl_grp = brow_tweak_ctrl.parent_control[0]

        self.brow_in_ctrl = brow_in_ctrl.control
        self.brow_in_ctrl_grp = brow_in_ctrl.parent_control[0]

        self.brow_mid_ctrl = brow_mid_ctrl.control
        self.brow_mid_ctrl_grp = brow_mid_ctrl.parent_control[0]
        self.brow_mid_ctrl_grp_offset = brow_mid_ctrl.parent_control[1]

        self.brow_out_ctrl = brow_out_ctrl.control
        self.brow_out_ctrl_grp = brow_out_ctrl.parent_control[0]

        self.brow_tip_ctrl = brow_tip_ctrl.control
        self.brow_tip_ctrl_grp = brow_tip_ctrl.parent_control[0]

        self.brow_ctrl = brow_main_ctrl.control
        self.brow_ctrl_grp = brow_main_ctrl.parent_control[0]

        # ==================================================================================================================
        #                                           EYEBROW CONTROLLER SETUP
        # ==================================================================================================================
        cmds.parent(self.brow_tweak_ctrl_grp, self.brow_in_ctrl)
        cmds.parent(self.brow_in_ctrl_grp, self.brow_mid_ctrl_grp, self.brow_out_ctrl_grp, self.brow_tip_ctrl_grp,
                    self.brow_ctrl)

        # GROUPING FOR OFFSET
        self.brow_in_center_ctrl_grp = cmds.group(em=1, n='browInCtrlCenter' + side + '_grp')
        self.brow_in_center_ctrl_grp_offset = cmds.group(em=1, n='browInCtrlOffsetCenter' + side + '_grp')
        cmds.parent(self.brow_in_center_ctrl_grp_offset, self.brow_in_center_ctrl_grp)

        self.brow_mid_center_ctrl_grp = cmds.group(em=1, n='browMidCtrlCenter' + side + '_grp')
        self.brow_mid_center_ctrl_grp_offset = cmds.group(em=1, n='browMidCtrlOffsetCenter' + side + '_grp')
        cmds.parent(self.brow_mid_center_ctrl_grp_offset, self.brow_mid_center_ctrl_grp)

        self.brow_out_center_ctrl_grp = cmds.group(em=1, n='browOutCtrlCenter' + side + '_grp')
        self.brow_out_center_ctrl_grp_offset = cmds.group(em=1, n='browOutCtrlOffsetCenter' + side + '_grp')
        cmds.parent(self.brow_out_center_ctrl_grp_offset, self.brow_out_center_ctrl_grp)

        self.brow_tip_center_ctrl_grp = cmds.group(em=1, n='browTipCtrlCenter' + side + '_grp')
        self.brow_tip_center_ctrl_grp_offset = cmds.group(em=1, n='browTipCtrlOffsetCenter' + side + '_grp')
        cmds.parent(self.brow_tip_center_ctrl_grp_offset, self.brow_tip_center_ctrl_grp)

        # CREATE GROUP CORESPONDENT THE JOINTS
        brow_tweak_jnt_grp = rlu_transform.create_parent_transform(parent_list=[''], object=brow_tweak_jnt,
                                                                   match_position=brow_tweak_jnt, prefix=brow_tw_prefix,
                                                                   suffix='_jnt', side=side)
        brow_in_jnt_grp = rlu_transform.create_parent_transform(parent_list=['', 'Offset'], object=brow_in_jnt,
                                                                match_position=brow_in_jnt, prefix=brow_in_prefix,
                                                                suffix='_jnt',
                                                                side=side)
        brow_mid_jnt_grp = rlu_transform.create_parent_transform(parent_list=['', 'Offset', 'Avg'], object=brow_mid_jnt,
                                                                 match_position=brow_mid_jnt, prefix=brow_mid_prefix,
                                                                 suffix='_jnt', side=side)
        brow_out_jnt_grp = rlu_transform.create_parent_transform(parent_list=['', 'Offset'], object=brow_out_jnt,
                                                                 match_position=brow_out_jnt, prefix=brow_out_prefix,
                                                                 suffix='_jnt', side=side)
        brow_tip_jnt_grp = rlu_transform.create_parent_transform(parent_list=['', 'Offset'], object=brow_tip_jnt,
                                                                 match_position=brow_tip_jnt, prefix=brow_tip_prefix,
                                                                 suffix='_jnt', side=side)

        # EYBROW MAIN OFFSET GRP JOINT TRANSFORM
        brow_in_main_grp = self.main_group_connection(name=brow_in_prefix, side=side, object_parent=brow_in_jnt_grp[0])
        brow_mid_main_grp = self.main_group_connection(name=brow_mid_prefix, side=side,
                                                       object_parent=brow_mid_jnt_grp[0])
        brow_out_main_grp = self.main_group_connection(name=brow_out_prefix, side=side,
                                                       object_parent=brow_out_jnt_grp[0])
        browTipMain = self.main_group_connection(name=brow_tip_prefix, side=side, object_parent=brow_tip_jnt_grp[0])

        # SHIFTING PARENT JOINT TO MAIN OFFSET GRP EYEBROW
        cmds.parent(brow_in_jnt_grp[1], brow_in_main_grp)
        cmds.parent(brow_mid_jnt_grp[1], brow_mid_main_grp)
        cmds.parent(brow_out_jnt_grp[1], brow_out_main_grp)
        cmds.parent(brow_tip_jnt_grp[1], browTipMain)

        # EYEBROW EXCEPTION PARENTING CTRL
        cmds.delete(cmds.pointConstraint(self.brow_ctrl, self.brow_in_center_ctrl_grp))
        cmds.delete(cmds.pointConstraint(self.brow_ctrl, self.brow_mid_center_ctrl_grp))
        cmds.delete(cmds.pointConstraint(self.brow_ctrl, self.brow_out_center_ctrl_grp))
        cmds.delete(cmds.pointConstraint(self.brow_ctrl, self.brow_tip_center_ctrl_grp))

        # FLIPPING THE CONTROLLER
        if position_brow_mid < 0:
            cmds.setAttr(self.brow_in_ctrl_grp + '.scaleX', -1)
            cmds.setAttr(self.brow_mid_ctrl_grp + '.scaleX', -1)
            cmds.setAttr(self.brow_out_ctrl_grp + '.scaleX', -1)
            cmds.setAttr(self.brow_tip_ctrl_grp + '.scaleX', -1)

            # mc.setAttr(self.browCtrlGrp + '.scaleX', -1)

            cmds.setAttr(self.brow_in_ctrl_grp + '.rotateY', brow_in_rotation_grp_offset * -1)
            cmds.setAttr(self.brow_mid_ctrl_grp + '.rotateY', brow_mid_rotation_grp_offset * -1)
            cmds.setAttr(self.brow_out_ctrl_grp + '.rotateY', brow_out_rotate_grp_offset * -1)
            cmds.setAttr(self.brow_tip_ctrl_grp + '.rotateY', brow_tip_rotate_grp_offset * -1)

            cmds.setAttr(brow_in_jnt_grp[1] + '.rotateY', brow_in_rotation_grp_offset * -1)
            cmds.setAttr(brow_mid_jnt_grp[1] + '.rotateY', brow_mid_rotation_grp_offset * -1)
            cmds.setAttr(brow_out_jnt_grp[1] + '.rotateY', brow_out_rotate_grp_offset * -1)
            cmds.setAttr(brow_tip_jnt_grp[1] + '.rotateY', brow_tip_rotate_grp_offset * -1)

            self.reverse_node(self.brow_tweak_ctrl, brow_tweak_jnt, side_RGT, side_LFT, side)
            self.reverse_node(self.brow_in_ctrl, brow_in_jnt, side_RGT, side_LFT, side)
            self.reverse_node(self.brow_mid_ctrl, brow_mid_jnt, side_RGT, side_LFT, side)
            self.reverse_node(self.brow_out_ctrl, brow_out_jnt, side_RGT, side_LFT, side)
            self.reverse_node(self.brow_tip_ctrl, brow_tip_jnt, side_RGT, side_LFT, side)

            self.reverse_node(self.brow_ctrl, brow_in_main_grp, side_RGT, side_LFT, side)
            self.reverse_node(self.brow_ctrl, brow_mid_main_grp, side_RGT, side_LFT, side)
            self.reverse_node(self.brow_ctrl, brow_out_main_grp, side_RGT, side_LFT, side)
            # self.reverseNode(self.browCtrl, browTipMain, sideRGT, sideLFT, side)

            rt_utils.connect_attr_scale(self.brow_tweak_ctrl, brow_tweak_jnt)
            rt_utils.connect_attr_scale(self.brow_in_ctrl, brow_in_jnt)
            rt_utils.connect_attr_scale(self.brow_mid_ctrl, brow_mid_jnt)
            rt_utils.connect_attr_scale(self.brow_out_ctrl, brow_out_jnt)
            rt_utils.connect_attr_scale(self.brow_tip_ctrl, brow_tip_jnt)

            rt_utils.connect_attr_scale(self.brow_ctrl, brow_in_main_grp)
            rt_utils.connect_attr_scale(self.brow_ctrl, brow_mid_main_grp)
            rt_utils.connect_attr_scale(self.brow_ctrl, brow_out_main_grp)
            # au.connectAttrScale(self.browCtrl, browTipMain)

            # connect attr
            self.reverse_node(self.brow_ctrl, self.brow_in_center_ctrl_grp_offset, side_RGT, side_LFT, side)
            self.reverse_node(self.brow_ctrl, self.brow_mid_center_ctrl_grp_offset, side_RGT, side_LFT, side)
            self.reverse_node(self.brow_ctrl, self.brow_out_center_ctrl_grp_offset, side_RGT, side_LFT, side)
            # self.reverseNode(self.browCtrl, self.ctrlOffsetGrpBrowTipCenter, sideRGT, sideLFT, side)

        else:
            cmds.setAttr(self.brow_in_ctrl_grp + '.rotateY', brow_in_rotation_grp_offset)
            cmds.setAttr(self.brow_mid_ctrl_grp + '.rotateY', brow_mid_rotation_grp_offset)
            cmds.setAttr(self.brow_out_ctrl_grp + '.rotateY', brow_out_rotate_grp_offset)
            cmds.setAttr(self.brow_tip_ctrl_grp + '.rotateY', brow_tip_rotate_grp_offset)

            cmds.setAttr(brow_in_jnt_grp[1] + '.rotateY', brow_in_rotation_grp_offset)
            cmds.setAttr(brow_mid_jnt_grp[1] + '.rotateY', brow_mid_rotation_grp_offset)
            cmds.setAttr(brow_out_jnt_grp[1] + '.rotateY', brow_out_rotate_grp_offset)
            cmds.setAttr(brow_tip_jnt_grp[1] + '.rotateY', brow_tip_rotate_grp_offset)

            rt_utils.connect_attr_object(self.brow_tweak_ctrl, brow_tweak_jnt)
            rt_utils.connect_attr_object(self.brow_in_ctrl, brow_in_jnt)
            rt_utils.connect_attr_object(self.brow_mid_ctrl, brow_mid_jnt)
            rt_utils.connect_attr_object(self.brow_out_ctrl, brow_out_jnt)
            rt_utils.connect_attr_object(self.brow_tip_ctrl, brow_tip_jnt)

            rt_utils.connect_attr_object(self.brow_ctrl, brow_in_main_grp)
            rt_utils.connect_attr_object(self.brow_ctrl, brow_mid_main_grp)
            rt_utils.connect_attr_object(self.brow_ctrl, brow_out_main_grp)
            # au.connectAttrObject(self.browCtrl, browTipMain)

            rt_utils.connect_attr_object(self.brow_ctrl, self.brow_in_center_ctrl_grp_offset)
            rt_utils.connect_attr_object(self.brow_ctrl, self.brow_mid_center_ctrl_grp_offset)
            rt_utils.connect_attr_object(self.brow_ctrl, self.brow_out_center_ctrl_grp_offset)
            # au.connectAttrObject(self.browCtrl, self.ctrlOffsetGrpBrowTipCenter)

        # regrouping to offset grp
        cmds.parent(self.brow_in_ctrl_grp, self.brow_in_center_ctrl_grp_offset)
        cmds.parent(self.brow_mid_ctrl_grp, self.brow_mid_center_ctrl_grp_offset)
        cmds.parent(self.brow_out_ctrl_grp, self.brow_out_center_ctrl_grp_offset)
        cmds.parent(self.brow_tip_ctrl_grp, self.brow_tip_center_ctrl_grp_offset)

        #
        if position_brow_mid < 0:
            cmds.setAttr(self.brow_ctrl_grp + '.scaleX', -1)

        self.brow_mid_jnt_grp = brow_mid_jnt_grp

        # ADD ATTRIBUTE BROW IN
        rt_utils.add_attribute(objects=[self.brow_in_ctrl], long_name=['weightSkinInfluence'], nice_name=[' '],
                               at="enum",
                               en='%s%s' % ('Weight ', 'Influence'), channel_box=True)

        self.brow_center_in_attr = rt_utils.add_attribute(objects=[self.brow_in_ctrl], long_name=['browCenter'],
                                                          attributeType="float", min=0, dv=1, keyable=True)
        self.brow_mid_in_attr = rt_utils.add_attribute(objects=[self.brow_in_ctrl], long_name=['browMid'],
                                                       attributeType="float", min=0, dv=1, keyable=True)

        # ADD ATTRIBUTE BROW OUT
        rt_utils.add_attribute(objects=[self.brow_out_ctrl], long_name=['weightSkinInfluence'], nice_name=[' '],
                               at="enum",
                               en='%s%s' % ('Weight ', 'Influence'), channel_box=True)

        self.brow_mid_out_attr = rt_utils.add_attribute(objects=[self.brow_out_ctrl], long_name=['browMid'],
                                                        attributeType="float", min=0, dv=1, keyable=True)

        # PARENT TO THE GROUP
        cmds.parent(self.brow_in_center_ctrl_grp, self.brow_mid_center_ctrl_grp, self.brow_out_center_ctrl_grp,
                    self.brow_tip_center_ctrl_grp, self.brow_ctrl_grp,
                    self.brow_all_ctrl_grp)

    def reverse_node(self, object, target_jnt, side_RGT, side_LFT, side, input_trans2X=-1, input_trans2Y=1,
                     input_trans2Z=1,
                     input_rotate2X=1, input_rotate2Y=-1, input_rotate2Z=-1):
        if side_RGT in target_jnt:
            newName = target_jnt.replace(side_RGT, '')
        elif side_LFT in target_jnt:
            newName = target_jnt.replace(side_LFT, '')
        else:
            newName = target_jnt

        translation_mdn = cmds.createNode('multiplyDivide', n=rt_utils.prefix_name(newName) + 'Trans' + side + '_mdn')
        cmds.connectAttr(object + '.translate', translation_mdn + '.input1')
        cmds.setAttr(translation_mdn + '.input2X', input_trans2X)
        cmds.setAttr(translation_mdn + '.input2Y', input_trans2Y)
        cmds.setAttr(translation_mdn + '.input2Z', input_trans2Z)

        cmds.connectAttr(translation_mdn + '.output', target_jnt + '.translate')

        rotation_mdn = cmds.createNode('multiplyDivide', n=rt_utils.prefix_name(newName) + 'Rot' + side + '_mdn')
        cmds.connectAttr(object + '.rotate', rotation_mdn + '.input1')
        cmds.setAttr(rotation_mdn + '.input2X', input_rotate2X)
        cmds.setAttr(rotation_mdn + '.input2Y', input_rotate2Y)
        cmds.setAttr(rotation_mdn + '.input2Z', input_rotate2Z)
        cmds.connectAttr(rotation_mdn + '.output', target_jnt + '.rotate')

    def main_group_connection(self, name, side, object_parent):
        # BROW MAIN OFFSET GRP JOINT TRANSFORM
        eyebrow_main_bind_grp = cmds.group(em=1, n=name + 'Main' + side + '_grp')
        eyebrow_main_bind_offset = cmds.group(em=1, n=name + 'MainOffset' + side + '_grp', p=eyebrow_main_bind_grp)
        cmds.delete(cmds.parentConstraint(self.brow_ctrl, eyebrow_main_bind_grp))

        cmds.parent(eyebrow_main_bind_grp, object_parent)

        return eyebrow_main_bind_offset
