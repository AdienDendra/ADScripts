import AD_controllers as ac
import AD_utils as au
import maya.cmds as mc

reload(ac)
reload(au)

#select constrained then geo

############################################## tools BPM ###############################################

def createCtrl(obj):
    ctrl = ac.ad_create_controller(select=obj,
                                   groups_ctrl=['Zro', 'BPM', 'Adjust'],
                                   ctrl_color='lightPink',
                                   shape=ac.JOINT,
                                   ctrl_size=0.4,
                                   connection=['parent'],
                                   group_connect_attr=['Offset'],
                                   lock_channels=[]
                                   )
    return ctrl


# listing the joint connection destination to skin cluster matrix
def jointDestinationMatrix(obj):
    lC = mc.listConnections(obj+'.worldMatrix[0]', p=True)
    return lC

#get the number of skin cluster matrix
def skinMatrixListFromJoint(obj):
    for item in jointDestinationMatrix(obj):
        split  = item.split('.')[1:]
        integer   = int((split[0].split('[')[-1][:-1]))
        return integer


def arrayBPMFolder(obj):
    relatives = mc.listRelatives(obj, p=True, f=True)
    for o in relatives:
        split = o.split('|')[-3]
        return split


############################### create bpm by listing of the source of skinCluster ############################################

def createBPM(joints=[],
              mainMesh='',
              meshBPM='',
              baseJoint=[],
              scaleObj =[],
              connectMesh=[]
              ):

    # create control from the joint list

# setup attribute

# create grp module joint

# look up the connection matrix skin cluster from the joint

# slicing to get number from the matrix long name and convert to integer

# look up the BPM folder from the joint parent

# connect bpm folder to bind pre matrix skin cluster regarding number that had been sliced


    #bpmGrp = groupNull('bpmGrp')

    #folGrp = groupNull('ctrlGrp')

    #mc.parent(folGrp, bpmGrp)


    mc.setAttr(mainMesh+'.visibility', 0)


    for obj in joints:

        ctrlN = createCtrl(obj)

        follicles = au.ad_follicle_set(obj, mainMesh, connectMesh)

        mc.parent(ctrlN[0], follicles)


        #mc.parent(follicles, folGrp)

        for scl in scaleObj:

            mc.scaleConstraint(scl, follicles[0])

        follicleShape = mc.listRelatives(follicles, s=True)

        mc.setAttr(follicleShape[0] + '.lodVisibility', 0)

        mc.setAttr(obj + '.drawStyle', 2)


        au.lock_hide_attr(['t', 'r', 's'], follicles[0])

        #au.lockAttr(['t','r','s'], obj)

        au.lock_hide_attr_object(follicles[0], 'v')

        au.lock_hide_attr_object(follicleShape[0], 'pu')

        au.lock_hide_attr_object(follicleShape[0], 'pv')

        au.lock_attr(['t', 'r', 's'], ctrlN[0])

        au.lock_attr(['t', 'r', 's'], ctrlN[1])

        mc.connectAttr('%s.worldInverseMatrix[0]' % arrayBPMFolder(obj),
        '%s.bindPreMatrix[%d]' % (au.ad_query_skin_name(meshBPM), skinMatrixListFromJoint(obj)))

    for objB in baseJoint:
        lR = mc.listRelatives(objB, p=True)
        if lR == None:
            au.ad_group_object(['Zro', 'BPM', 'Null', 'Adjust'], objB)
            #mc.parent(grp[0], bpmGrp)
            au.lock_attr(['t', 'r', 's'], objB)
            # partObj = arrayPartObject(joints, lisConn)
            mc.connectAttr('%s.worldInverseMatrix[0]' % arrayBPMFolder(objB),
                           '%s.bindPreMatrix[%d]' % (au.ad_query_skin_name(meshBPM), skinMatrixListFromJoint(objB)))
        else:
            return


#################################################### FK BPM ############################################

def createBPMFK(joints=[],
          mainMesh='',
          meshBPM='',
          baseJoint=[],
          scaleObj=[],
          connectMesh=[]
          ):

    createGrp = au.ad_group_object_outside('FolFK', joints)

    fol = []
    ctrls = []

    for obj in joints:
        ctrlN = createCtrl(obj)[:1]
        print ctrlN

        ctrls.append(ctrlN[0])

        print ctrls

        follicles = au.ad_follicle_set(obj, mainMesh, connectMesh)

        fol.append(follicles)

        """mc.connectAttr('%s.worldInverseMatrix[0]' % arrayBPMFolder(obj),
                       '%s.bindPreMatrix[%d]' % (au.querySkinName(meshBPM), skinMatrixListFromJoint(obj)))

        for scl in scaleObj:
            mc.scaleConstraint(scl, follicles[0])

        for scl in scaleObj:

            mc.scaleConstraint(scl, follicles[0])

        follicleShape = mc.listRelatives(follicles, s=True)

        mc.setAttr(follicleShape[0] + '.lodVisibility', 0)

        mc.setAttr(obj + '.drawStyle', 2)


        au.lockHideAttr(['t','r','s'], follicles[0])

        #au.lockAttr(['t','r','s'], obj)

        au.lockHideAttrObj(follicles[0], 'v')

        au.lockHideAttrObj(follicleShape[0], 'pu')

        au.lockHideAttrObj(follicleShape[0], 'pv')

        #au.lockAttr(['t','r','s'], ctrlN[0])

        #au.lockAttr(['t','r','s'], ctrlN[1])

    for i, item in enumerate(fol):
        mc.parentConstraint(item, createGrp[i], mo=1)

    for i, item in enumerate(createGrp):
        au.connectAttrObject(item, ctrls[i])


    for objB in baseJoint:
        lR = mc.listRelatives(objB, p=True)
        if lR == None:
            au.groupObject(['Zro', 'BPM', 'Null','Adjust'], objB)
            #mc.parent(grp[0], bpmGrp)
            au.lockAttr(['t','r','s'], objB)
            # partObj = arrayPartObject(joints, lisConn)
            mc.connectAttr('%s.worldInverseMatrix[0]' % arrayBPMFolder(objB),
                           '%s.bindPreMatrix[%d]' % (au.querySkinName(meshBPM), skinMatrixListFromJoint(objB)))
        else:
            return"""


################################################# re-skin the mesh ###################################################
def reskinMeshBPM (joints=[],
              meshBPM='',
              baseJoint=[],
                ):

    for obj in joints:

        mc.connectAttr('%s.worldInverseMatrix[0]' % arrayBPMFolder(obj),
                    '%s.bindPreMatrix[%d]' % (au.ad_query_skin_name(meshBPM), skinMatrixListFromJoint(obj)))

    for objB in baseJoint:
        lR = mc.listRelatives(objB, f=1, ap=1)[0]

        mc.connectAttr('%s.worldInverseMatrix[0]' % arrayBPMFolder(objB),
                       '%s.bindPreMatrix[%d]' % (au.ad_query_skin_name(meshBPM), skinMatrixListFromJoint(objB)))





####################################### sorting the skin matrix index (not used) ##############################################################


#remove the long name form matrix long name listing of skin cluster
def skinMatrixList(obj):
    objs =[]
    for o in skinMatrixListLong(obj):
        objs.append(int(o))
    return objs

#getting attribute matrix long name from listing of skin cluster
def skinMatrixListLong(obj):
    for i in obj:
        getAttr = mc.getAttr(i + '.matrix', mi=True)
        return getAttr

#getting complete name skin cluster matrix include the number
def skinClusterMatrixListNum(obj):
    listMtx = []
    for cluster in obj:
        for indexNum in skinMatrixList(obj):
                at = cluster+'.matrix[%d]' % (int(indexNum))
                listMtx.append(at)
    return listMtx

#getting the source connection from the skin cluster matrix
def sourceJointSkinMatrix(obj):
      list = mc.listConnections(skinClusterMatrixListNum(obj),  d=True)
      print list
      return  list


############################################# misc (not used) ##################################################


def groupFK(obj):
    for i in obj:
        splitName = i.split('|')[0]
        grpParent = au.group_parent(['ParentPos', 'PosSDK'], au.ad_prefix_name(i), '')
        au.match_position(splitName, grpParent[0])
        return grpParent

def listMatrixConnection(obj):
    list = mc.listConnections(obj[0] +'.matrix', s=True)
    return list

def listFolderBPMConnection(obj):
    objs = []
    for i in obj:
        objs.append(mc.listConnections(i, d=True))
    return objs


def listRelatives(obj):
    grps = []
    for o in obj:
        lR = grps.append(mc.listRelatives(o, ap=True))
    return grps

def addingGrpNotNoneListRelatives(obj):
        grps= groupFK(obj)
        return grps

def arrayPartObject(joints, listObj):
    grps=[]
    for obj in joints:
        if obj in listObj:
            grps.append(obj)
    return grps


##########################################################################################################

