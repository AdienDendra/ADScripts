from __future__ import absolute_import

import maya.cmds as cmds

from rigging.library.base.body import clavicle as rlbb_clavicle
from rigging.library.module import baseModule as rlm_baseModule, tmpSingleModule as rlm_tmpSingleModule
from rigging.tools import utils as rt_utils


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
        if not cmds.objExists('anim_ctrl'):
            cmds.error('Please create the module controller first!')

        if single_module:
            if left_side:
                if cmds.objExists('clavLFT_skn'):
                    cmds.error('please clean up the left clavicle first!')
                else:
                    self.joint_driver()
                    self.module(clavicle_jnt=self.sj.clav_LFT,
                                # skin_joint_clavicle=self.sSkn.clav_LFT,
                                prefix=prefix, base=base_controller, parent_jnt=False, side='LFT',
                                scale_jnt=self.ss.clav_LFT, size=1.0)
                    # mc.parent(self.sSkn.clav_LFT, base_controller.skinGrp)
                    cmds.delete(self.sj.upArm_LFT, self.ss.upArm_LFT)

            else:
                if cmds.objExists('clavRGT_skn'):
                    cmds.error('please clean up the right clavicle first!')
                else:
                    self.joint_driver()
                    self.module(clavicle_jnt=self.sj.clav_RGT,
                                prefix=prefix, base=base_controller, parent_jnt=False, side='RGT',
                                scale_jnt=self.ss.clav_RGT, size=1.0)
                    cmds.delete(self.sj.upArm_RGT, self.ss.upArm_RGT)

            cmds.delete(self.sj.root, self.ss.root, self.sFk.root, self.sIk.root, self.sTwistHelp.root,
                        self.sAdd.root, )
        else:
            if clavicle:
                self.module(clavicle_jnt=clavicle_jnt,
                            prefix=prefix, base=base_controller, parent_jnt=parent_jnt, side=side, scale_jnt=scale_jnt,
                            size=size)

    def joint_driver(self):
        skel = rlm_tmpSingleModule.all_skeleton(sj_prefix_value='ModClav', ss_prefix_value='ModClavScl',
                                                sFk_prefix_value='ModClavFk',
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
        build_clavicle = rlbb_clavicle.Build(
            clav_jnt=clavicle_jnt,
            prefix=prefix,
            side=side,
            scale=size)

        # instance the objects
        self.clavicle_controller_grp_zro = build_clavicle.controller_clavicle.parent_control[0]
        self.clavicle_controller = build_clavicle.controller_clavicle.control
        self.clavicle_gimbal = build_clavicle.controller_clavicle.control_gimbal

        # build part of group hierarchy
        part = rlm_baseModule.Part(prefix=prefix, side=side)
        cmds.parent(part.top_grp, base.body_part_grp)

        # parent some controls setup to part group
        cmds.parent(self.clavicle_controller_grp_zro, part.control_grp)

        if parent_jnt:
            # parent constraint the spine 04 joint to spine controller setup
            pac_clav_constraint = cmds.parentConstraint(parent_jnt, self.clavicle_controller_grp_zro, mo=1)
            # rename constraint
            rt_utils.constraint_rename(pac_clav_constraint)

        # connect scale attribute
        cmds.connectAttr(build_clavicle.scale_x + '.scaleX', scale_jnt + '.scaleX')
        cmds.connectAttr(build_clavicle.scale_y + '.scaleY', scale_jnt + '.scaleY')
        cmds.connectAttr(build_clavicle.scale_z + '.scaleZ', scale_jnt + '.scaleZ')

        # parent joint scale
        cmds.parent(scale_jnt, self.clavicle_gimbal)
