from __builtin__ import reload

import maya.cmds as mc

from rigging.library.base.body import spine as sp, spine_part_detail as rb
from rigging.library.module import base_module as gm, template_single_module as ds, template_module as sd
from rigging.library.utils import controller as ct
from rigging.tools import AD_utils as au

reload(gm)
reload(ct)
reload(sp)
reload(au)
reload(rb)
reload(sd)
reload(ds)

class Spine:
    def __init__(self,
                 prefix='spine',
                 prefix_spine_setup='spineSetup',
                 base_controller=None,
                 spine_jnt=None,
                 pelvis_jnt=None,
                 root_jnt=None,
                 detail_spine_deformer=True,
                 # skin_root_jnt=None,
                 # skin_pelvis_jnt=None,
                 # skin_spine_jnt=None,
                 single_module=True,
                 size= 1.0
                 ):
        """
        ###############################################################################################

        HOW TO CALL SINGLE MODULE:

        @:param > baseController, variable, module anim controller,
        @:param > detailLimbDeformer, True/False, True means has deformer, False means doesn't has
        @:param > size, float, can fill it in any number, use it if need it

        ################################################################################################
        """

        if not mc.objExists('anim_ctrl'):
            mc.error('Please create the module controller first!')

        # parent to body module
        part = gm.Part(prefix=prefix)
        mc.parent(part.top_grp, base_controller.body_part_grp)

        # set tmpJnt gpr to 0
        mc.setAttr('tmpJnt_grp.visibility', 0)

        # single module
        if single_module:
            skeleton = ds.all_skeleton(sj_prefix_value='ModSpine', ss_prefix_value='ModSpineScl',
                                       sFk_prefix_value='ModSpineFk', sIk_prefix_value='ModSpineIk',
                                       sAdd_prefix_value='ModSpineShape')
            sj = skeleton['sj']
            sFk = skeleton['sFk']
            sIk = skeleton['sIk']
            ss = skeleton['ss']
            sTwistHelp = skeleton['sTwistHelp']
            sAdd = skeleton['sAdd']
            self.module(prefix=prefix, prefix_spine_setup=prefix_spine_setup, base_controller=base_controller,
                        spine_jnt=sj.spine_list, pelvis_jnt=sj.pelvis, root_jnt=sj.root,
                        detail_spine_deformer=detail_spine_deformer,
                        # skin_root_jnt=sSkn.root, skin_pelvis_jnt=sSkn.pelvis,
                        # skin_spine_jnt=sSkn.spineList,
                        size=size, part=part)

            # # parent skin into skin group
            # mc.parent(sj.root, base_controller.skinGrp)

            mc.delete(sFk.root, ss.root, sIk.root, sTwistHelp.root, sAdd.root,
                      sj.clav_RGT, sj.clav_LFT, sj.neck, sj.upLeg_LFT, sj.upLeg_RGT)
        else:
            self.module(prefix=prefix, prefix_spine_setup=prefix_spine_setup, base_controller=base_controller,
                        spine_jnt=spine_jnt,
                        pelvis_jnt=pelvis_jnt, root_jnt=root_jnt, detail_spine_deformer=detail_spine_deformer,
                        # skin_root_jnt=skin_root_jnt,
                        # skin_pelvis_jnt=skin_pelvis_jnt, skin_spine_jnt=skin_spine_jnt,
                        size=size, part=part)

    def module(self, prefix, prefix_spine_setup, base_controller, spine_jnt, pelvis_jnt, root_jnt,
               detail_spine_deformer,
               # skin_root_jnt, skin_pelvis_jnt, skin_spine_jnt,
               size, part):
        # ==================================================================================================================
        #                                                  IMPORT SPINE MODULE
        # ==================================================================================================================
        build_spine = sp.Build(
            spine_jnt=spine_jnt,
            pelvis_jnt=pelvis_jnt,
            root_jnt=root_jnt,
            prefix_spine_setup=prefix_spine_setup,
            detail_spine_deformer=detail_spine_deformer,
            scale=size * 2.0)

        # instance the objects
        self.pelvis_gimbal_controller = build_spine.controller_pelvis.control_gimbal
        self.root_gimbal_controller = build_spine.controller_root.control_gimbal
        self.root_controller_grp_zro = build_spine.controller_root.parent_control[0]
        self.FkIk_spine_controller_grp_zro = build_spine.controller_FkIk_spine_setup.parent_control[0]
        self.FkIk_spine_controller = build_spine.controller_FkIk_spine_setup.control

        # parent some controls setup to part group
        # controller
        mc.parent(self.root_controller_grp_zro, part.control_grp)

        # parent all spine to module skeleton Grp
        mc.parent(spine_jnt, part.joint_grp)

        ctrl_mid = None
        if detail_spine_deformer:
            ctrl_mid = self.FkIk_spine_controller
        else:
            ctrl_mid = ctrl_mid

        # ==================================================================================================================
        #                                               IMPORT DETAIL SPINE MODULE
        # ==================================================================================================================
        detail_spine = rb.CreateDetail(part_grp_ctrl=part.control_grp,
                                       parallel_axis='y',
                                       tip_position='+',
                                       anim_ctrl=base_controller.anim_control,
                                       list_spine_jnt=[root_jnt, spine_jnt[0], spine_jnt[1], spine_jnt[2], spine_jnt[3]],

                                       list_spine_ctrl_fk=[build_spine.controller_spine_fk_low.control_gimbal,
                                                          build_spine.controller_spine_fk_mid.control_gimbal,
                                                          build_spine.controller_spine_fk_up.control_gimbal],

                                       list_spine_ctrl_ik=[build_spine.controller_spine_ik_low.control_gimbal,
                                                          build_spine.controller_spine_ik_up.control_gimbal,
                                                          build_spine.controller_spine_ik_up.control],

                                       FkIk_switch=self.FkIk_spine_controller,
                                       prefix=prefix,
                                       detail_spine_deformer=detail_spine_deformer,
                                       ctrl_details=ct.CIRCLEPLUS,
                                       ctrl_mid=ctrl_mid,
                                       scale=size
                                       )

        # Parent ribbon spine to nonTransformGrp
        mc.parent(detail_spine.grp_all_detail, part.non_transform_grp)

        # Visibility of follicle controller
        au.connect_part_object(obj_base_connection='detailCtrl', target_connection='visibility',
                               obj_name=build_spine.controller_FkIk_spine_setup.control,
                               target_name=[detail_spine.grp_follicle_main[0]],
                               select_obj=False)

        # scale the spine part
        self.spine_part_scale(build_spine.controller_FkIk_spine_setup.control, detail_spine.follicle_grp_zro)

        # # CREATE JOINT SKIN AND CONNECTING
        # au.parent_scale_constraint(root_jnt, skin_root_jnt)
        # au.parent_scale_constraint(pelvis_jnt, skin_pelvis_jnt)
        # au.parent_scale_constraint(spine_jnt[0], skin_spine_jnt[0])
        # au.parent_scale_constraint(spine_jnt[1], skin_spine_jnt[1])
        # au.parent_scale_constraint(spine_jnt[2], skin_spine_jnt[2])
        # au.parent_scale_constraint(spine_jnt[3], skin_spine_jnt[3])

    def spine_part_scale(self, controller, groupScale):
        # LIMB SCALE
        for i in groupScale:
            mc.connectAttr(controller + '.spineScaleX', i + '.scaleX')
            mc.connectAttr(controller + '.spineScaleY', i + '.scaleY')
            mc.connectAttr(controller + '.spineScaleZ', i + '.scaleZ')
