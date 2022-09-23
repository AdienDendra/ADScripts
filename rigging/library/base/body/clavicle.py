"""
creating clavicle module base
"""
from __future__ import absolute_import

import maya.cmds as cmds

from rigging.library.utils import rotationController as rlu_rotationController, controller as rlu_controller
from rigging.tools import utils as rt_utils


class Build:
    def __init__(self,
                 clav_jnt,
                 prefix,
                 side,
                 scale,
                 ):

        # ==============================================================================================================
        #                                       CREATE CONTROL CLAVICLE FK
        # ==============================================================================================================
        self.controller_clavicle = rlu_controller.Control(match_obj_first_position=clav_jnt, prefix=prefix, side=side,
                                                          shape=rlu_controller.STICKCIRCLE,
                                                          groups_ctrl=['Zro', 'Offset'], ctrl_size=scale,
                                                          ctrl_color='blue', gimbal=True, connection=['parent'],
                                                          lock_channels=['s', 'v'])

        # add scale attribute
        self.scale_x = rt_utils.add_attr_transform_shape(self.controller_clavicle.control, 'scaleX', 'float', edit=True,
                                                         keyable=True, dv=1)
        self.scale_y = rt_utils.add_attr_transform_shape(self.controller_clavicle.control, 'scaleY', 'float', edit=True,
                                                         keyable=True, dv=1)
        self.scale_z = rt_utils.add_attr_transform_shape(self.controller_clavicle.control, 'scaleZ', 'float', edit=True,
                                                         keyable=True, dv=1)

        # adjusting the controller direction
        clav_translateX_value = cmds.xform(clav_jnt, ws=1, q=1, t=1)[0]

        if clav_translateX_value > 0:
            rlu_rotationController.change_position(self.controller_clavicle.control, 'xz')
            rlu_rotationController.change_position(self.controller_clavicle.control, 'xy')
            rlu_rotationController.change_position(self.controller_clavicle.control_gimbal, 'xz')
            rlu_rotationController.change_position(self.controller_clavicle.control_gimbal, 'xy')

        else:
            rlu_rotationController.change_position(self.controller_clavicle.control, 'xz')
            rlu_rotationController.change_position(self.controller_clavicle.control, 'xy')
            rlu_rotationController.change_position(self.controller_clavicle.control, '-')
            rlu_rotationController.change_position(self.controller_clavicle.control_gimbal, 'xz')
            rlu_rotationController.change_position(self.controller_clavicle.control_gimbal, 'xy')
            rlu_rotationController.change_position(self.controller_clavicle.control_gimbal, '-')
