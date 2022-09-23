from __future__ import absolute_import

import maya.cmds as cmds

from rigging.library.utils import controller as rlu_controller, transform as rlu_transform
from rigging.tools import utils as rt_utils


class Chin:
    def __init__(self,
                 mentolabial_jnt,
                 mentolabial_prefix,
                 chin_jnt,
                 chin_prefix,
                 scale,
                 face_anim_ctrl_grp,
                 face_utils_grp,
                 lower_lip_bind_jnt,
                 jaw_jnt,
                 suffix_controller
                 ):
        # group cheek driver
        group_driver = cmds.group(em=1, n='chinJoint' + '_grp')
        setup_driver_grp = cmds.group(em=1, n='chinSetup' + '_grp')
        ctrl_driver_grp = cmds.group(em=1, n='chinCtrlAll' + '_grp')

        cmds.hide(setup_driver_grp)
        cheek_all_grp = cmds.group(em=1, n='chin' + '_grp')
        cmds.parent(group_driver, setup_driver_grp, cheek_all_grp)
        cmds.parent(ctrl_driver_grp, face_anim_ctrl_grp)
        cmds.parent(cheek_all_grp, face_utils_grp)

        self.group_driver = group_driver
        self.setup_driver_grp = setup_driver_grp
        self.ctrl_driver_grp = ctrl_driver_grp

        # ==================================================================================================================
        #                                                   CHIN AND MENTOLABIAL DRIVER
        # ==================================================================================================================

        mentolabial_ctrl = self.controller_setup(object_joint=mentolabial_jnt, object_prefix=mentolabial_prefix,
                                                 scale=scale,
                                                 constraint=[lower_lip_bind_jnt, jaw_jnt], w=[0.5, 0.5],
                                                 jaw_ctrl=jaw_jnt,
                                                 suffix_controller=suffix_controller)

        chin_ctrl = self.controller_setup(object_joint=chin_jnt, object_prefix=chin_prefix, scale=scale,
                                          constraint=[jaw_jnt], w=[1.0], jaw_ctrl=jaw_jnt,
                                          suffix_controller=suffix_controller)

        self.chin_ctrl = chin_ctrl[0]
        self.chin_ctrl_grp = chin_ctrl[1]
        self.mentolabial_ctrl_grp = mentolabial_ctrl[1]

    def controller_setup(self, object_joint, object_prefix, scale, constraint, w, jaw_ctrl, suffix_controller):
        # create controller
        object_ctrl = rlu_controller.Control(match_obj_first_position=object_joint,
                                             prefix=object_prefix,
                                             shape=rlu_controller.JOINT, groups_ctrl=['', 'Offset'],
                                             ctrl_size=scale * 0.05, suffix=suffix_controller,
                                             ctrl_color='red', lock_channels=['v'])

        self.object_ctrl = object_ctrl.control
        self.object_parent_ctrl_grp = object_ctrl.parent_control[0]
        self.object_parent_ctrl_grp_offset = object_ctrl.parent_control[1]

        # ROTATE CONTROLLER OFFSET
        cmds.setAttr(self.object_parent_ctrl_grp_offset + '.scaleY', -1)

        # CREATE GRP JOINT
        self.object_joint_grp = rlu_transform.create_parent_transform(['', 'Offset'], match_position=object_joint,
                                                                      object=object_joint,
                                                                      prefix=object_joint, suffix=object_joint
                                                                      )

        # CREATE DRIVER
        driver_grp = cmds.group(em=1, n=rt_utils.prefix_name(object_prefix) + '_set')
        driver = cmds.spaceLocator(n=rt_utils.prefix_name(object_prefix) + 'Drv' + '_set')[0]
        cmds.parent(driver, driver_grp)
        cmds.delete(cmds.parentConstraint(object_joint, driver_grp, mo=0))

        cmds.setAttr(driver + '.localScaleX', 0.5 * scale)
        cmds.setAttr(driver + '.localScaleY', 0.5 * scale)
        cmds.setAttr(driver + '.localScaleZ', 0.5 * scale)

        # CONSTRAINING THE OBJECT
        pac_constraint = None
        for cons, value in zip(constraint, w):
            pac_constraint = cmds.parentConstraint(cons, driver_grp, mo=1, w=value)

        scale_constraint = cmds.scaleConstraint(jaw_ctrl, driver_grp, mo=1)

        # RENAME CONSTRAINT
        rt_utils.constraint_rename([pac_constraint[0], scale_constraint[0]])

        # CONNECT BIND PARENT GRP TO CTRL GRP
        rt_utils.connect_attr_object(driver_grp, self.object_joint_grp[0])
        rt_utils.connect_attr_object(self.object_joint_grp[0], self.object_parent_ctrl_grp)

        # CONNECT CTRL TO JOINT
        reverse_trans = cmds.createNode('multiplyDivide',
                                        n=rt_utils.prefix_name(object_prefix) + 'ReverseTrans' + '_mdn')
        reverse_rotate = cmds.createNode('multiplyDivide',
                                         n=rt_utils.prefix_name(object_prefix) + 'ReverseRot' + '_mdn')

        cmds.setAttr(reverse_trans + '.input2X', 1)
        cmds.setAttr(reverse_trans + '.input2Y', -1)
        cmds.setAttr(reverse_trans + '.input2Z', 1)
        cmds.setAttr(reverse_rotate + '.input2X', -1)
        cmds.setAttr(reverse_rotate + '.input2Y', 1)
        cmds.setAttr(reverse_rotate + '.input2Z', -1)

        cmds.connectAttr(self.object_ctrl + '.translate', reverse_trans + '.input1')
        cmds.connectAttr(reverse_trans + '.output', object_joint + '.translate')
        cmds.connectAttr(self.object_ctrl + '.rotate', reverse_rotate + '.input1')
        cmds.connectAttr(reverse_rotate + '.output', object_joint + '.rotate')

        rt_utils.connect_attr_scale(self.object_ctrl, object_joint)

        # PARENT TO GROUP
        cmds.parent(driver_grp, self.setup_driver_grp)
        cmds.parent(self.object_joint_grp[0], self.group_driver)

        cmds.parent(self.object_parent_ctrl_grp, self.ctrl_driver_grp)

        return object_ctrl.control, object_ctrl.parent_control[0]
