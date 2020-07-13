import pymel.core as pm

main_window = pm.language.melGlobals['gMainWindow']

menu_obj = 'AdienCustomMenu'

menu_label= 'Adien Setup'

if pm.menu(menu_obj, label=menu_label, exists=True, parent=main_window):
    pm.deleteUI(pm.menu(menu_obj, e=True, deleteAllItems=True))

custom_tools_menu = pm.menu(menu_obj, label=menu_label, parent=main_window, tearOff=True)

module_menu = pm.menuItem(label='Module', subMenu=True, parent=custom_tools_menu, tearOff=True)

pipeline_menu = pm.menuItem(label='Pipeline', subMenu=True, parent=custom_tools_menu, tearOff=True)

tools_menu = pm.menuItem(label='Tools', subMenu=True, parent=custom_tools_menu, tearOff=True)

pm.setParent('..', menu=True)