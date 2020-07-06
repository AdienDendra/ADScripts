from __builtin__ import reload

import maya.cmds as mc

from rigging.library.base.body import foot as ft
from rigging.library.module import base_module as gm, template_single_module as ds
from rigging.library.utils import controller as ct, rotation_controller as rc, softIk_setup as rs
from rigging.tools import AD_utils as au

reload(gm)
reload(ct)
reload(au)
reload(ft)
reload(rc)
reload(ds)
reload(rs)


class Foot:
    def __init__(self,
                 foot=True,
                 leg=None,
                 prefix='foot',
                 upper_limb_jnt=None,
                 ball_fk_jnt=None,
                 ball_ik_jnt=None,
                 ball_jnt=None,
                 ball_scale_jnt=None,
                 toe_ik_jnt=None,
                 heel_jnt=None,
                 lower_limb_jnt=None,
                 in_tilt_jnt=None,
                 out_tilt_jnt=None,
                 prefix_ball_fk='ballFk',
                 prefix_toe_ik='toeIk',
                 lower_gimbal_fk_ctrl=None,
                 lower_limb_ik_hdl=None,
                 end_limb_ik_hdl=None,
                 controller_FkIk_limb_setup=None,
                 controller_lower_limb_ik=None,
                 position_soft_jnt=None,
                 part_joint_grp_module=None,
                 side=None,
                 single_module=False,
                 scale=1.0,
                 lower_limb_ik_gimbal=None,
                 position_lower_limb_jnt=None,
                 lower_limb_ik_control=None):


        if foot:
            build_foot = ft.Build(prefix=prefix,
                                  ball_fk_jnt=ball_fk_jnt,
                                  ball_ik_jnt=ball_ik_jnt,
                                  ball_jnt=ball_jnt,
                                  toe_ik_jnt=toe_ik_jnt,
                                  heel_jnt=heel_jnt,
                                  lower_limb_jnt=lower_limb_jnt,
                                  in_tilt_jnt=in_tilt_jnt,
                                  out_tilt_jnt=out_tilt_jnt,
                                  prefix_ball_fk=prefix_ball_fk,
                                  prefix_toe_ik=prefix_toe_ik,
                                  controller_FkIk_limb_setup=controller_FkIk_limb_setup,
                                  controller_lower_limb_ik=controller_lower_limb_ik,
                                  side=side,
                                  scale=scale)

            # delete constraint softIk
            if not single_module:
                mc.delete(leg.run_soft_ik[0], leg.run_soft_ik[1])

            get_value_tx_upper_limb_jnt = mc.xform(upper_limb_jnt, ws=1, q=1, t=1)[0]

            if get_value_tx_upper_limb_jnt>0:
                value_attribute = -1
            else:
                value_attribute = 1

            # parenting controller Fk ball and Ik ball to respective parent
            mc.parent(build_foot.parent_base_fk, lower_gimbal_fk_ctrl)

            # constraint foot reverse to soft ik
            mc.parent(position_soft_jnt, build_foot.foot_reverse_joint)

            # parent constraint toeRoll to posSoftJnt
            parent_constraint_position_soft = mc.parentConstraint(build_foot.toe_roll_joint, position_soft_jnt, mo=1)

            # parent toe ik handle, ball ik handle to wiggle locator
            mc.parent(build_foot.toe_ik_handle[0], build_foot.toe_wiggle_joint)

            # parent ankle handle to ball reverse
            mc.parent(lower_limb_ik_hdl, build_foot.ball_roll_joint)

            # parent ball handle to ball reverse
            mc.parent(end_limb_ik_hdl, build_foot.toe_wiggle_joint)

            # parent object reverse joint
            mc.parent(build_foot.ball_roll_joint, build_foot.outside_tilt_joint)

            mc.parent(build_foot.outside_tilt_joint, build_foot.inside_tilt_joint)

            mc.parent(build_foot.inside_tilt_joint, build_foot.toe_joint)

            mc.parent(build_foot.toe_joint, build_foot.heel_joint)

            mc.parent(build_foot.heel_joint, build_foot.toe_roll_joint)

            mc.parent(build_foot.toe_roll_joint, build_foot.foot_reverse_joint)

            # parent to part joint
            mc.parent(build_foot.foot_reverse_joint, part_joint_grp_module)

            # assigned name foot reverse joint
            self.foot_reverse_joint = build_foot.foot_reverse_joint

        # CREATE NODE REVERSE
        # FOOT ROLL NEGATIVE
            # create clamp
            clamp_roll_negative = mc.createNode('clamp', n='%s%s%s_clm' % (prefix, 'RollBack', side))
            mc.connectAttr(controller_lower_limb_ik + '.footRoll', clamp_roll_negative + '.inputR')
            mc.setAttr(clamp_roll_negative + '.minR', -90)

            # create mdl reverse value
            mdl_roll_negative = mc.createNode('multDoubleLinear', n='%s%s%s_mdl' % (prefix, 'RollBackRev', side))
            mc.connectAttr(clamp_roll_negative + '.outputR', mdl_roll_negative + '.input1')
            mc.setAttr(mdl_roll_negative + '.input2', -1)

            # connect to HEEL JOINT X
            mc.connectAttr(mdl_roll_negative + '.output', build_foot.heel_joint + '.rotateX')

        # FOOT ROLL POSITIVE
            # create clamp foot positive
            clamp_foot_position = mc.createNode('clamp', n='%s%s%s_clm' % (prefix, 'RollToe', side))
            mc.connectAttr(controller_lower_limb_ik + '.footRoll', clamp_foot_position + '.inputR')
            mc.connectAttr(controller_lower_limb_ik + '.toeStartStraight', clamp_foot_position + '.maxR')
            mc.connectAttr(controller_lower_limb_ik + '.ballStartLift', clamp_foot_position + '.minR')

            # create set range foot positive
            setRange_foot_position = mc.createNode('setRange', n='%s%s%s_str' % (prefix, 'RollToe', side))
            mc.connectAttr(clamp_foot_position + '.inputR', setRange_foot_position + '.valueX')
            mc.connectAttr(clamp_foot_position + '.maxR', setRange_foot_position + '.oldMaxX')
            mc.connectAttr(clamp_foot_position + '.minR', setRange_foot_position + '.oldMinX')
            mc.setAttr(setRange_foot_position + '.maxX', 1)

            # create mult double linear
            mdl_roll_position = mc.createNode('multDoubleLinear', n='%s%s%s_mdl' % (prefix, 'RollToe', side))
            mc.connectAttr(setRange_foot_position + '.outValueX', mdl_roll_position + '.input1')
            mc.connectAttr(clamp_foot_position + '.inputR', mdl_roll_position + '.input2')

            # create mult double linear revese
            mdl_roll_pos_reverse = mc.createNode('multDoubleLinear', n='%s%s%s_mdl' % (prefix, 'RollToeRev', side))
            mc.connectAttr(mdl_roll_position + '.output', mdl_roll_pos_reverse + '.input1')
            mc.setAttr(mdl_roll_pos_reverse + '.input2', -1)

            # create plus minus average positive
            pma_foot_position = mc.createNode('plusMinusAverage', n='%s%s%s_pma' % (prefix, 'RollToe', side))
            mc.setAttr(pma_foot_position + '.operation', 2)
            mc.setAttr(pma_foot_position + '.input1D[0]', 1)
            mc.connectAttr(setRange_foot_position + '.outValueX', pma_foot_position + '.input1D[1]')

            # create clamp ball positive
            clamp_ball_position = mc.createNode('clamp', n='%s%s%s_clm' % (prefix, 'RollBall', side))
            mc.connectAttr(controller_lower_limb_ik + '.footRoll', clamp_ball_position + '.inputR')
            mc.connectAttr(controller_lower_limb_ik + '.ballStartLift', clamp_ball_position + '.maxR')

            # create set range ball positive
            setRange_ball_position = mc.createNode('setRange', n='%s%s%s_str' % (prefix, 'RollBall', side))
            mc.connectAttr(clamp_ball_position + '.inputR', setRange_ball_position + '.valueX')
            mc.connectAttr(clamp_ball_position + '.maxR', setRange_ball_position + '.oldMaxX')
            mc.connectAttr(clamp_ball_position + '.minR', setRange_ball_position + '.oldMinX')
            mc.setAttr(setRange_ball_position + '.maxX', 1)

            # create mult double linear ball percent
            mdl_ball_position_percent = mc.createNode('multDoubleLinear', n='%s%s%s_mdl' % (prefix, 'RollBallPercent', side))
            mc.connectAttr(setRange_ball_position + '.outValueX', mdl_ball_position_percent + '.input1')
            mc.connectAttr(pma_foot_position + '.output1D', mdl_ball_position_percent + '.input2')

            # create mult double linear ball
            mdl_ball_position = mc.createNode('multDoubleLinear', n='%s%s%s_mdl' % (prefix, 'RollBall', side))
            mc.connectAttr(mdl_ball_position_percent + '.output', mdl_ball_position + '.input1')
            mc.connectAttr(controller_lower_limb_ik + '.footRoll', mdl_ball_position + '.input2')

            # create mult double linear ball reverse
            mdl_ball_pos_reverse = mc.createNode('multDoubleLinear', n='%s%s%s_mdl' % (prefix, 'RollBallRev', side))
            mc.connectAttr(mdl_ball_position + '.output', mdl_ball_pos_reverse + '.input1')
            mc.setAttr(mdl_ball_pos_reverse + '.input2', -1)

            # connect to BALL JOINT X
            mc.connectAttr(mdl_ball_pos_reverse + '.output', build_foot.ball_roll_joint + '.rotateX')

            # connect to TOE JOINT X
            mc.connectAttr(mdl_roll_pos_reverse + '.output', build_foot.toe_joint + '.rotateX')

        # FOOT HEEL SPIN
            mc.connectAttr(controller_lower_limb_ik + '.heelSpin', build_foot.heel_joint + '.rotateZ')

        # FOOT TOE SPIN
            # create mult double linear ball reverse
            mdl_toe_spin = mc.createNode('multDoubleLinear', n='%s%s%s_mdl' % (prefix, 'SpinToeRev', side))
            mc.connectAttr(controller_lower_limb_ik + '.toeSpin', mdl_toe_spin + '.input1')
            mc.setAttr(mdl_toe_spin + '.input2', -1)
            # connect to TOE JOINT Z
            mc.connectAttr(mdl_toe_spin + '.output', build_foot.toe_joint + '.rotateZ')

        # FOOT TOE ROLL
            # create mult double linear ball reverse
            mdl_toe_roll = mc.createNode('multDoubleLinear', n='%s%s%s_mdl' % (prefix, 'RollToeUDRev', side))
            mc.connectAttr(controller_lower_limb_ik + '.toeRoll', mdl_toe_roll + '.input1')
            mc.setAttr(mdl_toe_roll + '.input2', value_attribute)
            # connect to TOE JOINT ROLL X
            mc.connectAttr(mdl_toe_roll + '.output', build_foot.toe_roll_joint + '.rotateX')

            # create condition for toe roll to pos soft joint
            cnd_toe_roll = mc.createNode('condition', n='%s%s%s_cnd' % (prefix, 'RollToeUD', side))
            mc.setAttr(cnd_toe_roll + '.operation', 4)
            mc.connectAttr(build_foot.toe_roll_joint + '.rotateX', cnd_toe_roll + '.firstTerm')
            mc.connectAttr(cnd_toe_roll + '.outColorR', parent_constraint_position_soft[0] + '.%sW0' % build_foot.toe_roll_joint)

        # FOOT TOE WIGGLE
            # create mult double linear ball reverse
            mdl_toe_wiggle = mc.createNode('multDoubleLinear', n='%s%s%s_mdl' % (prefix, 'RollToeWglRev', side))
            mc.connectAttr(controller_lower_limb_ik + '.toeWiggle', mdl_toe_wiggle + '.input1')
            mc.setAttr(mdl_toe_wiggle + '.input2', -1)
            # connect to TOE JOINT ROLL X
            mc.connectAttr(mdl_toe_wiggle + '.output', build_foot.toe_wiggle_joint + '.rotateX')

        # FOOT TILT
            # create mult double linear ball reverse
            mdl_tilt = mc.createNode('multDoubleLinear', n='%s%s%s_mdl' % (prefix, 'TiltRev', side))
            mc.connectAttr(controller_lower_limb_ik + '.tilt', mdl_tilt + '.input1')
            mc.setAttr(mdl_tilt + '.input2', -1)

            # create condition
            cnd_tilt = mc.createNode('condition', n='%s%s%s_cnd' % (prefix, 'Tilt', side))
            mc.setAttr(cnd_tilt + '.operation', 2)
            mc.setAttr(cnd_tilt + '.colorIfFalseG', 0)
            mc.connectAttr(controller_lower_limb_ik + '.tilt', cnd_tilt + '.firstTerm')
            mc.connectAttr(mdl_tilt + '.output', cnd_tilt + '.colorIfFalseR')
            mc.connectAttr(mdl_tilt + '.output', cnd_tilt + '.colorIfTrueG')

            # connect to INSIDE JOINT y
            mc.connectAttr(cnd_tilt + '.outColorR', build_foot.inside_tilt_joint + '.rotateY')

            # connect to OUTSIDE JOINT y
            mc.connectAttr(cnd_tilt + '.outColorG', build_foot.outside_tilt_joint + '.rotateY')

            # rename constraint
            au.constraint_rename(parent_constraint_position_soft)

            if not single_module:
                rs.run_soft_ik_joint(prefix=prefix, side=side, lower_limb_ik_gimbal=leg.lower_limb_ik_gimbal,
                                     foot_reverse_joint_or_position_soft_jnt=self.foot_reverse_joint, position_lower_limb_jnt=leg.pos_lower_limb_jnt,
                                     lowerLimbIkControl=leg.lower_limb_ik_control)
            else:
                rs.run_soft_ik_joint(prefix=prefix, side=side, lower_limb_ik_gimbal=lower_limb_ik_gimbal,
                                     foot_reverse_joint_or_position_soft_jnt=self.foot_reverse_joint, position_lower_limb_jnt=position_lower_limb_jnt,
                                     lowerLimbIkControl=lower_limb_ik_control)
        else:
            mc.delete(ball_jnt, ball_scale_jnt)