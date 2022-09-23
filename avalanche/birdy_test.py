"""
You are free to change this script howevery you want.
But this should give you enough of a starting point to not struggle with syntax too much.

The only rule is that you have to use the same Matrix as in the put_on_party_hat function.
"""
import pymel.core as pm


def fix_present():
    present = pm.PyNode("BirthdayPresent")
    for vtx in present.getShape().vtx:
        # print vtx
        position_os = pm.xform(vtx, q=True, os=True, t=True)
        position_ws = pm.xform(vtx, q=True, ws=True, t=True)
        vector_os = pm.dt.Vector(position_os[0], position_os[1], position_os[2])

        vector_ws = pm.dt.Vector(position_ws[0], position_ws[1], position_ws[2])
        vector_position = vector_ws - vector_os
        vector_optimum = vector_os * 2

        move_x = (vector_optimum[0] * pm.dt.sqrt(1.0 - (vector_optimum[1] * vector_optimum[1] / 2.0) -
                                                 (vector_optimum[2] * vector_optimum[2] / 2.0) +
                                                 (vector_optimum[1] * vector_optimum[1] * vector_optimum[2] *
                                                  vector_optimum[2] / 3.0)))

        move_y = (vector_optimum[1] * pm.dt.sqrt(1.0 - (vector_optimum[2] * vector_optimum[2] / 2.0) -
                                                 (vector_optimum[0] * vector_optimum[0] / 2.0) +
                                                 (vector_optimum[2] * vector_optimum[2] * vector_optimum[0] *
                                                  vector_optimum[0] / 3.0)))

        move_z = (vector_optimum[2] * pm.dt.sqrt(1.0 - (vector_optimum[0] * vector_optimum[0] / 2.0) -
                                                 (vector_optimum[1] * vector_optimum[1] / 2.0) +
                                                 (vector_optimum[0] * vector_optimum[0] * vector_optimum[1] *
                                                  vector_optimum[1] / 3.0)))

        pm.move(move_x + (vector_position[0]), move_y + (vector_position[1]), move_z + (vector_position[2]), vtx)


def look_at_gift():
    bird = pm.PyNode("Birdy")
    mtx = pm.xform(bird, q=True, ws=True, m=True)

    # 90 degree Y axis rotation
    y_rot = pm.dt.Matrix([0.0, 0.0, -1.0, 0.0,
                          0.0, 1.0, 0.0, 0.0,
                          1.0, 0.0, 0.0, 0.0,
                          0.0, 0.0, 0.0, 1.0])

    yz_matrix = pm.dt.Matrix(mtx) * y_rot
    pm.xform('Birdy', ws=True, m=yz_matrix)


def put_on_party_hat():
    hat = pm.PyNode("PartyHat")
    # birdy = pm.PyNode('Birdy')
    birdy_likes_his_hat_here = pm.dt.Matrix([
        [0.99, -0.13, 0.022, 0.0],
        [0.13, 0.97, -0.16, 0.0],
        [0, 0.167, 0.985, 0.0],
        [12.13, 83.57, -15.185, 1.0],
    ])
    hat_spot = pm.PyNode('hat_spot')
    hat_spot_mtx = pm.dt.Matrix(pm.xform(hat_spot, ws=True, q=True, m=True))

    # query matrix value
    hatspot_x = hat_spot_mtx.__getitem__(0)
    hatspot_y = hat_spot_mtx.__getitem__(1)
    hatspot_z = hat_spot_mtx.__getitem__(2)
    hatspot_position = hat_spot_mtx.__getitem__(3)

    # replacing matrix value
    birdy_likes_his_hat_here.__setitem__(0, hatspot_x)
    birdy_likes_his_hat_here.__setitem__(1, hatspot_y)
    birdy_likes_his_hat_here.__setitem__(2, hatspot_z)
    birdy_likes_his_hat_here.__setitem__(3, hatspot_position)

    # set the hat position
    pm.xform(hat, ws=True, m=birdy_likes_his_hat_here)
