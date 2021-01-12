import pymel.core as pm
class Test(object):
    def __init__(self):
        self.WINDOW_NAME = 'test'
        self.prevValue = 0
    def UI(self):
        with pm.window(self.WINDOW_NAME, widthHeight=(200, 200))  as self.mainWindow:
            with pm.rowColumnLayout(nc=1):
                self.slider = pm.floatSlider( w=500,min=-10, max=10, value=0, step=0.0001,
                                              changeCommand=pm.Callback(self.action) , dragCommand=pm.Callback(self.dragSlider))
    def action(self):
        print('action')
        pm.floatSlider(self.slider, edit=True, v=0)
        self.prevValue = 0
    def dragSlider(self):
        value = pm.floatSlider(self.slider, q=True, v=True)
        deltaValue = (value - self.prevValue)
        self.scaleAction( deltaValue )
        self.prevValue = value

    def scaleAction(self, deltaValue):
        objList = [pm.PyNode(node) for node in pm.ls(selection=True)]
        for obj in objList:
            currentScale = obj.scaleX.get()
            obj.scale.set([currentScale+deltaValue, currentScale+deltaValue,currentScale+deltaValue])
            pm.makeIdentity(apply=True, s=1, n=0)
main = Test()
main.UI()