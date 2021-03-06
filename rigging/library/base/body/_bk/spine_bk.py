"""
creating spine module base
"""
import maya.cmds as mc
from rigLib.utils import rotation_controller as rc, controller as ct

from rigging.tools import AD_utils as au

reload (ct)
reload (au)
reload (rc)

class Build:
    def __init__(self,
                 spineJnt,
                 pelvisJnt,
                 rootJnt,
                 scale,
                 prefixSpineSetup,
                 detailSpineDeformer=True,
                 ):

    ### CREATE CONTROL PELVIS AND ROOT
        self.controllerRoot     = ct.Control(match_obj_first_position=rootJnt, prefix='hip', shape=ct.SQUAREPLUS,
                                             groups_ctrl=['Zro', 'Offset'], ctrl_size=scale * 1.2,
                                             ctrl_color='chocholate', gimbal=True, lock_channels=['v', 's'], connection=['parentCons'])

        self.controllerPelvis   = ct.Control(match_obj_first_position=pelvisJnt, prefix='pelvis', shape=ct.SQUAREPLUS,
                                             groups_ctrl=['Zro', 'Offset'], ctrl_size= scale,
                                             ctrl_color='yellow', gimbal=True, lock_channels=['v', 's'], connection=['parentCons'])
    ### CREATE CONTROL FK
        self.controllerSpineFKLow   = ct.Control(match_obj_first_position=spineJnt[0], prefix='spineFk01', shape=ct.CIRCLEPLUS,
                                                 groups_ctrl=['Zro', 'Offset'], ctrl_size=scale,
                                                 ctrl_color='yellow', gimbal=True, lock_channels=['v', 's'])

        self.controllerSpineFKMid   = ct.Control(match_obj_first_position=spineJnt[1], prefix='spineFk02', shape=ct.CIRCLEPLUS,
                                                 groups_ctrl=['Zro', 'Offset'], ctrl_size=scale,
                                                 ctrl_color='yellow', gimbal=True, lock_channels=['v', 's'])

        self.controllerSpineFKUp    = ct.Control(match_obj_first_position=spineJnt[3], prefix='spineFk03', shape=ct.CIRCLEPLUS,
                                                 groups_ctrl=['Zro', 'Offset'], ctrl_size=scale,
                                                 ctrl_color='yellow', gimbal=True, lock_channels=['v', 's'], connection=['parentCons'])

        # parent the controller FK from up to low
        mc.parent(self.controllerSpineFKUp.parent_control[0], self.controllerSpineFKMid.control_gimbal)
        mc.parent(self.controllerSpineFKMid.parent_control[0], self.controllerSpineFKLow.control_gimbal)

    ### CREATE CONTROL IK
        self.controllerSpineIKLow = ct.Control(match_obj_first_position=spineJnt[1], prefix='spineIk01', shape=ct.CIRCLEPLUS,
                                               groups_ctrl=['Zro', 'Offset'], ctrl_size=scale,
                                               ctrl_color='red', gimbal=True, lock_channels=['v', 's'])
        self.controllerSpineIKUp = ct.Control(match_obj_first_position=spineJnt[3], prefix='spineIk02', shape=ct.CIRCLEPLUS,
                                              groups_ctrl=['Zro', 'Offset'], ctrl_size=scale,
                                              ctrl_color='red', gimbal=True, lock_channels=['v', 's'], connection=['parentCons'])

    ### POINT CONSTRAINT ROOT AND SPINE IK UP TO SPINE IK LOW
        # point constraint IK Low
        mc.pointConstraint(self.controllerRoot.control_gimbal, self.controllerSpineIKUp.control_gimbal,
                           self.controllerSpineIKLow.parent_control[0], mo=1)

        ### CREATE CONTROL FK/IK SETUP
        self.controllerFKIKSpineSetup = ct.Control(match_obj_first_position=rootJnt, prefix=prefixSpineSetup, shape=ct.STICKCIRCLE,
                                                   groups_ctrl=['Zro'], ctrl_size=scale * 0.5,
                                                   ctrl_color='navy', lock_channels=['v', 't', 'r', 's'])
        # rotate the controller
        rc.change_position(self.controllerFKIKSpineSetup.control, 'xz')
        rc.change_position(self.controllerFKIKSpineSetup.control, '-')

        ### ADD ATTRIBUTE FOR FK/IK SETUP CONTROLLER
        # add attribute FK/IK
        au.add_attr_transform(self.controllerFKIKSpineSetup.control, 'FkIk', 'long', keyable=True, min=0, max=1, dv=0)

        # create reverse node for FK on/off
        spineSetupRevs = mc.createNode('reverse', n='spineFkIk01_rev')

        # set on/off attribute FK
        au.connect_part_object(obj_base_connection='FkIk', target_connection='inputX', obj_name=self.controllerFKIKSpineSetup.control,
                               target_name= [spineSetupRevs], select_obj= False)

        au.connect_part_object(obj_base_connection='outputX', target_connection='visibility', obj_name=spineSetupRevs,
                               target_name= [self.controllerSpineFKLow.parent_control[0]], select_obj= False)

        # set on/off attribute IK
        au.connect_part_object(obj_base_connection='FkIk', target_connection='visibility', obj_name=self.controllerFKIKSpineSetup.control,
                               target_name= [self.controllerSpineIKLow.parent_control[0], self.controllerSpineIKUp.parent_control[0]],
                               select_obj= False)

     ### setup UP controller set to IK
        au.connect_part_object(obj_base_connection='FkIk', target_connection='%s%s' % (self.controllerSpineIKUp.control_gimbal, 'W1'),
                               obj_name=self.controllerFKIKSpineSetup.control,
                               target_name=[self.controllerSpineIKUp.connection['parentCons'][0]],
                               select_obj=False)

        ## setup UP controller set to FK
        au.connect_part_object(obj_base_connection='outputX', target_connection='%s%s' % (self.controllerSpineFKUp.control_gimbal, 'W0'),
                               obj_name=spineSetupRevs, target_name=[self.controllerSpineFKUp.connection['parentCons'][0]],
                               select_obj=False)

        # Add attributes: Extra attributes
        au.add_attribute(objects=[self.controllerFKIKSpineSetup.control], long_name=['detailCtrl'],
                         at="long", min=0, max=1, dv=0, channel_box=True)

        if detailSpineDeformer:
            ### ADD ATTRIBUTES ON CTRL FLEX SPINE AND FOR CONNECTING TO DEFORMER

            au.add_attribute(objects=[self.controllerFKIKSpineSetup.control], long_name=['squash'], nice_name=[' '], at="enum",
                             en='Squash IK', channel_box=True)

            au.add_attr_transform(self.controllerFKIKSpineSetup.control, 'autoSquash', 'long', keyable=True, min=0, max=1, dv=0)

            # Add attributes: Volume attributes
            au.add_attribute(objects=[self.controllerFKIKSpineSetup.control], long_name=['volumeSep'], nice_name=[' '],
                             at="enum", en='Volume', channel_box=True)
            au.add_attribute(objects=[self.controllerFKIKSpineSetup.control], long_name=['volume'],
                             at="float", min=-1, max=1, keyable=True)
            au.add_attribute(objects=[self.controllerFKIKSpineSetup.control], long_name=['volumeMultiplier'],
                             at="float", min=1, dv=3, keyable=True)
            au.add_attribute(objects=[self.controllerFKIKSpineSetup.control], long_name=['startDropoff'],
                             at="float", min=0, max=1, dv=1, keyable=True)
            au.add_attribute(objects=[self.controllerFKIKSpineSetup.control], long_name=['endDropoff'],
                             at="float", min=0, max=1, dv=1, keyable=True)
            au.add_attribute(objects=[self.controllerFKIKSpineSetup.control], long_name=['volumeScale'],
                             at="float", min=-3 * 0.5, max=3 * 2, keyable=True)
            au.add_attribute(objects=[self.controllerFKIKSpineSetup.control], long_name=['volumePosition'],
                             min=-1, max=1, at="float", keyable=True)

            # Add attributes: Sine attributes
            au.add_attribute(objects=[self.controllerFKIKSpineSetup.control], long_name=['sineSep'], nice_name=[' '],
                             attributeType='enum', en="Sine", channel_box=True)

            au.add_attribute(objects=[self.controllerFKIKSpineSetup.control], long_name=['amplitude'],
                             attributeType="float", keyable=True)
            au.add_attribute(objects=[self.controllerFKIKSpineSetup.control], long_name=['offset'],
                             attributeType="float", keyable=True)
            au.add_attribute(objects=[self.controllerFKIKSpineSetup.control], long_name=['twist'],
                             attributeType="float", keyable=True)
            au.add_attribute(objects=[self.controllerFKIKSpineSetup.control], long_name=['sineLength'], min=0.1, dv=2,
                             attributeType="float", keyable=True)

    ### PARENT THE ROOT TO FK/IK CONTROL
        mc.parent(self.controllerSpineFKLow.parent_control[0], self.controllerSpineIKLow.parent_control[0],
                  self.controllerSpineIKUp.parent_control[0], self.controllerPelvis.parent_control[0],
                  self.controllerRoot.control_gimbal)