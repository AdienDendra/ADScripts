from functools import partial

import pymel.core as pm

SHAPE_CTRL = [[-1.0, 1.0, 1.0], [-1.0, 1.0, -1.0], [1.0, 1.0, -1.0], [1.0, 1.0, 1.0], [-1.0, 1.0, 1.0], [-1.0, -1.0, 1.0],
        [-1.0, -1.0, -1.0], [-1.0, 1.0, -1.0], [-1.0, 1.0, 1.0], [-1.0, -1.0, 1.0], [1.0, -1.0, 1.0], [1.0, 1.0, 1.0],
        [1.0, 1.0, -1.0], [1.0, -1.0, -1.0], [1.0, -1.0, 1.0], [1.0, -1.0, -1.0], [-1.0, -1.0, -1.0]]

layout = 400
percentage = 0.01 * layout
on_selector = 0
method_radio_button =1

def ad_show_ui():
    adien_tweak_ctrl = 'AD_TweakControllerTool'
    pm.window(adien_tweak_ctrl, exists=True)
    if pm.window(adien_tweak_ctrl, exists=True):
        pm.deleteUI(adien_tweak_ctrl)
    with pm.window(adien_tweak_ctrl, title='AD Tweak Controller Tool', width=400, height=400):
        with pm.tabLayout('tab', width=410, height=160):
            # CREATE TAB
            with pm.columnLayout('Create Tweak Controller', rowSpacing=1 * percentage, w=layout,
                                 co=('both', 1 * percentage)):
                pm.separator(h=10, st="in", w=layout)
                with pm.rowLayout(nc=3, columnAttach=[(1, 'right', 0), (2, 'left', 1 * percentage),
                                                      (3, 'left', 1 * percentage)],
                                  cw3=(29.5 * percentage, 30 * percentage, 30 * percentage,
                                       )
                                  ):
                    pm.text('Tweak Method:')
                    method_radio_button = pm.radioCollection()
                    method_joint_hierarchy = pm.radioButton(label='Hierarchy Joint',
                                                            onCommand=lambda x: ad_on_selection_button(1)
                                                            )
                    pm.radioButton(label='Non-Hierarchy Joint',
                                   onCommand=lambda x: ad_on_selection_button(2)
                                   )

                ad_defining_object_text_field(define_object='List_Tweak_Joint', label="List Tweak Joint:",
                                              multiple_selection=True)

                pm.radioCollection(method_radio_button, edit=True, select=method_joint_hierarchy)

                ad_defining_object_text_field(define_object='Tweak_Mesh', label="Tweak Mesh:")

                ad_defining_object_text_field(define_object='Main_Mesh', label="Main Mesh:")

                # ad_defining_object_text_field(define_object='Static_Joint', label="Static Joint:")
                with pm.rowColumnLayout(nc=2, rowSpacing=(2, 1 * percentage),
                                        co=(1 * percentage, 'both', 1 * percentage),
                                        cw=[(1, 3 * percentage), (2, 93 * percentage)]):
                    pm.checkBox(label='',
                                cc=partial(ad_enabling_disabling_ui, ['Scale_Connection']),
                                value=False)
                    ad_defining_object_text_field(define_object='Scale_Connection', label="Scale Connection:",
                                                  add_feature=True, enable=False)

                with pm.rowLayout(nc=2, cw2=(48 * percentage, 48 * percentage), cl2=('center', 'left'),
                                  columnAttach=[(1, 'both', 0.5 * percentage), (2, 'both', 0.5 * percentage)]):
                    pm.button(l="Clear All Define Objects", bgc=(1, 1, 0),
                              c=partial(ad_clearing_all_text_field, 'List_Tweak_Joint', 'Tweak_Mesh',
                                        'Main_Mesh', 'Scale_Connection'))

                    # create button to delete last pair of text fields
                    pm.button("create_tweak_controller", l="Create Tweak Controller", bgc=(0, 0.5, 0),
                              c=partial(ad_create_tweak_controller)
                              )
                pm.separator(h=10, st="in", w=layout)
                with pm.rowLayout(nc=2, cw2=(49 * percentage, 49 * percentage), cl2=('center', 'center'),
                                  columnAttach=[(1, 'both', 2 * percentage), (2, 'both', 2 * percentage)]):
                    pm.text(l='Adien Dendra | 11/2020', al='left')
                    pm.text(
                        l='<a href="http://projects.adiendendra.com/ad-universal-fkik-setup-tutorial/">find out how to use it! >> </a>',
                        hl=True,
                        al='right')

            # EDIT TAB
            with pm.columnLayout('Reconnect Tweak Controller', rowSpacing=1 * percentage, w=layout,
                                 co=('both', 1 * percentage), adj=1):
                pm.separator(h=10, st="in", w=layout)

                ad_defining_object_text_field(define_object='Reconnect_List_Tweak_Joint', label="List Tweak Joint:",
                                              multiple_selection=True)
                ad_defining_object_text_field(define_object='Reconnect_Tweak_Mesh', label="Tweak Mesh:")

                with pm.rowLayout(nc=3, cw3=(32 * percentage, 32 * percentage, 32 * percentage),
                                  columnAttach=[(1, 'both', 0 * percentage), (2, 'both', 0 * percentage),
                                                (3, 'both', 0 * percentage)]
                                  ):
                    pm.button(l="Clear Define Objects", bgc=(1, 1, 0),
                              c=partial(ad_clearing_all_text_field, 'Reconnect_List_Tweak_Joint', 'Reconnect_Tweak_Mesh'))
                    # create button to delete last pair of text fields
                    pm.button('disconnect_tweak_controller', l="Disconnect Tweak Ctrl", bgc=(0.5, 0, 0),
                              c=partial(ad_disconnect_tweak_controller)
                              )
                    # create button to delete last pair of text fields
                    pm.button("reconnect_tweak_controller", l="Reconnect Tweak Ctrl", bgc=(0, 0, 0.5),
                              c=partial(ad_reconnect_tweak_controller)
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
    ad_clearing_all_text_field(['List_Tweak_Joint'])

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

def ad_clearing_all_text_field(*args):
    # clearing object text field
    for object in args:
        if object:
            pm.textFieldButtonGrp(object, edit=True, tx='')
        else:
            pass


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
                pm.error("'%s' has wrong input object name. There is no object with name '%s'!" % (object_define, text))
        else:
            pm.error("'%s' can not be empty!" % object_define)
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
                    pm.error("'%s' is duplicate object!" % item)
            else:
                for item in listing:
                    if pm.ls(item):
                        listing_object.append(item)
                    else:
                        pm.error("'%s' has wrong input object name. There is no object with name '%s'!" % (object_define, item))
        else:
            pm.error("'%s' can not be empty!" % object_define)
    else:
        pass

    return listing_object, object_define


def ad_create_tweak_controller(*args):
    # text group define
    joints = ad_query_list_textfield_object('List_Tweak_Joint')[0]
    tweak_mesh = ad_query_list_textfield_object('Tweak_Mesh')[0]
    main_mesh = ad_query_textfield_object('Main_Mesh')[0]
    scale_connection = ad_query_textfield_object('Scale_Connection')[0]

    # checking the skin with joint
    ad_query_object_skin_influence(tweak_mesh, joints)
    # query skin exists on mesh
    ad_query_skin_name(tweak_mesh)

    # checking the method type
    list_joint = pm.ls(joints)

    if ad_hierarchy_joint():
        ad_tweak_hierarchy_condition(list_joint, main_mesh, scale_connection, tweak_mesh)
    else:
        ad_tweak_non_hierarchy_condition(list_joint, main_mesh, scale_connection, tweak_mesh)

def ad_tweak_non_hierarchy_condition(list_joint, main_mesh, scale_connection, tweak_mesh):
    for joint in list_joint:
        parents = joint.getParent()
        children = joint.getChildren()
        if pm.ls(parents, type='joint') or pm.ls(children, type='joint'):
            pm.error("Joint '%s' shouldn't have a hierarchy, check your Tweak Method option!" % joint)
        else:
            if pm.objExists("%s.AD_Parent_Grp" % joint):
                if pm.listConnections(joint + '.AD_Parent_Grp'):
                    pm.error("Tweak controller '%s' already added!" % joint)
                else:
                    ad_create_tweak_non_hierarchy_controller(joint, main_mesh, scale_connection, tweak_mesh)
            else:
                ad_create_tweak_non_hierarchy_controller(joint, main_mesh, scale_connection, tweak_mesh)

def ad_tweak_hierarchy_condition(list_joint, main_mesh, scale_connection, tweak_mesh):
    if len(list_joint) > 1:
        # create exception
        for joint in list_joint:
            if pm.objExists("%s.AD_Parent_Grp" % joint):
                if pm.listConnections(joint + '.AD_Parent_Grp'):
                    pm.error("Tweak controller '%s' already added!" % joint)
                else:
                    continue
            else:
                continue

        for joint_child in list_joint[:-1]:
            children = joint_child.getChildren()
            if not pm.ls(children, type='joint'):
                pm.error("Joint '%s' should have a hierarchy, check your Tweak Method option!" % joint_child)
            else:
                continue
        for joint_parent in list_joint[1:]:
            parent = joint_parent.getParent()
            if not pm.ls(parent, type='joint'):
                pm.error("Joint '%s' should have a hierarchy, check your Tweak Method option!" % joint_parent)
            else:
                continue

        # create group
        all_grp = ad_create_group('transform', "%s_%s" % ('AllTweakCtrl_HJ', 'grp'))
        follicle_grp = ad_create_group('transform', "%s_%s" % ('FollicleTweakCtrl_HJ', 'grp'))
        drive_grp = ad_create_group('transform', "%s_%s" % ('DriverTweakCtrl_HJ', 'grp'))
        ctrl_grp = ad_create_group('transform', "%s_%s" % ('ControllerTweakCtrl_HJ', 'grp'))
        driver_group = ad_group_object_outside('DriverHJ', list_joint)

        # create controller
        controller = ad_create_controller(object_list=list_joint,
                                          ctrl_color=20,
                                          )
        # parenting to group
        pm.parent(controller['group'][0], ctrl_grp)
        pm.parent(driver_group[0], drive_grp)
        pm.parent(follicle_grp, drive_grp, ctrl_grp, all_grp)

        # looping the object
        for joint, driver, controller in zip (list_joint, driver_group, controller['group']):
            ad_create_tweak_hierarchy_controller(joint, main_mesh, scale_connection, tweak_mesh, driver, controller, follicle_grp)

    else:
        for joint in list_joint:
            if pm.objExists("%s.AD_Parent_Grp" % joint):
                if pm.listConnections(joint + '.AD_Parent_Grp'):
                    pm.error("Tweak controller '%s' already added!" % joint)
                else:
                    pm.error("Joint '%s' shouldn't as a single joint input, check your Tweak Method option!" % list_joint[0])

            else:
                pm.error(
                    "Joint '%s' shouldn't as a single joint input, check your Tweak Method option!" % list_joint[0])

def ad_create_tweak_hierarchy_controller(joints, main_mesh, scale_connection, tweak_mesh, driver, controller, follicle_grp):
        # create follicle
        follicles = ad_follicle_set(joints, main_mesh)

        # add attribute
        ad_add_attr_message(joints, driver)

        # connected the bind pre matrix
        pm.connectAttr('%s.worldInverseMatrix[0]' % driver,
                       '%s.bindPreMatrix[%d]' % (
                           ad_query_skin_name(tweak_mesh), ad_skin_matrix_list_from_joint(joints)))

        if pm.textFieldButtonGrp('Scale_Connection', q=True, en=True):
            ad_scale_constraint(scale_connection, follicles['folTrans'])

        # hide visibility
        pm.setAttr(follicles['folShape'] + '.lodVisibility', 0)
        pm.setAttr(joints + '.drawStyle', 2)

        # lock_attr
        pm.setAttr(follicles['folTrans'] + '.translate', l=1)
        pm.setAttr(follicles['folTrans'] + '.rotate', l=1)
        pm.setAttr(follicles['folTrans'] + '.scale', l=1)
        pm.setAttr('%s.%s' % (follicles['folTrans'], 'v'), l=True, k=False)
        pm.setAttr('%s.%s' % (follicles['folTrans'], 'pu'), l=True, k=False)
        pm.setAttr('%s.%s' % (follicles['folTrans'], 'pv'), l=True, k=False)

        pm.parent(follicles['folTrans'], follicle_grp)
        # constraining
        ad_parent_scale_constraint(follicles['folTrans'], driver)

        # connect attribute
        pm.connectAttr(driver + '.translate', controller + '.translate')
        pm.connectAttr(driver + '.rotate', controller + '.rotate')
        pm.connectAttr(driver + '.scale', controller + '.scale')

def ad_create_tweak_non_hierarchy_controller(joint, main_mesh, scale_connection, tweak_mesh):

        all_grp = ad_create_group('transform', "%s_%s" % ('AllTweakCtrl_NonHJ', 'grp'))
        controller = ad_create_controller(object_list=[joint],
                                          ctrl_color=18,
                                          )

        # for list_joint, group_ctrl in zip(list_joint, controller['group']):
        # create follicle
        follicles = ad_follicle_set(joint, main_mesh)

        # # parent the object to follicle
        pm.parent(controller['group'], follicles['folTrans'])

        # for scl in scaleObj:
        if pm.textFieldButtonGrp('Scale_Connection', q=True, en=True):
            ad_scale_constraint(scale_connection, follicles['folTrans'])

        # add attribute
        ad_add_attr_message(joint, controller['group'][0])

        pm.setAttr(follicles['folShape'] + '.lodVisibility', 0)
        pm.setAttr(joint + '.drawStyle', 2)

        pm.setAttr(follicles['folTrans'] + '.translate', l=1)
        pm.setAttr(follicles['folTrans'] + '.rotate', l=1)
        pm.setAttr('%s.%s' % (follicles['folTrans'], 'v'), l=True, k=False)
        pm.setAttr('%s.%s' % (follicles['folTrans'], 'pu'), l=True, k=False)
        pm.setAttr('%s.%s' % (follicles['folTrans'], 'pv'), l=True, k=False)

        pm.setAttr(controller['group'][0] + '.translate', l=1)
        pm.setAttr(controller['group'][0] + '.rotate', l=1)
        pm.setAttr(controller['group'][0] + '.scale', l=1)

        pm.connectAttr('%s.worldInverseMatrix[0]' % ad_array_tweak_folder(follicles['folTrans']),
                       '%s.bindPreMatrix[%d]' % (
                           ad_query_skin_name(tweak_mesh), ad_skin_matrix_list_from_joint(joint)))

        pm.parent(follicles['folTrans'], all_grp)

        print "Tweak controller '%s' has been created!" % joint

################################################# reconnect tweak controller ##################################################
def ad_reconnect_tweak_controller(*args):
    ad_reconnect_or_disconnect_looping(reconnect=True)

def ad_disconnect_tweak_controller(*args):
    ad_reconnect_or_disconnect_looping(reconnect=False)

def ad_reconnect_or_disconnect_looping(reconnect):
    joints = ad_query_list_textfield_object('Reconnect_List_Tweak_Joint')[0]
    tweak_mesh = ad_query_list_textfield_object('Reconnect_Tweak_Mesh')[0]

    # checking the skin with joint
    ad_query_object_skin_influence(tweak_mesh, joints)
    # query skin exists on mesh
    ad_query_skin_name(tweak_mesh)

    for joint in joints:

        # listing the connection exists
        grp_driver = pm.listConnections(joint + '.AD_Parent_Grp', s=1)

        # query whether it has contain parent hook
        if not grp_driver:
            pm.error("Tweak controller '%s' doesn't exists! Create setup first or delete existing setup before create tweaker." % joint)

        # query list connection
        list_connection = pm.listConnections('%s.worldInverseMatrix[0]' % grp_driver[0], p=1)

        # got error if it has connection
        if reconnect:
            if list_connection:
                pm.warning("Tweak controller '%s' already has connected! Skip that tweak controller." % joint)

            else:
                # connect the bpm transform to skin bind pre matrix
                pm.connectAttr('%s.worldInverseMatrix[0]' % grp_driver[0],
                               '%s.bindPreMatrix[%d]' % (
                                   ad_query_skin_name(tweak_mesh), ad_skin_matrix_list_from_joint(joint)))
                print ("Tweak controller '%s' is reconnected!" % joint)
        else:
            # condition if it has connection
            if list_connection:
                pm.disconnectAttr('%s.worldInverseMatrix[0]' % grp_driver[0], list_connection[0])
                print ("Tweak controller '%s' is disconnected!" % joint)

            else:
                pm.warning(
                    "Tweak controller '%s' already has disconnected! Skip that tweak controller." % joint)


############################################## function tweak controller ###############################################
def ad_suffix_name(obj):
    objs = obj.split('|')[-1:]
    for l in objs:
        get_len = l.split('_')
        if len(get_len) > 1:
            get_suffix_name = get_len[1]
            return get_suffix_name
        else:
            get_suffix_no = l.replace(l, '')
            return get_suffix_no


def ad_group_object(grp_name_list, obj_base):
    list_relatives = pm.listRelatives(obj_base, ap=1)

    cGrp = ad_grouping_parent(grp_name_list, ad_prefix_name(obj_base), ad_suffix_name(obj_base).title())

    if list_relatives == None:
        pm.parent(obj_base, cGrp[-1])
    else:
        # parent group offset to list relatives
        pm.parent(cGrp[0], list_relatives)
        # parent obj to grp offset
        pm.parent(obj_base, cGrp[-1])

    return cGrp


def ad_group_object_outside(add_suffix, obj_base):
    # create group hierarchy
    grps = []
    for i in obj_base:
        grps.append(pm.createNode('transform', n="%s%s_%s" % (ad_prefix_name(i), add_suffix, 'grp')))

    for i, item in enumerate(obj_base):
        pm.delete(pm.parentConstraint(item, grps[i], mo=0))

        if i > 0:
            pm.parent(grps[i], grps[i - 1])

    return grps


def ad_parent_scale_constraint(obj_base, obj_target, mo=1):
    ad_parent_constraint(obj_base, obj_target, mo=mo)
    ad_scale_constraint(obj_base, obj_target)


def ad_query_skin_name(obj):
    # get the skincluster name
    relatives = pm.listRelatives(obj, type="shape")
    skin_cluster = pm.listConnections(relatives, type="skinCluster")
    if not skin_cluster:
        return pm.error("Please add bind skin to '%s' before create or reconnect or disconnect tweak controller!" % obj[0])
    else:
        return skin_cluster[0]

def ad_query_object_skin_influence(object_mesh, joints):
    skin_cluster = ad_query_skin_name(object_mesh)
    query_object_influence = pm.skinCluster(skin_cluster, query=True, inf=True)
    for joint in joints:
        if not joint in query_object_influence:
            pm.error("Joint '%s' doesn't have influence bind skin to '%s' mesh!" % (joint, object_mesh[0]))

    return query_object_influence

# CREATE FOLLICLE BASED ON OBJECT (JOINT OR TRANSFORM) SELECTED
def ad_create_follicle_selection(obj_select, obj_mesh, prefix=None, suffix=None):
    obj_mesh = pm.listRelatives(obj_mesh, s=1)[0]

    closest_node = None
    # If the inputSurface is of type 'nurbsSurface', connect the surface to the closest node
    if pm.objectType(obj_mesh) == 'nurbsSurface':
        closest_node = pm.createNode('closestPointOnSurface')
        pm.connectAttr((obj_mesh + '.local'), (closest_node + '.inputSurface'))

    # If the inputSurface is of type 'mesh', connect the surface to the closest node
    elif pm.objectType(obj_mesh) == 'mesh':
        closest_node = pm.createNode('closestPointOnMesh')
        pm.connectAttr((obj_mesh + '.outMesh'), (closest_node + '.inMesh'))
    else:
        pm.error('please check your type object. Object must be either nurbs or mesh')

    # query object selection
    xform = pm.xform(obj_select, ws=True, t=True, q=True)

    # set the position of node according to the loc
    pm.setAttr(closest_node + '.inPositionX', xform[0])
    pm.setAttr(closest_node + '.inPositionY', xform[1])
    pm.setAttr(closest_node + '.inPositionZ', xform[2])

    # create follicle
    follicle_node = pm.createNode('follicle')

    # query the transform follicle
    follicle_transform = pm.listRelatives(follicle_node, type='transform', p=True)

    # CONNECTING THE FOLLICLE
    pm.connectAttr(follicle_node + '.outRotate', follicle_transform[0] + '.rotate')
    pm.connectAttr(follicle_node + '.outTranslate', follicle_transform[0] + '.translate')

    # connect the world matrix mesh to the follicle shape
    pm.connectAttr(obj_mesh + '.worldMatrix[0]', follicle_node + '.inputWorldMatrix')

    # connect the output mesh of mesh to input mesh follicle
    if pm.objectType(obj_mesh) == 'nurbsSurface':
        pm.connectAttr((obj_mesh + '.local'), (follicle_node + '.inputSurface'))

    # If the inputSurface is of type 'mesh', connect the surface to the follicle
    if pm.objectType(obj_mesh) == 'mesh':
        pm.connectAttr(obj_mesh + '.outMesh', follicle_node + '.inputMesh')

    # turn off the simulation follicle
    pm.setAttr(follicle_node + '.simulationMethod', 0)

    # get u and v output closest point on mesh node
    par_u = pm.getAttr(closest_node + '.result.parameterU')
    par_v = pm.getAttr(closest_node + '.result.parameterV')

    # connect output closest point on mesh node to follicle
    pm.setAttr(follicle_node + '.parameterU', par_u)
    pm.setAttr(follicle_node + '.parameterV', par_v)

    # deleting node
    pm.delete(closest_node)

    # rename follicle
    if prefix or suffix:
        follicle_transform = pm.rename(follicle_transform, '%s_%s' % (ad_prefix_name(prefix), suffix))
    else:
        follicle_transform = pm.rename(follicle_transform, '%s_%s' % (ad_prefix_name(obj_select), 'fol'))

    # listing the shape of follicle
    follicle_shape = pm.listRelatives(follicle_transform, s=1)[0]
    pm.setAttr(follicle_shape + '.rsp', k=False)
    pm.setAttr(follicle_shape + '.ptl', k=False)
    pm.setAttr(follicle_shape + '.sim', k=False)
    pm.setAttr(follicle_shape + '.sdr', k=False)
    pm.setAttr(follicle_shape + '.fld', k=False)
    pm.setAttr(follicle_shape + '.ovd', k=False)
    pm.setAttr(follicle_shape + '.cld', k=False)
    pm.setAttr(follicle_shape + '.dmp', k=False)
    pm.setAttr(follicle_shape + '.stf', k=False)
    pm.setAttr(follicle_shape + '.lfl', k=False)
    pm.setAttr(follicle_shape + '.cwm', k=False)
    pm.setAttr(follicle_shape + '.sct', k=False)
    pm.setAttr(follicle_shape + '.ad', k=False)
    pm.setAttr(follicle_shape + '.dml', k=False)
    pm.setAttr(follicle_shape + '.ctf', k=False)
    pm.setAttr(follicle_shape + '.brd', k=False)
    pm.setAttr(follicle_shape + '.cbl', k=False)
    pm.setAttr(follicle_shape + '.cr', k=False)
    pm.setAttr(follicle_shape + '.cg', k=False)
    pm.setAttr(follicle_shape + '.fsl', k=False)
    pm.setAttr(follicle_shape + '.sgl', k=False)
    pm.setAttr(follicle_shape + '.sdn', k=False)
    pm.setAttr(follicle_shape + '.dgr', k=False)
    pm.setAttr(follicle_shape + '.cw', k=False)
    pm.setAttr(follicle_shape + '.cml', k=False)
    pm.setAttr(follicle_shape + '.cb', k=False)

    return follicle_transform, follicle_shape

def ad_follicle_set(obj_select, obj_mesh, prefix=None, suffix=None, ):
    grps = []
    grps.extend(ad_create_follicle_selection(obj_select, obj_mesh, prefix=prefix, suffix=suffix))
    return {'folTrans': grps[0],
            'folShape': grps[1]}


def ad_joint_destination_matrix(obj):
    list_connection = pm.listConnections(obj + '.worldMatrix[0]', p=True)
    return list_connection


def ad_skin_matrix_list_from_joint(obj):
    for item in ad_joint_destination_matrix(obj):
        split = item.split('.')[1:]
        integer = int((split[0].split('[')[-1][:-1]))
        return integer


def ad_array_tweak_folder(obj):
    list = pm.ls(obj)
    for node in list:
        children = node.getChildren()
        return children[1]


def ad_create_group(node, name):
    if not pm.objExists(name):
        node_name = pm.createNode(node, n=name)
        return node_name
    else:
        return name


def ad_create_ctrl(shape):
    ctrl = pm.curve(d=1, p=shape)
    return ctrl


def ad_grouping_parent(groups, prefix, suffix, number=''):
    # create group hierarchy
    grps = []
    for i in range(len(groups)):
        grps.append(pm.createNode('transform', n="%s%s%s%s_%s" % (prefix, suffix, groups[i], number, 'grp')))
        if i > 0:
            pm.parent(grps[i], grps[i - 1])
    return grps


def ad_prefix_name(obj):
    if '_' in obj:
        get_prefix_name = obj.split('_')[:-1]
        joining = '_'.join(get_prefix_name)
        return joining
    else:
        print obj


def ad_set_color(ctrl, color):
    list_relatives = pm.listRelatives(ctrl, s=1)[0]
    pm.setAttr(list_relatives + '.ove', 1)
    pm.setAttr(list_relatives + '.ovc', color)
    return list_relatives


def ad_add_attr_message(obj_target, obj):
    if pm.objExists('%s.AD_Parent_Grp' % obj_target):
        attr = pm.connectAttr('%s.message' % obj, '%s.AD_Parent_Grp' % obj_target)
    else:
        pm.addAttr(obj_target, ln='AD_Parent_Grp', at='message')
        attr = pm.connectAttr('%s.message' % obj, '%s.AD_Parent_Grp' % obj_target)
    return attr


def ctrl_attributes(rename_controller, ctrl_color, grp_parent):
    ad_set_color(rename_controller, ctrl_color)
    ad_add_attr_message(rename_controller, grp_parent[0])


def ad_parent_constraint(obj_base, obj_target, mo=1):
    par_constraint = pm.parentConstraint(obj_base, obj_target, mo=mo)
    split = par_constraint.split('_')
    x = '_'.join(split[:-1])
    n = x.replace(x, x + '_pac')
    pm.rename(par_constraint, n)


def ad_scale_constraint(obj_base, obj_target, mo=1):
    scale_constraint = pm.scaleConstraint(obj_base, obj_target, mo=mo)
    split = scale_constraint.split('_')
    x = '_'.join(split[:-1])
    n = x.replace(x, x + '_sc')
    pm.rename(scale_constraint, n)


def ad_create_controller(object_list=None,
                         groups_ctrl=['Zro', 'Offset'],
                         ctrl_color=20,
                         shape=SHAPE_CTRL,
                         ):
    controllers = []
    parent_groups = []
    for number, obj in enumerate(object_list):
        # create control
        creating_ctrl = ad_create_ctrl(shape)
        controller = pm.rename(creating_ctrl, '%s_%s' % (ad_prefix_name(obj), 'ctrl'))
        parent_group = ad_grouping_parent(groups_ctrl, ad_prefix_name(obj), 'ctrl'.title())

        # ctrl_grp = group_ctrl(obj, 'ctrl', groups_ctrl, ctrl)
        pm.parent(controller, parent_group[-1])

        controllers.append(controller)
        parent_groups.append(parent_group[0])

        # add control attributes
        ctrl_attributes(controller, ctrl_color, parent_group)

        # match position the group ctrl as the obj
        pm.delete(pm.parentConstraint(obj, parent_group[0], mo=0))

        # connection parent
        # query list relatives
        list_relatives_parent = pm.listRelatives(obj, p=1)
        pm.parent(obj, controller)

        if list_relatives_parent:
            # parent ctrl group to list relatives
            pm.parent(parent_group[0], list_relatives_parent[0])

    return {'ctrl': controllers,
            'group': parent_groups}
