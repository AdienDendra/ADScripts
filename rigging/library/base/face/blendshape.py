from __future__ import absolute_import

import re

import maya.cmds as cmds

from rigging.library.utils import transform as rlu_transform
from rigging.tools import utils as rt_utils


class BuildTwoSide:
    def __init__(self, blendshape_node_name, squash_stretch_prefix, roll_low_prefix, blendshape_suffix, roll_up_prefix,
                 squash_stretch_attr, mouth_ctrl,
                 controller_roll_up_bsh_attr, controller_roll_low_bsh_attr, cheek_out_prefix, cheek_out_attr_LFT,
                 cheek_out_attr_RGT, side_LFT, side_RGT):

        # TWO SLIDE
        self.two_value_slider(blendshape_name=blendshape_node_name, controller=mouth_ctrl, prefix=squash_stretch_prefix,
                              side='', slide_atribute=squash_stretch_attr,
                              sub_prefix_one='Stretch', value_pos_one=10, sub_prefix_two='Squash', value_pos_two=-10,
                              connect=True, suffix_bsh=blendshape_suffix)

        self.two_value_slider(blendshape_name=blendshape_node_name, controller=mouth_ctrl, prefix=roll_low_prefix,
                              side='', slide_atribute=controller_roll_low_bsh_attr,
                              sub_prefix_one='Out', value_pos_one=10, sub_prefix_two='In', value_pos_two=-10,
                              connect=True, suffix_bsh=blendshape_suffix)

        self.two_value_slider(blendshape_name=blendshape_node_name, controller=mouth_ctrl, prefix=roll_up_prefix,
                              side='', slide_atribute=controller_roll_up_bsh_attr,
                              sub_prefix_one='Out', value_pos_one=10, sub_prefix_two='In', value_pos_two=-10,
                              connect=True, suffix_bsh=blendshape_suffix)

        self.one_value_slider(blendshape_name=blendshape_node_name, controller=mouth_ctrl, prefix=cheek_out_prefix,
                              side=side_LFT, slide_atribute=cheek_out_attr_LFT, sub_prefix='',
                              valueNode=10, side_RGT=side_RGT, side_LFT=side_LFT, suffix_bsh=blendshape_suffix)

        self.one_value_slider(blendshape_name=blendshape_node_name, controller=mouth_ctrl, prefix=cheek_out_prefix,
                              side=side_RGT, slide_atribute=cheek_out_attr_RGT, sub_prefix='',
                              valueNode=10, side_RGT=side_RGT, side_LFT=side_LFT, suffix_bsh=blendshape_suffix)

    def combined_value_slider(self, blendshape_name, controller, side, sub_prefix_first='', sub_prefix_second='',
                              clamp_driver_first_one='',
                              clamp_driver_first_two='', clamp_driver_second_one='', clamp_driver_second_two='',
                              two_side=True):

        ctrl_new = rlu_transform.reposition_side(controller, 'BshRGT', 'BshLFT')
        list_weight = cmds.listAttr(blendshape_name + '.w', m=True)

        # DRIVER VALUE
        mult_double_linear_combined_one = cmds.createNode('multDoubleLinear', n=rt_utils.prefix_name(
            ctrl_new) + sub_prefix_first + 'BshCombined' + side + '_mdl')
        cmds.connectAttr(clamp_driver_first_one + '.outputR', mult_double_linear_combined_one + '.input1')
        cmds.connectAttr(clamp_driver_first_two + '.outputR', mult_double_linear_combined_one + '.input2')

        if two_side:
            mult_double_linear_combined_two = cmds.createNode('multDoubleLinear', n=rt_utils.prefix_name(
                ctrl_new) + sub_prefix_second + 'BshCombined' + side + '_mdl')
            cmds.connectAttr(clamp_driver_second_one + '.outputR', mult_double_linear_combined_two + '.input1')
            cmds.connectAttr(clamp_driver_second_two + '.outputR', mult_double_linear_combined_two + '.input2')
            self.connect_node_to_bsh(list_weight, mult_double_linear_combined_two, 'output',
                                     blendshape_name=blendshape_name, side_RGT='BshCombinedRGT',
                                     side_LFT='BshCombinedLFT', side=side)

        # CONNECT TO BSH
        self.connect_node_to_bsh(list_weight, mult_double_linear_combined_one, 'output',
                                 blendshape_name=blendshape_name, side_RGT='BshCombinedRGT', side_LFT='BshCombinedLFT',
                                 side=side)

    def two_value_slider(self, blendshape_name, controller, prefix, side, slide_atribute, sub_prefix_one, value_pos_one,
                         sub_prefix_two, value_pos_two, suffix_bsh,
                         side_RGT='', side_LFT='', connect=True, clamp_up_min=0.0, clamp_up_max=10.0,
                         clamp_down_min=0.0,
                         clamp_down_max=10.0):
        # UP
        ctrl_new = rlu_transform.reposition_side(prefix, side_RGT, side_LFT)
        mult_double_linear_up = cmds.createNode('multDoubleLinear',
                                                n=rt_utils.prefix_name(
                                                    ctrl_new) + sub_prefix_one + 'Bsh' + side + '_mdl')
        cmds.setAttr(mult_double_linear_up + '.input2', 1.0 / value_pos_one)
        cmds.connectAttr(controller + '.%s' % slide_atribute, mult_double_linear_up + '.input1')

        clamp_up = cmds.createNode('clamp', n=rt_utils.prefix_name(ctrl_new) + sub_prefix_one + 'Bsh' + side + '_clm')
        cmds.setAttr(clamp_up + '.maxR', clamp_up_max)
        cmds.setAttr(clamp_up + '.minR', clamp_up_min)

        cmds.connectAttr(mult_double_linear_up + '.output', clamp_up + '.inputR')

        # DOWN
        mult_double_linear_down = cmds.createNode('multDoubleLinear',
                                                  n=rt_utils.prefix_name(
                                                      ctrl_new) + sub_prefix_two + 'Bsh' + side + '_mdl')
        cmds.setAttr(mult_double_linear_down + '.input2', 1.0 / value_pos_two)
        cmds.connectAttr(controller + '.%s' % slide_atribute, mult_double_linear_down + '.input1')

        clamp_down = cmds.createNode('clamp', n=rt_utils.prefix_name(ctrl_new) + sub_prefix_two + 'Bsh' + side + '_clm')
        cmds.setAttr(clamp_down + '.maxR', clamp_down_max)
        cmds.setAttr(clamp_down + '.minR', clamp_down_min)
        cmds.connectAttr(mult_double_linear_down + '.output', clamp_down + '.inputR')

        # CONNECT TO BSH
        if connect:
            list_weight = cmds.listAttr(blendshape_name + '.w', m=True)
            self.connect_node_to_bsh(list_weight, clamp_up, 'outputR', blendshape_name=blendshape_name,
                                     side_RGT=side_RGT, side_LFT=side_LFT, side=side, suffix_bsh=suffix_bsh)
            self.connect_node_to_bsh(list_weight, clamp_down, 'outputR', blendshape_name=blendshape_name,
                                     side_RGT=side_RGT, side_LFT=side_LFT, side=side, suffix_bsh=suffix_bsh)
        # else:
        return clamp_up, clamp_down

    def one_value_slider(self, blendshape_name, controller, side, slide_atribute, prefix, suffix_bsh, sub_prefix,
                         valueNode, side_RGT='', side_LFT='',
                         clamp_max=10.0, clamp_min=0.0
                         ):
        ctrl_new = rlu_transform.reposition_side(prefix, side_RGT, side_LFT)
        mult_double_linear = cmds.createNode('multDoubleLinear',
                                             n=rt_utils.prefix_name(ctrl_new) + sub_prefix + 'Bsh' + side + '_mdl')
        cmds.setAttr(mult_double_linear + '.input2', 1.0 / valueNode)
        cmds.connectAttr(controller + '.%s' % slide_atribute, mult_double_linear + '.input1')

        clamp = cmds.createNode('clamp', n=rt_utils.prefix_name(ctrl_new) + sub_prefix + 'Bsh' + side + '_clm')
        cmds.setAttr(clamp + '.maxR', clamp_max)
        cmds.setAttr(clamp + '.minR', clamp_min)

        cmds.connectAttr(mult_double_linear + '.output', clamp + '.inputR')
        # CONNECT TO BSH
        list_weight = cmds.listAttr(blendshape_name + '.w', m=True)

        # UP
        self.connect_node_to_bsh(list_weight, clamp, 'outputR', blendshape_name=blendshape_name, side_RGT=side_RGT,
                                 side_LFT=side_LFT, side=side, suffix_bsh=suffix_bsh)
        return clamp

    def connect_node_to_bsh(self, list_weight, connector_node, attribute_node, blendshape_name, side_RGT, side_LFT,
                            side, suffix_bsh):
        list = []
        for i in list_weight:
            listI = i[:-7]
            list.append(listI)

        base_name = rlu_transform.reposition_side(connector_node, side_RGT, side_LFT)
        if re.compile('|'.join(list), re.IGNORECASE).search(connector_node):  # re.IGNORECASE is used to ignore case
            cmds.connectAttr(connector_node + '.%s' % attribute_node,
                             blendshape_name + '.%s%s%s' % (rt_utils.prefix_name(base_name), side, '_' + suffix_bsh))
        else:
            print(cmds.error('There is no weight on blendshape'))


class BuildOneSide:
    def __init__(self, blendshape_node_name, mouth_ctrl, upper_lip_roll_ctrl, lower_lip_roll_ctrl, upper_lip_ctrl,
                 lower_lip_ctrl, upper_lip_ctrl_out,
                 lower_lip_ctrl_out, mouth_twist_ctrl, a_ctrl, ah_ctrl, e_ctrl, fv_ctrl, l_ctrl, mbp_ctrl, oh_ctrl,
                 ooo_ctrl, r_ctrl,
                 tkg_ctrl, th_ctrl, uh_ctrl, y_ctrl, n_ctrl):

        # TWO VALUE
        self.two_value_slider(blendshape_node_name=blendshape_node_name, controller=mouth_ctrl,
                              slide_atribute='translateY',
                              sub_prefix_one='Up', value_pos_one=2, sub_prefix_two='Down', value_pos_two=-2)
        self.two_value_slider(blendshape_node_name=blendshape_node_name, controller=mouth_ctrl,
                              slide_atribute='translateX',
                              sub_prefix_one='LFT', value_pos_one=2, sub_prefix_two='RGT', value_pos_two=-2)

        self.two_value_slider(blendshape_node_name=blendshape_node_name, controller=upper_lip_ctrl,
                              slide_atribute='translateY',
                              sub_prefix_one='Up', value_pos_one=1, sub_prefix_two='Down', value_pos_two=-1,
                              add_prefix='MID',
                              side_RGT='BshMID', side_LFT='BshMID')

        self.two_value_slider(blendshape_node_name=blendshape_node_name, controller=lower_lip_ctrl,
                              slide_atribute='translateY',
                              sub_prefix_one='Up', value_pos_one=1, sub_prefix_two='Down', value_pos_two=-1,
                              add_prefix='MID',
                              side_RGT='BshMID', side_LFT='BshMID')

        self.two_value_slider(blendshape_node_name=blendshape_node_name, controller=mouth_twist_ctrl,
                              slide_atribute='translateX',
                              sub_prefix_one='RGT', value_pos_one=2, sub_prefix_two='LFT', value_pos_two=-2)

        # ONE VALUE
        self.one_value_slider(blendshape_node_name=blendshape_node_name, controller=upper_lip_ctrl_out,
                              slide_atribute='translateY',
                              sub_prefix='', value_node=3, add_prefix='MID', side_RGT='BshMID', side_LFT='BshMID')
        self.one_value_slider(blendshape_node_name=blendshape_node_name, controller=lower_lip_ctrl_out,
                              slide_atribute='translateY',
                              sub_prefix='', value_node=3, add_prefix='MID', side_RGT='BshMID', side_LFT='BshMID')

        self.one_value_slider(blendshape_node_name=blendshape_node_name, controller=upper_lip_roll_ctrl,
                              slide_atribute='translateY',
                              sub_prefix='Up', value_node=1, add_prefix='MID',
                              side_RGT='BshMID', side_LFT='BshMID')

        self.one_value_slider(blendshape_node_name=blendshape_node_name, controller=lower_lip_roll_ctrl,
                              slide_atribute='translateY',
                              sub_prefix='Down', value_node=1, add_prefix='MID',
                              side_RGT='BshMID', side_LFT='BshMID')

        # LETTER MOUTH
        self.one_value_slider(blendshape_node_name=blendshape_node_name, controller=a_ctrl, slide_atribute='translateX',
                              sub_prefix='', value_node=4, add_prefix='',
                              )
        self.one_value_slider(blendshape_node_name=blendshape_node_name, controller=ah_ctrl,
                              slide_atribute='translateX',
                              sub_prefix='', value_node=4, add_prefix='',
                              )
        self.one_value_slider(blendshape_node_name=blendshape_node_name, controller=e_ctrl, slide_atribute='translateX',
                              sub_prefix='', value_node=4, add_prefix='',
                              )
        self.one_value_slider(blendshape_node_name=blendshape_node_name, controller=fv_ctrl,
                              slide_atribute='translateX',
                              sub_prefix='', value_node=4, add_prefix='',
                              )
        self.one_value_slider(blendshape_node_name=blendshape_node_name, controller=l_ctrl, slide_atribute='translateX',
                              sub_prefix='', value_node=4, add_prefix='',
                              )
        self.one_value_slider(blendshape_node_name=blendshape_node_name, controller=mbp_ctrl,
                              slide_atribute='translateX',
                              sub_prefix='', value_node=4, add_prefix='',
                              )
        self.one_value_slider(blendshape_node_name=blendshape_node_name, controller=oh_ctrl,
                              slide_atribute='translateX',
                              sub_prefix='', value_node=4, add_prefix='',
                              )
        self.one_value_slider(blendshape_node_name=blendshape_node_name, controller=ooo_ctrl,
                              slide_atribute='translateX',
                              sub_prefix='', value_node=4, add_prefix='',
                              )
        self.one_value_slider(blendshape_node_name=blendshape_node_name, controller=r_ctrl, slide_atribute='translateX',
                              sub_prefix='', value_node=4, add_prefix='',
                              )
        self.one_value_slider(blendshape_node_name=blendshape_node_name, controller=tkg_ctrl,
                              slide_atribute='translateX',
                              sub_prefix='', value_node=4, add_prefix='',
                              )
        self.one_value_slider(blendshape_node_name=blendshape_node_name, controller=th_ctrl,
                              slide_atribute='translateX',
                              sub_prefix='', value_node=4, add_prefix='',
                              )
        self.one_value_slider(blendshape_node_name=blendshape_node_name, controller=uh_ctrl,
                              slide_atribute='translateX',
                              sub_prefix='', value_node=4, add_prefix='',
                              )
        self.one_value_slider(blendshape_node_name=blendshape_node_name, controller=y_ctrl, slide_atribute='translateX',
                              sub_prefix='', value_node=4, add_prefix='',
                              )
        self.one_value_slider(blendshape_node_name=blendshape_node_name, controller=n_ctrl, slide_atribute='translateX',
                              sub_prefix='', value_node=4, add_prefix='',
                              )

    def two_value_slider(self, blendshape_node_name, controller, slide_atribute, sub_prefix_one, value_pos_one,
                         sub_prefix_two,
                         value_pos_two, add_prefix='', side_RGT='Bsh', side_LFT='Bsh', clamp_up_min=0.0,
                         clamp_up_max=1.0, clamp_down_min=0.0,
                         clamp_down_max=1.0):
        # UP
        ctrl_new = rlu_transform.reposition_side(controller, side_RGT, side_LFT)
        mult_double_linear_up = cmds.createNode('multDoubleLinear',
                                                n=rt_utils.prefix_name(ctrl_new) + sub_prefix_one + '_mdl')
        cmds.setAttr(mult_double_linear_up + '.input2', 1.0 / value_pos_one)
        cmds.connectAttr(controller + '.%s' % slide_atribute, mult_double_linear_up + '.input1')

        clamp_up = cmds.createNode('clamp', n=rt_utils.prefix_name(ctrl_new) + sub_prefix_one + '_clm')
        cmds.setAttr(clamp_up + '.maxR', clamp_up_max)
        cmds.setAttr(clamp_up + '.minR', clamp_up_min)

        cmds.connectAttr(mult_double_linear_up + '.output', clamp_up + '.inputR')

        # DOWN
        mult_double_linear_down = cmds.createNode('multDoubleLinear',
                                                  n=rt_utils.prefix_name(ctrl_new) + sub_prefix_two + '_mdl')
        cmds.setAttr(mult_double_linear_down + '.input2', 1.0 / value_pos_two)
        cmds.connectAttr(controller + '.%s' % slide_atribute, mult_double_linear_down + '.input1')

        clamp_down = cmds.createNode('clamp', n=rt_utils.prefix_name(ctrl_new) + sub_prefix_two + '_clm')
        cmds.setAttr(clamp_down + '.maxR', clamp_down_max)
        cmds.setAttr(clamp_down + '.minR', clamp_down_min)

        cmds.connectAttr(mult_double_linear_down + '.output', clamp_down + '.inputR')

        # CONNECT TO BSH
        list_weight = cmds.listAttr(blendshape_node_name + '.w', m=True)
        # UP
        self.connect_node_to_bsh(list_weight, clamp_up, 'outputR', blendshape_node_name, add_prefix, side_RGT=side_RGT,
                                 side_LFT=side_LFT)
        self.connect_node_to_bsh(list_weight, clamp_down, 'outputR', blendshape_node_name, add_prefix,
                                 side_RGT=side_RGT, side_LFT=side_LFT)

        return clamp_up, clamp_down

    def one_value_slider(self, blendshape_node_name, controller, slide_atribute, sub_prefix, value_node, add_prefix,
                         side_RGT='Bsh', side_LFT='Bsh',
                         clamp_max=1.0, clamp_min=0.0,
                         ):
        ctrl_new = rlu_transform.reposition_side(controller, side_RGT, side_LFT)
        mult_double_linear = cmds.createNode('multDoubleLinear',
                                             n=rt_utils.prefix_name(ctrl_new) + sub_prefix + '_mdl')
        cmds.setAttr(mult_double_linear + '.input2', 1.0 / value_node)
        cmds.connectAttr(controller + '.%s' % slide_atribute, mult_double_linear + '.input1')

        clamp = cmds.createNode('clamp', n=rt_utils.prefix_name(ctrl_new) + sub_prefix + '_clm')
        cmds.setAttr(clamp + '.maxR', clamp_max)
        cmds.setAttr(clamp + '.minR', clamp_min)

        cmds.connectAttr(mult_double_linear + '.output', clamp + '.inputR')

        # CONNECT TO BSH
        list_weight = cmds.listAttr(blendshape_node_name + '.w', m=True)

        # UP
        self.connect_node_to_bsh(list_weight, clamp, 'outputR', blendshape_node_name, add_prefix, side_RGT=side_RGT,
                                 side_LFT=side_LFT)

    def connect_node_to_bsh(self, list_weight, connector_node, attribute_node, blendshape_node_name, add_prefix,
                            side_RGT, side_LFT):
        list = []
        for i in list_weight:
            listI = i[:-7]
            list.append(listI)

        base_name = rlu_transform.reposition_side(connector_node, side_RGT, side_LFT)
        if re.compile('|'.join(list), re.IGNORECASE).search(
                connector_node):  # re.IGNORECASE is used to ignore case
            cmds.connectAttr(connector_node + '.%s' % attribute_node,
                             blendshape_node_name + '.%s%s%s' % (rt_utils.prefix_name(base_name), add_prefix, '_ply'))
        else:
            print(cmds.error('There is no weight on blendshape'))


class BuildFree:
    def __init__(self, bsnName, rollCtrl, upperWeightBsnMID,
                 upperWeightBsnLFT, upperWeightBsnRGT,
                 lowerWeightBsnMID, lowerWeightBsnLFT,
                 lowerWeightBsnRGT):

        self.one_value_slider(bsnName, controller=rollCtrl, slide_atribute='translateY',
                              value_node=3, weight_blendshape_name=upperWeightBsnMID)

        self.one_value_slider(bsnName, controller=rollCtrl, slide_atribute='translateY',
                              value_node=3, weight_blendshape_name=upperWeightBsnLFT)

        self.one_value_slider(bsnName, controller=rollCtrl, slide_atribute='translateY',
                              value_node=3, weight_blendshape_name=upperWeightBsnRGT)

        self.one_value_slider(bsnName, controller=rollCtrl, slide_atribute='translateY',
                              value_node=3, weight_blendshape_name=lowerWeightBsnMID)

        self.one_value_slider(bsnName, controller=rollCtrl, slide_atribute='translateY',
                              value_node=3, weight_blendshape_name=lowerWeightBsnLFT)

        self.one_value_slider(bsnName, controller=rollCtrl, slide_atribute='translateY',
                              value_node=3, weight_blendshape_name=lowerWeightBsnRGT)

    def two_value_slider(self, blendshape_node_name, controller, slide_atribute, sub_prefix_one, value_pos_one,
                         sub_prefix_two,
                         value_pos_two, weight_blendshape_name,
                         connect=True):
        # UP
        # ctrlNew = self.replacePosLFTRGT(weightBsnName, sideRGT=sideRGT, sideLFT=sideLFT)
        weight_names = rt_utils.prefix_name(weight_blendshape_name)
        weight_name = weight_names.replace(sub_prefix_one, '').replace(sub_prefix_two, '')

        mult_double_linear_up = cmds.createNode('multDoubleLinear',
                                                n=weight_name[:-3] + sub_prefix_one + weight_name[-3:] + '_mdl')
        cmds.setAttr(mult_double_linear_up + '.input2', 1.0 / value_pos_one)
        cmds.connectAttr(controller + '.%s' % slide_atribute, mult_double_linear_up + '.input1')

        clamp_up = cmds.createNode('clamp', n=weight_name[:-3] + sub_prefix_one + weight_name[-3:] + '_clm')
        cmds.setAttr(clamp_up + '.maxR', 1)
        cmds.connectAttr(mult_double_linear_up + '.output', clamp_up + '.inputR')

        # DOWN
        mult_double_linear_down = cmds.createNode('multDoubleLinear',
                                                  n=weight_name[:-3] + sub_prefix_two + weight_name[-3:] + '_mdl')
        cmds.setAttr(mult_double_linear_down + '.input2', 1.0 / value_pos_two)
        cmds.connectAttr(controller + '.%s' % slide_atribute, mult_double_linear_down + '.input1')

        clamp_down = cmds.createNode('clamp', n=weight_name[:-3] + sub_prefix_two + weight_name[-3:] + '_clm')
        cmds.setAttr(clamp_down + '.maxR', 1)
        cmds.connectAttr(mult_double_linear_down + '.output', clamp_down + '.inputR')

        # CONNECT TO BSH
        if connect:
            list_weight = cmds.listAttr(blendshape_node_name + '.w', m=True)
            self.connect_node_to_bsh(list_weight, clamp_up, 'outputR', blendshape_node_name=blendshape_node_name)
            self.connect_node_to_bsh(list_weight, clamp_down, 'outputR', blendshape_node_name=blendshape_node_name)
        return clamp_up, clamp_down

    def one_value_slider(self, blendshape_node_name, controller, slide_atribute, value_node, weight_blendshape_name):
        weight_name = rt_utils.prefix_name(weight_blendshape_name)
        mult_double_linear_up = cmds.createNode('multDoubleLinear',
                                                n=weight_name[:-3] + weight_name[-3:] + '_mdl')
        cmds.setAttr(mult_double_linear_up + '.input2', 1.0 / value_node)
        cmds.connectAttr(controller + '.%s' % slide_atribute, mult_double_linear_up + '.input1')

        # CONNECT TO BSH
        list_weight = cmds.listAttr(blendshape_node_name + '.w', m=True)

        # UP
        self.connect_node_to_bsh(list_weight, mult_double_linear_up, 'output',
                                 blendshape_node_name=blendshape_node_name)

    def connect_node_to_bsh(self, list_weight, connector_node, attribute_node, blendshape_node_name):
        list = []
        for i in list_weight:
            listI = i[:-7]
            list.append(listI)

        # baseName = self.replacePosLFTRGT(connectorNode, sideRGT=sideRGT, sideLFT=sideLFT)
        if re.compile('|'.join(list), re.IGNORECASE).search(connector_node):  # re.IGNORECASE is used to ignore case
            cmds.connectAttr(connector_node + '.%s' % attribute_node,
                             blendshape_node_name + '.%s%s' % (rt_utils.prefix_name(connector_node), '_ply'))
        else:
            print(cmds.error('There is no weight on blendshape'))
