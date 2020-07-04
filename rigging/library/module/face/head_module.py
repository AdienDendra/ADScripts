from __builtin__ import reload

import maya.cmds as mc

from rigging.library.base.face import head as hd
from rigging.library.utils import controller as ct
from rigging.tools import AD_utils as au

# from library.base.body import detailLimb as dl

reload(hd)
reload(au)
reload(ct)
# reload(dl)

class Head:
    def __init__(self,
                 faceAnimCtrlGrp,
                 faceUtilsGrp,
                 neckJnt,
                 neckInBtwJnt,
                 headJnt,
                 jawJnt,
                 jawTipJnt,
                 headUpJnt,
                 headLowJnt,
                 jawPrefix,
                 jawTipPrefix,
                 headPrefix,
                 neckPrefix,
                 neckInBtwPrefix,
                 headUpPrefix,
                 headLowPrefix,
                 eyeAimPrefix,
                 eyeJntLFT,
                 eyeJntRGT,
                 positionEyeAimCtrl,
                 upperTeethJnt,
                 lowerTeethJnt,
                 tongue01Jnt,
                 tongue02Jnt,
                 tongue03Jnt,
                 tongue04Jnt,
                 suffixController,
                 scale
                 ):

        worldUpGrp = mc.spaceLocator(n='worldUpFacialObject_loc')[0]
        mc.hide(worldUpGrp)
        self.worldUpGrp = worldUpGrp

        head = hd.Build(neckJnt=neckJnt,
                        neckInBtwJnt=neckInBtwJnt,
                        headJnt=headJnt,
                        jawTipJnt=jawTipJnt,
                        jawJnt=jawJnt,
                        headUpJnt=headUpJnt,
                        headLowJnt=headLowJnt,
                        jawPrefix=jawPrefix,
                        jawTipPrefix= jawTipPrefix,

                        prefixHead=headPrefix,
                        prefixHeadUp=headUpPrefix,
                        prefixHeadLow=headLowPrefix,
                        prefixNeck=neckPrefix,
                        prefixInBtwNeck=neckInBtwPrefix,
                        upperTeethJnt=upperTeethJnt,
                        lowerTeethJnt=lowerTeethJnt,
                        tongue01Jnt=tongue01Jnt,
                        tongue02Jnt=tongue02Jnt,
                        tongue03Jnt=tongue03Jnt,
                        tongue04Jnt=tongue04Jnt,
                        scale=scale,
                        suffixController=suffixController)

        self.headUpCtrl = head.headUpCtrl.control
        self.headUpCtrlGimbal = head.headUpCtrl.control_gimbal

        self.headLowCtrl = head.headLowCtrl.control
        self.headLowCtrlGimbal = head.headLowCtrl.control_gimbal


        self.neckCtrl = head.neckCtrl.control
        self.neckCtrlGimbal = head.neckCtrl.control_gimbal
        self.neckCtrlGrp = head.neckCtrl.parent_control[0]

        self.headCtrl = head.headCtrl.control
        self.headCtrlGimbal = head.headCtrl.control_gimbal
        self.headCtrlGrp = head.headCtrl.parent_control[0]
        self.headCtrlGlobal = head.headCtrl.parent_control[1]
        self.headCtrlLocal = head.headCtrl.parent_control[2]

        self.jawCtrlGrp = head.jawCtrl.parent_control[0]
        self.jawCtrl = head.jawCtrl.control
        self.attr_upLip_follow = head.attr_upLip_follow
        self.headLow_normal_rotationGrp=head.headLow_normal_rotationGrp
        # self.jawCtrlGimbal = head.jawCtrl.control_gimbal

        self.prefixJaw =jawPrefix
        self.neckJntGrp = head.neckJntGrp
        # LOCAL WORLD HEAD
        self.localWorld(objectName='head', objectCtrl=self.headCtrl,
                        objectParentGrp=self.headCtrlGrp, objectParentGlobal=self.headCtrlGlobal,
                        objectParentLocal=self.headCtrlLocal,
                        localBase=self.neckCtrlGimbal, worldBase=worldUpGrp, eyeAim=False)

        # # parent head up and low ctrl to head controller
        # mc.parent(head.headUpCtrl.parentControl[0], head.headLowCtrl.parentControl[0], head.headCtrl.control_gimbal)

        # jaw reverse trans
        # self.jawReverseNode(nodeName='ReverseTrans', jawController=head.jawCtrl.control_gimbal,
        #                     jawOffsetGrpCtrl=head.jawCtrl.parentControl[1], connection='translate')
        #
        # self.jawReverseNode(nodeName='ReverseRot', jawController=head.jawCtrl.control_gimbal,
        #                     jawOffsetGrpCtrl=head.jawCtrl.parentControl[1], connection='rotate')

        # # connect to module joint
        # self.jawCtrlGimbalDriverJnt(nodeName='AddTrans', jawController=head.jawCtrl.control,
        #                             jawControllerGimbal=head.jawCtrl.control_gimbal, jawTarget=jawJnt,
        #                             attribute='translate')
        #
        # self.jawCtrlGimbalDriverJnt(nodeName='AddRot', jawController=head.jawCtrl.control,
        #                             jawControllerGimbal=head.jawCtrl.control_gimbal, jawTarget=jawJnt,
        #                             attribute='rotate')
        #
        # # connect to jaw direction offset
        # self.jawCtrlGimbalDriverJnt(nodeName='AddTransDir', jawController=head.jawCtrl.control,
        #                             jawControllerGimbal=head.jawCtrl.control_gimbal, jawTarget=head.jawDirectionOffsetGrp,
        #                             attribute='translate')
        #
        # self.jawCtrlGimbalDriverJnt(nodeName='AddRotDir', jawController=head.jawCtrl.control,
        #                             jawControllerGimbal=head.jawCtrl.control_gimbal, jawTarget=head.jawDirectionOffsetGrp,
        #                             attribute='rotate')


        # # connect the tip joint to parent ctrl jaw
        # dMtxJaw = mc.createNode('decomposeMatrix', n=self.prefixJaw+'_dmtx')
        # mc.connectAttr(jawTipJnt + '.worldMatrix[0]', dMtxJaw + '.inputMatrix')
        #
        # mc.connectAttr(dMtxJaw+'.outputTranslate', head.jawCtrl.parentControl[0]+'.translate')
        # mc.connectAttr(dMtxJaw+'.outputRotate', head.jawCtrl.parentControl[0]+'.rotate')
        # mc.connectAttr(dMtxJaw+'.outputScale', head.jawCtrl.parentControl[0]+'.scale')

        # JAW CONNECTION
        au.connectAttrTransRot(self.jawCtrl, head.jawDirectionOffsetGrp)
        au.connectAttrTransRot(self.jawCtrl, jawJnt)
        pacJawTip = mc.parentConstraint(jawJnt, head.jawTipGrp[1], mo=1)
        # au.connectAttrTransRot(head.jawTipGrp[0], self.jawCtrlGrp)
        # CREATE PMA
        jawPma = mc.createNode('plusMinusAverage', n=au.prefix_name(jawTipJnt) + 'Trans_pma')
        mc.setAttr(jawPma+'.operation', 2)
        mc.connectAttr(head.jawTipGrp[1]+'.translate', jawPma+'.input3D[0]')
        mc.connectAttr(self.jawCtrl+'.translate', jawPma+'.input3D[1]')
        # mc.connectAttr(self.jawCtrlGimbal+'.translate', jawPma+'.input3D[2]')

        mc.connectAttr(jawPma+'.output3D', head.jawCtrl.parent_control[1]+'.translate')

    # ==================================================================================================================
    #                                               CREATE AIM FOR EYE
    # ==================================================================================================================

        eyeAimMainCtrl = ct.Control(match_obj_first_position=eyeJntLFT,
                                    match_obj_second_position=eyeJntRGT,
                                    prefix=eyeAimPrefix,
                                    shape=ct.CAPSULE, groups_ctrl=['All', 'Global', 'Local'],
                                    ctrl_size=scale * 0.25,
                                    ctrl_color='blue', lock_channels=['v', 'r', 's'])

        self.eyeAimMainCtrl = eyeAimMainCtrl.control
        self.eyeAimMainCtrlGrp = eyeAimMainCtrl.parent_control[0]
        self.eyeAimMainCtrlGlobal = eyeAimMainCtrl.parent_control[1]
        self.eyeAimMainCtrlLocal = eyeAimMainCtrl.parent_control[2]

        # mc.setAttr(self.eyeAimMainCtrlGrp+'.rotate', 0, 0, 0, type="double3")

        getAttribute = mc.getAttr(eyeAimMainCtrl.parent_control[0] + '.translateZ')
        mc.setAttr(eyeAimMainCtrl.parent_control[0] + '.translateZ', getAttribute + (positionEyeAimCtrl * scale))

        # LOCAL WORLD AIM EYE
        self.localWorld(objectName='eyeAim', objectCtrl=self.eyeAimMainCtrl,
                        objectParentGrp=self.eyeAimMainCtrlGrp,
                        objectParentGlobal=self.eyeAimMainCtrlGlobal,
                        objectParentLocal=self.eyeAimMainCtrlLocal,
                        localBase=self.headUpCtrlGimbal, worldBase=worldUpGrp, eyeAim=True)

        # SCALE CONSTRAINT FROM HEAD UP CTRL TO EYE MAIN AIM ALL GRP
        sclEyeMainCons = mc.scaleConstraint(self.headUpCtrl, eyeAimMainCtrl.parent_control[0])

        mc.parent(self.neckCtrlGrp, self.eyeAimMainCtrlGrp, faceAnimCtrlGrp)
        mc.parent(worldUpGrp,  faceUtilsGrp)

        # RENAME CONSTRAINT
        au.constraint_rename([pacJawTip[0], sclEyeMainCons[0]])

    # def jawReverseNode(self, nodeName, jawController, jawOffsetGrpCtrl, connection):
    #     mdnReverseJaw = mc.createNode('multiplyDivide', n=self.prefixJaw + nodeName + '_mdn')
    #     mc.setAttr(mdnReverseJaw + '.input2X', -1)
    #     mc.setAttr(mdnReverseJaw + '.input2Y', -1)
    #     mc.setAttr(mdnReverseJaw + '.input2Z', -1)
    #
    #     mc.connectAttr(jawController +'.%s' % connection, mdnReverseJaw + '.input1')
    #     mc.connectAttr(mdnReverseJaw + '.output', jawOffsetGrpCtrl + '.%s' % connection)

    # ==================================================================================================================
    #                                               NECK IN BETWEEN
    # ==================================================================================================================

        # neckDtl = dl.CreateDetail(
        #                  detailLimbDeformer=False,
        #                  module=neckJnt,
        #                  tip=headJnt,
        #                  parallelAxis='y',
        #                  tipPos='+',
        #                  ctrlColor='lightPink',
        #                  prefix=neckPrefix,
        #                  side='',
        #                  scale=scale,
        #                  numJoints=1)
        #
        # self.neckDtlJnt = neckDtl.follicleJointLimb[1]
        #
        # # HIDING THE OBJEC CTRL DETAIL UP AND DOWN
        # mc.hide(neckDtl.follicleGrpSetGrp[0], neckDtl.follicleGrpSetGrp[-1], neckDtl.ctrlUp.parentControl[0],
        #         neckDtl.ctrlDown.parentControl[0])
        #
        # # PARENT CONSTRAINT AND SCALE CONSTRAINT TO CTRL RIBBON
        # mc.parentConstraint(neckJnt, neckDtl.ctrlUp.parentControl[0])
        # mc.parentConstraint(headJnt, neckDtl.ctrlDown.parentControl[0])
        # mc.scaleConstraint(neckJnt, neckDtl.grpTransform)
        #
        # # PARENTING THE OBJECT
        # mc.parent(neckDtl.grpTransformZro, faceAnimCtrlGrp)
        # mc.parent(neckDtl.grpNoTransformZro[0], faceUtilsGrp)




    def jawCtrlGimbalDriverJnt(self, nodeName, jawController, jawControllerGimbal, jawTarget, attribute):
        pmaJawAdd = mc.createNode('plusMinusAverage', n=self.prefixJaw+nodeName+'_pma')
        mc.connectAttr(jawController+'.%s' % attribute, pmaJawAdd+'.input3D[0]')
        mc.connectAttr(jawControllerGimbal+'.%s' % attribute, pmaJawAdd+'.input3D[1]')

        mc.connectAttr(pmaJawAdd +'.output3D', jawTarget + '.%s' % attribute)


    def localWorld(self,objectName, objectCtrl, objectParentGrp,
                   objectParentGlobal, objectParentLocal, localBase, worldBase, eyeAim=False):
        # LOCAL WORLD HEAD
        local = mc.createNode('transform', n=objectName + 'Local_grp')
        mc.parent(local, objectParentGrp)
        mc.setAttr(local + '.translate', 0, 0, 0, type="double3")
        mc.setAttr(local + '.rotate', 0, 0, 0, type="double3")

        world = mc.duplicate(local, n=objectName + 'World_grp')[0]

        pacLocBaseCons = mc.parentConstraint(localBase, local, mo=1)
        pacWrldBaseCons = mc.parentConstraint(worldBase, world, mo=1)

        if not eyeAim:
            pacObjGlobalCons = mc.parentConstraint(local, objectParentGlobal, mo=1)
            localWorldCons = mc.orientConstraint(local, world, objectParentLocal, mo=1)[0]
            # rename constraint
            au.constraint_rename(pacObjGlobalCons)

        else:
            localWorldCons = mc.parentConstraint(local, world, objectParentLocal, mo=1)[0]

        # CONNECT THE ATTRIBUTE
        headLocalWrld = au.add_attribute(objects=[objectCtrl], long_name=['localWorld'],
                                         attributeType="float", min=0, max=1, dv=0, keyable=True)

        # CREATE REVERSE
        reverse = mc.createNode('reverse', n=objectName + 'LocalWorld_rev')
        mc.connectAttr(objectCtrl + '.%s' % headLocalWrld, reverse + '.inputX')

        mc.connectAttr(reverse + '.outputX', localWorldCons + '.%sW0' % local)
        mc.connectAttr(objectCtrl + '.%s' % headLocalWrld, localWorldCons + '.%sW1' % world)

        # CONSTRAINT RENAME
        au.constraint_rename([pacLocBaseCons[0], pacWrldBaseCons[0], localWorldCons])