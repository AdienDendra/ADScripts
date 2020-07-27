from __builtin__ import reload

import maya.cmds as mc
from rigging.tools import AD_utils as au

reload(au)

class MessageAttribute:
    def __init__(self, fkik_ctrl, ball=False):

        if not mc.objExists('%s.%s' % (fkik_ctrl, 'middle_limb_jnt')):
            self.middle_limb_jnt = au.add_attr_transform(obj=fkik_ctrl, attr_name='middle_limb_jnt',
                                                        attr_type='message')

        if not mc.objExists('%s.%s' % (fkik_ctrl, 'lower_limb_jnt')):
            self.lower_limb_jnt = au.add_attr_transform(obj=fkik_ctrl, attr_name='lower_limb_jnt',
                                                           attr_type='message')

        if not mc.objExists('%s.%s' % (fkik_ctrl, 'upper_limb_fk_jnt')):
            self.upper_limb_fk_jnt = au.add_attr_transform(obj=fkik_ctrl, attr_name='upper_limb_fk_jnt',
                                                           attr_type='message')

        if not mc.objExists('%s.%s' % (fkik_ctrl, 'middle_limb_fk_jnt')):
            self.middle_limb_fk_jnt = au.add_attr_transform(obj=fkik_ctrl, attr_name='middle_limb_fk_jnt',
                                                        attr_type='message')

        if not mc.objExists('%s.%s' % (fkik_ctrl, 'lower_limb_fk_jnt')):
            self.lower_limb_fk_jnt = au.add_attr_transform(obj=fkik_ctrl, attr_name='lower_limb_fk_jnt',
                                                           attr_type='message')

        if not mc.objExists('%s.%s' % (fkik_ctrl, 'upper_limb_ik_jnt')):
            self.upper_limb_ik_jnt = au.add_attr_transform(obj=fkik_ctrl, attr_name='upper_limb_ik_jnt',
                                                       attr_type='message')

        if not mc.objExists('%s.%s' % (fkik_ctrl, 'middle_limb_ik_jnt')):
            self.middle_limb_ik_jnt = au.add_attr_transform(obj=fkik_ctrl, attr_name='middle_limb_ik_jnt',
                                                        attr_type='message')

        if not mc.objExists('%s.%s' % (fkik_ctrl, 'lower_limb_ik_jnt')):
            self.lower_limb_ik_jnt = au.add_attr_transform(obj=fkik_ctrl, attr_name='lower_limb_ik_jnt',
                                                       attr_type='message')

        if not mc.objExists('%s.%s' % (fkik_ctrl, 'upper_limb_fk_ctrl')):
            self.upper_limb_fk_ctrl = au.add_attr_transform(obj=fkik_ctrl, attr_name='upper_limb_fk_ctrl',
                                                        attr_type='message')

        if not mc.objExists('%s.%s' % (fkik_ctrl, 'middle_limb_fk_ctrl')):
            self.middle_limb_fk_ctrl = au.add_attr_transform(obj=fkik_ctrl, attr_name='middle_limb_fk_ctrl',
                                                             attr_type='message')

        if not mc.objExists('%s.%s' % (fkik_ctrl, 'lower_limb_fk_ctrl')):
            self.lower_limb_fk_ctrl = au.add_attr_transform(obj=fkik_ctrl, attr_name='lower_limb_fk_ctrl',
                                                        attr_type='message')

        if not mc.objExists('%s.%s' % (fkik_ctrl, 'upper_limb_ik_ctrl')):
            self.upper_limb_ik_ctrl = au.add_attr_transform(obj=fkik_ctrl, attr_name='upper_limb_ik_ctrl',
                                                        attr_type='message')

        if not mc.objExists('%s.%s' % (fkik_ctrl, 'poleVector_ctrl')):
            self.poleVector_ctrl = au.add_attr_transform(obj=fkik_ctrl, attr_name='poleVector_ctrl', attr_type='message')

        if not mc.objExists('%s.%s' % (fkik_ctrl, 'lower_limb_ik_ctrl')):
            self.lower_limb_ik_ctrl = au.add_attr_transform(obj=fkik_ctrl, attr_name='lower_limb_ik_ctrl',
                                                        attr_type='message')

        if not mc.objExists('%s.%s' % (fkik_ctrl, 'upper_limb_snap_jnt')):
            self.upper_limb_snap_jnt = au.add_attr_transform(obj=fkik_ctrl, attr_name='upper_limb_snap_jnt',
                                                        attr_type='message')

        if not mc.objExists('%s.%s' % (fkik_ctrl, 'middle_limb_snap_jnt')):
            self.middle_limb_snap_jnt = au.add_attr_transform(obj=fkik_ctrl, attr_name='middle_limb_snap_jnt',
                                                        attr_type='message')

        if not mc.objExists('%s.%s' % (fkik_ctrl, 'lower_limb_snap_jnt')):
            self.lower_limb_snap_jnt = au.add_attr_transform(obj=fkik_ctrl, attr_name='lower_limb_snap_jnt',
                                                        attr_type='message')

        if ball:
            if not mc.objExists('%s.%s' % (fkik_ctrl, 'end_limb_fk_jnt')):
                self.end_limb_fk_jnt = au.add_attr_transform(obj=fkik_ctrl, attr_name='end_limb_fk_jnt',
                                                         attr_type='message')
            if not mc.objExists('%s.%s' % (fkik_ctrl, 'end_limb_ik_jnt')):
                self.end_limb_ik_jnt = au.add_attr_transform(obj=fkik_ctrl, attr_name='end_limb_ik_jnt',
                                                         attr_type='message')
            if not mc.objExists('%s.%s' % (fkik_ctrl, 'end_limb_fk_ctrl')):
                self.end_limb_fk_ctrl = au.add_attr_transform(obj=fkik_ctrl, attr_name='end_limb_fk_ctrl',
                                                          attr_type='message')
            if not mc.objExists('%s.%s' % (fkik_ctrl, 'toe_wiggle_attr')):
                self.toe_wiggle_attr = au.add_attr_transform(obj=fkik_ctrl, attr_name='toe_wiggle_attr',
                                                         attr_type='message')

            if not mc.objExists('%s.%s' % (fkik_ctrl, 'end_limb_snap_jnt')):
                self.end_limb_snap_jnt = au.add_attr_transform(obj=fkik_ctrl, attr_name='end_limb_snap_jnt',
                                                                 attr_type='message')

    def connect_message_to_attribute(self, object_connector, fkik_ctrl, object_target):
        mc.connectAttr('%s.message' % (object_connector), '%s.%s' % (fkik_ctrl, object_target))
