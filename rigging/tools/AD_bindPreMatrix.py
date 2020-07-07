from __builtin__ import reload

import maya.cmds as mc

from rigging.tools import AD_utils as au, AD_controller as ac

reload(ac)
reload(au)


def create_bpm(Fk=None,
               joints='',
               main_mesh='',
               mesh_bpm='',
               base_joint='',
               scale_object=None,
               shape=ac.JOINT,
               ctrl_size=1.0,
               ctrl_color='lightPink',
               connect_mesh=[]
               ):
    """
    :param Fk : bool, either bpm run on FK or IK system
    :param joints: str, list joint bpm FK list
    :param main_mesh: str, object main mesh
    :param mesh_bpm: str, object bind pre matrix mesh
    :param base_joint: str, joint module of bpm
    :param scale_object: str, scaling for bpm, can be replaced by place or world ctrl
    :param connect_mesh: str, list of connection, can be either transConn, rotateConn or both
    :return: None
    """

    if Fk:
        follicle = []
        ctrls = []
        list_joints = []

        all_grp = create_group('transform', "%s%s_%s" % (au.prefix_name(main_mesh), 'AllBpmFk', 'grp'))
        follicle_grp = create_group('transform', "%s%s_%s" % (au.prefix_name(main_mesh), 'FollicleBpmFk', 'grp'))
        drive_grp = create_group('transform', "%s%s_%s" % (au.prefix_name(main_mesh), 'DriveBpmFk', 'grp'))
        ctrl_grp = create_group('transform', "%s%s_%s" % (au.prefix_name(main_mesh), 'ControllerBpmFk', 'grp'))

        list_relatives_allGrp = mc.listRelatives(all_grp, c=1)

        # for obj in joints:
        list_relatives_jnt = mc.listRelatives(joints, f=1, ad=1)
        for i in list_relatives_jnt:
            # remove empty list
            remove_empty_list = list(filter(None, (i.split('|'))))
            for o in remove_empty_list:

                # appending all the items
                if o not in list_joints:
                    list_joints.append(o)

        ac.create_controller(object_list=list_joints,
                             groups_ctrl=['Zro', 'Offset'],
                             ctrl_color=ctrl_color,
                             shape=shape,
                             ctrl_size=ctrl_size,
                             connection=['parent'],
                             lock_channels=[]
                             )

        create_grp = au.group_object_outside('FolFk', list_joints)

        for obj in list_joints:

            # sorting the full path of object then rid off []
            list_relatives_obj = mc.listRelatives(obj, ap=1, f=1)[0]

            # spliting the object with | and take out Zro grp which is on the -4 position
            split_object = list_relatives_obj.split('|')[-3]

            # appending all of the object this is purpose for enumerate later
            ctrls.append(split_object)

            follicles = au.follicle_set(obj, main_mesh, connect_follicle=connect_mesh)

            follicle.append(follicles['folTrans'])

            if scale_object:
                mc.scaleConstraint(scale_object, follicles['folTrans'])

            mc.setAttr(follicles['folShape'] + '.lodVisibility', 0)

            mc.setAttr(obj + '.drawStyle', 2)

            au.lock_hide_attr(['t', 'r', 's'], follicles['folTrans'])

            au.lock_hide_attr_object(follicles['folTrans'], 'v')

            au.lock_hide_attr_object(follicles['folShape'], 'pu')

            au.lock_hide_attr_object(follicles['folShape'], 'pv')

            mc.parent(follicles['folTrans'], follicle_grp)

        for i, obj in zip(create_grp, list_joints):
            # check the attribute root
            # if exist then deleted
            if mc.objExists('%s.root' % obj):
                mc.deleteAttr('%s.root' % obj)
            else:
                continue

            # add the attr root and message
            au.add_attr_message(obj, i)

            # connected the 'create group' to bind pre matrix
            mc.connectAttr('%s.worldInverseMatrix[0]' % i,
                           '%s.bindPreMatrix[%d]' % (au.query_skin_name(mesh_bpm), skin_matrix_list_from_joint(obj)))

        for i, item in enumerate(follicle):
            mc.parentConstraint(item, create_grp[i], mo=1)

        for i, item in enumerate(create_grp):
            au.connect_attr_object(item, ctrls[i])

        list_relatives_jnt = mc.listRelatives(base_joint, p=True)
        if list_relatives_jnt == None:
            grp_obj = au.group_object(['Zro', 'BPM', 'Null', 'Adjust'], base_joint, base_joint)

            mc.connectAttr('%s.worldInverseMatrix[0]' % array_bpm_folder(base_joint),
                           '%s.bindPreMatrix[%d]' % (
                           au.query_skin_name(mesh_bpm), skin_matrix_list_from_joint(base_joint)))

            mc.parent(grp_obj[0], ctrl_grp)

        mc.parent(create_grp[0], drive_grp)

        mc.parent(ctrls[0], ctrl_grp)

        if list_relatives_allGrp == None:
            mc.parent(follicle_grp, drive_grp, ctrl_grp, all_grp)

        mc.select(cl=1)

    if not Fk:

        mc.setAttr(main_mesh + '.visibility', 0)

        ac.create_controller(groups_ctrl=['Zro', 'BPM', 'Offset'],
                             ctrl_color=ctrl_color,
                             shape=shape,
                             ctrl_size=ctrl_size,
                             connection=['parent'],
                             lock_channels=[]
                             )

        all_grp = create_group('transform', "%s%s_%s" % (au.prefix_name(main_mesh), 'AllBPM', 'grp'))
        follicle_grp = create_group('transform', "%s%s_%s" % (au.prefix_name(main_mesh), 'ControllerBPM', 'grp'))

        list_relatives_allGrp = mc.listRelatives(all_grp, c=1)

        if list_relatives_allGrp == None:
            mc.parent(follicle_grp, all_grp)

        foll_append = []

        for obj in joints:
            # create ctrl

            # create follicle
            follicles = au.follicle_set(obj, main_mesh, connect_follicle=connect_mesh)

            foll_append.append(follicles['folTrans'])

            # sort the list full path object then rid off []
            list_relatives_obj = mc.listRelatives(obj, ap=1, f=1)[0]

            # spliting object |
            split_object = list_relatives_obj.split('|')

            # parent the object to follicle
            mc.parent(split_object[1], follicles['folTrans'])

            # for scl in scaleObj:
            if scale_object:
                mc.scaleConstraint(scale_object, follicles['folTrans'])

            mc.setAttr(follicles['folShape'] + '.lodVisibility', 0)

            mc.setAttr(obj + '.drawStyle', 2)

            au.lock_hide_attr_object(follicles['folTrans'], 'v')

            au.lock_hide_attr_object(follicles['folShape'], 'pu')

            au.lock_hide_attr_object(follicles['folShape'], 'pv')

            au.lock_attr(['t', 'r', 's'], split_object[1])

            au.lock_attr(['t', 'r', 's'], split_object[2])

            mc.connectAttr('%s.worldInverseMatrix[0]' % array_bpm_folder(obj),
                           '%s.bindPreMatrix[%d]' % (
                               au.query_skin_name(mesh_bpm), skin_matrix_list_from_joint(obj)))

            mc.parent(follicles['folTrans'], follicle_grp)

        list_relatives_jnt = mc.listRelatives(base_joint, p=True)
        if list_relatives_jnt == None:
            grp_obj = au.group_object(['Zro', 'BPM', 'Offset', 'Null'], base_joint, base_joint)

            mc.connectAttr('%s.worldInverseMatrix[0]' % array_bpm_folder(base_joint),
                           '%s.bindPreMatrix[%d]' % (
                               au.query_skin_name(mesh_bpm), skin_matrix_list_from_joint(base_joint)))

            mc.parent(grp_obj[0], all_grp)

        mc.select(cl=1)


################################################# re-skin the mesh ###################################################
def reskin_mesh_bpm(Fk=None,
                    joints='',
                    mesh_bpm='',
                    base_joint=''):
    """
    :param Fk : bool, either bpm run on FK or IK system
    :param joints: str, list joint bpm FK list
    :param mesh_bpm: str, object bind pre matrix mesh
    :param base_joint: str, joint module of bpm
    :return: None
    """

    if not Fk:
        for obj in joints:
            # listing the connection of group BPM
            list_connection = mc.listConnections('%s.worldInverseMatrix[0]' % array_bpm_folder(obj), p=1)

            # disconnect if its still connected
            if list_connection:
                mc.disconnectAttr('%s.worldInverseMatrix[0]' % array_bpm_folder(obj), list_connection[0])
            else:
                continue

            # connect the bpm transform to skin bind pre matrix
            mc.connectAttr('%s.worldInverseMatrix[0]' % array_bpm_folder(obj),
                           '%s.bindPreMatrix[%d]' % (au.query_skin_name(mesh_bpm), skin_matrix_list_from_joint(obj)))

    if Fk:
        grp_driver = mc.listConnections(joints, s=True, type='transform')

        for i, obj in zip(grp_driver, joints):
            # listing the connection of group BPM
            list_connection = mc.listConnections('%s.worldInverseMatrix[0]' % i, p=1)

            # disconnect if its still connected
            if list_connection:
                mc.disconnectAttr('%s.worldInverseMatrix[0]' % i, list_connection[0])

            else:
                continue

            # connect the bpm transform to skin bind pre matrix
            mc.connectAttr('%s.worldInverseMatrix[0]' % i,
                           '%s.bindPreMatrix[%d]' % (au.query_skin_name(mesh_bpm), skin_matrix_list_from_joint(obj)))

    # re-conncet module joint
    list_connetion_base = mc.listConnections('%s.worldInverseMatrix[0]' % array_bpm_folder(base_joint))
    if not list_connetion_base:
        mc.connectAttr('%s.worldInverseMatrix[0]' % array_bpm_folder(base_joint),
                       '%s.bindPreMatrix[%d]' % (au.query_skin_name(mesh_bpm), skin_matrix_list_from_joint(base_joint)))
    else:
        return

    mc.select(cl=1)


############################################## tools BPM ###############################################

# listing the joint connection destination to skin cluster matrix
def joint_destination_matrix(obj):
    list_connection = mc.listConnections(obj + '.worldMatrix[0]', p=True)
    return list_connection


# get the number of skin cluster matrix
def skin_matrix_list_from_joint(obj):
    for item in joint_destination_matrix(obj):
        split = item.split('.')[1:]
        integer = int((split[0].split('[')[-1][:-1]))
        return integer


def array_bpm_folder(obj):
    relatives = mc.listRelatives(obj, p=True, f=True)
    for o in relatives:
        split = o.split('|')[-3]
        return split


def create_group(node, name):
    if not mc.objExists(name):
        node_name = mc.createNode(node, n=name)
        return node_name
    else:
        return name


####################################### sorting the skin matrix index (not used) ##############################################################

# remove the long name form matrix long name listing of skin cluster
def skin_matrix_list(obj):
    objs = []
    for o in skin_matrix_list_long(obj):
        objs.append(int(o))
    return objs


# getting attribute matrix long name from listing of skin cluster
def skin_matrix_list_long(obj):
    for i in obj:
        get_attr = mc.getAttr(i + '.matrix', mi=True)
        return get_attr


# getting complete name skin cluster matrix include the number
def skin_cluster_matrix_list_num(obj):
    list_matrix = []
    for cluster in obj:
        for indexNum in skin_matrix_list(obj):
            at = cluster + '.matrix[%d]' % (int(indexNum))
            list_matrix.append(at)
    return list_matrix


# getting the source connection from the skin cluster matrix
def source_joint_skin_matrix(obj):
    list = mc.listConnections(skin_cluster_matrix_list_num(obj), d=True)
    return list


############################################# misc (not used) ##################################################


def group_fk(obj):
    for i in obj:
        split_name = i.split('|')[0]
        grp_parent = au.group_parent(['ParentPos', 'PosSDK'], au.prefix_name(i), '')
        au.match_position(split_name, grp_parent[0])
        return grp_parent


def list_matrix_connection(obj):
    list = mc.listConnections(obj[0] + '.matrix', s=True)
    return list


def list_folder_bpm_connection(obj):
    objs = []
    for i in obj:
        objs.append(mc.listConnections(i, d=True))
    return objs


def list_relatives(obj):
    grps = []
    for o in obj:
        lR = grps.append(mc.listRelatives(o, ap=True))
    return grps


def adding_grp_not_none_list_relatives(obj):
    grps = group_fk(obj)
    return grps


def array_part_object(joints, listObj):
    grps = []
    for obj in joints:
        if obj in listObj:
            grps.append(obj)
    return grps
