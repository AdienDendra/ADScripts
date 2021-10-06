# this was autocreated, please add functions in there
import thomasTools.nodes as nodes
import thomasTools.utilFunctions as utils

import thomasTabTools.builder as builderTools
import thomasTabTools.ctrls as ctrls
import thomasTabTools.interpolator as interpolator
import thomasTabTools.weights as weights
import thomasTools.sliderCtrls as sliderCtrls
import thomasTools.xforms as xforms

import maya.cmds as cmds
import os

kBuilderColor = utils.uiColors.default


@builderTools.addToBuild(iOrder=104)
def setDefaultValues(_report=None):
    # ctrls.ctrlFromName('lidTopLFT_ctrl').convertToSimpleTransforms()
    # ctrls.ctrlFromName('lidBotLFT_ctrl').convertToSimpleTransforms()
    # ctrls.ctrlFromName('lidTopRGT_ctrl').convertToSimpleTransforms()
    # ctrls.ctrlFromName('lidBotRGT_ctrl').convertToSimpleTransforms()
    cmds.delete('grp_r_lidBotPasser', 'grp_l_lidBotPasser')
    cmds.delete('grp_r_lidTopPasser', 'grp_l_lidTopPasser')
    ctrls.ctrlFromName('mouth_ctrl').convertToSimpleTransforms()

    # create space in between Front
    locator_m_l = cmds.spaceLocator(n='m_skirtGuidePasser_l_loc')[0]
    locator_m_r = cmds.spaceLocator(n='m_skirtGuidePasser_r_loc')[0]
    cmds.parent(locator_m_l, locator_m_r, 'ctrl_m_RootOut')

    cmds.pointConstraint('jnt_l_legWrist', locator_m_l, mo=0)
    cmds.pointConstraint('jnt_r_legWrist', locator_m_r, mo=0)

    skirtGuideFront_ctrl = 'skirtFrontA_ctrl'
    constraint_skirt_guide_m = \
    cmds.parentConstraint(locator_m_l, locator_m_r, 'jnt_m_hips', 'grp_m_skirtGuideOffsetSlider', mo=1)[0]
    constraint_skirt_offset_m = cmds.pointConstraint('ctrl_m_skirtGuideOut', 'grp_m_skirtFrontAOffset', mo=1)[0]


    reverse_node = cmds.createNode('reverse', n='skirtGuideFront_rev')
    cmds.addAttr(skirtGuideFront_ctrl, ln='spaceSkirt', at='long', min=0, max=1, dv=1)
    cmds.setAttr(skirtGuideFront_ctrl + '.spaceSkirt', e=True, keyable=True)

    cmds.addAttr(skirtGuideFront_ctrl, ln='legSpaceFollow', at='double', min=0, max=1, dv=0.5)
    cmds.setAttr(skirtGuideFront_ctrl + '.legSpaceFollow', e=True, keyable=True)

    cmds.connectAttr(skirtGuideFront_ctrl + '.spaceSkirt', constraint_skirt_offset_m + '.ctrl_m_skirtGuideOutW0')

    cmds.connectAttr(skirtGuideFront_ctrl + '.legSpaceFollow', constraint_skirt_guide_m + '.%sW0' % locator_m_l)

    cmds.connectAttr(skirtGuideFront_ctrl + '.legSpaceFollow', reverse_node + '.inputX')
    cmds.connectAttr(reverse_node + '.outputX', constraint_skirt_guide_m + '.%sW1' % locator_m_r)
    # cmds.setAttr('grp_m_skirtGuideOffsetSlider_parentConstraint1.jnt_m_hipsW2', 0.5)


    # create space in between LFT
    skirtGuideLFT_ctrl = 'skirtALFT_ctrl'
    locator_l = cmds.spaceLocator(n='l_skirtGuidePasser_loc')[0]
    cmds.parent(locator_l, 'ctrl_m_RootOut')
    cmds.pointConstraint('jnt_l_legWrist', locator_l, mo=0)

    constraint_skirt_guide_l = cmds.parentConstraint(locator_l, 'jnt_m_hips', 'grp_l_skirtGuideOffsetSlider', mo=1)[0]
    constraint_skirt_offset_l = cmds.pointConstraint('ctrl_l_skirtGuideOut', 'grp_l_skirtAOffset', mo=1)[0]


    reverse_node = cmds.createNode('reverse', n='skirtGuideLFT_rev')
    cmds.addAttr(skirtGuideLFT_ctrl, ln='spaceSkirt', at='long', min=0, max=1, dv=1)
    cmds.setAttr(skirtGuideLFT_ctrl + '.spaceSkirt', e=True, keyable=True)

    cmds.addAttr(skirtGuideLFT_ctrl, ln='skirtFollow', at='double', min=0, max=1, dv=0.5)
    cmds.setAttr(skirtGuideLFT_ctrl + '.skirtFollow', e=True, keyable=True)

    cmds.connectAttr(skirtGuideLFT_ctrl + '.spaceSkirt', constraint_skirt_offset_l + '.ctrl_l_skirtGuideOutW0')

    cmds.connectAttr(skirtGuideLFT_ctrl + '.skirtFollow', constraint_skirt_guide_l + '.%sW0' % locator_l)

    cmds.connectAttr(skirtGuideLFT_ctrl + '.skirtFollow', reverse_node + '.inputX')
    cmds.connectAttr(reverse_node + '.outputX', constraint_skirt_guide_l + '.jnt_m_hipsW1')

    # create space in between RGT
    skirtGuideRGT_ctrl = 'skirtARGT_ctrl'
    locator_r = cmds.spaceLocator(n='r_skirtGuidePasser_loc')[0]
    cmds.parent(locator_r, 'ctrl_m_RootOut')
    cmds.pointConstraint('jnt_r_legWrist', locator_r, mo=0)

    constraint_skirt_guide_r = cmds.parentConstraint(locator_r, 'jnt_m_hips', 'grp_r_skirtGuideOffsetSlider', mo=1)[0]
    constraint_skirt_offset_r = cmds.pointConstraint('ctrl_r_skirtGuideOut', 'grp_r_skirtAOffset', mo=1)[0]


    reverse_node = cmds.createNode('reverse', n='skirtGuideRGT_rev')
    cmds.addAttr(skirtGuideRGT_ctrl, ln='spaceSkirt', at='long', min=0, max=1, dv=1)
    cmds.setAttr(skirtGuideRGT_ctrl + '.spaceSkirt', e=True, keyable=True)

    cmds.addAttr(skirtGuideRGT_ctrl, ln='skirtFollow', at='double', min=0, max=1, dv=0.5)
    cmds.setAttr(skirtGuideRGT_ctrl + '.skirtFollow', e=True, keyable=True)

    cmds.connectAttr(skirtGuideRGT_ctrl + '.spaceSkirt', constraint_skirt_offset_r + '.ctrl_r_skirtGuideOutW0')

    cmds.connectAttr(skirtGuideRGT_ctrl + '.skirtFollow', constraint_skirt_guide_r + '.%sW0' % locator_r)

    cmds.connectAttr(skirtGuideRGT_ctrl + '.skirtFollow', reverse_node + '.inputX')
    cmds.connectAttr(reverse_node + '.outputX', constraint_skirt_guide_r + '.jnt_m_hipsW1')

    cmds.setAttr('skirtGuide_ctrl.visibility', lock=0, k=1)
    cmds.setAttr('skirtGuide_ctrl.visibility', 0)

    cmds.setAttr('skirtGuideLFT_ctrl.visibility', lock=0, k=1)
    cmds.setAttr('skirtGuideLFT_ctrl.visibility', 0)

    cmds.setAttr('skirtGuideRGT_ctrl.visibility', lock=0, k=1)
    cmds.setAttr('skirtGuideRGT_ctrl.visibility', 0)

###############
    cmds.addAttr('backPack_ctrl', ln='capeVisibility', at='long', min=0, max=1, dv=1)
    cmds.setAttr('backPack_ctrl' + '.capeVisibility', e=True, keyable=True)

    cmds.connectAttr('backPack_ctrl' + '.capeVisibility', 'grp_l_capeBasePasser' + '.visibility')
    cmds.connectAttr('backPack_ctrl' + '.capeVisibility', 'grp_l_capeSplineFk_APasser' + '.visibility')
    cmds.connectAttr('backPack_ctrl' + '.capeVisibility', 'grp_l_capeSplineFk_BPasser' + '.visibility')
    cmds.connectAttr('backPack_ctrl' + '.capeVisibility', 'grp_l_capeSplineFk_CPasser' + '.visibility')
    cmds.connectAttr('backPack_ctrl' + '.capeVisibility', 'grp_l_capeSplineFk_DPasser' + '.visibility')

    cmds.connectAttr('backPack_ctrl' + '.capeVisibility', 'grp_r_capeBasePasser' + '.visibility')
    cmds.connectAttr('backPack_ctrl' + '.capeVisibility', 'grp_r_capeSplineFk_APasser' + '.visibility')
    cmds.connectAttr('backPack_ctrl' + '.capeVisibility', 'grp_r_capeSplineFk_BPasser' + '.visibility')
    cmds.connectAttr('backPack_ctrl' + '.capeVisibility', 'grp_r_capeSplineFk_CPasser' + '.visibility')
    cmds.connectAttr('backPack_ctrl' + '.capeVisibility', 'grp_r_capeSplineFk_DPasser' + '.visibility')

    cmds.connectAttr('backPack_ctrl' + '.capeVisibility', 'clothBack_ply' + '.visibility')
    pass













