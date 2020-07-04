import maya.cmds as mc
from rigLib.utils import core as cr, controller as ct, transform as tr

from rigging.tools import AD_utils as au

reload(cr)
reload(tr)
reload(ct)
reload(au)

class CreateDetail:
    def __init__(self,
                 detailLimbDeformer=False,
                 tip = None,
                 base = None,
                 parallelAxis = None,
                 tipPos = None,
                 ctrlTip =ct.SQUARE,
                 ctrlMid = ct.SQUARE,
                 ctrlBase =ct.SQUARE,
                 ctrlDetails = ct.CIRCLEPLUS,
                 ctrlColor=None,
                 prefix='prefix',
                 side=None,
                 scale=None,
                 volumePosMin=None,
                 volumePosMax=None,
                 numJoints=None):

        """
        :param detailLimbDeformer     : bool, create deformer setup on detail
        :param createCtrl   : bool, parameters for creating the control module and tip
        :param tip          : str, transform or joint as the tip of detail
        :param base         : str, transform or joint as the module of detail
        :param parallelAxis : str, two point parallel position direction whether on x or y or z axis
        :param tipPos       : str, + if module seeing the tip with parallel with axis, - + if module seeing the tip with parallel opposite with axis
        :param ctrlTip      : var, ctrl shape of tip
        :param ctrlMid      : var, ctrl shape of middle
        :param ctrlBase     : var, ctrl shape of module
        :param ctrlTip      : var, ctrl shape of detail detail ctrl
        :param prefix       : str, prefix name for detail
        :param numJoints    : int, number of joint as well as the control of detail part
        """
        # Width plane variable (following the number of joints
        size = float(numJoints)

        # Tip point dictionary towards
        tipPoint = {'+': [(size / 2.0 * -1) * scale, (size / 2.0)*scale],
                    '-': [(size / 2.0)*scale, (size / 2.0 * -1)*scale]}

        if tipPos in tipPoint.keys():
            self.pos       = (0,0,0)
            self.upPoint   = tipPoint[tipPos][0]
            self.downPoint = tipPoint[tipPos][1]
        else:
            raise mc.error('The string %s in tipPos argument is not found. Fill with + or -' % tipPos)

        # Dictionary list
        tmpPlaneDic ={'x': [(0,1,0), size*scale, (1.0 / size), numJoints, 1],
                      'y': [(1,0,0), 1*scale, size, 1, numJoints],
                      'z': [(0,1,0), 1*scale, size, 1, numJoints]}

        direction = {'x': ['.rotateY', 90, '.translateZ'],
                     'y': ['.rotateZ', 90, '.translateZ'],
                     'z': ['.rotateX', 0, '.translateX']}

        if tipPos=='-':
            rotDefomer = {'x': (0, 0,-90),
                          'y': (0, 0, 0),
                          'z': (-90, 0, 90)}
        if tipPos == '+':
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
        self.grpTransformZro   = mc.group(empty=True, name=(prefix + 'Transform' + side + '_grp'))
        self.grpTransform      = mc.group(empty=True, name=(prefix + 'TransformOffset'+side +'_grp'))
        self.grpCtrl           = mc.duplicate(self.grpTransform, name=(prefix + 'Ctrl'+side +'_grp'))
        self.grpJntCluster     = mc.duplicate(self.grpTransform, name=(prefix + 'JntCluster'+side +'_grp'))
        self.grpNoTransform    = mc.duplicate(self.grpTransformZro, name=(prefix + 'NoTransformOffset' + side + '_grp'))
        self.grpNoTransformZro = mc.duplicate(self.grpTransformZro, name=(prefix + 'NoTransform' + side + '_grp'))
        self.grpSurface        = mc.duplicate(self.grpTransformZro, name=(prefix + 'Surface' + side + '_grp'))
        self.grpMisc           = mc.duplicate(self.grpTransformZro, name=(prefix + 'Misc' + side + '_grp'))
        self.grpSurfaces       = mc.duplicate(self.grpTransformZro, name=(prefix + 'Surfaces' + side + '_grp'))
        self.grpFollMain       = mc.duplicate(self.grpTransformZro, name=(prefix + 'FolliclesSkin' + side + '_grp'))
        self.grpFollMOff       = mc.duplicate(self.grpTransformZro, name=(prefix + 'FolliclesSkinOffset' + side + '_grp'))

        mc.setAttr(self.grpFollMOff[0] + '.it', 0, l=1)
        mc.setAttr(self.grpNoTransformZro[0] + '.it', 0, l=1)
        mc.setAttr(self.grpTransformZro + '.it', 0, l=1)

        # Create a NURBS-plane to use as a module
        tmpPlane = mc.nurbsPlane(axis=tmpPlaneDic[parallelAxis][0], width=tmpPlaneDic[parallelAxis][1],
                                 lengthRatio=tmpPlaneDic[parallelAxis][2], u=tmpPlaneDic[parallelAxis][3],
                                 v=tmpPlaneDic[parallelAxis][4], degree=3, ch=0)[0]

        # Create the NURBS-planes to use in the setup
        geoPlane       = mc.duplicate(tmpPlane, name=(prefix + side+'_geo'))
        geoPlaneWire   = mc.duplicate(tmpPlane, name=(prefix + 'WireDef'+side +'_geo'))
        geoPlaneOrient = mc.duplicate(tmpPlane, name=(prefix +  'OrientDef'+side +'_geo'))

        # Create Joint reference
        mc.select(cl=1)
        jointCreate = mc.joint(radius=scale / 5)

        # Duplicate joint from reference for skinning to the wire curve
        self.jointUp   = mc.duplicate(jointCreate, n=prefix +'Up'+side +'_jnt')
        self.jointMid  = mc.duplicate(jointCreate, n=prefix + 'Mid'+side +'_jnt')
        self.jointDown = mc.duplicate(jointCreate, n=prefix + 'Down'+side +'_jnt')

        # Set the position for joints
        mc.setAttr((self.jointUp[0] + '.translate'), self.upPoint, self.pos[1], self.pos[2])
        mc.setAttr((self.jointMid[0] + '.translate'), self.pos[0], self.pos[1], self.pos[2])
        mc.setAttr((self.jointDown[0] + '.translate'), self.downPoint, self.pos[1], self.pos[2])

        # Grouping the joints to have rotation according to parallel axis
        grpJointOrient = mc.group(self.jointUp[0], self.jointMid[0], self.jointDown[0])

        # Set the rotation group joints
        if parallelAxis == 'z':
            mc.setAttr((grpJointOrient + '.rotate'), 0, -90, 0)
        if parallelAxis == 'y':
            mc.setAttr((grpJointOrient + '.rotate'), 0, 0, 90)

        # Unparent from the group
        mc.parent(self.jointUp[0], self.jointMid[0], self.jointDown[0], w=1)

        # Create Group for joints wire curve
        self.jointUpParent   = tr.create_parent_transform(['Zro'], self.jointUp[0], self.jointUp[0])
        self.jointMidParent  = tr.create_parent_transform(['Zro'], self.jointMid[0], self.jointMid[0])
        self.jointDownParent = tr.create_parent_transform(['Zro'], self.jointDown[0], self.jointDown[0])

        # Create the controllers
        self.ctrlUp   = ct.Control(match_obj_first_position=self.jointUpParent[0], prefix=prefix + 'Up' + side, groups_ctrl=['Zro', 'Offset', 'Twist', 'Rotation'],
                                   ctrl_size=scale * 0.7, ctrl_color=ctrlColor, shape=ctrlTip)
        self.ctrlMid  = ct.Control(match_obj_first_position=self.jointMidParent[0], prefix=prefix + 'Mid' + side, groups_ctrl=['Zro', 'Aim'],
                                   ctrl_color='blue', ctrl_size=scale * 0.7, shape=ctrlMid)
        self.ctrlDown = ct.Control(match_obj_first_position=self.jointDownParent[0], prefix=prefix + 'Down' + side, groups_ctrl=['Zro', 'Offset', 'Twist'],
                                   ctrl_size=scale * 0.7, ctrl_color=ctrlColor, shape=ctrlBase)

        # control up
        self.upCtrlAimGrp = mc.group(empty=True, n=prefix+'UpAim'+side +'_grp')
        mc.delete(mc.parentConstraint(self.ctrlUp.control, self.upCtrlAimGrp))
        mc.parent(self.upCtrlAimGrp, self.ctrlUp.control)
        duplUpCtrlAimGrp = mc.duplicate(self.upCtrlAimGrp)
        self.upCtrlWorldOffGrp = mc.rename(duplUpCtrlAimGrp, (prefix+'UpAimWorld'+side +'_grp'))
        mc.setAttr(self.upCtrlWorldOffGrp+'.translateZ', -1)

        # control mid
        self.midCtrlWorldOffGrp = mc.group(empty=True, n=prefix + 'MidAimWorld'+side +'_grp')
        mc.delete(mc.parentConstraint(self.ctrlMid.parent_control[0], self.midCtrlWorldOffGrp))
        mc.parent(self.midCtrlWorldOffGrp, self.ctrlMid.parent_control[0])
        mc.setAttr(self.midCtrlWorldOffGrp + '.translateZ', -1)

        # control down
        self.downCtrlAimGrp = mc.group(empty=True, n=prefix + 'DownAim'+side +'_grp')
        mc.delete(mc.parentConstraint(self.ctrlDown.control, self.downCtrlAimGrp))
        mc.parent(self.downCtrlAimGrp, self.ctrlDown.control)
        duplDownCtrlAimGrp = mc.duplicate(self.downCtrlAimGrp)
        self.downCtrlWorldOffGrp = mc.rename(duplDownCtrlAimGrp, (prefix + 'DownAimWorld'+side +'_grp'))
        mc.setAttr(self.downCtrlWorldOffGrp + '.translateZ', -1)

        # Get part joint position
        self.jointRefUp = mc.duplicate(self.jointUp[0], n=prefix + 'Up'+side +'_jnt')
        self.jointRefDown = mc.duplicate(self.jointDown[0], n=prefix + 'Down'+side +'_jnt')

        # Unparent joint duplicate
        mc.parent(self.jointRefUp, self.jointRefDown, w=True)

        # Create joint on evenly position
        positionUVFol = cr.split_evenly(self.jointRefUp, self.jointRefDown, prefix, side=side, split=numJoints, base_tip=True)

        # Create deformers: Wire deformer
        deformCrv = mc.curve(p=[(self.downPoint, 0, 0), (0, 0, 0), (self.upPoint, 0, 0)], degree=2)
        deformCrv = mc.rename(deformCrv, (prefix + 'Wire'+side +'_crv'))

        # Set orient curve
        mc.delete(mc.orientConstraint(grpJointOrient, deformCrv))
        wireDef = mc.wire(geoPlaneWire, dds=(0, 100*scale), wire=deformCrv)
        wireDef[0] = mc.rename(wireDef[0], (au.prefix_name(geoPlaneWire[0]) + side + '_wireNode'))

        # Skining joints to curve
        mc.skinCluster([self.jointUp[0], self.jointMid[0], self.jointDown[0]], deformCrv,
                       n='wireSkinCluster', tsb=True, bm=0, sm=0, nw=1, mi=1)

        # Point constraining the the controller transform to the joint wire curve
        mc.parentConstraint(self.ctrlUp.control, self.jointUpParent[0])
        mc.parentConstraint(self.ctrlMid.control, self.jointMidParent[0])
        mc.parentConstraint(self.ctrlDown.control, self.jointDownParent[0])

        # Create deformers: Blendshape
        dtlBlendshp = mc.blendShape(geoPlaneWire[0], geoPlane[0], name=(prefix + side + '_bsn'), weight=[(0, 1)])

        # Create follicles: The main-surface and the volume-surface
        follicleS = self.itemFollicle(positionUVFol, geoPlane, 'fol')

        # Scaling the follicle with decompose matrix
        decomposeMtxNode = mc.createNode('decomposeMatrix', n=prefix + 'DtlScaleFol'+side +'_dmtx')
        mc.connectAttr(self.grpTransform + '.worldMatrix[0]', decomposeMtxNode + '.inputMatrix')

        # Grouping listing of the follicle parent group
        follicleCtrlGrp       = []
        self.follicleGrpOff        = []
        self.follicleGrpTwist = []

        for folS in (follicleS['follicle']):
            mc.connectAttr(decomposeMtxNode + '.outputScale', folS + '.scale')

            # Listing the shape of follicles
            folLr = mc.listRelatives(folS, s=1)[0]
            mc.setAttr(folLr + '.visibility', 0)

            # Parenting the follicles to grp follicle
            mc.parent(folS, self.grpFollMOff)

            # Create group offset for follilce
            follicleGrpOffset = mc.group(empty=True, name='%s_%s' % (au.prefix_name(folS), 'setGrp'))
            mc.delete(mc.parentConstraint(folS, follicleGrpOffset))
            self.follicleGrpOff.append(follicleGrpOffset)

            # Create offset group follicle
            follicleGrpOffset = mc.parent(follicleGrpOffset, folS)

            # Create a joint, controller and a group for the current skin-follicle
            mc.select(clear=True)

            # Create joint for follicle
            follicleJoint = mc.joint(name='%s_%s' % (au.prefix_name(folS), 'jnt'), radius=1.0)

            # Create control for joint in follicle
            follicleCtrl  = ct.Control(prefix=au.prefix_name(folS), groups_ctrl=['Zro', 'Twist', 'Offset'],
                                       ctrl_color=ctrlColor, ctrl_size=scale * 0.65, shape=ctrlDetails)
            follicleCtrlGrp.append(follicleCtrl.parent_control[0])
            self.follicleGrpTwist.append(follicleCtrl.parent_control[1])

            # Parent joint to controller
            mc.parent(follicleJoint, follicleCtrl.control)

            # Positioning skin-follicle control
            mc.delete(mc.parentConstraint(self.ctrlMid.control, follicleCtrl.parent_control[0]))
            mc.delete(mc.pointConstraint(follicleGrpOffset, follicleCtrl.parent_control[0]))

            # Parent controller to group offset follicle
            mc.parent(follicleCtrl.parent_control[0], follicleGrpOffset)

            # hide joint
            mc.setAttr(follicleJoint+'.visibility', 0)

    # ==================================================================================================================
    #                                               IF DEFORM TRUE
    # ==================================================================================================================
        if detailLimbDeformer:
            self.grpDeformers  = mc.duplicate(self.grpTransformZro, name=(prefix + 'Deformer' + side + '_grp'))
            self.grpFollVolume = mc.duplicate(self.grpTransformZro, name=(prefix + 'FolliclesVolume' + side + '_grp'))

            geoPlaneVolume = mc.duplicate(tmpPlane, name=(prefix + 'Volume'+side +'_geo'))
            geoPlaneTwist  = mc.duplicate(tmpPlane, name=(prefix + 'TwistDef'+side +'_geo'))
            geoPlaneSine   = mc.duplicate(tmpPlane, name=(prefix + 'SineDef'+side +'_geo'))

            # Offset the volume-plane
            mc.setAttr((geoPlaneVolume[0] + direction[parallelAxis][2]), -0.5*scale)

            # Add attributes: Twist/Roll attributes
            self.addAttribute(objects=[self.ctrlDown.control, self.ctrlMid.control, self.ctrlUp.control],
                              longName=['twistSep'], niceName=[' '], at="enum", en='Twist', cb=True)

            self.addAttribute(objects=[self.ctrlDown.control, self.ctrlUp.control], longName=['twist'], at="float", k=True)
            self.addAttribute(objects=[self.ctrlDown.control, self.ctrlUp.control], longName=['twistOffset'], at="float", k=True)
            self.addAttribute(objects=[self.ctrlDown.control, self.ctrlUp.control], longName=['affectToMid'], at="float", min=0,
                              max=10, dv=10, k=True)

            # Add attributes: Twist/Roll attributes parent
            self.addAttribute(objects=[self.ctrlDown.parent_control[2], self.ctrlUp.parent_control[2]], longName=['twist'], at="float", k=True)
            self.addAttribute(objects=[self.ctrlDown.parent_control[2], self.ctrlUp.parent_control[2]], longName=['twistOffset'], at="float", k=True)
            self.addAttribute(objects=[self.ctrlDown.parent_control[2], self.ctrlUp.parent_control[2]], longName=['affectToMid'], at="float", k=True)

            # connected twist controller to parent controller
            mc.connectAttr(self.ctrlUp.control +'.twist', self.ctrlUp.parent_control[2] + '.twist')
            mc.connectAttr(self.ctrlUp.control +'.twistOffset', self.ctrlUp.parent_control[2] + '.twistOffset')
            mc.connectAttr(self.ctrlUp.control +'.affectToMid', self.ctrlUp.parent_control[2] + '.affectToMid')

            mc.connectAttr(self.ctrlDown.control +'.twist', self.ctrlDown.parent_control[2] + '.twist')
            mc.connectAttr(self.ctrlDown.control +'.twistOffset', self.ctrlDown.parent_control[2] + '.twistOffset')
            mc.connectAttr(self.ctrlDown.control +'.affectToMid', self.ctrlDown.parent_control[2] + '.affectToMid')

            # add attribute twist mid controller
            self.addAttribute(objects=[self.ctrlMid.control], longName=['roll'], at="float", k=True)
            self.addAttribute(objects=[self.ctrlMid.control], longName=['rollOffset'], at="float", k=True)

            # Add attributes: Volume attributes
            self.addAttribute(objects=[self.ctrlMid.control], longName=['volumeSep'], niceName=[' '], at="enum",
                              en='Volume', cb=True)

            self.addAttribute(objects=[self.ctrlMid.control], longName=['volume'], at="float", min=-1, max=1, k=True)
            self.addAttribute(objects=[self.ctrlMid.control], longName=['volumeMultiplier'], at="float", min=1, dv=3, k=True)
            self.addAttribute(objects=[self.ctrlMid.control], longName=['startDropoff'], at="float", min=0, max=1, dv=1,
                              k=True)
            self.addAttribute(objects=[self.ctrlMid.control], longName=['endDropoff'], at="float", min=0, max=1, dv=1,
                              k=True)
            self.addAttribute(objects=[self.ctrlMid.control], longName=['volumeScale'], at="float", min=self.upPoint * 0.9,
                              max=self.downPoint * 2, k=True)
            self.addAttribute(objects=[self.ctrlMid.control], longName=['volumePosition'], min=volumePosMin * self.upPoint,
                              max=volumePosMax * self.downPoint, at="float", k=True)

            # Add attributes: Sine attributes
            self.addAttribute(objects=[self.ctrlMid.control], longName=['sineSep'], niceName=[' '], attributeType='enum',
                              en="Sine:", cb=True)

            self.addAttribute(objects=[self.ctrlMid.control], longName=['amplitude'], attributeType="float", k=True)
            self.addAttribute(objects=[self.ctrlMid.control], longName=['wide'], attributeType="float", k=True)
            self.addAttribute(objects=[self.ctrlMid.control], longName=['sineRotate'], attributeType="float", k=True)
            self.addAttribute(objects=[self.ctrlMid.control], longName=['offset'], attributeType="float", k=True)
            self.addAttribute(objects=[self.ctrlMid.control], longName=['twist'], attributeType="float", k=True)
            self.addAttribute(objects=[self.ctrlMid.control], longName=['sineLength'], min=0.1, dv=2, attributeType="float",
                              k=True)

            # Create deformers: Twist deformer, Sine deformer, Squash deformer
            # Set them rotation  according on point parallelFaceAxis position
            self.twistDef  = self.nonlinearDeformer(objects=[geoPlaneTwist[0]], defType='twist',
                                                    name=au.prefix_name(geoPlaneTwist[0]), lowBound=-1,
                                                    highBound=1, rotate=rotDefomer[parallelAxis])

            self.sineDef   = self.nonlinearDeformer(objects=[geoPlaneSine[0]], defType='sine',
                                                    name=au.prefix_name(geoPlaneSine[0]), lowBound=-1,
                                                    highBound=1, rotate=rotDefomer[parallelAxis])

            self.squashDef = self.nonlinearDeformer(objects=[geoPlaneVolume[0]], defType='squash',
                                                    name=au.prefix_name(geoPlaneVolume[0]), lowBound=-1,
                                                    highBound=1, rotate=rotDefomer[parallelAxis])

            mc.setAttr((self.sineDef[0] + '.dropoff'), 1)

        # Twist deformer: Sum the twist and the roll
            self.sumTopPma = mc.shadingNode('plusMinusAverage', asUtility=1, name=(prefix + 'TwistUpSum'+side +'_pma'))
            mc.connectAttr((self.ctrlDown.parent_control[2] + '.twist'), (self.sumTopPma + '.input1D[0]'))
            mc.connectAttr((self.ctrlDown.parent_control[2] + '.twistOffset'), (self.sumTopPma + '.input1D[1]'))
            mc.connectAttr((self.ctrlMid.control + '.roll'), (self.sumTopPma + '.input1D[2]'))
            mc.connectAttr((self.ctrlMid.control + '.rollOffset'), (self.sumTopPma + '.input1D[3]'))
            mc.connectAttr((self.sumTopPma + '.output1D'), (self.twistDef[0] + '.startAngle'))

            self.sumEndPma = mc.shadingNode('plusMinusAverage', asUtility=1, name=(prefix + 'TwistDownSum'+side +'_pma'))
            mc.connectAttr((self.ctrlUp.parent_control[2] + '.twist'), (self.sumEndPma + '.input1D[0]'))
            mc.connectAttr((self.ctrlUp.parent_control[2] + '.twistOffset'), (self.sumEndPma + '.input1D[1]'))
            mc.connectAttr((self.ctrlMid.control + '.roll'), (self.sumEndPma + '.input1D[2]'))
            mc.connectAttr((self.ctrlMid.control + '.rollOffset'), (self.sumEndPma + '.input1D[3]'))
            mc.connectAttr((self.sumEndPma + '.output1D'), (self.twistDef[0] + '.endAngle'))

        # Twist deformer: Set up the affect of the deformer
            topAffMdl = mc.shadingNode('multDoubleLinear', asUtility=1, name=(prefix + 'TwistUpAffect'+side +'_mdl'))
            mc.setAttr((topAffMdl + '.input1'), -0.1)
            mc.connectAttr((self.ctrlDown.parent_control[2] + '.affectToMid'), (topAffMdl + '.input2'))
            mc.connectAttr((topAffMdl + '.output'), (self.twistDef[0] + '.lowBound'))

            endAffMdl = mc.shadingNode('multDoubleLinear', asUtility=1, name=(prefix + 'TwistDownAffect'+side +'_mdl'))
            mc.setAttr((endAffMdl + '.input1'), 0.1)
            mc.connectAttr((self.ctrlUp.parent_control[2] + '.affectToMid'), (endAffMdl + '.input2'))
            mc.connectAttr((endAffMdl + '.output'), (self.twistDef[0] + '.highBound'))

        # Squash deformer: Set up the connections for the volume control
            self.volumeRevfAdl = mc.createNode('addDoubleLinear',
                                           n='%s%s%s_adl' % (prefix, 'CombineVolumeReverse', side))
            mc.connectAttr((self.ctrlMid.control + '.volume'), (self.volumeRevfAdl + '.input2'))
            volumeRevfMdl = mc.shadingNode('multDoubleLinear', asUtility=1, name=(prefix + 'VolumeReverse'+side +'_mdl'))
            mc.setAttr((volumeRevfMdl + '.input1'), -1)
            mc.connectAttr((self.volumeRevfAdl+'.output'), (volumeRevfMdl + '.input2'))
            mc.connectAttr((volumeRevfMdl + '.output'), (self.squashDef[0] + '.factor'))
            mc.connectAttr((self.ctrlMid.control + '.startDropoff'), (self.squashDef[0] + '.startSmoothness'))
            mc.connectAttr((self.ctrlMid.control + '.endDropoff'), (self.squashDef[0] + '.endSmoothness'))

            # Set the translate squash deformer according the point parallelFaceAxis position
            self.combineVolPosAdl = mc.createNode('addDoubleLinear',
                                           n='%s%s%s_adl' % (prefix, 'CombineVolumePos', side))
            mc.connectAttr((self.ctrlMid.control + '.volumePosition'), (self.combineVolPosAdl + '.input2'))
            mc.connectAttr((self.combineVolPosAdl + '.output'), (self.squashDef[1] + volInputMdn[parallelAxis][0]))

        # Squash deformer: Set up the volume scaling
            sumScalePma = mc.shadingNode('plusMinusAverage', asUtility=1, name=(prefix + 'VolumeScaleSum'+side +'_pma'))
            mc.setAttr((sumScalePma + '.input1D[0]'), self.downPoint)
            mc.connectAttr((self.ctrlMid.control + '.volumeScale'), (sumScalePma + '.input1D[1]'))
            mc.connectAttr((sumScalePma + '.output1D'), (self.squashDef[1] + '.scaleY'))

        # Sine deformer: Set up the connections for the sine

            # combine sine amplitude
            self.combineSineAmplitude = mc.createNode('addDoubleLinear', n=(prefix + 'CombineSineAmplitude' + side + '_adl'))
            mc.connectAttr(self.ctrlMid.control + '.amplitude', self.combineSineAmplitude + '.input2')
            mc.connectAttr((self.combineSineAmplitude + '.output'), (self.sineDef[0] + '.amplitude'))

            # combine sine offset
            self.combineSineOffset = mc.createNode('addDoubleLinear', n=(prefix + 'CombineSineOffset' + side + '_adl'))
            mc.connectAttr(self.ctrlMid.control + '.offset', self.combineSineOffset + '.input2')
            mc.connectAttr((self.combineSineOffset + '.output'), (self.sineDef[0] + '.offset'))

            # combine sine wide
            self.combineSineWide = mc.createNode('addDoubleLinear', n=(prefix + 'CombineSineWide' + side + '_adl'))
            mc.connectAttr(self.ctrlMid.control + '.wide', self.combineSineWide + '.input2')
            sineWideNode = mc.createNode('addDoubleLinear', n=(prefix + 'AdjustSineWide' + side + '_adl'))
            mc.setAttr(sineWideNode + '.input1', 2.5)
            mc.connectAttr(self.combineSineWide  + '.output', sineWideNode + '.input2')
            mc.connectAttr(sineWideNode + '.output', self.sineDef[1] + '.scaleY')

            # Sine Exception for z parallel axis
            if parallelAxis == 'z':
                # combine sine rotation
                self.combineSineRotate = mc.createNode('addDoubleLinear', n=(prefix + 'CombineSineRotate'+side +'_adl'))
                mc.connectAttr(self.ctrlMid.control + '.sineRotate', self.combineSineRotate  + '.input2')

                # sine rotation : set the sine rotation
                mc.connectAttr(self.combineSineRotate  + '.output', self.sineDef[1] + '.rotateY')

                # combine sine twist
                self.combineSineTwist = mc.createNode('addDoubleLinear', n=(prefix + 'CombineSineTwist' + side + '_adl'))
                mc.connectAttr(self.ctrlMid.control + '.twist', self.combineSineTwist + '.input2')

                sineTwistNode = mc.createNode('addDoubleLinear', n=(prefix + 'AdjustSineTwistRotZ'+side +'_adl'))
                mc.setAttr(sineTwistNode + '.input1', 90)
                mc.connectAttr(self.combineSineTwist + '.output', sineTwistNode + '.input2')
                mc.connectAttr(sineTwistNode + '.output', self.sineDef[1] + '.rotateZ')

            if parallelAxis == 'x':
                # combine sine rotation
                self.combineSineRotate = mc.createNode('addDoubleLinear',
                                                       n=(prefix + 'CombineSineRotate' + side + '_adl'))
                mc.connectAttr(self.ctrlMid.control + '.sineRotate', self.combineSineRotate + '.input2')

                # sine rotation : set the sine rotation
                sineRotateNode = mc.createNode('addDoubleLinear', n=(prefix + 'AdjustSineRotate'+side +'_adl'))
                mc.setAttr(sineRotateNode + '.input1', 90)
                mc.connectAttr(self.combineSineRotate + '.output', sineRotateNode + '.input2')
                mc.connectAttr(sineRotateNode + '.output', self.sineDef[1] + '.rotateZ')

                # sine twist
                self.combineSineTwist = mc.createNode('addDoubleLinear',
                                                      n=(prefix + 'CombineSineTwist' + side + '_adl'))

                mc.connectAttr(self.ctrlMid.control + '.twist', self.combineSineTwist + '.input2')
                mc.connectAttr(self.combineSineTwist + '.output', self.sineDef[1] + '.rotateY')

            if parallelAxis == 'y':
                # combine sine rotation
                self.combineSineRotate = mc.createNode('addDoubleLinear',
                                                       n=(prefix + 'CombineSineRotate' + side + '_adl'))
                mc.connectAttr(self.ctrlMid.control + '.sineRotate', self.combineSineRotate + '.input2')

                # sine rotation : set the sine rotation
                sineRotateNode = mc.createNode('addDoubleLinear', n=(prefix + 'AdjustSineRotate' + side + '_adl'))
                mc.setAttr(sineRotateNode + '.input1', 0)
                mc.connectAttr(self.combineSineRotate + '.output', sineRotateNode + '.input2')
                mc.connectAttr(sineRotateNode + '.output', self.sineDef[1] + '.rotateZ')

                # sine twist
                self.combineSineTwist = mc.createNode('addDoubleLinear',
                                                      n=(prefix + 'CombineSineTwist' + side + '_adl'))

                mc.connectAttr(self.ctrlMid.control + '.twist', self.combineSineTwist + '.input2')
                mc.connectAttr(self.combineSineTwist + '.output', self.sineDef[1] + '.rotateY')

            # sine length combine
            self.combineSineLength = mc.createNode('multDoubleLinear',
                                                          n=(prefix + 'CombineSineLength' + side + '_adl'))
            mc.connectAttr(self.ctrlMid.control + '.sineLength', self.combineSineLength + '.input2')
            mc.connectAttr(self.combineSineLength + '.output', self.sineDef[0] + '.wavelength')

        # Create deformers: Blendshape
            mc.blendShape(dtlBlendshp, e=1, t=(geoPlane[0], 1, geoPlaneTwist[0], 1.0))
            mc.blendShape(dtlBlendshp, e=1, t=(geoPlane[0], 2, geoPlaneSine[0], 1.0))

            mc.blendShape(dtlBlendshp, e=True, w=[(1, 1.0), (2, 1.0)])

            # Create follicles: The main-surface and the volume-surface
            follicleV = self.itemFollicle(positionUVFol, geoPlaneVolume, 'Volumefol')

            # Set the follicle U and V parameter
            for obj in follicleV['follicle']:
                mc.setAttr(obj + follicleVol[parallelAxis][0], follicleVol[parallelAxis][1])

            # list node combine multiply
            self.combineMultMpdAll = []

            # Looping the follicle S and follicle V
            for folV, folGrpOffst in zip(follicleV['follicle'], self.follicleGrpOff):
                # combine multiplier
                combineMultMpd = mc.shadingNode('multDoubleLinear', asUtility=1, name=au.prefix_name(folV)[:-3] + 'CombineMultiplier' + side + '_mdn')
                mc.connectAttr((self.ctrlMid.control + '.volumeMultiplier'), combineMultMpd+'.input1')

                # make list combine multiplier
                self.combineMultMpdAll.append(combineMultMpd)

                # Make the connections for the volume according on point parallelFaceAxis position
                multMpd = mc.shadingNode('multiplyDivide', asUtility=1, name=au.prefix_name(folV)[:-3] + 'Multiplier' + side + '_mdn')
                mc.connectAttr((combineMultMpd + '.output'), volInputMdn[parallelAxis][1])
                #mc.connectAttr((self.ctrlMid.control + '.volumeMultiplier'), volInputMdn[parallelAxis][1])
                mc.connectAttr((folV + '.translate'), (multMpd + '.input2'))

                sumPma = mc.shadingNode('plusMinusAverage', asUtility=1, name=au.prefix_name(folV)[:-3] + 'VolumeSum' + side + '_pma')
                mc.connectAttr((multMpd + volInputMdn[parallelAxis][2]), (sumPma + '.input1D[0]'))
                mc.setAttr((sumPma + '.input1D[1]'), 1)
                mc.connectAttr((sumPma + '.output1D'), (folGrpOffst + volInputMdn[parallelAxis][3]))
                mc.connectAttr((sumPma + '.output1D'), (folGrpOffst + volInputMdn[parallelAxis][4]))

            # Cleanup: Hierarchy
            mc.parent(self.twistDef[1], self.sineDef[1], self.squashDef[1], self.grpDeformers)
            mc.parent(geoPlaneTwist[0], geoPlaneSine[0], geoPlaneVolume[0], self.grpSurfaces)
            mc.parent(follicleV['follicle'], self.grpFollVolume)
            mc.parent(self.grpDeformers[0], self.grpFollVolume[0], self.grpNoTransform)

        # Add attributes: Extra attributes
        self.addAttribute(objects=[self.ctrlMid.control], longName=['extraSep'], niceName=[' '], at="enum", en='Extra',
                          cb=True)
        self.addAttribute(objects=[self.ctrlMid.control], longName=['detailCtrlVis'], at="long", min=0, max=1, dv=0,
                          cb=True)

        # connect the visibility-switch for the controller
        mc.connectAttr((self.ctrlMid.control + '.detailCtrlVis'),
                       (self.grpFollMOff[0] + '.visibility'))

        # Cleanup: Hierarchy
        mc.delete(mc.parentConstraint(base, tip, self.grpTransform))
        mc.delete(mc.orientConstraint(tmpPlane, self.grpTransformZro))
        mc.delete(mc.parentConstraint(base, tip, self.grpTransformZro))

        mc.parent(geoPlaneOrient[0], self.grpSurfaces)
        mc.parent(self.jointUpParent[0], self.jointMidParent[0], self.jointDownParent[0], self.grpJntCluster)
        mc.parent(self.ctrlDown.parent_control[0], self.ctrlMid.parent_control[0], self.ctrlUp.parent_control[0], self.grpCtrl)
        mc.parent(geoPlane[0], geoPlaneWire[0], (mc.listConnections(wireDef[0] + '.baseWire[0]')[0]), self.grpSurface)
        mc.parent(deformCrv, self.grpMisc)
        mc.parent(self.grpJntCluster, self.grpSurfaces[0], self.grpMisc[0], self.grpNoTransform)
        mc.parent(self.grpCtrl[0], self.grpSurface[0], self.grpFollMain[0], self.grpTransform)
        mc.parent(self.grpFollMOff[0], self.grpFollMain[0])
        mc.parent(self.grpTransform,  self.grpTransformZro)
        mc.parent(self.grpNoTransform[0],self.grpNoTransformZro[0])

        # Match position with the module and tip joint
        mc.delete(mc.parentConstraint(base, self.ctrlUp.parent_control[0]))
        mc.delete(mc.pointConstraint(tip, self.ctrlDown.parent_control[0]))
        mc.delete(mc.orientConstraint(base, self.ctrlDown.parent_control[0]))
        mc.delete(mc.parentConstraint(tip, self.ctrlDown.parent_control[0], mo=1))
        mc.delete(mc.parentConstraint(self.ctrlUp.parent_control[0], self.ctrlDown.parent_control[0], self.ctrlMid.parent_control[0]))

        # aim contraint for ctrl
        mc.aimConstraint(self.ctrlUp.control, self.downCtrlAimGrp, mo=1, w=1, aim=(0,-1, 0), u= (0,0,-1), wut='objectrotation',
                         wu= (0,0,-1), wuo=self.downCtrlWorldOffGrp)

        mc.aimConstraint(self.ctrlDown.control, self.upCtrlAimGrp, mo=1, w=1, aim=(0, 1, 0), u= (0,0,-1), wut='objectrotation',
                         wu= (0,0,-1), wuo=self.upCtrlWorldOffGrp)

        mc.aimConstraint(self.ctrlDown.control, self.ctrlMid.parent_control[1], mo=1, w=1,
                         aim=(0, -1, 0), u= (0,0,-1), wut='objectrotation', wu= (0,0,-1), wuo=self.midCtrlWorldOffGrp)

        # point constraint to mid
        mc.pointConstraint(self.ctrlUp.control, self.ctrlDown.control, self.ctrlMid.parent_control[0], mo=1)

        # Match the orientation of group control to the middle control detail
        for obj in follicleCtrlGrp:
            mc.delete(mc.orientConstraint(self.ctrlMid.control, obj, mo=0))

        # hide the visibility
        mc.hide(self.grpNoTransformZro, self.grpNoTransform, self.grpJntCluster, geoPlaneWire, self.grpSurfaces,
                self.grpSurface, self.grpMisc)

        # Lock unnecesarry key detail
        au.lock_hide_attr(['s'], self.ctrlUp.control)
        au.lock_hide_attr(['s'], self.ctrlMid.control)
        au.lock_hide_attr(['s'], self.ctrlDown.control)

        # Lock some groups
        au.lock_attr(['t', 'r', 's', 'v'], self.grpFollMain[0])
        au.lock_hide_attr(['t', 'r', 's', 'v'], self.grpNoTransformZro[0])
        au.lock_hide_attr(['t', 'r', 's', 'v'], self.grpNoTransform[0])
        au.lock_hide_attr(['t', 'r', 's', 'v'], self.grpJntCluster[0])
        au.lock_hide_attr(['t', 'r', 's', 'v'], self.grpSurfaces[0])
        au.lock_hide_attr(['t', 'r', 's', 'v'], self.grpMisc[0])
        au.lock_hide_attr(['t', 'r', 's', 'v'], geoPlaneWire[0])
        au.lock_hide_attr(['t', 'r', 's', 'v'], (mc.listConnections(wireDef[0] + '.baseWire[0]')[0]))

        if detailLimbDeformer:
            mc.hide(self.grpDeformers, self.grpFollVolume)
            au.lock_hide_attr(['t', 'r', 's', 'v'], self.grpFollVolume[0])
            au.lock_hide_attr(['t', 'r', 's', 'v'], self.grpDeformers[0])

        mc.delete(jointCreate, positionUVFol, self.jointRefUp, self.jointRefDown)

        # Delete the module surface and group rotation driver
        mc.delete(tmpPlane, grpJointOrient)

        # Clear all selection
        mc.select(cl=1)

    # ==================================================================================================================
    #                                               GENERAL FUNCTION
    # ==================================================================================================================
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

        return {'item': items,
                'follicle': fol,
                'folShape': folShp}

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
                    mc.setAttr((obj + '.' + longName[x]), k=k, e=1, cb=cb) if separator else mc.setAttr(
                        (obj + '.' + longName[x]), k=k, e=1, cb=cb)

    # GENERAL FUNCTION: CREATE A NONLINEAR DEFORMER
    def nonlinearDeformer(self, objects=[], defType=None, lowBound=-1, highBound=1, translate=None, rotate=None,
                          name='nonLinear'):

        # If something went wrong or the type is not valid, raise exception
        if not objects or defType not in ['bend', 'flare', 'sine', 'squash', 'twist', 'wave']:
            raise Exception, "function: 'nonlinearDeformer' - Make sure you specified a mesh and a valid deformer"

        # Create and rename the deformer
        nonLinDef    = mc.nonLinear(objects[0], type=defType, lowBound=lowBound, highBound=highBound)
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