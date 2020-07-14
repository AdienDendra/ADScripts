from __builtin__ import reload

import maya.cmds as mc

from rigging.library.base.face import head as hd
from rigging.library.utils import controller as ct
from rigging.tools import AD_utils as au

reload(hd)
reload(au)
reload(ct)


class Head:
    def __init__(self,
                 face_anim_ctrl_grp,
                 face_utils_grp,
                 neck_jnt,
                 neck_in_btw_jnt,
                 head_jnt,
                 jaw_jnt,
                 jaw_tip_jnt,
                 head_up_jnt,
                 head_low_jnt,
                 jaw_prefix,
                 jaw_tip_prefix,
                 head_prefix,
                 neck_prefix,
                 neck_in_btw_prefix,
                 head_up_prefix,
                 head_low_prefix,
                 eye_aim_prefix,
                 eye_jnt_LFT,
                 eye_jnt_RGT,
                 position_eye_aim_ctrl,
                 upper_teeth_jnt,
                 lower_teeth_jnt,
                 tongue01_jnt,
                 tongue02_jnt,
                 tongue03_jnt,
                 tongue04_jnt,
                 suffix_controller,
                 scale,
                 ):

        world_up_grp = mc.spaceLocator(n='worldUpFacialObject_loc')[0]
        mc.hide(world_up_grp)
        self.world_up_grp = world_up_grp

        head = hd.Build(neck_jnt=neck_jnt,
                        neck_in_btw_jnt=neck_in_btw_jnt,
                        head_jnt=head_jnt,
                        jaw_tip_jnt=jaw_tip_jnt,
                        jaw_jnt=jaw_jnt,
                        head_up_jnt=head_up_jnt,
                        head_low_jnt=head_low_jnt,
                        jaw_prefix=jaw_prefix,
                        jaw_tip_prefix=jaw_tip_prefix,

                        head_prefix=head_prefix,
                        head_up_prefix=head_up_prefix,
                        head_low_prefix=head_low_prefix,
                        neck_prefix=neck_prefix,
                        neck_in_between_prefix=neck_in_btw_prefix,
                        upper_teeth_jnt=upper_teeth_jnt,
                        lower_teeth_jnt=lower_teeth_jnt,
                        tongue01_jnt=tongue01_jnt,
                        tongue02_jnt=tongue02_jnt,
                        tongue03_jnt=tongue03_jnt,
                        tongue04_jnt=tongue04_jnt,
                        scale=scale,
                        suffix_controller=suffix_controller,
                        )

        self.head_up_ctrl = head.head_up_ctrl.control
        self.head_up_ctrl_gimbal = head.head_up_ctrl.control_gimbal

        self.head_low_ctrl = head.head_low_ctrl.control
        self.head_low_ctrl_gimbal = head.head_low_ctrl.control_gimbal

        self.neck_ctrl = head.neck_ctrl.control
        self.neck_ctrl_gimbal = head.neck_ctrl.control_gimbal
        self.neck_ctrl_grp = head.neck_ctrl.parent_control[0]

        self.head_ctrl = head.head_ctrl.control
        self.head_ctrl_gimbal = head.head_ctrl.control_gimbal
        self.head_ctrl_grp = head.head_ctrl.parent_control[0]
        self.head_ctrl_grp_global = head.head_ctrl.parent_control[1]
        self.head_ctrl_grp_local = head.head_ctrl.parent_control[2]

        self.jaw_ctrl_grp = head.jaw_ctrl.parent_control[0]
        self.jaw_ctrl = head.jaw_ctrl.control
        self.attr_upLip_follow = head.attr_upLip_follow
        self.attr_degree_follow = head.attr_degree_follow
        self.headLow_normal_rotationGrp = head.headLow_normal_rotationGrp

        self.jaw_prefix = jaw_prefix
        self.neck_jnt_grp = head.neck_jnt_grp
        # LOCAL WORLD HEAD
        self.local_world(object_name='head', object_ctrl=self.head_ctrl,
                         object_grp=self.head_ctrl_grp, object_grp_global=self.head_ctrl_grp_global,
                         object_grp_local=self.head_ctrl_grp_local,
                         local_base=self.neck_ctrl_gimbal, world_base=world_up_grp, eye_aim=False)

        # JAW CONNECTION
        au.connect_attr_translate_rotate(self.jaw_ctrl, head.jaw_direction_grp_offset)
        au.connect_attr_translate_rotate(self.jaw_ctrl, jaw_jnt)
        pac_jaw_tip = mc.parentConstraint(jaw_jnt, head.jaw_tip_jnt_grp[1], mo=1)

        # CREATE PMA
        jaw_pma = mc.createNode('plusMinusAverage', n=au.prefix_name(jaw_tip_jnt) + 'Trans_pma')
        mc.setAttr(jaw_pma + '.operation', 2)
        mc.connectAttr(head.jaw_tip_jnt_grp[1] + '.translate', jaw_pma + '.input3D[0]')
        mc.connectAttr(self.jaw_ctrl + '.translate', jaw_pma + '.input3D[1]')
        mc.connectAttr(jaw_pma + '.output3D', head.jaw_ctrl.parent_control[1] + '.translate')

        # ==================================================================================================================
        #                                               CREATE AIM FOR EYE
        # ==================================================================================================================

        eye_aim_main_ctrl = ct.Control(match_obj_first_position=eye_jnt_LFT,
                                       match_obj_second_position=eye_jnt_RGT,
                                       prefix=eye_aim_prefix,
                                       shape=ct.CAPSULE, groups_ctrl=['All', 'Global', 'Local'],
                                       ctrl_size=scale * 0.25,
                                       ctrl_color='blue', lock_channels=['v', 'r', 's'])

        self.eyeAimMainCtrl = eye_aim_main_ctrl.control
        self.eye_aim_main_ctrl_grp = eye_aim_main_ctrl.parent_control[0]
        self.eye_aim_main_ctrl_grp_global = eye_aim_main_ctrl.parent_control[1]
        self.eye_aim_main_ctrl_grp_local = eye_aim_main_ctrl.parent_control[2]

        get_attribute = mc.getAttr(eye_aim_main_ctrl.parent_control[0] + '.translateZ')
        mc.setAttr(eye_aim_main_ctrl.parent_control[0] + '.translateZ', get_attribute + (position_eye_aim_ctrl * scale))

        # LOCAL WORLD AIM EYE
        self.local_world(object_name='eyeAim', object_ctrl=self.eyeAimMainCtrl,
                         object_grp=self.eye_aim_main_ctrl_grp,
                         object_grp_global=self.eye_aim_main_ctrl_grp_global,
                         object_grp_local=self.eye_aim_main_ctrl_grp_local,
                         local_base=self.head_up_ctrl_gimbal, world_base=world_up_grp, eye_aim=True)

        # SCALE CONSTRAINT FROM HEAD UP CTRL TO EYE MAIN AIM ALL GRP
        scale_eye_main_constraint = mc.scaleConstraint(self.head_up_ctrl, eye_aim_main_ctrl.parent_control[0])

        mc.parent(self.neck_ctrl_grp, self.eye_aim_main_ctrl_grp, face_anim_ctrl_grp)
        mc.parent(world_up_grp, face_utils_grp)

        # RENAME CONSTRAINT
        au.constraint_rename([pac_jaw_tip[0], scale_eye_main_constraint[0]])

    def jaw_ctrl_gimbal_driver_jnt(self, node_name, jaw_controller, jaw_controller_gimbal, jaw_target, attribute):
        pma_jaw_add = mc.createNode('plusMinusAverage', n=self.jaw_prefix + node_name + '_pma')
        mc.connectAttr(jaw_controller + '.%s' % attribute, pma_jaw_add + '.input3D[0]')
        mc.connectAttr(jaw_controller_gimbal + '.%s' % attribute, pma_jaw_add + '.input3D[1]')

        mc.connectAttr(pma_jaw_add + '.output3D', jaw_target + '.%s' % attribute)

    def local_world(self, object_name, object_ctrl, object_grp, object_grp_global, object_grp_local, local_base,
                    world_base, eye_aim=False):
        # LOCAL WORLD HEAD
        local = mc.createNode('transform', n=object_name + 'Local_grp')
        mc.parent(local, object_grp)
        mc.setAttr(local + '.translate', 0, 0, 0, type="double3")
        mc.setAttr(local + '.rotate', 0, 0, 0, type="double3")

        world = mc.duplicate(local, n=object_name + 'World_grp')[0]

        pac_locator_base_constraint = mc.parentConstraint(local_base, local, mo=1)
        pac_world_base_constraint = mc.parentConstraint(world_base, world, mo=1)

        if not eye_aim:
            pac_obj_global_cons = mc.parentConstraint(local, object_grp_global, mo=1)
            local_world_cons = mc.orientConstraint(local, world, object_grp_local, mo=1)[0]
            # rename constraint
            au.constraint_rename(pac_obj_global_cons)

        else:
            local_world_cons = mc.parentConstraint(local, world, object_grp_local, mo=1)[0]

        # CONNECT THE ATTRIBUTE
        head_local_world = au.add_attribute(objects=[object_ctrl], long_name=['localWorld'],
                                            attributeType="float", min=0, max=1, dv=0, keyable=True)

        # CREATE REVERSE
        reverse = mc.createNode('reverse', n=object_name + 'LocalWorld_rev')
        mc.connectAttr(object_ctrl + '.%s' % head_local_world, reverse + '.inputX')

        mc.connectAttr(reverse + '.outputX', local_world_cons + '.%sW0' % local)
        mc.connectAttr(object_ctrl + '.%s' % head_local_world, local_world_cons + '.%sW1' % world)

        # CONSTRAINT RENAME
        au.constraint_rename([pac_locator_base_constraint[0], pac_world_base_constraint[0], local_world_cons])
