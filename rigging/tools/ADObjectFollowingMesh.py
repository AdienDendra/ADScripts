from __future__ import absolute_import

import maya.cmds as cmds

from rigging.tools import utils as rt_utils


def obj_follow(obj,
               obj_target,
               base_mesh):
    node = cmds.createNode('closestPointOnMesh', n='%s_cpm' % rt_utils.prefix_name(obj))
    cmds.connectAttr(base_mesh + '.worldMatrix[0]', node + '.inputMatrix')
    cmds.connectAttr(base_mesh + '.outMesh', node + '.inMesh')
    decompostMtx = cmds.createNode('decomposeMatrix', n='%s_dmt' % rt_utils.prefix_name(obj))
    cmds.connectAttr(obj + '.worldMatrix[0]', decompostMtx + '.inputMatrix')
    cmds.connectAttr(decompostMtx + '.outputTranslate', node + '.inPosition')
    cmds.connectAttr(node + '.result.position', obj_target + '.translate')
