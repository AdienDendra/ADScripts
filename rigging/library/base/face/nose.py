from __future__ import absolute_import

from rigging.library.utils import controller as rlu_controller, transform as rlu_transform


class Build:
    def __init__(self,
                 columella_jnt,
                 columella_prefix,
                 suffix_controller,
                 scale):
        # ==================================================================================================================
        #                                                   COLUMELLA
        # ==================================================================================================================
        # grouping joint
        self.columella_jnt_grp = rlu_transform.create_parent_transform(parent_list=['Zro', 'Offset'],
                                                                       object=columella_jnt,
                                                                       match_position=columella_jnt,
                                                                       prefix=columella_prefix, suffix='_jnt')

        # create columella controller
        columella_ctrl = rlu_controller.Control(match_obj_first_position=columella_jnt,
                                                prefix=columella_prefix,
                                                shape=rlu_controller.JOINT, groups_ctrl=[''],
                                                ctrl_size=scale * 0.05,
                                                ctrl_color='yellow', lock_channels=['v', 's'],
                                                suffix=suffix_controller,
                                                connection=['connectMatrixTransRot'])

        self.columella_ctrl = columella_ctrl.control
        self.columella_ctrl_grp_zro = columella_ctrl.parent_control[0]
