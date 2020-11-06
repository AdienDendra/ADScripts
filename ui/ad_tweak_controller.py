from __builtin__ import reload
from functools import partial

import maya.cmds as mc
import pymel.core as pm

from rigging.tools import AD_utils as au, AD_controller as ac

reload(ac)
reload(au)

layout = 400
percentage = 0.01 * layout
on_selector = 0
on_selector_rotate = 0
on_stretch = 0


def ad_show_ui():
    adien_tweaker_ctrl = 'AD_TweakController'
    pm.window(adien_tweaker_ctrl, exists=True)
    if pm.window(adien_tweaker_ctrl, exists=True):
        pm.deleteUI(adien_tweaker_ctrl)
    with pm.window(adien_tweaker_ctrl, title='AD Tweaker Controller', width=400, height=400):
        with pm.tabLayout('tab', width=410, height=210):
            with pm.columnLayout('Create Tweak Controller', rowSpacing=1 * percentage, w=layout,
                                 co=('both', 1 * percentage), adj=1):
                pm.separator(h=10, st="in", w=layout)
                # frame layout message fkik arm and leg
                # with pm.frameLayout(collapsable=True, l='Create Controller Tweaker', mh=5):
                with pm.rowLayout(nc=3, columnAttach=[(1, 'right', 0), (2, 'left', 1 * percentage),
                                                      (3, 'left', 1 * percentage)],
                                  cw3=(29.5 * percentage, 30 * percentage, 30 * percentage,
                                       )
                                  ):
                    pm.text('Tweak Method:')
                    method_radio_button = pm.radioCollection()
                    method_joint_hierarchy = pm.radioButton(label='Hierarchy Joint',
                                                            onCommand=lambda x: ad_on_selection_button(1))
                    pm.radioButton(label='Non-Hierarchy Joint',
                                   onCommand=lambda x: ad_on_selection_button(2))
                    pm.radioCollection(method_radio_button, edit=True, select=method_joint_hierarchy)

                ad_defining_object_text_field(define_object='List_Joint', label="List Joint:", multiple_selection=True)

                ad_defining_object_text_field(define_object='Tweak_Mesh', label="Tweak Mesh:")

                ad_defining_object_text_field(define_object='Main_Mesh', label="Main Mesh:")

                ad_defining_object_text_field(define_object='Static_Joint', label="Static Joint:")
                with pm.rowColumnLayout(nc=2, rowSpacing=(2, 1 * percentage),
                                        co=(1 * percentage, 'both', 1 * percentage),
                                        cw=[(1, 3 * percentage), (2, 93 * percentage)]):
                    pm.checkBox(label='',
                                # cc=partial(ad_enabling_disabling_ui, ['Upper_Limb_Ik_Ctrl']),
                                value=True)
                    ad_defining_object_text_field(define_object='Scale_Connection', label="Scale Connection:",
                                                  add_feature=True)

                with pm.rowLayout(nc=4, columnAttach=[(1, 'right', 0), (2, 'left', 1 * percentage),
                                                      (3, 'left', 1 * percentage), (4, 'left', 1 * percentage)],
                                  cw4=(30 * percentage, 18 * percentage, 18 * percentage, 20 * percentage)):
                    pm.text('Constraint:')
                    direction_control_translate = pm.radioCollection()
                    direction_translateX = pm.radioButton(label='Point',
                                                          # onCommand=lambda x: ad_on_selection_button(1)
                                                          )
                    pm.radioButton(label='Orient',
                                   # onCommand=lambda x: ad_on_selection_button(2)
                                   )
                    pm.radioButton(label='Parent',
                                   # onCommand=lambda x: ad_on_selection_button(3)
                                   )
                    pm.radioCollection(direction_control_translate, edit=True, select=direction_translateX)

                with pm.rowLayout(nc=2, cw2=(48 * percentage, 48 * percentage), cl2=('center', 'left'),
                                  columnAttach=[(1, 'both', 0.5 * percentage), (2, 'both', 0.5 * percentage)]):
                    pm.button(l="Clear All Define Objects!", bgc=(1, 1, 0),
                              # c=ad_additional_attr_adding
                              )

                    # create button to delete last pair of text fields
                    pm.button("create_tweak_controller", l="Create Tweak Controller!", bgc=(0, 0.5, 0),
                              c=partial(ad_create_tweaker)
                              )
                pm.separator(h=10, st="in", w=layout)
                with pm.rowLayout(nc=2, cw2=(49 * percentage, 49 * percentage), cl2=('center', 'center'),
                                  columnAttach=[(1, 'both', 2 * percentage), (2, 'both', 2 * percentage)]):
                    pm.text(l='Adien Dendra | 11/2020', al='left')
                    pm.text(
                        l='<a href="http://projects.adiendendra.com/ad-universal-fkik-setup-tutorial/">find out how to use it! >> </a>',
                        hl=True,
                        al='right')
            with pm.columnLayout('Edit Tweak Controller', rowSpacing=1 * percentage, w=layout,
                                 co=('both', 1 * percentage), adj=1):
                # frame layout message fkik arm and leg
                # with pm.frameLayout(collapsable=True, l='Edit Controller Tweaker', mh=5):
                pm.separator(h=10, st="in", w=layout)
                with pm.rowLayout(nc=3, columnAttach=[(1, 'right', 0), (2, 'left', 1 * percentage),
                                                      (3, 'left', 1 * percentage)],
                                  cw3=(29.5 * percentage, 30 * percentage, 30 * percentage),
                                  ):
                    pm.text('Tweak Method:')
                    method_edit_radio_button = pm.radioCollection()
                    method_edit_joint_hierarchy = pm.radioButton(label='Hierarchy Joint', )
                    # onCommand=lambda x: ad_on_position_button(1))
                    pm.radioButton(label='Non-Hierarchy Joint', )
                    # onCommand=lambda x: ad_on_position_button(2))
                    pm.radioCollection(method_edit_radio_button, edit=True, select=method_edit_joint_hierarchy)

                ad_defining_object_text_field(define_object='List_Edit_Joint', label="List Joint:",
                                              multiple_selection=True)
                ad_defining_object_text_field(define_object='Tweak_Edit_Mesh', label="Tweak Mesh:")
                ad_defining_object_text_field(define_object='Static_Edit_Joint', label="Static Joint:")

                with pm.rowLayout(nc=2, cw2=(48 * percentage, 48 * percentage), cl2=('center', 'center'),
                                  columnAttach=[(1, 'both', 0.5 * percentage), (2, 'both', 0.5 * percentage)]):
                    pm.button(l="Clear All Define Objects!", bgc=(1, 1, 0),
                              # c=ad_additional_attr_adding
                              )

                    # create button to delete last pair of text fields
                    pm.button(l="Edit Tweak Controller!", bgc=(0, 0, 0.5),
                              # c=ad_additional_attr_deleting
                              )
                pm.separator(h=10, st="in", w=layout)
                with pm.rowLayout(nc=2, cw2=(49 * percentage, 49 * percentage), cl2=('center', 'center'),
                                  columnAttach=[(1, 'both', 2 * percentage), (2, 'both', 2 * percentage)]):
                    pm.text(l='Adien Dendra | 11/2020', al='left')
                    pm.text(
                        l='<a href="http://projects.adiendendra.com/ad-universal-fkik-setup-tutorial/">find out how to use it! >> </a>',
                        hl=True,
                        al='right')
        pm.setParent(u=True)
    pm.showWindow()


def ad_adding_object_sel_to_textfield(text_input, *args):
    # elect and add object
    select = pm.ls(sl=True, l=True, tr=True)
    if len(select) == 1:
        object_selection = select[0]
        pm.textFieldButtonGrp(text_input, e=True, tx=object_selection)
    else:
        pm.error("please select one object!")


def ad_adding_multiple_object_sel_to_texfield(text_input, *args):
    select = pm.ls(sl=True, l=True, tr=True)
    list_joint = (','.join([item.name() for item in select]))
    pm.textFieldButtonGrp(text_input, e=True, tx=str(list_joint))

    # list = []
    # for item in select:
    #     list.append(str(item))
    # object = str(list)
    # replacing = object.replace('[', '').replace(']', '').replace("'", '').replace(" ", '')


def ad_on_selection_button(on):
    # save the current shape selection into global variable
    global on_selector
    on_selector = on
    print on_selector


def ad_hierarchy_joint(*args):
    hierarchy = []
    # query object with value on shape selector status

    if on_selector == 1:
        hierarchy = True
    elif on_selector == 2:
        hierarchy = False
    else:
        pass

    return hierarchy


def ad_defining_object_text_field(define_object, label, add_feature=False, multiple_selection=False, *args, **kwargs):
    if not add_feature:
        # if object doesn't has checkbox
        if multiple_selection:
            pm.textFieldButtonGrp(define_object, label=label, cal=(1, "right"),
                                  cw3=(30 * percentage, 58 * percentage, 15 * percentage),
                                  cat=[(1, 'right', 2), (2, 'both', 2), (3, 'left', 2)],
                                  bl="<<",
                                  bc=partial(ad_adding_multiple_object_sel_to_texfield, define_object,
                                             ))
        else:
            pm.textFieldButtonGrp(define_object, label=label, cal=(1, "right"),
                                  cw3=(30 * percentage, 58 * percentage, 15 * percentage),
                                  cat=[(1, 'right', 2), (2, 'both', 2), (3, 'left', 2)],
                                  bl="<<",
                                  bc=partial(ad_adding_object_sel_to_textfield, define_object,
                                             ))
    else:
        if multiple_selection:
            pm.textFieldButtonGrp(define_object, label=label, cal=(1, "right"),
                                  cw3=(27 * percentage, 58 * percentage, 15 * percentage),
                                  cat=[(1, 'right', 2), (2, 'both', 2), (3, 'left', 2)],
                                  bl="<<",
                                  bc=partial(ad_adding_multiple_object_sel_to_texfield, define_object),
                                  **kwargs)
        # if object has checkbox
        else:
            pm.textFieldButtonGrp(define_object, label=label, cal=(1, "right"),
                                  cw3=(27 * percentage, 58 * percentage, 15 * percentage),
                                  cat=[(1, 'right', 2), (2, 'both', 2), (3, 'left', 2)],
                                  bl="<<",
                                  bc=partial(ad_adding_object_sel_to_textfield, define_object),
                                  **kwargs)

def ad_query_textfield_object(object_define, *args):
    text = []
    if (pm.textFieldButtonGrp(object_define, q=True, en=True)):
        if (pm.textFieldButtonGrp(object_define, q=True, tx=True)):
            text = pm.textFieldButtonGrp(object_define, q=True, tx=True)
            if pm.ls(text):
                text = pm.textFieldButtonGrp(object_define, q=True, tx=True)
            else:
                pm.error('%s has wrong input object name.' % object_define, "There is no object with name '%s'!" % text)
        else:
            pm.error('%s can not be empty!' % object_define)
    else:
        pass
    return text, object_define


def ad_create_tweaker(Fk=None,
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

    if ad_hierarchy_joint():
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
        for item in list_relatives_jnt:
            # remove empty list
            list_joints = list(filter(None, (item.split('|'))))

        ac.create_controller(object_list=list_joints,
                             groups_ctrl=['Zro', 'Offset'],
                             ctrl_color=ctrl_color,
                             shape=shape,
                             ctrl_size=ctrl_size,
                             connection=['parent'],
                             lock_channels=[]
                             )

        create_grp = au.group_object_outside('FolFk', list_joints)

        for object_fol, item_grp in zip(list_joints, create_grp):

            # sorting the full path of object then rid off []
            list_relatives_obj = mc.listRelatives(object_fol, ap=1, f=1)[0]

            # spliting the object with | and take out Zro grp which is on the -4 position
            split_object = list_relatives_obj.split('|')[-3]

            # appending all of the object this is purpose for enumerate later
            ctrls.append(split_object)

            follicles = au.follicle_set(object_fol, main_mesh, connect_follicle=connect_mesh)

            follicle.append(follicles['folTrans'])

            # check the attribute root
            # if exist then deleted
            if mc.objExists('%s.root' % object_fol):
                mc.deleteAttr('%s.root' % object_fol)
            else:
                # add the attr root and message
                au.add_attr_message(object_fol, item_grp)

            # connected the 'create group' to bind pre matrix
            mc.connectAttr('%s.worldInverseMatrix[0]' % item_grp,
                           '%s.bindPreMatrix[%d]' % (
                               au.query_skin_name(mesh_bpm), skin_matrix_list_from_joint(object_fol)))

            if scale_object:
                mc.scaleConstraint(scale_object, follicles['folTrans'])

            mc.setAttr(follicles['folShape'] + '.lodVisibility', 0)

            mc.setAttr(object_fol + '.drawStyle', 2)

            au.lock_hide_attr(['t', 'r', 's'], follicles['folTrans'])

            au.lock_hide_attr_object(follicles['folTrans'], 'v')

            au.lock_hide_attr_object(follicles['folShape'], 'pu')

            au.lock_hide_attr_object(follicles['folShape'], 'pv')

            mc.parent(follicles['folTrans'], follicle_grp)

        for item, (object_fol, object_grp) in enumerate(zip(follicle, create_grp)):
            mc.parentConstraint(object_fol, create_grp[item], mo=1)
            au.connect_attr_object(object_grp, ctrls[item])

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

    else:

        mc.setAttr(main_mesh + '.visibility', 0)

        all_grp = create_group('transform', "%s%s_%s" % (au.prefix_name(main_mesh), 'AllBPM', 'grp'))
        follicle_grp = create_group('transform', "%s%s_%s" % (au.prefix_name(main_mesh), 'ControllerBPM', 'grp'))

        list_relatives_allGrp = mc.listRelatives(all_grp, c=1)

        if list_relatives_allGrp == None:
            mc.parent(follicle_grp, all_grp)

        ac.create_controller(object_list=joints,
                             groups_ctrl=['Zro', 'BPM', 'Offset'],
                             ctrl_color=ctrl_color,
                             shape=shape,
                             ctrl_size=ctrl_size,
                             connection=['parent'],
                             lock_channels=[]
                             )

        foll_append = []

        for object_fol in joints:

            # create follicle
            follicles = au.follicle_set(object_fol, main_mesh, connect_follicle=connect_mesh)

            foll_append.append(follicles['folTrans'])

            # sort the list full path object then rid off []
            list_relatives_obj = mc.listRelatives(object_fol, ap=1, f=1)[0]

            # spliting object |
            split_object = filter(None, list_relatives_obj.split('|'))
            print split_object

            # parent the object to follicle
            mc.parent(split_object[0], follicles['folTrans'])

            # for scl in scaleObj:
            if scale_object:
                mc.scaleConstraint(scale_object, follicles['folTrans'])

            mc.setAttr(follicles['folShape'] + '.lodVisibility', 0)

            mc.setAttr(object_fol + '.drawStyle', 2)

            au.lock_hide_attr_object(follicles['folTrans'], 'v')

            au.lock_hide_attr_object(follicles['folShape'], 'pu')

            au.lock_hide_attr_object(follicles['folShape'], 'pv')

            au.lock_attr(['t', 'r', 's'], split_object[1])

            au.lock_attr(['t', 'r', 's'], split_object[2])

            mc.connectAttr('%s.worldInverseMatrix[0]' % array_bpm_folder(object_fol),
                           '%s.bindPreMatrix[%d]' % (
                               au.query_skin_name(mesh_bpm), skin_matrix_list_from_joint(object_fol)))

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
def ad_edit_tweaker(Fk=None,
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
    if Fk:
        grp_driver = mc.listConnections(joints, s=True, type='transform')

        for group, joint in zip(grp_driver, joints):
            # listing the connection of group BPM
            list_connection = mc.listConnections('%s.worldInverseMatrix[0]' % group, p=1)
            print list_connection
            # disconnect if its still connected
            if list_connection:
                mc.disconnectAttr('%s.worldInverseMatrix[0]' % group, list_connection[0])
                # connect the bpm transform to skin bind pre matrix
                mc.connectAttr('%s.worldInverseMatrix[0]' % group,
                               '%s.bindPreMatrix[%d]' % (
                                   au.query_skin_name(mesh_bpm), skin_matrix_list_from_joint(joint)))

            else:
                # connect the bpm transform to skin bind pre matrix
                mc.connectAttr('%s.worldInverseMatrix[0]' % group,
                               '%s.bindPreMatrix[%d]' % (
                                   au.query_skin_name(mesh_bpm), skin_matrix_list_from_joint(joint)))

    else:
        for joint in joints:
            # listing the connection of group BPM
            list_connection = mc.listConnections('%s.worldInverseMatrix[0]' % array_bpm_folder(joint), p=1)

            # disconnect if its still connected
            if list_connection:
                mc.disconnectAttr('%s.worldInverseMatrix[0]' % array_bpm_folder(joint), list_connection[0])
                # connect the bpm transform to skin bind pre matrix
                mc.connectAttr('%s.worldInverseMatrix[0]' % array_bpm_folder(joint),
                               '%s.bindPreMatrix[%d]' % (
                                   au.query_skin_name(mesh_bpm), skin_matrix_list_from_joint(joint)))

            else:
                # connect the bpm transform to skin bind pre matrix
                mc.connectAttr('%s.worldInverseMatrix[0]' % array_bpm_folder(joint),
                               '%s.bindPreMatrix[%d]' % (
                                   au.query_skin_name(mesh_bpm), skin_matrix_list_from_joint(joint)))

    # re-conncet module joint
    list_connetion_base = mc.listConnections('%s.worldInverseMatrix[0]' % array_bpm_folder(base_joint))
    if not list_connetion_base:
        mc.connectAttr('%s.worldInverseMatrix[0]' % array_bpm_folder(base_joint),
                       '%s.bindPreMatrix[%d]' % (au.query_skin_name(mesh_bpm), skin_matrix_list_from_joint(base_joint)))
    else:
        return

    mc.select(cl=1)


############################################## tools tweaker ###############################################

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
