# Copyright (C) Animal Logic Pty Ltd. All rights reserved.
from __future__ import absolute_import
import logging

from AL.maya2 import cmds

from AL.rig.jobs.common.assets import icons
from AL.rig.jobs.common.libs import nodes
from AL.rig.jobs.common.libs import mayaViewportMsg
from AL.libs.commandmaya import undoablecommands as mayacommand
from AL.breed.ui import public as bui_public
from AL.breed.ui.services import sessionManager as buis_sessionManager

logger = logging.getLogger(__name__)


class ShapeCopyCmd(mayacommand.UndoablePureMayaCmdsCommand):
    uiData = {
        "title": "Shape Copy",
        "subtitle": "Copy / replace one shape from one transform to another",
        "tooltip": "Select the transform(s) you want to copy into the new shape, and select the transform with the shape you want to copy.",
        "iconPath": icons.COPY01,
    }

    @classmethod
    def id(cls):
        return "AL.rig.tools.ShapeCopyCmd"

    def resolve(self):
        accessor = bui_public.Accessor()
        if accessor.findApplication() is None:
            msg = "You need Breed Open to run this tool!"
            mayaViewportMsg.reportError(msg)
            return self.cancelExecution(msg)

        # secondary check to see if there is an active instance
        if buis_sessionManager.SessionManager.instance().activeManifest() is None:
            msg = "You need a valid breed session to run this tool!"
            mayaViewportMsg.reportError(msg)
            return self.cancelExecution(msg)

        selection = cmds.ls(sl=True, l=True)
        if not self.hasArgumentValue("selection"):
            if not selection or len(selection) < 2:
                logger.error(
                    "Invalid selection. Please select the source manipulator + xNum destination manipulator[s] to copy the shape[s] to."
                )
                return self.cancelExecution()

            self.setArgumentValue("selection", selection)

            # find if multiple shapes
            for manipulator in selection:
                shapes = cmds.listRelatives(manipulator, shapes=True, f=True)
                if len(shapes) > 1:
                    self.setArgumentValue("multi", True)
                    break
            else:
                self.setArgumentValue("multi", False)

    def doIt(self, selection=None, multi=None):
        if multi:
            nodes.copyMultipleShapes(nodeList=selection)
            # refresh breed
            bui_public.sessionManager().activeEntityTreeModel().updateVirtualTree()
        else:
            nodes.copyShape(nodeList=selection)
