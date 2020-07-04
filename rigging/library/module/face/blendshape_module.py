from __builtin__ import reload

from rigging.library.base.face import blendshape as bsh
from rigging.tools import AD_utils as au

reload(bsh)
reload(au)


def blendshape(bsnName, mouthCtrl, suffixBsh, prefixSquashStretch, prefixRollLow, prefixRollUp, controllerUpRollBshAttr,
               controllerLowRollBshAttr, squashStretchAttr, cheekOutAttrLFT, cheekOutAttrRGT, prefixCheekOut, sideLFT, sideRGT):

        center = bsh.BuildTwoSide(bsnName=bsnName, mouthCtrl=mouthCtrl, prefixSquashStretch=prefixSquashStretch,
                                  prefixRollLow=prefixRollLow, prefixRollUp=prefixRollUp, suffixBsh=suffixBsh,
                                  controllerUpRollBshAttr=controllerUpRollBshAttr, controllerLowRollBshAttr=controllerLowRollBshAttr,
                                  squashStretchAttr=squashStretchAttr, cheekOutAttrLFT=cheekOutAttrLFT, cheekOutAttrRGT=cheekOutAttrRGT,
                                  sideLFT=sideLFT, sideRGT=sideRGT, prefixCheekOut=prefixCheekOut,
                                  )


    # independent = bsh.BuildFree(bsnName='face_bsn', rollCtrl='rollLipBsh_ctrl',
    #                             upperWeightBsnMID='upperLipRollHalfDownMID_ply',
    #                             upperWeightBsnLFT='upperLipRollHalfDownLFT_ply',
    #                             upperWeightBsnRGT='upperLipRollHalfDownRGT_ply',
    #                             lowerWeightBsnMID='lowerLipRollHalfUpMID_ply',
    #                             lowerWeightBsnLFT='lowerLipRollHalfUpLFT_ply',
    #                             lowerWeightBsnRGT='lowerLipRollHalfUpRGT_ply', )