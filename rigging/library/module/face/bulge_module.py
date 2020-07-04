from __builtin__ import reload

import maya.cmds as mc

from rigging.library.utils import controller as ct
from rigging.library.utils import transform as tf
from rigging.tools import AD_utils as au

reload (ct)
reload (tf)
reload (au)


class Bulge:
    def __init__(self,
                 faceUtilsGrp,
                 faceAnimCtrlGrp,
                 cheekBulgeLFTJnt,
                 cheekBulgePrefix,
                 browInBulgePrefix,
                 browOutBulgePrefix,
                 cornerMouthBulgePrefix,
                 noseBulgePrefix,
                 chinBulgePrefix,
                 cheekBulgeRGTJnt,
                 browInBulgeLFTJnt,
                 browInBulgeRGTJnt,
                 browOutBulgeLFTJnt,
                 browOutBulgeRGTJnt,
                 cornerMouthBulgeLFTJnt,
                 cornerMouthBulgeRGTJnt,
                 noseBulgeJnt,
                 chinBulgeJnt,
                 bulgeMesh,
                 sideLFT,
                 sideRGT,
                 headUpCtrlGimbal,
                 headLowCtrlGimbal,
                 noseDrv03ctrl,
                 chinCtrl,
                 cornerMouthLFTCtrl,
                 cornerMouthRGTCtrl,
                 scale,
                 addSet):

        bulgeGrp = mc.group(em=1, n='bulgeHandle_grp')
        mc.parent(bulgeGrp, faceUtilsGrp)

        cheekBulgeLFTCtrl = self.bulgeCtrl(bulgePos=cheekBulgeLFTJnt, bulgePrefix=cheekBulgePrefix,
                                            side=sideLFT, scale=scale)

        cheekBulgeRGTCtrl = self.bulgeCtrl(bulgePos=cheekBulgeRGTJnt, bulgePrefix=cheekBulgePrefix,
                                            side=sideRGT, scale=scale)

        browInBulgeLFTCtrl = self.bulgeCtrl(bulgePos=browInBulgeLFTJnt, bulgePrefix=browInBulgePrefix,
                                            side=sideLFT, scale=scale)

        browInBulgeRGTCtrl = self.bulgeCtrl(bulgePos=browInBulgeRGTJnt, bulgePrefix=browInBulgePrefix,
                                            side=sideRGT, scale=scale)

        browOutBulgeLFTCtrl = self.bulgeCtrl(bulgePos=browOutBulgeLFTJnt, bulgePrefix=browOutBulgePrefix,
                                            side=sideLFT, scale=scale)

        browOutBulgeRGTCtrl = self.bulgeCtrl(bulgePos=browOutBulgeRGTJnt, bulgePrefix=browOutBulgePrefix,
                                            side=sideRGT, scale=scale)

        cornerMouthBulgeLFTCtrl = self.bulgeCtrl(bulgePos=cornerMouthBulgeLFTJnt, bulgePrefix=cornerMouthBulgePrefix,
                                            side=sideLFT, scale=scale)

        cornerMouthBulgeRGTCtrl = self.bulgeCtrl(bulgePos=cornerMouthBulgeRGTJnt, bulgePrefix=cornerMouthBulgePrefix,
                                            side=sideRGT, scale=scale)

        noseBulgeCtrl = self.bulgeCtrl(bulgePos=noseBulgeJnt, bulgePrefix=noseBulgePrefix,
                                       side=sideLFT, scale=scale)

        chinBulgeCtrl = self.bulgeCtrl(bulgePos=chinBulgeJnt, bulgePrefix=chinBulgePrefix,
                                            side=sideRGT, scale=scale)

        self.cheekBulgeLFTCtrlGrp = cheekBulgeLFTCtrl[2]
        self.cheekBulgeRGTCtrlGrp = cheekBulgeRGTCtrl[2]
        self.browInBulgeLFTCtrlGrp = browInBulgeLFTCtrl[2]
        self.browInBulgeRGTCtrlGrp = browInBulgeRGTCtrl[2]
        self.browOutBulgeLFTCtrlGrp = browOutBulgeLFTCtrl[2]
        self.browOutBulgeRGTCtrlGrp = browOutBulgeRGTCtrl[2]
        self.cornerMouthBulgeLFTCtrlGrp = cornerMouthBulgeLFTCtrl[2]
        self.cornerMouthBulgeRGTCtrlGrp = cornerMouthBulgeRGTCtrl[2]
        self.noseBulgeCtrlGrp = noseBulgeCtrl[2]
        self.chinBulgeCtrlGrp = chinBulgeCtrl[2]

        # SOFT NODE

        self.softModNode(bulgeJnt=cheekBulgeLFTJnt, bulgePrefix=cheekBulgePrefix, bulgeSlideCtrlParent=cheekBulgeLFTCtrl[2],
                         bulgeSlideCtrl=cheekBulgeLFTCtrl[1], bulgeSoftModCtrl=cheekBulgeLFTCtrl[0],
                         bulgeMesh=bulgeMesh, side=sideLFT, addSet=addSet, bulgeGrp=bulgeGrp)

        self.softModNode(bulgeJnt=cheekBulgeRGTJnt, bulgePrefix=cheekBulgePrefix, bulgeSlideCtrlParent=cheekBulgeRGTCtrl[2],
                         bulgeSlideCtrl=cheekBulgeRGTCtrl[1], bulgeSoftModCtrl=cheekBulgeRGTCtrl[0],
                         bulgeMesh=bulgeMesh, side=sideRGT, addSet=addSet, bulgeGrp=bulgeGrp)

        self.softModNode(bulgeJnt=browInBulgeLFTJnt, bulgePrefix=browInBulgePrefix, bulgeSlideCtrlParent=browInBulgeLFTCtrl[2],
                         bulgeSlideCtrl=browInBulgeLFTCtrl[1], bulgeSoftModCtrl=browInBulgeLFTCtrl[0],
                         bulgeMesh=bulgeMesh, side=sideLFT, addSet=addSet, bulgeGrp=bulgeGrp)

        self.softModNode(bulgeJnt=browInBulgeRGTJnt, bulgePrefix=browInBulgePrefix, bulgeSlideCtrlParent=browInBulgeRGTCtrl[2],
                         bulgeSlideCtrl=browInBulgeRGTCtrl[1], bulgeSoftModCtrl=browInBulgeRGTCtrl[0],
                         bulgeMesh=bulgeMesh, side=sideRGT, addSet=addSet, bulgeGrp=bulgeGrp)

        self.softModNode(bulgeJnt=browOutBulgeLFTJnt, bulgePrefix=browOutBulgePrefix, bulgeSlideCtrlParent=browOutBulgeLFTCtrl[2],
                         bulgeSlideCtrl=browOutBulgeLFTCtrl[1], bulgeSoftModCtrl=browOutBulgeLFTCtrl[0],
                         bulgeMesh=bulgeMesh, side=sideLFT, addSet=addSet, bulgeGrp=bulgeGrp)

        self.softModNode(bulgeJnt=browOutBulgeRGTJnt, bulgePrefix=browOutBulgePrefix, bulgeSlideCtrlParent=browOutBulgeRGTCtrl[2],
                         bulgeSlideCtrl=browOutBulgeRGTCtrl[1], bulgeSoftModCtrl=browOutBulgeRGTCtrl[0],
                         bulgeMesh=bulgeMesh, side=sideRGT, addSet=addSet, bulgeGrp=bulgeGrp)

        self.softModNode(bulgeJnt=cornerMouthBulgeLFTJnt, bulgePrefix=cornerMouthBulgePrefix, bulgeSlideCtrlParent=cornerMouthBulgeLFTCtrl[2],
                         bulgeSlideCtrl=cornerMouthBulgeLFTCtrl[1], bulgeSoftModCtrl=cornerMouthBulgeLFTCtrl[0],
                         bulgeMesh=bulgeMesh, side=sideLFT, addSet=addSet, bulgeGrp=bulgeGrp)

        self.softModNode(bulgeJnt=cornerMouthBulgeRGTJnt, bulgePrefix=cornerMouthBulgePrefix, bulgeSlideCtrlParent=cornerMouthBulgeRGTCtrl[2],
                         bulgeSlideCtrl=cornerMouthBulgeRGTCtrl[1], bulgeSoftModCtrl=cornerMouthBulgeRGTCtrl[0],
                         bulgeMesh=bulgeMesh, side=sideRGT, addSet=addSet, bulgeGrp=bulgeGrp)


        self.softModNode(bulgeJnt=noseBulgeJnt, bulgePrefix=noseBulgePrefix, bulgeSlideCtrlParent=noseBulgeCtrl[2],
                         bulgeSlideCtrl=noseBulgeCtrl[1], bulgeSoftModCtrl=noseBulgeCtrl[0],
                         bulgeMesh=bulgeMesh, addSet=addSet, bulgeGrp=bulgeGrp)

        self.softModNode(bulgeJnt=chinBulgeJnt, bulgePrefix=chinBulgePrefix, bulgeSlideCtrlParent=chinBulgeCtrl[2],
                         bulgeSlideCtrl=chinBulgeCtrl[1], bulgeSoftModCtrl=chinBulgeCtrl[0],
                         bulgeMesh=bulgeMesh, addSet=addSet, bulgeGrp=bulgeGrp)


        # PARENT CONSTRAINT
        cheekBulgeLFT = mc.parentConstraint(headUpCtrlGimbal, headLowCtrlGimbal, cheekBulgeLFTCtrl[2], mo=1)[0]
        cheekBulgeRGT = mc.parentConstraint(headUpCtrlGimbal, headLowCtrlGimbal, cheekBulgeRGTCtrl[2], mo=1)[0]
        mc.setAttr(cheekBulgeLFT+'.interpType', 2)
        mc.setAttr(cheekBulgeRGT+'.interpType', 2)
        sclCheekBulgeLFT = mc.scaleConstraint(headUpCtrlGimbal, headLowCtrlGimbal, cheekBulgeLFTCtrl[3], mo=1)
        sclCheekBulgeRGT = mc.scaleConstraint(headUpCtrlGimbal, headLowCtrlGimbal, cheekBulgeRGTCtrl[3], mo=1)

        # PARENT
        mc.parent(cheekBulgeLFTCtrl[2], cheekBulgeRGTCtrl[2], faceAnimCtrlGrp)
        mc.parent(browInBulgeLFTCtrl[2], browInBulgeRGTCtrl[2], browOutBulgeLFTCtrl[2], browOutBulgeRGTCtrl[2], headUpCtrlGimbal)
        mc.parent(noseBulgeCtrl[2], noseDrv03ctrl)
        mc.parent(chinBulgeCtrl[2], chinCtrl)
        mc.parent(cornerMouthBulgeLFTCtrl[2], cornerMouthLFTCtrl)
        mc.parent(cornerMouthBulgeRGTCtrl[2], cornerMouthRGTCtrl)

        # constraint rename
        au.constraint_rename([cheekBulgeLFT, cheekBulgeRGT, sclCheekBulgeLFT[0], sclCheekBulgeRGT[0]])

    def softModNode(self, bulgeJnt, bulgePrefix, bulgeSlideCtrl, bulgeSoftModCtrl, bulgeSlideCtrlParent,
                    bulgeGrp, bulgeMesh, addSet, side='',
                    ):

        self.posX = mc.xform(bulgeJnt, q=1, ws=1, t=1)[0]
        self.posY = mc.xform(bulgeJnt, q=1, ws=1, t=1)[1]
        self.posZ = mc.xform(bulgeJnt, q=1, ws=1, t=1)[2]

        reverseSlideTransMdn = mc.createNode('multiplyDivide', n=bulgePrefix + 'BulgeRevSlide' + side + '_mdn')
        reverseSoftModTransMdn = mc.createNode('multiplyDivide', n=bulgePrefix + 'BulgeRevSoftMod' + side + '_mdn')

        pma = mc.createNode('plusMinusAverage', n=bulgePrefix+'Bulge' + side + '_pma')

        softMod = mc.softMod(bulgeMesh, n=bulgePrefix+'Bulge'+ side +'_mod', fc=[self.posX,self.posY,self.posZ])

        if self.posX<0:
            mc.setAttr(bulgeSlideCtrlParent + '.scaleX', -1)

            mc.setAttr(reverseSlideTransMdn + '.input2X', -1)
            mc.setAttr(reverseSlideTransMdn + '.input2Y', 1)
            mc.setAttr(reverseSlideTransMdn + '.input2Z', 1)

            mc.setAttr(reverseSoftModTransMdn + '.input2X', -1)
            mc.setAttr(reverseSoftModTransMdn + '.input2Y', 1)
            mc.setAttr(reverseSoftModTransMdn + '.input2Z', 1)

        else:
            mc.setAttr(reverseSlideTransMdn + '.input2X', 1)
            mc.setAttr(reverseSlideTransMdn + '.input2Y', 1)
            mc.setAttr(reverseSlideTransMdn + '.input2Z', 1)

            mc.setAttr(reverseSoftModTransMdn + '.input2X', 1)
            mc.setAttr(reverseSoftModTransMdn + '.input2Y', 1)
            mc.setAttr(reverseSoftModTransMdn + '.input2Z', 1)


        mc.connectAttr(bulgeSlideCtrl + '.translate', reverseSlideTransMdn + '.input1')
        mc.connectAttr(reverseSlideTransMdn + '.output', pma + '.input3D[0]')

        mc.setAttr(pma+'.input3D[1].input3Dx', self.posX)
        mc.setAttr(pma+'.input3D[1].input3Dy', self.posY)
        mc.setAttr(pma+'.input3D[1].input3Dz', self.posZ)

        mc.connectAttr(pma+'.output3D', softMod[0]+'.falloffCenter')
        mc.connectAttr(bulgeSoftModCtrl + '.%s' % self.wide, softMod[0] + '.falloffRadius')
        mc.connectAttr(bulgeSoftModCtrl + '.%s' % self.bulge, softMod[0] + '.envelope')

        # CONNECT CTRL TO HANDLE
        mc.connectAttr(bulgeSoftModCtrl + '.translate', reverseSoftModTransMdn + '.input1')

        mc.connectAttr(reverseSoftModTransMdn+'.output', softMod[1]+'.translate')

        # HIDE
        mc.hide(softMod[1])

        # ADD SET LIST OBJECT
        if addSet:
            for i in addSet:
                setObj = mc.listConnections(softMod[0], type='objectSet')[0]
                mc.sets(i, add=setObj)

        # PARENT TO THE GRP
        mc.parent(softMod[1], bulgeGrp)

        return softMod[1]

    def bulgeCtrl(self, bulgePos,
                  bulgePrefix,
                  scale,
                  side=''):

        # SOFT MOD BULGE
        bulgeSoftModCtrl = ct.Control(prefix=bulgePrefix+'Bulge',
                                      shape=ct.LOCATOR, groups_ctrl=[''], ctrl_size=scale * 0.12,
                                      ctrl_color='turquoiseBlue', lock_channels=['v', 's', 'r'], side=side
                                      )
        # POSITION

        # ADD ATTRIBUTE
        au.add_attribute(objects=[bulgeSoftModCtrl.control], long_name=['setup'], nice_name=[' '], at="enum",
                         en='Setup', channel_box=True)

        self.wide = au.add_attribute(objects=[bulgeSoftModCtrl.control], long_name=['wide'],
                                     attributeType="float", min=0, dv=0.25, keyable=True)

        self.bulge = au.add_attribute(objects=[bulgeSoftModCtrl.control], long_name=['bulge'],
                                      attributeType="float", min=0, max=1, dv=1, keyable=True)


        # SLIDE BULGE
        bulgeSlideCtrl = ct.Control(prefix=bulgePrefix+'BulgeSlide',
                                    shape=ct.JOINT, groups_ctrl=['', 'Offset'], ctrl_size=scale * 0.1,
                                    ctrl_color='yellow', lock_channels=['v', 's', 'r'], side=side
                                    )

        # PARENT
        # mc.parent(bulgeSlideCtrl.parentControl[0], bulgeSoftModCtrl.control)
        mc.parent(bulgeSoftModCtrl.parent_control[0], bulgeSlideCtrl.control)

        mc.delete(mc.pointConstraint(bulgePos, bulgeSlideCtrl.parent_control[0]))

        return bulgeSoftModCtrl.control, bulgeSlideCtrl.control, bulgeSlideCtrl.parent_control[0], bulgeSlideCtrl.parent_control[1]
