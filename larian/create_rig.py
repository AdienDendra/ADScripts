import pymel.core as pm
import maya.cmds as mc
import maya.OpenMaya as om

class Rig():
    def __init__(self, head, tail, prefix, split):
        self.joint_bind(head, tail, prefix, split)
        self.joint_spline_Ik(head, tail, prefix, split)

    def joint_bind(self, head, tail, prefix, split):
        self.split_joint(obj_base=head, obj_tip=tail, prefix=prefix, suffix='bind', split=split)

    def joint_spline_Ik(self, head, tail, prefix, split):
        list_joint = self.split_joint(obj_base=head, obj_tip=tail, prefix=prefix, suffix='jnt', split=split)
        for i in range(len(list_joint)):
            if i > 0:
                mc.parent(list_joint[i], list_joint[i - 1])

    def split_joint(self, obj_base, obj_tip, prefix, suffix, split=1, base_tip=False):
        base_xform = mc.xform(obj_base, q=1, ws=1, t=1)
        tip_xform = mc.xform(obj_tip, q=1, ws=1, t=1)

        base_vector = om.MVector(base_xform[0], base_xform[1], base_xform[2])
        tip_vector = om.MVector(tip_xform[0], tip_xform[1], tip_xform[2])

        split_vector = (tip_vector - base_vector)
        segment_vector = (split_vector / (split + 1.0))

        segment_location = (base_vector + segment_vector)

        list = []
        new_list = []
        for i in range(0, split):
            segment = mc.duplicate(obj_base)
            new_name = mc.rename(segment, str('%s%01d_%s' % (prefix, (i + 1), 'ref')))
            list.append(new_name)
            mc.move(segment_location.x, segment_location.y, segment_location.z, new_name)
            segment_location = segment_location + segment_vector
        if base_tip:
            base = mc.duplicate(obj_base)
            tip = mc.duplicate(obj_tip)
            list.insert(0, base[0])
            list.insert(split + 1, tip[0])
            for i in list:
                new_name = mc.rename(i, '%s%s_%s' % (prefix, str(list.index(i) + 1).zfill(2), suffix))
                new_list.append(new_name)
        else:
            for i in list:
                new_name = mc.rename(i, '%s%s_%s' % (prefix, str(list.index(i) + 1).zfill(2), suffix))
                new_list.append(new_name)

        return new_list