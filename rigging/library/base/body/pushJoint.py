from __future__ import absolute_import

import maya.cmds as cmds

from rigging.library.utils import transform as rlu_transform
from rigging.tools import utils as rt_utils


class Build:
    def __init__(self,
                 add_joint,
                 fk_ik_setup,
                 controller_expand_name,
                 joint_driver_matrix,
                 joint_add_target,
                 joint_driver_inverse_matrix,
                 point_grp_driver,
                 side,
                 joint_grp,
                 rotation,
                 scale_driver,
                 rotation_pair_blend,
                 offset_translation_position,
                 offset_value,
                 position_name,
                 constraint_method=False
                 ):

        if add_joint:
            name_prefix = rt_utils.prefix_name(joint_add_target)
            if side in name_prefix:
                name_prefix = name_prefix.replace(side, '')

            # ADD GROUP FOR TRANSFORM
            driver_joint_duplicate = cmds.duplicate(joint_add_target)[0]
            driver_joint_rename = cmds.rename(driver_joint_duplicate,
                                              rt_utils.prefix_name(name_prefix) + position_name + side + '_jnt')

            cmds.setAttr(driver_joint_rename + '.visibility', 1)

            self.group_expand_joint = rlu_transform.create_parent_transform(parent_list=[''],
                                                                            object=driver_joint_rename,
                                                                            match_position=driver_joint_rename,
                                                                            prefix=driver_joint_rename, suffix='jnt',
                                                                            side=side)
            # DUPLICATE FOR POSITION ADJUST JOINT
            driver_adjust_joint = cmds.duplicate(driver_joint_rename)[0]
            cmds.parent(driver_adjust_joint, driver_joint_rename)
            cmds.setAttr((driver_adjust_joint + '.translate%s' % offset_translation_position), offset_value)
            driver_adjust_joint = cmds.rename(driver_adjust_joint,
                                              rt_utils.prefix_name(
                                                  name_prefix) + 'Adjust' + position_name + side + '_skn')

            # DUPLICATE FOR POSITION ADJUST JOINT
            # CREATE GRP TRANSFORM FOR THE JOINT
            self.grp_adjust_joint = rlu_transform.create_parent_transform(parent_list=[''],
                                                                          object=driver_adjust_joint,
                                                                          match_position=driver_adjust_joint,
                                                                          prefix=driver_adjust_joint, suffix='skn',
                                                                          side=side)

            if constraint_method:
                # point constraint
                point_constraint = cmds.pointConstraint(point_grp_driver[0], point_grp_driver[-1],
                                                        self.group_expand_joint,
                                                        mo=1)

                # orient constraint
                orient_constraint = cmds.orientConstraint(joint_driver_matrix, self.group_expand_joint, mo=1)

                # scale constraint
                scale_constraint = cmds.scaleConstraint(scale_driver[0], scale_driver[-1], self.group_expand_joint,
                                                        mo=1)

                # rename constraint
                rt_utils.constraint_rename([point_constraint[0], orient_constraint[0], scale_constraint[0]])

                # parent to skin grp
                cmds.parent(self.group_expand_joint, joint_grp)
            else:
                cmds.parent(self.group_expand_joint, point_grp_driver)

            # connecting node
            self.create_pair_blend(joint_driver_matrix=joint_driver_matrix,
                                   joint_driver_inverse_matrix=joint_driver_inverse_matrix,
                                   joint_add_target=driver_joint_rename,
                                   prefix=name_prefix, side=side, rotation=rotation,
                                   rotation_pair_blend=rotation_pair_blend,
                                   position_name=position_name)

            # connect the elbow pair blend
            cmds.connectAttr(fk_ik_setup + '.%s%sExpand' % (controller_expand_name, position_name),
                             self.pair_blend + '.weight')

            # ADD TO SETS
            if cmds.objExists('BODY_SKIN_LN'):
                cmds.sets(driver_adjust_joint, add='BODY_SKIN_LN')
            else:
                pass

    # ==================================================================================================================
    #                                               GENERAL FUNCTION
    # ==================================================================================================================

    def create_pair_blend(self, joint_driver_matrix, joint_driver_inverse_matrix, joint_add_target, prefix, side,
                          rotation, rotation_pair_blend, position_name):

        mult_matrix = cmds.createNode('multMatrix', n='%s%s%s%s_mmtx' % (prefix, position_name, 'BlendingShp', side))
        cmds.connectAttr(joint_driver_matrix + '.worldMatrix[0]', mult_matrix + '.matrixIn[0]')
        cmds.connectAttr(joint_driver_inverse_matrix + '.worldInverseMatrix[0]', mult_matrix + '.matrixIn[1]')

        # create decompose matrix
        decompose_matrix = cmds.createNode('decomposeMatrix',
                                           n='%s%s%s%s_dmtx' % (prefix, position_name, 'BlendingShp', side))
        cmds.connectAttr(mult_matrix + '.matrixSum', decompose_matrix + '.inputMatrix')

        # create quat to euler
        quat_to_euler = cmds.createNode('quatToEuler', n='%s%s%s%s_qte' % (prefix, position_name, 'BlendingShp', side))
        cmds.connectAttr(decompose_matrix + '.outputQuatW', quat_to_euler + '.inputQuatW')
        cmds.connectAttr(decompose_matrix + '.outputQuat%s' % rotation, quat_to_euler + '.inputQuat%s' % rotation)

        # create add double linear
        add_double_linear = cmds.createNode('addDoubleLinear',
                                            n='%s%s%s%s_adl' % (prefix, position_name, 'BlendingShp', side))
        cmds.connectAttr(quat_to_euler + '.outputRotate%s' % rotation, add_double_linear + '.input1')
        valueInput1 = cmds.getAttr(add_double_linear + '.input1')
        cmds.setAttr(add_double_linear + '.input2', valueInput1 * -1)

        # create mult double linear
        mult_double_linear = cmds.createNode('multDoubleLinear',
                                             n='%s%s%s%s_mdl' % (prefix, position_name, 'BlendingShp', side))
        cmds.connectAttr(add_double_linear + '.output', mult_double_linear + '.input1')
        cmds.setAttr(mult_double_linear + '.input2', -1)

        # create pair blend
        self.pair_blend = cmds.createNode('pairBlend', n='%s%s%s%s_pbn' % (prefix, position_name, 'BlendingShp', side))
        cmds.setAttr(self.pair_blend + '.weight', 0.5)
        cmds.connectAttr(mult_double_linear + '.output',
                         self.pair_blend + '.inRotate%s%s' % (rotation, rotation_pair_blend))

        if cmds.listConnections(joint_add_target + '.rotate%s' % rotation, d=False, s=True) == None:
            cmds.connectAttr(self.pair_blend + '.outRotate%s' % rotation, joint_add_target + '.rotate%s' % rotation)
        else:
            return self.pair_blend
