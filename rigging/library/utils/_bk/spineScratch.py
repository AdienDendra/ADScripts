# from . import module
# from . import controls
#
#
# def build(
#         ribbonSurface,
#         spineJoints,
#         pelvisJnt,
#         rootJnt,
#         prefix='spine',
#         ctrlScale=1.0
# ):
#     # make module
#     moduleObjs = module.make(prefix=prefix)
#
#     # make controls
#
#     bodyCtrl = controls.make(prefix=prefix + 'Body', ctrlScale=ctrlScale * 5, ctrlShape='square', matchObjectTr=rootJnt,
#                              parentObj=moduleObjs['controlsGrp'])
#
#     pelvisJntEnd = mc.listRelatives(pelvisJnt, c=True, type='joint')[0]
#     hipsCtrl = controls.make(prefix=prefix + 'Hips', ctrlScale=ctrlScale * 4, ctrlShape='circleY',
#                              matchObjectTr=pelvisJnt, parentObj=bodyCtrl['c'])
#     hipsLocalCtrl = controls.make(prefix=prefix + 'HipsLocal', ctrlScale=ctrlScale * 3, ctrlShape='circleY',
#                                   matchObjectTr=pelvisJnt, parentObj=hipsCtrl['c'])
#     chestCtrl = controls.make(prefix=prefix + 'Chest', ctrlScale=ctrlScale * 4.5, ctrlShape='circleY',
#                               matchObjectTr=spineJoints[-3], parentObj=bodyCtrl['c'])
#     chestLocalCtrl = controls.make(prefix=prefix + 'ChestLocal', ctrlScale=ctrlScale * 4, ctrlShape='circleY',
#                                    matchObjectTr=spineJoints[-2], parentObj=chestCtrl['c'])
#
#     # offset hips controls
#     hipsCls, hipsClsHdl = mc.cluster(hipsCtrl['c'], n='tempShapeOffset_cls')
#     mc.delete(mc.pointConstraint(pelvisJnt, pelvisJntEnd, hipsClsHdl))
#     mc.delete(hipsCtrl['c'], ch=True)
#
#     # attach skeleton
#     mc.parentConstraint(bodyCtrl['c'], rootJnt, mo=True)
#
#     # drive joints
#     mc.parentConstraint(hipsLocalCtrl['c'], pelvisJnt, mo=True)
#     mc.parentConstraint(chestLocalCtrl['c'], spineJoints[-2], mo=True)
#
#     # ribbon setup
#     mc.parent(ribbonSurface, moduleObjs['partsStaticGrp'])
#     ribbonFolliclesGrp = mc.group(n=prefix + 'RibbonFolic_grp', em=True, p=moduleObjs['partsStaticGrp'])
#
#     closestPointNode = mc.createNode('closestPointOnSurface', n=prefix + 'ClosestRibbonPoint_cpo')
#     mc.connectAttr(ribbonSurface + '.worldSpace[0]', closestPointNode + '.inputSurface')
#
#     for i, spineJnt in enumerate(spineJoints[:-2]):
#         jntPos = mc.xform(spineJnt, q=True, t=True, ws=True)
#         mc.setAttr(closestPointNode + '.inPosition', jntPos[0], jntPos[1], jntPos[2])
#         uParam = mc.getAttr(closestPointNode + '.parameterU')
#         vParam = mc.getAttr(closestPointNode + '.parameterV')
#
#         folic = mc.createNode('follicle', n='%sRibbon%d_folShape' % (prefix, i + 1))
#         folicTrans = mc.listRelatives(folic, p=1)[0]
#         folicParent = folicTrans
#         mc.parent(folicParent, ribbonFolliclesGrp)
#         mc.connectAttr(ribbonSurface + '.worldMatrix', folic + '.inputWorldMatrix')
#         mc.connectAttr(ribbonSurface + '.local', folic + '.inputSurface')
#
#         mc.connectAttr(folic + '.outTranslate', folicParent + '.t')
#         mc.connectAttr(folic + '.outRotate', folicParent + '.r')
#
#         mc.setAttr(folic + '.parameterU', uParam)
#         mc.setAttr(folic + '.parameterV', vParam)
#
#         mc.parentConstraint(folicParent, spineJnt, mo=True)
#
#     mc.delete(closestPointNode)
#
#     # connect controls to ribbon surface
#     chestRibbonCvs = '%s.cv[0:3][0:1]' % ribbonSurface
#     hipsRibbonCvs = '%s.cv[0:3][2:3]' % ribbonSurface
#
#     chestRibbonClsHdl = mc.cluster(chestRibbonCvs, wn=[chestCtrl['c'], chestCtrl['c']], bs=True,
#                                    n=prefix + 'ChestRibbon_cls')
#     hipsRibbonClsHdl = mc.cluster(hipsRibbonCvs, wn=[hipsCtrl['c'], hipsCtrl['c']], bs=True,
#                                   n=prefix + 'ChestRibbon_cls')
#
#     return {
#         'moduleObjs': moduleObjs,
#         'bodyCtrl': bodyCtrl
#     }
