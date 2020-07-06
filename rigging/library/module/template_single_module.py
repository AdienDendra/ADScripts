from __builtin__ import reload

import maya.cmds as mc

from rigging.library.module import template_module as sd

reload(sd)

def all_skeleton(side_LFT='LFT', side_RGT='RGT', suffix_joint='jnt', sj_prefix_value='', ss_prefix_value='Scl', sFk_prefix_value='Fk', sIk_prefix_value='Ik',
                 sAdd_prefix_value='Shape'):

    sj = sd.listSkeletonDuplicate(value_prefix=sj_prefix_value,
                                  key_prefix='Ori',
                                  suffix='skn',
                                  side_LFT=side_LFT,
                                  side_RGT=side_RGT
                                  )

    ss = sd.listSkeletonDuplicate(value_prefix=ss_prefix_value,
                                  key_prefix='Scl',
                                  suffix=suffix_joint,
                                  side_LFT=side_LFT,
                                  side_RGT=side_RGT
                                  )

    sFk = sd.listSkeletonDuplicate(value_prefix=sFk_prefix_value,
                                   key_prefix='Fk',
                                   suffix=suffix_joint,
                                   side_LFT=side_LFT,
                                   side_RGT=side_RGT
                                   )

    sIk = sd.listSkeletonDuplicate(value_prefix=sIk_prefix_value,
                                   key_prefix='Ik',
                                   suffix=suffix_joint,
                                   side_LFT=side_LFT,
                                   side_RGT=side_RGT
                                   )
    sTwistHelp = sd.listSkeletonDuplicate(value_prefix='TwistHelpDriver',
                                          key_prefix='DtlKey',
                                          suffix=suffix_joint,
                                          side_LFT=side_LFT,
                                          side_RGT=side_RGT
                                          )

    sAdd = sd.listSkeletonDuplicate(value_prefix=sAdd_prefix_value,
                                    key_prefix='Add',
                                    suffix=suffix_joint,
                                    side_LFT=side_LFT,
                                    side_RGT=side_RGT
                                    )

    mc.hide('tmpJnt_grp')

    #unhide skin joint
    unhide = mc.ls('*skn')
    for i in unhide:
        mc.setAttr(i + '.visibility', 1)

    hide = mc.ls('*jnt')
    for i in hide:
        mc.setAttr(i + '.visibility', 0)

    return {'sj':sj,
            'ss':ss,
            'sFk':sFk,
            'sIk':sIk,
            'sTwistHelp':sTwistHelp,
            'sAdd':sAdd}