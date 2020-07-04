from __builtin__ import reload

import maya.cmds as mc

from rigging.library.utils import controller as ct
from rigging.library.utils import transform as tf
from rigging.tools import AD_utils as au

reload (ct)
reload (au)
reload (tf)

class Build:
    def __init__(self,
                 browTwJnt,
                 browInJnt,
                 browMidJnt,
                 browOutJnt,
                 browTipJnt,
                 browTwPrefix,
                 browInPrefix,
                 browMidPrefix,
                 browOutPrefix,
                 browsPrefix,
                 browTipPrefix,
                 scale,
                 sideRGT,
                 sideLFT,
                 side,
                 browInGrpRotOffset,
                 browMidGrpRotOffset,
                 browOutGrpRotOffset,
                 browTipGrpRotOffset,
                 suffixController
                 ):
        # create group brow
        self.grpBrowAll = mc.group(em=1, n='brow' + side + '_grp')

        # check position
        pos = mc.xform(browMidJnt, ws=1, q=1, t=1)[0]

        browTwCtrl = ct.Control(match_obj_first_position=browTwJnt,
                                prefix=browTwPrefix,
                                shape=ct.ARROW4STRAIGHT, groups_ctrl=[''],
                                ctrl_size=scale * 0.03, suffix=suffixController,
                                ctrl_color='red', lock_channels=['v'],
                                side=side)

        browInCtrl = ct.Control(match_obj_first_position=browInJnt,
                                prefix=browInPrefix,
                                shape=ct.CUBE, groups_ctrl=[''],
                                ctrl_size=scale * 0.05, suffix=suffixController,
                                ctrl_color='blue', lock_channels=['v'],
                                side=side)

        browMidCtrl = ct.Control(match_obj_first_position=browMidJnt,
                                 prefix=browMidPrefix,
                                 shape=ct.CUBE, groups_ctrl=['', 'Offset'],
                                 ctrl_size=scale * 0.05, suffix=suffixController,
                                 ctrl_color='blue', lock_channels=['v'], side=side)

        browOutCtrl = ct.Control(match_obj_first_position=browOutJnt,
                                 prefix=browOutPrefix,
                                 shape=ct.CUBE, groups_ctrl=[''],
                                 ctrl_size=scale * 0.05, suffix=suffixController,
                                 ctrl_color='blue', lock_channels=['v'], side=side)

        browTipCtrl = ct.Control(match_obj_first_position=browTipJnt,
                                 prefix=browTipPrefix,
                                 shape=ct.CUBE, groups_ctrl=[''],
                                 ctrl_size=scale * 0.05, suffix=suffixController,
                                 ctrl_color='blue', lock_channels=['v'], side=side)

        browCtrl = ct.Control(match_obj_first_position=browInJnt,
                              match_obj_second_position=browOutJnt,
                              prefix=browsPrefix,
                              shape=ct.SQUAREPLUS, groups_ctrl=[''],
                              ctrl_size=scale * 0.1, suffix=suffixController,
                              ctrl_color='yellow', lock_channels=['v'], side=side)


    # ==================================================================================================================
    #                                            ASSIGNING THE INSTANCE NAME
    # ==================================================================================================================
        self.browTwCtrl = browTwCtrl.control
        self.browTwCtrlGrp = browTwCtrl.parent_control[0]

        self.browInCtrl = browInCtrl.control
        self.browInCtrlGrp = browInCtrl.parent_control[0]

        self.browMidCtrl = browMidCtrl.control
        self.browMidCtrlGrp = browMidCtrl.parent_control[0]
        self.browMidCtrlOffset = browMidCtrl.parent_control[1]


        self.browOutCtrl = browOutCtrl.control
        self.browOutCtrlGrp = browOutCtrl.parent_control[0]

        self.browTipCtrl = browTipCtrl.control
        self.browTipCtrlGrp = browTipCtrl.parent_control[0]

        self.browCtrl = browCtrl.control
        self.browCtrlGrp = browCtrl.parent_control[0]

    # ==================================================================================================================
    #                                           EYEBROW CONTROLLER SETUP
    # ==================================================================================================================
        mc.parent(self.browTwCtrlGrp, self.browInCtrl)
        mc.parent(self.browInCtrlGrp, self.browMidCtrlGrp, self.browOutCtrlGrp,  self.browTipCtrlGrp,
                  self.browCtrl)

    # GROUPING FOR OFFSET
        self.ctrlGrpBrowInCenter = mc.group(em=1, n='browInCtrlCenter' + side + '_grp')
        self.ctrlOffsetGrpBrowInCenter = mc.group(em=1, n='browInCtrlOffsetCenter' + side + '_grp')
        mc.parent(self.ctrlOffsetGrpBrowInCenter, self.ctrlGrpBrowInCenter)

        self.ctrlGrpBrowMidCenter = mc.group(em=1, n='browMidCtrlCenter' + side + '_grp')
        self.ctrlOffsetGrpBrowMidCenter = mc.group(em=1, n='browMidCtrlOffsetCenter' + side + '_grp')
        mc.parent(self.ctrlOffsetGrpBrowMidCenter, self.ctrlGrpBrowMidCenter)

        self.ctrlGrpBrowOutCenter = mc.group(em=1, n='browOutCtrlCenter' + side + '_grp')
        self.ctrlOffsetGrpBrowOutCenter = mc.group(em=1, n='browOutCtrlOffsetCenter' + side + '_grp')
        mc.parent(self.ctrlOffsetGrpBrowOutCenter, self.ctrlGrpBrowOutCenter)

        self.ctrlGrpBrowTipCenter = mc.group(em=1, n='browTipCtrlCenter' + side + '_grp')
        self.ctrlOffsetGrpBrowTipCenter = mc.group(em=1, n='browTipCtrlOffsetCenter' + side + '_grp')
        mc.parent(self.ctrlOffsetGrpBrowTipCenter, self.ctrlGrpBrowTipCenter)


    # CREATE GROUP CORESPONDENT THE JOINTS
        browTwGrp = tf.create_parent_transform(parent_list=[''], object=browTwJnt, match_position=browTwJnt, prefix=browTwPrefix, suffix='_jnt', side=side)
        browInGrp = tf.create_parent_transform(parent_list=['', 'Offset'], object=browInJnt, match_position=browInJnt, prefix=browInPrefix, suffix='_jnt', side=side)
        browMidGrp = tf.create_parent_transform(parent_list=['', 'Offset', 'Avg'], object=browMidJnt, match_position=browMidJnt, prefix=browMidPrefix, suffix='_jnt', side=side)
        browOutGrp = tf.create_parent_transform(parent_list=['', 'Offset'], object=browOutJnt, match_position=browOutJnt, prefix=browOutPrefix, suffix='_jnt', side=side)
        browTipGrp = tf.create_parent_transform(parent_list=['', 'Offset'], object=browTipJnt, match_position=browTipJnt, prefix=browTipPrefix, suffix='_jnt', side=side)

    # EYBROW MAIN OFFSET GRP JOINT TRANSFORM
        browInMain = self.mainGroupBindConnection(name=browInPrefix, side=side, objectParent=browInGrp[0])
        browMidMain = self.mainGroupBindConnection(name=browMidPrefix, side=side, objectParent=browMidGrp[0])
        browOutMain = self.mainGroupBindConnection(name=browOutPrefix, side=side, objectParent=browOutGrp[0])
        browTipMain = self.mainGroupBindConnection(name=browTipPrefix, side=side, objectParent=browTipGrp[0])

    # SHIFTING PARENT JOINT TO MAIN OFFSET GRP EYEBROW
        mc.parent(browInGrp[1], browInMain)
        mc.parent(browMidGrp[1], browMidMain)
        mc.parent(browOutGrp[1], browOutMain)
        mc.parent(browTipGrp[1], browTipMain)


        # EYEBROW EXCEPTION PARENTING CTRL
        mc.delete(mc.pointConstraint(self.browCtrl, self.ctrlGrpBrowInCenter))
        mc.delete(mc.pointConstraint(self.browCtrl, self.ctrlGrpBrowMidCenter))
        mc.delete(mc.pointConstraint(self.browCtrl, self.ctrlGrpBrowOutCenter))
        mc.delete(mc.pointConstraint(self.browCtrl, self.ctrlGrpBrowTipCenter))

        # FLIPPING THE CONTROLLER
        if pos <0:
            mc.setAttr(self.browInCtrlGrp + '.scaleX', -1)
            mc.setAttr(self.browMidCtrlGrp + '.scaleX', -1)
            mc.setAttr(self.browOutCtrlGrp + '.scaleX', -1)
            mc.setAttr(self.browTipCtrlGrp + '.scaleX', -1)

            # mc.setAttr(self.browCtrlGrp + '.scaleX', -1)

            mc.setAttr(self.browInCtrlGrp + '.rotateY', browInGrpRotOffset*-1)
            mc.setAttr(self.browMidCtrlGrp + '.rotateY', browMidGrpRotOffset*-1)
            mc.setAttr(self.browOutCtrlGrp + '.rotateY', browOutGrpRotOffset*-1)
            mc.setAttr(self.browTipCtrlGrp + '.rotateY', browTipGrpRotOffset*-1)

            mc.setAttr(browInGrp[1] + '.rotateY', browInGrpRotOffset*-1)
            mc.setAttr(browMidGrp[1] + '.rotateY', browMidGrpRotOffset*-1)
            mc.setAttr(browOutGrp[1] + '.rotateY', browOutGrpRotOffset*-1)
            mc.setAttr(browTipGrp[1] + '.rotateY', browTipGrpRotOffset*-1)

            self.reverseNode(self.browTwCtrl, browTwJnt, sideRGT, sideLFT, side)
            self.reverseNode(self.browInCtrl, browInJnt, sideRGT, sideLFT, side)
            self.reverseNode(self.browMidCtrl, browMidJnt, sideRGT, sideLFT, side)
            self.reverseNode(self.browOutCtrl, browOutJnt, sideRGT, sideLFT, side)
            self.reverseNode(self.browTipCtrl, browTipJnt, sideRGT, sideLFT, side)

            self.reverseNode(self.browCtrl, browInMain, sideRGT, sideLFT, side)
            self.reverseNode(self.browCtrl, browMidMain, sideRGT, sideLFT, side)
            self.reverseNode(self.browCtrl, browOutMain, sideRGT, sideLFT, side)
            # self.reverseNode(self.browCtrl, browTipMain, sideRGT, sideLFT, side)

            au.connect_attr_scale(self.browTwCtrl, browTwJnt)
            au.connect_attr_scale(self.browInCtrl, browInJnt)
            au.connect_attr_scale(self.browMidCtrl, browMidJnt)
            au.connect_attr_scale(self.browOutCtrl, browOutJnt)
            au.connect_attr_scale(self.browTipCtrl, browTipJnt)

            au.connect_attr_scale(self.browCtrl, browInMain)
            au.connect_attr_scale(self.browCtrl, browMidMain)
            au.connect_attr_scale(self.browCtrl, browOutMain)
            # au.connectAttrScale(self.browCtrl, browTipMain)

            # connect attr
            self.reverseNode(self.browCtrl, self.ctrlOffsetGrpBrowInCenter, sideRGT, sideLFT, side)
            self.reverseNode(self.browCtrl, self.ctrlOffsetGrpBrowMidCenter, sideRGT, sideLFT, side)
            self.reverseNode(self.browCtrl, self.ctrlOffsetGrpBrowOutCenter, sideRGT, sideLFT, side)
            # self.reverseNode(self.browCtrl, self.ctrlOffsetGrpBrowTipCenter, sideRGT, sideLFT, side)

            # au.connectAttrObject(self.browCtrl, self.ctrlOffsetGrpBrowInCenter)
            # au.connectAttrObject(self.browCtrl, self.ctrlOffsetGrpBrowMidCenter)
            # au.connectAttrObject(self.browCtrl, self.ctrlOffsetGrpBrowOutCenter)
            # au.connectAttrObject(self.browCtrl, self.ctrlOffsetGrpBrowTipCenter)


        else:
            mc.setAttr(self.browInCtrlGrp + '.rotateY', browInGrpRotOffset)
            mc.setAttr(self.browMidCtrlGrp + '.rotateY', browMidGrpRotOffset)
            mc.setAttr(self.browOutCtrlGrp + '.rotateY', browOutGrpRotOffset)
            mc.setAttr(self.browTipCtrlGrp + '.rotateY', browTipGrpRotOffset)

            mc.setAttr(browInGrp[1] + '.rotateY', browInGrpRotOffset)
            mc.setAttr(browMidGrp[1] + '.rotateY', browMidGrpRotOffset)
            mc.setAttr(browOutGrp[1] + '.rotateY', browOutGrpRotOffset)
            mc.setAttr(browTipGrp[1] + '.rotateY', browTipGrpRotOffset)

            au.connect_attr_object(self.browTwCtrl, browTwJnt)
            au.connect_attr_object(self.browInCtrl, browInJnt)
            au.connect_attr_object(self.browMidCtrl, browMidJnt)
            au.connect_attr_object(self.browOutCtrl, browOutJnt)
            au.connect_attr_object(self.browTipCtrl, browTipJnt)

            au.connect_attr_object(self.browCtrl, browInMain)
            au.connect_attr_object(self.browCtrl, browMidMain)
            au.connect_attr_object(self.browCtrl, browOutMain)
            # au.connectAttrObject(self.browCtrl, browTipMain)

            au.connect_attr_object(self.browCtrl, self.ctrlOffsetGrpBrowInCenter)
            au.connect_attr_object(self.browCtrl, self.ctrlOffsetGrpBrowMidCenter)
            au.connect_attr_object(self.browCtrl, self.ctrlOffsetGrpBrowOutCenter)
            # au.connectAttrObject(self.browCtrl, self.ctrlOffsetGrpBrowTipCenter)

        # grouping to follicle
        # mc.parent(self.ctrlGrpEyebrowInCenter,  self.follicleTransformAll[3])
        # mc.parent(self.ctrlGrpEyebrowMidCenter,  self.follicleTransformAll[4])
        # mc.parent(self.ctrlGrpEyebrowOutCenter,  self.follicleTransformAll[5])

        # regrouping to offset grp
        mc.parent(self.browInCtrlGrp, self.ctrlOffsetGrpBrowInCenter)
        mc.parent(self.browMidCtrlGrp, self.ctrlOffsetGrpBrowMidCenter)
        mc.parent(self.browOutCtrlGrp, self.ctrlOffsetGrpBrowOutCenter)
        mc.parent(self.browTipCtrlGrp, self.ctrlOffsetGrpBrowTipCenter)

        # # connect attr
        # au.connectAttrObject(self.browCtrl, self.ctrlOffsetGrpBrowInCenter)
        # au.connectAttrObject(self.browCtrl, self.ctrlOffsetGrpBrowMidCenter)
        # au.connectAttrObject(self.browCtrl, self.ctrlOffsetGrpBrowOutCenter)
        # au.connectAttrObject(self.browCtrl, self.ctrlOffsetGrpBrowTipCenter)
        #
        if pos<0:
            mc.setAttr(self.browCtrlGrp + '.scaleX', -1)

        self.browMidGrp = browMidGrp

        # ADD ATTRIBUTE BROW IN
        au.add_attribute(objects=[self.browInCtrl], long_name=['weightSkinInfluence'], nice_name=[' '], at="enum",
                         en='%s%s' % ('Weight ', 'Influence'), channel_box=True)

        self.browCenterInAttr = au.add_attribute(objects=[self.browInCtrl], long_name=['browCenter'],
                                                 attributeType="float", min=0, dv=1, keyable=True)
        self.browMidInAttr = au.add_attribute(objects=[self.browInCtrl], long_name=['browMid'],
                                              attributeType="float", min=0, dv=1, keyable=True)

        # ADD ATTRIBUTE BROW OUT
        au.add_attribute(objects=[self.browOutCtrl], long_name=['weightSkinInfluence'], nice_name=[' '], at="enum",
                         en='%s%s' % ('Weight ', 'Influence'), channel_box=True)

        self.browMidOutAttr = au.add_attribute(objects=[self.browOutCtrl], long_name=['browMid'],
                                               attributeType="float", min=0, dv=1, keyable=True)

        # PARENT TO THE GROUP
        mc.parent(self.ctrlGrpBrowInCenter, self.ctrlGrpBrowMidCenter, self.ctrlGrpBrowOutCenter,
                  self.ctrlGrpBrowTipCenter, self.browCtrlGrp,
                  self.grpBrowAll)

    def reverseNode(self, object, targetJnt, sideRGT, sideLFT, side, inputTrans2X=-1, inputTrans2Y=1, inputTrans2Z=1,
                    inputRot2X=1, inputRot2Y=-1, inputRot2Z=-1):
        if sideRGT in targetJnt:
            newName = targetJnt.replace(sideRGT, '')
        elif sideLFT in targetJnt:
            newName = targetJnt.replace(sideLFT, '')
        else:
            newName = targetJnt

        transMdn = mc.createNode('multiplyDivide', n=au.prefix_name(newName) + 'Trans' + side + '_mdn')
        mc.connectAttr(object+'.translate', transMdn+'.input1')
        mc.setAttr(transMdn+'.input2X', inputTrans2X)
        mc.setAttr(transMdn+'.input2Y', inputTrans2Y)
        mc.setAttr(transMdn+'.input2Z', inputTrans2Z)

        mc.connectAttr(transMdn+'.output', targetJnt +'.translate')

        rotMdn = mc.createNode('multiplyDivide', n=au.prefix_name(newName) + 'Rot' + side + '_mdn')
        mc.connectAttr(object+'.rotate', rotMdn+'.input1')
        mc.setAttr(rotMdn + '.input2X', inputRot2X)
        mc.setAttr(rotMdn+'.input2Y', inputRot2Y)
        mc.setAttr(rotMdn+'.input2Z', inputRot2Z)
        mc.connectAttr(rotMdn+'.output', targetJnt+'.rotate')

    def mainGroupBindConnection(self, name, side, objectParent):
        # BROW MAIN OFFSET GRP JOINT TRANSFORM
        eyebrowMainBindGrp = mc.group(em=1, n=name+'Main' + side + '_grp')
        eyebrowMainBindOffset = mc.group(em=1, n=name+'MainOffset' + side + '_grp', p=eyebrowMainBindGrp)
        mc.delete(mc.parentConstraint(self.browCtrl, eyebrowMainBindGrp))

        mc.parent(eyebrowMainBindGrp, objectParent)

        return eyebrowMainBindOffset