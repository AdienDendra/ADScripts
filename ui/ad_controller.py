from functools import partial
import pymel.core as pm

layout = 435
percentage = 0.01 * layout

def ad_controller_ui():
    adien_controller = 'AD_Controller'
    pm.window(adien_controller, exists=True)
    if pm.window(adien_controller, exists=True):
        pm.deleteUI(adien_controller)
    with pm.window(adien_controller, title='AD Controller', width=layout, height=400):
        with pm.tabLayout('tab',width=layout*1.05, height=400):
            with pm.columnLayout('Create Controller',rowSpacing=1 * percentage, w=layout*1.04, co=('both', 1 * percentage),
                                 adj=1, p='tab'):
                pm.separator(st="in", w=90 * percentage)
                with pm.rowColumnLayout(nc=2, rowSpacing=(2, 1 * percentage),
                                        co=(1 * percentage, 'both', 1 * percentage),
                                        cw=[(1, 5 * percentage), (2, 96 * percentage)]):
                    pm.checkBox(label='',
                                cc=partial(ad_enabling_disabling_ui, ['Prefix_Main'],''),
                                value=False)
                    ad_defining_object_text_field_no_button(define_object='Prefix_Main', label="Prefix Main:",
                                                  add_feature=True, enable=False)
                    pm.checkBox(label='',
                                cc=partial(ad_enabling_disabling_ui, ['Parent_Group_Name'],'Main'),
                                value=True)
                    ad_defining_object_text_field_no_button(define_object='Parent_Group_Name', label="Parent Group Name:",
                                                  add_feature=True, tx='Main',  enable=True)
                ad_defining_object_text_field_no_button(define_object='Suffix_Main', tx='ctrl', label="Suffix Main:")

                with pm.rowLayout(nc=2, cw2=(31 * percentage, 40 * percentage), cl2=('right', 'left'),
                                  columnAttach=[(1, 'both', 0.5 * percentage), (2, 'both', 0.5 * percentage)]):
                    pm.text('')
                    with pm.columnLayout():
                        pm.checkBox('Target_Visibility', label='Add Attr Target Visibility', value=False)
                        pm.checkBox('Add_Pivot_Ctrl', label='Add Pivot Controller', value=False)

                pm.separator(h=10, st="in", w=95*percentage)

                with pm.rowLayout('Palette_Port', nc=2, cw2=(31 * percentage, 69 * percentage), cl2=('right', 'left'),
                                  columnAttach=[(1, 'both', 0.5 * percentage), (2, 'both', 0.5 * percentage)],
                                  rowAttach=[(1, 'top', 0)]):

                    pm.text(label='Controller Color:')
                    ad_color_index()

                with pm.rowLayout(nc=3, cw3=(31 * percentage, 34.5 * percentage, 33.5 * percentage
                                                             ), cl3=('right', 'right', 'right'),
                                  columnAttach=[(1, 'both', 0.5 * percentage), (2, 'both', 0.5 * percentage),
                                                (3, 'both', 0.5 * percentage)]):
                    pm.text(label='')
                    pm.button("Replace_Color", l="Replace Color", c='')
                    pm.button('Select_All_AD_Controller',l="Select All AD Controller", c='')
                pm.separator(h=10, st="in", w=90*percentage)

                with pm.rowLayout(nc=3, cw3=(5*percentage, 46.5 * percentage, 50 * percentage),
                                  cl3=('right', 'right','right'),
                                  columnAttach=[(1, 'both', 0.5 * percentage), (2, 'both', 0.5 * percentage), (3, 'both', 0.5 * percentage),
                                               ]):
                    pm.checkBox(label='',
                                cc=partial(ad_enabling_disabling_ui, ['Suffix_Child_Ctrl'], 'Child'),
                                value=False)

                    pm.textFieldGrp('Suffix_Child_Ctrl', label='Adding Ctrl Child:', cal=(1, "right"),
                                    cw2=(25 * percentage, 15 * percentage),
                                    cat=[(1, 'right', 2), (2, 'both', 2)], enable=False, tx='child')


                pm.separator(h=10, st="in", w=90*percentage)

                with pm.rowLayout(nc=4, cw4=(31 * percentage, 28 * percentage, 25 * percentage, 22 * percentage
                                                             ), cl4=('right', 'left', 'left', 'left'),
                                  columnAttach=[(1, 'both', 0.5 * percentage), (2, 'both', 0.5 * percentage),
                                                (3, 'both', 0.5 * percentage), (4, 'both', 0.5 * percentage),
                                                ], rowAttach=[(1, 'top', 0)]):
                    pm.text('Controller Channel:')
                    ad_channelbox_translation()
                    ad_channelbox_rotation()
                    ad_channelbox_scale()

                with pm.rowLayout(nc=3, cw3=(31 * percentage, 34.5 * percentage, 33.5 * percentage
                                                                 ), cl3=('right', 'right', 'right'),
                                      columnAttach=[(1, 'both', 0.5 * percentage), (2, 'both', 0.5 * percentage),
                                                    (3, 'both', 0.5 * percentage)]):
                        pm.text(label='')
                        pm.button("Hide_Lock_Channel", l="Hide and Lock", c='')
                        pm.button('Show_Channel',l="Show", c='')
                pm.separator(h=10, st="in", w=90*percentage)

                with pm.rowLayout('Connection', nc=3, cw3=(31 * percentage, 28 * percentage, 35 * percentage
                                                             ), cl3=('right', 'left', 'left'),
                                  columnAttach=[(1, 'both', 0.5 * percentage), (2, 'both', 0.5 * percentage),
                                                (3, 'both', 0.5 * percentage),
                                                ], rowAttach=[(1, 'top', 0), (3, 'top', 0)]):
                    pm.text(label='Connection:')
                    ad_channelbox_constraint_connection()
                    ad_channelbox_direct_connection()
                pm.separator(h=10, st="in", w=90*percentage)
                # with pm.rowColumnLayout('Controller_Shape', nc=2, rowSpacing=(2, 1 * percentage),
                #                         co=(1 * percentage, 'both', 1 * percentage),
                #                         cw=[(1, 31 * percentage), (2, 70 * percentage)]):
                with pm.rowLayout(nc=2, cw2=(31 * percentage, 70 * percentage), cl2=('right', 'left'),
                              columnAttach=[(1, 'both', 0.5 * percentage), (2, 'both', 0.5 * percentage)],
                              rowAttach=[(1, 'top', 0)]):
                    pm.text(label='Controller Shape:')
                    with pm.rowColumnLayout(nc=9):

                            icon_radio_control = pm.iconTextRadioCollection()
                            circle = pm.iconTextRadioButton(st='iconOnly', image='E:/Google Drive/Script Sell/AD Controller Icon/circle.png')
                            circleplus = pm.iconTextRadioButton(st='iconOnly', image='E:/Google Drive/Script Sell/AD Controller Icon/circleplus.png')
                            circlehalf = pm.iconTextRadioButton(st='iconOnly', image='E:/Google Drive/Script Sell/AD Controller Icon/circlehalf.png')
                            circleplushalf = pm.iconTextRadioButton(st='iconOnly', image='E:/Google Drive/Script Sell/AD Controller Icon/circleplushalf.png')
                            square = pm.iconTextRadioButton(st='iconOnly', image='E:/Google Drive/Script Sell/AD Controller Icon/square.png')
                            squareplus = pm.iconTextRadioButton(st='iconOnly', image='E:/Google Drive/Script Sell/AD Controller Icon/squareplus.png')
                            capsule = pm.iconTextRadioButton(st='iconOnly', image='E:/Google Drive/Script Sell/AD Controller Icon/capsule.png')
                            capsulecurve = pm.iconTextRadioButton(st='iconOnly', image='E:/Google Drive/Script Sell/AD Controller Icon/capsulecurve.png')
                            stickcircle = pm.iconTextRadioButton(st='iconOnly', image='E:/Google Drive/Script Sell/AD Controller Icon/stickcircle.png')
                            stick2circle = pm.iconTextRadioButton(st='iconOnly', image='E:/Google Drive/Script Sell/AD Controller Icon/stick2circle.png')
                            sticksquare = pm.iconTextRadioButton(st='iconOnly', image='E:/Google Drive/Script Sell/AD Controller Icon/sticksquare.png')
                            stick2square = pm.iconTextRadioButton(st='iconOnly', image='E:/Google Drive/Script Sell/AD Controller Icon/stick2square.png')
                            stickstar = pm.iconTextRadioButton(st='iconOnly', image='E:/Google Drive/Script Sell/AD Controller Icon/stickstar.png')
                            circleplusarrow = pm.iconTextRadioButton(st='iconOnly', image='E:/Google Drive/Script Sell/AD Controller Icon/circleplusarrow.png')
                            rectangle = pm.iconTextRadioButton(st='iconOnly', image='E:/Google Drive/Script Sell/AD Controller Icon/rectangle.png')
                            cube = pm.iconTextRadioButton(st='iconOnly', image='E:/Google Drive/Script Sell/AD Controller Icon/cube.png')
                            arrow = pm.iconTextRadioButton(st='iconOnly', image='E:/Google Drive/Script Sell/AD Controller Icon/arrow.png')
                            arrowcircular = pm.iconTextRadioButton(st='iconOnly', image='E:/Google Drive/Script Sell/AD Controller Icon/arrowcircular.png')
                            arrow2halfcircular = pm.iconTextRadioButton(st='iconOnly', image='E:/Google Drive/Script Sell/AD Controller Icon/arrow2halfcircular.png')
                            arrow2straight = pm.iconTextRadioButton(st='iconOnly', image='E:/Google Drive/Script Sell/AD Controller Icon/arrow2straight.png')
                            arrow2flat = pm.iconTextRadioButton(st='iconOnly', image='E:/Google Drive/Script Sell/AD Controller Icon/arrow2flat.png')
                            arrowhead = pm.iconTextRadioButton(st='iconOnly', image='E:/Google Drive/Script Sell/AD Controller Icon/arrowhead.png')
                            joint = pm.iconTextRadioButton(st='iconOnly', image='E:/Google Drive/Script Sell/AD Controller Icon/joint.png')
                            jointplus = pm.iconTextRadioButton(st='iconOnly', image='E:/Google Drive/Script Sell/AD Controller Icon/jointplus.png')
                            hand = pm.iconTextRadioButton(st='iconOnly', image='E:/Google Drive/Script Sell/AD Controller Icon/hand.png')
                            locator = pm.iconTextRadioButton(st='iconOnly', image='E:/Google Drive/Script Sell/AD Controller Icon/locator.png')

                            continues = pm.iconTextButton(st='iconOnly', hi='E:/Google Drive/Script Sell/AD Controller Icon/continue_hi.png', image='E:/Google Drive/Script Sell/AD Controller Icon/continue.png')

                            pm.iconTextRadioCollection(icon_radio_control, edit=True, select=circle)
                pm.separator(h=5, st="in", w=90*percentage)

                with pm.rowLayout():
                    pm.floatSliderGrp('Controller_Resize', cw3=(31 * percentage, 10 * percentage, 59 * percentage
                                                                 ), cl3=('right', 'right', 'right'),
                                      columnAttach=[(1, 'both', 0.5 * percentage), (2, 'both', 0.5 * percentage),
                                                    (3, 'both', 0.5 * percentage)],l="Controller Resize:", field=True, min=-10.0, value=0.0, max=10)

                    # pm.floatFieldGrp('Controller_Size', l="Controller Size:", cal=(1, "right"),
                    #                  cw2=(30 * percentage, 12 * percentage),
                    #                  cat=[(1, 'right', 1), (2, 'both', 2)], value1=1.00,
                    #                  precision=3)
                pm.separator(h=5, st="in", w=90*percentage)

                with pm.rowLayout(nc=3, cw3=(31 * percentage, 34.5 * percentage, 33.5 * percentage
                                                                 ), cl3=('right', 'right', 'right'),
                                      columnAttach=[(1, 'both', 0.5 * percentage), (2, 'both', 0.5 * percentage),
                                                    (3, 'both', 0.5 * percentage)]):
                        pm.text(label='')
                        pm.button("Replace_Controller", l="Replace Controller", c='')
                        pm.button('Create_Controller',l="Create Controller", c='')
            with pm.columnLayout('Controller Utilities', rowSpacing=1 * percentage, w=layout * 1.04, co=('both', 1 * percentage),
                                     adj=1, p='tab'):
                pm.separator(st="in", w=90 * percentage)
                with pm.rowLayout(nc=1, cw=(1, 100 * percentage), cal=(1,'center'), columnAttach=(1, 'both', 0.5 * percentage)):
                    pm.text(label='Mirror Controller')
                with pm.rowLayout(nc=3, cw=[(1, 40 * percentage),(2, 20 * percentage),(3, 40 * percentage)], cal=[(1,'center'), (2,'center'), (3,'center')],
                                  columnAttach=[(1, 'both', 0.5 * percentage), (2, 'both', 0.5 * percentage), (3, 'both', 0.5 * percentage)]):
                    pm.text(label='From:')
                    pm.text(label='')
                    pm.text(label='To:')

                with pm.rowLayout(nc=3, cw3=(40 * percentage,20 * percentage, 40 * percentage),
                                  cl3=('center', 'center', 'center'),
                                  columnAttach=[(1, 'both', 0.5 * percentage), (2, 'both', 0.5 * percentage), (3, 'both', 0.5 * percentage)]
                                  ):
                    pm.textFieldButtonGrp('From', label='', cal=(1, "right"), cw3=(0 * percentage, 32 * percentage, 10 * percentage),
                                          bl="<<",
                                          bc=partial(ad_adding_object_sel_to_textfield, 'From'))
                    pm.text(label='>>>>>')
                    pm.textFieldButtonGrp('To', label='', cal=(1, "right"),cw3=(0 * percentage, 32 * percentage, 10 * percentage),
                                          bl="<<",
                                          bc=partial(ad_adding_object_sel_to_textfield, 'To'))
                with pm.rowLayout(nc=3, cw3=(33.3 * percentage, 33.3 * percentage, 33.3 * percentage
                                             ), cl3=('center', 'center', 'center'),
                                  columnAttach=[(1, 'both', 0 * percentage), (2, 'both', 0 * percentage),
                                                (3, 'both', 0 * percentage)]
                                  ):
                    pm.button("Mirror_X", l="X", c='', bgc=(0.5, 0, 0))
                    pm.button("Mirror_Y", l="Y", c='', bgc=(0, 0.5, 0))
                    pm.button('Mirror_Z', l="Z", c='', bgc=(0, 0, 0.5))

                pm.separator(st="in", w=90 * percentage)
                with pm.rowLayout(nc=1, cw=(1, 100 * percentage), cal=(1,'center'), columnAttach=(1, 'both', 0.5 * percentage)):
                    pm.text(label='Save/Load Controller')
                with pm.rowLayout(nc=3, cw=[(1, 40 * percentage),(2, 20 * percentage),(3, 40 * percentage)], cal=[(1,'center'), (2,'center'), (3,'center')],
                                  columnAttach=[(1, 'both', 0.5 * percentage), (2, 'both', 0.5 * percentage), (3, 'both', 0.5 * percentage)]):
                    pm.text(label='Save:')
                    pm.text(label='')
                    pm.text(label='Load:')

                with pm.rowLayout(nc=3, cw3=(40 * percentage,20 * percentage, 40 * percentage),
                                  cl3=('center', 'center', 'center'),
                                  columnAttach=[(1, 'both', 0.5 * percentage), (2, 'both', 0.5 * percentage), (3, 'both', 0.5 * percentage)]
                                  ):
                    pm.textFieldButtonGrp('Save', label='', cal=(1, "right"), cw3=(0 * percentage, 32 * percentage, 10 * percentage),
                                          bl="<<",
                                          bc=partial(ad_adding_object_sel_to_textfield, 'From'))
                    pm.text('')
                    pm.textFieldButtonGrp('Load', label='', cal=(1, "right"),cw3=(0 * percentage, 32 * percentage, 10 * percentage),
                                          bl="<<",
                                          bc=partial(ad_adding_object_sel_to_textfield, 'To'))

                pm.separator(st="in", w=90 * percentage)
                with pm.rowLayout(nc=1, cw=(1, 100 * percentage), cal=(1, 'center'),
                                  columnAttach=(1, 'both', 0.5 * percentage)):
                    pm.text('Rotate Controller')
                with pm.rowLayout(nc=3, cw3=(33.3 * percentage, 33.3 * percentage, 33.3 * percentage
                                             ), cl3=('center', 'center', 'center'),
                                  columnAttach=[(1, 'both', 0 * percentage), (2, 'both', 0 * percentage),
                                                (3, 'both', 0 * percentage)]
                                  ):
                    pm.button("Mirror_X", l="X", c='', bgc=(0.5, 0, 0))
                    pm.button("Mirror_Y", l="Y", c='', bgc=(0, 0.5, 0))
                    pm.button('Mirror_Z', l="Z", c='', bgc=(0, 0, 0.5))
                pm.separator(st="in", w=90 * percentage)

    pm.showWindow()

def ad_defining_object_text_field(define_object, label):
    # if object doesn't has checkbox
    pm.textFieldButtonGrp(define_object, label=label, cal=(1, "right"),
                          bl="Get Object",
                          bc=partial(ad_adding_object_sel_to_textfield, define_object))

def ad_defining_object_text_field_no_button(define_object, label, add_feature=False, tx='', *args, **kwargs):
    if not add_feature:
        # if object doesn't has checkbox
        pm.textFieldGrp(define_object, label=label, cal=(1, "right"),
                              cw2=(31 * percentage, 69 * percentage),
                              cat=[(1, 'right', 2), (2, 'both', 2)], tx=tx)
    else:
        pm.textFieldGrp(define_object, label=label, cal=(1, "right"),
                              cw2=(26 * percentage, 69 * percentage),
                              cat=[(1, 'right', 2), (2, 'both', 2)],tx=tx,
                              **kwargs)

def ad_adding_multiple_object_sel_to_texfield(text_input, *args):
    select = pm.ls(sl=True, l=True, tr=True)
    list_joint = (','.join([item.name() for item in select]))
    pm.textFieldGrp(text_input, e=True, tx=str(list_joint))


def ad_adding_object_sel_to_textfield(text_input, button, *args):
    # elect and add object
    select = pm.ls(sl=True, l=True, tr=True)
    if len(select) == 1:
        object_selection = select[0]
        pm.textFieldButtonGrp(text_input, e=True, tx=object_selection, bl="<<")
    else:
        pm.error("please select one object!")

def ad_enabling_disabling_ui(object, tx, value, *args):
    # query for enabling and disabling layout
    for item in object:
        objectType = pm.objectTypeUI(item)
        if objectType == 'rowGroupLayout':
            pm.textFieldGrp(item, edit=True, enable=value, tx=tx)
        else:
            pass

def ad_color_index():
    MAX_OVERRIDE_COLORS=32
    columns = MAX_OVERRIDE_COLORS / 4
    rows = 4
    cell_width = 17
    color_palette = pm.palettePort(dimensions=(columns, rows),
                                     transparent=0,
                                     width=(columns * cell_width),
                                     height=(rows * cell_width),
                                     topDown=True,
                                     colorEditable=False)
    for index in range(1, MAX_OVERRIDE_COLORS):
        color_component = pm.colorIndex(index, q=True)
        pm.palettePort(color_palette,
                         edit=True,
                         rgbValue=(index, color_component[0], color_component[1], color_component[2]))

    pm.palettePort(color_palette,
                     edit=True,
                     rgbValue=(0, 0.6, 0.6, 0.6))

def ad_channelbox_translation(*args):
    pm.columnLayout()
    all_trans = pm.checkBox('All_Trans', label='All Translation', value=False, cc=partial(ad_checkbox_check_channel_translate, ['Trans_X', 'Trans_Y', 'Trans_Z']))
    trans_x = pm.checkBox('Trans_X', label='Translate X', value=False, cc=partial(ad_checkbox_uncheck_all_channel, ['Trans_X']))
    trans_y = pm.checkBox('Trans_Y', label='Translate Y', value=False, cc=partial(ad_checkbox_uncheck_all_channel, ['Trans_Y']))
    trans_z = pm.checkBox('Trans_Z', label='Translate Z', value=False, cc=partial(ad_checkbox_uncheck_all_channel, ['Trans_Z']))
    visibility = pm.checkBox('Visibility', label='Visibility', value=False)
    pm.setParent(u=True)

def ad_channelbox_rotation(*args):
    pm.columnLayout()
    all_rot = pm.checkBox('All_Rot', label='All Rotation', value=False, cc=partial(ad_checkbox_check_channel_rotate, ['Rot_X', 'Rot_Y', 'Rot_Z']))
    rot_x = pm.checkBox('Rot_X', label='Rotate X', value=False, cc=partial(ad_checkbox_uncheck_all_channel, ['Rot_X']))
    rot_y = pm.checkBox('Rot_Y', label='Rotate Y', value=False, cc=partial(ad_checkbox_uncheck_all_channel, ['Rot_Y']))
    rot_z = pm.checkBox('Rot_Z', label='Rotate Z', value=False, cc=partial(ad_checkbox_uncheck_all_channel, ['Rot_Z']))
    pm.setParent(u=True)

def ad_channelbox_scale(*args):
    pm.columnLayout()
    all_scale = pm.checkBox('All_Scale', label='All Scale', value=False, cc=partial(ad_checkbox_check_channel_scale, ['Scl_X', 'Scl_Y', 'Scl_Z']))
    scale_x = pm.checkBox('Scl_X', label='Scale X', value=False, cc=partial(ad_checkbox_uncheck_all_channel, ['Scl_X']))
    scale_y = pm.checkBox('Scl_Y', label='Scale Y', value=False, cc=partial(ad_checkbox_uncheck_all_channel, ['Scl_Y']))
    scale_z = pm.checkBox('Scl_Z', label='Scale Z', value=False, cc=partial(ad_checkbox_uncheck_all_channel, ['Scl_Z']))
    pm.setParent(u=True)


def ad_checkbox_check_channel_translate(objects, value, *args):
    for item in objects:
        all_trans = pm.checkBox('All_Trans', q=True, value=value)
        if all_trans==1:
            pm.checkBox(item, e=True, value=True)
        else:
            pm.checkBox(item, e=True, value=False)

def ad_checkbox_check_channel_rotate(objects, value, *args):
    for item in objects:
        all_rot = pm.checkBox('All_Rot', q=True, value=value)
        if all_rot==1:
            pm.checkBox(item, e=True, value=True)
        else:
            pm.checkBox(item, e=True, value=False)

def ad_checkbox_check_channel_scale(objects, value, *args):
    for item in objects:
        all_scale = pm.checkBox('All_Scale', q=True, value=value)
        if all_scale==1:
            pm.checkBox(item, e=True, value=True)
        else:
            pm.checkBox(item, e=True, value=False)

def ad_checkbox_uncheck_all_channel(*args):
    trans_x = pm.checkBox('Trans_X', q=True, value=True)
    trans_y = pm.checkBox('Trans_Y', q=True, value=True)
    trans_z = pm.checkBox('Trans_Z', q=True, value=True)

    rot_x = pm.checkBox('Rot_X', q=True, value=True)
    rot_y = pm.checkBox('Rot_Y', q=True, value=True)
    rot_z = pm.checkBox('Rot_Z', q=True, value=True)

    scale_x = pm.checkBox('Scl_X', q=True, value=True)
    scale_y = pm.checkBox('Scl_Y', q=True, value=True)
    scale_z = pm.checkBox('Scl_Z', q=True, value=True)

    if trans_x == 0 or trans_y==0 or trans_z == 0:
        pm.checkBox('All_Trans', e=True, value=False)

    if rot_x == 0 or rot_y==0 or rot_z == 0:
        pm.checkBox('All_Rot', e=True, value=False)

    if scale_x == 0 or scale_y==0 or scale_z == 0:
        pm.checkBox('All_Scale', e=True, value=False)

def ad_channelbox_constraint_connection(*args):
    pm.columnLayout()
    pm.checkBox('Point_Cons', label='Point Constraint', value=False, cc=partial(ad_connection_uncheck_constraint,
                                                                                ['Parent_Cons', 'Direct_Trans','Parent'], 'Point_Cons'))
    pm.checkBox('Orient_Cons', label='Orient Constraint', value=False, cc=partial(ad_connection_uncheck_constraint,
                                                                                  ['Parent_Cons', 'Direct_Rot','Parent'], 'Orient_Cons'))
    pm.checkBox('Scale_Cons', label='Scale Constraint', value=False, cc=partial(ad_connection_uncheck_constraint,
                                                                                ['Direct_Scl','Parent'], 'Scale_Cons'))
    pm.checkBox('Parent_Cons', label='Parent Constraint', value=False, cc=partial(ad_connection_uncheck_constraint,
                                                                                  ['Point_Cons','Orient_Cons','Direct_Trans','Direct_Rot','Parent'],'Parent_Cons'))
    pm.setParent(u=True)

def ad_channelbox_direct_connection(*args):
    pm.columnLayout()
    pm.checkBox('Direct_Trans', label='Direct Connect Translate', value=False, cc=partial(ad_connection_uncheck_constraint,
                                                                                          ['Parent_Cons', 'Point_Cons','Parent'],'Direct_Trans'))
    pm.checkBox('Direct_Rot', label='Direct Connect Rotate', value=False, cc=partial(ad_connection_uncheck_constraint,
                                                                                     ['Parent_Cons', 'Orient_Cons','Parent'],'Direct_Rot'))
    pm.checkBox('Direct_Scl', label='Direct Connect Scale', value=False, cc=partial(ad_connection_uncheck_constraint,
                                                                                    ['Scale_Cons','Parent'], 'Direct_Scl'))
    pm.checkBox('Parent', label='Parent', value=False, cc=partial(ad_connection_uncheck_constraint,
                                                                  ['Point_Cons','Orient_Cons','Direct_Trans','Direct_Rot', 'Parent_Cons',
                                                                   'Direct_Scl', 'Scale_Cons'],
                                                                  'Parent'))
    pm.setParent(u=True)

def ad_connection_uncheck_constraint(target, object, value, *args):
    checkbox_obj = pm.checkBox(object, q=True, value=value)
    for item in target:
        if checkbox_obj == 1:
            pm.checkBox(item, e=True, value=False)



