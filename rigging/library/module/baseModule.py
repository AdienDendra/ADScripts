"""
module for making controller base, setup and base module
"""
from __future__ import absolute_import

import maya.cmds as cmds

from rigging.library.utils import controller as rlu_controller
from rigging.tools import utils as rt_utils

general_scale = 1.0


class GeneralBase:
    # top structure
    def __init__(self,
                 lockChannels=['t', 'r', 's'],
                 scale=general_scale
                 ):
        """
        @param lockChannels: str, list attribute channels
        @param scale       : float, scale general all object base
        @return            : None

        """
        # make world control
        world_control = rlu_controller.Control(
            prefix='World',
            suffix='Ctrl',
            groups_ctrl=['Zro'],
            side='',
            ctrl_size=scale * 5,
            gimbal=None,
            ctrl_color='darkBrown',
            lock_channels=['v'],
            shape=rlu_controller.CIRCLE,
        )

        # make placer control
        place_control = rlu_controller.Control(
            prefix='Place',
            suffix='Ctrl',
            groups_ctrl=['Zro'],
            side='',
            ctrl_size=scale * 5,
            gimbal=None,
            ctrl_color='yellow',
            lock_channels=['v'],
            shape=rlu_controller.WORLD,
        )

        # create group and parenting corresponding to its grp
        self.root_grp = cmds.group(n='Rig_Grp', em=1)
        self.world_grp = cmds.group(n='World_Grp', em=1, p=self.root_grp)
        cmds.parent(world_control.control, self.world_grp)

        self.place_grp = cmds.group(n='Place_Grp', em=1, p=world_control.control)
        cmds.parent(place_control.control, self.place_grp)

        self.anim_grp = cmds.group(n='anim_grp', em=1, p=place_control.control)

        self.util_grp = cmds.group(n='Utils_Grp', em=1, p=self.world_grp)

        # deleting grp parent ctrl
        cmds.delete(world_control.parent_control[0])
        cmds.delete(place_control.parent_control[0])

        # create more group for other utilities
        self.anim_util_grp = cmds.group(n='Anim_Grp', em=1, p=self.util_grp)

        self.joint_grp = cmds.group(n='Joint_Grp', em=1, p=self.anim_util_grp)
        self.curve_grp = cmds.group(n='Curve_Grp', em=1, p=self.anim_util_grp)
        self.surface_grp = cmds.group(n='Surface_Grp', em=1, p=self.anim_util_grp)
        self.locator_grp = cmds.group(n='Locator_Grp', em=1, p=self.anim_util_grp)
        self.ik_handle_grp = cmds.group(n='IkHandle_Grp', em=1, p=self.anim_util_grp)
        self.cluster_grp = cmds.group(n='Cluster_Grp', em=1, p=self.anim_util_grp)

        self.still_grp = cmds.group(n='Still_Grp', em=1, p=self.util_grp)

        self.geo_grp = cmds.group(n='Geo_Grp', em=1, p=self.root_grp)

        # locking the atributes directories
        rt_utils.lock_hide_attr(lockChannels, self.util_grp)
        rt_utils.lock_hide_attr(lockChannels, self.joint_grp)
        rt_utils.lock_hide_attr(lockChannels, self.curve_grp)
        rt_utils.lock_hide_attr(lockChannels, self.surface_grp)
        rt_utils.lock_hide_attr(lockChannels, self.locator_grp)
        rt_utils.lock_hide_attr(lockChannels, self.ik_handle_grp)
        rt_utils.lock_hide_attr(lockChannels, self.cluster_grp)


class Base:
    # create  main controller for base part
    def __init__(self,
                 scale=general_scale,
                 ):
        """
        @param scale: float, scale the main controller builder
        @return : None

        """
        anim_control = rlu_controller.Control(
            prefix='anim',
            suffix='ctrl',
            groups_ctrl=['Zro'],
            side='',
            ctrl_size=scale * 3,
            gimbal=True,
            ctrl_color='darkGreen',
            lock_channels=['v'],
            shape=rlu_controller.ARROW4STRAIGHT,
        )

        self.anim_control = anim_control.control
        self.unparent_main_control = cmds.parent(anim_control.control, w=True)
        self.gimbal_control = anim_control.control_gimbal
        cmds.delete(anim_control.parent_control[0])

        # adding attribute size to place ctrl
        rt_utils.add_attr_transform(anim_control.control, 'size', 'double', dv=1, min=0.1, edit=True, keyable=True)
        self.scale_matrix_node = cmds.shadingNode('decomposeMatrix', asUtility=1, n='animGeneralScale_dmtx')
        cmds.connectAttr(self.anim_control + '.worldMatrix[0]', self.scale_matrix_node + '.inputMatrix')

        # connecting the size attributes to its scale object
        for axis in ['x', 'y', 'z']:
            cmds.connectAttr(anim_control.control + '.size', anim_control.control + '.s' + axis)
            cmds.setAttr(anim_control.control + '.s' + axis, k=0, l=1)

        # adding group for anim control
        self.body_part_grp = cmds.group(n='bodyModule_grp', em=1, p=anim_control.control_gimbal)
        rt_utils.lock_hide_attr(['t', 'r', 's'], self.body_part_grp)

        # adding group for face control
        self.face_part_grp = cmds.group(n='faceModule_grp', em=1, p=anim_control.control_gimbal)
        rt_utils.lock_hide_attr(['t', 'r', 's'], self.face_part_grp)

        self.face_anim_grp = cmds.group(n='faceAnim_grp', em=1, p=self.face_part_grp)
        self.face_controller_grp = cmds.group(n='faceCtrl_grp', em=1, p=self.face_anim_grp)
        self.face_joint_grp = cmds.group(n='faceJoint_grp', em=1, p=self.face_part_grp)
        self.face_utils_grp = cmds.group(n='faceUtils_grp', em=1, p=self.face_part_grp)
        self.face_non_transform_grp = cmds.group(n='faceNonTransform_grp', em=1, p=self.face_part_grp)

        cmds.setAttr(self.face_controller_grp + '.it', 0, l=1)
        cmds.setAttr(self.face_joint_grp + '.it', 0, l=1)
        cmds.setAttr(self.face_non_transform_grp + '.it', 0, l=1)

        cmds.setAttr(self.face_utils_grp + '.visibility', 0)

        rt_utils.lock_hide_attr(['t', 'r', 's'], self.face_anim_grp)
        rt_utils.lock_hide_attr(['t', 'r', 's'], self.face_controller_grp)
        rt_utils.lock_hide_attr(['t', 'r', 's'], self.face_joint_grp)
        rt_utils.lock_hide_attr(['t', 'r', 's'], self.face_utils_grp)
        rt_utils.lock_hide_attr(['t', 'r', 's'], self.face_non_transform_grp)

        # adding group for joint
        self.skeleton_grp = cmds.group(n='skeleton_grp', em=1, p=anim_control.control_gimbal)
        rt_utils.lock_hide_attr(['t', 'r', 's'], self.skeleton_grp)
        cmds.hide(self.skeleton_grp)

        # adding group for skin
        self.additional_grp = cmds.group(n='additional_grp', em=1, p=anim_control.control_gimbal)
        rt_utils.lock_hide_attr(['t', 'r', 's'], self.additional_grp)
        cmds.hide(self.additional_grp)


class Part:
    # create part of base group
    def __init__(self,
                 prefix='prefix',
                 side='',
                 grpName='_grp',
                 ):
        """
        :param prefix: str, name of part of limbs
        :param baseObj: instance of the Part class
        :return : None
        """

        self.top_grp = cmds.group(n=prefix + 'Module' + side + grpName, em=1)

        self.control_grp = cmds.group(n=prefix + 'Anim' + side + grpName, em=1, p=self.top_grp)
        self.joint_grp = cmds.group(n=prefix + 'Joint' + side + grpName, em=1, p=self.top_grp)
        self.utils_grp = cmds.group(n=prefix + 'Utils' + side + grpName, em=1, p=self.top_grp)
        self.non_transform_grp = cmds.group(n=prefix + 'NonTransform' + side + grpName, em=1, p=self.top_grp)

        cmds.setAttr(self.non_transform_grp + '.it', 0, l=1)

        cmds.setAttr(self.utils_grp + '.visibility', 0)

        rt_utils.lock_hide_attr(['t', 'r', 's'], self.top_grp)
        rt_utils.lock_hide_attr(['t', 'r', 's'], self.control_grp)
        rt_utils.lock_hide_attr(['t', 'r', 's'], self.joint_grp)
        rt_utils.lock_hide_attr(['t', 'r', 's'], self.utils_grp)
        rt_utils.lock_hide_attr(['t', 'r', 's'], self.non_transform_grp)
