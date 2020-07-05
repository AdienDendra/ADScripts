import re
from __builtin__ import reload
from string import digits

import maya.cmds as mc

from rigging.library.utils import controller as ct, transform as tf
from rigging.tools import AD_utils as au

reload(ct)
reload(au)
reload(tf)


class Build:
    def __init__(self,
                 lid01_up, lid01_low,
                 lid05_up, lid05_low,
                 lid_up_joint_bind01_grp_offset,
                 lid_low_joint_bind01_grp_offset,
                 lid_up_joint_bind05_grp_offset,
                 lid_low_joint_bind05_grp_offset,
                 scale,
                 side_RGT,
                 side_LFT,
                 lid_up_ctrl_bind01_grp_zro,
                 lid_low_ctrl_bind01_grp_zro,
                 lid_up_ctrl_bind05_grp_zro,
                 lid_low_ctrl_bind05_grp_zro,
                 prefix_name_in,
                 prefix_name_out,
                 side,
                 ctrl_shape,
                 ctrl_color,
                 suffix_controller,
                 lid_out=False):

        # ==================================================================================================================
        #                                                  CORNER CONTROLLER
        # ==================================================================================================================
        # controller in corner
        lid_corner_in_ctrl = self.lid_corner_ctrl(match_pos_one=lid01_up,
                                                  match_pos_two=lid01_low,
                                                  prefix=prefix_name_in,
                                                  scale=scale,
                                                  side=side,
                                                  ctrl_shape=ctrl_shape,
                                                  ctrl_color=ctrl_color,
                                                  add_attr=lid_out,
                                                  suffix_controller=suffix_controller)

        # controller in corner
        lid_corner_out_ctrl = self.lid_corner_ctrl(match_pos_one=lid05_up,
                                                   match_pos_two=lid05_low,
                                                   prefix=prefix_name_out,
                                                   scale=scale,
                                                   side=side,
                                                   ctrl_shape=ctrl_shape,
                                                   ctrl_color=ctrl_color,
                                                   add_attr=lid_out,
                                                   suffix_controller=suffix_controller)

        self.lid_in_grp = lid_corner_in_ctrl[1]
        self.lid_out_grp = lid_corner_out_ctrl[1]
        self.lid_in_ctrl = lid_corner_in_ctrl[0]
        self.lid_out_ctrl = lid_corner_out_ctrl[0]

        position_lid_corner_out = mc.xform(lid_corner_out_ctrl[0], ws=1, q=1, t=1)[0]
        if position_lid_corner_out > 0:
            # parent constraint corner grp bind jnt
            au.connect_attr_translate_rotate(lid_corner_in_ctrl[0], lid_up_joint_bind01_grp_offset)
            au.connect_attr_translate_rotate(lid_corner_in_ctrl[0], lid_low_joint_bind01_grp_offset)
            au.connect_attr_translate_rotate(lid_corner_out_ctrl[0], lid_up_joint_bind05_grp_offset)
            au.connect_attr_translate_rotate(lid_corner_out_ctrl[0], lid_low_joint_bind05_grp_offset)
        else:
            self.corner_reverse_node(side_RGT, side_LFT, lidCornerCtrl=lid_corner_out_ctrl[0], side=side,
                                     lidCornerName=prefix_name_out,
                                     targetUp=lid_up_joint_bind05_grp_offset, targetLow=lid_low_joint_bind05_grp_offset)

            self.corner_reverse_node(side_RGT, side_LFT, lidCornerCtrl=lid_corner_in_ctrl[0], side=side,
                                     lidCornerName=prefix_name_in,
                                     targetUp=lid_up_joint_bind01_grp_offset, targetLow=lid_low_joint_bind01_grp_offset)

        # SHOW AND HIDE CONTROLLER CORNER
        if lid_out:
            # ADD ATTRIBUTE FOR LID OUT CONTROLLER
            mc.connectAttr(lid_corner_in_ctrl[0] + '.%s' % lid_corner_in_ctrl[3],
                           lid_up_ctrl_bind01_grp_zro + '.visibility')
            mc.connectAttr(lid_corner_in_ctrl[0] + '.%s' % lid_corner_in_ctrl[3],
                           lid_low_ctrl_bind01_grp_zro + '.visibility')
            mc.connectAttr(lid_corner_out_ctrl[0] + '.%s' % lid_corner_out_ctrl[3],
                           lid_up_ctrl_bind05_grp_zro + '.visibility')
            mc.connectAttr(lid_corner_out_ctrl[0] + '.%s' % lid_corner_out_ctrl[3],
                           lid_low_ctrl_bind05_grp_zro + '.visibility')

        # OFFSET GRP CONTROLLER
        self.lid_corner_in_ctrl_grp_offset = lid_corner_in_ctrl[2]
        self.lid_corner_out_ctrl_grp_offset = lid_corner_out_ctrl[2]
        # ==================================================================================================================
        #                                              PARENT TO GROUP
        # ==================================================================================================================
        mc.parent(lid_up_ctrl_bind01_grp_zro, lid_corner_in_ctrl[0])
        mc.parent(lid_low_ctrl_bind01_grp_zro, lid_corner_in_ctrl[0])
        mc.parent(lid_up_ctrl_bind05_grp_zro, lid_corner_out_ctrl[0])
        mc.parent(lid_low_ctrl_bind05_grp_zro, lid_corner_out_ctrl[0])

    def reorder_number(self, prefix, side_RGT, side_LFT):
        # get the number
        new_prefix = tf.reposition_side(object=prefix, side_RGT=side_RGT, side_LFT=side_LFT)
        try:
            patterns = [r'\d+']
            prefix_number = au.prefix_name(new_prefix)
            for p in patterns:
                prefix_number = re.findall(p, prefix_number)[0]
        except:
            prefix_number = ''

        # get the prefix without number
        prefix_no_number = str(new_prefix).translate(None, digits)

        return prefix_no_number, prefix_number

    def corner_reverse_node(self, sideRGT, sideLFT, lidCornerCtrl, side, lidCornerName='', targetUp='', targetLow=''):
        newName, numberNew = self.reorder_number(prefix=lidCornerName, side_RGT=sideRGT, side_LFT=sideLFT)

        transRev = mc.createNode('multiplyDivide', n=newName + 'Trans' + numberNew + side + '_mdn')
        rotRev = mc.createNode('multiplyDivide', n=newName + 'Rot' + numberNew + side + '_mdn')
        mc.connectAttr(lidCornerCtrl + '.translate', transRev + '.input1')
        mc.setAttr(transRev + '.input2X', -1)

        mc.connectAttr(lidCornerCtrl + '.rotate', rotRev + '.input1')
        mc.setAttr(rotRev + '.input2Y', -1)
        mc.setAttr(rotRev + '.input2Z', -1)

        mc.connectAttr(transRev + '.output', targetUp + '.translate')
        mc.connectAttr(rotRev + '.output', targetUp + '.rotate')
        mc.connectAttr(transRev + '.output', targetLow + '.translate')
        mc.connectAttr(rotRev + '.output', targetLow + '.rotate')

    def lid_corner_ctrl(self, match_pos_one, match_pos_two, prefix, scale, side, ctrl_shape, ctrl_color,
                        suffix_controller,
                        add_attr=False):
        corner_ctrl = ct.Control(match_obj_first_position=match_pos_one, match_obj_second_position=match_pos_two,
                                 prefix=prefix,
                                 shape=ctrl_shape, groups_ctrl=['Zro', 'Offset'],
                                 ctrl_size=scale * 0.07, suffix=suffix_controller,
                                 ctrl_color=ctrl_color, lock_channels=['v', 's'], side=side)

        # check position
        position_corner_ctrl = mc.xform(corner_ctrl.control, ws=1, q=1, t=1)[0]

        # flipping the controller
        if position_corner_ctrl < 0:
            mc.setAttr(corner_ctrl.parent_control[0] + '.scaleX', -1)

        self.control = corner_ctrl.control
        self.lid_corner_ctrl_grp = corner_ctrl.parent_control[0]
        self.lid_corner_ctrl_grp_offset = corner_ctrl.parent_control[1]

        # ADD ATTRIBUTE
        if add_attr:
            self.show_detail_ctrl = au.add_attribute(objects=[corner_ctrl.control], long_name=['showDetailCtrl'],
                                                     attributeType="long", min=0, max=1, dv=0, keyable=True)

            return corner_ctrl.control, corner_ctrl.parent_control[0], corner_ctrl.parent_control[
                1], self.show_detail_ctrl

        else:
            return corner_ctrl.control, corner_ctrl.parent_control[0], corner_ctrl.parent_control[1]
