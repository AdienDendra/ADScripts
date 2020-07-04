from __builtin__ import reload

from rigging.library.utils import controller as ct
from rigging.library.utils import transform as tf

reload (ct)
reload (tf)

class Build:
    def __init__(self,
                 columellaJnt,
                 columellaPrefix,
                 suffixController,
                 scale):
    # ==================================================================================================================
    #                                                   COLUMELLA
    # ==================================================================================================================
        # grouping joint
        self.grpColumellaJnt = tf.create_parent_transform(parent_list=['Zro', 'Offset'], object=columellaJnt, match_position=columellaJnt,
                                                          prefix=columellaPrefix, suffix='_jnt')

        # create columella controller
        columellaCtrl = ct.Control(match_obj_first_position=columellaJnt,
                                   prefix=columellaPrefix,
                                   shape=ct.JOINT, groups_ctrl=[''],
                                   ctrl_size=scale * 0.05,
                                   ctrl_color='yellow', lock_channels=['v', 's'],
                                   suffix=suffixController,
                                   connection=['connectMatrixTransRot'])

        self.columellaCtrl= columellaCtrl.control
        self.columellaParentCtrlZro = columellaCtrl.parent_control[0]