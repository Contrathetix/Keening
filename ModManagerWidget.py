# -*- coding: utf-8 -*-

import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import PyQt5.Qt as Qt


class ModList(QtWidgets.QTreeWidget):

    itemDropped = QtCore.pyqtSignal(QtWidgets.QTreeWidgetItem, int)

    def __init__(self, modManager):
        super(ModList, self).__init__()
        self.setRootIsDecorated(False)
        self.setAlternatingRowColors(True)
        self.setUniformRowHeights(True)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setSortingEnabled(True)
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.setHorizontalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOn)
        self.setHeaderLabels(modManager.Mod.columnHeaders)
        self.header().setSortIndicator(self.columnCount() - 1, Qt.Qt.AscendingOrder)
        self.header().setSortIndicatorShown(True)
        self.header().setStretchLastSection(False)
        self.header().setSectionResizeMode(0, self.header().Stretch)

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
            [self.addTopLevelItem(item) for item in modList]
        header = self.header()
        # for i in range(self.columnCount() - 1, 1):
        #    self.resizeColumnToContents(i)
        #    header.resizeSection(i, header.sectionSize(i) + 40)
        self.sortItems(header.sortIndicatorSection(), header.sortIndicatorOrder())
