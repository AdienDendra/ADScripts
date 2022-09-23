from __future__ import absolute_import

from rigging.tools import utils as rt_utils


def dic_list(obj_duplicate='', value_prefix='', suffix='', selection=False):
    dic = {}
    index = []
    list_name = rt_utils.obj_duplicate_then_rename(obj_duplicate=obj_duplicate, value_prefix=value_prefix,
                                                   suffix=suffix,
                                                   selection=selection)
    for i, value_name in enumerate(list_name[1]):
        enum = [value_name, i]
        index.append(enum)

    for i in index:
        keys = i[0]
        value = i[1]
        dic[keys] = value
    return dic


def list_skeleton_dic(obj_duplicate='', value_prefix='', key_prefix='', suffix='', selection=False, **kwargs):
    dic = {}
    list_name = rt_utils.obj_duplicate_then_rename(obj_duplicate=obj_duplicate, value_prefix=value_prefix,
                                                   key_prefix=key_prefix,
                                                   suffix=suffix, selection=selection, kwargs=kwargs)
    list_keys = list_name[0]
    list_value = list_name[1]

    append_list = []
    for list_keys, list_value in zip(list_keys, list_value):
        allList = [list_keys, list_value]
        append_list.append(allList)

    for i in append_list:
        list_keys = i[0]
        list_value = i[1]
        dic[list_keys] = list_value
    return dic
