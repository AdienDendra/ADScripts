from __builtin__ import reload

import pymel.core as pm
from rigging.library.utils import fkik_snap_position as sn

reload(sn)

def display_ui():

    adien_snap_fkIk = 'AdienSnapFkIk'
    pm.window(adien_snap_fkIk, exists=True)

    if pm.window(adien_snap_fkIk, exists=True):
        pm.deleteUI(adien_snap_fkIk)

    with pm.window(adien_snap_fkIk, title='Adien Fk/Ik Snap', width=275, height=50):
        with pm.columnLayout(rs=10, adjustableColumn=True):
            pm.button(label='To Fk', width=275, height=50, backgroundColor=[0.46, 0.86, 0.46],
                      command=pm.Callback(sn.ik_to_fk))
            pm.button(label='To Ik', width=275, height=50, backgroundColor=[0.86, 0.46, 0.46],
                      command=pm.Callback(sn.fk_to_ik))

            pm.text(l='<a href="http://projects.adiendendra.com/">find out how to use it! >> </a>', hl=True)
            pm.separator(h=1, st="single")


    pm.showWindow()