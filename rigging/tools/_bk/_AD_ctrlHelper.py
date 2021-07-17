import AD_utils as ut
import maya.cmds as mc


def parentConsCtrl(objFirst, objScnd):

#sel = mc.ls(sl=1)
# mul = sel.pop(1)

    for s in objFirst:
        renCtrl = mc.ls(s, sl=1)
        print renCtrl


        #nameSpace = mc.namespace(renCtrl, ex=True)
        #print nameSpace
        """if ':' in renCtrl == True:
            split = s.split(':')[1]
            grps= []
            grps.append(split)
            print grps

            objFirstCtrl = split
        else:
            objFirstCtrl = renCtrl"""

        for t in objScnd:
            shpScnd = ut.get_transform_shape_position(t)
            sCtrlScndScnd = ut.scale_curve(1.00, shpScnd)
            CtrlScnd = ut.create_controller(sCtrlScndScnd)

            renCtrlScnd = mc.rename(CtrlScnd, '%s%s' % (ut.ad_lib_main_name(t), 'Tweak_ctrl'))

            grpPrntScnd = ut.group_parent(['Zro'], '%s' % ut.ad_lib_main_name(t), 'TweakCtrl')

            # parent gimbal CtrlScnd to main CtrlScnd
            ut.parent_object(grpPrntScnd, renCtrlScnd)

            # match position the group CtrlScnd as the obj
            ut.match_position(t, grpPrntScnd[0])

            # color control
            ut.ad_cc_set_color(renCtrlScnd, 'darkBrown')

            mc.setAttr('%s.visibility' %renCtrlScnd, lock=False, keyable=False)

            #grpObj = ut.groupParent(['Zro','Offset'], t, 'Helper')


            #ut.matchPosition(t, grpObj[0])

            ut.ad_lib_parent_constraint(renCtrlScnd, t)
            #print a
            ut.ad_lib_scale_constraint(renCtrlScnd, t)

            prntConstraint = ut.ad_lib_parent_constraint(renCtrl, grpPrntScnd[0], mo=1)


            ut.add_attr_transform(renCtrlScnd, 'parentConsSet', 'long', min=0, max=1, dv=1, edit=True, keyable=True)

            dispLayer = mc.createDisplayLayer(t, n= '%s%s'% (t, '_lyr'), num=1, nr=True)
            mc.setAttr(dispLayer+'.visibility',0)

            mc.setDrivenKeyframe('%s.nodeState' % prntConstraint[0], cd='%s.parentConsSet' % renCtrlScnd, dv=0, v=10)
            mc.setDrivenKeyframe('%s.nodeState' % prntConstraint[0], cd='%s.parentConsSet' % renCtrlScnd, dv=1, v=0)

            mc.setKeyframe(renCtrlScnd, bd=0, hi='none', cp=0, s=0)

            mc.keyTangent('%s.parentConsSet' % renCtrlScnd, ott='step')

            mc.keyTangent('%s.nodeState' % prntConstraint[0], ott='step')

            mc.setAttr('%s.interpType' %prntConstraint[0], 0)

            #mc.connectAttr('%s.parentConsSet' %renCtrlScnd, '%s.wristFkLFT_ctrlW0' %prntConstraint[0])


            #mc.setDrivenKeyframe('%s.wristFkLFT_ctrlW0' %prntConstraint[0], cd='%s.parentConsSet' %renCtrlScnd, dv=0, v=0)
            #mc.setDrivenKeyframe('%s.wristFkLFT_ctrlW0' %prntConstraint[0], cd='%s.parentConsSet' %renCtrlScnd, dv=1, v=1)

            #decomposMtx = mc.createNode('decomposeMatrix', n= '%s_%s' % (ut.prefixName(renCtrlScnd),'dMt'))

            #mc.connectAttr('%s.worldMatrix[0]' %grpObj[1], '%s.inputMatrix' %decomposMtx)

            #mc.connectAttr('%s.outputRotate' %decomposMtx, '%s.rotate' %grpPrntScnd[0])
            #mc.connectAttr('%s.outputTranslate' %decomposMtx, '%s.translate' %grpPrntScnd[0])
            #mc.connectAttr('%s.outputScale' %decomposMtx, '%s.scale' %grpPrntScnd[0])

            #allGrouping = ut.groupParent(['Zro'], t, 'All')
            #ut.parentObj(allGrouping, grpObj[0])
            #ut.parentObj(allGrouping, grpPrntScnd)



#############
            #animCurve = mc.createNode('animCurveUL', n= '%s_%s' % (ut.prefixName(renCtrlScnd),'aCrv'))

            #mc.setAttr('%s.interpType' %prntConstraint, 0)

            #mc.connectAttr('%s.parentConsSet' %renCtrlScnd, '%s.nodeState' %prntConstraint)

            #setRange = mc.createNode('setRange', n= '%s_%s' % (ut.prefixName(renCtrlScnd),'sR'))

            #mc.connectAttr('%s.parentConsSet' %renCtrlScnd, '%s.valueX' %setRange)


