from __builtin__ import reload

import maya.cmds as mc

from rigging.library.utils import controller as ct
from rigging.tools import AD_utils as au

reload (ct)
reload (au)

class Build:
    def __init__(self,
                 matchPosOne,
                 matchPosTwo,
                 prefix,
                 scale,
                 sticky,
                 side,
                 suffixController):

        # create controller
        cornerCtrl = ct.Control(match_obj_first_position=matchPosOne, match_obj_second_position=matchPosTwo,
                                prefix=prefix, suffix=suffixController,
                                shape=ct.CIRCLEPLUS, groups_ctrl=['Zro', 'Offset'],
                                ctrl_size=scale * 0.15,
                                ctrl_color='blue', lock_channels=['v', 'r', 's'], side=side)

        # check position
        pos = mc.xform(cornerCtrl.control, ws=1, q=1, t=1)[0]


        # ADD ATTRIBUTE
        au.add_attribute(objects=[cornerCtrl.control], long_name=['offsetPart'], nice_name=[' '], at="enum",
                         en='Offset Part', channel_box=True)
        if sticky:
            self.stickyCtrl = au.add_attribute(objects=[cornerCtrl.control], long_name=['stickyLip'],
                                               attributeType="float", min=0, max=10, dv=0, keyable=True)

        self.jawFollowCtrl = au.add_attribute(objects=[cornerCtrl.control], long_name=['jawFollowing'],
                                              attributeType="float", min=0, max=10, dv=5, keyable=True)

        self.jawUDCtrl = au.add_attribute(objects=[cornerCtrl.control], long_name=['cornerAdjust'],
                                          attributeType="float", min=0, max=10, dv=0, keyable=True)

        # ADD ATTRIBUTE CHEEK
        au.add_attribute(objects=[cornerCtrl.control], long_name=['weightSkinInfluence'], nice_name=[' '], at="enum",
                         en='%s%s%s' % ('Weight ',side, ' Influence'), channel_box=True)

        self.nostrilCtrl = au.add_attribute(objects=[cornerCtrl.control], long_name=['nostril'],
                                            attributeType="float", min=0, dv=1, keyable=True)

        self.cheekMidCtrl = au.add_attribute(objects=[cornerCtrl.control], long_name=['cheekMid'],
                                             attributeType="float", min=0, dv=1, keyable=True)

        self.cheekLowCtrl = au.add_attribute(objects=[cornerCtrl.control], long_name=['cheekLow'],
                                             attributeType="float", min=0, dv=1, keyable=True)

        self.cheekOutUpCtrl = au.add_attribute(objects=[cornerCtrl.control], long_name=['cheekOutUp'],
                                               attributeType="float", min=0, dv=1, keyable=True)

        self.cheekOutLowCtrl = au.add_attribute(objects=[cornerCtrl.control], long_name=['cheekOutLow'],
                                                attributeType="float", min=0, dv=1, keyable=True)

        self.lidOutCtrl = au.add_attribute(objects=[cornerCtrl.control], long_name=['lidOut'],
                                           attributeType="float", min=0, dv=1, keyable=True)

        self.lidCtrl = au.add_attribute(objects=[cornerCtrl.control], long_name=['lid'],
                                        attributeType="float", min=0, dv=1, keyable=True)

        # flipping the controller
        if pos <0:
            mc.setAttr(cornerCtrl.parent_control[0] + '.scaleX', -1)

        self.control= cornerCtrl.control
        self.parentControlZro = cornerCtrl.parent_control[0]
        self.parentControlOffset = cornerCtrl.parent_control[1]