import maya.cmds as mc


def listingObject():
    sel = mc.ls(sl=1)

    jntSource = []
    grpTgt = []
    ctrl = []
    for i in sel:
        ctrl.append(i)
        lr = mc.listRelatives(i, ap=1, f=1)[0]
        spt = lr.split('|')
        lr = filter(None, spt)[-2]
        grpTgt.append(lr)
        lc = mc.listConnections(lr, s=1)
        if lc:
            lc = mc.listConnections(lr + '.translateX', s=1)[0]
            try:
                tgtList1 = mc.listConnections(lc + '.target[1].targetParentMatrix', s=1)[0]
                if tgtList1:
                    jntSource.append(tgtList1)
            except:
                tgtList0 = mc.listConnections(lc + '.target[0].targetParentMatrix', s=1)[0]
                jntSource.append(tgtList0)
        else:
            jntSource.append(lc)

    print('jointSource = ', jntSource)
    print('groupTarget = ', grpTgt)
    print('ctrls = ', ctrl)

    return {'jointSource': jntSource,
            'grpTarget': grpTgt,
            'ctrls': ctrl}


def reConnectConstraint(jointSource, groupTarget, ctrls, offset=True):
    for i, tgt, ctrl in zip(jointSource, groupTarget, ctrls):
        if i:
            if offset:
                constraint = mc.parentConstraint('worldspaceCon', i, tgt, mo=1)[0]
            else:
                mc.parentConstraint('worldspaceCon', tgt, mo=1, w=0)
                constraint = mc.parentConstraint(i, tgt, mo=0, w=1)[0]

            name = ctrl.replace('ctrl', 'rev')
            reverse = mc.createNode('reverse', n=name)

            if not mc.objExists('%s.LocalWorld' % (ctrl)):
                addAttrConf(ctrl, 'LocalWorld', at='float', k=True, dv=0, min=0, max=1)

            mc.connectAttr(ctrl + '.LocalWorld', reverse + '.inputX')

            mc.connectAttr(ctrl + '.LocalWorld', constraint + '.worldspaceConW0')

            mc.connectAttr(reverse + '.outputX', constraint + '.%sW1' % i)


def addAttrConf(obj, attrName, at, e=False, k=False, cb=False, **kwargs):
    if mc.nodeType(obj) == "transform":
        mc.addAttr(obj, ln=attrName, at=at, **kwargs)
        mc.setAttr('%s.%s' % (obj, attrName), e=e, k=k, cb=cb)
    return obj
