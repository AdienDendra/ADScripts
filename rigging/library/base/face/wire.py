from __builtin__ import reload

import maya.cmds as mc

from rigging.library.utils import controller as ct, transform as tf, core as cr
from rigging.tools import AD_utils as au

reload (ct)
reload (tf)
reload (au)
reload (cr)

class Build:
    def __init__(self, curve_template, scale, side_LFT, side_RGT, side, offset_jnt02_bind_position, offset_jnt04_bind_position,
                 ctrl01_direction, ctrl02_direction, ctrl03_direction, ctrl04_direction, ctrl05_direction,
                 ctrl_color, wire_low_controller, shape, position_joint_direction, face_utils_grp, suffix_controller,
                 base_module_nonTransform, game_bind_joint, parent_sgame_joint,
                 connect_with_corner_ctrl=False):

        # DUPLICATE CURVE THEN RENAME
        curve_new = au.obj_duplicate_then_rename(obj_duplicate=curve_template, suffix='crv')[1]
        curve = curve_new[0]
        mc.parent(curve, base_module_nonTransform)

        self.prefix_name_crv = tf.reposition_side(au.prefix_name(curve), side_LFT=side_LFT, side_RGT=side_RGT)

        self.position_jnt_direction = mc.xform(position_joint_direction, q=1, ws=1, t=1)[0]

        self.curve_vertex = mc.ls('%s.cv[0:*]' % curve, fl=True)

        self.create_joint_wire(curve=curve, scale=scale, side=side, game_bind_joint=game_bind_joint, parent_sgame_joint=parent_sgame_joint)

        self.wire_bind_curve(offset_jnt02_bind_position=offset_jnt02_bind_position, ctrl01_direction=ctrl01_direction,
                             ctrl02_direction=ctrl02_direction, offset_jnt04_bind_position=offset_jnt04_bind_position,
                             ctrl03_direction=ctrl03_direction, ctrl04_direction=ctrl04_direction,
                             ctrl05_direction=ctrl05_direction, curve=curve, scale=scale, side=side)

        self.controller_wire(scale=scale, side=side, controller_wire_low=wire_low_controller, shape=shape, ctrl_color=ctrl_color,
                             connect_with_corner_ctrl=connect_with_corner_ctrl, side_RGT=side_RGT, side_LFT=side_LFT,
                             suffix_controller=suffix_controller)

        self.grouping_wire(side=side, face_utils_grp=face_utils_grp, position_direction_jnt=position_joint_direction)

        self.curve = curve

    def grouping_wire(self, side, face_utils_grp, position_direction_jnt):
        setup_driver_grp = mc.group(em=1, n=self.prefix_name_crv + 'Setup' + side + '_grp')
        ctrl_driver_grp = mc.group(em=1, n=self.prefix_name_crv + 'Controller' + side + '_grp')

        mc.hide(setup_driver_grp)
        all_grp = mc.group(em=1, n=self.prefix_name_crv + side + '_grp')

        wire_driven_jnt_grp = mc.group(em=1, n=self.prefix_name_crv + 'DrivenJnt' + side + '_grp')
        mc.delete(mc.parentConstraint(position_direction_jnt, wire_driven_jnt_grp))
        wire_driven_jnt_grp_offset = mc.duplicate(wire_driven_jnt_grp, n=self.prefix_name_crv + 'DrivenOffsetJnt' + side + '_grp')[0]
        wire_driven_ctrl_grp = mc.duplicate(wire_driven_jnt_grp, n=self.prefix_name_crv + 'DrivenCtrl' + side + '_grp')[0]
        wire_driven_ctrl_grp_offset = mc.duplicate(wire_driven_ctrl_grp, n=self.prefix_name_crv + 'DrivenOffsetCtrl' + side + '_grp')[0]

        # parenting to joint grp
        mc.parent(wire_driven_jnt_grp_offset, wire_driven_jnt_grp)
        mc.parent(wire_driven_ctrl_grp_offset, wire_driven_ctrl_grp)

        mc.parent(wire_driven_jnt_grp, setup_driver_grp, all_grp)
        mc.parent(wire_driven_ctrl_grp, ctrl_driver_grp)

        mc.parent(all_grp, face_utils_grp)

        self.wire_driven_jnt_grp_offset = wire_driven_jnt_grp_offset
        self.wire_driven_ctrl_grp = wire_driven_ctrl_grp
        self.wire_driven_ctrl_grp_offset = wire_driven_ctrl_grp_offset
        self.setup_driver_grp =setup_driver_grp
        self.ctrl_driver_grp = ctrl_driver_grp

        mc.parent(self.drive_ctrl_grp, wire_driven_ctrl_grp_offset)
        mc.parent(self.joint_grp, setup_driver_grp)
        mc.parent(self.bind_jnt_grp, wire_driven_jnt_grp_offset)

        mc.parent(self.curves_grp, self.locator_grp, self.setup_driver_grp)


    def controller_wire(self, scale, ctrl_color, shape, controller_wire_low, suffix_controller,
                        side_RGT, side_LFT, side='', connect_with_corner_ctrl=False):

        # controller mid
        controller_bind03 = ct.Control(match_obj_first_position=self.jnt03, prefix=self.prefix_name_crv + 'Drv03',
                                       shape=shape, groups_ctrl=['Zro', 'Offset'], ctrl_size=scale * 0.075,
                                       ctrl_color=ctrl_color, lock_channels=['v', 's'], side=side, suffix=suffix_controller
                                       )

        # controller rgt 01
        controller_bind05 = ct.Control(match_obj_first_position=self.jnt05, prefix=self.prefix_name_crv + 'Drv05',
                                       shape=shape, groups_ctrl=['Zro', 'Offset', 'All'], ctrl_size=scale * 0.035,
                                       ctrl_color=ctrl_color, lock_channels=['v', 's'], side=side, suffix=suffix_controller
                                       )

        # controller rgt 02
        controller_bind04 = ct.Control(match_obj_first_position=self.jnt04, prefix=self.prefix_name_crv + 'Drv04',
                                      shape=shape, groups_ctrl=['Zro', 'Offset'], ctrl_size=scale * 0.05,
                                      ctrl_color=ctrl_color, lock_channels=['v', 's'], side=side, suffix=suffix_controller
                                      )
        # controller lft 01
        controller_bind01 = ct.Control(match_obj_first_position=self.jnt01, prefix=self.prefix_name_crv + 'Drv01',
                                       shape=shape, groups_ctrl=['Zro', 'Offset', 'All'], ctrl_size=scale * 0.035,
                                       ctrl_color=ctrl_color, lock_channels=['v', 's'], side=side, suffix=suffix_controller
                                       )
        # controller lft 02
        controller_bind02 = ct.Control(match_obj_first_position=self.jnt02, prefix=self.prefix_name_crv + 'Drv02',
                                      shape=shape, groups_ctrl=['Zro', 'Offset'], ctrl_size=scale * 0.05,
                                      ctrl_color=ctrl_color, lock_channels=['v', 's'], side=side, suffix=suffix_controller
                                      )

        # create grp controller and parent into it
        drive_ctrl_grp = mc.createNode('transform', n=self.prefix_name_crv + 'Ctrl' + side + '_grp')
        mc.parent(controller_bind03.parent_control[0], controller_bind05.parent_control[0],
                  controller_bind04.parent_control[0],
                  controller_bind01.parent_control[0], controller_bind02.parent_control[0], drive_ctrl_grp)

        # connect group parent bind joint 01 and 02 to the controller grp parent 01 and 02
        au.connect_attr_translate_rotate(self.joint_bind04_grp, controller_bind04.parent_control[0])
        au.connect_attr_translate_rotate(self.joint_bind02_grp, controller_bind02.parent_control[0])

        # connect bind parent zro to ctrl zro parent
        if not connect_with_corner_ctrl:
            au.connect_attr_translate(self.joint_bind05_grp, controller_bind05.parent_control[0])
            au.connect_attr_translate(self.joint_bind01_grp, controller_bind01.parent_control[0])

       # flipping controller
        if controller_wire_low:
            if self.position_jnt_direction >= 0:
                # LOW LID LFT
                mc.setAttr(controller_bind01.parent_control[1] + '.scaleX', -1)
                mc.setAttr(controller_bind02.parent_control[1] + '.scaleX', -1)
                mc.setAttr(controller_bind04.parent_control[1] + '.scaleX', 1)
                mc.setAttr(controller_bind05.parent_control[1] + '.scaleX', 1)

                # connect translate controller to joint
                # right side 01 translate and rotate
                tf.bind_translate_reverse(control=controller_bind01.control,
                                          input_2X=-1, input_2Y=-1, input_2Z=1,
                                          joint_bind_target=self.jnt01, side_RGT=side_RGT, side_LFT=side_LFT, side=side)
                tf.bind_rotate_reverse(control=controller_bind01.control,
                                       input_2X=-1, input_2Y=-1, input_2Z=1,
                                       joint_bind_target=self.jnt01, side_RGT=side_RGT, side_LFT=side_LFT, side=side)

                # right side 02 translate and rotate
                tf.bind_translate_reverse(control=controller_bind02.control,
                                          input_2X=-1, input_2Y=-1, input_2Z=1,
                                          joint_bind_target=self.jnt02, side_RGT=side_RGT, side_LFT=side_LFT, side=side)
                tf.bind_rotate_reverse(control=controller_bind02.control,
                                       input_2X=-1, input_2Y=-1, input_2Z=1,
                                       joint_bind_target=self.jnt02, side_RGT=side_RGT, side_LFT=side_LFT, side=side)

                # left side 04 translate and rotate
                tf.bind_translate_reverse(control=controller_bind04.control,
                                          input_2X=1, input_2Y=-1, input_2Z=1,
                                          joint_bind_target=self.jnt04, side_RGT=side_RGT, side_LFT=side_LFT, side=side)
                tf.bind_rotate_reverse(control=controller_bind04.control,
                                       input_2X=-1, input_2Y=1, input_2Z=-1,
                                       joint_bind_target=self.jnt04, side_RGT=side_RGT, side_LFT=side_LFT, side=side)

                # left side 05 translate and rotate
                tf.bind_translate_reverse(control=controller_bind05.control,
                                          input_2X=1, input_2Y=-1, input_2Z=1,
                                          joint_bind_target=self.jnt05, side_RGT=side_RGT, side_LFT=side_LFT, side=side)
                tf.bind_rotate_reverse(control=controller_bind05.control,
                                       input_2X=-1, input_2Y=1, input_2Z=-1,
                                       joint_bind_target=self.jnt05, side_RGT=side_RGT, side_LFT=side_LFT, side=side)
            else:
                # LOW LID RGT
                mc.setAttr(controller_bind01.parent_control[1] + '.scaleX', 1)
                mc.setAttr(controller_bind02.parent_control[1] + '.scaleX', 1)
                mc.setAttr(controller_bind04.parent_control[1] + '.scaleX', -1)
                mc.setAttr(controller_bind05.parent_control[1] + '.scaleX', -1)
                # connect translate controller to joint
                # right side 01 translate and rotate
                tf.bind_translate_reverse(control=controller_bind01.control,
                                          input_2X=1, input_2Y=-1, input_2Z=1,
                                          joint_bind_target=self.jnt01, side_RGT=side_RGT, side_LFT=side_LFT, side=side)
                tf.bind_rotate_reverse(control=controller_bind01.control,
                                       input_2X=-1, input_2Y=1, input_2Z=-1,
                                       joint_bind_target=self.jnt01, side_RGT=side_RGT, side_LFT=side_LFT, side=side)

                # right side 02 translate and rotate
                tf.bind_translate_reverse(control=controller_bind02.control,
                                          input_2X=1, input_2Y=-1, input_2Z=1,
                                          joint_bind_target=self.jnt02, side_RGT=side_RGT, side_LFT=side_LFT, side=side)
                tf.bind_rotate_reverse(control=controller_bind02.control,
                                       input_2X=-1, input_2Y=1, input_2Z=-1,
                                       joint_bind_target=self.jnt02, side_RGT=side_RGT, side_LFT=side_LFT, side=side)

                # left side 04 translate and rotate
                tf.bind_translate_reverse(control=controller_bind04.control,
                                          input_2X=-1, input_2Y=-1, input_2Z=1,
                                          joint_bind_target=self.jnt04, side_RGT=side_RGT, side_LFT=side_LFT, side=side)
                tf.bind_rotate_reverse(control=controller_bind04.control,
                                       input_2X=-1, input_2Y=-1, input_2Z=1,
                                       joint_bind_target=self.jnt04, side_RGT=side_RGT, side_LFT=side_LFT, side=side)


                # left side 05 translate and rotate
                tf.bind_translate_reverse(control=controller_bind05.control,
                                          input_2X=-1, input_2Y=-1, input_2Z=1,
                                          joint_bind_target=self.jnt05, side_RGT=side_RGT, side_LFT=side_LFT, side=side)
                tf.bind_rotate_reverse(control=controller_bind05.control,
                                       input_2X=-1, input_2Y=-1, input_2Z=1,
                                       joint_bind_target=self.jnt05, side_RGT=side_RGT, side_LFT=side_LFT, side=side)

            mc.setAttr(controller_bind01.parent_control[1] + '.scaleY', -1)
            mc.setAttr(controller_bind02.parent_control[1] + '.scaleY', -1)
            mc.setAttr(controller_bind03.parent_control[1] + '.scaleY', -1)
            mc.setAttr(controller_bind05.parent_control[1] + '.scaleY', -1)
            mc.setAttr(controller_bind04.parent_control[1] + '.scaleY', -1)

            # mid translate and rotate
            tf.bind_translate_reverse(control=controller_bind03.control,
                                      input_2X=1, input_2Y=-1, input_2Z=1,
                                      joint_bind_target=self.jnt03, side_RGT=side_RGT, side_LFT=side_LFT, side=side)
            tf.bind_rotate_reverse(control=controller_bind03.control,
                                   input_2X=-1, input_2Y=1, input_2Z=-1,
                                   joint_bind_target=self.jnt03, side_RGT=side_RGT, side_LFT=side_LFT, side=side)

        else:
            # left side 03 translate and rotate
            au.connect_attr_translate_rotate(controller_bind03.control, self.jnt03)

            # UPLID LFT
            if self.position_jnt_direction >= 0:
                mc.setAttr(controller_bind01.parent_control[1] + '.scaleX', -1)
                mc.setAttr(controller_bind02.parent_control[1] + '.scaleX', -1)
                mc.setAttr(controller_bind04.parent_control[1] + '.scaleX', 1)
                mc.setAttr(controller_bind05.parent_control[1] + '.scaleX', 1)

                # right side 01 translate and rotate
                tf.bind_translate_reverse(control=controller_bind01.control,
                                          input_2X=-1, input_2Y=1, input_2Z=1,
                                          joint_bind_target=self.jnt01, side_RGT=side_RGT, side_LFT=side_LFT, side=side)
                tf.bind_rotate_reverse(control=controller_bind01.control,
                                       input_2X=1, input_2Y=-1, input_2Z=-1,
                                       joint_bind_target=self.jnt01, side_RGT=side_RGT, side_LFT=side_LFT, side=side)

                # right side 02 translate and rotate
                tf.bind_translate_reverse(control=controller_bind02.control,
                                          input_2X=-1, input_2Y=1, input_2Z=1,
                                          joint_bind_target=self.jnt02, side_RGT=side_RGT, side_LFT=side_LFT, side=side)
                tf.bind_rotate_reverse(control=controller_bind02.control,
                                       input_2X=1, input_2Y=-1, input_2Z=-1,
                                       joint_bind_target=self.jnt02, side_RGT=side_RGT, side_LFT=side_LFT, side=side)


                # left side 04 translate and rotate
                au.connect_attr_translate_rotate(controller_bind04.control, self.jnt04)

                # left side 05 translate and rotate
                au.connect_attr_translate_rotate(controller_bind05.control, self.jnt05)

            else:
                # UPLID RGT
                mc.setAttr(controller_bind01.parent_control[1] + '.scaleX', 1)
                mc.setAttr(controller_bind02.parent_control[1] + '.scaleX', 1)
                mc.setAttr(controller_bind04.parent_control[1] + '.scaleX', -1)
                mc.setAttr(controller_bind05.parent_control[1] + '.scaleX', -1)

                # right side 01 translate and rotate
                au.connect_attr_translate_rotate(controller_bind01.control, self.jnt01)

                # right side 02 translate and rotate
                au.connect_attr_translate_rotate(controller_bind02.control, self.jnt02)

                # left side 04 translate and rotate
                tf.bind_translate_reverse(control=controller_bind04.control,
                                          input_2X=-1, input_2Y=1, input_2Z=1,
                                          joint_bind_target=self.jnt04, side_RGT=side_RGT, side_LFT=side_LFT, side=side)
                tf.bind_rotate_reverse(control=controller_bind04.control,
                                       input_2X=1, input_2Y=-1, input_2Z=-1,
                                       joint_bind_target=self.jnt04, side_RGT=side_RGT, side_LFT=side_LFT, side=side)

                # left side 05 translate and rotate
                tf.bind_translate_reverse(control=controller_bind05.control,
                                          input_2X=-1, input_2Y=1, input_2Z=1,
                                          joint_bind_target=self.jnt05, side_RGT=side_RGT, side_LFT=side_LFT, side=side)
                tf.bind_rotate_reverse(control=controller_bind05.control,
                                       input_2X=1, input_2Y=-1, input_2Z=-1,
                                       joint_bind_target=self.jnt05, side_RGT=side_RGT, side_LFT=side_LFT, side=side)

        self.drive_ctrl_grp=drive_ctrl_grp
        self.controller_bind01 = controller_bind01.control
        self.controller_bind01_grp = controller_bind01.parent_control[0]

        self.controller_bind05 = controller_bind05.control
        self.controller_bind05_grp = controller_bind05.parent_control[0]

        self.controller_bind03 = controller_bind03.control
        self.controller_bind03_grp = controller_bind03.parent_control[0]

        # CONNECT OFFSET BIND TO CTRL BIND
        au.connect_attr_translate(self.joint_bind01_grp_offset, controller_bind01.parent_control[1])
        au.connect_attr_translate(self.joint_bind02_grp_offset, controller_bind02.parent_control[1])
        au.connect_attr_translate(self.joint_bind03_grp_offset, controller_bind03.parent_control[1])
        au.connect_attr_translate(self.joint_bind04_grp_offset, controller_bind04.parent_control[1])
        au.connect_attr_translate(self.joint_bind05_grp_offset, controller_bind05.parent_control[1])


    def wire_bind_curve(self, curve, offset_jnt02_bind_position, offset_jnt04_bind_position, ctrl01_direction, ctrl02_direction,
                        ctrl03_direction, ctrl04_direction, ctrl05_direction, scale, side=''):
        length_joint_position = len(self.all_joint)

        # query position of bind joint
        joint01 =  self.all_joint[(length_joint_position * 0)]

        joint02 =  self.all_joint[(length_joint_position / 4) + offset_jnt02_bind_position]

        if not len(self.all_joint) % 2 == 0:
            joint03 = self.all_joint[int(length_joint_position / 2)]
            self.xform_jnt03 = mc.xform(joint03, ws=1, q=1, t=1)

        else:
            temp_jnt03 = self.all_joint[int(length_joint_position / 2)]
            temps_joint03 = self.all_joint[int(length_joint_position / 2) - 1]
            transform = mc.createNode('transform', n='guide')
            joint03 = mc.delete(mc.parentConstraint(temp_jnt03, temps_joint03, transform))
            self.xform_jnt03 = mc.xform(joint03, ws=1, q=1, t=1)
            mc.delete(transform)

        joint04 =  self.all_joint[(((length_joint_position / 2) + (length_joint_position / 4)) - offset_jnt04_bind_position) + 1]
        joint05 =  self.all_joint[-1]

        # query the position right side
        self.xform_jnt01 = mc.xform(joint01, ws=1, q=1, t=1)
        self.xform_jnt02 = mc.xform(joint02, ws=1, q=1, t=1)
        self.xform_jnt04 = mc.xform(joint04, ws=1, q=1, t=1)
        self.xform_jnt05 = mc.xform(joint05, ws=1, q=1, t=1)
        # mc.delete(transform)

        mc.select(cl=1)
        self.jnt01  = mc.joint(n=au.prefix_name(self.prefix_name_crv) + '01' + side + '_driver', p=self.xform_jnt01, rad=0.5 * scale)
        self.jnt02  = mc.duplicate(self.jnt01, n=au.prefix_name(self.prefix_name_crv) + '02' + side + '_driver')[0]
        self.jnt03  = mc.duplicate(self.jnt01, n=au.prefix_name(self.prefix_name_crv) + '03' + side + '_driver')[0]
        self.jnt04  = mc.duplicate(self.jnt01, n=au.prefix_name(self.prefix_name_crv) + '04' + side + '_driver')[0]
        self.jnt05  = mc.duplicate(self.jnt01, n=au.prefix_name(self.prefix_name_crv) + '05' + side + '_driver')[0]

        # set the position RGT joint
        mc.xform(self.jnt02, ws=1, t=self.xform_jnt02)
        mc.xform(self.jnt03, ws=1, t=self.xform_jnt03)
        mc.xform(self.jnt04, ws=1, t=self.xform_jnt04)
        mc.xform(self.jnt05, ws=1, t=self.xform_jnt05)

        # create bind curve
        deform_curve = mc.duplicate(curve)[0]

        deform_curve = mc.rename(deform_curve, (au.prefix_name(self.prefix_name_crv) + 'Driver' + side + '_crv'))


        # parent the bind joint
        joint_bind03_grp = tf.create_parent_transform(parent_list=['Zro', 'Offset'], object=self.jnt03,
                                                      match_position=self.jnt03, prefix=self.prefix_name_crv + 'Drv03',
                                                      suffix='_driver', side=side)

        joint_bind05_grp = tf.create_parent_transform(parent_list=['Zro', 'Offset', 'All', 'Corner'], object=self.jnt05,
                                                      match_position=self.jnt05, prefix=self.prefix_name_crv + 'Drv05',
                                                      suffix='_driver', side=side)

        joint_bind04_grp = tf.create_parent_transform(parent_list=['Zro', 'Offset'], object=self.jnt04,
                                                      match_position=self.jnt04, prefix=self.prefix_name_crv + 'Drv04',
                                                      suffix='_driver', side=side)

        joint_bind01_grp = tf.create_parent_transform(parent_list=['Zro', 'Offset', 'All', 'Corner'], object=self.jnt01,
                                                      match_position=self.jnt01, prefix=self.prefix_name_crv + 'Drv01',
                                                      suffix='_driver', side=side)

        joint_bind02_grp = tf.create_parent_transform(parent_list=['Zro', 'Offset'], object=self.jnt02,
                                                      match_position=self.jnt02, prefix=self.prefix_name_crv + 'Drv02',
                                                      suffix='_driver', side=side)

        if self.position_jnt_direction > 0:
            mc.setAttr(joint_bind01_grp[0] + '.rotateY', ctrl01_direction * -1)
            mc.setAttr(joint_bind02_grp[0] + '.rotateY', ctrl02_direction * -1)
            mc.setAttr(joint_bind03_grp[0] + '.rotateY', ctrl03_direction)
            mc.setAttr(joint_bind05_grp[0] + '.rotateY', ctrl05_direction)
            mc.setAttr(joint_bind04_grp[0] + '.rotateY', ctrl04_direction)

        else:
            mc.setAttr(joint_bind01_grp[0] + '.rotateY', ctrl01_direction)
            mc.setAttr(joint_bind02_grp[0] + '.rotateY', ctrl02_direction)
            mc.setAttr(joint_bind03_grp[0] + '.rotateY', ctrl03_direction * -1)
            mc.setAttr(joint_bind05_grp[0] + '.rotateY', ctrl05_direction * -1)
            mc.setAttr(joint_bind04_grp[0] + '.rotateY', ctrl04_direction * -1)

        # rebuild the curve
        mc.rebuildCurve(deform_curve, rpo=1, rt=0, end=1, kr=0, kcp=0,
                        kep=1, kt=0, s=8, d=3, tol=0.01)

        # skinning the joint to the bind curve
        skin_cluster = mc.skinCluster([self.jnt05, self.jnt04, self.jnt01, self.jnt02, self.jnt03], deform_curve,
                                      n='%s%s%s%s' % (au.prefix_name(self.prefix_name_crv), 'Wire', side, 'SkinCluster'), tsb=True,
                                      bm=0, sm=0, nw=1, mi=3)

        # Distribute the skin
        skin_percent_index0 = '%s.cv[0]' % deform_curve
        skin_percent_index1 = '%s.cv[1]' % deform_curve
        skin_percent_index2 = '%s.cv[2]' % deform_curve
        skin_percent_index3 = '%s.cv[3]' % deform_curve
        skin_percent_index4 = '%s.cv[4]' % deform_curve
        skin_percent_index5 = '%s.cv[5]' % deform_curve
        skin_percent_index6 = '%s.cv[6]' % deform_curve
        skin_percent_index7 = '%s.cv[7]' % deform_curve
        skin_percent_index8 = '%s.cv[8]' % deform_curve
        skin_percent_index9 = '%s.cv[9]' % deform_curve
        skin_percent_index10 = '%s.cv[10]' % deform_curve

        mc.skinPercent(skin_cluster[0], skin_percent_index0, tv=[(self.jnt01, 1.0)])
        mc.skinPercent(skin_cluster[0], skin_percent_index1, tv=[(self.jnt01, 0.9), (self.jnt02, 0.1)])
        mc.skinPercent(skin_cluster[0], skin_percent_index2, tv=[(self.jnt01, 0.7), (self.jnt02, 0.3)])
        mc.skinPercent(skin_cluster[0], skin_percent_index3, tv=[(self.jnt02, 0.5), (self.jnt01, 0.25), (self.jnt03, 0.25)])
        mc.skinPercent(skin_cluster[0], skin_percent_index4, tv=[(self.jnt02, 0.3), (self.jnt03, 0.7)])
        mc.skinPercent(skin_cluster[0], skin_percent_index5, tv=[(self.jnt03, 1.0)])
        mc.skinPercent(skin_cluster[0], skin_percent_index6, tv=[(self.jnt04, 0.3), (self.jnt03, 0.7)])
        mc.skinPercent(skin_cluster[0], skin_percent_index7, tv=[(self.jnt04, 0.5), (self.jnt05, 0.25), (self.jnt03, 0.25)])
        mc.skinPercent(skin_cluster[0], skin_percent_index8, tv=[(self.jnt05, 0.7), (self.jnt04, 0.3)])
        mc.skinPercent(skin_cluster[0], skin_percent_index9, tv=[(self.jnt05, 0.9), (self.jnt04, 0.1)])
        mc.skinPercent(skin_cluster[0], skin_percent_index10, tv=[(self.jnt05, 1.0)])

        # wire the curve
        wire_deformer = mc.wire(curve, dds=(0, 100 * scale), wire=deform_curve)
        wire_deformer[0] = mc.rename(wire_deformer[0], (au.prefix_name(self.prefix_name_crv) + side + '_wireNode'))
        mc.setAttr(wire_deformer[0] + '.scale[0]', 0)

        # constraint mid to 02 left and right
        jnt02_bind_constraint_grp = mc.parentConstraint(self.jnt03, self.jnt01, joint_bind02_grp[0], mo=1)
        jnt04_bind_constraint_grp = mc.parentConstraint(self.jnt03, self.jnt05, joint_bind04_grp[0], mo=1)

        # rename constraint
        au.constraint_rename([jnt02_bind_constraint_grp[0], jnt04_bind_constraint_grp[0]])

        # create grp curves
        curves_grp = mc.createNode('transform', n=self.prefix_name_crv + 'Crv' + side + '_grp')
        mc.setAttr(curves_grp + '.it', 0, l=1)
        mc.parent(deform_curve, mc.listConnections(wire_deformer[0] + '.baseWire[0]')[0], curves_grp)
        mc.hide(curves_grp)

        # create grp bind
        bind_jnt_grp = mc.createNode('transform', n=self.prefix_name_crv + 'JntDriver' + side + '_grp')
        mc.parent(joint_bind03_grp[0], joint_bind05_grp[0], joint_bind04_grp[0],
                  joint_bind01_grp[0], joint_bind02_grp[0], bind_jnt_grp)
        mc.hide(bind_jnt_grp)

        self.joint_bind04_grp = joint_bind04_grp[0]
        self.joint_bind02_grp = joint_bind02_grp[0]
        self.joint_bind05_grp_all = joint_bind05_grp[2]
        self.joint_bind01_grp_all = joint_bind01_grp[2]
        self.joint_bind05_grp = joint_bind05_grp[0]
        self.joint_bind01_grp = joint_bind01_grp[0]
        self.joint_bind03_grp = joint_bind03_grp[0]

        self.joint_bind04_grp_offset = joint_bind04_grp[1]
        self.joint_bind02_grp_offset = joint_bind02_grp[1]
        self.joint_bind05_grp_offset = joint_bind05_grp[1]
        self.joint_bind01_grp_offset = joint_bind01_grp[1]
        self.joint_bind03_grp_offset = joint_bind03_grp[1]

        self.joint_bind01_grp_corner = joint_bind01_grp[3]
        self.joint_bind05_grp_corner = joint_bind05_grp[3]


        self.curves_grp = curves_grp
        self.bind_jnt_grp =bind_jnt_grp

    def create_joint_wire(self, curve, side, scale, game_bind_joint, parent_sgame_joint):

        curve_vetex = mc.ls('%s.cv[0:*]' % curve, fl=True)

        self.all_joint = []
        self.locator_grp_offset = []
        self.locator_grp_zro = []
        self.all_skin = []
        self.joint_grp_zro = []

        for index, object in enumerate(curve_vetex):
            # create joint
            mc.select(cl=1)
            joint = mc.joint(n='%s%02d%s%s' % (self.prefix_name_crv, (index + 1), side, '_skn'), rad=0.1 * scale)
            if game_bind_joint:
                joint_bind = mc.joint(n='%s%02d%s%s' % (self.prefix_name_crv, (index + 1), side, '_bind'), rad=0.1 * scale)
                constraining = au.parent_scale_constraint(joint, joint_bind)
                mc.parent(joint_bind, parent_sgame_joint)
                mc.parent(constraining[0], constraining[1], 'additional_grp')
                mc.setAttr(joint_bind+'.segmentScaleCompensate', 0)

            postion_object = mc.xform(object, q=1, ws=1, t=1)
            mc.xform(joint, ws=1, t=postion_object)
            self.all_joint.append(joint)

            joint_grp = tf.create_parent_transform(parent_list=[''], object=joint,
                                                   match_position=joint,
                                                   prefix=self.prefix_name_crv + str(index + 1).zfill(2),
                                                   suffix='_jnt', side=side)

            self.joint_grp_zro.append(joint_grp[0])
            # create locator
            # locator = mc.spaceLocator(n='%s%02d%s%s' % (self.prefixNameCrv, (i + 1), side, '_loc'))[0]
            group_offset = mc.spaceLocator(n='%s%s%02d%s%s' % (self.prefix_name_crv, 'Offset', (index + 1), side, '_loc'))[0]
            mc.hide(group_offset)

            mc.xform(group_offset, ws=1, t=postion_object)
            locator_grp = tf.create_parent_transform(parent_list=[''], object=group_offset,
                                                     match_position=group_offset, prefix=self.prefix_name_crv + str(index + 1).zfill(2),
                                                     suffix='_zro', side=side)
            self.locator_grp_offset.append(group_offset)
            self.locator_grp_zro.append(locator_grp[0])
            # self.allLocator.append(groupOffset)

            # connect curve to locator grp
            curve_list_relatives = mc.listRelatives(curve, s=True)[0]
            uParam = cr.get_uParam(postion_object, curve_list_relatives)
            pci_node = mc.createNode("pointOnCurveInfo", n='%s%02d%s%s' % (self.prefix_name_crv, (index + 1), side, '_pci'))
            mc.connectAttr(curve_list_relatives + '.worldSpace', pci_node + '.inputCurve')
            mc.setAttr(pci_node + '.parameter', uParam)
            mc.connectAttr(pci_node + '.position', locator_grp[0] + '.t')

            decompose_node = mc.createNode('decomposeMatrix', n='%s%02d%s%s' % (self.prefix_name_crv, (index + 1), side, '_dmtx'))
            mc.connectAttr(group_offset + '.worldMatrix[0]', decompose_node + '.inputMatrix')

            mc.connectAttr(decompose_node + '.outputTranslate', joint_grp[0] + '.translate')
            mc.connectAttr(decompose_node + '.outputRotate', joint_grp[0] + '.rotate')

        # grouping joint
        self.joint_grp = mc.group(em=1, n=self.prefix_name_crv + 'Jnt' + side + '_grp')
        mc.parent(self.joint_grp_zro, self.joint_grp)

        # grouping locator
        self.locator_grp = mc.group(em=1, n=self.prefix_name_crv + 'Loc' + side + '_grp')
        mc.setAttr(self.locator_grp + '.it', 0, l=1)
        mc.parent(self.locator_grp_zro, self.locator_grp)