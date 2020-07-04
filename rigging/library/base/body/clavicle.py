"""
creating clavicle module base
"""
from __builtin__ import reload

import maya.cmds as mc

from rigging.library.utils import rotation_controller as rc, controller as ct
from rigging.tools import AD_utils as au

reload(ct)
reload(au)
reload(rc)

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
        self.controller_clavicle = ct.Control(match_obj_first_position=clav_jnt, prefix=prefix, side=side,
                                              shape=ct.STICKCIRCLE,
                                              groups_ctrl=['Zro', 'Offset'], ctrl_size=scale,
                                              ctrl_color='blue', gimbal=True, connection=['parent'],
                                              lock_channels=['s', 'v'])

        # add scale attribute
        self.scale_x = au.add_attr_transform_shape(self.controller_clavicle.control, 'scaleX', 'float', edit=True,
                                                   keyable=True, dv=1)
        self.scale_y = au.add_attr_transform_shape(self.controller_clavicle.control, 'scaleY', 'float', edit=True,
                                                   keyable=True, dv=1)
        self.scale_z = au.add_attr_transform_shape(self.controller_clavicle.control, 'scaleZ', 'float', edit=True,
                                                   keyable=True, dv=1)

        # adjusting the controller direction
        clav_translateX_value = mc.xform(clav_jnt, ws=1, q=1, t=1)[0]

        if clav_translateX_value > 0:
            rc.change_position(self.controller_clavicle.control, 'xz')
            rc.change_position(self.controller_clavicle.control, 'xy')
            rc.change_position(self.controller_clavicle.control_gimbal, 'xz')
            rc.change_position(self.controller_clavicle.control_gimbal, 'xy')

        else:
            rc.change_position(self.controller_clavicle.control, 'xz')
            rc.change_position(self.controller_clavicle.control, 'xy')
            rc.change_position(self.controller_clavicle.control, '-')
            rc.change_position(self.controller_clavicle.control_gimbal, 'xz')
            rc.change_position(self.controller_clavicle.control_gimbal, 'xy')
            rc.change_position(self.controller_clavicle.control_gimbal, '-')
