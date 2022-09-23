from __future__ import absolute_import

from importlib import reload

import pymel.core as pm

from rigging.tools import utils as au

reload(au)


def rearrange_rig():
    if pm.objExists('headx_ctrl') and pm.objExists('neckx_ctrl'):
        pass
    else:
        pm.rename('head_ctrl', 'headx_ctrl')
        pm.rename('neck_ctrl', 'neckx_ctrl')

    pm.parent('lidUpJntDriverLFT_grp ', 'lidLowJntDriverLFT_grp', 'eyeLFT_skn')
    pm.parent('lidUpJntDriverRGT_grp ', 'lidLowJntDriverRGT_grp', 'eyeRGT_skn')

    pm.setAttr("lidUpMoveZroLFT_grp.inheritsTransform", 1)
    pm.setAttr("lidLowMoveZroLFT_grp.inheritsTransform", 1)

    pm.setAttr("lidUpMoveZroRGT_grp.inheritsTransform", 1)
    pm.setAttr("lidLowMoveZroRGT_grp.inheritsTransform", 1)

    pm.setAttr('lidUpMoveZroLFT_grp' + '.translateX', 0)
    pm.setAttr('lidUpMoveZroLFT_grp' + '.translateY', 0)
    pm.setAttr('lidUpMoveZroLFT_grp' + '.translateZ', 0)

    pm.setAttr('lidLowMoveZroLFT_grp' + '.translateX', 0)
    pm.setAttr('lidLowMoveZroLFT_grp' + '.translateY', 0)
    pm.setAttr('lidLowMoveZroLFT_grp' + '.translateZ', 0)

    pm.setAttr('lidUpMoveZroRGT_grp' + '.translateX', 0)
    pm.setAttr('lidUpMoveZroRGT_grp' + '.translateY', 0)
    pm.setAttr('lidUpMoveZroRGT_grp' + '.translateZ', 0)

    pm.setAttr('lidLowMoveZroRGT_grp' + '.translateX', 0)
    pm.setAttr('lidLowMoveZroRGT_grp' + '.translateY', 0)
    pm.setAttr('lidLowMoveZroRGT_grp' + '.translateZ', 0)

    pm.parent('faceAnim_grp', 'anim_grp')
    faceSetup_grp = pm.createNode('transform', n='faceSetup_grp')
    pm.parent('faceModule_grp', 'additional_grp', faceSetup_grp)
    pm.parent(faceSetup_grp, 'still_grp')

    list_head_bind = pm.listRelatives('head_bind', c=True)
    list_gimbal_ctrl = pm.listRelatives('headGmbl_ctrl', c=True)

    for item in list_head_bind:
        pm.parent(item, 'head1_jnt')

    for item in list_gimbal_ctrl:
        pm.parent(item, 'head_gmbl_ctrl')

    pm.delete('headTip_bind')

    pm.setAttr('faceJoint_grp' + '.translateX', k=True, l=False)
    pm.setAttr('faceJoint_grp' + '.translateY', k=True, l=False)
    pm.setAttr('faceJoint_grp' + '.translateZ', k=True, l=False)
    pm.setAttr('faceJoint_grp' + '.rotateX', k=True, l=False)
    pm.setAttr('faceJoint_grp' + '.rotateY', k=True, l=False)
    pm.setAttr('faceJoint_grp' + '.rotateZ', k=True, l=False)
    pm.setAttr('faceJoint_grp' + '.scaleX', k=True, l=False)
    pm.setAttr('faceJoint_grp' + '.scaleY', k=True, l=False)
    pm.setAttr('faceJoint_grp' + '.scaleZ', k=True, l=False)

    au.parent_scale_constraint('head_gmbl_ctrl', 'faceJoint_grp', mo=1)

    head_skn = pm.listRelatives('head_skn', c=True)

    for item in head_skn:
        pm.parent(item, 'faceJoint_grp')

    pm.setAttr('faceUtils_grp' + '.translateX', k=True, l=False)
    pm.setAttr('faceUtils_grp' + '.translateY', k=True, l=False)
    pm.setAttr('faceUtils_grp' + '.translateZ', k=True, l=False)
    pm.setAttr('faceUtils_grp' + '.rotateX', k=True, l=False)
    pm.setAttr('faceUtils_grp' + '.rotateY', k=True, l=False)
    pm.setAttr('faceUtils_grp' + '.rotateZ', k=True, l=False)
    pm.setAttr('faceUtils_grp' + '.scaleX', k=True, l=False)
    pm.setAttr('faceUtils_grp' + '.scaleY', k=True, l=False)
    pm.setAttr('faceUtils_grp' + '.scaleZ', k=True, l=False)

    au.parent_scale_constraint('anim_grp', 'faceUtils_grp', mo=1)

    pm.delete('headTip_skn', 'neckJnt_grp', 'neckCtrlAll_grp', 'anim_ctrl', 'neck_bind')
    pm.rename('headx_ctrl', 'head_ctrl')
    pm.rename('neckx_ctrl', 'neck_ctrl')
