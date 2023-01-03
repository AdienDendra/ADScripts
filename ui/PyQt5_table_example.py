# Copyright (C) Animal Logic Pty Ltd. All rights reserved.
from __future__ import absolute_import, division

import logging
import sip
import itertools

from AL.maya2 import omx
from maya.OpenMayaUI import MQtUtil

from Qt import QtWidgets, QtGui, QtCore

from AL.rig.jobs.common.libs import mayaViewportMsg
from AL.rig.jobs.common.assets import icons
from AL.rig.jobs.common.libs import bond as rjml_bond

from AL.breed.ui.commands import base as buicmd_base
from AL.breed.ui import public as bui_public
from AL.breed.ui.services import sessionManager as buis_sessionManager

from AL.beast.core.constants import types as bcc_types
from AL.beast.core.trees import bindings as bct_bindings
from AL.beast.maya.trees import bindings as bmt_bindings
from AL.beast.maya.public.deformers import blendshape as bmpd_blendshape

logger = logging.getLogger(__name__)

HEADERS = ("Source", "Target", "Status", "Node")
COLORS = {
    "Invalid": QtCore.Qt.magenta,
    "InActive": QtCore.Qt.yellow,
    "Live": QtCore.Qt.green,
    "Connection Break": QtCore.Qt.red,
}
NAMING = ("Local_", "_")
UINAME = "Live BS Manager"


class LiveBStoolCmds(buicmd_base.BaseCommand):
    uiData = {
        "title": "Live BlendShape Tool",
        "subtitle": "",
        "tooltip": "",
        "iconPath": icons.ACTIVE,
    }

    @classmethod
    def id(cls):
        return "AL.rig.tools.LiveBStoolcmds"

    def resolve(self):
        # first check if breed opened
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

        # exit if not select the thing
        func = bui_public.Functor()
        sel = func.entityEditor_selection()
        if not sel:
            logger.warning("Please select one of binding variation")
            return self.cancelExecution()

        # exit if not selection the binding variation
        activeBindingTree = sel[0]
        if not activeBindingTree.nodeType() == bcc_types.BEAST_BINDINGS_DATA_VARIATION:
            logger.warning(
                "Invalid selection, aborting. Please select one binding variation and try again"
            )
            return self.cancelExecution()

        self.setArgumentValue("activeBindingTree", activeBindingTree)

    def doIt(self, activeBindingTree=None):
        # initiate the ui
        uiExists = MQtUtil.findWindow(UINAME)
        if uiExists is not None:
            _application = sip.wrapinstance(int(uiExists), QtWidgets.QWidget)
            _application.show()
            _application.setWindowState(QtCore.Qt.WindowState.WindowActive)
            return _application
        ui = LiveBStoolUI(activeBindingTree)
        ui.show()


class LiveBStoolUI(QtWidgets.QDialog):
    def __init__(self, activeBindingTree=None, parent=None):
        super(LiveBStoolUI, self).__init__(parent=parent)

        # initializing variables
        self.activeBindingTree = activeBindingTree
        self.mayaSelCheckBox = None

        # main layout
        self.setWindowTitle(UINAME)
        self.setGeometry(100, 100, 600, 500)

        # layout
        mainLayout = QtWidgets.QVBoxLayout(self)
        bindingLayout = QtWidgets.QHBoxLayout()
        refreshLayout = QtWidgets.QHBoxLayout()
        upLayout = QtWidgets.QHBoxLayout()
        bottomLayout = QtWidgets.QHBoxLayout()
        filterLayout = QtWidgets.QHBoxLayout()
        updateLayout = QtWidgets.QVBoxLayout()
        descriptionLayout = QtWidgets.QGridLayout()
        addRowSelLayout = QtWidgets.QHBoxLayout()
        addRowLayout = QtWidgets.QHBoxLayout()
        selectionCheckBoxLayout = QtWidgets.QHBoxLayout()

        # refresh part widgets
        self.bindingName = QtWidgets.QLabel("Binding:")
        self.hostLineEdit = QtWidgets.QLineEdit()
        self.hostLineEdit.setText(self.activeBindingTree.name())
        self.hostLineEdit.setStyleSheet(
            "QLineEdit"
            "{"
            "background : rgb(200, 100, 20);"
            "color: rgb(40, 40, 40);"
            "font: bold;"
            "} "
        )
        self.hostLineEdit.setReadOnly(True)

        # filter and select maya widget
        self.searchField = QtWidgets.QLineEdit()
        self.searchField.setStyleSheet("font: italic;")
        self.searchField.setPlaceholderText("search filter")
        self.searchField.setMaximumWidth(200)

        # refresh widget
        self.refreshButton = QtWidgets.QPushButton(maximumWidth=20)
        self.refreshButton.setIcon(QtGui.QIcon(":/refresh.png"))
        self.refreshButton.setStyleSheet("border:none")

        bindingLayout.addWidget(self.bindingName)
        bindingLayout.addWidget(self.hostLineEdit)
        refreshLayout.addWidget(self.searchField)
        refreshLayout.addWidget(self.refreshButton)

        # add row widget
        self.addRowButton = QtWidgets.QPushButton("Add Row")
        self.selectionCheckBox = QtWidgets.QCheckBox("Check All InActive Status")
        addRowLayout.addWidget(self.addRowButton)
        selectionCheckBoxLayout.addWidget(self.selectionCheckBox)

        # table
        self.table = Table(self.hostLineEdit)

        # description widget
        liveLabel = QtWidgets.QLabel("Live")
        liveText = QtWidgets.QLabel("Live BS is connected to the source")
        validLabel = QtWidgets.QLabel("InActive")
        validText = QtWidgets.QLabel("Live BS doesn't exist, ready to connect")
        invalidLabel = QtWidgets.QLabel("Invalid")
        invalidText = QtWidgets.QLabel(
            "Live BS does exist, but not connected to the object on source column"
        )
        connectionBreakLabel = QtWidgets.QLabel("Connection Break")
        connectionBreakText = QtWidgets.QLabel("Live BS is break, source is missing")

        liveLabel.setStyleSheet("color: green")
        validLabel.setStyleSheet("color: yellow")
        invalidLabel.setStyleSheet("color: magenta")
        connectionBreakLabel.setStyleSheet("color: red")

        descriptionLayout.addWidget(liveLabel, 0, 0)
        descriptionLayout.addWidget(liveText, 0, 1)
        descriptionLayout.addWidget(validLabel, 1, 0)
        descriptionLayout.addWidget(validText, 1, 1)
        descriptionLayout.addWidget(invalidLabel, 2, 0)
        descriptionLayout.addWidget(invalidText, 2, 1)
        descriptionLayout.addWidget(connectionBreakLabel, 3, 0)
        descriptionLayout.addWidget(connectionBreakText, 3, 1)

        self.mayaSelCheckBox = QtWidgets.QCheckBox("Select In Maya")
        self.mayaSelCheckBox.setChecked(False)

        # update button widget
        text = "Update Live BS"
        self.updateButton = QtWidgets.QPushButton(text)
        width = self.updateButton.fontMetrics().boundingRect(text).width() + 30
        self.updateButton.setMaximumWidth(width)
        updateLayout.addWidget(self.updateButton)

        # add all layouts to main layout
        upLayout.addLayout(bindingLayout)
        upLayout.addLayout(refreshLayout)
        mainLayout.addLayout(upLayout)
        mainLayout.addWidget(self.table)
        addRowSelLayout.addLayout(addRowLayout)
        addRowSelLayout.addLayout(selectionCheckBoxLayout)
        mainLayout.addLayout(addRowSelLayout)
        mainLayout.addLayout(bottomLayout)
        bottomLayout.addLayout(descriptionLayout)
        bottomLayout.addLayout(updateLayout)

        # alignment
        refreshLayout.setAlignment(QtCore.Qt.AlignRight)
        bindingLayout.setAlignment(QtCore.Qt.AlignLeft)
        filterLayout.setAlignment(QtCore.Qt.AlignLeft)
        updateLayout.setAlignment(QtCore.Qt.AlignBottom)
        descriptionLayout.setAlignment(QtCore.Qt.AlignLeft)
        addRowLayout.setAlignment(QtCore.Qt.AlignLeft)
        selectionCheckBoxLayout.setAlignment(QtCore.Qt.AlignRight)

        # setup
        self.setupUI()

    def setupUI(self):
        self.loadTableCMD()
        self.connectSignal()

    def connectSignal(self):
        self.searchField.textChanged.connect(self.table.proxyModel.setFilterRegExp)
        self.updateButton.clicked.connect(self.updateCMD)
        self.refreshButton.clicked.connect(self.loadTableCMD)
        self.addRowButton.clicked.connect(self.addRowCMD)
        self.selectionCheckBox.stateChanged.connect(self.selectionCheckBoxStatus)

    def loadTableCMD(self):
        data = self.prepareData()
        self.table.setTableData(data, HEADERS)

    def addRowCMD(self):
        self.table.insertRowCMD(1)

    def updateCMD(self):
        updatedTableData = self.updatedTableData()
        geoModData = self.getGeoModifiers()
        for row in updatedTableData:
            source = row[0]
            target = row[1]

            if source not in geoModData.keys():
                continue

            if target not in geoModData.keys():
                continue

            createLiveBS(liveGeoMod=geoModData[source], destGeoMod=geoModData[target])

        bui_public.Functor().refreshEntityTree()
        self.loadTableCMD()

    def updatedTableData(self):
        # the structure data tableData list return >> [[source, target, status, node, bool check/uncheck],[....],[....]]
        tableData = self.table.getTableData()

        # valid items
        updatedTableData = []
        for row in tableData:
            if row[2] == "InActive" and row[4] == True:
                updatedTableData.append(row)
            if row[2] == "Invalid" and row[4] == True:
                updatedTableData.append(row)
            if row[2] == "Connection Break" and row[4] == True:
                # delete bond node
                removeBondNode(self.activeBindingTree, row[1], row[3])
                updatedTableData.append(row)

        return updatedTableData

    def selectionCheckBoxStatus(self):
        status = self.selectionCheckBox.isChecked()
        if status:
            self.table.checkStateTrue()
        else:
            self.table.checkStateFalse()
        self.table.viewport().update()

    def prepareData(self):
        modelData = getDataFromBreed(self.activeBindingTree)
        return modelData

    def getGeoModifiers(self):
        geoModData = {}
        for geoMod in self.activeBindingTree.iterGeoModifiers():
            geoModData[geoMod.name()] = geoMod

        return geoModData


class Table(QtWidgets.QTableView):
    def __init__(self, hostLineEdit=None):

        super(Table, self).__init__()

        self.hostLineEdit = hostLineEdit

        self.setAlternatingRowColors(True)
        self.verticalHeader().hide()
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.installEventFilter(self)

        # column width settings
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.horizontalHeader().setStretchLastSection(True)

    def eventFilter(self, source, event):
        index = self.currentIndex()
        column = index.column()

        if event.type() == QtCore.QEvent.ContextMenu and source is self:
            menu = QtWidgets.QMenu()
            load, breed, clear, remove, removeNodes = (
                list(),
                list(),
                list(),
                list(),
                list(),
            )
            if column == 3:
                breed = menu.addAction("Sync Sel in Breed")
                removeNodes = menu.addAction("Remove Live Bls Node")

            if column <= 1:
                load = menu.addAction("Load Selection")
                breed = menu.addAction("Sync Sel in Breed")
                clear = menu.addAction("Clear Cell")
                if column == 0:
                    remove = menu.addAction("Remove Selected Rows")

            action = menu.exec_(event.globalPos())
            if action == load:
                self.loadCMD()
            if action == breed:
                self.breedSyncCMD()
            if action == clear:
                self.clearCellCMD()
            if action == remove:
                self.removeRowsCMD()
            if action == removeNodes:
                self.removeBondNodeMessageBoxCMD()

        return super().eventFilter(source, event)

    def resizeEvent(self, event):
        super(Table, self).resizeEvent(event)

        # return if no rows
        if self.proxyModel.rowCount() == 0:
            return

        # get column count
        numberOfColumns = self.proxyModel.columnCount()
        tableSize = self.width()
        sideHeaderWidth = self.verticalHeader().width()
        tableSize -= sideHeaderWidth

        remainingWidth = tableSize % numberOfColumns
        for columnNum in range(numberOfColumns):
            if remainingWidth > 0:
                self.setColumnWidth(columnNum, int(tableSize / numberOfColumns) + 1)
                remainingWidth -= 1
            else:
                self.setColumnWidth(columnNum, int(tableSize / numberOfColumns))

    def checkStateFalse(self):
        for checkStateIndex in self.checkStateRoleAndStatus().keys():
            self.model.setData(
                checkStateIndex, QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole
            )

    def checkStateTrue(self):
        for checkStateIndex in self.checkStateRoleAndStatus().keys():
            self.model.setData(
                checkStateIndex, QtCore.Qt.Checked, QtCore.Qt.CheckStateRole
            )

    def checkStateRoleAndStatus(self):
        checkStateDisplay = dict()

        for row in range(self.model.rowCount()):
            statusDisplay = self.indexCheckState(row, 2, QtCore.Qt.DisplayRole)
            if statusDisplay == "InActive":
                checkstate = self.model.data(
                    self.model.index(row, 3), QtCore.Qt.CheckStateRole
                )
                checkStateIndex = self.model.index(row, 3)
                checkStateDisplay[checkStateIndex] = checkstate

        return checkStateDisplay

    def getCellValue(self, index):
        itemText = index.data()
        return itemText

    def setTableData(self, data, header):
        # model
        self.model = Model(data, header)
        self.setModel(self.model)

        # filter settings
        self.proxyModel = QtCore.QSortFilterProxyModel()
        self.proxyModel.setSourceModel(self.model)
        self.proxyModel.setFilterKeyColumn(-1)
        self.setModel(self.proxyModel)

    def indexCheckState(self, row, column, role):
        indexCheckState = self.model.data(self.model.index(row, column), role)
        if role == QtCore.Qt.CheckStateRole:
            if indexCheckState != 2:
                indexCheckState = False
            else:
                indexCheckState = True
        else:
            str(indexCheckState)

        return indexCheckState

    def getTableData(self):
        data = []
        for row in range(self.model.rowCount()):
            data.append([])
            for column in range(4):
                index = self.model.index(row, column)
                # column 1-3 data are strings
                data[row].append(str(self.model.data(index)))

            # return bool for column 4
            indexCheckState = self.indexCheckState(row, 3, QtCore.Qt.CheckStateRole)
            data[row].append(indexCheckState)

        return data

    def getColumnData(self, col):
        data = []
        for row in range(self.model.rowCount()):
            index = self.model.index(row, col)
            data.append(str(self.model.data(index)))
        return data

    def loadCMD(self):
        indexes = self.selectedIndexes()

        statusInvalid = "Invalid"
        statusLive = "Live"
        statusInActive = "InActive"

        # matching the local to non local or vice versa
        matchLocalNonLocalGeo = self.targetSourceMatchCell()

        # update the status
        for targetSource, index in zip(matchLocalNonLocalGeo, indexes):
            row = index.row()
            tgt = targetSource[0]
            src = targetSource[1]
            if not tgt or not src:
                continue
            target = tgt[0]
            source = src[0]
            blendBufferDeformersTarget = blendBufferDeformer(target)
            if not blendBufferDeformersTarget:
                # set the name the liveBls node
                self.model.setData(self.model.index(row, 3), "")
                # set the status
                self.model.setData(self.model.index(row, 2), statusInActive)

            else:
                # set the name the liveBls node
                self.model.setData(
                    self.model.index(row, 3), blendBufferDeformersTarget[0].name()
                )
                # checking the node and set the status
                deformerFn = bmpd_blendshape.LiveBlendshapeFn(
                    deformerNode=blendBufferDeformersTarget[0]
                )
                weightsNode = deformerFn.blendBufferBeastNode()
                if weightsNode:
                    if weightsNode.geoModifier().name() != source.name():
                        self.model.setData(self.model.index(row, 2), statusInvalid)
                    else:
                        self.model.setData(self.model.index(row, 2), statusLive)

    def breedSyncCMD(self):
        func = bui_public.Functor()
        sm = bui_public.sessionManager()
        mod = sm.activeEntityTreeModel()
        eedTreeView = func.entityEditorTreeView()
        indexes = self.selectedIndexes()

        bindingVar = self.hostIterVariation()
        selection = QtCore.QItemSelection()

        for index in indexes:
            col = index.column()
            row = index.row()
            objSelIndex = self.getCellValue(index)
            if not bindingVar:
                return

            # condition node index which is col 3 is node
            if col == 3:
                geoTarget = self.getCellValue(self.model.index(row, 1))

                for blendBufferDeformers in geoModLiveBls(bindingVar):
                    bondNodeBls = blendBufferDeformers[1][0]
                    geoMod = blendBufferDeformers[0]

                    if geoMod.name() not in geoTarget:
                        continue
                    if bondNodeBls.name() != objSelIndex:
                        continue

                    vtn = mod.virtualTreeNodeOf(bondNodeBls)
                    gmQMIDX = mod.viewIndexFromVirtualTreeNode(vtn)
                    sourceIDX = eedTreeView.model().mapFromSource(gmQMIDX)
                    selection.select(sourceIDX, sourceIDX)
                eedTreeView.selectionModel().select(
                    selection,
                    QtCore.QItemSelectionModel.ClearAndSelect
                    | QtCore.QItemSelectionModel.Rows,
                )
                for eachIDX in selection.indexes():
                    eedTreeView.scrollTo(eachIDX)

            # condition node index which is col 1 and 2 are geo
            else:
                for eachGeoMod in bindingVar.iterGeoModifiers():
                    if eachGeoMod.name() != objSelIndex:
                        continue
                    vtn = mod.virtualTreeNodeOf(eachGeoMod)
                    gmQMIDX = mod.viewIndexFromVirtualTreeNode(vtn)
                    sourceIDX = eedTreeView.model().mapFromSource(gmQMIDX)
                    selection.select(sourceIDX, sourceIDX)
                eedTreeView.selectionModel().select(
                    selection,
                    QtCore.QItemSelectionModel.ClearAndSelect
                    | QtCore.QItemSelectionModel.Rows,
                )
                for eachIDX in selection.indexes():
                    eedTreeView.scrollTo(eachIDX)

    def removeBondNodeMessageBoxCMD(self):
        bindingVar = self.hostIterVariation()
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        msgBox.setText("Are you sure to remove the Live Bls node selected?")
        msgBox.setWindowTitle("Delete Live Bls Node")
        msgBox.setStandardButtons(
            QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel
        )

        returnValue = msgBox.exec()
        if returnValue == QtWidgets.QMessageBox.Ok:
            selectedIndex = self.selectedIndexes()
            for index in selectedIndex:
                col = index.column()
                row = index.row()
                if col != 3:
                    continue
                geoTarget = self.getCellValue(self.model.index(row, 1))
                liveBlsNode = self.getCellValue(self.model.index(row, 3))
                print(bindingVar, geoTarget, liveBlsNode)
                removeBondNode(bindingVar, geoTarget, liveBlsNode)

        # refresh table
        data = getDataFromBreed(bindingVar)
        self.setTableData(data, HEADERS)

    def clearCellCMD(self):
        indexes = self.selectedIndexes()
        value = ""
        for index in indexes:
            column = index.column()

            if self.getCellValue(index) == value:
                continue

            self.model.setData(index, value)
            if column == 0:
                self.model.setData(self.model.index(index.row(), 2), value)
            else:
                self.model.setData(self.model.index(index.row(), 2), value)
                self.model.setData(self.model.index(index.row(), 3), value)

    def removeRowsCMD(self):
        indexList = set()
        for index in self.selectedIndexes():
            indexList.add(index)

        for proxyIndex in sorted(indexList, reverse=True):
            index = self.proxyModel.mapToSource(proxyIndex)
            if index.row() >= 0:
                self.model.removeRows(index.row(), 1)

    def insertRowCMD(self, row):
        index = self.currentIndex()
        self.model.insertRows(self.model.rowCount(), row, index)

    def hostIterVariation(self):
        entityTree = bui_public.sessionManager().activeBeastCoreBindingTree()
        host = [
            n
            for n in entityTree.iterVariations()
            if n.name() == self.hostLineEdit.text()
        ]
        if not host:
            return

        # usually host is 'cache_deform_high'
        bindingVar = host[0]
        return bindingVar

    def targetSourceLib(self):
        # select item in breed
        selItem = loadSelection()
        if not selItem:
            return

        # get the index selection
        indexes = self.selectedIndexes()

        targetSourceList = list()
        for item, index in itertools.zip_longest(selItem, indexes):
            if not item or not index:
                continue
            else:
                itemName = item.name()
                column = index.column()

                self.model.setData(index, itemName)
                targetSourceList.append([itemName, column])

        return targetSourceList

    def getBreedGeoMod(self, geoName):
        # get the geo mod breed
        bindingVar = self.hostIterVariation()
        geoModifiers = list()
        for geoMod in bindingVar.iterGeoModifiers():
            if geoName == geoMod.name():
                geoModifiers.append(geoMod)

        return geoModifiers

    def localNonLocalRename(self, sourceTarget):
        # rename "Local_*side" to be "_*side"
        split = sourceTarget.split("_")
        LocalStr = NAMING[0]
        _Str = NAMING[1]
        side = split[1]
        # get the name Local_ and rename to be Local_*side and _ to be "_*side"
        newLocalName = "{}{}".format(LocalStr, side)
        newName = "{}{}".format(_Str, side)

        return newLocalName, newName

    def targetSourceMatchCell(self):
        # selection row
        indexes = self.selectedIndexes()

        # get the data from selection and columns
        # list of [target, source] selection
        targetSourceLibs = self.targetSourceLib()

        # iter host
        bindingVar = self.hostIterVariation()

        newTargetSourceLibs = list()

        # get the number of len column selected
        columnLen = [index.column() for index in indexes]

        # list geoMod in binding var
        listGeoMod = [geoMod.name() for geoMod in bindingVar.iterGeoModifiers()]

        # looping every object
        for targetSource, index in zip(targetSourceLibs, indexes):

            objectSel = targetSource[0]
            column = index.column()
            columnOpposite = column ^ 1
            row = index.row()

            source = str(self.model.data(self.model.index(row, 0)))
            target = str(self.model.data(self.model.index(row, 1)))

            # condition selected more than one column
            if len(set(columnLen)) > 1:
                # go ahead and query the data target and source
                newTargetSourceLibs.append([target, source])
                continue

            # check the column opposite condition
            columnFilled = str(self.model.data(self.model.index(row, columnOpposite)))
            if columnFilled:
                newTargetSourceLibs.append([target, source])
                continue
            # get the local or non local name and rename it the non-local and local name
            localNonLocalRename = self.localNonLocalRename(objectSel)
            newLocalName = localNonLocalRename[0]
            newName = localNonLocalRename[1]

            # check if there is 'Local_*side' prefix of the objectSel the rename it for opposite sel
            if newLocalName in objectSel:
                nameSwap = objectSel.replace(newLocalName, newName)

            else:
                nameSwap = objectSel.replace(newName, newLocalName)

            # condition if there is no match new swap name in breed
            if nameSwap in listGeoMod:
                self.model.setData(self.model.index(row, columnOpposite), nameSwap)

            source = str(self.model.data(self.model.index(row, 0)))
            target = str(self.model.data(self.model.index(row, 1)))
            newTargetSourceLibs.append([target, source])

        # get the geomod from object list
        geoModifiers = list()
        for geoMod in newTargetSourceLibs:
            target = self.getBreedGeoMod(geoMod[0])
            source = self.getBreedGeoMod(geoMod[1])
            geoModifiers.append([target, source])

        return geoModifiers


class Model(QtCore.QAbstractTableModel):
    def __init__(self, data, headerList):
        super(Model, self).__init__()
        self._data = data
        self._headerList = headerList
        self.checks = {}

    def data(self, index, role=QtCore.Qt.DisplayRole):

        value = self._data[index.row()][index.column()]
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return self._data[index.row()][index.column()]

        if role == QtCore.Qt.TextColorRole and index.column() == 2:
            if value == "Live":
                return QtGui.QBrush(COLORS["Live"])
            if value == "Invalid":
                return QtGui.QBrush(COLORS["Invalid"])
            if value == "InActive":
                return QtGui.QBrush(COLORS["InActive"])
            if value == "Connection Break":
                return QtGui.QBrush(COLORS["Connection Break"])

        if role == QtCore.Qt.TextAlignmentRole and index.column() == 2:
            return QtCore.Qt.AlignCenter

        if role == QtCore.Qt.CheckStateRole and index.column() == 3:
            return self.checkState(QtCore.QPersistentModelIndex(index))

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            self._data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index)
            return True

        if not index.isValid():
            return False

        if role == QtCore.Qt.CheckStateRole:
            self.checks[QtCore.QPersistentModelIndex(index)] = value
            return True

        return False

    def flags(self, index):
        fl = QtCore.QAbstractTableModel.flags(self, index)
        if index.column() == 3:
            fl |= QtCore.Qt.ItemIsUserCheckable

        return fl

    def checkState(self, index):
        if index in self.checks.keys():
            return self.checks[index]
        else:
            return QtCore.Qt.Unchecked

    def rowCount(self, *args):
        return len(self._data)

    def columnCount(self, *args):
        value = 0
        if self.rowCount() > 0:
            value = len(self._data[0])

        return value

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return str(self._headerList[section])

    def insertRows(self, position, rows, index):
        self.layoutAboutToBeChanged.emit()
        self.beginInsertRows(index, position, position + rows - 1)
        defaultRow = [""] * len(self._headerList)
        for row in range(rows):
            self._data.insert(position + row, defaultRow)
        self.endInsertRows()
        self.layoutChanged.emit()
        return True

    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        start = position
        end = position + rows - 1
        if 0 <= start <= end and end < self.rowCount(parent):
            self.beginRemoveRows(parent, start, end)
            for index in range(start, end + 1):
                del self._data[index]
            self.endRemoveRows()
            return True
        return False


def removeBondNode(bindingVar, geoMod, bondNode):
    # against the geo mod to the host
    deformerNode = [
        eachGeoMod
        for eachGeoMod in bindingVar.iterGeoModifiers()
        if eachGeoMod.name() == geoMod
    ]
    deformerNode = deformerNode[0]

    # functor
    bindingsTree = bct_bindings.bindingsTreeFromNode(deformerNode)
    bindingsTreeFn = bmt_bindings.Functor(bindingsTree)

    bondNodeToRemove = [
        node
        for node in bindingsTree.iterBondNodes(deformerNode)
        if node.name() == bondNode
    ]
    bondNodeToRemove = bondNodeToRemove[0]

    # remove in maya and breed tree
    bindingsTreeFn.removeBondNode(omx.currentModifier(), bondNodeToRemove)
    bindingsTree.removeBondNode(bondNodeToRemove)


def blendBufferDeformer(geoModTarget):
    blendBufferDeformers = [
        bondNode
        for bondNode in geoModTarget.iterChildren()
        if bondNode.bondNodeType() == "BlendBufferDeformer"
    ]

    return blendBufferDeformers


def geoModLiveBls(activeBindingTree):
    geoModLiveBls = list()
    for geoModTarget in activeBindingTree.iterGeoModifiers():
        blendBufferDeformers = blendBufferDeformer(geoModTarget)
        if not blendBufferDeformers:
            continue
        geoModLiveBls.append((geoModTarget, blendBufferDeformers))
    return geoModLiveBls


def getDataFromBreed(activeBindingTree):
    blendshapeBufferDataList = list()
    for geoModTarget, blendBufferDeformers in geoModLiveBls(activeBindingTree):
        for eachDeformer in blendBufferDeformers:
            deformerFn = bmpd_blendshape.LiveBlendshapeFn(deformerNode=eachDeformer)
            weightsNode = deformerFn.blendBufferBeastNode()
            if weightsNode:
                blendshapeBufferDataList.append(
                    [geoModTarget, weightsNode.geoModifier(), eachDeformer.name()]
                )
            else:
                blendshapeBufferDataList.append([geoModTarget, "", eachDeformer.name()])

    # preparing table data
    tableData = []
    for target, source, liveBsNode in blendshapeBufferDataList:
        statusLive = "Live"
        statusConnectionBreak = "Connection Break"
        if not source:
            tableData.append(["", target.name(), statusConnectionBreak, liveBsNode])
        else:
            tableData.append([source.name(), target.name(), statusLive, liveBsNode])

    return tableData


def loadSelection():
    sel = bui_public.Functor().entityEditor_selection()
    # return if selection is invalid
    if not sel or sel[0].nodeType() != 503:
        return logger.error("Invalid selection, aborting.")
    return sel


def createLiveBS(liveGeoMod, destGeoMod):
    bsDeformer = rjml_bond.getBlendshapeDeformerFromSelected(destGeoMod)
    selfNode = [d for d in destGeoMod.iterChildren()]
    selfNode = selfNode[0]

    if bsDeformer:
        insertAfter = bsDeformer
    else:
        insertAfter = selfNode

    # get the name for deformer
    deformerName = liveGeoMod.name().split("geo")[0]

    bmpd_blendshape.LiveBlendshapeFn.create(
        deformerName="{}{}".format(deformerName, "liveBLS"),
        destGeoMod=destGeoMod,
        liveGeoMod=liveGeoMod,
        insertAfter=insertAfter,
    )
