from __builtin__ import reload

import maya.OpenMaya as om
import maya.cmds as mc
import pymel.core as pm
import rigging.library.utils.pole_vector as pv
import rigging.tools.AD_utils as au

reload(au)
reload(pv)


class Snapping:
    def __init__(self, fkik_arm_LFT_setup, fkik_arm_RGT_setup, fkik_leg_LFT_setup, fkik_leg_RGT_setup):

        # listing fk ik setup selection
        fkik_ctrl_select = mc.ls(sl=1)
        self.fkik_ctrl_select = fkik_ctrl_select

        # query the reference or not
        query_reference = pm.selected()[0].namespace()

        # assign as instance fkik leg setup
        if query_reference:
            self.fkik_arm_LFT_setup = query_reference+fkik_arm_LFT_setup
            self.fkik_arm_RGT_setup = query_reference+fkik_arm_RGT_setup
            self.fkik_leg_LFT_setup = query_reference+fkik_leg_LFT_setup
            self.fkik_leg_RGT_setup = query_reference+fkik_leg_RGT_setup
        else:
            self.fkik_arm_LFT_setup = fkik_arm_LFT_setup
            self.fkik_arm_RGT_setup = fkik_arm_RGT_setup
            self.fkik_leg_LFT_setup = fkik_leg_LFT_setup
            self.fkik_leg_RGT_setup = fkik_leg_RGT_setup

        # condition selection fkik setup selection
        if len(fkik_ctrl_select) == 0:
            mc.error('please select one only the controller fkik setup')

        elif len(fkik_ctrl_select) == 1:
            upper_limb_fk_jnt = mc.listConnections(fkik_ctrl_select[0] + '.upper_limb_fk_jnt')[0]
            middle_limb_fk_jnt = mc.listConnections(fkik_ctrl_select[0] + '.middle_limb_fk_jnt')[0]
            lower_limb_fk_jnt = mc.listConnections(fkik_ctrl_select[0] + '.lower_limb_fk_jnt')[0]
            upper_limb_ik_ctrl = mc.listConnections(fkik_ctrl_select[0] + '.upper_limb_ik_ctrl')[0]
            poleVector_ctrl = mc.listConnections(fkik_ctrl_select[0] + '.poleVector_ctrl')[0]
            lower_limb_ik_ctrl = mc.listConnections(fkik_ctrl_select[0] + '.lower_limb_ik_ctrl')[0]

            upper_limb_ik_jnt = mc.listConnections(fkik_ctrl_select[0] + '.upper_limb_ik_jnt')[0]
            middle_limb_ik_jnt = mc.listConnections(fkik_ctrl_select[0] + '.middle_limb_ik_jnt')[0]
            lower_limb_ik_jnt = mc.listConnections(fkik_ctrl_select[0] + '.lower_limb_ik_jnt')[0]
            upper_limb_fk_ctrl = mc.listConnections(fkik_ctrl_select[0] + '.upper_limb_fk_ctrl')[0]
            middle_limb_fk_ctrl = mc.listConnections(fkik_ctrl_select[0] + '.middle_limb_fk_ctrl')[0]
            lower_limb_fk_ctrl = mc.listConnections(fkik_ctrl_select[0] + '.lower_limb_fk_ctrl')[0]

            if fkik_ctrl_select[0] == self.fkik_arm_LFT_setup or fkik_ctrl_select[0] == self.fkik_arm_RGT_setup:

                self.snap_to_fk(up_pos=upper_limb_fk_jnt, mid_pos=middle_limb_fk_jnt,
                                low_pos=lower_limb_fk_jnt,
                                controller_up_ik=upper_limb_ik_ctrl,
                                controller_poleVector_ik=poleVector_ctrl,
                                controller_low_ik=lower_limb_ik_ctrl)


                self.snap_to_ik(up_pos=upper_limb_ik_jnt, mid_pos=middle_limb_ik_jnt,
                                low_pos=lower_limb_ik_jnt,
                                controller_up_fk=upper_limb_fk_ctrl,
                                controller_mid_fk=middle_limb_fk_ctrl,
                                controller_low_fk=lower_limb_fk_ctrl)

            elif fkik_ctrl_select[0] == self.fkik_leg_LFT_setup or fkik_ctrl_select[0] == self.fkik_leg_RGT_setup:
                end_limb_fk_jnt = mc.listConnections(fkik_ctrl_select[0] + '.end_limb_fk_jnt')[0]
                end_limb_ik_jnt = mc.listConnections(fkik_ctrl_select[0] + '.end_limb_ik_jnt')[0]
                end_limb_fk_ctrl = mc.listConnections(fkik_ctrl_select[0] + '.end_limb_fk_ctrl')[0]
                toe_wiggle_attr = mc.listConnections(fkik_ctrl_select[0] + '.toe_wiggle_attr')[0]

                self.snap_to_fk(up_pos=upper_limb_fk_jnt, mid_pos=middle_limb_fk_jnt,
                                low_pos=lower_limb_fk_jnt,
                                controller_up_ik=upper_limb_ik_ctrl,
                                controller_poleVector_ik=poleVector_ctrl,
                                controller_low_ik=lower_limb_ik_ctrl,
                                toe_wiggle_attr=toe_wiggle_attr, end_pos=end_limb_fk_jnt
                                )

                self.snap_to_ik(up_pos=upper_limb_ik_jnt, mid_pos=middle_limb_ik_jnt,
                                low_pos=lower_limb_ik_jnt,
                                controller_up_fk=upper_limb_fk_ctrl,
                                controller_mid_fk=middle_limb_fk_ctrl,
                                controller_low_fk=lower_limb_fk_ctrl,
                                controller_end_fk=end_limb_fk_ctrl, toe_wiggle_attr=toe_wiggle_attr,
                                end_pos=end_limb_ik_jnt)

            else:
                mc.error('please select the the controller fkik arm or fkik leg ctrl setup')
        else:
            mc.error('only one selection the controller fkik setup can be proceed')
    def snap_to_fk(self, up_pos, mid_pos, low_pos, controller_up_ik, controller_poleVector_ik, controller_low_ik,
                   toe_wiggle_attr=None, end_pos=None):
        # root position
        get_up_query = mc.xform(up_pos, ws=1, q=1, t=1)
        get_up_position = om.MVector(get_up_query[0], get_up_query[1], get_up_query[2])

        # mid position
        up_joint_position = mc.xform(up_pos, q=1, ws=1, t=1)
        mid_joint_position = mc.xform(mid_pos, q=1, ws=1, t=1)
        low_joint_position = mc.xform(low_pos, q=1, ws=1, t=1)
        get_poleVector_position = pv.get_poleVector_position(up_joint_position, mid_joint_position, low_joint_position)

        # low position
        get_low_query = mc.xform(low_pos, ws=1, q=1, t=1)
        get_low_position = om.MVector(get_low_query[0], get_low_query[1], get_low_query[2])

        # move the controller
        move_controller_up_ik = mc.move(get_up_position.x, get_up_position.y, get_up_position.z, controller_up_ik)
        move_controller_polvec_ik = mc.move(get_poleVector_position.x, get_poleVector_position.y,
                                            get_poleVector_position.z, controller_poleVector_ik)
        move_controller_low_ik = mc.move(get_low_position.x, get_low_position.y, get_low_position.z, controller_low_ik)

        if self.fkik_ctrl_select[0] == self.fkik_leg_LFT_setup or self.fkik_ctrl_select[0] == self.fkik_leg_RGT_setup:
            if toe_wiggle_attr:
                # end position
                get_end_query = mc.getAttr(end_pos + '.rotateX')
                move_controller_end_ik = mc.setAttr('%s.toeWiggle' % (toe_wiggle_attr), get_end_query)

        mc.setAttr(self.fkik_ctrl_select[0]+'.FkIk', 1)

    def snap_to_ik(self, up_pos, mid_pos, low_pos, controller_up_fk, controller_mid_fk, controller_low_fk,
                   controller_end_fk=None, toe_wiggle_attr=None, end_pos=None):
        # root position
        get_up_query = mc.xform(up_pos, ws=1, q=1, t=1)
        get_up_position = om.MVector(get_up_query[0], get_up_query[1], get_up_query[2])

        # mid position
        get_mid_query = mc.xform(mid_pos, ws=1, q=1, t=1)
        get_mid_position = om.MVector(get_mid_query[0], get_mid_query[1], get_mid_query[2])

        # low position
        get_low_query = mc.xform(low_pos, ws=1, q=1, t=1)
        get_low_position = om.MVector(get_low_query[0], get_low_query[1], get_low_query[2])

        # move the controller
        move_controller_up_fk = mc.move(get_up_position.x, get_up_position.y, get_up_position.z, controller_up_fk)
        move_controller_mid_fk = mc.move(get_mid_position.x, get_mid_position.y, get_mid_position.z, controller_mid_fk)
        move_controller_low_fk = mc.move(get_low_position.x, get_low_position.y, get_low_position.z, controller_low_fk)

        if self.fkik_ctrl_select[0] == self.fkik_leg_LFT_setup or self.fkik_ctrl_select[0] == self.fkik_leg_RGT_setup:
            if toe_wiggle_attr:
                # end position
                get_end_query = mc.getAttr(end_pos + '.rotateX')
                move_controller_end_ik = mc.setAttr('%s.rotateX' % (controller_end_fk), get_end_query)

        mc.setAttr(self.fkik_ctrl_select[0]+'.FkIk', 0)
