def getSkinCluster(geomShape):
    """ from Nicholas Bolden -- a better way to locate the skin cluster on a piece of geometry """
    import maya.OpenMaya as om
    import maya.OpenMayaAnim as oma

    mesh = geomShape
    mSel = om.MSelectionList()
    mSel.add(mesh)
    meshMObject = om.MObject()
    meshDagPath  = om.MDagPath()
    mSel.getDependNode(0, meshMObject)
    mSel.getDagPath(0, meshDagPath)

    skinFn = None
    iterDg = om.MItDependencyGraph(meshMObject,
                                   om.MItDependencyGraph.kDownstream,
                                   om.MItDependencyGraph.kPlugLevel)

    while not iterDg.isDone():
        currentItem = iterDg.currentItem()
        if currentItem.hasFn(om.MFn.kSkinClusterFilter):
            skinFn = oma.MFnSkinCluster(currentItem)
            break
        iterDg.next()

    if skinFn:
        return skinFn.name()
    else:
        return None



def skinAs(source=None, targs=None):
    """ skins many pieces of geomtry the same as the source geom.
        Select all the geometry and the SOURCE geom last.  """

    import pymel.core as pm

    # DETERMINE IF ARGS ARE strings, pynodes or a selection
    source = source or  pm.selected()[-1]
    targs = targs or pm.selected()[:-1]

    # GET THE SHAPE NODE OF THE SOURCE GEOMETRTY
    sourceShape = source.getShape()

    # GET THE SKIN CLUSTER ON THE SOURCE GEOM MORE RELIABLE
    sscl = pm.PyNode(getSkinCluster(sourceShape.longName()))

    # GET THE INFLUENCES (including non-joint types)
    sInfs = sscl.getInfluence()

    for targ in targs:

        # DETATCH ANY existing OLD target skin clusters on the target geom
        tGeomScls = [ pm.delete(oldScl) for oldScl in targ.getShape().inputs(type="skinCluster")]

        # CREATE A DUMMY JOINT TO SKIN TO THEN ADD THE INFLUENCES stupid maya
        pm.select(d=True)
        dummyJnt=pm.joint(name="dummy_JNT")
        pm.select(d=True)

        # CREATE A NEW SKIN CLUSTER
        tscl = pm.skinCluster(targ,dummyJnt,n="%s_SCL"%targ.nodeName())

        # NOW LOOP THROUGH THE INFLUENCES AND ADD THEM INTO THE SCL
        for inf in sInfs:
            pm.skinCluster(tscl, e=True, ai=inf,)

        # DELETE THE DUMMY JNT ONCE ALL THE INFLUENCES ARE THERE
        pm.delete(dummyJnt)

        # COPY SKIN WEIGHTS
        pm.select(source, targ,r=True)
        pm.copySkinWeights(noMirror=True, surfaceAssociation="closestPoint", smooth=True, influenceAssociation=("name","label","oneToOne"))

skinAs(source=None, targs=None)
