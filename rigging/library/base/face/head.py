from __builtin__ import reload

import maya.cmds as mc

from rigging.library.utils import controller as ct
from rigging.library.utils import transform as tf
from rigging.tools import AD_utils as au

reload (ct)
reload (tf)
reload (au)


class Build:
    def __init__(self,
                 neckJnt,
                 neckInBtwJnt,
                 headJnt,
                 jawTipJnt,
                 jawJnt,
                 headUpJnt,
                 headLowJnt,
                 jawPrefix,
                 jawTipPrefix,
                 prefixHead,
                 prefixHeadUp,
                 prefixHeadLow,
                 prefixNeck,
                 prefixInBtwNeck,
                 scale,
                 upperTeethJnt,
                 lowerTeethJnt,
                 tongue01Jnt,
                 tongue02Jnt,
                 tongue03Jnt,
                 tongue04Jnt,
                 suffixController
                 ):

        # create group jaw
        jawDirectionGrp = mc.group(em=1, n=au.prefix_name(jawJnt) + 'Direction_grp')
        jawDirectionOffsetGrp = mc.group(em=1, n=au.prefix_name(jawJnt) + 'DirectionOffset_grp', p=jawDirectionGrp)
        self.jawDirectionOffsetGrp = jawDirectionOffsetGrp

        mc.select(cl=1)
        mc.delete(mc.parentConstraint(jawJnt, jawDirectionGrp))

        ## GROUPING THE JOINT
        self.neckJntGrp= tf.create_parent_transform(parent_list=[''], object=neckJnt, match_position=neckJnt,
                                                    prefix=prefixNeck, suffix='_jnt')

        self.neckInBtwJntGrp= tf.create_parent_transform(parent_list=[''], object=neckInBtwJnt, match_position=neckInBtwJnt,
                                                         prefix=prefixInBtwNeck, suffix='_jnt')

        tf.create_parent_transform(parent_list=[''], object=headJnt, match_position=headJnt,
                                   prefix=prefixHead, suffix='_jnt')
        tf.create_parent_transform(parent_list=[''], object=headUpJnt, match_position=headUpJnt,
                                   prefix=prefixHeadUp, suffix='_jnt')
        tf.create_parent_transform(parent_list=[''], object=headLowJnt, match_position=headLowJnt,
                                   prefix=prefixHeadLow, suffix='_jnt')
        tf.create_parent_transform(parent_list=[''], object=jawJnt, match_position=jawJnt,
                                   prefix=jawPrefix, suffix='_jnt')
        self.jawTipGrp=tf.create_parent_transform(parent_list=['', 'Offset'], object=jawTipJnt, match_position=jawTipJnt,
                                                  prefix=jawTipPrefix, suffix='_jnt')

        ## CREATE CONTROLLER FOR THE JOINT

        self.neckCtrl = ct.Control(match_obj_first_position=neckJnt, prefix=prefixNeck,
                                   shape=ct.CIRCLEPLUS,
                                   groups_ctrl=['All', 'Offset'], ctrl_size=scale * 1.0,
                                   ctrl_color='red', lock_channels=['v'], gimbal=True, suffix=suffixController,
                                   connection=['connectMatrixAll'])
        au.add_attribute(objects=[self.neckCtrl.control], long_name=['neckInBetween'],
                         nice_name=[' '], at="enum",
                         en='Neck In Btw', channel_box=True)
        inBtwAttr = au.add_attribute(objects=[self.neckCtrl.control], long_name=['neckInBtwn'],
                                     attributeType="long", min=0, max=1, dv=0, channel_box=True)

        self.neckInBtwCtrl = ct.Control(match_obj_first_position=neckInBtwJnt, prefix=prefixInBtwNeck,
                                        shape=ct.CIRCLEPLUS,
                                        groups_ctrl=[''], ctrl_size=scale * 1.0,
                                        ctrl_color='lightPink', lock_channels=['v'], gimbal=False, suffix=suffixController,
                                        connection=['connectMatrixAll'])

        mc.connectAttr('%s.%s' % (self.neckCtrl.control, inBtwAttr), self.neckInBtwCtrl.parent_control[0] + '.visibility')

        self.headCtrl = ct.Control(match_obj_first_position=headJnt, prefix=prefixHead,
                                   shape=ct.CUBE,
                                   groups_ctrl=['Zro', 'Global', 'Local'], ctrl_size=scale * 1.0,
                                   ctrl_color='blue', lock_channels=['v'], gimbal=True, suffix=suffixController,
                                   connection=['connectMatrixAll'])

        self.jawCtrl = ct.Control(match_obj_first_position=jawTipJnt, prefix=jawPrefix,
                                  shape=ct.SQUAREPLUS, suffix=suffixController,
                                  groups_ctrl=['All', 'Offset'], ctrl_size=scale * 0.15,
                                  ctrl_color='red', lock_channels=['s', 'v'])
        # ADD ATTRIBUTE UPLIP FOLLOW
        self.attr_upLip_follow = au.add_attribute(objects=[self.jawCtrl.control], long_name=['upperLipFollowing'],
                                                  attributeType="float", min=0, max=1, dv=0.2, keyable=True)

        self.headUpCtrl = ct.Control(match_obj_first_position=headUpJnt, prefix=prefixHeadUp,
                                     shape=ct.CIRCLEHALF, suffix=suffixController,
                                     groups_ctrl=['Zro', 'Offset'], ctrl_size=scale * 1.0,
                                     ctrl_color='red', lock_channels=['v'], gimbal=True,
                                     connection=['connectMatrixAll'])

        self.headLowCtrl = ct.Control(match_obj_first_position=headLowJnt, prefix=prefixHeadLow,
                                      shape=ct.CIRCLEHALF, suffix=suffixController,
                                      groups_ctrl=['Zro', 'Offset'], ctrl_size=scale * 1.0,
                                      ctrl_color='red', lock_channels=['v'], gimbal=True,
                                      connection=['connectMatrixAll'])

        # CREATE GROUP FOR NORMAL ROTATION LIKE JAW
        self.headLow_normal_rotationGrp = mc.createNode('transform', n=au.prefix_name(headLowJnt) + 'Normal_grp')
        mc.delete(mc.pointConstraint(jawJnt, self.headLow_normal_rotationGrp))

        mc.parent(self.headLow_normal_rotationGrp, headLowJnt)

        self.upperTeeth = ct.Control(match_obj_first_position=upperTeethJnt,
                                     prefix=upperTeethJnt, suffix=suffixController,
                                     shape=ct.CUBE, groups_ctrl=[''],
                                     ctrl_size=scale * 0.15,
                                     ctrl_color='yellow', lock_channels=['v'],
                                     connection=['connectAttr'])

        self.lowerTeeth = ct.Control(match_obj_first_position=lowerTeethJnt,
                                     prefix=lowerTeethJnt, suffix=suffixController,
                                     shape=ct.CUBE, groups_ctrl=[''],
                                     ctrl_size=scale * 0.15,
                                     ctrl_color='yellow', lock_channels=['v'],
                                     connection=['connectAttr'])

        self.tongue01 = ct.Control(match_obj_first_position=tongue01Jnt,
                                   prefix=tongue01Jnt, suffix=suffixController,
                                   shape=ct.SQUAREPLUS, groups_ctrl=[''],
                                   ctrl_size=scale * 0.15,
                                   ctrl_color='turquoiseBlue', lock_channels=['v'],
                                   connection=['connectAttr'])

        self.tongue02 = ct.Control(match_obj_first_position=tongue02Jnt,
                                   prefix=tongue02Jnt, suffix=suffixController,
                                   shape=ct.SQUAREPLUS, groups_ctrl=[''],
                                   ctrl_size=scale * 0.15,
                                   ctrl_color='turquoiseBlue', lock_channels=['v'],
                                   connection=['connectAttr'])

        self.tongue03 = ct.Control(match_obj_first_position=tongue03Jnt,
                                   prefix=tongue03Jnt, suffix=suffixController,
                                   shape=ct.SQUAREPLUS, groups_ctrl=[''],
                                   ctrl_size=scale * 0.15,
                                   ctrl_color='turquoiseBlue', lock_channels=['v'],
                                   connection=['connectAttr'])

        self.tongue04 = ct.Control(match_obj_first_position=tongue04Jnt,
                                   prefix=tongue04Jnt, suffix=suffixController,
                                   shape=ct.SQUAREPLUS, groups_ctrl=[''],
                                   ctrl_size=scale * 0.15,
                                   ctrl_color='turquoiseBlue', lock_channels=['v'],
                                   connection=['connectAttr'])

        mc.parent(self.jawTipGrp[0], headLowJnt)
        mc.parent(self.tongue04.parent_control[0], self.tongue03.control)
        mc.parent(self.tongue03.parent_control[0], self.tongue02.control)
        mc.parent(self.tongue02.parent_control[0], self.tongue01.control)
        mc.parent(jawDirectionGrp, self.jawCtrl.parent_control[0], self.headLowCtrl.control_gimbal)
        mc.parent(self.lowerTeeth.parent_control[0], self.tongue01.parent_control[0],
                  jawDirectionOffsetGrp)
        mc.parent(self.upperTeeth.parent_control[0], self.headLowCtrl.control_gimbal)
        mc.parent(self.headLowCtrl.parent_control[0], self.headUpCtrl.parent_control[0],
                  self.headCtrl.control_gimbal)
        mc.parent(self.headCtrl.parent_control[0], self.neckCtrl.control_gimbal)
        mc.parent(self.neckInBtwCtrl.parent_control[0], self.neckCtrl.parent_control[0])

        # INBETWEEN NECK CTRL
        # connect x and z rotation
        pmaNeckInbetween = mc.createNode('plusMinusAverage', n=au.prefix_name(neckInBtwJnt) + 'RotXZ' + '_pma')
        mc.connectAttr(self.neckCtrl.control_gimbal + '.rotateX', pmaNeckInbetween + '.input2D[0].input2Dx')
        mc.connectAttr(self.neckCtrl.control_gimbal + '.rotateZ', pmaNeckInbetween + '.input2D[0].input2Dy')
        mc.connectAttr(self.neckCtrl.control+'.rotateX', pmaNeckInbetween+'.input2D[1].input2Dx')
        mc.connectAttr(self.neckCtrl.control+'.rotateZ', pmaNeckInbetween+'.input2D[1].input2Dy')
        mc.connectAttr(pmaNeckInbetween +'.output2Dx', self.neckInBtwCtrl.parent_control[0] + '.rotateX')
        mc.connectAttr(pmaNeckInbetween +'.output2Dy', self.neckInBtwCtrl.parent_control[0] + '.rotateZ')

        # connect orient constraint y
        ctrlOri = mc.orientConstraint(self.headCtrl.control_gimbal, self.neckCtrl.control_gimbal,
                                      self.neckInBtwCtrl.parent_control[0], mo=1, skip=('x', 'z'))[0]
        pointOri = mc.pointConstraint(self.headCtrl.control_gimbal, self.neckCtrl.control_gimbal,
                                      self.neckInBtwCtrl.parent_control[0], mo=1)

        # INBETWEEN NECK JNT
        trfPoint = mc.pointConstraint(neckJnt, headJnt, self.neckInBtwJntGrp[0], mo=1)
        trfOri = mc.orientConstraint(neckJnt, headJnt, self.neckInBtwJntGrp[0],  mo=1, skip=('x','z'))[0]
        mc.setAttr(ctrlOri+'.interpType', 2)
        mc.setAttr(trfOri+'.interpType',2)

        # CONSTRAINT RENAME
        au.constraint_rename([ctrlOri, pointOri[0], trfPoint[0], trfOri])

