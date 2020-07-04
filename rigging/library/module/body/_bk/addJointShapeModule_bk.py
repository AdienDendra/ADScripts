from __builtin__ import reload

import maya.cmds as mc
from rigLib.rig.body import expand_skeleton as aj
from rigLib.utils import controller as ct

from rigging.tools import AD_utils as au

reload(ct)
reload(aj)
reload(au)

class AddJointShape:
    def __init__(self,
                 numArmDtlCtrl,
                 numLegDtlCtrl,
                 neckShapeJoint,
                 clavicleShapeJoint,
                 ballShapeJoint,
                 upperArmShapeJoint,
                 upperLegShapeJoint,
                 elbowShapeJoint,
                 kneeShapeJoint,
                 wristShapeJoint,
                 ankleShapeJoint,
                 leftSide,
                 rightSide,

                 prefixArmSetup,
                 prefixClav,
                 prefixUpperArm,
                 prefixElbow,
                 prefixWrist,
                 prefixLegSetup,
                 prefixBall,
                 prefixUpperLeg,
                 prefixKnee,
                 prefixAnkle,
                 sAddPrefixValue,
                 Dtl,
                 sjPrefixValue,
                 prefixForearm,
                 Fk,
                 prefixLowerLeg,

                 upArmJointLFTGrp,
                 elbowJointLFTGrp,
                 wristJointLFTGrp,
                 upArmJointRGTGrp,
                 elbowJointRGTGrp,
                 wristJointRGTGrp,
                 upLegJointLFTGrp,
                 kneeJointLFTGrp,
                 ankleJointLFTGrp,
                 upLegJointRGTGrp,
                 kneeJointRGTGrp,
                 ankleJointRGTGrp,
                 neckJointGrp,
                 prefixFkIkSpineSetup,
                 neckPrefix):

        self.prefixArmSetup = prefixArmSetup
        self.prefixClav = prefixClav
        self.prefixUpperArm = prefixUpperArm
        self.prefixElbow = prefixElbow
        self.prefixWrist = prefixWrist
        self.prefixLegSetup = prefixLegSetup
        self.prefixBall = prefixBall
        self.prefixUpperLeg= prefixUpperLeg
        self.prefixKnee = prefixKnee
        self.prefixAnkle = prefixAnkle
        self.sAddPrefixValue = sAddPrefixValue
        self.Dtl = Dtl
        self.sjPrefixValue = sjPrefixValue
        self.prefixForearm = prefixForearm
        self.Fk = Fk
        self.prefixLowerLeg = prefixLowerLeg
        self.prefixFkIkSpineSetup = prefixFkIkSpineSetup
        self.neckPrefix = neckPrefix

        # ==================================================================================================================
        #                                            SHAPE JOINT LEFT ARM PARAMETERS
        # ==================================================================================================================
        if mc.objExists('%s%s_ctrl' % (self.prefixArmSetup, leftSide)):

            # ARM LEFT
            self.AddJointAttribute(prefixSetup=self.prefixArmSetup, baseOrTipShapeJoint=clavicleShapeJoint,
                              upperShapeJoint=upperArmShapeJoint, middleShapeJoint=elbowShapeJoint,
                              lowerShapeJoint=wristShapeJoint,
                              prefixBaseOrTip=self.prefixClav, prefixUpper=self.prefixUpperArm, prefixMiddle=self.prefixElbow,
                              prefixLower=self.prefixWrist, side=leftSide)
            print('5% | adding attribute left arm is done!')

            # UPPERARM
            self.addUpperArmJoint(addJoint=upperArmShapeJoint, side=leftSide, jointGrp=upArmJointLFTGrp,
                                  rotation='Z',
                                  translateOne='X',
                                  translateTwo='Y',
                                  rotationOnePos=-1,
                                  rotationTwoPos=1,
                                  rotationOneNeg=1,
                                  rotationTwoNeg=0,
                                  offsetTranslate=-1.006)

            print('10% | left upper arm add joint deform is done!')

            # ELBOW
            self.addElbowJoint(addJoint=elbowShapeJoint, side=leftSide, numArmDtlCtrl=numArmDtlCtrl, jointGrp=elbowJointLFTGrp,
                               rotation='X',
                               translateOne='Y',
                               translateTwo='Z',
                               rotationOnePos=-1,
                               rotationTwoPos=-1,
                               rotationOneNeg=-1,
                               rotationTwoNeg=1,
                               offsetTranslate=-1.006)

            print('15% | left elbow add joint deform is done!')

            # WRIST
            self.addWristJoint(addJoint=wristShapeJoint, side=leftSide, numArmDtlCtrl=numArmDtlCtrl, jointGrp=wristJointLFTGrp,
                               rotation='Z',
                               translateOne='Y',
                               translateTwo='X',
                               rotationOnePos=-1,
                               rotationTwoPos=-1,
                               rotationOneNeg=1,
                               rotationTwoNeg=1,
                               offsetTranslate=-1.006)

            print('20% | left wrist add joint deform is done!')

    # ==================================================================================================================
    #                                           ADDITIONAL JOINT RIGHT ARM PARAMETERS
    # ==================================================================================================================
        if mc.objExists('%s%s_ctrl' % (self.prefixArmSetup, rightSide)):
            # ARM RIGHT
            self.AddJointAttribute(prefixSetup=self.prefixArmSetup, baseOrTipShapeJoint=clavicleShapeJoint,
                              upperShapeJoint=upperArmShapeJoint, middleShapeJoint=elbowShapeJoint,
                              lowerShapeJoint=wristShapeJoint,
                              prefixBaseOrTip=self.prefixClav, prefixUpper=self.prefixUpperArm, prefixMiddle=self.prefixElbow,
                              prefixLower=self.prefixWrist, side=rightSide)

            print('25% | adding attribute right arm is done!')

            # UPPERARM
            self.addUpperArmJoint(addJoint=upperArmShapeJoint, side=rightSide, jointGrp=upArmJointRGTGrp,
                                  rotation='Z',
                                  translateOne='X',
                                  translateTwo='Y',
                                  rotationOnePos=-1,
                                  rotationTwoPos=1,
                                  rotationOneNeg=1,
                                  rotationTwoNeg=0,
                                  offsetTranslate=-1.006)

            print('30% | right upper arm add joint deform is done!')

            # ELBOW
            self.addElbowJoint(addJoint=elbowShapeJoint, side=rightSide, numArmDtlCtrl=numArmDtlCtrl, jointGrp=elbowJointRGTGrp,
                               rotation='X',
                               translateOne='Y',
                               translateTwo='Z',
                               rotationOnePos=-1,
                               rotationTwoPos=-1,
                               rotationOneNeg=-1,
                               rotationTwoNeg=1,
                               offsetTranslate=-1.006)

            print('35% | right elbow add joint deform is done!')

            # WRIST
            self.addWristJoint(addJoint=wristShapeJoint, side=rightSide, numArmDtlCtrl=numArmDtlCtrl, jointGrp=wristJointRGTGrp,
                               rotation='Z',
                               translateOne='Y',
                               translateTwo='X',
                               rotationOnePos=-1,
                               rotationTwoPos=-1,
                               rotationOneNeg=1,
                               rotationTwoNeg=1,
                               offsetTranslate=-1.006)

            print('40% | right wrist add joint deform is done!')

    # ==================================================================================================================
    #                                        ADDITIONAL JOINT LEFT LEG PARAMETERS
    # ==================================================================================================================
        if mc.objExists('%s%s_ctrl' % (self.prefixLegSetup, leftSide)):
            # LEG LEFT
            self.AddJointAttribute(prefixSetup=self.prefixLegSetup, baseOrTipShapeJoint=ballShapeJoint,
                              upperShapeJoint=upperLegShapeJoint, middleShapeJoint=kneeShapeJoint,
                              lowerShapeJoint=ankleShapeJoint,
                              prefixBaseOrTip=self.prefixBall, prefixUpper=self.prefixUpperLeg, prefixMiddle=self.prefixKnee,
                              prefixLower=self.prefixAnkle, side=leftSide)

            print('45% | adding attribute left leg is done!')

            # UPPERLEG
            self.addUpperLegJoint(addJoint=upperLegShapeJoint, side=leftSide, jointGrp=upLegJointLFTGrp,
                                  rotation='Z',
                                  translateOne='X',
                                  translateTwo='Y',
                                  rotationOnePos=-1,
                                  rotationTwoPos=1,
                                  rotationOneNeg=1,
                                  rotationTwoNeg=0,
                                  offsetTranslate=-1.006)
            print('50% | left upper leg add joint deform is done!')

            # KNEE
            self.addKneeJoint(addJoint=kneeShapeJoint, side=leftSide, numArmDtlCtrl=numLegDtlCtrl, jointGrp=kneeJointLFTGrp,
                              rotation='X',
                              translateOne='Y',
                              translateTwo='Z',
                              rotationOnePos=1,
                              rotationTwoPos=1,
                              rotationOneNeg=1,
                              rotationTwoNeg=-1,
                              offsetTranslate=-1.006)
            print('55% | left knee add joint deform is done!')

            # ANKLE
            self.addAnkleJoint(addJoint=ankleShapeJoint, side=leftSide, numArmDtlCtrl=numLegDtlCtrl, jointGrp=ankleJointLFTGrp,
                               rotation='X',
                               translateOne='Y',
                               translateTwo='Z',
                               rotationOnePos=0,
                               rotationTwoPos=0,
                               rotationOneNeg=-2,
                               rotationTwoNeg=2,
                               offsetTranslate=-1.006)
            print('60% | left ankle add joint deform is done!')

        # ==================================================================================================================
        #                                       ADDITIONAL JOINT RIGHT LEG PARAMETERS
        # ==================================================================================================================
        if mc.objExists('%s%s_ctrl' % (self.prefixLegSetup, rightSide)):
            # LEG LEFT
            self.AddJointAttribute(prefixSetup=self.prefixLegSetup, baseOrTipShapeJoint=ballShapeJoint,
                              upperShapeJoint=upperLegShapeJoint, middleShapeJoint=kneeShapeJoint,
                              lowerShapeJoint=ankleShapeJoint,
                              prefixBaseOrTip=self.prefixBall, prefixUpper=self.prefixUpperLeg, prefixMiddle=self.prefixKnee,
                              prefixLower=self.prefixAnkle, side=rightSide)
            print('65% | adding attribute right leg is done!')

            # UPPERLEG
            self.addUpperLegJoint(addJoint=upperLegShapeJoint, side=rightSide, jointGrp=upLegJointRGTGrp,
                                  rotation='Z',
                                  translateOne='X',
                                  translateTwo='Y',
                                  rotationOnePos=-1,
                                  rotationTwoPos=1,
                                  rotationOneNeg=1,
                                  rotationTwoNeg=0,
                                  offsetTranslate=-1.006)
            print('70% | right upper leg add joint deform is done!')

            # KNEE
            self.addKneeJoint(addJoint=kneeShapeJoint, side=rightSide, numArmDtlCtrl=numLegDtlCtrl, jointGrp=kneeJointRGTGrp,
                              rotation='X',
                              translateOne='Y',
                              translateTwo='Z',
                              rotationOnePos=1,
                              rotationTwoPos=1,
                              rotationOneNeg=1,
                              rotationTwoNeg=-1,
                              offsetTranslate=-1.006)
            print('75% | right knee add joint deform is done!')

            # ANKLE
            self.addAnkleJoint(addJoint=ankleShapeJoint, side=rightSide, numArmDtlCtrl=numLegDtlCtrl, jointGrp=ankleJointRGTGrp,
                               rotation='X',
                               translateOne='Y',
                               translateTwo='Z',
                               rotationOnePos=0,
                               rotationTwoPos=0,
                               rotationOneNeg=-2,
                               rotationTwoNeg=2,
                               offsetTranslate=-1.006)

            print('80% | right ankle add joint deform is done!')

    # ==================================================================================================================
    #                                        ADDITIONAL NECK PARAMETERS
    # ==================================================================================================================
        if mc.objExists('%s_ctrl' % self.neckPrefix):
            if not mc.objExists('%s_ctrl.%sShape' % (self.prefixFkIkSpineSetup, self.neckPrefix)):
                au.add_attribute(objects=['%s_ctrl' % self.prefixFkIkSpineSetup], long_name=['cornerShape'],
                                 nice_name=[' '], at="enum",
                                 en='Corner Shape', channel_box=True)
                au.add_attribute(objects=['%s_ctrl' % self.prefixFkIkSpineSetup], long_name=['neckShape'],
                                 attributeType="float", min=0, dv=0.5, channel_box=True)

            print('85% | adding attribute neck is done!')

            # UPPERLEG
            self.addNeckJoint(addJoint=neckShapeJoint,
                              jointGrp=neckJointGrp,
                              rotation='X',
                              translateOne='Z',
                              translateTwo='Y',
                              rotationOnePos=0,
                              rotationTwoPos=0,
                              rotationOneNeg=1,
                              rotationTwoNeg=0,
                              offsetTranslate=-1.006)
            print('90% | neck add joint deform is done!')

            print('100% | clean up!')

    # ==================================================================================================================
    #                                                   FUNCTIONS
    # ==================================================================================================================

    def AddJointAttribute(self, prefixSetup, baseOrTipShapeJoint, upperShapeJoint, middleShapeJoint, lowerShapeJoint,
                          prefixBaseOrTip, prefixUpper, prefixMiddle, prefixLower,
                          side):

        if mc.objExists('%s%s%s' % (prefixSetup, side, '_ctrl')):
            if baseOrTipShapeJoint or upperShapeJoint or middleShapeJoint or lowerShapeJoint:
                au.add_attribute(objects=['%s%s_ctrl' % (prefixSetup, side)], long_name=['cornerShape'],
                                 nice_name=[' '], at="enum",
                                 en='Corner Shape', channel_box=True)

            if baseOrTipShapeJoint:
                if not mc.objExists('%s%s_ctrl' % (prefixSetup, side) + '.' + prefixBaseOrTip + 'Shape'):
                    au.add_attribute(objects=['%s%s_ctrl' % (prefixSetup, side)], long_name=[prefixBaseOrTip + 'Shape'],
                                     attributeType="float", min=0, dv=0.5, channel_box=True)
            if upperShapeJoint:
                if not mc.objExists('%s%s_ctrl' % (prefixSetup, side) + '.' + prefixUpper + 'Shape'):
                    au.add_attribute(objects=['%s%s_ctrl' % (prefixSetup, side)], long_name=[prefixUpper + 'Shape'],
                                     attributeType="float", min=0, dv=0.5, channel_box=True)
            if middleShapeJoint:
                if not mc.objExists('%s%s_ctrl' % (prefixSetup, side) + '.' + prefixMiddle + 'Shape'):
                    au.add_attribute(objects=['%s%s_ctrl' % (prefixSetup, side)], long_name=[prefixMiddle + 'Shape'],
                                     attributeType="float", min=0, dv=0.5, channel_box=True)
            if lowerShapeJoint:
                if not mc.objExists('%s%s_ctrl' % (prefixSetup, side) + '.' + prefixLower + 'Shape'):
                    au.add_attribute(objects=['%s%s_ctrl' % (prefixSetup, side)], long_name=[prefixLower + 'Shape'],
                                     attributeType="float", min=0, dv=0.5, channel_box=True)

    def addUpperArmJoint(self, addJoint, side, rotation, translateOne, translateTwo, rotationOnePos,
                         rotationTwoPos, rotationOneNeg, rotationTwoNeg, offsetTranslate, jointGrp):

        if mc.objExists('%s%s%s' % (self.prefixArmSetup, side, '_ctrl')):
            if not mc.objExists('upArm%s%s_grp' % (self.sAddPrefixValue, side)):
                aj.Build(add_joint=addJoint,
                         fk_ik_setup='%s%s_ctrl' % (self.prefixArmSetup, side),
                         controller_expand_name=self.prefixUpperArm,
                         joint_driver_matrix='%s%s01%s_ctrl' % (self.prefixUpperArm, self.Dtl, side),
                         joint_add_target='upArm%s%s_jnt' % (self.sAddPrefixValue, side),
                         joint_driver_inverse_matrix='clav%s%s_jnt' % (self.sjPrefixValue, side),
                         point_grp_driver=['%s%s01%s_ctrl' % (self.prefixUpperArm, self.Dtl, side)],
                         scale_driver=['%s%s01%s_ctrl' % (self.prefixUpperArm, self.Dtl, side)],
                         prefix=self.prefixUpperArm,
                         side=side,
                         joint_grp=jointGrp,
                         rotation=rotation,
                         translateOne=translateOne,
                         translateTwo=translateTwo,
                         rotationOnePos=rotationOnePos,
                         rotationTwoPos=rotationTwoPos,
                         rotationOneNeg=rotationOneNeg,
                         rotationTwoNeg=rotationTwoNeg,
                         offsetTranslate=offsetTranslate,
                         )
            else:
                print('Additional joint', 'upArm%s%s_jnt' % (self.sAddPrefixValue, side), 'is already added!')

    def addElbowJoint(self, addJoint, side, numArmDtlCtrl, rotation, translateOne, translateTwo, rotationOnePos,
                      rotationTwoPos, rotationOneNeg, rotationTwoNeg, offsetTranslate, jointGrp):

        if mc.objExists('%s%s%s' % (self.prefixArmSetup, side, '_ctrl')):
            if not mc.objExists('forearm%s%s_grp' % (self.sAddPrefixValue, side)):
                aj.Build(add_joint=addJoint,
                         fk_ik_setup='%s%s_ctrl' % (self.prefixArmSetup, side),
                         controller_expand_name=self.prefixElbow,
                         joint_driver_matrix='forearm%s%s_jnt' % (self.sjPrefixValue, side),
                         joint_add_target='forearm%s%s_jnt' % (self.sAddPrefixValue, side),
                         joint_driver_inverse_matrix='upArm%s%s_jnt' % (self.sjPrefixValue, side),
                         point_grp_driver=['%s%s%02d%s_ctrl' % (self.prefixUpperArm, self.Dtl, numArmDtlCtrl, side),
                                         '%s%s01%s_ctrl' % (self.prefixForearm, self.Dtl, side)],
                         scale_driver=['%s%s%02d%s_ctrl' % (self.prefixUpperArm, self.Dtl, numArmDtlCtrl, side),
                                      '%s%s01%s_ctrl' % (self.prefixForearm, self.Dtl, side)],
                         prefix=self.prefixForearm,
                         side=side,
                         joint_grp=jointGrp,
                         rotation=rotation,
                         translateOne=translateOne,
                         translateTwo=translateTwo,
                         rotationOnePos=rotationOnePos,
                         rotationTwoPos=rotationTwoPos,
                         rotationOneNeg=rotationOneNeg,
                         rotationTwoNeg=rotationTwoNeg,
                         offsetTranslate=offsetTranslate,
                         )
            else:
                print('Shape joint', 'forearm%s%s_jnt' % (self.sAddPrefixValue, side), 'is already added!')

    def addWristJoint(self, addJoint, side, numArmDtlCtrl, rotation, translateOne, translateTwo, rotationOnePos,
                      rotationTwoPos,
                      rotationOneNeg, rotationTwoNeg, offsetTranslate, jointGrp):

        if mc.objExists('%s%s%s' % (self.prefixArmSetup, side, '_ctrl')):
            if not mc.objExists('wrist%s%s_grp' % (self.sAddPrefixValue, side)):
                aj.Build(add_joint=addJoint,
                         fk_ik_setup='%s%s_ctrl' % (self.prefixArmSetup, side),
                         controller_expand_name=self.prefixWrist,
                         joint_driver_matrix='wrist%s%s_jnt' % (self.sjPrefixValue, side),
                         joint_add_target='wrist%s%s_jnt' % (self.sAddPrefixValue, side),
                         joint_driver_inverse_matrix='forearm%s%s_jnt' % (self.sjPrefixValue, side),
                         point_grp_driver=['%s%s%02d%s_ctrl' % (self.prefixForearm, self.Dtl, numArmDtlCtrl, side),
                                         'wrist%s%s_jnt' % (self.sjPrefixValue, side)],
                         scale_driver=['%s%s%02d%s_ctrl' % (self.prefixForearm, self.Dtl, numArmDtlCtrl, side),
                                      'wrist%s%s_jnt' % (self.sjPrefixValue, side)],
                         prefix=self.prefixWrist,
                         side=side,
                         joint_grp=jointGrp,
                         rotation=rotation,
                         translateOne=translateOne,
                         translateTwo=translateTwo,
                         rotationOnePos=rotationOnePos,
                         rotationTwoPos=rotationTwoPos,
                         rotationOneNeg=rotationOneNeg,
                         rotationTwoNeg=rotationTwoNeg,
                         offsetTranslate=offsetTranslate
                         )
            else:
                print('Shape joint', 'wrist%s%s_jnt' % (self.sAddPrefixValue, side), 'is already added!')

    def addUpperLegJoint(self, addJoint, side, rotation, translateOne, translateTwo, rotationOnePos, rotationTwoPos,
                         rotationOneNeg, rotationTwoNeg, offsetTranslate, jointGrp):

        if mc.objExists('%s%s%s' % (self.prefixLegSetup, side, '_ctrl')):
            if not mc.objExists('upLeg%s%s_grp' % (self.sAddPrefixValue, side)):
                aj.Build(add_joint=addJoint,
                         fk_ik_setup='%s%s_ctrl' % (self.prefixLegSetup, side),
                         controller_expand_name=self.prefixUpperLeg,
                         joint_driver_matrix='%s%s01%s_ctrl' % (self.prefixUpperLeg, self.Dtl, side),
                         joint_add_target='upLeg%s%s_jnt' % (self.sAddPrefixValue, side),
                         joint_driver_inverse_matrix='%s%sCtrlOffset%s_grp' % (self.prefixUpperLeg, self.Fk, side),
                         point_grp_driver=['%s%s01%s_ctrl' % (self.prefixUpperLeg, self.Dtl, side)],
                         scale_driver=['%s%s01%s_ctrl' % (self.prefixUpperLeg, self.Dtl, side)],
                         prefix=self.prefixUpperLeg,
                         side=side,
                         joint_grp=jointGrp,
                         rotation=rotation,
                         translateOne=translateOne,
                         translateTwo=translateTwo,
                         rotationOnePos=rotationOnePos,
                         rotationTwoPos=rotationTwoPos,
                         rotationOneNeg=rotationOneNeg,
                         rotationTwoNeg=rotationTwoNeg,
                         offsetTranslate=offsetTranslate
                         )
            else:
                print('Shape joint', 'upLeg%s%s_jnt' % (self.sAddPrefixValue, side), 'is already added!')

    def addKneeJoint(self, addJoint, side, numArmDtlCtrl, rotation, translateOne, translateTwo, rotationOnePos,
                     rotationTwoPos,
                     rotationOneNeg, rotationTwoNeg, offsetTranslate, jointGrp):

        if mc.objExists('%s%s%s' % (self.prefixLegSetup, side, '_ctrl')):
            if not mc.objExists('lowLeg%s%s_grp' % (self.sAddPrefixValue, side)):
                aj.Build(add_joint=addJoint,
                         fk_ik_setup='%s%s_ctrl' % (self.prefixLegSetup, side),
                         controller_expand_name=self.prefixKnee,
                         joint_driver_matrix='lowLeg%s%s_jnt' % (self.sjPrefixValue, side),
                         joint_add_target='lowLeg%s%s_jnt' % (self.sAddPrefixValue, side),
                         joint_driver_inverse_matrix='upLeg%s%s_jnt' % (self.sjPrefixValue, side),
                         point_grp_driver=['%s%s%02d%s_ctrl' % (self.prefixUpperLeg, self.Dtl, numArmDtlCtrl, side),
                                         '%s%s01%s_ctrl' % (self.prefixLowerLeg, self.Dtl, side)],
                         scale_driver=['%s%s%02d%s_ctrl' % (self.prefixUpperLeg, self.Dtl, numArmDtlCtrl, side),
                                      '%s%s01%s_ctrl' % (self.prefixLowerLeg, self.Dtl, side)],
                         prefix=self.prefixLowerLeg,
                         side=side,
                         joint_grp=jointGrp,
                         rotation=rotation,
                         translateOne=translateOne,
                         translateTwo=translateTwo,
                         rotationOnePos=rotationOnePos,
                         rotationTwoPos=rotationTwoPos,
                         rotationOneNeg=rotationOneNeg,
                         rotationTwoNeg=rotationTwoNeg,
                         offsetTranslate=offsetTranslate,
                         )
            else:
                print('Shape joint', 'lowLeg%s%s_jnt' % (self.sAddPrefixValue, side), 'is already added!')

    def addAnkleJoint(self, addJoint, side, numArmDtlCtrl, rotation, translateOne, translateTwo, rotationOnePos,
                      rotationTwoPos,
                      rotationOneNeg, rotationTwoNeg, offsetTranslate, jointGrp):

        if mc.objExists('%s%s%s' % (self.prefixLegSetup, side, '_ctrl')):
            if not mc.objExists('ankle%s%s_grp' % (self.sAddPrefixValue, side)):
                aj.Build(add_joint=addJoint,
                         fk_ik_setup='%s%s_ctrl' % (self.prefixLegSetup, side),
                         controller_expand_name=self.prefixAnkle,
                         joint_driver_matrix='ankle%s%s_jnt' % (self.sjPrefixValue, side),
                         joint_add_target='ankle%s%s_jnt' % (self.sAddPrefixValue, side),
                         joint_driver_inverse_matrix='lowLeg%s%s_jnt' % (self.sjPrefixValue, side),
                         point_grp_driver=['%s%s%02d%s_ctrl' % (self.prefixLowerLeg, self.Dtl, numArmDtlCtrl, side),
                                         'ankle%s%s_jnt' % (self.sjPrefixValue, side)],
                         scale_driver=['%s%s%02d%s_ctrl' % (self.prefixLowerLeg, self.Dtl, numArmDtlCtrl, side),
                                      'ankle%s%s_jnt' % (self.sjPrefixValue, side)],
                         prefix=self.prefixAnkle,
                         side=side,
                         joint_grp=jointGrp,
                         rotation=rotation,
                         translateOne=translateOne,
                         translateTwo=translateTwo,
                         rotationOnePos=rotationOnePos,
                         rotationTwoPos=rotationTwoPos,
                         rotationOneNeg=rotationOneNeg,
                         rotationTwoNeg=rotationTwoNeg,
                         offsetTranslate=offsetTranslate
                         )
            else:
                print('Shape joint', 'ankle%s%s_jnt' % (self.sAddPrefixValue, side), 'is already added!')

    def addNeckJoint(self, addJoint, rotation, translateOne, translateTwo, rotationOnePos, rotationTwoPos,
                     rotationOneNeg, rotationTwoNeg, offsetTranslate, jointGrp):

        if mc.objExists('%s%s' % (self.prefixFkIkSpineSetup, '_ctrl')):
            if not mc.objExists('neck%s_grp' % (self.sAddPrefixValue)):
                aj.Build(add_joint=addJoint,
                         fk_ik_setup='%s_ctrl' % (self.prefixFkIkSpineSetup),
                         controller_expand_name=self.neckPrefix,
                         joint_driver_matrix='%sGmbl_ctrl' % self.neckPrefix,
                         joint_add_target='neck%s_jnt' % self.sAddPrefixValue,
                         joint_driver_inverse_matrix='spine%s04_jnt' % self.sjPrefixValue,
                         point_grp_driver=['%sGmbl_ctrl' % self.neckPrefix],
                         scale_driver=['%sGmbl_ctrl' % self.neckPrefix],
                         prefix=self.neckPrefix,
                         side='',
                         joint_grp=jointGrp,
                         rotation=rotation,
                         translateOne=translateOne,
                         translateTwo=translateTwo,
                         rotationOnePos=rotationOnePos,
                         rotationTwoPos=rotationTwoPos,
                         rotationOneNeg=rotationOneNeg,
                         rotationTwoNeg=rotationTwoNeg,
                         offsetTranslate=offsetTranslate
                         )
            else:
                print('Shape joint', 'neck%s_jnt' % (self.sAddPrefixValue), 'is already added!')
   # SOFT IK

            # # CLAVICLE
            # addJointClavLFT = aj.Build(addJoint=clavicleShapeJoint,
            #                                fkIkSetup=armLFT.fkIkLimbSetupController,
            #                                controllerShapeName=prefixClav,
            #                                jointDriverMatrix=sj.clavLFT,
            #                                jointAddTarget=sDtlJnt.clavLFT,
            #                                jointDriverInverseMatrix=sj.spineList[3],
            #                                pointGrpDriver=sj.clavLFT,
            #                                prefix=prefixClav,
            #                                prefixLimb=prefixArm,
            #                                side=sideLFT,
            #                                skinGrp=module.skinGrp,
            #                                rotation='Z',
            #                                translateOne='X',
            #                                translateTwo='Y',
            #                                rotationOnePos=-1,
            #                                rotationTwoPos=1,
            #                                rotationOneNeg=1,
            #                                rotationTwoNeg=0,
            #                                offsetTranslate=-1.006,
            #                                scaleObjectOne=sj.clavLFT,
            #                                scaleObjectTwo=None,
            #                                )

            # SOFT IK

            # # CLAVICLE
            # addJointClavLFT = aj.Build(addJoint=clavicleShapeJoint,
            #                                fkIkSetup=armLFT.fkIkLimbSetupController,
            #                                controllerShapeName=prefixClav,
            #                                jointDriverMatrix=sj.clavLFT,
            #                                jointAddTarget=sDtlJnt.clavLFT,
            #                                jointDriverInverseMatrix=sj.spineList[3],
            #                                pointGrpDriver=sj.clavLFT,
            #                                prefix=prefixClav,
            #                                prefixLimb=prefixArm,
            #                                side=sideLFT,
            #                                skinGrp=module.skinGrp,
            #                                rotation='Z',
            #                                translateOne='X',
            #                                translateTwo='Y',
            #                                rotationOnePos=-1,
            #                                rotationTwoPos=1,
            #                                rotationOneNeg=1,
            #                                rotationTwoNeg=0,
            #                                offsetTranslate=-1.006,
            #                                scaleObjectOne=sj.clavLFT,
            #                                scaleObjectTwo=None,
            #                                )

            # SOFT IK

            # # CLAVICLE
            # addJointClavLFT = aj.Build(addJoint=clavicleShapeJoint,
            #                                fkIkSetup=armLFT.fkIkLimbSetupController,
            #                                controllerShapeName=prefixClav,
            #                                jointDriverMatrix=sj.clavLFT,
            #                                jointAddTarget=sDtlJnt.clavLFT,
            #                                jointDriverInverseMatrix=sj.spineList[3],
            #                                pointGrpDriver=sj.clavLFT,
            #                                prefix=prefixClav,
            #                                prefixLimb=prefixArm,
            #                                side=sideLFT,
            #                                skinGrp=module.skinGrp,
            #                                rotation='Z',
            #                                translateOne='X',
            #                                translateTwo='Y',
            #                                rotationOnePos=-1,
            #                                rotationTwoPos=1,
            #                                rotationOneNeg=1,
            #                                rotationTwoNeg=0,
            #                                offsetTranslate=-1.006,
            #                                scaleObjectOne=sj.clavLFT,
            #                                scaleObjectTwo=None,
            #                                )