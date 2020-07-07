from __builtin__ import reload

import maya.cmds as mc

from rigging.library.utils import controller as ct
from rigging.library.utils import transform as tf
from rigging.tools import AD_utils as au

reload (ct)
reload (tf)
reload (au)

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
        group_driver = mc.group(em=1, n='chinJoint' + '_grp')
        setup_driver_grp = mc.group(em=1, n='chinSetup' + '_grp')
        ctrl_driver_grp = mc.group(em=1, n='chinCtrlAll' + '_grp')

        mc.hide(setup_driver_grp)
        cheek_all_grp = mc.group(em=1, n='chin' + '_grp')
        mc.parent(group_driver, setup_driver_grp, cheek_all_grp)
        mc.parent(ctrl_driver_grp, face_anim_ctrl_grp)
        mc.parent(cheek_all_grp, face_utils_grp)

        self.group_driver = group_driver
        self.setup_driver_grp = setup_driver_grp
        self.ctrl_driver_grp = ctrl_driver_grp

    # ==================================================================================================================
    #                                                   CHIN AND MENTOLABIAL DRIVER
    # ==================================================================================================================

        mentolabial_ctrl = self.controller_setup(object_joint=mentolabial_jnt, object_prefix=mentolabial_prefix, scale=scale,
                                                 constraint=[lower_lip_bind_jnt, jaw_jnt], w=[0.5, 0.5], jaw_ctrl=jaw_jnt,
                                                 suffix_controller=suffix_controller)

        chin_ctrl = self.controller_setup(object_joint=chin_jnt, object_prefix=chin_prefix, scale=scale,
                                          constraint=[jaw_jnt], w=[1.0], jaw_ctrl=jaw_jnt, suffix_controller=suffix_controller)

        self.chin_ctrl = chin_ctrl[0]
        self.chin_ctrl_grp = chin_ctrl[1]
        self.mentolabial_ctrl_grp = mentolabial_ctrl[1]

    def controller_setup(self, object_joint, object_prefix, scale, constraint, w, jaw_ctrl, suffix_controller):
        # create controller
        object_ctrl = ct.Control(match_obj_first_position=object_joint,
                                 prefix=object_prefix,
                                 shape=ct.JOINT, groups_ctrl=['', 'Offset'],
                                 ctrl_size=scale * 0.05, suffix=suffix_controller,
                                 ctrl_color='red', lock_channels=['v'])

        self.object_ctrl = object_ctrl.control
        self.object_parent_ctrl_grp = object_ctrl.parent_control[0]
        self.object_parent_ctrl_grp_offset = object_ctrl.parent_control[1]

        # ROTATE CONTROLLER OFFSET
        mc.setAttr(self.object_parent_ctrl_grp_offset + '.scaleY', -1)

        # CREATE GRP JOINT
        self.object_joint_grp = tf.create_parent_transform(['', 'Offset'], match_position=object_joint, object=object_joint,
                                                           prefix=object_joint, suffix=object_joint
                                                           )

        # CREATE DRIVER
        driver_grp = mc.group(em=1, n=au.prefix_name(object_prefix) + '_set')
        driver = mc.spaceLocator(n=au.prefix_name(object_prefix) + 'Drv' + '_set')[0]
        mc.parent(driver, driver_grp)
        mc.delete(mc.parentConstraint(object_joint, driver_grp, mo=0))

        mc.setAttr(driver+'.localScaleX', 0.5*scale)
        mc.setAttr(driver+'.localScaleY', 0.5*scale)
        mc.setAttr(driver+'.localScaleZ', 0.5*scale)

        # CONSTRAINING THE OBJECT
        pac_constraint = None
        for cons, value in zip(constraint, w):
            pac_constraint = mc.parentConstraint(cons, driver_grp, mo=1, w=value)

        scale_constraint = mc.scaleConstraint(jaw_ctrl, driver_grp, mo=1)

        # RENAME CONSTRAINT
        au.constraint_rename([pac_constraint[0], scale_constraint[0]])

        # CONNECT BIND PARENT GRP TO CTRL GRP
        au.connect_attr_object(driver_grp, self.object_joint_grp[0])
        au.connect_attr_object(self.object_joint_grp[0], self.object_parent_ctrl_grp)

        # CONNECT CTRL TO JOINT
        reverse_trans = mc.createNode('multiplyDivide', n=au.prefix_name(object_prefix) + 'ReverseTrans' + '_mdn')
        reverse_rotate = mc.createNode('multiplyDivide', n=au.prefix_name(object_prefix) + 'ReverseRot' + '_mdn')

        mc.setAttr(reverse_trans + '.input2X', 1)
        mc.setAttr(reverse_trans + '.input2Y', -1)
        mc.setAttr(reverse_trans + '.input2Z', 1)
        mc.setAttr(reverse_rotate + '.input2X', -1)
        mc.setAttr(reverse_rotate + '.input2Y', 1)
        mc.setAttr(reverse_rotate + '.input2Z', -1)

        mc.connectAttr(self.object_ctrl + '.translate', reverse_trans + '.input1')
        mc.connectAttr(reverse_trans + '.output', object_joint + '.translate')
        mc.connectAttr(self.object_ctrl + '.rotate', reverse_rotate + '.input1')
        mc.connectAttr(reverse_rotate + '.output', object_joint + '.rotate')

        au.connect_attr_scale(self.object_ctrl, object_joint)

        # PARENT TO GROUP
        mc.parent(driver_grp, self.setup_driver_grp)
        mc.parent(self.object_joint_grp[0], self.group_driver)

        mc.parent(self.object_parent_ctrl_grp, self.ctrl_driver_grp)

        return object_ctrl.control, object_ctrl.parent_control[0]

