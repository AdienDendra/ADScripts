"""
creating arm module base
"""
from __future__ import absolute_import

from rigging.library.utils import controller as rlu_controller
from rigging.tools import utils as rt_utils


class Build:
    def __init__(self,
                 joint,
                 prefix_joint,
                 shape,
                 side,
                 scale,
                 scale_adjust=0.2,
                 ctrl_color='yellow',
                 lock_channels=['v'],
                 connection=['parent']
                 ):
        ## CREATE CONTROLLER FINGER
        finger_joint = rlu_controller.Control(match_obj_first_position=joint, prefix='%s' % (prefix_joint), side=side,
                                              shape=shape,
                                              groups_ctrl=['Zro', 'Offset', 'Curl'], ctrl_size=scale * scale_adjust,
                                              ctrl_color=ctrl_color, lock_channels=lock_channels,
                                              connection=connection)

        self.parent_base = finger_joint.parent_control[0]
        self.parent_mid = finger_joint.parent_control[1]
        self.parent_curl = finger_joint.parent_control[2]
        self.control = finger_joint.control

    def add_attribute_finger(self, finger_setup_ctrl, thumb):
        # ARM SETUP
        rt_utils.add_attribute(objects=[finger_setup_ctrl], long_name=['handScale'], nice_name=[' '], at="enum",
                               en='Hand Scale', channel_box=True)

        rt_utils.add_attribute(objects=[finger_setup_ctrl], long_name=['handScaleX'],
                               attributeType="float", dv=1, keyable=True)
        rt_utils.add_attribute(objects=[finger_setup_ctrl], long_name=['handScaleY'],
                               attributeType="float", dv=1, keyable=True)
        rt_utils.add_attribute(objects=[finger_setup_ctrl], long_name=['handScaleZ'],
                               attributeType="float", dv=1, keyable=True)

        # HAND SETUP
        rt_utils.add_attribute(objects=[finger_setup_ctrl], long_name=['fingerSetup'], nice_name=[' '],
                               at="enum", en='Finger Setup', channel_box=True)

        rt_utils.add_attribute(objects=[finger_setup_ctrl], long_name=['curl'],
                               attributeType="float", dv=0, keyable=True)

        rt_utils.add_attribute(objects=[finger_setup_ctrl], long_name=['cupInner'],
                               attributeType="float", dv=0, keyable=True)

        rt_utils.add_attribute(objects=[finger_setup_ctrl], long_name=['cupOuter'],
                               attributeType="float", dv=0, keyable=True)

        rt_utils.add_attribute(objects=[finger_setup_ctrl], long_name=['spread'],
                               attributeType="float", dv=0, keyable=True)

        rt_utils.add_attribute(objects=[finger_setup_ctrl], long_name=['slide'],
                               attributeType="float", dv=0, keyable=True)

        rt_utils.add_attribute(objects=[finger_setup_ctrl], long_name=['crunch'],
                               attributeType="float", dv=0, keyable=True)

        if thumb:
            rt_utils.add_attribute(objects=[finger_setup_ctrl], long_name=['thumbCurl'],
                                   attributeType="float", dv=0, keyable=True)

            rt_utils.add_attribute(objects=[finger_setup_ctrl], long_name=['thumbSpread'],
                                   attributeType="float", dv=0, keyable=True)

            rt_utils.add_attribute(objects=[finger_setup_ctrl], long_name=['thumbCrunch'],
                                   attributeType="float", dv=0, keyable=True)
