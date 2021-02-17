import pymel.core as pm


main_window = pm.language.melGlobals['gMainWindow']
menu_obj = 'AvalancheMenu'
menu_label= 'Avalanche Tech Animator Test'

if pm.menu(menu_obj, label=menu_label, exists=True, parent=main_window):
    pm.deleteUI(pm.menu(menu_obj, e=True, deleteAllItems=True))

def show_menu():
    custom_tools_menu = pm.menu(menu_obj, label=menu_label, parent=main_window, tearOff=True)
    renamer_menu = pm.menuItem(label='Renamer', parent=custom_tools_menu, c='from avalanche import find_rename as sr \nsr.FindRenameDialog.show_ui()', tearOff=True)
    fixer_menu = pm.menuItem(label='Geo Test Scene Fixer', subMenu=True, parent=custom_tools_menu, tearOff=True)
    fix_present = pm.menuItem(label='Fix Present', parent=fixer_menu, c='from avalanche import birdy_test as bt \nreload(bt) \nbt.fix_present()', tearOff=True)
    look_at_gift = pm.menuItem(label='Look at Gift', parent=fixer_menu, c='from avalanche import birdy_test as bt \nreload(bt) \nbt.look_at_gift()', tearOff=True)
    put_on_party_hat = pm.menuItem(label='Put on Party Hat', parent=fixer_menu, c='from avalanche import birdy_test as bt \nreload(bt) \nbt.put_on_party_hat()', tearOff=True)

    pm.setParent('..', menu=True)