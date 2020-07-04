from __builtin__ import reload

import maya.cmds as mc

import rigging.library.module.base_module as gm
from rigging.library.base.body import hand as hn
from rigging.library.utils import controller as ct, rotation_controller as rc
from rigging.tools import AD_utils as au

reload(gm)
reload(ct)
reload(au)
reload(hn)
reload(rc)

prefix_thumb = 'thumb'
prefix_index = 'index'
prefix_middle = 'middle'
prefix_ring = 'ring'
prefix_pinky = 'pinky'

# FINGER POSITION
BaseF = 'Base'
UpF = 'Up'
MidF = 'Mid'
LowF = 'Low'

class Hand:
    def __init__(self,
                 parent=True,
                 arm_object=None,
                 thumb_finger_base=None,
                 thumb_finger_up=None,
                 thumb_finger_mid=None,
                 skin_thumb_finger_base=None,
                 skin_thumb_finger_up=None,
                 skin_thumb_finger_mid=None,
                 skin_thumb_finger_end=None,
                 prefix_thumb_finger_base=prefix_thumb + BaseF,
                 prefix_thumb_finger_up=prefix_thumb + UpF,
                 prefix_thumb_finger_mid=prefix_thumb + MidF,
                 index_finger_base=None,
                 index_finger_up=None,
                 index_finger_mid=None,
                 index_finger_low=None,
                 skin_index_finger_base=None,
                 skin_index_finger_up=None,
                 skin_index_finger_mid=None,
                 skin_index_finger_low=None,
                 skin_index_finger_end=None,
                 prefix_index_finger_base=prefix_index + BaseF,
                 prefix_index_finger_up=prefix_index + UpF,
                 prefix_index_finger_mid=prefix_index + MidF,
                 prefix_index_finger_low=prefix_index + LowF,
                 middle_finger_base=None,
                 middle_finger_up=None,
                 middle_finger_mid=None,
                 middle_finger_low=None,
                 skin_middle_finger_base=None,
                 skin_middle_finger_up=None,
                 skin_middle_finger_mid=None,
                 skin_middle_finger_low=None,
                 skin_middle_finger_end=None,
                 prefix_middle_finger_base=prefix_middle + BaseF,
                 prefix_middle_finger_up=prefix_middle + UpF,
                 prefix_middle_finger_mid=prefix_middle + MidF,
                 prefix_middle_finger_low=prefix_middle + LowF,
                 ring_finger_base=None,
                 ring_finger_up=None,
                 ring_finger_mid=None,
                 ring_finger_low=None,
                 skin_ring_finger_base=None,
                 skin_ring_finger_up=None,
                 skin_ring_finger_mid=None,
                 skin_ring_finger_low=None,
                 skin_ring_finger_end=None,
                 prefix_ring_finger_base=prefix_ring + BaseF,
                 prefix_ring_finger_up=prefix_ring + UpF,
                 prefix_ring_finger_mid=prefix_ring + MidF,
                 prefix_ring_finger_low=prefix_ring + LowF,
                 pinky_finger_base=None,
                 pinky_finger_up=None,
                 pinky_finger_mid=None,
                 pinky_finger_low=None,
                 skin_pinky_finger_base=None,
                 skin_pinky_finger_up=None,
                 skin_pinky_finger_mid=None,
                 skin_pinky_finger_low=None,
                 skin_pinky_finger_end=None,
                 prefix_pinky_finger_base=prefix_pinky + BaseF,
                 prefix_pinky_finger_up=prefix_pinky + UpF,
                 prefix_pinky_finger_mid=prefix_pinky + MidF,
                 prefix_pinky_finger_low=prefix_pinky + LowF,
                 prefix_finger_setup='fingerSetup',
                 prefix_palm='palm',
                 side=None,
                 thumb=True,
                 index=True,
                 middle=True,
                 ring=True,
                 pinky=True,
                 wrist_jnt=None,
                 hand_jnt=None,
                 skin_hand_jnt=None,
                 palm_jnt=None,
                 skin_palm_jnt=None,
                 size=1.0,
                 single_module=False):

        if parent:
            if thumb or index or middle or ring or pinky == True:
                # create controller hand
                self.finger_setup_ctrl = hn.Build(joint=hand_jnt,
                                                  prefix_joint=prefix_finger_setup,
                                                  shape=ct.STAR,
                                                  ctrl_color='blue',
                                                  side=side,
                                                  scale=size,
                                                  lock_channels=['s', 'v'],
                                                  scale_adjust=0.4,
                                                  )

                # palm
                self.palm_setup_ctrl = hn.Build(joint=palm_jnt,
                                                prefix_joint=prefix_palm,
                                                shape=ct.CUBE,
                                                ctrl_color='red',
                                                side=side,
                                                scale=size,
                                                lock_channels=['v'],
                                                scale_adjust=0.1,
                                                )

                # parent palm parent to hand controller
                mc.parent(self.palm_setup_ctrl.parent_base, self.finger_setup_ctrl.control)

                # add attribute
                self.finger_setup_ctrl.add_attribute_finger(finger_setup_ctrl=self.finger_setup_ctrl.control, thumb=thumb)

                # change position hand
                get_value_tx_hand_jnt = mc.xform(hand_jnt, ws=1, q=1, t=1)[0]

                if get_value_tx_hand_jnt > 0:
                    rc.change_position(self.finger_setup_ctrl.control, '-')
                    rc.change_position(self.finger_setup_ctrl.control, 'xz')
                    rc.change_position(self.finger_setup_ctrl.control, 'xy')

                else:
                    rc.change_position(self.finger_setup_ctrl.control, 'xz')
                    rc.change_position(self.finger_setup_ctrl.control, 'xy')

                # assign controller variable
                self.finger_setup_parent_base = self.finger_setup_ctrl.parent_base
                self.finger_setup_parent_mid = self.finger_setup_ctrl.parent_mid
                self.finger_setup_control = self.finger_setup_ctrl.control

                # PARENT TO ARM
                if not single_module:
                    self.hand_grp_parent(group_finger=self.finger_setup_parent_base, part_ctrl_grp=arm_object.part_control_grp,
                                         constraint=wrist_jnt)
                else:
                    self.hand_grp_parent(group_finger=self.finger_setup_parent_base, part_ctrl_grp=arm_object,
                                         constraint=wrist_jnt)

                # HAND SCALE
                self.hand_scale(controller=self.finger_setup_control, wrist_jnt=wrist_jnt)

                # SKIN JOINT
                au.parent_scale_constraint(hand_jnt, skin_hand_jnt)
                au.parent_scale_constraint(palm_jnt, skin_palm_jnt)
            else:
                mc.delete(skin_palm_jnt, skin_hand_jnt)

        # ==========================================================================================================
        #                                                THUMB CONTROLLER
        # ==========================================================================================================
            if thumb:
                # thumb hand
                self.thumb_finger1 = hn.Build (joint=thumb_finger_base,
                                               prefix_joint=prefix_thumb_finger_base,
                                               shape=ct.STICKSQUARE,
                                               ctrl_color='red',
                                               side=side,
                                               scale=size,
                                               scale_adjust=0.3)

                self.thumb_finger2 = hn.Build(joint=thumb_finger_up,
                                              prefix_joint=prefix_thumb_finger_up,
                                              shape=ct.CIRCLEPLUS,
                                              side=side,
                                              scale=size)

                self.thumb_finger3 = hn.Build(joint=thumb_finger_mid,
                                              prefix_joint=prefix_thumb_finger_mid,
                                              shape=ct.CIRCLEPLUS,
                                              side=side,
                                              scale=size)


                # parent respectively objects
                self.parent_object(self.thumb_finger1.control, self.thumb_finger2.parent_base,
                                   self.thumb_finger2.control, self.thumb_finger3.parent_base)

                # parent to group hand
                mc.parent(self.thumb_finger1.parent_base, self.finger_setup_control)

                # connect general slide crunch, and curl
                self.general_adl_thumb1 = mc.createNode('addDoubleLinear', n='%s%s%s%s_adl' % ('thumb01', 'General', 'CrunchCurl', side))
                self.general_adl_thumb3 = mc.createNode('addDoubleLinear', n='%s%s%s%s_adl' % ('thumb03', 'General', 'CrunchCurl', side))

                # connect to parent offset from output slide, crunch, curl index 2
                mc.connectAttr(self.general_adl_thumb1 + '.output', self.thumb_finger1.parent_mid + '.rotateZ')

                # crunch
                self.thumb_crunch(name_connection='thumbCrunch', control_finger_setup=self.finger_setup_control, prefix_finger='thumb',
                                  side=side, output2=self.general_adl_thumb1 + '.input2', output3=self.general_adl_thumb3 + '.input2')

                # curl
                self.curl(name_connection='thumbCurl', control_finger_setup=self.finger_setup_control, prefix_finger='thumb',
                          output=self.thumb_finger2.parent_mid + '.rotateZ', side=side)

                # spread
                self.spread(name_connection='thumbSpread', control_finger_setup=self.finger_setup_control, prefix_finger='thumb', side=side,
                            percentage=0.75, output=self.general_adl_thumb1 + '.input1')

                # curl general
                self.general_curl_thumb3 = mc.createNode('addDoubleLinear', n='%s%s%s%s_adl' % ('thumb03', 'General', 'Curl', side))
                mc.connectAttr(self.thumb_finger2.parent_mid + '.rotateZ', self.general_curl_thumb3 + '.input1')
                mc.connectAttr(self.general_adl_thumb3 + '.output', self.general_curl_thumb3 + '.input2')

                # connect attribute to below part hand
                mc.connectAttr(self.thumb_finger1.parent_mid + '.rotateZ', self.general_adl_thumb3 + '.input1')
                mc.connectAttr(self.general_curl_thumb3 + '.output', self.thumb_finger3.parent_mid + '.rotateZ')

                # rotate module controller
                self.change_pos_ctrl(thumb_finger_base, self.thumb_finger1.control)

                # SKINNING JOINT
                au.parent_scale_constraint(thumb_finger_base, skin_thumb_finger_base)
                au.parent_scale_constraint(thumb_finger_up, skin_thumb_finger_up)
                au.parent_scale_constraint(thumb_finger_mid, skin_thumb_finger_mid)
                mc.delete(skin_thumb_finger_end)
            else:
                mc.delete(skin_thumb_finger_base)

        # ==========================================================================================================
        #                                                INDEX CONTROLLER
        # ==========================================================================================================
            if index:
                # index hand
                self.index_finger1 = hn.Build(joint=index_finger_base,
                                              prefix_joint=prefix_index_finger_base,
                                              shape=ct.STICKSQUARE,
                                              ctrl_color='red',
                                              side=side,
                                              scale=size,
                                              scale_adjust=0.3)

                index_curl = au.add_attribute(objects=[self.index_finger1.control], long_name=['curl'],
                                              attributeType="float", dv=0, keyable=True)

                self.index_finger2 = hn.Build(joint=index_finger_up,
                                              prefix_joint=prefix_index_finger_up,
                                              shape=ct.CIRCLEPLUS,
                                              side=side,
                                              scale=size)

                self.index_finger3 = hn.Build(joint=index_finger_mid,
                                              prefix_joint=prefix_index_finger_mid,
                                              shape=ct.CIRCLEPLUS,
                                              side=side,
                                              scale=size)

                self.index_finger4 = hn.Build(joint=index_finger_low,
                                              prefix_joint=prefix_index_finger_low,
                                              shape=ct.CIRCLEPLUS,
                                              side=side,
                                              scale=size)
                # parent respectively objects
                self.parent_object(self.index_finger1.control, self.index_finger2.parent_base,
                                   self.index_finger2.control, self.index_finger3.parent_base,
                                   self.index_finger3.control, self.index_finger4.parent_base)

                # parent to group hand
                mc.parent(self.index_finger1.parent_base, self.finger_setup_control)

                # connect general slide crunch, and curl
                self.general_adl_index2 = mc.createNode('addDoubleLinear', n='%s%s%s%s_adl' % ('index02', 'General', 'SlideCrunchCurl', side))
                self.general_adl_index3 = mc.createNode('addDoubleLinear', n='%s%s%s%s_adl' % ('index03', 'General', 'SlideCrunchCurl', side))
                self.general_adl_index4 = mc.createNode('addDoubleLinear', n='%s%s%s%s_adl' % ('index04', 'General', 'SlideCrunchCurl', side))

                # connect to parent offset from output slide, crunch, curl index 2
                mc.connectAttr(self.general_adl_index2 + '.output', self.index_finger2.parent_mid + '.rotateZ')

                # slide
                self.slide(name_connection='slide', control_finger_setup=self.finger_setup_control, prefix_finger='index',
                           side=side, output2=self.general_adl_index2 + '.input1', output3=self.general_adl_index3 + '.input1',
                           output4=self.general_adl_index4 + '.input1')

                # crunch
                self.crunch(name_connection='crunch', control_finger_setup=self.finger_setup_control, prefix_finger='index',
                            side=side, output2=self.finger2_slide_adl + '.input2', output3=self.finger3_slide_adl + '.input2',
                            output4=self.finger4_slide_adl + '.input2')
                # curl
                self.curl(name_connection='curl', control_finger_setup=self.finger_setup_control, prefix_finger='index',
                          output=(self.general_adl_index2 + '.input2'), side=side)

                # curl ind
                self.curl_independent(control_finger_setup_base=self.index_finger1.control, curl_variable=index_curl,
                                      first_ctrl_parent_grp=self.index_finger2.parent_curl, second_ctrl_parent_grp=self.index_finger3.parent_curl,
                                      third_ctrl_parent_grp=self.index_finger4.parent_curl)

                # cup pinky
                self.cup(name_connection='cupOuter', control_finger_setup= self.finger_setup_control, prefix_finger='index',
                         percentage= 0.1, output= (self.finger_add_two_cup + '.input1'), side=side)

                # cup index
                self.cup(name_connection='cupInner', control_finger_setup=self.finger_setup_control, prefix_finger='index',
                         percentage=0.9, output=(self.finger_add_two_cup + '.input2'), side=side)


                # spread
                self.spread(name_connection='spread', control_finger_setup=self.finger_setup_control, prefix_finger='index', side=side,
                            percentage=0.5, output=self.index_finger2.parent_mid + '.rotateX')


                # connect attribute to below part hand
                mc.connectAttr(self.index_finger2.parent_mid + '.rotateZ', self.general_adl_index3 + '.input2')
                mc.connectAttr(self.index_finger3.parent_mid + '.rotateZ', self.general_adl_index4 + '.input2')

                # connect to parent offset from output slide, crunch, curl index 3 and 4
                mc.connectAttr(self.general_adl_index3 + '.output', self.index_finger3.parent_mid + '.rotateZ')
                mc.connectAttr(self.general_adl_index4 + '.output', self.index_finger4.parent_mid + '.rotateZ')

                # rotate module controller
                self.change_pos_ctrl(index_finger_base, self.index_finger1.control)

                # SKINNING JOINT
                au.parent_scale_constraint(index_finger_base, skin_index_finger_base)
                au.parent_scale_constraint(index_finger_up, skin_index_finger_up)
                au.parent_scale_constraint(index_finger_mid, skin_index_finger_mid)
                au.parent_scale_constraint(index_finger_low, skin_index_finger_low)
                mc.delete(skin_index_finger_end)
            else:
                mc.delete(skin_index_finger_base)
        # ==========================================================================================================
        #                                                MIDDLE CONTROLLER
        # ==========================================================================================================
            if middle:
                # middle hand
                self.middle_finger1 = hn.Build(joint=middle_finger_base,
                                               prefix_joint=prefix_middle_finger_base,
                                               shape=ct.STICKSQUARE,
                                               ctrl_color='red',
                                               side=side,
                                               scale=size,
                                               scale_adjust=0.3)

                middle_curl = au.add_attribute(objects=[self.middle_finger1.control], long_name=['curl'],
                                               attributeType="float", dv=0, keyable=True)

                self.middle_finger2 = hn.Build(joint=middle_finger_up,
                                               prefix_joint=prefix_middle_finger_up,
                                               shape=ct.CIRCLEPLUS,
                                               side=side,
                                               scale=size)

                self.middle_finger3 = hn.Build(joint=middle_finger_mid,
                                               prefix_joint=prefix_middle_finger_mid,
                                               shape=ct.CIRCLEPLUS,
                                               side=side,
                                               scale=size)

                self.middle_finger4 = hn.Build(joint=middle_finger_low,
                                               prefix_joint=prefix_middle_finger_low,
                                               shape=ct.CIRCLEPLUS,
                                               side=side,
                                               scale=size)

                # parent respectively objects
                self.parent_object(self.middle_finger1.control, self.middle_finger2.parent_base,
                                   self.middle_finger2.control, self.middle_finger3.parent_base,
                                   self.middle_finger3.control, self.middle_finger4.parent_base)

                # parent to group hand
                mc.parent(self.middle_finger1.parent_base, self.finger_setup_control)

                # connect general slide crunch, and curl
                self.general_adl_middle2 = mc.createNode('addDoubleLinear',
                                                         n='%s%s%s%s_adl' % ('middle02', 'General', 'SlideCrunchCurl', side))
                self.general_adl_middle3 = mc.createNode('addDoubleLinear',
                                                         n='%s%s%s%s_adl' % ('middle03', 'General', 'SlideCrunchCurl', side))
                self.general_adl_middle4 = mc.createNode('addDoubleLinear',
                                                         n='%s%s%s%s_adl' % ('middle04', 'General', 'SlideCrunchCurl', side))

                # connect to parent offset from output slide, crunch, curl index 2
                mc.connectAttr(self.general_adl_middle2 + '.output', self.middle_finger2.parent_mid + '.rotateZ')

                # slide
                self.slide(name_connection='slide', control_finger_setup=self.finger_setup_control, prefix_finger='middle',
                           side=side, output2=self.general_adl_middle2 + '.input1', output3=self.general_adl_middle3 + '.input1',
                           output4=self.general_adl_middle4 + '.input1')

                # crunch
                self.crunch(name_connection='crunch', control_finger_setup=self.finger_setup_control, prefix_finger='middle',
                            side=side, output2=self.finger2_slide_adl + '.input2', output3=self.finger3_slide_adl + '.input2',
                            output4=self.finger4_slide_adl + '.input2')
                # curl
                self.curl(name_connection='curl', control_finger_setup=self.finger_setup_control, prefix_finger='middle',
                          output=(self.general_adl_middle2 + '.input2'), side=side)

                # curl ind
                self.curl_independent(control_finger_setup_base=self.middle_finger1.control, curl_variable=middle_curl,
                                      first_ctrl_parent_grp=self.middle_finger2.parent_curl, second_ctrl_parent_grp=self.middle_finger3.parent_curl,
                                      third_ctrl_parent_grp=self.middle_finger4.parent_curl)

                # cup pinky
                self.cup(name_connection='cupOuter', control_finger_setup=self.finger_setup_control,
                         prefix_finger='middle', percentage=0.35, output=(self.finger_add_two_cup + '.input1'), side=side)

                # cup index
                self.cup(name_connection='cupInner', control_finger_setup=self.finger_setup_control,
                         prefix_finger='middle', percentage=0.65, output=(self.finger_add_two_cup + '.input2'), side=side)

                # connect attribute to below part hand
                mc.connectAttr(self.middle_finger2.parent_mid + '.rotateZ', self.general_adl_middle3 + '.input2')
                mc.connectAttr(self.middle_finger3.parent_mid + '.rotateZ', self.general_adl_middle4 + '.input2')

                # connect to parent offset from output slide, crunch, curl index 3 and 4
                mc.connectAttr(self.general_adl_middle3 + '.output', self.middle_finger3.parent_mid + '.rotateZ')
                mc.connectAttr(self.general_adl_middle4 + '.output', self.middle_finger4.parent_mid + '.rotateZ')

                # rotate module controller
                self.change_pos_ctrl(middle_finger_base, self.middle_finger1.control)

                # SKINNING JOINT
                au.parent_scale_constraint(middle_finger_base, skin_middle_finger_base)
                au.parent_scale_constraint(middle_finger_up, skin_middle_finger_up)
                au.parent_scale_constraint(middle_finger_mid, skin_middle_finger_mid)
                au.parent_scale_constraint(middle_finger_low, skin_middle_finger_low)
                mc.delete(skin_middle_finger_end)
            else:
                mc.delete(skin_middle_finger_base)
        # ==========================================================================================================
        #                                                RING CONTROLLER
        # ==========================================================================================================
            if ring:
                # ring hand
                self.ring_finger1 = hn.Build(joint=ring_finger_base,
                                             prefix_joint=prefix_ring_finger_base,
                                             shape=ct.STICKSQUARE,
                                             ctrl_color='red',
                                             side=side,
                                             scale=size,
                                             scale_adjust=0.3)

                ring_curl = au.add_attribute(objects=[self.ring_finger1.control], long_name=['curl'],
                                             attributeType="float", dv=0, keyable=True)

                self.ring_finger2 = hn.Build(joint=ring_finger_up,
                                             prefix_joint=prefix_ring_finger_up,
                                             shape=ct.CIRCLEPLUS,
                                             side=side,
                                             scale=size)

                self.ring_finger3 = hn.Build(joint=ring_finger_mid,
                                             prefix_joint=prefix_ring_finger_mid,
                                             shape=ct.CIRCLEPLUS,
                                             side=side,
                                             scale=size)

                self.ring_finger4 = hn.Build(joint=ring_finger_low,
                                             prefix_joint=prefix_ring_finger_low,
                                             shape=ct.CIRCLEPLUS,
                                             side=side,
                                             scale=size)

                # parent respectively objects
                self.parent_object(self.ring_finger1.control, self.ring_finger2.parent_base,
                                   self.ring_finger2.control, self.ring_finger3.parent_base,
                                   self.ring_finger3.control, self.ring_finger4.parent_base)

                # parent to group hand
                mc.parent(self.ring_finger1.parent_base, self.finger_setup_control)

                # connect general slide crunch, and curl
                self.general_adl_ring2 = mc.createNode('addDoubleLinear',
                                                       n='%s%s%s%s_adl' % ('ring02', 'General', 'SlideCrunchCurl', side))
                self.general_adl_ring3 = mc.createNode('addDoubleLinear',
                                                       n='%s%s%s%s_adl' % ('ring03', 'General', 'SlideCrunchCurl', side))
                self.general_adl_ring4 = mc.createNode('addDoubleLinear',
                                                       n='%s%s%s%s_adl' % ('ring04', 'General', 'SlideCrunchCurl', side))

                # connect to parent offset from output slide, crunch, curl index 2
                mc.connectAttr(self.general_adl_ring2 + '.output', self.ring_finger2.parent_mid + '.rotateZ')

                # slide
                self.slide(name_connection='slide', control_finger_setup=self.finger_setup_control, prefix_finger='ring',
                           side=side, output2=self.general_adl_ring2 + '.input1',
                           output3=self.general_adl_ring3 + '.input1',
                           output4=self.general_adl_ring4 + '.input1')

                # crunch
                self.crunch(name_connection='crunch', control_finger_setup=self.finger_setup_control, prefix_finger='ring',
                            side=side, output2=self.finger2_slide_adl + '.input2', output3=self.finger3_slide_adl + '.input2',
                            output4=self.finger4_slide_adl + '.input2')
                # curl
                self.curl(name_connection='curl', control_finger_setup=self.finger_setup_control, prefix_finger='ring',
                          output=(self.general_adl_ring2 + '.input2'), side=side)

                # curl ind
                self.curl_independent(control_finger_setup_base=self.ring_finger1.control, curl_variable=ring_curl,
                                      first_ctrl_parent_grp=self.ring_finger2.parent_curl, second_ctrl_parent_grp=self.ring_finger3.parent_curl,
                                      third_ctrl_parent_grp=self.ring_finger4.parent_curl)

                # cup pinky
                self.cup(name_connection='cupOuter', control_finger_setup=self.finger_setup_control,
                         prefix_finger='ring', percentage=0.65, output=(self.finger_add_two_cup + '.input1'), side=side)

                # cup index
                self.cup(name_connection='cupInner', control_finger_setup=self.finger_setup_control,
                         prefix_finger='ring', percentage=0.35, output=(self.finger_add_two_cup + '.input2'), side=side)

                # spread
                self.spread(name_connection='spread', control_finger_setup=self.finger_setup_control, prefix_finger='ring', side=side,
                            percentage=-0.35, output=self.ring_finger2.parent_mid + '.rotateX')

                # connect attribute to below part hand
                mc.connectAttr(self.ring_finger2.parent_mid + '.rotateZ', self.general_adl_ring3 + '.input2')
                mc.connectAttr(self.ring_finger3.parent_mid + '.rotateZ', self.general_adl_ring4 + '.input2')

                # connect to parent offset from output slide, crunch, curl index 3 and 4
                mc.connectAttr(self.general_adl_ring3 + '.output', self.ring_finger3.parent_mid + '.rotateZ')
                mc.connectAttr(self.general_adl_ring4 + '.output', self.ring_finger4.parent_mid + '.rotateZ')

                # rotate module controller
                self.change_pos_ctrl(ring_finger_base, self.ring_finger1.control)

                # SKINNING JOINT
                au.parent_scale_constraint(ring_finger_base, skin_ring_finger_base)
                au.parent_scale_constraint(ring_finger_up, skin_ring_finger_up)
                au.parent_scale_constraint(ring_finger_mid, skin_ring_finger_mid)
                au.parent_scale_constraint(ring_finger_low, skin_ring_finger_low)
                mc.delete(skin_ring_finger_end)
            else:
                mc.delete(skin_ring_finger_base)

        # ==========================================================================================================
        #                                                PINKY CONTROLLER
        # ==========================================================================================================
            if pinky:
                # pinky hand
                self.pinky_finger1 = hn.Build(joint=pinky_finger_base,
                                              prefix_joint=prefix_pinky_finger_base,
                                              shape=ct.STICKSQUARE,
                                              ctrl_color='red',
                                              side=side,
                                              scale=size,
                                              scale_adjust=0.3)

                pinky_curl = au.add_attribute(objects=[self.pinky_finger1.control], long_name=['curl'],
                                              attributeType="float", dv=0, keyable=True)

                self.pinky_finger2 = hn.Build(joint=pinky_finger_up,
                                              prefix_joint=prefix_pinky_finger_up,
                                              shape=ct.CIRCLEPLUS,
                                              side=side,
                                              scale=size)

                self.pinky_finger3 = hn.Build(joint=pinky_finger_mid,
                                              prefix_joint=prefix_pinky_finger_mid,
                                              shape=ct.CIRCLEPLUS,
                                              side=side,
                                              scale=size)

                self.pinky_finger4 = hn.Build(joint=pinky_finger_low,
                                              prefix_joint=prefix_pinky_finger_low,
                                              shape=ct.CIRCLEPLUS,
                                              side=side,
                                              scale=size)

                # parent respectively objects
                self.parent_object(self.pinky_finger1.control, self.pinky_finger2.parent_base,
                                   self.pinky_finger2.control, self.pinky_finger3.parent_base,
                                   self.pinky_finger3.control, self.pinky_finger4.parent_base)

                # parent to group hand
                mc.parent(self.pinky_finger1.parent_base, self.finger_setup_control)

                # connect general slide crunch, and curl
                self.general_adl_pinky2 = mc.createNode('addDoubleLinear',
                                                        n='%s%s%s%s_adl' % ('pinky02', 'General', 'SlideCrunchCurl', side))
                self.general_adl_pinky3 = mc.createNode('addDoubleLinear',
                                                        n='%s%s%s%s_adl' % ('pinky03', 'General', 'SlideCrunchCurl', side))
                self.general_adl_pinky4 = mc.createNode('addDoubleLinear',
                                                        n='%s%s%s%s_adl' % ('pinky04', 'General', 'SlideCrunchCurl', side))

                # connect to parent offset from output slide, crunch, curl index 2
                mc.connectAttr(self.general_adl_pinky2 + '.output', self.pinky_finger2.parent_mid + '.rotateZ')

                # slide
                self.slide(name_connection='slide', control_finger_setup=self.finger_setup_control, prefix_finger='pinky',
                           side=side, output2=self.general_adl_pinky2 + '.input1',
                           output3=self.general_adl_pinky3 + '.input1',
                           output4=self.general_adl_pinky4 + '.input1')

                # crunch
                self.crunch(name_connection='crunch', control_finger_setup=self.finger_setup_control, prefix_finger='pinky',
                            side=side, output2=self.finger2_slide_adl + '.input2', output3=self.finger3_slide_adl + '.input2',
                            output4=self.finger4_slide_adl + '.input2')
                # curl
                self.curl(name_connection='curl', control_finger_setup=self.finger_setup_control, prefix_finger='pinky',
                          output=(self.general_adl_pinky2 + '.input2'), side=side)

                # curl ind
                self.curl_independent(control_finger_setup_base=self.pinky_finger1.control, curl_variable=pinky_curl,
                                      first_ctrl_parent_grp=self.pinky_finger2.parent_curl, second_ctrl_parent_grp=self.pinky_finger3.parent_curl,
                                      third_ctrl_parent_grp=self.pinky_finger4.parent_curl)
                # cup pinky
                self.cup(name_connection='cupOuter', control_finger_setup=self.finger_setup_control,
                         prefix_finger='pinky', percentage=0.9, output=(self.finger_add_two_cup + '.input1'), side=side)

                # cup index
                self.cup(name_connection='cupInner', control_finger_setup=self.finger_setup_control,
                         prefix_finger='pinky', percentage=0.1, output=(self.finger_add_two_cup + '.input2'), side=side)

                # spread
                self.spread(name_connection='spread', control_finger_setup=self.finger_setup_control, prefix_finger='pinky', side=side,
                            percentage=-0.75, output=self.pinky_finger2.parent_mid + '.rotateX')

                # connect attribute to below part hand
                mc.connectAttr(self.pinky_finger2.parent_mid + '.rotateZ', self.general_adl_pinky3 + '.input2')
                mc.connectAttr(self.pinky_finger3.parent_mid + '.rotateZ', self.general_adl_pinky4 + '.input2')

                # connect to parent offset from output slide, crunch, curl index 3 and 4
                mc.connectAttr(self.general_adl_pinky3 + '.output', self.pinky_finger3.parent_mid + '.rotateZ')
                mc.connectAttr(self.general_adl_pinky4 + '.output', self.pinky_finger4.parent_mid + '.rotateZ')

                # rotate module controller
                self.change_pos_ctrl(pinky_finger_base, self.pinky_finger1.control)

                # SKINNING JOINT
                au.parent_scale_constraint(pinky_finger_base, skin_pinky_finger_base)
                au.parent_scale_constraint(pinky_finger_up, skin_pinky_finger_up)
                au.parent_scale_constraint(pinky_finger_mid, skin_pinky_finger_mid)
                au.parent_scale_constraint(pinky_finger_low, skin_pinky_finger_low)
                mc.delete(skin_pinky_finger_end)
            else:
                mc.delete(skin_pinky_finger_base)
        else:
            mc.delete(skin_hand_jnt, skin_palm_jnt, skin_thumb_finger_base)
    # ==================================================================================================================
    #                                               GENERAL FUNCTION FINGER
    # ==================================================================================================================
    def parent_object(self, base_ctrl='', up='', up_ctrl='', mid='', mid_ctrl='', low=''):
        if mc.objExists(low):
            mc.parent(low, mid_ctrl)
            mc.parent(mid, up_ctrl)
            mc.parent(up, base_ctrl)
        else:
            mc.parent(mid, up_ctrl)
            mc.parent(up, base_ctrl)

    def change_pos_ctrl(self, finger_base, controller):
        get_value_tx_finger_jnt = mc.xform(finger_base, ws=1, q=1, t=1)[0]
        if get_value_tx_finger_jnt > 0:
                rc.change_position(controller, '-')
                rc.change_position(controller, 'yz')

        else:
            rc.change_position(controller, 'yz')

    def curl_independent(self, control_finger_setup_base, curl_variable, first_ctrl_parent_grp, second_ctrl_parent_grp, third_ctrl_parent_grp):

        mc.connectAttr(control_finger_setup_base + '.%s' % curl_variable, first_ctrl_parent_grp + '.rotateZ')
        mc.connectAttr(control_finger_setup_base + '.%s' % curl_variable, second_ctrl_parent_grp + '.rotateZ')
        mc.connectAttr(control_finger_setup_base + '.%s' % curl_variable, third_ctrl_parent_grp + '.rotateZ')


    def curl(self, name_connection, control_finger_setup, prefix_finger, side, output):
        # create mult double linear for cup
        self.finger_add_two_cup = mc.createNode('addDoubleLinear', n='%s%s%s_adl' % (prefix_finger, 'CupPinkyIndex', side))

        # add double linear for curl
        self.finger_curl_adl = mc.createNode('addDoubleLinear', n='%s%s%s_adl' % (prefix_finger, 'Curl', side))
        mc.connectAttr(control_finger_setup + '.' + name_connection, self.finger_curl_adl + '.input1')
        mc.connectAttr(self.finger_add_two_cup + '.output', self.finger_curl_adl + '.input2')
        mc.connectAttr(self.finger_curl_adl + '.output', output)

    def cup(self, name_connection, control_finger_setup, prefix_finger, side, percentage, output):
        # multiplied by percentage
        self.finger_cup_percentage_mdl = mc.createNode('multDoubleLinear', n='%s%s%s_mdl' % (prefix_finger, name_connection.capitalize() + 'Percent', side))
        mc.connectAttr(control_finger_setup + '.' + name_connection, self.finger_cup_percentage_mdl + '.input1')
        mc.setAttr(self.finger_cup_percentage_mdl + '.input2', percentage)

        mc.connectAttr(self.finger_cup_percentage_mdl + '.output', output)

    def spread(self, name_connection, control_finger_setup, prefix_finger, side, percentage, output):
        # multiplied by percentage
        self.finger_spread_percentage_mdl = mc.createNode('multDoubleLinear', n='%s%s%s_mdl' % (prefix_finger, 'Spread', side))
        mc.connectAttr(control_finger_setup + '.' + name_connection, self.finger_spread_percentage_mdl + '.input1')
        mc.setAttr(self.finger_spread_percentage_mdl + '.input2', percentage)

        mc.connectAttr(self.finger_spread_percentage_mdl + '.output', output)

    def slide(self, control_finger_setup, name_connection, prefix_finger, side, output2, output3, output4):
        # finger up
        self.finger2_slide_adl = mc.createNode('addDoubleLinear', n='%s%s%s%s_adl' % (prefix_finger, 'Up', name_connection.capitalize(), side))
        mc.connectAttr(control_finger_setup + '.' + name_connection, self.finger2_slide_adl + '.input1')
        mc.connectAttr(self.finger2_slide_adl + '.output', output2)

        # finger mid
        self.finger3_slide_mdl = mc.createNode('multDoubleLinear', n='%s%s%s%s_mdl' % (prefix_finger, 'Mid', name_connection.capitalize(), side))
        mc.connectAttr(control_finger_setup + '.' + name_connection, self.finger3_slide_mdl + '.input1')
        mc.setAttr(self.finger3_slide_mdl + '.input2', -3)

        self.finger3_slide_adl = mc.createNode('addDoubleLinear',
                                               n='%s%s%s%s_adl' % (prefix_finger, 'Mid', name_connection.capitalize(), side))
        mc.connectAttr(self.finger3_slide_mdl + '.output', self.finger3_slide_adl + '.input1')
        mc.connectAttr(self.finger3_slide_adl + '.output', output3)

        # finger low
        self.finger4_slide_mdl = mc.createNode('multDoubleLinear', n='%s%s%s%s_mdl' % (prefix_finger, 'Low', name_connection.capitalize(), side))
        mc.connectAttr(control_finger_setup + '.' + name_connection, self.finger4_slide_mdl + '.input1')
        mc.setAttr(self.finger4_slide_mdl + '.input2', 2.6)

        self.finger4_slide_adl = mc.createNode('addDoubleLinear',
                                               n='%s%s%s%s_adl' % (prefix_finger, 'Low', name_connection.capitalize(), side))
        mc.connectAttr(self.finger4_slide_mdl + '.output', self.finger4_slide_adl + '.input1')
        mc.connectAttr(self.finger4_slide_adl + '.output', output4)

    def crunch(self, control_finger_setup, name_connection, prefix_finger, side, output2, output3, output4):
        # finger up
        mc.connectAttr(control_finger_setup + '.' + name_connection, output2)

        # finger mid
        self.finger3_crunch_mdl = mc.createNode('multDoubleLinear', n='%s%s%s%s_mdl' % (prefix_finger, 'Mid', name_connection.capitalize(), side))
        mc.connectAttr(control_finger_setup + '.' + name_connection, self.finger3_crunch_mdl + '.input1')
        mc.setAttr(self.finger3_crunch_mdl + '.input2', -3)

        mc.connectAttr(self.finger3_crunch_mdl + '.output', output3)

        # finger low
        self.finger4_crunch_mdl = mc.createNode('multDoubleLinear', n='%s%s%s%s_mdl' % (
            prefix_finger, 'Low', name_connection.capitalize(), side))
        mc.connectAttr(control_finger_setup + '.' + name_connection, self.finger4_crunch_mdl + '.input1')
        mc.setAttr(self.finger4_crunch_mdl + '.input2', 0.01)
        mc.connectAttr(self.finger4_crunch_mdl + '.output', output4)

    def thumb_crunch(self, control_finger_setup, name_connection, prefix_finger, side, output2, output3):
        # finger up
        mc.connectAttr(control_finger_setup + '.' + name_connection, output2)

        # finger mid
        self.finger3_slide_mdl = mc.createNode('multDoubleLinear', n='%s%s%s%s_mdl' % (prefix_finger, 'Mid', name_connection.capitalize(), side))
        mc.connectAttr(control_finger_setup + '.' + name_connection, self.finger3_slide_mdl + '.input1')
        mc.setAttr(self.finger3_slide_mdl + '.input2', -3)
        mc.connectAttr(self.finger3_slide_mdl + '.output', output3)

    def hand_grp_parent(self, group_finger, part_ctrl_grp, constraint):
        # parent group finger to arm part controller
        mc.parent(group_finger, part_ctrl_grp)
        # parent constraint from hand joint
        pac = mc.parentConstraint(constraint, group_finger, mo=1)
        # scale constraint from hand joint
        sc = mc.scaleConstraint(constraint, group_finger, mo=1)

        # rename constraint
        au.constraint_rename([pac[0], sc[0]])


    def hand_scale(self, controller, wrist_jnt):
        mc.connectAttr(controller + '.handScaleX', wrist_jnt + '.scaleX')
        mc.connectAttr(controller + '.handScaleY', wrist_jnt + '.scaleY')
        mc.connectAttr(controller + '.handScaleZ', wrist_jnt + '.scaleZ')