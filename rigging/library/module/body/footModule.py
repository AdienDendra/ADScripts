from __future__ import absolute_import

import maya.cmds as cmds

from rigging.library.base.body import foot as rlbb_foot
from rigging.library.utils import softIkSetup as rlu_softIkSetup, addAttrMessage as rlu_addAttrMessage
from rigging.tools import utils as rt_utils


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
            build_foot = rlbb_foot.Build(prefix=prefix,
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
                cmds.delete(leg.run_soft_ik[0], leg.run_soft_ik[1])
            get_value_tx_upper_limb_jnt = cmds.xform(upper_limb_jnt, ws=1, q=1, t=1)[0]

            if get_value_tx_upper_limb_jnt > 0:
                value_attribute = -1
            else:
                value_attribute = 1

            # ADD MESSAGE ATTRIBUTE
            message = rlu_addAttrMessage.MessageAttribute(fkik_ctrl=controller_FkIk_limb_setup, ball=True)

            # connect end limb fk joint
            message.connect_message_to_attribute(object_target=ball_fk_jnt,
                                                 fkik_ctrl=controller_FkIk_limb_setup,
                                                 object_connector=message.end_limb_fk_jnt)
            # # connect end limb ik joint
            # message.connect_message_to_attribute(object_connector=ball_ik_jnt,
            #                                      fkik_ctrl=controller_FkIk_limb_setup,
            #                                      object_target=message.end_limb_ik_jnt)
            # connect end limb joint
            message.connect_message_to_attribute(object_target=ball_jnt,
                                                 fkik_ctrl=controller_FkIk_limb_setup,
                                                 object_connector=message.end_limb_jnt)
            # connect end limb fk ctrl
            message.connect_message_to_attribute(object_target=build_foot.control_fk,
                                                 fkik_ctrl=controller_FkIk_limb_setup,
                                                 object_connector=message.end_limb_fk_ctrl)
            # connect toe wiggle attribute
            message.connect_message_to_attribute(object_target=lower_limb_ik_control,
                                                 fkik_ctrl=controller_FkIk_limb_setup,
                                                 object_connector=message.toe_wiggle_attr)
            # # connect end snap joint
            # message.connect_message_to_attribute(object_connector=end_limb_snap_jnt,
            #                                      fkik_ctrl=controller_FkIk_limb_setup,
            #                                      object_target=message.end_limb_snap_jnt)

            # parenting controller Fk ball and Ik ball to respective parent
            cmds.parent(build_foot.parent_base_fk, lower_gimbal_fk_ctrl)

            # constraint foot reverse to soft ik
            cmds.parent(position_soft_jnt, build_foot.foot_reverse_joint)

            # parent constraint toeRoll to posSoftJnt
            parent_constraint_position_soft = cmds.parentConstraint(build_foot.toe_roll_joint, position_soft_jnt, mo=1)

            # parent toe ik handle, ball ik handle to wiggle locator
            cmds.parent(build_foot.toe_ik_handle[0], build_foot.toe_wiggle_joint)

            # parent ankle handle to ball reverse
            cmds.parent(lower_limb_ik_hdl, build_foot.ball_roll_joint)

            # parent ball handle to ball reverse
            cmds.parent(end_limb_ik_hdl, build_foot.toe_wiggle_joint)

            # parent object reverse joint
            cmds.parent(build_foot.ball_roll_joint, build_foot.outside_tilt_joint)

            cmds.parent(build_foot.outside_tilt_joint, build_foot.inside_tilt_joint)

            cmds.parent(build_foot.inside_tilt_joint, build_foot.toe_joint)

            cmds.parent(build_foot.toe_joint, build_foot.heel_joint)

            cmds.parent(build_foot.heel_joint, build_foot.toe_roll_joint)

            cmds.parent(build_foot.toe_roll_joint, build_foot.foot_reverse_joint)

            # parent to part joint
            cmds.parent(build_foot.foot_reverse_joint, part_joint_grp_module)

            # assigned name foot reverse joint
            self.foot_reverse_joint = build_foot.foot_reverse_joint

            # CREATE NODE REVERSE
            # FOOT ROLL NEGATIVE
            # create clamp
            clamp_roll_negative = cmds.createNode('clamp', n='%s%s%s_clm' % (prefix, 'RollBack', side))
            cmds.connectAttr(controller_lower_limb_ik + '.footRoll', clamp_roll_negative + '.inputR')
            cmds.setAttr(clamp_roll_negative + '.minR', -90)

            # create mdl reverse value
            mdl_roll_negative = cmds.createNode('multDoubleLinear', n='%s%s%s_mdl' % (prefix, 'RollBackRev', side))
            cmds.connectAttr(clamp_roll_negative + '.outputR', mdl_roll_negative + '.input1')
            cmds.setAttr(mdl_roll_negative + '.input2', -1)

            # connect to HEEL JOINT X
            cmds.connectAttr(mdl_roll_negative + '.output', build_foot.heel_joint + '.rotateX')

            # FOOT ROLL POSITIVE
            # create clamp foot positive
            clamp_foot_position = cmds.createNode('clamp', n='%s%s%s_clm' % (prefix, 'RollToe', side))
            cmds.connectAttr(controller_lower_limb_ik + '.footRoll', clamp_foot_position + '.inputR')
            cmds.connectAttr(controller_lower_limb_ik + '.toeStartStraight', clamp_foot_position + '.maxR')
            cmds.connectAttr(controller_lower_limb_ik + '.ballStartLift', clamp_foot_position + '.minR')

            # create set range foot positive
            setRange_foot_position = cmds.createNode('setRange', n='%s%s%s_str' % (prefix, 'RollToe', side))
            cmds.connectAttr(clamp_foot_position + '.inputR', setRange_foot_position + '.valueX')
            cmds.connectAttr(clamp_foot_position + '.maxR', setRange_foot_position + '.oldMaxX')
            cmds.connectAttr(clamp_foot_position + '.minR', setRange_foot_position + '.oldMinX')
            cmds.setAttr(setRange_foot_position + '.maxX', 1)

            # create mult double linear
            mdl_roll_position = cmds.createNode('multDoubleLinear', n='%s%s%s_mdl' % (prefix, 'RollToe', side))
            cmds.connectAttr(setRange_foot_position + '.outValueX', mdl_roll_position + '.input1')
            cmds.connectAttr(clamp_foot_position + '.inputR', mdl_roll_position + '.input2')

            # create mult double linear revese
            mdl_roll_pos_reverse = cmds.createNode('multDoubleLinear', n='%s%s%s_mdl' % (prefix, 'RollToeRev', side))
            cmds.connectAttr(mdl_roll_position + '.output', mdl_roll_pos_reverse + '.input1')
            cmds.setAttr(mdl_roll_pos_reverse + '.input2', -1)

            # create plus minus average positive
            pma_foot_position = cmds.createNode('plusMinusAverage', n='%s%s%s_pma' % (prefix, 'RollToe', side))
            cmds.setAttr(pma_foot_position + '.operation', 2)
            cmds.setAttr(pma_foot_position + '.input1D[0]', 1)
            cmds.connectAttr(setRange_foot_position + '.outValueX', pma_foot_position + '.input1D[1]')

            # create clamp ball positive
            clamp_ball_position = cmds.createNode('clamp', n='%s%s%s_clm' % (prefix, 'RollBall', side))
            cmds.connectAttr(controller_lower_limb_ik + '.footRoll', clamp_ball_position + '.inputR')
            cmds.connectAttr(controller_lower_limb_ik + '.ballStartLift', clamp_ball_position + '.maxR')

            # create set range ball positive
            setRange_ball_position = cmds.createNode('setRange', n='%s%s%s_str' % (prefix, 'RollBall', side))
            cmds.connectAttr(clamp_ball_position + '.inputR', setRange_ball_position + '.valueX')
            cmds.connectAttr(clamp_ball_position + '.maxR', setRange_ball_position + '.oldMaxX')
            cmds.connectAttr(clamp_ball_position + '.minR', setRange_ball_position + '.oldMinX')
            cmds.setAttr(setRange_ball_position + '.maxX', 1)

            # create mult double linear ball percent
            mdl_ball_position_percent = cmds.createNode('multDoubleLinear',
                                                        n='%s%s%s_mdl' % (prefix, 'RollBallPercent', side))
            cmds.connectAttr(setRange_ball_position + '.outValueX', mdl_ball_position_percent + '.input1')
            cmds.connectAttr(pma_foot_position + '.output1D', mdl_ball_position_percent + '.input2')

            # create mult double linear ball
            mdl_ball_position = cmds.createNode('multDoubleLinear', n='%s%s%s_mdl' % (prefix, 'RollBall', side))
            cmds.connectAttr(mdl_ball_position_percent + '.output', mdl_ball_position + '.input1')
            cmds.connectAttr(controller_lower_limb_ik + '.footRoll', mdl_ball_position + '.input2')

            # create mult double linear ball reverse
            mdl_ball_pos_reverse = cmds.createNode('multDoubleLinear', n='%s%s%s_mdl' % (prefix, 'RollBallRev', side))
            cmds.connectAttr(mdl_ball_position + '.output', mdl_ball_pos_reverse + '.input1')
            cmds.setAttr(mdl_ball_pos_reverse + '.input2', -1)

            # connect to BALL JOINT X
            cmds.connectAttr(mdl_ball_pos_reverse + '.output', build_foot.ball_roll_joint + '.rotateX')

            # connect to TOE JOINT X
            cmds.connectAttr(mdl_roll_pos_reverse + '.output', build_foot.toe_joint + '.rotateX')

            # FOOT HEEL SPIN
            cmds.connectAttr(controller_lower_limb_ik + '.heelSpin', build_foot.heel_joint + '.rotateZ')

            # FOOT TOE SPIN
            # create mult double linear ball reverse
            mdl_toe_spin = cmds.createNode('multDoubleLinear', n='%s%s%s_mdl' % (prefix, 'SpinToeRev', side))
            cmds.connectAttr(controller_lower_limb_ik + '.toeSpin', mdl_toe_spin + '.input1')
            cmds.setAttr(mdl_toe_spin + '.input2', -1)
            # connect to TOE JOINT Z
            cmds.connectAttr(mdl_toe_spin + '.output', build_foot.toe_joint + '.rotateZ')

            # FOOT TOE ROLL
            # create mult double linear ball reverse
            mdl_toe_roll = cmds.createNode('multDoubleLinear', n='%s%s%s_mdl' % (prefix, 'RollToeUDRev', side))
            cmds.connectAttr(controller_lower_limb_ik + '.toeRoll', mdl_toe_roll + '.input1')
            cmds.setAttr(mdl_toe_roll + '.input2', value_attribute)
            # connect to TOE JOINT ROLL X
            cmds.connectAttr(mdl_toe_roll + '.output', build_foot.toe_roll_joint + '.rotateX')

            # create condition for toe roll to pos soft joint
            cnd_toe_roll = cmds.createNode('condition', n='%s%s%s_cnd' % (prefix, 'RollToeUD', side))
            cmds.setAttr(cnd_toe_roll + '.operation', 4)
            cmds.connectAttr(build_foot.toe_roll_joint + '.rotateX', cnd_toe_roll + '.firstTerm')
            cmds.connectAttr(cnd_toe_roll + '.outColorR',
                             parent_constraint_position_soft[0] + '.%sW0' % build_foot.toe_roll_joint)

            # FOOT TOE WIGGLE
            # create mult double linear ball reverse
            mdl_toe_wiggle = cmds.createNode('multDoubleLinear', n='%s%s%s_mdl' % (prefix, 'RollToeWglRev', side))
            cmds.connectAttr(controller_lower_limb_ik + '.toeWiggle', mdl_toe_wiggle + '.input1')
            cmds.setAttr(mdl_toe_wiggle + '.input2', -1)
            # connect to TOE JOINT ROLL X
            cmds.connectAttr(mdl_toe_wiggle + '.output', build_foot.toe_wiggle_joint + '.rotateX')

            # FOOT TILT
            # create mult double linear ball reverse
            mdl_tilt = cmds.createNode('multDoubleLinear', n='%s%s%s_mdl' % (prefix, 'TiltRev', side))
            cmds.connectAttr(controller_lower_limb_ik + '.tilt', mdl_tilt + '.input1')
            cmds.setAttr(mdl_tilt + '.input2', -1)

            # create condition
            cnd_tilt = cmds.createNode('condition', n='%s%s%s_cnd' % (prefix, 'Tilt', side))
            cmds.setAttr(cnd_tilt + '.operation', 2)
            cmds.setAttr(cnd_tilt + '.colorIfFalseG', 0)
            cmds.connectAttr(controller_lower_limb_ik + '.tilt', cnd_tilt + '.firstTerm')
            cmds.connectAttr(mdl_tilt + '.output', cnd_tilt + '.colorIfFalseR')
            cmds.connectAttr(mdl_tilt + '.output', cnd_tilt + '.colorIfTrueG')

            # connect to INSIDE JOINT y
            cmds.connectAttr(cnd_tilt + '.outColorR', build_foot.inside_tilt_joint + '.rotateY')

            # connect to OUTSIDE JOINT y
            cmds.connectAttr(cnd_tilt + '.outColorG', build_foot.outside_tilt_joint + '.rotateY')

            # rename constraint
            rt_utils.constraint_rename(parent_constraint_position_soft)

            if not single_module:
                rlu_softIkSetup.run_soft_ik_joint(prefix=prefix, side=side,
                                                  lower_limb_ik_gimbal=leg.lower_limb_ik_gimbal,
                                                  foot_reverse_joint_or_position_soft_jnt=self.foot_reverse_joint,
                                                  position_lower_limb_jnt=leg.pos_lower_limb_jnt,
                                                  lowerLimbIkControl=leg.lower_limb_ik_control)
            else:
                rlu_softIkSetup.run_soft_ik_joint(prefix=prefix, side=side, lower_limb_ik_gimbal=lower_limb_ik_gimbal,
                                                  foot_reverse_joint_or_position_soft_jnt=self.foot_reverse_joint,
                                                  position_lower_limb_jnt=position_lower_limb_jnt,
                                                  lowerLimbIkControl=lower_limb_ik_control)
        else:
            cmds.delete(ball_jnt, ball_scale_jnt)
