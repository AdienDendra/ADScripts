import re
from __builtin__ import reload

import maya.cmds as mc

from rigging.tools import AD_utils as au

reload(au)

class BuildTwoSide:
    def __init__(self, bsnName, prefixSquashStretch, prefixRollLow, suffixBsh, prefixRollUp, squashStretchAttr, mouthCtrl,
                 controllerUpRollBshAttr, controllerLowRollBshAttr, prefixCheekOut, cheekOutAttrLFT, cheekOutAttrRGT, sideLFT, sideRGT):

        # TWO SLIDE
        self.twoValueSlider(bsnName=bsnName, controller=mouthCtrl, prefix=prefixSquashStretch, side='', slideAtribute=squashStretchAttr,
                            subPrefixOne='Stretch', valuePosOne=10, subPrefixTwo='Squash', valuePosTwo=-10, connect=True, suffixBsh=suffixBsh)

        self.twoValueSlider(bsnName=bsnName, controller=mouthCtrl, prefix=prefixRollLow, side='', slideAtribute=controllerLowRollBshAttr,
                            subPrefixOne='Out', valuePosOne=10, subPrefixTwo='In', valuePosTwo=-10, connect=True, suffixBsh=suffixBsh)

        self.twoValueSlider(bsnName=bsnName, controller=mouthCtrl, prefix=prefixRollUp, side='', slideAtribute=controllerUpRollBshAttr,
                            subPrefixOne='Out', valuePosOne=10, subPrefixTwo='In', valuePosTwo=-10, connect=True, suffixBsh=suffixBsh)

        self.oneValueSlider(bsnName=bsnName, controller=mouthCtrl, prefix=prefixCheekOut, side=sideLFT, slideAtribute=cheekOutAttrLFT, subPrefix='',
                            valueNode=10, sideRGT=sideRGT, sideLFT=sideLFT, suffixBsh=suffixBsh)

        self.oneValueSlider(bsnName=bsnName, controller=mouthCtrl, prefix=prefixCheekOut, side=sideRGT, slideAtribute=cheekOutAttrRGT, subPrefix='',
                            valueNode=10, sideRGT=sideRGT, sideLFT=sideLFT, suffixBsh=suffixBsh)

    def combinedValueSlider(self, bsnName, controller, side, subPrefixFirst='', subPrefixSecond='', clampDriverFirstOne='',
                            clampDriverFirstTwo='', clampDriverSecondOne='', clampDriverSecondTwo='', twoSide=True):

        ctrlNew = self.replacePosLFTRGT(controller, 'BshRGT', 'BshLFT')
        listWeight = mc.listAttr(bsnName+'.w', m=True)

        # DRIVER VALUE
        multDoubleLinearCombinedOne = mc.createNode('multDoubleLinear', n=au.prefix_name(ctrlNew) + subPrefixFirst + 'BshCombined' + side + '_mdl')
        mc.connectAttr(clampDriverFirstOne + '.outputR', multDoubleLinearCombinedOne + '.input1')
        mc.connectAttr(clampDriverFirstTwo + '.outputR', multDoubleLinearCombinedOne + '.input2')

        if twoSide :
            multDoubleLinearCombinedTwo = mc.createNode('multDoubleLinear', n=au.prefix_name(ctrlNew) + subPrefixSecond + 'BshCombined' + side + '_mdl')
            mc.connectAttr(clampDriverSecondOne + '.outputR', multDoubleLinearCombinedTwo + '.input1')
            mc.connectAttr(clampDriverSecondTwo + '.outputR', multDoubleLinearCombinedTwo + '.input2')
            self.connectNodeToBsh(listWeight, multDoubleLinearCombinedTwo, 'output', bsnName=bsnName, sideRGT='BshCombinedRGT', sideLFT='BshCombinedLFT', side=side)

        # CONNECT TO BSH
        self.connectNodeToBsh(listWeight, multDoubleLinearCombinedOne, 'output', bsnName=bsnName, sideRGT='BshCombinedRGT', sideLFT='BshCombinedLFT', side=side)

    def twoValueSlider(self, bsnName, controller, prefix, side, slideAtribute, subPrefixOne, valuePosOne, subPrefixTwo, valuePosTwo, suffixBsh,
                       sideRGT='', sideLFT='', connect=True, clampUpMin=0.0, clampUpMax=10.0, clampDownMin=0.0,
                       clampDownMax=10.0):
        # UP
        ctrlNew = self.replacePosLFTRGT(prefix, sideRGT, sideLFT)
        multDoubleLinearUp = mc.createNode('multDoubleLinear', n=au.prefix_name(ctrlNew) + subPrefixOne + 'Bsh' + side + '_mdl')
        mc.setAttr(multDoubleLinearUp + '.input2', 1.0/valuePosOne)
        mc.connectAttr(controller + '.%s' % slideAtribute, multDoubleLinearUp + '.input1')

        clampUp = mc.createNode('clamp', n=au.prefix_name(ctrlNew) + subPrefixOne + 'Bsh' + side + '_clm')
        mc.setAttr(clampUp + '.maxR', clampUpMax)
        mc.setAttr(clampUp + '.minR', clampUpMin)

        mc.connectAttr(multDoubleLinearUp + '.output', clampUp + '.inputR')

        # DOWN
        multDoubleLinearDown = mc.createNode('multDoubleLinear', n=au.prefix_name(ctrlNew) + subPrefixTwo + 'Bsh' + side + '_mdl')
        mc.setAttr(multDoubleLinearDown + '.input2', 1.0/valuePosTwo)
        mc.connectAttr(controller + '.%s' % slideAtribute, multDoubleLinearDown + '.input1')

        clampDown = mc.createNode('clamp', n=au.prefix_name(ctrlNew) + subPrefixTwo + 'Bsh' + side + '_clm')
        mc.setAttr(clampDown + '.maxR', clampDownMax)
        mc.setAttr(clampDown + '.minR', clampDownMin)
        mc.connectAttr(multDoubleLinearDown + '.output', clampDown + '.inputR')

        # CONNECT TO BSH
        if connect:
            listWeight = mc.listAttr(bsnName+'.w', m=True)
            self.connectNodeToBsh(listWeight, clampUp, 'outputR', bsnName=bsnName, sideRGT=sideRGT, sideLFT=sideLFT, side=side, suffixBsh=suffixBsh)
            self.connectNodeToBsh(listWeight, clampDown, 'outputR', bsnName=bsnName, sideRGT=sideRGT, sideLFT=sideLFT, side=side, suffixBsh=suffixBsh)
        # else:
        return clampUp, clampDown

    def oneValueSlider(self, bsnName, controller, side, slideAtribute, prefix, suffixBsh, subPrefix, valueNode, sideRGT='', sideLFT='',
                       clampMax=10.0, clampMin=0.0
                       ):
        ctrlNew = self.replacePosLFTRGT(prefix, sideRGT, sideLFT)
        multDoubleLinear = mc.createNode('multDoubleLinear', n=au.prefix_name(ctrlNew) + subPrefix + 'Bsh' + side + '_mdl')
        mc.setAttr(multDoubleLinear + '.input2', 1.0 / valueNode)
        mc.connectAttr(controller + '.%s' % slideAtribute, multDoubleLinear + '.input1')

        clamp = mc.createNode('clamp', n=au.prefix_name(ctrlNew) + subPrefix + 'Bsh' + side + '_clm')
        mc.setAttr(clamp + '.maxR', clampMax)
        mc.setAttr(clamp + '.minR', clampMin)

        mc.connectAttr(multDoubleLinear + '.output', clamp + '.inputR')
        # CONNECT TO BSH
        listWeight = mc.listAttr(bsnName+'.w', m=True)

        # UP
        self.connectNodeToBsh(listWeight, clamp, 'outputR', bsnName=bsnName, sideRGT=sideRGT, sideLFT=sideLFT, side=side, suffixBsh=suffixBsh)
        return clamp

    def replacePosLFTRGT(self, nameObj, sideRGT, sideLFT):
        if sideRGT in nameObj:
            crvNewName = nameObj.replace(sideRGT, '')
        elif sideLFT in nameObj:
            crvNewName = nameObj.replace(sideLFT, '')
        else:
            crvNewName = nameObj

        return crvNewName

    def connectNodeToBsh(self, listWeight, connectorNode, atttNode, bsnName, sideRGT, sideLFT, side, suffixBsh):
        list = []
        for i in listWeight:
            listI = i[:-7]
            list.append(listI)

        baseName = self.replacePosLFTRGT(connectorNode, sideRGT, sideLFT)
        if re.compile('|'.join(list), re.IGNORECASE).search(connectorNode):  # re.IGNORECASE is used to ignore case
            mc.connectAttr(connectorNode +'.%s' % atttNode, bsnName +'.%s%s%s' % (au.prefix_name(baseName), side, '_' + suffixBsh))
        else:
            print (mc.error ('There is no weight on blendshape'))

class BuildOneSide:
    def __init__(self, bsnName, mouthCtrl, upperLipRollCtrl, lowerLipRollCtrl, upperLipCtrl, lowerLipCtrl, upperLipCtrlOut,
                 lowerLipCtrlOut, mouthTwistCtrl, ACtrl, AhCtrl, ECtrl, FVCtrl, LCtrl, MBPCtrl, OhCtrl, OOOCtrl, RCtrl,
                 TKGCtrl, ThCtrl, UhCtrl, YCtrl, NCtrl):

        # TWO VALUE
        self.twoValueSlider(bsnName=bsnName, controller=mouthCtrl, slideAtribute='translateY',
                            subPrefixOne='Up', valuePosOne=2, subPrefixTwo='Down', valuePosTwo=-2)
        self.twoValueSlider(bsnName=bsnName, controller=mouthCtrl, slideAtribute='translateX',
                            subPrefixOne='LFT', valuePosOne=2, subPrefixTwo='RGT', valuePosTwo=-2)

        # self.twoValueSlider(bsnName=bsnName, controller=upperLipRollCtrl, slideAtribute='translateY',
        #                     subPrefixOne='Up', valuePosOne=1, subPrefixTwo='Down', valuePosTwo=-1, addPrefix='MID',
        #                     sideRGT='BshMID', sideLFT='BshMID')
        #
        # self.twoValueSlider(bsnName=bsnName, controller=lowerLipRollCtrl, slideAtribute='translateY',
        #                     subPrefixOne='Up', valuePosOne=-1, subPrefixTwo='Down', valuePosTwo=1, addPrefix='MID',
        #                     sideRGT='BshMID', sideLFT='BshMID')



        self.twoValueSlider(bsnName=bsnName, controller=upperLipCtrl, slideAtribute='translateY',
                            subPrefixOne='Up', valuePosOne=1, subPrefixTwo='Down', valuePosTwo=-1, addPrefix='MID',
                            sideRGT='BshMID', sideLFT='BshMID')

        self.twoValueSlider(bsnName=bsnName, controller=lowerLipCtrl, slideAtribute='translateY',
                            subPrefixOne='Up', valuePosOne=1, subPrefixTwo='Down', valuePosTwo=-1, addPrefix='MID',
                            sideRGT='BshMID', sideLFT='BshMID')

        self.twoValueSlider(bsnName=bsnName, controller=mouthTwistCtrl, slideAtribute='translateX',
                            subPrefixOne='RGT', valuePosOne=2, subPrefixTwo='LFT', valuePosTwo=-2)

        # ONE VALUE
        self.oneValueSlider(bsnName=bsnName, controller=upperLipCtrlOut, slideAtribute='translateY',
                            subPrefix='', valueNode=3, addPrefix='MID', sideRGT='BshMID', sideLFT='BshMID')
        self.oneValueSlider(bsnName=bsnName, controller=lowerLipCtrlOut, slideAtribute='translateY',
                            subPrefix='', valueNode=3, addPrefix='MID', sideRGT='BshMID', sideLFT='BshMID')

        # self.oneValueSlider(bsnName=bsnName, controller=lowerLipRollCtrl, slideAtribute='translateY',
        #                     subPrefix='HalfUp', valueNode=-1, addPrefix='MID',
        #                     sideRGT='BshMID', sideLFT='BshMID')
        #
        # self.oneValueSlider(bsnName=bsnName, controller=upperLipRollCtrl, slideAtribute='translateY',
        #                     subPrefix='HalfDown', valueNode=-1, addPrefix='MID',
        #                     sideRGT='BshMID', sideLFT='BshMID')

        self.oneValueSlider(bsnName=bsnName, controller=upperLipRollCtrl, slideAtribute='translateY',
                            subPrefix='Up', valueNode=1, addPrefix='MID',
                            sideRGT='BshMID', sideLFT='BshMID')

        self.oneValueSlider(bsnName=bsnName, controller=lowerLipRollCtrl, slideAtribute='translateY',
                             subPrefix='Down', valueNode=1, addPrefix='MID',
                            sideRGT='BshMID', sideLFT='BshMID')

        # LETTER MOUTH
        self.oneValueSlider(bsnName=bsnName, controller=ACtrl, slideAtribute='translateX',
                             subPrefix='', valueNode=4, addPrefix='',
                            )
        self.oneValueSlider(bsnName=bsnName, controller=AhCtrl, slideAtribute='translateX',
                             subPrefix='', valueNode=4, addPrefix='',
                            )
        self.oneValueSlider(bsnName=bsnName, controller=ECtrl, slideAtribute='translateX',
                             subPrefix='', valueNode=4, addPrefix='',
                            )
        self.oneValueSlider(bsnName=bsnName, controller=FVCtrl, slideAtribute='translateX',
                             subPrefix='', valueNode=4, addPrefix='',
                            )
        self.oneValueSlider(bsnName=bsnName, controller=LCtrl, slideAtribute='translateX',
                             subPrefix='', valueNode=4, addPrefix='',
                            )
        self.oneValueSlider(bsnName=bsnName, controller=MBPCtrl, slideAtribute='translateX',
                             subPrefix='', valueNode=4, addPrefix='',
                            )
        self.oneValueSlider(bsnName=bsnName, controller=OhCtrl, slideAtribute='translateX',
                             subPrefix='', valueNode=4, addPrefix='',
                            )
        self.oneValueSlider(bsnName=bsnName, controller=OOOCtrl, slideAtribute='translateX',
                             subPrefix='', valueNode=4, addPrefix='',
                            )
        self.oneValueSlider(bsnName=bsnName, controller=RCtrl, slideAtribute='translateX',
                             subPrefix='', valueNode=4, addPrefix='',
                            )
        self.oneValueSlider(bsnName=bsnName, controller=TKGCtrl, slideAtribute='translateX',
                             subPrefix='', valueNode=4, addPrefix='',
                            )
        self.oneValueSlider(bsnName=bsnName, controller=ThCtrl, slideAtribute='translateX',
                             subPrefix='', valueNode=4, addPrefix='',
                            )
        self.oneValueSlider(bsnName=bsnName, controller=UhCtrl, slideAtribute='translateX',
                             subPrefix='', valueNode=4, addPrefix='',
                            )
        self.oneValueSlider(bsnName=bsnName, controller=YCtrl, slideAtribute='translateX',
                             subPrefix='', valueNode=4, addPrefix='',
                            )
        self.oneValueSlider(bsnName=bsnName, controller=NCtrl, slideAtribute='translateX',
                             subPrefix='', valueNode=4, addPrefix='',
                            )

    def twoValueSlider(self, bsnName, controller, slideAtribute, subPrefixOne, valuePosOne, subPrefixTwo,
                       valuePosTwo, addPrefix='', sideRGT='Bsh', sideLFT='Bsh', clampUpMin=0.0, clampUpMax=1.0, clampDownMin=0.0,
                       clampDownMax=1.0):
        # UP
        ctrlNew = self.replacePosLFTRGT(controller, sideRGT, sideLFT)
        multDoubleLinearUp = mc.createNode('multDoubleLinear',
                                           n=au.prefix_name(ctrlNew) + subPrefixOne + '_mdl')
        mc.setAttr(multDoubleLinearUp + '.input2', 1.0 / valuePosOne)
        mc.connectAttr(controller + '.%s' % slideAtribute, multDoubleLinearUp + '.input1')

        clampUp = mc.createNode('clamp', n=au.prefix_name(ctrlNew) + subPrefixOne + '_clm')
        mc.setAttr(clampUp + '.maxR', clampUpMax)
        mc.setAttr(clampUp + '.minR', clampUpMin)

        mc.connectAttr(multDoubleLinearUp + '.output', clampUp + '.inputR')

        # DOWN
        multDoubleLinearDown = mc.createNode('multDoubleLinear',
                                             n=au.prefix_name(ctrlNew) + subPrefixTwo + '_mdl')
        mc.setAttr(multDoubleLinearDown + '.input2', 1.0 / valuePosTwo)
        mc.connectAttr(controller + '.%s' % slideAtribute, multDoubleLinearDown + '.input1')

        clampDown = mc.createNode('clamp', n=au.prefix_name(ctrlNew) + subPrefixTwo + '_clm')
        mc.setAttr(clampDown + '.maxR', clampDownMax)
        mc.setAttr(clampDown + '.minR', clampDownMin)

        mc.connectAttr(multDoubleLinearDown + '.output', clampDown + '.inputR')

        # CONNECT TO BSH
        listWeight = mc.listAttr(bsnName + '.w', m=True)
        # UP
        self.connectNodeToBsh(listWeight, clampUp, 'outputR', bsnName, addPrefix, sideRGT=sideRGT, sideLFT=sideLFT)
        self.connectNodeToBsh(listWeight, clampDown, 'outputR', bsnName, addPrefix, sideRGT=sideRGT, sideLFT=sideLFT)

        return clampUp, clampDown

    def oneValueSlider(self, bsnName, controller, slideAtribute, subPrefix, valueNode, addPrefix, sideRGT='Bsh', sideLFT='Bsh',
                       clampMax=1.0, clampMin=0.0,
                       ):
        ctrlNew = self.replacePosLFTRGT(controller, sideRGT, sideLFT)
        multDoubleLinear = mc.createNode('multDoubleLinear',
                                         n=au.prefix_name(ctrlNew) + subPrefix + '_mdl')
        mc.setAttr(multDoubleLinear + '.input2', 1.0 / valueNode)
        mc.connectAttr(controller + '.%s' % slideAtribute, multDoubleLinear + '.input1')

        clamp = mc.createNode('clamp', n=au.prefix_name(ctrlNew) + subPrefix + '_clm')
        mc.setAttr(clamp + '.maxR', clampMax)
        mc.setAttr(clamp + '.minR', clampMin)

        mc.connectAttr(multDoubleLinear + '.output', clamp + '.inputR')

        # CONNECT TO BSH
        listWeight = mc.listAttr(bsnName + '.w', m=True)

        # UP
        self.connectNodeToBsh(listWeight, clamp, 'outputR', bsnName, addPrefix, sideRGT=sideRGT, sideLFT=sideLFT)

    def replacePosLFTRGT(self, nameObj, sideRGT, sideLFT):
        if sideRGT in nameObj:
            crvNewName = nameObj.replace(sideRGT, '')
        elif sideLFT in nameObj:
            crvNewName = nameObj.replace(sideLFT, '')
        else:
            crvNewName = nameObj

        return crvNewName

    def connectNodeToBsh(self, listWeight, connectorNode, atttNode, bsnName, addPrefix, sideRGT, sideLFT):
        list = []
        for i in listWeight:
            listI = i[:-7]
            list.append(listI)

        baseName = self.replacePosLFTRGT(connectorNode, sideRGT, sideLFT)
        if re.compile('|'.join(list), re.IGNORECASE).search(
                connectorNode):  # re.IGNORECASE is used to ignore case
            mc.connectAttr(connectorNode + '.%s' % atttNode,
                           bsnName + '.%s%s%s' % (au.prefix_name(baseName), addPrefix, '_ply'))
        else:
            print(mc.error('There is no weight on blendshape'))

class BuildFree:
    def __init__(self, bsnName, rollCtrl, upperWeightBsnMID,
                 upperWeightBsnLFT, upperWeightBsnRGT,
                 lowerWeightBsnMID, lowerWeightBsnLFT,
                 lowerWeightBsnRGT):

        self.oneValueSlider(bsnName, controller=rollCtrl, slideAtribute='translateY',
                            valueNode=3, weightBsnName=upperWeightBsnMID)

        self.oneValueSlider(bsnName, controller=rollCtrl, slideAtribute='translateY',
                            valueNode=3, weightBsnName=upperWeightBsnLFT)

        self.oneValueSlider(bsnName, controller=rollCtrl, slideAtribute='translateY',
                            valueNode=3, weightBsnName=upperWeightBsnRGT)

        self.oneValueSlider(bsnName, controller=rollCtrl, slideAtribute='translateY',
                            valueNode=3, weightBsnName=lowerWeightBsnMID)

        self.oneValueSlider(bsnName, controller=rollCtrl, slideAtribute='translateY',
                            valueNode=3, weightBsnName=lowerWeightBsnLFT)

        self.oneValueSlider(bsnName, controller=rollCtrl, slideAtribute='translateY',
                            valueNode=3, weightBsnName=lowerWeightBsnRGT)

        # self.twoValueSlider(bsnName, controller=mouthCtrlRGT, slideAtribute='translateY',
        #                     subPrefixOne='SmileRGT', valuePosOne=1.5, subPrefixTwo='DownRGT',
        #                valuePosTwo=-1.5, weightBsnName=mouthCtrlSmileRGT,
        #                connect=True)

    def twoValueSlider(self, bsnName, controller, slideAtribute, subPrefixOne, valuePosOne, subPrefixTwo,
                       valuePosTwo, weightBsnName,
                     connect=True):
        # UP
        # ctrlNew = self.replacePosLFTRGT(weightBsnName, sideRGT=sideRGT, sideLFT=sideLFT)
        weightNames = au.prefix_name(weightBsnName)
        weightName = weightNames.replace(subPrefixOne,'').replace(subPrefixTwo,'')

        multDoubleLinearUp = mc.createNode('multDoubleLinear',
                                           n=weightName[:-3]+ subPrefixOne+ weightName[-3:] +'_mdl')
        mc.setAttr(multDoubleLinearUp + '.input2', 1.0 / valuePosOne)
        mc.connectAttr(controller + '.%s' % slideAtribute, multDoubleLinearUp + '.input1')

        clampUp = mc.createNode('clamp', n=weightName[:-3]+ subPrefixOne+ weightName[-3:] +'_clm')
        mc.setAttr(clampUp + '.maxR', 1)
        mc.connectAttr(multDoubleLinearUp + '.output', clampUp + '.inputR')

        # DOWN
        multDoubleLinearDown = mc.createNode('multDoubleLinear',
                                             n=weightName[:-3]+ subPrefixTwo+ weightName[-3:] + '_mdl')
        mc.setAttr(multDoubleLinearDown + '.input2', 1.0 / valuePosTwo)
        mc.connectAttr(controller + '.%s' % slideAtribute, multDoubleLinearDown + '.input1')

        clampDown = mc.createNode('clamp', n=weightName[:-3]+ subPrefixTwo+ weightName[-3:] + '_clm')
        mc.setAttr(clampDown + '.maxR', 1)
        mc.connectAttr(multDoubleLinearDown + '.output', clampDown + '.inputR')

        # CONNECT TO BSH
        if connect:
            listWeight = mc.listAttr(bsnName + '.w', m=True)
            self.connectNodeToBsh(listWeight, clampUp, 'outputR', bsnName=bsnName)
            self.connectNodeToBsh(listWeight, clampDown, 'outputR', bsnName=bsnName)
        return clampUp, clampDown

    def oneValueSlider(self, bsnName, controller, slideAtribute, valueNode, weightBsnName):
        # ctrlNew = self.replacePosLFTRGT(controller, sideRGT, sideLFT)
        weightName = au.prefix_name(weightBsnName)
        multDoubleLinearUp = mc.createNode('multDoubleLinear',
                                           n=weightName[:-3]+ weightName[-3:] + '_mdl')
        mc.setAttr(multDoubleLinearUp + '.input2', 1.0 / valueNode)
        mc.connectAttr(controller + '.%s' % slideAtribute, multDoubleLinearUp + '.input1')


        # CONNECT TO BSH
        listWeight = mc.listAttr(bsnName + '.w', m=True)

        # UP
        self.connectNodeToBsh(listWeight, multDoubleLinearUp, 'output', bsnName=bsnName)

    def replacePosLFTRGT(self, nameObj, sideRGT, sideLFT):
        if sideRGT in nameObj:
            crvNewName = nameObj.replace(sideRGT, '')
        elif sideLFT in nameObj:
            crvNewName = nameObj.replace(sideLFT, '')
        else:
            crvNewName = nameObj

        return crvNewName

    def connectNodeToBsh(self, listWeight, connectorNode, atttNode, bsnName):
        list = []
        for i in listWeight:
            listI = i[:-7]
            list.append(listI)

        # baseName = self.replacePosLFTRGT(connectorNode, sideRGT=sideRGT, sideLFT=sideLFT)
        if re.compile('|'.join(list), re.IGNORECASE).search(connectorNode):  # re.IGNORECASE is used to ignore case
            mc.connectAttr(connectorNode + '.%s' % atttNode,
                           bsnName + '.%s%s' % (au.prefix_name(connectorNode) , '_ply'))
        else:
            print(mc.error('There is no weight on blendshape'))