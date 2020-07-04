from __builtin__ import reload

import maya.cmds as mc

from rigging.library.utils import controller as ct
from rigging.library.utils import transform as tf
from rigging.tools import AD_utils as au

reload (ct)
reload (tf)
reload (au)

class Chin:
    def __init__(self,
                 mentolabialJnt,
                 mentolabialPrefix,
                 chinJnt,
                 chinPrefix,
                 scale,
                 faceAnimCtrlGrp,
                 faceUtilsGrp,
                 lowerLipBindJnt,
                 jawJnt,
                 suffixController
                 ):

        # group cheek driver
        groupDriver = mc.group(em=1, n='chinJoint' + '_grp')
        setupDriverGrp = mc.group(em=1, n='chinSetup' + '_grp')
        ctrlDriverGrp = mc.group(em=1, n='chinCtrlAll' + '_grp')

        mc.hide(setupDriverGrp)
        grpCheekAll = mc.group(em=1, n='chin' + '_grp')
        mc.parent(groupDriver, setupDriverGrp, grpCheekAll)
        mc.parent(ctrlDriverGrp, faceAnimCtrlGrp)
        mc.parent(grpCheekAll, faceUtilsGrp)

        self.groupDriver = groupDriver
        self.setupDriverGrp = setupDriverGrp
        self.ctrlDriverGrp = ctrlDriverGrp

    # ==================================================================================================================
    #                                                   CHIN AND MENTOLABIAL DRIVER
    # ==================================================================================================================

        mentolabialCtrl = self.controllerSetup(objJoint=mentolabialJnt, objPrefix=mentolabialPrefix, scale=scale,
                             constraint=[lowerLipBindJnt, jawJnt], w=[0.5, 0.5], jawCtrl=jawJnt,
                             suffixController=suffixController)

        chinCtrl = self.controllerSetup(objJoint=chinJnt, objPrefix=chinPrefix, scale=scale,
                             constraint=[jawJnt], w=[1.0], jawCtrl=jawJnt, suffixController=suffixController)

        self.chinCtrl = chinCtrl[0]
        self.chinCtrlGrp = chinCtrl[1]
        self.mentolabialCtrlGrp = mentolabialCtrl[1]

    def controllerSetup(self, objJoint, objPrefix, scale, constraint, w, jawCtrl, suffixController):
        # create controller
        objectCtrl = ct.Control(match_obj_first_position=objJoint,
                                prefix=objPrefix,
                                shape=ct.JOINT, groups_ctrl=['', 'Offset'],
                                ctrl_size=scale * 0.05, suffix=suffixController,
                                ctrl_color='red', lock_channels=['v'])

        self.objectCtrl = objectCtrl.control
        self.objectParentCtrlZro = objectCtrl.parent_control[0]
        self.objectParentCtrlOffset = objectCtrl.parent_control[1]

        # ROTATE CONTROLLER OFFSET
        mc.setAttr(self.objectParentCtrlOffset + '.scaleY', -1)

        # CREATE GRP JOINT
        self.objJointParentGrp = tf.create_parent_transform(['', 'Offset'], match_position=objJoint, object=objJoint,
                                                            prefix=objJoint, suffix=objJoint
                                                            )

        # CREATE DRIVER
        parentDriver = mc.group(em=1, n=au.prefix_name(objPrefix) + '_set')
        driver = mc.spaceLocator(n=au.prefix_name(objPrefix) + 'Drv' + '_set')[0]
        mc.parent(driver, parentDriver)
        mc.delete(mc.parentConstraint(objJoint, parentDriver, mo=0))

        mc.setAttr(driver+'.localScaleX', 0.5*scale)
        mc.setAttr(driver+'.localScaleY', 0.5*scale)
        mc.setAttr(driver+'.localScaleZ', 0.5*scale)

        # CONSTRAINING THE OBJECT
        pacCons = None
        for cons, value in zip(constraint, w):
            pacCons = mc.parentConstraint(cons, parentDriver, mo=1, w=value)

        sclCons = mc.scaleConstraint(jawCtrl, parentDriver, mo=1)

        # RENAME CONSTRAINT
        au.constraint_rename([pacCons[0], sclCons[0]])

        # CONNECT BIND PARENT GRP TO CTRL GRP
        au.connect_attr_object(parentDriver, self.objJointParentGrp[0])
        au.connect_attr_object(self.objJointParentGrp[0], self.objectParentCtrlZro)

        # CONNECT CTRL TO JOINT
        reverseTrans = mc.createNode('multiplyDivide', n=au.prefix_name(objPrefix) + 'ReverseTrans' + '_mdn')
        reverseRot = mc.createNode('multiplyDivide', n=au.prefix_name(objPrefix) + 'ReverseRot' + '_mdn')

        mc.setAttr(reverseTrans + '.input2X', 1)
        mc.setAttr(reverseTrans + '.input2Y', -1)
        mc.setAttr(reverseTrans + '.input2Z', 1)
        mc.setAttr(reverseRot + '.input2X', -1)
        mc.setAttr(reverseRot + '.input2Y', 1)
        mc.setAttr(reverseRot + '.input2Z', -1)

        mc.connectAttr(self.objectCtrl + '.translate', reverseTrans + '.input1')
        mc.connectAttr(reverseTrans + '.output', objJoint + '.translate')
        mc.connectAttr(self.objectCtrl  + '.rotate', reverseRot + '.input1')
        mc.connectAttr(reverseRot + '.output', objJoint + '.rotate')

        au.connect_attr_scale(self.objectCtrl, objJoint)

        # PARENT TO GROUP
        mc.parent(parentDriver, self.setupDriverGrp)
        mc.parent(self.objJointParentGrp[0], self.groupDriver)

        mc.parent(self.objectParentCtrlZro , self.ctrlDriverGrp)

        return objectCtrl.control, objectCtrl.parent_control[0]

