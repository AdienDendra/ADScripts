
def squashStretch():
    ## ------------------ CTY squash stretch head
    ## select group hair( or anything on head )
    ## make sure pivot group it's same head ctrl
    from nnTools import weTools as we
    reload( we )

    we.headSS()

def weapon():
    ## ----------------- CTY
    ## weapon base
    ## selet weapon group and make sure it's transfrom 0
    from tool.rig.nnTools import nnTools as nn
    reload(nn)
    nn.weaponRig(cha='movie')

def fileTextureManager():
    files = mc.ls('*_file')

    searchFor = 'P:/Library/rigging/miniFig/_texture/miniFigStdM/4K'
    pastesFor = 'P:/CMD_TS4/asset/3D/character/character/TS4_trex/textures/4K'

    for i in files:
        set = mc.getAttr('%s.fileTextureName' % i).replace(searchFor, pastesFor)
        mc.setAttr('%s.fileTextureName' % i, set, type='string')

def repathTexture():

    ## ------------------ Repath All Texture
    ## file must be in asset folder
    from nnTools import weTools as we
    reload(we)

    we.repathTextures()