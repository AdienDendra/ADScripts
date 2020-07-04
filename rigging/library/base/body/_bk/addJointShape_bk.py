from __builtin__ import reload

import maya.cmds as mc
from rigLib.utils import transform as tf

from rigging.tools import AD_utils as au

reload (tf)
reload (au)


class Build:
    def __init__(self,
                 addJoint,
                 fkIkSetup,
                 controllerShapeName,
                 jointDriverMatrix,
                 jointAddTarget,
                 jointDriverInverseMatrix,
                 pointGrpDriver,
                 prefix,
                 side,
                 jointGrp,
                 rotation,
                 translateOne,
                 translateTwo,
                 rotationOnePos,
                 rotationOneNeg,
                 rotationTwoPos,
                 rotationTwoNeg,
                 offsetTranslate,
                 scaleDriver,
                 ):

        if addJoint:
            self.grpAddJoint= tf.create_parent_transform(parent_list=[''],
                                                         object=jointAddTarget, match_position=jointAddTarget,
                                                         prefix=jointAddTarget, suffix='',
                                                         side='')
            # point constraint
            ptCons = mc.pointConstraint(pointGrpDriver[0], pointGrpDriver[-1], self.grpAddJoint, mo=1)

            # orient constraint
            oriCons = mc.orientConstraint(jointDriverMatrix, self.grpAddJoint, mo=1)

            # scale constraint
            sclCons = mc.scaleConstraint(scaleDriver[0], scaleDriver[-1], self.grpAddJoint, mo=1)

            # rename constraint
            au.constraint_rename([ptCons[0], oriCons[0], sclCons[0]])

            # parent to skin grp
            mc.parent(self.grpAddJoint, jointGrp)

            # connecting node
            self.createPairBlend(jointDriverMatrix=jointDriverMatrix,
                                 jointDriverInverseMatrix=jointDriverInverseMatrix,
                                 jointAddTarget=jointAddTarget,
                                 prefix=prefix, side=side, rotation=rotation,
                                 translateOne=translateOne, translateTwo=translateTwo, offsetTranslate=offsetTranslate,
                                 rotationOnePos=rotationOnePos, rotationOneNeg=rotationOneNeg,
                                 rotationTwoPos=rotationTwoPos, rotationTwoNeg=rotationTwoNeg
                                 )

            # connect the elbow pair blend
            mc.connectAttr(fkIkSetup + '.%sShape' % controllerShapeName, self.pairBlend + '.weight')


    # ==================================================================================================================
    #                                               GENERAL FUNCTION
    # ==================================================================================================================

    def createPairBlend(self, jointDriverMatrix, jointDriverInverseMatrix, jointAddTarget, prefix, side, rotation,
                        translateOne, translateTwo, offsetTranslate, rotationOnePos, rotationOneNeg,
                        rotationTwoPos, rotationTwoNeg):

        getValueTxUpperObjJnt = mc.xform(jointDriverInverseMatrix, ws=1, q=1, t=1)[0]

        multMatrix = mc.createNode('multMatrix', n='%s%s%s_mmtx' % (prefix, 'BlendingShp', side))
        mc.connectAttr(jointDriverMatrix + '.worldMatrix[0]', multMatrix + '.matrixIn[0]')
        mc.connectAttr(jointDriverInverseMatrix + '.worldInverseMatrix[0]', multMatrix + '.matrixIn[1]')

        # create decompose matrix
        decMatrix = mc.createNode('decomposeMatrix', n='%s%s%s_dmtx' % (prefix, 'BlendingShp', side))
        mc.connectAttr(multMatrix+'.matrixSum', decMatrix+'.inputMatrix')

        # create quat to euler
        quatToEuler = mc.createNode('quatToEuler', n='%s%s%s_qte' % (prefix, 'BlendingShp', side))
        mc.connectAttr(decMatrix+'.outputQuatW', quatToEuler+'.inputQuatW')
        mc.connectAttr(decMatrix+'.outputQuat%s' % rotation, quatToEuler+'.inputQuat%s'% rotation)

        # create add double linear
        addDoubleLin = mc.createNode('addDoubleLinear', n='%s%s%s_adl' % (prefix, 'BlendingShp', side))
        mc.connectAttr(quatToEuler+'.outputRotate%s'% rotation, addDoubleLin+'.input1')
        valueInput1 = mc.getAttr(addDoubleLin+'.input1')
        mc.setAttr(addDoubleLin+'.input2', valueInput1*-1)

        # create mult double linear
        multDoubleLin = mc.createNode('multDoubleLinear', n='%s%s%s_mdl' % (prefix, 'BlendingShp', side))
        mc.connectAttr(addDoubleLin+'.output', multDoubleLin+'.input1')
        mc.setAttr(multDoubleLin+'.input2', -1)

        # create pair blend
        self.pairBlend = mc.createNode('pairBlend', n='%s%s%s_pbn' % (prefix, 'BlendingShp', side))
        mc.setAttr(self.pairBlend+'.weight', 0.5)
        mc.connectAttr(multDoubleLin+'.output', self.pairBlend+('.inRotate%s2' % rotation))
        mc.connectAttr(self.pairBlend +'.outRotate%s' % rotation, jointAddTarget + '.rotate%s' % rotation)

    # create translate connected
        adlMultTrans= None
        if translateOne or translateTwo:
            mdlRevTrans = mc.createNode('multDoubleLinear', n='%s%s%s_mdl' % (prefix, 'BlendingShpTrans', side))
            mc.connectAttr(self.pairBlend+'.outRotate%s' % rotation, mdlRevTrans+'.input1')
            mc.setAttr(mdlRevTrans+'.input2', offsetTranslate)

            # adding out rotate both pair blend
            adlMultTrans = mc.createNode('addDoubleLinear', n='%s%s%s_adl' % (prefix, 'BlendingShpTrans', side))
            mc.connectAttr(self.pairBlend+'.outRotate%s' % rotation, adlMultTrans+'.input1')
            mc.connectAttr(mdlRevTrans+'.output', adlMultTrans+'.input2')

        if translateOne:
            # multiply by reverse for left or right condition for connection one
            multConOnePOS = mc.createNode('multDoubleLinear', n='%s%s%s_mdl' % (prefix, 'BlendingShpTransOnePos', side))
            mc.connectAttr(adlMultTrans + '.output', multConOnePOS + '.input1')

            if getValueTxUpperObjJnt > 0:
                mc.setAttr(multConOnePOS + '.input2', rotationOnePos)
            else:
                mc.setAttr(multConOnePOS + '.input2', rotationOnePos*-1)

            multConOneNEG = mc.createNode('multDoubleLinear', n='%s%s%s_mdl' % (prefix, 'BlendingShpTransOneNeg', side))
            mc.connectAttr(adlMultTrans + '.output', multConOneNEG + '.input1')

            if getValueTxUpperObjJnt > 0:
                mc.setAttr(multConOneNEG + '.input2', rotationOneNeg)
            else:
                mc.setAttr(multConOneNEG + '.input2', rotationOneNeg*-1)

            # condition for reverse rotation
            condTransOne = mc.createNode('condition', n='%s%s%s_cnd' % (prefix, 'BlendingShpTransOne', side))
            mc.setAttr(condTransOne + '.operation', 2)

            mc.connectAttr(self.pairBlend +'.outRotate%s' % rotation, condTransOne + '.firstTerm')

            # connect to condition reverse
            mc.connectAttr(multConOnePOS + '.output', condTransOne + '.colorIfFalseR')
            mc.connectAttr(multConOneNEG +'.output', condTransOne + '.colorIfTrueR')

            # connect to translate pair blend
            mc.connectAttr(condTransOne + '.outColorR', self.pairBlend + '.inTranslate%s2' % translateOne)
            mc.connectAttr(self.pairBlend + '.outTranslate%s' % translateOne, jointAddTarget + '.translate%s' % translateOne)

        if translateTwo:
            # multiply by reverse for left or right condition for connection one
            multConTwoPOS = mc.createNode('multDoubleLinear', n='%s%s%s_mdl' % (prefix, 'BlendingShpTransTwoPos', side))
            mc.connectAttr(adlMultTrans + '.output', multConTwoPOS + '.input1')

            if getValueTxUpperObjJnt > 0:
                mc.setAttr(multConTwoPOS + '.input2', rotationTwoPos)
            else:
                mc.setAttr(multConTwoPOS + '.input2', rotationTwoPos * -1)

            multConTwoNEG = mc.createNode('multDoubleLinear', n='%s%s%s_mdl' % (prefix, 'BlendingShpTransTwoNeg', side))
            mc.connectAttr(adlMultTrans + '.output', multConTwoNEG + '.input1')

            if getValueTxUpperObjJnt > 0:
                mc.setAttr(multConTwoNEG + '.input2', rotationTwoNeg)
            else:
                mc.setAttr(multConTwoNEG + '.input2', rotationTwoNeg * -1)

            # condition for reverse rotation
            condTransTwo = mc.createNode('condition', n='%s%s%s_cnd' % (prefix, 'BlendingShpTransTwo', side))
            mc.setAttr(condTransTwo + '.operation', 2)

            mc.connectAttr(self.pairBlend + '.outRotate%s' % rotation, condTransTwo + '.firstTerm')

            # connect to condition reverse
            mc.connectAttr(multConTwoPOS + '.output', condTransTwo + '.colorIfFalseR')
            mc.connectAttr(multConTwoNEG + '.output', condTransTwo + '.colorIfTrueR')

            # connect to translate pair blend
            mc.connectAttr(condTransTwo + '.outColorR', self.pairBlend + '.inTranslate%s2' % translateTwo)
            mc.connectAttr(self.pairBlend + '.outTranslate%s' % translateTwo, jointAddTarget + '.translate%s' % translateTwo)