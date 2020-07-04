import maya.cmds as mc
import rigLib.utils.core as cr
import rigLib.utils.transform as tr
from rigLib.utils import controller as ct

from rigging.tools import AD_utils as au

reload(cr)
reload(tr)
reload(ct)
reload(au)

class CreateRibbon:
    def __init__(self,
                 createCtrl =False,
                 tip = '',
                 base ='',
                 parallelAxis ='z',
                 tipPos = '',
                 aimAxis='',
                 upAxis ='',
                 ctrlTip =ct.SQUARE,
                 ctrlMid = ct.SQUARE,
                 ctrlBase =ct.SQUARE,
                 ctrlDetails = ct.CIRCLEPLUS,
                 ctrlSize = 1.0,
                 prefix='prefix',
                 numJoints=None):

        """
        :param createCtrl: bool, parameters for creating the control module and tip
        :param tip       : str, transform or joint as the tip of ribbon
        :param base      : str, transform or joint as the module of ribbon
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
                      'y': [(1,0,0), 1, size, 1, numJoints],
                      'z': [(0,1,0), 1, size, 1, numJoints]}

        direction = {'x': ['.rotateY', 90, '.translateZ'],
                     'y': ['.rotateZ', 90, '.translateZ'],
                     'z': ['.rotateX', 0, '.translateX']}

        rotDefomer = {'x': (0, 0, 90),
                      'y': (0, 0, 180),
                      'z': (-90, 0, 90)}

        volInputMdn = {'x': ['.translateX','.input1Z', '.outputZ','.scaleY', '.scaleZ'],
                       'y': ['.translateY','.input1Z', '.outputZ', '.scaleX', '.scaleZ'],
                       'z': ['.translateZ','.input1X', '.outputX','.scaleX', '.scaleZ']}

        follicleVol ={'x': ('.parameterV', -1),
                      'y': ('.parameterU', -1),
                      'z': ('.parameterU', 1)}

        # Create the main groups
        self.grpAllRibbon  = mc.group(empty=True, name=(prefix + 'AllRibbon_grp'))

        self.grpTransform        = mc.group(empty=True, name=(prefix + 'Transform_grp'))
        self.grpOffsetTransform  = mc.duplicate(self.grpTransform, name=(prefix + 'TransformOffset_grp'))
        self.grpCtrl             = mc.duplicate(self.grpTransform, name=(prefix + 'Ctrl_grp'))
        self.grpJntCluster       = mc.duplicate(self.grpTransform, name=(prefix + 'JntCluster_grp'))

        self.grpNoTransform = mc.duplicate(self.grpAllRibbon, name=(prefix + 'NoTransform_grp'))
        self.grpUtils       = mc.duplicate(self.grpAllRibbon, name=(prefix + 'Utils_grp'))
        self.grpSurface     = mc.duplicate(self.grpAllRibbon, name=(prefix + 'Surface_grp'))
        self.grpDeformers   = mc.duplicate(self.grpAllRibbon, name=(prefix + 'Deformer_grp'))
        self.grpMisc        = mc.duplicate(self.grpAllRibbon, name=(prefix + 'Misc_grp'))
        self.grpSurfaces    = mc.duplicate(self.grpAllRibbon, name=(prefix + 'Surfaces_grp'))
        self.grpFollMain    = mc.duplicate(self.grpAllRibbon, name=(prefix + 'FolliclesSkin_grp'))
        self.grpFollVolume  = mc.duplicate(self.grpAllRibbon, name=(prefix + 'FolliclesVolume_grp'))


        # Parenting the groups
        mc.parent(self.grpUtils, self.grpNoTransform)
        mc.parent(self.grpJntCluster, self.grpUtils)
        mc.parent(self.grpCtrl,self.grpOffsetTransform )
        mc.parent(self.grpNoTransform, self.grpTransform, self.grpAllRibbon)

        # Create a NURBS-plane to use as a module
        tmpPlane = mc.nurbsPlane(axis=tmpPlaneDic[parallelAxis][0], width=tmpPlaneDic[parallelAxis][1],
                                 lengthRatio=tmpPlaneDic[parallelAxis][2], u=tmpPlaneDic[parallelAxis][3],
                                 v=tmpPlaneDic[parallelAxis][4], degree=3, ch=0)[0]

        # Create the NURBS-planes to use in the setup
        geoPlane          = mc.duplicate(tmpPlane, name=(prefix + '_geo'))
        geoPlaneTwist     = mc.duplicate(tmpPlane, name=(prefix + 'TwistDef_geo'))
        geoPlaneSine      = mc.duplicate(tmpPlane, name=(prefix + 'SineDef_geo'))
        geoPlaneWire      = mc.duplicate(tmpPlane, name=(prefix + 'WireDef_geo'))
        geoPlaneOrient    = mc.duplicate(tmpPlane, name=(prefix + 'OrientDef_geo'))
        geoPlaneVolume    = mc.duplicate(tmpPlane, name=(prefix + 'Volume_geo'))

        # Offset the volume-plane
        mc.setAttr((geoPlaneVolume[0] + direction[parallelAxis][2]), -0.5)

        # Create Joint reference
        jointCreate = mc.createNode('joint')

        # Duplicate joint from reference for skinning to the wire curve
        self.jointUp = mc.duplicate(jointCreate, n=prefix + 'Up_jnt')
        self.jointMid = mc.duplicate(jointCreate, n=prefix + 'Mid_jnt')
        self.jointDown = mc.duplicate(jointCreate, n=prefix + 'Down_jnt')

        # Duplicate joint from reference for orientation ribbon
        self.jointOrientUp = mc.duplicate(jointCreate, n=prefix + 'OrientUp_jnt')
        self.jointOrientMid = mc.duplicate(jointCreate, n=prefix + 'OrientMid_jnt')
        self.jointOrientDown = mc.duplicate(jointCreate, n=prefix + 'OrientDown_jnt')

        # Set the position for joints
        mc.setAttr((self.jointUp[0] + '.translate'),self.upPoint, self.pos[1], self.pos[2])
        mc.setAttr((self.jointMid[0] + '.translate'),self.pos[0], self.pos[1], self.pos[2])
        mc.setAttr((self.jointDown[0] + '.translate'), self.downPoint, self.pos[1], self.pos[2])

        # Set the position for joints orient
        mc.setAttr((self.jointOrientUp[0] + '.translate'),self.upPoint, self.pos[1], self.pos[2])
        mc.setAttr((self.jointOrientMid[0] + '.translate'),self.pos[0], self.pos[1], self.pos[2])
        mc.setAttr((self.jointOrientDown[0] + '.translate'), self.downPoint, self.pos[1], self.pos[2])

        # Set the joints rotation axis aiming and upper
        cr.direction_pivot(self.jointOrientUp[0], aim_axis=aimAxis, up_axis=upAxis)
        cr.direction_pivot(self.jointOrientMid[0], aim_axis=aimAxis, up_axis=upAxis)
        cr.direction_pivot(self.jointOrientDown[0], aim_axis=aimAxis, up_axis=upAxis)

        # Grouping the joints to have rotation according to parallel axis
        grpJointOrient = mc.group(self.jointOrientUp[0], self.jointOrientMid[0], self.jointOrientDown[0],
                                  self.jointUp[0], self.jointMid[0], self.jointDown[0])

        # Set the rotation group joints
        if parallelAxis == 'z':
            mc.setAttr((grpJointOrient + '.rotate'), 0, -90, 0)

        if parallelAxis == 'y':
            mc.setAttr((grpJointOrient + '.rotate'), 0, 0, 90)

        # Unparent from the group
        mc.parent(self.jointOrientUp[0], self.jointOrientMid[0], self.jointOrientDown[0],
                      self.jointUp[0], self.jointMid[0], self.jointDown[0], w=1)

        # Create Group for joints wire curve
        self.jointUpParent = tr.create_parent_transform(['Zro', 'Offset'], self.jointUp[0], self.jointUp[0])
        self.jointMidParent = tr.create_parent_transform(['Zro', 'Offset'], self.jointMid[0], self.jointMid[0])
        self.jointDownParent = tr.create_parent_transform(['Zro', 'Offset'], self.jointDown[0], self.jointDown[0])

        # Create Group for joints orientation ribbon
        self.jointUpOrientParent = tr.create_parent_transform(['Zro', 'Offset'], self.jointOrientUp[0],
                                                              self.jointOrientUp[0])
        self.jointMidOrientParent = tr.create_parent_transform(['Zro', 'Offset'], self.jointOrientMid[0],
                                                               self.jointOrientMid[0])
        self.jointDownOrientParent = tr.create_parent_transform(['Zro', 'Offset'], self.jointOrientDown[0],
                                                                self.jointOrientDown[0])

        # Create the controllers
        ctrlUp   = ct.Control(match_obj_first_position=self.jointUpParent[0], prefix =prefix + 'Up', groups_ctrl=['Zro', 'Offset', 'SDK'], ctrl_size=ctrlSize, shape=ctrlTip)
        ctrlMid  = ct.Control(match_obj_first_position=self.jointMidParent[0], prefix =prefix + 'Mid', groups_ctrl=['Zro', 'Offset', 'SDK'], ctrl_color='blue', ctrl_size=ctrlSize * 1.3, shape=ctrlMid)
        ctrlDown = ct.Control(match_obj_first_position=self.jointDownParent[0], prefix =prefix + 'Down', groups_ctrl=['Zro', 'Offset', 'SDK'], ctrl_size=ctrlSize, shape=ctrlBase)

        # PointConstraint the midCtrl between the top/end
        mc.pointConstraint(ctrlDown.control, ctrlUp.control, ctrlMid.parent_control[1], mo=1)


        # Add attributes: Twist/Roll attributes
        self.addAttribute(objects=[ctrlDown.control, ctrlMid.control, ctrlUp.control],
                          longName=['twistSep'], niceName=[' '], at="enum", en='Twist', cb=True)

        self.addAttribute(objects=[ctrlDown.control, ctrlUp.control], longName=['twist'], at="float", k=True)
        self.addAttribute(objects=[ctrlDown.control, ctrlUp.control], longName=['twistOffset'], at="float", k=True)
        self.addAttribute(objects=[ctrlDown.control, ctrlUp.control], longName=['affectToMid'], at="float", min=0, max=10, dv=10, k=True)
        self.addAttribute(objects=[ctrlMid.control], longName=['roll'], at="float", k=True)
        self.addAttribute(objects=[ctrlMid.control], longName=['rollOffset'], at="float", k=True)

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
        self.addAttribute(objects=[ctrlMid.control], longName=['showExtraCtrl'], at="long",  min=0, max=1, dv=0, cb=True)
        self.addAttribute(objects=[ctrlMid.control], longName=['showSurfaceRibbon'], at="long",  min=0, max=1, dv=0, cb=True)


        # Create deformers: Twist deformer, Sine deformer, Squash deformer
        # Set them rotation  according on point parallelFaceAxis position
        self.twistDef   = self.nonlinearDeformer(objects=[geoPlaneTwist[0]], defType='twist',
                                                 name=au.prefix_name(geoPlaneTwist[0]), lowBound=-1,
                                                 highBound=1, rotate=rotDefomer[parallelAxis])

        self.sineDef    = self.nonlinearDeformer(objects=[geoPlaneSine[0]], defType='sine',
                                                 name=au.prefix_name(geoPlaneSine[0]), lowBound=-1,
                                                 highBound=1, rotate=rotDefomer[parallelAxis])

        self.squashDef  = self.nonlinearDeformer(objects=[geoPlaneVolume[0]], defType='squash',
                                                 name=au.prefix_name(geoPlaneVolume[0]), lowBound=-1,
                                                 highBound=1, rotate=rotDefomer[parallelAxis])

        mc.setAttr((self.sineDef[0] + '.dropoff'), 1)


        # Create deformers: Wire deformer
        deformCrv  = mc.curve(p=[(self.downPoint, 0, 0), (0, 0, 0), (self.upPoint, 0, 0)], degree=2)
        deformCrv  = mc.rename(deformCrv, (prefix + 'Wire_crv'))
        # Set orient curve
        mc.delete(mc.orientConstraint(grpJointOrient, deformCrv))

        wireDef    = mc.wire(geoPlaneWire, dds=(0, 15), wire=deformCrv)
        wireDef[0] = mc.rename(wireDef[0], (au.prefix_name(geoPlaneWire[0]) + '_wireNode'))


        # Skining joints to curve
        mc.skinCluster([self.jointUp[0], self.jointMid[0], self.jointDown[0]], deformCrv,
                       n='wireSkinCluster', tsb=True, bm=0, sm=0, nw=1, mi=1)

        # Skining joints orient to plane orient
        mc.skinCluster([self.jointOrientUp[0], self.jointOrientMid[0], self.jointOrientDown[0]], geoPlaneOrient,
                       n='orientSkinCluster', tsb=True, bm=0, sm=0, nw=1, mi=2)

        # Point constraining the the controller transform to the joint wire curve
        mc.pointConstraint(ctrlUp.control , self.jointUpParent[0])
        mc.pointConstraint(ctrlMid.control, self.jointMidParent[0])
        mc.pointConstraint(ctrlDown.control , self.jointDownParent[0])

        # Create deformers: Blendshape
        mc.blendShape(geoPlaneWire[0], geoPlaneTwist[0], geoPlaneSine[0], geoPlaneOrient[0],
                                geoPlane[0], name=(prefix + '_bsn'), weight=[(0, 1), (1, 1), (2, 1),(3, 1)])

        # Twist deformer: Sum the twist and the roll
        sumTopPma = mc.shadingNode('plusMinusAverage', asUtility=1, name=(prefix + 'TwistUpSum_pma'))
        mc.connectAttr((ctrlDown.control + '.twist'), (sumTopPma + '.input1D[0]'))
        mc.connectAttr((ctrlDown.control + '.twistOffset'), (sumTopPma + '.input1D[1]'))
        mc.connectAttr((ctrlMid.control + '.roll'), (sumTopPma + '.input1D[2]'))
        mc.connectAttr((ctrlMid.control + '.rollOffset'), (sumTopPma + '.input1D[3]'))
        mc.connectAttr((sumTopPma + '.output1D'), (self.twistDef[0] + '.startAngle'))

        sumEndPma = mc.shadingNode('plusMinusAverage', asUtility=1, name=(prefix + 'TwistDownSum_pma'))
        mc.connectAttr((ctrlUp.control + '.twist'), (sumEndPma + '.input1D[0]'))
        mc.connectAttr((ctrlUp.control + '.twistOffset'), (sumEndPma + '.input1D[1]'))
        mc.connectAttr((ctrlMid.control + '.roll'), (sumEndPma + '.input1D[2]'))
        mc.connectAttr((ctrlMid.control + '.rollOffset'), (sumEndPma + '.input1D[3]'))
        mc.connectAttr((sumEndPma + '.output1D'), (self.twistDef[0] + '.endAngle'))

        # Twist deformer: Set up the affect of the deformer
        topAffMdl = mc.shadingNode('multDoubleLinear', asUtility=1, name=(prefix + 'TwistUpAffect_mdl'))
        mc.setAttr((topAffMdl + '.input1'), -0.1)
        mc.connectAttr((ctrlDown.control + '.affectToMid'), (topAffMdl + '.input2'))
        mc.connectAttr((topAffMdl + '.output'), (self.twistDef[0] + '.lowBound'))

        endAffMdl = mc.shadingNode('multDoubleLinear', asUtility=1, name=(prefix + 'TwistDownAffect_mdl'))
        mc.setAttr((endAffMdl + '.input1'), 0.1)
        mc.connectAttr((ctrlUp.control + '.affectToMid'), (endAffMdl + '.input2'))
        mc.connectAttr((endAffMdl + '.output'), (self.twistDef[0] + '.highBound'))

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

        # Scaling the follicle with decompose matrix
        decomposeMtxScale = mc.createNode('decomposeMatrix', n=(prefix + 'scaleFol_dmt'))
        mc.connectAttr(self.grpOffsetTransform[0]+'.worldMatrix[0]', decomposeMtxScale+'.inputMatrix')

        # Get part joint position
        self.jointRefUp   = mc.duplicate(self.jointUp[0], n=prefix + 'Up_jnt')
        self.jointRefDown = mc.duplicate(self.jointDown[0], n=prefix + 'Down_jnt')

        # Unparent joint duplicate
        mc.parent(self.jointRefUp, self.jointRefDown, w=True)

        # Create joint on evenly position
        positionUVFol = cr.split_evenly(self.jointRefUp, self.jointRefDown, prefix, split=numJoints)

        # Create follicles: The main-surface and the volume-surface
        follicleS = self.itemFollicle(positionUVFol, geoPlane, 'fol')
        follicleV = self.itemFollicle(positionUVFol, geoPlaneVolume, 'Volumefol')

        # Set the follicle U and V parameter
        for obj in follicleV['follicle']:
            mc.setAttr(obj + follicleVol[parallelAxis][0], follicleVol[parallelAxis][1])

        # Grouping listing of the follicle parent group
        follicleCtrlGrp =[]

        # Looping the follicle S and follicle V
        for folS, folV in zip (follicleS['follicle'], follicleV['follicle']):

            # Listing the shape of follicles
            folLr = mc.listRelatives(folS, s=1)[0]
            mc.setAttr(folLr +'.visibility', 0)

            # Parenting the follicles to grp follicle
            mc.parent(folS, self.grpFollMain)
            mc.parent(folV, self.grpFollVolume)

            # Create group offset for follilce
            follicleGrpOffset = mc.group(empty=True, name='%s_%s' % (au.prefix_name(folS), 'setGrp'))
            mc.delete(mc.parentConstraint(folS, follicleGrpOffset))

            # Create offset group follicle
            follicleGrpOffset = mc.parent(follicleGrpOffset, folS)

            # Create a joint, controller and a group for the current skin-follicle
            mc.select(clear=True)

            # Create joint for follicle
            follicleJoint = mc.joint(name='%s_%s' % (au.prefix_name(folS), 'jnt'), radius=1.0)

            # Create control for joint in follicle
            follicleCtrl = ct.Control(prefix =au.prefix_name(folS), groups_ctrl=['Zro', 'Offset'], ctrl_color='lightPink', ctrl_size=ctrlSize * 0.8, shape=ctrlDetails)
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
                           (follicleGrpOffset[0]+ '.visibility'))

            # Make the connections for the volume according on point parallelFaceAxis position
            multMpd    = mc.shadingNode('multiplyDivide', asUtility=1, name=au.prefix_name(folS) + 'Multiplier_mdn')
            mc.connectAttr((ctrlMid.control + '.volumeMultiplier'), volInputMdn[parallelAxis][1])
            mc.connectAttr((folV + '.translate'), (multMpd + '.input2'))

            sumPma = mc.shadingNode('plusMinusAverage', asUtility=1, name=au.prefix_name(folV) + 'VolumeSum_pma')
            mc.connectAttr((multMpd + volInputMdn[parallelAxis][2]), (sumPma + '.input1D[0]'))
            mc.setAttr((sumPma + '.input1D[1]'), 1)
            mc.connectAttr((sumPma + '.output1D'), (follicleGrpOffset[0] + volInputMdn[parallelAxis][3]))
            mc.connectAttr((sumPma + '.output1D'), (follicleGrpOffset[0] + volInputMdn[parallelAxis][4]))


        # Connect controller module and up joint orient
        sumDoubleCtrlUp = mc.shadingNode('plusMinusAverage', asUtility=1, name=(prefix + 'AverageOrientUp_pma'))
        mc.connectAttr((ctrlUp.control + '.rotate'), (sumDoubleCtrlUp + '.input3D[0]'))
        mc.connectAttr((base + '.rotate'), (sumDoubleCtrlUp + '.input3D[1]'))
        mc.connectAttr((sumDoubleCtrlUp + '.output3D'), (self.jointOrientUp[0] + '.rotate'))

        # Connect controller middle to joint orient
        mc.connectAttr(ctrlMid.control + '.rotate', self.jointOrientMid[0] + '.rotate')

        # Connect controller tip and down joint orient
        sumDoubleCtrlDown = mc.shadingNode('plusMinusAverage', asUtility=1, name=(prefix + 'AverageOrientDwn_pma'))
        mc.connectAttr((ctrlDown.control + '.rotate'), (sumDoubleCtrlDown + '.input3D[0]'))
        mc.connectAttr((tip + '.rotate'), (sumDoubleCtrlDown + '.input3D[1]'))
        mc.connectAttr((sumDoubleCtrlDown + '.output3D'), (self.jointOrientDown[0] + '.rotate'))

        # Match position with the module and tip joint
        mc.delete(mc.parentConstraint(base, tip, self.grpTransform))
        mc.parentConstraint(base, ctrlUp.parent_control[0])
        mc.parentConstraint(tip, ctrlDown.parent_control[0])
        mc.delete(mc.parentConstraint(ctrlUp.parent_control[0], ctrlDown.parent_control[0], ctrlMid.parent_control[0]))

        # Aiming the mid control to the module
        mc.aimConstraint(ctrlUp.control, ctrlMid.parent_control[1], mo=1, wut='vector')

        # Match the orientation of group control to the middle control ribbon
        for obj in follicleCtrlGrp:
            mc.delete(mc.orientConstraint(ctrlMid.control, obj, mo=0))

        # Cleanup: Hierarchy
        mc.delete(mc.orientConstraint(tmpPlane, self.grpAllRibbon))
        mc.parent(base, tip, self.grpAllRibbon)
        mc.parent(self.twistDef[1], self.sineDef[1], self.squashDef[1], self.grpDeformers)
        mc.parent(geoPlaneOrient[0], geoPlaneWire[0], geoPlaneTwist[0], geoPlaneSine[0], geoPlaneVolume[0], self.grpSurfaces)
        mc.parent(self.jointUpParent[0], self.jointMidParent[0], self.jointDownParent[0], self.grpJntCluster)
        mc.parent(ctrlDown.parent_control[0], ctrlMid.parent_control[0], ctrlUp.parent_control[0], self.grpCtrl)
        mc.parent(geoPlane[0], self.grpSurface)
        mc.parent(deformCrv, (mc.listConnections(wireDef[0] + '.baseWire[0]')[0]), self.jointUpOrientParent[0],
                  self.jointMidOrientParent[0], self.jointDownOrientParent[0], self.grpMisc)
        mc.parent(self.grpSurfaces[0], self.grpSurface[0], self.grpDeformers[0], self.grpMisc[0], self.grpFollMain[0],
                  self.grpFollVolume[0], self.grpUtils[0])
        mc.parent(self.grpOffsetTransform[0],  self.grpTransform)

        # Cleanup: Visibility
        mc.hide(self.grpFollVolume, self.grpSurfaces, self.grpDeformers, self.grpMisc, self.grpJntCluster, base, tip)

        # If creating controller the module and tip
        if createCtrl:
            # Create module controller
            baseCtrl = ct.Control(prefix =base + 'Base', groups_ctrl=['Zro', 'Offset'], ctrl_color='yellow', ctrl_size=ctrlSize * 1.2, shape=ct.CUBE)
            mc.delete(mc.parentConstraint(base, baseCtrl.parent_control[0]))
            mc.parent(base, baseCtrl.control)

            # Connected the rotation control up to rotation joint orientation
            mc.connectAttr((baseCtrl.control + '.rotate'), (sumDoubleCtrlUp + '.input3D[2]'))

            # Create tip controller
            tipCtrl = ct.Control(prefix =tip + 'Tip', groups_ctrl=['Zro', 'Offset'], ctrl_color='yellow', ctrl_size=ctrlSize * 1.2, shape=ct.CUBE)
            mc.delete(mc.parentConstraint(tip, tipCtrl.parent_control[0]))
            mc.parent(tip, tipCtrl.control)

            # Connected the rotation control down to rotation joint orientation
            mc.connectAttr((tipCtrl.control + '.rotate'), (sumDoubleCtrlDown + '.input3D[2]'))

            # Parent to all grp ribbon
            mc.parent(baseCtrl.parent_control[0], tipCtrl.parent_control[0], self.grpAllRibbon)


        # Lock unnecesarry key ribbon
        au.lock_hide_attr(['s'], ctrlUp.control)
        au.lock_hide_attr(['s'], ctrlMid.control)
        au.lock_hide_attr(['s'], ctrlDown.control)

        # Lock some groups
        au.lock_attr(['t', 'r', 's'], self.grpAllRibbon)
        au.lock_attr(['t', 'r', 's'], self.grpNoTransform[0])
        au.lock_attr(['t', 'r', 's'], self.grpUtils[0])
        au.lock_attr(['t', 'r', 's'], self.grpFollMain[0])
        au.lock_attr(['t', 'r', 's'], self.grpFollVolume[0])
        au.lock_attr(['t', 'r', 's'], self.grpFollVolume[0])
        au.lock_attr(['t', 'r', 's'], self.grpTransform)

        # Deleted the reference joint
        mc.delete(jointCreate, positionUVFol, self.jointRefUp, self.jointRefDown)

        # Delete the module surface and group rotation driver
        mc.delete(tmpPlane, grpJointOrient)

        # Clear all selection
        mc.select(cl=1)

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