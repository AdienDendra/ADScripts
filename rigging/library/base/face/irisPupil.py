from __future__ import absolute_import

import maya.cmds as cmds

from rigging.library.utils import controller as rlu_controller, transform as rlu_transform
from rigging.tools import utils as rt_utils


class Build:
    def __init__(self,
                 pupil_jnt,
                 iris_jnt,
                 pupil_prefix,
                 iris_prefix,
                 eyeball_jnt,
                 eye_jnt_grp_offset,
                 scale,
                 eye_ctrl,
                 side,
                 suffix_controller,
                 ):
        self.iris_connect_grp = cmds.group(em=1, n='irisConnect' + side + '_grp')
        cmds.delete(cmds.parentConstraint(eyeball_jnt, self.iris_connect_grp))

        # CREATE CONTROLLER
        pupil_ctrl = rlu_controller.Control(match_obj_first_position=pupil_jnt,
                                            prefix=pupil_prefix,
                                            shape=rlu_controller.CIRCLEPLUS, groups_ctrl=[''],
                                            ctrl_size=scale * 0.08,
                                            ctrl_color='red', lock_channels=['v'],
                                            suffix=suffix_controller,
                                            side=side)

        iris_ctrl = rlu_controller.Control(match_obj_first_position=iris_jnt,
                                           prefix=iris_prefix,
                                           shape=rlu_controller.CIRCLEPLUS, groups_ctrl=[''],
                                           ctrl_size=scale * 0.12,
                                           suffix=suffix_controller,
                                           ctrl_color='blue', lock_channels=['v'], side=side)

        # CREATE GROUP CORESPONDENT THE JOINTS
        pupil_jnt_grp = rlu_transform.create_parent_transform(parent_list=[''], object=pupil_jnt,
                                                              match_position=pupil_jnt,
                                                              prefix=pupil_prefix, suffix='_jnt', side=side)

        iris_jnt_grp = rlu_transform.create_parent_transform(parent_list=[''], object=iris_jnt, match_position=iris_jnt,
                                                             prefix=iris_prefix, suffix='_jnt', side=side)

        # ASSIGNED THE INSTANCE CLASS
        self.pupil_ctrl = pupil_ctrl.control
        self.pupil_ctrl_grp = pupil_ctrl.parent_control[0]
        self.iris_ctrl = iris_ctrl.control
        self.iris_ctrl_grp = iris_ctrl.parent_control[0]

        rt_utils.connect_attr_object(pupil_ctrl.control, pupil_jnt)
        rt_utils.connect_attr_object(iris_ctrl.control, iris_jnt)

        cmds.parent(self.pupil_ctrl_grp, self.iris_ctrl)
        cmds.parent(self.iris_connect_grp, eye_ctrl)
        rt_utils.connect_attr_rotate(eye_jnt_grp_offset, self.iris_connect_grp)

        cmds.parent(iris_jnt_grp[0], eyeball_jnt)
        cmds.parent(self.iris_ctrl_grp, self.iris_connect_grp)
