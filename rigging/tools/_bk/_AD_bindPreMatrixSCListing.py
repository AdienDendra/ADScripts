import AD_utils as ut
import _AD_controllerV02 as ad
import maya.cmds as mc

reload(ad)
reload(ut)

#select constrained then geo


def connectFollicleRot(follicleNode, follicleTransf):
    conn = mc.connectAttr(follicleNode + '.outRotate', follicleTransf + '.rotate')
    return conn


def connectFollicleTrans(follicleNode, follicleTransf):
    conn = mc.connectAttr(follicleNode + '.outTranslate', follicleTransf + '.translate')
    return conn


def dicConnectFol(connect,follicleNode, follicleTransf):
        dic = {'rotateConn': connectFollicleRot,
               'transConn': connectFollicleTrans,
               }
        for con in connect:
            if con in dic.keys():
                dic[con](follicleNode, follicleTransf)
            else:
                return mc.warning("Your %s key name is wrong. Please check on the key list connection!" % con)
        return dic


def createFollicle(objSel, objMesh, conectFoll=['']):

    closestNode = mc.createNode('closestPointOnMesh')

    # connect attr mesh with node
    mc.connectAttr(objMesh + '.outMesh', closestNode + '.inMesh')

    # query locator position
    xform = mc.xform(objSel, ws=True, t=True, q=True)

    # set the position of node according to the loc
    mc.setAttr(closestNode + '.inPositionX', xform[0])
    mc.setAttr(closestNode + '.inPositionY', xform[1])
    mc.setAttr(closestNode + '.inPositionZ', xform[2])

    # create follicle
    follicleNode = mc.createNode('follicle')


    # query the transform follicle
    follicleTransform = mc.listRelatives(follicleNode, type='transform', p=True)


    # connecting the shape follicle to transform follicle
    dicConnectFol(conectFoll, follicleNode, follicleTransform[0])


    # connect the world matrix mesh to the follicle shape
    mc.connectAttr(objMesh+ '.worldMatrix', follicleNode + '.inputWorldMatrix')

    # connect the output mesh of mesh to input mesh follicle
    mc.connectAttr(objMesh + '.outMesh', follicleNode + '.inputMesh')

    # turn off the simulation follicle
    mc.setAttr(follicleNode + '.simulationMethod', 0)

    # get u and v output closest point on mesh node
    parU = mc.getAttr(closestNode + '.result.parameterU')
    parV = mc.getAttr(closestNode + '.result.parameterV')

    # connect output closest point on mesh node to follicle
    mc.setAttr(follicleNode + '.parameterU', parU)
    mc.setAttr(follicleNode + '.parameterV', parV)

    # parent constraint locator to follicle
    #mc.parent(follicleTransform[0], objLoc, mo=1)

    #rename follicle
    rename = mc.rename(follicleTransform, '%s_%s' % (ut.ad_main_name(objSel), 'fol'))

    mc.delete(closestNode)

    return rename

def snapLocator(obj):
    for i in obj:
        mc.select(cl=1)
        loc = mc.spaceLocator()
        cls = mc.cluster(i)
        mc.parentConstraint(cls, loc, mo=0)
        mc.delete(cls)
    return obj

def snapJoint(obj):
    for i in obj:
        mc.select(cl=1)
        loc = mc.joint()
        cls = mc.cluster(i)
        mc.parentConstraint(cls, loc, mo=0)
        mc.delete(cls)
    return obj

def locator(obj):
    mc.select(cl=1)
    loc = mc.spaceLocator()
    rnm = mc.rename(loc, '%s_%s' % (ut.ad_main_name(obj), 'loc'))
    cls = mc.cluster(obj)
    mc.parentConstraint(cls, rnm, mo=0)
    mc.delete(cls)
    return obj

def joint(obj):
    mc.select(cl=1)
    jnt = mc.joint()
    rnm = mc.rename(jnt, '%s_%s' % (ut.ad_main_name(obj), 'jnt'))
    cls = mc.cluster(obj)
    mc.parentConstraint(cls, rnm, mo=0)
    mc.delete(cls)
    return obj

def connectMesh(objOri, objTgt):
    objShape = mc.listRelatives(objOri, s=1)[0]
    objTgtShape = mc.listRelatives(objTgt, s=1)[-1]
    cnntMesh = mc.connectAttr ('%s.outMesh' % (objShape), '%s.inMesh' % (objTgtShape))
    return cnntMesh


def follicleSet(obj, mesh, connect):
    grps = []
    grps.append(createFollicle (obj, mesh, connect))
    return grps

def querySkinName(obj):
    # get the skincluster name
    relatives = mc.listRelatives(obj, type = "shape")
    sCluster = mc.listConnections(relatives, type = "skinCluster")
    if sCluster == None:
        return mc.error("Please add your skin cluster before run the script!")
    else:
        return sCluster

def groupNull(name):
    mc.createNode('transform', name=name)
    return name


def groupFK(obj):
    for i in obj:
        splitName = i.split('|')[0]
        grpParent = ut.group_parent(['ParentPos', 'PosSDK'], ut.ad_main_name(i), '')
        ut.match_position(splitName, grpParent[0])
        return grpParent


def createCtrl(obj):
        ctrl = ad.create_controller (select=obj,
                                     groups_ctrl=['Zro', 'BPM'],
                                     ctrl_color='lightPink',
                                     shape=ad.JOINT,
                                     ctrl_size=0.1,
                                     connection=['parent'],
                                     groupsObjectSel=['Offset'],
                                     lock_channels=[]
                                     )
        return ctrl


def listMatrixConnection(obj):
    list = mc.listConnections(obj[0] +'.matrix', s=True)
    return list

def listFolderBPMConnection(obj):
    objs = []
    for i in obj:
        objs.append(mc.listConnections(i, d=True))
    return objs

def arrayBPMFolder(obj):
    relatives = mc.listRelatives(obj, p=True, f=True)
    objs = []
    for o in relatives:
        objs.append(o.split('|')[-2])
    return objs

def listRelatives(obj):
    grps = []
    for o in obj:
        lR = grps.append(mc.listRelatives(o, ap=True))
    return grps

def addingGrpNotNoneListRelatives(obj):
        grps= groupFK(obj)
        return grps

def createBPM(joints =[],
              mainMesh ='',
              meshBPM ='',
              baseJoint = [],
              connectMesh=[]
              ):

############################### create bpm by listing of skinCluster / cannot add the joint ############################################

#create control from the joint list

#setup attribute

#create grp module joint

#query connection source (joint) of skin cluster corresponding on matrix number

#array BPM folder from the joint (source connection)

#enumerate all of the bpm grp to bind pre matrix regarding on enumerate number


    bpmGrp = groupNull('bpmGrp')

    folGrp = groupNull('ctrlGrp')

    mc.parent(folGrp, bpmGrp)


    mc.setAttr(mainMesh+'.visibility', 0)


    for obj in joints:

        ctrlN = createCtrl(obj)

        follicles = follicleSet(obj, mainMesh, connectMesh)

        a = mc.parent(ctrlN[0], follicles)


        mc.parent(follicles, folGrp)


        follicleShape = mc.listRelatives(follicles, s=True)

        mc.setAttr(follicleShape[0] + '.lodVisibility', 0)

        mc.setAttr(obj + '.visibility', 0)


        ut.lock_hide_attr(['t', 'r', 's'], follicles[0])

        #ut.lockAttr(['t','r','s'], obj)

        ut.lock_hide_attr_object(follicles[0], 'v')

        ut.lock_hide_attr_object(follicleShape[0], 'pu')

        ut.lock_hide_attr_object(follicleShape[0], 'pv')

        ut.lock_attr(['t', 'r', 's'], ctrlN[0])

        ut.lock_attr(['t', 'r', 's'], ctrlN[1])



    for objB in baseJoint:
        grp = ut.ad_group_object(['Zro', 'BPM', 'Null'], objB)
        mc.parent(grp[0], bpmGrp)
        #ut.lockAttr(['t','r','s'], objB)


    lisConn = listMatrixConnection(querySkinName(meshBPM))

    arBPM = arrayBPMFolder(lisConn)

    for indexJoint, item in enumerate(arBPM):

           mc.connectAttr('%s.worldInverseMatrix[0]' % item, '%s.bindPreMatrix[%d]' % (querySkinName(meshBPM)[0], indexJoint))

