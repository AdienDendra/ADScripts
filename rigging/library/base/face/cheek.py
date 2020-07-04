from __builtin__ import reload

import maya.cmds as mc

from rigging.library.utils import controller as ct
from rigging.library.utils import transform as tf

reload (ct)
reload (tf)

class Build:
    def __init__(self,
                 cheekLowJnt,
                 cheekLowPrefix,
                 cheekMidJnt,
                 cheekMidPrefix,
                 cheekUpJnt,
                 cheekUpPrefix,
                 cheekInUpJnt,
                 cheekInUpPrefix,
                 cheekInLowJnt,
                 cheekInLowPrefix,
                 cheekOutUpJnt,
                 cheekOutUpPrefix,
                 cheekOutLowJnt,
                 cheekOutLowPrefix,
                 scale,
                 side,
                 suffixController):

    # ==================================================================================================================
    #                                            CHEEK CONTROLLER
    # ==================================================================================================================

        # check position
        pos = mc.xform(cheekLowJnt, ws=1, q=1, t=1)[0]

        # cheek ctrl grp
        # self.cheekDriverCtrlGrp = mc.createNode('transform', n='cheekDriverCtrl_grp')
    # ==================================================================================================================
    #                                            CHEEK MIDDLE AREA
    # ==================================================================================================================

        # create cheek low controller
        cheekLowCtrl = ct.Control(match_obj_first_position=cheekLowJnt,
                                  prefix=cheekLowPrefix,
                                  shape=ct.JOINT, groups_ctrl=['', 'Offset'],
                                  ctrl_size=scale * 0.05, suffix=suffixController,
                                  ctrl_color='red', lock_channels=['v'], side=side)

        self.cheekLowCtrl= cheekLowCtrl.control
        self.cheekLowParentCtrlZro = cheekLowCtrl.parent_control[0]
        self.cheekLowParentCtrlOffset = cheekLowCtrl.parent_control[1]

        # create cheek mid controller
        cheekMidCtrl = ct.Control(match_obj_first_position=cheekMidJnt,
                                  prefix=cheekMidPrefix,
                                  shape=ct.JOINT, groups_ctrl=['', 'Offset'],
                                  ctrl_size=scale * 0.05, suffix=suffixController,
                                  ctrl_color='red', lock_channels=['v'], side=side)

        self.cheekMidCtrl= cheekMidCtrl.control
        self.cheekMidParentCtrlZro = cheekMidCtrl.parent_control[0]
        self.cheekMidParentCtrlOffset = cheekMidCtrl.parent_control[1]

        # create cheek up controller
        cheekUpCtrl = ct.Control(match_obj_first_position=cheekUpJnt,
                                 prefix=cheekUpPrefix,
                                 shape=ct.JOINT, groups_ctrl=['', 'Offset'],
                                 ctrl_size=scale * 0.05, suffix=suffixController,
                                 ctrl_color='red', lock_channels=['v'], side=side)

        self.cheekUpCtrl= cheekUpCtrl.control
        self.cheekUpParentCtrlZro = cheekUpCtrl.parent_control[0]
        self.cheekUpParentCtrlOffset = cheekUpCtrl.parent_control[1]

    # ==================================================================================================================
    #                                            CHEEK IN AREA
    # ==================================================================================================================

        # create cheek in up controller
        cheekInUpCtrl = ct.Control(match_obj_first_position=cheekInUpJnt,
                                   prefix=cheekInUpPrefix,
                                   shape=ct.JOINT, groups_ctrl=['', 'Offset'],
                                   ctrl_size=scale * 0.05, suffix=suffixController,
                                   ctrl_color='turquoiseBlue', lock_channels=['v'], side=side)

        self.cheekInUpCtrl= cheekInUpCtrl.control
        self.cheekInUpParentCtrlZro = cheekInUpCtrl.parent_control[0]
        self.cheekInUpParentCtrlOffset = cheekInUpCtrl.parent_control[1]

        # create cheek in low controller
        cheekInLowCtrl = ct.Control(match_obj_first_position=cheekInLowJnt,
                                    prefix=cheekInLowPrefix,
                                    shape=ct.JOINT, groups_ctrl=['', 'Offset'],
                                    ctrl_size=scale * 0.05, suffix=suffixController,
                                    ctrl_color='turquoiseBlue', lock_channels=['v'], side=side)

        self.cheekInLowCtrl = cheekInLowCtrl.control
        self.cheekInLowParentCtrlZro = cheekInLowCtrl.parent_control[0]
        self.cheekInLowParentCtrlOffset = cheekInLowCtrl.parent_control[1]

        mc.setAttr(self.cheekInLowParentCtrlOffset + '.scaleY', -1)

        if pos<0:
            mc.setAttr(self.cheekInLowParentCtrlOffset + '.scaleX', -1)

    # ==================================================================================================================
    #                                            CHEEK OUT AREA
    # ==================================================================================================================

        # create cheek out up controller
        cheekOutUpCtrl = ct.Control(match_obj_first_position=cheekOutUpJnt,
                                    prefix=cheekOutUpPrefix,
                                    shape=ct.JOINT, groups_ctrl=['', 'Offset'],
                                    ctrl_size=scale * 0.05, suffix=suffixController,
                                    ctrl_color='red', lock_channels=['v'], side=side)

        self.cheekOutUpCtrl= cheekOutUpCtrl.control
        self.cheekOutUpParentCtrlZro = cheekOutUpCtrl.parent_control[0]
        self.cheekOutUpParentCtrlOffset = cheekOutUpCtrl.parent_control[1]

        # create cheek out low controller
        cheekOutLowCtrl = ct.Control(match_obj_first_position=cheekOutLowJnt,
                                     prefix=cheekOutLowPrefix,
                                     shape=ct.JOINT, groups_ctrl=['', 'Offset'],
                                     ctrl_size=scale * 0.05, suffix=suffixController,
                                     ctrl_color='red', lock_channels=['v'], side=side)

        self.cheekOutLowCtrl= cheekOutLowCtrl.control
        self.cheekOutLowParentCtrlZro = cheekOutLowCtrl.parent_control[0]
        self.cheekOutLowParentCtrlOffset = cheekOutLowCtrl.parent_control[1]

    # ==================================================================================================================
    #                                           CHEEK JOINT GROUP TRANSFORM
    # ==================================================================================================================

        # parenting the joint
        # self.cheekDriverJntGrp = mc.createNode('transform', n='cheekDriverJnt_grp')

        self.cheekLowJnt = tf.create_parent_transform(['', 'Offset'], match_position=cheekLowJnt, object=cheekLowJnt,
                                                      prefix=cheekLowJnt, suffix=cheekLowJnt, side=side
                                                      )

        self.cheekMidJnt = tf.create_parent_transform(['', 'Offset'], match_position=cheekMidJnt, object=cheekMidJnt,
                                                      prefix=cheekMidJnt, suffix=cheekMidJnt, side=side
                                                      )

        self.cheekUpJnt = tf.create_parent_transform(['', 'Offset'], match_position=cheekUpJnt, object=cheekUpJnt,
                                                     prefix=cheekUpJnt, suffix=cheekUpJnt, side=side
                                                     )

        self.cheekInUpJnt = tf.create_parent_transform(['', 'Offset'], match_position=cheekInUpJnt, object=cheekInUpJnt,
                                                       prefix=cheekInUpJnt, suffix=cheekInUpJnt, side=side
                                                       )

        self.cheekInLowJnt = tf.create_parent_transform(['', 'Offset'], match_position=cheekInLowJnt, object=cheekInLowJnt,
                                                        prefix=cheekInLowJnt, suffix=cheekInLowJnt, side=side
                                                        )

        self.cheekOutUpJnt = tf.create_parent_transform(['', 'Offset'], match_position=cheekOutUpJnt, object=cheekOutUpJnt,
                                                        prefix=cheekOutUpJnt, suffix=cheekOutUpJnt, side=side)

        self.cheekOutLowJnt = tf.create_parent_transform(['', 'Offset'], match_position=cheekOutLowJnt, object=cheekOutLowJnt,
                                                         prefix=cheekOutLowJnt, suffix=cheekOutLowJnt, side=side)

        # flipping the controller
        if pos <0:
            mc.setAttr(self.cheekLowParentCtrlOffset + '.scaleX', -1)
            mc.setAttr(self.cheekMidParentCtrlOffset + '.scaleX', -1)
            mc.setAttr(self.cheekUpParentCtrlOffset + '.scaleX', -1)
            mc.setAttr(self.cheekInUpParentCtrlOffset + '.scaleX', -1)
            mc.setAttr(self.cheekOutUpParentCtrlOffset + '.scaleX', -1)
            mc.setAttr(self.cheekOutLowParentCtrlOffset + '.scaleX', -1)


