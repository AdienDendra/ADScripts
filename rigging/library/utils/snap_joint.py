from __builtin__ import reload

import maya.cmds as mc

from rigging.library.utils import transform as tf
from rigging.tools import AD_utils as au

reload(au)
reload(tf)

def joint(limb_jnt, side_LFT, side_RGT, side):
    # create locator
    mc.select(cl=1)
    upper_limb_snap_jnt = mc.joint(n=au.prefix_name(
        tf.reposition_side(object=limb_jnt, side_LFT=side_LFT, side_RGT=side_RGT)) + 'Ref' + side + '_jnt')

    # match position
    mc.delete(mc.parentConstraint(limb_jnt, upper_limb_snap_jnt))

    # parent locator to main joint
    mc.parent(upper_limb_snap_jnt, limb_jnt)

    # freezing rotation
    mc.makeIdentity(upper_limb_snap_jnt, a=1, r=1, n=2, pn=1)

    # hide
    mc.hide(upper_limb_snap_jnt)

    return upper_limb_snap_jnt

