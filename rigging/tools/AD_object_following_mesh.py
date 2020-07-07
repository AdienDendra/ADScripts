from __builtin__ import reload

import maya.cmds as mc

from rigging.tools import AD_utils as au, AD_controller as ac

reload(ac)
reload(au)


def obj_follow(obj,
               obj_target,
               base_mesh):
    node = mc.createNode('closestPointOnMesh', n='%s_cpm' % au.prefix_name(obj))
    mc.connectAttr(base_mesh + '.worldMatrix[0]', node + '.inputMatrix')
    mc.connectAttr(base_mesh + '.outMesh', node + '.inMesh')
    decompostMtx = mc.createNode('decomposeMatrix', n='%s_dmt' % au.prefix_name(obj))
    mc.connectAttr(obj + '.worldMatrix[0]', decompostMtx + '.inputMatrix')
    mc.connectAttr(decompostMtx + '.outputTranslate', node + '.inPosition')
    mc.connectAttr(node + '.result.position', obj_target + '.translate')
