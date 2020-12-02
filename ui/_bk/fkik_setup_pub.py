"""
DESCRIPTION:
    FkIk Setup is tool before run FkIk match, this script purposes to setup for match Fk/Ik task.
    Works properly in any version of Autodesk Maya.
USAGE:
    You may go to this link for have more detail >>
    project.adiendendra.com/setup_fkik
AUTHOR:
    Adien Dendra
CONTACT:
    adien.dendra@gmail.com | hello@adiendendra.com
VERSION:
    1.0 - 20 September 2020 - Initial Release
***************************************************************
Copyright (C) 2020 Adien Dendra - hello@adiendendra.com>
This is commercial license can not be copied and/or
distributed without the express permission of Adien Dendra
***************************************************************
"""
vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR=True
vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXFr=False
vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXFR=object
vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXRr=None
vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXRF=len
vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbFrX=str
vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbFrR=zip
vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbFXr=range
vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbFXR=filter
from functools import partial
import pymel.core as pm
vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbF=600
vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR=0.01*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbF
vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXFb=0
vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXFR=0
vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXRb=0
vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXRF=0
def vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXbFR():
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBbXF='AD_MatchSetupFkIk'
 pm.window(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBbXF,exists=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
 if pm.window(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBbXF,exists=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR):
  pm.deleteUI(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBbXF)
 with pm.window(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBbXF,title='AD Fk/Ik Match Setup',width=600,height=800):
  with pm.scrollLayout('scroll'):
   with pm.columnLayout(rowSpacing=1*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,w=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbF,co=('both',1*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),adj=1):
    with pm.frameLayout(collapsable=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,l='Define Fk/Ik Controller',mh=5):
     with pm.rowColumnLayout('fkIk_controller_layout',nc=2,rowSpacing=(2,1*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),co=(1*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,'both',1*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),cw=[(1,5*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),(2,93*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR)],ca=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR):
      vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBbRF=pm.radioCollection()
      pm.radioButton('arm_setup_controller',label='',cc=partial(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXRrb,['FkIk_Arm_Setup_Controller','ik_ball_rotation_layout','ik_ball_layout']))
      vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXFRb(define_object='FkIk_Arm_Setup_Controller',label="Fk/Ik Arm Setup Controller:",add_feature=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,enable=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXFr)
      vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBFbX=pm.radioButton(label='',cc=partial(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXRrb,['FkIk_Leg_Setup_Controller','endlimb_fk_ctrl_layout','endlimb_joint_ctrl_layout','endlimb_ik_ctrl_layout','endlimb_ik_ctrl','End_Limb_Joint','End_Limb_Fk_Ctrl',]))
      vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXFRb(define_object='FkIk_Leg_Setup_Controller',label="Fk/Ik Leg Setup Controller:",add_feature=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
    pm.separator(h=5,st="in",w=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbF)
    with pm.frameLayout(collapsable=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,l='Define Objects',mh=5):
     vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXFRb(define_object='Upper_Limb_Joint',label="Upper Limb Joint:")
     vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXFRb(define_object='Middle_Limb_Joint',label="Middle Limb Joint:")
     vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXFRb(define_object='Lower_Limb_Joint',label="Lower Limb Joint:")
     with pm.rowColumnLayout('endlimb_joint_ctrl_layout',nc=1,rowSpacing=(1,1*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),co=(1*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,'both',1*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),cw=[(2,98*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR)]):
      vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXFRb(define_object='End_Limb_Joint',label="End Limb Joint:",enable=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXFr)
     vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXFRb(define_object='Upper_Limb_Fk_Ctrl',label="Upper Limb Fk Ctrl:")
     vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXFRb(define_object='Middle_Limb_Fk_Ctrl',label="Middle Limb Fk Ctrl:")
     vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXFRb(define_object='Lower_Limb_Fk_Ctrl',label="Lower Limb Fk Ctrl:")
     with pm.rowColumnLayout('endlimb_fk_ctrl_layout',nc=1,rowSpacing=(1,1*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),co=(1*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,'both',1*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),cw=[(2,98*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR)]):
      vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXFRb(define_object='End_Limb_Fk_Ctrl',label="End Limb Fk Ctrl:",enable=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXFr)
     with pm.rowColumnLayout(nc=2,rowSpacing=(2,1*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),co=(1*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,'both',1*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),cw=[(1,5*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),(2,93*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR)]):
      pm.checkBox(label='',cc=partial(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXRrb,['Upper_Limb_Ik_Ctrl']),value=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
      vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXFRb(define_object='Upper_Limb_Ik_Ctrl',label="Upper Limb Ik Ctrl:",add_feature=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
     vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXFRb(define_object='Pole_Vector_Ik_Ctrl',label="Pole Vector Ik Ctrl:")
     vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXFRb(define_object='Lower_Limb_Ik_Ctrl',label="Lower Limb Ik Ctrl:")
     with pm.rowColumnLayout('endlimb_ik_ctrl_layout',nc=2,rowSpacing=(2,1*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),co=(1*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,'both',1*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),cw=[(1,5*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),(2,93*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR)]):
      pm.checkBox('endlimb_ik_ctrl',label='',cc=partial(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXRrb,['End_Limb_Ik_Ctrl','ik_ball_layout','ik_ball_rotation_layout']))
      pm.checkBox('endlimb_ik_ctrl',edit=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,value=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXFr)
      vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXFRb(define_object='End_Limb_Ik_Ctrl',label="End Limb Ik Ctrl:",add_feature=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,enable=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXFr)
     with pm.rowLayout(nc=1,cw1=(35*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),cl1=('center'),columnAttach=[(1,'both',2*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR)]):
      pm.button(bgc=(1,1,0),l="Clear All Define Objects!",c=partial(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXRrF,'Upper_Limb_Joint','Middle_Limb_Joint','Lower_Limb_Joint','End_Limb_Joint','Upper_Limb_Fk_Ctrl','Middle_Limb_Fk_Ctrl','Lower_Limb_Fk_Ctrl','End_Limb_Fk_Ctrl','Upper_Limb_Ik_Ctrl','Pole_Vector_Ik_Ctrl','Lower_Limb_Ik_Ctrl','End_Limb_Ik_Ctrl'))
    pm.separator(h=5,st="in",w=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbF)
    with pm.frameLayout(collapsable=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,l='Additional Setup',mh=5):
     with pm.rowLayout(nc=3,columnAttach=[(1,'right',0),(2,'left',1*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),(3,'left',1*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR)],cw3=(30*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,18*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,18*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR)):
      pm.text('Matching Position:')
      vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBFRb=pm.radioCollection()
      vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBRXb=pm.radioButton(label='Left Side',onCommand=lambda x:vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXFbR(1))
      pm.radioButton(label='Right Side',onCommand=lambda x:vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXFbR(2))
      pm.radioCollection(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBFRb,edit=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,select=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBRXb)
     with pm.rowLayout(nc=4,columnAttach=[(1,'right',0),(2,'left',1*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),(3,'left',1*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),(4,'left',1*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR)],cw4=(30*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,18*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,18*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,20*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR)):
      pm.text('Limb Aim Axis:')
      vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBRXF=pm.radioCollection()
      vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBRbX=pm.radioButton(label='Translate X',onCommand=lambda x:vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXFbr(1))
      pm.radioButton(label='Translate Y',onCommand=lambda x:vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXFbr(2))
      pm.radioButton(label='Translate Z',onCommand=lambda x:vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXFbr(3))
      pm.radioCollection(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBRXF,edit=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,select=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBRbX)
     with pm.rowLayout(nc=3,columnAttach=[(1,'right',0),(2,'left',3.5*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),(3,'left',3.5*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR)],cw3=(40*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,20*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,20*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR)):
      pm.textFieldGrp('Fk_Ik_Attr_Name',l="Fk/Ik Controller Attr:",cw2=(30*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,10*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),tx='FkIk',cat=[(1,'right',2),(2,'both',4)])
      pm.floatFieldGrp('Fk_Value_On',l="Fk Value On:",cal=(1,"left"),cw2=(11*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,5*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),precision=1)
      pm.floatFieldGrp('Ik_Value_On',l="Ik Value On:",cal=(1,"left"),cw2=(11*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,5*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),precision=1,value1=1)
     with pm.rowColumnLayout(nc=2,rowSpacing=(2,1*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),cw=[(1,5*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),(2,93*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR)]):
      pm.checkBox('Ik_Snap_Checkbox',label='',cc=partial(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXRrb,['ik_snap_row']),value=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
      with pm.rowColumnLayout('ik_snap_row',nc=4,columnAttach=[(1,'right',0),(2,'left',2*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),(3,'left',3.5*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),(4,'left',3*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR)],cw=[(1,47*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),(2,15*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),(3,13*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),(4,13*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR)]):
       pm.textFieldButtonGrp('Ik_Snap_Ctrl_Name',l="Elbow/Knee Snap Ctrl:",cal=(1,"right"),cw3=(25*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,16*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,6*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),cat=[(1,'right',1),(2,'both',5)],bl="<<",bc=partial(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXRFr,'Ik_Snap_Ctrl_Name'),tx='wristIk_ctrl')
       pm.textFieldGrp('Ik_Snap_Attr_Name',l='Attr:',cw2=(4*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,8*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),tx='ikSnap')
       pm.floatFieldGrp('Ik_Snap_Off',l="Off:",cal=(1,"right"),cw2=(4*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,5*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),precision=1)
       pm.floatFieldGrp('Ik_Snap_On',l="On:",cal=(1,"right"),cw2=(4*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,5*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),precision=1,value1=1)
     pm.separator(h=5,st="in",w=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbF)
     pm.radioCollection(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBbRF,edit=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,select=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBFbX)
     with pm.rowLayout('ik_ball_layout',nc=3,columnAttach=[(1,'right',0),(2,'left',2*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR)],cw2=(52*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,20*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR)):
      pm.textFieldButtonGrp('Ik_Toe_Wiggle_Ctrl',l="Ik Ball Toe Wiggle Ctrl:",cal=(1,"right"),cw3=(30*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,16*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,6*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),cat=[(1,'right',1),(2,'both',5)],bl="<<",bc=partial(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXRFr,'Ik_Toe_Wiggle_Ctrl'),tx='ankleIk_ctrl')
      pm.textFieldGrp('Ik_Toe_Wiggle_Attr_Name',l='Attr Toe Wiggle:',cw2=(14*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,12*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),tx='toeWiggle')
     with pm.rowLayout('ik_ball_rotation_layout',nc=5,columnAttach=[(1,'right',0),(2,'left',1*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),(3,'left',1*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),(4,'left',1*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),(5,'left',1*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR)],cw5=(30*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,18*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,18*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,17*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,16*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR)):
      pm.text('Rotation_Toe_Wiggle',l="Rotation Toe Wiggle:")
      vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBRbF=pm.radioCollection()
      vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBRFX=pm.radioButton(label='Rotate X',onCommand=lambda x:vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXFrR(1))
      pm.radioButton(label='Rotate Y',onCommand=lambda x:vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXFrR(2))
      pm.radioButton(label='Rotate Z',onCommand=lambda x:vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXFrR(3))
      pm.radioCollection(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBRbF,edit=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,select=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBRFX)
      pm.checkBox('Reverse_Wiggle_Value',l='Reverse')
     pm.separator(h=5,st="in",w=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbF)
     with pm.rowLayout(nc=2,columnAttach=[(1,'left',0),(2,'right',1*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),],cw2=(5*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,55*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR)):
      pm.checkBox('Translate_Fk',label='',cc=partial(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXRrb,['row_column_stretch_fk_add_object','stretch_attribute_connected_with']))
      pm.text('Using stretch attribute instead of Fk controller translate?')
     with pm.rowColumnLayout('stretch_attribute_connected_with',nc=3,columnAttach=[(1,'right',0),(2,'left',1*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),(3,'left',1.5*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR)],cw=[(1,30*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),(2,18*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),(3,18*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR)],en=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXFr):
      pm.text('Which attribute connected with?:')
      vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBRFb=pm.radioCollection()
      vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXBbF=pm.radioButton(label='Scale',onCommand=lambda x:vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXFRr(1))
      pm.radioButton(label='Translate',onCommand=lambda x:vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXFRr(2))
      pm.radioCollection(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBRFb,edit=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,select=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXBbF)
     with pm.rowColumnLayout("row_column_stretch_fk_add_object",nc=3,cw=[(1,42*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),(2,28*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),(3,19*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR)],en=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXFr):
      pm.textFieldButtonGrp('Fk_Ctrl_Up_Stretch',l="Ctrl 1st Stretch:",cal=(1,"right"),cw3=(16*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,18*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,10*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),cat=[(3,'left',2)],tx='upperFk_ctrl',bl="<<",bc=partial(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXRFr,'Fk_Ctrl_Up_Stretch'))
      pm.textFieldGrp('Fk_Attr_Up_Stretch',l="Attr Name:",cal=(1,"right"),cw2=(12*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,10*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),tx='stretch',)
      pm.floatFieldGrp('Fk_Value_Up_Stretch',l="Default Value:",cal=(1,"right"),cw2=(12*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,5*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),precision=1,value1=1)
      pm.textFieldButtonGrp('Fk_Ctrl_Mid_Stretch',l="Ctrl 2nd Stretch:",cal=(1,"right"),cw3=(16*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,18*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,10*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),cat=[(3,'left',2)],tx='middleFk_ctrl',bl="<<",bc=partial(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXRFr,'Fk_Ctrl_Mid_Stretch'))
      pm.textFieldGrp('Fk_Attr_Mid_Stretch',l="Attr Name:",cal=(1,"right"),cw2=(12*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,10*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),tx='stretch',)
      pm.floatFieldGrp('Fk_Value_Mid_Stretch',l="Default Value:",cal=(1,"right"),cw2=(12*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,5*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),precision=1,value1=1)
    pm.separator(h=5,st="in",w=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbF)
    with pm.frameLayout(collapsable=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,l='Additional Attributes Set to Default',mh=5):
     with pm.rowLayout(nc=2,cw2=(49*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,49*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),cl2=('center','center'),columnAttach=[(1,'both',2*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),(2,'both',2*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR)]):
      pm.button(l="Add Object And Set Default Attribute Value",bgc=(0,0,0.5),c=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXRbr)
      pm.button(l="Delete Object And Set Default Attribute Value",bgc=(0.5,0,0),c=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXRbF)
      pm.setParent(u=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
      pm.rowColumnLayout("row_column_add_object",nc=5,cw=[(1,37*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),(2,22*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),(3,25*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),(4,7*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),(5,7*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR)])
      pm.setParent(u=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
    pm.separator(h=5,st="in",w=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbF)
    with pm.frameLayout(collapsable=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,l='Setup',mh=5):
     pm.text(l='Select Leg/Arm Ctrl Setup :')
     with pm.rowLayout(nc=2,cw2=(49*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,49*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),cl2=('center','center'),columnAttach=[(1,'both',2*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),(2,'both',2*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR)]):
      pm.button("run_setup",bgc=(0,0.5,0),l="Run Setup",c=partial(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbrRF))
      pm.button("delete_setup",bgc=(0.5,0,0),l="Delete Setup",c=partial(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrF))
    pm.separator(h=10,st="in",w=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbF)
    with pm.rowLayout(nc=3,cw3=(32*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,32*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,32*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),cl3=('left','center','right'),columnAttach=[(1,'both',2*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),(2,'both',2*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),(3,'both',2*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR)]):
     pm.text(l='Adien Dendra | 10/2020',al='left')
     pm.text(l='<a href="http://projects.adiendendra.com/">find out how to use it! >> </a>',hl=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,al='center')
     pm.text(l='Version 1.0',al='right')
    pm.separator(h=1,st="none",w=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbF)
   pm.setParent(u=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
 pm.showWindow()
def vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXbRr(*args):
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXBbR=[]
 if vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXFR==1:
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXBbR='Left'
 elif vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXFR==2:
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXBbR='Right'
 else:
  pass
 return vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXBbR
def vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXbRF(axis='',*args):
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXBFb=[]
 if vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXRF==1:
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXBFb='scale'+axis
 elif vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXRF==2:
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXBFb='translate'+axis
 else:
  pass
 return vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXBFb
def vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXFrb(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXFR='',*args):
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXBFR,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXBRb,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXBRF,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbBF,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbBR,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbFB=[],[],[],[],[],[]
 if vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXFb==1:
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXBRb='translateX'
 elif vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXFb==2:
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXBRb='translateY'
 elif vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXFb==3:
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXBRb='translateZ'
 else:
  pass
 if vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXRb==1:
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbBF='rotateX'
 elif vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXRb==2:
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbBF='rotateY'
 elif vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXRb==3:
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbBF='rotateZ'
 else:
  pass
 if vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXFb==1:
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbFB='scaleX'
 elif vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXFb==2:
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbFB='scaleY'
 elif vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXFb==3:
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbFB='scaleZ'
 else:
  pass
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXBFR=pm.getAttr('%s.%s'%(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXFR,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXBRb))
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXBRF=pm.getAttr('%s.%s'%(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXFR,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbBF))
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbBR=pm.getAttr('%s.%s'%(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXFR,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbFB))
 return vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXBFR,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXBRb,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXBRF,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbBF,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbBR,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbFB,
def vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXFrR(on):
 global vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXRb
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXRb=on
def vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXFbr(on):
 global vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXFb
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXFb=on
def vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXFbR(on):
 global vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXFR
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXFR=on
def vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXFRr(on):
 global vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXRF
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXRF=on
def vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXFRb(define_object=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXRr,label=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXRr,add_feature=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXFr,*args,**kwargs):
 if not add_feature:
  pm.textFieldButtonGrp(define_object,label=label,cal=(1,"right"),cw3=(30*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,54*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,15*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),cat=[(1,'right',2),(2,'both',2),(3,'left',2)],bl="Get Object",bc=partial(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXRFr,define_object))
 else:
  pm.textFieldButtonGrp(define_object,label=label,cal=(1,"right"),cw3=(25*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,54*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,15*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),cat=[(1,'right',2),(2,'both',2),(3,'left',2)],bl="Get Object",bc=partial(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXRFr,define_object),**kwargs)
def vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXRrb(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXFR=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXRr,value=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXRr,*args):
 for vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbFR in vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXFR:
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbRB=pm.objectTypeUI(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbFR)
  if vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbRB=='rowGroupLayout':
   pm.textFieldButtonGrp(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbFR,edit=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,enable=value,tx='')
  elif vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbRB=='rowColumnLayout':
   pm.rowColumnLayout(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbFR,edit=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,enable=value)
  elif vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbRB=='checkBox':
   pm.checkBox(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbFR,edit=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,enable=value)
  elif vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbRB=='rowLayout':
   if value:
    pm.rowLayout(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbFR,edit=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,enable=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXFr)
   else:
    pm.rowLayout(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbFR,edit=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,enable=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
  else:
   pass
def vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXRrF(*args):
 for vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbRF in args:
  if vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbRF:
   pm.textFieldButtonGrp(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbRF,edit=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,tx='')
  else:
   pass
def vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXRbr(*args):
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXFBb=pm.rowColumnLayout("row_column_add_object",q=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,ca=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
 if vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXFBb:
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXFBR=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXRF(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXFBb)/5+1
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXFbB="default_value"+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbFrX(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXFBR)
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXFbR="attribute"+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbFrX(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXFBR)
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXFRB="object"+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbFrX(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXFBR)
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXFRb='fk_ik_choose'+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbFrX(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXFBR)
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXRBb="fk_add_setup"+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbFrX(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXFBR)
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXRBF="ik_add_setup"+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbFrX(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXFBR)
 else:
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXFbB="default_value1"
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXFbR="attribute1"
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXFRB="object1"
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXFRb='fk_ik_choose1'
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXRBb="fk_add_setup1"
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXRBF="ik_add_setup1"
 pm.textFieldButtonGrp(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXFRB,l="Object:",cal=(1,"right"),cw3=(8*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,22*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,7*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),p="row_column_add_object",cat=[(3,'left',2)],bl="<<",bc=partial(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXRFr,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXFRB))
 pm.textFieldGrp(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXFbR,l="Attr:",cal=(1,"right"),cw2=(6*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,14*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),p="row_column_add_object")
 pm.floatFieldGrp(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXFbB,l="Set Default Value:",cal=(1,"right"),cw2=(16*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR,6*vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrBXbR),p="row_column_add_object",precision=3)
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXRbB=pm.radioCollection(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXFRb,p='row_column_add_object')
 pm.radioButton(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXRBb,label='Fk',p='row_column_add_object')
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXRbF=pm.radioButton(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXRBF,label='Ik',p='row_column_add_object')
 pm.radioCollection(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXRbB,edit=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,select=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXRbF)
def vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXRbF(*args):
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXFBb=pm.rowColumnLayout("row_column_add_object",q=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,ca=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
 if vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXFBb:
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXRFB=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXRF(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXFBb)
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXRFb="default_value"+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbFrX(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXRFB/5)
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbBXF="attribute"+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbFrX(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXRFB/5)
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbBXR="object"+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbFrX(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXRFB/5)
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbBFX="fk_add_setup"+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbFrX(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXRFB/5)
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbBFR="ik_add_setup"+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbFrX(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXRFB/5)
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbBRX="fk_ik_choose"+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbFrX(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXRFB/5)
  pm.deleteUI(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXRFb,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbBXF,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbBXR,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbBFX,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbBFR,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbBRX)
 else:
  pass
def vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXRFr(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbXBR,*args):
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbBRF=pm.ls(sl=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,l=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,tr=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
 if vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXRF(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbBRF)==1:
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbXBF=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbBRF[0]
  pm.textFieldButtonGrp(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbXBR,e=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,tx=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbXBF)
 else:
  pm.error("please select one object!")
def vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXRFb(object_define,*args):
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbXFB=[]
 if(pm.textFieldButtonGrp(object_define,q=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,en=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)):
  if(pm.textFieldButtonGrp(object_define,q=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,tx=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)):
   vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbXFB=pm.textFieldButtonGrp(object_define,q=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,tx=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
   if pm.ls(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbXFB):
    vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbXFB=pm.textFieldButtonGrp(object_define,q=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,tx=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
   else:
    pm.error('%s has wrong input object name.'%object_define,"There is no object with name '%s'!"%vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbXFB)
  else:
   pm.error('%s can not be empty!'%object_define)
 else:
  pass
 return vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbXFB,object_define
def vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbrXF(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRXB,joint,controller,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRXF):
 pm.select(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRXB[0])
 pm.addAttr(longName='Translate'+'_'+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRXF,attributeType='double3')
 pm.addAttr(longName='Translate'+'_'+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRXF+'_x',attributeType='double',parent='Translate'+'_'+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRXF)
 pm.addAttr(longName='Translate'+'_'+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRXF+'_y',attributeType='double',parent='Translate'+'_'+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRXF)
 pm.addAttr(longName='Translate'+'_'+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRXF+'_z',attributeType='double',parent='Translate'+'_'+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRXF)
 pm.addAttr(longName='Rotate'+'_'+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRXF,attributeType='double3')
 pm.addAttr(longName='Rotate'+'_'+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRXF+'_x',attributeType='double',parent='Rotate'+'_'+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRXF)
 pm.addAttr(longName='Rotate'+'_'+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRXF+'_y',attributeType='double',parent='Rotate'+'_'+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRXF)
 pm.addAttr(longName='Rotate'+'_'+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRXF+'_z',attributeType='double',parent='Rotate'+'_'+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRXF)
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbXRB=pm.xform(joint,ws=1,q=1,t=1)
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbXRF=pm.xform(joint,ws=1,q=1,ro=1)
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbFBX=pm.xform(controller,ws=1,q=1,t=1)
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbFBR=pm.xform(controller,ws=1,q=1,ro=1)
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbFXB=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbFBX[0]-vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbXRB[0]
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbFXR=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbFBX[1]-vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbXRB[1]
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbFRB=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbFBX[2]-vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbXRB[2]
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbFRX=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbFBR[0]-vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbXRF[0]
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRBX=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbFBR[1]-vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbXRF[1]
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRBF=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbFBR[2]-vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbXRF[2]
 pm.setAttr('%s.%s'%(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRXB[0],'Translate'+'_'+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRXF+'_x'),vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbFXB,l=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
 pm.setAttr('%s.%s'%(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRXB[0],'Translate'+'_'+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRXF+'_y'),vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbFXR,l=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
 pm.setAttr('%s.%s'%(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRXB[0],'Translate'+'_'+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRXF+'_z'),vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbFRB,l=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
 pm.setAttr('%s.%s'%(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRXB[0],'Rotate'+'_'+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRXF+'_x'),vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbFRX,l=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
 pm.setAttr('%s.%s'%(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRXB[0],'Rotate'+'_'+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRXF+'_y'),vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRBX,l=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
 pm.setAttr('%s.%s'%(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRXB[0],'Rotate'+'_'+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRXF+'_z'),vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRBF,l=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
def vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbrXR(Upper_Limb_Joint_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXRr,Middle_Limb_Joint_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXRr,Lower_Limb_Joint_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXRr,End_Limb_Joint_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXRr,ik_snap_ctrl=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXRr,fk_ctrl_up_stretch=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXRr,fk_ctrl_mid_stretch=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXRr,fkIk_setup_ctrl=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXRr,ik_toe_wiggle_ctrl=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXRr):
 pm.addAttr(fkIk_setup_ctrl[0],ln='Snapping_Position',dt='string')
 pm.setAttr('%s.Snapping_Position'%fkIk_setup_ctrl[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXbRr(),l=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
 pm.addAttr(fkIk_setup_ctrl[0],ln='Aim_Axis',dt='string')
 pm.setAttr('%s.Aim_Axis'%fkIk_setup_ctrl[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXFrb(Lower_Limb_Joint_Define[0])[1],l=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
 pm.addAttr(fkIk_setup_ctrl[0],ln='Middle_Translate_Aim_Joint',at='float')
 pm.setAttr('%s.Middle_Translate_Aim_Joint'%fkIk_setup_ctrl[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXFrb(Middle_Limb_Joint_Define[0])[0],l=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
 pm.addAttr(fkIk_setup_ctrl[0],ln='Lower_Translate_Aim_Joint',at='float')
 pm.setAttr('%s.Lower_Translate_Aim_Joint'%fkIk_setup_ctrl[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXFrb(Lower_Limb_Joint_Define[0])[0],l=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
 pm.addAttr(fkIk_setup_ctrl[0],ln='Upper_Scale_Aim_Joint',at='float')
 pm.setAttr('%s.Upper_Scale_Aim_Joint'%fkIk_setup_ctrl[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXFrb(Upper_Limb_Joint_Define[0])[4],l=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
 pm.addAttr(fkIk_setup_ctrl[0],ln='Middle_Scale_Aim_Joint',at='float')
 pm.setAttr('%s.Middle_Scale_Aim_Joint'%fkIk_setup_ctrl[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXFrb(Middle_Limb_Joint_Define[0])[4],l=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFBXR=pm.textFieldGrp('Fk_Ik_Attr_Name',q=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,tx=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
 if pm.objExists(fkIk_setup_ctrl[0]+'.'+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFBXR):
  pm.addAttr(fkIk_setup_ctrl[0],ln='Fk_Ik_Attr_Name',dt='string')
  pm.setAttr('%s.Fk_Ik_Attr_Name'%fkIk_setup_ctrl[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFBXR,l=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
 else:
  pm.error("There is no attribute name '%s' in the scene. " "Please check your Fk/Ik input attribute name!"%vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFBXR)
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFBbX=pm.floatFieldGrp('Fk_Value_On',q=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,value1=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
 pm.addAttr(fkIk_setup_ctrl[0],ln='Fk_Value_On',at='float')
 pm.setAttr('%s.Fk_Value_On'%fkIk_setup_ctrl[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFBbX,l=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFBbR=pm.floatFieldGrp('Ik_Value_On',q=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,value1=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
 pm.addAttr(fkIk_setup_ctrl[0],ln='Ik_Value_On',at='float')
 pm.setAttr('%s.Ik_Value_On'%fkIk_setup_ctrl[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFBbR,l=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFBRX=pm.checkBox('Ik_Snap_Checkbox',q=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,value=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
 pm.addAttr(fkIk_setup_ctrl[0],ln='Ik_Snap_Checkbox',at='bool')
 pm.setAttr('%s.Ik_Snap_Checkbox'%fkIk_setup_ctrl[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFBRX,l=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
 if pm.rowColumnLayout('ik_snap_row',q=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,enable=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR):
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFBRb=pm.textFieldGrp('Ik_Snap_Attr_Name',q=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,tx=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
  if pm.objExists(ik_snap_ctrl+'.'+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFBRb):
   pm.addAttr(fkIk_setup_ctrl[0],ln='Ik_Snap_Attr_Name',dt='string')
   pm.setAttr('%s.Ik_Snap_Attr_Name'%fkIk_setup_ctrl[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFBRb,l=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
  else:
   pm.error("There is no controller '%s' with attribute name '%s' in the scene. Please check both the input name!"%(ik_snap_ctrl,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFBRb))
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFXBb=pm.floatFieldGrp('Ik_Snap_Off',q=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,value1=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
  pm.addAttr(fkIk_setup_ctrl[0],ln='Ik_Snap_Off',at='float')
  pm.setAttr('%s.Ik_Snap_Off'%fkIk_setup_ctrl[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFXBb,l=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFXBR=pm.floatFieldGrp('Ik_Snap_On',q=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,value1=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
  pm.addAttr(fkIk_setup_ctrl[0],ln='Ik_Snap_On',at='float')
  pm.setAttr('%s.Ik_Snap_On'%fkIk_setup_ctrl[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFXBR,l=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
 if pm.rowLayout('ik_ball_layout',q=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,enable=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR):
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFXbB=pm.textFieldGrp('Ik_Toe_Wiggle_Attr_Name',q=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,tx=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
  if pm.objExists(ik_toe_wiggle_ctrl+'.'+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFXbB):
   pm.addAttr(fkIk_setup_ctrl[0],ln='Ik_Toe_Wiggle_Attr_Name',dt='string')
   pm.setAttr('%s.Ik_Toe_Wiggle_Attr_Name'%fkIk_setup_ctrl[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFXbB,l=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
  else:
   pm.error("There is no controller '%s' with attribute name '%s' in the scene. Please check both the input name!"%(ik_toe_wiggle_ctrl,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFXbB))
 if pm.rowLayout('ik_ball_rotation_layout',q=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,enable=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR):
  pm.addAttr(fkIk_setup_ctrl[0],ln='Rotation_Wiggle',dt='string')
  pm.setAttr('%s.Rotation_Wiggle'%fkIk_setup_ctrl[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXFrb(End_Limb_Joint_Define[0])[3],l=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFXRB=pm.checkBox('Reverse_Wiggle_Value',q=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,value=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
  pm.addAttr(fkIk_setup_ctrl[0],ln='Reverse_Wiggle_Value',at='bool')
  pm.setAttr('%s.Reverse_Wiggle_Value'%fkIk_setup_ctrl[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFXRB,l=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFXRb=pm.checkBox('Translate_Fk',q=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,value=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
 pm.addAttr(fkIk_setup_ctrl[0],ln='Translate_Fk_Ctrl_Exists',at='bool')
 pm.setAttr('%s.Translate_Fk_Ctrl_Exists'%fkIk_setup_ctrl[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFXRb,l=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
 if pm.rowColumnLayout('stretch_attribute_connected_with',q=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,enable=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR):
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFbBX=pm.getAttr('%s.Aim_Axis'%fkIk_setup_ctrl[0])
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFbBR=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFbBX.replace('translate','')
  pm.addAttr(fkIk_setup_ctrl[0],ln='Stretch_Attr',dt='string')
  pm.setAttr('%s.Stretch_Attr'%fkIk_setup_ctrl[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXbRF(axis=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFbBR),l=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
 if pm.rowColumnLayout('row_column_stretch_fk_add_object',q=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,enable=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR):
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFbXR=pm.textFieldGrp('Fk_Attr_Up_Stretch',q=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,tx=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
  if pm.objExists(fk_ctrl_up_stretch+'.'+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFbXR):
   pm.addAttr(fkIk_setup_ctrl[0],ln='Fk_Attr_Up_Stretch',dt='string')
   pm.setAttr('%s.Fk_Attr_Up_Stretch'%fkIk_setup_ctrl[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFbXR,l=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
  else:
   pm.error("There is no controller '%s' with attribute name '%s' in the scene. Please check both the input name!"%(fk_ctrl_up_stretch,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFbXR))
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFbRB=pm.floatFieldGrp('Fk_Value_Up_Stretch',q=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,value1=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
  pm.addAttr(fkIk_setup_ctrl[0],ln='Fk_Value_Up_Stretch',at='float')
  pm.setAttr('%s.Fk_Value_Up_Stretch'%fkIk_setup_ctrl[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFbRB,l=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFbRX=pm.textFieldGrp('Fk_Attr_Mid_Stretch',q=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,tx=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
  if pm.objExists(fk_ctrl_mid_stretch+'.'+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFbRX):
   pm.addAttr(fkIk_setup_ctrl[0],ln='Fk_Attr_Mid_Stretch',dt='string')
   pm.setAttr('%s.Fk_Attr_Mid_Stretch'%fkIk_setup_ctrl[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFbRX,l=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
  else:
   pm.error("There is no controller '%s' with attribute name '%s' in the scene. Please check both the input name!"%(fk_ctrl_mid_stretch,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFbRX))
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFRBX=pm.floatFieldGrp('Fk_Value_Mid_Stretch',q=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,value1=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
  pm.addAttr(fkIk_setup_ctrl[0],ln='Fk_Value_Mid_Stretch',at='float')
  pm.setAttr('%s.Fk_Value_Mid_Stretch'%fkIk_setup_ctrl[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFRBX,l=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
def vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbrFX(name=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXRr,side=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXRr,fk_or_ik_controller=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXRr,object_joint=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXRr):
 pm.select(cl=1)
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFRBb=pm.joint(n=name+'_'+side+'_GDE_jnt')
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFRXB=name+'_Guide_Joint'
 pm.parent(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFRBb,object_joint)
 if fk_or_ik_controller:
  pm.delete(pm.parentConstraint(fk_or_ik_controller,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFRBb,mo=0))
 else:
  pm.delete(pm.parentConstraint(object_joint,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFRBb,mo=0))
 pm.makeIdentity(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFRBb,apply=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,translate=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,rotate=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
 if fk_or_ik_controller:
  pm.connectAttr(fk_or_ik_controller+'.rotateOrder',vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFRBb+'.rotateOrder')
 else:
  pm.connectAttr(object_joint+'.rotateOrder',vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFRBb+'.rotateOrder')
 pm.setAttr(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFRBb+'.radius',0.1)
 pm.setAttr(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFRBb+'.drawStyle',2)
 return vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFRBb,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFRXB
def vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbrFR(prefix=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXRr,Upper_Limb_Fk_Ctrl_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXRr,Upper_Limb_Ik_Ctrl_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXRr,Upper_Limb_Joint_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXRr,Middle_Limb_Fk_Ctrl_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXRr,Middle_Limb_Ik_Ctrl_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXRr,Middle_Limb_Joint_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXRr,Lower_Limb_Fk_Ctrl_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXRr,Lower_Limb_Ik_Ctrl_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXRr,Lower_Limb_Joint_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXRr,leg=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXFr,End_Limb_Joint_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXRr,End_Limb_Fk_Ctrl_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXRr,End_Limb_Ik_Ctrl_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXRr):
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFRbX=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbrFX(name="upper%s_Fk"%prefix,side=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXbRr(),fk_or_ik_controller=Upper_Limb_Fk_Ctrl_Define[0],object_joint=Upper_Limb_Joint_Define[0])
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRBXb='Upper_Limb_Fk_Guide_Joint'
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRBXF=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbrFX(name="upper%s_Ik"%prefix,side=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXbRr(),fk_or_ik_controller=Upper_Limb_Ik_Ctrl_Define[0],object_joint=Upper_Limb_Joint_Define[0])
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRBbX='Upper_Limb_Ik_Guide_Joint'
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRBbF=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbrFX(name="middle%s_Fk"%prefix,side=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXbRr(),fk_or_ik_controller=Middle_Limb_Fk_Ctrl_Define[0],object_joint=Middle_Limb_Joint_Define[0])
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRBFX='Middle_Limb_Fk_Guide_Joint'
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRBFb=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbrFX(name="middle%s_Ik"%prefix,side=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXbRr(),fk_or_ik_controller=Middle_Limb_Ik_Ctrl_Define[0],object_joint=Middle_Limb_Joint_Define[0])
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRXBb='Middle_Limb_Ik_Guide_Joint'
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRXBF=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbrFX(name="lower%s_Fk"%prefix,side=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXbRr(),fk_or_ik_controller=Lower_Limb_Fk_Ctrl_Define[0],object_joint=Lower_Limb_Joint_Define[0])
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRXbB='Lower_Limb_Fk_Guide_Joint'
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRXbF=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbrFX(name="lower%s_Ik"%prefix,side=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXbRr(),fk_or_ik_controller=Lower_Limb_Ik_Ctrl_Define[0],object_joint=Lower_Limb_Joint_Define[0])
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRXFB='Lower_Limb_Ik_Guide_Joint'
 if leg:
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRXFb=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbrFX(name="end%s_Fk"%prefix,side=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXbRr(),fk_or_ik_controller=End_Limb_Fk_Ctrl_Define[0],object_joint=End_Limb_Joint_Define[0])
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRbBX='End_Limb_Fk_Guide_Joint'
  if End_Limb_Ik_Ctrl_Define[0]:
   vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRbBF=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbrFX(name="end%s_Ik"%prefix,side=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXbRr(),fk_or_ik_controller=End_Limb_Ik_Ctrl_Define[0],object_joint=End_Limb_Joint_Define[0])
   vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRbXB='End_Limb_Ik_Guide_Joint'
  else:
   vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRbBF=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbrFX(name="end%s_Ik"%prefix,side=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXbRr(),fk_or_ik_controller=End_Limb_Joint_Define[0],object_joint=End_Limb_Joint_Define[0])
   vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRbXB='End_Limb_Ik_Guide_Joint'
  return{'upperLimb_fk_GDE_jnt':vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFRbX,'upperLimb_ik_GDE_jnt':vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRBXF,'middleLimb_fk_GDE_jnt':vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRBbF,'middleLimb_ik_GDE_jnt':vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRBFb,'lowerLimb_fk_GDE_jnt':vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRXBF,'lowerLimb_ik_GDE_jnt':vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRXbF,'endLimb_fk_GDE_jnt':vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRXFb,'endLimb_ik_GDE_jnt':vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRbBF,'upperLimb_fk_GDE_name_box':vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRBXb,'upperLimb_ik_GDE_name_box':vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRBbX,'middleLimb_fk_GDE_name_box':vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRBFX,'middleLimb_ik_GDE_name_box':vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRXBb,'lowerLimb_fk_GDE_name_box':vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRXbB,'lowerLimb_ik_GDE_name_box':vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRXFB,'endLimb_fk_GDE_name_box':vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRbBX,'endLimb_ik_GDE_name_box':vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRbXB}
 return{'upperLimb_fk_GDE_jnt':vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFRbX,'upperLimb_ik_GDE_jnt':vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRBXF,'middleLimb_fk_GDE_jnt':vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRBbF,'middleLimb_ik_GDE_jnt':vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRBFb,'lowerLimb_fk_GDE_jnt':vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRXBF,'lowerLimb_ik_GDE_jnt':vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRXbF,'upperLimb_fk_GDE_name_box':vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRBXb,'upperLimb_ik_GDE_name_box':vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRBbX,'middleLimb_fk_GDE_name_box':vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRBFX,'middleLimb_ik_GDE_name_box':vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRXBb,'lowerLimb_fk_GDE_name_box':vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRXbB,'lowerLimb_ik_GDE_name_box':vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRXFB,}
def vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbrRX(prefix=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXRr,Upper_Limb_Joint_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXRr,Lower_Limb_Joint_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXRr,Setup_Controller=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXRr):
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRbXF=pm.shadingNode('distanceBetween',asUtility=1,n='%s_AD_MEASURE_%s_dist'%(prefix,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXbRr()))
 pm.connectAttr(Upper_Limb_Joint_Define+'.worldMatrix[0]',vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRbXF+'.inMatrix1')
 pm.connectAttr(Lower_Limb_Joint_Define+'.worldMatrix[0]',vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRbXF+'.inMatrix2')
 pm.connectAttr(Upper_Limb_Joint_Define+'.rotatePivotTranslate',vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRbXF+'.point1')
 pm.connectAttr(Lower_Limb_Joint_Define+'.rotatePivotTranslate',vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRbXF+'.point2')
 pm.addAttr(Setup_Controller,ln='Joint_Distance_Value_Dynamic',at='float')
 pm.connectAttr(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRbXF+'.distance','%s.Joint_Distance_Value_Dynamic'%Setup_Controller,l=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRbFX=pm.getAttr('%s.Joint_Distance_Value_Dynamic'%Setup_Controller)
 pm.addAttr(Setup_Controller,ln='Joint_Distance_Value_Static',at='float')
 pm.setAttr('%s.Joint_Distance_Value_Static'%Setup_Controller,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRbFX,l=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
 pm.addAttr(Setup_Controller,ln='Distance_Node',at='message')
 pm.connectAttr(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRbXF+'.message','%s.Distance_Node'%(Setup_Controller))
 return vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRbXF
def vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbrRF(*args):
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFBX=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXRFb('FkIk_Arm_Setup_Controller')
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFBb=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXRFb('FkIk_Leg_Setup_Controller')
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFBXb=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXRFb('Upper_Limb_Joint')
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRFX=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXRFb('Middle_Limb_Joint')
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRFB=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXRFb('Lower_Limb_Joint')
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFXbR=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXRFb('End_Limb_Joint')
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFXB=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXRFb('Upper_Limb_Fk_Ctrl')
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFXb=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXRFb('Middle_Limb_Fk_Ctrl')
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFbB=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXRFb('Lower_Limb_Fk_Ctrl')
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFbX=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXRFb('End_Limb_Fk_Ctrl')
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrXbF=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXRFb('Upper_Limb_Ik_Ctrl')
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrXbR=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXRFb('Pole_Vector_Ik_Ctrl')
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrXFb=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXRFb('Lower_Limb_Ik_Ctrl')
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrXFR=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXRFb('End_Limb_Ik_Ctrl')
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrXRb=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXRFb('Ik_Snap_Ctrl_Name')
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrXRF=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXRFb('Fk_Ctrl_Up_Stretch')
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbXF=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXRFb('Fk_Ctrl_Mid_Stretch')
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbXR=[vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFBX[1],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFBb[1],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFBXb[1],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRFX[1],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRFB[1],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFXB[1],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFXb[1],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFbB[1],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrXbF[1],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrXbR[1],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrXFb[1],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrXRb[1],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrXRF[1],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbXF[1],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFXbR[1],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFbX[1],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrXFR[1]]
 vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbFX=[vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFBX[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFBb[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFBXb[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRFX[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRFB[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFXB[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFXb[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFbB[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrXbF[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrXbR[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrXFb[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrXRb[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrXRF[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbXF[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFXbR[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFbX[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrXFR[0]]
 if pm.objExists('%s.%s'%(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFBX[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFBXb[1])):
  pm.error('Please delete the previous setup first before run the setup!')
 elif pm.objExists('%s.%s'%(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFBb[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFBXb[1])):
  pm.error('Please delete the previous setup first before run the setup!')
 else:
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbFR=[vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFXB[1],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrXbF[1],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFXb[1],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrXbR[1],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFbB[1],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrXFb[1],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFbX[1],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrXFR[1]]
  if(pm.textFieldButtonGrp(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFBX[1],q=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,en=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)):
   vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbRX=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbrFR(prefix='Arm',Upper_Limb_Fk_Ctrl_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFXB,Upper_Limb_Ik_Ctrl_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrXbF,Upper_Limb_Joint_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFBXb,Middle_Limb_Fk_Ctrl_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFXb,Middle_Limb_Ik_Ctrl_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRFX,Middle_Limb_Joint_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRFX,Lower_Limb_Fk_Ctrl_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFbB,Lower_Limb_Ik_Ctrl_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrXFb,Lower_Limb_Joint_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRFB,)
   vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbRF=[vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbRX['upperLimb_fk_GDE_jnt'][0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbRX['upperLimb_ik_GDE_jnt'][0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbRX['middleLimb_fk_GDE_jnt'][0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbRX['middleLimb_ik_GDE_jnt'][0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbRX['lowerLimb_fk_GDE_jnt'][0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbRX['lowerLimb_ik_GDE_jnt'][0]]
   vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrFXb=[vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbRX['upperLimb_fk_GDE_name_box'],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbRX['upperLimb_ik_GDE_name_box'],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbRX['middleLimb_fk_GDE_name_box'],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbRX['middleLimb_ik_GDE_name_box'],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbRX['lowerLimb_fk_GDE_name_box'],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbRX['lowerLimb_ik_GDE_name_box']]
   for vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrFXR,object_item,in vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbFrR(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbXR[:14],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbFX[:14]):
    pm.addAttr(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFBX[0],ln=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrFXR,at='message')
    if pm.textFieldButtonGrp(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrFXR,q=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,en=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR):
     pm.connectAttr(object_item+'.message','%s.%s'%(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFBX[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrFXR))
   for vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrFbX,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXrRb,label_joint in vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbFrR(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbFR,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbRF,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrFXb,):
    pm.addAttr(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFBX[0],ln=label_joint,at='message')
    if pm.textFieldButtonGrp(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrFbX,q=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,en=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR):
     pm.connectAttr(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXrRb+'.message','%s.%s'%(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFBX[0],label_joint))
    if not pm.listConnections(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXrRb+'.message'):
     pm.delete(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXrRb)
   vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbrRX(prefix='Arm',Upper_Limb_Joint_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFBXb[0],Lower_Limb_Joint_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRFB[0],Setup_Controller=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFBX[0])
   vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbrXR(Upper_Limb_Joint_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFBXb,Middle_Limb_Joint_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRFX,Lower_Limb_Joint_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRFB,End_Limb_Joint_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFXbR,ik_snap_ctrl=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrXRb[0],fk_ctrl_up_stretch=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrXRF[0],fk_ctrl_mid_stretch=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbXF[0],fkIk_setup_ctrl=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFBX)
  else:
   vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbRX=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbrFR(prefix='Leg',Upper_Limb_Fk_Ctrl_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFXB,Upper_Limb_Ik_Ctrl_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrXbF,Upper_Limb_Joint_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFBXb,Middle_Limb_Fk_Ctrl_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFXb,Middle_Limb_Ik_Ctrl_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRFX,Middle_Limb_Joint_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRFX,Lower_Limb_Fk_Ctrl_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFbB,Lower_Limb_Ik_Ctrl_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrXFb,Lower_Limb_Joint_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRFB,leg=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,End_Limb_Fk_Ctrl_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFbX,End_Limb_Ik_Ctrl_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrXFR,End_Limb_Joint_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFXbR)
   vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbRF=[vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbRX['upperLimb_fk_GDE_jnt'][0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbRX['upperLimb_ik_GDE_jnt'][0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbRX['middleLimb_fk_GDE_jnt'][0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbRX['middleLimb_ik_GDE_jnt'][0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbRX['lowerLimb_fk_GDE_jnt'][0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbRX['lowerLimb_ik_GDE_jnt'][0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbRX['endLimb_fk_GDE_jnt'][0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbRX['endLimb_ik_GDE_jnt'][0]]
   vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrFXb=[vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbRX['upperLimb_fk_GDE_name_box'],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbRX['upperLimb_ik_GDE_name_box'],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbRX['middleLimb_fk_GDE_name_box'],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbRX['middleLimb_ik_GDE_name_box'],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbRX['lowerLimb_fk_GDE_name_box'],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbRX['lowerLimb_ik_GDE_name_box'],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbRX['endLimb_fk_GDE_name_box'],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbRX['endLimb_ik_GDE_name_box']]
   vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrFRX=[]
   if pm.rowLayout('ik_ball_layout',q=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,enable=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR):
    vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrFRb=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXRFb('Ik_Toe_Wiggle_Ctrl')[1]
    vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrFRX=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXRFb('Ik_Toe_Wiggle_Ctrl')[0]
    vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbXR.append(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrFRb)
    vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbFX.append(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrFRX)
   for vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrFXR,object_item in vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbFrR(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbXR,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbFX):
    pm.addAttr(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFBb[0],ln=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrFXR,at='message')
    if pm.textFieldButtonGrp(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrFXR,q=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,en=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR):
     pm.connectAttr(object_item+'.message','%s.%s'%(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFBb[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrFXR))
   for vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrFbX,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXrRb,label_joint in vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbFrR(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbFR,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbRF,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrFXb,):
    pm.addAttr(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFBb[0],ln=label_joint,at='message')
    if pm.textFieldButtonGrp(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrFbX,q=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,en=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR):
     pm.connectAttr(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXrRb+'.message','%s.%s'%(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFBb[0],label_joint))
    if not pm.listConnections(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXrRb+'.message'):
     pm.delete(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXrRb)
   vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbrRX(prefix='Leg',Upper_Limb_Joint_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFBXb[0],Lower_Limb_Joint_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRFB[0],Setup_Controller=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFBb[0])
   if pm.rowLayout('ik_ball_layout',q=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,enable=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR):
    vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbrXR(Upper_Limb_Joint_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFBXb,Middle_Limb_Joint_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRFX,Lower_Limb_Joint_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRFB,End_Limb_Joint_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFXbR,ik_snap_ctrl=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrXRb[0],fk_ctrl_up_stretch=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrXRF[0],fk_ctrl_mid_stretch=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbXF[0],fkIk_setup_ctrl=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFBb,ik_toe_wiggle_ctrl=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrFRX)
   else:
    vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbrXR(Upper_Limb_Joint_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFBXb,Middle_Limb_Joint_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRFX,Lower_Limb_Joint_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRFB,End_Limb_Joint_Define=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrFXbR,ik_snap_ctrl=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrXRb[0],fk_ctrl_up_stretch=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrXRF[0],fk_ctrl_mid_stretch=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrbXF[0],fkIk_setup_ctrl=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFBb)
 if pm.rowColumnLayout("row_column_add_object",q=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,ca=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR):
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrRXb=pm.rowColumnLayout("row_column_add_object",q=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,ca=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrRXF=(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXRF(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrRXb)/5)
  if vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrRXF:
   for vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXFBR in vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbFXr(1,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrRXF+1):
    vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXFRB="object"+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbFrX(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXFBR)
    vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXFbR="attribute"+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbFrX(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXFBR)
    vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXFbB="default_value"+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbFrX(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXFBR)
    vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXFRb='fk_ik_choose'+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbFrX(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXFBR)
    vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXRBb="fk_add_setup"+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbFrX(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXFBR)
    vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXRBF="ik_add_setup"+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbFrX(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXFBR)
    vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbRF=pm.textFieldButtonGrp(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXFRB,q=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,tx=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
    vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRXF=pm.textFieldGrp(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXFbR,q=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,tx=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
    vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrRbX=pm.floatFieldGrp(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXFbB,q=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,value1=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
    vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrRbF=pm.radioCollection(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXFRb,q=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,select=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
    vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrRFX,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrRFb=[],[]
    if vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrRbF==vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXRBb:
     if pm.objExists(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbRF+'.'+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRXF):
      vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrRFX='_DOTAT_'+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRXF+'_DOFK_'+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbRF
      vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrRFb='_DOTVA_'+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRXF+'_DOFK_'+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbRF
     else:
      pm.error("There is no object '%s' with attribute name '%s' in the scene. " "Please check both of the input name!"%(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbRF,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRXF))
    else:
     if pm.objExists(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbRF+'.'+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRXF):
      vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrRFX='_DOTAT_'+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRXF+'_DOTIK_'+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbRF
      vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrRFb='_DOTVA_'+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRXF+'_DOTIK_'+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbRF
     else:
      pm.error("There is no object '%s' with attribute name '%s' in the scene. " "Please check both of the input name!"%(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbRF,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRXF))
    if vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbRF and vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbRXF:
     if(pm.textFieldButtonGrp(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFBX[1],q=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR,en=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)):
      if not pm.objExists(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFBX[0]+'.'+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrRFX):
       pm.addAttr(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFBX[0],ln=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrRFX,at='message')
       pm.connectAttr(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbRF+'.message','%s.%s'%(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFBX[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrRFX))
       pm.addAttr(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFBX[0],ln=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrRFb,at='float')
       pm.setAttr('%s.%s'%(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFBX[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrRFb),vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrRbX,l=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
      else:
       pm.warning("Text field # "+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbFrX(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrRXF)+" same object and attribute! Skipped this attribute.")
     else:
      if not pm.objExists(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFBb[0]+'.'+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrRFX):
       pm.addAttr(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFBb[0],ln=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrRFX,at='message')
       pm.connectAttr(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbRF+'.message','%s.%s'%(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFBb[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrRFX))
       pm.addAttr(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFBb[0],ln=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrRFb,at='float')
       pm.setAttr('%s.%s'%(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrRFBb[0],vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrRFb),vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrRbX,l=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
      else:
       pm.warning("Text field # "+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbFrX(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrRXF)+" same object and attribute! Skipped this attribute.")
    else:
     pm.warning("Line # "+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbFrX(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBrRXF)+" is empty! Skipped this attribute.")
 pm.confirmDialog(title='Add Inform',icon="information",message='Adding setup Fk Ik has done!')
 pm.select(cl=1)
def vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrF(*args):
 if pm.ls(sl=1):
  vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbBRF=pm.ls(sl=1)[0]
  if vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbBRF:
   vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXrbF=['FkIk_Arm_Setup_Controller','FkIk_Leg_Setup_Controller','Upper_Limb_Joint','Middle_Limb_Joint','Lower_Limb_Joint','Upper_Limb_Fk_Guide_Joint','Upper_Limb_Ik_Guide_Joint','Middle_Limb_Fk_Guide_Joint','Middle_Limb_Ik_Guide_Joint','Lower_Limb_Fk_Guide_Joint','Lower_Limb_Ik_Guide_Joint','End_Limb_Fk_Guide_Joint','End_Limb_Ik_Guide_Joint','Stretch_Attr','Upper_Scale_Aim_Joint','Middle_Scale_Aim_Joint','Joint_Distance_Value_Dynamic','Joint_Distance_Value_Static','Distance_Node','Upper_Limb_Fk_Ctrl','Middle_Limb_Fk_Ctrl','Lower_Limb_Fk_Ctrl','Upper_Limb_Ik_Ctrl','Pole_Vector_Ik_Ctrl','Lower_Limb_Ik_Ctrl','End_Limb_Joint','End_Limb_Fk_Ctrl','End_Limb_Ik_Ctrl','Middle_Translate_Aim_Joint','Ik_Snap_Ctrl_Name','Ik_Snap_Attr_Name','Ik_Snap_Off','Ik_Snap_On','Lower_Translate_Aim_Joint','Aim_Axis','Translate_Fk_Ctrl_Exists','Fk_Ik_Attr_Name','Fk_Ctrl_Up_Stretch','Fk_Ctrl_Mid_Stretch','Fk_Value_Up_Stretch','Fk_Value_Mid_Stretch','Fk_Attr_Up_Stretch','Fk_Attr_Mid_Stretch','Fk_Value_On','Ik_Value_On','Ik_Toe_Wiggle_Ctrl','Ik_Toe_Wiggle_Attr_Name','Rotation_Wiggle','Reverse_Wiggle_Value','Snapping_Position','Ik_Snap_Checkbox','Translate_Upper_Limb_Ik_Ctrl','Translate_Pole_Vector_Ik_Ctrl','Translate_Lower_Limb_Ik_Ctrl','Translate_End_Limb_Ik_Ctrl','Rotate_Upper_Limb_Ik_Ctrl','Rotate_Pole_Vector_Ik_Ctrl','Rotate_Lower_Limb_Ik_Ctrl','Rotate_End_Limb_Ik_Ctrl','Translate_Upper_Limb_Fk_Ctrl','Translate_Middle_Limb_Fk_Ctrl','Translate_Lower_Limb_Fk_Ctrl','Translate_End_Limb_Fk_Ctrl','Rotate_Upper_Limb_Fk_Ctrl','Rotate_Middle_Limb_Fk_Ctrl','Rotate_Lower_Limb_Fk_Ctrl','Rotate_End_Limb_Fk_Ctrl']
   if pm.objExists(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbBRF+'.'+'FkIk_Arm_Setup_Controller'):
    vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXrbR=pm.confirmDialog(title='Delete Confirm',message='Are you sure to delete setup?',button=['Yes','No'],defaultButton='Yes',icon="warning",cancelButton='No',dismissString='No')
    if vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXrbR=='Yes':
     vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXrFb=pm.listAttr(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbBRF)
     vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXrFR=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbFXR(lambda x:'_Guide_Joint' in x or 'AD_MEASURE' in x,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXrFb)
     for vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXrRb in vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXrFR:
      vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXrRF=pm.listConnections(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbBRF+'.'+vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXrRb,s=1)
      if vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXrRF:
       pm.delete(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXrRF)
     for vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbFR in vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXrbF:
      if pm.attributeQuery(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbFR,n=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbBRF,ex=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR):
       vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXbrF=pm.listAttr('%s.%s'%(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbBRF,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbFR),l=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
       if vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXbrF:
        pm.setAttr('%s.%s'%(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbBRF,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXbrF[0]),l=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXFr)
       pm.deleteAttr('%s.%s'%(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbBRF,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbFR))
     if vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbFXR(lambda x:'_DOTAT_' in x or '_DOTVA_' in x,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXrFb):
      vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXbrR=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbFXR(lambda x:'_DOTAT_' in x or '_DOTVA_' in x,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXrFb)
      for vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbFR in vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXbrR:
       vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXbFr=pm.listAttr('%s.%s'%(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbBRF,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbFR),l=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXrR)
       if vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXbFr:
        pm.setAttr('%s.%s'%(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbBRF,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBXbFr[0]),l=vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYBbXFr)
       pm.deleteAttr('%s.%s'%(vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbBRF,vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrXbFR))
    else:
     return vEnNWHCpzIdsogUjhTLelKawPAuMmfqSGcQyxOVtJDkiYrbBRF
   else:
    pm.warning('There are no setup exists or the setup already deleted.')
  else:
   pm.warning('There are no setup exists! Either you have selected wrong controller object or the setup already deleted.')
 else:
  pm.error('Please select either arm or leg setup to clean up the setup!')
# Created by pyminifier (https://github.com/liftoff/pyminifier)
