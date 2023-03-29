# Copyright (C) Animal Logic Pty Ltd. All rights reserved.
from __future__ import absolute_import
import logging

import sip
from AL.maya2 import cmds
from AL.utils import application
from Qt import QtCore, QtWidgets
from maya.OpenMayaUI import MQtUtil

from AL.libs.command.executor import Executor
from AL.libs.commandmaya import undoablecommands as mayacommand
from AL.rig.jobs.common.assets import icons

from edgeFlowMirror import edgeFlowMirrorUI
from weights_editor_tool import weights_editor

from AL.rig.jobs.common.commands.maya.utilities import planeWeighter

logger = logging.getLogger(__name__)

UINAME = "Skin UI"


class ToolUICmd(mayacommand.UndoablePureMayaCmdsCommand):
    uiData = {
        "title": "Skin Tools UI",
        "subtitle": "Animal Logic compiling skin tools and editor",
        "tooltip": "all in one skin tool UI",
        "iconPath": icons.OPENAPPLICATION01,
    }

    @classmethod
    def id(cls):
        return "AL.rig.tools.SkinToolUICmd"

    def doIt(self):
        uiExists = MQtUtil.findWindow(UINAME)
        if uiExists is not None:
            _application = sip.wrapinstance(int(uiExists), QtWidgets.QWidget)
            _application.show()
            _application.setWindowState(QtCore.Qt.WindowState.WindowActive)
            return _application
        uiMain = ToolUI()
        uiMain.show()
        return uiMain


class ToolUI(QtWidgets.QDialog):
    inside_maya = application.isInsideMayaUI()
    __Instance = None

    def __init__(self, parent=None):
        # UI and Maya
        object_name = UINAME
        super(ToolUI, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setObjectName(object_name)
        self.setWindowTitle("Skin UI")

        ### LAYOUT ###
        self.main_layout = QtWidgets.QVBoxLayout()

        ### SET LAYOUT ###
        self.setLayout(self.main_layout)

        ##### SKELETON UTILS GROUP
        self.group_jointUtils = QtWidgets.QGroupBox("Skeleton Utils:")
        self.group_jointUtils_layout = QtWidgets.QHBoxLayout()
        self.group_jointUtils.setLayout(self.group_jointUtils_layout)
        self.main_layout.addWidget(self.group_jointUtils)

        self.labelAllJoint_button = QtWidgets.QPushButton("Label All Joints")
        self.labelAllJoint_button.setToolTip(
            "Sets the label name and side for all joints in scene (in deform layers) to support precise mirroring"
        )
        self.group_jointUtils_layout.addWidget(self.labelAllJoint_button)

        self.randomColourJoint_button = QtWidgets.QPushButton("Random Colour Joints")
        self.randomColourJoint_button.setToolTip("Select the joints, then run the tool")
        self.group_jointUtils_layout.addWidget(self.randomColourJoint_button)

        ##### SKIN AND MESH UTILS GROUP
        self.group_skinMeshUtils = QtWidgets.QGroupBox("Skin and Mesh Utils:")
        self.grid_skinMeshUtilsLayout = QtWidgets.QGridLayout()
        self.group_skinMeshUtils.setLayout(self.grid_skinMeshUtilsLayout)

        self.renameSkCls_button = QtWidgets.QPushButton()
        self.renameSkCls_button.setText("Rename SkCls")

        self.renameSkCls_button.setToolTip(
            "Changes names for the skinCluster and respective sets, groupIds etc \n Usage: Just click the tool :)"
        )
        self.grid_skinMeshUtilsLayout.addWidget(self.renameSkCls_button, 0, 0)

        self.resetskin_button = QtWidgets.QPushButton()
        self.resetskin_button.setText("Reset Skin")

        self.resetskin_button.setToolTip(
            "Select transform nodes to resets bind pose of skin"
        )
        self.grid_skinMeshUtilsLayout.addWidget(self.resetskin_button, 0, 1)
        self.main_layout.addWidget(self.group_skinMeshUtils)

        self.surfaceUtilMesh_button = QtWidgets.QPushButton()
        self.surfaceUtilMesh_button.setText("Surface Util Mesh")

        self.surfaceUtilMesh_button.setToolTip(
            "Select a node in a surface component and run"
        )
        self.grid_skinMeshUtilsLayout.addWidget(self.surfaceUtilMesh_button, 1, 0)

        # plane weighter
        self.planeWeighter_button = QtWidgets.QPushButton()
        self.planeWeighter_button.setText("Plane Weighter")

        self.planeWeighter_button.setToolTip(
            "Tool that distributes skin weights based on a sequence of planes"
        )
        self.grid_skinMeshUtilsLayout.addWidget(self.planeWeighter_button, 1, 1)

        # TRANSFER SKIN GROUP
        self.groupBox_transferSkin = QtWidgets.QGroupBox("Transfer Skin:")
        self.group_transferSkin_layout = QtWidgets.QVBoxLayout(
            self.groupBox_transferSkin
        )

        self.keepInfluence_radioButton = QtWidgets.QRadioButton()
        self.keepInfluence_radioButton.setChecked(True)
        self.keepInfluence_radioButton.setText("SkinAs, keep influence")
        self.group_transferSkin_layout.addWidget(self.keepInfluence_radioButton)
        self.removeInfluence_radioButton = QtWidgets.QRadioButton()
        self.removeInfluence_radioButton.setText("SkinAs, remove influence")
        self.group_transferSkin_layout.addWidget(self.removeInfluence_radioButton)

        self.transferButton_button = QtWidgets.QPushButton()
        self.transferButton_button.setText("Run")
        self.transferButton_button.setToolTip(
            "Transfer skin to selected from source. \nUsage: \n- sel geo[s] to skin \n- sel source geo [last] \n- runTool"
        )
        self.group_transferSkin_layout.addWidget(self.transferButton_button)
        self.main_layout.addWidget(self.groupBox_transferSkin)

        #### SKIN AS GROUP
        self.group_skinAs = QtWidgets.QGroupBox("Skin As:")
        self.group_skinAsBox_layout = QtWidgets.QVBoxLayout()
        self.group_skinAs.setLayout(self.group_skinAsBox_layout)
        self.main_layout.addWidget(self.group_skinAs)

        self.skinAs_button = QtWidgets.QPushButton("Skin As UI")
        self.skinAs_button.setToolTip(
            "Usage: \nSelect target geometries, then the source with the skinCluster to transfer from"
        )

        self.group_skinAsBox_layout.addWidget(self.skinAs_button)

        ##### SKIN AND WEIGHT EDITOR GROUP
        self.group_skinEditor = QtWidgets.QGroupBox("Skin and Weight Editor:")
        self.group_skinEditor_layout = QtWidgets.QGridLayout()
        self.group_skinEditor.setLayout(self.group_skinEditor_layout)
        self.main_layout.addWidget(self.group_skinEditor)

        # Skin
        self.edgeFlowMirror_button = QtWidgets.QPushButton("Edge Flow Mirror")
        self.edgeFlowMirror_button.setToolTip("Open EdgeFlowMirror UI")
        self.group_skinEditor_layout.addWidget(self.edgeFlowMirror_button, 0, 0)

        self.NGSkinTools_button = QtWidgets.QPushButton("Open NG Skin 2.0")
        self.NGSkinTools_button.setToolTip(
            "NgSkin version 2.0 Toolset for maintaining skin weights"
        )
        self.group_skinEditor_layout.addWidget(self.NGSkinTools_button, 0, 1)

        # weight
        self.RPWeightEditor_button = QtWidgets.QPushButton("RP Weight Editor")
        self.RPWeightEditor_button.setToolTip(
            "A skin weights component editor inspired from Softimage."
        )
        self.group_skinEditor_layout.addWidget(self.RPWeightEditor_button, 1, 0)

        self.weightEditor_button = QtWidgets.QPushButton("Weight Editor")
        self.weightEditor_button.setToolTip("Open AL Weight Editor")
        self.group_skinEditor_layout.addWidget(self.weightEditor_button, 1, 1)

        ### SIGNAL AND SLOT #################
        executor = Executor()
        # label all joint
        self.labelAllJoint_button.clicked.connect(
            lambda: executor.execute("AL.rig.tools.LabelAllJointsCmd")
        )
        # random colour joint
        self.randomColourJoint_button.clicked.connect(
            lambda: executor.execute("AL.rig.tools.RandomJointColorsCmd")
        )
        # rename skin cluster
        self.renameSkCls_button.clicked.connect(
            lambda: executor.execute("AL.rig.tools.RenameSkinClustersCmd")
        )
        # rename skin cluster
        self.resetskin_button.clicked.connect(
            lambda: executor.execute("AL.rig.tools.ResetSkinCmd")
        )
        # radio button transfer skin
        self.keepInfluence_radioButton.toggled.connect(self.onClickedKeepInfluence)

        # radio button transfer skin weight
        self.transferButton_button.clicked.connect(
            lambda: executor.execute(
                "AL.rig.tools.SkinAsCmd", removeInfluence=self.onClickedKeepInfluence(),
            )
        )
        # skin as button
        self.skinAs_button.clicked.connect(
            lambda: executor.execute("AL.rig.tools.SkinAsUICmd")
        )

        # surface util mesh
        self.surfaceUtilMesh_button.clicked.connect(
            lambda: executor.execute("AL.rig.tools.SurfaceGeoCMD")
        )
        # plane weighter
        self.planeWeighter_button.clicked.connect(lambda: self.planeWeighter())

        # edge flow mirror ui
        self.edgeFlowMirror_button.clicked.connect(lambda: edgeFlowMirrorUI.showUI())

        # ng skin tool
        self.NGSkinTools_button.clicked.connect(
            lambda: executor.execute("AL.rig.tools.NgSkinToolsCmd")
        )

        # edge flow mirror ui
        self.RPWeightEditor_button.clicked.connect(lambda: weights_editor.run())

        # ng skin tool
        self.weightEditor_button.clicked.connect(lambda: cmds.AL_MayaWeightEditor())

    def onClickedKeepInfluence(self):
        checked = self.keepInfluence_radioButton.isChecked()
        return checked

    def planeWeighter(self):
        global toolUIInstance
        try:
            toolUIInstance.closeIt()
        except:
            pass
        toolUIInstance = planeWeighter.PlaneWeighter()
        toolUIInstance.showUp()
