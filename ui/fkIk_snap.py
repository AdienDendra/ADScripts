from __builtin__ import reload

import pymel.core as pm
from rigging.library.utils import fkIk_snap_position as sn

reload(sn)

def display():

    # create window
    adien_snap_fkIk = 'AdienSnapFkIk'
    pm.window(adien_snap_fkIk, exists=True)

    if pm.window(adien_snap_fkIk, exists=True):
        pm.deleteUI(adien_snap_fkIk)

    with pm.window(adien_snap_fkIk, title='Adien Fk/Ik Snap', width=275, height=50):
        with pm.columnLayout(rs=10, adjustableColumn=True):
            pm.button(label='Snap To Fk', width=275, height=50, backgroundColor=[0.46, 0.86, 0.46],
                      command=pm.Callback(snap_module().snap_to_fk()))
            pm.button(label='Snap To Ik', width=275, height=50, backgroundColor=[0.86, 0.46, 0.46],
                      command=pm.Callback(snap_module().snap_to_ik()))

    pm.showWindow()

def snap_module():
    snap = sn.Snapping(fkik_arm_LFT_setup='armSetupLFT_ctrl', fkik_arm_RGT_setup='armSetupRGT_ctrl',
                fkik_leg_LFT_setup='legSetupLFT_ctrl', fkik_leg_RGT_setup='legSetupRGT_ctrl')

    return snap