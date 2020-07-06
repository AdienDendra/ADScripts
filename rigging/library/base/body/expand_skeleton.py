from __builtin__ import reload

import maya.cmds as mc

from rigging.library.utils import transform as tf
from rigging.tools import AD_utils as au

reload(tf)
reload(au)


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
                 # skin_joint_parent,
                 constraint_method=False
                 ):

        if add_joint:
            name_prefix = au.prefix_name(joint_add_target)
            if side in name_prefix:
                name_prefix = name_prefix.replace(side, '')

            # skinJnt = mc.duplicate(jointAddTarget)[0]
            # skinJoint = mc.rename(skinJnt, au.prefixName(namePrefix) + positionName + side + '_skn')

            # ADD GROUP FOR TRANSFORM
            driver_joint_duplicate = mc.duplicate(joint_add_target)[0]
            driver_joint_rename = mc.rename(driver_joint_duplicate,
                                            au.prefix_name(name_prefix) + position_name + side + '_jnt')

            mc.setAttr(driver_joint_rename+'.visibility', 1)

            self.group_expand_joint = tf.create_parent_transform(parent_list=[''],
                                                                 object=driver_joint_rename,
                                                                 match_position=driver_joint_rename,
                                                                 prefix=driver_joint_rename, suffix='jnt',
                                                                 side=side)
            # DUPLICATE FOR POSITION ADJUST JOINT
            driver_adjust_joint = mc.duplicate(driver_joint_rename)[0]
            mc.parent(driver_adjust_joint, driver_joint_rename)
            mc.setAttr((driver_adjust_joint + '.translate%s' % offset_translation_position), offset_value)
            driver_adjust_joint = mc.rename(driver_adjust_joint,
                                            au.prefix_name(name_prefix) + 'Adjust' + position_name + side + '_skn')


            # # CREATE TRANS SKIN JNT
            # adjust_skinning = mc.duplicate(driver_adjust_joint)[0]
            # adjust_skinning = mc.rename(adjust_skinning,
            #                             au.prefix_name(name_prefix) + 'Adjust' + position_name + side + '_skn')
            # mc.parent(adjust_skinning, driver_adjust_joint)

            # DUPLICATE FOR POSITION ADJUST JOINT
            # CREATE GRP TRANSFORM FOR THE JOINT
            self.grp_adjust_joint = tf.create_parent_transform(parent_list=[''],
                                                               object=driver_adjust_joint,
                                                               match_position=driver_adjust_joint,
                                                               prefix=driver_adjust_joint, suffix='skn',
                                                               side=side)
            # # MATCH POSITION JOINT AND SKIN
            # au.match_position(driver_adjust_joint, adjust_skinning)
            if constraint_method:
                # point constraint
                point_constraint = mc.pointConstraint(point_grp_driver[0], point_grp_driver[-1], self.group_expand_joint,
                                                      mo=1)

                # orient constraint
                orient_constraint = mc.orientConstraint(joint_driver_matrix, self.group_expand_joint, mo=1)

                # scale constraint
                scale_constraint = mc.scaleConstraint(scale_driver[0], scale_driver[-1], self.group_expand_joint, mo=1)

                # rename constraint
                au.constraint_rename([point_constraint[0], orient_constraint[0], scale_constraint[0]])

                # parent to skin grp
                mc.parent(self.group_expand_joint, joint_grp)
            else:
                mc.parent(self.group_expand_joint, point_grp_driver)

            # connecting node
            self.create_pair_blend(joint_driver_matrix=joint_driver_matrix,
                                   joint_driver_inverse_matrix=joint_driver_inverse_matrix,
                                   joint_add_target=driver_joint_rename,
                                   prefix=name_prefix, side=side, rotation=rotation,
                                   rotation_pair_blend=rotation_pair_blend,
                                   position_name=position_name)

            # connect the elbow pair blend
            mc.connectAttr(fk_ik_setup + '.%s%sExpand' % (controller_expand_name, position_name),
                           self.pair_blend + '.weight')

            # # HIDE JOINT DRIVER
            # mc.setAttr(driver_joint_rename+'.drawStyle', 2)

            # ADD TO SETS
            mc.sets(driver_adjust_joint, add='BODY_SKIN_LN')

            # # SKIN JOINT
            # # ADD GROUP FOR TRANSFORM
            #
            # # mc.parent(transSkin, skinJoint)
            # mc.parent(adjust_skinning, skin_joint_parent)
            # # au.parentScaleCons(driverJoint, skinJoint)
            # au.parent_scale_constraint(driver_adjust_joint, adjust_skinning)
            #
            # # mc.setAttr(skinJoint+'.visibility', 1)
            # mc.setAttr(adjust_skinning + '.visibility', 1)

    # ==================================================================================================================
    #                                               GENERAL FUNCTION
    # ==================================================================================================================

    def create_pair_blend(self, joint_driver_matrix, joint_driver_inverse_matrix, joint_add_target, prefix, side,
                          rotation, rotation_pair_blend, position_name):

        # getValueTxUpperObjJnt = mc.xform(joint_driver_inverse_matrix, ws=1, q=1, t=1)[0]

        mult_matrix = mc.createNode('multMatrix', n='%s%s%s%s_mmtx' % (prefix, position_name, 'BlendingShp', side))
        mc.connectAttr(joint_driver_matrix + '.worldMatrix[0]', mult_matrix + '.matrixIn[0]')
        mc.connectAttr(joint_driver_inverse_matrix + '.worldInverseMatrix[0]', mult_matrix + '.matrixIn[1]')

        # create decompose matrix
        decompose_matrix = mc.createNode('decomposeMatrix',
                                         n='%s%s%s%s_dmtx' % (prefix, position_name, 'BlendingShp', side))
        mc.connectAttr(mult_matrix + '.matrixSum', decompose_matrix + '.inputMatrix')

        # create quat to euler
        quat_to_euler = mc.createNode('quatToEuler', n='%s%s%s%s_qte' % (prefix, position_name, 'BlendingShp', side))
        mc.connectAttr(decompose_matrix + '.outputQuatW', quat_to_euler + '.inputQuatW')
        mc.connectAttr(decompose_matrix + '.outputQuat%s' % rotation, quat_to_euler + '.inputQuat%s' % rotation)

        # create add double linear
        add_double_linear = mc.createNode('addDoubleLinear',
                                          n='%s%s%s%s_adl' % (prefix, position_name, 'BlendingShp', side))
        mc.connectAttr(quat_to_euler + '.outputRotate%s' % rotation, add_double_linear + '.input1')
        valueInput1 = mc.getAttr(add_double_linear + '.input1')
        mc.setAttr(add_double_linear + '.input2', valueInput1 * -1)

        # create mult double linear
        mult_double_linear = mc.createNode('multDoubleLinear',
                                           n='%s%s%s%s_mdl' % (prefix, position_name, 'BlendingShp', side))
        mc.connectAttr(add_double_linear + '.output', mult_double_linear + '.input1')
        mc.setAttr(mult_double_linear + '.input2', -1)

        # create pair blend
        self.pair_blend = mc.createNode('pairBlend', n='%s%s%s%s_pbn' % (prefix, position_name, 'BlendingShp', side))
        mc.setAttr(self.pair_blend + '.weight', 0.5)
        mc.connectAttr(mult_double_linear + '.output',
                       self.pair_blend + '.inRotate%s%s' % (rotation, rotation_pair_blend))

        if mc.listConnections(joint_add_target + '.rotate%s' % rotation, d=False, s=True) == None:
            mc.connectAttr(self.pair_blend + '.outRotate%s' % rotation, joint_add_target + '.rotate%s' % rotation)
        else:
            return self.pair_blend
