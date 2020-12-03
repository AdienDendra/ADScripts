from __builtin__ import reload

import maya.cmds as mc

from rigging.library.utils import core as cr, controller as ct
from rigging.library.utils import transform as tr
from rigging.tools import AD_utils as au

reload(cr)
reload(tr)
reload(ct)
reload(au)

class CreateDetail:
    def __init__(self,
                 limb_bind_joint_parent,
                 detail_limb_deformer=False,
                 tip = None,
                 base = None,
                 parallel_axis = None,
                 tip_pos = None,
                 ctrl_tip =ct.SQUARE,
                 ctrl_mid = ct.SQUARE,
                 ctrl_base =ct.SQUARE,
                 ctrl_details = ct.CIRCLEPLUS,
                 ctrl_color=None,
                 prefix='prefix',
                 side=None,
                 scale=None,
                 volume_pos_min=None,
                 volume_pos_max=None,
                 number_joints=None,
                 game_bind_joint=None,
                 ):

        """
        :param detail_limb_deformer     : bool, create deformer setup on detail
        :param createCtrl   : bool, parameters for creating the control module and tip
        :param tip          : str, transform or joint as the tip of detail
        :param base         : str, transform or joint as the module of detail
        :param parallel_axis : str, two point parallel position direction whether on x or y or z axis
        :param tip_pos       : str, + if module seeing the tip with parallel with axis, - + if module seeing the tip with parallel opposite with axis
        :param ctrl_tip      : var, ctrl shape of tip
        :param ctrl_mid      : var, ctrl shape of middle
        :param ctrl_base     : var, ctrl shape of module
        :param ctrlTip      : var, ctrl shape of detail detail ctrl
        :param prefix       : str, prefix name for detail
        :param number_joints    : int, number of joint as well as the control of detail part
        """

        # Width plane variable (following the number of joints
        size = float(number_joints)

        # Tip point dictionary towards
        tip_point = {'+': [(size / 2.0 * -1) * scale, (size / 2.0) * scale],
                    '-': [(size / 2.0)*scale, (size / 2.0 * -1)*scale]}

        if tip_pos in tip_point.keys():
            self.pos       = (0,0,0)
            self.up_point   = tip_point[tip_pos][0]
            self.down_point = tip_point[tip_pos][1]
        else:
            raise mc.error('The string %s in tipPos argument is not found. Fill with + or -' % tip_pos)

        # Dictionary list
        tmp_plane_dic ={'x': [(0, 1, 0), size * scale, (1.0 / size), number_joints, 1],
                      'y': [(1,0,0), 1 * scale, size, 1, number_joints],
                      'z': [(0,1,0), 1 * scale, size, 1, number_joints]}

        direction = {'x': ['.rotateY', 90, '.translateZ'],
                     'y': ['.rotateZ', 90, '.translateZ'],
                     'z': ['.rotateX', 0, '.translateX']}

        if tip_pos== '-':
            rotation_defomer = {'x': (0, 0, -90),
                          'y': (0, 0, 0),
                          'z': (-90, 0, 90)}
        if tip_pos == '+':
            rotation_defomer = {'x': (0, 0, 90),
                          'y': (0, 0, 180),
                          'z': (-90, 0, 90)}

        vol_input_mdn = {'x': ['.translateX', '.input1Z', '.outputZ', '.scaleY', '.scaleZ'],
                       'y': ['.translateY','.input1Z', '.outputZ', '.scaleX', '.scaleZ'],
                       'z': ['.translateZ','.input1X', '.outputX','.scaleX', '.scaleZ']}

        follicle_vol ={'x': ('.parameterV', -1),
                      'y': ('.parameterU', -1),
                      'z': ('.parameterU', 1)}

        # Create the main groups
        self.grp_transform_zro   = mc.group(empty=True, name=(prefix + 'Transform' + side + '_grp'))
        self.grp_transform      = mc.group(empty=True, name=(prefix + 'TransformOffset' + side + '_grp'))
        self.grp_ctrl           = mc.duplicate(self.grp_transform, name=(prefix + 'Ctrl' + side + '_grp'))
        self.grp_jnt_cluster     = mc.duplicate(self.grp_transform, name=(prefix + 'JntCluster' + side + '_grp'))
        self.grp_no_transform    = mc.duplicate(self.grp_transform_zro, name=(prefix + 'NoTransformOffset' + side + '_grp'))
        self.grp_no_transform_zro = mc.duplicate(self.grp_transform_zro, name=(prefix + 'NoTransform' + side + '_grp'))
        self.grp_surface        = mc.duplicate(self.grp_transform_zro, name=(prefix + 'Surface' + side + '_grp'))
        self.grp_misc           = mc.duplicate(self.grp_transform_zro, name=(prefix + 'Misc' + side + '_grp'))
        self.grp_surfaces       = mc.duplicate(self.grp_transform_zro, name=(prefix + 'Surfaces' + side + '_grp'))
        self.grp_follicle_main       = mc.duplicate(self.grp_transform_zro, name=(prefix + 'FolliclesSkin' + side + '_grp'))
        self.grp_follicle_offset       = mc.duplicate(self.grp_transform_zro, name=(prefix + 'FolliclesSkinOffset' + side + '_grp'))

        mc.setAttr(self.grp_follicle_offset[0] + '.it', 0, l=1)
        mc.setAttr(self.grp_no_transform_zro[0] + '.it', 0, l=1)
        mc.setAttr(self.grp_transform_zro + '.it', 0, l=1)

        # Create a NURBS-plane to use as a module
        tmp_plane = mc.nurbsPlane(axis=tmp_plane_dic[parallel_axis][0], width=tmp_plane_dic[parallel_axis][1],
                                  lengthRatio=tmp_plane_dic[parallel_axis][2], u=tmp_plane_dic[parallel_axis][3],
                                  v=tmp_plane_dic[parallel_axis][4], degree=3, ch=0)[0]

        # Create the NURBS-planes to use in the setup
        geo_plane       = mc.duplicate(tmp_plane, name=(prefix + side+'_geo'))
        geo_plane_wire   = mc.duplicate(tmp_plane, name=(prefix + 'WireDef' + side + '_geo'))
        geo_plane_orient = mc.duplicate(tmp_plane, name=(prefix + 'OrientDef' + side + '_geo'))

        # Create Joint reference
        mc.select(cl=1)
        create_joint = mc.joint(radius=scale / 5)

        # Duplicate joint from reference for skinning to the wire curve
        self.joint_up   = mc.duplicate(create_joint, n=prefix + 'Up' + side + '_jnt')
        self.joint_mid  = mc.duplicate(create_joint, n=prefix + 'Mid' + side + '_jnt')
        self.joint_down = mc.duplicate(create_joint, n=prefix + 'Down' + side + '_jnt')

        # Set the position for joints
        mc.setAttr((self.joint_up[0] + '.translate'), self.up_point, self.pos[1], self.pos[2])
        mc.setAttr((self.joint_mid[0] + '.translate'), self.pos[0], self.pos[1], self.pos[2])
        mc.setAttr((self.joint_down[0] + '.translate'), self.down_point, self.pos[1], self.pos[2])

        # Grouping the joints to have rotation according to parallel axis
        grp_joint_orient = mc.group(self.joint_up[0], self.joint_mid[0], self.joint_down[0])

        # Set the rotation group joints
        if parallel_axis == 'z':
            mc.setAttr((grp_joint_orient + '.rotate'), 0, -90, 0)
        if parallel_axis == 'y':
            mc.setAttr((grp_joint_orient + '.rotate'), 0, 0, 90)

        # Unparent from the group
        mc.parent(self.joint_up[0], self.joint_mid[0], self.joint_down[0], w=1)

        # Create Group for joints wire curve  listparent, object, matchPos, prefix, suffix, side=''
        self.joint_up_parent = tr.create_parent_transform(parent_list=['Zro'], object=self.joint_up[0],
                                                          match_position=self.joint_up[0], prefix=prefix + 'Up',
                                                          suffix='_jnt', side=side)

        self.joint_mid_parent = tr.create_parent_transform(parent_list=['Zro'], object=self.joint_mid[0],
                                                           match_position=self.joint_mid[0], prefix=prefix + 'Mid',
                                                           suffix='_jnt', side=side)

        self.joint_down_parent = tr.create_parent_transform(parent_list=['Zro'], object=self.joint_down[0],
                                                            match_position=self.joint_down[0], prefix=prefix + 'Down',
                                                            suffix='_jnt', side=side)

        # Create the controllers
        self.ctrl_up = ct.Control(match_obj_first_position=self.joint_up_parent[0], prefix=prefix + 'Up', side=side,
                                  groups_ctrl=['Zro', 'Offset', 'Twist', 'Rotation'],
                                  ctrl_size=scale * 0.7, ctrl_color=ctrl_color, shape=ctrl_tip)
        self.ctrl_mid = ct.Control(match_obj_first_position=self.joint_mid_parent[0], prefix=prefix + 'Mid', side=side,
                                   groups_ctrl=['Zro', 'Aim'],
                                   ctrl_color='blue', ctrl_size=scale * 0.7, shape=ctrl_mid)
        self.ctrl_down = ct.Control(match_obj_first_position=self.joint_down_parent[0], prefix=prefix + 'Down', side=side,
                                    groups_ctrl=['Zro', 'Offset', 'Twist'],
                                    ctrl_size=scale * 0.7, ctrl_color=ctrl_color, shape=ctrl_base)

        # control up
        self.up_ctrl_aim_group = mc.spaceLocator(n=prefix + 'UpAim' + side + '_loc')[0]
        mc.delete(mc.parentConstraint(self.ctrl_up.control, self.up_ctrl_aim_group))
        mc.parent(self.up_ctrl_aim_group, self.ctrl_up.control)
        duplicate_up_ctrl_aim_group = mc.duplicate(self.up_ctrl_aim_group)
        self.up_ctrl_world_offset_group = mc.rename(duplicate_up_ctrl_aim_group, (prefix + 'UpAimWorld' + side + '_loc'))
        mc.setAttr(self.up_ctrl_world_offset_group + '.translateZ', -1)

        mc.hide(self.up_ctrl_aim_group, self.up_ctrl_world_offset_group)

        # control mid
        self.mid_ctrl_world_offset_group = mc.group(empty=True, n=prefix + 'MidAimWorld' + side + '_grp')
        mc.delete(mc.parentConstraint(self.ctrl_mid.parent_control[0], self.mid_ctrl_world_offset_group))
        mc.parent(self.mid_ctrl_world_offset_group, self.ctrl_mid.parent_control[0])
        mc.setAttr(self.mid_ctrl_world_offset_group + '.translateZ', -1)

        # control down
        self.down_ctrl_aim_group = mc.spaceLocator(n=prefix + 'DownAim' + side + '_loc')[0]
        mc.delete(mc.parentConstraint(self.ctrl_down.control, self.down_ctrl_aim_group))
        mc.parent(self.down_ctrl_aim_group, self.ctrl_down.control)
        duplicate_down_ctrl_aim_group = mc.duplicate(self.down_ctrl_aim_group)
        self.down_ctrl_world_offset_group = mc.rename(duplicate_down_ctrl_aim_group, (prefix + 'DownAimWorld' + side + '_loc'))
        mc.setAttr(self.down_ctrl_world_offset_group + '.translateZ', -1)

        mc.hide(self.down_ctrl_aim_group, self.down_ctrl_world_offset_group)

        # Get part joint position
        self.joint_reference_up = mc.duplicate(self.joint_up[0], n=prefix + 'Up' + side + '_jnt')
        self.joint_reference_down = mc.duplicate(self.joint_down[0], n=prefix + 'Down' + side + '_jnt')

        # Unparent joint duplicate
        mc.parent(self.joint_reference_up, self.joint_reference_down, w=True)

        # Create joint on evenly position
        position_uv_fol = cr.split_evenly(self.joint_reference_up, self.joint_reference_down, prefix, side=side,
                                          split=number_joints, base_tip=True)

        # Create deformers: Wire deformer
        deform_crv = mc.curve(p=[(self.down_point, 0, 0), (0, 0, 0), (self.up_point, 0, 0)], degree=2)
        deform_crv = mc.rename(deform_crv, (prefix + 'Wire' + side + '_crv'))

        # Set orient curve
        mc.delete(mc.orientConstraint(grp_joint_orient, deform_crv))
        wire_deformer = mc.wire(geo_plane_wire, dds=(0, 100 * scale), wire=deform_crv)
        wire_deformer[0] = mc.rename(wire_deformer[0], (au.prefix_name(geo_plane_wire[0]) + '_wireNode'))

        # Skining joints to curve
        mc.skinCluster([self.joint_up[0], self.joint_mid[0], self.joint_down[0]], deform_crv,
                       n='wireSkinCluster', tsb=True, bm=0, sm=0, nw=1, mi=1)

        # Point constraining the the controller transform to the joint wire curve
        ctrl_up_parentConstraint = mc.parentConstraint(self.ctrl_up.control, self.joint_up_parent[0])
        ctrl_mid_parentConstraint = mc.parentConstraint(self.ctrl_mid.control, self.joint_mid_parent[0])
        ctrl_down_parentConstraint = mc.parentConstraint(self.ctrl_down.control, self.joint_down_parent[0])

        # Create deformers: Blendshape
        deformer_blendshape = mc.blendShape(geo_plane_wire[0], geo_plane[0], name=(prefix + side + '_bsn'), weight=[(0, 1)])

        # Create follicles: The main-surface and the volume-surface
        follicle_s = self.item_follicle(position_uv_fol, geo_plane, 'fol')

        # Scaling the follicle with decompose matrix
        decompose_matrix_node = mc.createNode('decomposeMatrix', n=prefix + 'DtlScaleFol' + side + '_dmtx')
        mc.connectAttr(self.grp_transform + '.worldMatrix[0]', decompose_matrix_node + '.inputMatrix')

        # Grouping listing of the follicle parent group
        follicle_ctrl_grp        = []
        self.follicle_set_grp = []
        self.follicle_grp_twist  = []
        self.follicle_grp_offset = []
        self.follicle_ctrl      = []
        self.follicle_joint_limb = []
        # self.joint_skin         = []

        for i, fol_s in enumerate(follicle_s['follicle']):
            mc.connectAttr(decompose_matrix_node + '.outputScale', fol_s + '.scale')

            # Listing the shape of follicles
            follicle_listRelatives = mc.listRelatives(fol_s, s=1)[0]
            mc.setAttr(follicle_listRelatives + '.visibility', 0)

            # Parenting the follicles to grp follicle
            mc.parent(fol_s, self.grp_follicle_offset)

            # Create group offset for follilce
            follicle_grp_set = mc.group(empty=True, n='%s%02d%s_%s' % (prefix, (i + 1), side, 'setGrp'))
            mc.delete(mc.parentConstraint(fol_s, follicle_grp_set))

            # append the set grp
            self.follicle_set_grp.append(follicle_grp_set)

            # Create offset group follicle
            follicle_grp_set = mc.parent(follicle_grp_set, fol_s)

            # Create a joint, controller and a group for the current skin-follicle
            mc.select(clear=True)

            # Create joint for follicle
            follicle_joint = mc.joint(name='%s_%s' % (au.prefix_name(fol_s), 'skn'), radius=0.1*scale)
            self.follicle_joint_limb.append(follicle_joint)
            # mc.hide(follicle_joint)

            # if game joint hierarchy
            if game_bind_joint:
                game_joint = mc.joint(name='%s_%s' % (au.prefix_name(fol_s), 'bind'), radius=0.1 * scale)
                constraining = au.parent_scale_constraint(follicle_joint, game_joint)
                mc.parent(game_joint, limb_bind_joint_parent)
                mc.parent(constraining[0], constraining[1], 'additional_grp')
                mc.setAttr(game_joint+'.segmentScaleCompensate', 0)

            # Create control for joint in follicle
            follicle_ctrl = ct.Control(prefix=prefix + ('%02d' % (i + 1)), groups_ctrl=['Zro', 'Twist', 'Offset']
                                       , side=side, ctrl_color=ctrl_color, ctrl_size=scale * 0.65, shape=ctrl_details)

            # append grp and controller follicle
            follicle_ctrl_grp.append(follicle_ctrl.parent_control[0])
            self.follicle_grp_twist.append(follicle_ctrl.parent_control[1])
            self.follicle_grp_offset.append(follicle_ctrl.parent_control[2])
            self.follicle_ctrl.append(follicle_ctrl.control)

            # Parent joint to controller
            mc.parent(follicle_joint, follicle_ctrl.control)

            # Positioning skin-follicle control
            mc.delete(mc.parentConstraint(self.ctrl_mid.control, follicle_ctrl.parent_control[0]))
            mc.delete(mc.pointConstraint(follicle_grp_set, follicle_ctrl.parent_control[0]))

            # Parent controller to group offset follicle
            mc.parent(follicle_ctrl.parent_control[0], follicle_grp_set)

            # hide joint
            mc.setAttr(follicle_joint + '.visibility', 0)

            # # SKINNING JOINT
            # skinning_joint = mc.joint(name='%s_%s' % (au.prefix_name(fol_s), 'skn'), radius=0.1 * scale)
            # self.joint_skin.append(skinning_joint)
            #
            # # COSNTRAINT SKIN
            # au.parent_scale_constraint(follicle_joint, skinning_joint)

    # ==================================================================================================================
    #                                               TWIST DEFORM
    # ==================================================================================================================

        self.grp_deformers = mc.duplicate(self.grp_transform_zro, name=(prefix + 'Deformer' + side + '_grp'))
        geo_plane_twist = mc.duplicate(tmp_plane, name=(prefix + 'TwistDef' + side + '_geo'))


        # Add attributes: Twist/Roll attributes
        self.add_attribute(objects=[self.ctrl_down.control, self.ctrl_mid.control, self.ctrl_up.control],
                           long_name=['twistSep'], nice_name=[' '], at="enum", en='Twist', channel_box=True)

        self.add_attribute(objects=[self.ctrl_down.control, self.ctrl_up.control], long_name=['twist'], at="float", keyable=True)
        self.add_attribute(objects=[self.ctrl_down.control, self.ctrl_up.control], long_name=['twistOffset'], at="float",
                           keyable=True)
        self.add_attribute(objects=[self.ctrl_down.control, self.ctrl_up.control], long_name=['affectToMid'], at="float",
                           min=0,
                           max=10, dv=10, keyable=True)

        # Add attributes: Twist/Roll attributes parent
        self.add_attribute(objects=[self.ctrl_down.parent_control[2], self.ctrl_up.parent_control[2]], long_name=['twist'],
                           at="float", keyable=True)
        self.add_attribute(objects=[self.ctrl_down.parent_control[2], self.ctrl_up.parent_control[2]],
                           long_name=['twistOffset'], at="float", keyable=True)
        self.add_attribute(objects=[self.ctrl_down.parent_control[2], self.ctrl_up.parent_control[2]],
                           long_name=['affectToMid'], at="float", keyable=True)

        # connected twist controller to parent controller
        mc.connectAttr(self.ctrl_up.control + '.twist', self.ctrl_up.parent_control[2] + '.twist')
        mc.connectAttr(self.ctrl_up.control + '.twistOffset', self.ctrl_up.parent_control[2] + '.twistOffset')
        mc.connectAttr(self.ctrl_up.control + '.affectToMid', self.ctrl_up.parent_control[2] + '.affectToMid')

        mc.connectAttr(self.ctrl_down.control + '.twist', self.ctrl_down.parent_control[2] + '.twist')
        mc.connectAttr(self.ctrl_down.control + '.twistOffset', self.ctrl_down.parent_control[2] + '.twistOffset')
        mc.connectAttr(self.ctrl_down.control + '.affectToMid', self.ctrl_down.parent_control[2] + '.affectToMid')

        # add attribute twist mid controller
        self.add_attribute(objects=[self.ctrl_mid.control], long_name=['roll'], at="float", keyable=True)
        self.add_attribute(objects=[self.ctrl_mid.control], long_name=['rollOffset'], at="float", keyable=True)

        # Create deformers: Twist deformer, Sine deformer, Squash deformer
        # Set them rotation  according on point parallelFaceAxis position
        self.twist_deformer = self.nonlinear_deformer(objects=[geo_plane_twist[0]], deformer_type='twist',
                                                      name=au.prefix_name(geo_plane_twist[0]), low_bound=-1,
                                                      high_bound=1, rotate=rotation_defomer[parallel_axis])

        # Twist deformer: Sum the twist and the roll
        self.sum_top_pma = mc.shadingNode('plusMinusAverage', asUtility=1, name=(prefix + 'TwistUpSum' + side + '_pma'))
        mc.connectAttr((self.ctrl_down.parent_control[2] + '.twist'), (self.sum_top_pma + '.input1D[0]'))
        mc.connectAttr((self.ctrl_down.parent_control[2] + '.twistOffset'), (self.sum_top_pma + '.input1D[1]'))
        mc.connectAttr((self.ctrl_mid.control + '.roll'), (self.sum_top_pma + '.input1D[2]'))
        mc.connectAttr((self.ctrl_mid.control + '.rollOffset'), (self.sum_top_pma + '.input1D[3]'))
        mc.connectAttr((self.sum_top_pma + '.output1D'), (self.twist_deformer[0] + '.startAngle'))

        self.sum_end_pma = mc.shadingNode('plusMinusAverage', asUtility=1, name=(prefix + 'TwistDownSum' + side + '_pma'))
        mc.connectAttr((self.ctrl_up.parent_control[2] + '.twist'), (self.sum_end_pma + '.input1D[0]'))
        mc.connectAttr((self.ctrl_up.parent_control[2] + '.twistOffset'), (self.sum_end_pma + '.input1D[1]'))
        mc.connectAttr((self.ctrl_mid.control + '.roll'), (self.sum_end_pma + '.input1D[2]'))
        mc.connectAttr((self.ctrl_mid.control + '.rollOffset'), (self.sum_end_pma + '.input1D[3]'))
        mc.connectAttr((self.sum_end_pma + '.output1D'), (self.twist_deformer[0] + '.endAngle'))

        # Twist deformer: Set up the affect of the deformer
        top_affect_mdl = mc.shadingNode('multDoubleLinear', asUtility=1, name=(prefix + 'TwistUpAffect' + side + '_mdl'))
        mc.setAttr((top_affect_mdl + '.input1'), -0.1)
        mc.connectAttr((self.ctrl_down.parent_control[2] + '.affectToMid'), (top_affect_mdl + '.input2'))
        mc.connectAttr((top_affect_mdl + '.output'), (self.twist_deformer[0] + '.lowBound'))

        end_affect_mdl = mc.shadingNode('multDoubleLinear', asUtility=1, name=(prefix + 'TwistDownAffect' + side + '_mdl'))
        mc.setAttr((end_affect_mdl + '.input1'), 0.1)
        mc.connectAttr((self.ctrl_up.parent_control[2] + '.affectToMid'), (end_affect_mdl + '.input2'))
        mc.connectAttr((end_affect_mdl + '.output'), (self.twist_deformer[0] + '.highBound'))

        # create and set blendshape
        mc.blendShape(deformer_blendshape, e=1, t=(geo_plane[0], 1, geo_plane_twist[0], 1.0))

        mc.blendShape(deformer_blendshape, e=True, w=[(1, 1.0)])

    # ==================================================================================================================
    #                                               IF DEFORM TRUE
    # ==================================================================================================================
        if detail_limb_deformer:
            # self.grpDeformers  = mc.duplicate(self.grpTransformZro, name=(prefix + 'Deformer' + side + '_grp'))
            self.grp_follicle_volume = mc.duplicate(self.grp_transform_zro, name=(prefix + 'FolliclesVolume' + side + '_grp'))

            geo_plane_volume = mc.duplicate(tmp_plane, name=(prefix + 'Volume' + side + '_geo'))
            # geoPlaneTwist  = mc.duplicate(tmpPlane, name=(prefix + 'TwistDef'+side +'_geo'))
            geo_plane_sine   = mc.duplicate(tmp_plane, name=(prefix + 'SineDef' + side + '_geo'))

            # Offset the volume-plane
            mc.setAttr((geo_plane_volume[0] + direction[parallel_axis][2]), -0.5 * scale)

            # Add attributes: Volume attributes
            self.add_attribute(objects=[self.ctrl_mid.control], long_name=['volumeSep'], nice_name=[' '], at="enum",
                               en='Volume', channel_box=True)

            self.add_attribute(objects=[self.ctrl_mid.control], long_name=['volume'], at="float", min=-1, max=1, keyable=True)
            self.add_attribute(objects=[self.ctrl_mid.control], long_name=['volumeMultiplier'], at="float", min=1, dv=3, keyable=True)
            self.add_attribute(objects=[self.ctrl_mid.control], long_name=['startDropoff'], at="float", min=0, max=1, dv=1,
                               keyable=True)
            self.add_attribute(objects=[self.ctrl_mid.control], long_name=['endDropoff'], at="float", min=0, max=1, dv=1,
                               keyable=True)
            self.add_attribute(objects=[self.ctrl_mid.control], long_name=['volumeScale'], at="float", min=self.up_point * 0.9,
                               max=self.down_point * 2, keyable=True)
            self.add_attribute(objects=[self.ctrl_mid.control], long_name=['volumePosition'], min=volume_pos_min * self.up_point,
                               max=volume_pos_max * self.down_point, at="float", keyable=True)

            # Add attributes: Sine attributes
            self.add_attribute(objects=[self.ctrl_mid.control], long_name=['sineSep'], nice_name=[' '], attributeType='enum',
                               en="Sine:", channel_box=True)

            self.add_attribute(objects=[self.ctrl_mid.control], long_name=['amplitude'], attributeType="float", keyable=True)
            self.add_attribute(objects=[self.ctrl_mid.control], long_name=['wide'], attributeType="float", keyable=True)
            self.add_attribute(objects=[self.ctrl_mid.control], long_name=['sineRotate'], attributeType="float", keyable=True)
            self.add_attribute(objects=[self.ctrl_mid.control], long_name=['offset'], attributeType="float", keyable=True)
            self.add_attribute(objects=[self.ctrl_mid.control], long_name=['twist'], attributeType="float", keyable=True)
            self.add_attribute(objects=[self.ctrl_mid.control], long_name=['sineLength'], min=0.1, dv=2, attributeType="float",
                               keyable=True)

            # Create deformers: Twist deformer, Sine deformer, Squash deformer
            # Set them rotation  according on point parallelFaceAxis position
            self.sine_deformer   = self.nonlinear_deformer(objects=[geo_plane_sine[0]], deformer_type='sine',
                                                           name=au.prefix_name(geo_plane_sine[0]), low_bound=-1,
                                                           high_bound=1, rotate=rotation_defomer[parallel_axis])

            self.squash_deformer = self.nonlinear_deformer(objects=[geo_plane_volume[0]], deformer_type='squash',
                                                           name=au.prefix_name(geo_plane_volume[0]), low_bound=-1,
                                                           high_bound=1, rotate=rotation_defomer[parallel_axis])

            mc.setAttr((self.sine_deformer[0] + '.dropoff'), 1)

        # Squash deformer: Set up the connections for the volume control
            self.volume_reverse_adl = mc.createNode('addDoubleLinear',
                                                    n='%s%s%s_adl' % (prefix, 'CombineVolumeReverse', side))
            mc.connectAttr((self.ctrl_mid.control + '.volume'), (self.volume_reverse_adl + '.input2'))
            volume_reverse_mdl = mc.shadingNode('multDoubleLinear', asUtility=1, name=(prefix + 'VolumeReverse' + side + '_mdl'))
            mc.setAttr((volume_reverse_mdl + '.input1'), -1)
            mc.connectAttr((self.volume_reverse_adl + '.output'), (volume_reverse_mdl + '.input2'))
            mc.connectAttr((volume_reverse_mdl + '.output'), (self.squash_deformer[0] + '.factor'))
            mc.connectAttr((self.ctrl_mid.control + '.startDropoff'), (self.squash_deformer[0] + '.startSmoothness'))
            mc.connectAttr((self.ctrl_mid.control + '.endDropoff'), (self.squash_deformer[0] + '.endSmoothness'))

            # Set the translate squash deformer according the point parallelFaceAxis position
            self.combine_vol_position_adl = mc.createNode('addDoubleLinear',
                                                          n='%s%s%s_adl' % (prefix, 'CombineVolumePos', side))
            mc.connectAttr((self.ctrl_mid.control + '.volumePosition'), (self.combine_vol_position_adl + '.input2'))
            mc.connectAttr((self.combine_vol_position_adl + '.output'), (self.squash_deformer[1] + vol_input_mdn[parallel_axis][0]))

        # Squash deformer: Set up the volume scaling
            sum_scale_pma = mc.shadingNode('plusMinusAverage', asUtility=1, name=(prefix + 'VolumeScaleSum' + side + '_pma'))
            mc.setAttr((sum_scale_pma + '.input1D[0]'), self.down_point)
            mc.connectAttr((self.ctrl_mid.control + '.volumeScale'), (sum_scale_pma + '.input1D[1]'))
            mc.connectAttr((sum_scale_pma + '.output1D'), (self.squash_deformer[1] + '.scaleY'))

        # Sine deformer: Set up the connections for the sine

            # combine sine amplitude
            self.combine_sine_amplitude = mc.createNode('addDoubleLinear', n=(prefix + 'CombineSineAmplitude' + side + '_adl'))
            mc.connectAttr(self.ctrl_mid.control + '.amplitude', self.combine_sine_amplitude + '.input2')
            mc.connectAttr((self.combine_sine_amplitude + '.output'), (self.sine_deformer[0] + '.amplitude'))

            # combine sine offset
            self.combine_sine_offset = mc.createNode('addDoubleLinear', n=(prefix + 'CombineSineOffset' + side + '_adl'))
            mc.connectAttr(self.ctrl_mid.control + '.offset', self.combine_sine_offset + '.input2')
            mc.connectAttr((self.combine_sine_offset + '.output'), (self.sine_deformer[0] + '.offset'))

            # combine sine wide
            self.combine_sine_wide = mc.createNode('addDoubleLinear', n=(prefix + 'CombineSineWide' + side + '_adl'))
            mc.connectAttr(self.ctrl_mid.control + '.wide', self.combine_sine_wide + '.input2')
            sine_wide_node = mc.createNode('addDoubleLinear', n=(prefix + 'AdjustSineWide' + side + '_adl'))
            mc.setAttr(sine_wide_node + '.input1', 2.5)
            mc.connectAttr(self.combine_sine_wide + '.output', sine_wide_node + '.input2')
            mc.connectAttr(sine_wide_node + '.output', self.sine_deformer[1] + '.scaleY')

            # Sine Exception for z parallel axis
            if parallel_axis == 'z':
                # combine sine rotation
                self.combine_sine_rotate = mc.createNode('addDoubleLinear', n=(prefix + 'CombineSineRotate' + side + '_adl'))
                mc.connectAttr(self.ctrl_mid.control + '.sineRotate', self.combine_sine_rotate + '.input2')

                # sine rotation : set the sine rotation
                mc.connectAttr(self.combine_sine_rotate + '.output', self.sine_deformer[1] + '.rotateY')

                # combine sine twist
                self.combine_sine_twist = mc.createNode('addDoubleLinear', n=(prefix + 'CombineSineTwist' + side + '_adl'))
                mc.connectAttr(self.ctrl_mid.control + '.twist', self.combine_sine_twist + '.input2')

                sine_twist_node = mc.createNode('addDoubleLinear', n=(prefix + 'AdjustSineTwistRotZ' + side + '_adl'))
                mc.setAttr(sine_twist_node + '.input1', 90)
                mc.connectAttr(self.combine_sine_twist + '.output', sine_twist_node + '.input2')
                mc.connectAttr(sine_twist_node + '.output', self.sine_deformer[1] + '.rotateZ')

            if parallel_axis == 'x':
                # combine sine rotation
                self.combine_sine_rotate = mc.createNode('addDoubleLinear',
                                                         n=(prefix + 'CombineSineRotate' + side + '_adl'))
                mc.connectAttr(self.ctrl_mid.control + '.sineRotate', self.combine_sine_rotate + '.input2')

                # sine rotation : set the sine rotation
                sine_rotate_node = mc.createNode('addDoubleLinear', n=(prefix + 'AdjustSineRotate' + side + '_adl'))
                mc.setAttr(sine_rotate_node + '.input1', 90)
                mc.connectAttr(self.combine_sine_rotate + '.output', sine_rotate_node + '.input2')
                mc.connectAttr(sine_rotate_node + '.output', self.sine_deformer[1] + '.rotateZ')

                # sine twist
                self.combine_sine_twist = mc.createNode('addDoubleLinear',
                                                        n=(prefix + 'CombineSineTwist' + side + '_adl'))

                mc.connectAttr(self.ctrl_mid.control + '.twist', self.combine_sine_twist + '.input2')
                mc.connectAttr(self.combine_sine_twist + '.output', self.sine_deformer[1] + '.rotateY')

            if parallel_axis == 'y':
                # combine sine rotation
                self.combine_sine_rotate = mc.createNode('addDoubleLinear',
                                                         n=(prefix + 'CombineSineRotate' + side + '_adl'))
                mc.connectAttr(self.ctrl_mid.control + '.sineRotate', self.combine_sine_rotate + '.input2')

                # sine rotation : set the sine rotation
                sine_rotate_node = mc.createNode('addDoubleLinear', n=(prefix + 'AdjustSineRotate' + side + '_adl'))
                mc.setAttr(sine_rotate_node + '.input1', 0)
                mc.connectAttr(self.combine_sine_rotate + '.output', sine_rotate_node + '.input2')
                mc.connectAttr(sine_rotate_node + '.output', self.sine_deformer[1] + '.rotateZ')

                # sine twist
                self.combine_sine_twist = mc.createNode('addDoubleLinear',
                                                        n=(prefix + 'CombineSineTwist' + side + '_adl'))

                mc.connectAttr(self.ctrl_mid.control + '.twist', self.combine_sine_twist + '.input2')
                mc.connectAttr(self.combine_sine_twist + '.output', self.sine_deformer[1] + '.rotateY')

            # sine length combine
            self.combine_sine_length = mc.createNode('multDoubleLinear',
                                                     n=(prefix + 'CombineSineLength' + side + '_mdl'))
            mc.connectAttr(self.ctrl_mid.control + '.sineLength', self.combine_sine_length + '.input2')
            mc.connectAttr(self.combine_sine_length + '.output', self.sine_deformer[0] + '.wavelength')

        # Create deformers: Blendshape
        #     mc.blendShape(dtlBlendshp, e=1, t=(geoPlane[0], 1, geoPlaneTwist[0], 1.0))
            mc.blendShape(deformer_blendshape, e=1, t=(geo_plane[0], 2, geo_plane_sine[0], 1.0))

            mc.blendShape(deformer_blendshape, e=True, w=[(2, 1.0)])

            # Create follicles: The main-surface and the volume-surface
            follicle_v = self.item_follicle(position_uv_fol, geo_plane_volume, 'Volumefol')

            # Set the follicle U and V parameter
            for obj in follicle_v['follicle']:
                mc.setAttr(obj + follicle_vol[parallel_axis][0], follicle_vol[parallel_axis][1])

            # list node combine multiply
            self.combine_mult_all = []

            # Looping the follicle S and follicle V
            for fol_v, fol_grp_offset in zip(follicle_v['follicle'], self.follicle_set_grp):
                # combine multiplier
                combine_mult = mc.shadingNode('multDoubleLinear', asUtility=1,
                                              name=au.prefix_name(fol_v)[:-3] + 'CombineMultiplier' + side + '_mdl')
                mc.connectAttr((self.ctrl_mid.control + '.volumeMultiplier'), combine_mult + '.input1')

                # make list combine multiplier
                self.combine_mult_all.append(combine_mult)

                # Make the connections for the volume according on point parallelFaceAxis position
                multiplier_volume = mc.shadingNode('multiplyDivide', asUtility=1,
                                                   name=au.prefix_name(fol_v)[:-3] + 'Multiplier' + side + '_mdn')
                mc.connectAttr((combine_mult + '.output'), vol_input_mdn[parallel_axis][1])
                mc.connectAttr((fol_v + '.translate'), (multiplier_volume + '.input2'))

                sum_volume_pma = mc.shadingNode('plusMinusAverage', asUtility=1,
                                                name=au.prefix_name(fol_v)[:-3] + 'VolumeSum' + side + '_pma')
                mc.connectAttr((multiplier_volume + vol_input_mdn[parallel_axis][2]), (sum_volume_pma + '.input1D[0]'))
                mc.setAttr((sum_volume_pma + '.input1D[1]'), 1)
                mc.connectAttr((sum_volume_pma + '.output1D'), (fol_grp_offset + vol_input_mdn[parallel_axis][3]))
                mc.connectAttr((sum_volume_pma + '.output1D'), (fol_grp_offset + vol_input_mdn[parallel_axis][4]))

            # Cleanup: Hierarchy
            mc.parent(self.sine_deformer[1], self.squash_deformer[1], self.grp_deformers)
            mc.parent(geo_plane_sine[0], geo_plane_volume[0], self.grp_surfaces)
            mc.parent(follicle_v['follicle'], self.grp_follicle_volume)
            mc.parent(self.grp_follicle_volume[0], self.grp_no_transform)

            # hide grp
            mc.hide(self.grp_no_transform_zro)

            # lock and hide grp
            au.lock_hide_attr(['t', 'r', 's', 'v'], self.grp_follicle_volume[0])

    # ==================================================================================================================
    #                                 END DEFORM | CLEANING UP THE ATTRIBUTES
    # ==================================================================================================================
        # Add attributes: Extra attributes
        self.add_attribute(objects=[self.ctrl_mid.control], long_name=['extraSep'], nice_name=[' '], at="enum", en='Extra',
                           channel_box=True)
        self.add_attribute(objects=[self.ctrl_mid.control], long_name=['detailCtrlVis'], at="long", min=0, max=1, dv=0,
                           channel_box=True)

        # connect the visibility-switch for the controller
        mc.connectAttr((self.ctrl_mid.control + '.detailCtrlVis'),
                       (self.grp_follicle_offset[0] + '.visibility'))

        # Cleanup: Hierarchy
        mc.delete(mc.parentConstraint(base, tip, self.grp_transform))
        mc.delete(mc.orientConstraint(tmp_plane, self.grp_transform_zro))
        mc.delete(mc.parentConstraint(base, tip, self.grp_transform_zro))

        mc.parent(geo_plane_orient[0], geo_plane_twist[0], self.grp_surfaces)
        mc.parent(self.twist_deformer[1], self.grp_deformers)

        mc.parent(self.joint_up_parent[0], self.joint_mid_parent[0], self.joint_down_parent[0], self.grp_jnt_cluster)
        mc.parent(self.ctrl_down.parent_control[0], self.ctrl_mid.parent_control[0], self.ctrl_up.parent_control[0],
                  self.grp_ctrl)
        mc.parent(geo_plane[0], geo_plane_wire[0], (mc.listConnections(wire_deformer[0] + '.baseWire[0]')[0]), self.grp_surface)
        mc.parent(deform_crv, self.grp_misc)
        mc.parent(self.grp_jnt_cluster, self.grp_surfaces[0], self.grp_deformers[0], self.grp_misc[0], self.grp_no_transform)
        mc.parent(self.grp_ctrl[0], self.grp_surface[0], self.grp_follicle_main[0], self.grp_transform)
        mc.parent(self.grp_follicle_offset[0], self.grp_follicle_main[0])
        mc.parent(self.grp_transform, self.grp_transform_zro)
        mc.parent(self.grp_no_transform[0], self.grp_no_transform_zro[0])

        # Match position with the module and tip joint
        mc.delete(mc.parentConstraint(base, self.ctrl_up.parent_control[0]))
        mc.delete(mc.pointConstraint(tip, self.ctrl_down.parent_control[0]))
        mc.delete(mc.orientConstraint(base, self.ctrl_down.parent_control[0]))
        mc.delete(mc.parentConstraint(tip, self.ctrl_down.parent_control[0], mo=1))
        mc.delete(mc.parentConstraint(self.ctrl_up.parent_control[0], self.ctrl_down.parent_control[0],
                                      self.ctrl_mid.parent_control[0]))

        # aim contraint for ctrl
        ctrl_down_aim_constraint = mc.aimConstraint(self.ctrl_up.control, self.down_ctrl_aim_group, mo=1, w=1, aim=(0, -1, 0),
                                                    u=(0, 0, -1),
                                                    wut='objectrotation', wu=(0, 0, -1), wuo=self.down_ctrl_world_offset_group)

        ctrl_up_aim_constraint = mc.aimConstraint(self.ctrl_down.control, self.up_ctrl_aim_group, mo=1, w=1, aim=(0, 1, 0),
                                                  u=(0, 0, -1),
                                                  wut='objectrotation', wu=(0, 0, -1), wuo=self.up_ctrl_world_offset_group)

        ctrl_mid_aim_constraint = mc.aimConstraint(self.ctrl_down.control, self.ctrl_mid.parent_control[1], mo=1, w=1,
                                                   aim=(0, -1, 0), u=(0, 0, -1), wut='objectrotation', wu=(0, 0, -1),
                                                   wuo=self.mid_ctrl_world_offset_group)

        # point constraint to mid
        point_to_mid_constraint = mc.pointConstraint(self.ctrl_up.control, self.ctrl_down.control, self.ctrl_mid.parent_control[0],
                                                     mo=1)

        # parent constraint to mid world
        parent_to_mid_constraint = mc.parentConstraint(self.ctrl_up.control, self.ctrl_down.control, self.mid_ctrl_world_offset_group, mo=1)

        # Match the orientation of group control to the middle control detail
        for obj in follicle_ctrl_grp:
            mc.delete(mc.orientConstraint(self.ctrl_mid.control, obj, mo=0))

        # hide the visibility
        mc.hide(self.grp_no_transform_zro, self.grp_no_transform, self.grp_deformers, self.grp_jnt_cluster, geo_plane_wire,
                self.grp_surfaces, self.grp_surface, self.grp_misc)

        # Lock unnecesarry key detail
        au.lock_hide_attr(['s'], self.ctrl_up.control)
        au.lock_hide_attr(['r', 's'], self.ctrl_mid.control)
        au.lock_hide_attr(['s'], self.ctrl_down.control)

        # Lock some groups
        au.lock_attr(['t', 'r', 's', 'v'], self.grp_follicle_main[0])
        au.lock_hide_attr(['t', 'r', 's', 'v'], self.grp_no_transform_zro[0])
        au.lock_hide_attr(['t', 'r', 's', 'v'], self.grp_no_transform[0])
        au.lock_hide_attr(['t', 'r', 's', 'v'], self.grp_jnt_cluster[0])
        au.lock_hide_attr(['t', 'r', 's', 'v'], self.grp_deformers[0])
        au.lock_hide_attr(['t', 'r', 's', 'v'], self.grp_surfaces[0])
        au.lock_hide_attr(['t', 'r', 's', 'v'], self.grp_misc[0])
        au.lock_hide_attr(['t', 'r', 's', 'v'], geo_plane_wire[0])
        au.lock_hide_attr(['t', 'r', 's', 'v'], (mc.listConnections(wire_deformer[0] + '.baseWire[0]')[0]))

        mc.delete(create_joint, position_uv_fol, self.joint_reference_up, self.joint_reference_down)

        # Delete the module surface and group rotation driver
        mc.delete(tmp_plane, grp_joint_orient)

        # rename constraint
        au.constraint_rename([ctrl_up_parentConstraint[0], ctrl_mid_parentConstraint[0], ctrl_down_parentConstraint[0], ctrl_down_aim_constraint[0], ctrl_up_aim_constraint[0],
                              ctrl_mid_aim_constraint[0], point_to_mid_constraint[0], parent_to_mid_constraint[0]])

        # Clear all selection
        mc.select(cl=1)

    # ==================================================================================================================
    #                                               GENERAL FUNCTION
    # ==================================================================================================================
    # GENERAL FUNCTION: ADD JOINTS FOR GUIDANCE OF FOLLICLES
    def item_follicle(self, items, obj_tansform, suffix):
        follicles = []
        follicle_shape = []
        for i in items:
            follicle = au.create_follicle_selection(i, obj_tansform, connect_follicle=['rotateConn', 'transConn'])[0]
            rename_fol = mc.rename(follicle, '%s_%s' % (au.prefix_name(i), suffix))
            follicles.append(rename_fol)
            list_relatives_follicleShape = mc.listRelatives(rename_fol, s=1)[0]
            follicle_shape.append(list_relatives_follicleShape)

        return {'item': items,
                'follicle': follicles,
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
        nonLinear_deformer    = mc.nonLinear(objects[0], type=deformer_type, lowBound=low_bound, highBound=high_bound)
        nonLinear_deformer[0] = mc.rename(nonLinear_deformer[0], (name + '_' + deformer_type + 'Def'))
        nonLinear_deformer[1] = mc.rename(nonLinear_deformer[1], (name + '_' + deformer_type + 'Handle'))

        # If translate was specified, set the translate
        if translate:
            mc.setAttr((nonLinear_deformer[1] + '.translate'), translate[0], translate[1], translate[2])

        # If rotate was specified, set the rotate
        if rotate:
            mc.setAttr((nonLinear_deformer[1] + '.rotate'), rotate[0], rotate[1], rotate[2])

        # Return the deformer
        return nonLinear_deformer