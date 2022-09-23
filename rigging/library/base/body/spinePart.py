from __future__ import absolute_import

import maya.cmds as cmds

from rigging.library.utils import controller as rlu_controller
from rigging.tools import utils as rt_utils


class CreateDetail:
    def __init__(self,
                 part_grp_ctrl,
                 parallel_axis,
                 tip_position,
                 list_spine_jnt,
                 list_spine_ctrl_fk,
                 list_spine_ctrl_ik,
                 FkIk_switch,
                 anim_ctrl,
                 ctrl_mid,
                 ctrl_details,
                 scale,
                 prefix,
                 detail_spine_deformer,
                 side='',
                 ):

        """
        :param parallel_axis  : str, two point parallel position direction whether on x or y or z axis
        :param tip_position    : str, position point (joint) of the tip regarding on the module joint whether on + or - axis
        :param prefix    : str, prefix name for detail
        :param numJoints : int, number of joint as well as the control of detail part
        """
        # Width plane variable (following the number of joints
        # size = float(3)

        # Tip point dictionary towards
        tip_point = {'+': [(3 / 2.0 * -1) * scale, (3 / 2.0) * scale],
                     '-': [(3 / 2.0) * scale, (3 / 2.0 * -1) * scale]}

        if tip_position in tip_point.keys():
            self.pos = (0, 0, 0)
            self.upPoint = tip_point[tip_position][0]
            self.downPoint = tip_point[tip_position][1]
        else:
            raise cmds.error('The string %s in tipPos argument is not found. Fill with + or -' % tip_position)

        # Dictionary list
        tmp_plane_dic = {'x': [(0, 1, 0), 3 * scale, (1.0 / 3), 3, 1],
                         'y': [(0, 0, 1), 1 * scale, 3, 1, 3],
                         'z': [(0, 1, 0), 1 * scale, 3, 1, 3]}

        direction = {'x': ['.rotateY', 90, '.translateZ'],
                     'y': ['.rotateZ', 90, '.translateX'],
                     'z': ['.rotateX', 0, '.translateX']}

        rotation_defomer = {'x': (0, 0, 90),
                            'y': (0, 0, 180),
                            'z': (-90, 0, 90)}

        vol_input_mdn = {'x': ['.translateX', '.input1Z', '.outputZ', '.scaleY', '.scaleZ'],
                         'y': ['.translateY', '.input1X', '.outputX', '.scaleX', '.scaleZ'],
                         'z': ['.translateZ', '.input1X', '.outputX', '.scaleX', '.scaleZ']}

        follicle_vol = {'x': ('.parameterV', -1),
                        'y': ('.parameterU', 1),
                        'z': ('.parameterU', 1)}

        ### GROUPS AND SURFACES
        # Create the main groups
        self.grp_all_detail = cmds.group(empty=True, name=(prefix + 'AllDetail_grp'))
        self.grp_surface = cmds.duplicate(self.grp_all_detail, name=(prefix + 'RefSurface_grp'))
        self.grp_follicle_main = cmds.duplicate(self.grp_all_detail, name=(prefix + 'FolSkin_grp'))
        self.grp_extra_follicle = cmds.duplicate(self.grp_all_detail, name=(prefix + 'Extra_grp'))

        # inherits follicleS main grp
        cmds.setAttr(self.grp_follicle_main[0] + '.it', 0, l=1)

        # Create a NURBS-plane to use as a module
        tmp_plane = cmds.nurbsPlane(axis=tmp_plane_dic[parallel_axis][0], width=tmp_plane_dic[parallel_axis][1],
                                    lengthRatio=tmp_plane_dic[parallel_axis][2], u=1,
                                    v=5, degree=3, ch=0)[0]

        ### CREATING JOINT TEMPORARY FOR SPLITTING JNT FOLLICLE
        # Create Joint reference
        cmds.select(cl=1)
        create_joint = cmds.joint(radius=scale / 5)

        # Duplicate joint from reference for orientation detail
        self.joint_skin_up = cmds.duplicate(create_joint, n=prefix + 'SkinHip_jnt')
        self.joint_skin_mid = cmds.duplicate(create_joint, n=prefix + 'SkinMid_jnt')
        self.joint_skin_down = cmds.duplicate(create_joint, n=prefix + 'SkinChest_jnt')

        # Set the position for joints orient
        cmds.setAttr((self.joint_skin_up[0] + '.translate'), self.upPoint, self.pos[1], self.pos[2])
        cmds.setAttr((self.joint_skin_mid[0] + '.translate'), self.pos[0], self.pos[1], self.pos[2])
        cmds.setAttr((self.joint_skin_down[0] + '.translate'), self.downPoint, self.pos[1], self.pos[2])

        # Grouping the joints to have rotation according to parallel axis
        grp_joint_orient = cmds.group(self.joint_skin_up[0], self.joint_skin_mid[0], self.joint_skin_down[0])

        # Set the rotation group joints
        if parallel_axis == 'z':
            cmds.setAttr((grp_joint_orient + '.rotate'), 0, -90, 0)

        if parallel_axis == 'y':
            cmds.setAttr((grp_joint_orient + '.rotate'), 0, 0, 90)

        cmds.delete(cmds.orientConstraint(list_spine_jnt[0], self.joint_skin_up[0], mo=0))
        cmds.delete(cmds.orientConstraint(list_spine_jnt[0], self.joint_skin_mid[0], mo=0))
        cmds.delete(cmds.orientConstraint(list_spine_jnt[0], self.joint_skin_down[0], mo=0))

        # Create the NURBS-planes to use in the setup
        geo_plane_skin = cmds.duplicate(tmp_plane, name=(prefix + 'Skin_geo'))

        # grouping deformer surface geoPlane and geoPlaneSKin
        self.grp_geo_plane_cluster = rt_utils.group_object(['Zro'], geo_plane_skin[0], geo_plane_skin[0])

        follicle_v = None
        if detail_spine_deformer:

            # Create the NURBS-planes to use in the setup
            self.geo_plane_sine = cmds.duplicate(tmp_plane, name=(prefix + 'SineDef_geo'))
            self.geo_plane_volume = cmds.duplicate(tmp_plane, name=(prefix + 'Volume_geo'))

            # Offset the volume-plane
            cmds.setAttr((self.geo_plane_volume[0] + direction[parallel_axis][2]), -0.5 * scale)

            # Create deformers: Blendshape
            cmds.blendShape(self.geo_plane_sine[0],
                            geo_plane_skin[0], name=(prefix + 'Ref_bsn'), weight=[(0, 1)], foc=1)

            # create grp for follicle volume
            self.grp_follicle_volume = cmds.group(empty=True, name=(prefix + 'FolVolume_grp'))
            self.grp_deformer_surface = cmds.duplicate(self.grp_follicle_volume, name=(prefix + 'DeformSurf_grp'))
            self.grp_deformer = cmds.duplicate(self.grp_follicle_volume, name=(prefix + 'Deformer_grp'))
            self.grp_volume_deformer = cmds.duplicate(self.grp_follicle_volume, name=(prefix + 'VolumeSquash_grp'))
            self.grp_sine_deformer = cmds.duplicate(self.grp_follicle_volume, name=(prefix + 'SineDef_grp'))

            # Create deformers: Twist deformer, Sine deformer, Squash deformer
            # Set them rotation  according on point parallelFaceAxis position
            self.sine_deformer = self.nonlinear_deformer(objects=[self.geo_plane_sine[0]], deformer_type='sine',
                                                         name=rt_utils.prefix_name(self.geo_plane_sine[0]), low_bound=-1,
                                                         high_bound=1, rotate=rotation_defomer[parallel_axis])

            self.squash_deformer = self.nonlinear_deformer(objects=[self.geo_plane_volume[0]], deformer_type='squash',
                                                           name=rt_utils.prefix_name(self.geo_plane_volume[0]), low_bound=-1,
                                                           high_bound=1, rotate=rotation_defomer[parallel_axis])
            cmds.parent(self.sine_deformer[1], self.grp_sine_deformer[0])
            cmds.parent(self.squash_deformer[1], self.grp_volume_deformer[0])

            cmds.setAttr((self.sine_deformer[0] + '.dropoff'), 1)

            # Squash deformer: Set up the connections for the volume control
            volume_reverse_mdl = cmds.shadingNode('multDoubleLinear', asUtility=1, name=(prefix + 'VolReverse_mdl'))
            # Adding multiple scale for volume
            volume_multiply_position_mdl = cmds.createNode('multDoubleLinear', n=(prefix + 'VolPosMultiplier_mdl'))
            volume_multiply_sclale_mdl = cmds.createNode('multDoubleLinear', n=(prefix + 'VolSclMultiplier_mdl'))

            # Auto squash setup
            auto_squash_ctrl_ik = cmds.createNode('addDoubleLinear', n=(prefix + 'AutoSquashCtrlIk_adl'))
            auto_squash_multiply_div = cmds.createNode('multiplyDivide', n=(prefix + 'AutoSquash_mdn'))
            auto_squash_blend_color = cmds.createNode('blendColors', n=(prefix + 'AutoSquash_bnd'))
            comb_add_between_adl = cmds.createNode('addDoubleLinear', n=(prefix + 'AutoSquashVol_adl'))

            cmds.connectAttr(list_spine_ctrl_ik[1] + '.translateY', auto_squash_ctrl_ik + '.input1')
            cmds.connectAttr(list_spine_ctrl_ik[2] + '.translateY', auto_squash_ctrl_ik + '.input2')

            cmds.setAttr(auto_squash_multiply_div + '.operation', 2)
            cmds.setAttr(auto_squash_multiply_div + '.input2X', -3 * scale)
            cmds.connectAttr(auto_squash_ctrl_ik + '.output', auto_squash_multiply_div + '.input1X')

            cmds.connectAttr(ctrl_mid + '.autoSquash', auto_squash_blend_color + '.blender')
            cmds.connectAttr(auto_squash_multiply_div + '.outputX', auto_squash_blend_color + '.color1R')
            cmds.connectAttr(auto_squash_blend_color + '.outputR', comb_add_between_adl + '.input1')
            cmds.connectAttr((ctrl_mid + '.volume'), (comb_add_between_adl + '.input2'))

            # Connect from add double linear to squash handle
            cmds.setAttr((volume_reverse_mdl + '.input1'), -1)
            cmds.connectAttr((comb_add_between_adl + '.output'), (volume_reverse_mdl + '.input2'))
            cmds.connectAttr((volume_reverse_mdl + '.output'), (self.squash_deformer[0] + '.factor'))
            cmds.connectAttr((ctrl_mid + '.startDropoff'), (self.squash_deformer[0] + '.startSmoothness'))
            cmds.connectAttr((ctrl_mid + '.endDropoff'), (self.squash_deformer[0] + '.endSmoothness'))

            # Set the translate squash deformer according the point parallelFaceAxis position
            cmds.setAttr((volume_multiply_position_mdl + '.input2'), tip_point[tip_position][1])
            cmds.connectAttr((ctrl_mid + '.volumePosition'), (volume_multiply_position_mdl + '.input1'))
            cmds.connectAttr((volume_multiply_position_mdl + '.output'),
                             (self.squash_deformer[1] + vol_input_mdn[parallel_axis][0]))

            # Squash deformer: Set up the volume scaling
            sum_scale_pma = cmds.shadingNode('plusMinusAverage', asUtility=1, name=(prefix + 'VolScaleSum_pma'))
            cmds.connectAttr((ctrl_mid + '.volumeScale'), (volume_multiply_sclale_mdl + '.input1'))
            cmds.setAttr((volume_multiply_sclale_mdl + '.input2'), scale)
            cmds.setAttr((sum_scale_pma + '.input1D[0]'), self.downPoint)
            cmds.connectAttr((volume_multiply_sclale_mdl + '.output'), (sum_scale_pma + '.input1D[1]'))
            cmds.connectAttr((sum_scale_pma + '.output1D'), (self.squash_deformer[1] + '.scaleY'))

            # Sine deformer: Set up the connections for the sine
            cmds.connectAttr((ctrl_mid + '.amplitude'), (self.sine_deformer[0] + '.amplitude'))
            cmds.connectAttr((ctrl_mid + '.offset'), (self.sine_deformer[0] + '.offset'))

            # Exception for z parallel axis
            if parallel_axis == 'z':
                sine_twist_node = cmds.createNode('addDoubleLinear', n=(prefix + 'AdjustSineTwistRotZ_adl'))
                cmds.setAttr(sine_twist_node + '.input1', 90)
                cmds.connectAttr(ctrl_mid + '.twist', sine_twist_node + '.input2')
                cmds.connectAttr(sine_twist_node + '.output', self.sine_deformer[1] + '.rotateZ')
            else:
                cmds.connectAttr((ctrl_mid + '.twist'), (self.sine_deformer[1] + '.rotateY'))

            cmds.connectAttr((ctrl_mid + '.sineLength'), (self.sine_deformer[0] + '.wavelength'))

            # create follicle V
            follicle_v = self.item_follicle(prefix + 'Chest',
                                            [self.joint_skin_down[0], self.joint_skin_mid[0], self.joint_skin_up[0]],
                                            self.geo_plane_volume, 'fol')

            # Set the follicleS U and V parameter
            for obj in follicle_v['follicle']:
                cmds.setAttr(obj + follicle_vol[parallel_axis][0], follicle_vol[parallel_axis][1])

            # Cleanup: Hierarchy
            cmds.parent(self.grp_sine_deformer[0], self.grp_volume_deformer[0], self.grp_deformer)
            cmds.parent(self.geo_plane_sine[0], self.geo_plane_volume[0], self.grp_deformer_surface)
            cmds.parent(self.grp_deformer_surface, self.grp_deformer, self.grp_follicle_volume, self.grp_all_detail)

            # Cleanup: Visibility
            cmds.hide(self.grp_deformer_surface, self.grp_deformer, self.grp_follicle_volume)

            rt_utils.lock_hide_attr(['t', 'r', 's', 'v'], self.grp_volume_deformer[0])
            rt_utils.lock_hide_attr(['t', 'r', 's', 'v'], self.grp_deformer[0])
            rt_utils.lock_hide_attr(['t', 'r', 's', 'v'], self.grp_deformer_surface[0])

        ######################
        # Parent to grp extra and freeze the joints
        cmds.parent(self.joint_skin_up[0], self.joint_skin_mid[0], self.joint_skin_down[0], self.grp_extra_follicle)
        cmds.makeIdentity(self.joint_skin_up[0], self.joint_skin_mid[0], self.joint_skin_down[0], a=1, r=1, pn=1)

        # Skining joints orient to plane orient
        skin_cluster = cmds.skinCluster([self.joint_skin_up[0], self.joint_skin_mid[0], self.joint_skin_down[0]],
                                        geo_plane_skin,
                                        n='spineDtlSkinCluster', tsb=True, bm=0, sm=0, nw=1, mi=2)

        # Distribute the skin
        skin_percent8 = '%s.cv[0:3][7]' % geo_plane_skin[0]
        skin_percent7 = '%s.cv[0:3][6]' % geo_plane_skin[0]
        skin_percent1 = '%s.cv[0:3][5]' % geo_plane_skin[0]
        skin_percent2 = '%s.cv[0:3][4]' % geo_plane_skin[0]
        skin_percent3 = '%s.cv[0:3][3]' % geo_plane_skin[0]
        skin_percent4 = '%s.cv[0:3][2]' % geo_plane_skin[0]
        skin_percent5 = '%s.cv[0:3][1]' % geo_plane_skin[0]
        skin_percent6 = '%s.cv[0:3][0]' % geo_plane_skin[0]

        cmds.skinPercent(skin_cluster[0], skin_percent8, tv=[(self.joint_skin_down[0], 1)])
        cmds.skinPercent(skin_cluster[0], skin_percent7,
                         tv=[(self.joint_skin_down[0], 0.9), (self.joint_skin_mid[0], 0.1)])
        cmds.skinPercent(skin_cluster[0], skin_percent1,
                         tv=[(self.joint_skin_down[0], 0.7), (self.joint_skin_mid[0], 0.3)])
        cmds.skinPercent(skin_cluster[0], skin_percent2,
                         tv=[(self.joint_skin_down[0], 0.4), (self.joint_skin_mid[0], 0.6)])
        cmds.skinPercent(skin_cluster[0], skin_percent3, tv=[(self.joint_skin_up[0], 0.4), (self.joint_skin_mid[0], 0.6)])
        cmds.skinPercent(skin_cluster[0], skin_percent4, tv=[(self.joint_skin_up[0], 0.8), (self.joint_skin_mid[0], 0.2)])
        cmds.skinPercent(skin_cluster[0], skin_percent5, tv=[(self.joint_skin_up[0], 1)])
        cmds.skinPercent(skin_cluster[0], skin_percent6, tv=[(self.joint_skin_up[0], 1)])

        ### NODE REVERSE FOR DETAIL SETUP
        # create reverse node for set FK
        ctrl_spine_fk_reverse = cmds.createNode('reverse', n='spineFkIk02_rev')
        rt_utils.connect_part_object(obj_base_connection='FkIk', target_connection='inputX',
                                     obj_name=FkIk_switch, target_name=[ctrl_spine_fk_reverse],
                                     select_obj=False)

        ### PARENT CONSTRAINT SKIN JOINT
        ## Constraint skin spine 01 joint
        list_spine_constraint = cmds.parentConstraint(list_spine_ctrl_fk[0], self.joint_skin_up[0], mo=0)

        ## Costraint skin chest joint
        skin_chest_constraint = cmds.parentConstraint(list_spine_ctrl_fk[2], list_spine_ctrl_ik[1],
                                                      self.joint_skin_down[0], mo=0)

        ## setup UP controller set to IK
        rt_utils.connect_part_object(obj_base_connection='FkIk', target_connection='%s%s' % (list_spine_ctrl_ik[1], 'W1'),
                                     obj_name=FkIk_switch,
                                     target_name=[skin_chest_constraint[0]],
                                     select_obj=False)

        ## setup UP controller set to FK
        rt_utils.connect_part_object(obj_base_connection='outputX', target_connection='%s%s' % (list_spine_ctrl_fk[2], 'W0'),
                                     obj_name=ctrl_spine_fk_reverse, target_name=[skin_chest_constraint[0]],
                                     select_obj=False)

        # position mid joint
        cmds.delete(cmds.parentConstraint(self.joint_skin_up[0], self.joint_skin_down[0], self.joint_skin_mid[0], mo=0))

        ## Costraint skin mid joint
        skin_mid_constraint = cmds.parentConstraint(list_spine_ctrl_fk[1], list_spine_ctrl_ik[0], self.joint_skin_mid[0],
                                                    mo=1)

        ## setup MID controller set to IK
        rt_utils.connect_part_object(obj_base_connection='FkIk', target_connection='%s%s' % (list_spine_ctrl_ik[0], 'W1'),
                                     obj_name=FkIk_switch,
                                     target_name=[skin_mid_constraint[0]],
                                     select_obj=False)

        ## setup MID controller set to FK
        rt_utils.connect_part_object(obj_base_connection='outputX', target_connection='%s%s' % (list_spine_ctrl_fk[1], 'W0'),
                                     obj_name=ctrl_spine_fk_reverse, target_name=[skin_mid_constraint[0]],
                                     select_obj=False)

        ### SCALE DECOMPOSE MATRIX FROM ANIM CONTROLLER TO FOLLICLE AND SKIN JOINT
        jnt_skin_list = [self.joint_skin_up[0], self.joint_skin_mid[0], self.joint_skin_down[0]]

        decompose_matrix_node = cmds.createNode('decomposeMatrix', n=prefix + 'ScaleFol_dmtx')
        cmds.connectAttr(anim_ctrl + '.worldMatrix[0]', decompose_matrix_node + '.inputMatrix')

        for jnt_skn in jnt_skin_list:
            cmds.connectAttr(decompose_matrix_node + '.outputScale', jnt_skn + '.scale')

        ### CREATE FOLLICLE S
        follicle_s = self.item_follicle(prefix, list_spine_jnt[1:4], geo_plane_skin, 'fol')

        follicle_grp_offset = []
        follicle_ctrl = []
        self.follicle_grp_zro = []
        # Looping the follicle S
        for fol_s, fol_shp, jntSpine in zip(follicle_s['follicle'], follicle_s['folShape'], list_spine_jnt[1:4]):
            # Parenting the follicles to grp follicleS
            cmds.parent(fol_s, self.grp_follicle_main)

            # Group follicleS offset
            # Create group offset for follice
            follicleGrpOffset = cmds.group(empty=True, name='%s_%s' % (rt_utils.prefix_name(fol_s), 'setGrp'))

            # append
            follicle_grp_offset.append(follicleGrpOffset)

            # Create control for joint in follicleS
            follicleCtrl = rlu_controller.Control(prefix=rt_utils.prefix_name(fol_s), groups_ctrl=['Zro'], side=side,
                                                  ctrl_color='lightPink',
                                                  ctrl_size=scale * 1.2, shape=ctrl_details)
            follicle_ctrl.append(follicleCtrl.control)
            self.follicle_grp_zro.append(follicleCtrl.parent_control[0])

            # Parent constraint follicle control to joint spine
            cmds.parent(jntSpine, follicleCtrl.control)

            # set value to 0
            cmds.setAttr(jntSpine + '.translate', 0, 0, 0, type='double3')
            cmds.setAttr(jntSpine + '.rotate', 0, 0, 0, type='double3')

            # Parent ctrl grp to grp offset
            cmds.parent(follicleCtrl.parent_control[0], follicleGrpOffset)

            # Parent grp offset to follicleS
            cmds.delete(cmds.pointConstraint(fol_s, follicleGrpOffset))
            # parent setGrp
            cmds.parent(follicleGrpOffset, fol_s)

            cmds.connectAttr(decompose_matrix_node + '.outputScale', fol_s + '.scale')
            # Turn off visibility
            cmds.setAttr(fol_shp + '.visibility', 0)

        # constraint rename
        rt_utils.constraint_rename([list_spine_constraint[0], skin_chest_constraint[0], skin_mid_constraint[0]])

        # ==================================================================================================================
        #                                               IF DEFORM TRUE
        # ==================================================================================================================
        if detail_spine_deformer:
            # Looping the follicle S V
            for fol_s, fol_shp, fol_v, fol_grp_offset, fol_ctrl, in zip(follicle_s['follicle'], follicle_s['folShape'],
                                                                        follicle_v['follicle'], follicle_grp_offset,
                                                                        follicle_ctrl):
                # Parenting the follicles to grp follicleS
                cmds.parent(fol_v, self.grp_follicle_volume)

                # Multiplier from follicleS to multiplier for the size
                mult_mpd_size = cmds.shadingNode('multiplyDivide', asUtility=1,
                                                 name=rt_utils.prefix_name(fol_s) + 'MultiplierSize_mdn')
                cmds.setAttr(mult_mpd_size + '.operation', 2)
                cmds.connectAttr((fol_v + '.translate'), (mult_mpd_size + '.input1'))
                cmds.setAttr(mult_mpd_size + '.input2X', scale)
                cmds.setAttr(mult_mpd_size + '.input2Y', scale)
                cmds.setAttr(mult_mpd_size + '.input2Z', scale)

                # Make the connections for the volume according on point parallelFaceAxis position
                mult_mpd = cmds.shadingNode('multiplyDivide', asUtility=1, name=rt_utils.prefix_name(fol_s) + 'Multiplier_mdn')
                cmds.connectAttr((ctrl_mid + '.volumeMultiplier'), vol_input_mdn[parallel_axis][1])
                cmds.connectAttr((mult_mpd_size + '.output'), (mult_mpd + '.input2'))

                sum_pma = cmds.shadingNode('plusMinusAverage', asUtility=1, name=rt_utils.prefix_name(fol_v) + 'VolumeSum_pma')
                cmds.connectAttr((mult_mpd + vol_input_mdn[parallel_axis][2]), (sum_pma + '.input1D[0]'))
                cmds.setAttr((sum_pma + '.input1D[1]'), 1)
                cmds.connectAttr((sum_pma + '.output1D'), (fol_grp_offset + vol_input_mdn[parallel_axis][3]))
                cmds.connectAttr((sum_pma + '.output1D'), (fol_grp_offset + vol_input_mdn[parallel_axis][4]))

                # Turn off visibility
                cmds.setAttr(fol_shp + '.visibility', 0)

        # Cleanup: Hierarchy
        cmds.parent(self.grp_geo_plane_cluster[0], self.grp_surface)
        cmds.parent(self.grp_surface[0],
                    self.grp_extra_follicle[0], self.grp_all_detail)

        cmds.parent(self.grp_follicle_main[0], part_grp_ctrl)

        # Cleanup: Visibility
        cmds.hide(self.grp_surface[0], self.grp_geo_plane_cluster[0], self.grp_extra_follicle[0])

        # Lock some groups
        rt_utils.lock_hide_attr(['t', 'r', 's', 'v'], self.grp_all_detail)

        rt_utils.lock_hide_attr(['t', 'r', 's'], self.grp_follicle_main[0])
        rt_utils.lock_hide_attr(['t', 'r', 's', 'v'], self.grp_surface[0])
        rt_utils.lock_hide_attr(['t', 'r', 's', 'v'], self.grp_geo_plane_cluster[0])
        rt_utils.lock_hide_attr(['t', 'r', 's', 'v'], self.grp_extra_follicle[0])

        # Deleted the reference joint
        cmds.delete(create_joint, tmp_plane, grp_joint_orient)

    # ==================================================================================================================
    #                                               GENERAL FUNCTION
    # ==================================================================================================================
    # GENERAL FUNCTION: ADD JOINTS FOR GUIDANCE OF FOLLICLES
    def item_follicle(self, prefix, items, obj_transform, suffix):
        follicle_all = []
        follicleShape_all = []
        for number, i in enumerate(items):
            follicle = rt_utils.create_follicle_selection(i, obj_transform, connect_follicle=['rotateConn', 'transConn'])[0]
            rename_follicle = cmds.rename(follicle, '%s%02d%s_%s' % (rt_utils.prefix_name(prefix), number + 1, 'Dtl', suffix))
            follicle_all.append(rename_follicle)
            list_relatives_follicleShape = cmds.listRelatives(rename_follicle, s=1)[0]
            follicleShape_all.append(list_relatives_follicleShape)

        return {'item': items,
                'follicle': follicle_all,
                'folShape': follicleShape_all}

    # GENERAL FUNCTION: ADD ATTRIBUTE(S) ON MULTIPLE OBJECTS
    def add_attribute(self, objects=[], long_name='', nice_name='', separator=False, keyable=False, channel_box=False,
                      **kwargs):
        # For each object
        for obj in objects:
            # For each attribute
            for x in range(0, len(long_name)):
                # See if a niceName was defined
                attr_nice = '' if not nice_name else nice_name[x]
                # If the attribute does not exists
                if not cmds.attributeQuery(long_name[x], node=obj, exists=True):
                    # Add the attribute
                    cmds.addAttr(obj, longName=long_name[x], niceName=attr_nice, **kwargs)
                    # If lock was set to True
                    cmds.setAttr((obj + '.' + long_name[x]), k=keyable, e=1, cb=channel_box) if separator else cmds.setAttr(
                        (obj + '.' + long_name[x]), k=keyable, e=1, cb=channel_box)

    # GENERAL FUNCTION: CREATE A NONLINEAR DEFORMER
    def nonlinear_deformer(self, objects=[], deformer_type=None, low_bound=-1, high_bound=1, translate=None,
                           rotate=None, name='nonLinear'):

        # If something went wrong or the type is not valid, raise exception
        if not objects or deformer_type not in ['bend', 'flare', 'sine', 'squash', 'twist', 'wave']:
            raise Exception("function: 'nonlinearDeformer' - Make sure you specified a mesh and a valid deformer")

        # Create and rename the deformer
        non_linear_deformer = cmds.nonLinear(objects[0], type=deformer_type, lowBound=low_bound, highBound=high_bound)
        non_linear_deformer[0] = cmds.rename(non_linear_deformer[0], (name + '_' + deformer_type + 'Def'))
        non_linear_deformer[1] = cmds.rename(non_linear_deformer[1], (name + '_' + deformer_type + 'Handle'))

        # If translate was specified, set the translate
        if translate:
            cmds.setAttr((non_linear_deformer[1] + '.translate'), translate[0], translate[1], translate[2])

        # If rotate was specified, set the rotate
        if rotate:
            cmds.setAttr((non_linear_deformer[1] + '.rotate'), rotate[0], rotate[1], rotate[2])

        # Return the deformer
        return non_linear_deformer
