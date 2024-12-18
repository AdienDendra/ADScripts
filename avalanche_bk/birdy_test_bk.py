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
        position = pm.xform(vtx, q=True, os=True, t=True)
        position_ws = pm.xform(vtx, q=True, ws=True, t=True)
        start_vector = pm.dt.Vector(position[0], position[1], position[2])

        start_vector_ws = pm.dt.Vector(position_ws[0], position_ws[1], position_ws[2])
        vector_position = start_vector_ws - start_vector
        start_vector = start_vector * 2
        print
        start_vector

        move_x = (start_vector[0] * pm.dt.sqrt(1.0 - (start_vector[1] * start_vector[1] / 2.0) -
                                               (start_vector[2] * start_vector[2] / 2.0) +
                                               (start_vector[1] * start_vector[1] * start_vector[2] * start_vector[
                                                   2] / 3.0)))

        move_y = (start_vector[1] * pm.dt.sqrt(1.0 - (start_vector[2] * start_vector[2] / 2.0) -
                                               (start_vector[0] * start_vector[0] / 2.0) +
                                               (start_vector[2] * start_vector[2] * start_vector[0] * start_vector[
                                                   0] / 3.0)))

        move_z = (start_vector[2] * pm.dt.sqrt(1.0 - (start_vector[0] * start_vector[0] / 2.0) -
                                               (start_vector[1] * start_vector[1] / 2.0) +
                                               (start_vector[0] * start_vector[0] * start_vector[1] * start_vector[
                                                   1] / 3.0)))

        # pm.move(move_x+(vector_position[0]), move_y+(vector_position[1]), move_z+(vector_position[2]), vtx)

        pm.move(move_x * 0.5 + (vector_position[0]), move_y * 0.5 + (vector_position[1]),
                move_z * 0.5 + (vector_position[2]), vtx)


def look_at_gift():
    # import maya.OpenMaya as om
    # import math
    #
    # eyeAim = om.MVector().xAxis
    # eyeUp = om.MVector().yAxis
    #
    # targetDag = om.MDagPath()
    # sel = om.MSelectionList()
    # sel.add('BirthdayPresent')
    # sel.getDagPath(0, targetDag)
    # targetDag.fullPathName()
    #
    # eyeDag = om.MDagPath()
    # sel = om.MSelectionList()
    # sel.add('Birdy')
    # sel.getDagPath(0, eyeDag)
    # eyeDag.fullPathName()
    #
    # # eyeDag, targetDag = pbApi.api_getMDagPath('Birdy', 'BirthdayPresent')
    #
    # transformFn = om.MFnTransform(eyeDag)
    # eyePivotPOS = transformFn.rotatePivot(om.MSpace.kWorld)
    #
    # transformFn = om.MFnTransform(targetDag)
    # targetPivotPOS = transformFn.rotatePivot(om.MSpace.kWorld)
    #
    # aimVector = (targetPivotPOS - eyePivotPOS)
    # eyeU = aimVector.normal()
    # worldUp = om.MGlobal.upAxis()
    #
    # eyeV = worldUp
    # eyeW = (eyeU ^ eyeV).normal()
    #
    # eyeV = eyeW ^ eyeU
    # quaternion = om.MQuaternion()
    # quaternionU = om.MQuaternion(eyeAim, eyeU)
    # quaternion = quaternionU
    #
    # upRotated = eyeUp.rotateBy(quaternion)
    # angle = math.acos(upRotated * eyeV)
    # quaternionV = om.MQuaternion(angle, eyeU)
    #
    # if not eyeV.isEquivalent(upRotated.rotateBy(quaternionV), 1.0e-5):
    #     angle = (2 * math.pi) - angle
    #     quaternionV = om.MQuaternion(angle, eyeU)
    #
    # quaternion *= quaternionV
    #
    # transformFn.setObject(eyeDag)
    # transformFn.setRotation(quaternion)
    bird = pm.PyNode("Birdy")
    # bird_pos = bird.getRotation(ws=1)

    # get radian
    # radian =360/ (360*(3.14159/180))
    # # reverse value and multiplying by radians
    # bird_posx = (-3*bird_pos.x) * radian
    # bird_posy = (-2*bird_pos.y) * radian
    # bird_posz =  (1*bird_pos.z) * radian
    # pm.xform(bird, ws=True, ro=((bird_posx), (bird_posy), (bird_posz)))

    # print bird_posx
    # print bird_posy
    # print bird_posz

    # vecAxis = pm.dt.Vector(bird_pos)
    # print vecAxis
    # newVector = vecAxis.rotateBy(vecAxis, math.radians(90))
    #
    # # print "initial Vector: ", vec1[0], vec1[1], vec1[2]
    # print "new Vector: ", newVector[0], newVector[1], newVector[2]
    # pm.xform(bird, ws=True, ro=((newVector[0]), (newVector[1]), (newVector[2])))

    # pm.xform(bird, ws=True, ro=((newVector[0]* math.radians(45)), (newVector[1]* math.radians(45)), (newVector[2]* math.radians(45))))

    mtx = pm.xform(bird, q=True, ws=True, m=True)
    print
    mtx
    # print mtx
    #
    # print mtx
    # mtx = [0.7797672568842143, -0.4750407758702958, -0.4077980950811512, 0.0,
    #        0.4364356809126459, 0.8216065262485838, 0.12255659989689752, 0.0,
    #        0.3932689586134617, -0.08241201558696216, 0.84798661168925, 0.0,
    #        0.0, 178.67416191492592, 0.0, 1.0]

    # # Invert rotation columns,
    # rx = [n * -1 for n in mtx[0:9:4]] #xy
    # ry = [n * -1 for n in mtx[1:10:4]] #yz
    # rz = [n for n in mtx[2:11:4]]
    # print rz
    # print mtx
    # mtx =[0.7797672568842147, -0.4750407758702952, 0.40779809508115117, 0.0,
    #       0.4364356809126453, 0.8216065262485841, 0.12255659989689753, 0.0,
    #       -0.3932689586134618, 0.0824120155869618, 0.84798661168925, 0.0,
    #       0.0, 178.67416191492592, 0.0, 1.0]
    # x = [n for n in mtx[2:11:4]]
    # print x

    # rz = [n * -1 for n in mtx[2:11:4]] #z1
    # print rz
    # mtx[2:11:4] = rz
    # print mtx
    # mtx_2 = [0.7797672568842147, -0.4750407758702952, -0.40779809508115117, 0.0,
    #          0.4364356809126453, 0.8216065262485841, -0.12255659989689753, 0.0,
    #          -0.3932689586134618, 0.0824120155869618, -0.84798661168925, 0.0,
    #          0.0,178.67416191492592, 0.0, 1.0]

    # print rz
    # # rotate_x = [n * -1 for n in mtx[0:9:4]]
    # # rotate_y =
    # # rotate_z =
    #
    # x = [0,1,xz,3,
    #      yx,5,6,7,
    #      8,9,10,wz,
    #      12,13,14,15]

    # # Invert translation row,
    # t = [n * -1 for n in mtx[12:15]]
    #
    #
    # # Set matrix based on given plane, and whether to include behaviour or not.
    # # if across is 'XY':
    # # mtx[14] = t[2]  # set inverse of the Z translation
    #
    #     # Set inverse of all rotation columns but for the one we've set translate to.
    #     # if behaviour:
    # mtx[0:9:4] = rx
    # mtx[1:10:4] = ry
    # mtx[2:11:4] = rz
    #
    # mtx[12] = t[1]
    #
    # matrix = pm.dt.Matrix(pm.xform(bird, ws=True, q=True, m=True))
    # revere_matrix = mtx.inverse()
    #
    # print mtx
    # mtx = [0.7797672568842143, -0.4750407758702958, -0.4077980950811512, 0.0,
    #        0.4364356809126459, 0.8216065262485838, -0.12255659989689752, 0.0,
    #        -0.3932689586134617, 0.08241201558696216, -0.84798661168925, 0.0,
    #        0.0, 178.67416191492592, 0.0, 1.0]
    #
    # # bird_rot = bird.getRotation(worldSpace=1)
    # # print bird_rot
    # # print bird_rot.x*-1
    #
    # # pm.setAttr(bird+'.rotate', (bird_rot.x*-1), (bird_rot.y*-2), (bird_rot.z*1), type='double3')
    #
    # # print matrix

    # numbers are approximated!
    # y axis rotation 60 degrees

    # 45 degrees
    y_rot = pm.dt.Matrix([0.52532198881, 0.0, -0.85090352453, 0.0,
                          0.0, 1.0, 0.0, 0.0,
                          0.85090352453, 0.0, 0.52532198881, 0.0,
                          0.0, 0.0, 0.0, 1.0])
    # 90 degree
    y_rot = pm.dt.Matrix([-0.44807361612, 0.0, -0.8939966636, 0.0,
                          0.0, 1.0, 0.0, 0.0,
                          0.8939966636, 0.0, -0.44807361612, 0.0,
                          0.0, 0.0, 0.0, 1.0])

    # 60 degree
    y_rot = pm.dt.Matrix([0.5, 0.0, -0.86602540378443864676372317075294, 0.0,
                          0.0, 1.0, 0.0, 0.0,
                          0.86602540378443864676372317075294, 0.0, 0.5, 0.0,
                          0.0, 0.0, 0.0, 1.0])
    # 75 degree
    y_rot = pm.dt.Matrix([0.25881904510252076234889883762405, 0.0, -0.9659258262890682867497431997289, 0.0,
                          0.0, 1.0, 0.0, 0.0,
                          0.9659258262890682867497431997289, 0.0, 0.25881904510252076234889883762405, 0.0,
                          0.0, 0.0, 0.0, 1.0])

    # 90 degree Y axis
    y_rot = pm.dt.Matrix([0.0, 0.0, -1, 0.0,
                          0.0, 1.0, 0.0, 0.0,
                          1, 0.0, 0.0, 0.0,
                          0.0, 0.0, 0.0, 1.0])

    # 45 degrees in Z
    # z_rot = pm.dt.Matrix([0.707, 0.707, 0, 0, -0.707, 0.707, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1])

    # # 30 degrees in Y
    # y_rot = pm.dt.Matrix([0.866, 0, 0.5, 0,
    #                       0, 1, 0, 0,
    #                       -0.5, 0, 0.866, 0,
    #                       0, 0, 0, 1])

    # a = pm.dt.Matrix([0.7797672568842143, -0.4750407758702958, 0.4077980950811512, 0.0,
    #                   0.4364356809126459, 0.8216065262485838, 0.12255659989689752, 0.0,
    #                   -0.3932689586134617, 0.08241201558696216, 0.84798661168925, 0.0,
    #                   0.0, 178.67416191492592, 0.0, 1.0])

    yz_matrix = pm.dt.Matrix(mtx) * y_rot

    pm.xform('Birdy', ws=True, m=yz_matrix)

    # zy_matrix = z_rot * y_rot

    # print (yz_matrix)
    #  MMatrix([0.612, 0.707, 0.354, 0, -0.612, 0.707, -0.354, -0.5, 0, 0.866, 0, 0,0, 0, 1])

    # print (zy_matrix)

    #  MMatrix([0.612, 0.707, 0.354, 0, -707, 0.707, 0, -0.354, -0.354, 0.866, 0, 0,0, 0, 1])


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

    #
    # replacing matrix value
    birdy_likes_his_hat_here.__setitem__(0, hatspot_x)
    birdy_likes_his_hat_here.__setitem__(1, hatspot_y)
    birdy_likes_his_hat_here.__setitem__(2, hatspot_z)
    birdy_likes_his_hat_here.__setitem__(3, hatspot_position)

    # set the hat position
    pm.xform(hat, ws=True, m=birdy_likes_his_hat_here)

# fix_present()
# look_at_gift()
# put_on_party_hat()
