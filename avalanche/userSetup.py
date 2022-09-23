import maya.utils as utils


def load_menu():
    import avalanche_menu
    avalanche_menu.show_menu()


utils.executeDeferred('load_menu()')
