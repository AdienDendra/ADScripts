import maya.cmds as mc
import rigLib.rig.body.spine as sp
from rigLib.utils import core as cr, controller as ct

from rigging.tools import AD_utils as au

reload(cr)
reload(ct)
reload(au)
reload(sp)

class RibbonSpine:
    def __init__(self,
                 parallelAxis ='y',
                 tipPos = '+',
                 listSpineJnt='',
                 pelvisCtrl='',
                 listSpineCtrlFK='',
                 listSpineCtrlIK='',
                 FKIKSwitch='',
                 animCtrl='',
                 grpJoints='',
                 grpJntSpine='',
                 ctrlMid = '',
                 ctrlDetails = ct.CIRCLEPLUS,
                 scale=None,
                 prefix='prefix',
                 numJoints=5):

        """
        :param parallelAxis  : str, two point parallel position direction whether on x or y or z axis
        :param tipPos    : str, position point (joint) of the tip regarding on the module joint whether on + or - axis
        :param prefix    : str, prefix name for ribbon
        :param numJoints : int, number of joint as well as the control of ribbon part
        """
        # Width plane variable (following the number of joints
        size = float(numJoints)


        # Tip point dictionary towards
        tipPoint = {'+': [(size / 2.0 * -1) * scale, (size / 2.0) * scale],
                    '-': [(size / 2.0) * scale, (size / 2.0 * -1) * scale]}

        if tipPos in tipPoint.keys():
            self.pos       = (0,0,0)
            self.upPoint   = tipPoint[tipPos][0]
            self.downPoint = tipPoint[tipPos][1]
        else:
            raise mc.error('The string %s in tipPos argument is not found. Fill with + or -' % tipPos)

        # Dictionary list
        tmpPlaneDic ={'x': [(0,1,0), size * scale, (1.0 / size), numJoints, 1],
                      'y': [(0,0,1), 1 * scale, size, 1, numJoints],
                      'z': [(0,1,0), 1 * scale, size, 1, numJoints]}

        direction = {'x': ['.rotateY', 90, '.translateZ'],
                     'y': ['.rotateZ', 90, '.translateX'],
                     'z': ['.rotateX', 0, '.translateX']}

        rotDefomer = {'x': (0, 0, 90),
                      'y': (0, 0, 180),
                      'z': (-90, 0, 90)}

        volInputMdn = {'x': ['.translateX','.input1Z', '.outputZ','.scaleY', '.scaleZ'],
                       'y': ['.translateY','.input1X', '.outputX', '.scaleX', '.scaleZ'],
                       'z': ['.translateZ','.input1X', '.outputX','.scaleX', '.scaleZ']}

        follicleVol ={'x': ('.parameterV', -1),
                      'y': ('.parameterU', 1),
                      'z': ('.parameterU', 1)}


    ### GROUPS AND SURFACES
        # Create the main groups
        self.grpAllRibbon    = mc.group(empty=True, name=(prefix + 'AllRibbon_grp'))
        self.grpCluster      = mc.duplicate(self.grpAllRibbon, name=(prefix + 'RbnCluster_grp'))
        self.grpSurface      = mc.duplicate(self.grpAllRibbon, name=(prefix + 'RbnRefSurface_grp'))
        self.grpDeformers    = mc.duplicate(self.grpAllRibbon, name=(prefix + 'RbnDeformer_grp'))
        self.grpDeform       = mc.duplicate(self.grpAllRibbon, name=(prefix + 'RbnDeformSurf_grp'))
        self.grpFollMain     = mc.duplicate(self.grpAllRibbon, name=(prefix + 'RbnFolSkin_grp'))
        self.grpFollVolume   = mc.duplicate(self.grpAllRibbon, name=(prefix + 'RbnFolVolume_grp'))
        self.grpVolDef       = mc.duplicate(self.grpAllRibbon, name=(prefix + 'RbnVolumeSquash_grp'))
        self.grpSineDef      = mc.duplicate(self.grpAllRibbon, name=(prefix + 'RbnSineDef_grp'))
        self.grpParentFol    = mc.duplicate(self.grpAllRibbon, name=(prefix + 'RbnExtra_grp'))

        # Create a NURBS-plane to use as a module
        tmpPlane = mc.nurbsPlane(axis=tmpPlaneDic[parallelAxis][0], width=tmpPlaneDic[parallelAxis][1],
                                 lengthRatio=tmpPlaneDic[parallelAxis][2], u=1,
                                 v=5, degree=3, ch=0)[0]

        # Create the NURBS-planes to use in the setup
        geoPlaneCls       = mc.duplicate(tmpPlane, name=(prefix + 'RbnCls_geo'))
        geoPlaneSine      = mc.duplicate(tmpPlane, name=(prefix + 'RbnSineDef_geo'))
        geoPlane          = mc.duplicate(tmpPlane, name=(prefix + 'RbnDef_geo'))
        geoPlaneVolume    = mc.duplicate(tmpPlane, name=(prefix + 'RbnVolume_geo'))

        # Offset the volume-plane
        mc.setAttr((geoPlaneVolume[0] + direction[parallelAxis][2]), -0.5 * scale)


    ### CREATING JOINT TEMPORARY FOR SPLITTING JNT FOLLICLE
        # Create Joint reference
        mc.select(cl=1)
        jointCreate = mc.joint(radius=scale / 5)

        # Duplicate joint from reference for orientation ribbon
        self.jointSkinUp = mc.duplicate(jointCreate, n=prefix + 'SkinHip_jnt')
        self.jointSkinMid = mc.duplicate(jointCreate, n=prefix + 'SkinMid_jnt')
        self.jointSkinDown = mc.duplicate(jointCreate, n=prefix + 'SkinChest_jnt')

        # Set the position for joints orient
        mc.setAttr((self.jointSkinUp[0] + '.translate'),self.upPoint, self.pos[1], self.pos[2])
        mc.setAttr((self.jointSkinMid[0] + '.translate'),self.pos[0], self.pos[1], self.pos[2])
        mc.setAttr((self.jointSkinDown[0] + '.translate'), self.downPoint, self.pos[1], self.pos[2])


        # Grouping the joints to have rotation according to parallel axis
        grpJointOrient = mc.group(self.jointSkinUp[0], self.jointSkinMid[0], self.jointSkinDown[0])


        # Set the rotation group joints
        if parallelAxis == 'z':
            mc.setAttr((grpJointOrient + '.rotate'), 0, -90, 0)

        if parallelAxis == 'y':
            mc.setAttr((grpJointOrient + '.rotate'), 0, 0, 90)

        mc.delete(mc.orientConstraint(listSpineJnt[0], self.jointSkinUp[0], mo=0))
        mc.delete(mc.orientConstraint(listSpineJnt[0], self.jointSkinMid[0], mo=0))
        mc.delete(mc.orientConstraint(listSpineJnt[0], self.jointSkinDown[0], mo=0))

        # Duplicate joint for volume
        jointVolSkinVolHip   = mc.duplicate(self.jointSkinUp[0], n=prefix + 'VolHip_jnt')
        jointVolSkinVolChest = mc.duplicate(self.jointSkinDown[0], n=prefix + 'VolChest_jnt')

        # Unparent from group
        mc.parent(jointVolSkinVolHip, jointVolSkinVolChest, w=1)

        # Freeze the joint
        mc.makeIdentity(jointVolSkinVolHip, jointVolSkinVolChest, a=1, r=1, pn=1)

        # Create deformers: Twist deformer, Sine deformer, Squash deformer
        # Set them rotation  according on point parallelFaceAxis position
        self.sineDef    = self.nonlinearDeformer(objects=[geoPlaneSine[0]], defType='sine',
                                                 name=au.prefix_name(geoPlaneSine[0]), lowBound=-1,
                                                 highBound=1, rotate=rotDefomer[parallelAxis])

        self.squashDef  = self.nonlinearDeformer(objects=[geoPlaneVolume[0]], defType='squash',
                                                 name=au.prefix_name(geoPlaneVolume[0]), lowBound=-1,
                                                 highBound=1, rotate=rotDefomer[parallelAxis])
        mc.parent(self.sineDef[1], self.grpSineDef[0])
        mc.parent(self.squashDef[1], self.grpVolDef[0])

        mc.setAttr((self.sineDef[0] + '.dropoff'), 1)

        # grouping deformer surface geoPlane and geoPlaneSKin
        self.grpGeoPlane    = au.group_object(['Zro'], geoPlane[0], geoPlane[0])
        self.grpGeoPlaneCls = au.group_object(['Zro'], geoPlaneCls[0], geoPlaneCls[0])

        # Create deformers: Blendshape
        mc.blendShape(geoPlaneSine[0],
                      geoPlaneCls[0], name=(prefix + 'Ref_bsn'), weight=[(0, 1)], foc=1)

        mc.blendShape(geoPlaneCls[0], geoPlane[0], name=(prefix + '_bsn'), weight=[(0, 1)], foc=1)

        # Squash deformer: Set up the connections for the volume control
        volumeRevfMdl = mc.shadingNode('multDoubleLinear', asUtility=1, name=(prefix + 'VolumeReverse_mdl'))
        mc.setAttr((volumeRevfMdl + '.input1'), -1)
        mc.connectAttr((ctrlMid + '.volume'), (volumeRevfMdl + '.input2'))
        mc.connectAttr((volumeRevfMdl + '.output'), (self.squashDef[0] + '.factor'))
        mc.connectAttr((ctrlMid + '.startDropoff'), (self.squashDef[0] + '.startSmoothness'))
        mc.connectAttr((ctrlMid + '.endDropoff'), (self.squashDef[0] + '.endSmoothness'))

        # Set the translate squash deformer according the point parallelFaceAxis position
        mc.connectAttr((ctrlMid + '.volumePosition'), (self.squashDef[1] + volInputMdn[parallelAxis][0]))

        # Squash deformer: Set up the volume scaling
        sumScalePma = mc.shadingNode('plusMinusAverage', asUtility=1, name=(prefix + 'VolumeScaleSum_pma'))
        mc.setAttr((sumScalePma + '.input1D[0]'), self.downPoint)
        mc.connectAttr((ctrlMid + '.volumeScale'), (sumScalePma + '.input1D[1]'))
        mc.connectAttr((sumScalePma + '.output1D'), (self.squashDef[1] + '.scaleY'))

        # Sine deformer: Set up the connections for the sine
        mc.connectAttr((ctrlMid + '.amplitude'), (self.sineDef[0] + '.amplitude'))
        mc.connectAttr((ctrlMid + '.offset'), (self.sineDef[0] + '.offset'))

        # Exception for z parallel axis
        if parallelAxis == 'z':
            sineTwistNode = mc.createNode('addDoubleLinear', n=(prefix + 'adjustSineTwistRotZ_adl'))
            mc.setAttr(sineTwistNode+'.input1', 90)
            mc.connectAttr(ctrlMid + '.twist', sineTwistNode+'.input2')
            mc.connectAttr(sineTwistNode + '.output', self.sineDef[1] + '.rotateZ')
        else:
            mc.connectAttr((ctrlMid + '.twist'), (self.sineDef[1] + '.rotateY'))

        mc.connectAttr((ctrlMid + '.sineLength'), (self.sineDef[0] + '.wavelength'))

        # Match position to the spine
        mc.delete(mc.parentConstraint(listSpineJnt[0], listSpineJnt[4], self.grpGeoPlane, mo=0))
        mc.delete(mc.parentConstraint(listSpineJnt[0], listSpineJnt[4], self.grpGeoPlaneCls, mo=0))
        mc.delete(mc.pointConstraint(listSpineJnt[0], listSpineJnt[4], grpJointOrient, mo=0))

        # Parent to grp extra and freeze the joints
        mc.parent(self.jointSkinUp[0], self.jointSkinMid[0], self.jointSkinDown[0], self.grpParentFol)
        mc.makeIdentity(self.jointSkinUp[0], self.jointSkinMid[0], self.jointSkinDown[0], a=1, r=1, pn=1)

        # Freeze grp plane skin and ref
        mc.makeIdentity(self.grpGeoPlane,self.grpGeoPlaneCls, a=1, t=1, pn=1)

        # Skining joints orient to plane orient
        skinCls = mc.skinCluster([self.jointSkinUp[0], self.jointSkinMid[0], self.jointSkinDown[0]], geoPlaneCls,
                       n='spineSkinCluster', tsb=True, bm=0, sm=0, nw=1, mi=2)

        # Distribute the skin
        skinPercent8  = '%s.cv[0:3][7]' % geoPlaneCls[0]
        skinPercent7  = '%s.cv[0:3][6]' % geoPlaneCls[0]
        skinPercent1  = '%s.cv[0:3][5]' % geoPlaneCls[0]
        skinPercent2  = '%s.cv[0:3][4]' % geoPlaneCls[0]
        skinPercent3  = '%s.cv[0:3][3]' % geoPlaneCls[0]
        skinPercent4  = '%s.cv[0:3][2]' % geoPlaneCls[0]
        skinPercent5  = '%s.cv[0:3][1]' % geoPlaneCls[0]
        skinPercent6  = '%s.cv[0:3][0]' % geoPlaneCls[0]

        mc.skinPercent(skinCls[0], skinPercent8, tv=[(self.jointSkinDown[0], 1)])
        mc.skinPercent(skinCls[0], skinPercent7, tv=[(self.jointSkinDown[0], 0.9),(self.jointSkinMid[0], 0.1)])
        mc.skinPercent(skinCls[0], skinPercent1, tv=[(self.jointSkinDown[0], 0.7),(self.jointSkinMid[0], 0.3)])
        mc.skinPercent(skinCls[0], skinPercent2, tv=[(self.jointSkinDown[0], 0.5),(self.jointSkinMid[0], 0.5)])
        mc.skinPercent(skinCls[0], skinPercent3, tv=[(self.jointSkinUp[0], 0.7),(self.jointSkinMid[0], 0.3)])
        mc.skinPercent(skinCls[0], skinPercent4, tv=[(self.jointSkinUp[0], 1)])
        mc.skinPercent(skinCls[0], skinPercent5, tv=[(self.jointSkinUp[0], 1)])
        mc.skinPercent(skinCls[0], skinPercent6, tv=[(self.jointSkinUp[0], 1)])

        # Match joint skin
        mc.delete(mc.parentConstraint(listSpineJnt[4], self.jointSkinDown))
        mc.delete(mc.parentConstraint(listSpineJnt[2], self.jointSkinMid))
        mc.delete(mc.parentConstraint(pelvisCtrl, self.jointSkinUp))

        ### CREATING FOLLICLE AND PART OF IT
        # Create joint on evenly position
        positionUVFolV = cr.split_evenly(jointVolSkinVolChest, jointVolSkinVolHip, prefix, split=3)
        # positionUVFol = cr.splitEvenly(self.jointSkinUp, self.jointSkinDown, prefix, split=numJoints)

        # Create follicles: The main-surface and the volume-surface
        follicleS =self.itemFollicle([listSpineJnt[1],listSpineJnt[2],listSpineJnt[3]], geoPlaneCls, 'fol')
        follicleV = self.itemFollicle(positionUVFolV, geoPlaneVolume, 'Volumefol')

        # Set the follicle U and V parameter
        for obj in follicleV['follicle']:
            mc.setAttr(obj + follicleVol[parallelAxis][0], follicleVol[parallelAxis][1])

        # Grouping listing of the follicle parent group
        follicleCtrlGrp = []
        follicleAllCtrl = []
        follicleSetGrp  = []

        # Looping the follicle S and follicle V
        for folS, folV in zip(follicleS['follicle'], follicleV['follicle']):
            # Listing the shape of follicles
            folLr = mc.listRelatives(folS, s=1)[0]
            # mc.setAttr(folLr + '.visibility', 0)

            # Parenting the follicles to grp follicle
            grpFolS = mc.parent(folS, self.grpFollMain)
            grpFolV = mc.parent(folV, self.grpFollVolume)

            # Create group offset for follilce
            follicleGrpOffset = mc.group(empty=True, name='%s_%s' % (au.prefix_name(folS), 'setGrp'))
            mc.delete(mc.parentConstraint(folS, follicleGrpOffset))

            # Append the grp set of follicle
            follicleSetGrp.append(follicleGrpOffset)

            # Create offset group follicle
            follicleGrpOffset = mc.parent(follicleGrpOffset, folS)

            # Create a joint, controller and a group for the current skin-follicle
            mc.select(clear=True)

            # Create joint for follicle
            #follicleJoint = mc.joint(name='%s_%s' % (au.prefixName(folS), 'jnt'), radius=scale / 6)

            # Create control for joint in follicle
            follicleCtrl = ct.Control(prefix=au.prefix_name(folS), groups_ctrl=['Zro'], ctrl_color='lightPink',
                                      ctrl_size=scale * 0.8, shape=ctrlDetails)

            follicleCtrlGrp.append(follicleCtrl.parent_control[0])
            follicleAllCtrl.append(follicleCtrl.control)
            # Parent joint to controller
            #mc.parent(follicleJoint, follicleCtrl.control)

            # Positioning skin-follicle control
            mc.delete(mc.parentConstraint(self.jointSkinMid, follicleCtrl.parent_control[0]))
            mc.delete(mc.pointConstraint(follicleGrpOffset, follicleCtrl.parent_control[0]))

            # Parent controller to group offset follicle
            mc.parent(follicleCtrl.parent_control[0], follicleGrpOffset)
            mc.setAttr(follicleCtrl.parent_control[0] + '.rotate', 0, 0, 0, type='double3')

            # Multiplier from follicle to multiplier for the size
            multMpdSize = mc.shadingNode('multiplyDivide', asUtility=1, name=au.prefix_name(folS) + 'MultiplierSize_mdn')
            mc.setAttr(multMpdSize + '.operation', 2)
            mc.connectAttr((folV + '.translate'), (multMpdSize + '.input1'))
            mc.setAttr(multMpdSize + '.input2X', scale)
            mc.setAttr(multMpdSize + '.input2Y', scale)
            mc.setAttr(multMpdSize + '.input2Z', scale)

            # Make the connections for the volume according on point parallelFaceAxis position
            multMpd = mc.shadingNode('multiplyDivide', asUtility=1, name=au.prefix_name(folS) + 'Multiplier_mdn')
            mc.connectAttr((ctrlMid + '.volumeMultiplier'), volInputMdn[parallelAxis][1])
            mc.connectAttr((multMpdSize + '.output'), (multMpd + '.input2'))

            sumPma = mc.shadingNode('plusMinusAverage', asUtility=1, name=au.prefix_name(folV) + 'VolumeSum_pma')
            mc.connectAttr((multMpd + volInputMdn[parallelAxis][2]), (sumPma + '.input1D[0]'))
            mc.setAttr((sumPma + '.input1D[1]'), 1)
            mc.connectAttr((sumPma + '.output1D'), (follicleGrpOffset[0] + volInputMdn[parallelAxis][3]))
            mc.connectAttr((sumPma + '.output1D'), (follicleGrpOffset[0] + volInputMdn[parallelAxis][4]))


    ### CONNECT ATTRIBUTE TRANSLATE AND ROTATE ALSO SCALE FROM CONTROLLER FOLLICLE TO JOINTS
        for folCtrl, spJnt in zip(follicleAllCtrl, listSpineJnt[1:]):
            mc.scaleConstraint(folCtrl, spJnt)
            au.connection(['connectTrans', 'connectOrient'], folCtrl, spJnt)

    ### NODE REVERSE FOR RIBBON SETUP
        # create reverse node for set FK
        ctrlSpineFKRev = mc.createNode('reverse', n='spineFkIk02_rev')
        au.connect_part_object(obj_base_connection='FkIk', target_connection='inputX',
                               obj_name=FKIKSwitch, target_name=[ctrlSpineFKRev],
                               select_obj=False)


    ### PARENT CONSTRAINT SKIN JOINT
     ## Constraint skin hip joint
        mc.parentConstraint(listSpineJnt[0], self.jointSkinUp[0], mo=1)

     ## Costraint skin mid joint
        skinMidCons = mc.parentConstraint(listSpineCtrlFK[1], listSpineCtrlIK[0], self.jointSkinMid[0], mo=1)

        ## setup MID controller set to IK
        au.connect_part_object(obj_base_connection='FkIk', target_connection='%s%s' % (listSpineCtrlIK[0], 'W1'),
                               obj_name=FKIKSwitch,
                               target_name=[skinMidCons[0]],
                               select_obj=False)

        ## setup MID controller set to FK
        au.connect_part_object(obj_base_connection='outputX', target_connection='%s%s' % (listSpineCtrlFK[1], 'W0'),
                               obj_name=ctrlSpineFKRev, target_name=[skinMidCons[0]],
                               select_obj=False)

     ## Costraint skin chest joint
        skinChestCons = mc.parentConstraint(listSpineCtrlFK[2], listSpineCtrlIK[1], self.jointSkinDown[0], mo=1)

        ## setup UP controller set to IK
        au.connect_part_object(obj_base_connection='FkIk', target_connection='%s%s' % (listSpineCtrlIK[1], 'W1'),
                               obj_name=FKIKSwitch,
                               target_name=[skinChestCons[0]],
                               select_obj=False)

        ## setup UP controller set to FK
        au.connect_part_object(obj_base_connection='outputX', target_connection='%s%s' % (listSpineCtrlFK[2], 'W0'),
                               obj_name=ctrlSpineFKRev, target_name=[skinChestCons[0]],
                               select_obj=False)


    ### CONNECTING BETWEEN CONTROLLER TO SPINE RIBBON AND JOINTS DRIVER
     ## Create grp null for spine follicle 03
        # Create Null driver grp controller FK spine 3
        ctrlFK3Null = mc.createNode('transform', n=prefix+'FKDrive_null')
        mc.delete(mc.parentConstraint(listSpineCtrlFK[1], listSpineCtrlFK[2],ctrlFK3Null))

        ctrlIK3Null = mc.createNode('transform', n=prefix + 'IKDrive_null')
        mc.delete(mc.parentConstraint(listSpineCtrlIK[0], listSpineCtrlIK[1], ctrlIK3Null))

        mc.parentConstraint(listSpineCtrlFK[1],listSpineCtrlFK[2], ctrlFK3Null)
        mc.parentConstraint(listSpineCtrlIK[0],listSpineCtrlIK[1], ctrlIK3Null)

        mc.parent(ctrlFK3Null, ctrlIK3Null, self.grpParentFol[0])

    ### CONSTRAINT CONTROLLER TO GRP FOLLICLE CTRL
      ## Constraint FK spine 01 to grp follicle control 01
        mc.parentConstraint(listSpineCtrlFK[0], follicleSetGrp[0], mo=0)

      ## Constraint FK spine 02 and IK spine 01 to grp follicle control 02
        ctrlSpine02Foll = mc.parentConstraint(listSpineCtrlFK[1], listSpineCtrlIK[0], follicleSetGrp[1], mo=0)

        # setup controller set to IK
        au.connect_part_object(obj_base_connection='FkIk', target_connection='%s%s' % (listSpineCtrlIK[0], 'W1'),
                               obj_name=FKIKSwitch,
                               target_name=[ctrlSpine02Foll[0]],
                               select_obj=False)

        # setup controller set to FK
        au.connect_part_object(obj_base_connection='outputX', target_connection='%s%s' % (listSpineCtrlFK[1], 'W0'),
                               obj_name=ctrlSpineFKRev, target_name=[ctrlSpine02Foll[0]],
                               select_obj=False)

      ## Constraint FK spine 03 and IK spine 02 to grp follicle control 03
        ctrlSpine03Foll = mc.parentConstraint(ctrlFK3Null, ctrlIK3Null, follicleSetGrp[2], mo=0)

        # setup controller set to IK
        au.connect_part_object(obj_base_connection='FkIk', target_connection='%s%s' % (ctrlIK3Null, 'W1'),
                               obj_name=FKIKSwitch,
                               target_name=[ctrlSpine03Foll[0]],
                               select_obj=False)

        # setup controller set to FK
        au.connect_part_object(obj_base_connection='outputX', target_connection='%s%s' % (ctrlFK3Null, 'W0'),
                               obj_name=ctrlSpineFKRev, target_name=[ctrlSpine03Foll[0]],
                               select_obj=False)

    ### CONSTRAINT CONTROLLER TO GRP JOINT SPINE
        ## Constraint FK spine 01 to grp joint control 01
        mc.parentConstraint(listSpineCtrlFK[0], grpJntSpine[0], mo=0)

        ## Constraint FK spine 02 and IK spine 01 to grp joint control 02
        ctrlSpine02Jnt = mc.parentConstraint(listSpineCtrlFK[1], listSpineCtrlIK[0], grpJntSpine[1], mo=0)

        # setup controller set to IK
        au.connect_part_object(obj_base_connection='FkIk', target_connection='%s%s' % (listSpineCtrlIK[0], 'W1'),
                               obj_name=FKIKSwitch,
                               target_name=[ctrlSpine02Jnt[0]],
                               select_obj=False)

        # setup controller set to FK
        au.connect_part_object(obj_base_connection='outputX', target_connection='%s%s' % (listSpineCtrlFK[1], 'W0'),
                               obj_name=ctrlSpineFKRev, target_name=[ctrlSpine02Jnt[0]],
                               select_obj=False)

        ## Constraint FK spine 03 and IK spine 02 to grp joint control 03
        ctrlSpine03Jnt = mc.parentConstraint(ctrlFK3Null, ctrlIK3Null, grpJntSpine[2], mo=0)

        # setup controller set to IK
        au.connect_part_object(obj_base_connection='FkIk', target_connection='%s%s' % (ctrlIK3Null, 'W1'),
                               obj_name=FKIKSwitch,
                               target_name=[ctrlSpine03Jnt[0]],
                               select_obj=False)

        # setup controller set to FK
        au.connect_part_object(obj_base_connection='outputX', target_connection='%s%s' % (ctrlFK3Null, 'W0'),
                               obj_name=ctrlSpineFKRev, target_name=[ctrlSpine03Jnt[0]],
                               select_obj=False)


    ### SCALE DECOMPOSE MATRIX FROM ANIM CONTROLLER TO FOLLICLE AND SKIN JOINT
        jntSkinList = [self.jointSkinUp[0], self.jointSkinMid[0], self.jointSkinDown[0]]

        decomposeMtxNode = mc.createNode('decomposeMatrix', n=prefix + 'ScaleFol_dmt')
        mc.connectAttr(animCtrl + '.worldMatrix[0]', decomposeMtxNode + '.inputMatrix')

        for i, j in zip (follicleS['follicle'], jntSkinList):
            mc.connectAttr(decomposeMtxNode + '.outputScale', i + '.scale')
            mc.connectAttr(decomposeMtxNode + '.outputScale', j + '.scale')


        # Cleanup: Hierarchy
        mc.parent(self.grpSineDef[0], self.grpVolDef[0], self.grpDeformers)
        mc.parent(self.grpGeoPlane[0], self.grpGeoPlaneCls[0], self.grpSurface)
        mc.parent(geoPlaneSine[0], geoPlaneVolume[0], self.grpDeform)
        mc.parent(self.grpCluster[0], self.grpDeform[0], self.grpSurface[0], self.grpDeformers[0], self.grpFollMain[0],
                  self.grpFollVolume[0], self.grpParentFol[0], self.grpAllRibbon)

    #     # Cleanup: Visibility
    #     mc.hide(self.grpCluster[0], self.grpGeoPlaneCls[0],self.grpDeform[0], self.grpDeformers[0],
    #             self.grpFollMain[0], self.grpFollVolume[0], self.grpParentFol[0])
    #
    #     # Lock some groups
    #     au.lockHideAttr(['t','r','s','v'], self.grpAllDetail)
    #     au.lockHideAttr(['t','r','s','v'], self.grpParentFol[0])
    #     au.lockHideAttr(['t','r','s','v'], self.grpFollVolume[0])
    #     au.lockHideAttr(['t','r','s','v'], self.grpFollMain[0])
    #     au.lockHideAttr(['t','r','s','v'], self.grpDeformers[0])
    #     au.lockHideAttr(['t','r','s'], self.grpSurface[0])
    #     au.lockHideAttr(['t','r','s','v'], self.grpDeform[0])
    #     au.lockHideAttr(['t', 'r', 's','v'], self.grpGeoPlaneCls[0])
    #     au.lockHideAttr(['t', 'r', 's','v'], self.grpCluster[0])
    #
    #     # Deleted the reference joint
    #     mc.delete(jointCreate, tmpPlane, grpJointOrient, self.jointSkinDown, self.jointSkinMid, self.jointSkinUp)



















    #     # If creating controller the module and tip
    #     if createCtrl:
    #         # Create module controller
    #         baseCtrl = ct.Control(prefix =module + 'Base', groupsCtrl=['Zro', 'Offset'], ctrlColor = 'yellow', ctrlSize=ctrlSize*1.2, shape=ct.CUBE)
    #         mc.delete(mc.parentConstraint(module, baseCtrl.parentControl[0]))
    #         mc.parent(module, baseCtrl.control)
    #
    #         # Connected the rotation control up to rotation joint orientation
    #         mc.connectAttr((baseCtrl.control + '.rotate'), (sumDoubleCtrlUp + '.input3D[2]'))
    #
    #         # Create tip controller
    #         tipCtrl = ct.Control(prefix =tip + 'Tip', groupsCtrl=['Zro', 'Offset'], ctrlColor = 'yellow', ctrlSize=ctrlSize*1.2, shape=ct.CUBE)
    #         mc.delete(mc.parentConstraint(tip,tipCtrl.parentControl[0]))
    #         mc.parent(tip, tipCtrl.control)
    #
    #         # Connected the rotation control down to rotation joint orientation
    #         mc.connectAttr((tipCtrl.control + '.rotate'), (sumDoubleCtrlDown + '.input3D[2]'))
    #
    #         # Parent to all grp ribbon
    #         mc.parent(baseCtrl.parentControl[0], tipCtrl.parentControl[0], self.grpAllDetail)
    #
    #
    #     # Lock unnecesarry key ribbon
    #     au.lockHideAttr(['s'], ctrlUp.control)
    #     au.lockHideAttr(['s'], ctrlMid.control)
    #     au.lockHideAttr(['s'], ctrlDown.control)
    #

    #

    #
    #     # Delete the module surface and group rotation driver
    #     mc.delete(tmpPlane, grpJointOrient)
    #
    #     # Clear all selection
    #     mc.select(cl=1)
    #
    # GENERAL FUNCTION: ADD JOINTS FOR GUIDANCE OF FOLLICLES
    def itemFollicle(self, items, objTansform, suffix):
        fol = []
        folShp = []
        for i in items:
            follicle = au.create_follicle_selection(i, objTansform, connect_follicle=['rotateConn', 'transConn'])[0]
            renameFol = mc.rename(follicle, '%s%s_%s' % (au.prefix_name(i), 'Rbn', suffix))
            fol.append(renameFol)
            folShape = mc.listRelatives(renameFol, s=1)[0]
            folShp.append(folShape)

        return {'item' : items,
                'follicle' : fol,
                'folShape' : folShp}

    # GENERAL FUNCTION: ADD ATTRIBUTE(S) ON MULTIPLE OBJECTS
    def addAttribute(self, objects=[], longName='', niceName='', separator=False, k=False, cb=False, **kwargs):
        # For each object
        for obj in objects:
            # For each attribute
            for x in range(0, len(longName)):
                # See if a niceName was defined
                attrNice = '' if not niceName else niceName[x]
                # If the attribute does not exists
                if not mc.attributeQuery(longName[x], node=obj, exists=True):
                    # Add the attribute
                    mc.addAttr(obj, longName=longName[x], niceName=attrNice, **kwargs)
                    # If lock was set to True
                    mc.setAttr((obj + '.' + longName[x]), k=k, e=1, cb=cb) if separator else mc.setAttr((obj + '.' + longName[x]), k=k, e=1, cb=cb)


    # GENERAL FUNCTION: CREATE A NONLINEAR DEFORMER
    def nonlinearDeformer(self, objects=[], defType=None, lowBound=-1, highBound=1, translate=None, rotate=None,
                          name='nonLinear'):

        # If something went wrong or the type is not valid, raise exception
        if not objects or defType not in ['bend', 'flare', 'sine', 'squash', 'twist', 'wave']:
            raise Exception, "function: 'nonlinearDeformer' - Make sure you specified a mesh and a valid deformer"

        # Create and rename the deformer
        nonLinDef = mc.nonLinear(objects[0], type=defType, lowBound=lowBound, highBound=highBound)
        nonLinDef[0] = mc.rename(nonLinDef[0], (name + '_' + defType + 'Def'))
        nonLinDef[1] = mc.rename(nonLinDef[1], (name + '_' + defType + 'Handle'))

        # If translate was specified, set the translate
        if translate:
            mc.setAttr((nonLinDef[1] + '.translate'), translate[0], translate[1], translate[2])

        # If rotate was specified, set the rotate
        if rotate:
            mc.setAttr((nonLinDef[1] + '.rotate'), rotate[0], rotate[1], rotate[2])

        # Return the deformer
        return nonLinDef