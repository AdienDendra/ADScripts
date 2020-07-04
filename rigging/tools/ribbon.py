from __builtin__ import reload

import maya.cmds as mc

from rigging.library.utils import controller as ct, core as cr, transform as tr
from rigging.tools import AD_utils as au

reload(cr)
reload(tr)
reload(ct)
reload(au)

class CreateRibbon:
    def __init__(self,
                 deformer=False,
                 create_ctrl =False,
                 tip = '',
                 base ='',
                 parallel_axis ='z',
                 tip_position ='',
                 aim_axis='',
                 up_axis ='',
                 ctrlShape_tip =ct.SQUARE,
                 ctrlShape_mid = ct.SQUARE,
                 ctrlShape_base =ct.SQUARE,
                 ctrlShape_details = ct.CIRCLEPLUS,
                 ctrl_size = 1.0,
                 prefix='prefix',
                 number_joints=None):

        """
        :param deformer     : bool, create deformer setup on ribbon
        :param create_ctrl   : bool, parameters for creating the control module and tip
        :param tip          : str, transform or joint as the tip of ribbon
        :param base         : str, transform or joint as the module of ribbon
        :param parallel_axis : str, two point parallel position direction whether on x or y or z axis
        :param tip_position       : str, position point (joint) of the tip regarding on the module joint by seeing the axis whether on + or - axis
        :param aim_axis      : str, aim axis is that tip pivot looking the module joint. Can fill with +x +y +z or -x -y -z
        :param up_axis       : str, up axis is that one pivot towards to y axis for rotation joint. Can fill with +x +y +z or -x -y -z
        :param ctrlShape_tip      : var, ctrl shape of tip
        :param ctrl_mid      : var, ctrl shape of middle
        :param ctrlShape_base     : var, ctrl shape of module
        :param ctrlTip      : var, ctrl shape of detail ribbon ctrl
        :param prefix       : str, prefix name for ribbon
        :param number_joints    : int, number of joint as well as the control of ribbon part
        """
        # Width plane variable (following the number of joints
        size = float(number_joints)

        # Tip point dictionary towards
        tip_point = {'+': [(size / 2.0 * -1), (size / 2.0)],
                    '-': [(size / 2.0), (size / 2.0 * -1)]}

        if tip_position in tip_point.keys():
            self.pos       = (0,0,0)
            self.up_point   = tip_point[tip_position][0]
            self.down_point = tip_point[tip_position][1]
        else:
            raise mc.error('The string %s in tipPos argument is not found. Fill with + or -' % tip_position)

        # Dictionary list
        tmp_plane_dictionary ={'x': [(0, 1, 0), size, (1.0 / size), number_joints, 1],
                      'y': [(1,0,0), 1, size, 1, number_joints],
                      'z': [(0,1,0), 1, size, 1, number_joints]}

        direction = {'x': ['.rotateY', 90, '.translateZ'],
                     'y': ['.rotateZ', 90, '.translateZ'],
                     'z': ['.rotateX', 0, '.translateX']}

        if tip_position== '-':
            rot_defomer = {'x': (0, 0, -90),
                          'y': (0, 0, 180),
                          'z': (-90, 0, 90)}
        else:
            rot_defomer = {'x': (0, 0, 90),
                          'y': (0, 0, 180),
                          'z': (-90, 0, 90)}

        volume_input_mdn = {'x': ['.translateX', '.input1Z', '.outputZ', '.scaleY', '.scaleZ'],
                       'y': ['.translateY','.input1Z', '.outputZ', '.scaleX', '.scaleZ'],
                       'z': ['.translateZ','.input1X', '.outputX','.scaleX', '.scaleZ']}

        follicle_volume ={'x': ('.parameterV', -1),
                      'y': ('.parameterU', -1),
                      'z': ('.parameterU', 1)}

        # Create the main groups
        self.grp_all_ribbon = mc.group(empty=True, name=(prefix + 'AllRibbon_grp'))

        self.grp_transform = mc.group(empty=True, name=(prefix + 'Transform_grp'))
        self.grp_ctrl = mc.duplicate(self.grp_transform, name=(prefix + 'Ctrl_grp'))
        self.grp_jnt_cluster = mc.duplicate(self.grp_transform, name=(prefix + 'JntCluster_grp'))

        self.grp_no_transform = mc.duplicate(self.grp_all_ribbon, name=(prefix + 'NoTransform_grp'))
        self.grp_surface = mc.duplicate(self.grp_all_ribbon, name=(prefix + 'Surface_grp'))

        self.grp_misc = mc.duplicate(self.grp_all_ribbon, name=(prefix + 'Misc_grp'))
        self.grp_surfaces = mc.duplicate(self.grp_all_ribbon, name=(prefix + 'Surfaces_grp'))
        self.grp_follicle_main = mc.duplicate(self.grp_all_ribbon, name=(prefix + 'FolliclesSkin_grp'))
        self.grp_follicle_offset = mc.duplicate(self.grp_all_ribbon, name=(prefix + 'FolliclesSkinOffset_grp'))
        mc.setAttr(self.grp_follicle_offset[0] + '.it', 0, l=1)

        # Create a NURBS-plane to use as a module
        tmp_plane = mc.nurbsPlane(axis=tmp_plane_dictionary[parallel_axis][0], width=tmp_plane_dictionary[parallel_axis][1],
                                  lengthRatio=tmp_plane_dictionary[parallel_axis][2], u=tmp_plane_dictionary[parallel_axis][3],
                                  v=tmp_plane_dictionary[parallel_axis][4], degree=3, ch=0)[0]

        # Create the NURBS-planes to use in the setup
        geo_plane = mc.duplicate(tmp_plane, name=(prefix + '_geo'))
        geo_plane_wire = mc.duplicate(tmp_plane, name=(prefix + 'WireDef_geo'))
        geo_plane_orient = mc.duplicate(tmp_plane, name=(prefix + 'OrientDef_geo'))

        # Create Joint reference
        joint_create = mc.createNode('joint')

        # Duplicate joint from reference for skinning to the wire curve
        self.joint_up = mc.duplicate(joint_create, n=prefix + 'Up_jnt')
        self.joint_mid = mc.duplicate(joint_create, n=prefix + 'Mid_jnt')
        self.joint_down = mc.duplicate(joint_create, n=prefix + 'Down_jnt')

        # Duplicate joint from reference for orientation ribbon
        self.joint_orient_up = mc.duplicate(joint_create, n=prefix + 'OrientUp_jnt')
        self.joint_orient_mid = mc.duplicate(joint_create, n=prefix + 'OrientMid_jnt')
        self.joint_orient_down = mc.duplicate(joint_create, n=prefix + 'OrientDown_jnt')

        # Set the position for joints
        mc.setAttr((self.joint_up[0] + '.translate'), self.up_point, self.pos[1], self.pos[2])
        mc.setAttr((self.joint_mid[0] + '.translate'), self.pos[0], self.pos[1], self.pos[2])
        mc.setAttr((self.joint_down[0] + '.translate'), self.down_point, self.pos[1], self.pos[2])

        # Set the position for joints orient
        mc.setAttr((self.joint_orient_up[0] + '.translate'), self.up_point, self.pos[1], self.pos[2])
        mc.setAttr((self.joint_orient_mid[0] + '.translate'), self.pos[0], self.pos[1], self.pos[2])
        mc.setAttr((self.joint_orient_down[0] + '.translate'), self.down_point, self.pos[1], self.pos[2])

        # Set the joints rotation axis aiming and upper
        cr.direction_pivot(self.joint_orient_up[0], aim_axis=aim_axis, up_axis=up_axis)
        cr.direction_pivot(self.joint_orient_mid[0], aim_axis=aim_axis, up_axis=up_axis)
        cr.direction_pivot(self.joint_orient_down[0], aim_axis=aim_axis, up_axis=up_axis)

        # Grouping the joints to have rotation according to parallel axis
        grp_joint_orient = mc.group(self.joint_orient_up[0], self.joint_orient_mid[0], self.joint_orient_down[0],
                                    self.joint_up[0], self.joint_mid[0], self.joint_down[0])

        # Set the rotation group joints
        if parallel_axis == 'z':
            mc.setAttr((grp_joint_orient + '.rotate'), 0, -90, 0)

        if parallel_axis == 'y':
            mc.setAttr((grp_joint_orient + '.rotate'), 0, 0, 90)

        # Unparent from the group
        mc.parent(self.joint_orient_up[0], self.joint_orient_mid[0], self.joint_orient_down[0],
                  self.joint_up[0], self.joint_mid[0], self.joint_down[0], w=1)

        # Create Group for joints wire curve
        self.joint_up_parent = tr.create_parent_transform(parent_list=['Zro'], object=self.joint_up[0],
                                                          match_position=self.joint_up[0], prefix=au.prefix_name(self.joint_up[0]),
                                                          suffix='_jnt')

        self.joint_mid_parent = tr.create_parent_transform(parent_list=['Zro'], object=self.joint_mid[0],
                                                           match_position=self.joint_mid[0],
                                                           prefix=au.prefix_name(self.joint_mid[0]),
                                                           suffix='_jnt')

        self.joint_down_parent = tr.create_parent_transform(parent_list=['Zro'], object=self.joint_down[0],
                                                            match_position=self.joint_down[0],
                                                            prefix=au.prefix_name(self.joint_down[0]),
                                                            suffix='_jnt')

        # Create Group for joints orientation ribbon
        self.joint_up_orient_parent = tr.create_parent_transform(['Zro'], self.joint_orient_up[0],
                                                                 self.joint_orient_up[0], self.joint_orient_up[0], '_jnt')
        self.joint_mid_orient_parent = tr.create_parent_transform(['Zro'], self.joint_orient_mid[0],
                                                                  self.joint_orient_mid[0], self.joint_orient_mid[0], '_jnt')
        self.joint_down_orient_parent = tr.create_parent_transform(['Zro'], self.joint_orient_down[0],
                                                                   self.joint_orient_down[0], self.joint_orient_down[0], '_jnt')

        # Create the controllers
        ctrl_up = ct.Control(match_obj_first_position=self.joint_up_parent[0], prefix=prefix + 'Up',
                             groups_ctrl=['Zro', 'Offset'],
                             ctrl_size=ctrl_size, shape=ctrlShape_tip)
        ctrl_mid = ct.Control(match_obj_first_position=self.joint_mid_parent[0], prefix=prefix + 'Mid',
                              groups_ctrl=['Zro', 'Offset'],
                              ctrl_color='blue', ctrl_size=ctrl_size * 1.3, shape=ctrlShape_mid)
        ctrl_down = ct.Control(match_obj_first_position=self.joint_down_parent[0], prefix=prefix + 'Down',
                               groups_ctrl=['Zro', 'Offset'],
                               ctrl_size=ctrl_size, shape=ctrlShape_base)

        # Get part joint position
        self.joint_reference_up = mc.duplicate(self.joint_up[0], n=prefix + 'Up_jnt')
        self.joint_reference_down = mc.duplicate(self.joint_down[0], n=prefix + 'Down_jnt')

        # Unparent joint duplicate
        mc.parent(self.joint_reference_up, self.joint_reference_down, w=True)

        # Create joint on evenly position
        position_uv_follicle = cr.split_evenly(self.joint_reference_up, self.joint_reference_down, prefix, split=number_joints)

        # match orient joint
        mc.delete(mc.orientConstraint(base, self.joint_up_orient_parent[0]))
        mc.delete(mc.orientConstraint(base, tip, self.joint_mid_orient_parent[0]))
        mc.delete(mc.orientConstraint(tip, self.joint_down_orient_parent[0]))

        # Create deformers: Wire deformer
        deform_curve = mc.curve(p=[(self.down_point, 0, 0), (0, 0, 0), (self.up_point, 0, 0)], degree=2)
        deform_curve = mc.rename(deform_curve, (prefix + 'Wire_crv'))
        # Set orient curve
        mc.delete(mc.orientConstraint(grp_joint_orient, deform_curve))

        wire_deformer = mc.wire(geo_plane_wire, dds=(0, 15), wire=deform_curve)
        wire_deformer[0] = mc.rename(wire_deformer[0], (au.prefix_name(geo_plane_wire[0]) + '_wireNode'))

        # Skining joints to curve
        mc.skinCluster([self.joint_up[0], self.joint_mid[0], self.joint_down[0]], deform_curve,
                       n='wireSkinCluster', tsb=True, bm=0, sm=0, nw=1, mi=1)

        # Skining joints orient to plane orient
        mc.skinCluster([self.joint_orient_up[0], self.joint_orient_mid[0], self.joint_orient_down[0]], geo_plane_orient,
                       n='orientSkinCluster', tsb=True, bm=0, sm=0, nw=1, mi=2)

        # Point constraining the the controller transform to the joint wire curve
        pac_jnt_up = mc.parentConstraint(ctrl_up.control, self.joint_up_parent[0])
        pac_jnt_mid = mc.parentConstraint(ctrl_mid.control, self.joint_mid_parent[0])
        pac_jnt_down = mc.parentConstraint(ctrl_down.control, self.joint_down_parent[0])

        # Connect controller module and up joint orient
        sum_double_ctrl_up = mc.shadingNode('plusMinusAverage', asUtility=1, name=(prefix + 'AverageOrientUp_pma'))
        mc.connectAttr((ctrl_up.control + '.rotate'), (sum_double_ctrl_up + '.input3D[0]'))
        mc.connectAttr((base + '.rotate'), (sum_double_ctrl_up + '.input3D[1]'))
        mc.connectAttr((sum_double_ctrl_up + '.output3D'), (self.joint_orient_up[0] + '.rotate'))

        # Connect controller middle to joint orient
        mc.connectAttr(ctrl_mid.control + '.rotate', self.joint_orient_mid[0] + '.rotate')

        # Connect controller tip and down joint orient
        sum_double_ctrl_down = mc.shadingNode('plusMinusAverage', asUtility=1, name=(prefix + 'AverageOrientDwn_pma'))
        mc.connectAttr((ctrl_down.control + '.rotate'), (sum_double_ctrl_down + '.input3D[0]'))
        mc.connectAttr((tip + '.rotate'), (sum_double_ctrl_down + '.input3D[1]'))
        mc.connectAttr((sum_double_ctrl_down + '.output3D'), (self.joint_orient_down[0] + '.rotate'))

        # Create deformers: Blendshape
        ribbon_blendshape = mc.blendShape(geo_plane_wire[0], geo_plane_orient[0],
                                          geo_plane[0], name=(prefix + '_bsn'), weight=[(0, 1), (1, 1)])


        # Create follicles: The main-surface and the volume-surface
        follicle_s = self.item_follicle(position_uv_follicle, geo_plane, 'fol')

        # Scaling the follicle with decompose matrix
        decompose_matrix_node = mc.createNode('decomposeMatrix', n=prefix + 'RbnScaleFol_dmtx')
        mc.connectAttr(self.grp_transform + '.worldMatrix[0]', decompose_matrix_node + '.inputMatrix')


        # Grouping listing of the follicle parent group
        follicle_ctrl_grp = []
        follicle_grp_off = []

        for fols in (follicle_s['follicle']):
            mc.connectAttr(decompose_matrix_node + '.outputScale', fols + '.scale')
            folLr = mc.listRelatives(fols, s=1)[0]
            mc.setAttr(folLr + '.visibility', 0)

            # Listing the shape of follicles
            folLr = mc.listRelatives(fols, s=1)[0]
            mc.setAttr(folLr + '.visibility', 0)

            # Parenting the follicles to grp follicle
            mc.parent(fols, self.grp_follicle_offset)

            # Create group offset for follilce
            follicle_grp_offset = mc.group(empty=True, name='%s_%s' % (au.prefix_name(fols), 'setGrp'))
            mc.delete(mc.parentConstraint(fols, follicle_grp_offset))
            follicle_grp_off.append(follicle_grp_offset)

            # Create offset group follicle
            follicle_grp_offset = mc.parent(follicle_grp_offset, fols)

            # Create a joint, controller and a group for the current skin-follicle
            mc.select(clear=True)

            # Create joint for follicle
            follicle_joint = mc.joint(name='%s_%s' % (au.prefix_name(fols), 'jnt'), radius=1.0)

            # Create control for joint in follicle
            follicle_ctrl = ct.Control(prefix=au.prefix_name(fols), groups_ctrl=['Zro', 'Offset'],
                                       ctrl_color='lightPink', ctrl_size=ctrl_size * 0.8, shape=ctrlShape_details)
            follicle_ctrl_grp.append(follicle_ctrl.parent_control[0])
            # Parent joint to controller
            mc.parent(follicle_joint, follicle_ctrl.control)

            # Positioning skin-follicle control
            mc.delete(mc.parentConstraint(ctrl_mid.control, follicle_ctrl.parent_control[0]))
            mc.delete(mc.pointConstraint(follicle_grp_offset, follicle_ctrl.parent_control[0]))

            # Parent controller to group offset follicle
            mc.parent(follicle_ctrl.parent_control[0], follicle_grp_offset)

        #### IF DEFORM TRUE
        if deformer:
            self.grp_deformers = mc.duplicate(self.grp_all_ribbon, name=(prefix + 'Deformer_grp'))
            self.grp_foll_volume = mc.duplicate(self.grp_all_ribbon, name=(prefix + 'FolliclesVolume_grp'))

            geo_plane_volume = mc.duplicate(tmp_plane, name=(prefix + 'Volume_geo'))
            geo_plane_twist = mc.duplicate(tmp_plane, name=(prefix + 'TwistDef_geo'))
            geo_plane_sine = mc.duplicate(tmp_plane, name=(prefix + 'SineDef_geo'))

            # Offset the volume-plane
            mc.setAttr((geo_plane_volume[0] + direction[parallel_axis][2]), -0.5)

            # Add attributes: Twist/Roll attributes
            self.add_attribute(objects=[ctrl_down.control, ctrl_mid.control, ctrl_up.control],
                               long_name=['twistSep'], nice_name=[' '], at="enum", en='Twist', channel_box=True)

            self.add_attribute(objects=[ctrl_down.control, ctrl_up.control], long_name=['twist'], at="float", keyable=True)
            self.add_attribute(objects=[ctrl_down.control, ctrl_up.control], long_name=['twistOffset'], at="float", keyable=True)
            self.add_attribute(objects=[ctrl_down.control, ctrl_up.control], long_name=['affectToMid'], at="float", min=0,
                               max=10, dv=10, keyable=True)
            self.add_attribute(objects=[ctrl_mid.control], long_name=['roll'], at="float", keyable=True)
            self.add_attribute(objects=[ctrl_mid.control], long_name=['rollOffset'], at="float", keyable=True)

            # Add attributes: Volume attributes
            self.add_attribute(objects=[ctrl_mid.control], long_name=['volumeSep'], nice_name=[' '], at="enum",
                               en='Volume', channel_box=True)

            self.add_attribute(objects=[ctrl_mid.control], long_name=['volume'], at="float", min=-1, max=1, keyable=True)
            self.add_attribute(objects=[ctrl_mid.control], long_name=['volumeMultiplier'], at="float", min=1, dv=3, keyable=True)
            self.add_attribute(objects=[ctrl_mid.control], long_name=['startDropoff'], at="float", min=0, max=1, dv=1,
                               keyable=True)
            self.add_attribute(objects=[ctrl_mid.control], long_name=['endDropoff'], at="float", min=0, max=1, dv=1,
                               keyable=True)
            self.add_attribute(objects=[ctrl_mid.control], long_name=['volumeScale'], at="float", min=self.up_point * 0.9,
                               max=self.down_point * 2, keyable=True)
            self.add_attribute(objects=[ctrl_mid.control], long_name=['volumePosition'], min=self.up_point,
                               max=self.down_point, at="float", keyable=True)

            # Add attributes: Sine attributes
            self.add_attribute(objects=[ctrl_mid.control], long_name=['sineSep'], nice_name=[' '], attributeType='enum',
                               en="Sine:", channel_box=True)

            self.add_attribute(objects=[ctrl_mid.control], long_name=['amplitude'], attributeType="float", keyable=True)
            self.add_attribute(objects=[ctrl_mid.control], long_name=['offset'], attributeType="float", keyable=True)
            self.add_attribute(objects=[ctrl_mid.control], long_name=['twist'], attributeType="float", keyable=True)
            self.add_attribute(objects=[ctrl_mid.control], long_name=['sineLength'], min=0.1, dv=2, attributeType="float",
                               keyable=True)


            # Create deformers: Twist deformer, Sine deformer, Squash deformer
            # Set them rotation  according on point parallelFaceAxis position
            self.twist_deformer = self.nonlinear_deformer(objects=[geo_plane_twist[0]], deformer_type='twist',
                                                          name=au.prefix_name(geo_plane_twist[0]), low_bound=-1,
                                                          high_bound=1, rotate=rot_defomer[parallel_axis])

            self.sine_deformer = self.nonlinear_deformer(objects=[geo_plane_sine[0]], deformer_type='sine',
                                                         name=au.prefix_name(geo_plane_sine[0]), low_bound=-1,
                                                         high_bound=1, rotate=rot_defomer[parallel_axis])

            self.squash_deformer = self.nonlinear_deformer(objects=[geo_plane_volume[0]], deformer_type='squash',
                                                           name=au.prefix_name(geo_plane_volume[0]), low_bound=-1,
                                                           high_bound=1, rotate=rot_defomer[parallel_axis])

            mc.setAttr((self.sine_deformer[0] + '.dropoff'), 1)

            # Twist deformer: Sum the twist and the roll
            sum_top_pma = mc.shadingNode('plusMinusAverage', asUtility=1, name=(prefix + 'TwistUpSum_pma'))
            mc.connectAttr((ctrl_down.control + '.twist'), (sum_top_pma + '.input1D[0]'))
            mc.connectAttr((ctrl_down.control + '.twistOffset'), (sum_top_pma + '.input1D[1]'))
            mc.connectAttr((ctrl_mid.control + '.roll'), (sum_top_pma + '.input1D[2]'))
            mc.connectAttr((ctrl_mid.control + '.rollOffset'), (sum_top_pma + '.input1D[3]'))
            mc.connectAttr((sum_top_pma + '.output1D'), (self.twist_deformer[0] + '.startAngle'))

            sum_end_pma = mc.shadingNode('plusMinusAverage', asUtility=1, name=(prefix + 'TwistDownSum_pma'))
            mc.connectAttr((ctrl_up.control + '.twist'), (sum_end_pma + '.input1D[0]'))
            mc.connectAttr((ctrl_up.control + '.twistOffset'), (sum_end_pma + '.input1D[1]'))
            mc.connectAttr((ctrl_mid.control + '.roll'), (sum_end_pma + '.input1D[2]'))
            mc.connectAttr((ctrl_mid.control + '.rollOffset'), (sum_end_pma + '.input1D[3]'))
            mc.connectAttr((sum_end_pma + '.output1D'), (self.twist_deformer[0] + '.endAngle'))

            # Twist deformer: Set up the affect of the deformer
            top_affect_mdl = mc.shadingNode('multDoubleLinear', asUtility=1, name=(prefix + 'TwistUpAffect_mdl'))
            mc.setAttr((top_affect_mdl + '.input1'), -0.1)
            mc.connectAttr((ctrl_down.control + '.affectToMid'), (top_affect_mdl + '.input2'))
            mc.connectAttr((top_affect_mdl + '.output'), (self.twist_deformer[0] + '.lowBound'))

            end_affect_mdl = mc.shadingNode('multDoubleLinear', asUtility=1, name=(prefix + 'TwistDownAffect_mdl'))
            mc.setAttr((end_affect_mdl + '.input1'), 0.1)
            mc.connectAttr((ctrl_up.control + '.affectToMid'), (end_affect_mdl + '.input2'))
            mc.connectAttr((end_affect_mdl + '.output'), (self.twist_deformer[0] + '.highBound'))

            # Squash deformer: Set up the connections for the volume control
            volume_reverse_mdl = mc.shadingNode('multDoubleLinear', asUtility=1, name=(prefix + 'VolumeReverse_mdl'))
            mc.setAttr((volume_reverse_mdl + '.input1'), -1)
            mc.connectAttr((ctrl_mid.control + '.volume'), (volume_reverse_mdl + '.input2'))
            mc.connectAttr((volume_reverse_mdl + '.output'), (self.squash_deformer[0] + '.factor'))
            mc.connectAttr((ctrl_mid.control + '.startDropoff'), (self.squash_deformer[0] + '.startSmoothness'))
            mc.connectAttr((ctrl_mid.control + '.endDropoff'), (self.squash_deformer[0] + '.endSmoothness'))

            # Set the translate squash deformer according the point parallelFaceAxis position
            mc.connectAttr((ctrl_mid.control + '.volumePosition'), (self.squash_deformer[1] + volume_input_mdn[parallel_axis][0]))

            # Squash deformer: Set up the volume scaling
            sum_scale_pma = mc.shadingNode('plusMinusAverage', asUtility=1, name=(prefix + 'VolumeScaleSum_pma'))
            mc.setAttr((sum_scale_pma + '.input1D[0]'), self.down_point)
            mc.connectAttr((ctrl_mid.control + '.volumeScale'), (sum_scale_pma + '.input1D[1]'))
            mc.connectAttr((sum_scale_pma + '.output1D'), (self.squash_deformer[1] + '.scaleY'))

            # Sine deformer: Set up the connections for the sine
            mc.connectAttr((ctrl_mid.control + '.amplitude'), (self.sine_deformer[0] + '.amplitude'))
            mc.connectAttr((ctrl_mid.control + '.offset'), (self.sine_deformer[0] + '.offset'))

            # Exception for z parallel axis
            if parallel_axis == 'z':
                sine_twist_node = mc.createNode('addDoubleLinear', n=(prefix + 'adjustSineTwistRotZ_adl'))
                mc.setAttr(sine_twist_node + '.input1', 90)
                mc.connectAttr(ctrl_mid.control + '.twist', sine_twist_node + '.input2')
                mc.connectAttr(sine_twist_node + '.output', self.sine_deformer[1] + '.rotateZ')
            else:
                mc.connectAttr((ctrl_mid.control + '.twist'), (self.sine_deformer[1] + '.rotateY'))

            mc.connectAttr((ctrl_mid.control + '.sineLength'), (self.sine_deformer[0] + '.wavelength'))

            # Create deformers: Blendshape
            mc.blendShape(ribbon_blendshape, e=1, t=(geo_plane[0], 2, geo_plane_twist[0], 1.0))
            mc.blendShape(ribbon_blendshape, e=1, t=(geo_plane[0], 3, geo_plane_sine[0], 1.0))

            mc.blendShape(ribbon_blendshape, e=True, w=[(2, 1.0), (3, 1.0)])

            # Create follicles: The main-surface and the volume-surface
            follicle_v = self.item_follicle(position_uv_follicle, geo_plane_volume, 'Volumefol')

            # Set the follicle U and V parameter
            for obj in follicle_v['follicle']:
                mc.setAttr(obj + follicle_volume[parallel_axis][0], follicle_volume[parallel_axis][1])

            # Looping the follicle S and follicle V
            for folv, fol_grp_offset in zip(follicle_v['follicle'], follicle_grp_off):

                # Make the connections for the volume according on point parallelFaceAxis position
                multiplier_mdn = mc.shadingNode('multiplyDivide', asUtility=1, name=au.prefix_name(folv) + 'Multiplier_mdn')
                mc.connectAttr((ctrl_mid.control + '.volumeMultiplier'), volume_input_mdn[parallel_axis][1])
                mc.connectAttr((folv + '.translate'), (multiplier_mdn + '.input2'))

                sum_volume = mc.shadingNode('plusMinusAverage', asUtility=1, name=au.prefix_name(folv) + 'VolumeSum_pma')
                mc.connectAttr((multiplier_mdn + volume_input_mdn[parallel_axis][2]), (sum_volume + '.input1D[0]'))
                mc.setAttr((sum_volume + '.input1D[1]'), 1)
                mc.connectAttr((sum_volume + '.output1D'), (fol_grp_offset + volume_input_mdn[parallel_axis][3]))
                mc.connectAttr((sum_volume + '.output1D'), (fol_grp_offset + volume_input_mdn[parallel_axis][4]))

            # Cleanup: Hierarchy
            mc.parent(self.twist_deformer[1], self.sine_deformer[1], self.squash_deformer[1], self.grp_deformers)
            mc.parent(geo_plane_twist[0], geo_plane_sine[0], geo_plane_volume[0], self.grp_surfaces)
            mc.parent(follicle_v['follicle'], self.grp_foll_volume)
            mc.parent(self.grp_deformers[0], self.grp_foll_volume[0], self.grp_no_transform)

        # Add attributes: Extra attributes
        self.add_attribute(objects=[ctrl_mid.control], long_name=['extraSep'], nice_name=[' '], at="enum", en='Extra',
                           channel_box=True)
        self.add_attribute(objects=[ctrl_mid.control], long_name=['showExtraCtrl'], at="long", min=0, max=1, dv=0,
                           channel_box=True)
        self.add_attribute(objects=[ctrl_mid.control], long_name=['showSurfaceRibbon'], at="long", min=0, max=1, dv=0,
                           channel_box=True)

        # connect the visibility-switch for the controller
        mc.connectAttr((ctrl_mid.control + '.showExtraCtrl'),
                       (self.grp_follicle_offset[0] + '.visibility'))

        # Connect the visibility of surface group
        mc.connectAttr((ctrl_mid.control + '.showSurfaceRibbon'),
                       (self.grp_surface[0] + '.visibility'))

        # Cleanup: Hierarchy
        mc.delete(mc.parentConstraint(base, tip, self.grp_transform))
        mc.delete(mc.orientConstraint(tmp_plane, self.grp_all_ribbon))
        mc.delete(mc.parentConstraint(base, tip, self.grp_all_ribbon))

        mc.parent(geo_plane_orient[0], self.grp_surfaces)
        mc.parent(self.joint_up_parent[0], self.joint_mid_parent[0], self.joint_down_parent[0], self.grp_jnt_cluster)
        mc.parent(ctrl_down.parent_control[0], ctrl_mid.parent_control[0], ctrl_up.parent_control[0], self.grp_ctrl)
        mc.parent(geo_plane[0], geo_plane_wire[0], (mc.listConnections(wire_deformer[0] + '.baseWire[0]')[0]), self.grp_surface)
        mc.parent(deform_curve, self.joint_up_orient_parent[0],
                  self.joint_mid_orient_parent[0], self.joint_down_orient_parent[0], self.grp_misc)
        mc.parent(self.grp_jnt_cluster, self.grp_surfaces[0], self.grp_misc[0], self.grp_no_transform)
        mc.parent(self.grp_ctrl[0], self.grp_surface[0], self.grp_follicle_main[0], base, tip, self.grp_transform)
        mc.parent(self.grp_follicle_offset[0], self.grp_follicle_main[0])
        mc.parent(self.grp_transform, self.grp_no_transform[0], self.grp_all_ribbon)

        # Match position with the module and tip joint
        mc.parentConstraint(base, ctrl_up.parent_control[0])
        mc.parentConstraint(tip, ctrl_down.parent_control[0])
        mc.delete(mc.parentConstraint(ctrl_up.parent_control[0], ctrl_down.parent_control[0], ctrl_mid.parent_control[0]))

        # PointConstraint the midCtrl between the top/end
        pt_mid_constraint = mc.pointConstraint(ctrl_down.control, ctrl_up.control, ctrl_mid.parent_control[0], mo=1)

        # Aiming the mid control to the module
        aim_mid_constraint = mc.aimConstraint(ctrl_up.control, ctrl_mid.parent_control[0], aim=(1, 0, 0), u=(0, 1, 0),
                                              wut='objectrotation',
                                              wu=(0, 1, 0),
                                              mo=1, wuo=self.grp_transform)

        # Match the orientation of group control to the middle control ribbon
        for obj in follicle_ctrl_grp:
            mc.delete(mc.orientConstraint(ctrl_mid.control, obj, mo=0))

        # If creating controller the module and tip
        if create_ctrl:
            # Create module controller
            base_ctrl = ct.Control(prefix=base + 'Base', groups_ctrl=['Zro', 'Offset'], ctrl_color='yellow',
                                   ctrl_size=ctrl_size * 1.2, shape=ct.CUBE)
            mc.delete(mc.parentConstraint(base, base_ctrl.parent_control[0]))
            mc.parent(base, base_ctrl.control)

            # Connected the rotation control up to rotation joint orientation
            mc.connectAttr((base_ctrl.control + '.rotate'), (sum_double_ctrl_up + '.input3D[2]'))

            # Create tip controller
            tip_ctrl = ct.Control(prefix=tip + 'Tip', groups_ctrl=['Zro', 'Offset'], ctrl_color='yellow',
                                  ctrl_size=ctrl_size * 1.2, shape=ct.CUBE)
            mc.delete(mc.parentConstraint(tip, tip_ctrl.parent_control[0]))
            mc.parent(tip, tip_ctrl.control)

            # Connected the rotation control down to rotation joint orientation
            mc.connectAttr((tip_ctrl.control + '.rotate'), (sum_double_ctrl_down + '.input3D[2]'))

            # Parent to all grp ribbon
            mc.parent(base_ctrl.parent_control[0], tip_ctrl.parent_control[0], self.grp_transform)

        # hide the visibility
        mc.hide(self.grp_no_transform, geo_plane_wire, self.grp_surfaces, self.grp_misc)

        # Lock unnecesarry key ribbon
        au.lock_hide_attr(['s'], ctrl_up.control)
        au.lock_hide_attr(['s'], ctrl_mid.control)
        au.lock_hide_attr(['s'], ctrl_down.control)

        # Lock some groups
        au.lock_attr(['t', 'r', 's', 'v'], self.grp_follicle_main[0])
        au.lock_hide_attr(['t', 'r', 's'], self.grp_no_transform[0])
        au.lock_hide_attr(['t', 'r', 's'], self.grp_jnt_cluster[0])
        au.lock_hide_attr(['t', 'r', 's', 'v'], self.grp_surfaces[0])
        au.lock_hide_attr(['t', 'r', 's', 'v'], self.grp_misc[0])
        au.lock_hide_attr(['t', 'r', 's', 'v'], geo_plane_wire[0])
        au.lock_hide_attr(['t', 'r', 's', 'v'], (mc.listConnections(wire_deformer[0] + '.baseWire[0]')[0]))

        if deformer:
            mc.hide(self.grp_deformers, self.grp_foll_volume)
            au.lock_hide_attr(['t', 'r', 's', 'v'], self.grp_foll_volume[0])
            au.lock_hide_attr(['t', 'r', 's', 'v'], self.grp_deformers[0])

        # Deleted the reference joint
        mc.delete(joint_create, position_uv_follicle, self.joint_reference_up, self.joint_reference_down)

        # Delete the module surface and group rotation driver
        mc.delete(tmp_plane, grp_joint_orient)

        # rename constraint
        au.constraint_rename([pt_mid_constraint[0], aim_mid_constraint[0], pac_jnt_up[0], pac_jnt_mid[0], pac_jnt_down[0]])

        # Clear all selection
        mc.select(cl=1)


    # GENERAL FUNCTION: ADD JOINTS FOR GUIDANCE OF FOLLICLES
    def item_follicle(self, items, obj_tansform, suffix):
        follicle = []
        follicle_shape = []
        for i in items:
            follicle = au.create_follicle_selection(i, obj_tansform, connect_follicle=['rotateConn', 'transConn'])[0]
            rename_follicle = mc.rename(follicle, '%s_%s' % (au.prefix_name(i), suffix))
            follicle.append(rename_follicle)
            fol_shape = mc.listRelatives(rename_follicle, s=1)[0]
            follicle_shape.append(fol_shape)

        return {'item': items,
                'follicle': follicle,
                'folShape': follicle_shape}

        # GENERAL FUNCTION: ADD ATTRIBUTE(S) ON MULTIPLE OBJECTS

    def add_attribute(self, objects=[], long_name='', nice_name='', separator=False, keyable=False, channel_box=False, **kwargs):
        # For each object
        for obj in objects:
            # For each attribute
            for x in range(0, len(long_name)):
                # See if a niceName was defined
                attr_nice = '' if not nice_name else nice_name[x]
                # If the attribute does not exists
                if not mc.attributeQuery(long_name[x], node=obj, exists=True):
                    # Add the attribute
                    mc.addAttr(obj, longName=long_name[x], niceName=attr_nice, **kwargs)
                    # If lock was set to True
                    mc.setAttr((obj + '.' + long_name[x]), k=keyable, e=1, cb=channel_box) if separator else mc.setAttr(
                        (obj + '.' + long_name[x]), k=keyable, e=1, cb=channel_box)

        # GENERAL FUNCTION: CREATE A NONLINEAR DEFORMER

    def nonlinear_deformer(self, objects=[], deformer_type=None, low_bound=-1, high_bound=1, translate=None, rotate=None,
                           name='nonLinear'):

        # If something went wrong or the type is not valid, raise exception
        if not objects or deformer_type not in ['bend', 'flare', 'sine', 'squash', 'twist', 'wave']:
            raise Exception("function: 'nonlinearDeformer' - Make sure you specified a mesh and a valid deformer")

        # Create and rename the deformer
        non_lin_deformer = mc.nonLinear(objects[0], type=deformer_type, lowBound=low_bound, highBound=high_bound)
        non_lin_deformer[0] = mc.rename(non_lin_deformer[0], (name + '_' + deformer_type + 'Def'))
        non_lin_deformer[1] = mc.rename(non_lin_deformer[1], (name + '_' + deformer_type + 'Handle'))

        # If translate was specified, set the translate
        if translate:
            mc.setAttr((non_lin_deformer[1] + '.translate'), translate[0], translate[1], translate[2])

        # If rotate was specified, set the rotate
        if rotate:
            mc.setAttr((non_lin_deformer[1] + '.rotate'), rotate[0], rotate[1], rotate[2])

        # Return the deformer
        return non_lin_deformer