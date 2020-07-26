"""
creating arm module base
"""
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
                 prefix,
                 ball_fk_jnt,
                 ball_ik_jnt,
                 ball_jnt,
                 toe_ik_jnt,
                 out_tilt_jnt,
                 in_tilt_jnt,
                 heel_jnt,
                 lower_limb_jnt,
                 prefix_ball_fk,
                 prefix_toe_ik,
                 controller_FkIk_limb_setup,
                 controller_lower_limb_ik,
                 side,
                 scale):

        # FK CTRL SETUP
        foot_fk = ct.Control(match_obj_first_position=ball_fk_jnt, prefix='%s' % prefix_ball_fk, side=side,
                             shape=ct.CIRCLEPLUS, groups_ctrl=['Zro', 'Offset'], ctrl_size=scale * 0.5,
                             ctrl_color='yellow', gimbal=True, lock_channels=['v', 's'],
                             connection=['parent'])

        self.parent_base_fk = foot_fk.parent_control[0]
        self.parent_mid_fk = foot_fk.parent_control[1]
        self.control_fk = foot_fk.control
        self.control_gimbal_fk = foot_fk.control_gimbal

        # IK CTRL SETUP
        au.add_attribute(objects=[controller_lower_limb_ik], long_name=['%s%s' % ('foot', 'IkSetup')],
                         nice_name=[' '], at="enum",
                         en='%s%s' % ('Foot', ' Ik Setup'), channel_box=True)

        au.add_attribute(objects=[controller_lower_limb_ik], long_name=['footRoll'],
                         at="float", dv=0, keyable=True)

        au.add_attribute(objects=[controller_lower_limb_ik], long_name=['ballStartLift'],
                         at="float", dv=30, keyable=True)

        au.add_attribute(objects=[controller_lower_limb_ik], long_name=['toeStartStraight'],
                         at="float", dv=60, keyable=True)

        au.add_attribute(objects=[controller_lower_limb_ik], long_name=['tilt'],
                         at="float", dv=0, keyable=True)

        au.add_attribute(objects=[controller_lower_limb_ik], long_name=['heelSpin'],
                         at="float", dv=0, keyable=True)

        au.add_attribute(objects=[controller_lower_limb_ik], long_name=['toeSpin'],
                         at="float", dv=0, keyable=True)

        au.add_attribute(objects=[controller_lower_limb_ik], long_name=['toeRoll'],
                         at="float", dv=0, keyable=True)

        self.toe_wiggle_attr = au.add_attribute(objects=[controller_lower_limb_ik], long_name=['toeWiggle'],
                         at="float", dv=0, keyable=True)

        # create reverse node for FK on/off
        ball_setup_reverse = mc.createNode('reverse', n=('%s%s%s_rev' % (prefix, 'FkIk', side)))

        ball_blend_constraint = mc.parentConstraint(ball_fk_jnt, ball_ik_jnt, ball_jnt)

        # set on/off attribute FK
        au.connect_part_object(obj_base_connection='FkIk', target_connection='inputX', obj_name=controller_FkIk_limb_setup,
                               target_name=[ball_setup_reverse], select_obj=False)

        # set on/off attribute Fk/Ik upper limb
        au.connect_part_object(obj_base_connection='outputX', target_connection='%sW0' % ball_fk_jnt,
                               obj_name=ball_setup_reverse,
                               target_name=ball_blend_constraint, select_obj=False)
        au.connect_part_object(obj_base_connection='FkIk', target_connection='%sW1' % ball_ik_jnt,
                               obj_name=controller_FkIk_limb_setup,
                               target_name=ball_blend_constraint, select_obj=False)

        # TOE IK SOLVER
        self.toe_ik_handle = mc.ikHandle(sj=ball_ik_jnt, ee=toe_ik_jnt, sol='ikSCsolver', n='%s%s_hdl' % (prefix_toe_ik, side))
        mc.hide(self.toe_ik_handle[0])

        # REVERSE FOOT
        mc.select(cl=1)
        # foot reverse joint
        self.foot_reverse_joint = self.foot_joint_reverse(obj_name='Reverse', prefix=prefix, side=side,
                                                          joint_constraint=lower_limb_jnt, scale=scale)

        # toe roll joint
        self.toe_roll_joint = self.foot_joint_reverse(obj_name='ToeRoll', prefix=prefix, side=side, joint_constraint=toe_ik_jnt, scale=scale)

        # heel joint
        self.heel_joint = self.foot_joint_reverse(obj_name='Heel', prefix=prefix, side=side, joint_constraint=heel_jnt, scale=scale)

        # toe joint
        self.toe_joint = self.foot_joint_reverse(obj_name='Toe', prefix=prefix, side=side, joint_constraint=toe_ik_jnt, scale=scale)

        # inside joint
        self.inside_tilt_joint = self.foot_joint_reverse(obj_name='InTilt', prefix=prefix, side=side, joint_constraint=in_tilt_jnt, scale=scale)

        # outside joint
        self.outside_tilt_joint = self.foot_joint_reverse(obj_name='OutTilt', prefix=prefix, side=side, joint_constraint=out_tilt_jnt, scale=scale)

        # ball locator
        self.ball_roll_joint = self.foot_joint_reverse(obj_name='BallRoll', prefix=prefix, side=side, joint_constraint=ball_jnt, scale=scale)

        # toe wiggle joint
        self.toe_wiggle_joint = self.foot_joint_reverse(obj_name='ToeWiggle', prefix=prefix, side=side, joint_constraint=ball_jnt, scale=scale)

        # change position of toe wiggle
        mc.parent(self.toe_wiggle_joint, self.outside_tilt_joint)

        # constraint rename
        au.constraint_rename(ball_blend_constraint)

    def foot_joint_reverse(self, obj_name, prefix, side, joint_constraint, scale):
        joint = mc.joint(n='%s%s%s_jnt' % (prefix, obj_name, side), rad=0.1 * scale)
        mc.delete(mc.parentConstraint(joint_constraint, joint))
        mc.makeIdentity(joint, apply=True, t=1, r=1, s=1, n=0)
        mc.hide(joint)
        return joint