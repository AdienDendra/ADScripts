from __builtin__ import reload

from rigging.library.utils import controller as ct
from rigging.library.utils import transform as tf

reload (ct)
reload (tf)

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
        self.columella_jnt_grp = tf.create_parent_transform(parent_list=['Zro', 'Offset'], object=columella_jnt, match_position=columella_jnt,
                                                            prefix=columella_prefix, suffix='_jnt')

        # create columella controller
        columella_ctrl = ct.Control(match_obj_first_position=columella_jnt,
                                    prefix=columella_prefix,
                                    shape=ct.JOINT, groups_ctrl=[''],
                                    ctrl_size=scale * 0.05,
                                    ctrl_color='yellow', lock_channels=['v', 's'],
                                    suffix=suffix_controller,
                                    connection=['connectMatrixTransRot'])

        self.columella_ctrl= columella_ctrl.control
        self.columella_ctrl_grp_zro = columella_ctrl.parent_control[0]