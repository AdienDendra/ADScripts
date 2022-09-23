from __future__ import absolute_import

import maya.cmds as cmds

from rigging.library.utils import snapJoint as rlu_snapJoint


class MessageAttribute:
    def __init__(self, fkik_ctrl, ball=False):

        if not cmds.objExists('%s.%s' % (fkik_ctrl, 'middle_ref_jnt')):
            self.middle_ref_message_jnt = self.add_attr_transform(obj=fkik_ctrl, attr_name='middle_ref_jnt',
                                                                  attr_type='message')
        if not cmds.objExists('%s.%s' % (fkik_ctrl, 'lower_ref_jnt')):
            self.lower_ref_message_jnt = self.add_attr_transform(obj=fkik_ctrl, attr_name='lower_ref_jnt',
                                                                 attr_type='message')

        if not cmds.objExists('%s.%s' % (fkik_ctrl, 'upper_limb_jnt')):
            self.upper_limb_jnt = self.add_attr_transform(obj=fkik_ctrl, attr_name='upper_limb_jnt',
                                                          attr_type='message')

        if not cmds.objExists('%s.%s' % (fkik_ctrl, 'middle_limb_jnt')):
            self.middle_limb_jnt = self.add_attr_transform(obj=fkik_ctrl, attr_name='middle_limb_jnt',
                                                           attr_type='message')

        if not cmds.objExists('%s.%s' % (fkik_ctrl, 'lower_limb_jnt')):
            self.lower_limb_jnt = self.add_attr_transform(obj=fkik_ctrl, attr_name='lower_limb_jnt',
                                                          attr_type='message')

        if not cmds.objExists('%s.%s' % (fkik_ctrl, 'upper_limb_fk_ctrl')):
            self.upper_limb_fk_ctrl = self.add_attr_transform(obj=fkik_ctrl, attr_name='upper_limb_fk_ctrl',
                                                              attr_type='message')

        if not cmds.objExists('%s.%s' % (fkik_ctrl, 'middle_limb_fk_ctrl')):
            self.middle_limb_fk_ctrl = self.add_attr_transform(obj=fkik_ctrl, attr_name='middle_limb_fk_ctrl',
                                                               attr_type='message')

        if not cmds.objExists('%s.%s' % (fkik_ctrl, 'lower_limb_fk_ctrl')):
            self.lower_limb_fk_ctrl = self.add_attr_transform(obj=fkik_ctrl, attr_name='lower_limb_fk_ctrl',
                                                              attr_type='message')

        if not cmds.objExists('%s.%s' % (fkik_ctrl, 'upper_limb_ik_ctrl')):
            self.upper_limb_ik_ctrl = self.add_attr_transform(obj=fkik_ctrl, attr_name='upper_limb_ik_ctrl',
                                                              attr_type='message')

        if not cmds.objExists('%s.%s' % (fkik_ctrl, 'poleVector_ctrl')):
            self.poleVector_ctrl = self.add_attr_transform(obj=fkik_ctrl, attr_name='poleVector_ctrl',
                                                           attr_type='message')

        if not cmds.objExists('%s.%s' % (fkik_ctrl, 'lower_limb_ik_ctrl')):
            self.lower_limb_ik_ctrl = self.add_attr_transform(obj=fkik_ctrl, attr_name='lower_limb_ik_ctrl',
                                                              attr_type='message')

        if not cmds.objExists('%s.%s' % (fkik_ctrl, 'fk_ik_arm_ctrl')):
            self.fk_ik_arm_ctrl = self.add_attr_transform(obj=fkik_ctrl, attr_name='fk_ik_arm_ctrl',
                                                          attr_type='message')

        if not cmds.objExists('%s.%s' % (fkik_ctrl, 'fk_ik_leg_ctrl')):
            self.fk_ik_leg_ctrl = self.add_attr_transform(obj=fkik_ctrl, attr_name='fk_ik_leg_ctrl',
                                                          attr_type='message')
        if ball:
            if not cmds.objExists('%s.%s' % (fkik_ctrl, 'end_limb_fk_jnt')):
                self.end_limb_fk_jnt = self.add_attr_transform(obj=fkik_ctrl, attr_name='end_limb_fk_jnt',
                                                               attr_type='message')
            if not cmds.objExists('%s.%s' % (fkik_ctrl, 'end_limb_jnt')):
                self.end_limb_jnt = self.add_attr_transform(obj=fkik_ctrl, attr_name='end_limb_jnt',
                                                            attr_type='message')

            if not cmds.objExists('%s.%s' % (fkik_ctrl, 'end_limb_fk_ctrl')):
                self.end_limb_fk_ctrl = self.add_attr_transform(obj=fkik_ctrl, attr_name='end_limb_fk_ctrl',
                                                                attr_type='message')
            if not cmds.objExists('%s.%s' % (fkik_ctrl, 'toe_wiggle_attr')):
                self.toe_wiggle_attr = self.add_attr_transform(obj=fkik_ctrl, attr_name='toe_wiggle_attr',
                                                               attr_type='message')

    def connect_message_to_attribute(self, object_target, fkik_ctrl, object_connector):
        cmds.connectAttr('%s.message' % (object_target), '%s.%s' % (fkik_ctrl, object_connector))

    # add attribute on transform
    def add_attr_transform(self, obj, attr_name, attr_type, edit=False, keyable=False, channel_box=False, **kwargs):
        if cmds.nodeType(obj) == "transform":
            cmds.addAttr(obj, ln=attr_name, at=attr_type, **kwargs)
            cmds.setAttr('%s.%s' % (obj, attr_name), e=edit, k=keyable, cb=channel_box)
            return attr_name
        else:
            cmds.error('object is not transform')

    def add_joint_reference(self, upper_limb_jnt, middle_limb_jnt, lower_limb_jnt, side_LFT, side_RGT, side):
        upper_ref_joint = rlu_snapJoint.joint(limb_jnt=upper_limb_jnt, side_LFT=side_LFT, side_RGT=side_RGT, side=side)
        self.middle_ref_joint = rlu_snapJoint.joint(limb_jnt=middle_limb_jnt, side_LFT=side_LFT, side_RGT=side_RGT,
                                                    side=side)
        self.lower_ref_joint = rlu_snapJoint.joint(limb_jnt=lower_limb_jnt, side_LFT=side_LFT, side_RGT=side_RGT,
                                                   side=side)

        # parent
        cmds.parent(self.lower_ref_joint, self.middle_ref_joint)
        cmds.parent(self.middle_ref_joint, upper_ref_joint)

        # lock attribute
