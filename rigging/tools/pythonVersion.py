import sys
from string import digits

# query the version
python_version = sys.version_info.major


def translation_string(prefix):
    if python_version == 2:
        prefix_without_number = str(prefix).translate(None, digits)
    else:
        prefix_without_number = str.maketrans('', '', digits)
        prefix_without_number = prefix.translate(prefix_without_number)

    return prefix_without_number
