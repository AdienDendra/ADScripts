from __future__ import absolute_import

import maya.cmds as cmds

from rigging.library.utils import transform as rlu_transform
from rigging.tools import utils as rt_utils


def joint(limb_jnt, side_LFT, side_RGT, side):
    # create locator
    cmds.select(cl=1)
    upper_limb_snap_jnt = cmds.joint(n=rt_utils.prefix_name(
        rlu_transform.reposition_side(object=limb_jnt, side_LFT=side_LFT, side_RGT=side_RGT)) + 'Ref' + side + '_jnt')

    # match position
    cmds.delete(cmds.parentConstraint(limb_jnt, upper_limb_snap_jnt))

    # parent locator to main joint
    cmds.parent(upper_limb_snap_jnt, limb_jnt)

    # freezing rotation
    cmds.makeIdentity(upper_limb_snap_jnt, a=1, r=1, n=2, pn=1)

    # hide
    cmds.hide(upper_limb_snap_jnt)

    return upper_limb_snap_jnt
