"""
remove the suffix name and take the prefix name
"""
from __builtin__ import reload

from rigging.tools import AD_utils as ut

reload (ut)

def remove_suffix(obj):
    return ut.prefix_name(obj)
