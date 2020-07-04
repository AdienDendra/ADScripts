import maya.cmds as mc

def createGear(teeth=10, length=0.3):
    spans = teeth*2

    transform, constructor = mc.polyPipe(sa= spans)

    sideFaces = range(spans*2, spans*3, 2)

    mc.select(clear=True)

    for face in sideFaces:

         mc.select('%s.f[%s]' % (transform, face), add=True)

    extrude = mc.polyExtrudeFacet(ltz = length) [0]

    return transform, constructor, extrude

def changeTeeth(constructor, extrude, teeth=10, length=0.3):

    spans = teeth*2

    mc.polyPipe(constructor, edit =1,
                sa=spans)

    sideFaces = range(spans*2, spans*3, 2)
    faceNames = []

    for face in sideFaces:
        faceName = 'f[%s]' % face
        faceNames.append(faceName)

    mc.setAttr ('%s.inputComponents' % extrude,
                len(faceNames), *faceNames,
                type ="componentList")

    mc.polyExtrudeFacet(extrude, edit =1, ltz=length)
