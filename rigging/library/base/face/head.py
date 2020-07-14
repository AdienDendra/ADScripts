from __builtin__ import reload

import maya.cmds as mc

from rigging.library.utils import controller as ct
from rigging.library.utils import transform as tf
from rigging.tools import AD_utils as au

reload (ct)
reload (tf)
reload (au)


class Build:
    def __init__(self,
                 neck_jnt,
                 neck_in_btw_jnt,
                 head_jnt,
                 jaw_tip_jnt,
                 jaw_jnt,
                 head_up_jnt,
                 head_low_jnt,
                 jaw_prefix,
                 jaw_tip_prefix,
                 head_prefix,
                 head_up_prefix,
                 head_low_prefix,
                 neck_prefix,
                 neck_in_between_prefix,
                 scale,
                 upper_teeth_jnt,
                 lower_teeth_jnt,
                 tongue01_jnt,
                 tongue02_jnt,
                 tongue03_jnt,
                 tongue04_jnt,
                 suffix_controller,
                 ):
        # create group jaw
        jaw_direction_grp = mc.group(em=1, n=au.prefix_name(jaw_jnt) + 'Direction_grp')
        self.jaw_direction_grp_offset = mc.group(em=1, n=au.prefix_name(jaw_jnt) + 'DirectionOffset_grp',
                                                 p=jaw_direction_grp)

        mc.select(cl=1)
        mc.delete(mc.parentConstraint(jaw_jnt, jaw_direction_grp))

        ## GROUPING THE JOINT
        self.neck_jnt_grp = tf.create_parent_transform(parent_list=[''], object=neck_jnt, match_position=neck_jnt,
                                                       prefix=neck_prefix, suffix='_jnt')

        self.neck_in_btw_jnt_grp = tf.create_parent_transform(parent_list=[''], object=neck_in_btw_jnt,
                                                              match_position=neck_in_btw_jnt,
                                                              prefix=neck_in_between_prefix, suffix='_jnt')

        tf.create_parent_transform(parent_list=[''], object=head_jnt, match_position=head_jnt,
                                   prefix=head_prefix, suffix='_jnt')
        tf.create_parent_transform(parent_list=[''], object=head_up_jnt, match_position=head_up_jnt,
                                   prefix=head_up_prefix, suffix='_jnt')
        tf.create_parent_transform(parent_list=[''], object=head_low_jnt, match_position=head_low_jnt,
                                   prefix=head_low_prefix, suffix='_jnt')
        tf.create_parent_transform(parent_list=[''], object=jaw_jnt, match_position=jaw_jnt,
                                   prefix=jaw_prefix, suffix='_jnt')
        self.jaw_tip_jnt_grp = tf.create_parent_transform(parent_list=['', 'Offset'], object=jaw_tip_jnt,
                                                          match_position=jaw_tip_jnt,
                                                          prefix=jaw_tip_prefix, suffix='_jnt')

        ## CREATE CONTROLLER FOR THE JOINT
        # NECK
        self.neck_ctrl = ct.Control(match_obj_first_position=neck_jnt, prefix=neck_prefix,
                                    shape=ct.CIRCLEPLUS,
                                    groups_ctrl=['All', 'Offset'], ctrl_size=scale * 1.0,
                                    ctrl_color='red', lock_channels=['v'], gimbal=True, suffix=suffix_controller,
                                    connection=['connectMatrixAll'])
        au.add_attribute(objects=[self.neck_ctrl.control], long_name=['neckInBetween'],
                         nice_name=[' '], at="enum",
                         en='Neck In Btw', channel_box=True)
        neck_in_btw_attr = au.add_attribute(objects=[self.neck_ctrl.control], long_name=['neckInBtwn'],
                                            attributeType="long", min=0, max=1, dv=0, channel_box=True)

        self.neck_in_btw_ctrl = ct.Control(match_obj_first_position=neck_in_btw_jnt, prefix=neck_in_between_prefix,
                                           shape=ct.CIRCLEPLUS,
                                           groups_ctrl=[''], ctrl_size=scale * 1.0,
                                           ctrl_color='lightPink', lock_channels=['v'], gimbal=False,
                                           suffix=suffix_controller,
                                           connection=['connectMatrixAll'])

        mc.connectAttr('%s.%s' % (self.neck_ctrl.control, neck_in_btw_attr),
                       self.neck_in_btw_ctrl.parent_control[0] + '.visibility')
        # HEAD
        self.head_ctrl = ct.Control(match_obj_first_position=head_jnt, prefix=head_prefix,
                                    shape=ct.CUBE,
                                    groups_ctrl=['Zro', 'Global', 'Local'], ctrl_size=scale * 1.0,
                                    ctrl_color='blue', lock_channels=['v'], gimbal=True, suffix=suffix_controller,
                                    connection=['connectMatrixAll'])

        # JAW
        self.jaw_ctrl = ct.Control(match_obj_first_position=jaw_tip_jnt, prefix=jaw_prefix,
                                   shape=ct.SQUAREPLUS, suffix=suffix_controller,
                                   groups_ctrl=['All', 'Offset'], ctrl_size=scale * 0.15,
                                   ctrl_color='red', lock_channels=['s', 'v'])
        # ADD ATTRIBUTE UPLIP FOLLOW
        au.add_attribute(objects=[self.jaw_ctrl.control], long_name=['upLipSetup'],
                         nice_name=[' '], at="enum",
                         en='Up Lip Setup', channel_box=True)

        self.attr_upLip_follow = au.add_attribute(objects=[self.jaw_ctrl.control], long_name=['upLipFollowingJaw'],
                                                  attributeType="float", min=0, max=1, dv=1, keyable=True)
        self.attr_degree_follow = au.add_attribute(objects=[self.jaw_ctrl.control], long_name=['degreeFollowing'],
                                                  attributeType="float", min=0, max=10, dv=0, keyable=True)
        # HEAD UP
        self.head_up_ctrl = ct.Control(match_obj_first_position=head_up_jnt, prefix=head_up_prefix,
                                       shape=ct.CIRCLEHALF, suffix=suffix_controller,
                                       groups_ctrl=['Zro', 'Offset'], ctrl_size=scale * 1.0,
                                       ctrl_color='red', lock_channels=['v'], gimbal=True,
                                       connection=['connectMatrixAll'])
        # HEAD LOW
        self.head_low_ctrl = ct.Control(match_obj_first_position=head_low_jnt, prefix=head_low_prefix,
                                        shape=ct.CIRCLEHALF, suffix=suffix_controller,
                                        groups_ctrl=['Zro', 'Offset'], ctrl_size=scale * 1.0,
                                        ctrl_color='red', lock_channels=['v'], gimbal=True,
                                        connection=['connectMatrixAll'])

        # CREATE GROUP FOR NORMAL ROTATION LIKE JAW
        self.headLow_normal_rotationGrp = mc.createNode('transform', n=au.prefix_name(head_low_jnt) + 'Normal_grp')
        mc.delete(mc.pointConstraint(jaw_jnt, self.headLow_normal_rotationGrp))

        mc.parent(self.headLow_normal_rotationGrp, head_low_jnt)
        # UPPER TEETH
        self.upper_teeth = ct.Control(match_obj_first_position=upper_teeth_jnt,
                                      prefix=upper_teeth_jnt, suffix=suffix_controller,
                                      shape=ct.CUBE, groups_ctrl=[''],
                                      ctrl_size=scale * 0.15,
                                      ctrl_color='yellow', lock_channels=['v'],
                                      connection=['connectAttr'])
        # LOWER TEETH
        self.lower_teeth = ct.Control(match_obj_first_position=lower_teeth_jnt,
                                      prefix=lower_teeth_jnt, suffix=suffix_controller,
                                      shape=ct.CUBE, groups_ctrl=[''],
                                      ctrl_size=scale * 0.15,
                                      ctrl_color='yellow', lock_channels=['v'],
                                      connection=['connectAttr'])
        # TONGUE 01
        self.tongue01 = ct.Control(match_obj_first_position=tongue01_jnt,
                                   prefix=tongue01_jnt, suffix=suffix_controller,
                                   shape=ct.SQUAREPLUS, groups_ctrl=[''],
                                   ctrl_size=scale * 0.15,
                                   ctrl_color='turquoiseBlue', lock_channels=['v'],
                                   connection=['connectAttr'])
        # TONGUE 02
        self.tongue02 = ct.Control(match_obj_first_position=tongue02_jnt,
                                   prefix=tongue02_jnt, suffix=suffix_controller,
                                   shape=ct.SQUAREPLUS, groups_ctrl=[''],
                                   ctrl_size=scale * 0.15,
                                   ctrl_color='turquoiseBlue', lock_channels=['v'],
                                   connection=['connectAttr'])
        # TONGUE 03
        self.tongue03 = ct.Control(match_obj_first_position=tongue03_jnt,
                                   prefix=tongue03_jnt, suffix=suffix_controller,
                                   shape=ct.SQUAREPLUS, groups_ctrl=[''],
                                   ctrl_size=scale * 0.15,
                                   ctrl_color='turquoiseBlue', lock_channels=['v'],
                                   connection=['connectAttr'])
        # TONGUE 04
        self.tongue04 = ct.Control(match_obj_first_position=tongue04_jnt,
                                   prefix=tongue04_jnt, suffix=suffix_controller,
                                   shape=ct.SQUAREPLUS, groups_ctrl=[''],
                                   ctrl_size=scale * 0.15,
                                   ctrl_color='turquoiseBlue', lock_channels=['v'],
                                   connection=['connectAttr'])

        mc.parent(self.jaw_tip_jnt_grp[0], head_low_jnt)
        mc.parent(self.tongue04.parent_control[0], self.tongue03.control)
        mc.parent(self.tongue03.parent_control[0], self.tongue02.control)
        mc.parent(self.tongue02.parent_control[0], self.tongue01.control)
        mc.parent(jaw_direction_grp, self.jaw_ctrl.parent_control[0], self.head_low_ctrl.control_gimbal)
        mc.parent(self.lower_teeth.parent_control[0], self.tongue01.parent_control[0],
                  self.jaw_direction_grp_offset)
        mc.parent(self.upper_teeth.parent_control[0], self.head_low_ctrl.control_gimbal)
        mc.parent(self.head_low_ctrl.parent_control[0], self.head_up_ctrl.parent_control[0],
                  self.head_ctrl.control_gimbal)
        mc.parent(self.head_ctrl.parent_control[0], self.neck_ctrl.control_gimbal)
        mc.parent(self.neck_in_btw_ctrl.parent_control[0], self.neck_ctrl.parent_control[0])

        # INBETWEEN NECK CTRL
        # connect x and z rotation
        neck_inbetween_pma = mc.createNode('plusMinusAverage', n=au.prefix_name(neck_in_btw_jnt) + 'RotXZ' + '_pma')
        mc.connectAttr(self.neck_ctrl.control_gimbal + '.rotateX', neck_inbetween_pma + '.input2D[0].input2Dx')
        mc.connectAttr(self.neck_ctrl.control_gimbal + '.rotateZ', neck_inbetween_pma + '.input2D[0].input2Dy')
        mc.connectAttr(self.neck_ctrl.control + '.rotateX', neck_inbetween_pma + '.input2D[1].input2Dx')
        mc.connectAttr(self.neck_ctrl.control + '.rotateZ', neck_inbetween_pma + '.input2D[1].input2Dy')
        mc.connectAttr(neck_inbetween_pma + '.output2Dx', self.neck_in_btw_ctrl.parent_control[0] + '.rotateX')
        mc.connectAttr(neck_inbetween_pma + '.output2Dy', self.neck_in_btw_ctrl.parent_control[0] + '.rotateZ')

        # connect orient constraint y
        ctrl_orient_constraint = mc.orientConstraint(self.head_ctrl.control_gimbal, self.neck_ctrl.control_gimbal,
                                                     self.neck_in_btw_ctrl.parent_control[0], mo=1, skip=('x', 'z'))[0]
        ctrl_point_constraint = mc.pointConstraint(self.head_ctrl.control_gimbal, self.neck_ctrl.control_gimbal,
                                                   self.neck_in_btw_ctrl.parent_control[0], mo=1)

        # INBETWEEN NECK JNT
        transform_point_cosntraint = mc.pointConstraint(neck_jnt, head_jnt, self.neck_in_btw_jnt_grp[0], mo=1)
        transform_orient_constraint = \
        mc.orientConstraint(neck_jnt, head_jnt, self.neck_in_btw_jnt_grp[0], mo=1, skip=('x', 'z'))[0]
        mc.setAttr(ctrl_orient_constraint + '.interpType', 2)
        mc.setAttr(transform_orient_constraint + '.interpType', 2)

        # CONSTRAINT RENAME
        au.constraint_rename([ctrl_orient_constraint, ctrl_point_constraint[0], transform_point_cosntraint[0],
                              transform_orient_constraint])