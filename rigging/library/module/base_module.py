"""
module for making controller base, setup and base module
"""
from __builtin__ import reload

import maya.cmds as mc

from rigging.library.utils import controller as ct
from rigging.tools import AD_utils as au

reload(ct)
reload(au)

general_scale = 1.0
class GeneralBase:
    #top structure
    def __init__(self,
                lockChannels = ['t','r','s'],
                scale = general_scale
                 ):
        """
        @param lockChannels: str, list attribute channels
        @param scale       : float, scale general all object base
        @return            : None

        """
        # make world control
        world_control = ct.Control(
            prefix='World',
            suffix='Ctrl',
            groups_ctrl=['Zro'],
            side='',
            ctrl_size=scale * 5,
            gimbal=None,
            ctrl_color='darkBrown',
            lock_channels=['v'],
            shape=ct.CIRCLE,
        )

        # make placer control
        place_control = ct.Control(
            prefix='Place',
            suffix='Ctrl',
            groups_ctrl=['Zro'],
            side='',
            ctrl_size=scale * 5,
            gimbal=None,
            ctrl_color='yellow',
            lock_channels=['v'],
            shape=ct.WORLD,
        )

        # create group and parenting corresponding to its grp
        self.root_grp  = mc.group (n='Rig_Grp', em=1)
        self.world_grp = mc.group (n='World_Grp', em=1, p=self.root_grp)
        mc.parent(world_control.control, self.world_grp)

        self.place_grp = mc.group(n='Place_Grp', em=1, p=world_control.control)
        mc.parent(place_control.control, self.place_grp)

        self.anim_grp = mc.group(n='anim_grp', em=1, p=place_control.control)
        # self.jntGrp   = mc.group(n='jnt_grp', em=1, p=placeControl.control)

        self.util_grp = mc.group(n='Utils_Grp', em=1, p=self.world_grp)

        # deleting grp parent ctrl
        mc.delete(world_control.parent_control[0])
        mc.delete(place_control.parent_control[0])

        # create more group for other utilities
        self.anim_util_grp = mc.group(n='Anim_Grp', em=1, p=self.util_grp)

        self.joint_grp = mc.group(n='Joint_Grp', em=1, p=self.anim_util_grp)
        self.curve_grp = mc.group(n='Curve_Grp', em=1, p=self.anim_util_grp)
        self.surface_grp = mc.group(n='Surface_Grp', em=1, p=self.anim_util_grp)
        self.locator_grp = mc.group(n='Locator_Grp', em=1, p=self.anim_util_grp)
        self.ik_handle_grp = mc.group(n='IkHandle_Grp', em=1, p=self.anim_util_grp)
        self.cluster_grp = mc.group(n='Cluster_Grp', em=1, p=self.anim_util_grp)

        self.still_grp = mc.group(n='Still_Grp', em=1, p=self.util_grp)

        self.geo_grp = mc.group(n='Geo_Grp', em=1, p=self.root_grp)

        # locking the atributes directories
        au.lock_hide_attr(lockChannels, self.util_grp)
        au.lock_hide_attr(lockChannels, self.joint_grp)
        au.lock_hide_attr(lockChannels, self.curve_grp)
        au.lock_hide_attr(lockChannels, self.surface_grp)
        au.lock_hide_attr(lockChannels, self.locator_grp)
        au.lock_hide_attr(lockChannels, self.ik_handle_grp)
        au.lock_hide_attr(lockChannels, self.cluster_grp)


class Base:
    # create  main controller for base part
    def __init__(self,
                 scale = general_scale,
                 ):
        """
        @param scale: float, scale the main controller builder
        @return : None

        """
        anim_control = ct.Control(
            prefix='anim',
            suffix='ctrl',
            groups_ctrl=['Zro'],
            side='',
            ctrl_size=scale * 3,
            gimbal=True,
            ctrl_color='darkGreen',
            lock_channels=['v'],
            shape=ct.ARROW4STRAIGHT,
        )

        self.anim_control = anim_control.control
        self.unparent_main_control = mc.parent(anim_control.control, w=True)
        self.gimbal_control = anim_control.control_gimbal
        mc.delete(anim_control.parent_control[0])

        # adding attribute size to place ctrl
        au.add_attr_transform(anim_control.control, 'size', 'double', dv=1, min=0.1, edit=True, keyable=True)
        self.scale_matrix_node = mc.shadingNode('decomposeMatrix', asUtility=1, n='animGeneralScale_dmtx')
        mc.connectAttr(self.anim_control + '.worldMatrix[0]', self.scale_matrix_node + '.inputMatrix')

        # connecting the size attributes to its scale object
        for axis in ['x', 'y', 'z']:
            mc.connectAttr(anim_control.control + '.size', anim_control.control + '.s' + axis)
            mc.setAttr(anim_control.control + '.s' + axis, k=0, l=1)

        # adding group for anim control
        self.body_part_grp = mc.group(n='bodyModule_grp', em=1, p=anim_control.control_gimbal)
        au.lock_hide_attr(['t', 'r', 's'], self.body_part_grp)

        # adding group for face control
        self.face_part_grp = mc.group(n='faceModule_grp', em=1, p=anim_control.control_gimbal)
        au.lock_hide_attr(['t', 'r', 's'], self.face_part_grp)

        self.face_anim_grp = mc.group(n='faceAnim_grp', em=1, p=self.face_part_grp)
        self.face_controller_grp = mc.group(n='faceCtrl_grp', em=1, p=self.face_anim_grp)
        self.face_joint_grp = mc.group(n='faceJoint_grp', em=1, p=self.face_part_grp)
        self.face_utils_grp = mc.group(n='faceUtils_grp', em=1, p=self.face_part_grp)
        self.face_non_transform_grp = mc.group(n='faceNonTransform_grp', em=1, p=self.face_part_grp)

        mc.setAttr(self.face_controller_grp + '.it', 0, l=1)
        mc.setAttr(self.face_joint_grp + '.it', 0, l=1)
        mc.setAttr(self.face_non_transform_grp + '.it', 0, l=1)

        # mc.setAttr(self.face_joint_grp + '.visibility', 0)
        mc.setAttr(self.face_utils_grp + '.visibility', 0)
        # mc.setAttr(self.face_non_transform_grp + '.visibility', 0)

        au.lock_hide_attr(['t', 'r', 's'], self.face_anim_grp)
        au.lock_hide_attr(['t', 'r', 's'], self.face_controller_grp)
        au.lock_hide_attr(['t', 'r', 's'], self.face_joint_grp)
        au.lock_hide_attr(['t', 'r', 's'], self.face_utils_grp)
        au.lock_hide_attr(['t', 'r', 's'], self.face_non_transform_grp)


        # # adding group for joint
        # self.skin_grp = mc.group(n='skin_grp', em=1, p=anim_control.control_gimbal)
        # au.lock_hide_attr(['t', 'r', 's'], self.skin_grp)

        # adding group for joint
        self.skeleton_grp = mc.group(n='skeleton_grp', em=1, p=anim_control.control_gimbal)
        au.lock_hide_attr(['t', 'r', 's'], self.skeleton_grp)
        mc.hide(self.skeleton_grp)

        # adding group for skin
        self.additional_grp = mc.group(n='additional_grp', em=1, p=anim_control.control_gimbal)
        au.lock_hide_attr(['t', 'r', 's'], self.additional_grp)
        mc.hide(self.additional_grp)

        # # adding group for still
        # self.nonTransformGrp = mc.group(n='nonTransform_grp', em=1, p=animControl.controlGimbal)
        # mc.setAttr (self.nonTransformGrp + '.it', 0, l=1)
        # au.lockHideAttr(['t','r','s'], self.nonTransformGrp)
        # mc.hide(self.nonTransformGrp)

        # # adding group for utilities
        # self.utilitiesGrp = mc.group(n='utilities_grp', em=1, p=animControl.controlGimbal)
        # au.lockHideAttr(['t','r','s'], self.utilitiesGrp)
        # mc.hide(self.utilitiesGrp)

        # # adding group for skin
        # self.skinGrp = mc.group(n='skin_grp', em=1, p=animControl.controlGimbal)
        # au.lockHideAttr(['t','r','s'], self.skinGrp)
        # mc.hide(self.skinGrp)

class Part:
    # create part of base group
    def __init__(self,
                 prefix ='prefix',
                 side='',
                 grpName ='_grp',
                 ):
        """
        :param prefix: str, name of part of limbs
        :param baseObj: instance of the Part class
        :return : None
        """

        self.top_grp       = mc.group(n=prefix + 'Module' + side + grpName, em=1)

        self.control_grp   = mc.group (n=prefix + 'Anim' + side + grpName, em=1, p=self.top_grp)
        self.joint_grp = mc.group(n=prefix + 'Joint' + side + grpName, em=1, p=self.top_grp)
        # self.skinGrp = mc.group (n=prefix +'Skin' + side + grpName, em=1, p=self.topGrp)
        self.utils_grp = mc.group(n=prefix + 'Utils' + side + grpName, em=1, p=self.top_grp)
        self.non_transform_grp = mc.group(n=prefix + 'NonTransform' + side + grpName, em=1, p=self.top_grp)

        mc.setAttr(self.non_transform_grp + '.it', 0, l=1)

        # mc.setAttr(self.joint_grp + '.visibility', 0)
        mc.setAttr(self.utils_grp + '.visibility', 0)

        au.lock_hide_attr(['t', 'r', 's'], self.top_grp)
        au.lock_hide_attr(['t', 'r', 's'], self.control_grp)
        au.lock_hide_attr(['t', 'r', 's'], self.joint_grp)
        au.lock_hide_attr(['t', 'r', 's'], self.utils_grp)
        au.lock_hide_attr(['t', 'r', 's'], self.non_transform_grp)
