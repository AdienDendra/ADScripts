from __future__ import absolute_import

import maya.cmds as cmds


class Parts():

    def __init__(self):
        pass


class Spine():

    def __init__(self, prefix):
        self.parent_elem = None
        self.name = prefix + "_spine"
        self.part = Parts()

    def rename(self, name):
        self.name = name + "_spine"

    def parent(self, parent):
        self.parent_elem = parent


class Arm(object):

    def __init__(self, prefix, suffix):
        self.parent_elem = None
        self.suffix = suffix
        self.name = prefix + "_arm_" + self.suffix
        self.part = Parts()

    def rename(self, name):
        self.name = name + "_arm_" + self.suffix

    def parent(self, parent):
        self.parent_elem = parent
        cmds.parent(self.name, parent)


# class Arm_l():
#
#     def __init__(self):
#         self.arm = Arm('Left')

class BipedBuild():

    def __init__(self, prefix, left_name='LFT', right_name='RGT'):
        self.arm_left = Arm(prefix, left_name)
        self.arm_right = Arm(prefix, right_name)

        self.arm_right.parent('eeeeeee')
        self.arm_left.parent('ffffff')

    def rename(self, name):
        self.arm_left.rename(name)
        self.arm_right.rename(name)


build = BipedBuild(prefix='myBiped')
print(build.arm_left.name)
print(build.arm_right.name)

build.rename('Adien')
print(build.arm_left.name)
print(build.arm_right.name)
