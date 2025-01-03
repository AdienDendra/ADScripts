import os

import maya.cmds as cmds

sub_dir_list = ['assets', 'data', 'publish', 'scene']


# scene_dir_list = ['anim', 'bsh', 'build', 'csp', 'ctrl', 'master']


def create_dir(root_path, sub_dir_list):
    result = {}
    for o in sub_dir_list:
        new_path = os.path.join(root_path, o)
        result[o] = new_path
        os.mkdir(new_path)

    return result


def create_character_dir(root_path, new_dir_name):
    new_path = os.path.join(root_path, new_dir_name)
    if not os.path.exists(new_path):
        os.mkdir(new_path)
    else:
        return cmds.error("The directory %s already exist. Please change another name" % new_dir_name)

    res_dir = create_dir(new_path, sub_dir_list)
    # create_dir(res_dir.get('scene'), scene_dir_list)


def create_directories(project_name='name', biped=True):
    # change to character biped directory
    if biped:
        os.chdir('E:/Project/character/biped')
        get_path = os.getcwd()
    else:
        os.chdir('E:/Project/character/quadruped')
        get_path = os.getcwd()

    if not os.path.isdir(project_name):
        os.mkdir(project_name)
    else:
        cmds.error("The directory %s already exist. Please change another name" % project_name)

    path_name = os.path.join(get_path, project_name)

    # create all folder directories inside of name folder
    for folder in sub_dir_list:
        os.mkdir(os.path.join(path_name, folder))

    # # make scene folder inside of name object
    # os.mkdir(os.path.join(path_name, 'scene'))

    # # change to the scene directory
    # os.chdir('E:/Project/character/biped/%s/scene' % name)

    # get_path_scene = os.getcwd()

    # # create all folder directoriesScene inside of scene folder
    # for folder in scene_dir_list:
    #     os.mkdir(os.path.join(get_path_scene, folder))
