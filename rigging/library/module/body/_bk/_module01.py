"""
module for making controller base, setup and base module
"""

import maya.cmds as mc
import rigLib.utils.controller as ct
import rigLib.utils.template_skeleton as tp
from rigLib.rig.body import spine_part_detail as rb, spine as sp

from rigging.tools import AD_utils as au, AD_utils as ut

reload (ct)
reload (ut)
reload (sp)
reload (au)
reload (tp)
reload (rb)

generalScale = 1.0

class GeneralBase:
    #top structure
    def __init__(self,
                lockChannels = ['t','r','s'],
                scale = generalScale
                 ):
        """
        @param lockChannels: str, list attribute channels
        @param scale       : float, scale general all object base
        @return            : None

        """
        # make world control
        worldControl = ct.Control(
                                          prefix='World',
                                          suffix='Ctrl',
                                          groups_ctrl=['Zro'],
                                          ctrl_size=scale * 5,
                                          gimbal=None,
                                          ctrl_color='darkBrown',
                                          lock_channels=['v'],
                                          shape=ct.CIRCLE,
                                          )

        # make placer control
        placeControl = ct.Control(
                                        prefix='Place',
                                        suffix='Ctrl',
                                        groups_ctrl=['Zro'],
                                        ctrl_size=scale * 5,
                                        gimbal = None,
                                        ctrl_color='darkBlue',
                                        lock_channels=['v'],
                                        shape=ct.WORLD,
                                    )

        # create group and parenting corresponding to its grp
        self.rootGrp  = mc.group (n='Rig_Grp', em=1)
        self.worldGrp = mc.group (n='World_Grp', em=1, p=self.rootGrp)
        mc.parent(worldControl.control, self.worldGrp)

        self.placeGrp = mc.group(n='Place_Grp', em=1, p=worldControl.control)
        mc.parent(placeControl.control, self.placeGrp)

        self.animGrp = mc.group(n='anim_grp', em=1, p=placeControl.control)
        self.jntGrp   = mc.group(n='jnt_grp', em=1, p=placeControl.control)

        self.utilGrp  = mc.group(n='Util_Grp', em=1, p=self.worldGrp)


        # deleting grp parent ctrl
        mc.delete(worldControl.parent_control[0])
        mc.delete(placeControl.parent_control[0])

        # create more group for other utilities
        self.animUtilGrp = mc.group(n='AnimUtil_Grp', em=1, p=self.utilGrp)
        self.stillGrp    = mc.group(n='Still_Grp', em=1, p=self.utilGrp)


        self.jointGrp    = mc.group(n='Joints_Grp', em=1, p=self.animUtilGrp)
        self.curveGrp    = mc.group(n='Curve_Grp', em=1, p=self.animUtilGrp)
        self.surfaceGrp  = mc.group(n='Surface_Grp', em=1, p=self.animUtilGrp)
        self.locatorGrp  = mc.group(n='Locator_Grp', em=1, p=self.animUtilGrp)
        self.ikHandleGrp = mc.group(n='IkHandle_Grp', em=1, p=self.animUtilGrp)
        self.clusterGrp  = mc.group(n='Cluster_Grp', em=1, p=self.animUtilGrp)

        self.geoGrp      = mc.group (n='Geo_Grp', em=1, p=self.rootGrp)


        # locking the atributes directories
        ut.lock_hide_attr(lockChannels, self.utilGrp)
        ut.lock_hide_attr(lockChannels, self.jointGrp)
        ut.lock_hide_attr(lockChannels, self.curveGrp)
        ut.lock_hide_attr(lockChannels, self.surfaceGrp)
        ut.lock_hide_attr(lockChannels, self.locatorGrp)
        ut.lock_hide_attr(lockChannels, self.ikHandleGrp)
        ut.lock_hide_attr(lockChannels, self.clusterGrp)


class Base:
    # create  main controller for base part
    def __init__(self,
                 scale = generalScale,
                 ):
        """
        @param scale: float, scale the main controller builder
        @return : None

        """
        animControl = ct.Control(
                                          prefix='anim',
                                          suffix='ctrl',
                                          groups_ctrl=['Zro'],
                                          ctrl_size=scale * 3,
                                          gimbal=True,
                                          ctrl_color='darkGreen',
                                          lock_channels=['v'],
                                          shape=ct.ARROW4STRAIGHT,
                                          )

        self.animControl         = animControl.control
        self.unparentMainControl = mc.parent(animControl.control, w=True)
        self.gimbalControl       = animControl.control_gimbal
        mc.delete(animControl.parent_control[0])

        # adding attribute size to place ctrl
        ut.add_attr_transform(animControl.control, 'size', 'double', dv=1, min=0.1, edit=True, keyable=True)


        # connecting the size attributes to its scale object
        for axis in ['x','y','z']:
            mc.connectAttr(animControl.control+'.size', animControl.control+'.s'+axis)
            mc.setAttr(animControl.control+'.s'+axis, k=0, l=1)

        # adding group for anim control
        self.partGrp = mc.group(n='parts_grp', em=1, p=animControl.control_gimbal)

        # adding group for joint
        self.jntGrp = mc.group(n='jnt_grp', em=1, p=animControl.control_gimbal)

        # adding group for still
        self.stillGrp = mc.group(n='still_grp', em=1, p=animControl.control_gimbal)
        mc.setAttr (self.stillGrp + '.it', 0, l=1)
        au.lock_hide_attr(['t', 'r', 's'], self.stillGrp)


class Part:
    # create part of base group
    def __init__(self,
                 prefix ='prefix',
                 baseObj = None,
                 ):
        """
        :param prefix: str, name of part of limbs
        :param baseObj: instance of the Part class
        :return : None
        """

        self.topGrp       = mc.group(n=prefix + 'Part_grp', em=1)

        self.controlGrp   = mc.group (n=prefix +'Control_grp', em=1, p=self.topGrp)
        self.jointGrp     = mc.group (n=prefix +'Joint_grp', em=1, p=self.topGrp)
        self.locGrp       = mc.group (n=prefix +'Locator_grp', em=1, p=self.topGrp)
        self.utilsGrp     = mc.group (n=prefix +'Utils_grp', em=1, p=self.topGrp)
        self.nonTransform = mc.group (n=prefix +'NonTrans_grp', em=1, p=self.topGrp)

        mc.setAttr (self.nonTransform + '.it', 0, l=1)


        # parent top grp of part class to part group on module instance

        if baseObj:
            mc.parent(self.topGrp, baseObj.partGrp)


class ControlRigSetup:

    def __init__(self,
                 prefix ='spine',
                 size = generalScale):

    ### Check the base exist
        if mc.objExists('anim_ctrl'):
            mc.error('Please rid off the whole old base first! Then continue the script.')

    ### IMPORT BASE RIG MODULE
        base = Base(scale=size)

    ### DUPLICATE TMP JNT GRP
        sj = tp.list_skeleton_dic(obj_duplicate='root_tmpJnt', value_prefix='Driver', suffix='jnt', selection=False)

        mc.parent(sj['root_jnt'], base.jntGrp)
        mc.setAttr('tmpJnt_grp.visibility', 0)

    ### IMPORT SPINE MODULE
        spineList  = [sj['spine1_jnt'], sj['spine2_jnt'], sj['spine3_jnt'], sj['spine4_jnt']]
        buildSpine = sp.Build(
                     spine_jnt= spineList,
                     pelvis_jnt= sj['pelvis_jnt'],
                     root_jnt= sj['root_jnt'],
                     scale    =size * 2.0)

        part = Part(prefix=prefix, baseObj= base)

        # parent root to part control group
        mc.parent(buildSpine.controller_root.parentControl[0], part.controlGrp)

        # parent spine setup controller to part control group
        mc.parent(buildSpine.controller_FkIk_spine_setup.parentControl[0], part.controlGrp)

        # constraint the root joint to spine controller setup
        mc.parentConstraint(sj['root_jnt'], buildSpine.controller_FkIk_spine_setup.parentControl[0])

        # parent all spine to module jnt grp
        mc.parent(spineList, base.jntGrp)

        # grouping spine 01 - 03
        grpJntSpine = []
        for i in spineList[0:3]:
            grpJntSpine.extend(au.group_object(['Zro'], i, i))

        ## IMPORT RIBBON SPINE MODULE
        ribbonSpine = rb.CreateDetail(pelvisCtrl      = buildSpine.controller_pelvis.controlGimbal,
                                      anim_ctrl= base.animControl,
                                      grpJntSpine     = grpJntSpine,
                                      list_spine_jnt= [sj['root_jnt'], sj['spine1_jnt'],
                                                       sj['spine2_jnt'], sj['spine3_jnt'], sj['spine4_jnt']],

                                      list_spine_ctrl_fk= [buildSpine.controller_spine_fk_low.controlGimbal,
                                                           buildSpine.controller_spine_fk_mid.controlGimbal,
                                                           buildSpine.controller_spine_fk_up.controlGimbal],

                                      list_spine_ctrl_ik= [buildSpine.controller_spine_ik_low.controlGimbal,
                                                           buildSpine.controller_spine_ik_up.controlGimbal],

                                      FkIk_switch= buildSpine.controller_FkIk_spine_setup.control,
                                      prefix          = prefix,
                                      ctrl_mid= buildSpine.controllerFlexSpineSetup.control,
                                      scale           = size,
                                      numJoints       = 3)

        # Parent ribbon spine to still grp
        mc.parent(ribbonSpine.grp_all_detail, base.stillGrp)



