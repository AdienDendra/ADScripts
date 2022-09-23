from __future__ import absolute_import

import maya.cmds as cmds
from rigging.library.utils import controller as rlu_controller, transform as rlu_transform


class Build:
    def __init__(self,
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
                 suffix_controller):

        # ==================================================================================================================
        #                                            CHEEK CONTROLLER
        # ==================================================================================================================

        # check position
        position_cheek_low_jnt = cmds.xform(cheek_low_jnt, ws=1, q=1, t=1)[0]

        # ==================================================================================================================
        #                                            CHEEK MIDDLE AREA
        # ==================================================================================================================

        # create cheek low controller
        cheek_low_ctrl = rlu_controller.Control(match_obj_first_position=cheek_low_jnt,
                                                prefix=cheek_low_prefix,
                                                shape=rlu_controller.JOINT, groups_ctrl=['', 'Offset'],
                                                ctrl_size=scale * 0.05, suffix=suffix_controller,
                                                ctrl_color='red', lock_channels=['v'], side=side)

        self.cheek_low_ctrl = cheek_low_ctrl.control
        self.cheek_low_ctrl_grp = cheek_low_ctrl.parent_control[0]
        self.cheek_low_ctrl_grp_offset = cheek_low_ctrl.parent_control[1]

        # create cheek mid controller
        cheek_mid_ctrl = rlu_controller.Control(match_obj_first_position=cheek_mid_jnt,
                                                prefix=cheek_mid_prefix,
                                                shape=rlu_controller.JOINT, groups_ctrl=['', 'Offset'],
                                                ctrl_size=scale * 0.05, suffix=suffix_controller,
                                                ctrl_color='red', lock_channels=['v'], side=side)

        self.cheek_mid_ctrl = cheek_mid_ctrl.control
        self.cheek_mid_ctrl_grp = cheek_mid_ctrl.parent_control[0]
        self.cheek_mid_ctrl_grp_offset = cheek_mid_ctrl.parent_control[1]

        # create cheek up controller
        cheek_up_ctrl = rlu_controller.Control(match_obj_first_position=cheek_up_jnt,
                                               prefix=cheek_up_prefix,
                                               shape=rlu_controller.JOINT, groups_ctrl=['', 'Offset'],
                                               ctrl_size=scale * 0.05, suffix=suffix_controller,
                                               ctrl_color='red', lock_channels=['v'], side=side)

        self.cheek_up_ctrl = cheek_up_ctrl.control
        self.cheek_up_ctrl_grp = cheek_up_ctrl.parent_control[0]
        self.cheek_up_ctrl_grp_offset = cheek_up_ctrl.parent_control[1]

        # ==================================================================================================================
        #                                            CHEEK IN AREA
        # ==================================================================================================================

        # create cheek in up controller
        cheek_in_up_ctrl = rlu_controller.Control(match_obj_first_position=cheek_in_up_jnt,
                                                  prefix=cheek_in_up_prefix,
                                                  shape=rlu_controller.JOINT, groups_ctrl=['', 'Offset'],
                                                  ctrl_size=scale * 0.05, suffix=suffix_controller,
                                                  ctrl_color='turquoiseBlue', lock_channels=['v'], side=side)

        self.cheek_in_up_ctrl = cheek_in_up_ctrl.control
        self.cheek_in_up_ctrl_grp = cheek_in_up_ctrl.parent_control[0]
        self.cheek_in_up_ctrl_grp_offset = cheek_in_up_ctrl.parent_control[1]

        # create cheek in low controller
        cheek_in_low_ctrl = rlu_controller.Control(match_obj_first_position=cheek_in_low_jnt,
                                                   prefix=cheek_in_low_prefix,
                                                   shape=rlu_controller.JOINT, groups_ctrl=['', 'Offset'],
                                                   ctrl_size=scale * 0.05, suffix=suffix_controller,
                                                   ctrl_color='turquoiseBlue', lock_channels=['v'], side=side)

        self.cheek_in_low_ctrl = cheek_in_low_ctrl.control
        self.cheek_in_low_ctrl_grp = cheek_in_low_ctrl.parent_control[0]
        self.cheek_in_low_ctrl_grp_offset = cheek_in_low_ctrl.parent_control[1]

        cmds.setAttr(self.cheek_in_low_ctrl_grp_offset + '.scaleY', -1)

        if position_cheek_low_jnt < 0:
            cmds.setAttr(self.cheek_in_low_ctrl_grp_offset + '.scaleX', -1)

        # ==================================================================================================================
        #                                            CHEEK OUT AREA
        # ==================================================================================================================

        # create cheek out up controller
        cheek_out_up_ctrl = rlu_controller.Control(match_obj_first_position=cheek_out_up_jnt,
                                                   prefix=cheek_out_up_prefix,
                                                   shape=rlu_controller.JOINT, groups_ctrl=['', 'Offset'],
                                                   ctrl_size=scale * 0.05, suffix=suffix_controller,
                                                   ctrl_color='red', lock_channels=['v'], side=side)

        self.cheek_out_up_ctrl = cheek_out_up_ctrl.control
        self.cheek_out_up_ctrl_grp = cheek_out_up_ctrl.parent_control[0]
        self.cheek_out_up_ctrl_grp_offset = cheek_out_up_ctrl.parent_control[1]

        # create cheek out low controller
        cheek_out_low_ctrl = rlu_controller.Control(match_obj_first_position=cheek_out_low_jnt,
                                                    prefix=cheek_out_low_prefix,
                                                    shape=rlu_controller.JOINT, groups_ctrl=['', 'Offset'],
                                                    ctrl_size=scale * 0.05, suffix=suffix_controller,
                                                    ctrl_color='red', lock_channels=['v'], side=side)

        self.cheek_out_low_ctrl = cheek_out_low_ctrl.control
        self.cheek_out_low_ctrl_grp = cheek_out_low_ctrl.parent_control[0]
        self.cheek_out_low_ctrl_grp_offset = cheek_out_low_ctrl.parent_control[1]

        # ==================================================================================================================
        #                                           CHEEK JOINT GROUP TRANSFORM
        # ==================================================================================================================

        # parenting the joint
        self.cheek_low_jnt_grp = rlu_transform.create_parent_transform(['', 'Offset'], match_position=cheek_low_jnt,
                                                                       object=cheek_low_jnt,
                                                                       prefix=cheek_low_jnt, suffix=cheek_low_jnt, side=side
                                                                       )

        self.cheek_mid_jnt_grp = rlu_transform.create_parent_transform(['', 'Offset'], match_position=cheek_mid_jnt,
                                                                       object=cheek_mid_jnt,
                                                                       prefix=cheek_mid_jnt, suffix=cheek_mid_jnt, side=side
                                                                       )

        self.cheek_up_jnt_grp = rlu_transform.create_parent_transform(['', 'Offset'], match_position=cheek_up_jnt,
                                                                      object=cheek_up_jnt,
                                                                      prefix=cheek_up_jnt, suffix=cheek_up_jnt, side=side
                                                                      )

        self.cheek_in_up_jnt_grp = rlu_transform.create_parent_transform(['', 'Offset'], match_position=cheek_in_up_jnt,
                                                                         object=cheek_in_up_jnt,
                                                                         prefix=cheek_in_up_jnt, suffix=cheek_in_up_jnt, side=side
                                                                         )

        self.cheek_in_low_jnt_grp = rlu_transform.create_parent_transform(['', 'Offset'], match_position=cheek_in_low_jnt,
                                                                          object=cheek_in_low_jnt,
                                                                          prefix=cheek_in_low_jnt, suffix=cheek_in_low_jnt,
                                                                          side=side
                                                                          )

        self.cheek_out_up_jnt_grp = rlu_transform.create_parent_transform(['', 'Offset'], match_position=cheek_out_up_jnt,
                                                                          object=cheek_out_up_jnt,
                                                                          prefix=cheek_out_up_jnt, suffix=cheek_out_up_jnt,
                                                                          side=side)

        self.cheek_out_low_jnt_grp = rlu_transform.create_parent_transform(['', 'Offset'], match_position=cheek_out_low_jnt,
                                                                           object=cheek_out_low_jnt,
                                                                           prefix=cheek_out_low_jnt, suffix=cheek_out_low_jnt,
                                                                           side=side)

        # flipping the controller
        if position_cheek_low_jnt < 0:
            cmds.setAttr(self.cheek_low_ctrl_grp_offset + '.scaleX', -1)
            cmds.setAttr(self.cheek_mid_ctrl_grp_offset + '.scaleX', -1)
            cmds.setAttr(self.cheek_up_ctrl_grp_offset + '.scaleX', -1)
            cmds.setAttr(self.cheek_in_up_ctrl_grp_offset + '.scaleX', -1)
            cmds.setAttr(self.cheek_out_up_ctrl_grp_offset + '.scaleX', -1)
            cmds.setAttr(self.cheek_out_low_ctrl_grp_offset + '.scaleX', -1)
