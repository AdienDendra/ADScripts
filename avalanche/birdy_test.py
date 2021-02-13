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
    gift = pm.pyNode('BirthdayPresent')
    bird_pos = bird.getTranslation(worldSpace=1)
    # bird_rot = bird.getRotation(worldSpace=1)
    # pm.move(bird_rot.x, bird_rot.y, bird_rot.z, bird)
    # [0.7797672568842143, -0.4750407758702958, 0.4077980950811512, 0.0,
    #  0.4364356809126459, 0.8216065262485838, 0.12255659989689752, 0.0,
    #  -0.3932689586134617, 0.08241201558696216, 0.84798661168925, 0.0,
    #  0.0, 178.67416191492592, 0.0, 1.0]
    #
    # print matrix
    print bird_pos

def put_on_party_hat():
    hat = pm.PyNode("PartyHat")
    birdy_likes_his_hat_here = pm.dt.Matrix([
        [0.99, -0.13, 0.022, 0.0],
        [0.13, 0.97, -0.16, 0.0],
        [0, 0.167, 0.985, 0.0],
        [12.13, 83.57, -15.185, 1.0],
    ])
    print pm.dt.Vector(birdy_likes_his_hat_here).get()

    # print pm.xform(birdy_likes_his_hat_here, q=True, m=True, t=True)
    postion_hat = pm.xform(hat, ws=True, q=True, t=True)
    print postion_hat

    x =  birdy_likes_his_hat_here + postion_hat
    # print x

    # pm.xform(hat, ws=True, m=x)



# fix_present()
# look_at_gift()
# put_on_party_hat()