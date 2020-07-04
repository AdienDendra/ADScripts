from __builtin__ import reload

import maya.cmds as mc

from rigging.library.base.face import brow as br
from rigging.library.utils import controller as ct
from rigging.library.utils import transform as tf
from rigging.tools import AD_utils as au

reload (ct)
reload (tf)
reload (au)
reload (br)

class Brows:
    def __init__(self,
                 browTwJntLFT,
                 browInJntLFT,
                 browMidJntLFT,
                 browOutJntLFT,
                 browTipJntLFT,
                 browTwJntRGT,
                 browInJntRGT,
                 browMidJntRGT,
                 browOutJntRGT,
                 browTipJntRGT,
                 browCenterJnt,
                 browTwPrefix,
                 browInPrefix,
                 browMidPrefix,
                 browOutPrefix,
                 browsPrefix,
                 browTipPrefix,
                 browCenterPrefix,
                 scale,
                 sideRGT,
                 sideLFT,
                 browInGrpRotOffset,
                 browMidGrpRotOffset,
                 browOutGrpRotOffset,
                 browTipGrpRotOffset,
                 headUpCtrlGimbal,
                 suffixController
                 ):

        ctrlDriverGrp = mc.group(em=1, n='browCtrlAll' + '_grp')
        mc.parent(ctrlDriverGrp, headUpCtrlGimbal)
        self.browAllCtrl = ctrlDriverGrp

    # ==================================================================================================================
    #                                               BROWS CONTROLLER
    # ==================================================================================================================

        leftBrow = br.Build(browTwJnt=browTwJntLFT,
                     browInJnt=browInJntLFT,
                     browMidJnt=browMidJntLFT,
                     browOutJnt=browOutJntLFT,
                     browTipJnt=browTipJntLFT,
                     browTwPrefix=browTwPrefix,
                     browInPrefix=browInPrefix,
                     browMidPrefix=browMidPrefix,
                     browOutPrefix=browOutPrefix,
                     browsPrefix=browsPrefix,
                     browTipPrefix=browTipPrefix,
                     scale=scale,
                     sideRGT=sideRGT,
                     sideLFT=sideLFT,
                     side=sideLFT,
                    browInGrpRotOffset=browInGrpRotOffset,
                    browMidGrpRotOffset=browMidGrpRotOffset,
                    browOutGrpRotOffset=browOutGrpRotOffset,
                    browTipGrpRotOffset=browTipGrpRotOffset,
                     suffixController=suffixController)

        rightBrow = br.Build(browTwJnt=browTwJntRGT,
                             browInJnt=browInJntRGT,
                            browMidJnt=browMidJntRGT,
                            browOutJnt=browOutJntRGT,
                            browTipJnt=browTipJntRGT,
                            browTwPrefix=browTwPrefix,
                            browInPrefix=browInPrefix,
                            browMidPrefix=browMidPrefix,
                            browOutPrefix=browOutPrefix,
                            browsPrefix=browsPrefix,
                            browTipPrefix=browTipPrefix,
                            scale=scale,
                            sideRGT=sideRGT,
                            sideLFT=sideLFT,
                            side=sideRGT,
                         browInGrpRotOffset=browInGrpRotOffset,
                         browMidGrpRotOffset=browMidGrpRotOffset,
                         browOutGrpRotOffset=browOutGrpRotOffset,
                         browTipGrpRotOffset=browTipGrpRotOffset,
                            suffixController=suffixController)

        centerBrowCtrl =ct.Control(match_obj_first_position=browCenterJnt,
                                   prefix=browCenterPrefix,
                                   shape=ct.JOINT, groups_ctrl=['', 'Offset'],
                                   ctrl_size=scale * 0.07, suffix=suffixController,
                                   ctrl_color='blue', lock_channels=['v'],
                                   )

        browCenterGrp = tf.create_parent_transform(parent_list=['', 'Offset'], object=browCenterJnt, match_position=browCenterJnt,
                                                   prefix=browCenterPrefix, suffix='_jnt')

        au.connect_attr_object(centerBrowCtrl.control, browCenterJnt)

        # ==============================================================================================================
        #                                               BROWS CENTER SETUP
        # ==============================================================================================================

        sumNodeBrow = self.sum(targetJnt=browCenterGrp[1] + '.translateY', sideRGT=sideRGT, sideLFT=sideLFT)

        sumNodeBrowIn = self.sum(targetJnt=sumNodeBrow + '.input1D[2]', sideRGT=sideRGT, sideLFT=sideLFT)

        self.dividedTwoItems(browFirstCtrl=leftBrow.browCtrl, browSecondCtrl=rightBrow.browCtrl,
                         targetSum0=sumNodeBrow + '.input1D[0]',
                         targetSum1=sumNodeBrow + '.input1D[1]',
                         sideRGT=sideRGT, sideLFT=sideLFT, sideObjOne=sideLFT, sideObjTwo=sideRGT,
                             addPrefixFirst='StCtr',
                             addPrefixSecond='NdCtr')

        self.dividedTwoItems(browFirstCtrl=leftBrow.browInCtrl, browSecondCtrl=rightBrow.browInCtrl,
                             targetSum0=sumNodeBrowIn + '.input1D[0]',
                             targetSum1=sumNodeBrowIn + '.input1D[1]',
                             sideRGT=sideRGT, sideLFT=sideLFT, sideObjOne=sideLFT, sideObjTwo=sideRGT,
                             objectSecondOne=leftBrow.browInCtrl, attrSecondOne=leftBrow.browCenterInAttr,
                             objectSecondTwo=rightBrow.browInCtrl, attrSecondTwo=rightBrow.browCenterInAttr,
                             addAttr=True,
                             addPrefixFirst='StIn',
                             addPrefixSecond='NdIn')

        mc.connectAttr(browCenterGrp[1] +'.translateY', centerBrowCtrl.parent_control[1] + '.translateY')

        # ==============================================================================================================
        #                                               BROWS SETUP
        # ==============================================================================================================

        sumBrowLFT = self.sum(targetJnt=leftBrow.browMidGrp[2] + '.translateY', sideRGT=sideRGT, sideLFT=sideLFT, side=sideLFT)
        self.dividedTwoItems(browFirstCtrl=leftBrow.browInCtrl, browSecondCtrl=leftBrow.browOutCtrl,
                             targetSum0=sumBrowLFT + '.input1D[0]',
                             targetSum1=sumBrowLFT + '.input1D[1]', sideRGT=sideRGT, sideLFT=sideLFT,
                             sideObjOne=sideLFT, sideObjTwo=sideLFT,
                             objectSecondOne=leftBrow.browInCtrl, attrSecondOne=leftBrow.browMidInAttr,
                             objectSecondTwo=leftBrow.browOutCtrl, attrSecondTwo=leftBrow.browMidOutAttr,
                             addAttr=True,
                             addPrefixFirst='StInOut',
                             addPrefixSecond='NdInOut')

        mc.connectAttr(leftBrow.browMidGrp[2] + '.translateY', leftBrow.browMidCtrlOffset+ '.translateY')

        sumBrowRGT = self.sum(targetJnt=rightBrow.browMidGrp[2] + '.translateY', sideRGT=sideRGT, sideLFT=sideLFT, side=sideRGT)
        self.dividedTwoItems(browFirstCtrl=rightBrow.browInCtrl, browSecondCtrl=rightBrow.browOutCtrl,
                             targetSum0=sumBrowRGT + '.input1D[0]',
                             targetSum1=sumBrowRGT + '.input1D[1]', sideRGT=sideRGT, sideLFT=sideLFT,
                             sideObjOne=sideRGT, sideObjTwo=sideRGT,
                             objectSecondOne=rightBrow.browInCtrl, attrSecondOne=rightBrow.browMidInAttr,
                             objectSecondTwo=rightBrow.browOutCtrl, attrSecondTwo=rightBrow.browMidOutAttr,
                             addAttr=True,
                             addPrefixFirst='StInOut',
                             addPrefixSecond='NdInOut')

        mc.connectAttr(rightBrow.browMidGrp[2] + '.translateY', rightBrow.browMidCtrlOffset + '.translateY')

        # PARENT TO THE GROUP
        mc.parent(centerBrowCtrl.parent_control[0], leftBrow.grpBrowAll, rightBrow.grpBrowAll, ctrlDriverGrp)


    def dividedTwoItems(self, browFirstCtrl, browSecondCtrl, targetSum0, targetSum1, sideRGT, sideLFT, sideObjOne, sideObjTwo,
                        objectSecondOne='', attrSecondOne='', objectSecondTwo='', attrSecondTwo='', addAttr=False, addPrefixFirst='',
                        addPrefixSecond=''):
        if addAttr:
            itemFirstDiv = self.divide(object=browFirstCtrl, sideRGT=sideRGT, sideLFT=sideLFT,
                                       side=sideObjOne, target=False, addPrefix=addPrefixFirst)
            itemSecondDiv = self.divide(object=browSecondCtrl, sideRGT=sideRGT, sideLFT=sideLFT,
                                        side=sideObjTwo, target=False, addPrefix=addPrefixSecond)
            self.multiply(objectFirst=itemFirstDiv, objectSecond=objectSecondOne, target=targetSum0, sideRGT=sideRGT, sideLFT=sideLFT,
                          side=sideObjOne, attrFirst='outputY', attrSecond=attrSecondOne,addPrefix=addPrefixFirst)

            self.multiply(objectFirst=itemSecondDiv, objectSecond=objectSecondTwo, target=targetSum1, sideRGT=sideRGT, sideLFT=sideLFT,
                          side=sideObjTwo, attrFirst='outputY', attrSecond=attrSecondTwo, addPrefix=addPrefixSecond)

        else:
            itemFirstDiv = self.divide(object=browFirstCtrl,  targetSum=targetSum0, sideRGT=sideRGT, sideLFT=sideLFT,
                                       side=sideObjOne, addPrefix=addPrefixFirst)
            itemSecondDiv = self.divide(object=browSecondCtrl, targetSum=targetSum1, sideRGT=sideRGT, sideLFT=sideLFT,
                                        side=sideObjTwo, addPrefix=addPrefixSecond)

    def divide(self, object,sideRGT, sideLFT, side, addPrefix, inputTrans2Y=2,  targetSum='', target=True):
        if sideRGT in object:
            newName = object.replace(sideRGT, '')
        elif sideLFT in object:
            newName = object.replace(sideLFT, '')
        else:
            newName = object

        div = mc.createNode('multiplyDivide', n=au.prefix_name(newName) + 'TyDiv' + addPrefix + side + '_mdn')
        mc.connectAttr(object +'.translateY', div + '.input1Y')
        mc.setAttr(div + '.operation', 2)
        mc.setAttr(div + '.input2Y', inputTrans2Y)
        if target:
            mc.connectAttr(div+'.outputY', targetSum)
        else:
            return div

    def multiply(self, objectFirst, objectSecond, target, sideRGT, sideLFT, side, attrFirst, attrSecond, addPrefix):
        if sideRGT in objectFirst:
            newName = objectFirst.replace(sideRGT, '')
        elif sideLFT in objectFirst:
            newName = objectFirst.replace(sideLFT, '')
        else:
            newName = objectFirst

        div = mc.createNode('multiplyDivide', n=au.prefix_name(newName) + 'TyMul' + addPrefix + side + '_mdn')
        mc.connectAttr(objectFirst + '.%s'% attrFirst, div + '.input1Y')
        mc.connectAttr(objectSecond + '.%s'% attrSecond, div + '.input2Y')

        mc.connectAttr(div +'.outputY', target)
        return div

    # connectAttr - f
    # noseWeightTransYCtrl_pma.output1D
    # noseWeightJawTransYCtrl_pma.input1D[0];

    def sum(self, targetJnt, sideRGT, sideLFT, side=''):
        if sideRGT in targetJnt:
            newName = targetJnt.replace(sideRGT, '')
        elif sideLFT in targetJnt:
            newName = targetJnt.replace(sideLFT, '')
        else:
            newName = targetJnt

        sum = mc.createNode('plusMinusAverage', n=au.prefix_name(newName) + 'Ty' + side + '_pma')
        mc.connectAttr(sum + '.output1D', targetJnt)

        return sum





