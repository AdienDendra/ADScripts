from __builtin__ import reload

import maya.OpenMaya as om
import maya.cmds as mc
from rigLib.utils import controller as ct, transform as tf

from rigging.tools import AD_utils as au

reload (ct)
reload (au)
reload (tf)

# load Plug-ins
matrixNode = mc.pluginInfo('matrixNodes.mll', query=True, loaded=True)
quatNode = mc.pluginInfo('quatNodes.mll', query=True, loaded=True)

if not matrixNode:
    mc.loadPlugin( 'matrixNodes.mll' )

if not quatNode:
    mc.loadPlugin( 'quatNodes.mll' )

class Build:
    def __init__(self, crv, eyeJnt, worldUpObject,
                 scale, sideLFT, sideRGT, side, offsetLidPos02Jnt, offsetLidPos04Jnt,
                 directionLid01, directionLid02, directionLid03, directionLid04, directionLid05,
                 ctrlColor, ctrlShape, controllerLidLow, eyeLid):

        self.pos = mc.xform(eyeJnt, q=1, ws=1, t=1)[0]

        self.vtxCrv = mc.ls('%s.cv[0:*]' % crv, fl=True)

        self.createJointLid(crv=crv, worldUpObject=worldUpObject, scale=scale, eyeJnt=eyeJnt,
                            sideLFT=sideLFT, sideRGT=sideRGT, side=side, eyeLid=eyeLid)

        self.wireBindCurve(sideLFT=sideLFT, sideRGT=sideRGT, crv=crv, scale=scale, side=side,
                           directionLid01=directionLid01, eyeJnt=eyeJnt, directionLid03=directionLid03,
                           directionLid02=directionLid02, directionLid04=directionLid04, directionLid05=directionLid05,
                           offsetPos02Jnt=offsetLidPos02Jnt, offsetPos04Jnt=offsetLidPos04Jnt)


        self.controllerLid(sideLFT=sideLFT, sideRGT=sideRGT, scale=scale, side=side, crv=crv,
                           controllerLidLow=controllerLidLow, ctrlColor=ctrlColor, ctrlShape=ctrlShape)


    def controllerLid(self, sideRGT, sideLFT, scale, side, crv, controllerLidLow, ctrlShape, ctrlColor):
        crvNewName = self.replacePosLFTRGT(crv=crv, sideRGT=sideRGT, sideLFT=sideLFT)

        # controller 03
        self.controllerBind03 = ct.Control(match_obj_first_position=self.jnt03, prefix=au.prefix_name(crvNewName) + '03',
                                           shape=ctrlShape, groups_ctrl=['Zro', 'Offset'], ctrl_size=scale * 1.0,
                                           ctrl_color='red', lock_channels=['v', 's'], side=side
                                           )
        # ADD ATTRIBUTE
        au.add_attribute(objects=[self.controllerBind03.control], long_name=['lid'], nice_name=[' '], at="enum",
                         en='Eyelid', channel_box=True)

        self.closeLid = au.add_attribute(objects=[self.controllerBind03.control], long_name=['closeLid'],
                                         attributeType="float", min=0, max=1, dv=0, keyable=True)

        self.controllerBind03Ctrl = self.controllerBind03.control
        self.controllerBind03OffsetCtrl = self.controllerBind03.parent_control[1]

        # controller 01
        self.controllerBind01 = ct.Control(match_obj_first_position=self.jnt01, prefix=au.prefix_name(crvNewName) + '01',
                                           shape=ctrlShape, groups_ctrl=['Zro', 'Offset', 'All'], ctrl_size=scale * 0.5,
                                           ctrl_color=ctrlColor, lock_channels=['v', 's'], side=side
                                           )
        self.controllerBindGrpZro01 = self.controllerBind01.parent_control[0]

        # controller 02
        self.controllerBind02 = ct.Control(match_obj_first_position=self.jnt02, prefix=au.prefix_name(crvNewName) + '02',
                                           shape=ctrlShape, groups_ctrl=['Zro', 'Offset'], ctrl_size=scale * 0.7,
                                           ctrl_color=ctrlColor, lock_channels=['v', 's'], side=side
                                           )
        # controller 05
        self.controllerBind05 = ct.Control(match_obj_first_position=self.jnt05, prefix=au.prefix_name(crvNewName) + '05',
                                           shape=ctrlShape, groups_ctrl=['Zro', 'Offset', 'All'], ctrl_size=scale * 0.5,
                                           ctrl_color=ctrlColor, lock_channels=['v', 's'], side=side
                                           )
        self.controllerBindGrpZro05 = self.controllerBind05.parent_control[0]

        # controller 04
        self.controllerBind04 = ct.Control(match_obj_first_position=self.jnt04, prefix=au.prefix_name(crvNewName) + '04',
                                           shape=ctrlShape, groups_ctrl=['Zro', 'Offset'], ctrl_size=scale * 0.7,
                                           ctrl_color=ctrlColor, lock_channels=['v', 's'], side=side
                                           )

        # create grp controller and parent into it
        self.grpDrvCtrl = mc.createNode('transform', n=au.prefix_name(crvNewName) + 'Ctrl' + side + '_grp')
        mc.parent(self.controllerBind03.parent_control[0], self.controllerBind01.parent_control[0], self.controllerBind02.parent_control[0],
                  self.controllerBind05.parent_control[0], self.controllerBind04.parent_control[0], self.grpDrvCtrl)

        # flipping controller
        if controllerLidLow:
            if self.pos > 0:
                mc.setAttr(self.controllerBind01.parent_control[0] + '.scaleX', -1)
                mc.setAttr(self.controllerBind02.parent_control[0] + '.scaleX', -1)
                mc.setAttr(self.controllerBind04.parent_control[0] + '.scaleX', 1)
                mc.setAttr(self.controllerBind05.parent_control[0] + '.scaleX', 1)

                # connect translate controller to joint
                # right side 01 translate and rotate
                self.bindTranslateReverse(control=self.controllerBind01.control,
                                          input2X=-1, input2Y=-1, input2Z=1,
                                          jointBindTarget=self.jnt01)

                # right side 02 translate and rotate
                self.bindTranslateReverse(control=self.controllerBind02.control,
                                          input2X=-1, input2Y=-1, input2Z=1,
                                          jointBindTarget=self.jnt02)

                # left side 02 translate and rotate
                self.bindTranslateReverse(control=self.controllerBind04.control,
                                          input2X=1, input2Y=-1, input2Z=1,
                                          jointBindTarget=self.jnt04)

                # left side 01 translate and rotate
                self.bindTranslateReverse(control=self.controllerBind05.control,
                                          input2X=1, input2Y=-1, input2Z=1,
                                          jointBindTarget=self.jnt05)
            else:
                mc.setAttr(self.controllerBind01.parent_control[0] + '.scaleX', 1)
                mc.setAttr(self.controllerBind02.parent_control[0] + '.scaleX', 1)
                mc.setAttr(self.controllerBind04.parent_control[0] + '.scaleX', -1)
                mc.setAttr(self.controllerBind05.parent_control[0] + '.scaleX', -1)
                # connect translate controller to joint
                # right side 01 translate and rotate
                self.bindTranslateReverse(control=self.controllerBind01.control,
                                          input2X=1, input2Y=-1, input2Z=1,
                                          jointBindTarget=self.jnt01)

                # right side 02 translate and rotate
                self.bindTranslateReverse(control=self.controllerBind02.control,
                                          input2X=1, input2Y=-1, input2Z=1,
                                          jointBindTarget=self.jnt02)

                # left side 02 translate and rotate
                self.bindTranslateReverse(control=self.controllerBind04.control,
                                          input2X=-1, input2Y=-1, input2Z=1,
                                          jointBindTarget=self.jnt04)

                # left side 01 translate and rotate
                self.bindTranslateReverse(control=self.controllerBind05.control,
                                          input2X=-1, input2Y=-1, input2Z=1,
                                          jointBindTarget=self.jnt05)

            mc.setAttr(self.controllerBind01.parent_control[0] + '.scaleY', -1)
            mc.setAttr(self.controllerBind02.parent_control[0] + '.scaleY', -1)

            mc.setAttr(self.controllerBind05.parent_control[0] + '.scaleY', -1)
            mc.setAttr(self.controllerBind04.parent_control[0] + '.scaleY', -1)

            mc.setAttr(self.controllerBind03.parent_control[0] + '.scaleY', -1)

            au.connect_attr_rotate(self.controllerBind01.control, self.jnt01)

            au.connect_attr_rotate(self.controllerBind02.control, self.jnt02)

            # mid translate and rotate
            self.bindTranslateReverse(control=self.controllerBind03.control,
                                      input2X=1, input2Y=-1, input2Z=1,
                                      jointBindTarget=self.jnt03)

            au.connect_attr_rotate(self.controllerBind03.control, self.jnt03)

            au.connect_attr_rotate(self.controllerBind04.control, self.jnt04)

            au.connect_attr_rotate(self.controllerBind05.control, self.jnt05)

        else:
            if self.pos > 0:
                mc.setAttr(self.controllerBind01.parent_control[0] + '.scaleX', -1)
                mc.setAttr(self.controllerBind02.parent_control[0] + '.scaleX', -1)
                mc.setAttr(self.controllerBind04.parent_control[0] + '.scaleX', 1)
                mc.setAttr(self.controllerBind05.parent_control[0] + '.scaleX', 1)

                # right side 01 translate and rotate
                self.bindTranslateReverse(control=self.controllerBind01.control,
                                          input2X=-1, input2Y=1, input2Z=1,
                                          jointBindTarget=self.jnt01)
                # right side 02 translate and rotate
                self.bindTranslateReverse(control=self.controllerBind02.control,
                                          input2X=-1, input2Y=1, input2Z=1,
                                          jointBindTarget=self.jnt02)
                # left side 02 translate and rotate
                self.bindTranslateReverse(control=self.controllerBind04.control,
                                          input2X=1, input2Y=1, input2Z=1,
                                          jointBindTarget=self.jnt04)

                # left side 01 translate and rotate
                self.bindTranslateReverse(control=self.controllerBind05.control,
                                          input2X=1, input2Y=1, input2Z=1,
                                          jointBindTarget=self.jnt05)

            else:
                mc.setAttr(self.controllerBind01.parent_control[0] + '.scaleX', 1)
                mc.setAttr(self.controllerBind02.parent_control[0] + '.scaleX', 1)
                mc.setAttr(self.controllerBind04.parent_control[0] + '.scaleX', -1)
                mc.setAttr(self.controllerBind05.parent_control[0] + '.scaleX', -1)

                # right side 01 translate and rotate
                self.bindTranslateReverse(control=self.controllerBind01.control,
                                          input2X=1, input2Y=1, input2Z=1,
                                          jointBindTarget=self.jnt01)

                # right side 02 translate and rotate
                self.bindTranslateReverse(control=self.controllerBind02.control,
                                          input2X=1, input2Y=1, input2Z=1,
                                          jointBindTarget=self.jnt02)

                # left side 02 translate and rotate
                self.bindTranslateReverse(control=self.controllerBind04.control,
                                          input2X=-1, input2Y=1, input2Z=1,
                                          jointBindTarget=self.jnt04)

                # left side 01 translate and rotate
                self.bindTranslateReverse(control=self.controllerBind05.control,
                                          input2X=-1, input2Y=1, input2Z=1,
                                          jointBindTarget=self.jnt05)


            au.connect_attr_rotate(self.controllerBind02.control, self.jnt02)

            au.connect_attr_rotate(self.controllerBind01.control, self.jnt01)

            # left side 02 translate and rotate
            au.connect_attr_rotate(self.controllerBind04.control, self.jnt04)

            # left side 01 translate and rotate
            au.connect_attr_rotate(self.controllerBind05.control, self.jnt05)

            # mid translate and rotate
            au.connect_attr_translate_rotate(self.controllerBind03.control, self.jnt03)

    def bindTranslateReverse(self,  control, input2X, input2Y, input2Z, jointBindTarget):
        mdnReverse = mc.createNode('multiplyDivide', n=au.prefix_name(control) + '_mdn')
        mc.connectAttr(control + '.translate', mdnReverse + '.input1')

        mc.setAttr(mdnReverse + '.input2X', input2X)
        mc.setAttr(mdnReverse + '.input2Y', input2Y)
        mc.setAttr(mdnReverse + '.input2Z', input2Z)

        # connect to object
        mc.connectAttr(mdnReverse+'.output', jointBindTarget+'.translate')

    def wireBindCurve(self, sideRGT, sideLFT, crv, directionLid01, directionLid02, directionLid03,
                      directionLid04, directionLid05,
                      offsetPos02Jnt, offsetPos04Jnt,
                      scale, eyeJnt, side):

        crvNewName = self.replacePosLFTRGT(crv=crv, sideRGT=sideRGT, sideLFT=sideLFT)
        jointPosBind = len(self.allJoint)

        # query position of bind joint
        joint01 = self.allJoint[(jointPosBind * 0)]

        joint02 =  self.allJoint[(jointPosBind / 4) + offsetPos02Jnt]

        transform = None
        if not len(self.allJoint) % 2 == 0:
            joint03 = self.allJoint[int(jointPosBind / 2)]

        else:
            tempJnt03 = self.allJoint[int(jointPosBind / 2)]
            tempsjoint03 = self.allJoint[int(jointPosBind / 2)-1]
            transform = mc.createNode('transform', n='guide')
            joint03 = mc.delete(mc.parentConstraint(tempJnt03, tempsjoint03, transform))

        joint04 =  self.allJoint[((jointPosBind / 2) + (jointPosBind / 4)) - offsetPos04Jnt]
        joint05 =  self.allJoint[-1]

        # query the position right side
        self.xformJnt01 = mc.xform(joint01, ws=1, q=1, t=1)
        self.xformJnt02 = mc.xform(joint02, ws=1, q=1, t=1)
        self.xformJnt03 = mc.xform(joint03, ws=1, q=1, t=1)
        self.xformJnt04 = mc.xform(joint04, ws=1, q=1, t=1)
        self.xformJnt05 = mc.xform(joint05, ws=1, q=1, t=1)
        mc.delete(transform)

        mc.select(cl=1)
        jnt01  = mc.joint(n=au.prefix_name(crvNewName) + '01' + side + '_bind', p=self.xformJnt01, rad=0.5 * scale)
        jnt02  = mc.duplicate(jnt01, n=au.prefix_name(crvNewName) + '02' + side + '_bind')[0]
        jnt03  = mc.duplicate(jnt01, n=au.prefix_name(crvNewName) + '03' + side + '_bind')[0]
        jnt04  = mc.duplicate(jnt01, n=au.prefix_name(crvNewName) + '04' + side + '_bind')[0]
        jnt05  = mc.duplicate(jnt01, n=au.prefix_name(crvNewName) + '05' + side + '_bind')[0]

        # set the position RGT joint
        mc.xform(jnt02, ws=1, t=self.xformJnt02)
        mc.xform(jnt03, ws=1, t=self.xformJnt03)
        mc.xform(jnt04, ws=1, t=self.xformJnt04)
        mc.xform(jnt05, ws=1, t=self.xformJnt05)

        # create bind curve
        deformCrv = mc.duplicate(crv)[0]

        deformCrv = mc.rename(deformCrv, (au.prefix_name(crvNewName) + 'Bind' + side + '_crv'))

        # parent the bind joint
        self.jointBind03Grp = tf.create_parent_transform(parent_list=['Zro', 'Offset', 'All'], object=jnt03,
                                                         match_position=jnt03, prefix=au.prefix_name(crvNewName) + '03',
                                                         suffix='_bind', side=side)

        self.jointBind01Grp = tf.create_parent_transform(parent_list=['Zro', 'Offset'], object=jnt01,
                                                         match_position=jnt01, prefix=au.prefix_name(crvNewName) + '01',
                                                         suffix='_bind', side=side)

        self.jointBind02Grp = tf.create_parent_transform(parent_list=['Zro', 'Offset'], object=jnt02,
                                                         match_position=jnt02, prefix=au.prefix_name(crvNewName) + '02',
                                                         suffix='_bind', side=side)

        self.jointBind05Grp = tf.create_parent_transform(parent_list=['Zro', 'Offset'], object=jnt05,
                                                         match_position=jnt05, prefix=au.prefix_name(crvNewName) + '05',
                                                         suffix='_bind', side=side)

        self.jointBind04Grp = tf.create_parent_transform(parent_list=['Zro', 'Offset'], object=jnt04,
                                                         match_position=jnt04, prefix=au.prefix_name(crvNewName) + '04',
                                                         suffix='_bind', side=side)

        # assign bind grp jnt
        self.jointBind03GrpAll = self.jointBind03Grp[2]
        self.jointBind03GrpOffset = self.jointBind03Grp[1]

        # eye grp connect
        self.eyeOffsetBind01 = self.eyeGrpBind(crv=crvNewName, bindZroGrp=self.jointBind01Grp[0],
                                               number='01', side=side, eyeJnt=eyeJnt)

        self.eyeOffsetBind03 = self.eyeGrpBind(crv=crvNewName, bindZroGrp=self.jointBind03Grp[0],
                                               number='03', side=side, eyeJnt=eyeJnt)

        self.eyeOffsetBind05 = self.eyeGrpBind(crv=crvNewName, bindZroGrp=self.jointBind05Grp[0],
                                               number='05', side=side, eyeJnt=eyeJnt)

        if self.pos > 0:
            mc.setAttr(self.jointBind01Grp[0] + '.rotateY', directionLid01 * -1)
            mc.setAttr(self.jointBind02Grp[0] + '.rotateY', directionLid02 * -1)
            mc.setAttr(self.jointBind03Grp[0] + '.rotateY', directionLid03)
            mc.setAttr(self.jointBind05Grp[0] + '.rotateY', directionLid05)
            mc.setAttr(self.jointBind04Grp[0] + '.rotateY', directionLid04)

        else:
            mc.setAttr(self.jointBind01Grp[0] + '.rotateY', directionLid01)
            mc.setAttr(self.jointBind02Grp[0] + '.rotateY', directionLid02)
            mc.setAttr(self.jointBind03Grp[0] + '.rotateY', directionLid03 * -1)
            mc.setAttr(self.jointBind05Grp[0] + '.rotateY', directionLid05 * -1)
            mc.setAttr(self.jointBind04Grp[0] + '.rotateY', directionLid04 * -1)

        # rebuild the curve
        mc.rebuildCurve(deformCrv, ch=0, rpo=1, rt=0, end=1, kr=0, kcp=0,
                        kep=1, kt=0, s=8, d=3, tol=0.01)

        # skinning the joint to the bind curve
        skinCls = mc.skinCluster([jnt05, jnt04, jnt01, jnt02, jnt03], deformCrv,
                                 n='%s%s%s%s'% (au.prefix_name(crvNewName), 'Wire', side, 'SkinCluster'), tsb=True, bm=0, sm=0, nw=1, mi=3)

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

        mc.skinPercent(skinCls[0], skinPercent0, tv=[(jnt01, 1.0)])
        mc.skinPercent(skinCls[0], skinPercent1, tv=[(jnt01, 0.9), (jnt02, 0.1)])
        mc.skinPercent(skinCls[0], skinPercent2, tv=[(jnt01, 0.7), (jnt02, 0.3)])
        mc.skinPercent(skinCls[0], skinPercent3, tv=[(jnt02, 0.5), (jnt01, 0.25), (jnt03, 0.25)])
        mc.skinPercent(skinCls[0], skinPercent4, tv=[(jnt02, 0.3), (jnt03, 0.7)])
        mc.skinPercent(skinCls[0], skinPercent5, tv=[(jnt03, 1.0)])
        mc.skinPercent(skinCls[0], skinPercent6, tv=[(jnt04, 0.3), (jnt03, 0.7)])
        mc.skinPercent(skinCls[0], skinPercent7, tv=[(jnt04, 0.5), (jnt05, 0.25), (jnt03, 0.25)])
        mc.skinPercent(skinCls[0], skinPercent8, tv=[(jnt05, 0.7), (jnt04, 0.3)])
        mc.skinPercent(skinCls[0], skinPercent9, tv=[(jnt05, 0.9), (jnt04, 0.1)])
        mc.skinPercent(skinCls[0], skinPercent10, tv=[(jnt05, 1.0)])

        # wire the curve
        wireDef = mc.wire(crv, dds=(0, 100 * scale), wire=deformCrv)
        wireDef[0] = mc.rename(wireDef[0], (au.prefix_name(crvNewName) + side + '_wireNode'))
        mc.setAttr(wireDef[0]+'.scale[0]', 0)

        # constraint mid to 02 left and right
        mc.parentConstraint(jnt03, jnt05, self.jointBind04Grp[0], mo=1)
        mc.parentConstraint(jnt03, jnt01, self.jointBind02Grp[0], mo=1)

        self.jnt03 = jnt03
        self.jnt01 = jnt01
        self.jnt02 = jnt02
        self.jnt05 = jnt05
        self.jnt04 = jnt04

        # create grp curves
        self.curvesGrp = mc.createNode('transform', n=au.prefix_name(crvNewName) + 'Crv' + side + '_grp')
        mc.setAttr (self.curvesGrp + '.it', 0, l=1)
        mc.parent(deformCrv, mc.listConnections(wireDef[0] + '.baseWire[0]')[0], self.curvesGrp)
        mc.hide(self.curvesGrp)

        # create grp bind
        self.bindJntGrp = mc.createNode('transform', n=au.prefix_name(crvNewName) + 'JntBind' + side + '_grp')
        mc.parent(self.eyeOffsetBind03[0], self.eyeOffsetBind01[0], self.jointBind02Grp[0],
                  self.eyeOffsetBind05[0], self.jointBind04Grp[0], self.bindJntGrp)
        mc.hide(self.bindJntGrp)

        self.deformCrv = deformCrv

    def eyeGrpBind(self, crv, number, side, bindZroGrp, eyeJnt):
        # bind grp for eye
        eyeZro = mc.group(em=1, n=au.prefix_name(crv) + 'EyeZro' + number + side + '_grp')
        eyeOffset = mc.group(em=1, n=au.prefix_name(crv) + 'EyeOffset' + number + side + '_grp', p=eyeZro)
        mc.delete(mc.parentConstraint(eyeJnt, eyeZro))

        mc.parent(bindZroGrp, eyeOffset)

        return eyeZro, eyeOffset

    def createJointLid(self, crv, worldUpObject, eyeJnt, scale, sideRGT, sideLFT, side, eyeLid=False):
        self.allJointCenter =[]
        self.allJoint = []
        self.parentLocGrpOffset = []
        self.parentLocGrpZro = []
        self.allLocator = []
        self.parentJntGrpZro = []

        crvNewName = self.replacePosLFTRGT(crv=crv, sideRGT=sideRGT, sideLFT=sideLFT)

        self.jointGrp = mc.group(em=1, n=au.prefix_name(crvNewName) + 'Jnt' + side + '_grp')
        mc.hide(self.jointGrp)

        for i, v in enumerate(self.vtxCrv):

            # create joint
            mc.select(cl=1)
            self.joint = mc.joint(n='%s%02d%s%s' % (au.prefix_name(crvNewName), (i + 1), side, '_jnt'), rad=0.1 * scale)
            pos = mc.xform(v, q=1, ws=1, t=1)
            mc.xform(self.joint, ws=1, t=pos)
            self.allJoint.append(self.joint)

            # create locator
            self.locator = mc.spaceLocator(n='%s%02d%s%s' % (au.prefix_name(crvNewName), (i + 1), side, '_loc'))[0]

            mc.xform(self.locator, ws=1, t=pos)

            self.allLocator.append(self.locator)

            if eyeLid:
                mc.select(cl=1)
                self.jointCenter = mc.joint(n='%s%s%02d%s%s' % (au.prefix_name(crvNewName), 'Ctr', (i + 1), side, '_jnt'), rad=0.1 * scale)
                posC = mc.xform(eyeJnt, q=1, ws=1, t=1)
                mc.xform(self.jointCenter, ws=1, t=posC)
                mc.parent(self.joint, self.jointCenter)

                # change direction of joint center
                mc.joint(self.jointCenter, e=1, oj="xyz", secondaryAxisOrient="yup", ch=1, zso=1)
                self.allJointCenter.append(self.jointCenter)

                # aim constraint of joint
                mc.aimConstraint(self.locator, self.jointCenter, mo=1, weight=1, aimVector=(1, 0, 0), upVector=(0, 1, 0),
                                   worldUpType="object", worldUpObject=worldUpObject)

                mc.parent(self.allJointCenter, worldUpObject, self.jointGrp)



            else:
                # joint grp
                parentJntGrp = tf.create_parent_transform(parent_list=[''], object=self.joint,
                                                          match_position=self.joint,
                                                          prefix=au.prefix_name(crvNewName) + str(i + 1).zfill(2),
                                                          suffix='_jnt', side=side)

                self.parentJntGrpZro.append(parentJntGrp[0])

                # locator grp
                parentLocGrp = tf.create_parent_transform(parent_list=['Zro', 'Offset'], object=self.locator,
                                                          match_position=self.locator,
                                                          prefix=au.prefix_name(crvNewName) + str(i + 1).zfill(2),
                                                          suffix='_loc', side=side)
                self.parentLocGrpOffset.append(parentLocGrp[1])
                self.parentLocGrpZro.append(parentLocGrp[0])
                self.allLocator.append(self.locator)

            # connect curve to locator grp
            curveRelatives = mc.listRelatives(crv, s=True)[0]
            u = self.getUParam(pos, curveRelatives)
            pci = mc.createNode("pointOnCurveInfo", n='%s%02d%s%s' % (au.prefix_name(crvNewName), (i + 1), side, '_pci'))
            mc.connectAttr(curveRelatives + '.worldSpace', pci + '.inputCurve')
            mc.setAttr(pci + '.parameter', u)
            mc.connectAttr(pci + '.position', self.locator + '.t')

        # grouping locator
        self.locatorGrp = mc.group(em=1, n=au.prefix_name(crvNewName) + 'Loc' + side + '_grp')
        mc.setAttr (self.locatorGrp + '.it', 0, l=1)
        mc.hide(self.locatorGrp)

        if not eyeLid:
            # grouping joint
            self.jointGrp = mc.group(em=1, n=au.prefix_name(crvNewName) + 'Jnt' + side + '_grp')
            mc.parent(self.parentJntGrpZro, self.jointGrp)
            mc.parent(self.parentLocGrpZro, self.locatorGrp)

        else:
            mc.parent(self.allLocator, self.locatorGrp)

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
