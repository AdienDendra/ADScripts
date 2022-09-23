from __future__ import absolute_import

import maya.cmds as cmds

from rigging.library.utils import controller as rlu_controller
from rigging.tools import utils as rt_utils


class Build:
    def __init__(self,
                 match_pos_one,
                 match_pos_two,
                 prefix,
                 scale,
                 sticky,
                 side,
                 suffix_controller):

        # create controller
        corner_ctrl = rlu_controller.Control(match_obj_first_position=match_pos_one,
                                             match_obj_second_position=match_pos_two,
                                             prefix=prefix, suffix=suffix_controller,
                                             shape=rlu_controller.CIRCLEPLUS, groups_ctrl=['Zro', 'Offset'],
                                             ctrl_size=scale * 0.15,
                                             ctrl_color='blue', lock_channels=['v', 'r', 's'], side=side)

        # check position
        position_corner_controller = cmds.xform(corner_ctrl.control, ws=1, q=1, t=1)[0]

        # ADD ATTRIBUTE
        rt_utils.add_attribute(objects=[corner_ctrl.control], long_name=['offsetPart'], nice_name=[' '], at="enum",
                               en='Offset Part', channel_box=True)
        if sticky:
            self.sticky_ctrl = rt_utils.add_attribute(objects=[corner_ctrl.control], long_name=['stickyLip'],
                                                      attributeType="float", min=0, max=10, dv=0, keyable=True)

        self.jaw_following_ctrl = rt_utils.add_attribute(objects=[corner_ctrl.control], long_name=['jawFollowing'],
                                                         attributeType="float", min=0, max=10, dv=5, keyable=True)

        self.jaw_ud_ctrl = rt_utils.add_attribute(objects=[corner_ctrl.control], long_name=['cornerAdjust'],
                                                  attributeType="float", min=0, max=10, dv=0, keyable=True)

        # ADD ATTRIBUTE CHEEK
        rt_utils.add_attribute(objects=[corner_ctrl.control], long_name=['weightSkinInfluence'], nice_name=[' '],
                               at="enum",
                               en='%s%s%s' % ('Weight ', side, ' Influence'), channel_box=True)

        self.nostril_ctrl = rt_utils.add_attribute(objects=[corner_ctrl.control], long_name=['nostril'],
                                                   attributeType="float", min=0, dv=1, keyable=True)

        self.cheek_mid_ctrl = rt_utils.add_attribute(objects=[corner_ctrl.control], long_name=['cheekMid'],
                                                     attributeType="float", min=0, dv=1, keyable=True)

        self.cheek_low_ctrl = rt_utils.add_attribute(objects=[corner_ctrl.control], long_name=['cheekLow'],
                                                     attributeType="float", min=0, dv=1, keyable=True)

        self.cheek_out_up_ctrl = rt_utils.add_attribute(objects=[corner_ctrl.control], long_name=['cheekOutUp'],
                                                        attributeType="float", min=0, dv=1, keyable=True)

        self.cheek_out_low_ctrl = rt_utils.add_attribute(objects=[corner_ctrl.control], long_name=['cheekOutLow'],
                                                         attributeType="float", min=0, dv=1, keyable=True)

        self.lid_out_ctrl = rt_utils.add_attribute(objects=[corner_ctrl.control], long_name=['lidOut'],
                                                   attributeType="float", min=0, dv=1, keyable=True)

        self.lid_ctrl = rt_utils.add_attribute(objects=[corner_ctrl.control], long_name=['lid'],
                                               attributeType="float", min=0, dv=1, keyable=True)

        # flipping the controller
        if position_corner_controller < 0:
            cmds.setAttr(corner_ctrl.parent_control[0] + '.scaleX', -1)

        self.control = corner_ctrl.control
        self.control_grp_zro = corner_ctrl.parent_control[0]
        self.control_grp_offset = corner_ctrl.parent_control[1]
