import AD_utils as au
import _AD_controllerV02 as ac
import maya.cmds as mc

reload(ac)
reload(au)

#select constrained then geo

############################################## tools BPM ###############################################

def createCtrl(obj):
    ctrl = ac.create_controller(select=obj,
                                groups_ctrl=['Zro', 'BPM'],
                                ctrl_color='lightPink',
                                shape=ac.JOINT,
                                ctrl_size=0.07,
                                connection=['parent'],
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
        intg   = int((split[0].split('[')[-1][:-1]))
        return intg


def arrayBPMFolder(obj):
    relatives = mc.listRelatives(obj, p=True, f=True)
    for o in relatives:
        split = o.split('|')[-2]
        return split

############################### create bpm by listing of the source of skinCluster ############################################

# create control from the joint list

# setup attribute

# create grp module joint

# look up the connection matrix skin cluster from the joint

# slicing to get number from the matrix long name and convert to integer

# look up the BPM folder from the joint parent

# connect bpm folder to bind pre matrix skin cluster regarding number that had been sliced
def listRelativesAllParent(obj):
    grps = []
    for i in obj:
       lR =  grps.append(mc.listRelatives(i, p=1))
    return grps

def createBPM(joints=[],
              mainMesh='',
              meshBPM='',
              baseJoint=[],
              connectMesh=[]
              ):

    #bpmGrp = groupNull('bpmGrp')

    #folGrp = groupNull('ctrlGrp')

    #mc.parent(folGrp, bpmGrp)

    mc.setAttr(mainMesh+'.visibility', 0)


    for obj in joints:

        lP = mc.listRelatives(obj, ad=1, p=1)

        if lP == None:

            ctrlN = createCtrl(obj)

            follicles = au.ad_follicle_set(obj, mainMesh, connectMesh)

            mc.parent(ctrlN[0], follicles)


            #mc.parent(follicles, folGrp)


            follicleShape = mc.listRelatives(follicles, s=True)

            mc.setAttr(follicleShape[0] + '.lodVisibility', 0)

            mc.setAttr(obj + '.visibility', 0)


            au.lock_hide_attr(['t', 'r', 's'], follicles[0])

            #au.lockAttr(['t','r','s'], obj)

            au.lock_hide_attr_object(follicles[0], 'v')

            au.lock_hide_attr_object(follicleShape[0], 'pu')

            au.lock_hide_attr_object(follicleShape[0], 'pv')

            au.lock_attr(['t', 'r', 's'], ctrlN[0])

            au.lock_attr(['t', 'r', 's'], ctrlN[1])

            mc.connectAttr('%s.worldInverseMatrix[0]' % arrayBPMFolder(obj),
            '%s.bindPreMatrix[%d]' % (au.ad_query_skin_name(meshBPM), skinMatrixListFromJoint(obj)))

        if lP != None:

            nullGrp = au.group_parent(['Zro'], '%s' % au.ad_lib_main_name(obj), 'Jnt')
    
            #ctrlN = createCtrl(obj)

            #follicles = au.follicleSet(obj, mainMesh, connectMesh)


   # mc.setAttr(mainMesh+'.visibility', 0)



        #else:

            #nullGrp = au.groupObjectOneParent(['Adien'], joints)

            #ctrlN = createCtrl(obj)


           # follicles = au.follicleSet(obj, mainMesh, connectMesh)

            #au.parentCons(follicles, nullGrp)

           # au.groupParent([], '%s' % ctrlN, 'helper')


    for objB in baseJoint:
        lR = mc.listRelatives(objB, p=True)
        if lR == None:
            au.ad_group_object(['Zro', 'BPM', 'Null'], objB)
            #mc.parent(grp[0], bpmGrp)
            au.lock_attr(['t', 'r', 's'], objB)
            # partObj = arrayPartObject(joints, lisConn)
            mc.connectAttr('%s.worldInverseMatrix[0]' % arrayBPMFolder(objB),
                           '%s.bindPreMatrix[%d]' % (au.ad_query_skin_name(meshBPM), skinMatrixListFromJoint(objB)))
        else:
            return


################################### sorting the skin matrix index (not used) ##############################################################

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
        grpParent = au.group_parent(['ParentPos', 'PosSDK'], au.ad_lib_main_name(i), '')
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

def addingJoint(joints=[],
                meshBPM ='',
                mainMesh = '',
                connectMesh =[]
                ):

    for obj in joints:

        ctrlN = createCtrl(obj)

        follicles = follicleSet(obj, mainMesh, connectMesh)

        mc.parent(ctrlN[0], follicles)


        #mc.parent(follicles, folGrp)


        follicleShape = mc.listRelatives(follicles, s=True)

        mc.setAttr(follicleShape[0] + '.lodVisibility', 0)

        mc.setAttr(obj + '.visibility', 0)


        au.lock_hide_attr(['t', 'r', 's'], follicles[0])

        #au.lockAttr(['t','r','s'], obj)

        au.lock_hide_attr_object(follicles[0], 'v')

        au.lock_hide_attr_object(follicleShape[0], 'pu')

        au.lock_hide_attr_object(follicleShape[0], 'pv')

        au.lock_attr(['t', 'r', 's'], ctrlN[0])

        au.lock_attr(['t', 'r', 's'], ctrlN[1])

    arBPM = arrayBPMFolder(joints)
    print arBPM

    numIndex = listingLongN(querySkinName(meshBPM))
    print numIndex

   # lC = mc.listConnections(arBPM, p=True ,d=True)

    for indexJoint, item in enumerate(arBPM):
        mc.connectAttr('%s.worldInverseMatrix[0]' % item,
                       '%s.bindPreMatrix[%d]' % (querySkinName(meshBPM)[0], numIndex[indexJoint]))

