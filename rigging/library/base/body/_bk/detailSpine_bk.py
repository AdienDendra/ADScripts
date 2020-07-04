import maya.cmds as mc
import spine as sp
from rigLib.utils import core as cr, controller as ct

from rigging.tools import AD_utils as au

reload(cr)
reload(ct)
reload(au)
reload(sp)

class CreateDetail:
    def __init__(self,
                 parallelAxis ='y',
                 tipPos = '+',
                 listSpineJnt='',
                 listSpineCtrlFK='',
                 listSpineCtrlIK='',
                 FKIKSwitch='',
                 animCtrl='',
                 ctrlMid = '',
                 ctrlDetails = ct.CIRCLEPLUS,
                 scale=None,
                 prefix='prefix',
                 detailSpineDeformer=True,
                 numJoints=5):

        """
        :param parallelAxis  : str, two point parallel position direction whether on x or y or z axis
        :param tipPos    : str, position point (joint) of the tip regarding on the module joint whether on + or - axis
        :param prefix    : str, prefix name for detail
        :param numJoints : int, number of joint as well as the control of detail part
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
        self.grpAllDetail    = mc.group(empty=True, name=(prefix + 'AllDetail_grp'))
        self.grpSurface      = mc.duplicate(self.grpAllDetail, name=(prefix + 'RefSurface_grp'))
        self.grpFollMain     = mc.duplicate(self.grpAllDetail, name=(prefix + 'FolSkin_grp'))
        self.grpExtraFol     = mc.duplicate(self.grpAllDetail, name=(prefix + 'Extra_grp'))

        # Create a NURBS-plane to use as a module
        tmpPlane = mc.nurbsPlane(axis=tmpPlaneDic[parallelAxis][0], width=tmpPlaneDic[parallelAxis][1],
                                 lengthRatio=tmpPlaneDic[parallelAxis][2], u=1,
                                 v=5, degree=3, ch=0)[0]

    ### CREATING JOINT TEMPORARY FOR SPLITTING JNT FOLLICLE
        # Create Joint reference
        mc.select(cl=1)
        jointCreate = mc.joint(radius=scale / 5)

        # Duplicate joint from reference for orientation detail
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

        # Create the NURBS-planes to use in the setup
        geoPlaneSkin      = mc.duplicate(tmpPlane, name=(prefix + 'Skin_geo'))

        # grouping deformer surface geoPlane and geoPlaneSKin
        self.grpGeoPlaneCls = au.group_object(['Zro'], geoPlaneSkin[0], geoPlaneSkin[0])

        # Duplicate joint for volume
        jointVolSkinVolHip = mc.duplicate(self.jointSkinUp[0], n=prefix + 'VolHip_jnt')
        jointVolSkinVolChest = mc.duplicate(self.jointSkinDown[0], n=prefix + 'VolChest_jnt')

        # Unparent from group
        mc.parent(jointVolSkinVolHip, jointVolSkinVolChest, w=1)

        # Freeze the joint
        mc.makeIdentity(jointVolSkinVolHip, jointVolSkinVolChest, a=1, r=1, pn=1)

        if detailSpineDeformer:

            # Create the NURBS-planes to use in the setup
            self.geoPlaneSine = mc.duplicate(tmpPlane, name=(prefix + 'SineDef_geo'))
            self.geoPlaneVolume = mc.duplicate(tmpPlane, name=(prefix + 'Volume_geo'))

            # Offset the volume-plane
            mc.setAttr((self.geoPlaneVolume[0] + direction[parallelAxis][2]), -0.5 * scale)

            # Create deformers: Blendshape
            mc.blendShape(self.geoPlaneSine[0],
                          geoPlaneSkin[0], name=(prefix + 'Ref_bsn'), weight=[(0, 1)], foc=1)


        # Match position to the spine
        mc.delete(mc.parentConstraint(listSpineJnt[0], listSpineJnt[4], self.grpGeoPlaneCls, mo=0))
        mc.delete(mc.pointConstraint(listSpineJnt[0], listSpineJnt[4], grpJointOrient, mo=0))

        # Parent to grp extra and freeze the joints
        mc.parent(self.jointSkinUp[0], self.jointSkinMid[0], self.jointSkinDown[0], self.grpExtraFol)
        mc.makeIdentity(self.jointSkinUp[0], self.jointSkinMid[0], self.jointSkinDown[0], a=1, r=1, pn=1)

        # Freeze grp plane skin and ref
        mc.makeIdentity(self.grpGeoPlaneCls, a=1, t=1, pn=1)

        # Skining joints orient to plane orient
        skinCls = mc.skinCluster([self.jointSkinUp[0], self.jointSkinMid[0], self.jointSkinDown[0]], geoPlaneSkin,
                                 n='spineDtlSkinCluster', tsb=True, bm=0, sm=0, nw=1, mi=2)

        # Distribute the skin
        skinPercent8 = '%s.cv[0:3][7]' % geoPlaneSkin[0]
        skinPercent7 = '%s.cv[0:3][6]' % geoPlaneSkin[0]
        skinPercent1 = '%s.cv[0:3][5]' % geoPlaneSkin[0]
        skinPercent2 = '%s.cv[0:3][4]' % geoPlaneSkin[0]
        skinPercent3 = '%s.cv[0:3][3]' % geoPlaneSkin[0]
        skinPercent4 = '%s.cv[0:3][2]' % geoPlaneSkin[0]
        skinPercent5 = '%s.cv[0:3][1]' % geoPlaneSkin[0]
        skinPercent6 = '%s.cv[0:3][0]' % geoPlaneSkin[0]

        mc.skinPercent(skinCls[0], skinPercent8, tv=[(self.jointSkinDown[0], 1)])
        mc.skinPercent(skinCls[0], skinPercent7, tv=[(self.jointSkinDown[0], 0.9), (self.jointSkinMid[0], 0.1)])
        mc.skinPercent(skinCls[0], skinPercent1, tv=[(self.jointSkinDown[0], 0.7), (self.jointSkinMid[0], 0.3)])
        mc.skinPercent(skinCls[0], skinPercent2, tv=[(self.jointSkinDown[0], 0.4), (self.jointSkinMid[0], 0.6)])
        mc.skinPercent(skinCls[0], skinPercent3, tv=[(self.jointSkinUp[0], 0.4), (self.jointSkinMid[0], 0.6)])
        mc.skinPercent(skinCls[0], skinPercent4, tv=[(self.jointSkinUp[0], 0.8), (self.jointSkinMid[0], 0.2)])
        mc.skinPercent(skinCls[0], skinPercent5, tv=[(self.jointSkinUp[0], 1)])
        mc.skinPercent(skinCls[0], skinPercent6, tv=[(self.jointSkinUp[0], 1)])

        # Match joint skin
        mc.delete(mc.parentConstraint(listSpineJnt[4], self.jointSkinDown))
        mc.delete(mc.parentConstraint(listSpineJnt[2], self.jointSkinMid))
        mc.delete(mc.parentConstraint(listSpineJnt[1], self.jointSkinUp))

        ### CREATING FOLLICLE AND PART OF IT

        # Create follicles: The main-surface and the volume-surface
        mc.select(cl=1)
        offsetJntHip = mc.joint(n=prefix + 'Driver')
        matchPos = mc.parentConstraint(listSpineJnt[1], listSpineJnt[2], offsetJntHip, w=0.9)
        mc.setAttr('%s.%s' % (matchPos[0], listSpineJnt[2] + 'W1'), 0.1)

        follicleS = self.itemFollicle(prefix, [offsetJntHip, listSpineJnt[2], listSpineJnt[3]], geoPlaneSkin, 'fol')

        mc.delete(offsetJntHip, matchPos)

        follGrpOffset =[]
        follCtrl = []
        # Looping the follicle S and follicle V
        for folS, folShp, jntSpine in zip(follicleS['follicle'], follicleS['folShape'], listSpineJnt[1:4]):
            # Parenting the follicles to grp follicle
            mc.parent(folS, self.grpFollMain)

            # Group follicle offset
            # Create group offset for follice
            follicleGrpOffset = mc.group(empty=True, name='%s_%s' % (au.prefix_name(folS), 'setGrp'))
            follGrpOffset.append(follicleGrpOffset)

            # Create control for joint in follicle
            follicleCtrl = ct.Control(prefix=au.prefix_name(folS), groups_ctrl=['Zro'], ctrl_color='lightPink',
                                      ctrl_size=scale * 1.2, shape=ctrlDetails)
            follCtrl.append(follicleCtrl.control)

            # Parent ctrl grp to grp offset
            mc.parent(follicleCtrl.parent_control[0], follicleGrpOffset)

            # Parent grp offset to follicle
            mc.parent(follicleGrpOffset, folS)

            # Match position to the follicle
            mc.delete(mc.pointConstraint(jntSpine, follicleGrpOffset))

            # Parent constraint follicle control to joint spine
            mc.parentConstraint(follicleCtrl.control, jntSpine)
            mc.scaleConstraint(follicleCtrl.control, jntSpine)

            # Turn off visibility
            mc.setAttr(folShp + '.visibility', 0)

        ### NODE REVERSE FOR DETAIL SETUP
        # create reverse node for set FK
        ctrlSpineFKRev = mc.createNode('reverse', n='spineFkIk02_rev')
        au.connect_part_object(obj_base_connection='FkIk', target_connection='inputX',
                               obj_name=FKIKSwitch, target_name=[ctrlSpineFKRev],
                               select_obj=False)

        ### PARENT CONSTRAINT SKIN JOINT
        ## Constraint skin spine 01 joint
        mc.parentConstraint(listSpineCtrlFK[0], self.jointSkinUp[0], mo=0)

        ## Costraint skin mid joint
        skinMidCons = mc.parentConstraint(listSpineCtrlFK[1], listSpineCtrlIK[0], self.jointSkinMid[0], mo=0)

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
        skinChestCons = mc.parentConstraint(listSpineCtrlFK[2], listSpineCtrlIK[1], self.jointSkinDown[0], mo=0)

        ## setup UP controller set to IK
        au.connect_part_object(obj_base_connection='FkIk', target_connection='%s%s' % (listSpineCtrlIK[1], 'W1'),
                               obj_name=FKIKSwitch,
                               target_name=[skinChestCons[0]],
                               select_obj=False)

        ## setup UP controller set to FK
        au.connect_part_object(obj_base_connection='outputX', target_connection='%s%s' % (listSpineCtrlFK[2], 'W0'),
                               obj_name=ctrlSpineFKRev, target_name=[skinChestCons[0]],
                               select_obj=False)

        ### SCALE DECOMPOSE MATRIX FROM ANIM CONTROLLER TO FOLLICLE AND SKIN JOINT
        jntSkinList = [self.jointSkinUp[0], self.jointSkinMid[0], self.jointSkinDown[0]]

        decomposeMtxNode = mc.createNode('decomposeMatrix', n=prefix + 'ScaleFol_dmtx')
        mc.connectAttr(animCtrl + '.worldMatrix[0]', decomposeMtxNode + '.inputMatrix')

        for fol, jntSkn in zip(follicleS['follicle'], jntSkinList):
            mc.connectAttr(decomposeMtxNode + '.outputScale', fol + '.scale')
            mc.connectAttr(decomposeMtxNode + '.outputScale', jntSkn + '.scale')

        # Cleanup: Hierarchy
        mc.parent(self.grpGeoPlaneCls[0], self.grpSurface)
        mc.parent(self.grpSurface[0], self.grpFollMain[0],
                  self.grpExtraFol[0], self.grpAllDetail)

        # Cleanup: Visibility
        mc.hide(self.grpSurface[0], self.grpGeoPlaneCls[0], self.grpExtraFol[0])

        # Lock some groups
        au.lock_hide_attr(['t', 'r', 's', 'v'], self.grpAllDetail)

        au.lock_hide_attr(['t', 'r', 's'], self.grpFollMain[0])
        au.lock_hide_attr(['t', 'r', 's', 'v'], self.grpSurface[0])
        au.lock_hide_attr(['t', 'r', 's', 'v'], self.grpGeoPlaneCls[0])
        au.lock_hide_attr(['t', 'r', 's', 'v'], self.grpExtraFol[0])

        if detailSpineDeformer:

            self.grpFollVolume   = mc.group(empty=True, name=(prefix + 'FolVolume_grp'))
            self.grpDeform       = mc.duplicate(self.grpFollVolume, name=(prefix + 'DeformSurf_grp'))
            self.grpDeformers    = mc.duplicate(self.grpFollVolume, name=(prefix + 'Deformer_grp'))
            self.grpVolDef       = mc.duplicate(self.grpFollVolume, name=(prefix + 'VolumeSquash_grp'))
            self.grpSineDef      = mc.duplicate(self.grpFollVolume, name=(prefix + 'SineDef_grp'))

            # Create deformers: Twist deformer, Sine deformer, Squash deformer
            # Set them rotation  according on point parallelFaceAxis position
            self.sineDef    = self.nonlinearDeformer(objects=[self.geoPlaneSine[0]], defType='sine',
                                                     name=au.prefix_name(self.geoPlaneSine[0]), lowBound=-1,
                                                     highBound=1, rotate=rotDefomer[parallelAxis])

            self.squashDef  = self.nonlinearDeformer(objects=[self.geoPlaneVolume[0]], defType='squash',
                                                     name=au.prefix_name(self.geoPlaneVolume[0]), lowBound=-1,
                                                     highBound=1, rotate=rotDefomer[parallelAxis])
            mc.parent(self.sineDef[1], self.grpSineDef[0])
            mc.parent(self.squashDef[1], self.grpVolDef[0])

            mc.setAttr((self.sineDef[0] + '.dropoff'), 1)

            # Squash deformer: Set up the connections for the volume control
            volumeRevfMdl = mc.shadingNode('multDoubleLinear', asUtility=1, name=(prefix + 'VolReverse_mdl'))
            # Adding multiple scale for volume
            volumeMultPosMdl = mc.createNode('multDoubleLinear', n=(prefix + 'VolPosMultiplier_mdl'))
            volumeMultSclMdl = mc.createNode('multDoubleLinear', n=(prefix + 'VolSclMultiplier_mdl'))

            # Auto squash setup
            autoSquashCtrlIK    = mc.createNode('addDoubleLinear', n=(prefix + 'AutoSquashCtrlIk_adl'))
            autoSquashMultDiv   = mc.createNode('multiplyDivide', n=(prefix + 'AutoSquash_mdn'))
            autoSquashBlndColor = mc.createNode('blendColors', n=(prefix + 'AutoSquash_bnd'))
            combAddBetweenAdl   = mc.createNode('addDoubleLinear', n=(prefix + 'AutoSquashVol_adl'))

            mc.connectAttr(listSpineCtrlIK[1]+'.translateY', autoSquashCtrlIK+'.input1')
            mc.connectAttr(listSpineCtrlIK[2]+'.translateY', autoSquashCtrlIK+'.input2')

            mc.setAttr(autoSquashMultDiv+'.operation', 2)
            mc.setAttr(autoSquashMultDiv+'.input2X', -3*scale)
            mc.connectAttr(autoSquashCtrlIK+'.output', autoSquashMultDiv+'.input1X')

            mc.connectAttr(ctrlMid+'.autoSquash', autoSquashBlndColor+'.blender')
            mc.connectAttr(autoSquashMultDiv+'.outputX', autoSquashBlndColor+'.color1R')
            mc.connectAttr(autoSquashBlndColor+'.outputR', combAddBetweenAdl+'.input1')
            mc.connectAttr((ctrlMid + '.volume'), (combAddBetweenAdl + '.input2'))

            # Connect from add double linear to squash handle
            mc.setAttr((volumeRevfMdl + '.input1'), -1)
            mc.connectAttr((combAddBetweenAdl + '.output'), (volumeRevfMdl + '.input2'))
            mc.connectAttr((volumeRevfMdl + '.output'), (self.squashDef[0] + '.factor'))
            mc.connectAttr((ctrlMid + '.startDropoff'), (self.squashDef[0] + '.startSmoothness'))
            mc.connectAttr((ctrlMid + '.endDropoff'), (self.squashDef[0] + '.endSmoothness'))

            # Set the translate squash deformer according the point parallelFaceAxis position
            mc.setAttr((volumeMultPosMdl + '.input2'), scale)
            mc.connectAttr((ctrlMid + '.volumePosition'), (volumeMultPosMdl + '.input1'))
            mc.connectAttr((volumeMultPosMdl + '.output'), (self.squashDef[1] + volInputMdn[parallelAxis][0]))

            # Squash deformer: Set up the volume scaling
            sumScalePma = mc.shadingNode('plusMinusAverage', asUtility=1, name=(prefix + 'VolScaleSum_pma'))
            mc.connectAttr((ctrlMid + '.volumeScale'), (volumeMultSclMdl + '.input1'))
            mc.setAttr((volumeMultSclMdl + '.input2'), scale)
            mc.setAttr((sumScalePma + '.input1D[0]'), self.downPoint)
            mc.connectAttr((volumeMultSclMdl + '.output'), (sumScalePma + '.input1D[1]'))
            mc.connectAttr((sumScalePma + '.output1D'), (self.squashDef[1] + '.scaleY'))

            # Sine deformer: Set up the connections for the sine
            mc.connectAttr((ctrlMid + '.amplitude'), (self.sineDef[0] + '.amplitude'))
            mc.connectAttr((ctrlMid + '.offset'), (self.sineDef[0] + '.offset'))

            # Exception for z parallel axis
            if parallelAxis == 'z':
                sineTwistNode = mc.createNode('addDoubleLinear', n=(prefix + 'AdjustSineTwistRotZ_adl'))
                mc.setAttr(sineTwistNode+'.input1', 90)
                mc.connectAttr(ctrlMid + '.twist', sineTwistNode+'.input2')
                mc.connectAttr(sineTwistNode + '.output', self.sineDef[1] + '.rotateZ')
            else:
                mc.connectAttr((ctrlMid + '.twist'), (self.sineDef[1] + '.rotateY'))

            mc.connectAttr((ctrlMid + '.sineLength'), (self.sineDef[0] + '.wavelength'))


            # Create joint on evenly position
            positionUVFolV = cr.split_evenly(jointVolSkinVolChest, jointVolSkinVolHip, prefix, split=3)
            follicleV = self.itemFollicle(prefix, positionUVFolV, self.geoPlaneVolume, 'Volumefol')

            # Set the follicle U and V parameter
            for obj in follicleV['follicle']:
                mc.setAttr(obj + follicleVol[parallelAxis][0], follicleVol[parallelAxis][1])

            # Looping the follicle V
            for folS, folShp, folV, folGrpOfst, follCtl, jntSpine in zip(follicleS['follicle'], follicleS['folShape'],
                                                                follicleV['follicle'], follGrpOffset, follCtrl,
                                                                listSpineJnt[1:4]):
                # Parenting the follicles to grp follicle
                mc.parent(folV, self.grpFollVolume)

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
                mc.connectAttr((sumPma + '.output1D'), (folGrpOfst + volInputMdn[parallelAxis][3]))
                mc.connectAttr((sumPma + '.output1D'), (folGrpOfst + volInputMdn[parallelAxis][4]))

                # Parent constraint follicle control to joint spine
                mc.parentConstraint(follCtl, jntSpine)
                mc.scaleConstraint(follCtl, jntSpine)

                # Turn off visibility
                mc.setAttr(folShp+'.visibility', 0)

            # Cleanup: Hierarchy
            mc.parent(self.grpSineDef[0], self.grpVolDef[0], self.grpDeformers)
            mc.parent(self.geoPlaneSine[0], self.geoPlaneVolume[0], self.grpDeform)
            mc.parent(self.grpDeform, self.grpDeformers, self.grpFollVolume, self.grpAllDetail)

            # Cleanup: Visibility
            mc.hide(self.grpDeform, self.grpDeformers, self.grpFollVolume)

            au.lock_hide_attr(['t', 'r', 's', 'v'], self.grpVolDef[0])
            au.lock_hide_attr(['t', 'r', 's', 'v'], self.grpDeformers[0])
            au.lock_hide_attr(['t', 'r', 's', 'v'], self.grpDeform[0])

            mc.delete( positionUVFolV)

        # Deleted the reference joint
        mc.delete(jointCreate, tmpPlane, grpJointOrient, jointVolSkinVolHip, jointVolSkinVolChest)
        # print follCtrl
    # GENERAL FUNCTION: ADD JOINTS FOR GUIDANCE OF FOLLICLES
    def itemFollicle(self, prefix, items, objTansform, suffix):
        fol = []
        folShp = []
        for number, i in enumerate (items):
            follicle = au.create_follicle_selection(i, objTansform, connect_follicle=['rotateConn', 'transConn'])[0]
            renameFol = mc.rename(follicle, '%s%02d%s_%s' % (au.prefix_name(prefix), number + 1, 'Dtl', suffix))
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