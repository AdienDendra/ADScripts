from __builtin__ import reload
from functools import partial
from string import digits

# import maya.cmds as mc
import pymel.core as pm
import re

from rigging.tools import AD_utils as au, AD_controller as ac

reload(ac)
reload(au)

layout = 400
percentage = 0.01 * layout
on_selector = 0
# on_connection_select = 0


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

                ad_defining_object_text_field(define_object='List_Tweak_Joint', label="List Tweak Joint:", multiple_selection=True)

                ad_defining_object_text_field(define_object='Tweak_Mesh', label="Tweak Mesh:")

                ad_defining_object_text_field(define_object='Main_Mesh', label="Main Mesh:")

                ad_defining_object_text_field(define_object='Static_Joint', label="Static Joint:")
                with pm.rowColumnLayout(nc=2, rowSpacing=(2, 1 * percentage),
                                        co=(1 * percentage, 'both', 1 * percentage),
                                        cw=[(1, 3 * percentage), (2, 93 * percentage)]):
                    pm.checkBox(label='',
                                cc=partial(ad_enabling_disabling_ui, ['Scale_Connection']),
                                value=False)
                    ad_defining_object_text_field(define_object='Scale_Connection', label="Scale Connection:",
                                                  add_feature=True, enable=False)

                # with pm.rowLayout(nc=4, columnAttach=[(1, 'right', 0), (2, 'left', 1 * percentage),
                #                                       (3, 'left', 1 * percentage), (4, 'left', 1 * percentage)],
                #                   cw4=(30 * percentage, 18 * percentage, 18 * percentage, 20 * percentage)):
                #     pm.text('Constraint:')
                #     connection_tweak_controller = pm.radioCollection()
                #     point_constraint = pm.radioButton(label='Point',
                #                                           onCommand=lambda x: ad_on_connection_button(1)
                #                                           )
                #     pm.radioButton(label='Orient',
                #                    onCommand=lambda x: ad_on_connection_button(2)
                #                    )
                #     pm.radioButton(label='Parent',
                #                    onCommand=lambda x: ad_on_connection_button(3)
                #                    )
                #     pm.radioCollection(connection_tweak_controller, edit=True, select=point_constraint)

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

def ad_enabling_disabling_ui(object, value, *args):
    # query for enabling and disabling layout
    for item in object:
        objectType = pm.objectTypeUI(item)
        if objectType == 'rowGroupLayout':
            pm.textFieldButtonGrp(item, edit=True, enable=value, tx='')
        else:
            pass

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


def ad_on_selection_button(on):
    # save the current shape selection into global variable
    global on_selector
    on_selector = on

# def ad_on_connection_button(on):
#     # save the current shape selection into global variable
#     global on_connection_select
#     on_connection_select = on

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

# def ad_connection_joint(*args):
#     connection = []
#     # query object with value on shape selector status
#
#     if on_connection_select == 1:
#         connection = ['transConn']
#     elif on_connection_select == 2:
#         connection = ['rotateConn']
#     elif on_connection_select == 3:
#         connection = ['transConn', 'rotateConn']
#     else:
#         pass
#
#     return connection
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
    if pm.textFieldButtonGrp(object_define, q=True, en=True):
        if pm.textFieldButtonGrp(object_define, q=True, tx=True):
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

def ad_query_list_textfield_object(object_define, *args):
    listing_object = []
    if pm.textFieldButtonGrp(object_define, q=True, en=True):
        if pm.textFieldButtonGrp(object_define, q=True, tx=True):
            text = pm.textFieldButtonGrp(object_define, q=True, tx=True)
            listing = text.split(',')
            set_duplicate = set([x for x in listing if listing.count(x) > 1])
            if set_duplicate:
                for item in list(set_duplicate):
                    pm.error('%s is duplicate object!' % item)
            else:
                for item in listing:
                    if pm.ls(item):
                        listing_object.append(item)
                    else:
                        pm.error('%s has wrong input object name.' % object_define, "There is no object with name '%s'!" % item)
        else:
            pm.error('%s can not be empty!' % object_define)
    else:
        pass

    return listing_object, object_define

def ad_create_tweaker(Fk=None,
                      # joints='',
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
        # list_joints = []
        joints = ad_query_list_textfield_object('List_Tweak_Joint')[0]
        tweak_mesh = ad_query_list_textfield_object('Tweak_Mesh')[0]
        main_mesh = ad_query_textfield_object('Main_Mesh')[0]
        scale_connection = ad_query_textfield_object('Scale_Connection')[0]

        all_grp = create_group('transform', "%s%s_%s" % (au.prefix_name(main_mesh), 'AllBpmFk', 'grp'))
        follicle_grp = create_group('transform', "%s%s_%s" % (au.prefix_name(main_mesh), 'FollicleBpmFk', 'grp'))
        drive_grp = create_group('transform', "%s%s_%s" % (au.prefix_name(main_mesh), 'DriveBpmFk', 'grp'))
        ctrl_grp = create_group('transform', "%s%s_%s" % (au.prefix_name(main_mesh), 'ControllerBpmFk', 'grp'))

        list_relatives_allGrp = pm.listRelatives(all_grp, c=1)

        # # for obj in joints:
        # list_relatives_jnt = pm.listRelatives(joints[0], f=1, ad=1)
        # print list_relatives_jnt
        #
        # for item in list_relatives_jnt:
        #     print item
        #     # remove empty list
        #     list_joints = list(filter(None, (item.split('|'))))

        group = create_controller(object_list=joints,
                             groups_ctrl=['Zro', 'Offset'],
                             ctrl_color='turquoiseBlue',
                             shape=ac.JOINT,
                             ctrl_size=1.0,
                             connection=['parent'],
                             lock_channels=[]
                             )
        

        driver_group = group_object_outside('DriverFk', joints)

        for joint, driver in zip(joints, driver_group):
            # create follicle
            follicles = follicle_set(joint, main_mesh)
            follicle.append(follicles['folTrans'])

            # check the attribute root
            # if exist then deleted
            if pm.objExists('%s.root' % joint):
                pm.deleteAttr('%s.root' % joint)
            else:
                # add the attr root and message
                add_attr_message(joint, driver)

            # connected the 'create group' to bind pre matrix
            pm.connectAttr('%s.worldInverseMatrix[0]' % driver,
                           '%s.bindPreMatrix[%d]' % (
                               query_skin_name(tweak_mesh), skin_matrix_list_from_joint(joint)))

            if pm.textFieldButtonGrp('Scale_Connection', q=True, en=True):
                scale_constraint(scale_connection, follicles['folTrans'])

            pm.setAttr(follicles['folShape'] + '.lodVisibility', 0)

            pm.setAttr(joint + '.drawStyle', 2)

            # lock_attr(['t', 'r', 's'], follicles['folTrans'])
            pm.setAttr(follicles['folTrans']+'.translate', l=1)
            pm.setAttr(follicles['folTrans']+'.rotate', l=1)
            pm.setAttr(follicles['folTrans']+'.scale', l=1)

            au.lock_hide_attr_object(follicles['folTrans'], 'v')

            au.lock_hide_attr_object(follicles['folShape'], 'pu')

            au.lock_hide_attr_object(follicles['folShape'], 'pv')

            pm.parent(follicles['folTrans'], follicle_grp)

        for item, (joint, object_grp) in enumerate(zip(follicle, driver_group)):
            parent_scale_constraint(joint, driver_group[item])
            pm.connectAttr(object_grp+'.translate', ctrls[item]+'.translate')
            pm.connectAttr(object_grp+'.rotate', ctrls[item]+'.rotate')
            pm.connectAttr(object_grp+'.scale', ctrls[item]+'.scale')

            # au.connect_attr_object(object_grp, ctrls[item])

        list_relatives_jnt = pm.listRelatives(base_joint, p=True)
        if list_relatives_jnt == None:
            grp_obj = au.group_object(['Zro', 'BPM', 'Null', 'Adjust'], base_joint, base_joint)

            pm.connectAttr('%s.worldInverseMatrix[0]' % array_bpm_folder(base_joint),
                           '%s.bindPreMatrix[%d]' % (
                               query_skin_name(mesh_bpm), skin_matrix_list_from_joint(base_joint)))

            pm.parent(grp_obj[0], ctrl_grp)

        pm.parent(create_grp[0], drive_grp)

        pm.parent(ctrls[0], ctrl_grp)

        if list_relatives_allGrp == None:
            pm.parent(follicle_grp, drive_grp, ctrl_grp, all_grp)

        pm.select(cl=1)

    else:
        print 'Dendra'
        # mc.setAttr(main_mesh + '.visibility', 0)
        #
        # all_grp = create_group('transform', "%s%s_%s" % (au.prefix_name(main_mesh), 'AllBPM', 'grp'))
        # follicle_grp = create_group('transform', "%s%s_%s" % (au.prefix_name(main_mesh), 'ControllerBPM', 'grp'))
        #
        # list_relatives_allGrp = mc.listRelatives(all_grp, c=1)
        #
        # if list_relatives_allGrp == None:
        #     mc.parent(follicle_grp, all_grp)
        #
        # ac.create_controller(object_list=joints,
        #                      groups_ctrl=['Zro', 'BPM', 'Offset'],
        #                      ctrl_color=ctrl_color,
        #                      shape=shape,
        #                      ctrl_size=ctrl_size,
        #                      connection=['parent'],
        #                      lock_channels=[]
        #                      )
        #
        # foll_append = []
        #
        # for object_fol in joints:
        #
        #     # create follicle
        #     follicles = au.follicle_set(object_fol, main_mesh, connect_follicle=connect_mesh)
        #
        #     foll_append.append(follicles['folTrans'])
        #
        #     # sort the list full path object then rid off []
        #     list_relatives_obj = mc.listRelatives(object_fol, ap=1, f=1)[0]
        #
        #     # spliting object |
        #     split_object = filter(None, list_relatives_obj.split('|'))
        #     print split_object
        #
        #     # parent the object to follicle
        #     mc.parent(split_object[0], follicles['folTrans'])
        #
        #     # for scl in scaleObj:
        #     if scale_object:
        #         mc.scaleConstraint(scale_object, follicles['folTrans'])
        #
        #     mc.setAttr(follicles['folShape'] + '.lodVisibility', 0)
        #
        #     mc.setAttr(object_fol + '.drawStyle', 2)
        #
        #     au.lock_hide_attr_object(follicles['folTrans'], 'v')
        #
        #     au.lock_hide_attr_object(follicles['folShape'], 'pu')
        #
        #     au.lock_hide_attr_object(follicles['folShape'], 'pv')
        #
        #     au.lock_attr(['t', 'r', 's'], split_object[1])
        #
        #     au.lock_attr(['t', 'r', 's'], split_object[2])
        #
        #     mc.connectAttr('%s.worldInverseMatrix[0]' % array_bpm_folder(object_fol),
        #                    '%s.bindPreMatrix[%d]' % (
        #                        au.query_skin_name(mesh_bpm), skin_matrix_list_from_joint(object_fol)))
        #
        #     mc.parent(follicles['folTrans'], follicle_grp)
        #
        # list_relatives_jnt = mc.listRelatives(base_joint, p=True)
        # if list_relatives_jnt == None:
        #     grp_obj = au.group_object(['Zro', 'BPM', 'Offset', 'Null'], base_joint, base_joint)
        #
        #     mc.connectAttr('%s.worldInverseMatrix[0]' % array_bpm_folder(base_joint),
        #                    '%s.bindPreMatrix[%d]' % (
        #                        au.query_skin_name(mesh_bpm), skin_matrix_list_from_joint(base_joint)))
        #
        #     mc.parent(grp_obj[0], all_grp)
        #
        # mc.select(cl=1)


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
def group_object_outside(add_suffix, obj_base):
    # create group hierarchy
    grps = []
    for i in obj_base:
        grps.append(mc.createNode('transform', n="%s%s_%s" % (prefix_name(i), add_suffix, 'grp')))

    for i, item in enumerate(obj_base):
        match_position(item, grps[i])

        if i > 0:
            parent_object(grps[i - 1], grps[i])

    return grps

def parent_scale_constraint(obj_base, obj_target, mo=0):
    par_cons = parent_constraint(obj_base, obj_target, mo=mo)
    scl_cons = scale_constraint(obj_base, obj_target)
    return par_cons, scl_cons


def query_skin_name(obj):
    # get the skincluster name
    relatives = mc.listRelatives(obj, type="shape")
    skin_cluster = mc.listConnections(relatives, type="skinCluster")
    if not skin_cluster:
        return mc.error("Please add your skin cluster before run the script!")
    else:
        for obj in skin_cluster:
            return obj

# CREATE FOLLICLE BASED ON OBJECT (JOINT OR TRANSFORM) SELECTED
def create_follicle_selection(obj_select, obj_mesh, prefix=None, suffix=None):
    obj_mesh = mc.listRelatives(obj_mesh, s=1)[0]

    closest_node = None
    # If the inputSurface is of type 'nurbsSurface', connect the surface to the closest node
    if mc.objectType(obj_mesh) == 'nurbsSurface':
        closest_node = mc.createNode('closestPointOnSurface')
        mc.connectAttr((obj_mesh + '.local'), (closest_node + '.inputSurface'))

    # If the inputSurface is of type 'mesh', connect the surface to the closest node
    elif mc.objectType(obj_mesh) == 'mesh':
        closest_node = mc.createNode('closestPointOnMesh')
        mc.connectAttr((obj_mesh + '.outMesh'), (closest_node + '.inMesh'))
    else:
        mc.error('please check your type object. Object must be either nurbs or mesh')

    # query object selection
    xform = mc.xform(obj_select, ws=True, t=True, q=True)

    # set the position of node according to the loc
    mc.setAttr(closest_node + '.inPositionX', xform[0])
    mc.setAttr(closest_node + '.inPositionY', xform[1])
    mc.setAttr(closest_node + '.inPositionZ', xform[2])

    # create follicle
    follicle_node = mc.createNode('follicle')

    # query the transform follicle
    follicle_transform = mc.listRelatives(follicle_node, type='transform', p=True)

    # # connecting the shape follicle to transform follicle
    # dic_connect_follicle(connect_follicle, follicle_node, follicle_transform[0])

    # CONNECTING THE FOLLICLE
    mc.connectAttr(follicle_node + '.outRotate', follicle_transform[0] + '.rotate')
    mc.connectAttr(follicle_node + '.outTranslate', follicle_transform[0]+ '.translate')

    # connect the world matrix mesh to the follicle shape
    mc.connectAttr(obj_mesh + '.worldMatrix[0]', follicle_node + '.inputWorldMatrix')

    # connect the output mesh of mesh to input mesh follicle
    if mc.objectType(obj_mesh) == 'nurbsSurface':
        mc.connectAttr((obj_mesh + '.local'), (follicle_node + '.inputSurface'))

    # If the inputSurface is of type 'mesh', connect the surface to the follicle
    if mc.objectType(obj_mesh) == 'mesh':
        mc.connectAttr(obj_mesh + '.outMesh', follicle_node + '.inputMesh')

    # turn off the simulation follicle
    mc.setAttr(follicle_node + '.simulationMethod', 0)

    # get u and v output closest point on mesh node
    par_u = mc.getAttr(closest_node + '.result.parameterU')
    par_v = mc.getAttr(closest_node + '.result.parameterV')

    # connect output closest point on mesh node to follicle
    mc.setAttr(follicle_node + '.parameterU', par_u)
    mc.setAttr(follicle_node + '.parameterV', par_v)

    # deleting node
    mc.delete(closest_node)

    # rename follicle
    if prefix or suffix:
        follicle_transform = mc.rename(follicle_transform, '%s_%s' % (prefix_name(prefix), suffix))
    else:
        follicle_transform = mc.rename(follicle_transform, '%s_%s' % (prefix_name(obj_select), 'fol'))


    # listing the shape of follicle
    follicle_shape = mc.listRelatives(follicle_transform, s=1)[0]

    return follicle_transform, follicle_shape

def follicle_set(obj_select, obj_mesh, prefix=None, suffix=None,):
    grps = []
    grps.extend(create_follicle_selection(obj_select, obj_mesh, prefix=prefix, suffix=suffix))
    return {'folTrans': grps[0],
            'folShape': grps[1]}

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

def create_ctrl(ctrl_size, shape):
    scale_ctrl = scale_curve(ctrl_size, shape)
    ctrl = controller(scale_ctrl)
    return ctrl

def controller(shape):
    createCrv = mc.curve(d=1, p=shape)
    return createCrv

def scale_curve(size_obj, shape):
    scaleShp = [[size_obj * i for i in j] for j in shape]
    return scaleShp

def parent_object(objBase, objTgt):
    parent_object = mc.parent(objTgt, objBase)
    return parent_object

def grouping_parent(groups, prefix, suffix, number='', side=''):
    # create group hierarchy
    grps = []
    for i in range(len(groups)):
        grps.append(mc.createNode('transform', n="%s%s%s%s%s_%s" % (prefix, suffix, groups[i], number, side, 'grp')))

        if i > 0:
            parent_object(grps[i - 1], grps[i])

    return grps


def group_ctrl(prefix, suffix, groups_ctrl, ctrl, side=''):
    rename_controller = mc.rename(ctrl, '%s_%s' % (ut.prefix_name(prefix), suffix))
    group_parent = grouping_parent(groups_ctrl, '%s' % ut.prefix_name(prefix), suffix.title(), side=side)

    return {'grpPrnt': group_parent,
            'renCtrl': rename_controller}

def set_color(ctrl, color):
    color_dic = {
        'turquoiseBlue': 18,
        'lightPink': 20,
    }
    if color in color_dic.keys():
        list_relatives = mc.listRelatives(ctrl, s=1)[0]
        mc.setAttr(list_relatives + '.ove', 1)
        mc.setAttr(list_relatives + '.ovc', color_dic[color])
        return list_relatives
    else:
        return mc.warning("Could not find %s name color. Please check color name!" % color)

def add_attr_message(obj_target, obj):
    mc.addAttr(obj_target, ln='root', at='message')
    attr = mc.connectAttr('%s.message' % obj, '%s.root' % obj_target)
    return attr

def ctrl_attributes(rename_controller, ctrl_color, grp_parent, lock_channels):
    # color control
    set_color(rename_controller, ctrl_color)
    add_attr_message(rename_controller, grp_parent[0])


def parent_constraint(obj_base, obj_target, mo=1):
    par_constraint = mc.parentConstraint(obj_base, obj_target, mo=mo)[0]
    split = par_constraint.split('_')
    x = '_'.join(split[:-1])
    n = x.replace(x, x + '_pac')
    new_name = [mc.rename(par_constraint, n)]
    return new_name

def scale_constraint(obj_base, obj_target, mo=1):
    scale_constraint = mc.scaleConstraint(obj_base, obj_target, mo=mo)[0]
    split = scale_constraint.split('_')
    x = '_'.join(split[:-1])
    n = x.replace(x, x + '_sc')
    new_name = [mc.rename(scale_constraint, n)]

    return new_name
def match_position(obj_base, obj_target):
    mc.delete(parent_constraint(obj_base, obj_target, mo=0))


def match_scale(obj_base, obj_target):
    mc.delete(scale_constraint(obj_base, obj_target, mo=0))


def create_controller(object_list=None,
             groups_ctrl=['Zro', 'Offset'],
             ctrl_color='turquoiseBlue',
             shape=ac.JOINT,
             ctrl_size=1.0,
             connection=['parent'],
             lock_channels=[]):
    controller = []
    parent_group=[]
    for number, obj in enumerate(object_list):
        # create control
        ctrl = create_ctrl(ctrl_size, shape)

        ctrl_grp = group_ctrl(obj, 'ctrl', groups_ctrl, ctrl)

        parCtrl = parent_object(ctrl_grp['grpPrnt'][-1], ctrl_grp['renCtrl'])
        cnntCtrl = ctrl_grp['renCtrl']

        controller.append(ctrl_grp['renCtrl'])
        parent_group.append(ctrl_grp['grpPrnt'][0])


        # add control attributes
        ctrl_attributes(ctrl_grp['renCtrl'], ctrl_color, ctrl_grp['grpPrnt'], lock_channels)

        # match position the group ctrl as the obj
        match_position(obj, ctrl_grp['grpPrnt'][0])

        # match scale the group ctrl as the obj
        match_scale(obj, ctrl_grp['grpPrnt'][0])

        # connection None
        if connection == None:
            continue

        # connection parent
        # query list relatives
        list_relatives_parent = mc.listRelatives(obj, p=1)

        if list_relatives_parent == None:
            parent_object(cnntCtrl, obj)

        else:
            # parent object to controller
            parent_object(cnntCtrl, obj)
            # parent ctrl group to list relatives
            parent_object(list_relatives_parent, ctrl_grp['grpPrnt'][0])
        # clear selection
        mc.select(cl=1)


    return {'ctrl': controller,
            'group': parent_group}
