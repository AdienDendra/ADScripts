from __future__ import absolute_import

import maya.cmds as cmds

from rigging.library.base.face import wire as rlbf_wire, lidCorner as rlbf_lidCorner
from rigging.library.utils import controller as rlu_controller
from rigging.tools import utils as rt_utils


class LidOut:
    def __init__(self,
                 face_utils_grp,
                 curve_up_template,
                 curve_low_template,
                 offset_jnt02_bind_position,
                 offset_jnt04_bind_position,
                 ctrl01_direction,
                 ctrl02_direction,
                 ctrl03_direction,
                 ctrl04_direction,
                 ctrl05_direction,
                 ctrl_color,
                 shape,
                 scale,
                 side_RGT,
                 side_LFT,
                 side,
                 eyeball_jnt,
                 head_up_jnt,
                 eye_ctrl,
                 corner_lip,
                 corner_lip_attr,
                 ctrl_bind01_up,
                 ctrl_bind02_up,
                 ctrl_bind03_up,
                 ctrl_bind04_up,
                 ctrl_bind05_up,
                 ctrl_bind01_low,
                 ctrl_bind02_low,
                 ctrl_bind03_low,
                 ctrl_bind04_low,
                 ctrl_bind05_low,
                 lid_out_follow,
                 close_lid_up_attr,
                 close_lid_low_attr,
                 eyeball_ctrl,
                 lid_corner_in_ctrl,
                 lid_corner_out_ctrl,
                 wire_up_bind01_grp_offset,
                 wire_low_bind01_grp_offset,
                 wire_up_bind05_grp_offset,
                 wire_low_bind05_grp_offset,
                 lid_out_on_off_follow_trans_mdn,
                 lid_out_on_off_follow_rot_mdn,
                 eye_ctrl_direction,
                 suffix_controller,
                 base_module_nonTransform,
                 parent_sgame_joint=None,
                 game_bind_joint=False
                 ):

        # ==================================================================================================================
        #                                               LID OUT CONTROLLER
        # ==================================================================================================================
        self.position = cmds.xform(eyeball_jnt, ws=1, q=1, t=1)[0]

        wire_up = rlbf_wire.Build(curve_template=curve_up_template, position_joint_direction=eyeball_jnt, scale=scale,
                                  side_LFT=side_LFT, side_RGT=side_RGT, side=side,
                                  offset_jnt02_bind_position=offset_jnt02_bind_position,
                                  offset_jnt04_bind_position=offset_jnt04_bind_position,
                                  ctrl01_direction=ctrl01_direction, ctrl02_direction=ctrl02_direction,
                                  ctrl03_direction=ctrl03_direction, ctrl04_direction=ctrl04_direction,
                                  ctrl05_direction=ctrl05_direction, suffix_controller=suffix_controller,
                                  ctrl_color=ctrl_color, wire_low_controller=False, shape=shape,
                                  face_utils_grp=face_utils_grp,
                                  connect_with_corner_ctrl=True, base_module_nonTransform=base_module_nonTransform,
                                  game_bind_joint=game_bind_joint, parent_sgame_joint=parent_sgame_joint
                                  )

        wire_low = rlbf_wire.Build(curve_template=curve_low_template, position_joint_direction=eyeball_jnt, scale=scale,
                                   side_LFT=side_LFT, side_RGT=side_RGT, side=side,
                                   offset_jnt02_bind_position=offset_jnt02_bind_position,
                                   offset_jnt04_bind_position=offset_jnt04_bind_position,
                                   ctrl01_direction=ctrl01_direction, ctrl02_direction=ctrl02_direction,
                                   ctrl03_direction=ctrl03_direction, ctrl04_direction=ctrl04_direction,
                                   ctrl05_direction=ctrl05_direction, suffix_controller=suffix_controller,
                                   ctrl_color=ctrl_color, wire_low_controller=True, shape=shape,
                                   face_utils_grp=face_utils_grp,
                                   connect_with_corner_ctrl=True, base_module_nonTransform=base_module_nonTransform,
                                   game_bind_joint=game_bind_joint, parent_sgame_joint=parent_sgame_joint
                                   )

        self.lid_out_up_jnt = wire_up.all_joint
        self.lid_out_low_jnt = wire_low.all_joint

        # ==================================================================================================================
        #                                                  CORNER CONTROLLER
        # ==================================================================================================================
        # controller in corner
        lid_corner_ctrl = rlbf_lidCorner.Build(lid01_up=wire_up.jnt01,
                                               lid01_low=wire_low.jnt01,
                                               lid05_up=wire_up.jnt05,
                                               lid05_low=wire_low.jnt05,
                                               lid_up_joint_bind01_grp_offset=wire_up.joint_bind01_grp_all,
                                               lid_low_joint_bind01_grp_offset=wire_low.joint_bind01_grp_all,
                                               lid_up_joint_bind05_grp_offset=wire_up.joint_bind05_grp_all,
                                               lid_low_joint_bind05_grp_offset=wire_low.joint_bind05_grp_all,
                                               scale=scale, side_RGT=side_RGT, side_LFT=side_LFT,
                                               lid_up_ctrl_bind01_grp_zro=wire_up.controller_bind01_grp,
                                               lid_low_ctrl_bind01_grp_zro=wire_low.controller_bind01_grp,
                                               lid_up_ctrl_bind05_grp_zro=wire_up.controller_bind05_grp,
                                               lid_low_ctrl_bind05_grp_zro=wire_low.controller_bind05_grp,
                                               prefix_name_in='cornerOutLidIn',
                                               prefix_name_out='cornerOutLidOut',
                                               side=side,
                                               ctrl_shape=rlu_controller.JOINT,
                                               ctrl_color='red',
                                               lid_out=True,
                                               suffix_controller=suffix_controller)

        # ADJUSTING LID CORNER CONTROLLER TO LID OUT CORNER CONTROLLER
        self.lid_in_corner_follow_attr = rt_utils.add_attribute(objects=[lid_corner_in_ctrl],
                                                                long_name=['lidOutFollow'],
                                                                attributeType="float", min=0, dv=1, keyable=True)
        self.corner_multiply_lid_follow(wire=rt_utils.prefix_name(wire_up.prefix_name_crv), side=side,
                                        bind_grp_source=wire_up_bind01_grp_offset,
                                        bind_grp_destination=wire_up.joint_bind01_grp_corner,
                                        sub_prefix='Bind01',
                                        ctrl_corner_lid=lid_corner_in_ctrl,
                                        attribute=self.lid_in_corner_follow_attr)

        self.corner_multiply_lid_follow(wire=rt_utils.prefix_name(wire_low.prefix_name_crv), side=side,
                                        bind_grp_source=wire_low_bind01_grp_offset,
                                        bind_grp_destination=wire_low.joint_bind01_grp_corner,
                                        sub_prefix='Bind01',
                                        ctrl_corner_lid=lid_corner_in_ctrl,
                                        attribute=self.lid_in_corner_follow_attr)

        self.lid_out_corner_follow_attr = rt_utils.add_attribute(objects=[lid_corner_out_ctrl],
                                                                 long_name=['lidOutFollow'],
                                                                 attributeType="float", min=0, dv=1, keyable=True)

        self.corner_multiply_lid_follow(wire=rt_utils.prefix_name(wire_up.prefix_name_crv), side=side,
                                        bind_grp_source=wire_up_bind05_grp_offset,
                                        bind_grp_destination=wire_up.joint_bind05_grp_corner,
                                        sub_prefix='Bind05',
                                        ctrl_corner_lid=lid_corner_out_ctrl,
                                        attribute=self.lid_out_corner_follow_attr)

        self.corner_multiply_lid_follow(wire=rt_utils.prefix_name(wire_low.prefix_name_crv), side=side,
                                        bind_grp_source=wire_low_bind05_grp_offset,
                                        bind_grp_destination=wire_low.joint_bind05_grp_corner,
                                        sub_prefix='Bind05',
                                        ctrl_corner_lid=lid_corner_out_ctrl,
                                        attribute=self.lid_out_corner_follow_attr)

        self.corner_multiply_lid_follow(wire=rt_utils.prefix_name(wire_up.prefix_name_crv), side=side,
                                        bind_grp_source=lid_corner_in_ctrl,
                                        bind_grp_destination=lid_corner_ctrl.lid_corner_in_ctrl_grp_offset,
                                        sub_prefix='Ctrl',
                                        ctrl_corner_lid=lid_corner_in_ctrl,
                                        attribute=self.lid_in_corner_follow_attr)

        self.corner_multiply_lid_follow(wire=rt_utils.prefix_name(wire_low.prefix_name_crv), side=side,
                                        bind_grp_source=lid_corner_out_ctrl,
                                        bind_grp_destination=lid_corner_ctrl.lid_corner_out_ctrl_grp_offset,
                                        sub_prefix='Ctrl',
                                        ctrl_corner_lid=lid_corner_out_ctrl,
                                        attribute=self.lid_out_corner_follow_attr)

        # ==================================================================================================================
        #                                               LIP TO LOWER LID OUT
        # ==================================================================================================================
        # CONNECT THE BIND LID OUT TO CONTROLLER BIND LID OUT 03
        rt_utils.connect_attr_translate(wire_low.joint_bind03_grp, wire_low.controller_bind03_grp)

        ## CREATE FOLLOWING LID
        self.position = cmds.xform(wire_low.joint_bind03_grp, ws=1, q=1, t=1)[0]

        if self.position < 0:
            multiplier = -1
        else:
            multiplier = 1

        # MULTIPLY BY MULTIPLIER
        mdl_node = cmds.createNode('multDoubleLinear',
                                   n=rt_utils.prefix_name(wire_low.prefix_name_crv) + 'Reverse' + side + '_mdl')
        cmds.connectAttr(corner_lip + '.translateX', mdl_node + '.input1')
        cmds.setAttr(mdl_node + '.input2', multiplier)

        # CREATE CONDITION
        condition_node = cmds.createNode('condition', n=rt_utils.prefix_name(wire_low.prefix_name_crv) + side + '_cnd')
        cmds.setAttr(condition_node + '.operation', 3)
        cmds.setAttr(condition_node + '.colorIfTrueR', 20)
        cmds.setAttr(condition_node + '.colorIfFalseR', 50)
        cmds.connectAttr(corner_lip + '.translateY', condition_node + '.firstTerm')

        # CREATE PMA FOR SUM
        jnt03_translate = cmds.xform(wire_low.jnt03, ws=1, q=1, t=1)
        pma_node = cmds.createNode('plusMinusAverage', n=rt_utils.prefix_name(wire_low.prefix_name_crv) + side + '_pma')
        cmds.setAttr(pma_node + '.input3D[0].input3Dx', jnt03_translate[0])
        cmds.setAttr(pma_node + '.input3D[0].input3Dy', jnt03_translate[1])
        cmds.setAttr(pma_node + '.input3D[0].input3Dz', jnt03_translate[2])

        # CONNECT THE ATTRIBUTE TO MDN
        multiply = self.multiply_divide(wire_low_name=wire_low.prefix_name_crv + 'Mult', side=side,
                                        object_1X=mdl_node + '.output',
                                        object_1Y=corner_lip + '.translateY', object_1Z=corner_lip + '.translateY',
                                        object_2X=corner_lip + '.%s' % corner_lip_attr,
                                        object_2Y=corner_lip + '.%s' % corner_lip_attr,
                                        object_2Z=corner_lip + '.%s' % corner_lip_attr, set_attr=False, scale=scale)

        divide = self.multiply_divide(wire_low_name=wire_low.prefix_name_crv + 'Div', side=side,
                                      object_1X=multiply + '.outputX',
                                      object_1Y=multiply + '.outputY', object_1Z=multiply + '.outputZ', operation=2,
                                      valueX=20, valueY=20, valueZ=20, set_attr=True, scale=scale)

        cmds.connectAttr(condition_node + '.outColorR', divide + '.input2Y')
        cmds.connectAttr(divide + '.output', pma_node + '.input3D[1]')

        # CONNECT TO OBJECT
        cmds.connectAttr(pma_node + '.output3D', wire_low.joint_bind03_grp + '.translate')

        # ==================================================================================================================
        #                                         ADD FOLLOWING ATTR CONTROLLER
        # ==================================================================================================================
        # UP LID
        self.all_ctrl_connecting_lid_out(wire=rt_utils.prefix_name(wire_up.prefix_name_crv), side=side,
                                         ctrl_bind01=ctrl_bind01_up,
                                         ctrl_bind02=ctrl_bind02_up,
                                         ctrl_bind03=ctrl_bind03_up, ctrl_bind04=ctrl_bind04_up,
                                         ctrl_bind05=ctrl_bind05_up,
                                         lid_out_follow=lid_out_follow,
                                         eyeball_ctrl=eyeball_ctrl,
                                         drv_bind01_grp_offset=wire_up.joint_bind01_grp_offset,
                                         drv_bind02_grp_offset=wire_up.joint_bind02_grp_offset,
                                         drv_bind03_grp_offset=wire_up.joint_bind03_grp_offset,
                                         drv_bind04_grp_offset=wire_up.joint_bind04_grp_offset,
                                         drv_bind05_grp_offset=wire_up.joint_bind05_grp_offset,
                                         close_lid_attr=close_lid_up_attr, upLid=True)
        # LOW LID
        self.all_ctrl_connecting_lid_out(wire=rt_utils.prefix_name(wire_low.prefix_name_crv), side=side,
                                         ctrl_bind01=ctrl_bind01_low,
                                         ctrl_bind02=ctrl_bind02_low,
                                         ctrl_bind03=ctrl_bind03_low, ctrl_bind04=ctrl_bind04_low,
                                         ctrl_bind05=ctrl_bind05_low,
                                         lid_out_follow=lid_out_follow,
                                         eyeball_ctrl=eyeball_ctrl,
                                         drv_bind01_grp_offset=wire_low.joint_bind01_grp_offset,
                                         drv_bind02_grp_offset=wire_low.joint_bind02_grp_offset,
                                         drv_bind03_grp_offset=wire_low.joint_bind03_grp_offset,
                                         drv_bind04_grp_offset=wire_low.joint_bind04_grp_offset,
                                         drv_bind05_grp_offset=wire_low.joint_bind05_grp_offset,
                                         close_lid_attr=close_lid_low_attr, upLid=False)

        # PARENT TO GROUP
        cmds.parent(wire_up.joint_grp, wire_low.joint_grp, head_up_jnt)
        cmds.parent(wire_up.ctrl_driver_grp, wire_low.ctrl_driver_grp, lid_corner_ctrl.lid_in_grp,
                    lid_corner_ctrl.lid_out_grp, eye_ctrl)

        # ==================================================================================================================
        #                                         ROTATE THE OFFSET LID OUT BIND GRP
        # ==================================================================================================================

        for up, low in zip(wire_up.locator_grp_offset, wire_low.locator_grp_offset):
            # ROTATE THE EYE GROUP
            if self.position >= 0:
                cmds.setAttr(up + '.rotateY', eye_ctrl_direction)
                cmds.setAttr(low + '.rotateY', eye_ctrl_direction)

            else:
                cmds.setAttr(up + '.rotateY', eye_ctrl_direction * -1)
                cmds.setAttr(low + '.rotateY', eye_ctrl_direction * -1)

        # ==================================================================================================================
        #                               CONNECT EYE CONTROLLER TO EVERY JOINT LID OUT CURVE
        # ==================================================================================================================
        for up, low in zip(wire_up.all_joint, wire_low.all_joint):
            cmds.connectAttr(lid_out_on_off_follow_trans_mdn + '.output', up + '.translate')
            cmds.connectAttr(lid_out_on_off_follow_trans_mdn + '.output', low + '.translate')
            cmds.connectAttr(lid_out_on_off_follow_rot_mdn + '.output', up + '.rotate')
            cmds.connectAttr(lid_out_on_off_follow_rot_mdn + '.output', low + '.rotate')
            rt_utils.connect_attr_scale(eye_ctrl, up)
            rt_utils.connect_attr_scale(eye_ctrl, low)

    # ==================================================================================================================
    #                                                   FUNCTION
    # ==================================================================================================================
    def corner_multiply_lid_follow(self, wire, side, bind_grp_source, bind_grp_destination, sub_prefix, ctrl_corner_lid,
                                   attribute):
        translate = cmds.createNode('multiplyDivide', n=wire + 'TransCorner' + sub_prefix + side + '_mdn')
        rotate = cmds.createNode('multiplyDivide', n=wire + 'RotCorner' + sub_prefix + side + '_mdn')

        cmds.connectAttr(bind_grp_source + '.translate', translate + '.input1')
        cmds.connectAttr(ctrl_corner_lid + '.%s' % attribute, translate + '.input2X')
        cmds.connectAttr(ctrl_corner_lid + '.%s' % attribute, translate + '.input2Y')
        cmds.connectAttr(ctrl_corner_lid + '.%s' % attribute, translate + '.input2Z')

        cmds.connectAttr(translate + '.output', bind_grp_destination + '.translate')

        cmds.connectAttr(bind_grp_source + '.rotate', rotate + '.input1')
        cmds.connectAttr(ctrl_corner_lid + '.%s' % attribute, rotate + '.input2X')
        cmds.connectAttr(ctrl_corner_lid + '.%s' % attribute, rotate + '.input2Y')
        cmds.connectAttr(ctrl_corner_lid + '.%s' % attribute, rotate + '.input2Z')

        cmds.connectAttr(rotate + '.output', bind_grp_destination + '.rotate')

    def all_ctrl_connecting_lid_out(self, wire, side, ctrl_bind01, ctrl_bind02, ctrl_bind03, eyeball_ctrl, ctrl_bind04,
                                    ctrl_bind05,
                                    lid_out_follow, drv_bind01_grp_offset, drv_bind02_grp_offset, drv_bind03_grp_offset,
                                    drv_bind04_grp_offset, drv_bind05_grp_offset, close_lid_attr, upLid):
        if self.position > 0:
            self.connecting_lid_to_lid_out(wire=wire, side=side, ctrl_bind=ctrl_bind01, number_ctrl='01',
                                           lid_out_follow_attr=lid_out_follow,
                                           middle_bind_ctrl=False, drv_bind_offset=drv_bind01_grp_offset,
                                           close_lid_attr=None,
                                           upLid=upLid, reverse_tx=True)
            self.connecting_lid_to_lid_out(wire=wire, side=side, ctrl_bind=ctrl_bind02, number_ctrl='02',
                                           lid_out_follow_attr=lid_out_follow,
                                           middle_bind_ctrl=False, drv_bind_offset=drv_bind02_grp_offset,
                                           close_lid_attr=None,
                                           upLid=upLid, reverse_tx=True)
            self.connecting_lid_to_lid_out(wire=wire, side=side, ctrl_bind=ctrl_bind04, number_ctrl='04',
                                           lid_out_follow_attr=lid_out_follow,
                                           middle_bind_ctrl=False, drv_bind_offset=drv_bind04_grp_offset,
                                           close_lid_attr=None,
                                           upLid=upLid, reverse_tx=False)
            self.connecting_lid_to_lid_out(wire=wire, side=side, ctrl_bind=ctrl_bind05, number_ctrl='05',
                                           lid_out_follow_attr=lid_out_follow,
                                           middle_bind_ctrl=False, drv_bind_offset=drv_bind05_grp_offset,
                                           close_lid_attr=None,
                                           upLid=upLid, reverse_tx=False)
        else:
            self.connecting_lid_to_lid_out(wire=wire, side=side, ctrl_bind=ctrl_bind01, number_ctrl='01',
                                           lid_out_follow_attr=lid_out_follow,
                                           middle_bind_ctrl=False, drv_bind_offset=drv_bind01_grp_offset,
                                           close_lid_attr=None,
                                           upLid=upLid, reverse_tx=False)
            self.connecting_lid_to_lid_out(wire=wire, side=side, ctrl_bind=ctrl_bind02, number_ctrl='02',
                                           lid_out_follow_attr=lid_out_follow,
                                           middle_bind_ctrl=False, drv_bind_offset=drv_bind02_grp_offset,
                                           close_lid_attr=None,
                                           upLid=upLid, reverse_tx=False)
            self.connecting_lid_to_lid_out(wire=wire, side=side, ctrl_bind=ctrl_bind04, number_ctrl='04',
                                           lid_out_follow_attr=lid_out_follow,
                                           middle_bind_ctrl=False, drv_bind_offset=drv_bind04_grp_offset,
                                           close_lid_attr=None,
                                           upLid=upLid, reverse_tx=True)
            self.connecting_lid_to_lid_out(wire=wire, side=side, ctrl_bind=ctrl_bind05, number_ctrl='05',
                                           lid_out_follow_attr=lid_out_follow,
                                           middle_bind_ctrl=False, drv_bind_offset=drv_bind05_grp_offset,
                                           close_lid_attr=None,
                                           upLid=upLid, reverse_tx=True)

        self.connecting_lid_to_lid_out(wire=wire, side=side, ctrl_bind=eyeball_ctrl, number_ctrl='',
                                       lid_out_follow_attr=lid_out_follow,
                                       middle_bind_ctrl=True, drv_bind_offset=drv_bind03_grp_offset,
                                       close_lid_attr=close_lid_attr, upLid=upLid,
                                       reverse_tx=False)

    def connecting_lid_to_lid_out(self, wire, side, ctrl_bind, number_ctrl, lid_out_follow_attr, middle_bind_ctrl,
                                  drv_bind_offset, close_lid_attr, upLid, reverse_tx):

        if middle_bind_ctrl:
            if upLid:
                mdl_close_lid = self.close_lid(wire, side, ctrl_bind, number_ctrl=number_ctrl, sub_prefix='RevCloseLid',
                                               attribute=close_lid_attr, value=-0.125)

                mdl_ty = self.close_lid(wire, side, ctrl_bind, number_ctrl=number_ctrl, sub_prefix='RevTy',
                                        attribute='translateY',
                                        value=1)

            else:
                mdl_close_lid = self.close_lid(wire, side, ctrl_bind, number_ctrl=number_ctrl, sub_prefix='RevCloseLid',
                                               attribute=close_lid_attr, value=0.125)
                mdl_ty = self.close_lid(wire, side, ctrl_bind, number_ctrl=number_ctrl, sub_prefix='RevTy',
                                        attribute='translateY',
                                        value=-1)

            mdn_ty = self.multiply_divide_lid(wire_low_name=wire, side=side, object_1X=mdl_close_lid + '.output',
                                              object_2X=ctrl_bind + '.%s' % lid_out_follow_attr,
                                              object_1Y=mdl_ty + '.output',
                                              object_2Y=ctrl_bind + '.%s' % lid_out_follow_attr,
                                              sub_prefix='Ty', number_ctrl=number_ctrl, two_attr=True)

            cnd_close_lid = self.condition(wire, sub_prefix='CloseLid',
                                           obj_condition=ctrl_bind + '.%s' % close_lid_attr,
                                           obj_first=mdn_ty + '.outputX', side=side, number_ctrl=number_ctrl,
                                           operation=5)

            cnd_ty = self.condition(wire, sub_prefix='Ty', obj_condition=ctrl_bind + '.translateY',
                                    obj_first=mdn_ty + '.outputY', side=side, number_ctrl=number_ctrl, operation=3)

            pma = self.plus_minus_avg(wire, sub_prefix='CloseLidTy', side=side,
                                      object_first=cnd_close_lid + '.outColorR',
                                      object_second=cnd_ty + '.outColorR', number_ctrl=number_ctrl, )
            cmds.connectAttr(pma + '.output1D', drv_bind_offset + '.translateY')

        else:
            if upLid:
                mdl_ty = self.close_lid(wire, side, ctrl_bind, number_ctrl=number_ctrl, sub_prefix='RevTy',
                                        attribute='translateY',
                                        value=1)

            else:
                mdl_ty = self.close_lid(wire, side, ctrl_bind, number_ctrl=number_ctrl, sub_prefix='RevTy',
                                        attribute='translateY',
                                        value=-1)

            mdn_ty_direct = self.multiply_divide_lid(wire_low_name=wire, sub_prefix='DirectTy', side=side,
                                                     object_1X=mdl_ty + '.output',
                                                     object_2X=ctrl_bind + '.%s' % lid_out_follow_attr,
                                                     number_ctrl=number_ctrl, two_attr=False)

            cnd_ty_direct = self.condition(wire, sub_prefix='Ty', obj_condition=ctrl_bind + '.translateY',
                                           obj_first=mdn_ty_direct + '.outputX', side=side,
                                           number_ctrl=number_ctrl, operation=3)

            cmds.connectAttr(cnd_ty_direct + '.outColorR', drv_bind_offset + '.translateY')

        if reverse_tx:
            rev_tx = self.close_lid(wire, side, ctrl_bind, number_ctrl=number_ctrl, sub_prefix='RevTx',
                                    attribute='translateX',
                                    value=-1)

            mdn_tx = self.multiply_divide_lid(wire_low_name=wire, sub_prefix='Tx', side=side,
                                              object_1X=rev_tx + '.output',
                                              object_2X=ctrl_bind + '.%s' % lid_out_follow_attr,
                                              number_ctrl=number_ctrl, two_attr=False)
        else:
            mdn_tx = self.multiply_divide_lid(wire_low_name=wire, sub_prefix='Tx', side=side,
                                              object_1X=ctrl_bind + '.translateX',
                                              object_2X=ctrl_bind + '.%s' % lid_out_follow_attr,
                                              number_ctrl=number_ctrl, two_attr=False)

        cmds.connectAttr(mdn_tx + '.outputX', drv_bind_offset + '.translateX')

    def close_lid(self, wire, side, ctrl_bind03, sub_prefix, number_ctrl, attribute, value):
        mdl = cmds.createNode('multDoubleLinear', n=wire + sub_prefix + number_ctrl + side + '_mdl')
        cmds.setAttr(mdl + '.input2', value)
        cmds.connectAttr(ctrl_bind03 + '.%s' % attribute, mdl + '.input1')
        return mdl

    def plus_minus_avg(self, wire, sub_prefix, side, object_first, number_ctrl, object_second):
        pma = cmds.createNode('plusMinusAverage', n=wire + sub_prefix + number_ctrl + side + '_pma')
        cmds.connectAttr(object_first, pma + '.input1D[0]')
        cmds.connectAttr(object_second, pma + '.input1D[1]')
        return pma

    def condition(self, wire, sub_prefix, obj_condition, obj_first, side, number_ctrl, operation):
        cnd = cmds.createNode('condition', n=wire + sub_prefix + number_ctrl + side + '_cnd')
        cmds.connectAttr(obj_condition, cnd + '.firstTerm')
        cmds.connectAttr(obj_first, cnd + '.colorIfTrueR')
        cmds.setAttr(cnd + '.operation', operation)
        cmds.setAttr(cnd + '.colorIfFalseR', 0)
        return cnd

    def multiply_divide_lid(self, wire_low_name, side, object_1X, object_2X, number_ctrl, sub_prefix, object_1Y=None,
                            object_2Y=None, operation=1, two_attr=True):
        mdn = cmds.createNode('multiplyDivide', n=wire_low_name + sub_prefix + number_ctrl + side + '_mdn')
        cmds.connectAttr(object_1X, mdn + '.input1X')
        cmds.connectAttr(object_2X, mdn + '.input2X')
        cmds.setAttr(mdn + '.operation', operation)
        if two_attr:
            cmds.connectAttr(object_1Y, mdn + '.input1Y')
            cmds.connectAttr(object_2Y, mdn + '.input2Y')

        return mdn

    def multiply_divide(self, wire_low_name, side, scale, object_1X, object_1Y, object_1Z, operation=1, valueX=None,
                        valueY=None, valueZ=None, object_2X=None, object_2Y=None, object_2Z=None, set_attr=True):

        mdn = cmds.createNode('multiplyDivide', n=rt_utils.prefix_name(wire_low_name) + side + '_mdn')
        cmds.connectAttr(object_1X, mdn + '.input1X')
        cmds.connectAttr(object_1Y, mdn + '.input1Y')
        cmds.connectAttr(object_1Z, mdn + '.input1Z')
        cmds.setAttr(mdn + '.operation', operation)

        if set_attr:
            cmds.setAttr(mdn + '.input2X', valueX * scale)
            cmds.setAttr(mdn + '.input2Y', valueY * scale)
            cmds.setAttr(mdn + '.input2Z', valueZ * scale)
        else:
            cmds.connectAttr(object_2X, mdn + '.input2X')
            cmds.connectAttr(object_2Y, mdn + '.input2Y')
            cmds.connectAttr(object_2Z, mdn + '.input2Z')

        return mdn
