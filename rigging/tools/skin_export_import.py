import os
import pickle
from __builtin__ import xrange

import maya.cmds as mc
import maya.mel as mm
import pymel.core as pm


def getDataFld():
    wfn = os.path.normpath(pm.sceneName())

    tmpAry = wfn.split('\\')
    tmpAry[-2] = 'data'

    dataFld = '\\'.join(tmpAry[0:-1])

    if not os.path.isdir(dataFld):
        os.mkdir(dataFld)

    return dataFld


def writeWeight(geo='', fn=''):
    skn = mm.eval('findRelatedSkinCluster( "%s" )' % geo)

    if skn:

        sknMeth = mc.getAttr('%s.skinningMethod' % skn)
        useCompo = mc.getAttr('%s.useComponents' % skn)
        infs = mc.skinCluster(skn, q=True, inf=True)
        sknSet = mc.listConnections('%s.message' % skn, d=True, s=False)[0]
        print(fn)
        fid = open(fn, 'w')
        wDct = {}

        wDct['influences'] = infs
        wDct['name'] = skn
        wDct['set'] = sknSet
        wDct['skinningMethod'] = sknMeth
        wDct['useComponents'] = useCompo

        for ix in xrange(mc.polyEvaluate(geo, v=True)):
            currVtx = '%s.vtx[%d]' % (geo, ix)
            skinVal = mc.skinPercent(skn, currVtx, q=True, v=True)
            wDct[ix] = skinVal

        pickle.dump(wDct, fid)
        fid.close()
    else:
        print('%s has no related skinCluster node.' % geo)


def writeSelectedWeight():
    # Export skin weight values into selected geometries
    suffix = 'Weight'
    for sel in mc.ls(sl=True):
        dataFld = getDataFld()
        fls = os.listdir(dataFld)
        fn = '%s%s.txt' % (sel, suffix)

        fPth = '%s/%s' % (dataFld, fn)
        writeWeight(sel, fPth)

    mc.confirmDialog(title='Progress', message='Exporting weight has done.')


def readWeight(geo='', fn=''):
    print('Loading %s' % fn)
    fid = open(fn, 'r')
    wDct = pickle.load(fid)
    fid.close()

    infs = wDct['influences']

    for inf in infs:
        if not mc.objExists(inf):
            print('Scene has no %s ' % inf)

    oSkn = mm.eval('findRelatedSkinCluster "%s"' % geo)
    if oSkn:
        mc.skinCluster(oSkn, e=True, ub=True)

    tmpSkn = mc.skinCluster(infs[0], geo, tsb=True)[0]

    for inf in infs[1:]:
        infTyp = mc.objectType(inf)
        if infTyp == 'joint':
            mc.skinCluster(tmpSkn, e=True, ai=inf, lw=True)
        elif infTyp == 'transform':
            baseInf = mc.duplicate(inf)[0]
            mc.setAttr('%s.v' % baseInf, 0)
            baseInf = mc.rename(baseInf, '%sBase' % baseInf)
            shp = mc.listRelatives(baseInf, s=True, f=True, ni=True)[0]
            mc.skinCluster(tmpSkn, e=True, lw=True, ug=True, dr=4, ps=0, ns=10, wt=0,
                           ai=inf, bsh=shp)

    skn = mc.rename(tmpSkn, wDct['name'])
    mc.setAttr('%s.skinningMethod' % skn, wDct['skinningMethod'])
    mc.setAttr('%s.useComponents' % skn, wDct['useComponents'])

    sknSet = mc.listConnections('%s.message' % skn, d=True, s=False)[0]
    mc.rename(sknSet, wDct['set'])

    for inf in infs:
        mc.setAttr('%s.liw' % inf, False)

    mc.setAttr('%s.normalizeWeights' % skn, False)
    mc.skinPercent(skn, geo, nrm=False, prw=100)
    mc.setAttr('%s.normalizeWeights' % skn, True)

    vtxNo = mc.polyEvaluate(geo, v=True)

    for ix in xrange(vtxNo):
        for iy in xrange(len(infs)):
            wVal = wDct[ix][iy]
            if wVal:
                wlAttr = '%s.weightList[%s].weights[%s]' % (skn, ix, iy)
                mc.setAttr(wlAttr, wVal)

        # Percent calculation
        if ix == (vtxNo - 1):
            print('100%% done.')
        else:
            prePrcnt = 0
            if ix > 0:
                prePrcnt = int((float(ix - 1) / vtxNo) * 100.00)

            prcnt = int((float(ix) / vtxNo) * 100.00)

            if not prcnt == prePrcnt:
                print('%s%% done.' % str(prcnt))


def readWeight2(geo='', fn='', searchFor='', replaceWith='', prefix='', suffix=''):
    print('Loading %s' % fn)
    fid = open(fn, 'r')
    wDct = pickle.load(fid)
    fid.close()

    infs = wDct['influences']

    print(infs)

    currInfs = []

    for inf in infs:
        currInf = inf
        if searchFor:
            currInf = currInf.replace(searchFor, replaceWith)
        print(currInf)
        currInfs.append('%s%s%s' % (prefix, currInf, suffix))

    for currInf in currInfs:
        if not mc.objExists(currInf):
            print('Scene has no %s ' % currInf)

    oSkn = mm.eval('findRelatedSkinCluster "%s"' % geo)
    if oSkn:
        mc.skinCluster(oSkn, e=True, ub=True)

    tmpSkn = mc.skinCluster(currInfs, geo, tsb=True)[0]
    skn = mc.rename(tmpSkn, wDct['name'])
    mc.setAttr('%s.skinningMethod' % skn, wDct['skinningMethod'])

    sknSet = mc.listConnections('%s.message' % skn, d=True, s=False)[0]
    mc.rename(sknSet, wDct['set'])

    for currInf in currInfs:
        mc.setAttr('%s.liw' % currInf, False)

    mc.setAttr('%s.normalizeWeights' % skn, False)
    mc.skinPercent(skn, geo, nrm=False, prw=100)
    mc.setAttr('%s.normalizeWeights' % skn, True)

    vtxNo = mc.polyEvaluate(geo, v=True)

    for ix in xrange(vtxNo):
        for iy in xrange(len(currInfs)):
            wVal = wDct[ix][iy]
            if wVal:
                wlAttr = '%s.weightList[%s].weights[%s]' % (skn, ix, iy)
                mc.setAttr(wlAttr, wVal)

        # Percent calculation
        if ix == (vtxNo - 1):
            print('100%% done.')
        else:
            prePrcnt = 0
            if ix > 0:
                prePrcnt = int((float(ix - 1) / vtxNo) * 100.00)

            prcnt = int((float(ix) / vtxNo) * 100.00)

            if not prcnt == prePrcnt:
                print('%s%% done.' % str(prcnt))


def readSelectedWeight2(weightFolderPath='', searchFor='', replaceWith='', prefix='', suffix=''):
    # Import skin weight values into selected geometries
    sels = mc.ls(sl=True)
    for sel in sels:

        if not weightFolderPath:
            dataFld = getDataFld()
        else:
            dataFld = os.path.normpath(weightFolderPath)
        fn = '%sWeight.txt' % sel

        try:
            print('Importing %s.' % sel)
            readWeight2(sel, os.path.join(dataFld, fn), searchFor, replaceWith, prefix, suffix)
            print('Importing %s done.' % fn)
        except:
            print('Cannot find weight file for %s' % sel)

    mc.select(sels)
    mc.confirmDialog(title='Progress', message='Importing weight is done.')


def readSelectedWeight(weightFolderPath=''):
    # Import skin weight values into selected geometries
    sels = mc.ls(sl=True)
    for sel in sels:

        if not weightFolderPath:
            dataFld = getDataFld()
        else:
            dataFld = os.path.normpath(weightFolderPath)
        fn = '%sWeight.txt' % sel

        try:
            print('Importing %s.' % sel)
            readWeight(sel, os.path.join(dataFld, fn))
            print('Importing %s done.' % fn)
        except Exception as e:
            print('Cannot find weight file for %s' % sel)
            print(e)

    mc.select(sels)
    mc.confirmDialog(title='Progress', message='Importing weight is done.')


def copySelectedWeight():
    # Copy skin weights from source object to target object.
    # Select source geometry then target geometry then run script.
    sels = mc.ls(sl=True)

    jnts = mc.skinCluster(sels[0], q=True, inf=True)

    oSkn = mm.eval('findRelatedSkinCluster( "%s" )' % sels[1])
    if oSkn:
        mc.skinCluster(oSkn, e=True, ub=True)

    skn = mc.skinCluster(jnts, sels[1], tsb=True)[0]

    mc.select(sels[0], r=True)
    mc.select(sels[1], add=True)
    mm.eval('copySkinWeights  -noMirror -surfaceAssociation closestPoint -influenceAssociation closestJoint;')
