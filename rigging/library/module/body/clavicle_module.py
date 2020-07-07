from __builtin__ import reload

import maya.cmds as mc

from rigging.library.base.body import clavicle as cl
from rigging.library.module import base_module as gm, template_single_module as ds, template_module as sd
from rigging.library.utils import controller as ct
from rigging.tools import AD_utils as au

reload(gm)
reload(ct)
reload(au)
reload(cl)
reload(sd)
reload(ds)


class Clavicle:
    def __init__(self,
                 clavicle=None,
                 prefix='clavicle',
                 base_controller=None,
                 clavicle_jnt=None,
                 parent_jnt=None,
                 side=None,
                 scale_jnt=None,
                 size=1.0,
                 single_module=True,
                 left_side=True):

        """
        ###############################################################################################

        HOW TO CALL SINGLE MODULE:
        @:param > baseController, variable, module anim controller,
        @:param > leftSide, True/False, True means left side, False means right side
        @:param > size, float, can fill it in any number, use it if need it

        ################################################################################################
        """
        if not mc.objExists('anim_ctrl'):
            mc.error('Please create the module controller first!')

        if single_module:
            if left_side:
                if mc.objExists('clavLFT_skn'):
                    mc.error('please clean up the left clavicle first!')
                else:
                    self.joint_driver()
                    self.module(clavicle_jnt=self.sj.clav_LFT,
                                # skin_joint_clavicle=self.sSkn.clav_LFT,
                                prefix=prefix, base=base_controller, parent_jnt=False, side='LFT',
                                scale_jnt=self.ss.clav_LFT, size=1.0)
                    # mc.parent(self.sSkn.clav_LFT, base_controller.skinGrp)
                    mc.delete(self.sj.upArm_LFT, self.ss.upArm_LFT)

            else:
                if mc.objExists('clavRGT_skn'):
                    mc.error('please clean up the right clavicle first!')
                else:
                    self.joint_driver()
                    self.module(clavicle_jnt=self.sj.clav_RGT,
                                prefix=prefix, base=base_controller, parent_jnt=False, side='RGT',
                                scale_jnt=self.ss.clav_RGT, size=1.0)
                    mc.delete(self.sj.upArm_RGT, self.ss.upArm_RGT)

            mc.delete(self.sj.root, self.ss.root, self.sFk.root, self.sIk.root, self.sTwistHelp.root, self.sAdd.root,)
        else:
            if clavicle:
                self.module(clavicle_jnt=clavicle_jnt,
                            prefix=prefix, base=base_controller, parent_jnt=parent_jnt, side=side, scale_jnt=scale_jnt,
                            size=size)

    def joint_driver(self):
        skel = ds.all_skeleton(sj_prefix_value='ModClav', ss_prefix_value='ModClavScl', sFk_prefix_value='ModClavFk',
                               sIk_prefix_value='ModClavIk',
                               sAdd_prefix_value='ModClavShape')
        self.sj = skel['sj']
        self.sFk = skel['sFk']
        self.sIk = skel['sIk']
        self.ss = skel['ss']
        self.sTwistHelp = skel['sTwistHelp']
        self.sAdd = skel['sAdd']

    def module(self, clavicle_jnt, prefix, base, side, scale_jnt, size, parent_jnt=True):
        ### IMPORT SPINE MODULE
        build_clavicle = cl.Build(
            clav_jnt=clavicle_jnt,
            prefix=prefix,
            side=side,
            scale=size)

        # instance the objects
        self.clavicle_controller_grp_zro = build_clavicle.controller_clavicle.parent_control[0]
        self.clavicle_controller = build_clavicle.controller_clavicle.control
        self.clavicle_gimbal = build_clavicle.controller_clavicle.control_gimbal

        # build part of group hierarchy
        part = gm.Part(prefix=prefix, side=side)
        mc.parent(part.top_grp, base.body_part_grp)

        # parent some controls setup to part group
        mc.parent(self.clavicle_controller_grp_zro, part.control_grp)

        if parent_jnt:
            # parent constraint the spine 04 joint to spine controller setup
            pac_clav_constraint = mc.parentConstraint(parent_jnt, self.clavicle_controller_grp_zro, mo=1)
            # rename constraint
            au.constraint_rename(pac_clav_constraint)

        # connect scale attribute
        mc.connectAttr(build_clavicle.scale_x + '.scaleX', scale_jnt + '.scaleX')
        mc.connectAttr(build_clavicle.scale_y + '.scaleY', scale_jnt + '.scaleY')
        mc.connectAttr(build_clavicle.scale_z + '.scaleZ', scale_jnt + '.scaleZ')

        # parent joint scale
        mc.parent(scale_jnt, self.clavicle_gimbal)