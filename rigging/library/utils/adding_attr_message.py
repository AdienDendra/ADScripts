import maya.cmds as mc

class MessageAttribute:
    def __init__(self, fkik_ctrl, ball=False):

        if not mc.objExists('%s.%s' % (fkik_ctrl, 'upper_limb_jnt')):
            self.upper_limb_jnt =  self.add_attr_transform(obj=fkik_ctrl, attr_name='upper_limb_jnt',
                                                        attr_type='message')

        if not mc.objExists('%s.%s' % (fkik_ctrl, 'middle_limb_jnt')):
            self.middle_limb_jnt =   self.add_attr_transform(obj=fkik_ctrl, attr_name='middle_limb_jnt',
                                                        attr_type='message')

        if not mc.objExists('%s.%s' % (fkik_ctrl, 'lower_limb_jnt')):
            self.lower_limb_jnt =   self.add_attr_transform(obj=fkik_ctrl, attr_name='lower_limb_jnt',
                                                           attr_type='message')

        if not mc.objExists('%s.%s' % (fkik_ctrl, 'upper_limb_fk_ctrl')):
            self.upper_limb_fk_ctrl =   self.add_attr_transform(obj=fkik_ctrl, attr_name='upper_limb_fk_ctrl',
                                                        attr_type='message')

        if not mc.objExists('%s.%s' % (fkik_ctrl, 'middle_limb_fk_ctrl')):
            self.middle_limb_fk_ctrl =   self.add_attr_transform(obj=fkik_ctrl, attr_name='middle_limb_fk_ctrl',
                                                             attr_type='message')

        if not mc.objExists('%s.%s' % (fkik_ctrl, 'lower_limb_fk_ctrl')):
            self.lower_limb_fk_ctrl =   self.add_attr_transform(obj=fkik_ctrl, attr_name='lower_limb_fk_ctrl',
                                                        attr_type='message')

        if not mc.objExists('%s.%s' % (fkik_ctrl, 'upper_limb_ik_ctrl')):
            self.upper_limb_ik_ctrl =   self.add_attr_transform(obj=fkik_ctrl, attr_name='upper_limb_ik_ctrl',
                                                        attr_type='message')

        if not mc.objExists('%s.%s' % (fkik_ctrl, 'poleVector_ctrl')):
            self.poleVector_ctrl =   self.add_attr_transform(obj=fkik_ctrl, attr_name='poleVector_ctrl', attr_type='message')

        if not mc.objExists('%s.%s' % (fkik_ctrl, 'lower_limb_ik_ctrl')):
            self.lower_limb_ik_ctrl =   self.add_attr_transform(obj=fkik_ctrl, attr_name='lower_limb_ik_ctrl',
                                                        attr_type='message')

        if not mc.objExists('%s.%s' % (fkik_ctrl, 'fk_ik_arm_ctrl')):
            self.fk_ik_arm_ctrl =   self.add_attr_transform(obj=fkik_ctrl, attr_name='fk_ik_arm_ctrl',
                                                        attr_type='message')

        if not mc.objExists('%s.%s' % (fkik_ctrl, 'fk_ik_leg_ctrl')):
            self.fk_ik_leg_ctrl =   self.add_attr_transform(obj=fkik_ctrl, attr_name='fk_ik_leg_ctrl',
                                                        attr_type='message')
        if ball:
            if not mc.objExists('%s.%s' % (fkik_ctrl, 'end_limb_fk_jnt')):
                self.end_limb_fk_jnt =   self.add_attr_transform(obj=fkik_ctrl, attr_name='end_limb_fk_jnt',
                                                         attr_type='message')
            if not mc.objExists('%s.%s' % (fkik_ctrl, 'end_limb_jnt')):
                self.end_limb_jnt =   self.add_attr_transform(obj=fkik_ctrl, attr_name='end_limb_jnt',
                                                             attr_type='message')

            if not mc.objExists('%s.%s' % (fkik_ctrl, 'end_limb_fk_ctrl')):
                self.end_limb_fk_ctrl =   self.add_attr_transform(obj=fkik_ctrl, attr_name='end_limb_fk_ctrl',
                                                          attr_type='message')
            if not mc.objExists('%s.%s' % (fkik_ctrl, 'toe_wiggle_attr')):
                self.toe_wiggle_attr =   self.add_attr_transform(obj=fkik_ctrl, attr_name='toe_wiggle_attr',
                                                         attr_type='message')

    def connect_message_to_attribute(self, object_connector, fkik_ctrl, object_target):
        mc.connectAttr('%s.message' % (object_connector), '%s.%s' % (fkik_ctrl, object_target))

    # add attribute on transform
    def add_attr_transform(self, obj, attr_name, attr_type, edit=False, keyable=False, channel_box=False, **kwargs):
        if mc.nodeType(obj) == "transform":
            mc.addAttr(obj, ln=attr_name, at=attr_type, **kwargs)
            mc.setAttr('%s.%s' % (obj, attr_name), e=edit, k=keyable, cb=channel_box)
            return attr_name
        else:
            mc.error('object is not transform')
