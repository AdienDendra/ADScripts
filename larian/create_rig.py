import pymel.core as pm
import maya.cmds as mc
import maya.OpenMaya as om
from functools import partial
import re
from string import digits

CIRCLE = [[1.006715677346795, -0.0006702548752642524, -3.694798373504726e-15],
          [0.9942995854608142, -0.15846311195050425, -3.5110803153770576e-15],
          [0.957352671256412, -0.31236840627503687, -3.4555691641457997e-15],
          [0.8967790190942225, -0.4585990289160014, -3.2890357104520263e-15],
          [0.8140753908601714, -0.593558733194448, -3.4416913763379853e-15],
          [0.7112809990565734, -0.7139124523578333, -3.552713678800501e-15],
          [0.5909272798931885, -0.816706844161434, -3.524958103184872e-15],
          [0.45596757561474005, -0.8994104723954811, -3.58046925441613e-15],
          [0.309736952973776, -0.9599841245576726, -3.552713678800501e-15],
          [0.15583165864924373, -0.9969310387620733, -3.552713678800501e-15],
          [-0.001961198425996145, -1.009347130648053, -3.552713678800501e-15],
          [-0.15975405550123625, -0.9969310387620733, -3.552713678800501e-15],
          [-0.31365934982576843, -0.9599841245576726, -3.552713678800501e-15],
          [-0.45988997246673363, -0.8994104723954811, -3.58046925441613e-15],
          [-0.59484967674518, -0.8167068441614339, -3.4139358007223564e-15],
          [-0.7152033959085659, -0.7139124523578333, -3.552713678800501e-15],
          [-0.8179977877121639, -0.5935587331944481, -3.7192471324942744e-15],
          [-0.9007014159462143, -0.45859902891600135, -3.4416913763379853e-15],
          [-0.9612750681084048, -0.31236840627503687, -3.3584246494910985e-15],
          [-0.9982219823128072, -0.15846311195050422, -3.427813588530171e-15],
          [-1.0106380741987873, -0.0006702548752642523, -3.462480952995395e-15],
          [-0.9982219823128072, 0.15712260219997573, -3.4139358007223564e-15],
          [-0.9612750681084048, 0.3110278965245084, -3.2751579226442118e-15],
          [-0.9007014159462143, 0.45725851916547167, -3.3584246494910985e-15],
          [-0.8179977877121639, 0.5922182234439194, -3.552713678800501e-15],
          [-0.7152033959085659, 0.712571942607305, -3.3584246494910985e-15],
          [-0.59484967674518, 0.8153663344109039, -3.164135620181696e-15],
          [-0.45988997246673363, 0.8980699626449538, -3.469446951953614e-15],
          [-0.31365934982576843, 0.9586436148071453, -3.552713678800501e-15],
          [-0.15975405550123625, 0.9955905290115453, -3.469446951953614e-15],
          [-0.001961198425996145, 1.008006620897526, -3.3861802251067274e-15],
          [0.15583165864924373, 0.9955905290115453, -3.469446951953614e-15],
          [0.309736952973776, 0.9586436148071452, -3.497202527569243e-15],
          [0.45596757561474005, 0.8980699626449536, -3.4139358007223564e-15],
          [0.5909272798931885, 0.815366334410904, -3.3584246494910985e-15],
          [0.7112809990565734, 0.712571942607305, -3.469446951953614e-15],
          [0.8140753908601714, 0.5922182234439194, -3.4416913763379853e-15],
          [0.8967790190942225, 0.45725851916547183, -3.1780134079895106e-15],
          [0.957352671256412, 0.31102789652450846, -3.427813588530171e-15],
          [0.9942995854608142, 0.15712260219997573, -3.5110803153770576e-15],
          [1.006715677346795, -0.0006702548752642524, -3.694798373504726e-15]]
STAR = [[0.29029436932199354, 4.354415539829906, -6.661338147750939e-16],
        [0.0, 5.902652176213871, -1.1102230246251565e-15], [-0.29029436932199354, 4.354415539829906, -6.661338147750939e-16],
        [-0.43544155398299034, 3.918973985846915, -3.3306690738754696e-16],
        [-0.7741183181919832, 2.9513260881069354, -5.551115123125783e-16],
        [-1.1127950824009758, 2.322354954575948, -8.881784197001252e-16],
        [-1.5966190312709652, 1.5966190312709654, 5.551115123125783e-17],
        [-2.3223549545759483, 1.1127950824009756, -5.551115123125783e-17],
        [-2.9997084829939347, 0.7741183181919832, -2.498001805406602e-16],
        [-3.870591590959915, 0.4354415539829902, 2.7755575615628914e-17],
        [-4.402797934716903, 0.2902943693219935, -1.1102230246251565e-16],
        [-5.757504991552873, 0.0, 0.0], [-4.402797934716903, -0.2902943693219935, 1.1102230246251565e-16],
        [-3.870591590959915, -0.4354415539829902, -2.7755575615628914e-17],
        [-2.9997084829939347, -0.7741183181919832, 2.498001805406602e-16],
        [-2.3223549545759483, -1.1127950824009756, 5.551115123125783e-17],
        [-1.5966190312709652, -1.5966190312709654, -5.551115123125783e-17],
        [-1.1127950824009758, -2.322354954575948, 8.881784197001252e-16],
        [-0.7741183181919832, -2.9997084829939347, 2.220446049250313e-16],
        [-0.43544155398299034, -3.8705915909599153, -3.3306690738754696e-16],
        [-0.29029436932199354, -4.402797934716903, 4.440892098500626e-16],
        [0.0, -5.757504991552872, 4.440892098500626e-16],
        [0.29029436932199354, -4.402797934716903, 4.440892098500626e-16],
        [0.43544155398299034, -3.8705915909599153, -3.3306690738754696e-16],
        [0.7741183181919832, -2.9997084829939347, 2.220446049250313e-16],
        [1.1127950824009758, -2.322354954575948, 8.881784197001252e-16],
        [1.5966190312709652, -1.5966190312709654, -5.551115123125783e-17],
        [2.3223549545759483, -1.1127950824009756, 5.551115123125783e-17],
        [2.9997084829939347, -0.7741183181919832, 2.498001805406602e-16],
        [3.870591590959915, -0.4354415539829902, -2.7755575615628914e-17],
        [4.402797934716903, -0.2902943693219935, 1.1102230246251565e-16], [5.757504991552873, 0.0, 0.0],
        [4.402797934716903, 0.2902943693219935, -1.1102230246251565e-16],
        [3.870591590959915, 0.4354415539829902, 2.7755575615628914e-17],
        [2.9997084829939347, 0.7741183181919832, -2.498001805406602e-16],
        [2.3223549545759483, 1.1127950824009756, -5.551115123125783e-17],
        [1.5966190312709652, 1.5966190312709654, 5.551115123125783e-17],
        [1.1127950824009758, 2.322354954575948, -8.881784197001252e-16],
        [0.7741183181919832, 2.9513260881069354, -5.551115123125783e-16],
        [0.48382394886998936, 3.7254444062989176, -1.1102230246251565e-16],
        [0.29029436932199354, 4.354415539829906, -6.661338147750939e-16],
        [0.29029436932199354, 4.354415539829906, -6.661338147750939e-16],
        [0.29029436932199354, 4.354415539829906, -6.661338147750939e-16],
        [0.29029436932199354, 4.354415539829906, -6.661338147750939e-16]]

layout = 200
percentage = 0.01 * layout
#**********************************************************************************************************************#
#                                                         UI                                                           #
#**********************************************************************************************************************#
def show_ui():
    snake_rig = 'Larian_Ui'
    pm.window(snake_rig, exists=True)
    if pm.window(snake_rig, exists=True):
        pm.deleteUI(snake_rig)
    with pm.window(snake_rig, title='Larian Rig Test Adien', width=layout, height=200):
        with pm.columnLayout('Create__Column', w=layout*1.04, co=('both', 1 * percentage), adj=1):
            # ADDITIONAL
            with pm.rowLayout(nc=2, cw2=(85 * percentage, 15 * percentage), cl2=('right','right'),
                              columnAttach=[(1, 'both', 0),(2, 'both', 0)],
                              rowAttach=[(1, 'top', 4),(2, 'top', 4) ]):
                pm.button('Create_Template', l="Create Template Joint",
                          c=partial(Lr_Template))
                pm.button('Delete_Template', l="Del",  bgc=(0.5, 0, 0), c=partial(lr_delete_template))
            # with pm.rowLayout(nc=1, cw=(1, 100 * percentage), cal=(1, 'right'), columnAttach=(1, 'both', 0),
            #                   rowAttach=[(1, 'top', 1)]):
            #     pm.button('Delete_Template', l="Del",
            #               c=partial(lr_delete_template))

            pm.separator(h=8, st="in", w=90 * percentage)
            pm.textFieldGrp('From_Prefix', label='Prefix Name:', cal=(1, "right"),
                                  cw2=(50 * percentage, 25 * percentage, ),
                                  columnAttach=[(1, 'both', 0 * percentage),
                                                (2, 'both', 0 * percentage),
                                                ], tx='snake')

            with pm.rowLayout(nc=2, cw2=(50 * percentage, 25 * percentage), cl2=('right', 'left'),
                              columnAttach=[(1, 'both', 0.5 * percentage), (2, 'both', 0.5 * percentage)]):
                pm.text('Skeleton Number:')
                pm.intField('Skeleton_Number', value=20)

            with pm.rowLayout(nc=2, cw2=(85 * percentage, 15 * percentage), cl2=('right','right'),
                              columnAttach=[(1, 'both', 0),(2, 'both', 0)],
                              rowAttach=[(1, 'top', 4),(2, 'top', 4) ]):
                pm.button('Create_Rig', l="Create Rig", bgc=(0, 0.5, 0),
                          c=partial(Lr_Template))
                pm.button('CleanUp_Rig', l="Del", bgc=(0.5, 0, 0),
                          c=partial(lr_delete_template))
            # with pm.rowLayout(nc=1, cw=(1, 100 * percentage), cal=(1, 'right'), columnAttach=(1, 'both', 0),
            #                   rowAttach=[(1, 'top', 1)]):
            #     pm.button('CleanUp_Rig', l="Clean Up Rig", bgc=(0.5, 0, 0),
            #               c=partial(lr_delete_template))
            pm.separator(h=8, st="in", w=90 * percentage)

                # with pm.rowLayout(nc=4, cw4=(10 * percentage, 21.5 * percentage, 21.5 * percentage, 21.5 * percentage),
                #                   cl4=('center', 'center', 'center', 'center'),
                #                   columnAttach=[(1, 'both', 0 * percentage), (2, 'both', 0 * percentage),
                #                                 (3, 'both', 0 * percentage), (4, 'both', 0 * percentage)]):

    pm.showWindow()
#**********************************************************************************************************************#
#                                                  CLASS RIG                                                           #
#**********************************************************************************************************************#
class Lr_Template():
    def __init__(self, *args):
        if mc.objExists('tmp_grp'):
            om.MGlobal.displayError('joint template already exist')
        else:
            self.head_joint = self.joint_template(name_template='head_tmp', pos_x=0, pos_y=0, pos_z=111)
            self.tail_joint = self.joint_template(name_template='tail_tmp', pos_x=0, pos_y=0, pos_z=-132)
            self.jaw_joint = self.joint_template(name_template='jaw_tmp', pos_x=0, pos_y=1.324, pos_z=113.612)
            self.jaw_tip = self.joint_template(name_template='jawTip_tmp', pos_x=0, pos_y=-4.005, pos_z=121.998)
            self.tongue = self.joint_template(name_template='tongue_tmp', pos_x=0, pos_y=1.137, pos_z=116.245)
            self.tongue_tip = self.joint_template(name_template='tongueTip_tmp', pos_x=0, pos_y=-7.289, pos_z=127.29)
            self.left_fang = self.joint_template(name_template='leftFang_tmp', pos_x=1, pos_y=3.398, pos_z=124.581)
            self.right_fang = self.joint_template(name_template='rightFang_tmp', pos_x=-1, pos_y=3.398, pos_z=124.581)

            # parent
            mc.parent(self.tail_joint, self.head_joint)
            mc.parent(self.jaw_tip, self.jaw_joint)
            mc.parent(self.tongue_tip, self.tongue)

            # group
            self.tmp_grp = mc.group(n='tmp_grp', empty=True)
            mc.parent(self.head_joint, self.jaw_joint, self.tongue, self.left_fang, self.right_fang, self.tmp_grp)

    def joint_template(self, name_template, pos_x, pos_y, pos_z):
        mc.select(cl=1)
        joint_tmp = mc.joint(name=name_template, rad=2, p=(pos_x, pos_y, pos_z))
        mc.setAttr(joint_tmp+'.type', 18)
        mc.setAttr(joint_tmp+'.drawLabel', 1)
        mc.setAttr(joint_tmp+'.otherType', name_template, type='string')
        mc.setAttr(joint_tmp+'.ove', 1)
        mc.setAttr(joint_tmp+'.ovc', 17)

        return joint_tmp

class Lr_Rig():
    def __init__(self, head, tail, prefix, skeleton_number):
        if mc.objExists('tmp_grp'):
            mc.hide('tmp_grp')
            self.lr_joint_bind(head, tail, prefix, skeleton_number)
            self.lr_create_jointIk_spline_solver(head, tail, prefix, skeleton_number)
        else:
            om.MGlobal.displayError('before create rig, please create template joint first.')

    def lr_create_jointIk_spline_solver(self, head, tail, prefix, skeleton_number):

        self.lr_joint_spline_Ik(head=head, tail=tail, prefix=prefix, skeleton_number=skeleton_number)

        head_ik_joint = mc.xform(self.list_jointIk[0], q=1, ws=True, t=1)
        tail_ik_joint = mc.xform(self.list_jointIk[-1], q=1, ws=True, t=1)

        # create curve for ik spline
        curve_ik_spline_detail = mc.curve(d=3, ep=[head_ik_joint, tail_ik_joint])
        mc.rebuildCurve(curve_ik_spline_detail, ch=0, rpo=1, rt=0, end=1, kr=0, kcp=0,
                        kep=1, kt=0, s=(skeleton_number/2)-1, d=3, tol=0.01)

        self.limb_detail_hdl = mc.ikHandle(sj=self.list_jointIk[0], ee=self.list_jointIk[-1],
                                           sol='ikSplineSolver',
                                           n='%s_hdl' % (prefix + 'Ik'), ccv=False,
                                           c=curve_ik_spline_detail, ns=1, rootOnCurve=True)
        detail_hdl_curve = mc.rename(curve_ik_spline_detail, '%s_crv' % (prefix + 'Ik'))
        # skinning the joint to the bind curve
        skin_cluster = mc.skinCluster(self.bind_joint, detail_hdl_curve,
                                 n='%s%s'% (prefix, 'SkinCluster'), tsb=True, bm=0, sm=0, nw=1, mi=1)

        # create controller


    def lr_joint_bind(self, head, tail, prefix, skeleton_number):
        self.bind_joint = self.lr_split_joint(obj_base=head, obj_tip=tail, prefix=prefix, suffix='bind', skeleton_number=skeleton_number / 2)
        group_head=[]
        controller_head=[]
        for item in self.bind_joint[0:2]:
            controller = Lr_Control(match_obj_first_position=item,
                 prefix=item, suffix='ctrl', groups_ctrl=['Main','Offset'],
                 ctrl_color='red', ctrl_size=2.0,
                 lock_channels=['v'],  shape=STAR, connection=['parent'])
            group_head.append(controller.parent_control[0])
            controller_head.append(controller.control)
        # lr_parent_constraint(controller_head[0],group_head[1])

        for item in self.bind_joint[2:]:
            Lr_Control(match_obj_first_position=item,
                 prefix=item, suffix='ctrl', groups_ctrl=['Main','Offset'],
                 ctrl_color='yellow',
                 lock_channels=['v'],  shape=CIRCLE, connection=['parent'])


    def lr_joint_spline_Ik(self, head, tail, prefix, skeleton_number):
        self.list_jointIk = self.lr_split_joint(obj_base=head, obj_tip=tail, prefix=prefix, suffix='jnt', skeleton_number=skeleton_number)
        for i in range(len(self.list_jointIk)):
            if i > 0:
                mc.parent(self.list_jointIk[i], self.list_jointIk[i - 1])

    def lr_split_joint(self, obj_base, obj_tip, prefix, suffix, skeleton_number=1):

        base_xform = mc.xform(obj_base, q=1, ws=1, t=1)
        tip_xform = mc.xform(obj_tip, q=1, ws=1, t=1)

        base_vector = om.MVector(base_xform[0], base_xform[1], base_xform[2])
        tip_vector = om.MVector(tip_xform[0], tip_xform[1], tip_xform[2])

        split_vector = (tip_vector - base_vector)
        segment_vector = (split_vector / (skeleton_number - 1))

        segment_location = (base_vector + segment_vector)

        mc.select(cl=1)
        base = mc.joint(name='%s%s_%s' % (prefix, str(1).zfill(2), suffix))
        mc.delete(mc.parentConstraint(obj_base, base))
        mc.makeIdentity(base, apply=True, t=1, r=1, s=1, n=0, pn=1)

        list = []
        new_list = []
        for i in range(0, (skeleton_number - 2)):
            mc.select(cl=1)
            segment = mc.joint()
            new_name = mc.rename(segment, str('%s%01d_%s' % (prefix, (i + 2), 'ref')))
            list.append(new_name)
            mc.move(segment_location.x, segment_location.y, segment_location.z, new_name)
            segment_location = segment_location + segment_vector

        mc.select(cl=1)
        tip = mc.joint(name='%s%s_%s' % (prefix, str(list.index(list[-1])+3).zfill(2), suffix))
        mc.delete(mc.parentConstraint(obj_tip, tip))
        mc.makeIdentity(tip, apply=True, t=1, r=1, s=1, n=0, pn=1)

        for i in list:
            new_name = mc.rename(i, '%s%s_%s' % (prefix, str(list.index(i) + 2).zfill(2), suffix))
            new_list.append(new_name)
        new_list.append(base)
        new_list.append(tip)

        # create controller
        return sorted(new_list)
#**********************************************************************************************************************#
#                                                 CONTROLLER                                                           #
#**********************************************************************************************************************#
class Lr_Control():
    def __init__(self, match_obj_second_position=None, match_obj_first_position=False,
                 prefix=None, suffix='ctrl', groups_ctrl=['Zro'],
                 group_connect_attr=[''], ctrl_size=5.0, ctrl_color='turquoiseBlue',
                 lock_channels=['v'],  shape=CIRCLE, connection=''):


        scale_controller =  lr_scale_curve(ctrl_size, shape)
        ctrl = lr_controller_shape(scale_controller)

        rename_controller = mc.rename(ctrl, '%s_%s' % (lr_prefix_name(prefix), suffix))

        # get the number
        try:
            patterns = [r'\d+']
            prefix_number =lr_prefix_name(prefix)
            for p in patterns:
                prefix_number = re.findall(p, prefix_number)[0]
        except:
            prefix_number = ''

        # get the prefix without number
        prefix_without_number = str(lr_prefix_name(prefix)).translate(None, digits)

        group_parent = lr_group_parents(groups=groups_ctrl, prefix=prefix_without_number, number=prefix_number,
                                       suffix=suffix.title(),
                                       )

        parent_controller = mc.parent(rename_controller, group_parent[-1])

        lr_set_color(rename_controller, ctrl_color)

        # lock and hide attribute
        lr_lock_hide_attr(lock_channels, rename_controller)

        connection_controller = rename_controller

        if match_obj_first_position:
            mc.delete(mc.parentConstraint(match_obj_first_position, match_obj_second_position, group_parent[0]))

        # connection to attribute
        if connection == ['connectAttr']:
            group_connection =  lr_group_object(group_connect_attr, match_obj_first_position, connection_controller)
            connection =  lr_connections(connection, rename_controller, match_obj_first_position)

        # connection parent
        elif connection == ['parent']:
            # query list relatives
            list_relatives_parent = mc.listRelatives(match_obj_first_position, p=1)

            if list_relatives_parent == None:
                connection =  lr_connections(connection, connection_controller, match_obj_first_position)

            else:
                # parent object to controller
                connection =  lr_connections(connection, connection_controller, match_obj_first_position)

                # parent ctrl group to list relatives
                mc.parent(group_parent[0],list_relatives_parent)

        # connection constraint
        else:
            connection =  lr_connections(connection, connection_controller, match_obj_first_position)

        # clear selection
        mc.select(cl=1)

        self.control = rename_controller
        self.parent_control = group_parent
        self.connection = connection
#**********************************************************************************************************************#
#                                                MOTION PATH                                                           #
#**********************************************************************************************************************#
class Lr_MotionPath():
    def __init__(self, curve='', world_up_loc='', set_value_length =1, controller=False):
        # load Plug-ins
        lr_load_matrix_quad_plugin()

        all_grp = mc.group(empty=True, n=lr_prefix_name(curve) + 'MotionLoop' + '_grp')
        setup_grp = mc.group(empty=True, n=lr_prefix_name(curve) + 'Setup' + '_grp')
        grp_jnt = mc.group(empty=True, n=lr_prefix_name(curve) + 'Joints' + '_grp')
        grp_crv = mc.group(empty=True, n=lr_prefix_name(curve) + 'Crv' + '_grp')

        create_ik = lr_joint_on_curve(curve=curve, world_up_loc=world_up_loc, delete_group=False,
                                      ctrl=controller)
        arc_length = mc.arclen(curve)

        value_length = arc_length/set_value_length

        print arc_length

        ctrl = Lr_Control(match_obj_first_position=create_ik['joints'][0], prefix=lr_prefix_name(curve),
                          shape=STAR,
                          groups_ctrl=['Zro'], ctrl_size=10.0,
                          ctrl_color='blue', lock_channels=['r', 's', 'v'])

        attribute_speed = lr_add_attribute(objects=[ctrl.control], long_name=['speed'], min=0, dv=0, max=50, at="float",
                                           keyable=True)

        lr_change_position(ctrl.control, 'xy')

        for i, ctrls in zip(create_ik['motionPath'], create_ik['ctrl']):

            motion_path_uvalue = mc.getAttr(i + '.u')

            mult_timing = mc.shadingNode('multDoubleLinear', asUtility=1, n=lr_prefix_name(i) + 'TimeMult' + '_mdl')
            mc.connectAttr(ctrl.control + '.%s' % attribute_speed, mult_timing + '.input1')
            mc.connectAttr('time1.outTime', mult_timing + '.input2')

            add_speed = mc.shadingNode('addDoubleLinear', asUtility=1, n=lr_prefix_name(i) + 'SpeedAdd' + '_adl')
            mc.setAttr(add_speed + '.input2', (((motion_path_uvalue/value_length) * 1000)))

            mult_offset = mc.shadingNode('multiplyDivide', asUtility=1, n=lr_prefix_name(i) + 'SpeedOffset' + '_mdn')
            mc.setAttr(mult_offset + '.operation', 2)
            mc.setAttr(mult_offset + '.input2X', 1000)
            mc.connectAttr(add_speed + '.output', mult_offset + '.input1X')

            condition_speed = mc.shadingNode('condition', asUtility=1, n=lr_prefix_name(i) + 'Speed' + '_cnd')
            mc.setAttr(condition_speed + '.operation', 2)
            mc.connectAttr(mult_timing + '.output', condition_speed + '.firstTerm')

            add_value = mc.shadingNode('plusMinusAverage', asUtility=1, n=lr_prefix_name(i) + 'Speed' + '_pma')
            mc.connectAttr(mult_offset + '.outputX', add_value + '.input1D[0]')
            mc.setAttr(add_value + '.input1D[1]', 1)

            mc.connectAttr(mult_offset + '.outputX', condition_speed + '.colorIfTrueR')
            mc.connectAttr(add_value + '.output1D', condition_speed + '.colorIfFalseR')

            mc.setDrivenKeyframe(i + '.u', cd=condition_speed + '.outColorR', dv=0, v=0)
            mc.setDrivenKeyframe(i + '.u', cd=condition_speed + '.outColorR', dv=1, v=1)

            mc.keyTangent(i + '_uValue', edit=True, inTangentType='linear', outTangentType='linear')

            mc.setAttr(i + '_uValue' + '.preInfinity', 3)
            mc.setAttr(i + '_uValue' + '.postInfinity', 3)

            if controller:
                pos_offset_attr = lr_add_attribute(objects=[ctrls], long_name=['posOffset'], dv=0, min=0, at="float",
                                                   keyable=True)

                obj_offset = mc.shadingNode('plusMinusAverage', asUtility=1, n=lr_prefix_name(i) + 'ObjSpeed' + '_pma')
                mc.connectAttr(mult_timing + '.output', obj_offset + '.input1D[0]')
                mc.connectAttr(obj_offset + '.output1D', add_speed + '.input1')

                obj_condition = mc.shadingNode('condition', asUtility=1, n=lr_prefix_name(i) + 'ObjSpeed' + '_cnd')
                mc.setAttr(obj_condition + '.operation', 4)
                mc.connectAttr(mult_timing + '.output', obj_condition + '.firstTerm')

                mc.setDrivenKeyframe(obj_condition + '.colorIfTrueR', cd=ctrls + '.%s' % pos_offset_attr, dv=0, v=0)
                mc.setDrivenKeyframe(obj_condition + '.colorIfTrueR', cd=ctrls + '.%s' % pos_offset_attr, dv=1, v=-1)

                mc.keyTangent(obj_condition + '_colorIfTrueR', edit=True, inTangentType='spline', outTangentType='spline')

                mc.setAttr(obj_condition + '_colorIfTrueR' + '.preInfinity', 1)
                mc.setAttr(obj_condition + '_colorIfTrueR' + '.postInfinity', 1)

                mc.setDrivenKeyframe(obj_condition + '.colorIfFalseR', cd=ctrls + '.%s' % pos_offset_attr, dv=0, v=0)
                mc.setDrivenKeyframe(obj_condition + '.colorIfFalseR', cd=ctrls + '.%s' % pos_offset_attr, dv=1, v=1)

                mc.keyTangent(obj_condition + '_colorIfFalseR', edit=True, inTangentType='spline', outTangentType='spline')

                mc.setAttr(obj_condition + '_colorIfFalseR' + '.preInfinity', 1)
                mc.setAttr(obj_condition + '_colorIfFalseR' + '.postInfinity', 1)

                mc.connectAttr(obj_condition + '.outColorR', obj_offset + '.input1D[1]')

            else:
                mc.connectAttr(mult_timing + '.output', add_speed + '.input1')

            mc.setAttr(i + '.u', lock=True)

        decompose = mc.shadingNode('decomposeMatrix', asUtility=1, n=lr_prefix_name(curve) + 'Scale' + 'dmt')
        mc.connectAttr(grp_crv + '.worldMatrix[0]', decompose + '.inputMatrix')

        for i in create_ik['joints']:
            mc.connectAttr(decompose + '.outputScale', i + '.scale')
            lr_lock_attr(['t', 'r', 's'], i)

        mc.parent(create_ik['joints'], grp_jnt)
        # mc.parent(createIk['wUpLocGrp'], grpJnt)

        mc.parent(curve, grp_crv)

        mc.parent(grp_jnt, grp_crv, setup_grp)
        mc.parent(ctrl.parent_control[0], setup_grp, all_grp)

        # mc.setAttr(createIk['wUpLoc']+'.visibility', 0)
        lr_lock_attr(['t', 'r', 's'], curve)
        lr_lock_attr(['t', 'r', 's'], grp_jnt)
        lr_lock_attr(['t', 'r', 's'], setup_grp)

        mc.select(cl=1)
#**********************************************************************************************************************#
#                                              ARGS TEMPLATE                                                           #
#**********************************************************************************************************************#
def lr_create_template(*args):
    template = Lr_Template()

def lr_delete_template(*args):
    if mc.objExists('tmp_grp'):
        mc.delete('tmp_grp')
    else:
        om.MGlobal.displayError('There is no template joint in the scene')

#**********************************************************************************************************************#
#                                                   FUNCTION                                                           #
#**********************************************************************************************************************#

def lr_scale_curve(size_obj, shape):
    scaleShp = [[size_obj * i for i in j] for j in shape]
    return scaleShp

def lr_controller_shape(shape):
    createCrv = mc.curve(d=1, p=shape)
    return createCrv

def lr_group_parents(groups, prefix, suffix, number='',):
    # create group hierarchy
    grps = []
    for i in range(len(groups)):
        grps.append(
            mc.createNode('transform', n="%s%s%s%s_%s" % (prefix, suffix, groups[i], number, 'grp')))

        if i > 0:
            mc.parent(grps[i],grps[i - 1])

    return grps

def lr_set_color(ctrl, color):
    color_dic = {'blue': 6, 'darkGreen': 7, 'darkPurple': 8, 'dullRed': 12, 'red': 13, 'navy': 15,
                 'yellow': 17, 'turquoiseBlue': 18, 'turquoiseGreen': 19, 'lightPink': 20, 'lightYellow': 22,
                 'dullGreen': 23, 'dullYellow': 25, 'greenYellow': 26, 'greenBlue': 27, 'blueGreen': 28,
                 'lightNavy': 29, 'violet': 30, 'ruby': 31
    }
    if color in color_dic.keys():
        list_relatives = mc.listRelatives(ctrl, s=1)[0]
        mc.setAttr(list_relatives + '.ove', 1)
        mc.setAttr(list_relatives + '.ovc', color_dic[color])
        return list_relatives
    else:
        return mc.warning("Could not find %s name color. Please check color name!" % color)

def lr_lock_hide_attr(lock_channel, ctrl):
    attr_lock_list = []
    for lc in lock_channel:
        if lc in ['t', 'r', 's']:
            for axis in ['x', 'y', 'z']:
                at = lc + axis
                attr_lock_list.append(at)
        else:
            attr_lock_list.append(lc)
    for at in attr_lock_list:
        mc.setAttr(ctrl + '.' + at, l=1, k=0)
    return attr_lock_list

def lr_group_object(grp_name_list, obj_base, prefix, suffix, match_pos=None, side=''):
    list_relatives = mc.listRelatives(obj_base, ap=1)

    cGrp = lr_group_parents(grp_name_list, '%s' % prefix, suffix.title(), side)

    if match_pos:
        lr_match_position(match_pos, cGrp[0])
        #match_scale(match_pos, cGrp[0])

    if list_relatives == None:
        mc.parent(obj_base, cGrp[-1])
    else:
        # parent group offset to list relatives
        mc.parent(cGrp[0], list_relatives)
        # parent obj to grp offset
        mc.parent(obj_base, cGrp[-1], )

    return cGrp

def lr_match_position(obj_base, obj_target):
    mc.delete(lr_parent_constraint(obj_base, obj_target, mo=0))

def lr_parent_constraint(obj_base, obj_target, mo=1):
    par_constraint = mc.parentConstraint(obj_base, obj_target, mo=mo)[0]
    split = par_constraint.split('_')
    x = '_'.join(split[:-1])
    n = x.replace(x, x + '_pac')
    new_name = [mc.rename(par_constraint, n)]
    return new_name

def lr_orient_constraint(obj_base, obj_target, mo=1):
    orient_constraint = mc.orientConstraint(obj_base, obj_target, mo=mo)[0]
    split = orient_constraint.split('_')
    x = '_'.join(split[:-1])
    n = x.replace(x, x + '_oc')
    new_name = [mc.rename(orient_constraint, n)]
    return new_name

def lr_point_constraint(obj_base, obj_target, mo=1):
    point_constraint = mc.pointConstraint(obj_base, obj_target, mo=mo)[0]
    split = point_constraint.split('_')
    x = '_'.join(split[:-1])
    n = x.replace(x, x + '_pc')
    new_name = [mc.rename(point_constraint, n)]
    return new_name

def lr_scale_constraint(obj_base, obj_target, mo=1):
    scale_constraint = mc.scaleConstraint(obj_base, obj_target, mo=mo)[0]
    split = scale_constraint.split('_')
    x = '_'.join(split[:-1])
    n = x.replace(x, x + '_sc')
    new_name = [mc.rename(scale_constraint, n)]

    return new_name

def lr_parent_object(objBase, objTgt):
    parent_object = mc.parent(objTgt, objBase)
    return parent_object

def lr_connect_attr_object(objBase, objTgt):
    lr_connect_attr_translate(objBase, objTgt)
    lr_connect_attr_rotate(objBase, objTgt)
    lr_connect_attr_scale(objBase, objTgt)
    return

def lr_connect_attr_scale(obj_base, obj_target):
    list_relatives = mc.listRelatives(obj_target, ap=1)
    if list_relatives == True:
        attr = mc.connectAttr(obj_base + '.scaleX', list_relatives + '.scaleX')
        attr = mc.connectAttr(obj_base + '.scaleY', list_relatives + '.scaleY')
        attr = mc.connectAttr(obj_base + '.scaleZ', list_relatives + '.scaleZ')

    else:
        attr = mc.connectAttr(obj_base + '.scaleX', obj_target + '.scaleX')
        attr = mc.connectAttr(obj_base + '.scaleY', obj_target + '.scaleY')
        attr = mc.connectAttr(obj_base + '.scaleZ', obj_target + '.scaleZ')
    return attr

def lr_connect_attr_translate(objBase, objTgt):
    list_relatives = mc.listRelatives(objTgt, ap=1)
    if list_relatives == True:
        translate_attr = mc.connectAttr(objBase + '.translate', list_relatives + '.translate')
    else:
        translate_attr = mc.connectAttr(objBase + '.translate', objTgt + '.translate')
    return translate_attr

def lr_connect_attr_rotate(obj_base, obj_target):
    list_relatives = mc.listRelatives(obj_target, ap=1)
    if list_relatives == True:
        rotate_attr = mc.connectAttr(obj_base + '.rotate', list_relatives + '.rotate')
    else:
        rotate_attr = mc.connectAttr(obj_base + '.rotate', obj_target + '.rotate')
    return rotate_attr

def lr_connections(connect, ctrl, obj):
    dic = {'parentCons': lr_parent_constraint, 'pointCons':  lr_point_constraint, 'orientCons':  lr_orient_constraint,
           'scaleCons':  lr_scale_constraint, 'parent':  lr_parent_object, 'connectAttr':  lr_connect_attr_object,
           'connectTrans':  lr_connect_attr_translate, 'connectOrient':  lr_connect_attr_rotate,
           'connectScale':  lr_connect_attr_scale,
           }
    rs = {}
    for con in connect:
        if con in dic.keys():
            rs[con] = dic[con](ctrl, obj)
        else:
            return mc.error("Your %s key name is wrong. Please check on the key list connection!" % con)
    return rs

def lr_prefix_name(obj):
    if '_' in obj:
        get_prefix_name = obj.split('_')[:-1]
        joining = '_'.join(get_prefix_name)
        return joining
    else:
        return obj
def lr_load_matrix_quad_plugin():
    # load Plug-ins
    matrix_node = mc.pluginInfo('matrixNodes.mll', query=True, loaded=True)
    quat_node = mc.pluginInfo('quatNodes.mll', query=True, loaded=True)

    if not matrix_node:
        mc.loadPlugin('matrixNodes.mll')

    if not quat_node:
        mc.loadPlugin('quatNodes.mll')

def lr_add_attribute(objects=[], long_name=[''], nice_name='', separator=False, keyable=False, channel_box=False, **kwargs):
    # For each object
    for obj in objects:
        # For each attribute
        for x in range(0, len(long_name)):
            # See if a niceName was defined
            attr_nice = '' if not nice_name else nice_name[x]
            # If the attribute does not exists
            if not mc.attributeQuery(long_name[x], node=obj, exists=True):
                # Add the attribute
                mc.addAttr(obj, longName=long_name[x], niceName=attr_nice, **kwargs)
                # If lock was set to True
                mc.setAttr((obj + '.' + long_name[x]), k=keyable, e=1, cb=channel_box) if separator else mc.setAttr(
                    (obj + '.' + long_name[x]), k=keyable, e=1, cb=channel_box)
    return long_name[0]

def lr_joint_on_curve(curve='', world_up_loc='', spline_ik=None, delete_group=True, ctrl=False):
    newJnt = lr_create_joint_lid(curve)

    num = (1.0 / (int(newJnt[3]) - 1))
    transform = []
    controls = []
    motion_paths = []
    joints = []
    ikHdl = None

    for n, i in enumerate(newJnt[0]):
        ranges = num * n
        if ctrl:
            new_transform = Lr_Control(match_obj_first_position=i, prefix=lr_prefix_name(i) + 'Jnt', shape=CIRCLE,
                                       groups_ctrl=['Zro'], ctrl_size=2.0,
                                       ctrl_color='blue', lock_channels=['r', 's', 'v'],
                                       connection=['parent'])
            motion_path = mc.pathAnimation(new_transform.parent_control[0], fractionMode=True, fa='z', ua='x',
                                           wut='objectrotation',
                                           wuo=world_up_loc,
                                           c=curve,
                                           n=lr_prefix_name(i) + '_mpt')

            transform.append(new_transform.parent_control[0])
            controls.append(new_transform.control)
            new_transform = new_transform.control

        else:
            new_transform = mc.createNode('transform', n=lr_prefix_name(i) + 'Jnt_grp')
            mc.parent(i, new_transform)
            motion_path = mc.pathAnimation(new_transform, fractionMode=True, fa='z', ua='x',
                                           wut='objectrotation',
                                           wuo=world_up_loc,
                                           c=curve,
                                           n=lr_prefix_name(i) + '_mpt')
            transform.append(new_transform)
            controls.append(newJnt[0])

        mc.cutKey(motion_path + '.u', time=())
        mc.setAttr(motion_path + '.u', ranges)
        motion_paths.append(motion_path)

        mc.setAttr(i + '.translate', 0, 0, 0, type='double3')
        mc.setAttr(i + '.rotate', 0, 0, 0, type='double3')

        joints.append(i)

        if delete_group:
            mc.parent(joints[n], w=True)
            mc.delete(new_transform + '.tx', icn=1)
            mc.delete(new_transform + '.ty', icn=1)
            mc.delete(new_transform + '.tz', icn=1)
            mc.delete(new_transform + '.rx', icn=1)
            mc.delete(new_transform + '.ry', icn=1)
            mc.delete(new_transform + '.rz', icn=1)
            mc.xform(new_transform, ws=True, ro=(0, 0, 0))
            mc.delete(motion_path)
            mc.delete(new_transform)

            if n > 0:
                mc.parent(joints[n], joints[n - 1])

            mc.joint(joints[0], e=True, oj='xyz', sao='yup', ch=True, zso=True)

    if spline_ik:
        if not delete_group:
            mc.error('Spline Ik cannot be created. Please delGrp set to True in order to remove group parent joints!')
        else:
            ikHdl = mc.ikHandle(sj=joints[0], ee=joints[-1], c=curve, sol='ikSplineSolver', ccv=False,
                                n=lr_prefix_name(curve) + '_ikh')

        return {'joints': transform,
                'motionPath': motion_paths,
                'ctrl': controls,
                'ikHdl': ikHdl,
                'curve': curve}

    print motion_paths

    return {'joints': transform,
            'motionPath': motion_paths,
            'ctrl': controls,
            'ikHdl': ikHdl,
            'wUpLoc': newJnt[1],
            'curve': curve}

def lr_create_joint_lid(crv):
    all_joint = []
    all_locator = []
    ranges = []
    for i, v in enumerate(mc.ls('%s.cv[0:*]' % crv, fl=True)):
        # create joint
        mc.select(cl=1)
        joint = mc.joint(n='%s%02d%s' % (lr_prefix_name(crv), (i + 1), '_jnt'), rad=0.1)
        pos = mc.xform(v, q=1, ws=1, t=1)
        mc.xform(joint, ws=1, t=pos)
        all_joint.append(joint)

        ranges.append(i)

    length = len(ranges)
    return all_joint, all_locator, ranges, length

def lr_change_position(shape, destination):
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
def lr_lock_attr(lock_channel, ctrl):
    attrLockList = []
    for lc in lock_channel:
        if lc in ['t', 'r', 's']:
            for axis in ['x', 'y', 'z']:
                at = lc + axis
                attrLockList.append(at)
        else:
            attrLockList.append(lc)

    for at in attrLockList:
        mc.setAttr(ctrl + '.' + at, l=1)

    return attrLockList