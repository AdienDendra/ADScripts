from __builtin__ import reload

import maya.cmds as mc

from rigging.library.utils import controller as ct, transform as tf, core as cr
from rigging.tools import AD_utils as au

reload(ct)
reload(au)
reload(tf)
reload(cr)

# load Plug-ins
cr.load_matrix_quad_plugin()


class Build:
    def __init__(self, curve_template, eyeball_jnt, world_up_object,
                 scale, side_LFT, side_RGT, side, offset_jnt02_position, offset_jnt04_position,
                 lid01_direction, lid02_direction, lid03_direction, lid04_direction, lid05_direction,
                 ctrl_color, lid_low_controller, upper_head_gimbal_ctrl, suffix_controller, base_module_nonTransform,
                 game_bind_joint, parent_sgame_joint
                 ):

        self.position_eyeball_jnt = mc.xform(eyeball_jnt, q=1, ws=1, t=1)[0]

        # DUPLICATE THEN RENAME
        curve_new = au.obj_duplicate_then_rename(obj_duplicate=curve_template, suffix='crv')[1]
        curve = curve_new[0]
        mc.parent(curve, base_module_nonTransform)
        self.curve = curve

        self.vertex_curve = mc.ls('%s.cv[0:*]' % curve, fl=True)

        self.create_joint_lid(curve=curve, world_up_object=world_up_object, scale=scale, eye_jnt=eyeball_jnt,
                              side_LFT=side_LFT, side_RGT=side_RGT, side=side, ctrl_color=ctrl_color,
                              upper_head_gimbal_ctrl=upper_head_gimbal_ctrl, suffix_controller=suffix_controller,
                              game_bind_joint=game_bind_joint, parent_sgame_joint=parent_sgame_joint)

        self.wire_bind_curve(side_LFT=side_LFT, side_RGT=side_RGT, curve=curve, scale=scale, side=side,
                             lid01_direction=lid01_direction, eye_jnt=eyeball_jnt, lid03_direction=lid03_direction,
                             lid02_direction=lid02_direction, lid04_direction=lid04_direction,
                             lid05_direction=lid05_direction,
                             offset_jnt02_position=offset_jnt02_position, offset_jnt04_position=offset_jnt04_position)

        self.controller_lid(side_LFT=side_LFT, side_RGT=side_RGT, scale=scale, side=side, curve=curve,
                            controller_lid_low=lid_low_controller, ctrl_color=ctrl_color,
                            suffix_controller=suffix_controller)


    def controller_lid(self, side_RGT, side_LFT, scale, side, curve, controller_lid_low, ctrl_color,
                       suffix_controller):
        curve_new_name = tf.reposition_side(object=curve, side_RGT=side_RGT, side_LFT=side_LFT)

        # controller 01
        self.lid_bind01 = ct.Control(match_obj_first_position=self.jnt01, prefix=au.prefix_name(curve_new_name) + '01',
                                     shape=ct.CIRCLEPLUS, groups_ctrl=['Zro', 'Offset', 'All'], ctrl_size=scale * 0.035,
                                     ctrl_color=ctrl_color, lock_channels=['v', 's'], side=side,
                                     suffix=suffix_controller
                                     )
        # controller 02
        self.lid_bind02 = ct.Control(match_obj_first_position=self.jnt02, prefix=au.prefix_name(curve_new_name) + '02',
                                     shape=ct.CIRCLEPLUS, groups_ctrl=['Zro', 'Offset'], ctrl_size=scale * 0.05,
                                     ctrl_color=ctrl_color, lock_channels=['v', 's'], side=side,
                                     suffix=suffix_controller
                                     )
        # controller 03
        self.lid_bind03 = ct.Control(match_obj_first_position=self.jnt03, prefix=au.prefix_name(curve_new_name) + '03',
                                     shape=ct.CIRCLEPLUS, groups_ctrl=['Zro', 'Offset', 'EyeFollow'],
                                     ctrl_size=scale * 0.07,
                                     ctrl_color='red', lock_channels=['v', 's'], side=side, suffix=suffix_controller
                                     )
        # controller 05
        self.lid_bind05 = ct.Control(match_obj_first_position=self.jnt05, prefix=au.prefix_name(curve_new_name) + '05',
                                     shape=ct.CIRCLEPLUS, groups_ctrl=['Zro', 'Offset', 'All'], ctrl_size=scale * 0.035,
                                     ctrl_color=ctrl_color, lock_channels=['v', 's'], side=side,
                                     suffix=suffix_controller
                                     )
        # controller 04
        self.lid_bind04 = ct.Control(match_obj_first_position=self.jnt04, prefix=au.prefix_name(curve_new_name) + '04',
                                     shape=ct.CIRCLEPLUS, groups_ctrl=['Zro', 'Offset'], ctrl_size=scale * 0.05,
                                     ctrl_color=ctrl_color, lock_channels=['v', 's'], side=side,
                                     suffix=suffix_controller
                                     )

        # ADD ATTRIBUTE
        au.add_attribute(objects=[self.lid_bind03.control], long_name=['lid'], nice_name=[' '], at="enum",
                         en='Eyelid', channel_box=True)

        # self.close_lid_attr = au.add_attribute(objects=[self.lid_bind03.control], long_name=['closeLid'],
        #                                        attributeType="float", min=-1, max=1, dv=0, keyable=True)

        self.lid_out03_follow_attr = au.add_attribute(objects=[self.lid_bind03.control], long_name=['lidOutFollow'],
                                                      attributeType="float", min=0, dv=1, keyable=True)

        self.show_detail_ctrl = au.add_attribute(objects=[self.lid_bind03.control], long_name=['showDetailCtrl'],
                                                 attributeType="long", min=0, max=1, dv=0, keyable=True)

        self.lid_out01_follow_attr = au.add_attribute(objects=[self.lid_bind01.control], long_name=['lidOutFollow'],
                                                      attributeType="float", min=0, dv=1, keyable=True)
        self.lid_out02_follow_attr = au.add_attribute(objects=[self.lid_bind02.control], long_name=['lidOutFollow'],
                                                      attributeType="float", min=0, dv=1, keyable=True)
        self.lid_out04_follow_attr = au.add_attribute(objects=[self.lid_bind04.control], long_name=['lidOutFollow'],
                                                      attributeType="float", min=0, dv=1, keyable=True)
        self.lid_out05_follow_attr = au.add_attribute(objects=[self.lid_bind05.control], long_name=['lidOutFollow'],
                                                      attributeType="float", min=0, dv=1, keyable=True)

        self.lid_bind05_ctrl_grp = self.lid_bind05.parent_control[0]
        self.lid_bind01_ctrl_grp = self.lid_bind01.parent_control[0]
        self.lid_bind03_ctrl = self.lid_bind03.control
        self.lid_bind03_ctrl_grp_offset = self.lid_bind03.parent_control[1]
        self.lid_bind03_ctrl_grp_eyeAim = self.lid_bind03.parent_control[2]

        # SHOW AND HIDE VISIBILITY
        for item in self.jnt_ctrl_grp_offset:
            mc.connectAttr(self.lid_bind03.control + '.%s' % self.show_detail_ctrl, item + '.visibility')

        # create grp controller and parent into it
        self.drive_ctrl_grp = mc.createNode('transform', n=au.prefix_name(curve_new_name) + 'Ctrl' + side + '_grp')
        self.ctrl_0204_grp = mc.createNode('transform', n=au.prefix_name(curve_new_name) + '0204' + side + '_grp')
        mc.parent(self.lid_bind02.parent_control[0], self.lid_bind04.parent_control[0], self.ctrl_0204_grp)
        mc.parent(self.lid_bind03.parent_control[0], self.lid_bind01.parent_control[0],
                  self.lid_bind05.parent_control[0], self.drive_ctrl_grp)

        # flipping controller
        if controller_lid_low:
            if self.position_eyeball_jnt > 0:
                # LOW LID LFT
                mc.setAttr(self.lid_bind01.parent_control[1] + '.scaleX', -1)
                mc.setAttr(self.lid_bind02.parent_control[1] + '.scaleX', -1)
                mc.setAttr(self.lid_bind04.parent_control[1] + '.scaleX', 1)
                mc.setAttr(self.lid_bind05.parent_control[1] + '.scaleX', 1)

                # connect translate controller to joint
                # right side 01 translate and rotate
                tf.bind_translate_reverse(control=self.lid_bind01.control,
                                          input_2X=-1, input_2Y=-1, input_2Z=1,
                                          joint_bind_target=self.jnt01, side_RGT=side_RGT, side_LFT=side_LFT, side=side)
                tf.bind_rotate_reverse(control=self.lid_bind01.control,
                                       input_2X=-1, input_2Y=-1, input_2Z=1,
                                       joint_bind_target=self.jnt01, side_RGT=side_RGT, side_LFT=side_LFT, side=side)

                # right side 02 translate and rotate
                tf.bind_translate_reverse(control=self.lid_bind02.control,
                                          input_2X=-1, input_2Y=-1, input_2Z=1,
                                          joint_bind_target=self.jnt02, side_RGT=side_RGT, side_LFT=side_LFT, side=side)
                tf.bind_rotate_reverse(control=self.lid_bind02.control,
                                       input_2X=-1, input_2Y=-1, input_2Z=1,
                                       joint_bind_target=self.jnt02, side_RGT=side_RGT, side_LFT=side_LFT, side=side)

                # left side 04 translate and rotate
                tf.bind_translate_reverse(control=self.lid_bind04.control,
                                          input_2X=1, input_2Y=-1, input_2Z=1,
                                          joint_bind_target=self.jnt04, side_RGT=side_RGT, side_LFT=side_LFT, side=side)
                tf.bind_rotate_reverse(control=self.lid_bind04.control,
                                       input_2X=-1, input_2Y=1, input_2Z=-1,
                                       joint_bind_target=self.jnt04, side_RGT=side_RGT, side_LFT=side_LFT, side=side)

                # left side 05 translate and rotate
                tf.bind_translate_reverse(control=self.lid_bind05.control,
                                          input_2X=1, input_2Y=-1, input_2Z=1,
                                          joint_bind_target=self.jnt05, side_RGT=side_RGT, side_LFT=side_LFT, side=side)
                tf.bind_rotate_reverse(control=self.lid_bind05.control,
                                       input_2X=-1, input_2Y=1, input_2Z=-1,
                                       joint_bind_target=self.jnt05, side_RGT=side_RGT, side_LFT=side_LFT, side=side)
            else:
                # LOW LID RGT
                mc.setAttr(self.lid_bind01.parent_control[1] + '.scaleX', 1)
                mc.setAttr(self.lid_bind02.parent_control[1] + '.scaleX', 1)
                mc.setAttr(self.lid_bind04.parent_control[1] + '.scaleX', -1)
                mc.setAttr(self.lid_bind05.parent_control[1] + '.scaleX', -1)
                # connect translate controller to joint
                # right side 01 translate and rotate
                tf.bind_translate_reverse(control=self.lid_bind01.control,
                                          input_2X=1, input_2Y=-1, input_2Z=1,
                                          joint_bind_target=self.jnt01, side_RGT=side_RGT, side_LFT=side_LFT, side=side)
                tf.bind_rotate_reverse(control=self.lid_bind01.control,
                                       input_2X=-1, input_2Y=1, input_2Z=-1,
                                       joint_bind_target=self.jnt01, side_RGT=side_RGT, side_LFT=side_LFT, side=side)

                # right side 02 translate and rotate
                tf.bind_translate_reverse(control=self.lid_bind02.control,
                                          input_2X=1, input_2Y=-1, input_2Z=1,
                                          joint_bind_target=self.jnt02, side_RGT=side_RGT, side_LFT=side_LFT, side=side)
                tf.bind_rotate_reverse(control=self.lid_bind02.control,
                                       input_2X=-1, input_2Y=1, input_2Z=-1,
                                       joint_bind_target=self.jnt02, side_RGT=side_RGT, side_LFT=side_LFT, side=side)

                # left side 04 translate and rotate
                tf.bind_translate_reverse(control=self.lid_bind04.control,
                                          input_2X=-1, input_2Y=-1, input_2Z=1,
                                          joint_bind_target=self.jnt04, side_RGT=side_RGT, side_LFT=side_LFT, side=side)
                tf.bind_rotate_reverse(control=self.lid_bind04.control,
                                       input_2X=-1, input_2Y=-1, input_2Z=1,
                                       joint_bind_target=self.jnt04, side_RGT=side_RGT, side_LFT=side_LFT, side=side)

                # left side 05 translate and rotate
                tf.bind_translate_reverse(control=self.lid_bind05.control,
                                          input_2X=-1, input_2Y=-1, input_2Z=1,
                                          joint_bind_target=self.jnt05, side_RGT=side_RGT, side_LFT=side_LFT, side=side)
                tf.bind_rotate_reverse(control=self.lid_bind05.control,
                                       input_2X=-1, input_2Y=-1, input_2Z=1,
                                       joint_bind_target=self.jnt05, side_RGT=side_RGT, side_LFT=side_LFT, side=side)

            mc.setAttr(self.lid_bind01.parent_control[1] + '.scaleY', -1)
            mc.setAttr(self.lid_bind02.parent_control[1] + '.scaleY', -1)
            mc.setAttr(self.lid_bind03.parent_control[1] + '.scaleY', -1)
            mc.setAttr(self.lid_bind05.parent_control[1] + '.scaleY', -1)
            mc.setAttr(self.lid_bind04.parent_control[1] + '.scaleY', -1)

            # mid translate and rotate
            tf.bind_translate_reverse(control=self.lid_bind03.control,
                                      input_2X=1, input_2Y=-1, input_2Z=1,
                                      joint_bind_target=self.jnt03, side_RGT=side_RGT, side_LFT=side_LFT, side=side)
            tf.bind_rotate_reverse(control=self.lid_bind03.control,
                                   input_2X=-1, input_2Y=1, input_2Z=-1,
                                   joint_bind_target=self.jnt03, side_RGT=side_RGT, side_LFT=side_LFT, side=side)

        else:
            # left side 03 translate and rotate
            au.connect_attr_translate_rotate(self.lid_bind03.control, self.jnt03)

            # UPLID LFT
            if self.position_eyeball_jnt > 0:
                mc.setAttr(self.lid_bind01.parent_control[1] + '.scaleX', -1)
                mc.setAttr(self.lid_bind02.parent_control[1] + '.scaleX', -1)
                mc.setAttr(self.lid_bind04.parent_control[1] + '.scaleX', 1)
                mc.setAttr(self.lid_bind05.parent_control[1] + '.scaleX', 1)

                # right side 01 translate and rotate
                tf.bind_translate_reverse(control=self.lid_bind01.control,
                                          input_2X=-1, input_2Y=1, input_2Z=1,
                                          joint_bind_target=self.jnt01, side_RGT=side_RGT, side_LFT=side_LFT, side=side)
                tf.bind_rotate_reverse(control=self.lid_bind01.control,
                                       input_2X=1, input_2Y=-1, input_2Z=-1,
                                       joint_bind_target=self.jnt01, side_RGT=side_RGT, side_LFT=side_LFT, side=side)

                # right side 02 translate and rotate
                tf.bind_translate_reverse(control=self.lid_bind02.control,
                                          input_2X=-1, input_2Y=1, input_2Z=1,
                                          joint_bind_target=self.jnt02, side_RGT=side_RGT, side_LFT=side_LFT, side=side)
                tf.bind_rotate_reverse(control=self.lid_bind02.control,
                                       input_2X=1, input_2Y=-1, input_2Z=-1,
                                       joint_bind_target=self.jnt02, side_RGT=side_RGT, side_LFT=side_LFT, side=side)

                # left side 04 translate and rotate
                au.connect_attr_translate_rotate(self.lid_bind04.control, self.jnt04)

                # left side 05 translate and rotate
                au.connect_attr_translate_rotate(self.lid_bind05.control, self.jnt05)

            else:
                # UPLID RGT
                mc.setAttr(self.lid_bind01.parent_control[1] + '.scaleX', 1)
                mc.setAttr(self.lid_bind02.parent_control[1] + '.scaleX', 1)
                mc.setAttr(self.lid_bind04.parent_control[1] + '.scaleX', -1)
                mc.setAttr(self.lid_bind05.parent_control[1] + '.scaleX', -1)

                # right side 01 translate and rotate
                au.connect_attr_translate_rotate(self.lid_bind01.control, self.jnt01)

                # right side 02 translate and rotate
                au.connect_attr_translate_rotate(self.lid_bind02.control, self.jnt02)

                # left side 04 translate and rotate
                tf.bind_translate_reverse(control=self.lid_bind04.control,
                                          input_2X=-1, input_2Y=1, input_2Z=1,
                                          joint_bind_target=self.jnt04, side_RGT=side_RGT, side_LFT=side_LFT, side=side)
                tf.bind_rotate_reverse(control=self.lid_bind04.control,
                                       input_2X=1, input_2Y=-1, input_2Z=-1,
                                       joint_bind_target=self.jnt04, side_RGT=side_RGT, side_LFT=side_LFT, side=side)

                # left side 05 translate and rotate
                tf.bind_translate_reverse(control=self.lid_bind05.control,
                                          input_2X=-1, input_2Y=1, input_2Z=1,
                                          joint_bind_target=self.jnt05, side_RGT=side_RGT, side_LFT=side_LFT, side=side)
                tf.bind_rotate_reverse(control=self.lid_bind05.control,
                                       input_2X=1, input_2Y=-1, input_2Z=-1,
                                       joint_bind_target=self.jnt05, side_RGT=side_RGT, side_LFT=side_LFT, side=side)

        # CONNECT GROUP PARENT BIND JOINT 01 AND 02 TO THE CONTROLLER GRP PARENT 01 AND 02
        au.connect_attr_translate_rotate(self.joint_bind02_grp[0], self.lid_bind02.parent_control[0])
        au.connect_attr_translate_rotate(self.joint_bind04_grp[0], self.lid_bind04.parent_control[0])

    def wire_bind_curve(self, side_RGT, side_LFT, curve, lid01_direction, lid02_direction, lid03_direction,
                        lid04_direction, lid05_direction,
                        offset_jnt02_position, offset_jnt04_position,
                        scale, eye_jnt, side):

        crv_new_name = tf.reposition_side(object=curve, side_RGT=side_RGT, side_LFT=side_LFT)
        joint_position_bind = len(self.all_joint)

        # query position of bind joint
        joint01 = self.all_joint[(joint_position_bind * 0)]

        joint02 = self.all_joint[(joint_position_bind / 4) + offset_jnt02_position]

        # transformGuide = None
        if not len(self.all_joint) % 2 == 0:
            joint03 = self.all_joint[int(joint_position_bind / 2)]
            self.xformJnt03 = mc.xform(joint03, ws=1, q=1, t=1)

        else:
            temp_jnt03 = self.all_joint[int(joint_position_bind / 2)]
            temps_joint03 = self.all_joint[int(joint_position_bind / 2) - 1]
            transform_guide = mc.createNode('transform', n='guide')
            joint03 = mc.delete(mc.parentConstraint(temp_jnt03, temps_joint03, transform_guide))
            self.xformJnt03 = mc.xform(joint03, ws=1, q=1, t=1)
            mc.delete(transform_guide)

        joint04 = self.all_joint[(((joint_position_bind / 2) + (joint_position_bind / 4)) - offset_jnt04_position) + 1]
        joint05 = self.all_joint[-1]

        # query the position right side
        self.xform_jnt01 = mc.xform(joint01, ws=1, q=1, t=1)
        self.xform_jnt02 = mc.xform(joint02, ws=1, q=1, t=1)
        self.xform_jnt04 = mc.xform(joint04, ws=1, q=1, t=1)
        self.xform_jnt05 = mc.xform(joint05, ws=1, q=1, t=1)

        mc.select(cl=1)
        jnt01 = mc.joint(n=au.prefix_name(crv_new_name) + '01' + side + '_driver', p=self.xform_jnt01, rad=0.5 * scale)
        jnt02 = mc.duplicate(jnt01, n=au.prefix_name(crv_new_name) + '02' + side + '_driver')[0]
        jnt03 = mc.duplicate(jnt01, n=au.prefix_name(crv_new_name) + '03' + side + '_driver')[0]
        jnt04 = mc.duplicate(jnt01, n=au.prefix_name(crv_new_name) + '04' + side + '_driver')[0]
        jnt05 = mc.duplicate(jnt01, n=au.prefix_name(crv_new_name) + '05' + side + '_driver')[0]

        # set the position RGT joint
        mc.xform(jnt02, ws=1, t=self.xform_jnt02)
        mc.xform(jnt03, ws=1, t=self.xformJnt03)
        mc.xform(jnt04, ws=1, t=self.xform_jnt04)
        mc.xform(jnt05, ws=1, t=self.xform_jnt05)

        # create bind curve
        deform_curve = mc.duplicate(curve)[0]

        deform_curve = mc.rename(deform_curve, (au.prefix_name(crv_new_name) + 'Driver' + side + '_crv'))

        # parent the bind joint
        self.joint_bind03_grp = tf.create_parent_transform(parent_list=['Zro', 'CornerLip', 'Offset', 'All'],
                                                           object=jnt03,
                                                           match_position=jnt03,
                                                           prefix=au.prefix_name(crv_new_name) + '03',
                                                           suffix='_driver', side=side)

        self.joint_bind01_grp = tf.create_parent_transform(parent_list=['Zro', 'Offset'], object=jnt01,
                                                           match_position=jnt01,
                                                           prefix=au.prefix_name(crv_new_name) + '01',
                                                           suffix='_driver', side=side)

        self.joint_bind02_grp = tf.create_parent_transform(parent_list=['Zro', 'Offset'], object=jnt02,
                                                           match_position=jnt02,
                                                           prefix=au.prefix_name(crv_new_name) + '02',
                                                           suffix='_driver', side=side)

        self.joint_bind05_grp = tf.create_parent_transform(parent_list=['Zro', 'Offset'], object=jnt05,
                                                           match_position=jnt05,
                                                           prefix=au.prefix_name(crv_new_name) + '05',
                                                           suffix='_driver', side=side)

        self.joint_bind04_grp = tf.create_parent_transform(parent_list=['Zro', 'Offset'], object=jnt04,
                                                           match_position=jnt04,
                                                           prefix=au.prefix_name(crv_new_name) + '04',
                                                           suffix='_driver', side=side)

        # assign bind grp jnt
        self.joint_bind03_grp_all = self.joint_bind03_grp[3]
        self.joint_bind03_grp_offset = self.joint_bind03_grp[2]
        self.joint_bind03_grp_corner_lip = self.joint_bind03_grp[1]

        self.joint_bind01_grp_offset = self.joint_bind01_grp[1]
        self.joint_bind05_grp_offset = self.joint_bind05_grp[1]

        if self.position_eyeball_jnt > 0:
            mc.setAttr(self.joint_bind01_grp[0] + '.rotateY', lid01_direction * -1)
            mc.setAttr(self.joint_bind02_grp[0] + '.rotateY', lid02_direction * -1)
            mc.setAttr(self.joint_bind03_grp[0] + '.rotateY', lid03_direction)
            mc.setAttr(self.joint_bind05_grp[0] + '.rotateY', lid05_direction)
            mc.setAttr(self.joint_bind04_grp[0] + '.rotateY', lid04_direction)

        else:
            mc.setAttr(self.joint_bind01_grp[0] + '.rotateY', lid01_direction)
            mc.setAttr(self.joint_bind02_grp[0] + '.rotateY', lid02_direction)
            mc.setAttr(self.joint_bind03_grp[0] + '.rotateY', lid03_direction * -1)
            mc.setAttr(self.joint_bind05_grp[0] + '.rotateY', lid05_direction * -1)
            mc.setAttr(self.joint_bind04_grp[0] + '.rotateY', lid04_direction * -1)

        # rebuild the curve
        mc.rebuildCurve(deform_curve, rpo=1, rt=0, end=1, kr=0, kcp=0,
                        kep=1, kt=0, s=8, d=3, tol=0.01)

        # skinning the joint to the bind curve
        skin_cluster = mc.skinCluster([jnt05, jnt04, jnt01, jnt02, jnt03], deform_curve,
                                      n='%s%s%s%s' % (au.prefix_name(crv_new_name), 'Wire', side, '_sc'),
                                      tsb=True, bm=0, sm=0, nw=1, mi=3)

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

        mc.skinPercent(skin_cluster[0], skin_percent_index0, tv=[(jnt01, 1.0)])
        mc.skinPercent(skin_cluster[0], skin_percent_index1, tv=[(jnt01, 0.9), (jnt02, 0.1)])
        mc.skinPercent(skin_cluster[0], skin_percent_index2, tv=[(jnt01, 0.7), (jnt02, 0.3)])
        mc.skinPercent(skin_cluster[0], skin_percent_index3, tv=[(jnt02, 0.5), (jnt01, 0.25), (jnt03, 0.25)])
        mc.skinPercent(skin_cluster[0], skin_percent_index4, tv=[(jnt02, 0.3), (jnt03, 0.7)])
        mc.skinPercent(skin_cluster[0], skin_percent_index5, tv=[(jnt03, 1.0)])
        mc.skinPercent(skin_cluster[0], skin_percent_index6, tv=[(jnt04, 0.3), (jnt03, 0.7)])
        mc.skinPercent(skin_cluster[0], skin_percent_index7, tv=[(jnt04, 0.5), (jnt05, 0.25), (jnt03, 0.25)])
        mc.skinPercent(skin_cluster[0], skin_percent_index8, tv=[(jnt05, 0.7), (jnt04, 0.3)])
        mc.skinPercent(skin_cluster[0], skin_percent_index9, tv=[(jnt05, 0.9), (jnt04, 0.1)])
        mc.skinPercent(skin_cluster[0], skin_percent_index10, tv=[(jnt05, 1.0)])

        # wire the curve
        wire_deformer = mc.wire(curve, dds=(0, 100 * scale), wire=deform_curve)
        wire_deformer[0] = mc.rename(wire_deformer[0], (au.prefix_name(crv_new_name) + side + '_wireNode'))
        mc.setAttr(wire_deformer[0] + '.scale[0]', 0)

        # constraint mid to 02 left and right
        jnt03_constraint = mc.parentConstraint(jnt03, jnt05, self.joint_bind04_grp[0], mo=1)
        jnt01_constraint = mc.parentConstraint(jnt03, jnt01, self.joint_bind02_grp[0], mo=1)

        # constraint rename
        au.constraint_rename([jnt03_constraint[0], jnt01_constraint[0]])

        self.jnt03 = jnt03
        self.jnt01 = jnt01
        self.jnt02 = jnt02
        self.jnt05 = jnt05
        self.jnt04 = jnt04

        # create grp curves
        self.curves_group = mc.createNode('transform', n=au.prefix_name(crv_new_name) + 'Crv' + side + '_grp')
        mc.setAttr(self.curves_group + '.it', 0, l=1)
        mc.parent(deform_curve, mc.listConnections(wire_deformer[0] + '.baseWire[0]')[0], self.curves_group)
        mc.hide(self.curves_group)

        # eye grp connect
        self.eye_bind01_grp_offset = self.eye_bind_grp(curve=crv_new_name, bind_grp_zro=self.joint_bind01_grp[0],
                                                       number='01', side=side, eye_jnt=eye_jnt)

        self.eye_bind03_grp_offset = self.eye_bind_grp(curve=crv_new_name, bind_grp_zro=self.joint_bind03_grp[0],
                                                       number='03', side=side, eye_jnt=eye_jnt)

        self.eye_bind05_grp_offset = self.eye_bind_grp(curve=crv_new_name, bind_grp_zro=self.joint_bind05_grp[0],
                                                       number='05', side=side, eye_jnt=eye_jnt)

        # create grp bind
        self.bind_jnt_grp = mc.createNode('transform', n=au.prefix_name(crv_new_name) + 'JntDriver' + side + '_grp')
        mc.parent(self.eye_bind03_grp_offset[0], self.eye_bind01_grp_offset[0], self.joint_bind02_grp[0],
                  self.eye_bind05_grp_offset[0], self.joint_bind04_grp[0], self.bind_jnt_grp)
        mc.hide(self.bind_jnt_grp)

        self.deform_curve = deform_curve

    def eye_bind_grp(self, curve, number, side, bind_grp_zro, eye_jnt):
        # bind grp for eye
        eye_grp_zro = mc.group(em=1, n=au.prefix_name(curve) + 'EyeZro' + number + side + '_grp')
        eye_grp_offset = mc.group(em=1, n=au.prefix_name(curve) + 'EyeOffset' + number + side + '_grp', p=eye_grp_zro)
        mc.delete(mc.parentConstraint(eye_jnt, eye_grp_zro))

        mc.parent(bind_grp_zro, eye_grp_offset)

        return eye_grp_zro, eye_grp_offset

    def create_joint_lid(self, curve, world_up_object, eye_jnt, scale, side_RGT, side_LFT, side, ctrl_color,
                         upper_head_gimbal_ctrl,
                         suffix_controller,
                         game_bind_joint,
                         parent_sgame_joint
                         ):
        self.all_joint_center = []
        self.all_joint = []
        self.all_locator = []
        self.jnt_ctrl_grp_offset = []
        self.ctrl_joint_grp = []

        curve_new_name = tf.reposition_side(object=curve, side_RGT=side_RGT, side_LFT=side_LFT)

        for index, object in enumerate(self.vertex_curve):
            # create joint
            mc.select(cl=1)
            self.joint = mc.joint(
                n='%s%s%02d%s%s' % (au.prefix_name(curve_new_name), 'Dtl', (index + 1), side, '_skn'),
                rad=0.1 * scale)

            if game_bind_joint:
                joint_bind = mc.joint(n='%s%s%02d%s%s' % (au.prefix_name(curve_new_name), 'Dtl', (index + 1), side, '_bind'),
                rad=0.1 * scale)
                constraining = au.parent_scale_constraint(self.joint, joint_bind)
                mc.parent(joint_bind, parent_sgame_joint)
                mc.parent(constraining[0], constraining[1], 'additional_grp')
                mc.setAttr(joint_bind + '.segmentScaleCompensate', 0)

            mc.setAttr(self.joint + '.visibility', 0)

            position = mc.xform(object, q=1, ws=1, t=1)
            mc.xform(self.joint, ws=1, t=position)
            joint_group = tf.create_parent_transform(parent_list=[''], object=self.joint,
                                                     match_position=self.joint,
                                                     prefix=tf.reposition_side(object=au.prefix_name(self.joint),
                                                                               side_RGT=side_RGT, side_LFT=side_LFT),
                                                     suffix='_jnt', side=side)

            mc.select(cl=1)
            self.joint_center = mc.joint(
                n='%s%s%02d%s%s' % (au.prefix_name(curve_new_name), 'Ctr', (index + 1), side, '_jnt'), rad=0.1 * scale)
            mc.setAttr(self.joint_center + '.drawStyle', 2)

            position_eye_translation = mc.xform(eye_jnt, q=1, ws=1, t=1)
            pos_eye_rotation = mc.xform(eye_jnt, q=1, ws=1, ro=1)

            mc.xform(self.joint_center, ws=1, t=position_eye_translation, ro=pos_eye_rotation)

            self.all_joint_center.append(self.joint_center)

            # create locator
            self.locator = mc.spaceLocator(n='%s%02d%s%s' % (au.prefix_name(curve_new_name), (index + 1), side, '_loc'))[0]
            mc.xform(self.locator, ws=1, t=position)

            # aim constraint of joint
            jnt_aim_constraint = mc.aimConstraint(self.locator, self.joint_center, mo=1, weight=1, aimVector=(0, 0, 1),
                                                  upVector=(0, 1, 0),
                                                  worldUpType="object", worldUpObject=world_up_object)
            # rename constraint
            au.constraint_rename(jnt_aim_constraint)

            self.all_locator.append(self.locator)
            mc.parent(joint_group[0], self.joint_center)

            # REPOSITION CONTROLLER ROTATION
            mc.delete(mc.aimConstraint(self.joint_center, joint_group[0], weight=1, aimVector=(0, 0, -1), upVector=(0, 1, 0),
                                 worldUpType="object", worldUpObject=world_up_object))

            # connect curve to locator grp
            curve_list_relatives = mc.listRelatives(curve, s=True)[0]
            getU_parameter = cr.get_uParam(position, curve_list_relatives)
            point_curve_info = mc.createNode("pointOnCurveInfo", n='%s%02d%s%s' % (
                au.prefix_name(curve_new_name), (index + 1), side, '_pci'))
            mc.connectAttr(curve_list_relatives + '.worldSpace', point_curve_info + '.inputCurve')
            mc.setAttr(point_curve_info + '.parameter', getU_parameter)
            mc.connectAttr(point_curve_info + '.position', self.locator + '.t')

            # CREATE JOINT CONTROLLER
            joint_controller = ct.Control(match_obj_first_position=eye_jnt, prefix=tf.reposition_side(
                object=au.prefix_name(self.joint),
                side_RGT=side_RGT, side_LFT=side_LFT),
                                          shape=ct.JOINT, groups_ctrl=['', 'Offset'], ctrl_size=scale * 0.01,
                                          ctrl_color=ctrl_color, lock_channels=['s', 'v'], side=side,
                                          suffix=suffix_controller
                                          )
            self.all_joint.append(self.joint)
            self.jnt_ctrl_grp_offset.append(joint_controller.parent_control[1])
            self.ctrl_joint_grp.append(joint_controller.parent_control[0])

            mc.xform(joint_controller.parent_control[0], ws=1, t=position_eye_translation)

            # REMATCH POSITION
            mc.delete(mc.parentConstraint(self.joint, joint_controller.parent_control[1]))

            # CONNECT THE CONTROLLER TO JOINT
            au.connect_attr_rotate(self.joint_center, joint_controller.parent_control[0])
            au.connect_attr_translate_rotate(joint_controller.control, self.joint)

        # grouping joint
        self.all_joint_ctrl = mc.group(em=1, n=au.prefix_name(curve_new_name) + 'DtlCtrl' + side + '_grp')
        mc.delete(mc.parentConstraint(upper_head_gimbal_ctrl, self.all_joint_ctrl))
        mc.parent(self.ctrl_joint_grp, self.all_joint_ctrl)

        self.joint_grp = mc.group(em=1, n=au.prefix_name(curve_new_name) + 'JntCtrl' + side + '_grp')
        mc.parent(self.all_joint_center, world_up_object, self.joint_grp)

        self.move_grp = mc.group(em=1, n=au.prefix_name(curve_new_name) + 'MoveZro' + side + '_grp')
        mc.delete(mc.parentConstraint(eye_jnt, self.move_grp))
        self.move_grp_offset = \
            mc.duplicate(self.move_grp, n=au.prefix_name(curve_new_name) + 'MoveOffset' + side + '_grp')[0]

        mc.parent(self.move_grp_offset, self.move_grp)
        mc.parent(self.joint_grp, self.move_grp_offset)

        # grouping locator
        self.locator_grp = mc.group(em=1, n=au.prefix_name(curve_new_name) + 'Loc' + side + '_grp')
        mc.setAttr(self.locator_grp + '.it', 0, l=1)
        mc.parent(self.all_locator, self.locator_grp)
        mc.hide(self.locator_grp)