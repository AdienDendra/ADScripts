from __builtin__ import reload

import maya.cmds as mc

from rigging.library.utils import controller as ct
from rigging.library.utils import transform as tf
from rigging.tools import AD_utils as au

reload (ct)
reload (tf)
reload (au)


class Bulge:
    def __init__(self,
                 face_utils_grp,
                 face_anim_ctrl_grp,
                 cheek_bulge_jnt_LFT,
                 cheek_bulge_prefix,
                 brow_in_bulge_prefix,
                 brow_out_bulge_prefix,
                 corner_mouth_bulge_prefix,
                 nose_bulge_prefix,
                 chin_bulge_prefix,
                 cheek_bulge_jnt_RGT,
                 brow_in_bulge_jnt_LFT,
                 brow_in_bulge_jnt_RGT,
                 brow_out_bulge_jnt_LFT,
                 brow_out_bulge_jnt_RGT,
                 corner_mouth_bulge_jnt_LFT,
                 corner_mouth_bulge_jnt_RGT,
                 nose_bulge_jnt,
                 chin_bulge_jnt,
                 bulge_mesh,
                 side_LFT,
                 side_RGT,
                 head_up_ctrl_gimbal,
                 head_low_ctrl_gimbal,
                 nose_drv03_ctrl,
                 chin_ctrl,
                 corner_mouth_ctrl_LFT,
                 corner_mouth_ctrl_RGT,
                 scale,
                 add_set):

        bulge_grp = mc.group(em=1, n='bulgeHandle_grp')
        mc.parent(bulge_grp, face_utils_grp)

        cheek_bulge_ctrl_LFT = self.bulge_ctrl(bulge_position=cheek_bulge_jnt_LFT, bulge_prefix=cheek_bulge_prefix,
                                               side=side_LFT, scale=scale)

        cheek_bulge_ctrl_RGT = self.bulge_ctrl(bulge_position=cheek_bulge_jnt_RGT, bulge_prefix=cheek_bulge_prefix,
                                               side=side_RGT, scale=scale)

        brow_in_bulge_ctrl_LFT = self.bulge_ctrl(bulge_position=brow_in_bulge_jnt_LFT,
                                                 bulge_prefix=brow_in_bulge_prefix,
                                                 side=side_LFT, scale=scale)

        brow_in_bulge_ctrl_RGT = self.bulge_ctrl(bulge_position=brow_in_bulge_jnt_RGT,
                                                 bulge_prefix=brow_in_bulge_prefix,
                                                 side=side_RGT, scale=scale)

        brow_out_bulge_ctrl_LFT = self.bulge_ctrl(bulge_position=brow_out_bulge_jnt_LFT,
                                                  bulge_prefix=brow_out_bulge_prefix,
                                                  side=side_LFT, scale=scale)

        brow_out_bulge_ctrl_RGT = self.bulge_ctrl(bulge_position=brow_out_bulge_jnt_RGT,
                                                  bulge_prefix=brow_out_bulge_prefix,
                                                  side=side_RGT, scale=scale)

        corner_mouth_bulge_ctrl_LFT = self.bulge_ctrl(bulge_position=corner_mouth_bulge_jnt_LFT,
                                                      bulge_prefix=corner_mouth_bulge_prefix,
                                                      side=side_LFT, scale=scale)

        corner_mouth_bulge_ctrl_RGT = self.bulge_ctrl(bulge_position=corner_mouth_bulge_jnt_RGT,
                                                      bulge_prefix=corner_mouth_bulge_prefix,
                                                      side=side_RGT, scale=scale)

        nose_bulge_ctrl = self.bulge_ctrl(bulge_position=nose_bulge_jnt, bulge_prefix=nose_bulge_prefix,
                                          side=side_LFT, scale=scale)

        chin_bulge_ctrl = self.bulge_ctrl(bulge_position=chin_bulge_jnt, bulge_prefix=chin_bulge_prefix,
                                          side=side_RGT, scale=scale)

        self.cheek_bulge_ctrl_LFT_grp = cheek_bulge_ctrl_LFT[2]
        self.cheek_bulge_ctrl_RGT_grp = cheek_bulge_ctrl_RGT[2]
        self.brow_in_bulge_ctrl_LFT_grp = brow_in_bulge_ctrl_LFT[2]
        self.brow_in_bulge_ctrl_RGT_grp = brow_in_bulge_ctrl_RGT[2]
        self.brow_out_bulge_ctrl_LFT_grp = brow_out_bulge_ctrl_LFT[2]
        self.brow_out_bulge_ctrl_RGT_grp = brow_out_bulge_ctrl_RGT[2]
        self.corner_mouth_bulge_ctrl_LFT_grp = corner_mouth_bulge_ctrl_LFT[2]
        self.corner_mouth_bulge_ctrl_RGT_grp = corner_mouth_bulge_ctrl_RGT[2]
        self.nose_bulge_ctrl_grp = nose_bulge_ctrl[2]
        self.chin_bulge_ctrl_grp = chin_bulge_ctrl[2]

        # SOFT NODE

        self.soft_mod_node(bulge_jnt=cheek_bulge_jnt_LFT, bulge_prefix=cheek_bulge_prefix,
                           bulge_slide_ctrl_parent=cheek_bulge_ctrl_LFT[2],
                           bulge_slide_ctrl=cheek_bulge_ctrl_LFT[1], bulge_soft_mod_ctrl=cheek_bulge_ctrl_LFT[0],
                           bulge_mesh=bulge_mesh, side=side_LFT, add_set=add_set, bulge_grp=bulge_grp)

        self.soft_mod_node(bulge_jnt=cheek_bulge_jnt_RGT, bulge_prefix=cheek_bulge_prefix,
                           bulge_slide_ctrl_parent=cheek_bulge_ctrl_RGT[2],
                           bulge_slide_ctrl=cheek_bulge_ctrl_RGT[1], bulge_soft_mod_ctrl=cheek_bulge_ctrl_RGT[0],
                           bulge_mesh=bulge_mesh, side=side_RGT, add_set=add_set, bulge_grp=bulge_grp)

        self.soft_mod_node(bulge_jnt=brow_in_bulge_jnt_LFT, bulge_prefix=brow_in_bulge_prefix,
                           bulge_slide_ctrl_parent=brow_in_bulge_ctrl_LFT[2],
                           bulge_slide_ctrl=brow_in_bulge_ctrl_LFT[1], bulge_soft_mod_ctrl=brow_in_bulge_ctrl_LFT[0],
                           bulge_mesh=bulge_mesh, side=side_LFT, add_set=add_set, bulge_grp=bulge_grp)

        self.soft_mod_node(bulge_jnt=brow_in_bulge_jnt_RGT, bulge_prefix=brow_in_bulge_prefix,
                           bulge_slide_ctrl_parent=brow_in_bulge_ctrl_RGT[2],
                           bulge_slide_ctrl=brow_in_bulge_ctrl_RGT[1], bulge_soft_mod_ctrl=brow_in_bulge_ctrl_RGT[0],
                           bulge_mesh=bulge_mesh, side=side_RGT, add_set=add_set, bulge_grp=bulge_grp)

        self.soft_mod_node(bulge_jnt=brow_out_bulge_jnt_LFT, bulge_prefix=brow_out_bulge_prefix,
                           bulge_slide_ctrl_parent=brow_out_bulge_ctrl_LFT[2],
                           bulge_slide_ctrl=brow_out_bulge_ctrl_LFT[1], bulge_soft_mod_ctrl=brow_out_bulge_ctrl_LFT[0],
                           bulge_mesh=bulge_mesh, side=side_LFT, add_set=add_set, bulge_grp=bulge_grp)

        self.soft_mod_node(bulge_jnt=brow_out_bulge_jnt_RGT, bulge_prefix=brow_out_bulge_prefix,
                           bulge_slide_ctrl_parent=brow_out_bulge_ctrl_RGT[2],
                           bulge_slide_ctrl=brow_out_bulge_ctrl_RGT[1], bulge_soft_mod_ctrl=brow_out_bulge_ctrl_RGT[0],
                           bulge_mesh=bulge_mesh, side=side_RGT, add_set=add_set, bulge_grp=bulge_grp)

        self.soft_mod_node(bulge_jnt=corner_mouth_bulge_jnt_LFT, bulge_prefix=corner_mouth_bulge_prefix,
                           bulge_slide_ctrl_parent=corner_mouth_bulge_ctrl_LFT[2],
                           bulge_slide_ctrl=corner_mouth_bulge_ctrl_LFT[1],
                           bulge_soft_mod_ctrl=corner_mouth_bulge_ctrl_LFT[0],
                           bulge_mesh=bulge_mesh, side=side_LFT, add_set=add_set, bulge_grp=bulge_grp)

        self.soft_mod_node(bulge_jnt=corner_mouth_bulge_jnt_RGT, bulge_prefix=corner_mouth_bulge_prefix,
                           bulge_slide_ctrl_parent=corner_mouth_bulge_ctrl_RGT[2],
                           bulge_slide_ctrl=corner_mouth_bulge_ctrl_RGT[1],
                           bulge_soft_mod_ctrl=corner_mouth_bulge_ctrl_RGT[0],
                           bulge_mesh=bulge_mesh, side=side_RGT, add_set=add_set, bulge_grp=bulge_grp)

        self.soft_mod_node(bulge_jnt=nose_bulge_jnt, bulge_prefix=nose_bulge_prefix,
                           bulge_slide_ctrl_parent=nose_bulge_ctrl[2],
                           bulge_slide_ctrl=nose_bulge_ctrl[1], bulge_soft_mod_ctrl=nose_bulge_ctrl[0],
                           bulge_mesh=bulge_mesh, add_set=add_set, bulge_grp=bulge_grp)

        self.soft_mod_node(bulge_jnt=chin_bulge_jnt, bulge_prefix=chin_bulge_prefix,
                           bulge_slide_ctrl_parent=chin_bulge_ctrl[2],
                           bulge_slide_ctrl=chin_bulge_ctrl[1], bulge_soft_mod_ctrl=chin_bulge_ctrl[0],
                           bulge_mesh=bulge_mesh, add_set=add_set, bulge_grp=bulge_grp)

        # PARENT CONSTRAINT
        cheek_bulge_LFT = mc.parentConstraint(head_up_ctrl_gimbal, head_low_ctrl_gimbal, cheek_bulge_ctrl_LFT[2], mo=1)[
            0]
        cheek_bulge_RGT = mc.parentConstraint(head_up_ctrl_gimbal, head_low_ctrl_gimbal, cheek_bulge_ctrl_RGT[2], mo=1)[
            0]
        mc.setAttr(cheek_bulge_LFT + '.interpType', 2)
        mc.setAttr(cheek_bulge_RGT + '.interpType', 2)
        scale_cheek_bulge_LFT = mc.scaleConstraint(head_up_ctrl_gimbal, head_low_ctrl_gimbal, cheek_bulge_ctrl_LFT[3],
                                                   mo=1)
        scale_cheek_bulge_RGT = mc.scaleConstraint(head_up_ctrl_gimbal, head_low_ctrl_gimbal, cheek_bulge_ctrl_RGT[3],
                                                   mo=1)

        # PARENT
        mc.parent(cheek_bulge_ctrl_LFT[2], cheek_bulge_ctrl_RGT[2], face_anim_ctrl_grp)
        mc.parent(brow_in_bulge_ctrl_LFT[2], brow_in_bulge_ctrl_RGT[2], brow_out_bulge_ctrl_LFT[2],
                  brow_out_bulge_ctrl_RGT[2], head_up_ctrl_gimbal)
        mc.parent(nose_bulge_ctrl[2], nose_drv03_ctrl)
        mc.parent(chin_bulge_ctrl[2], chin_ctrl)
        mc.parent(corner_mouth_bulge_ctrl_LFT[2], corner_mouth_ctrl_LFT)
        mc.parent(corner_mouth_bulge_ctrl_RGT[2], corner_mouth_ctrl_RGT)

        # constraint rename
        au.constraint_rename([cheek_bulge_LFT, cheek_bulge_RGT, scale_cheek_bulge_LFT[0], scale_cheek_bulge_RGT[0]])

    def soft_mod_node(self, bulge_jnt, bulge_prefix, bulge_slide_ctrl, bulge_soft_mod_ctrl, bulge_slide_ctrl_parent,
                      bulge_grp, bulge_mesh, add_set, side='',
                      ):

        self.posX = mc.xform(bulge_jnt, q=1, ws=1, t=1)[0]
        self.posY = mc.xform(bulge_jnt, q=1, ws=1, t=1)[1]
        self.posZ = mc.xform(bulge_jnt, q=1, ws=1, t=1)[2]

        reverse_slide_trans_mdn = mc.createNode('multiplyDivide', n=bulge_prefix + 'BulgeRevSlide' + side + '_mdn')
        reverse_soft_mod_trans_mdn = mc.createNode('multiplyDivide', n=bulge_prefix + 'BulgeRevSoftMod' + side + '_mdn')

        pma_node = mc.createNode('plusMinusAverage', n=bulge_prefix + 'Bulge' + side + '_pma')

        soft_mod = mc.softMod(bulge_mesh, n=bulge_prefix + 'Bulge' + side + '_mod',
                              fc=[self.posX, self.posY, self.posZ])

        if self.posX < 0:
            mc.setAttr(bulge_slide_ctrl_parent + '.scaleX', -1)

            mc.setAttr(reverse_slide_trans_mdn + '.input2X', -1)
            mc.setAttr(reverse_slide_trans_mdn + '.input2Y', 1)
            mc.setAttr(reverse_slide_trans_mdn + '.input2Z', 1)

            mc.setAttr(reverse_soft_mod_trans_mdn + '.input2X', -1)
            mc.setAttr(reverse_soft_mod_trans_mdn + '.input2Y', 1)
            mc.setAttr(reverse_soft_mod_trans_mdn + '.input2Z', 1)

        else:
            mc.setAttr(reverse_slide_trans_mdn + '.input2X', 1)
            mc.setAttr(reverse_slide_trans_mdn + '.input2Y', 1)
            mc.setAttr(reverse_slide_trans_mdn + '.input2Z', 1)

            mc.setAttr(reverse_soft_mod_trans_mdn + '.input2X', 1)
            mc.setAttr(reverse_soft_mod_trans_mdn + '.input2Y', 1)
            mc.setAttr(reverse_soft_mod_trans_mdn + '.input2Z', 1)

        mc.connectAttr(bulge_slide_ctrl + '.translate', reverse_slide_trans_mdn + '.input1')
        mc.connectAttr(reverse_slide_trans_mdn + '.output', pma_node + '.input3D[0]')

        mc.setAttr(pma_node + '.input3D[1].input3Dx', self.posX)
        mc.setAttr(pma_node + '.input3D[1].input3Dy', self.posY)
        mc.setAttr(pma_node + '.input3D[1].input3Dz', self.posZ)

        mc.connectAttr(pma_node + '.output3D', soft_mod[0] + '.falloffCenter')
        mc.connectAttr(bulge_soft_mod_ctrl + '.%s' % self.wide, soft_mod[0] + '.falloffRadius')
        mc.connectAttr(bulge_soft_mod_ctrl + '.%s' % self.bulge, soft_mod[0] + '.envelope')

        # CONNECT CTRL TO HANDLE
        mc.connectAttr(bulge_soft_mod_ctrl + '.translate', reverse_soft_mod_trans_mdn + '.input1')

        mc.connectAttr(reverse_soft_mod_trans_mdn + '.output', soft_mod[1] + '.translate')

        # HIDE
        mc.hide(soft_mod[1])

        # ADD SET LIST OBJECT
        if add_set:
            for i in add_set:
                setObj = mc.listConnections(soft_mod[0], type='objectSet')[0]
                mc.sets(i, add=setObj)

        # PARENT TO THE GRP
        mc.parent(soft_mod[1], bulge_grp)

        return soft_mod[1]

    def bulge_ctrl(self, bulge_position,
                   bulge_prefix,
                   scale,
                   side=''):

        # SOFT MOD BULGE
        bulge_soft_mod_ctrl = ct.Control(prefix=bulge_prefix + 'Bulge',
                                         shape=ct.LOCATOR, groups_ctrl=[''], ctrl_size=scale * 0.12,
                                         ctrl_color='turquoiseBlue', lock_channels=['v', 's', 'r'], side=side
                                         )
        # POSITION

        # ADD ATTRIBUTE
        au.add_attribute(objects=[bulge_soft_mod_ctrl.control], long_name=['setup'], nice_name=[' '], at="enum",
                         en='Setup', channel_box=True)

        self.wide = au.add_attribute(objects=[bulge_soft_mod_ctrl.control], long_name=['wide'],
                                     attributeType="float", min=0, dv=0.25, keyable=True)

        self.bulge = au.add_attribute(objects=[bulge_soft_mod_ctrl.control], long_name=['bulge'],
                                      attributeType="float", min=0, max=1, dv=1, keyable=True)


        # SLIDE BULGE
        bulge_slide_ctrl = ct.Control(prefix=bulge_prefix + 'BulgeSlide',
                                      shape=ct.JOINT, groups_ctrl=['', 'Offset'], ctrl_size=scale * 0.1,
                                      ctrl_color='yellow', lock_channels=['v', 's', 'r'], side=side
                                      )

        # PARENT
        # mc.parent(bulgeSlideCtrl.parentControl[0], bulgeSoftModCtrl.control)
        mc.parent(bulge_soft_mod_ctrl.parent_control[0], bulge_slide_ctrl.control)

        mc.delete(mc.pointConstraint(bulge_position, bulge_slide_ctrl.parent_control[0]))

        return bulge_soft_mod_ctrl.control, bulge_slide_ctrl.control, bulge_slide_ctrl.parent_control[0], \
               bulge_slide_ctrl.parent_control[1]
