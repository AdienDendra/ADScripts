import maya.cmds as mc


class Gear(object):

    def __init__(self):
        self.transform = None
        # self.extrude = None
        # self.constructor = None

    def createGear(self, teeth=10, length=0.3):
        spans = teeth * 2

        self.transform, self.constructor = mc.polyPipe(sa=spans)

        sideFaces = range(spans * 2, spans * 3, 2)

        mc.select(clear=True)

        for face in sideFaces:
            mc.select('%s.f[%s]' % (self.transform, face), add=True)

        self.extrude = mc.polyExtrudeFacet(ltz=length)[0]

    def changeTeeth(self, teeth=10, length=0.3):
        spans = teeth * 2

        mc.polyPipe(self.constructor, edit=1,
                    sa=spans)

        sideFaces = range(spans * 2, spans * 3, 2)
        faceNames = []

        for face in sideFaces:
            faceName = 'f[%s]' % face
            faceNames.append(faceName)

        mc.setAttr('%s.inputComponents' % self.extrude,
                   len(faceNames), *faceNames,
                   type="componentList")

        mc.polyExtrudeFacet(self.extrude, edit=1, ltz=length)
