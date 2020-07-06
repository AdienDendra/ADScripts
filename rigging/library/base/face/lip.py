from __builtin__ import reload

import maya.cmds as mc

from rigging.library.utils import controller as ct, transform as tf, core as cr
from rigging.tools import AD_utils as au

reload (ct)
reload (tf)
reload (au)
reload (cr)

# load Plug-ins

cr.load_matrix_quad_plugin()

class Build:
    def __init__(self, curve_lip_template,
                 curve_lip_roll_template,
                 offset_jnt02_bind_position,
                 scale,
                 lip01_cheek_direction,
                 lip02_cheek_direction,
                 side_LFT,
                 side_RGT,
                 mouth_jnt,
                 ctrl_color,
                 low_lip_controller,
                 suffix_controller,
                 base_module_nonTransform,
                 # parent_skin
                 ):

        # DUPLICATE CURVE THEN RENAME
        curve_lip_new = au.obj_duplicate_then_rename(obj_duplicate=curve_lip_template, suffix='crv')[1]
        curve_lip = curve_lip_new[0]

        curve_lip_roll_new = au.obj_duplicate_then_rename(obj_duplicate=curve_lip_roll_template, suffix='crv')[1]
        curve_lip_roll = curve_lip_roll_new[0]

        mc.parent(curve_lip, curve_lip_roll, base_module_nonTransform)

        self.prefix_name_curve = au.prefix_name(curve_lip)
        self.curve_vertex = mc.ls('%s.cv[0:*]' % curve_lip, fl=True)

        self.create_joint_lip(curve=curve_lip, scale=scale, ctrl_color=ctrl_color, suffix_controller=suffix_controller,
                              # parent_skin=parent_skin
                              )

        self.create_reset_mouth_position_grp(mouth_base_jnt=mouth_jnt)


        self.wire_bind_curve(lip_curve=curve_lip, offset_jnt02_bind_position=offset_jnt02_bind_position, scale=scale,
                             side_LFT=side_LFT, side_RGT=side_RGT, lip01_direction=lip01_cheek_direction,
                             lip02_direction=lip02_cheek_direction)

        self.set_driver_locator(side_LFT=side_LFT, side_RGT=side_RGT)

        self.sticky_lip(lip_curve=curve_lip, scale=scale)

        self.roll_locator(roll_curve=curve_lip_roll, scale=scale, curve=curve_lip)

        self.all_controller_lip(scale=scale, controller_lip_low=low_lip_controller, suffix_controller=suffix_controller)

        self.controller_lip(scale=scale, side_LFT=side_LFT, side_RGT=side_RGT,
                            controller_lip_low=low_lip_controller, ctrl_color=ctrl_color, suffix_controller=suffix_controller)


        # ==============================================================================================================
        #                                             CREATE GRP AND PARENT GRP
        # ==============================================================================================================

        self.ctrl_grp = mc.group(em=1, n=self.prefix_name_curve + 'Controller_grp')
        self.sticky_grp = mc.group(em=1, n=self.prefix_name_curve + 'Sticky_grp')

        # UTILITIES GRP
        self.utils_grp = mc.createNode('transform', n=self.prefix_name_curve + 'Utils_grp')
        mc.parent(self.curves_grp, self.grp_drv_locator, self.locator_grp, self.bind_jnt_grp,
                  self.reset_all_mouth_ctrl_grp, self.utils_grp)

        # CTRL GRP
        mc.parent(self.mouth_ctrl_grp, self.grp_drive_ctrl, self.ctrl_grp)

        mc.parent(self.sticky_curve_grp, self.sticky_cluster_hdl_grp, self.origin_locator_grp, self.mid_locator_grp, self.sticky_grp)

        self.curve_lip = curve_lip
        self.curve_lip_roll = curve_lip_roll


    def controller_lip(self, scale, side_LFT, side_RGT, controller_lip_low, ctrl_color, suffix_controller):

        # CONTROLLER MID
        self.controller_bind_mid = ct.Control(match_obj_first_position=self.jnt_mid, prefix=self.prefix_name_curve + 'Drv',
                                              shape=ct.SQUAREPLUS, groups_ctrl=['Zro', 'Offset'], ctrl_size=scale * 0.1,
                                              ctrl_color=ctrl_color, lock_channels=['v', 's'], suffix=suffix_controller
                                              )
        # CONTROLLER RGT 01
        self.controller_bind01_RGT = ct.Control(match_obj_first_position=self.jnt01_RGT, prefix=self.prefix_name_curve + 'Drv01',
                                                shape=ct.SQUAREPLUS, groups_ctrl=['Zro', 'Offset', 'All'], ctrl_size=scale * 0.05,
                                                ctrl_color=ctrl_color, lock_channels=['v', 'r', 's'], side=side_RGT, suffix=suffix_controller
                                                )

        # CONTROLLER RGT 02
        self.controller_bind02_RGT = ct.Control(match_obj_first_position=self.jnt02_RGT, prefix=self.prefix_name_curve + 'Drv02',
                                                shape=ct.SQUAREPLUS, groups_ctrl=['Zro', 'Offset'], ctrl_size=scale * 0.07,
                                                ctrl_color=ctrl_color, lock_channels=['v', 's'], side=side_RGT, suffix=suffix_controller
                                                )
        # CONTROLLER LFT 01
        self.controller_bind01_LFT = ct.Control(match_obj_first_position=self.jnt01_LFT, prefix=self.prefix_name_curve + 'Drv01',
                                                shape=ct.SQUAREPLUS, groups_ctrl=['Zro', 'Offset', 'All'], ctrl_size=scale * 0.05,
                                                ctrl_color=ctrl_color, lock_channels=['v', 'r', 's'], side=side_LFT, suffix=suffix_controller
                                                )
        # CONTROLLER LFT 02
        self.controller_bind02_LFT = ct.Control(match_obj_first_position=self.jnt02_LFT, prefix=self.prefix_name_curve + 'Drv02',
                                                shape=ct.SQUAREPLUS, groups_ctrl=['Zro', 'Offset'], ctrl_size=scale * 0.07,
                                                ctrl_color=ctrl_color, lock_channels=['v', 's'], side=side_LFT, suffix=suffix_controller
                                                )

        # CREATE GRP CONTROLLER AND PARENT INTO IT
        self.grp_drive_ctrl = mc.createNode('transform', n=self.prefix_name_curve + 'Ctrl' + '_grp')
        mc.parent(self.controller_bind_mid.parent_control[0], self.controller_bind01_RGT.parent_control[0], self.controller_bind02_RGT.parent_control[0],
                  self.controller_bind01_LFT.parent_control[0], self.controller_bind02_LFT.parent_control[0], self.joint_grp, self.grp_drive_ctrl)

        # CONNECT GROUP PARENT BIND JOINT 01 AND 02 TO THE CONTROLLER GRP PARENT 01 AND 02
        au.connect_attr_translate_rotate(self.joint_bind02_RGT_grp[0], self.controller_bind02_RGT.parent_control[0])
        au.connect_attr_translate_rotate(self.joint_bind02_LFT_grp[0], self.controller_bind02_LFT.parent_control[0])

        # FLIPPING CONTROLLER
        if controller_lip_low:
            mc.setAttr(self.controller_bind01_RGT.parent_control[0] + '.scaleX', -1)
            mc.setAttr(self.controller_bind02_RGT.parent_control[0] + '.scaleX', -1)

            mc.setAttr(self.controller_bind01_RGT.parent_control[0] + '.scaleY', -1)
            mc.setAttr(self.controller_bind02_RGT.parent_control[0] + '.scaleY', -1)

            mc.setAttr(self.controller_bind01_LFT.parent_control[0] + '.scaleY', -1)
            mc.setAttr(self.controller_bind02_LFT.parent_control[0] + '.scaleY', -1)

            mc.setAttr(self.controller_bind_mid.parent_control[0] + '.scaleY', -1)


            # CONNECT TRANSLATE CONTROLLER TO JOINT
            # RIGHT SIDE 02 TRANSLATE AND ROTATE
            tf.bind_translate_reverse(control=self.controller_bind02_RGT.control,
                                      input_2X=-1, input_2Y=-1, input_2Z=1,
                                      joint_bind_target=self.jnt02_RGT, side_RGT=side_RGT, side_LFT=side_LFT, side='RGT')

            au.connect_attr_rotate(self.controller_bind02_RGT.control, self.jnt02_RGT)

            # RIGHT SIDE 01 TRANSLATE AND ROTATE
            tf.bind_translate_reverse(control=self.controller_bind01_RGT.control,
                                      input_2X=-1, input_2Y=-1, input_2Z=1,
                                      joint_bind_target=self.jnt01_RGT, side_RGT=side_RGT, side_LFT=side_LFT, side='RGT')

            au.connect_attr_rotate(self.controller_bind01_RGT.control, self.jnt01_RGT)

            # LEFT SIDE 02 TRANSLATE AND ROTATE
            tf.bind_translate_reverse(control=self.controller_bind02_LFT.control,
                                      input_2X=1, input_2Y=-1, input_2Z=1,
                                      joint_bind_target=self.jnt02_LFT, side_RGT=side_RGT, side_LFT=side_LFT, side='LFT')

            au.connect_attr_rotate(self.controller_bind02_LFT.control, self.jnt02_LFT)

            # LEFT SIDE 01 TRANSLATE AND ROTATE
            tf.bind_translate_reverse(control=self.controller_bind01_LFT.control,
                                      input_2X=1, input_2Y=-1, input_2Z=1,
                                      joint_bind_target=self.jnt01_LFT, side_RGT=side_RGT, side_LFT=side_LFT, side='LFT')

            au.connect_attr_rotate(self.controller_bind01_LFT.control, self.jnt01_LFT)

            # MID TRANSLATE AND ROTATE
            tf.bind_translate_reverse(control=self.controller_bind_mid.control,
                                      input_2X=1, input_2Y=-1, input_2Z=1,
                                      joint_bind_target=self.jnt_mid, side_RGT=side_RGT, side_LFT=side_LFT, side='')

            tf.bind_rotate_reverse(control=self.controller_bind_mid.control,
                                   input_2X=-1, input_2Y=1, input_2Z=-1,
                                   joint_bind_target=self.jnt_mid, side_RGT=side_RGT, side_LFT=side_LFT, side='')

        else:
            mc.setAttr(self.controller_bind01_RGT.parent_control[0] + '.scaleX', -1)
            mc.setAttr(self.controller_bind02_RGT.parent_control[0] + '.scaleX', -1)

            # RIGHT SIDE 02 TRANSLATE AND ROTATE
            tf.bind_translate_reverse(control=self.controller_bind02_RGT.control,
                                      input_2X=-1, input_2Y=1, input_2Z=1,
                                      joint_bind_target=self.jnt02_RGT, side_RGT=side_RGT, side_LFT=side_LFT, side='RGT')

            mc.connectAttr(self.controller_bind02_RGT.control + '.rotate', self.jnt02_RGT + '.rotate')

            # RIGHT SIDE 01 TRANSLATE AND ROTATE
            tf.bind_translate_reverse(control=self.controller_bind01_RGT.control,
                                      input_2X=-1, input_2Y=1, input_2Z=1,
                                      joint_bind_target=self.jnt01_RGT, side_RGT=side_RGT, side_LFT=side_LFT, side='RGT')

            mc.connectAttr(self.controller_bind01_RGT.control + '.rotate', self.jnt01_RGT + '.rotate')

            # LEFT SIDE 02 TRANSLATE AND ROTATE
            au.connect_attr_translate_rotate(self.controller_bind02_LFT.control, self.jnt02_LFT)

            # LEFT SIDE 01 TRANSLATE AND ROTATE
            au.connect_attr_translate_rotate(self.controller_bind01_LFT.control, self.jnt01_LFT)

            # MID TRANSLATE AND ROTATE
            au.connect_attr_translate_rotate(self.controller_bind_mid.control, self.jnt_mid)

        # SCALING THE CTRL
        list_second_grp = [self.controller_bind_mid.parent_control[1], self.controller_bind01_RGT.parent_control[1],
                           self.controller_bind02_RGT.parent_control[1], self.controller_bind01_LFT.parent_control[1],
                           self.controller_bind02_LFT.parent_control[1]]
        for item in list_second_grp:
            au.connect_attr_scale(self.mouth_ctrl_grp, item)


    def all_controller_lip(self, scale, controller_lip_low, suffix_controller):

        # controller
        controller_all= ct.Control(match_obj_first_position=self.jnt_mid, prefix=self.prefix_name_curve + 'DrvAll',
                                   shape=ct.CIRCLE, groups_ctrl=[''], ctrl_size=scale * 0.15,
                                   ctrl_color='blue', lock_channels=['v', 's'], suffix=suffix_controller)

        self.controller_all_grp_zro = controller_all.parent_control[0]
        self.controller_all = controller_all.control

        show_detail_ctrl = au.add_attribute(objects=[controller_all.control], long_name=['showDetailCtrl'],
                                            attributeType="long", min=0, max=1, dv=0, keyable=True)

        for item in self.control_group_offset:
            mc.connectAttr(self.controller_all + '.%s' % show_detail_ctrl, item + '.visibility')


        if controller_lip_low:
            mc.setAttr(self.controller_all_grp_zro + '.scaleY', -1)

        # PARENT TO RESPECTIVE OBJECT
        mc.parent(self.controller_all_grp_zro, self.mouth_ctrl_grp_offset)

    def roll_locator(self, roll_curve, curve, scale):
        joint = self.all_joint
        length_joint = len(joint)
        right_position_length = joint[0:((length_joint - 1) / 2)]
        left_position_length = joint[((length_joint + 1) / 2):]
        left_position_length = left_position_length[::-1]
        mid_joint_position = joint[(length_joint - 1) / 2]

        divide = (1.000 / ((length_joint / 2.000) - 1.000))

        self.lip_roll_mdl = mc.createNode('multDoubleLinear', n=self.prefix_name_curve + 'Roll' + '_mdl')
        # REBUILD THE CURVE
        vertex_list = mc.ls('%s.cv[1:]' % curve, fl=True)
        vertex_list = len(vertex_list)

        rebuild_curve = mc.rebuildCurve(roll_curve, rpo=1, rt=0, end=1, kr=0, kcp=0,
                                        kep=0, kt=0, s=vertex_list, d=1, tol=0.01)
        new_name = mc.rename(rebuild_curve, self.prefix_name_curve + 'Roll_crv')

        vertex = mc.ls('%s.cv[0:*]' % new_name, fl=True)
        all_locator_roll = []
        mult_double=[]
        condition=[]
        for index, object in enumerate(vertex):
            position = mc.xform(object, q=1, ws=1, t=1)
            # CREATE LOCATOR
            locator_roll = mc.spaceLocator(n='%s%s%02d%s' % (self.prefix_name_curve, 'Roll', (index + 1), '_loc'))[0]
            # GRPLOCATORROLL =
            locator_list_relatives = mc.listRelatives(locator_roll, s=True)[0]

            mc.setAttr(locator_list_relatives + '.localScaleX', 0.1 * scale)
            mc.setAttr(locator_list_relatives + '.localScaleY', 0.1 * scale)
            mc.setAttr(locator_list_relatives + '.localScaleZ', 0.1 * scale)

            mc.xform(locator_roll, ws=1, t=position)

            # CONNECT MDL NODE ROLL TO OBJECT LOCATOR
            # mc.connectAttr(self.mdlLipRoll + '.output', locatorRoll + '.rotateX')
            all_locator_roll.append(locator_roll)

        for index, object_RGT, in enumerate(right_position_length):
            prefix_name, number_name = tf.reorder_number(prefix=object_RGT, side_RGT='', side_LFT='')
            mdl = mc.createNode('multDoubleLinear', n=au.prefix_name(prefix_name) + 'MulRoll' + number_name + '_mdl')
            self.cnd_RGT = mc.createNode('condition', n=au.prefix_name(prefix_name) + 'Roll' + number_name + '_cnd')
            mc.setAttr(self.cnd_RGT + '.operation', 3)
            mc.setAttr(self.cnd_RGT + '.colorIfTrueR', (divide * index))
            mc.setAttr(self.cnd_RGT + '.colorIfFalseR', 1)

            # mc.setAttr(mdl + '.input2', (div * n))
            mc.connectAttr(self.lip_roll_mdl + '.output', mdl + '.input1')
            mc.connectAttr(self.cnd_RGT + '.outColorR', mdl + '.input2')
            mult_double.append(mdl)
            condition.append(self.cnd_RGT)

            # mc.connectAttr(mdl + '.output', locatorRoll + '.rotateX')

        for index, object_LFT, in enumerate(left_position_length):
            prefix_name, number_name = tf.reorder_number(prefix=object_LFT, side_RGT='', side_LFT='')
            mdl = mc.createNode('multDoubleLinear', n=au.prefix_name(prefix_name) + 'MulRoll' + number_name + '_mdl')
            self.cnd_LFT = mc.createNode('condition', n=au.prefix_name(prefix_name) + 'Roll' + number_name + '_cnd')
            mc.setAttr(self.cnd_LFT + '.operation', 3)
            mc.setAttr(self.cnd_LFT + '.colorIfTrueR', (divide * index))
            mc.setAttr(self.cnd_LFT + '.colorIfFalseR', 1)

            # mc.setAttr(mdl + '.input2', (div * n))
            mc.connectAttr(self.lip_roll_mdl + '.output', mdl + '.input1')
            mc.connectAttr(self.cnd_LFT + '.outColorR', mdl + '.input2')

            mult_double.append(mdl)
            condition.append(self.cnd_LFT)

        # MID MUL ROLL
        prefix_name, number_name = tf.reorder_number(prefix=mid_joint_position, side_RGT='', side_LFT='')
        middle_mdl = mc.createNode('multDoubleLinear', n=au.prefix_name(prefix_name) + 'MulRoll' + number_name + '_mdl')
        mc.setAttr(middle_mdl + '.input2', 1)
        mc.connectAttr(self.lip_roll_mdl + '.output', middle_mdl + '.input1')
        mult_double.append(middle_mdl)

        for mdl, roll_loc, loc, joint in zip(sorted(mult_double), all_locator_roll, self.locator_group_offset, self.control_group_offset):
            mc.parent(roll_loc, loc)
            mc.connectAttr(mdl + '.output', roll_loc + '.rotateX')
            mc.connectAttr(roll_loc + '.rotateX', joint + '.rotateX')

        self.allLocatorRoll = all_locator_roll
        self.condition=sorted(condition)

        mc.delete(self.all_locator)

    def sticky_lip(self, lip_curve, scale):
        # DUPLICATE THE CURVES
        self.sticky_mid_crv = mc.duplicate(lip_curve, n=self.prefix_name_curve + 'StickyMid' + '_crv')[0]
        self.bind_sticky_mid_crv = mc.duplicate(self.deform_curve, n=self.prefix_name_curve + 'BindStickyMid' + '_crv')[0]
        self.sticky_origin_crv = mc.duplicate(lip_curve, n=self.prefix_name_curve + 'StickyOrigin' + '_crv')[0]
        self.sticky_move_crv = mc.duplicate(lip_curve, n=self.prefix_name_curve + 'StickyMove' + '_crv')[0]

        mc.select(cl=1)
        # WIRE DEFORM ON MID CURVES
        sticky_mid_wire_deformer = mc.wire(self.sticky_mid_crv, dds=(0, 100 * scale), wire=self.bind_sticky_mid_crv)
        sticky_mid_wire_deformer[0] = mc.rename(sticky_mid_wire_deformer[0], (self.prefix_name_curve + 'StickyMid' + '_wireNode'))
        mc.setAttr(sticky_mid_wire_deformer[0] + '.scale[0]', 0)

        # WIRE BIND CURVES TO ORIGIN CURVE
        sticky_origin_wire_deformer = mc.wire(self.sticky_origin_crv, dds=(0, 100 * scale), wire=self.deform_curve)
        sticky_origin_wire_deformer[0] = mc.rename(sticky_origin_wire_deformer[0], (self.prefix_name_curve + 'StickyOrigin' + '_wireNode'))
        mc.setAttr(sticky_origin_wire_deformer[0] + '.scale[0]', 0)

        # BLENDSHAPE STICKY MOVE TO CRV
        mc.blendShape(self.sticky_move_crv, lip_curve, n=(self.prefix_name_curve + 'StickyMove' + '_bsn'), weight=[(0, 1)])

        # LOCATOR ORIGIN
        origin_locator = self.duplicate_locator_and_add_pci_node(name_locator='Origin', curve=self.sticky_origin_crv)
        self.origin_locator_grp = origin_locator[1]
        # LOCATOR MID
        mid_locator = self.duplicate_locator_and_add_pci_node(name_locator='Mid', curve=self.sticky_mid_crv)
        self.mid_locator_grp = mid_locator[1]

        # SET CLUSTER FOR STICKY MOVE
        sticky_move_curve_vertex = mc.ls('%s.cv[0:*]' % self.sticky_move_crv, fl=True)
        self.clsHandle=[]
        for index, object in enumerate(sticky_move_curve_vertex):
            cluster = mc.cluster(object, n='%s%s%02d%s' % (self.prefix_name_curve, 'StickyMove', index + 1, '_cls'))
            replace_name = cluster[1].replace('Handle', 'Hdl')
            self.clsHandle.append(mc.rename(cluster[1], replace_name))

        # CONSTRAINING STICKY
        self.cluster_constraint=[]
        for ori_loc, mid_loc, cls_hdl in zip(origin_locator[0], mid_locator[0], self.clsHandle):
            constraint = mc.parentConstraint(ori_loc, mid_loc, cls_hdl)
            # RENAME CONSTRAINT
            constraint = au.constraint_rename(constraint)[0]
            self.cluster_constraint.append(constraint)

        # GROUPING THE CURVES
        self.sticky_curve_grp = mc.createNode('transform', n=self.prefix_name_curve + 'StickyCurves' + '_grp')
        mc.setAttr (self.sticky_curve_grp + '.it', 0, l=1)
        mc.parent(self.sticky_mid_crv, self.bind_sticky_mid_crv, self.sticky_origin_crv, self.sticky_move_crv,
                  mc.listConnections(sticky_mid_wire_deformer[0] + '.baseWire[0]')[0],
                  mc.listConnections(sticky_origin_wire_deformer[0] + '.baseWire[0]')[0], self.sticky_curve_grp)
        mc.hide(self.sticky_curve_grp)

        # GROUPING CLUSTER HANDLE
        self.sticky_cluster_hdl_grp = mc.createNode('transform', n=self.prefix_name_curve + 'StickyClusterHdl' + '_grp')
        mc.parent(self.clsHandle, self.sticky_cluster_hdl_grp)
        mc.hide(self.sticky_cluster_hdl_grp)

    def duplicate_locator_and_add_pci_node(self, name_locator, curve):
        # DUPLICATE LOCATOR FOR CURVE
        sticky_locator = mc.duplicate(self.all_locator)
        new_sticky_locator = []
        for index, object in enumerate(sticky_locator):
            rename= mc.rename(object, '%s%s%s%02d%s' % (self.prefix_name_curve, 'Sticky', name_locator, index + 1, '_loc'))

            # CREATE POINT ON CURVE NODE
            position = mc.xform(rename, q=1, ws=1, t=1)
            rename_suffix_locator = rename.replace('loc', 'pci')
            # CONNECT CURVE TO LOCATOR GRP
            curve_list_relatives = mc.listRelatives(curve, s=True)[0]
            uParam = cr.get_uParam(position, curve_list_relatives)
            pci_node = mc.createNode("pointOnCurveInfo", n=rename_suffix_locator)
            mc.connectAttr(curve_list_relatives + '.worldSpace', pci_node + '.inputCurve')
            mc.setAttr(pci_node + '.parameter', uParam)
            mc.connectAttr(pci_node + '.position', rename + '.t')
            new_sticky_locator.append(rename)

        # GROUPING THE STICKY LOC
        sticky_locator_grp = mc.createNode('transform', n=self.prefix_name_curve + 'Sticky' + name_locator + 'Loc' + '_grp')
        mc.parent(new_sticky_locator, sticky_locator_grp)
        mc.hide(sticky_locator_grp)

        return new_sticky_locator, sticky_locator_grp

    def set_driver_locator(self, side_LFT, side_RGT):
        # CREATE LOCATOR
        self.locator_set01_RGT = mc.spaceLocator(n=self.prefix_name_curve + 'Drv01' + side_RGT + '_set')[0]
        self.locator_set01_LFT = mc.spaceLocator(n=self.prefix_name_curve + 'Drv01' + side_LFT + '_set')[0]

        self.locator_set_mid = mc.spaceLocator(n=self.prefix_name_curve + 'Drv01' + '_set')[0]

        # MATCH POSITION
        mc.delete(mc.parentConstraint(self.jnt01_RGT, self.locator_set01_RGT))
        mc.delete(mc.parentConstraint(self.jnt01_LFT, self.locator_set01_LFT))
        mc.delete(mc.parentConstraint(self.jnt_mid, self.locator_set_mid))

        # CONNECT MOUTH RESET UTILS GRP TO SET DRIVER LOCATOR
        list_set_locator = [self.locator_set01_RGT, self.locator_set01_LFT, self.locator_set_mid]
        for item in list_set_locator:
            au.connect_attr_scale(self.reset_all_mouth_ctrl_grp, item)

        # CREATE GRP CONTROLLER AND PARENT INTO IT
        self.grp_drv_locator = mc.createNode('transform', n=self.prefix_name_curve + 'DrvSet' + '_grp')
        mc.parent(self.locator_set01_RGT, self.locator_set01_LFT, self.locator_set_mid, self.grp_drv_locator)
        mc.hide(self.grp_drv_locator)

    def wire_bind_curve(self, lip_curve, offset_jnt02_bind_position, lip01_direction, lip02_direction,
                        scale, side_LFT, side_RGT):

        joint_position_bind = len(self.all_joint)

        # QUERY POSITION OF BIND JOINT
        joint01_RGT =  self.all_joint[(joint_position_bind * 0)]

        joint02_RGT =  self.all_joint[((joint_position_bind / 4) + offset_jnt02_bind_position)]

        joint_mid =  self.all_joint[int(joint_position_bind / 2)]

        # QUERY THE POSITION RIGHT SIDE
        self.xform_jnt01_RGT = mc.xform(joint01_RGT, ws=1, q=1, t=1)
        self.xform_jnt02_RGT = mc.xform(joint02_RGT, ws=1, q=1, t=1)
        self.xform_jnt_mid = mc.xform(joint_mid, ws=1, q=1, t=1)

        mc.select(cl=1)
        jnt01_RGT   = mc.joint(n=self.prefix_name_curve + '01' + side_RGT + '_bind', p=self.xform_jnt01_RGT, rad=0.5 * scale)
        jnt02_RGT   = mc.duplicate(jnt01_RGT, n=self.prefix_name_curve + '02' + side_RGT + '_bind')[0]
        jnt_mid     = mc.duplicate(jnt01_RGT, n=self.prefix_name_curve + '_bind')[0]

        # SET THE POSITION RGT JOINT
        mc.xform(jnt02_RGT, ws=1, t=self.xform_jnt02_RGT)
        mc.xform(jnt_mid, ws=1, t=self.xform_jnt_mid)

        # MIRROR BIND JOINT 02 AND 01
        jnt01_LFT = mc.mirrorJoint(jnt01_RGT, mirrorYZ=True, searchReplace=(side_RGT, side_LFT))[0]
        jnt02_LFT = mc.mirrorJoint(jnt02_RGT, mirrorYZ=True, searchReplace=(side_RGT, side_LFT))[0]

        # QUERY POSITION LFT JOINT
        self.xform_jnt02_LFT = mc.xform(jnt02_LFT, ws=1, q=1, t=1)
        self.xform_jnt01_LFT = mc.xform(jnt01_LFT, ws=1, q=1, t=1)

        # CREATE BIND CURVE
        deform_curve = mc.curve(ep=[(self.xform_jnt01_RGT), (self.xform_jnt02_RGT), (self.xform_jnt_mid),
                                    (self.xform_jnt02_LFT), (self.xform_jnt01_LFT)],
                                degree=1)
        deform_curve = mc.rename(deform_curve, (self.prefix_name_curve + 'Bind' + '_crv'))

        # PARENT THE BIND JOINT
        self.joint_bind_mid_grp = tf.create_parent_transform(parent_list=['Zro', 'Offset'], object=jnt_mid,
                                                             match_position=jnt_mid, prefix=self.prefix_name_curve + 'Drv',
                                                             suffix='_bind')

        self.joint_bind01_RGT_grp = tf.create_parent_transform(parent_list=['Zro', 'Offset', 'All'], object=jnt01_RGT,
                                                               match_position=jnt01_RGT, prefix=self.prefix_name_curve + 'Drv01',
                                                               suffix='_bind', side=side_RGT)

        self.joint_bind02_RGT_grp = tf.create_parent_transform(parent_list=['Zro', 'Offset'], object=jnt02_RGT,
                                                               match_position=jnt02_RGT, prefix=self.prefix_name_curve + 'Drv02',
                                                               suffix='_bind', side=side_RGT)

        self.joint_bind01_LFT_grp = tf.create_parent_transform(parent_list=['Zro', 'Offset', 'All'], object=jnt01_LFT,
                                                               match_position=jnt01_LFT, prefix=self.prefix_name_curve + 'Drv01',
                                                               suffix='_bind', side=side_LFT)

        self.joint_bind02_LFT_grp = tf.create_parent_transform(parent_list=['Zro', 'Offset'], object=jnt02_LFT,
                                                               match_position=jnt02_LFT, prefix=self.prefix_name_curve + 'Drv02',
                                                               suffix='_bind', side=side_LFT)

        # ROTATION BIND JOINT FOLLOW THE MOUTH SHAPE
        mc.setAttr(self.joint_bind01_RGT_grp[0] + '.rotateY', lip01_direction * -1)
        mc.setAttr(self.joint_bind02_RGT_grp[0] + '.rotateY', lip02_direction * -1)
        mc.setAttr(self.joint_bind01_LFT_grp[0] + '.rotateY', lip01_direction)
        mc.setAttr(self.joint_bind02_LFT_grp[0] + '.rotateY', lip02_direction)

        # REBUILD THE CURVE
        mc.rebuildCurve(deform_curve, rpo=1, rt=0, end=1, kr=0, kcp=0,
                        kep=1, kt=0, s=2, d=3, tol=0.01)

        # SKINNING THE JOINT TO THE BIND CURVE
        skin_cluster = mc.skinCluster([jnt01_LFT, jnt02_LFT, jnt01_RGT, jnt02_RGT, jnt_mid], deform_curve,
                                      n='%s%s%s'% ('wire', self.prefix_name_curve.capitalize(), 'SkinCluster'), tsb=True, bm=0, sm=0, nw=1, mi=3)

        # Distribute the skin
        skin_percent_index0 = '%s.cv[0]' % deform_curve
        skin_percent_index1 = '%s.cv[1]' % deform_curve
        skin_percent_index2 = '%s.cv[2]' % deform_curve
        skin_percent_index3 = '%s.cv[3]' % deform_curve
        skin_percent_index4 = '%s.cv[4]' % deform_curve

        mc.skinPercent(skin_cluster[0], skin_percent_index0, tv=[(jnt01_RGT, 1.0)])
        mc.skinPercent(skin_cluster[0], skin_percent_index1, tv=[(jnt02_RGT, 1.0)])
        mc.skinPercent(skin_cluster[0], skin_percent_index2, tv=[(jnt_mid, 1.0)])
        mc.skinPercent(skin_cluster[0], skin_percent_index3, tv=[(jnt02_LFT, 1.0)])
        mc.skinPercent(skin_cluster[0], skin_percent_index4, tv=[(jnt01_LFT, 1.0)])

        # WIRE THE CURVE
        wire_deformer = mc.wire(lip_curve, dds=(0, 100 * scale), wire=deform_curve)
        wire_deformer[0] = mc.rename(wire_deformer[0], (self.prefix_name_curve + '_wireNode'))
        mc.setAttr(wire_deformer[0] + '.scale[0]', 0)


        # CONSTRAINT MID TO 02 LEFT AND RIGHT
        jnt_mid_LFT_constraint = mc.parentConstraint(jnt_mid, self.joint_bind02_LFT_grp[0], mo=1)
        jnt_mid_RGT_constraint = mc.parentConstraint(jnt_mid, self.joint_bind02_RGT_grp[0], mo=1)

        # CONSTRAINT RENAME
        au.constraint_rename([jnt_mid_LFT_constraint[0], jnt_mid_RGT_constraint[0]])

        self.jnt_mid = jnt_mid
        self.jnt01_RGT = jnt01_RGT
        self.jnt02_RGT = jnt02_RGT
        self.jnt01_LFT = jnt01_LFT
        self.jnt02_LFT = jnt02_LFT

        # CREATE GRP CURVES
        self.curves_grp = mc.createNode('transform', n=self.prefix_name_curve + 'DrvCrv' + '_grp')
        mc.setAttr (self.curves_grp + '.it', 0, l=1)
        mc.parent(deform_curve, mc.listConnections(wire_deformer[0] + '.baseWire[0]')[0], self.curves_grp)
        mc.hide(self.curves_grp)

        # CONNECT MOUTH RESET UTILS GRP TO BIND SCALE PARENT GRP
        list_bind_joint_grp = [self.joint_bind_mid_grp[0], self.joint_bind01_RGT_grp[0], self.joint_bind02_RGT_grp[0],
                               self.joint_bind01_LFT_grp[0], self.joint_bind02_LFT_grp[0]]
        for item in list_bind_joint_grp:
            au.connect_attr_scale(self.reset_all_mouth_ctrl_grp, item)

        # CREATE GRP BIND
        self.bind_jnt_grp = mc.createNode('transform', n=self.prefix_name_curve + 'DrvJntBind' + '_grp')
        mc.parent(self.joint_bind_mid_grp[0], self.joint_bind01_RGT_grp[0], self.joint_bind02_RGT_grp[0],
                  self.joint_bind01_LFT_grp[0], self.joint_bind02_LFT_grp[0], self.bind_jnt_grp)
        mc.hide(self.bind_jnt_grp)

        self.deform_curve = deform_curve

    def create_reset_mouth_position_grp(self, mouth_base_jnt):
        joint_position_bind = len(self.all_joint)

        joint_mid_all =  self.all_joint[int(joint_position_bind / 2)]
        joint_mid =mc.xform(joint_mid_all, ws=1, q=1, t=1)

        # OFFSETTING TO MOUTH
        position_mouth = mc.xform(mouth_base_jnt, ws=1, q=1, t=1)
        self.mouth_ctrl_grp = mc.createNode('transform', n=self.prefix_name_curve + 'DrvAllCtrlMouth_grp')
        self.mouth_ctrl_grp_offset = mc.group(em=1, n=self.prefix_name_curve + 'DrvAllCtrlMouthOffset_grp', p=self.mouth_ctrl_grp)
        mc.xform(self.mouth_ctrl_grp, ws=1, t=position_mouth)

        # RESETTING TRANSFORM FOR SET
        self.reset_all_mouth_ctrl_grp = mc.createNode('transform', n=self.prefix_name_curve + 'DrvAllResetUtilMouth_grp')
        self.reset_all_mouth_ctrl_grp_offset = mc.group(em=1, n=self.prefix_name_curve + 'DrvAllResetUtilMouthOffset_grp', p=self.reset_all_mouth_ctrl_grp)
        mc.xform(self.reset_all_mouth_ctrl_grp, ws=1, t=position_mouth)

        reset_mouth_ctrl_grp = mc.createNode('transform', n=self.prefix_name_curve + 'DrvAllResetUtilOffset_grp')
        self.reset_mouth_ctrl_grp_offset = mc.spaceLocator(n=self.prefix_name_curve + 'DrvAllResetUtil_loc')[0]
        mc.parent(self.reset_mouth_ctrl_grp_offset, reset_mouth_ctrl_grp)
        mc.hide(self.reset_mouth_ctrl_grp_offset)

        mc.xform(reset_mouth_ctrl_grp, ws=1, t=joint_mid)

        mc.parent(reset_mouth_ctrl_grp, self.reset_all_mouth_ctrl_grp_offset)

        # CONNECT ATRIBUTE FROM MOUTH TO RESET MOUTH OFFSET AND RESET CONTROLLER MOUTH
        au.connect_attr_rotate(mouth_base_jnt, self.reset_all_mouth_ctrl_grp_offset)
        au.connect_attr_rotate(mouth_base_jnt, self.mouth_ctrl_grp_offset)

        # CONNECT DRIVE ALL RESET MOUTH TO  THE GRP PARENT JNT GRP LIP
        for jnt_grp, loc_offset in zip (self.control_group_zro, self.locator_group_offset):
            au.connect_attr_scale(self.reset_all_mouth_ctrl_grp, jnt_grp)
            au.connect_attr_scale(self.reset_all_mouth_ctrl_grp, loc_offset)

    def create_joint_lip(self, curve, scale, ctrl_color, suffix_controller,
                         # parent_skin
                         ):
        self.all_joint =[]
        # self.all_skin=[]
        self.locator_group_offset=[]
        self.locator_group_zro = []
        self.all_locator=[]
        self.control_group_zro=[]
        self.control_group_offset=[]

        for index, object in enumerate(self.curve_vertex):
            # create joint
            mc.select(cl=1)
            self.joint = mc.joint(n='%s%02d%s' % (self.prefix_name_curve, (index + 1), '_skn'), rad=0.1 * scale)
            mc.setAttr(self.joint+'.visibility', 0)
            position = mc.xform(object, q=1, ws=1, t=1)
            mc.xform(self.joint, ws=1, t=position)
            self.all_joint.append(self.joint)

            control_group = ct.Control(match_obj_first_position=self.joint, prefix=self.prefix_name_curve + str(index + 1).zfill(2),
                                       shape=ct.JOINT, groups_ctrl=['', 'Offset'], ctrl_size=scale * 0.1,
                                       ctrl_color=ctrl_color, lock_channels=['v'], connection=['parent'], suffix=suffix_controller
                                       )
            self.control_group_zro.append(control_group.parent_control[0])
            self.control_group_offset.append(control_group.parent_control[1])

            # create locator
            self.locator = mc.spaceLocator(n='%s%02d%s' % (self.prefix_name_curve, (index + 1), '_loc'))[0]

            mc.xform(self.locator, ws=1, t=position)
            locator_group = tf.create_parent_transform(parent_list=['Zro', 'Offset'], object=self.locator,
                                                       match_position=self.locator, prefix=self.prefix_name_curve + str(index + 1).zfill(2),
                                                       suffix='_loc')
            self.locator_group_offset.append(locator_group[1])
            self.locator_group_zro.append(locator_group[0])
            self.all_locator.append(self.locator)

            # connect curve to locator grp
            curveRelatives = mc.listRelatives(curve, s=True)[0]
            uParam = cr.get_uParam(position, curveRelatives)
            pci_node = mc.createNode("pointOnCurveInfo", n='%s%02d%s' % (self.prefix_name_curve, (index + 1), '_pci'))
            mc.connectAttr(curveRelatives + '.worldSpace', pci_node + '.inputCurve')
            mc.setAttr(pci_node + '.parameter', uParam)
            mc.connectAttr(pci_node + '.position', locator_group[0] + '.t')

            decompose_node = mc.createNode('decomposeMatrix', n='%s%02d%s' % (self.prefix_name_curve, (index + 1), '_dmtx'))
            mc.connectAttr(locator_group[1] + '.worldMatrix[0]', decompose_node + '.inputMatrix')

            mc.connectAttr(decompose_node + '.outputTranslate', control_group.parent_control[0] + '.translate')
            mc.connectAttr(decompose_node + '.outputRotate', control_group.parent_control[0] + '.rotate')
            # mc.connectAttr(dMtx + '.outputScale', parentJntGrp[0] + '.scale')
            mc.setAttr(self.joint+'.visibility', 0)

            # # CREATE SKINNING JOINT
            # mc.select(cl=1)
            # self.skin = mc.joint(n='%s%02d%s' % (self.prefix_name_curve, (index + 1), '_skn'), rad=0.1 * scale)
            #
            # # SKIN PARENT AND SCALE CONSTRAINT
            # au.parent_scale_constraint(self.joint, self.skin)
            # self.all_skin.append(self.skin)

        # grouping joint
        self.joint_grp = mc.group(em=1, n=self.prefix_name_curve + 'JntCtr' + '_grp')
        mc.parent(self.control_group_zro, self.joint_grp)

        # grouping locator
        self.locator_grp = mc.group(em=1, n=self.prefix_name_curve + 'Loc' + '_grp')
        mc.setAttr (self.locator_grp + '.it', 0, l=1)
        mc.parent(self.locator_group_zro, self.locator_grp)

        # # PARENT SKIN JOINT
        # mc.parent(self.all_skin, parent_skin)
