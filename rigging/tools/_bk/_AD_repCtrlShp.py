import AD_utils as ut
import maya.cmds as mc


def controlShapeQuery(obj):
    for s in obj:
        shapeNode = mc.listRelatives(s, s=True)[0]
        return shapeNode

def controlShapeCreate(obj):
    ctrl = ut.controller(obj)
    return  ctrl

def listAttrUserDefined(obj):
    lA = mc.listAttr(obj, ud=True)
    print lA
    return lA

def listType(obj):
    for i in obj:
        lA = mc.listAttr(i, ud=True)
        for o in lA:
            gA = mc.getAttr('%s.%s' % (obj[0], o), type=True)
            print gA
    return obj

def listType2(obj):
    gA = mc.getAttr('%s.%s' % (obj[0], listAttrUserDefined(obj)), type=True)
    return gA

def attrQuery(obj):
    aQ = mc.attributeQuery(listAttrUserDefined(obj), node=obj, k=True)
    return aQ

def attrQuery2(obj):
    for i in obj:
        for n in listAttrUserDefined(obj):
            aQ = mc.attributeQuery(n, node=i, k=True)
            print aQ
    return obj

def listConnectionSource(obj):
    lC = mc.listConnections('%s.%s' % (obj[0], listAttrUserDefined(obj)), d=False, c=True, p=True)
    return lC

def listConnectionSource2(obj):
    for i in listAttrUserDefined(obj):
        lC = mc.listConnections('%s.%s' % (obj[0], i), d=False, c=True, p=True)
        print lC
    return obj

def listConnectionDestination(obj):
    lC = mc.listConnections('%s.%s' % (obj[0], listAttrUserDefined(obj)), s=False, c=True, p=True)
    return lC

def listConnectionDestination2(obj):
    for i in listAttrUserDefined(obj):
        lC = mc.listConnections('%s.%s' % (obj[0], i), s=False, c=True, p=True)
        print lC
    return obj

def addAttrDic(obj):
    dic = {'longName': longName,
           'pointCons': pointCons,
           'orientCons': orientCons,
           'scaleCons': scaleCons,
           'parent': parentObj,
           'connectAttr' : connectAttrObject,
           }
    for con in connect:
        if con in dic.keys():
            dic[con](ctrl, obj)
        else:
           return mc.warning("Your %s key name is wrong. Please check on the key list connection!" % con)
    return dic


def createAttribute(objOld, objNew):
        oN = controlShapeCreate(objNew)
        aT = mc.addAttr(oN, ln=str(listAttrUserDefined(objOld)), at=str(listType(objOld)))
        mc.setAttr('%s.%s' % (oN, listAttrUserDefined(objOld)), e=True, k=True)
        return aT

def controlReplace (objOld, objNew):
    oO = controlShapeOld(objOld)
    oN = controlShapeNew(objNew)

    for o in objOld:
        ut.match_position(o, oN)
        ls = mc.listRelatives(oN, s=True)[0]
        par = mc.parent(ls, o, r=True, s=True)
        createAttribute(o, objNew)


        lsConn = mc.listConnections(oO, s=True, d= True, sh=True)
        print lsConn

        #mc.delete(oN)
        #mc.delete(oO)




    # get point position

    #print pointPos
