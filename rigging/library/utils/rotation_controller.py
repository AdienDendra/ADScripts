import maya.cmds as mc


def change_position(shape, destination):
    points = mc.ls('%s.cv[0:*]' % shape, fl=True)

    for i in points:
        xforms = mc.xform(i, q=1, os=1, t=1)
        forms_x = xforms[0]
        forms_y = xforms[1]
        forms_z = xforms[2]
        rev_forms_x = xforms[0] * -1
        rev_forms_y = xforms[1] * -1
        rev_forms_z = xforms[2] * -1

        if destination == '-':
            move = mc.setAttr(i + '.xValue', rev_forms_x)
            move = mc.setAttr(i + '.yValue', rev_forms_y)
            move = mc.setAttr(i + '.zValue', rev_forms_z)

        elif destination == 'xy' or destination == 'yx':
            move = mc.setAttr(i + '.xValue', forms_y)
            move = mc.setAttr(i + '.yValue', forms_x)
            move = mc.setAttr(i + '.zValue', forms_z)

        elif destination == 'xz' or destination == 'zx':
            move = mc.setAttr(i + '.xValue', forms_z)
            move = mc.setAttr(i + '.yValue', forms_y)
            move = mc.setAttr(i + '.zValue', forms_x)

        elif destination == 'yz' or destination == 'zy':
            move = mc.setAttr(i + '.xValue', forms_x)
            move = mc.setAttr(i + '.yValue', forms_z)
            move = mc.setAttr(i + '.zValue', forms_y)

        else:
            mc.error('please check your dest parameter name!')
