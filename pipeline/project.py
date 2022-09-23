"""
main project path

"""
import pymel.core as pm

sceneScale = 1.0


def character_name(project_path):
    char_name_array = project_path.split('/')
    character_name = char_name_array[-1]
    return character_name


def path_base(project_path):
    char_name_array = project_path.split('/')
    base_path = '/'.join(char_name_array[:-2])
    return base_path


def query_character_name():
    query_file_path = pm.sceneName()
    char_name_array = query_file_path.split('/')[-1]
    split_name = char_name_array.split('_')[0]
    print(split_name)
    return split_name


def query_project_name():
    query_file_path = pm.sceneName()
    char_name_array = query_file_path.split('/')
    join_path = '/'.join(char_name_array[0:5])
    print(join_path)
    return join_path


def query_project_path():
    query_file_path = pm.sceneName()
    char_name_array = query_file_path.split('/')
    join_path = '/'.join(char_name_array[0:4])
    print(join_path)
    return join_path
