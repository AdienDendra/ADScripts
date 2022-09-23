from __future__ import absolute_import

import maya.cmds as cmds

from rigging.library.module import tmpModule as rlm_tmpModule


def all_skeleton(side_LFT='LFT', side_RGT='RGT', suffix_joint='jnt', sj_prefix_value='', ss_prefix_value='Scl',
                 sFk_prefix_value='Fk', sIk_prefix_value='Ik',
                 sAdd_prefix_value='Shape'):
    sj = rlm_tmpModule.listSkeletonDuplicate(value_prefix=sj_prefix_value,
                                             key_prefix='Ori',
                                             suffix='skn',
                                             side_LFT=side_LFT,
                                             side_RGT=side_RGT
                                             )

    ss = rlm_tmpModule.listSkeletonDuplicate(value_prefix=ss_prefix_value,
                                             key_prefix='Scl',
                                             suffix=suffix_joint,
                                             side_LFT=side_LFT,
                                             side_RGT=side_RGT
                                             )

    sFk = rlm_tmpModule.listSkeletonDuplicate(value_prefix=sFk_prefix_value,
                                              key_prefix='Fk',
                                              suffix=suffix_joint,
                                              side_LFT=side_LFT,
                                              side_RGT=side_RGT
                                              )

    sIk = rlm_tmpModule.listSkeletonDuplicate(value_prefix=sIk_prefix_value,
                                              key_prefix='Ik',
                                              suffix=suffix_joint,
                                              side_LFT=side_LFT,
                                              side_RGT=side_RGT
                                              )
    sTwistHelp = rlm_tmpModule.listSkeletonDuplicate(value_prefix='TwistHelpDriver',
                                                     key_prefix='DtlKey',
                                                     suffix=suffix_joint,
                                                     side_LFT=side_LFT,
                                                     side_RGT=side_RGT
                                                     )

    sAdd = rlm_tmpModule.listSkeletonDuplicate(value_prefix=sAdd_prefix_value,
                                               key_prefix='Add',
                                               suffix=suffix_joint,
                                               side_LFT=side_LFT,
                                               side_RGT=side_RGT
                                               )

    cmds.hide('tmpJnt_grp')

    # unhide skin joint
    unhide = cmds.ls('*skn')
    for i in unhide:
        cmds.setAttr(i + '.visibility', 1)

    hide = cmds.ls('*jnt')
    for i in hide:
        cmds.setAttr(i + '.visibility', 0)

    return {'sj': sj,
            'ss': ss,
            'sFk': sFk,
            'sIk': sIk,
            'sTwistHelp': sTwistHelp,
            'sAdd': sAdd}
