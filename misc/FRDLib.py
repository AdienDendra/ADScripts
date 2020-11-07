def NUN_Module():
    ## --------------- N.NUN MODULE ---------------- ##
    import sys
    path = ['G:/My Drive/PERSONAL/base']
    for p in path :
        if p in sys.path :
            sys.path.remove( p )
        if not p in sys.path :
            sys.path.insert( 0,p )
    from nnTools import nnCurve as nc
    from nnTools import nnCore as nnc
    from nnTools import nnRigTools as nt
    from nnTools import nnTools as nn
    from nnTools import weTools as we
    reload( nc )
    reload( nnc )
    reload( nt )
    reload( nn )
    reload( we )
def skinExportImport():

    import pkmel.weightTools as pwt

    pwt.writeSelectedWeight()
    pwt.readSelectedWeight()

def CreateFK_UI():
    ##________________ CREATE FK UI ________________ ##

    from nnTools.python import nnFkRig
    from nnTools.python.nnFkRig import nnFkRigMain

    reload(nnFkRig)
    reload(nnFkRigMain)

    if mc.window('nnFkRigUI', exists=True):
        mc.deleteUI('nnFkRigUI')
    myapp = nnFkRigMain.MyForm(nnFkRigMain.getMayaWindow())

    ##________________ CONTROLLER UI ________________ ##

    from nnTools.python.nnControls import nnControlsMain2 as nnControlsMain2

    if mc.window('nnControlsUI', exists=True):
        mc.deleteUI('nnControlsUI')

    myapp = nnControlsMain2.MyForm(nnControlsMain2.getMayaWindow())

    ##________________ ASSIGN SHADE UI ________________ ##

    import sys

    path = 'G:/My Drive/PERSONAL/base/nnTools/manager'
    if not path in sys.path:
        sys.path.append(path)

    import nAssign

    reload(nAssign)

    nAssign.nAssignUI().show()




def inBetweenJoint:

#PY------------------------------RUN Between Jnt -----------------------------------------------------------

from nuTools.rigTools import proc
reload(proc)


# Select 1.parentJnt, 2.startJnt, 3.endJnt
# Neck
proc.btwJnt(jnts=['spine5ScaProxySkin_jnt', 'neck1ProxySkin_jnt', 'neckRbnProxySkin_jnt'], pointConstraint=True)

# Arm LFT
  # clavicle
proc.btwJnt(jnts=['spine5ScaProxySkin_jnt', 'clav1ProxySkinLFT_jnt', 'clav2ProxySkinLFT_jnt'], pointConstraint=True)
  # uparm
proc.btwJnt(jnts=['clav1ProxySkinLFT_jnt', 'upArmProxySkinLFT_jnt', 'upArmRbnDtl1ProxySkinLFT_jnt'], pointConstraint=True)
  # forearm
proc.btwJnt(jnts=['upArmRbnDtl5ProxySkinLFT_jnt', 'forearmProxySkinLFT_jnt', 'forearmRbnDtl1ProxySkinLFT_jnt'], pointConstraint=False)
  # wrist
proc.btwJnt(jnts=['forearmRbnDtl5ProxySkinLFT_jnt', 'wristProxySkinLFT_jnt', 'handProxySkinLFT_jnt'], pointConstraint=True)

# Arm RGT
  # clavicle
proc.btwJnt(jnts=['spine5ScaProxySkin_jnt', 'clav1ProxySkinRGT_jnt', 'clav2ProxySkinRGT_jnt'], pointConstraint=True)
  # uparm
proc.btwJnt(jnts=['clav1ProxySkinRGT_jnt', 'upArmProxySkinRGT_jnt', 'upArmRbnDtl1ProxySkinRGT_jnt'], pointConstraint=True)
  # forearm
proc.btwJnt(jnts=['upArmRbnDtl5ProxySkinRGT_jnt', 'forearmProxySkinRGT_jnt', 'forearmRbnDtl1ProxySkinRGT_jnt'], pointConstraint=False)
  # wrist
proc.btwJnt(jnts=['forearmRbnDtl5ProxySkinRGT_jnt', 'wristProxySkinRGT_jnt', 'handProxySkinRGT_jnt'], pointConstraint=True)

# Leg LFT
  # upleg
proc.btwJnt(jnts=['spine1ScaProxySkin_jnt', 'upLegProxySkinLFT_jnt', 'upLegRbnDtl1ProxySkinLFT_jnt'], pointConstraint=True)
  # knee
proc.btwJnt(jnts=['upLegRbnDtl5ProxySkinLFT_jnt', 'lowLegProxySkinLFT_jnt', 'lowLegRbnDtl1ProxySkinLFT_jnt'], pointConstraint=False)
  # ankle
proc.btwJnt(jnts=['lowLegRbnDtl5ProxySkinLFT_jnt', 'ankleProxySkinLFT_jnt', 'ballProxySkinLFT_jnt'], pointConstraint=True)

# Leg RGT
  # upleg
proc.btwJnt(jnts=['spine1ScaProxySkin_jnt', 'upLegProxySkinRGT_jnt', 'upLegRbnDtl1ProxySkinRGT_jnt'], pointConstraint=True)
  # knee
proc.btwJnt(jnts=['upLegRbnDtl5ProxySkinRGT_jnt', 'lowLegProxySkinRGT_jnt', 'lowLegRbnDtl1ProxySkinRGT_jnt'], pointConstraint=False)
  # ankle
proc.btwJnt(jnts=['lowLegRbnDtl5ProxySkinRGT_jnt', 'ankleProxySkinRGT_jnt', 'ballProxySkinRGT_jnt'], pointConstraint=True)

mc.setAttr( 'forearmProxySkinBtwLFT_jnt.scaleLimit' , 1.7 )
mc.setAttr( 'forearmProxySkinBtwRGT_jnt.scaleLimit' , 1.7 )
mc.setAttr( 'lowLegProxySkinBtwLFT_jnt.scaleBtw' , 0.5 )
mc.setAttr( 'lowLegProxySkinBtwRGT_jnt.scaleBtw' , 0.5 )


#--------------------run fix cloth (nonRoll Rbb)

import pkmel.weightTools as pwt
pwt.writeSelectedWeight()


from nuTools.rigTools import proc
reload(proc)
proc.ribbonNonRollRig(
                        rbnCtrl=pm.selected()[0],
                        elem='lowSleeve',
                        side='LFT',
                        skinGrp='skin_grp',
                        animGrp='anim_grp',
                        rbnAttr='detail',
                        visAttrName='nonRollDetail',
                        ctrlColor='pink'
                      )


def nunControl:

# ------------------------------------------nun create control------------------------------

from nnTools import nnTools as nn
reload( nn )






nn.ad_create_ctrl(
					shape='circle' ,
					scale=1 ,
					color='red' ,
					gmbl=True ,
					geoVis=True ,
					locWor=None ,
					targetWor='Anim_Ctrl_Grp' ,
					targetLoc='' ,
					constraint='parent' ,
					connect='parentConstraint'

			)

#shape ctrl list =
'circle', 'circlePlus' , 'circle3d', 'circle3dPlus', 'square', 'squarePlus', 'cube', 'circleHalf3dPlus'
'stickCircle', 'stickCirclePlus', 'stickCircle3d', 'stickCircle3dPlus', 'stick2CirclePlus'
'stickSquare', 'stickSquarePlus', 'stick2SquarePlus', 'stickSquareCurve', 'stickKnot'
'arrow', 'circleArrow', 'circleArrowTwo', 'crossArrow', 'curveArrow'
'cylinder', 'octagon', 'capsule', 'rectangle', 'plus'
'grid', 'null', 'rectangleCurve', 'cylinderHalf', 'squareCurve', 'circleCover','circleCurve'

from tool.rig.nnTools import nnCurve as nc
reload(nc)

from tool.rig.nnTools.python import nnCore as nnc
reload( nnc )

from tool.rig.nnTools import nnRigTools as nt
reload(nt)

from tool.rig.nnTools import nnTools as nn
reload(nn)

#### BS utilities #########
Y:\USERS\Beau\blendshapeUtil.py

#blendshape reverse#####
misc.inverseBlendShapeWeight(blendShapeNode='cheekSep_bsn', index=None, geoIndex=0)







def faceDetailControl:

# --------------- facre detail controls  ------------------------
    from nuTools.rigTools import dtlRig as dr
    reload(dr)

    sel = mc.ls( sl=True )
    faceDtlRig = dr.DtlRig(
                               rivetMesh   = 'headFacDtlPos_ply' ,
                               skinMesh    = '' ,
                               elem        = 'face' ,
                               tempLocs    = sel ,
                               ctrlColor   = 'lightBlue' ,
                               ctrlShape   = 'cube' ,
                               size        = 0.2
                           )
    faceDtlRig.rig()


    # 1. create locators in the positions you want to add dtl controllers
    # 2. duplicate original mesh, name it as xxxPos_ply, fill the name in script
    # 3. runscript
    # 4. bind the new joint those ones created by script to the xxxDtl_ply paintSkin weight

def bladeFan:
    # BLADE FAN
    nn.timeSpeed(rotate='X')

def vehicleRigging:

#-------------------- vechicle rigging

## 1.create ctrl wheel
## 2.select ctrl and Rotate wheel geo group( can select all at once )
## 3.run script
from nuTools.rigTools import proc
reload( proc )
proc.wheelAutoRotateExp( direction = 'z' , axis = 'x' )


## 1.create chassis group and move to correct point
## 2.run script
from tool.rig.nnTools import nnTools as nn
reload( nn )
nn.chassisRig()

#####
spineCRig.attach(base='spine3_jnt',
				tip='spine4_jnt',
				baseParent='spine3_jnt',
				tipTwistParent='spine4_jnt',
				twistFromBase=False,
				upAxis='+x',
				parentUpAxis='+x')




def connectSkeletonToProxySkin:

#--------------------- Connect DuleSkeleton to ProxySkin --------------------
from nuTools.pipeline import pipeTools
reload( pipeTools )

#--- Pipeline publish
pipeTools.importAllRefs()
pipeTools.removeAllNameSpace()
pipeTools.deleteAllTurtleNodes()
pipeTools.deleteExtraDefaultRenderLayer()
pipeTools.deleteUnusedNodes()
pipeTools.parentPreConsObj()

pipeTools.connectDualSkeleton(False, False)

#--- Cleanup Scene
pipeTools.deleteUnusedNodes()
pipeTools.optimizeSceneSize()

pipeTools.removePlugin('Mayatomr.mll')
pipeTools.removePlugin('vrayformaya.mll')
pipeTools.removePlugin('Turtle.mll')



def createRivet():
from nuTools import misc
reload(misc)
misc.createRivetFromPosition_Mesh()

#blendshape base
from nuTools.rigTools import faceCurveRig as fcr
reload(fcr)

print fcr.__doc__


def nonRollRibbonCloth:

# --------------------run fix cloth (nonRoll Rbb)
from nuTools.rigTools import proc
reload(proc)
proc.ribbonNonRollRig(
    rbnCtrl=None,
    elem='dtlRbb',
    side='LFT',
    skinGrp='skin_grp',
    animGrp='anim_grp',
    rbnAttr='detail',
    visAttrName='nonRollDetail',
    ctrlColor='pink'
)


def rigHair:

#--------------------------------------- base hair ------------------------------
    from nnTools.python import nnRigHair

    reload(nnRigHair)

    hairRig = nnRigHair.HairRig(parentSpine='beard_loc')

    hairRig.rigRoot(tmpJnt=['beardRoot_jnt'])
    hairRig.rig(
        parent='Rig:jaw1Lwr_jnt',
        parentSpine='Rig:neck1_jnt',
        elem='',
        animGrp='',
        stillGrp='',
        tmpJnt=[
            'beardA01_jnt',
            'beardB02_jnt',
            'beardC03_jnt',
            'beardD04_jnt',
            'beardE05_jnt'

        ])



def eyeRig:

#-------------------------------------------------------- eye base ----------------------
# Left iris
    lIrisRig = phead.IrisRig(
                                parent=headRig.eyeLFT_jnt ,
                                eyeGmbl=headRig.eyeGmblLFT_ctrl ,
                                charSize=size ,
                                tmpJnt='irisLFT_tmpJnt'
                            )

    rigTools.nodeNaming(
                            lIrisRig ,
                            charName = '' ,
                            elem = '' ,
                            side = 'LFT'
                        )
    rIrisRig = phead.IrisRig(
                                parent=headRig.eyeRGT_jnt ,
                                eyeGmbl=headRig.eyeGmblRGT_ctrl ,
                                charSize=size ,
                                tmpJnt='irisRGT_tmpJnt'
                            )

    rigTools.nodeNaming(
                            rIrisRig ,
                            charName = '' ,
                            elem = '' ,
                            side = 'RGT'
                        )

    # Left Eye Spec
    lEyeSpecRig = phead.EyeSpecRig(
                                        parent=headRig.eyeLFT_jnt ,
                                        worldSpace = headRig.head1_jnt ,
                                        eyeGmbl=headRig.eyeGmblLFT_ctrl ,
                                        charSize=size ,
                                        tmpJnt='eyeSpecLFT_tmpJnt'
                                    )

    rigTools.nodeNaming(
                            lEyeSpecRig ,
                            charName = '' ,
                            elem = '' ,
                            side = 'LFT'
                        )

    # Right Eye Spec
    REyeSpecRig = phead.EyeSpecRig(
                                        parent=headRig.eyeRGT_jnt ,
                                        worldSpace = headRig.head1_jnt ,
                                        eyeGmbl=headRig.eyeGmblRGT_ctrl ,
                                        charSize=size ,
                                        tmpJnt='eyeSpecRGT_tmpJnt'
                                    )

    rigTools.nodeNaming(
                            REyeSpecRig ,
                            charName = '' ,
                            elem = '' ,
                            side = 'RGT'
                        )



def runGlobalPublishAndConnectedSkel:


#----------------------------------------- run global publish and run connected the skeleton ------------
    from nuTools.pipeline import pipeTools
    reload( pipeTools )
    from tool.rig.nnTools import nnTools as nn
    reload(nn)

    #--- Pipeline publish
    pipeTools.importAllRefs()
    pipeTools.removeAllNameSpace()
    pipeTools.deleteAllTurtleNodes()
    pipeTools.deleteExtraDefaultRenderLayer()
    pipeTools.deleteUnusedNodes()
    pipeTools.parentPreConsObj()

    pipeTools.connectDualSkeleton(True, False)
    nn.turnOffScale()
    #-----------------connect at Rig-------------------
    from nuTools.pipeline import pipeTools
    reload(pipeTools)
    pipeTools.connectProxyCtrl(True)  # connect eyeLid to Control @ Anim

    ## ------------------------------ clen all node none used
    from nuTools.pipeline import fix
    node = fix.cleanUnusedDGs()
    print len( node )
    pm.delete( node )

    #attach geometry
    misc.attachToGeom(objs=[], mode='follicle', attachMethod='parent')

    #follicle and Rivet
    misc.attachToGeom(objs=[], mode='follicle', attachMethod='parent')





def blendshape:

# ----------------------------- blendshape run -----------------------------------
    from nuTools.util import bshUtil
    reload( bshUtil )

    bshUtil.inverseBlendShapeWeight(blendShapeNode='deform_bsn', index=None, geoIndex=0)
    reload(bsu)
    #--- select  skinMesh, jointInner, jointMid, jointOuter, jointRoot

    print mc.ls( sl = True )


    #--- copy the result from print command and replace in the brackets below
    head = ['MESHORGRP','ebSepIn_jnt','ebSepMid_jnt','ebSepOut_jnt','ebSepRoot_jnt' ]
    eb = ['MESHORGRP','ebSepIn_jnt','ebSepMid_jnt','ebSepOut_jnt','ebSepRoot_jnt' ]
    mouth = ['MESHORGRP','lipIN','lipMD','lipOT','lipSepRoot' ]


    #--- specific blendshape node name
    bshNodeName = 'ebSep_bsn'
    # geoIndex is number of mesh

    mc.select( head )
    weights = bsu.getNormalizeSkinClusterWeights()
    bsu.setBlendShapeWeight(weight=weights[0], blendShapeNode=bshNodeName, index=0, geoIndex=0)
    bsu.setBlendShapeWeight(weight=weights[1], blendShapeNode=bshNodeName, index=1, geoIndex=0)
    bsu.setBlendShapeWeight(weight=weights[2], blendShapeNode=bshNodeName, index=2, geoIndex=0)
    bsu.setBlendShapeWeight(weight=weights[0], blendShapeNode=bshNodeName, index=3, geoIndex=0)
    bsu.setBlendShapeWeight(weight=weights[1], blendShapeNode=bshNodeName, index=4, geoIndex=0)
    bsu.setBlendShapeWeight(weight=weights[2], blendShapeNode=bshNodeName, index=5, geoIndex=0)

    mc.select( eb )
    weights2 = bsu.getNormalizeSkinClusterWeights()
    bsu.setBlendShapeWeight(weight=weights2[0], blendShapeNode=bshNodeName, index=0, geoIndex=1)
    bsu.setBlendShapeWeight(weight=weights2[1], blendShapeNode=bshNodeName, index=1, geoIndex=1)
    bsu.setBlendShapeWeight(weight=weights2[2], blendShapeNode=bshNodeName, index=2, geoIndex=1)
    bsu.setBlendShapeWeight(weight=weights2[0], blendShapeNode=bshNodeName, index=3, geoIndex=1)
    bsu.setBlendShapeWeight(weight=weights2[1], blendShapeNode=bshNodeName, index=4, geoIndex=1)
    bsu.setBlendShapeWeight(weight=weights2[2], blendShapeNode=bshNodeName, index=5, geoIndex=1)


    mc.select( mouth )
    weights = bsu.getNormalizeSkinClusterWeights()
    bsu.setBlendShapeWeight(weight=weights[0], blendShapeNode=bshNodeName, index=0, geoIndex=0)
    bsu.setBlendShapeWeight(weight=weights[1], blendShapeNode=bshNodeName, index=1, geoIndex=0)
    bsu.setBlendShapeWeight(weight=weights[2], blendShapeNode=bshNodeName, index=2, geoIndex=0)
    bsu.setBlendShapeWeight(weight=weights[0], blendShapeNode=bshNodeName, index=3, geoIndex=0)
    bsu.setBlendShapeWeight(weight=weights[1], blendShapeNode=bshNodeName, index=4, geoIndex=0)
    bsu.setBlendShapeWeight(weight=weights[2], blendShapeNode=bshNodeName, index=5, geoIndex=0)
    bsu.setBlendShapeWeight(weight=weights[0], blendShapeNode=bshNodeName, index=6, geoIndex=0)
    bsu.setBlendShapeWeight(weight=weights[1], blendShapeNode=bshNodeName, index=7, geoIndex=0)
    bsu.setBlendShapeWeight(weight=weights[2], blendShapeNode=bshNodeName, index=8, geoIndex=0)
    bsu.setBlendShapeWeight(weight=weights[0], blendShapeNode=bshNodeName, index=9, geoIndex=0)
    bsu.setBlendShapeWeight(weight=weights[1], blendShapeNode=bshNodeName, index=10, geoIndex=0)
    bsu.setBlendShapeWeight(weight=weights[2], blendShapeNode=bshNodeName, index=11, geoIndex=0)


    # ------------------- clear unused target -------------------------
    bsu.cleanUnusedBlendShapeTarget('facialBuffer_bsn')

    ## ------------------------------ run face curve base ------------------------
    from nuTools.rigTools import faceCurveRig as fcr

    reload(fcr)
    # from top to bottom
    # head, eyebrow, eyelashes, eyeball, cheekUpr, mouth&cheeks
    fcrObj = fcr.FaceCurveRig(headJnt='headBshRig_jnt',
                              headGeo='bodyBshRig_ply',
                              eyebrowCrv='eb_crv',
                              eyebrowGeo='eyebrowBshRig_ply',
                              eyebrowPatch='eyebrowPatchFaceRig_ply',
                              eyelashCrvs=['eyelash_crv'],
                              eyelashGeos=['eyelashBase_ply'],
                              eyeballTmpLoc='eyeBallTmpLFT_loc',
                              cheekUprCrv='cheekUpr_crv',
                              cheekCrv='cheek_crv',
                              lipUprCrv='lipUpr_crv',
                              lipLwrCrv='lipLwr_crv',
                              size=0.1)
    fcrObj.rig()

def wrapObject :
    # select A then B, and run this script to wrap A with offset node and move to B
    # Untitled
    import maya.cmds as cmds
    ​
    ctrl_select = cmds.ls(sl=True)
    ​
    grp = cmds.group(empty=True,n="{0}_offset".format(ctrl_select[0]))
    ctrl_select_parent = cmds.listRelatives(ctrl_select[0], p=True)
    cmds.parent(grp, ctrl_select_parent, relative=True)
    cmds.parent(ctrl_select[0], grp, relative=True)
    cmds.parentConstraint(ctrl_select[1],grp, maintainOffset=False)
    cmds.select(clear=True)
    cmds.select(grp)
    cmds.delete(constraints=True)
    ​
    print("constraint : {0} >> {1}".format(grp, ctrl_select[1]))

# To delete all reference nodes, just add them to layer "DELETE" and run this script.
# deleteAllRefsByLayerName
def deleteLayer :
    from teeTools import teeUtilFunc as tuf
    reload(tuf)
    ​
    tuf.deleteAllRefsByLayerName('DELETE')
def BPM:

    from nuTools.rigTools import bpmRig as br

    reload(br)

    # --- FK, must run 1 FK chain at a time
    jnts = ['shirt01A01_jnt', 'shirt01A02_jnt', 'shirt01A03_jnt']
    parent = 'anim_grp'
    inputGeom = 'shirt01BpmInput_ply'
    skc = 'skinCluster114'
    rootJnt = 'shirt01BpmHolder_jnt'

    nameSplits = misc.nameSplit(jnts[0])
    brObj = br.BpmFkRig(jnts=jnts,
                        parent=parent,
                        rootJnt=rootJnt,
                        inputGeometry=inputGeom,
                        skinCluster=skc,
                        elem=nameSplits['elem'],
                        side=nameSplits['pos'],
                        size=0.2)

    # --- IK, can run on multiple joints
    jnts = ['shirtColler01A01_jnt', 'shirtColler01A02_jnt', 'shirtColler01A03_jnt', 'shirtColler01A04_jnt',
            'shirtColler01A05_jnt', ]
    parent = 'anim_grp'
    inputGeom = 'shirt01BpmInput_ply'
    skc = 'skinCluster82'
    rootJnt = 'shirt01BpmHolder_jnt'

    nameSplits = misc.nameSplit(jnts[0])
    brObj = br.BpmIkRig(jnts=jnts,
                        parent=parent,
                        rootJnt=rootJnt,
                        inputGeometry=inputGeom,
                        skinCluster=skc,
                        elem='coller',
                        side='',
                        size=0.2)

    brObj.rig()


def bindButton:
    # select all the buttons
    import pymel.core as pm
    buttons = pm.selected()

    # select all joints
    jnts = pm.selected()

    # select the jacket
    jacket = pm.selected()[0]

    # batch attach follicles and bind skin
    for button, jnt in zip(buttons, jnts):
        pm.select(jacket, jnt)
        fol = misc.createFollicleFromPosition_Mesh(attachMethod='parent')

        pm.skinCluster(jnt, button)

    from nuTools import misc
    reload(misc)
    misc.createRivetFromPosition_Mesh()

    ##############################

def poleVectorPosition():
    ######pole vector

    misc.getPoleVectorPosition(createLoc=True, offset=5)

def nonRollSkirt():
    import pkmel.aimRig as aimRig
    reload(aimRig)

    nnRlRigGRP = mc.group(em=True, n='nnRlRig_grp')
    nnRlJntGRP = mc.group(em=True, n='nnRlJnt_grp')

    a = aimRig.NonRollRig2(
        parent='Rig:spine1_jnt',
        animGrp=nnRlRigGRP,
        rootJnt='upLegNnRlLFT_jnt',
        endJnt='lowLegNnRlLFT_jnt',
        parentRoot='Rig:upLegProxySkinLFT_jnt',
        parentEnd='Rig:lowLegProxySkinLFT_jnt',
        name='skirt',
        side='LFT',
        aimAx='y+',
        upAx='x-'
    )

    b = aimRig.NonRollRig2(
        parent='Rig:spine1_jnt',
        animGrp=nnRlRigGRP,
        rootJnt='upLegNnRlRGT_jnt',
        endJnt='lowLegNnRlRGT_jnt',
        parentRoot='Rig:upLegProxySkinRGT_jnt',
        parentEnd='Rig:lowLegProxySkinRGT_jnt',
        name='skirt',
        side='RGT',
        aimAx='y+',
        upAx='x-'
    )

    c = aimRig.NonRollRig2(
        parent='upLegNnRlLFT_jnt',
        animGrp=nnRlRigGRP,
        rootJnt='lowLegNnRlLFT_jnt',
        endJnt='ankleNnRlLFT_jnt',
        parentRoot='Rig:legRbnLFT_ctrl',
        parentEnd='Rig:ankleProxySkinLFT_jnt',
        name='skirtLow',
        side='LFT',
        aimAx='y+',
        upAx='x-'
    )

    d = aimRig.NonRollRig2(
        parent='upLegNnRlRGT_jnt',
        animGrp=nnRlRigGRP,
        rootJnt='lowLegNnRlRGT_jnt',
        endJnt='ankleNnRlRGT_jnt',
        parentRoot='Rig:legRbnRGT_ctrl',
        parentEnd='Rig:ankleProxySkinRGT_jnt',
        name='skirtLow',
        side='RGT',
        aimAx='y+',
        upAx='x-'
    )

    mc.parent('upLegNnRlLFT_jnt', 'upLegNnRlRGT_jnt', nnRlJntGRP)


def createCtrlRig:

    # ----------- Create CTRL RIG ---------------------
    sys.path.append(r'P:\Lego_FRD\asset\3D\base\body\frd_dean\rig\rig_master\data')
    import frd_dean as sd
    reload(sd)

    # ---- to get Ctrl
    from tool.rig.nnTools import nnTools as nn
    reload(nn)
    nn.readShapeController()

    # ---------------- SNAP JOINT To CTRL--------------
    from nuTools import misc
    reload(misc)

    misc.turnOffScaleCompensate()

def snapSkeleton():

    misc.snapSkeleton(namespace='frd_jame_rig_ctrlRig:')

    from nuTools.pipeline import pipeTools
    reload(pipeTools)

    # --- Pipeline publish
    pipeTools.importAllRefs()
    pipeTools.removeAllNameSpace()
    pipeTools.deleteAllTurtleNodes()
    pipeTools.deleteExtraDefaultRenderLayer()
    pipeTools.deleteUnusedNodes()
    pipeTools.parentPreConsObj()

def connectSkeleton():
    pipeTools.connectDualSkeleton(False, False)

    #---- TURN OFF SCALE COMPENSATE ------
    from nnTools import nnTools as nn
    nn.turnOffScale()

    ################
def ctrlexportImport():
    import pkmel.ctrlShapeTools as pct
    pct.readAllCtrl()

    import pkmel.ctrlShapeTools as pct
    pct.writeAllCtrl()

def nonRollArmOrLeg:
    # non roll script################

    import pkmel.aimRig as aimRig
    reload(aimRig)t

    legNnRlRigLFT = aimRig.NonRollRig2(
        parent='pelvisNnRlParent_jnt',
        animGrp='legNnRlRig_grp',
        rootJnt='upLegNnRlLFT_jnt',
        endJnt='lowLegNnRlLFT_jnt',
        parentRoot='upLegNnRlParentLFT_jnt',
        parentEnd='lowLegNnRlParentLFT_jnt',
        name='upLeg',
        side='LFT',
        aimAx='y+',
        upAx='x-')

    legNnRlRigRGT = aimRig.NonRollRig2(
        parent='pelvisNnRlParent_jnt',
        animGrp='legNnRlRig_grp',
        rootJnt='upLegNnRlRGT_jnt',
        endJnt='lowLegNnRlRGT_jnt',
        parentRoot='upLegNnRlParentRGT_jnt',
        parentEnd='lowLegNnRlParentRGT_jnt',
        name='upLeg',
        side='RGT',
        aimAx='y+',
        upAx='x-')

    brObj = br.BpmRig(skinCluster='skinCluster112', inputGeometry='bodyInput_ply')
    brObj.changeSkinCluster('MERGED__skinCluster113')
    brObj.changeInputGeom('body_ply', orig=False)

def cleanUpFile:
    ref = mc.ls(type='reference')
    print ref
    mc.delete(ref)

    we.cleanUpMesh('andreaBeachWearGeo_grp')

    ## --------------- CLEAN UP FILES ---------------- ##
    filePath = r'C:/Users/nun/WORK/LIB/HAIR/ADTFMD/RIGGING/RIG_LIB_HAIR_ADTFMD_LONG_PONYTAIL_C.ma'
    import sys
    if not 'M:\SCRIPTS\MEME\memeXplorer\sanitizer' in sys.path:
        sys.path.append('M:\SCRIPTS\MEME\memeXplorer\sanitizer')
    import os
    import maya.cmds as mc
    inFile = filePath
    outFile = filePath
    from sanitizer import sanitizeFile as sf
    reload(sf)
    sf.sanitizeFile(inFile, outFile, ref=False)
    if not os.path.exists(outFile):
        mc.file(inFile, f=True, o=True)
    else:
        mc.file(outFile, f=True, o=True)

    
def replacingGeo:
    # from nuTools.util import geoReplacer3_4 as gr
    # reload(gr)
    #
    # geoReplacerObject = gr.GeoReplacer()
    # geoReplacerObject.UI()

    from nuTools.util import geoReplacer3_4
    reload(geoReplacer3_4)

    geoReplacerObject = geoReplacer3_4.GeoReplacer()
    geoReplacerObject.UI()

def ribbonRig:
    # ---------------------- ribbonRig ----------------------

    from nuTools.rigTools import ribbonRig as rbr
    reload(rbr)

    strapAnimGrp = 'strapAnim_grp'
    strapUtilGrp = 'strapUtil_grp'
    strapStillGrp = 'strapStill_grp'

    baseJnt = 'ropeA_jnt'
    tipJnt = 'ropeB_jnt'

    # front
    strapRig = rbr.RibbonIkRig(numJnt=5,
                              aimAxis='+y',
                              upAxis='+x',
                              elem='strap',
                              side='RGT',
                              parent=baseJnt,
                              animGrp=strapAnimGrp,
                              utilGrp=strapUtilGrp,
                              stillGrp=strapStillGrp)

    strapRig.rig()
    strapRig.attach(base = baseJnt,
                  tip  = tipJnt,
                  baseParent = baseJnt,

              tipTwistParent=tipJnt,
              twistFromBase=False,
              upAxis='+x',
              parentUpAxis='+x')



def exportImportSkin:
    from pkmel import weightTools as pwt
    reload(pwt)

    pwt.readWeight2( geo = '' , fn = '' , searchFor='' , replaceWith='' , prefix='' , suffix='' )

    pwt.readSelectedWeight2( weightFolderPath='' , searchFor='' , replaceWith='' , prefix='' , suffix='' )



    skinGrp = pm.PyNode('skin_grp')
    child = pm.list_relatives(skinGrp, ad=True, typ='transform')
    for i in ( c for c in child if '_grp' in c.nodeName() ) :
       pm.delete(i)

def follicleAndRivet:
    ## ------------------------------ rivet

    from nuTools import misc
    reload(misc)
    misc.createRivetFromPosition_Mesh()

def connectEyeProxyRig():
    # -----------------connect at Rig-------------------
    from nuTools.pipeline import pipeTools
    reload(pipeTools)
    pipeTools.connectProxyCtrl(True)  # connect eyeLid to Control @ Anim



def text:
    ######################### f text ###################
    nn.createText()