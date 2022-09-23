"""
remove the suffix name and take the prefix name
"""
from __future__ import absolute_import

from importlib import reload

from rigging.tools import utils as rt_utils

reload(rt_utils)


def remove_suffix(obj):
    return rt_utils.prefix_name(obj)
