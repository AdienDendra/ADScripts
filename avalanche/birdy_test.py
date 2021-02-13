"""
You are free to change this script howevery you want.
But this should give you enough of a starting point to not struggle with syntax too much.

The only rule is that you have to use the same Matrix as in the put_on_party_hat function.
"""

import pymel.core as pm
import math

def fix_present():
    present = pm.PyNode("BirthdayPresent")
    for vtx in present.getShape().vtx:
        position = pm.xform(vtx, q=True, os=True, t=True)
        position_ws = pm.xform(vtx, q=True, ws=True, t=True)
        print position
        # print position_ws

        # start_point = pm.dt.Point(position)
        start_vector = pm.dt.Vector(position[0], position[1], position[2])
        start_vector_ws = pm.dt.Vector(position_ws[0], position_ws[1], position_ws[2])
        subtract_vec = start_vector_ws - start_vector
        # print pos

        # print start_vector
        # result =(1.0 - (start_vector[1] * start_vector[1] / 2.0) - (start_vector[2] * start_vector[2] / 2.0) + (start_vector[1] * start_vector[1] * start_vector[2] * start_vector[2] / 3.0))
        move_x = start_vector[0] * pm.dt.sqrt(1.0 - (start_vector[1] * start_vector[1] / 2.0) - (start_vector[2] * start_vector[2] / 2.0) +
                                        (start_vector[1] * start_vector[1] * start_vector[2] * start_vector[2] / 3.0))
        move_y =  start_vector[1] * pm.dt.sqrt(1.0 - (start_vector[2] * start_vector[2] / 2.0) - (start_vector[0] * start_vector[0] / 2.0) +
                                          (start_vector[2] * start_vector[2] * start_vector[0] * start_vector[0] / 3.0))
        move_z = start_vector[2] * pm.dt.sqrt(1.0 - (start_vector[0] * start_vector[0] / 2.0) - (start_vector[1] * start_vector[1] / 2.0) +
                                         (start_vector[0] * start_vector[0] * start_vector[1] * start_vector[1] / 3.0))

        # move_x = start_vector[0] * pm.dt.sqrt(1.0 - (start_vector[1] * start_vector[1] / 2.0) - (start_vector[2] * start_vector[2] / 2.0) +
        #                                 (start_vector[1] * start_vector[1] * start_vector[2] * start_vector[2] / 3.0))
        # move_y =  start_vector[1] * pm.dt.sqrt(1.0 - (start_vector[2] * start_vector[2] / 2.0) - (move_x * move_x / 2.0) +
        #                                   (start_vector[2] * start_vector[2] * move_x * move_x / 3.0))
        # move_z = start_vector[2] * pm.dt.sqrt(1.0 - (move_x * move_x / 2.0) - (move_y * move_y / 2.0) +
        #                                  (move_x * move_x * move_y * move_y / 3.0))

        # x_position = position_ws[0] - move_x
        # y_position = position_ws[1] - move_y
        # z_position = position_ws[2] - move_z

        # x_position = position_ws[0] + move_x
        # y_position = position_ws[1] + move_y
        # z_position = position_ws[2] + move_z
        #
        # x_position = (pos[0] + move_x) +x_position
        # y_position = (pos[0] + move_y) +y_position
        # z_position = (pos[0] + move_z) + z_position

        #
        # pos_x = move_x + x_position
        # pos_y = move_x + y_position
        # pos_z = move_x + y_position

        # start_vector[0] *
        # print result
        # print move_x
        # print move_y
        # print move_z
        # pm.move(move_x+position_ws[0], move_y+position_ws[1], move_z+position_ws[2], vtx)
        # pm.move(move_x+position_ws[0], move_y+position_ws[1], move_z+position_ws[2], vtx)
        # pm.move(move_x, move_y, move_z, vtx)

        #
        # pm.move(move_x-pos[0], move_y-pos[1], move_z-pos[2], vtx)
        # pm.move(x_position, y_position, z_position, vtx)

        pm.move(move_x + subtract_vec[0], move_y + subtract_vec[1], move_z + subtract_vec[2], vtx)


        # print start_point

        # print vtx
        # pass

def look_at_gift():
    bird = pm.PyNode("Birdy")
    # gift = pm.pyNode('BirthdayPresent')
    bird_pos = bird.getTranslation(worldSpace=1)

    matrix = pm.dt.Matrix(pm.xform(bird, ws=True, q=True, m=True))
    revere_matrix = matrix.inverse()

    pm.xform(bird, ws=True, m=revere_matrix)

    # bird_rot = bird.getRotation(worldSpace=1)
    # print bird_rot
    # print bird_rot.x*-1

    # pm.setAttr(bird+'.rotate', (bird_rot.x*-1), (bird_rot.y*-2), (bird_rot.z*1), type='double3')

    # print matrix

def put_on_party_hat():
    hat = pm.PyNode("PartyHat")
    birdy = pm.PyNode('Birdy')
    birdy_likes_his_hat_here = pm.dt.Matrix([
        [0.99, -0.13, 0.022, 0.0],
        [0.13, 0.97, -0.16, 0.0],
        [0, 0.167, 0.985, 0.0],
        [12.13, 83.57, -15.185, 1.0],
    ])
    birdy_matrix =  pm.dt.Matrix(pm.xform(birdy, ws=True, q=True, m=True))
    birdy_position = birdy_matrix.__getitem__(3)
    target_hat_position =  birdy_likes_his_hat_here.__getitem__(3)
    adding_birdy_pos_and_target_position = birdy_position + target_hat_position

    # insert the adding value into the position
    birdy_likes_his_hat_here.__setitem__(3, adding_birdy_pos_and_target_position)
    # set the hat position
    pm.xform(hat, ws=True, m=birdy_likes_his_hat_here)



# fix_present()
# look_at_gift()
# put_on_party_hat()