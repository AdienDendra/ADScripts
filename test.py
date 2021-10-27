import maya.cmds as cmds

class TransferMode(object):
    vertexIndex = 0
    closestVertex = 1
    closestPoint = 2
    closestUV = 3
    closestUVPoint = 4
    spikes = 5


dControls = {}
dControls['iMode'] = controls.RadioButtonsControl(TransferMode)


@uiSettings.addToUI(sTab='SkinCluster', sModuleButton='Transfer', sRunButton='Transfer', dControls=dControls,
                  tRefreshControlsAfterRun=[], bAddDefaultButton=True)
def transferSkinCluster(_pSelection=None, sFrom=[], fBlend=1.0, iJointLocks=patch.JointLocks.ignore,
                        iMode=TransferMode.closestPoint, sPositionMesh=None,
                        xDistanceMeshes=None, iBorderEdges=patch.BorderEdges.doEverything, iSmoothBorderMask=2,
                        sChooseSkinCluster=None, bCreateNewSkinCluster=False, sRenameSkinClusterIfNew=None,
                        iCheckMissingInfluences=patch.MissingInfluencesOptions.askToAddOrCreateInfluences,
                        sJointsOverride=None, bMirror=False, _bResetSettings=True, funcMapJoint=None, bLogReport=True):
    if bCreateNewSkinCluster:
        sChooseSkinCluster = None

    # _validateChooseSkinCluster(sChooseSkinCluster)


    sFroms = utils.toList(sFrom)
    dFroms = defaultdict(list)
    for sF in sFroms:
        if '.' in sF:
            sObj, _ = sF.split('.')
            dFroms[sObj].append(sF)
        else:
            dFroms[sF] = None


    if _bResetSettings:
        patch.iMissingInfluencesForNext = None
        cmds.undoInfo(openChunk=True)
    try:
        sSelBefore = cmds.ls(sl=True)

        # tbFromPatches = [patch.patchFromName(sM) for sM in sFroms]
        pPatches = _translateInput(_pSelection)
        if bLogReport: report.report.resetProgress(len(pPatches))
        dChooseSkinCluster = {}
        for pSelected in pPatches:
            sConvertedChooseSkinCluster = deformers.convertChooseSkinCluster(sChooseSkinCluster, pSelected.getName())
            if bLogReport:
                report.report.incrementProgress()
                report.report.addLogText('transferring to %s...' % pSelected.getTransformName())

            sNonExistingMeshes = []
            sFromsTransfer = dFroms.keys()
            xSkipDict = {}
            for i, sFromMesh in enumerate(sFromsTransfer):
                if dFroms[sFromMesh] != None:
                    sComponents = dFroms[sFromMesh]#sFromMesh.split(' ')
                    # sFromMeshMesh = sComponents[0].split('.')[0]

                    if iMode in [TransferMode.closestVertex, TransferMode.closestUV]:
                        sComps = cmds.ls(cmds.polyListComponentConversion(sComponents, tv=True), flatten=True)
                    elif iMode in [TransferMode.closestPoint, TransferMode.closestUVPoint]:
                        sComps = cmds.ls(cmds.polyListComponentConversion(sComponents, tf=True), flatten=True)

                    aComps = np.array([int(sC.split('[')[1].split(']')[0]) for sC in sComps], dtype=int)
                    # sFromsTransfer[i] = sFromMeshMesh

                    if iMode in [TransferMode.closestVertex, TransferMode.closestUV]:
                        aSkip = np.setdiff1d(np.arange(cmds.polyEvaluate(sFromMesh, vertex=True)), aComps)
                    elif iMode in [TransferMode.closestPoint, TransferMode.closestUVPoint]:
                        aSkip = np.setdiff1d(np.arange(cmds.polyEvaluate(sFromMesh, face=True)), aComps)
                    xSkipDict[sFromMesh] = aSkip


                if cmds.objectType(sFromMesh) == 'skinCluster':
                    sFromsTransfer[i] = deformers.getGeoFromDeformer(sFromMesh)
                    dChooseSkinCluster[sFromsTransfer[i]] = sFromMesh
                if ',' in sFromMesh:
                    sFromMesh = sFromMesh.replace(' ', '')
                    sSearch, sReplace = sFromMesh.split(',')
                    sMesh = pSelected.getTransformName()
                    if sSearch in sMesh:
                        sFromsTransfer[i] = re.sub(sSearch, sReplace, sMesh)
                        if not cmds.objExists(sFromsTransfer[i]):
                            sNonExistingMeshes.append(sFromsTransfer[i])
                    else:
                        sFromsTransfer[i] = None

            if sNonExistingMeshes:
                print 'WARNING: skipping %s, because mesh %s don\'t exist!' % (sMesh, ', '.join(sNonExistingMeshes))
                continue
            sFromsTransfer = [sM for sM in sFromsTransfer if sM != None]
            if not sFromsTransfer:
                cmds.warning('no meshes to transfer found for %s' % pSelected.getName())
                continue

            tbFromPatches = [patch.patchFromName(sM) for sM in sFromsTransfer]
            iVertCounts = [tbP.getTotalCount() for tbP in tbFromPatches]

            # bUseComponents = False

            def _addProgressBarStep():
                pass

            if iMode in [TransferMode.closestVertex, TransferMode.closestPoint, TransferMode.closestUV,
                         TransferMode.closestUVPoint]:
                iSkipIds = [xSkipDict.get(sFromMeshTransfer, None) for sFromMeshTransfer in sFromsTransfer]
                bVertex = iMode in [TransferMode.closestVertex, TransferMode.closestUV]
                bUvs = iMode in [TransferMode.closestUV, TransferMode.closestUVPoint]
                pPositionMesh = pSelected if not sPositionMesh else patch.patchFromName(sPositionMesh)
                aAllMapVerts, aMapCoords, aMeshes = barycentric.getVertexCoordinates(tbFromPatches, pPositionMesh,
                                                                                     bUvs=bUvs,
                                                                                     bClosestVertex=bVertex,
                                                                                     fProgressBarFunc=_addProgressBarStep,
                                                                                     iiSkipVertOrFaceIds=iSkipIds,
                                                                                     bMirror=bMirror)
            elif iMode == TransferMode.vertexIndex:
                if len(sFromsTransfer) > 1:
                    cmds.warning(
                        'when vertexIndex is set, multiple meshes is not supported, taking the first one ("%s")' %
                        tbFromPatches[0].getName())
                aMeshes = np.zeros(len(pSelected.aIds), dtype=int)
                aAllMapVerts = pSelected.aIds
                # bVertex = True
            elif iMode == TransferMode.spikes:
                iNbs = pSelected.getIslands()
                aVerts = pSelected.getAllPoints(bWorld=True)

                mPoints, iIntersectionEdges = tbFromPatches[0].getEdgeIntersections(pSelected)
                if mPoints:
                    aPoints = np.array(mPoints, dtype='float64')[:, 0:3]
                    aIntersectionEdges = np.array(iIntersectionEdges, dtype=int)
                    aMapEdges = np.zeros(np.max(aIntersectionEdges) + 1, dtype=int)
                    aMapEdges[aIntersectionEdges] = np.arange(len(aIntersectionEdges))

                    fMeans = []
                    # for each Island get eiher the mean intersection point, or the mean point between all its
                    # vertices if it doesn't intersect

                    if len(iNbs) > 1:  # polys (curves and surfaces wouldn't fall into that since they only have one island)
                        aVertexEdges = utils.numpify2dList(pSelected.getAllVertexEdges())

                    if bLogReport:
                        if len(iNbs) > 1:
                            report.report.addLogText('spikes count: %d' % len(iNbs))
                            report.report.addToMaximum(len(iNbs) / 10)

                    for i, iIsland in enumerate(iNbs):
                        aIsland = np.array(iIsland, dtype=int)
                        if len(iNbs) > 1:  # polys (curves and surfaces wouldn't fall into that since they only have one island)
                            aIslandEdges = np.unique(aVertexEdges[aIsland].flatten())
                            aIslandIntersectionEdges = np.intersect1d(aIntersectionEdges, aIslandEdges,
                                                                      assume_unique=True)
                        else:  # curves or surfaces
                            aIslandIntersectionEdges = aIntersectionEdges
                        if len(aIslandIntersectionEdges):
                            if isinstance(pSelected, patch.CurvePatch): # if it's a hair strand, we just want the closest intersection at the root
                                aIslandIntersectionEdges = aIslandIntersectionEdges[:1]
                            aIslandIntersectionEdges = np.array(aIslandIntersectionEdges, dtype=int)
                            aIndices = aMapEdges[aIslandIntersectionEdges]
                            aIslandPoints = aPoints[aIndices]
                            aMean = np.average(aIslandPoints, axis=0)
                        else:
                            aMean = np.mean(aVerts[aIsland], axis=0)
                        fMeans.append(aMean)

                        if bLogReport and not i % 10:
                            report.report.incrementProgress()

                else:
                    fMeans = []
                    for i, iIsland in enumerate(iNbs):
                        aIsland = np.array(iIsland, dtype=int)
                        fMeans.append(np.mean(aVerts[aIsland], axis=0))

                fnCurve = OpenMaya2.MFnNurbsCurve()

                mMeans = OpenMaya2.MPointArray([OpenMaya2.MPoint(fM) for fM in fMeans])

                mMeansCurve = mMeans if len(mMeans) > 1 else [mMeans[0], OpenMaya2.MPoint(0, 0, 0)]
                mKnots = OpenMaya2.MDoubleArray([0] * len(mMeansCurve))
                oCurve = fnCurve.create(mMeansCurve, mKnots, 1, OpenMaya2.MFnNurbsCurve.kOpen, False, False)
                sCurve = OpenMaya2.MFnDagNode(oCurve).fullPathName()
                pCurve = patch.patchFromName(sCurve)
                aCurveVerts, aCurveCoords, aCurveMeshes = barycentric.getVertexCoordinates([tbFromPatches[0]], pCurve,
                                                                                           bClosestVertex=False,
                                                                                           bMirror=False)

                if len(mMeansCurve) != len(mMeans):
                    aCurveVerts = aCurveVerts[:-1]
                    aCurveCoords = aCurveCoords[:-1]

                cmds.delete(sCurve)
                aAllMapVerts = np.zeros((pSelected.getTotalCount(), aCurveVerts.shape[1]), dtype=int)
                aMapCoords = np.zeros((pSelected.getTotalCount(), aCurveVerts.shape[1]), dtype='float64')
                aMeshes = np.zeros(pSelected.getTotalCount(), dtype=int)

                for i, iIsland in enumerate(iNbs):
                    aIsland = np.array(iIsland, dtype=int)
                    aAllMapVerts[aIsland] = aCurveVerts[i]
                    aMapCoords[aIsland] = aCurveCoords[i]
                # end of analyzing for spikes

            sAllFromSkinClusters = []
            xWeights, xInfluences, xGetIds, xInds, xIdMaps = [], [], [], [], []
            for iMesh, tbFromPatch in enumerate(tbFromPatches):
                iSourceVertexCount = iVertCounts[iMesh]

                aInds = np.array(np.where(aMeshes == iMesh)[0], dtype=int)
                xInds.append(aInds)
                aGetIds = np.unique(aAllMapVerts[aInds].ravel())
                aGetIds.sort()
                aGetIds = np.delete(aGetIds, np.where(aGetIds == -1)[0])
                xGetIds.append(aGetIds)
                aIdMapper = np.zeros(iSourceVertexCount, dtype=int)
                aIdMapper[aGetIds] = np.arange(aGetIds.size)
                xIdMaps.append(aIdMapper[aAllMapVerts[aInds]])

                sChooseFromSkinCluster = dChooseSkinCluster.get(sFromsTransfer[iMesh], None)
                sSkinCluster, sInfluences, aWeights2d = tbFromPatch.getSkinCluster(aOverrideIds=aGetIds,
                                                                                   sChooseSkinCluster=sChooseFromSkinCluster)

                if not sSkinCluster:
                    raise Exception, 'trying to transfer weights from %s, but it doesn\'t have a skinCluster!' % tbFromPatch.getName()


                sInfluences = np.array(sInfluences)
                if funcMapJoint != None:
                    sInfluences = [funcMapJoint(sJ) for sJ in sInfluences]
                sDuplicates = utils.getDuplicates(sInfluences)
                if sDuplicates:
                    for sDupl in sDuplicates:
                        iDuplInds = []
                        for i,sInf in enumerate(sInfluences):
                            if sInf == sDupl:
                                iDuplInds.append(i)
                        for iInd in iDuplInds[1:]:
                            aWeights2d[:,iDuplInds[0]] += aWeights2d[:,iInd]
                        sInfluences = np.delete(sInfluences, iDuplInds[1:])
                        aWeights2d = np.delete(aWeights2d, iDuplInds[1:], axis=1)



                sAllFromSkinClusters.append(sSkinCluster)

                if sJointsOverride != None:
                    sInfluences = sJointsOverride[iMesh]
                xWeights.append(aWeights2d)
                xInfluences.append(list(sInfluences))

            sReducedInfluences = reduce((lambda x, y: x + y), xInfluences)

            aAllInfluences = np.unique(np.array(sReducedInfluences))

            dAllInfluences = dict(zip(aAllInfluences, xrange(aAllInfluences.size)))
            iInfCount = aAllInfluences.size
            aWeights = np.zeros((pSelected.aIds.size, iInfCount), dtype='float64')
            for iMesh, tbFromPatch in enumerate(tbFromPatches):

                if xInds[iMesh].size == 0:
                    continue
                aMappedInfluences = np.array([dAllInfluences[sInf] for sInf in xInfluences[iMesh]], dtype=int)
                if iMode in [0, 1, 3]:
                    aWeights[xInds[iMesh][:, np.newaxis], aMappedInfluences] = xWeights[iMesh][xIdMaps[iMesh]]
                elif iMode in [2, 4, 5]:
                    aMultiplied = xWeights[iMesh][xIdMaps[iMesh]] * aMapCoords[xInds[iMesh]][..., np.newaxis]
                    aWeights[xInds[iMesh][:, np.newaxis], aMappedInfluences] = np.sum(aMultiplied, axis=1)

            if bCreateNewSkinCluster and not sRenameSkinClusterIfNew:
                sRenameSkinClusterIfNewLocal = 'skinCluster__%s' % pSelected.getTransformName()
                sSplits = sFroms[0].split('__')
                if len(sSplits) == 3:
                    sRenameSkinClusterIfNewLocal = '%s__%s' % (sRenameSkinClusterIfNewLocal, sSplits[-1])
            else:
                sRenameSkinClusterIfNewLocal = sRenameSkinClusterIfNew

            aExtractedWeights2d, sExtractedInfluences = patch._removeZeroInfluencesNumpy(aWeights, aAllInfluences)
            pSelected.setSkinClusterWeights(aExtractedWeights2d, sExtractedInfluences,
                                            iCheckMissingInfluences=iCheckMissingInfluences, iJointLocks=iJointLocks,
                                            iBorderEdges=iBorderEdges, iSmoothBorderMask=iSmoothBorderMask,
                                            xDistanceMeshes=xDistanceMeshes, fBlend=fBlend,
                                            sChooseSkinCluster=sConvertedChooseSkinCluster,
                                            bAlwaysCreateNew=bCreateNewSkinCluster,
                                            sRenameSkinClusterIfNew=sRenameSkinClusterIfNewLocal,
                                            iSkinningMethodIfNew=cmds.getAttr(
                                                '%s.skinningMethod' % sAllFromSkinClusters[0]))

        cmds.select(sSelBefore)
    except:
        raise
    finally:
        if _bResetSettings:
            patch.iMissingInfluencesForNext = None
            cmds.undoInfo(closeChunk=True)