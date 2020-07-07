from rigging.library.base.face import blendshape as bsh
from rigging.tools import AD_utils as au

reload(bsh)
reload(au)


def blendshape(blendshape_node_name, mouth_ctrl, blendshape_suffix, squash_stretch_prefix, roll_low_prefix, roll_up_prefix, controller_roll_up_bsh_attr,
               controller_roll_low_bsh_attr, squash_stretch_attr, cheek_out_attr_LFT, cheek_out_attr_RGT, cheek_out_prefix, side_LFT, side_RGT):

        center = bsh.BuildTwoSide(blendshape_node_name=blendshape_node_name, mouth_ctrl=mouth_ctrl, squash_stretch_prefix=squash_stretch_prefix,
                                  roll_low_prefix=roll_low_prefix, roll_up_prefix=roll_up_prefix, blendshape_suffix=blendshape_suffix,
                                  controller_roll_up_bsh_attr=controller_roll_up_bsh_attr, controller_roll_low_bsh_attr=controller_roll_low_bsh_attr,
                                  squash_stretch_attr=squash_stretch_attr, cheek_out_attr_LFT=cheek_out_attr_LFT, cheek_out_attr_RGT=cheek_out_attr_RGT,
                                  side_LFT=side_LFT, side_RGT=side_RGT, cheek_out_prefix=cheek_out_prefix,
                                  )