import maya.OpenMaya as om
import maya.cmds as mc
from rigLib.utils import controller as ct, transform as tf

from rigging.tools import AD_utils as au

reload (ct)
reload (tf)
reload (au)

# load Plug-ins
matrixNode = mc.pluginInfo('matrixNodes.mll', query=True, loaded=True)
quatNode = mc.pluginInfo('quatNodes.mll', query=True, loaded=True)

if not matrixNode:
    mc.loadPlugin( 'matrixNodes.mll' )

if not quatNode:
    mc.loadPlugin( 'quatNodes.mll' )

class Build:
    def __init__(self, crv,
                 crvRoll,
                 offsetJnt02BindPos,
                 scale,
                 directionLip01,
                 directionLip02,
                 sideLFT,
                 sideRGT,
                 mouthJnt,
                 ctrlColor,
                 headLowCtrl,
                 controllerLipDown):

        self.prefixNameCrv = au.prefix_name(crv)
        self.vtxCrv = mc.ls('%s.cv[0:*]' % crv, fl=True)

        self.createJointLip(crv=crv, scale=scale)

        self.wireBindCurve(crv=crv, offsetJnt02BindPos=offsetJnt02BindPos, scale=scale,
                           sideLFT=sideLFT, sideRGT=sideRGT, directionLip01=directionLip01,
                           directionLip02=directionLip02 )

        self.setDriverLocator(sideLFT=sideLFT, sideRGT=sideRGT)

        self.stickyLip(crv=crv, scale=scale)

        self.rollLocator(crvRoll=crvRoll, scale=scale, crv=crv)

        self.controllerLip(scale=scale, sideLFT=sideLFT, sideRGT=sideRGT,
                           controllerLipDown=controllerLipDown, ctrlColor=ctrlColor, headLowCtrl=headLowCtrl)

        self.allControllerLip(scale=scale, controllerLipDown=controllerLipDown, mouthBaseJnt=mouthJnt)

        self.ctrlGrp = mc.group(em=1, n=self.prefixNameCrv+'Controller_grp')
        self.stickyGrp = mc.group(em=1, n=self.prefixNameCrv+'Sticky_grp')

        # utilities grp
        self.utilsGrp = mc.createNode('transform', n=self.prefixNameCrv + 'Utils_grp')
        mc.parent(self.curvesGrp, self.jointGrp, self.grpDrvLocator, self.locatorGrp, self.bindJntGrp,
                  self.resetAllMouthCtrlGrp, self.utilsGrp)

        # ctrl grp
        mc.parent(self.mouthCtrlGrp, self.grpDrvCtrl, self.ctrlGrp)

        mc.parent(self.stickyCrvGrp, self.stickyClsHdlGrp, self.originLocGrp, self.midLocGrp, self.stickyGrp)

    def allControllerLip(self, scale, controllerLipDown, mouthBaseJnt):
        # offsetting to mouth
        posMouth = mc.xform(mouthBaseJnt, ws=1, q=1, t=1)

        self.mouthCtrlGrp = mc.createNode('transform', n=self.prefixNameCrv+'DrvAllCtrlMouth_grp')
        mouthOffsetCtrlGrp = mc.group(em=1, n=self.prefixNameCrv+'DrvAllCtrlMouthOffset_grp', p=self.mouthCtrlGrp)
        mc.xform(self.mouthCtrlGrp, ws=1, t=posMouth)

        # controller
        controllerAll= ct.Control(match_obj_first_position=self.jntMid, prefix=self.prefixNameCrv + 'DrvAll',
                                  shape=ct.CIRCLE, groups_ctrl=[''], ctrl_size=scale * 0.4,
                                  ctrl_color='blue', lock_channels=['v', 's'])

        self.controllerAllZroGrp = controllerAll.parent_control[0]
        self.controllerAll = controllerAll.control

        posCtrl = mc.xform(self.controllerAll, ws=1, q=1, t=1)

        # resetting transform for set
        self.resetAllMouthCtrlGrp = mc.createNode('transform', n=self.prefixNameCrv+'DrvAllResetMouth_grp')
        self.resetAllMouthOffsetCtrlGrp = mc.group(em=1, n=self.prefixNameCrv+'DrvAllResetMouthOffset_grp', p=self.resetAllMouthCtrlGrp)
        mc.xform(self.resetAllMouthCtrlGrp, ws=1, t=posMouth)

        resetMouthCtrlGrp = mc.createNode('transform', n=self.prefixNameCrv+'DrvAllResetOffset_grp')
        self.resetMouthOffsetCtrlGrp = mc.group(em=1, n=self.prefixNameCrv+'DrvAllReset_grp', p=resetMouthCtrlGrp)
        mc.xform(resetMouthCtrlGrp, ws=1, t=posCtrl)

        if controllerLipDown:
            mc.setAttr(self.controllerAllZroGrp+ '.scaleY', -1)

        # parent to respective object
        mc.parent(self.controllerAllZroGrp, mouthOffsetCtrlGrp)
        mc.parent(resetMouthCtrlGrp, self.resetAllMouthOffsetCtrlGrp)

        # connect atribute from mouth to reset mouth offset and reset controller mouth
        au.connect_attr_rotate(mouthBaseJnt, self.resetAllMouthOffsetCtrlGrp)
        au.connect_attr_rotate(mouthBaseJnt, mouthOffsetCtrlGrp)

    def stickyLip(self, crv, scale):
        # duplicate the curves
        self.stickyMidCrv = mc.duplicate(crv, n=self.prefixNameCrv + 'StickyMid' + '_crv')[0]
        self.bindStickyMidCrv = mc.duplicate(self.deformCrv, n=self.prefixNameCrv + 'BindStickyMid' + '_crv')[0]
        self.stickyOriginCrv = mc.duplicate(crv, n=self.prefixNameCrv + 'StickyOrigin' + '_crv')[0]
        self.stickyMoveCrv = mc.duplicate(crv, n=self.prefixNameCrv + 'StickyMove' + '_crv')[0]

        mc.select(cl=1)
        # wire deform on mid curves
        stickyMidwireDef = mc.wire(self.stickyMidCrv, dds=(0, 100 * scale), wire=self.bindStickyMidCrv)
        stickyMidwireDef[0] = mc.rename(stickyMidwireDef[0], (self.prefixNameCrv + 'StickyMid' + '_wireNode'))

        # wire bind curves to origin curve
        stickyOriginWireDef = mc.wire(self.stickyOriginCrv, dds=(0, 100 * scale), wire=self.deformCrv)
        stickyOriginWireDef[0] = mc.rename(stickyOriginWireDef[0], (self.prefixNameCrv + 'StickyOrigin' + '_wireNode'))

        # blendshape sticky move to crv
        mc.blendShape(self.stickyMoveCrv, crv, n=(self.prefixNameCrv + 'StickyMove' + '_bsn'), weight=[(0, 1)])

        # locator origin
        originLoc = self.duplicateLocAndAddPciNode(nameLoc='Origin', crv=self.stickyOriginCrv)
        self.originLocGrp = originLoc[1]
        # locator mid
        midLoc = self.duplicateLocAndAddPciNode(nameLoc='Mid', crv=self.stickyMidCrv)
        self.midLocGrp = midLoc[1]

        # set cluster for sticky move
        stickyMoveCrvVtx = mc.ls('%s.cv[0:*]' % self.stickyMoveCrv, fl=True)
        self.clsHandle=[]
        for n, i in enumerate(stickyMoveCrvVtx):
            cls = mc.cluster(i, n='%s%s%02d%s' % (self.prefixNameCrv, 'StickyMove', n + 1, '_cls'))
            repName = cls[1].replace('Handle','Hdl')
            self.clsHandle.append(mc.rename(cls[1], repName))

        # constraining sticky
        self.clsConstraint=[]
        for o, l, c in zip(originLoc[0], midLoc[0], self.clsHandle):
            cons = mc.parentConstraint(o,l,c)[0]
            self.clsConstraint.append(cons)

        # grouping the curves
        self.stickyCrvGrp = mc.createNode('transform', n=self.prefixNameCrv + 'StickyCurves' + '_grp')
        mc.setAttr (self.stickyCrvGrp + '.it', 0, l=1)
        mc.parent(self.stickyMidCrv, self.bindStickyMidCrv, self.stickyOriginCrv, self.stickyMoveCrv,
                  mc.listConnections(stickyMidwireDef[0] + '.baseWire[0]')[0],
                  mc.listConnections(stickyOriginWireDef[0] + '.baseWire[0]')[0], self.stickyCrvGrp)
        mc.hide(self.stickyCrvGrp)

        # grouping cluster handle
        self.stickyClsHdlGrp = mc.createNode('transform', n=self.prefixNameCrv + 'StickyClusterHdl' + '_grp')
        mc.parent(self.clsHandle, self.stickyClsHdlGrp)
        mc.hide(self.stickyClsHdlGrp)

    def duplicateLocAndAddPciNode(self, nameLoc, crv):
        # duplicate locator for curve
        stickyLoc = mc.duplicate(self.allLocator)
        newStickyLoc = []
        for n, i in enumerate(stickyLoc):
            v= mc.rename(i, '%s%s%s%02d%s' % (self.prefixNameCrv, 'Sticky', nameLoc, n + 1, '_loc'))

            # create point on curve node
            pos = mc.xform(v, q=1, ws=1, t=1)
            name = v.replace('loc', 'pci')
            # connect curve to locator grp
            curveRelatives = mc.listRelatives(crv, s=True)[0]
            u = self.getUParam(pos, curveRelatives)
            pci = mc.createNode("pointOnCurveInfo", n=name)
            mc.connectAttr(curveRelatives + '.worldSpace', pci + '.inputCurve')
            mc.setAttr(pci + '.parameter', u)
            mc.connectAttr(pci + '.position', v + '.t')
            newStickyLoc.append(v)

        # grouping the sticky loc
        stickyLocGrp = mc.createNode('transform', n=self.prefixNameCrv + 'Sticky' + nameLoc + 'Loc' + '_grp')
        mc.parent(newStickyLoc, stickyLocGrp)
        mc.hide(stickyLocGrp)

        return newStickyLoc, stickyLocGrp

    def setDriverLocator(self, sideLFT, sideRGT):
        # create locator
        self.locatorSet01RGT = mc.spaceLocator(n=self.prefixNameCrv + 'Drv01' + sideRGT + '_set')[0]
        self.locatorSet01LFT = mc.spaceLocator(n=self.prefixNameCrv + 'Drv01' + sideLFT + '_set')[0]

        self.locatorSetMid = mc.spaceLocator(n=self.prefixNameCrv + 'Drv01' + '_set')[0]

        # match position
        mc.delete(mc.parentConstraint(self.jnt01RGT, self.locatorSet01RGT))
        mc.delete(mc.parentConstraint(self.jnt01LFT, self.locatorSet01LFT))
        mc.delete(mc.parentConstraint(self.jntMid, self.locatorSetMid))


        # create grp controller and parent into it
        self.grpDrvLocator = mc.createNode('transform', n=self.prefixNameCrv + 'DrvSet' + '_grp')
        mc.parent(self.locatorSet01RGT,  self.locatorSet01LFT, self.locatorSetMid, self.grpDrvLocator)
        mc.hide(self.grpDrvLocator)


    def controllerLip(self, scale, sideLFT, sideRGT, controllerLipDown, ctrlColor, headLowCtrl):
        # controller mid
        self.controllerBindMid = ct.Control(match_obj_first_position=self.jntMid, prefix=self.prefixNameCrv + 'Drv',
                                            shape=ct.SQUAREPLUS, groups_ctrl=['Zro', 'Offset'], ctrl_size=scale * 0.4,
                                            ctrl_color=ctrlColor, lock_channels=['v', 's'],
                                            )

        # controller rgt 01
        self.controllerBind01RGT = ct.Control(match_obj_first_position=self.jnt01RGT, prefix=self.prefixNameCrv + 'Drv01',
                                              shape=ct.SQUAREPLUS, groups_ctrl=['Zro', 'Offset', 'All'], ctrl_size=scale * 0.15,
                                              ctrl_color=ctrlColor, lock_channels=['v', 's'], side=sideRGT
                                              )

        # controller rgt 02
        self.controllerBind02RGT = ct.Control(match_obj_first_position=self.jnt02RGT, prefix=self.prefixNameCrv + 'Drv02',
                                              shape=ct.SQUAREPLUS, groups_ctrl=['Zro', 'Offset'], ctrl_size=scale * 0.2,
                                              ctrl_color=ctrlColor, lock_channels=['v', 's'], side=sideRGT
                                              )
        # controller lft 01
        self.controllerBind01LFT = ct.Control(match_obj_first_position=self.jnt01LFT, prefix=self.prefixNameCrv + 'Drv01',
                                              shape=ct.SQUAREPLUS, groups_ctrl=['Zro', 'Offset', 'All'], ctrl_size=scale * 0.15,
                                              ctrl_color=ctrlColor, lock_channels=['v', 's'], side=sideLFT
                                              )
        # controller lft 02
        self.controllerBind02LFT = ct.Control(match_obj_first_position=self.jnt02LFT, prefix=self.prefixNameCrv + 'Drv02',
                                              shape=ct.SQUAREPLUS, groups_ctrl=['Zro', 'Offset'], ctrl_size=scale * 0.2,
                                              ctrl_color=ctrlColor, lock_channels=['v', 's'], side=sideLFT
                                              )

        # create grp controller and parent into it
        self.grpDrvCtrl = mc.createNode('transform', n=self.prefixNameCrv + 'Ctrl' + '_grp')
        mc.parent(self.controllerBindMid.parent_control[0], self.controllerBind01RGT.parent_control[0], self.controllerBind02RGT.parent_control[0],
                  self.controllerBind01LFT.parent_control[0], self.controllerBind02LFT.parent_control[0], self.grpDrvCtrl)

        # connect group parent bind joint 01 and 02 to the controller grp parent 01 and 02
        au.connectAttrTransRot(self.jointBind02GrpRGT[0], self.controllerBind02RGT.parent_control[0])
        au.connectAttrTransRot(self.jointBind02GrpLFT[0], self.controllerBind02LFT.parent_control[0])

        # flipping controller
        if controllerLipDown:
            mc.setAttr(self.controllerBind01RGT.parent_control[0] + '.scaleX', -1)
            mc.setAttr(self.controllerBind02RGT.parent_control[0] + '.scaleX', -1)

            mc.setAttr(self.controllerBind01RGT.parent_control[0] + '.scaleY', -1)
            mc.setAttr(self.controllerBind02RGT.parent_control[0] + '.scaleY', -1)

            mc.setAttr(self.controllerBind01LFT.parent_control[0] + '.scaleY', -1)
            mc.setAttr(self.controllerBind02LFT.parent_control[0] + '.scaleY', -1)

            mc.setAttr(self.controllerBindMid.parent_control[0] + '.scaleY', -1)


            # connect translate controller to joint
            # right side 02 translate and rotate
            self.bindTranslateReverse(control=self.controllerBind02RGT.control,
                                      input2X=-1, input2Y=-1, input2Z=1,
                                      jointBindTarget=self.jnt02RGT)

            au.connect_attr_rotate(self.controllerBind02RGT.control, self.jnt02RGT)

            # right side 01 translate and rotate
            self.bindTranslateReverse(control=self.controllerBind01RGT.control,
                                      input2X=-1, input2Y=-1, input2Z=1,
                                      jointBindTarget=self.jnt01RGT)

            au.connect_attr_rotate(self.controllerBind01RGT.control, self.jnt01RGT)

            # left side 02 translate and rotate
            self.bindTranslateReverse(control=self.controllerBind02LFT.control,
                                      input2X=1, input2Y=-1, input2Z=1,
                                      jointBindTarget=self.jnt02LFT)

            au.connect_attr_rotate(self.controllerBind02LFT.control, self.jnt02LFT)

            # left side 01 translate and rotate
            self.bindTranslateReverse(control=self.controllerBind01LFT.control,
                                      input2X=1, input2Y=-1, input2Z=1,
                                      jointBindTarget=self.jnt01LFT)

            au.connect_attr_rotate(self.controllerBind01LFT.control, self.jnt01LFT)

            # mid translate and rotate
            self.bindTranslateReverse(control=self.controllerBindMid.control,
                                      input2X=1, input2Y=-1, input2Z=1,
                                      jointBindTarget=self.jntMid)

            au.connect_attr_rotate(self.controllerBindMid.control, self.jntMid)

        else:
            mc.setAttr(self.controllerBind01RGT.parent_control[0] + '.scaleX', -1)
            mc.setAttr(self.controllerBind02RGT.parent_control[0] + '.scaleX', -1)

            # right side 02 translate and rotate
            self.bindTranslateReverse(control=self.controllerBind02RGT.control,
                                      input2X=-1, input2Y=1, input2Z=1,
                                      jointBindTarget=self.jnt02RGT)

            mc.connectAttr(self.controllerBind02RGT.control + '.rotate', self.jnt02RGT + '.rotate')

            # right side 01 translate and rotate
            self.bindTranslateReverse(control=self.controllerBind01RGT.control,
                                      input2X=-1, input2Y=1, input2Z=1,
                                      jointBindTarget=self.jnt01RGT)

            mc.connectAttr(self.controllerBind01RGT.control + '.rotate', self.jnt01RGT + '.rotate')

            # left side 02 translate and rotate
            au.connectAttrTransRot(self.controllerBind02LFT.control, self.jnt02LFT)

            # left side 01 translate and rotate
            au.connectAttrTransRot(self.controllerBind01LFT.control, self.jnt01LFT)

            # mid translate and rotate
            au.connectAttrTransRot(self.controllerBindMid.control, self.jntMid)


        # SCALING THE CTRL
        decomposeScl = mc.createNode('decomposeMatrix', n=self.prefixNameCrv+'_dmtx')
        mc.connectAttr(headLowCtrl+'.worldMatrix[0]', decomposeScl+'.inputMatrix')

        mc.connectAttr(decomposeScl +'.outputScale', self.controllerBindMid.parent_control[1] + '.scale')
        mc.connectAttr(decomposeScl +'.outputScale', self.controllerBind01RGT.parent_control[1] + '.scale')
        mc.connectAttr(decomposeScl +'.outputScale', self.controllerBind02RGT.parent_control[1] + '.scale')
        mc.connectAttr(decomposeScl +'.outputScale', self.controllerBind01LFT.parent_control[1] + '.scale')
        mc.connectAttr(decomposeScl +'.outputScale', self.controllerBind02LFT.parent_control[1] + '.scale')

        # CONNECT TO BIND JOINT
        au.connect_attr_scale(self.controllerBindMid.parent_control[1], self.jntMid)
        au.connect_attr_scale(self.controllerBind01RGT.parent_control[1], self.jnt01RGT)
        au.connect_attr_scale(self.controllerBind01LFT.parent_control[1], self.jnt01LFT)

        # CONNECT TO OFFSET LOCATOR GRP
        for i in self.parentLocGrpOffset:
            mc.connectAttr(decomposeScl + '.outputScale', i + '.scale')

    def bindTranslateReverse(self, control, input2X, input2Y, input2Z, jointBindTarget):
        mdnReverse = mc.createNode('multiplyDivide', n=au.prefix_name(control) + '_mdn')
        mc.connectAttr(control + '.translate', mdnReverse + '.input1')

        mc.setAttr(mdnReverse + '.input2X', input2X)
        mc.setAttr(mdnReverse + '.input2Y', input2Y)
        mc.setAttr(mdnReverse + '.input2Z', input2Z)

        # connect to object
        mc.connectAttr(mdnReverse+'.output', jointBindTarget+'.translate')

    def wireBindCurve(self, crv, offsetJnt02BindPos, directionLip01, directionLip02,
                      scale, sideLFT, sideRGT):

        jointPosBind = len(self.allJoint)

        # query position of bind joint
        joint01RGT =  self.allJoint[(jointPosBind * 0)]

        joint02RGT =  self.allJoint[((jointPosBind / 4) + offsetJnt02BindPos)]

        jointMid =  self.allJoint[int(jointPosBind / 2)]

        # query the position right side
        self.xformJnt01RGT = mc.xform(joint01RGT, ws=1, q=1, t=1)
        self.xformJnt02RGT = mc.xform(joint02RGT, ws=1, q=1, t=1)
        self.xformJntMid = mc.xform(jointMid, ws=1, q=1, t=1)

        mc.select(cl=1)
        jnt01RGT   = mc.joint(n=self.prefixNameCrv + '01' + sideRGT + '_bind', p=self.xformJnt01RGT, rad=0.5 * scale)
        jnt02RGT   = mc.duplicate(jnt01RGT, n=self.prefixNameCrv + '02' + sideRGT + '_bind')[0]
        jntMid     = mc.duplicate(jnt01RGT, n=self.prefixNameCrv + '_bind')[0]

        # set the position RGT joint
        mc.xform(jnt02RGT, ws=1, t=self.xformJnt02RGT)
        mc.xform(jntMid, ws=1, t=self.xformJntMid)

        # mirror bind joint 02 and 01
        jnt01LFT = mc.mirrorJoint(jnt01RGT, mirrorYZ=True, searchReplace=(sideRGT, sideLFT))[0]
        jnt02LFT = mc.mirrorJoint(jnt02RGT, mirrorYZ=True, searchReplace=(sideRGT, sideLFT))[0]

        # query position LFT joint
        self.xformJnt02LFT = mc.xform(jnt02LFT, ws=1, q=1, t=1)
        self.xformJnt01LFT = mc.xform(jnt01LFT, ws=1, q=1, t=1)

        # create bind curve
        deformCrv = mc.curve(ep=[(self.xformJnt01RGT), (self.xformJnt02RGT), (self.xformJntMid),
                                (self.xformJnt02LFT), (self.xformJnt01LFT)],
                             degree=3)
        deformCrv = mc.rename(deformCrv, (self.prefixNameCrv + 'Bind' + '_crv'))

        # parent the bind joint
        self.jointBindGrpMid = tf.create_parent_transform(parent_list=['Zro', 'Offset'], object=jntMid,
                                                          match_position=jntMid, prefix=self.prefixNameCrv + 'Drv',
                                                          suffix='_bind')

        self.jointBind01GrpRGT = tf.create_parent_transform(parent_list=['Zro', 'Offset', 'All'], object=jnt01RGT,
                                                            match_position=jnt01RGT, prefix=self.prefixNameCrv + 'Drv01',
                                                            suffix='_bind', side=sideRGT)

        self.jointBind02GrpRGT = tf.create_parent_transform(parent_list=['Zro', 'Offset'], object=jnt02RGT,
                                                            match_position=jnt02RGT, prefix=self.prefixNameCrv + 'Drv02',
                                                            suffix='_bind', side=sideRGT)

        self.jointBind01GrpLFT = tf.create_parent_transform(parent_list=['Zro', 'Offset', 'All'], object=jnt01LFT,
                                                            match_position=jnt01LFT, prefix=self.prefixNameCrv + 'Drv01',
                                                            suffix='_bind', side=sideLFT)

        self.jointBind02GrpLFT = tf.create_parent_transform(parent_list=['Zro', 'Offset'], object=jnt02LFT,
                                                            match_position=jnt02LFT, prefix=self.prefixNameCrv + 'Drv02',
                                                            suffix='_bind', side=sideLFT)

        # rotation bind joint follow the mouth shape
        mc.setAttr(self.jointBind01GrpRGT[0] + '.rotateY', directionLip01 * -1)
        mc.setAttr(self.jointBind02GrpRGT[0] + '.rotateY', directionLip02 * -1)
        mc.setAttr(self.jointBind01GrpLFT[0] + '.rotateY', directionLip01)
        mc.setAttr(self.jointBind02GrpLFT[0] + '.rotateY', directionLip02)

        # rebuild the curve
        mc.rebuildCurve(deformCrv, ch=0, rpo=1, rt=0, end=1, kr=0, kcp=0,
                        kep=1, kt=0, s=2, d=3, tol=0.01)

        # skinning the joint to the bind curve
        skinCls = mc.skinCluster([jnt01LFT, jnt02LFT, jnt01RGT, jnt02RGT, jntMid], deformCrv,
                                 n='%s%s%s'% ('wire', self.prefixNameCrv.capitalize(), 'SkinCluster'), tsb=True, bm=0, sm=0, nw=1, mi=3)

        # wire the curve
        wireDef = mc.wire(crv, dds=(0, 100 * scale), wire=deformCrv)
        wireDef[0] = mc.rename(wireDef[0], (self.prefixNameCrv + '_wireNode'))

        # constraint mid to 02 left and right
        mc.parentConstraint(jntMid, self.jointBind02GrpLFT[0], mo=1)
        mc.parentConstraint(jntMid, self.jointBind02GrpRGT[0], mo=1)
        mc.scaleConstraint(jntMid, self.jointBind02GrpLFT[0], mo=1)
        mc.scaleConstraint(jntMid, self.jointBind02GrpRGT[0], mo=1)

        self.jntMid = jntMid
        self.jnt01RGT = jnt01RGT
        self.jnt02RGT = jnt02RGT
        self.jnt01LFT = jnt01LFT
        self.jnt02LFT = jnt02LFT

        # create grp curves
        self.curvesGrp = mc.createNode('transform', n=self.prefixNameCrv + 'DrvCrv' + '_grp')
        mc.setAttr (self.curvesGrp + '.it', 0, l=1)
        mc.parent(deformCrv, mc.listConnections(wireDef[0] + '.baseWire[0]')[0], self.curvesGrp)
        mc.hide(self.curvesGrp)

        # create grp bind
        self.bindJntGrp = mc.createNode('transform', n=self.prefixNameCrv + 'DrvJntBind' + '_grp')
        mc.parent(self.jointBindGrpMid[0], self.jointBind01GrpRGT[0], self.jointBind02GrpRGT[0],
                  self.jointBind01GrpLFT[0], self.jointBind02GrpLFT[0], self.bindJntGrp)
        mc.hide(self.bindJntGrp)

        self.deformCrv = deformCrv

    def createJointLip(self, crv, scale):
        self.allJoint =[]
        self.parentLocGrpOffset=[]
        self.parentLocGrpZro = []
        self.allLocator=[]
        self.parentJntGrpZro=[]

        for i, v in enumerate(self.vtxCrv):
            # create joint
            mc.select(cl=1)
            self.joint = mc.joint(n='%s%02d%s' % (self.prefixNameCrv, (i + 1), '_jnt'), rad=0.1 * scale)
            pos = mc.xform(v, q=1, ws=1, t=1)
            mc.xform(self.joint, ws=1, t=pos)
            self.allJoint.append(self.joint)

            parentJntGrp = tf.create_parent_transform(parent_list=[''], object=self.joint,
                                                      match_position=self.joint,
                                                      prefix=self.prefixNameCrv + str(i + 1).zfill(2),
                                                      suffix='_jnt')

            self.parentJntGrpZro.append(parentJntGrp[0])
            # create locator
            self.locator = mc.spaceLocator(n='%s%02d%s' % (self.prefixNameCrv, (i + 1), '_loc'))[0]

            mc.xform(self.locator, ws=1, t=pos)
            parentLocGrp = tf.create_parent_transform(parent_list=['Zro', 'Offset'], object=self.locator,
                                                      match_position=self.locator, prefix=self.prefixNameCrv + str(i + 1).zfill(2),
                                                      suffix='_loc')
            self.parentLocGrpOffset.append(parentLocGrp[1])
            self.parentLocGrpZro.append(parentLocGrp[0])
            self.allLocator.append(self.locator)

            # connect curve to locator grp
            curveRelatives = mc.listRelatives(crv, s=True)[0]
            u = self.getUParam(pos, curveRelatives)
            pci = mc.createNode("pointOnCurveInfo", n='%s%02d%s' % (self.prefixNameCrv, (i + 1), '_pci'))
            mc.connectAttr(curveRelatives + '.worldSpace', pci + '.inputCurve')
            mc.setAttr(pci + '.parameter', u)
            mc.connectAttr(pci + '.position', parentLocGrp[0] + '.t')

            dMtx = mc.createNode('decomposeMatrix', n='%s%02d%s' % (self.prefixNameCrv, (i + 1), '_dmtx'))
            mc.connectAttr(parentLocGrp[1] + '.worldMatrix[0]', dMtx + '.inputMatrix')

            mc.connectAttr(dMtx + '.outputTranslate', parentJntGrp[0] + '.translate')
            mc.connectAttr(dMtx + '.outputRotate', parentJntGrp[0] + '.rotate')
            mc.connectAttr(dMtx + '.outputScale', parentJntGrp[0] + '.scale')

        # grouping joint
        self.jointGrp = mc.group(em=1, n=self.prefixNameCrv + 'Jnt' + '_grp')
        mc.parent(self.parentJntGrpZro, self.jointGrp)

        # grouping locator
        self.locatorGrp = mc.group(em=1, n=self.prefixNameCrv+'Loc'+'_grp')
        mc.setAttr (self.locatorGrp + '.it', 0, l=1)
        mc.parent(self.parentLocGrpZro, self.locatorGrp)

    def rollLocator(self, crvRoll, crv, scale):
        self.mdlLipRoll = mc.createNode('multDoubleLinear', n=self.prefixNameCrv + 'Roll' + '_mdl')
        # rebuild the curve
        vtxRef = mc.ls('%s.cv[1:]' % crv, fl=True)
        vtxRef = len(vtxRef)

        crvRbld = mc.rebuildCurve(crvRoll, ch=1, rpo=1, rt=0, end=1, kr=0, kcp=0,
                        kep=0, kt=0, s=vtxRef, d=1, tol=0.01)
        newName = mc.rename(crvRbld, self.prefixNameCrv + 'Roll_crv')

        vtx = mc.ls('%s.cv[0:*]' % newName, fl=True)
        allLocatorRoll=[]
        for i, v in enumerate(vtx):
            pos = mc.xform(v, q=1, ws=1, t=1)
            # create locator
            locatorRoll = mc.spaceLocator(n='%s%s%02d%s' % (self.prefixNameCrv, 'Roll', (i + 1),'_loc'))[0]
            # grpLocatorRoll =
            locRelatives = mc.listRelatives(locatorRoll, s=True)[0]

            mc.setAttr(locRelatives + '.localScaleX', 0.1 * scale)
            mc.setAttr(locRelatives + '.localScaleY', 0.1 * scale)
            mc.setAttr(locRelatives + '.localScaleZ', 0.1 * scale)

            mc.xform(locatorRoll, ws=1, t=pos)

            # connect mdl node roll to object locator
            mc.connectAttr(self.mdlLipRoll+'.output', locatorRoll+'.rotateX')
            allLocatorRoll.append(locatorRoll)

        for rollLoc, loc, joint in zip(allLocatorRoll, self.parentLocGrpOffset, self.allJoint):
            mc.parent(rollLoc, loc)
            mc.connectAttr(rollLoc + '.rotateX', joint + '.rotateX')

        self.allLocatorRoll = allLocatorRoll
        mc.delete(self.allLocator)

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