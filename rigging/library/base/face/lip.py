import re
from __builtin__ import reload
from string import digits

import maya.OpenMaya as om
import maya.cmds as mc

from rigging.library.utils import controller as ct
from rigging.library.utils import transform as tf
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
    def __init__(self, crvLip,
                 crvLipRoll,
                 offsetJnt02BindPos,
                 scale,
                 directionLip01Cheek,
                 directionLip02Cheek,
                 sideLFT,
                 sideRGT,
                 mouthJnt,
                 ctrlColor,
                 controllerLowLip,
                 suffixController):

        self.prefixNameCrv = au.prefix_name(crvLip)
        self.vtxCrv = mc.ls('%s.cv[0:*]' % crvLip, fl=True)

        self.createJointLip(crv=crvLip, scale=scale, ctrlColor=ctrlColor,suffixController=suffixController)

        self.createResetMouthPositionGrp(mouthBaseJnt=mouthJnt)


        self.wireBindCurve(crvLip=crvLip, offsetJnt02BindPos=offsetJnt02BindPos, scale=scale,
                           sideLFT=sideLFT, sideRGT=sideRGT, directionLip01=directionLip01Cheek,
                           directionLip02=directionLip02Cheek)

        self.setDriverLocator(sideLFT=sideLFT, sideRGT=sideRGT)

        self.stickyLip(crvLip=crvLip, scale=scale)

        self.rollLocator(crvRoll=crvLipRoll, scale=scale, crv=crvLip)

        self.allControllerLip(scale=scale, controllerLipLow=controllerLowLip, suffixController=suffixController)

        self.controllerLip(scale=scale, sideLFT=sideLFT, sideRGT=sideRGT,
                           controllerLipLow=controllerLowLip, ctrlColor=ctrlColor, suffixController=suffixController)


        # ==============================================================================================================
        #                                             CREATE GRP AND PARENT GRP
        # ==============================================================================================================

        self.ctrlGrp = mc.group(em=1, n=self.prefixNameCrv+'Controller_grp')
        self.stickyGrp = mc.group(em=1, n=self.prefixNameCrv+'Sticky_grp')

        # UTILITIES GRP
        self.utilsGrp = mc.createNode('transform', n=self.prefixNameCrv + 'Utils_grp')
        mc.parent(self.curvesGrp, self.grpDrvLocator, self.locatorGrp, self.bindJntGrp,
                  self.resetAllMouthCtrlGrp, self.utilsGrp)

        # CTRL GRP
        mc.parent(self.mouthCtrlGrp, self.grpDrvCtrl,  self.ctrlGrp)

        mc.parent(self.stickyCrvGrp, self.stickyClsHdlGrp, self.originLocGrp, self.midLocGrp, self.stickyGrp)

    def controllerLip(self, scale, sideLFT, sideRGT, controllerLipLow, ctrlColor, suffixController):

        # CONTROLLER MID
        self.controllerBindMid = ct.Control(match_obj_first_position=self.jntMid, prefix=self.prefixNameCrv + 'Drv',
                                            shape=ct.SQUAREPLUS, groups_ctrl=['Zro', 'Offset'], ctrl_size=scale * 0.1,
                                            ctrl_color=ctrlColor, lock_channels=['v', 's'], suffix=suffixController
                                            )
        # CONTROLLER RGT 01
        self.controllerBind01RGT = ct.Control(match_obj_first_position=self.jnt01RGT, prefix=self.prefixNameCrv + 'Drv01',
                                              shape=ct.SQUAREPLUS, groups_ctrl=['Zro', 'Offset', 'All'], ctrl_size=scale * 0.05,
                                              ctrl_color=ctrlColor, lock_channels=['v', 'r', 's'], side=sideRGT, suffix=suffixController
                                              )

        # CONTROLLER RGT 02
        self.controllerBind02RGT = ct.Control(match_obj_first_position=self.jnt02RGT, prefix=self.prefixNameCrv + 'Drv02',
                                              shape=ct.SQUAREPLUS, groups_ctrl=['Zro', 'Offset'], ctrl_size=scale * 0.07,
                                              ctrl_color=ctrlColor, lock_channels=['v', 's'], side=sideRGT, suffix=suffixController
                                              )
        # CONTROLLER LFT 01
        self.controllerBind01LFT = ct.Control(match_obj_first_position=self.jnt01LFT, prefix=self.prefixNameCrv + 'Drv01',
                                              shape=ct.SQUAREPLUS, groups_ctrl=['Zro', 'Offset', 'All'], ctrl_size=scale * 0.05,
                                              ctrl_color=ctrlColor, lock_channels=['v', 'r', 's'], side=sideLFT, suffix=suffixController
                                              )
        # CONTROLLER LFT 02
        self.controllerBind02LFT = ct.Control(match_obj_first_position=self.jnt02LFT, prefix=self.prefixNameCrv + 'Drv02',
                                              shape=ct.SQUAREPLUS, groups_ctrl=['Zro', 'Offset'], ctrl_size=scale * 0.07,
                                              ctrl_color=ctrlColor, lock_channels=['v', 's'], side=sideLFT, suffix=suffixController
                                              )

        # CREATE GRP CONTROLLER AND PARENT INTO IT
        self.grpDrvCtrl = mc.createNode('transform', n=self.prefixNameCrv + 'Ctrl' + '_grp')
        mc.parent(self.controllerBindMid.parent_control[0], self.controllerBind01RGT.parent_control[0], self.controllerBind02RGT.parent_control[0],
                  self.controllerBind01LFT.parent_control[0], self.controllerBind02LFT.parent_control[0], self.jointGrp, self.grpDrvCtrl)

        # CONNECT GROUP PARENT BIND JOINT 01 AND 02 TO THE CONTROLLER GRP PARENT 01 AND 02
        au.connectAttrTransRot(self.jointBind02GrpRGT[0], self.controllerBind02RGT.parent_control[0])
        au.connectAttrTransRot(self.jointBind02GrpLFT[0], self.controllerBind02LFT.parent_control[0])

        # FLIPPING CONTROLLER
        if controllerLipLow:
            mc.setAttr(self.controllerBind01RGT.parent_control[0] + '.scaleX', -1)
            mc.setAttr(self.controllerBind02RGT.parent_control[0] + '.scaleX', -1)

            mc.setAttr(self.controllerBind01RGT.parent_control[0] + '.scaleY', -1)
            mc.setAttr(self.controllerBind02RGT.parent_control[0] + '.scaleY', -1)

            mc.setAttr(self.controllerBind01LFT.parent_control[0] + '.scaleY', -1)
            mc.setAttr(self.controllerBind02LFT.parent_control[0] + '.scaleY', -1)

            mc.setAttr(self.controllerBindMid.parent_control[0] + '.scaleY', -1)


            # CONNECT TRANSLATE CONTROLLER TO JOINT
            # RIGHT SIDE 02 TRANSLATE AND ROTATE
            tf.bind_translate_reverse(control=self.controllerBind02RGT.control,
                                      input_2X=-1, input_2Y=-1, input_2Z=1,
                                      joint_bind_target=self.jnt02RGT, side_RGT=sideRGT, side_LFT=sideLFT, side='RGT')

            au.connect_attr_rotate(self.controllerBind02RGT.control, self.jnt02RGT)

            # RIGHT SIDE 01 TRANSLATE AND ROTATE
            tf.bind_translate_reverse(control=self.controllerBind01RGT.control,
                                      input_2X=-1, input_2Y=-1, input_2Z=1,
                                      joint_bind_target=self.jnt01RGT, side_RGT=sideRGT, side_LFT=sideLFT, side='RGT')

            au.connect_attr_rotate(self.controllerBind01RGT.control, self.jnt01RGT)

            # LEFT SIDE 02 TRANSLATE AND ROTATE
            tf.bind_translate_reverse(control=self.controllerBind02LFT.control,
                                      input_2X=1, input_2Y=-1, input_2Z=1,
                                      joint_bind_target=self.jnt02LFT, side_RGT=sideRGT, side_LFT=sideLFT, side='LFT')

            au.connect_attr_rotate(self.controllerBind02LFT.control, self.jnt02LFT)

            # LEFT SIDE 01 TRANSLATE AND ROTATE
            tf.bind_translate_reverse(control=self.controllerBind01LFT.control,
                                      input_2X=1, input_2Y=-1, input_2Z=1,
                                      joint_bind_target=self.jnt01LFT, side_RGT=sideRGT, side_LFT=sideLFT, side='LFT')

            au.connect_attr_rotate(self.controllerBind01LFT.control, self.jnt01LFT)

            # MID TRANSLATE AND ROTATE
            tf.bind_translate_reverse(control=self.controllerBindMid.control,
                                      input_2X=1, input_2Y=-1, input_2Z=1,
                                      joint_bind_target=self.jntMid, side_RGT=sideRGT, side_LFT=sideLFT, side='')

            tf.bind_rotate_reverse(control=self.controllerBindMid.control,
                                   input_2X=-1, input_2Y=1, input_2Z=-1,
                                   joint_bind_target=self.jntMid, side_RGT=sideRGT, side_LFT=sideLFT, side='')

        else:
            mc.setAttr(self.controllerBind01RGT.parent_control[0] + '.scaleX', -1)
            mc.setAttr(self.controllerBind02RGT.parent_control[0] + '.scaleX', -1)

            # RIGHT SIDE 02 TRANSLATE AND ROTATE
            tf.bind_translate_reverse(control=self.controllerBind02RGT.control,
                                      input_2X=-1, input_2Y=1, input_2Z=1,
                                      joint_bind_target=self.jnt02RGT, side_RGT=sideRGT, side_LFT=sideLFT, side='RGT')

            mc.connectAttr(self.controllerBind02RGT.control + '.rotate', self.jnt02RGT + '.rotate')

            # RIGHT SIDE 01 TRANSLATE AND ROTATE
            tf.bind_translate_reverse(control=self.controllerBind01RGT.control,
                                      input_2X=-1, input_2Y=1, input_2Z=1,
                                      joint_bind_target=self.jnt01RGT, side_RGT=sideRGT, side_LFT=sideLFT, side='RGT')

            mc.connectAttr(self.controllerBind01RGT.control + '.rotate', self.jnt01RGT + '.rotate')

            # LEFT SIDE 02 TRANSLATE AND ROTATE
            au.connectAttrTransRot(self.controllerBind02LFT.control, self.jnt02LFT)

            # LEFT SIDE 01 TRANSLATE AND ROTATE
            au.connectAttrTransRot(self.controllerBind01LFT.control, self.jnt01LFT)

            # MID TRANSLATE AND ROTATE
            au.connectAttrTransRot(self.controllerBindMid.control, self.jntMid)

        # SCALING THE CTRL
        listSecondGrp = [self.controllerBindMid.parent_control[1], self.controllerBind01RGT.parent_control[1],
                         self.controllerBind02RGT.parent_control[1], self.controllerBind01LFT.parent_control[1],
                         self.controllerBind02LFT.parent_control[1]]
        for i in listSecondGrp:
            au.connect_attr_scale(self.mouthCtrlGrp, i)


    def allControllerLip(self, scale, controllerLipLow, suffixController):

        # controller
        controllerAll= ct.Control(match_obj_first_position=self.jntMid, prefix=self.prefixNameCrv + 'DrvAll',
                                  shape=ct.CIRCLE, groups_ctrl=[''], ctrl_size=scale * 0.15,
                                  ctrl_color='blue', lock_channels=['v', 's'], suffix=suffixController)

        self.controllerAllZroGrp = controllerAll.parent_control[0]
        self.controllerAll = controllerAll.control

        showDtlCtrl = au.add_attribute(objects=[controllerAll.control], long_name=['showDetailCtrl'],
                                       attributeType="long", min=0, max=1, dv=0, keyable=True)

        for i in self.parentJntGrpOffset:
            mc.connectAttr( self.controllerAll+'.%s' % showDtlCtrl, i+'.visibility')


        if controllerLipLow:
            mc.setAttr(self.controllerAllZroGrp+ '.scaleY', -1)

        # PARENT TO RESPECTIVE OBJECT
        mc.parent(self.controllerAllZroGrp, self.mouthOffsetCtrlGrp)

    def rollLocator(self, crvRoll, crv, scale):
        joint = self.allJoint
        lenJnt = len(joint)
        right = joint[0:((lenJnt - 1) / 2)]
        left = joint[((lenJnt + 1) / 2):]
        left = left[::-1]
        mid = joint[(lenJnt - 1)/2]

        div = (1.000 / ((lenJnt / 2.000)-1.000))

        self.mdlLipRoll = mc.createNode('multDoubleLinear', n=self.prefixNameCrv + 'Roll' + '_mdl')
        # REBUILD THE CURVE
        vtxRef = mc.ls('%s.cv[1:]' % crv, fl=True)
        vtxRef = len(vtxRef)

        crvRbld = mc.rebuildCurve(crvRoll, rpo=1, rt=0, end=1, kr=0, kcp=0,
                                  kep=0, kt=0, s=vtxRef, d=1, tol=0.01)
        newName = mc.rename(crvRbld, self.prefixNameCrv + 'Roll_crv')

        vtx = mc.ls('%s.cv[0:*]' % newName, fl=True)
        allLocatorRoll = []
        multDouble=[]
        condition=[]
        for i, v in enumerate(vtx):
            pos = mc.xform(v, q=1, ws=1, t=1)
            # CREATE LOCATOR
            locatorRoll = mc.spaceLocator(n='%s%s%02d%s' % (self.prefixNameCrv, 'Roll', (i + 1), '_loc'))[0]
            # GRPLOCATORROLL =
            locRelatives = mc.listRelatives(locatorRoll, s=True)[0]

            mc.setAttr(locRelatives + '.localScaleX', 0.1 * scale)
            mc.setAttr(locRelatives + '.localScaleY', 0.1 * scale)
            mc.setAttr(locRelatives + '.localScaleZ', 0.1 * scale)

            mc.xform(locatorRoll, ws=1, t=pos)

            # CONNECT MDL NODE ROLL TO OBJECT LOCATOR
            # mc.connectAttr(self.mdlLipRoll + '.output', locatorRoll + '.rotateX')
            allLocatorRoll.append(locatorRoll)

        for n, rgt, in enumerate(right):
            prefixName, numberName = self.reorderNumber(prefix=rgt, sideRGT='', sideLFT='')
            mdl = mc.createNode('multDoubleLinear', n=au.prefix_name(prefixName) + 'MulRoll' + numberName + '_mdl')
            self.cndRGT = mc.createNode('condition', n=au.prefix_name(prefixName) + 'Roll' + numberName + '_cnd')
            mc.setAttr(self.cndRGT+'.operation', 3)
            mc.setAttr(self.cndRGT+'.colorIfTrueR', (div * n))
            mc.setAttr(self.cndRGT+'.colorIfFalseR', 1)

            # mc.setAttr(mdl + '.input2', (div * n))
            mc.connectAttr(self.mdlLipRoll + '.output', mdl + '.input1')
            mc.connectAttr(self.cndRGT + '.outColorR', mdl + '.input2')
            multDouble.append(mdl)
            condition.append(self.cndRGT)

            # mc.connectAttr(mdl + '.output', locatorRoll + '.rotateX')

        for n, lft, in enumerate(left):
            prefixName, numberName = self.reorderNumber(prefix=lft, sideRGT='', sideLFT='')
            mdl = mc.createNode('multDoubleLinear', n=au.prefix_name(prefixName) + 'MulRoll' + numberName + '_mdl')
            self.cndLFT = mc.createNode('condition', n=au.prefix_name(prefixName) + 'Roll' + numberName + '_cnd')
            mc.setAttr(self.cndLFT+'.operation', 3)
            mc.setAttr(self.cndLFT+'.colorIfTrueR', (div * n))
            mc.setAttr(self.cndLFT+'.colorIfFalseR', 1)

            # mc.setAttr(mdl + '.input2', (div * n))
            mc.connectAttr(self.mdlLipRoll + '.output', mdl + '.input1')
            mc.connectAttr(self.cndLFT + '.outColorR', mdl + '.input2')

            multDouble.append(mdl)
            condition.append(self.cndLFT)

        # MID MUL ROLL
        prefixName, numberName = self.reorderNumber(prefix=mid, sideRGT='', sideLFT='')
        middleMdl = mc.createNode('multDoubleLinear', n=au.prefix_name(prefixName) + 'MulRoll' + numberName + '_mdl')
        mc.setAttr(middleMdl + '.input2', 1)
        mc.connectAttr(self.mdlLipRoll + '.output', middleMdl + '.input1')
        multDouble.append(middleMdl)

        for mdl, rollLoc, loc, joint in zip(sorted(multDouble), allLocatorRoll, self.parentLocGrpOffset, self.parentJntGrpOffset):
            mc.parent(rollLoc, loc)
            mc.connectAttr(mdl + '.output', rollLoc + '.rotateX')
            mc.connectAttr(rollLoc + '.rotateX', joint + '.rotateX')

        self.allLocatorRoll = allLocatorRoll
        self.condition=sorted(condition)

        mc.delete(self.allLocator)

    def stickyLip(self, crvLip, scale):
        # DUPLICATE THE CURVES
        self.stickyMidCrv = mc.duplicate(crvLip, n=self.prefixNameCrv + 'StickyMid' + '_crv')[0]
        self.bindStickyMidCrv = mc.duplicate(self.deformCrv, n=self.prefixNameCrv + 'BindStickyMid' + '_crv')[0]
        self.stickyOriginCrv = mc.duplicate(crvLip, n=self.prefixNameCrv + 'StickyOrigin' + '_crv')[0]
        self.stickyMoveCrv = mc.duplicate(crvLip, n=self.prefixNameCrv + 'StickyMove' + '_crv')[0]

        mc.select(cl=1)
        # WIRE DEFORM ON MID CURVES
        stickyMidwireDef = mc.wire(self.stickyMidCrv, dds=(0, 100 * scale), wire=self.bindStickyMidCrv)
        stickyMidwireDef[0] = mc.rename(stickyMidwireDef[0], (self.prefixNameCrv + 'StickyMid' + '_wireNode'))
        mc.setAttr(stickyMidwireDef[0]+'.scale[0]', 0)

        # WIRE BIND CURVES TO ORIGIN CURVE
        stickyOriginWireDef = mc.wire(self.stickyOriginCrv, dds=(0, 100 * scale), wire=self.deformCrv)
        stickyOriginWireDef[0] = mc.rename(stickyOriginWireDef[0], (self.prefixNameCrv + 'StickyOrigin' + '_wireNode'))
        mc.setAttr(stickyOriginWireDef[0]+'.scale[0]', 0)

        # BLENDSHAPE STICKY MOVE TO CRV
        mc.blendShape(self.stickyMoveCrv, crvLip, n=(self.prefixNameCrv + 'StickyMove' + '_bsn'), weight=[(0, 1)])

        # LOCATOR ORIGIN
        originLoc = self.duplicateLocAndAddPciNode(nameLoc='Origin', crv=self.stickyOriginCrv)
        self.originLocGrp = originLoc[1]
        # LOCATOR MID
        midLoc = self.duplicateLocAndAddPciNode(nameLoc='Mid', crv=self.stickyMidCrv)
        self.midLocGrp = midLoc[1]

        # SET CLUSTER FOR STICKY MOVE
        stickyMoveCrvVtx = mc.ls('%s.cv[0:*]' % self.stickyMoveCrv, fl=True)
        self.clsHandle=[]
        for n, i in enumerate(stickyMoveCrvVtx):
            cls = mc.cluster(i, n='%s%s%02d%s' % (self.prefixNameCrv, 'StickyMove', n + 1, '_cls'))
            repName = cls[1].replace('Handle','Hdl')
            self.clsHandle.append(mc.rename(cls[1], repName))

        # CONSTRAINING STICKY
        self.clsConstraint=[]
        for o, l, c in zip(originLoc[0], midLoc[0], self.clsHandle):
            cons = mc.parentConstraint(o,l,c)
            # RENAME CONSTRAINT
            cons = au.constraint_rename(cons)[0]
            self.clsConstraint.append(cons)

        # GROUPING THE CURVES
        self.stickyCrvGrp = mc.createNode('transform', n=self.prefixNameCrv + 'StickyCurves' + '_grp')
        mc.setAttr (self.stickyCrvGrp + '.it', 0, l=1)
        mc.parent(self.stickyMidCrv, self.bindStickyMidCrv, self.stickyOriginCrv, self.stickyMoveCrv,
                  mc.listConnections(stickyMidwireDef[0] + '.baseWire[0]')[0],
                  mc.listConnections(stickyOriginWireDef[0] + '.baseWire[0]')[0], self.stickyCrvGrp)
        mc.hide(self.stickyCrvGrp)

        # GROUPING CLUSTER HANDLE
        self.stickyClsHdlGrp = mc.createNode('transform', n=self.prefixNameCrv + 'StickyClusterHdl' + '_grp')
        mc.parent(self.clsHandle, self.stickyClsHdlGrp)
        mc.hide(self.stickyClsHdlGrp)

    def duplicateLocAndAddPciNode(self, nameLoc, crv):
        # DUPLICATE LOCATOR FOR CURVE
        stickyLoc = mc.duplicate(self.allLocator)
        newStickyLoc = []
        for n, i in enumerate(stickyLoc):
            v= mc.rename(i, '%s%s%s%02d%s' % (self.prefixNameCrv, 'Sticky', nameLoc, n + 1, '_loc'))

            # CREATE POINT ON CURVE NODE
            pos = mc.xform(v, q=1, ws=1, t=1)
            name = v.replace('loc', 'pci')
            # CONNECT CURVE TO LOCATOR GRP
            curveRelatives = mc.listRelatives(crv, s=True)[0]
            u = self.getUParam(pos, curveRelatives)
            pci = mc.createNode("pointOnCurveInfo", n=name)
            mc.connectAttr(curveRelatives + '.worldSpace', pci + '.inputCurve')
            mc.setAttr(pci + '.parameter', u)
            mc.connectAttr(pci + '.position', v + '.t')
            newStickyLoc.append(v)

        # GROUPING THE STICKY LOC
        stickyLocGrp = mc.createNode('transform', n=self.prefixNameCrv + 'Sticky' + nameLoc + 'Loc' + '_grp')
        mc.parent(newStickyLoc, stickyLocGrp)
        mc.hide(stickyLocGrp)

        return newStickyLoc, stickyLocGrp

    def setDriverLocator(self, sideLFT, sideRGT):
        # CREATE LOCATOR
        self.locatorSet01RGT = mc.spaceLocator(n=self.prefixNameCrv + 'Drv01' + sideRGT + '_set')[0]
        self.locatorSet01LFT = mc.spaceLocator(n=self.prefixNameCrv + 'Drv01' + sideLFT + '_set')[0]

        self.locatorSetMid = mc.spaceLocator(n=self.prefixNameCrv + 'Drv01' + '_set')[0]

        # MATCH POSITION
        mc.delete(mc.parentConstraint(self.jnt01RGT, self.locatorSet01RGT))
        mc.delete(mc.parentConstraint(self.jnt01LFT, self.locatorSet01LFT))
        mc.delete(mc.parentConstraint(self.jntMid, self.locatorSetMid))

        # CONNECT MOUTH RESET UTILS GRP TO SET DRIVER LOCATOR
        listSetLocator = [self.locatorSet01RGT, self.locatorSet01LFT, self.locatorSetMid]
        for i in listSetLocator:
            au.connect_attr_scale(self.resetAllMouthCtrlGrp, i)

        # CREATE GRP CONTROLLER AND PARENT INTO IT
        self.grpDrvLocator = mc.createNode('transform', n=self.prefixNameCrv + 'DrvSet' + '_grp')
        mc.parent(self.locatorSet01RGT,  self.locatorSet01LFT, self.locatorSetMid, self.grpDrvLocator)
        mc.hide(self.grpDrvLocator)

    def wireBindCurve(self, crvLip, offsetJnt02BindPos, directionLip01, directionLip02,
                      scale, sideLFT, sideRGT):

        jointPosBind = len(self.allJoint)

        # QUERY POSITION OF BIND JOINT
        joint01RGT =  self.allJoint[(jointPosBind * 0)]

        joint02RGT =  self.allJoint[((jointPosBind / 4) + offsetJnt02BindPos)]

        jointMid =  self.allJoint[int(jointPosBind / 2)]

        # QUERY THE POSITION RIGHT SIDE
        self.xformJnt01RGT = mc.xform(joint01RGT, ws=1, q=1, t=1)
        self.xformJnt02RGT = mc.xform(joint02RGT, ws=1, q=1, t=1)
        self.xformJntMid = mc.xform(jointMid, ws=1, q=1, t=1)

        mc.select(cl=1)
        jnt01RGT   = mc.joint(n=self.prefixNameCrv + '01' + sideRGT + '_bind', p=self.xformJnt01RGT, rad=0.5 * scale)
        jnt02RGT   = mc.duplicate(jnt01RGT, n=self.prefixNameCrv + '02' + sideRGT + '_bind')[0]
        jntMid     = mc.duplicate(jnt01RGT, n=self.prefixNameCrv + '_bind')[0]

        # SET THE POSITION RGT JOINT
        mc.xform(jnt02RGT, ws=1, t=self.xformJnt02RGT)
        mc.xform(jntMid, ws=1, t=self.xformJntMid)

        # MIRROR BIND JOINT 02 AND 01
        jnt01LFT = mc.mirrorJoint(jnt01RGT, mirrorYZ=True, searchReplace=(sideRGT, sideLFT))[0]
        jnt02LFT = mc.mirrorJoint(jnt02RGT, mirrorYZ=True, searchReplace=(sideRGT, sideLFT))[0]

        # QUERY POSITION LFT JOINT
        self.xformJnt02LFT = mc.xform(jnt02LFT, ws=1, q=1, t=1)
        self.xformJnt01LFT = mc.xform(jnt01LFT, ws=1, q=1, t=1)

        # CREATE BIND CURVE
        deformCrv = mc.curve(ep=[(self.xformJnt01RGT), (self.xformJnt02RGT), (self.xformJntMid),
                                (self.xformJnt02LFT), (self.xformJnt01LFT)],
                             degree=1)
        deformCrv = mc.rename(deformCrv, (self.prefixNameCrv + 'Bind' + '_crv'))

        # PARENT THE BIND JOINT
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

        # ROTATION BIND JOINT FOLLOW THE MOUTH SHAPE
        mc.setAttr(self.jointBind01GrpRGT[0] + '.rotateY', directionLip01 * -1)
        mc.setAttr(self.jointBind02GrpRGT[0] + '.rotateY', directionLip02 * -1)
        mc.setAttr(self.jointBind01GrpLFT[0] + '.rotateY', directionLip01)
        mc.setAttr(self.jointBind02GrpLFT[0] + '.rotateY', directionLip02)

        # REBUILD THE CURVE
        mc.rebuildCurve(deformCrv, rpo=1, rt=0, end=1, kr=0, kcp=0,
                        kep=1, kt=0, s=2, d=3, tol=0.01)

        # SKINNING THE JOINT TO THE BIND CURVE
        skinCls = mc.skinCluster([jnt01LFT, jnt02LFT, jnt01RGT, jnt02RGT, jntMid], deformCrv,
                                 n='%s%s%s'% ('wire', self.prefixNameCrv.capitalize(), 'SkinCluster'), tsb=True, bm=0, sm=0, nw=1, mi=3)

        # Distribute the skin
        skinPercent0 = '%s.cv[0]' % deformCrv
        skinPercent1 = '%s.cv[1]' % deformCrv
        skinPercent2 = '%s.cv[2]' % deformCrv
        skinPercent3 = '%s.cv[3]' % deformCrv
        skinPercent4 = '%s.cv[4]' % deformCrv

        mc.skinPercent(skinCls[0], skinPercent0, tv=[(jnt01RGT, 1.0)])
        mc.skinPercent(skinCls[0], skinPercent1, tv=[(jnt02RGT, 1.0)])
        mc.skinPercent(skinCls[0], skinPercent2, tv=[(jntMid, 1.0)])
        mc.skinPercent(skinCls[0], skinPercent3, tv=[(jnt02LFT, 1.0)])
        mc.skinPercent(skinCls[0], skinPercent4, tv=[(jnt01LFT, 1.0)])

        # WIRE THE CURVE
        wireDef = mc.wire(crvLip, dds=(0, 100 * scale), wire=deformCrv)
        wireDef[0] = mc.rename(wireDef[0], (self.prefixNameCrv + '_wireNode'))
        mc.setAttr(wireDef[0]+'.scale[0]', 0)


        # CONSTRAINT MID TO 02 LEFT AND RIGHT
        jntMidLFTCons = mc.parentConstraint(jntMid, self.jointBind02GrpLFT[0], mo=1)
        jntMidRGTCons = mc.parentConstraint(jntMid, self.jointBind02GrpRGT[0], mo=1)

        # CONSTRAINT RENAME
        au.constraint_rename([jntMidLFTCons[0], jntMidRGTCons[0]])

        self.jntMid = jntMid
        self.jnt01RGT = jnt01RGT
        self.jnt02RGT = jnt02RGT
        self.jnt01LFT = jnt01LFT
        self.jnt02LFT = jnt02LFT

        # CREATE GRP CURVES
        self.curvesGrp = mc.createNode('transform', n=self.prefixNameCrv + 'DrvCrv' + '_grp')
        mc.setAttr (self.curvesGrp + '.it', 0, l=1)
        mc.parent(deformCrv, mc.listConnections(wireDef[0] + '.baseWire[0]')[0], self.curvesGrp)
        mc.hide(self.curvesGrp)

        # CONNECT MOUTH RESET UTILS GRP TO BIND SCALE PARENT GRP
        listGrpParentBindJoint = [self.jointBindGrpMid[0], self.jointBind01GrpRGT[0], self.jointBind02GrpRGT[0],
                                  self.jointBind01GrpLFT[0], self.jointBind02GrpLFT[0]]
        for i in listGrpParentBindJoint:
            au.connect_attr_scale(self.resetAllMouthCtrlGrp, i)

        # CREATE GRP BIND
        self.bindJntGrp = mc.createNode('transform', n=self.prefixNameCrv + 'DrvJntBind' + '_grp')
        mc.parent(self.jointBindGrpMid[0], self.jointBind01GrpRGT[0], self.jointBind02GrpRGT[0],
                  self.jointBind01GrpLFT[0], self.jointBind02GrpLFT[0], self.bindJntGrp)
        mc.hide(self.bindJntGrp)

        self.deformCrv = deformCrv

    def createResetMouthPositionGrp(self, mouthBaseJnt):
        jointPosBind = len(self.allJoint)

        jointMids =  self.allJoint[int(jointPosBind / 2)]
        jointMid =mc.xform(jointMids, ws=1, q=1, t=1)

        # OFFSETTING TO MOUTH
        posMouth = mc.xform(mouthBaseJnt, ws=1, q=1, t=1)
        self.mouthCtrlGrp = mc.createNode('transform', n=self.prefixNameCrv + 'DrvAllCtrlMouth_grp')
        self.mouthOffsetCtrlGrp = mc.group(em=1, n=self.prefixNameCrv + 'DrvAllCtrlMouthOffset_grp', p=self.mouthCtrlGrp)
        mc.xform(self.mouthCtrlGrp, ws=1, t=posMouth)

        # RESETTING TRANSFORM FOR SET
        self.resetAllMouthCtrlGrp = mc.createNode('transform', n=self.prefixNameCrv+'DrvAllResetUtilMouth_grp')
        self.resetAllMouthOffsetCtrlGrp = mc.group(em=1, n=self.prefixNameCrv+'DrvAllResetUtilMouthOffset_grp', p=self.resetAllMouthCtrlGrp)
        mc.xform(self.resetAllMouthCtrlGrp, ws=1, t=posMouth)

        resetMouthCtrlGrp = mc.createNode('transform', n=self.prefixNameCrv+'DrvAllResetUtilOffset_grp')
        self.resetMouthOffsetCtrlGrp = mc.spaceLocator(n=self.prefixNameCrv+'DrvAllResetUtil_loc')[0]
        mc.parent(self.resetMouthOffsetCtrlGrp, resetMouthCtrlGrp)
        mc.hide(self.resetMouthOffsetCtrlGrp)

        mc.xform(resetMouthCtrlGrp, ws=1, t=jointMid)

        mc.parent(resetMouthCtrlGrp, self.resetAllMouthOffsetCtrlGrp)

        # CONNECT ATRIBUTE FROM MOUTH TO RESET MOUTH OFFSET AND RESET CONTROLLER MOUTH
        au.connect_attr_rotate(mouthBaseJnt, self.resetAllMouthOffsetCtrlGrp)
        au.connect_attr_rotate(mouthBaseJnt, self.mouthOffsetCtrlGrp)

        # CONNECT DRIVE ALL RESET MOUTH TO  THE GRP PARENT JNT GRP LIP
        for jntGrp, locOff in zip (self.parentJntGrpZro, self.parentLocGrpOffset):
            au.connect_attr_scale(self.resetAllMouthCtrlGrp, jntGrp)
            au.connect_attr_scale(self.resetAllMouthCtrlGrp, locOff)

    def createJointLip(self, crv, scale, ctrlColor, suffixController):
        self.allJoint =[]
        self.parentLocGrpOffset=[]
        self.parentLocGrpZro = []
        self.allLocator=[]
        self.parentJntGrpZro=[]
        self.parentJntGrpOffset=[]

        for i, v in enumerate(self.vtxCrv):
            # create joint
            mc.select(cl=1)
            self.joint = mc.joint(n='%s%02d%s' % (self.prefixNameCrv, (i + 1), '_jnt'), rad=0.1 * scale)
            mc.setAttr(self.joint+'.visibility', 0)
            pos = mc.xform(v, q=1, ws=1, t=1)
            mc.xform(self.joint, ws=1, t=pos)
            self.allJoint.append(self.joint)

            # parentJntGrp = tf.createParentTransform(listparent=[''], object=self.joint,
            #                                         matchPos=self.joint,
            #                                         prefix=self.prefixNameCrv + str(i + 1).zfill(2),
            #                                         suffix='_jnt')

            parentJntGrp = ct.Control(match_obj_first_position=self.joint, prefix=self.prefixNameCrv + str(i + 1).zfill(2),
                                      shape=ct.JOINT, groups_ctrl=['', 'Offset'], ctrl_size=scale * 0.1,
                                      ctrl_color=ctrlColor, lock_channels=['v'], connection=['parent'], suffix=suffixController
                                      )
            self.parentJntGrpZro.append(parentJntGrp.parent_control[0])
            self.parentJntGrpOffset.append(parentJntGrp.parent_control[1])

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

            mc.connectAttr(dMtx + '.outputTranslate', parentJntGrp.parent_control[0] + '.translate')
            mc.connectAttr(dMtx + '.outputRotate', parentJntGrp.parent_control[0] + '.rotate')
            # mc.connectAttr(dMtx + '.outputScale', parentJntGrp[0] + '.scale')
            mc.setAttr(self.joint+'.visibility', 0)

        # grouping joint
        self.jointGrp = mc.group(em=1, n=self.prefixNameCrv + 'JntCtr' + '_grp')
        mc.parent(self.parentJntGrpZro, self.jointGrp)

        # grouping locator
        self.locatorGrp = mc.group(em=1, n=self.prefixNameCrv+'Loc'+'_grp')
        mc.setAttr (self.locatorGrp + '.it', 0, l=1)
        mc.parent(self.parentLocGrpZro, self.locatorGrp)

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

    def replacePosLFTRGT(self, crv, sideRGT, sideLFT):
        if sideRGT in crv:
            crvNewName = crv.replace(sideRGT, '')
        elif sideLFT in crv:
            crvNewName = crv.replace(sideLFT, '')
        else:
            crvNewName = crv

        return crvNewName

    def reorderNumber(self, prefix, sideRGT, sideLFT):
        # get the number
        newPrefix = self.replacePosLFTRGT(crv=prefix, sideRGT=sideRGT, sideLFT=sideLFT)
        try:
            patterns = [r'\d+']
            prefixNumber = au.prefix_name(newPrefix)
            for p in patterns:
                prefixNumber = re.findall(p, prefixNumber)[0]
        except:
            prefixNumber=''

        # get the prefix without number
        prefixNoNumber = str(newPrefix).translate(None, digits)

        return prefixNoNumber, prefixNumber