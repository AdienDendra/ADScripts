"""
creating spine module base
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
                 spine_jnt,
                 pelvis_jnt,
                 root_jnt,
                 scale,
                 prefix_spine_setup,
                 detail_spine_deformer=True,
                 side=''
                 ):
        # ==============================================================================================================
        #                                              CONTROL PELVIS AND ROOT
        # ==============================================================================================================
        self.controller_root = ct.Control(match_obj_first_position=root_jnt, prefix='hip', shape=ct.SQUAREPLUS,
                                          groups_ctrl=['Zro', 'Offset'], side=side, ctrl_size=scale * 1.2,
                                          ctrl_color='chocholate', gimbal=True, lock_channels=['v', 's'],
                                          connection=['parent'])

        self.controller_pelvis = ct.Control(match_obj_first_position=pelvis_jnt, prefix='pelvis', shape=ct.SQUAREPLUS,
                                            groups_ctrl=['Zro', 'Offset'], side=side, ctrl_size=scale,
                                            ctrl_color='yellow', gimbal=True, lock_channels=['v', 's'],
                                            connection=['parent'])

        # ==============================================================================================================
        #                                                   CONTROL FK
        # ==============================================================================================================
        self.controller_spine_fk_low = ct.Control(match_obj_first_position=spine_jnt[0],
                                                  match_obj_second_position=root_jnt,
                                                  prefix='spineFk01', shape=ct.CIRCLEPLUS,
                                                  groups_ctrl=['Zro', 'Offset'], side=side, ctrl_size=scale,
                                                  ctrl_color='yellow', gimbal=True, lock_channels=['v', 's'])

        self.controller_spine_fk_mid = ct.Control(match_obj_first_position=spine_jnt[1],
                                                  match_obj_second_position=spine_jnt[0], prefix='spineFk02',
                                                  shape=ct.CIRCLEPLUS,
                                                  groups_ctrl=['Zro', 'Offset'], side=side, ctrl_size=scale,
                                                  ctrl_color='yellow', gimbal=True, lock_channels=['v', 's'])

        self.controller_spine_fk_up = ct.Control(match_obj_first_position=spine_jnt[3],
                                                 match_obj_second_position=spine_jnt[2], prefix='spineFk03',
                                                 shape=ct.CIRCLEPLUS,
                                                 groups_ctrl=['Zro', 'Offset'], side=side, ctrl_size=scale,
                                                 ctrl_color='yellow', gimbal=True, lock_channels=['v', 's'],
                                                 connection=['parentCons'])

        # parent the controller FK from up to low
        mc.parent(self.controller_spine_fk_up.parent_control[0], self.controller_spine_fk_mid.control_gimbal)
        mc.parent(self.controller_spine_fk_mid.parent_control[0], self.controller_spine_fk_low.control_gimbal)

        # ==============================================================================================================
        #                                                   CONTROL IK
        # ==============================================================================================================
        self.controller_spine_ik_low = ct.Control(match_obj_first_position=spine_jnt[1], prefix='spineIk01',
                                                  shape=ct.CIRCLEPLUS,
                                                  groups_ctrl=['Zro', 'Offset'], side=side, ctrl_size=scale,
                                                  ctrl_color='red', gimbal=True, lock_channels=['v', 's'])
        self.controller_spine_ik_up = ct.Control(match_obj_first_position=spine_jnt[3],
                                                 match_obj_second_position=spine_jnt[2], prefix='spineIk02',
                                                 shape=ct.CIRCLEPLUS,
                                                 groups_ctrl=['Zro', 'Offset'], side=side, ctrl_size=scale,
                                                 ctrl_color='red', gimbal=True, lock_channels=['v', 's'],
                                                 connection=['parentCons'])

        # ==============================================================================================================
        #                               POINT CONSTRAINT ROOT AND SPINE IK UP TO SPINE IK LOW
        # ==============================================================================================================
        # point constraint IK Low
        ik_low_point_constraint = mc.pointConstraint(self.controller_root.control_gimbal,
                                                     self.controller_spine_ik_up.control_gimbal,
                                                     self.controller_spine_ik_low.parent_control[0], mo=1)

        # constraint rename
        au.constraint_rename(ik_low_point_constraint)

        ### CREATE CONTROL FK/IK SETUP
        self.controller_FkIk_spine_setup = ct.Control(match_obj_first_position=root_jnt, prefix=prefix_spine_setup,
                                                      shape=ct.STICKCIRCLE,
                                                      groups_ctrl=['Zro'], side=side, ctrl_size=scale * 0.5,
                                                      ctrl_color='navy', lock_channels=['v', 't', 'r', 's'])
        # rotate the controller
        rc.change_position(self.controller_FkIk_spine_setup.control, 'xz')
        rc.change_position(self.controller_FkIk_spine_setup.control, '-')

        # parent to root gimbal ctrl
        mc.parent(self.controller_FkIk_spine_setup.parent_control[0], self.controller_root.control_gimbal)

        # ==============================================================================================================
        #                               ADD ATTRIBUTE FOR FK/IK SETUP CONTROLLER
        # ==============================================================================================================
        # add attribute FK/IK
        au.add_attr_transform(self.controller_FkIk_spine_setup.control, 'FkIk', 'long', keyable=True, min=0, max=1,
                              dv=0)

        # create reverse node for FK on/off
        spine_setup_reverse = mc.createNode('reverse', n='spineFkIk01_rev')

        # set on/off attribute FK
        au.connect_part_object(obj_base_connection='FkIk', target_connection='inputX',
                               obj_name=self.controller_FkIk_spine_setup.control,
                               target_name=[spine_setup_reverse], select_obj=False)

        au.connect_part_object(obj_base_connection='outputX', target_connection='visibility',
                               obj_name=spine_setup_reverse,
                               target_name=[self.controller_spine_fk_low.parent_control[0]], select_obj=False)

        # set on/off attribute IK
        au.connect_part_object(obj_base_connection='FkIk', target_connection='visibility',
                               obj_name=self.controller_FkIk_spine_setup.control,
                               target_name=[self.controller_spine_ik_low.parent_control[0],
                                            self.controller_spine_ik_up.parent_control[0]],
                               select_obj=False)

        ### setup UP controller set to IK
        au.connect_part_object(obj_base_connection='FkIk',
                               target_connection='%s%s' % (self.controller_spine_ik_up.control_gimbal, 'W1'),
                               obj_name=self.controller_FkIk_spine_setup.control,
                               target_name=[self.controller_spine_ik_up.connection['parentCons'][0]],
                               select_obj=False)

        ## setup UP controller set to FK
        au.connect_part_object(obj_base_connection='outputX',
                               target_connection='%s%s' % (self.controller_spine_fk_up.control_gimbal, 'W0'),
                               obj_name=spine_setup_reverse,
                               target_name=[self.controller_spine_fk_up.connection['parentCons'][0]],
                               select_obj=False)

        # Add attributes: Extra attributes
        au.add_attribute(objects=[self.controller_FkIk_spine_setup.control], long_name=['detailCtrl'],
                         at="long", min=0, max=1, dv=0, channel_box=True)

        # Add attributes: Scale spine
        au.add_attribute(objects=[self.controller_FkIk_spine_setup.control], long_name=['spineScale'], nice_name=[' '],
                         at="enum",
                         en='Spine Scale', channel_box=True)

        au.add_attribute(objects=[self.controller_FkIk_spine_setup.control], long_name=['spineScaleX'],
                         at="float", dv=1, keyable=True)
        au.add_attribute(objects=[self.controller_FkIk_spine_setup.control], long_name=['spineScaleY'],
                         at="float", dv=1, keyable=True)
        au.add_attribute(objects=[self.controller_FkIk_spine_setup.control], long_name=['spineScaleZ'],
                         at="float", dv=1, keyable=True)
        # ==============================================================================================================
        #                                               IF DEFORM TRUE
        # ==============================================================================================================
        if detail_spine_deformer:
            ### ADD ATTRIBUTES ON CTRL FLEX SPINE AND FOR CONNECTING TO DEFORMER
            au.add_attribute(objects=[self.controller_FkIk_spine_setup.control], long_name=['squash'], nice_name=[' '],
                             at="enum",
                             en='Squash IK', channel_box=True)

            au.add_attr_transform(self.controller_FkIk_spine_setup.control, 'autoSquash', 'long', keyable=True, min=0,
                                  max=1, dv=0)

            # Add attributes: Volume attributes
            au.add_attribute(objects=[self.controller_FkIk_spine_setup.control], long_name=['volumeSep'],
                             nice_name=[' '],
                             at="enum", en='Volume', channel_box=True)
            au.add_attribute(objects=[self.controller_FkIk_spine_setup.control], long_name=['volume'],
                             at="float", min=-1, max=1, keyable=True)
            au.add_attribute(objects=[self.controller_FkIk_spine_setup.control], long_name=['volumeMultiplier'],
                             at="float", min=1, dv=3, keyable=True)
            au.add_attribute(objects=[self.controller_FkIk_spine_setup.control], long_name=['startDropoff'],
                             at="float", min=0, max=1, dv=1, keyable=True)
            au.add_attribute(objects=[self.controller_FkIk_spine_setup.control], long_name=['endDropoff'],
                             at="float", min=0, max=1, dv=1, keyable=True)
            au.add_attribute(objects=[self.controller_FkIk_spine_setup.control], long_name=['volumeScale'],
                             at="float", min=-3 * 0.5, max=3 * 2, keyable=True)
            au.add_attribute(objects=[self.controller_FkIk_spine_setup.control], long_name=['volumePosition'],
                             min=-1, max=1, at="float", keyable=True)

            # Add attributes: Sine attributes
            au.add_attribute(objects=[self.controller_FkIk_spine_setup.control], long_name=['sineSep'], nice_name=[' '],
                             attributeType='enum', en="Sine", channel_box=True)

            au.add_attribute(objects=[self.controller_FkIk_spine_setup.control], long_name=['amplitude'],
                             attributeType="float", keyable=True)
            au.add_attribute(objects=[self.controller_FkIk_spine_setup.control], long_name=['offset'],
                             attributeType="float", keyable=True)
            au.add_attribute(objects=[self.controller_FkIk_spine_setup.control], long_name=['twist'],
                             attributeType="float", keyable=True)
            au.add_attribute(objects=[self.controller_FkIk_spine_setup.control], long_name=['sineLength'], min=0.1,
                             dv=2,
                             attributeType="float", keyable=True)

        ### PARENT THE ROOT TO FK/IK CONTROL
        mc.parent(self.controller_spine_fk_low.parent_control[0], self.controller_spine_ik_low.parent_control[0],
                  self.controller_spine_ik_up.parent_control[0], self.controller_pelvis.parent_control[0],
                  self.controller_root.control_gimbal)
