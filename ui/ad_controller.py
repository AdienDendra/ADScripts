from functools import partial
import pymel.core as pm

layout = 500
percentage = 0.01 * layout

def ad_controller_ui():
    adien_controller = 'AD_Controller'
    pm.window(adien_controller, exists=True)
    if pm.window(adien_controller, exists=True):
        pm.deleteUI(adien_controller)
    with pm.window(adien_controller, title='AD Controller', width=500, height=400):
        with pm.tabLayout('tab', width=480, height=160):
            with pm.columnLayout('Create Controller', rowSpacing=1 * percentage, w=layout,
                                 co=('both', 1 * percentage)):
                pm.separator(h=10, st="in", w=95*percentage)
                with pm.rowColumnLayout(nc=2, rowSpacing=(2, 1 * percentage),
                                        co=(1 * percentage, 'both', 1 * percentage),
                                        cw=[(1, 4 * percentage), (2, 90 * percentage)]):
                    pm.checkBox(label='',
                                cc=partial(ad_enabling_disabling_ui, ['Prefix_Name']),
                                value=False)
                    ad_defining_object_text_field_no_button(define_object='Prefix_Name', label="Prefix Name:",
                                                  add_feature=True, enable=False)
                    pm.checkBox(label='',
                                cc=partial(ad_enabling_disabling_ui, ['Parent_Group_Name']),
                                value=True)
                    ad_defining_object_text_field_no_button(define_object='Parent_Group_Name', label="Parent Group Name:",
                                                  add_feature=True, tx='Main',  enable=True)
                ad_defining_object_text_field_no_button(define_object='Suffix_Name', tx='ctrl', label="Suffix Name:")

                with pm.rowLayout('Size_And_Visibility', nc=3, cw4=(32 * percentage, 32 * percentage, 30 * percentage, 30 * percentage),
                                  cl4=('right','right', 'left', 'left'),
                                  columnAttach=[(1, 'both', 0.5 * percentage), (2, 'both', 0.5 * percentage), (3, 'both', 0.5 * percentage),
                                                (4, 'both', 0.5 * percentage)]):

                    pm.floatFieldGrp('Controller_Size', l="Controller Size:", cal=(1, "right"),
                                     cw2=(32 * percentage, 12 * percentage),
                                     cat=[(1, 'right', 2), (2, 'both', 2)], value1=1.00,
                                     precision=3)
                    pm.checkBoxGrp('Target_Visibility', l='Add Attr Target Visibility:')

                pm.separator(h=10, st="in", w=95*percentage)

                with pm.rowLayout('Palette_Port', nc=2, cw2=(32 * percentage, 60 * percentage), cl2=('right', 'left'),
                                  columnAttach=[(1, 'both', 0.5 * percentage), (2, 'both', 0.5 * percentage)]):

                    pm.text('Controller Color:')
                    ad_color_index()

                with pm.rowLayout('Hide_Controller_Channel', nc=5, cw5=(32 * percentage, 25 * percentage, 20 * percentage, 20 * percentage,
                                                             20 * percentage), cl5=('right', 'left', 'left', 'left', 'left'),
                                  columnAttach=[(1, 'both', 0.5 * percentage), (2, 'both', 0.5 * percentage),
                                                (3, 'both', 0.5 * percentage), (4, 'both', 0.5 * percentage),
                                                (5, 'both', 0.5 * percentage)]):
                    pm.text('Hide Controller Channel:')
                    ad_channelbox_translation()
                    ad_channelbox_rotation()
                    ad_channelbox_scale()

                with pm.columnLayout('Controller Utilities', rowSpacing=1 * percentage, w=layout,
                                     co=('both', 1 * percentage)):
                    pm.separator(h=10, st="in", w=95*percentage)


    pm.showWindow()

def ad_defining_object_text_field_no_button(define_object, label, add_feature=False, tx='', *args, **kwargs):
    if not add_feature:
        # if object doesn't has checkbox
        pm.textFieldGrp(define_object, label=label, cal=(1, "right"),
                              cw2=(32 * percentage, 60 * percentage),
                              cat=[(1, 'right', 2), (2, 'both', 2)], tx=tx)
    else:
        pm.textFieldGrp(define_object, label=label, cal=(1, "right"),
                              cw2=(28 * percentage, 60 * percentage),
                              cat=[(1, 'right', 2), (2, 'both', 2)],tx=tx,
                              **kwargs)

def ad_adding_multiple_object_sel_to_texfield(text_input, *args):
    select = pm.ls(sl=True, l=True, tr=True)
    list_joint = (','.join([item.name() for item in select]))
    pm.textFieldGrp(text_input, e=True, tx=str(list_joint))


def ad_adding_object_sel_to_textfield(text_input, *args):
    # elect and add object
    select = pm.ls(sl=True, l=True, tr=True)
    if len(select) == 1:
        object_selection = select[0]
        pm.textFieldGrp(text_input, e=True, tx=object_selection)
    else:
        pm.error("please select one object!")

def ad_enabling_disabling_ui(object, value, *args):
    # query for enabling and disabling layout
    for item in object:
        objectType = pm.objectTypeUI(item)
        if objectType == 'rowGroupLayout':
            pm.textFieldGrp(item, edit=True, enable=value, tx='')
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
            trans_x = pm.checkBox(item, e=True, value=True)
            trans_y = pm.checkBox(item, e=True, value=True)
            trans_z = pm.checkBox(item, e=True, value=True)
        else:
            trans_x = pm.checkBox(item, e=True, value=False)
            trans_y = pm.checkBox(item, e=True, value=False)
            trans_z = pm.checkBox(item, e=True, value=False)

def ad_checkbox_check_channel_rotate(objects, value, *args):
    for item in objects:
        all_rot = pm.checkBox('All_Rot', q=True, value=value)
        if all_rot==1:
            rot_x = pm.checkBox(item, e=True, value=True)
            rot_y = pm.checkBox(item, e=True, value=True)
            rot_z = pm.checkBox(item, e=True, value=True)
        else:
            rot_x = pm.checkBox(item, e=True, value=False)
            rot_y = pm.checkBox(item, e=True, value=False)
            rot_z = pm.checkBox(item, e=True, value=False)

def ad_checkbox_check_channel_scale(objects, value, *args):
    for item in objects:
        all_scale = pm.checkBox('All_Scale', q=True, value=value)
        if all_scale==1:
            scale_x = pm.checkBox(item, e=True, value=True)
            scale_y = pm.checkBox(item, e=True, value=True)
            scale_z = pm.checkBox(item, e=True, value=True)
        else:
            scale_x = pm.checkBox(item, e=True, value=False)
            scale_y = pm.checkBox(item, e=True, value=False)
            scale_z = pm.checkBox(item, e=True, value=False)


def ad_checkbox_uncheck_all_channel(*args):
    trans_x = pm.checkBox('Trans_X', q=True, value=True)
    trans_y = pm.checkBox('Trans_Y', q=True, value=True)
    trans_z = pm.checkBox('Trans_Z', q=True, value=True)

    rot_x = pm.checkBox('Rot_X', q=True, value=True)
    rot_y = pm.checkBox('Rot_X', q=True, value=True)
    rot_z = pm.checkBox('Rot_X', q=True, value=True)

    scale_x = pm.checkBox('Scl_X', q=True, value=True)
    scale_y = pm.checkBox('Scl_Y', q=True, value=True)
    scale_z = pm.checkBox('Scl_Z', q=True, value=True)

    if trans_x == 0 or trans_y==0 or trans_z == 0:
        all_trans = pm.checkBox('All_Trans', e=True, value=False)

    if rot_x == 0 or rot_y==0 or rot_z == 0:
        all_rot = pm.checkBox('All_Rot', e=True, value=False)

    if scale_x == 0 or scale_y==0 or scale_z == 0:
        all_scale = pm.checkBox('All_Scale', e=True, value=False)




