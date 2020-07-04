from __builtin__ import reload

import maya.OpenMaya as om
import maya.cmds as mc

from rigging.library.utils import controller as ct
from rigging.library.utils import transform as tf
from rigging.tools import AD_utils as au

reload (ct)
reload (tf)
reload (au)

class Build:
    def __init__(self, crv, scale, sideLFT, sideRGT, side, offsetJnt02BindPos, offsetJnt04BindPos,
                 directionCtrl01, directionCtrl02, directionCtrl03, directionCtrl04, directionCtrl05,
                 ctrlColor, controllerWireLow, shape, posDirectionJnt, faceUtilsGrp, suffixController,
                 connectWithCornerCtrl=False):

        self.prefixNameCrv = self.replacePosLFTRGT(au.prefix_name(crv), sideLFT=sideLFT, sideRGT=sideRGT)

        self.pos = mc.xform(posDirectionJnt, q=1, ws=1, t=1)[0]

        self.vtxCrv = mc.ls('%s.cv[0:*]' % crv, fl=True)

        self.createJointWire(crv=crv, scale=scale, side=side)

        self.wireBindCurve(offsetJnt02BindPos=offsetJnt02BindPos, directionCtrl01=directionCtrl01,
                           directionCtrl02=directionCtrl02, offsetJnt04BindPos=offsetJnt04BindPos,
                           directionCtrl03=directionCtrl03, directionCtrl04=directionCtrl04, directionCtrl05=directionCtrl05,
                           crv=crv, scale=scale, side=side)

        self.controllerWire(scale=scale, side=side, controllerWireLow=controllerWireLow, shape=shape, ctrlColor=ctrlColor,
                            connectWithCornerCtrl=connectWithCornerCtrl, sideRGT=sideRGT, sideLFT=sideLFT, suffixController=suffixController)

        self.groupingWire(side=side, faceUtilsGrp=faceUtilsGrp, posDirectionJnt=posDirectionJnt)

    def groupingWire(self, side, faceUtilsGrp, posDirectionJnt):
        setupDriverGrp = mc.group(em=1, n=self.prefixNameCrv+'Setup'+side+'_grp')
        ctrlDriverGrp = mc.group(em=1, n=self.prefixNameCrv+'Controller'+side+'_grp')

        mc.hide(setupDriverGrp)
        grpNoseAll = mc.group(em=1, n=self.prefixNameCrv+side+'_grp')

        wireGrpDrivenJnt = mc.group(em=1, n= self.prefixNameCrv+'DrivenJnt' + side + '_grp')
        mc.delete(mc.parentConstraint(posDirectionJnt, wireGrpDrivenJnt))
        wireGrpDrivenOffsetJnt = mc.duplicate(wireGrpDrivenJnt, n=self.prefixNameCrv + 'DrivenOffsetJnt' + side + '_grp')[0]
        wireGrpDrivenCtrl = mc.duplicate(wireGrpDrivenJnt, n=self.prefixNameCrv + 'DrivenCtrl' + side + '_grp')[0]
        wireGrpDrivenOffsetCtrl = mc.duplicate(wireGrpDrivenCtrl, n=self.prefixNameCrv + 'DrivenOffsetCtrl' + side + '_grp')[0]

        # parenting to joint grp
        mc.parent(wireGrpDrivenOffsetJnt, wireGrpDrivenJnt)
        mc.parent(wireGrpDrivenOffsetCtrl, wireGrpDrivenCtrl)

        mc.parent(wireGrpDrivenJnt, setupDriverGrp, grpNoseAll)
        mc.parent(wireGrpDrivenCtrl, ctrlDriverGrp)

        # mc.parent(groupDriver, setupDriverGrp, ctrlDriverGrp, grpNoseAll)

        mc.parent(grpNoseAll, faceUtilsGrp)

        self.wireGrpDrivenOffsetJnt = wireGrpDrivenOffsetJnt
        self.wireGrpDrivenCtrl = wireGrpDrivenCtrl
        self.wireGrpDrivenOffsetCtrl = wireGrpDrivenOffsetCtrl
        self.setupDriverGrp =setupDriverGrp
        self.ctrlDriverGrp = ctrlDriverGrp

        mc.parent(self.grpDrvCtrl, wireGrpDrivenOffsetCtrl)
        mc.parent(self.jointGrp, setupDriverGrp)
        mc.parent(self.bindJntGrp, wireGrpDrivenOffsetJnt)

        mc.parent(self.curvesGrp, self.locatorGrp, self.setupDriverGrp)


    def controllerWire(self, scale, ctrlColor, shape, controllerWireLow, suffixController, sideRGT, sideLFT, side='', connectWithCornerCtrl=False):

        # controller mid
        controllerBind03 = ct.Control(match_obj_first_position=self.jnt03, prefix=self.prefixNameCrv + 'Drv03',
                                      shape=shape, groups_ctrl=['Zro', 'Offset'], ctrl_size=scale * 0.075,
                                      ctrl_color=ctrlColor, lock_channels=['v', 's'], side=side, suffix=suffixController
                                      )

        # controller rgt 01
        controllerBind05 = ct.Control(match_obj_first_position=self.jnt05, prefix=self.prefixNameCrv + 'Drv05',
                                      shape=shape, groups_ctrl=['Zro', 'Offset', 'All'], ctrl_size=scale * 0.035,
                                      ctrl_color=ctrlColor, lock_channels=['v', 's'], side=side, suffix=suffixController
                                      )

        # controller rgt 02
        controllerBind04 = ct.Control(match_obj_first_position=self.jnt04, prefix=self.prefixNameCrv + 'Drv04',
                                      shape=shape, groups_ctrl=['Zro', 'Offset'], ctrl_size=scale * 0.05,
                                      ctrl_color=ctrlColor, lock_channels=['v', 's'], side=side, suffix=suffixController
                                      )
        # controller lft 01
        controllerBind01 = ct.Control(match_obj_first_position=self.jnt01, prefix=self.prefixNameCrv + 'Drv01',
                                      shape=shape, groups_ctrl=['Zro', 'Offset', 'All'], ctrl_size=scale * 0.035,
                                      ctrl_color=ctrlColor, lock_channels=['v', 's'], side=side, suffix=suffixController
                                      )
        # controller lft 02
        controllerBind02 = ct.Control(match_obj_first_position=self.jnt02, prefix=self.prefixNameCrv + 'Drv02',
                                      shape=shape, groups_ctrl=['Zro', 'Offset'], ctrl_size=scale * 0.05,
                                      ctrl_color=ctrlColor, lock_channels=['v', 's'], side=side, suffix=suffixController
                                      )

        # create grp controller and parent into it
        grpDrvCtrl = mc.createNode('transform', n=self.prefixNameCrv + 'Ctrl' + side + '_grp')
        mc.parent(controllerBind03.parent_control[0], controllerBind05.parent_control[0],
                  controllerBind04.parent_control[0],
                  controllerBind01.parent_control[0], controllerBind02.parent_control[0], grpDrvCtrl)

        # connect group parent bind joint 01 and 02 to the controller grp parent 01 and 02
        au.connectAttrTransRot(self.jointBindGrp04, controllerBind04.parent_control[0])
        au.connectAttrTransRot(self.jointBindGrp02, controllerBind02.parent_control[0])

        # connect bind parent zro to ctrl zro parent
        if not connectWithCornerCtrl:
            au.connect_attr_translate(self.jointBindGrp05, controllerBind05.parent_control[0])
            au.connect_attr_translate(self.jointBindGrp01, controllerBind01.parent_control[0])

       # flipping controller
        if controllerWireLow:
            if self.pos >= 0:
                # LOW LID LFT
                mc.setAttr(controllerBind01.parent_control[1] + '.scaleX', -1)
                mc.setAttr(controllerBind02.parent_control[1] + '.scaleX', -1)
                mc.setAttr(controllerBind04.parent_control[1] + '.scaleX', 1)
                mc.setAttr(controllerBind05.parent_control[1] + '.scaleX', 1)

                # connect translate controller to joint
                # right side 01 translate and rotate
                tf.bind_translate_reverse(control=controllerBind01.control,
                                          input_2X=-1, input_2Y=-1, input_2Z=1,
                                          joint_bind_target=self.jnt01, side_RGT=sideRGT, side_LFT=sideLFT, side=side)
                tf.bind_rotate_reverse(control=controllerBind01.control,
                                       input_2X=-1, input_2Y=-1, input_2Z=1,
                                       joint_bind_target=self.jnt01, side_RGT=sideRGT, side_LFT=sideLFT, side=side)

                # right side 02 translate and rotate
                tf.bind_translate_reverse(control=controllerBind02.control,
                                          input_2X=-1, input_2Y=-1, input_2Z=1,
                                          joint_bind_target=self.jnt02, side_RGT=sideRGT, side_LFT=sideLFT, side=side)
                tf.bind_rotate_reverse(control=controllerBind02.control,
                                       input_2X=-1, input_2Y=-1, input_2Z=1,
                                       joint_bind_target=self.jnt02, side_RGT=sideRGT, side_LFT=sideLFT, side=side)

                # left side 04 translate and rotate
                tf.bind_translate_reverse(control=controllerBind04.control,
                                          input_2X=1, input_2Y=-1, input_2Z=1,
                                          joint_bind_target=self.jnt04, side_RGT=sideRGT, side_LFT=sideLFT, side=side)
                tf.bind_rotate_reverse(control=controllerBind04.control,
                                       input_2X=-1, input_2Y=1, input_2Z=-1,
                                       joint_bind_target=self.jnt04, side_RGT=sideRGT, side_LFT=sideLFT, side=side)

                # left side 05 translate and rotate
                tf.bind_translate_reverse(control=controllerBind05.control,
                                          input_2X=1, input_2Y=-1, input_2Z=1,
                                          joint_bind_target=self.jnt05, side_RGT=sideRGT, side_LFT=sideLFT, side=side)
                tf.bind_rotate_reverse(control=controllerBind05.control,
                                       input_2X=-1, input_2Y=1, input_2Z=-1,
                                       joint_bind_target=self.jnt05, side_RGT=sideRGT, side_LFT=sideLFT, side=side)
            else:
                # LOW LID RGT
                mc.setAttr(controllerBind01.parent_control[1] + '.scaleX', 1)
                mc.setAttr(controllerBind02.parent_control[1] + '.scaleX', 1)
                mc.setAttr(controllerBind04.parent_control[1] + '.scaleX', -1)
                mc.setAttr(controllerBind05.parent_control[1] + '.scaleX', -1)
                # connect translate controller to joint
                # right side 01 translate and rotate
                tf.bind_translate_reverse(control=controllerBind01.control,
                                          input_2X=1, input_2Y=-1, input_2Z=1,
                                          joint_bind_target=self.jnt01, side_RGT=sideRGT, side_LFT=sideLFT, side=side)
                tf.bind_rotate_reverse(control=controllerBind01.control,
                                       input_2X=-1, input_2Y=1, input_2Z=-1,
                                       joint_bind_target=self.jnt01, side_RGT=sideRGT, side_LFT=sideLFT, side=side)

                # right side 02 translate and rotate
                tf.bind_translate_reverse(control=controllerBind02.control,
                                          input_2X=1, input_2Y=-1, input_2Z=1,
                                          joint_bind_target=self.jnt02, side_RGT=sideRGT, side_LFT=sideLFT, side=side)
                tf.bind_rotate_reverse(control=controllerBind02.control,
                                       input_2X=-1, input_2Y=1, input_2Z=-1,
                                       joint_bind_target=self.jnt02, side_RGT=sideRGT, side_LFT=sideLFT, side=side)

                # left side 04 translate and rotate
                tf.bind_translate_reverse(control=controllerBind04.control,
                                          input_2X=-1, input_2Y=-1, input_2Z=1,
                                          joint_bind_target=self.jnt04, side_RGT=sideRGT, side_LFT=sideLFT, side=side)
                tf.bind_rotate_reverse(control=controllerBind04.control,
                                       input_2X=-1, input_2Y=-1, input_2Z=1,
                                       joint_bind_target=self.jnt04, side_RGT=sideRGT, side_LFT=sideLFT, side=side)


                # left side 05 translate and rotate
                tf.bind_translate_reverse(control=controllerBind05.control,
                                          input_2X=-1, input_2Y=-1, input_2Z=1,
                                          joint_bind_target=self.jnt05, side_RGT=sideRGT, side_LFT=sideLFT, side=side)
                tf.bind_rotate_reverse(control=controllerBind05.control,
                                       input_2X=-1, input_2Y=-1, input_2Z=1,
                                       joint_bind_target=self.jnt05, side_RGT=sideRGT, side_LFT=sideLFT, side=side)

            mc.setAttr(controllerBind01.parent_control[1] + '.scaleY', -1)
            mc.setAttr(controllerBind02.parent_control[1] + '.scaleY', -1)
            mc.setAttr(controllerBind03.parent_control[1] + '.scaleY', -1)
            mc.setAttr(controllerBind05.parent_control[1] + '.scaleY', -1)
            mc.setAttr(controllerBind04.parent_control[1] + '.scaleY', -1)

            # mid translate and rotate
            tf.bind_translate_reverse(control=controllerBind03.control,
                                      input_2X=1, input_2Y=-1, input_2Z=1,
                                      joint_bind_target=self.jnt03, side_RGT=sideRGT, side_LFT=sideLFT, side=side)
            tf.bind_rotate_reverse(control=controllerBind03.control,
                                   input_2X=-1, input_2Y=1, input_2Z=-1,
                                   joint_bind_target=self.jnt03, side_RGT=sideRGT, side_LFT=sideLFT, side=side)

        else:
            # left side 03 translate and rotate
            au.connectAttrTransRot(controllerBind03.control, self.jnt03)

            # UPLID LFT
            if self.pos >= 0:
                mc.setAttr(controllerBind01.parent_control[1] + '.scaleX', -1)
                mc.setAttr(controllerBind02.parent_control[1] + '.scaleX', -1)
                mc.setAttr(controllerBind04.parent_control[1] + '.scaleX', 1)
                mc.setAttr(controllerBind05.parent_control[1] + '.scaleX', 1)

                # right side 01 translate and rotate
                tf.bind_translate_reverse(control=controllerBind01.control,
                                          input_2X=-1, input_2Y=1, input_2Z=1,
                                          joint_bind_target=self.jnt01, side_RGT=sideRGT, side_LFT=sideLFT, side=side)
                tf.bind_rotate_reverse(control=controllerBind01.control,
                                       input_2X=1, input_2Y=-1, input_2Z=-1,
                                       joint_bind_target=self.jnt01, side_RGT=sideRGT, side_LFT=sideLFT, side=side)

                # right side 02 translate and rotate
                tf.bind_translate_reverse(control=controllerBind02.control,
                                          input_2X=-1, input_2Y=1, input_2Z=1,
                                          joint_bind_target=self.jnt02, side_RGT=sideRGT, side_LFT=sideLFT, side=side)
                tf.bind_rotate_reverse(control=controllerBind02.control,
                                       input_2X=1, input_2Y=-1, input_2Z=-1,
                                       joint_bind_target=self.jnt02, side_RGT=sideRGT, side_LFT=sideLFT, side=side)


                # left side 04 translate and rotate
                au.connectAttrTransRot(controllerBind04.control, self.jnt04)

                # left side 05 translate and rotate
                au.connectAttrTransRot(controllerBind05.control, self.jnt05)

            else:
                # UPLID RGT
                mc.setAttr(controllerBind01.parent_control[1] + '.scaleX', 1)
                mc.setAttr(controllerBind02.parent_control[1] + '.scaleX', 1)
                mc.setAttr(controllerBind04.parent_control[1] + '.scaleX', -1)
                mc.setAttr(controllerBind05.parent_control[1] + '.scaleX', -1)

                # right side 01 translate and rotate
                au.connectAttrTransRot(controllerBind01.control, self.jnt01)

                # right side 02 translate and rotate
                au.connectAttrTransRot(controllerBind02.control, self.jnt02)

                # left side 04 translate and rotate
                tf.bind_translate_reverse(control=controllerBind04.control,
                                          input_2X=-1, input_2Y=1, input_2Z=1,
                                          joint_bind_target=self.jnt04, side_RGT=sideRGT, side_LFT=sideLFT, side=side)
                tf.bind_rotate_reverse(control=controllerBind04.control,
                                       input_2X=1, input_2Y=-1, input_2Z=-1,
                                       joint_bind_target=self.jnt04, side_RGT=sideRGT, side_LFT=sideLFT, side=side)

                # left side 05 translate and rotate
                tf.bind_translate_reverse(control=controllerBind05.control,
                                          input_2X=-1, input_2Y=1, input_2Z=1,
                                          joint_bind_target=self.jnt05, side_RGT=sideRGT, side_LFT=sideLFT, side=side)
                tf.bind_rotate_reverse(control=controllerBind05.control,
                                       input_2X=1, input_2Y=-1, input_2Z=-1,
                                       joint_bind_target=self.jnt05, side_RGT=sideRGT, side_LFT=sideLFT, side=side)

        # # CONNECT GROUP PARENT BIND JOINT 01 AND 02 TO THE CONTROLLER GRP PARENT 01 AND 02
        # au.connectAttrTransRot(jointBind02Grp[0], controllerBind02.parentControl[0])
        # au.connectAttrTransRot(self.jointBind04Grp[0], controllerBind04.parentControl[0])

        self.grpDrvCtrl=grpDrvCtrl
        self.controllerBind01 = controllerBind01.control
        self.controllerBindZro01 = controllerBind01.parent_control[0]

        self.controllerBind05 = controllerBind05.control
        self.controllerBindZro05 = controllerBind05.parent_control[0]

        self.controllerBind03 = controllerBind03.control
        self.controllerBindZro03 = controllerBind03.parent_control[0]

        # CONNECT OFFSET BIND TO CTRL BIND
        au.connect_attr_translate(self.jointBindOffset01, controllerBind01.parent_control[1])
        au.connect_attr_translate(self.jointBindOffset02, controllerBind02.parent_control[1])
        au.connect_attr_translate(self.jointBindOffset03, controllerBind03.parent_control[1])
        au.connect_attr_translate(self.jointBindOffset04, controllerBind04.parent_control[1])
        au.connect_attr_translate(self.jointBindOffset05, controllerBind05.parent_control[1])


    def wireBindCurve(self, crv, offsetJnt02BindPos, offsetJnt04BindPos, directionCtrl01, directionCtrl02,
                      directionCtrl03, directionCtrl04, directionCtrl05, scale, side=''):
        jointPosBind = len(self.allJoint)

        # query position of bind joint
        joint01 =  self.allJoint[(jointPosBind * 0)]

        joint02 =  self.allJoint[(jointPosBind / 4) + offsetJnt02BindPos]

        if not len(self.allJoint) % 2 == 0:
            joint03 = self.allJoint[int(jointPosBind / 2)]
            self.xformJnt03 = mc.xform(joint03, ws=1, q=1, t=1)

        else:
            tempJnt03 = self.allJoint[int(jointPosBind / 2)]
            tempsjoint03 = self.allJoint[int(jointPosBind / 2)-1]
            transform = mc.createNode('transform', n='guide')
            joint03 = mc.delete(mc.parentConstraint(tempJnt03, tempsjoint03, transform))
            self.xformJnt03 = mc.xform(joint03, ws=1, q=1, t=1)
            mc.delete(transform)

        joint04 =  self.allJoint[(((jointPosBind / 2) + (jointPosBind / 4)) - offsetJnt04BindPos)+1]
        joint05 =  self.allJoint[-1]

        # query the position right side
        self.xformJnt01 = mc.xform(joint01, ws=1, q=1, t=1)
        self.xformJnt02 = mc.xform(joint02, ws=1, q=1, t=1)
        self.xformJnt04 = mc.xform(joint04, ws=1, q=1, t=1)
        self.xformJnt05 = mc.xform(joint05, ws=1, q=1, t=1)
        # mc.delete(transform)

        mc.select(cl=1)
        self.jnt01  = mc.joint(n=au.prefix_name(self.prefixNameCrv) + '01' + side + '_bind', p=self.xformJnt01, rad=0.5 * scale)
        self.jnt02  = mc.duplicate(self.jnt01, n=au.prefix_name(self.prefixNameCrv) + '02' + side + '_bind')[0]
        self.jnt03  = mc.duplicate(self.jnt01, n=au.prefix_name(self.prefixNameCrv) + '03' + side + '_bind')[0]
        self.jnt04  = mc.duplicate(self.jnt01, n=au.prefix_name(self.prefixNameCrv) + '04' + side + '_bind')[0]
        self.jnt05  = mc.duplicate(self.jnt01, n=au.prefix_name(self.prefixNameCrv) + '05' + side + '_bind')[0]

        # set the position RGT joint
        mc.xform(self.jnt02, ws=1, t=self.xformJnt02)
        mc.xform(self.jnt03, ws=1, t=self.xformJnt03)
        mc.xform(self.jnt04, ws=1, t=self.xformJnt04)
        mc.xform(self.jnt05, ws=1, t=self.xformJnt05)

        # create bind curve
        deformCrv = mc.duplicate(crv)[0]

        deformCrv = mc.rename(deformCrv, (au.prefix_name(self.prefixNameCrv) + 'Bind' + side + '_crv'))


        # parent the bind joint
        jointBindGrp03 = tf.create_parent_transform(parent_list=['Zro', 'Offset'], object=self.jnt03,
                                                    match_position=self.jnt03, prefix=self.prefixNameCrv + 'Drv03',
                                                    suffix='_bind', side=side)

        jointBindGrp05 = tf.create_parent_transform(parent_list=['Zro', 'Offset', 'All', 'Corner'], object=self.jnt05,
                                                    match_position=self.jnt05, prefix=self.prefixNameCrv + 'Drv05',
                                                    suffix='_bind', side=side)

        jointBindGrp04 = tf.create_parent_transform(parent_list=['Zro', 'Offset'], object=self.jnt04,
                                                    match_position=self.jnt04, prefix=self.prefixNameCrv + 'Drv04',
                                                    suffix='_bind', side=side)

        jointBindGrp01 = tf.create_parent_transform(parent_list=['Zro', 'Offset', 'All', 'Corner'], object=self.jnt01,
                                                    match_position=self.jnt01, prefix=self.prefixNameCrv + 'Drv01',
                                                    suffix='_bind', side=side)

        jointBindGrp02 = tf.create_parent_transform(parent_list=['Zro', 'Offset'], object=self.jnt02,
                                                    match_position=self.jnt02, prefix=self.prefixNameCrv + 'Drv02',
                                                    suffix='_bind', side=side)

        if self.pos > 0:
            mc.setAttr(jointBindGrp01[0] + '.rotateY', directionCtrl01 * -1)
            mc.setAttr(jointBindGrp02[0] + '.rotateY', directionCtrl02 * -1)
            mc.setAttr(jointBindGrp03[0] + '.rotateY', directionCtrl03)
            mc.setAttr(jointBindGrp05[0] + '.rotateY', directionCtrl05)
            mc.setAttr(jointBindGrp04[0] + '.rotateY', directionCtrl04)

        else:
            mc.setAttr(jointBindGrp01[0] + '.rotateY', directionCtrl01)
            mc.setAttr(jointBindGrp02[0] + '.rotateY', directionCtrl02)
            mc.setAttr(jointBindGrp03[0] + '.rotateY', directionCtrl03 * -1)
            mc.setAttr(jointBindGrp05[0] + '.rotateY', directionCtrl05 * -1)
            mc.setAttr(jointBindGrp04[0] + '.rotateY', directionCtrl04 * -1)

        # # rotation bind joint follow the mouth shape
        # mc.setAttr(jointBindGrp05[0] + '.rotateY', directionCtrl01 * -1)
        # mc.setAttr(jointBindGrp04[0] + '.rotateY', directionCtrl02 * -1)
        # mc.setAttr(jointBindGrp01[0] + '.rotateY', directionCtrl01)
        # mc.setAttr(jointBindGrp02[0] + '.rotateY', directionCtrl02)

        # rebuild the curve
        mc.rebuildCurve(deformCrv, rpo=1, rt=0, end=1, kr=0, kcp=0,
                        kep=1, kt=0, s=8, d=3, tol=0.01)

        # skinning the joint to the bind curve
        skinCls = mc.skinCluster([self.jnt05, self.jnt04, self.jnt01, self.jnt02, self.jnt03], deformCrv,
                                 n='%s%s%s%s' % (au.prefix_name(self.prefixNameCrv), 'Wire', side, 'SkinCluster'), tsb=True,
                                 bm=0, sm=0, nw=1, mi=3)

        # Distribute the skin
        skinPercent0 = '%s.cv[0]' % deformCrv
        skinPercent1 = '%s.cv[1]' % deformCrv
        skinPercent2 = '%s.cv[2]' % deformCrv
        skinPercent3 = '%s.cv[3]' % deformCrv
        skinPercent4 = '%s.cv[4]' % deformCrv
        skinPercent5 = '%s.cv[5]' % deformCrv
        skinPercent6 = '%s.cv[6]' % deformCrv
        skinPercent7 = '%s.cv[7]' % deformCrv
        skinPercent8 = '%s.cv[8]' % deformCrv
        skinPercent9 = '%s.cv[9]' % deformCrv
        skinPercent10 = '%s.cv[10]' % deformCrv

        mc.skinPercent(skinCls[0], skinPercent0, tv=[(self.jnt01, 1.0)])
        mc.skinPercent(skinCls[0], skinPercent1, tv=[(self.jnt01, 0.9), (self.jnt02, 0.1)])
        mc.skinPercent(skinCls[0], skinPercent2, tv=[(self.jnt01, 0.7), (self.jnt02, 0.3)])
        mc.skinPercent(skinCls[0], skinPercent3, tv=[(self.jnt02, 0.5), (self.jnt01, 0.25), (self.jnt03, 0.25)])
        mc.skinPercent(skinCls[0], skinPercent4, tv=[(self.jnt02, 0.3), (self.jnt03, 0.7)])
        mc.skinPercent(skinCls[0], skinPercent5, tv=[(self.jnt03, 1.0)])
        mc.skinPercent(skinCls[0], skinPercent6, tv=[(self.jnt04, 0.3), (self.jnt03, 0.7)])
        mc.skinPercent(skinCls[0], skinPercent7, tv=[(self.jnt04, 0.5), (self.jnt05, 0.25), (self.jnt03, 0.25)])
        mc.skinPercent(skinCls[0], skinPercent8, tv=[(self.jnt05, 0.7), (self.jnt04, 0.3)])
        mc.skinPercent(skinCls[0], skinPercent9, tv=[(self.jnt05, 0.9), (self.jnt04, 0.1)])
        mc.skinPercent(skinCls[0], skinPercent10, tv=[(self.jnt05, 1.0)])

        # wire the curve
        wireDef = mc.wire(crv, dds=(0, 100 * scale), wire=deformCrv)
        wireDef[0] = mc.rename(wireDef[0], (au.prefix_name(self.prefixNameCrv) + side + '_wireNode'))
        mc.setAttr(wireDef[0] + '.scale[0]', 0)

        # constraint mid to 02 left and right
        jntBindGrp02Cons = mc.parentConstraint(self.jnt03, self.jnt01, jointBindGrp02[0], mo=1)
        jntBindGrp04Cons = mc.parentConstraint(self.jnt03, self.jnt05, jointBindGrp04[0], mo=1)

        # rename constraint
        au.constraint_rename([jntBindGrp02Cons[0], jntBindGrp04Cons[0]])

        # create grp curves
        curvesGrp = mc.createNode('transform', n=self.prefixNameCrv + 'DrvCrv' + side+ '_grp')
        mc.setAttr(curvesGrp + '.it', 0, l=1)
        mc.parent(deformCrv, mc.listConnections(wireDef[0] + '.baseWire[0]')[0], curvesGrp)
        mc.hide(curvesGrp)

        # create grp bind
        bindJntGrp = mc.createNode('transform', n=self.prefixNameCrv + 'DrvJntBind' + side+ '_grp')
        mc.parent(jointBindGrp03[0], jointBindGrp05[0], jointBindGrp04[0],
                  jointBindGrp01[0], jointBindGrp02[0], bindJntGrp)
        mc.hide(bindJntGrp)

        self.jointBindGrp04 = jointBindGrp04[0]
        self.jointBindGrp02 = jointBindGrp02[0]
        self.jointBindGrpAll05 = jointBindGrp05[2]
        self.jointBindGrpAll01 = jointBindGrp01[2]
        self.jointBindGrp05 = jointBindGrp05[0]
        self.jointBindGrp01 = jointBindGrp01[0]
        self.jointBindGrp03 = jointBindGrp03[0]

        self.jointBindOffset04 = jointBindGrp04[1]
        self.jointBindOffset02 = jointBindGrp02[1]
        self.jointBindOffset05 = jointBindGrp05[1]
        self.jointBindOffset01 = jointBindGrp01[1]
        self.jointBindOffset03 = jointBindGrp03[1]

        self.jointBindCorner01 = jointBindGrp01[3]
        self.jointBindCorner05 = jointBindGrp05[3]


        self.curvesGrp = curvesGrp
        self.bindJntGrp =bindJntGrp

    def createJointWire(self, crv,side, scale):

        vtxCrv = mc.ls('%s.cv[0:*]' % crv, fl=True)

        self.allJoint = []
        self.parentLocGrpOffset = []
        self.parentLocGrpZro = []
        # self.allLocator = []
        self.parentJntGrpZro = []

        for i, v in enumerate(vtxCrv):
            # create joint
            mc.select(cl=1)
            joint = mc.joint(n='%s%02d%s%s' % (self.prefixNameCrv, (i + 1), side, '_jnt'), rad=0.1 * scale)
            pos = mc.xform(v, q=1, ws=1, t=1)
            mc.xform(joint, ws=1, t=pos)
            self.allJoint.append(joint)

            parentJntGrp = tf.create_parent_transform(parent_list=[''], object=joint,
                                                      match_position=joint,
                                                      prefix=self.prefixNameCrv + str(i + 1).zfill(2),
                                                      suffix='_jnt', side=side)

            self.parentJntGrpZro.append(parentJntGrp[0])
            # create locator
            # locator = mc.spaceLocator(n='%s%02d%s%s' % (self.prefixNameCrv, (i + 1), side, '_loc'))[0]
            groupOffset = mc.spaceLocator(n='%s%s%02d%s%s' % (self.prefixNameCrv, 'Offset', (i + 1), side, '_loc'))[0]
            mc.hide(groupOffset)

            mc.xform(groupOffset, ws=1, t=pos)
            parentLocGrp = tf.create_parent_transform(parent_list=[''], object=groupOffset,
                                                      match_position=groupOffset, prefix=self.prefixNameCrv + str(i + 1).zfill(2),
                                                      suffix='_zro', side=side)
            self.parentLocGrpOffset.append(groupOffset)
            self.parentLocGrpZro.append(parentLocGrp[0])
            # self.allLocator.append(groupOffset)

            # connect curve to locator grp
            curveRelatives = mc.listRelatives(crv, s=True)[0]
            u = self.getUParam(pos, curveRelatives)
            pci = mc.createNode("pointOnCurveInfo", n='%s%02d%s%s' % (self.prefixNameCrv, (i + 1), side,'_pci'))
            mc.connectAttr(curveRelatives + '.worldSpace', pci + '.inputCurve')
            mc.setAttr(pci + '.parameter', u)
            mc.connectAttr(pci + '.position', parentLocGrp[0] + '.t')

            dMtx = mc.createNode('decomposeMatrix', n='%s%02d%s%s' % (self.prefixNameCrv, (i + 1), side,'_dmtx'))
            mc.connectAttr(groupOffset + '.worldMatrix[0]', dMtx + '.inputMatrix')

            mc.connectAttr(dMtx + '.outputTranslate', parentJntGrp[0] + '.translate')
            mc.connectAttr(dMtx + '.outputRotate', parentJntGrp[0] + '.rotate')

        # grouping joint
        self.jointGrp = mc.group(em=1, n=self.prefixNameCrv + 'Jnt' +side+ '_grp')
        mc.parent(self.parentJntGrpZro, self.jointGrp)

        # grouping locator
        self.locatorGrp = mc.group(em=1, n=self.prefixNameCrv + 'Loc' +side+ '_grp')
        mc.setAttr(self.locatorGrp + '.it', 0, l=1)
        mc.parent(self.parentLocGrpZro, self.locatorGrp)

    def replacePosLFTRGT(self, crv, sideRGT, sideLFT):
        if sideRGT in crv:
            crvNewName = crv.replace(sideRGT, '')
        elif sideLFT in crv:
            crvNewName = crv.replace(sideLFT, '')
        else:
            crvNewName = crv

        return crvNewName
    def getUParam(self, pnt=[], crv=None):
        point = om.MPoint(pnt[0], pnt[1], pnt[2])
        curveFn = om.MFnNurbsCurve(self.getDagPath(crv))
        paramUtill = om.MScriptUtil()
        paramPtr = paramUtill.asDoublePtr()
        isOnCurve = curveFn.isPointOnCurve(point)
        if isOnCurve == True:

            curveFn.getParamAtPoint(point, paramPtr, 0.001, om.MSpace.kObject)
        else:
            point = curveFn.closestPoint(point, paramPtr, 0.001, om.MSpace.kObject)
            curveFn.getParamAtPoint(point, paramPtr, 0.001, om.MSpace.kObject)

        param = paramUtill.getDouble(paramPtr)
        return param

    def getDagPath(self, objectName):
        if isinstance(objectName, list) == True:
            oNodeList = []
            for o in objectName:
                selectionList = om.MSelectionList()
                selectionList.add(o)
                oNode = om.MDagPath()
                selectionList.getDagPath(0, oNode)
                oNodeList.append(oNode)
            return oNodeList
        else:
            selectionList = om.MSelectionList()
            selectionList.add(objectName)
            oNode = om.MDagPath()
            selectionList.getDagPath(0, oNode)
            return oNode