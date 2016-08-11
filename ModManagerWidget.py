# -*- coding: utf-8 -*-

import PyQt5.QtWidgets as QtWidgets
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

    def __init__(self, modManager):
        super(ModList, self).__init__()

        # drag and drop
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)

        # signal connections
        self.itemChanged.connect(self.itemChangeHandler)

        # visual changes
        self.setRootIsDecorated(False)
        self.setUniformRowHeights(True)
        self.setSortingEnabled(False)
        self.setAlternatingRowColors(True)
        self.setVerticalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOff)

        # headers and sorting
        header = self.header()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, header.Stretch)
        self.setSorting(True)

    def dropEvent(self, event):
        try:
            item = self.currentItem()
            index = self.indexOfTopLevelItem(self.itemAt(self.mapFrom(self, event.pos())))
            print(str(item), index)
            if index > -1:
                item.setIndex(index)
                for i in range(index, self.topLevelItemCount()):
                    self.topLevelItem(i).setIndex(i + 1, dbUpdate=False)
                self.sort()
                event.acceptProposedAction()
            else:
                raise Exception()
        except Exception:
            event.ignore()

    def itemChangeHandler(self, item, column):
        item.newColumnValue(column, item.text(column))

    def setSorting(self, enabled):
        header = self.header()
        self.setSortingEnabled(enabled)
        header.setSortIndicatorShown(enabled)
        if enabled:
            self.sortByColumn(self.columnCount() - 1, Qt.Qt.AscendingOrder)
            self.sortItems(header.sortIndicatorSection(), header.sortIndicatorOrder())

    def onSelectionChanged(self, oldItem, newItem):
        print(oldItem, newItem)

    def newHeaderLabels(self, labels):
        self.setHeaderLabels(labels)
        self.header().setSortIndicator(
            self.columnCount() - 1,
            self.header().sortIndicatorOrder()
        )

    def newItems(self, modList):
        try:
            self.setSorting(False)
            [self.takeTopLevelItem(i) for i in range(0, self.topLevelItemCount())]
            [self.addTopLevelItem(item) for item in modList]
            self.setSorting(True)
        except Exception:
            pass


class SidePanel(QtWidgets.QWidget):

    def __init__(self):
        super(SidePanel, self).__init__()

        # widget init
        self.nameWidget = QtWidgets.QLabel("-", self)
        self.sizeWidget = QtWidgets.QLabel("-", self)
        self.numfWidget = QtWidgets.QLabel("-", self)

        # subpackage tab
        self.subpWidget = SubpackageWidget()
        self.subpWidget.setAlternatingRowColors(True)

        # installed files listing widget
        self.fileWidget = QtWidgets.QListWidget(self)
        self.fileWidget.setAlternatingRowColors(True)

        # conflict lose lister widget
        self.loseWidget = QtWidgets.QListWidget(self)
        self.loseWidget.setAlternatingRowColors(True)

        # conflict win list widget
        self.winsWidget = QtWidgets.QListWidget(self)
        self.winsWidget.setAlternatingRowColors(True)

        # top widget
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
        self.nameWidget.setText(mod.getName())
        # self.sizeWidget.setText(str(mod.size()))
        self.numfWidget.setText(str(mod.getFileCount()))
        self.fileWidget.clear()
        self.fileWidget.addItems(mod.getRelativeFiles())


class SubpackageWidget(QtWidgets.QListWidget):

    def __init__(self):
        super(SubpackageWidget, self).__init__()
