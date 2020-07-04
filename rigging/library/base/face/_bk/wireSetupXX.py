from __builtin__ import reload

import maya.OpenMaya as om
import maya.cmds as mc
from rigLib.utils import controller as ct, transform as tf

from rigging.tools import AD_utils as au

reload (ct)
reload (tf)
reload (au)


def controllerWire(crv, scale, sideLFT, sideRGT, offsetJnt02BindPos, directionCtrl01, directionCtrl02,
                   ctrlColor, shape, controllerWireLow):
    prefixNameCrv = au.prefix_name(crv)
    wireCrv = wireBindCurve(crv=crv, offsetJnt02BindPos=offsetJnt02BindPos, directionCtrl01=directionCtrl01,
                            directionWire02=directionCtrl02, scale=scale, sideLFT=sideLFT, sideRGT=sideRGT)
    curvesGrp = wireCrv['curvesGrp']
    bindJntGrp = wireCrv['bindJntGrp']
    jointGrp = wireCrv['jointGrp']
    locatorGrp = wireCrv['locatorGrp']
    allJoint = wireCrv['allJoint']
    jointBind01GrpOffsetRGT =  wireCrv['jointBind01GrpRGT[1]']
    jointBind01GrpOffsetLFT =  wireCrv['jointBind01GrpLFT[1]']
    jointBind01GrpZroRGT =  wireCrv['jointBind01GrpRGT[0]']
    jointBind01GrpZroLFT =  wireCrv['jointBind01GrpLFT[0]']

    # controller mid
    controllerBindMid = ct.Control(match_obj_first_position=wireCrv['jntMid'], prefix=prefixNameCrv + 'Drv',
                                   shape=shape, groups_ctrl=['Zro', 'Offset'], ctrl_size=scale * 1.0,
                                   ctrl_color=ctrlColor, lock_channels=['v', 's'],
                                   )

    # controller rgt 01
    controllerBind01RGT = ct.Control(match_obj_first_position=wireCrv['jnt01RGT'], prefix=prefixNameCrv + 'Drv01',
                                     shape=shape, groups_ctrl=['Zro', 'Offset', 'All'], ctrl_size=scale * 0.5,
                                     ctrl_color=ctrlColor, lock_channels=['v', 's'], side=sideRGT
                                     )

    # controller rgt 02
    controllerBind02RGT = ct.Control(match_obj_first_position=wireCrv['jnt02RGT'], prefix=prefixNameCrv + 'Drv02',
                                     shape=shape, groups_ctrl=['Zro', 'Offset'], ctrl_size=scale * 0.7,
                                     ctrl_color=ctrlColor, lock_channels=['v', 's'], side=sideRGT
                                     )
    # controller lft 01
    controllerBind01LFT = ct.Control(match_obj_first_position=wireCrv['jnt01LFT'], prefix=prefixNameCrv + 'Drv01',
                                     shape=shape, groups_ctrl=['Zro', 'Offset', 'All'], ctrl_size=scale * 0.5,
                                     ctrl_color=ctrlColor, lock_channels=['v', 's'], side=sideLFT
                                     )
    # controller lft 02
    controllerBind02LFT = ct.Control(match_obj_first_position=wireCrv['jnt02LFT'], prefix=prefixNameCrv + 'Drv02',
                                     shape=shape, groups_ctrl=['Zro', 'Offset'], ctrl_size=scale * 0.7,
                                     ctrl_color=ctrlColor, lock_channels=['v', 's'], side=sideLFT
                                     )


    # create grp controller and parent into it
    grpDrvCtrl = mc.createNode('transform', n=prefixNameCrv + 'Ctrl' + '_grp')
    mc.parent(controllerBindMid.parent_control[0], controllerBind01RGT.parent_control[0],
              controllerBind02RGT.parent_control[0],
              controllerBind01LFT.parent_control[0], controllerBind02LFT.parent_control[0], grpDrvCtrl)

    # connect group parent bind joint 01 and 02 to the controller grp parent 01 and 02
    au.connectAttrTransRot(wireCrv['jointBind02GrpRGT[0]'], controllerBind02RGT.parent_control[0])
    au.connectAttrTransRot(wireCrv['jointBind02GrpLFT[0]'], controllerBind02LFT.parent_control[0])

    # connect bind parent zro to ctrl zro parent
    au.connect_attr_translate(wireCrv['jointBind01GrpRGT[0]'], controllerBind01RGT.parent_control[0])
    au.connect_attr_translate(wireCrv['jointBind01GrpLFT[0]'], controllerBind01LFT.parent_control[0])

    # flipping controller
    if controllerWireLow:
        mc.setAttr(controllerBind01RGT.parent_control[0] + '.scaleX', -1)
        mc.setAttr(controllerBind02RGT.parent_control[0] + '.scaleX', -1)

        mc.setAttr(controllerBind01RGT.parent_control[0] + '.scaleY', -1)
        mc.setAttr(controllerBind02RGT.parent_control[0] + '.scaleY', -1)

        mc.setAttr(controllerBind01LFT.parent_control[0] + '.scaleY', -1)
        mc.setAttr(controllerBind02LFT.parent_control[0] + '.scaleY', -1)

        mc.setAttr(controllerBindMid.parent_control[0] + '.scaleY', -1)

        # connect translate controller to joint
        # right side 02 translate and rotate
        bindTranslateReverse(control=controllerBind02RGT.control,
                             input2X=-1, input2Y=-1, input2Z=1,
                             jointBindTarget=wireCrv['jnt02RGT'])

        au.connect_attr_rotate(controllerBind02RGT.control, wireCrv['jnt02RGT'])

        # right side 01 translate and rotate
        bindTranslateReverse(control=controllerBind01RGT.control,
                             input2X=-1, input2Y=-1, input2Z=1,
                             jointBindTarget=wireCrv['jnt01RGT'])

        au.connect_attr_rotate(controllerBind01RGT.control, wireCrv['jnt01RGT'])

        # left side 02 translate and rotate
        bindTranslateReverse(control=controllerBind02LFT.control,
                             input2X=1, input2Y=-1, input2Z=1,
                             jointBindTarget=wireCrv['jnt02LFT'])

        au.connect_attr_rotate(controllerBind02LFT.control, wireCrv['jnt02LFT'])

        # left side 01 translate and rotate
        bindTranslateReverse(control=controllerBind01LFT.control,
                             input2X=1, input2Y=-1, input2Z=1,
                             jointBindTarget=wireCrv['jnt01LFT'])

        au.connect_attr_rotate(controllerBind01LFT.control, wireCrv['jnt01LFT'])

        # mid translate and rotate
        bindTranslateReverse(control=controllerBindMid.control,
                             input2X=1, input2Y=-1, input2Z=1,
                             jointBindTarget=wireCrv['jntMid'])

        au.connect_attr_rotate(controllerBindMid.control, wireCrv['jntMid'])

    else:
        mc.setAttr(controllerBind01RGT.parent_control[0] + '.scaleX', -1)
        mc.setAttr(controllerBind02RGT.parent_control[0] + '.scaleX', -1)

        # right side 02 translate and rotate
        bindTranslateReverse(control=controllerBind02RGT.control,
                             input2X=-1, input2Y=1, input2Z=1,
                             jointBindTarget=wireCrv['jnt02RGT'])

        mc.connectAttr(controllerBind02RGT.control + '.rotate', wireCrv['jnt02RGT'] + '.rotate')

        # right side 01 translate and rotate
        bindTranslateReverse(control=controllerBind01RGT.control,
                             input2X=-1, input2Y=1, input2Z=1,
                             jointBindTarget=wireCrv['jnt01RGT'])

        mc.connectAttr(controllerBind01RGT.control + '.rotate', wireCrv['jnt01RGT'] + '.rotate')

        # left side 02 translate and rotate
        au.connectAttrTransRot(controllerBind02LFT.control, wireCrv['jnt02LFT'])

        # left side 01 translate and rotate
        au.connectAttrTransRot(controllerBind01LFT.control, wireCrv['jnt01LFT'])

        # mid translate and rotate
        au.connectAttrTransRot(controllerBindMid.control, wireCrv['jntMid'])

        return {'grpDrvCtrl':grpDrvCtrl,
                'curvesGrp':curvesGrp,
                'bindJntGrp': bindJntGrp,
                'jointGrp': jointGrp,
                'locatorGrp':locatorGrp,
                'controllerBind01LFT': controllerBind01LFT.control,
                'controllerBind01RGT': controllerBind01RGT.control,
                'controllerBindZroGrp01LFT': controllerBind01LFT.parent_control[0],
                'controllerBindZroGrp01RGT': controllerBind01RGT.parent_control[0],
                'jointBind01GrpOffsetRGT': jointBind01GrpOffsetRGT,
                'jointBind01GrpOffsetLFT': jointBind01GrpOffsetLFT,
                'jointBind01GrpZroRGT': jointBind01GrpZroRGT,
                'jointBind01GrpZroLFT': jointBind01GrpZroLFT,
                'allJoint':allJoint}

def bindTranslateReverse(control, input2X, input2Y, input2Z, jointBindTarget):
    mdnReverse = mc.createNode('multiplyDivide', n=au.prefix_name(control) + '_mdn')
    mc.connectAttr(control + '.translate', mdnReverse + '.input1')

    mc.setAttr(mdnReverse + '.input2X', input2X)
    mc.setAttr(mdnReverse + '.input2Y', input2Y)
    mc.setAttr(mdnReverse + '.input2Z', input2Z)

    # connect to object
    mc.connectAttr(mdnReverse + '.output', jointBindTarget + '.translate')

def wireBindCurve(crv, offsetJnt02BindPos, directionCtrl01, directionWire02,
                  scale, sideLFT, sideRGT):

    prefixNameCrv = au.prefix_name(crv)

    jointWire = createJointWire(crv, scale)
    allJoint = jointWire['allJoint']
    jointGrp = jointWire['jointGrp']
    locatorGrp = jointWire['locatorGrp']

    jointPosBind = len(allJoint)

    # query position of bind joint
    joint01RGT = allJoint[(jointPosBind * 0)]

    joint02RGT = allJoint[((jointPosBind / 4) + offsetJnt02BindPos)]

    jointMid = allJoint[(jointPosBind / 2)]

    # query the position right side
    xformJnt01RGT = mc.xform(joint01RGT, ws=1, q=1, t=1)
    xformJnt02RGT = mc.xform(joint02RGT, ws=1, q=1, t=1)
    xformJntMid = mc.xform(jointMid, ws=1, q=1, t=1)

    mc.select(cl=1)
    jnt01RGT = mc.joint(n=prefixNameCrv + '01' + sideRGT + '_bind', p=xformJnt01RGT, rad=0.5 * scale)
    jnt02RGT = mc.duplicate(jnt01RGT, n=prefixNameCrv + '02' + sideRGT + '_bind')[0]
    jntMid = mc.duplicate(jnt01RGT, n=prefixNameCrv + '_bind')[0]

    # set the position RGT joint
    mc.xform(jnt02RGT, ws=1, t=xformJnt02RGT)
    mc.xform(jntMid, ws=1, t=xformJntMid)

    # mirror bind joint 02 and 01
    jnt01LFT = mc.mirrorJoint(jnt01RGT, mirrorYZ=True, searchReplace=(sideRGT, sideLFT))[0]
    jnt02LFT = mc.mirrorJoint(jnt02RGT, mirrorYZ=True, searchReplace=(sideRGT, sideLFT))[0]

    # query position LFT joint
    xformJnt02LFT = mc.xform(jnt02LFT, ws=1, q=1, t=1)
    xformJnt01LFT = mc.xform(jnt01LFT, ws=1, q=1, t=1)

    # create bind curve
    deformCrv = mc.curve(ep=[(xformJnt01RGT), (xformJnt02RGT), (xformJntMid),
                             (xformJnt02LFT), (xformJnt01LFT)],
                         degree=3)
    deformCrv = mc.rename(deformCrv, (prefixNameCrv + 'Bind' + '_crv'))

    # parent the bind joint
    jointBindGrpMid = tf.create_parent_transform(parent_list=['Zro', 'Offset'], object=jntMid,
                                                 match_position=jntMid, prefix=prefixNameCrv + 'Drv',
                                                 suffix='_bind')

    jointBind01GrpRGT = tf.create_parent_transform(parent_list=['Zro', 'Offset', 'All'], object=jnt01RGT,
                                                   match_position=jnt01RGT, prefix=prefixNameCrv + 'Drv01',
                                                   suffix='_bind', side=sideRGT)

    jointBind02GrpRGT = tf.create_parent_transform(parent_list=['Zro', 'Offset'], object=jnt02RGT,
                                                   match_position=jnt02RGT, prefix=prefixNameCrv + 'Drv02',
                                                   suffix='_bind', side=sideRGT)

    jointBind01GrpLFT = tf.create_parent_transform(parent_list=['Zro', 'Offset', 'All'], object=jnt01LFT,
                                                   match_position=jnt01LFT, prefix=prefixNameCrv + 'Drv01',
                                                   suffix='_bind', side=sideLFT)

    jointBind02GrpLFT = tf.create_parent_transform(parent_list=['Zro', 'Offset'], object=jnt02LFT,
                                                   match_position=jnt02LFT, prefix=prefixNameCrv + 'Drv02',
                                                   suffix='_bind', side=sideLFT)

    # rotation bind joint follow the mouth shape
    mc.setAttr(jointBind01GrpRGT[0] + '.rotateY', directionCtrl01 * -1)
    mc.setAttr(jointBind02GrpRGT[0] + '.rotateY', directionWire02 * -1)
    mc.setAttr(jointBind01GrpLFT[0] + '.rotateY', directionCtrl01)
    mc.setAttr(jointBind02GrpLFT[0] + '.rotateY', directionWire02)

    # rebuild the curve
    mc.rebuildCurve(deformCrv, ch=0, rpo=1, rt=0, end=1, kr=0, kcp=0,
                    kep=1, kt=0, s=8, d=3, tol=0.01)

    # skinning the joint to the bind curve
    skinCls = mc.skinCluster([jnt01LFT, jnt02LFT, jnt01RGT, jnt02RGT, jntMid], deformCrv,
                             n='%s%s%s' % ('wire', prefixNameCrv.capitalize(), 'SkinCluster'), tsb=True, bm=0,
                             sm=0, nw=1, mi=3)

    # wire the curve
    wireDef = mc.wire(crv, dds=(0, 100 * scale), wire=deformCrv)
    wireDef[0] = mc.rename(wireDef[0], (prefixNameCrv + '_wireNode'))

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

    mc.skinPercent(skinCls[0], skinPercent0, tv=[(jnt01RGT, 1.0)])
    mc.skinPercent(skinCls[0], skinPercent1, tv=[(jnt01RGT, 0.9), (jnt02RGT, 0.1)])
    mc.skinPercent(skinCls[0], skinPercent2, tv=[(jnt01RGT, 0.7), (jnt02RGT, 0.3)])
    mc.skinPercent(skinCls[0], skinPercent3, tv=[(jnt02RGT, 0.5), (jnt01RGT, 0.25), (jntMid, 0.25)])
    mc.skinPercent(skinCls[0], skinPercent4, tv=[(jnt02RGT, 0.3), (jntMid, 0.7)])
    mc.skinPercent(skinCls[0], skinPercent5, tv=[(jntMid, 1.0)])
    mc.skinPercent(skinCls[0], skinPercent6, tv=[(jnt02LFT, 0.3), (jntMid, 0.7)])
    mc.skinPercent(skinCls[0], skinPercent7, tv=[(jnt02LFT, 0.5), (jnt01LFT, 0.25), (jntMid, 0.25)])
    mc.skinPercent(skinCls[0], skinPercent8, tv=[(jnt01LFT, 0.7), (jnt02LFT, 0.3)])
    mc.skinPercent(skinCls[0], skinPercent9, tv=[(jnt01LFT, 0.9), (jnt02LFT, 0.1)])
    mc.skinPercent(skinCls[0], skinPercent10, tv=[(jnt01LFT, 1.0)])

    # constraint mid to 02 left and right
    mc.parentConstraint(jntMid, jointBind02GrpLFT[0], mo=1)
    mc.parentConstraint(jntMid, jointBind02GrpRGT[0], mo=1)

    # create grp curves
    curvesGrp = mc.createNode('transform', n=prefixNameCrv + 'DrvCrv' + '_grp')
    mc.setAttr(curvesGrp + '.it', 0, l=1)
    mc.parent(deformCrv, mc.listConnections(wireDef[0] + '.baseWire[0]')[0], curvesGrp)
    mc.hide(curvesGrp)

    # create grp bind
    bindJntGrp = mc.createNode('transform', n=prefixNameCrv + 'DrvJntBind' + '_grp')
    mc.parent(jointBindGrpMid[0], jointBind01GrpRGT[0], jointBind02GrpRGT[0],
              jointBind01GrpLFT[0], jointBind02GrpLFT[0], bindJntGrp)
    mc.hide(bindJntGrp)

    deformCrv = deformCrv

    return{'jntMid':jntMid,
           'jnt01RGT' : jnt01RGT,
            'jnt02RGT' : jnt02RGT,
            'jnt01LFT' : jnt01LFT,
            'jnt02LFT' : jnt02LFT,
           'jointBind02GrpRGT[0]': jointBind02GrpRGT[0],
            'jointBind02GrpLFT[0]': jointBind02GrpLFT[0],
           'jointBind01GrpRGT[1]': jointBind01GrpRGT[1],
           'jointBind01GrpLFT[1]': jointBind01GrpLFT[1],
           'jointBind01GrpRGT[0]': jointBind01GrpRGT[0],
           'jointBind01GrpLFT[0]': jointBind01GrpLFT[0],
           'curvesGrp':curvesGrp,
           'bindJntGrp': bindJntGrp,
            'jointGrp' : jointGrp,
            'locatorGrp' :locatorGrp,
           'allJoint':allJoint,
            }

def createJointWire(crv, scale):
    prefixNameCrv = au.prefix_name(crv)
    vtxCrv = mc.ls('%s.cv[0:*]' % crv, fl=True)

    allJoint = []
    parentLocGrpOffset = []
    parentLocGrpZro = []
    allLocator = []
    parentJntGrpZro = []

    for i, v in enumerate(vtxCrv):
        # create joint
        mc.select(cl=1)
        joint = mc.joint(n='%s%02d%s' % (prefixNameCrv, (i + 1), '_jnt'), rad=0.1 * scale)
        pos = mc.xform(v, q=1, ws=1, t=1)
        mc.xform(joint, ws=1, t=pos)
        allJoint.append(joint)

        parentJntGrp = tf.create_parent_transform(parent_list=[''], object=joint,
                                                  match_position=joint,
                                                  prefix=prefixNameCrv + str(i + 1).zfill(2),
                                                  suffix='_jnt')

        parentJntGrpZro.append(parentJntGrp[0])
        # create locator
        locator = mc.spaceLocator(n='%s%02d%s' % (prefixNameCrv, (i + 1), '_loc'))[0]

        mc.xform(locator, ws=1, t=pos)
        parentLocGrp = tf.create_parent_transform(parent_list=['Zro', 'Offset'], object=locator,
                                                  match_position=locator, prefix=prefixNameCrv + str(i + 1).zfill(2),
                                                  suffix='_loc')
        parentLocGrpOffset.append(parentLocGrp[1])
        parentLocGrpZro.append(parentLocGrp[0])
        allLocator.append(locator)

        # connect curve to locator grp
        curveRelatives = mc.listRelatives(crv, s=True)[0]
        u = getUParam(pos, curveRelatives)
        pci = mc.createNode("pointOnCurveInfo", n='%s%02d%s' % (prefixNameCrv, (i + 1), '_pci'))
        mc.connectAttr(curveRelatives + '.worldSpace', pci + '.inputCurve')
        mc.setAttr(pci + '.parameter', u)
        mc.connectAttr(pci + '.position', parentLocGrp[0] + '.t')

        dMtx = mc.createNode('decomposeMatrix', n='%s%02d%s' % (prefixNameCrv, (i + 1), '_dmtx'))
        mc.connectAttr(parentLocGrp[1] + '.worldMatrix[0]', dMtx + '.inputMatrix')

        mc.connectAttr(dMtx + '.outputTranslate', parentJntGrp[0] + '.translate')
        mc.connectAttr(dMtx + '.outputRotate', parentJntGrp[0] + '.rotate')

    # grouping joint
    jointGrp = mc.group(em=1, n=prefixNameCrv + 'Jnt' + '_grp')
    mc.parent(parentJntGrpZro, jointGrp)

    # grouping locator
    locatorGrp = mc.group(em=1, n=prefixNameCrv + 'Loc' + '_grp')
    mc.setAttr(locatorGrp + '.it', 0, l=1)
    mc.parent(parentLocGrpZro, locatorGrp)

    return {'allJoint':allJoint,
            'jointGrp': jointGrp,
            'locatorGrp': locatorGrp}

def replacePosLFTRGT(crv, sideRGT, sideLFT):
    if sideRGT in crv:
        crvNewName = crv.replace(sideRGT, '')
    elif sideLFT in crv:
        crvNewName = crv.replace(sideLFT, '')
    else:
        crvNewName = crv

    return crvNewName
def getUParam(pnt=[], crv=None):
    point = om.MPoint(pnt[0], pnt[1], pnt[2])
    curveFn = om.MFnNurbsCurve(getDagPath(crv))
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

def getDagPath(objectName):
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