"""
base setup
main module

"""

import maya.cmds as cmds

from pipeline import project

model_path = '%s/assets/%s.ma'
builder_biped_path = '%s/builder/bipedTmp_jnt.ma'
builder_quadruped_path = '%s/builder/quadrupedTmp_jnt.ma'

# skin_jnt_path      = '%s/builder/skinBiped_skin.ma'
# ctrl_path_hero     = '%s/release/%s_ctrl.ma'
# def_scene         = '%s/hero/%s_def.ma'

project_path = 'E:/Project/character'


# import def file
def import_builder_file(character_mesh_name, project_name, biped=True):
    """
    main function to instance controller base
    """
    # new scene
    cmds.file(new=True, f=True)

    # query character name of the path

    if biped:
        # import builder jnt
        builder_file = builder_biped_path % (project_path)
        model_file = model_path % ((project_path + '/biped/%s' % project_name), character_mesh_name)
    else:
        builder_file = builder_biped_path % (builder_quadruped_path)
        model_file = model_path % ((project_path + '/quadruped/%s' % project_name), character_mesh_name)

    cmds.file(builder_file, i=1)
    cmds.file(model_file, i=1)


def csp_file(projectPath):
    """
    main function to build control, skin, poly base

    """
    # # new scene
    # mc.file(new = True, f=True)
    #
    # # reference ctrl
    # ctrl_path = ctrl_path_hero % (projectPath, pr.character_name(projectPath))
    #
    # mc.file (ctrl_path, r=1, ns='%s_ctrl' % pr.character_name(projectPath))

    # # import skin jnt
    # skin_path = skin_jnt_path % (pr.path_base(projectPath))
    # mc.file(skin_path, i = 1)

    # import model
    model_file = model_path % (projectPath, project.character_name(projectPath))
    cmds.file(model_file, i=1)

    # # parent joint to Skin grp Base
    # mc.parent('rootSkin_jnt', baseRig.skinGrp)
    #
    # # parent reference ctrl to Anim grp Base
    # ctrl_name = '%s_ctrl:partAnim_grp' % (pr.character_name(projectPath))
    # mc.parent(ctrl_name, baseRig.partGrp)


def ref_model():
    # reference model
    model_file = model_path % (project.query_project_name(), project.query_character_name())
    cmds.file(model_file, r=1, ns='%s_ply' % project.query_character_name())
