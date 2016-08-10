# -*- coding: utf-8 -*-

import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import PyQt5.Qt as Qt


class ModManagerWidget(QtWidgets.QWidget):

    def __init__(self, modManager):
        super(ModManagerWidget, self).__init__()

        # collect the widgets
        self.sidePanel = SidePanel()
        self.modList = ModList(modManager)
        self.modList.currentItemChanged.connect(self.sidePanel.updateInfo)

        # horisontal splitter
        self.splitter = QtWidgets.QSplitter(self)
        self.splitter.setContentsMargins(0, 0, 0, 0)
        self.splitter.addWidget(self.modList)
        self.splitter.addWidget(self.sidePanel)
        self.splitter.setStretchFactor(0, 2)
        self.splitter.setStretchFactor(1, 1)

        # mandatory layout for the whole thing
        self.vbox = QtWidgets.QVBoxLayout(self)
        self.vbox.addWidget(self.splitter)

        # set the layout
        self.setLayout(self.vbox)


class ModList(QtWidgets.QTreeWidget):

    itemDropped = QtCore.pyqtSignal(QtWidgets.QTreeWidgetItem, int)

    def __init__(self, modManager):
        super(ModList, self).__init__()

        # drag and drop
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)

        # visual changes
        self.setRootIsDecorated(False)
        self.setUniformRowHeights(True)
        self.setAlternatingRowColors(True)
        self.setVerticalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOff)

        # headers and sorting
        header = self.header()
        self.setSortingEnabled(True)
        header.setSortIndicatorShown(True)
        header.setSortIndicator(self.columnCount() - 1, Qt.Qt.AscendingOrder)
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, header.Stretch)

    def dropEvent(self, event):
        item = self.currentItem()
        index = self.indexOfTopLevelItem(self.itemAt(self.mapFrom(self, event.pos())))
        if index > -1:
            self.itemDropped.emit(item, index)
            event.acceptProposedAction()
        else:
            event.ignore()

    def onSelectionChanged(self, oldItem, newItem):
        print(oldItem, newItem)

    def setMods(self, modList):
        [self.takeTopLevelItem(i) for i in range(0, self.topLevelItemCount())]
        if len(modList) > 0:
            self.setHeaderLabels(modList[0].columnHeaders())
            [self.addTopLevelItem(item) for item in modList]
        header = self.header()
        self.sortItems(header.sortIndicatorSection(), header.sortIndicatorOrder())


class SidePanel(QtWidgets.QWidget):

    def __init__(self):
        super(SidePanel, self).__init__()

        # widget init
        self.nameWidget = QtWidgets.QLabel("-", self)
        self.sizeWidget = QtWidgets.QLabel("-", self)
        self.numfWidget = QtWidgets.QLabel("-", self)
        self.fileWidget = QtWidgets.QListWidget(self)
        self.fileWidget.setAlternatingRowColors(True)
        self.loseWidget = QtWidgets.QListWidget(self)
        self.loseWidget.setAlternatingRowColors(True)
        self.winsWidget = QtWidgets.QListWidget(self)
        self.winsWidget.setAlternatingRowColors(True)
        self.subpWidget = SubpackageWidget()

        # top layout
        self.grid = QtWidgets.QGridLayout(self)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setColumnStretch(0, 1)
        self.grid.setColumnStretch(1, 5)
        self.grid.addWidget(QtWidgets.QLabel("name", self), 0, 0, 1, 1)
        self.grid.addWidget(self.nameWidget, 0, 1, 1, 1)
        self.grid.addWidget(QtWidgets.QLabel("size", self), 1, 0, 1, 1)
        self.grid.addWidget(self.sizeWidget, 1, 1, 1, 1)
        self.grid.addWidget(QtWidgets.QLabel("files", self), 2, 0, 1, 1)
        self.grid.addWidget(self.numfWidget, 2, 1, 1, 1)
        self.widget = QtWidgets.QWidget(self)
        self.widget.setLayout(self.grid)

        # tabs
        self.tabs = QtWidgets.QTabWidget(self)
        self.tabs.addTab(self.subpWidget, "Subpackages")
        self.tabs.addTab(self.fileWidget, "Files")
        self.tabs.addTab(self.winsWidget, "Overrides")
        self.tabs.addTab(self.loseWidget, "Overridden")

        # final vertical layout
        self.vbox = QtWidgets.QVBoxLayout(self)
        self.vbox.setContentsMargins(5, 0, 0, 0)
        self.vbox.addWidget(self.widget)
        self.vbox.addWidget(self.tabs)

        # final layout
        self.setLayout(self.vbox)

    def updateInfo(self, mod, old):
        self.nameWidget.setText(mod.name())
        # self.sizeWidget.setText(str(mod.size()))
        self.numfWidget.setText(str(mod.fileCount()))
        self.fileWidget.clear()
        self.fileWidget.addItems(mod.relativeFiles())


class SubpackageWidget(QtWidgets.QListWidget):

    def __init__(self):
        super(SubpackageWidget, self).__init__()
