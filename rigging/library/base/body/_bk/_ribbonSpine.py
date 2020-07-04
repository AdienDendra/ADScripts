import maya.cmds as mc
import rigLib.rig.body.spine as sp
from rigLib.utils import core as cr, controller as ct
from rigLib.utils import transform as tr

from rigging.tools import AD_utils as au

reload(cr)
reload(tr)
reload(ct)
reload(au)
reload(sp)

class RibbonSpine:
    def __init__(self,
                 parallelAxis ='y',
                 tipPos = '+',
                 aimAxis='+y',
                 upAxis ='-x',
                 listSpineJnt='',
                 pelvisCtrl='',
                 listSpineCtrlFK='',
                 listSpineCtrlIK='',
                 FKIKSwitch='',
                 FKIKConnectionList='',
                 ctrlMid = ct.SQUARE,
                 ctrlDetails = ct.CIRCLEPLUS,
                 ctrlSize = 1.0,
                 prefix='prefix',
                 numJoints=None):

        """
        :param createCtrl: bool, parameters for creating the control module and tip
        :param tip       : str, transform or joint as the tip of ribbon
        :param module      : str, transform or joint as the module of ribbon
        :param parallelAxis  : str, two point parallel position direction whether on x or y or z axis
        :param tipPos    : str, position point (joint) of the tip regarding on the module joint whether on + or - axis
        :param aimAxis   : str, aim axis is that pivot towards to x axis for rotation joint. Can fill with +x +y +z or -x -y -z
        :param upAxis    : str, up axis is that one pivot towards to y axis for rotation joint. Can fill with +x +y +z or -x -y -z
        :param ctrlTip   : var, ctrl shape of tip
        :param ctrlMid   : var, ctrl shape of middle
        :param ctrlBase  : var, ctrl shape of module
        :param ctrlTip   : var, ctrl shape of detail ribbon ctrl
        :param prefix    : str, prefix name for ribbon
        :param numJoints : int, number of joint as well as the control of ribbon part
        """
        # Width plane variable (following the number of joints
        size = float(numJoints)

        # Tip point dictionary towards
        tipPoint = {'+': [(size / 2.0 * -1), (size / 2.0)],
                    '-': [(size / 2.0), (size / 2.0 * -1)]}

        if tipPos in tipPoint.keys():
            self.pos       = (0,0,0)
            self.upPoint   = tipPoint[tipPos][0]
            self.downPoint = tipPoint[tipPos][1]
        else:
            raise mc.error('The string %s in tipPos argument is not found. Fill with + or -' % tipPos)

        # Dictionary list
        tmpPlaneDic ={'x': [(0,1,0), size, (1.0 / size), numJoints, 1],
                      'y': [(0,0,1), 1, size, 1, numJoints],
                      'z': [(0,1,0), 1, size, 1, numJoints]}

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

        # Create the main groups
        self.grpAllRibbon        = mc.group(empty=True, name=(prefix + 'AllRibbon_grp'))
        self.grpTransform        = mc.group(empty=True, name=(prefix + 'RbnTransform_grp'))
        self.grpJntCluster       = mc.duplicate(self.grpTransform, name=(prefix + 'RbnJntCluster_grp'))

        self.grpNoTransform     = mc.duplicate(self.grpAllRibbon, name=(prefix + 'RbnNoTransform_grp'))
        self.grpUtils           = mc.duplicate(self.grpAllRibbon, name=(prefix + 'RbnUtils_grp'))
        self.grpSurface         = mc.duplicate(self.grpAllRibbon, name=(prefix + 'RbnRefSurface_grp'))
        self.grpDeformers       = mc.duplicate(self.grpAllRibbon, name=(prefix + 'RbnDeformer_grp'))
        self.grpMisc            = mc.duplicate(self.grpAllRibbon, name=(prefix + 'RbnMisc_grp'))
        self.grpSurfaces        = mc.duplicate(self.grpAllRibbon, name=(prefix + 'RbnSurfaces_grp'))
        self.grpFollMain        = mc.duplicate(self.grpAllRibbon, name=(prefix + 'RbnFolSkin_grp'))
        self.grpFollVolume      = mc.duplicate(self.grpAllRibbon, name=(prefix + 'RbnFolVolume_grp'))
        self.grpVolDef          = mc.duplicate(self.grpAllRibbon, name=(prefix + 'RbnVolumeSquash_grp'))
        self.grpSineDef         = mc.duplicate(self.grpAllRibbon, name=(prefix + 'RbnSineDef_grp'))
        self.grpParentFol       = mc.duplicate(self.grpAllRibbon, name=(prefix + 'RbnParentClsFol_grp'))


        # Parenting the groups
        mc.parent(self.grpUtils, self.grpNoTransform)
        mc.parent(self.grpJntCluster, self.grpUtils)
        mc.parent(self.grpNoTransform, self.grpTransform, self.grpAllRibbon)

        # Create a NURBS-plane to use as a module
        tmpPlane = mc.nurbsPlane(axis=tmpPlaneDic[parallelAxis][0], width=tmpPlaneDic[parallelAxis][1],
                                 lengthRatio=tmpPlaneDic[parallelAxis][2], u=1,
                                 v=2, degree=3, ch=0)[0]

        # Create the NURBS-planes to use in the setup
        geoPlaneSkin      = mc.duplicate(tmpPlane, name=(prefix + 'RbnSkin_geo'))
        geoPlaneSine      = mc.duplicate(tmpPlane, name=(prefix + 'RbnSineDef_geo'))
        geoPlane          = mc.duplicate(tmpPlane, name=(prefix + 'RbnDef_geo'))
        geoPlaneVolume    = mc.duplicate(tmpPlane, name=(prefix + 'RbnVolume_geo'))

        # Offset the volume-plane
        mc.setAttr((geoPlaneVolume[0] + direction[parallelAxis][2]), -0.5)

        # Create Joint reference
        jointCreate = mc.createNode('joint')

        # Duplicate joint from reference for orientation ribbon
        self.jointSkinUp = mc.duplicate(jointCreate, n=prefix + 'SkinHip_jnt')
        self.jointSkinMid = mc.duplicate(jointCreate, n=prefix + 'SkinMid_jnt')
        self.jointSkinDown = mc.duplicate(jointCreate, n=prefix + 'SkinChest_jnt')

        # Set the position for joints orient
        mc.setAttr((self.jointSkinUp[0] + '.translate'),self.upPoint, self.pos[1], self.pos[2])
        mc.setAttr((self.jointSkinMid[0] + '.translate'),self.pos[0], self.pos[1], self.pos[2])
        mc.setAttr((self.jointSkinDown[0] + '.translate'), self.downPoint, self.pos[1], self.pos[2])

        # Set the joints rotation axis aiming and upper
        cr.direction_pivot(self.jointSkinUp[0], aim_axis=aimAxis, up_axis=upAxis)
        cr.direction_pivot(self.jointSkinMid[0], aim_axis=aimAxis, up_axis=upAxis)
        cr.direction_pivot(self.jointSkinDown[0], aim_axis=aimAxis, up_axis=upAxis)

        # Create Group for joints orientation ribbon
        self.jointUpSkinParent = tr.create_parent_transform(['Zro'], self.jointSkinUp[0],
                                                            self.jointSkinUp[0])
        self.jointMidSkinParent = tr.create_parent_transform(['Zro'], self.jointSkinMid[0],
                                                             self.jointSkinMid[0])
        self.jointDownSkinParent = tr.create_parent_transform(['Zro'], self.jointSkinDown[0],
                                                              self.jointSkinDown[0])

        # Grouping the joints to have rotation according to parallel axis
        grpJointOrient = mc.group(self.jointUpSkinParent[0], self.jointMidSkinParent[0], self.jointDownSkinParent[0])


        # Set the rotation group joints
        if parallelAxis == 'z':
            mc.setAttr((grpJointOrient + '.rotate'), 0, -90, 0)

        if parallelAxis == 'y':
            mc.setAttr((grpJointOrient + '.rotate'), 0, 0, 90)

        mc.makeIdentity(grpJointOrient, a=1, n=1, rotate=1, translate=1)

        ctrlMid  = ct.Control(match_obj_first_position=self.jointSkinMid[0], prefix =prefix + 'Mid', groups_ctrl=['Zro', 'SDK'],
                              ctrl_color='blue', ctrl_size=ctrlSize * 1.3, shape=ctrlMid)

        # Add attributes: Volume attributes
        self.addAttribute(objects=[ctrlMid.control], longName=['volumeSep'], niceName=[' '], at="enum",
                          en='Volume', cb=True)

        self.addAttribute(objects=[ctrlMid.control], longName=['volume'], at="float", min=-1, max=1, k=True)
        self.addAttribute(objects=[ctrlMid.control], longName=['volumeMultiplier'], at="float", min=1, dv=3, k=True)
        self.addAttribute(objects=[ctrlMid.control], longName=['startDropoff'], at="float", min=0, max=1, dv=1, k=True)
        self.addAttribute(objects=[ctrlMid.control], longName=['endDropoff'], at="float", min=0, max=1, dv=1, k=True)
        self.addAttribute(objects=[ctrlMid.control], longName=['volumeScale'], at="float", min=self.upPoint * 0.9, max=self.downPoint * 2, k=True)
        self.addAttribute(objects=[ctrlMid.control], longName=['volumePosition'], min=self.upPoint, max=self.downPoint, at="float", k=True)

        # Add attributes: Sine attributes
        self.addAttribute(objects=[ctrlMid.control], longName=['sineSep'], niceName=[' '], attributeType='enum', en="Sine:", cb=True)

        self.addAttribute(objects=[ctrlMid.control], longName=['amplitude'], attributeType="float", k=True)
        self.addAttribute(objects=[ctrlMid.control], longName=['offset'], attributeType="float", k=True)
        self.addAttribute(objects=[ctrlMid.control], longName=['twist'], attributeType="float", k=True)
        self.addAttribute(objects=[ctrlMid.control], longName=['sineLength'], min=0.1, dv=2, attributeType="float", k=True)

        # Add attributes: Extra attributes
        self.addAttribute(objects=[ctrlMid.control], longName=['extraSep'], niceName=[' '], at="enum", en='Extra', cb=True)
        self.addAttribute(objects=[ctrlMid.control], longName=['showExtraCtrl'], at="long",  min=0, max=1, dv=1, cb=True)
        self.addAttribute(objects=[ctrlMid.control], longName=['showSurfaceRibbon'], at="long",  min=0, max=1, dv=1, cb=True)

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

        # Cleanup: Hierarchy
        mc.parent(self.grpSineDef[0], self.grpVolDef[0], self.grpDeformers)
        mc.parent(geoPlane[0],geoPlaneSkin[0], self.grpSurface)
        mc.parent(self.jointUpSkinParent[0],
                  self.jointMidSkinParent[0], self.jointDownSkinParent[0], self.grpJntCluster)
        mc.parent(self.grpSurfaces[0], self.grpSurface[0], self.grpDeformers[0], self.grpMisc[0], self.grpFollMain[0],
                  self.grpFollVolume[0], self.grpUtils[0])
        mc.parent(ctrlMid.parent_control[0], self.grpTransform)
        mc.parent(geoPlaneSine[0], geoPlaneVolume[0], self.grpSurfaces)



        # Create deformers: Blendshape
        mc.blendShape(geoPlaneSine[0],
                      geoPlaneSkin[0], name=(prefix + 'Ref_bsn'), weight=[(0, 1)], foc=1)


        mc.blendShape(geoPlaneSkin[0], geoPlane[0], name=(prefix + '_bsn'), weight=[(0, 1)], foc=1)

        # Squash deformer: Set up the connections for the volume control
        volumeRevfMdl = mc.shadingNode('multDoubleLinear', asUtility=1, name=(prefix + 'VolumeReverse_mdl'))
        mc.setAttr((volumeRevfMdl + '.input1'), -1)
        mc.connectAttr((ctrlMid.control + '.volume'), (volumeRevfMdl + '.input2'))
        mc.connectAttr((volumeRevfMdl + '.output'), (self.squashDef[0] + '.factor'))
        mc.connectAttr((ctrlMid.control + '.startDropoff'), (self.squashDef[0] + '.startSmoothness'))
        mc.connectAttr((ctrlMid.control + '.endDropoff'), (self.squashDef[0] + '.endSmoothness'))

        # Set the translate squash deformer according the point parallelFaceAxis position
        mc.connectAttr((ctrlMid.control + '.volumePosition'), (self.squashDef[1] + volInputMdn[parallelAxis][0]))

        # Squash deformer: Set up the volume scaling
        sumScalePma = mc.shadingNode('plusMinusAverage', asUtility=1, name=(prefix + 'VolumeScaleSum_pma'))
        mc.setAttr((sumScalePma + '.input1D[0]'), self.downPoint)
        mc.connectAttr((ctrlMid.control + '.volumeScale'), (sumScalePma + '.input1D[1]'))
        mc.connectAttr((sumScalePma + '.output1D'), (self.squashDef[1] + '.scaleY'))

        # Sine deformer: Set up the connections for the sine
        mc.connectAttr((ctrlMid.control + '.amplitude'), (self.sineDef[0] + '.amplitude'))
        mc.connectAttr((ctrlMid.control + '.offset'), (self.sineDef[0] + '.offset'))

        # Exception for z parallel axis
        if parallelAxis == 'z':
            sineTwistNode = mc.createNode('addDoubleLinear', n=(prefix + 'adjustSineTwistRotZ_adl'))
            mc.setAttr(sineTwistNode+'.input1', 90)
            mc.connectAttr(ctrlMid.control + '.twist', sineTwistNode+'.input2')
            mc.connectAttr(sineTwistNode + '.output', self.sineDef[1] + '.rotateZ')
        else:
            mc.connectAttr((ctrlMid.control + '.twist'), (self.sineDef[1] + '.rotateY'))

        mc.connectAttr((ctrlMid.control + '.sineLength'), (self.sineDef[0] + '.wavelength'))

        # Connect the visibility of surface group
        mc.connectAttr((ctrlMid.control + '.showSurfaceRibbon'),
                       (self.grpSurface[0] + '.visibility'))

        # Create joint on evenly position
        positionUVFol = cr.split_evenly(self.jointSkinUp, self.jointSkinDown, prefix, split=numJoints)

        # Create follicles: The main-surface and the volume-surface
        follicleS = self.itemFollicle(positionUVFol, geoPlaneSkin, 'fol')
        follicleV = self.itemFollicle(positionUVFol, geoPlaneVolume, 'Volumefol')

        # Set the follicle U and V parameter
        for obj in follicleV['follicle']:
            mc.setAttr(obj + follicleVol[parallelAxis][0], follicleVol[parallelAxis][1])

        # # Match position to the spine
        # mc.delete(mc.parentConstraint(chest, hip, self.grpAllDetail))

        # delete joint reference
        mc.delete(positionUVFol)

        # Grouping listing of the follicle parent group
        follicleCtrlGrp = []
        follicleSetGrp =[]

        # Looping the follicle S and follicle V
        for folS, folV in zip(follicleS['follicle'], follicleV['follicle']):
            # Listing the shape of follicles
            folLr = mc.listRelatives(folS, s=1)[0]
            #mc.setAttr(folLr + '.visibility', 0)

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
            follicleJoint = mc.joint(name='%s_%s' % (au.prefix_name(folS), 'jnt'), radius=1.0)

            # Create control for joint in follicle
            follicleCtrl = ct.Control(prefix=au.prefix_name(folS), groups_ctrl=['Zro'], ctrl_color='lightPink',
                                      ctrl_size=ctrlSize * 0.8, shape=ctrlDetails)
            follicleCtrlGrp.append(follicleCtrl.parent_control[0])
            # Parent joint to controller
            mc.parent(follicleJoint, follicleCtrl.control)

            # Positioning skin-follicle control
            mc.delete(mc.parentConstraint(ctrlMid.control, follicleCtrl.parent_control[0]))
            mc.delete(mc.pointConstraint(follicleGrpOffset, follicleCtrl.parent_control[0]))

            # Parent controller to group offset follicle
            mc.parent(follicleCtrl.parent_control[0], follicleGrpOffset)

            # connect the visibility-switch for the controller
            mc.connectAttr((ctrlMid.control + '.showExtraCtrl'),
                           (follicleGrpOffset[0] + '.visibility'))

            # Make the connections for the volume according on point parallelFaceAxis position
            multMpd = mc.shadingNode('multiplyDivide', asUtility=1, name=au.prefix_name(folS) + 'Multiplier_mdn')
            mc.connectAttr((ctrlMid.control + '.volumeMultiplier'), volInputMdn[parallelAxis][1])
            mc.connectAttr((folV + '.translate'), (multMpd + '.input2'))

            sumPma = mc.shadingNode('plusMinusAverage', asUtility=1, name=au.prefix_name(folV) + 'VolumeSum_pma')
            mc.connectAttr((multMpd + volInputMdn[parallelAxis][2]), (sumPma + '.input1D[0]'))
            mc.setAttr((sumPma + '.input1D[1]'), 1)
            mc.connectAttr((sumPma + '.output1D'), (follicleGrpOffset[0] + volInputMdn[parallelAxis][3]))
            mc.connectAttr((sumPma + '.output1D'), (follicleGrpOffset[0] + volInputMdn[parallelAxis][4]))

        # Skining joints orient to plane def
        tempSkinCluster = mc.skinCluster([self.jointSkinUp[0], self.jointSkinMid[0], self.jointSkinDown[0]], geoPlaneSkin,
                                         n=prefix+'SkinCluster', tsb=True, bm=0, sm=0, nw=1, mi=2)

        # Match position to the spine
        chestPosition    = mc.delete(mc.parentConstraint(listSpineJnt[4], self.jointSkinDown[0], mo=0))
        midSpinePosition = mc.delete(mc.parentConstraint(listSpineJnt[2], self.jointSkinMid[0], mo=0))
        hipPosition      = mc.delete(mc.parentConstraint(listSpineJnt[0], self.jointSkinUp[0], mo=0))

        # Create Follicle for parent constraint
        spine4PrntFol = au.create_follicle_selection(listSpineJnt[4], geoPlane, prefix='spine4Prnt', suffix='fol',
                                                     connect_follicle=['rotateConn', 'transConn'])
        spine3PrntFol = au.create_follicle_selection(listSpineJnt[3], geoPlane, prefix='spine3Prnt', suffix='fol',
                                                     connect_follicle=['rotateConn', 'transConn'])
        spine2PrntFol = au.create_follicle_selection(listSpineJnt[2], geoPlane, prefix='spine2Prnt', suffix='fol',
                                                     connect_follicle=['rotateConn', 'transConn'])
        spine1PrntFol = au.create_follicle_selection(listSpineJnt[1], geoPlane, prefix='spine1Prnt', suffix='fol',
                                                     connect_follicle=['rotateConn', 'transConn'])
        rootPrntFol   = au.create_follicle_selection(listSpineJnt[0], geoPlane, prefix='rootPrnt', suffix='fol',
                                                     connect_follicle=['rotateConn', 'transConn'])

        # Parent all follicle to parent group follicle
        mc.parent(spine4PrntFol[0], spine3PrntFol[0], spine2PrntFol[0], spine1PrntFol[0], rootPrntFol[0], self.grpParentFol)

        # parent grp parent fol to grp utils
        mc.parent(self.grpParentFol[0], self.grpUtils)

        # Create group for replacing cluster position
        chestGrpCls  = au.group_follow_object(['Zro', 'Driver'], [listSpineJnt[4]], 'Cls')
        spine2GrpCls = au.group_follow_object(['Zro', 'Driver'], [listSpineJnt[2]], 'Cls')
        spine1GrpCls = au.group_follow_object(['Zro', 'Driver'], [listSpineJnt[1]], 'Cls')
        pelvisGrpCls    = au.group_follow_object(['Zro', 'Driver'], [listSpineJnt[0]], 'Cls')

        # Grouping cluster postion grp to group misc
        mc.parent(chestGrpCls[0], spine2GrpCls[0], spine1GrpCls[0], pelvisGrpCls[0], self.grpMisc)

        # Freezing the rotate and translate of cluster group
        mc.makeIdentity(chestGrpCls[0], a=1, n=1, rotate=1, translate=1)
        mc.makeIdentity(spine2GrpCls[0], a=1, n=1, rotate=1, translate=1)
        mc.makeIdentity(spine1GrpCls[0], a=1, n=1, rotate=1, translate=1)
        mc.makeIdentity(pelvisGrpCls[0], a=1, n=1, rotate=1, translate=1)

        # Connect cluster controls to ribbon surface
        chestRibbonCvs      = '%s.cv[0:3][3:4]' % geoPlane[0]
        spine2RibbonCvs     = '%s.cv[0:3][2]' % geoPlane[0]
        spine1RibbonCvs     = '%s.cv[0:3][1]' % geoPlane[0]
        pelvisRibbonCvs     = '%s.cv[0:3][0]' % geoPlane[0]

        chestRibbonClstr  = mc.cluster(chestRibbonCvs, wn=[chestGrpCls[1], chestGrpCls[1]], bs=True,
                                      n=prefix+'Chest_cls')
        spine2RibbonClstr = mc.cluster(spine2RibbonCvs, wn=[spine2GrpCls[1], spine2GrpCls[1]], bs=True,
                                      n=prefix + 'Spine2_cls')
        spine1RibbonClstr = mc.cluster(spine1RibbonCvs, wn=[spine1GrpCls[1], spine1GrpCls[1]], bs=True,
                                      n=prefix + 'Spine1_cls')
        pelvisRibbonClstr    = mc.cluster(pelvisRibbonCvs, wn=[pelvisGrpCls[1], pelvisGrpCls[1]], bs=True,
                                       n=prefix + 'Pelvis_cls')

    ### PARENT CONSTRAINT CONTROLLER TO CLUSTER GRP
        chestConsCls  = mc.parentConstraint(listSpineCtrlFK[2],listSpineCtrlIK[1], chestGrpCls[0], mo=1)
        spine2ConsCls = mc.parentConstraint(listSpineCtrlFK[1],listSpineCtrlIK[0], spine2GrpCls[0], mo=1)
        spine1ConsCls = mc.parentConstraint(listSpineCtrlFK[0], spine1GrpCls[0], mo=1)
        pelvisConsCls    = mc.parentConstraint(pelvisCtrl, pelvisGrpCls[0], mo=1)

    ### SWITCH CONSTRAINT FK/IK SETUP FOR spine2ConsCls AND chestConsCls
        ## setup MID controller set to IK
        au.connect_part_object(obj_base_connection='FkIk', target_connection='%s%s' % (listSpineCtrlIK[0], 'W1'),
                               obj_name=FKIKSwitch,
                               target_name=[spine2ConsCls[0]],
                               select_obj=False)

        ## setup MID controller set to FK
        # create reverse node for set FK
        ctrlSpineFKMidRev = mc.createNode('reverse',
                                          n=('%s%s' % (au.prefix_name(listSpineCtrlFK[1]), 'FK') + '_rev'))

        au.connect_part_object(obj_base_connection='FkIk', target_connection='inputX',
                               obj_name=FKIKSwitch, target_name=[ctrlSpineFKMidRev],
                               select_obj=False)

        au.connect_part_object(obj_base_connection='outputX', target_connection='%s%s' % (listSpineCtrlFK[1], 'W0'),
                               obj_name=ctrlSpineFKMidRev, target_name=[spine2ConsCls[0]],
                               select_obj=False)

        ## setup UP controller set to IK
        au.connect_part_object(obj_base_connection='FkIk', target_connection='%s%s' % (listSpineCtrlIK[1], 'W1'),
                               obj_name=FKIKSwitch,
                               target_name=[chestConsCls[0]],
                               select_obj=False)

        ## setup UP controller set to FK
        # create reverse node for set FK
        ctrlSpineFKUpRev = mc.createNode('reverse',
                                         n=('%s%s' % (au.prefix_name(listSpineCtrlFK[2]), 'FK') + '_rev'))

        au.connect_part_object(obj_base_connection='FkIk', target_connection='inputX',
                               obj_name=FKIKSwitch, target_name=[ctrlSpineFKUpRev],
                               select_obj=False)

        au.connect_part_object(obj_base_connection='outputX', target_connection='%s%s' % (listSpineCtrlFK[2], 'W0'),
                               obj_name=ctrlSpineFKUpRev, target_name=[chestConsCls[0]],
                               select_obj=False)

    ### PARENT CONSTRAINT FROM FOLLICLE PARENT CLS TO TO JOINT SPINE
        mc.parentConstraint(spine3PrntFol, listSpineJnt[3], mo=1)
        mc.parentConstraint(spine2PrntFol, listSpineJnt[2], mo=1)
        mc.parentConstraint(spine1PrntFol, listSpineJnt[1], mo=1)


    ### SCALE CONSTRAINT FROM FOLLICLE PARENT CLS TO TO JOINT SPINE
        mc.scaleConstraint(follicleSetGrp[0], listSpineJnt[1])
        mc.scaleConstraint(follicleSetGrp[2], listSpineJnt[2])
        mc.scaleConstraint(follicleSetGrp[4], listSpineJnt[3])




  ################################################################################################





        # chestRibbonClsHdl = mc.cluster(chestRibbonCvs, wn=[chestCtrl['c'], chestCtrl['c']], bs=True,
        #                                n=prefix + 'ChestRibbon_cls')
        # hipRibbonClsHdl = mc.cluster(hipRibbonCvs, wn=[hipCtrl['c'], hipCtrl['c']], bs=True,
        #                               n=prefix + 'ChestRibbon_cls')


    #

    #     # connect controls to ribbon surface
    #     #geoPlane          = mc.duplicate(tmpPlane, name=(prefix + '_geo'))
    #     # chestRibbonCvs = '%s.cv[0:3][2:3]' % geoPlane[0]
    #     # hipsRibbonCvs = '%s.cv[0:3][0:1]' % geoPlane[0]
    #     #
    #     # chestRibbonClstr = mc.cluster(chestRibbonCvs, n=prefix+'Chest_cls')
    #     # hipsRibbonClstr  = mc.cluster(hipsRibbonCvs, n=prefix+'Hip_cls')


        # # Get part joint position
        # self.jointRefUp   = mc.duplicate(self.jointSkinUp[0], n=prefix + 'Up_jnt')
        # self.jointRefDown = mc.duplicate(self.jointSkinDown[0], n=prefix + 'Down_jnt')

    #     # Unparent joint duplicate
    #     mc.parent(self.jointRefUp, self.jointRefDown, w=True)
    #









    #     # Connect controller module and up joint orient
    #     sumDoubleCtrlUp = mc.shadingNode('plusMinusAverage', asUtility=1, name=(prefix + 'AverageOrientUp_pma'))
    #     mc.connectAttr((ctrlUp.control + '.rotate'), (sumDoubleCtrlUp + '.input3D[0]'))
    #     mc.connectAttr((module + '.rotate'), (sumDoubleCtrlUp + '.input3D[1]'))
    #     mc.connectAttr((sumDoubleCtrlUp + '.output3D'), (self.jointSkinUp[0] + '.rotate'))
    #
    #     # Connect controller middle to joint orient
    #     mc.connectAttr(ctrlMid.control + '.rotate', self.jointOrientMid[0] + '.rotate')
    #
    #     # Connect controller tip and down joint orient
    #     sumDoubleCtrlDown = mc.shadingNode('plusMinusAverage', asUtility=1, name=(prefix + 'AverageOrientDwn_pma'))
    #     mc.connectAttr((ctrlDown.control + '.rotate'), (sumDoubleCtrlDown + '.input3D[0]'))
    #     mc.connectAttr((tip + '.rotate'), (sumDoubleCtrlDown + '.input3D[1]'))
    #     mc.connectAttr((sumDoubleCtrlDown + '.output3D'), (self.jointOrientDown[0] + '.rotate'))
    #
    #     # Match position with the module and tip joint
    #     mc.delete(mc.parentConstraint(module, tip, self.grpTransform))
    #     mc.parentConstraint(module, ctrlUp.parentControl[0])
    #     mc.parentConstraint(tip, ctrlDown.parentControl[0])
    #     mc.delete(mc.parentConstraint(ctrlUp.parentControl[0], ctrlDown.parentControl[0], ctrlMid.parentControl[0]))
    #
    #     # Aiming the mid control to the module
    #     mc.aimConstraint(ctrlUp.control, ctrlMid.parentControl[1], mo=1, wut='vector')
    #
    #     # Match the orientation of group control to the middle control ribbon
    #     for obj in follicleCtrlGrp:
    #         mc.delete(mc.orientConstraint(ctrlMid.control, obj, mo=0))
    #
    #     # Cleanup: Hierarchy
    #     mc.delete(mc.orientConstraint(tmpPlane, self.grpAllDetail))
    #     mc.parent(module, tip, self.grpAllDetail)
    #     mc.parent(self.twistDef[1], self.sineDef[1], self.squashDef[1], self.grpDeformers)
    #     mc.parent(geoPlaneOrient[0], geoPlaneWire[0], geoPlaneTwist[0], geoPlaneSine[0], geoPlaneVolume[0], self.grpSurfaces)
    #     mc.parent(self.jointUpParent[0], self.jointMidParent[0], self.jointDownParent[0], self.grpJntCluster)
    #     mc.parent(ctrlDown.parentControl[0], ctrlMid.parentControl[0], ctrlUp.parentControl[0], self.grpCtrl)
    #     mc.parent(geoPlane[0], self.grpSurface)
    #     mc.parent(deformCrv, (mc.listConnections(wireDef[0] + '.baseWire[0]')[0]), self.jointUpOrientParent[0],
    #               self.jointMidOrientParent[0], self.jointDownOrientParent[0], self.grpMisc)
    #     mc.parent(self.grpSurfaces[0], self.grpSurface[0], self.grpDeformers[0], self.grpMisc[0], self.grpFollMain[0],
    #               self.grpFollVolume[0], self.grpUtils[0])
    #     mc.parent(self.grpOffsetTransform[0],  self.grpTransform)
    #
    #     # Cleanup: Visibility
    #     mc.hide(self.grpFollVolume, self.grpSurfaces, self.grpDeformers, self.grpMisc, self.grpJntCluster, module, tip)
    #
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
    #     # Lock some groups
    #     au.lockAttr(['t','r','s'], self.grpAllDetail)
    #     au.lockAttr(['t','r','s'], self.grpNoTransform[0])
    #     au.lockAttr(['t','r','s'], self.grpUtils[0])
    #     au.lockAttr(['t','r','s'], self.grpFollMain[0])
    #     au.lockAttr(['t','r','s'], self.grpFollVolume[0])
    #     au.lockAttr(['t','r','s'], self.grpFollVolume[0])
    #     au.lockAttr(['t','r','s'], self.grpTransform)
    #
    #     # Deleted the reference joint
    #     mc.delete(jointCreate, positionUVFol, self.jointRefUp, self.jointRefDown)
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
            renameFol = mc.rename(follicle, '%s_%s' % (au.prefix_name(i), suffix))
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