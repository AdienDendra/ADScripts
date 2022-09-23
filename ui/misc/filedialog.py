import pymel.core as pm


class SimpleBrowserUI():
    def __init__(self):
        # Create a "handle" for our UI. Nobody will ever see it, but we want to control it so we can check for it
        self.handle = 'SimpleBrowser'

        # Delete the UI if it exists - basically ensure we only ever have one instance running
        if pm.window(self.handle, exists=True):
            pm.deleteUI(self.handle)

        # Delete the prefs - this is useful while building out your UI. It can be removed for deployment though
        if pm.windowPref(self.handle, exists=True):
            pm.windowPref(self.handle, remove=True)

        # PyMEL allows us to build UIs using a python context
        # the "with" context wraps everything, and makes building UIs in Maya much simpler
        with pm.window(self.handle, title='Simple Directory Browser', width=400, height=100):

            # Create a basic layout
            with pm.columnLayout(rs=10):
                # Now we want two columns, we do this using a rowLayout and defining the numberOfColumns
                with pm.rowLayout(nc=2):
                    # Make a "browse" button and link the command using a callback
                    pm.button(label='Browse', width=80, height=30, command=pm.Callback(self.browse))
                    # A textField is where can save and visualize a string (our dir path)
                    self.target_dir = pm.textField(width=320, height=30)
                # Create our main button and link the command again
                # This time we set the backgroundColor to a soft green
                pm.button(label='Go', width=400, height=50, backgroundColor=[0.46, 0.86, 0.46],
                          command=pm.Callback(self.do_stuff))

            # Don't forget to show the window!
            pm.showWindow()

    def browse(self):
        """Basic browse function to locate an existing directory on disk
        """
        # dialogStyle defines how the UI looks, fileMode determines what we browse for
        # See the docs for more info
        files = pm.fileDialog2(dialogStyle=2, fileMode=3)
        # If the user presses "Cancel", fileDialog2 returns None so check for this
        if files is not None:
            # fileDialog2 returns a list of files selected, but for fileMode=3 we only get one, so get the first element
            self.target_dir.setText(files[0])

    def do_stuff(self):
        """This function is called when you press the "Go" button
        """
        # If the user presses "Go" without entering a path, warn them and exit gracefully
        if self.target_dir.getText() == '':
            print
            'No directory chosen yet'
            return

        # Now we can do stuff with our directory path from the UI
        print
        'Doing stuff using directory : "%s"' % self.target_dir.getText()

        print
        'Directory exists = %s' % os.path.exists(self.target_dir.getText())


SimpleBrowserUI()

import urllib2
import json


def makeObjectAt(type, position, size):
    if (type == 1):
        cmds.polyCube(height=size, width=size, depth=size)
    elif (type == 2):
        cmds.sphere(radius=size / 2)
        cmds.move(position[0], position[1], position[2])


def loadJSON():
    url = 'http://localhost:8000/data.json'
    try:
        webData = urllib2.urlopen(url)
    except Exception as e:
        print("ERROR: ", e)
    return
    data = json.loads(webData.read())
    for item in data:
        objectType = 1
        objectSize = 1
        position = [0, 0, 0]
    if ('type' in item and item['type'] == "sphere"):
        objectType = 2
    if ('x' in item):
        position[0] = item['x']
    if ('y' in item):
        position[1] = item['y']
    if ('z' in item):
        position[2] = item['z']
    if ('size' in item):
        objectSize = float(item['size'])
    print(objectType, position, objectSize)
    makeObjectAt(objectType, position, objectSize)


loadJSON()

import os
import maya.cmds as cmds


def browseCustomData():
    projDir = cmds.internalVar(userWorkspaceDir=True)
    newDir = os.path.join(projDir, 'customData')
    if (not os.path.exists(newDir)):
        os.makedirs(newDir)
    cmds.fileDialog2(startingDirectory=newDir)


browseCustomData()
