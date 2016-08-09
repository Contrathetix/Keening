# -*- coding: utf-8 -*-

import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.Qt as Qt


class ModList(QtWidgets.QTreeWidget):

    itemDropped = QtCore.pyqtSignal()

    def __init__(self, modManager):
        super(ModList, self).__init__()
        self.setRootIsDecorated(False)
        self.setAlternatingRowColors(True)
        # self.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        # self.setHeaderLabels(self.main.modManager.getModInfoHeaders())
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setHorizontalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOn)
        self.itemChanged.connect(modManager.widgetItemChanged)
        modManager.updateWidget.connect(self.setMods)

    def dropEvent(self, event):
        print(event.mimeData())
        event.acceptProposedAction()
        return
        if (event.mimeData().hasFormat('application/x-icon-and-text')):
            event.acceptProposedAction()
            data = event.mimeData().data("application/x-icon-and-text")
            stream = QtCore.QDataStream(data, QtCore.QIODevice.ReadOnly)
            text = QtCore.QString()
            icon = QtGui.QIcon()
            stream >> text >> icon
            item = QtGui.QTreeWidgetItem(self)
            item.setText(0, text)
            item.setIcon(0, icon)
            self.addTopLevelItem(item)
            self.itemDropped.emit()
        else:
            event.ignore()

    def onSelectionChanged(self, oldItem, newItem):
        print(oldItem, newItem)

    def setMods(self, modList):
        self.clear()
        if len(modList) > 0:
            self.setHeaderLabels(modList[0].getColumnHeaders())
            self.addTopLevelItems(modList)
        for i in range(0, self.columnCount() - 1):
            self.resizeColumnToContents(i)
            self.header().resizeSection(i, self.header().sectionSize(i) + 80)
