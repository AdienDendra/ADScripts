"""
You are free to change this script howevery you want.
But this should give you enough of a starting point to not struggle with syntax too much.

The only rule is that you have to use the same Matrix as in the put_on_party_hat function.
"""

import pymel.core as pm

def fix_present():
    present = pm.PyNode("BirthdayPresent")
    for vtx in present.getShape().vtx:
        # pos = pm.xform(vtx, q=True, ws=True, t=True)
        # print pos
        # start_vector = pm.dt.Vector(3, pos[0], pos[1], pos[2])
        # print start_vector

        # hatspot_position = pm.dt.Matrix(pos).__getitem__(3)
        # print hatspot_position
        # set_item =[0,0,0,1]
        # pm.dt.Matrix(pos).__setitem__(3, set_item)
        # #
        # print pos
        #
        # pm.xform(vtx, ws=True, m=sphere)

        position = pm.xform(vtx, q=True, os=True, t=True)
        position_ws = pm.xform(vtx, q=True, ws=True, t=True)
        # print position
        # print position_ws

        # start_point = pm.dt.Point(position)
        start_vector = pm.dt.Vector(position[0], position[1], position[2])
        # print start_vector[1]

        start_vector_ws = pm.dt.Vector(position_ws[0], position_ws[1], position_ws[2])
        subtract_vec = start_vector_ws - start_vector
        # print start_vector_ws
        # vectorize = pm.dt.Vector(position[0], position[1], subtract_vec[2])
        # print subtract_vec
        # print pos

        # print start_vector
        result =(1.0 - (start_vector[1] * start_vector[1] / 2.0) - (start_vector[2] * start_vector[2] / 2.0) + (start_vector[1] * start_vector[1] * start_vector[2] * start_vector[2] / 3.0))

        move_x = start_vector[0] * pm.dt.sqrt(1.0 - (start_vector[1] * start_vector[1] / 2.0) - (start_vector[2] * start_vector[2] / 2.0) +
                                        (start_vector[1] * start_vector[1] * start_vector[2] * start_vector[2] / 3.0))
        # print move_x
        move_y =  start_vector[1]  * pm.dt.sqrt(1.0 - (start_vector[2] * start_vector[2] / 2.0) - (start_vector[0] * start_vector[0] / 2.0) +
                                          (start_vector[2] * start_vector[2] * start_vector[0] * start_vector[0] / 3.0))
        print move_y
        move_z = start_vector[2] * pm.dt.sqrt(1.0 - (start_vector[0] * start_vector[0] / 2.0) - (start_vector[1] * start_vector[1] / 2.0) +
                                         (start_vector[0] * start_vector[0] * start_vector[1] * start_vector[1] / 3.0))

        # move_x = start_vector[0] * pm.dt.sqrt(1.0 - (start_vector[1] * start_vector[1] / 2.0) - (start_vector[2] * start_vector[2] / 2.0) +
        #                                 (start_vector[1] * start_vector[1] * start_vector[2] * start_vector[2] / 3.0))
        # # print move_x
        # move_y =  start_vector[1] * pm.dt.sqrt(1.0 - (start_vector[2] * start_vector[2] / 2.0) - (move_x * move_x / 2.0) +
        #                                   (start_vector[2] * start_vector[2] * move_x * move_x / 3.0))
        #
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
        # pm.move(move_x-subtract_vec[0], move_y-subtract_vec[1], move_z-subtract_vec[2], vtx)

        # pm.move(move_x+position_ws[0], move_y+position_ws[1], move_z+position_ws[2], vtx)
        pm.move(move_x, move_y, move_z, vtx)

        #
        # pm.move(move_x-pos[0], move_y-pos[1], move_z-pos[2], vtx)
        # pm.move(x_position, y_position, z_position, vtx)
        # pm.move(start_vector_ws[0]-(move_x*1.25), start_vector_ws[1]-(move_y*1.25), start_vector_ws[2]-(move_z*1.25), vtx)

        # pm.move(move_x + start_vector_ws[0], move_y + start_vector_ws[1], move_z + start_vector_ws[2], vtx)


        # print start_point

        # print vtx
        # pass

def look_at_gift():
    bird = pm.PyNode("Birdy")
    # gift = pm.pyNode('BirthdayPresent')
    # get rotation
    bird_pos = bird.getRotation(ws=1)

    # get radian
    radian =360/ (360*(3.14159/180))
    # reverse value and multiplying by radians
    bird_posx = -3*bird_pos.x * radian
    bird_posy = -2*bird_pos.y * radian
    bird_posz =  1*bird_pos.z * radian
    # print bird_posx
    # print bird_posy
    # print bird_posz

    mtx = pm.xform(bird, q=True, ws=True, m=True)
    # print mtx


    # Invert rotation columns,
    # rx = [n * -1 for n in mtx[0:9:4]]
    # ry = [n * -1 for n in mtx[1:10:4]]
    # rz = [n * -1 for n in mtx[2:11:4]]
    # print rz
    # x = [0,1,2,3,
    #      4,5,6,7,
    #      8,9,10,11,
    #      12,13,14,15]

    # Invert translation row,
    # t = [n * -1 for n in mtx[12:15]]

    # Set matrix based on given plane, and whether to include behaviour or not.
    # if across is 'XY':
    # mtx[14] = t[2]  # set inverse of the Z translation

        # Set inverse of all rotation columns but for the one we've set translate to.
        # if behaviour:
    # mtx[0:9:4] = rx
    # mtx[1:10:4] = ry
    # mtx[2:11:4] = rz

    # mtx[12] = t[1]
    pm.xform(bird, ws=True, ro=((bird_posx), (bird_posy), (bird_posz)))

    # matrix = pm.dt.Matrix(pm.xform(bird, ws=True, q=True, m=True))
    # revere_matrix = matrix.inverse()
    #
    # pm.xform(bird, ws=True, m=revere_matrix)

    # bird_rot = bird.getRotation(worldSpace=1)
    # print bird_rot
    # print bird_rot.x*-1

    # pm.setAttr(bird+'.rotate', (bird_rot.x*-1), (bird_rot.y*-2), (bird_rot.z*1), type='double3')

    # print matrix

def put_on_party_hat():
    hat = pm.PyNode("PartyHat")
    # birdy = pm.PyNode('Birdy')
    birdy_likes_his_hat_here = pm.dt.Matrix([
        [0.99, -0.13, 0.022, 0.0],
        [0.13, 0.97, -0.16, 0.0],
        [0, 0.167, 0.985, 0.0],
        [12.13, 83.57, -15.185, 1.0],
    ])
    hat_spot=pm.PyNode('hat_spot')
    hat_spot_mtx = pm.dt.Matrix(pm.xform(hat_spot, ws=True, q=True, m=True))

    # hatspot = [0.7797672568842141, -0.4750407758702957, 0.4077980950811511, 0.0,
    #            0.4364356809126458, 0.8216065262485835, 0.12255659989689749, 0.0,
    #            -0.39326895861346167, 0.08241201558696215, 0.8479866116892499, 0.0,
    #            38.94775116164466, 251.99476317785977, 10.937015841647028, 1.0]
    #
    #
    # birdy_mtx = [0.7797672568842143, -0.4750407758702958, 0.4077980950811512, 0.0,
    #          0.4364356809126459, 0.8216065262485838, 0.12255659989689752, 0.0,
    #          -0.3932689586134617, 0.08241201558696216, 0.84798661168925, 0.0,
    #          0.0, 178.67416191492592, 0.0, 1.0]
    #
    # party_hat = [0.7797672568842144, -0.4750407758702956, 0.4077980950811512, 0.0,
    #              0.43643568091264573, 0.8216065262485839, 0.1225565998968975, 0.0,
    #              -0.3932689586134617, 0.0824120155869621, 0.84798661168925, 0.0,
    #              12.13, 83.57, -15.185, 1.0]
    #
    # party_hat_opox = [0.7797672568842144, -0.4750407758702956, 0.4077980950811512, 0.0,
    #                   0.43643568091264573, 0.8216065262485839, 0.1225565998968975, 0.0,
    #                   -0.3932689586134617, 0.0824120155869621, 0.84798661168925, 0.0,
    #                   12.13, 262.24416191492594, -15.185, 1.0]

    # birdy_matrix =  pm.dt.Matrix(pm.xform(birdy, ws=True, q=True, m=True))
    # query matrix value
    hatspot_x = hat_spot_mtx.__getitem__(0)
    hatspot_y = hat_spot_mtx.__getitem__(1)
    hatspot_z = hat_spot_mtx.__getitem__(2)
    hatspot_position = hat_spot_mtx.__getitem__(3)

    # target_hat_position =  birdy_likes_his_hat_here.__getitem__(3)
    # # birdy_likes_his_hat_here[13] = birdy_matrix[13]
    # adding_birdy_pos_and_target_position = target_hat_position + birdy_position
    #
    # replacing matrix value
    birdy_likes_his_hat_here.__setitem__(0, hatspot_x)
    birdy_likes_his_hat_here.__setitem__(1, hatspot_y)
    birdy_likes_his_hat_here.__setitem__(2, hatspot_z)
    birdy_likes_his_hat_here.__setitem__(3, hatspot_position)


    # set the hat position
    pm.xform(hat, ws=True, m=birdy_likes_his_hat_here)

    # #########################
    # hat = pm.PyNode("PartyHat")
    # # birdy = pm.PyNode('Birdy')
    # birdy_likes_his_hat_here = pm.dt.Matrix([
    #     [0.99, -0.13, 0.022, 0.0],
    #     [0.13, 0.97, -0.16, 0.0],
    #     [0, 0.167, 0.985, 0.0],
    #     [12.13, 83.57, -15.185, 1.0],
    # ])
    # hat_spot = pm.PyNode('hat_spot')
    #
    # hat_spot_mtx =pm.dt.Matrix(pm.xform(hat_spot, ws=True, q=True, m=True))
    # # birdy_matrix =  pm.dt.Matrix(pm.xform(birdy, ws=True, q=True, m=True))
    #
    # # birdy_position = birdy_matrix.__getitem__(3)
    # target_hat_position =  hat_spot_mtx.__getitem__(3)
    #
    # # adding_birdy_pos_and_target_position = (target_hat_position)
    #
    # # insert the adding value into the position
    # birdy_likes_his_hat_here.__setitem__(3, target_hat_position)
    #
    # # set the hat position
    # pm.xform(hat, ws=True, m=birdy_likes_his_hat_here)



# fix_present()
# look_at_gift()
# put_on_party_hat()