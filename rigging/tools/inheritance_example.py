class Arm(object):

    def __init__(self):
        pass

    def rename(self):
        print("do rename")

    def setParent(self, parent):
        print("setParent to " + parent)


class ArmLeft(Arm): pass