from __builtin__ import reload

import maya.cmds as mc

from rigging.library.base.face import lid as el, lid_corner as cl, iris_pupil as ip
from rigging.library.utils import controller as ct, transform as tf
from rigging.tools import AD_utils as au

reload(el)
reload(ct)
reload(au)
reload(tf)
reload(cl)
reload(ip)


class Lid:
    def __init__(self,
                 face_utils_grp,
                 curve_up_lid_template,
                 curve_low_lid_template,
                 offset_lid02_position,
                 offset_lid04_position,
                 eyeball_jnt,
                 eye_jnt,
                 prefix_eye,
                 prefix_eye_aim,
                 scale,
                 side,
                 side_LFT,
                 side_RGT,
                 lid01_direction,
                 lid02_direction,
                 lid03_direction,
                 lid04_direction,
                 lid05_direction,
                 position_eye_aim_ctrl,
                 eye_aim_main_ctrl,
                 head_up_ctrl_gimbal,
                 corner_lip,
                 corner_lip_lid_attr,
                 low_lid_following_down,
                 upLid_following_down_lowLid_following_up,
                 upLid_LR_lowLid_LR,
                 upLid_following_up,
                 upper_head_gimbal_ctrl,
                 pupil_jnt,
                 iris_jnt,
                 pupil_prefix,
                 iris_prefix,
                 eye_ctrl_direction,
                 suffix_controller,
                 base_module_nonTransform,
                 ):

        self.position = mc.xform(eyeball_jnt, ws=1, q=1, t=1)[0]

        # CREATE GROUP FOR LID STUFF
        lid_grp = mc.group(em=1, n='lid' + side + '_grp')

        # world up object lid
        world_up_object = mc.spaceLocator(n='eyeWorldObj' + side + '_loc')[0]
        mc.delete(mc.parentConstraint(eyeball_jnt, world_up_object))
        value = mc.getAttr(world_up_object + '.translateY')
        mc.setAttr(world_up_object + '.translateY', value + (10 * scale))
        self.world_up_object = world_up_object

        # world up object eye aim
        world_up_aim_object = mc.duplicate(world_up_object, n='eyeWorldAimObj' + side + '_loc')[0]
        mc.parent(world_up_aim_object, head_up_ctrl_gimbal)
        mc.hide(world_up_aim_object)
        self.world_up_aim_object = world_up_aim_object

        self.eye_move_grp = mc.group(em=1, n='eyeMove' + side + '_grp')
        self.eye_move_grp_offset = mc.group(em=1, n='eyeMoveOffset' + side + '_grp', p=self.eye_move_grp)
        mc.delete(mc.parentConstraint(eyeball_jnt, self.eye_move_grp))

        self.eye_move_all = mc.group(em=1, n='eyeMoveAll' + side + '_grp')
        mc.parent(self.eye_move_all, self.eye_move_grp_offset)

        mc.parent(self.eye_move_grp, lid_grp)

        # LID UP LFT
        self.upLid = el.Build(curve_template=curve_up_lid_template,
                              world_up_object=world_up_object,
                              eyeball_jnt=eyeball_jnt,
                              scale=scale,
                              offset_jnt02_position=offset_lid02_position,
                              offset_jnt04_position=offset_lid04_position,
                              lid01_direction=lid01_direction,
                              lid02_direction=lid02_direction,
                              lid03_direction=lid03_direction,
                              lid04_direction=lid04_direction,
                              lid05_direction=lid05_direction,
                              side=side,
                              side_LFT=side_LFT,
                              side_RGT=side_RGT,
                              ctrl_color='yellow',
                              lid_low_controller=False,
                              upper_head_gimbal_ctrl=upper_head_gimbal_ctrl,
                              suffix_controller=suffix_controller,
                              base_module_nonTransform=base_module_nonTransform,
                              )
        self.lid_out_up01_follow_attr = self.upLid.lid_out01_follow_attr
        self.lid_out_up02_follow_attr = self.upLid.lid_out02_follow_attr
        self.lid_out_up03_follow_attr = self.upLid.lid_out03_follow_attr
        self.lid_out_up04_follow_attr = self.upLid.lid_out04_follow_attr
        self.lid_out_up05_follow_attr = self.upLid.lid_out05_follow_attr
        # self.up_lid_close_lid = self.upLid.close_lid_attr

        self.up_lid_bind01_ctrl = self.upLid.lid_bind01.control
        self.up_lid_bind02_ctrl = self.upLid.lid_bind02.control
        self.up_lid_bind03_ctrl = self.upLid.lid_bind03.control
        self.up_lid_bind04_ctrl = self.upLid.lid_bind04.control
        self.up_lid_bind05_ctrl = self.upLid.lid_bind05.control

        self.up_lid_bind01_grp_offset = self.upLid.joint_bind01_grp_offset
        self.up_lid_bind05_grp_offset = self.upLid.joint_bind05_grp_offset
        self.up_lid_all_jnt = self.upLid.all_joint
        self.up_lid_move_grp = self.upLid.move_grp

        self.lowLid = el.Build(curve_template=curve_low_lid_template,
                               world_up_object=world_up_object,
                               eyeball_jnt=eyeball_jnt,
                               scale=scale,
                               offset_jnt02_position=offset_lid02_position,
                               offset_jnt04_position=offset_lid04_position,
                               lid01_direction=lid01_direction,
                               lid02_direction=lid02_direction,
                               lid03_direction=lid03_direction,
                               lid04_direction=lid04_direction,
                               lid05_direction=lid05_direction,
                               side=side,
                               side_LFT=side_LFT,
                               side_RGT=side_RGT,
                               ctrl_color='red',
                               lid_low_controller=True,
                               upper_head_gimbal_ctrl=upper_head_gimbal_ctrl,
                               suffix_controller=suffix_controller,
                               base_module_nonTransform=base_module_nonTransform,
                               )
        self.lid_out_low01_follow_attr = self.lowLid.lid_out01_follow_attr
        self.lid_out_low02_follow_attr = self.lowLid.lid_out02_follow_attr
        self.lid_out_low03_follow_attr = self.lowLid.lid_out03_follow_attr
        self.lid_out_low04_follow_attr = self.lowLid.lid_out04_follow_attr
        self.lid_out_low05_follow_attr = self.lowLid.lid_out05_follow_attr
        # self.low_lid_close_lid = self.lowLid.close_lid_attr

        self.low_lid_bind01_ctrl = self.lowLid.lid_bind01.control
        self.low_lid_bind02_ctrl = self.lowLid.lid_bind02.control
        self.low_lid_bind03_ctrl = self.lowLid.lid_bind03.control
        self.low_lid_bind04_ctrl = self.lowLid.lid_bind04.control
        self.low_lid_bind05_ctrl = self.lowLid.lid_bind05.control

        self.low_lid_bind01_grp_offset = self.lowLid.joint_bind01_grp_offset
        self.low_lid_bind05_grp_offset = self.lowLid.joint_bind05_grp_offset
        self.low_lid_all_jnt = self.lowLid.all_joint
        self.low_lid_move_grp = self.lowLid.move_grp


        # ASSIGN CURVE
        curve_up_lid = self.upLid.curve
        curve_low_lid = self.lowLid.curve

        # BLINK SETUP
        self.blink_setup(side_RGT=side_RGT, side_LFT=side_LFT, eyeball_jnt=eyeball_jnt, eye_prefix=prefix_eye,
                         eye_aim_prefix=prefix_eye_aim, curve_up=curve_up_lid,
                         curve_low=curve_low_lid, scale=scale, side=side, upLid=self.upLid,
                         lowLid=self.lowLid, position_eye_aim_ctrl=position_eye_aim_ctrl,
                         world_up_aim_object=world_up_aim_object, eye_aim_jnt=eye_jnt,
                         eye_aim_main_ctrl=eye_aim_main_ctrl, suffix_controller=suffix_controller,
                         eye_ctrl_direction=eye_ctrl_direction, base_module_nonTransform=base_module_nonTransform)

        # LID BIND FOLLOWING
        self.lid_follow_bind(range_valueA=low_lid_following_down, range_valueB=upLid_following_down_lowLid_following_up,
                             range_valueC=upLid_LR_lowLid_LR,
                             range_valueD=upLid_following_up,
                             eye_aim_follow=self.eye_aim_follow, eye_ctrl=self.eyeball_ctrl.control,
                             eye_aim_side_ctrl=self.eye_aim_ctrl.control,
                             lid_up_bind03_all_grp=self.upLid.joint_bind03_grp_all,
                             lid_low_bind03_all_grp=self.lowLid.joint_bind03_grp_all, side=side,
                             eye_aim_ctrl=eye_aim_main_ctrl,
                             lid_low_bind03_grp_offset=self.lowLid.joint_bind03_grp_offset,
                             lidUpBindOffset03Grp=self.upLid.joint_bind03_grp_offset)

        # LID CTRL FOLLOWING
        self.lid_follow_ctrl(eye_aim_follow=self.eye_aim_follow, eye_ctrl=self.eyeball_ctrl.control,
                             eye_aim_side_ctrl=self.eye_aim_ctrl.control,
                             side=side, eyeAimCtrl=eye_aim_main_ctrl,
                             lid_low_ctrl03_grp_offset=self.lowLid.lid_bind03_ctrl_grp_eyeAim,
                             lid_up_ctrl03_grp_offset=self.upLid.lid_bind03_ctrl_grp_eyeAim)

        # LID OUT ON OFF FOLLOW
        self.lid_out_eye_ctrl_trans = self.lid_out_eye_ctrl_connect(side, sub_prefix='TransLidOut', side_RGT=side_RGT,
                                                                    side_LFT=side_LFT,
                                                                    attribute='translate')
        self.lid_out_eye_ctrl_rotate = self.lid_out_eye_ctrl_connect(side, sub_prefix='RotLidOut', side_RGT=side_RGT,
                                                                     side_LFT=side_LFT,
                                                                     attribute='rotate')

        # ==================================================================================================================
        #                                                  CORNER CONTROLLER
        # ==================================================================================================================
        # controller in corner
        lid_corner_ctrl = cl.Build(lid01_up=self.upLid.jnt01,
                                   lid01_low=self.lowLid.jnt01,
                                   lid05_up=self.upLid.jnt05,
                                   lid05_low=self.lowLid.jnt05,
                                   lid_up_joint_bind01_grp_offset=self.upLid.joint_bind01_grp[1],
                                   lid_low_joint_bind01_grp_offset=self.lowLid.joint_bind01_grp[1],
                                   lid_up_joint_bind05_grp_offset=self.upLid.joint_bind05_grp[1],
                                   lid_low_joint_bind05_grp_offset=self.lowLid.joint_bind05_grp[1],
                                   scale=scale, side_RGT=side_RGT, side_LFT=side_LFT,
                                   lid_up_ctrl_bind01_grp_zro=self.upLid.lid_bind01_ctrl_grp,
                                   lid_low_ctrl_bind01_grp_zro=self.lowLid.lid_bind01_ctrl_grp,
                                   lid_up_ctrl_bind05_grp_zro=self.upLid.lid_bind05_ctrl_grp,
                                   lid_low_ctrl_bind05_grp_zro=self.lowLid.lid_bind05_ctrl_grp,
                                   prefix_name_in='cornerLidIn',
                                   prefix_name_out='cornerLidOut',
                                   side=side,
                                   ctrl_shape=ct.CIRCLEPLUS,
                                   ctrl_color='blue',
                                   suffix_controller=suffix_controller)

        self.lid_corner_in_ctrl_grp_offset = lid_corner_ctrl.lid_corner_in_ctrl_grp_offset
        self.lid_corner_out_ctrl_grp_offset = lid_corner_ctrl.lid_corner_out_ctrl_grp_offset
        self.lid_corner_in_ctrl = lid_corner_ctrl.lid_in_ctrl
        self.lid_corner_out_ctrl = lid_corner_ctrl.lid_out_ctrl

        # ==================================================================================================================
        #                                               CORNER LIP TO LID DOWN
        # ==================================================================================================================
        self.corner_lip_to_lid_down(range_great=30, range_less=10, side=side, corner_lip=corner_lip,
                                    lid_attr=corner_lip_lid_attr,
                                    lid_low_ctrl03_grp_offset=self.lowLid.lid_bind03.parent_control[1],
                                    lid_low_lip03_bind_corner=self.lowLid.joint_bind03_grp_corner_lip)

        # ==================================================================================================================
        #                                               IRIS PUPIL
        # ==================================================================================================================
        iris_pupil = ip.Build(pupil_jnt=pupil_jnt,
                              iris_jnt=iris_jnt,
                              pupil_prefix=pupil_prefix,
                              iris_prefix=iris_prefix,
                              scale=scale,
                              side=side,
                              eyeball_jnt=eyeball_jnt,
                              eye_ctrl=self.eyeball_controller,
                              eye_jnt_grp_offset=self.eyeball_ctrl_grp_offset,
                              suffix_controller=suffix_controller,
                              )

        # ==================================================================================================================
        #                                              PARENT TO GROUP
        # ==================================================================================================================

        mc.parent(self.upLid.drive_ctrl_grp, self.lowLid.drive_ctrl_grp, lid_corner_ctrl.lid_in_grp,
                  lid_corner_ctrl.lid_out_grp, self.upLid.all_joint_ctrl, self.lowLid.all_joint_ctrl,
                  self.eyeball_ctrl.control)

        mc.parent(self.upLid.locator_grp, self.upLid.curves_group, self.lowLid.locator_grp, self.lowLid.curves_group,
                  self.eye_move_all)

        mc.parent(self.upLid.bind_jnt_grp, self.lowLid.bind_jnt_grp, lid_grp)

        mc.parent(self.eyeball_ctrl.parent_control[0], self.upLid.ctrl_0204_grp, self.lowLid.ctrl_0204_grp,
                  head_up_ctrl_gimbal)
        mc.parent(lid_grp, self.upLid.move_grp, self.lowLid.move_grp, face_utils_grp)

    # ==================================================================================================================
    #                                                   FUNCTIONS
    # ==================================================================================================================
    def part_lid_follow_value_range(self, range_value, side, attr_ctrl, prefix, sub_prefix, attribute, input1='input1X',
                                    input2='input2X', prefix_name='eyeAimValueRange'):
        value_range = mc.createNode('multiplyDivide', n=prefix_name + prefix + sub_prefix + side + '_mdn')
        mc.setAttr(value_range + '.operation', 2)
        mc.setAttr(value_range + '.%s' % input1, range_value)
        mc.connectAttr(attr_ctrl + '.%s' % attribute, value_range + '.%s' % input2)

        return value_range

    def part_lid_follow_range_connected(self, side, attr_ctrl, value_range, prefix, sub_prefix, attribute, operation=2,
                                        prefix_name='eyeAimRange'):
        range_side = mc.createNode('multiplyDivide', n=prefix_name + prefix + sub_prefix + side + '_mdn')
        mc.setAttr(range_side + '.operation', operation)
        mc.connectAttr(attr_ctrl + '.%s' % attribute, range_side + '.input1X')
        mc.connectAttr(value_range + '.outputX', range_side + '.input2X')

        return range_side

    def corner_lip_to_lid_down(self, range_great, range_less, side, corner_lip, lid_attr, lid_low_ctrl03_grp_offset,
                               lid_low_lip03_bind_corner):

        if self.position > 0:
            positionValue = 1
        else:
            positionValue = -1

        value_range_great = self.part_lid_follow_value_range(range_value=range_great, side=side, attr_ctrl=corner_lip,
                                                             prefix='',
                                                             sub_prefix='rngGreat', attribute=lid_attr,
                                                             prefix_name='eyeCornerLip',
                                                             input1='input2X',
                                                             input2='input1X',
                                                             )

        value_range_less = self.part_lid_follow_value_range(range_value=range_less, side=side, attr_ctrl=corner_lip,
                                                            prefix='',
                                                            sub_prefix='rngLess', attribute=lid_attr,
                                                            prefix_name='eyeCornerLip',
                                                            input1='input2X',
                                                            input2='input1X',
                                                            )

        # CONNECT THE VALUE RANGE
        mult_ctrl_to_range_great_x = self.part_lid_follow_range_connected(side, attr_ctrl=corner_lip,
                                                                          value_range=value_range_great,
                                                                          prefix='', sub_prefix='GreatTx',
                                                                          attribute='translateX',
                                                                          operation=1, prefix_name='eyeCornerLip')

        mult_ctrl_to_range_great_y = self.part_lid_follow_range_connected(side, attr_ctrl=corner_lip,
                                                                          value_range=value_range_great,
                                                                          prefix='', sub_prefix='GreatTy',
                                                                          attribute='translateY',
                                                                          operation=1, prefix_name='eyeCornerLip')

        mult_ctrl_to_range_less_y = self.part_lid_follow_range_connected(side, attr_ctrl=corner_lip,
                                                                         value_range=value_range_less,
                                                                         prefix='', sub_prefix='LessTy',
                                                                         attribute='translateY',
                                                                         operation=1, prefix_name='eyeCornerLip')

        # CONNECT NODE MDL WHETHER ON LFT AS POSITIVE OR RIGHT AS NEGATIVE
        pos_mdl = mc.createNode('multDoubleLinear', n='eyeCornerLipPos' + side + '_mdl')
        mc.setAttr(pos_mdl + '.input2', positionValue)
        mc.connectAttr(mult_ctrl_to_range_great_x + '.outputX', pos_mdl + '.input1')

        # CONNECT THE ATTRIBUTE FOR TRANSLATE X
        mc.connectAttr(pos_mdl + '.output', lid_low_ctrl03_grp_offset + '.translateX')
        mc.connectAttr(pos_mdl + '.output', lid_low_lip03_bind_corner + '.translateX')

        # CREATE CONDITION FOR GREAT AND LESS
        condition_side = mc.createNode('condition', n='eyeCornerLipBind' + side + '_cnd')
        mc.setAttr(condition_side + '.operation', 3)
        mc.connectAttr(corner_lip + '.translateY', condition_side + '.firstTerm')

        mc.connectAttr(mult_ctrl_to_range_less_y + '.outputX', condition_side + '.colorIfTrueR')
        mc.connectAttr(mult_ctrl_to_range_great_y + '.outputX', condition_side + '.colorIfFalseR')

        mc.connectAttr(condition_side + '.outColorR', lid_low_ctrl03_grp_offset + '.translateY')
        mc.connectAttr(condition_side + '.outColorR', lid_low_lip03_bind_corner + '.translateY')

    def lid_out_eye_ctrl_connect(self, side, sub_prefix, side_RGT, side_LFT, attribute):
        new_target_up, number_target_up = tf.reorder_number(prefix=self.eyeball_controller, side_RGT=side_RGT,
                                                            side_LFT=side_LFT)

        mdn = mc.createNode('multiplyDivide',
                            n=au.prefix_name(new_target_up) + sub_prefix + number_target_up + side + '_mdn')
        mc.connectAttr(self.eyeball_controller + '.%s' % attribute, mdn + '.input1')
        mc.connectAttr(self.eyeball_controller + '.' + self.lid_out_follow, mdn + '.input2X')
        mc.connectAttr(self.eyeball_controller + '.' + self.lid_out_follow, mdn + '.input2Y')
        mc.connectAttr(self.eyeball_controller + '.' + self.lid_out_follow, mdn + '.input2Z')

        return mdn

    def blink_setup(self, side_RGT, side_LFT, eyeball_jnt, eye_prefix, eye_aim_prefix, curve_up, curve_low, scale,
                    side, upLid, lowLid, position_eye_aim_ctrl, world_up_aim_object, eye_aim_main_ctrl, eye_aim_jnt,
                    suffix_controller, base_module_nonTransform,
                    eye_ctrl_direction
                    ):

        # ==============================================================================================================
        #                                             EYEBALL CONTROLLER
        # ==============================================================================================================

        eyeball_grp = tf.create_parent_transform(parent_list=['Zro', 'Offset'], object=eyeball_jnt,
                                                 match_position=eyeball_jnt,
                                                 prefix='eyeball',
                                                 suffix='_jnt', side=side)

        self.eyeball_ctrl = ct.Control(match_obj_first_position=eyeball_jnt,
                                       prefix=eye_prefix,
                                       shape=ct.JOINTPLUS, groups_ctrl=['Zro', 'Offset'],
                                       ctrl_size=scale * 0.5,
                                       ctrl_color='turquoiseBlue', lock_channels=['v'], side=side,
                                       suffix=suffix_controller,
                                       connection=['connectMatrixAll'])

        self.eyeball_controller = self.eyeball_ctrl.control
        self.eyeball_ctrl_grp_offset = eyeball_grp[1]

        # ADD ATTRIBUTE
        au.add_attribute(objects=[self.eyeball_ctrl.control], long_name=['lidDegree'], nice_name=[' '], at="enum",
                         en='Lid Degree', channel_box=True)

        self.eye_aim_follow = au.add_attribute(objects=[self.eyeball_ctrl.control], long_name=['eyeAimFollow'],
                                               attributeType="float", min=0.001, dv=1, keyable=True)

        self.lid_out_follow = au.add_attribute(objects=[self.eyeball_ctrl.control], long_name=['lidOutFollow'],
                                               attributeType="float", min=0, dv=0.5, keyable=True)

        # EYELID CLOSER
        au.add_attribute(objects=[self.eyeball_ctrl.control], long_name=['lidCloser'], nice_name=[' '], at="enum",
                         en='Lid Closer', channel_box=True)

        self.lid_position = au.add_attribute(objects=[self.eyeball_ctrl.control], long_name=['lidPos'],
                                             attributeType="float", min=0, max=1, dv=0.5, keyable=True)
        self.upLid_closer = au.add_attribute(objects=[self.eyeball_ctrl.control], long_name=['upLid'],
                                             attributeType="float", min=-1, max=1, dv=0, keyable=True)
        self.lowLid_closer = au.add_attribute(objects=[self.eyeball_ctrl.control], long_name=['lowLid'],
                                              attributeType="float", min=-1, max=1, dv=0, keyable=True)
        # ==============================================================================================================
        #                                                   EYE AIM
        # ==============================================================================================================

        if mc.xform(eyeball_jnt, q=1, ws=1, t=1)[0] > 0:
            ctrl_color = 'red'
        else:
            ctrl_color = 'yellow'

        self.eye_aim_ctrl = ct.Control(match_obj_first_position=eye_aim_jnt,
                                       prefix=eye_aim_prefix,
                                       shape=ct.LOCATOR, groups_ctrl=['Zro', 'Offset'],
                                       ctrl_size=scale * 0.25, suffix=suffix_controller,
                                       ctrl_color=ctrl_color, lock_channels=['v', 'r', 's'], side=side)

        get_attribute = mc.getAttr(self.eye_aim_ctrl.parent_control[0] + '.translateZ')
        mc.setAttr(self.eye_aim_ctrl.parent_control[0] + '.translateZ', get_attribute + (position_eye_aim_ctrl * scale))

        aim_eye_constraint = mc.aimConstraint(self.eye_aim_ctrl.control, eyeball_grp[1], mo=1, weight=1,
                                              aimVector=(0, 0, 1), upVector=(0, 1, 0),
                                              worldUpType="object", worldUpObject=world_up_aim_object)

        # CONSTRAINT RENAME
        au.constraint_rename(aim_eye_constraint)

        # PARENT EYE AIM TO EYE AIM MAIN CTRL
        mc.parent(self.eye_aim_ctrl.parent_control[0], eye_aim_main_ctrl)

        # MAKE GRP TRANSFORM EYE JNT
        eye_grp = tf.create_parent_transform(parent_list=[''], object=eye_aim_jnt, match_position=eye_aim_jnt,
                                             prefix='eye',
                                             suffix='_jnt', side=side)

        # ROTATE THE EYE GROUP
        if self.position >= 0:
            mc.setAttr(eye_grp[0] + '.rotateY', eye_ctrl_direction)

        else:
            mc.setAttr(eye_grp[0] + '.rotateY', eye_ctrl_direction * -1)

        # CONNECT THE AIM JNT
        au.connect_attr_object(self.eyeball_controller, eye_aim_jnt)

        # ==============================================================================================================
        #                                                   BLINK
        # ==============================================================================================================
        # CREATE CURVE MID BLINK
        curve_blink_bind_mid_old = mc.curve(d=3, ep=[(self.upLid.xform_jnt01), (self.upLid.xform_jnt05)])

        curve_blink_bind_mid_rebuild = mc.rebuildCurve(curve_blink_bind_mid_old, ch=0, rpo=1, rt=0, end=1, kr=0, kcp=0,
                                                       kep=1, kt=0, s=8, d=3, tol=0.01)

        curve_blink_bind_mid = mc.rename(curve_blink_bind_mid_rebuild, ('lidBlink' + side + '_crv'))

        curve_blink_up = mc.duplicate(curve_up, n='lidBlinkUp' + side + '_crv')[0]
        curve_blink_low = mc.duplicate(curve_low, n='lidBlinkLow' + side + '_crv')[0]

        blink_bsn = \
            mc.blendShape(upLid.deform_curve, lowLid.deform_curve, curve_blink_bind_mid, n=('lidBlink' + side + '_bsn'),
                          weight=[(0, 1), (1, 0)])[0]

        # SKINNING UP AND DOWN BIND JOINT
        # skinning the joint to the bind curve
        skin_cluster = mc.skinCluster([upLid.jnt05, upLid.jnt04, upLid.jnt01, upLid.jnt02, upLid.jnt03, lowLid.jnt05,
                                       lowLid.jnt04, lowLid.jnt01, lowLid.jnt02, lowLid.jnt03], curve_blink_bind_mid,
                                      n='%s%s%s%s' % (
                                          'lidBlink', 'Bind', side, '_sc'),
                                      tsb=True, bm=0, sm=0, nw=1, mi=3)

        # Distribute the skin
        skin_percent_index0 = '%s.cv[0]' % curve_blink_bind_mid
        skin_percent_index1 = '%s.cv[1]' % curve_blink_bind_mid
        skin_percent_index2 = '%s.cv[2]' % curve_blink_bind_mid
        skin_percent_index3 = '%s.cv[3]' % curve_blink_bind_mid
        skin_percent_index4 = '%s.cv[4]' % curve_blink_bind_mid
        skin_percent_index5 = '%s.cv[5]' % curve_blink_bind_mid
        skin_percent_index6 = '%s.cv[6]' % curve_blink_bind_mid
        skin_percent_index7 = '%s.cv[7]' % curve_blink_bind_mid
        skin_percent_index8 = '%s.cv[8]' % curve_blink_bind_mid
        skin_percent_index9 = '%s.cv[9]' % curve_blink_bind_mid
        skin_percent_index10 = '%s.cv[10]' % curve_blink_bind_mid

        mc.skinPercent(skin_cluster[0], skin_percent_index0, tv=[(upLid.jnt01, 0.5), (lowLid.jnt01, 0.5)])
        mc.skinPercent(skin_cluster[0], skin_percent_index1,
                       tv=[(upLid.jnt01, 0.45), (upLid.jnt02, 0.05), (lowLid.jnt01, 0.45), (lowLid.jnt02, 0.05)])
        mc.skinPercent(skin_cluster[0], skin_percent_index2,
                       tv=[(upLid.jnt01, 0.35), (upLid.jnt02, 0.15), (lowLid.jnt01, 0.35), (lowLid.jnt02, 0.15)])
        mc.skinPercent(skin_cluster[0], skin_percent_index3,
                       tv=[(upLid.jnt02, 0.25), (upLid.jnt01, 0.125), (upLid.jnt03, 0.125), (lowLid.jnt02, 0.25),
                           (lowLid.jnt01, 0.125), (lowLid.jnt03, 0.125)])
        mc.skinPercent(skin_cluster[0], skin_percent_index4,
                       tv=[(upLid.jnt02, 0.15), (upLid.jnt03, 0.35), (lowLid.jnt02, 0.15), (lowLid.jnt03, 0.35)])
        mc.skinPercent(skin_cluster[0], skin_percent_index5, tv=[(upLid.jnt03, 0.5), (lowLid.jnt03, 0.5)])
        mc.skinPercent(skin_cluster[0], skin_percent_index6,
                       tv=[(upLid.jnt04, 0.15), (upLid.jnt03, 0.35), (lowLid.jnt04, 0.15), (lowLid.jnt03, 0.35)])
        mc.skinPercent(skin_cluster[0], skin_percent_index7,
                       tv=[(upLid.jnt04, 0.25), (upLid.jnt05, 0.125), (upLid.jnt03, 0.125), (lowLid.jnt04, 0.25),
                           (lowLid.jnt05, 0.125), (lowLid.jnt03, 0.125)])
        mc.skinPercent(skin_cluster[0], skin_percent_index8,
                       tv=[(upLid.jnt05, 0.35), (upLid.jnt04, 0.15), (lowLid.jnt05, 0.35), (lowLid.jnt04, 0.15)])
        mc.skinPercent(skin_cluster[0], skin_percent_index9,
                       tv=[(upLid.jnt05, 0.45), (upLid.jnt04, 0.05), (lowLid.jnt05, 0.45), (lowLid.jnt04, 0.05)])
        mc.skinPercent(skin_cluster[0], skin_percent_index10, tv=[(upLid.jnt05, 0.5), (lowLid.jnt05, 0.5)])

        mc.select(cl=1)
        # replace position LFT and RGT
        crv_up_new_name = tf.reposition_side(object=curve_up, side_RGT=side_RGT, side_LFT=side_LFT)

        # wire deform up on mid curves
        sticky_mid_wire_deformer_up = mc.wire(curve_blink_up, dds=(0, 100 * scale), wire=curve_blink_bind_mid)
        sticky_mid_wire_deformer_up[0] = mc.rename(sticky_mid_wire_deformer_up[0],
                                                   (au.prefix_name(crv_up_new_name) + 'Blink' + side + '_wireNode'))
        mc.setAttr(sticky_mid_wire_deformer_up[0] + '.scale[0]', 0)

        # SET TO LOW CURVE
        mc.setAttr(blink_bsn + '.%s' % upLid.deform_curve, 0)
        mc.setAttr(blink_bsn + '.%s' % lowLid.deform_curve, 1)

        mc.select(cl=1)
        # replace position LFT and RGT
        crv_low_new_name = tf.reposition_side(object=curve_low, side_RGT=side_RGT, side_LFT=side_LFT)

        sticky_mid_wire_deformer_low = mc.wire(curve_blink_low, dds=(0, 100 * scale), wire=curve_blink_bind_mid)
        sticky_mid_wire_deformer_low[0] = mc.rename(sticky_mid_wire_deformer_low[0],
                                                    (au.prefix_name(crv_low_new_name) + 'Blink' + side + '_wireNode'))
        mc.setAttr(sticky_mid_wire_deformer_low[0] + '.scale[0]', 0)

        # SET KEYFRAME
        mc.setDrivenKeyframe(blink_bsn + '.%s' % upLid.deform_curve,
                             cd='%s.%s' % (self.eyeball_ctrl.control, self.lid_position),
                             dv=0, v=1, itt='linear', ott='linear')

        mc.setDrivenKeyframe(blink_bsn + '.%s' % upLid.deform_curve,
                             cd='%s.%s' % (self.eyeball_ctrl.control, self.lid_position),
                             dv=0.5, v=0, itt='linear', ott='linear')

        mc.setDrivenKeyframe(blink_bsn + '.%s' % lowLid.deform_curve,
                             cd='%s.%s' % (self.eyeball_ctrl.control, self.lid_position),
                             dv=0.5, v=0, itt='linear', ott='linear')

        mc.setDrivenKeyframe(blink_bsn + '.%s' % lowLid.deform_curve,
                             cd='%s.%s' % (self.eyeball_ctrl.control, self.lid_position),
                             dv=1, v=1, itt='linear', ott='linear')

        # CONNECT TO BLENDSHAPE BIND CURVE
        up_lid_bsn = mc.blendShape(curve_blink_up, curve_up, n=('lidBlinkUp' + side + '_bsn'),
                                   weight=[(0, 1)])[0]

        mc.connectAttr(self.eyeball_controller + '.%s' % self.upLid_closer, up_lid_bsn + '.%s' % curve_blink_up)

        low_lid_bsn = mc.blendShape(curve_blink_low, curve_low, n=('lidBlinkLow' + side + '_bsn'),
                                    weight=[(0, 1)])[0]

        mc.connectAttr(self.eyeball_controller + '.%s' % self.lowLid_closer, low_lid_bsn + '.%s' % curve_blink_low)

        # parent eyeblink crve to face curve grp
        mc.parent(curve_blink_bind_mid, mc.listConnections(sticky_mid_wire_deformer_low[0] + '.baseWire[0]')[0],
                  mc.listConnections(sticky_mid_wire_deformer_up[0] + '.baseWire[0]')[0], base_module_nonTransform)

    # CONNECTION UP AND LOW FOLLOW LID BIND
    def lid_follow_bind(self, range_valueA, range_valueB, range_valueC, range_valueD, eye_aim_follow, eye_ctrl,
                        eye_aim_side_ctrl,
                        lid_up_bind03_all_grp, lid_low_bind03_all_grp, side,
                        eye_aim_ctrl, lid_low_bind03_grp_offset, lidUpBindOffset03Grp):

        self.part_lid_bind_follow(range_valueA, range_valueB, range_valueC, range_valueD, eye_aim_follow, eye_ctrl,
                                  eye_aim_side_ctrl,
                                  lid_bind03_grp=lid_up_bind03_all_grp, prefix='Up',
                                  side=side, up_lid=True)
        self.part_lid_bind_follow(range_valueA, range_valueB, range_valueC, range_valueD, eye_aim_follow, eye_ctrl,
                                  eye_aim_side_ctrl,
                                  lid_bind03_grp=lid_low_bind03_all_grp, prefix='Low',
                                  side=side, up_lid=False)

        self.part_lid_bind_follow(range_valueA, range_valueB, range_valueC, range_valueD, eye_aim_follow, eye_ctrl,
                                  eye_aim_ctrl,
                                  lid_bind03_grp=lidUpBindOffset03Grp, prefix='MainUp',
                                  side=side, up_lid=True)

        self.part_lid_bind_follow(range_valueA, range_valueB, range_valueC, range_valueD, eye_aim_follow, eye_ctrl,
                                  eye_aim_ctrl,
                                  lid_bind03_grp=lid_low_bind03_grp_offset, prefix='MainLow',
                                  side=side, up_lid=False)

    def part_lid_bind_follow(self, range_valueA, range_valueB, range_valueC, range_valueD, eye_aim_follow,
                             eye_ctrl, eye_aim_ctrl, lid_bind03_grp, side, up_lid, prefix='', ):
        value_range_b = self.part_lid_follow_value_range(range_value=range_valueB, side=side, attr_ctrl=eye_ctrl,
                                                         prefix=prefix,
                                                         sub_prefix='BBind', attribute=eye_aim_follow)
        value_range_c = self.part_lid_follow_value_range(range_value=range_valueC, side=side, attr_ctrl=eye_ctrl,
                                                         prefix=prefix,
                                                         sub_prefix='CBind', attribute=eye_aim_follow)

        # CREATE CONDITION AIM SIDE
        condition_aim_side_greater = mc.createNode('condition', n='eyeAimBind' + prefix + side + '_cnd')
        mc.setAttr(condition_aim_side_greater + '.colorIfTrueG', 0)
        mc.connectAttr(eye_aim_ctrl + '.translateY', condition_aim_side_greater + '.firstTerm')

        # CREATE DIVIDE RANGE AIM SIDE B
        range_aim_bind_b = self.part_lid_follow_range_connected(side, eye_aim_ctrl, value_range=value_range_b,
                                                                prefix=prefix, sub_prefix='BBind',
                                                                attribute='translateY')
        mc.connectAttr(range_aim_bind_b + '.outputX', condition_aim_side_greater + '.colorIfTrueR')

        # CREATE DIVIDE RANGE AIM SIDE D
        if up_lid:
            value_rangeD = self.part_lid_follow_value_range(range_value=range_valueD, side=side, attr_ctrl=eye_ctrl,
                                                            prefix=prefix,
                                                            sub_prefix='DBind', attribute=eye_aim_follow)
            mc.setAttr(condition_aim_side_greater + '.operation', 5)
            range_aim_bindD = self.part_lid_follow_range_connected(side, eye_aim_ctrl, value_range=value_rangeD,
                                                                   prefix=prefix, sub_prefix='DBind',
                                                                   attribute='translateY')
            mc.connectAttr(range_aim_bindD + '.outputX', condition_aim_side_greater + '.colorIfFalseR')

        # CREATE DIVIDE RANGE AIM SIDE A
        else:
            value_rangeA = self.part_lid_follow_value_range(range_value=range_valueA, side=side, attr_ctrl=eye_ctrl,
                                                            prefix=prefix,
                                                            sub_prefix='ABind', attribute=eye_aim_follow)
            mc.setAttr(condition_aim_side_greater + '.operation', 3)
            range_aim_bindA = self.part_lid_follow_range_connected(side, eye_aim_ctrl, value_range=value_rangeA,
                                                                   prefix=prefix, sub_prefix='ABind',
                                                                   attribute='translateY')
            mc.connectAttr(range_aim_bindA + '.outputX', condition_aim_side_greater + '.colorIfFalseR')

        mc.connectAttr(condition_aim_side_greater + '.outColorR', lid_bind03_grp + '.translateY')

        # CREATE DIVIDE RANGE AIM SIDE C
        range_aim_bindC = self.part_lid_follow_range_connected(side, eye_aim_ctrl, value_range=value_range_c,
                                                               prefix=prefix, sub_prefix='CBind',
                                                               attribute='translateX')
        mc.connectAttr(range_aim_bindC + '.outputX', lid_bind03_grp + '.translateX')

    def lid_follow_ctrl(self, eye_aim_follow, eye_ctrl, eye_aim_side_ctrl, side,
                        eyeAimCtrl, lid_low_ctrl03_grp_offset, lid_up_ctrl03_grp_offset):

        value_rangeA = self.part_lid_follow_value_range(range_value=20.0, side=side, attr_ctrl=eye_ctrl, prefix='',
                                                        sub_prefix='ACtrl', attribute=eye_aim_follow)
        value_rangeB = self.part_lid_follow_value_range(range_value=30.0, side=side, attr_ctrl=eye_ctrl, prefix='',
                                                        sub_prefix='BCtrl', attribute=eye_aim_follow)
        value_rangeC = self.part_lid_follow_value_range(range_value=80.0, side=side, attr_ctrl=eye_ctrl, prefix='',
                                                        sub_prefix='CCtrl', attribute=eye_aim_follow)

        # CREATE DIVIDE RANGE AIM AND AIM SIDE C
        range_aimC = self.part_lid_follow_range_connected(side=side, attr_ctrl=eyeAimCtrl, value_range=value_rangeC,
                                                          prefix='Main', sub_prefix='CCtrl', attribute='translateX')

        range_aim_sideC = self.part_lid_follow_range_connected(side=side, attr_ctrl=eye_aim_side_ctrl,
                                                               value_range=value_rangeC,
                                                               prefix='', sub_prefix='CCtrl', attribute='translateX')

        sum_aim_side_and_aimC = mc.createNode('plusMinusAverage', n='eyeAimCtrlRangeC' + side + '_pma')
        mc.connectAttr(range_aimC + '.outputX', sum_aim_side_and_aimC + '.input1D[0]')
        mc.connectAttr(range_aim_sideC + '.outputX', sum_aim_side_and_aimC + '.input1D[1]')

        # CREATE DIVIDE RANGE AIM SIDE A
        range_aimA = self.part_lid_follow_range_connected(side=side, attr_ctrl=eyeAimCtrl, value_range=value_rangeA,
                                                          prefix='Main', sub_prefix='ACtrl', attribute='translateY')
        range_aim_sideA = self.part_lid_follow_range_connected(side=side, attr_ctrl=eye_aim_side_ctrl,
                                                               value_range=value_rangeA,
                                                               prefix='', sub_prefix='ACtrl', attribute='translateY')

        sum_aim_side_and_aimA = mc.createNode('plusMinusAverage', n='eyeAimCtrlRangeA' + side + '_pma')
        mc.connectAttr(range_aimA + '.outputX', sum_aim_side_and_aimA + '.input1D[0]')
        mc.connectAttr(range_aim_sideA + '.outputX', sum_aim_side_and_aimA + '.input1D[1]')

        # CREATE DIVIDE RANGE AIM B
        range_aimB = self.part_lid_follow_range_connected(side=side, attr_ctrl=eyeAimCtrl, value_range=value_rangeB,
                                                          prefix='Main', sub_prefix='BCtrl', attribute='translateY')
        range_aim_sideB = self.part_lid_follow_range_connected(side=side, attr_ctrl=eye_aim_side_ctrl,
                                                               value_range=value_rangeB,
                                                               prefix='', sub_prefix='BCtrl', attribute='translateY')

        range_aimB_rev = mc.createNode('multDoubleLinear', n='eyeAimCtrlRangeBRev' + side + '_mdl')
        mc.setAttr(range_aimB_rev + '.input1', -1)
        mc.connectAttr(range_aimB + '.outputX', range_aimB_rev + '.input2')

        sum_aim_side_and_aimB = mc.createNode('plusMinusAverage', n='eyeAimCtrlRangeB' + side + '_pma')
        mc.setAttr(sum_aim_side_and_aimB + '.operation', 2)
        mc.connectAttr(range_aimB_rev + '.output', sum_aim_side_and_aimB + '.input1D[0]')
        mc.connectAttr(range_aim_sideB + '.outputX', sum_aim_side_and_aimB + '.input1D[1]')

        mc.connectAttr(sum_aim_side_and_aimC + '.output1D', lid_up_ctrl03_grp_offset + '.translateX')
        mc.connectAttr(sum_aim_side_and_aimA + '.output1D', lid_up_ctrl03_grp_offset + '.translateY')
        mc.connectAttr(sum_aim_side_and_aimC + '.output1D', lid_low_ctrl03_grp_offset + '.translateX')
        mc.connectAttr(sum_aim_side_and_aimB + '.output1D', lid_low_ctrl03_grp_offset + '.translateY')
