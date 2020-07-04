import generalModule as gm
import maya.cmds as mc
from rigLib.rig.body import spine_part_detail as rb, spine as sp
from rigLib.utils import controller as ct

from rigging.tools import AD_utils as au

reload(gm)
reload(ct)
reload(sp)
reload(au)
reload(rb)

generalScale = 1.0

class Spine:
    def __init__(self,
                 prefix,
                 prefixSpineSetup,
                 base,
                 spineJnt,
                 pelvisJnt,
                 rootJnt,
                 parentJnt,
                 detailSpineDeformer=True,
                 size= generalScale):

        self.spineList = spineJnt

        # parent Jnt driver to module jntGrp
        mc.parent(parentJnt, base.jntGrp)

        # set tmpJnt gpr to 0
        mc.setAttr('tmpJnt_grp.visibility', 0)

    ### IMPORT SPINE MODULE
        buildSpine = sp.Build(
                     spine_jnt= spineJnt,
                     pelvis_jnt= pelvisJnt,
                     root_jnt= rootJnt,
                     prefix_spine_setup= prefixSpineSetup,
                     detail_spine_deformer= detailSpineDeformer,
                     scale            = size * 2.0)

        # instance the objects
        self.rootControllerGrpZro       = buildSpine.controller_root.parentControl[0]
        self.fkIkSpineControllerGrpZro  = buildSpine.controller_FkIk_spine_setup.parentControl[0]

        # build part of group hierarchy
        part = gm.Part(prefix=prefix, baseObj= base)

        # parent some controls setup to part group
        # controller
        mc.parent(self.rootControllerGrpZro, part.controlGrp)
        mc.parent(self.fkIkSpineControllerGrpZro, part.controlGrp)

        # constraint the root joint to spine controller setup
        mc.parentConstraint(rootJnt, self.fkIkSpineControllerGrpZro)

        # parent all spine to module jnt grp
        mc.parent(spineJnt, base.jntGrp)

        ctrlMid = None
        if detailSpineDeformer :
            ctrlMid = buildSpine.controller_FkIk_spine_setup.control
        else:
            ctrlMid = ctrlMid

        ## IMPORT DETAIL SPINE MODULE
        detailSpine = rb.CreateDetail(anim_ctrl= base.animControl,
                                      list_spine_jnt= [rootJnt, spineJnt[0], spineJnt[1], spineJnt[2], spineJnt[3]],

                                      list_spine_ctrl_fk= [buildSpine.controller_spine_fk_low.controlGimbal,
                                                           buildSpine.controller_spine_fk_mid.controlGimbal,
                                                           buildSpine.controller_spine_fk_up.controlGimbal],

                                      list_spine_ctrl_ik= [buildSpine.controller_spine_ik_low.controlGimbal,
                                                           buildSpine.controller_spine_ik_up.controlGimbal,
                                                           buildSpine.controller_spine_ik_up.control],

                                      FkIk_switch= buildSpine.controller_FkIk_spine_setup.control,
                                      prefix          = prefix+'Dtl',
                                      detail_spine_deformer= detailSpineDeformer,
                                      ctrl_mid= ctrlMid,
                                      scale           = size,
                                      numJoints       = 3)

        # Parent ribbon spine to still grp
        mc.parent(detailSpine.grp_all_detail, base.stillGrp)

        #Visibility of follicle controller
        au.connect_part_object(obj_base_connection='detailCtrl', target_connection='visibility',
                               obj_name=buildSpine.controller_FkIk_spine_setup.control,
                               target_name=[detailSpine.grp_follicle_main[0]],
                               select_obj=False)