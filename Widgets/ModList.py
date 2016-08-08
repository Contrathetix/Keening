# -*- coding: utf-8 -*-

import PyQt5.Qt as Qt
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets


class ModListItem(QtWidgets.QTreeWidgetItem):

    def __init__(self, mod):
        super(ModListItem, self).__init__()
        columnTexts = mod.getColumns()
        for i in range(0, len(columnTexts)):
            self.setText(i, columnTexts[i])
        if mod.isActive():
            # item.setIcon(0, QtGui.QIcon("resource/mod_a.png"))
            self.setCheckState(0, Qt.Qt.Checked)
            self.setbackgroundColour((204, 255, 204))
        else:
            # item.setIcon(0, QtGui.QIcon("resource/mod_b.png"))
            self.setCheckState(0, Qt.Qt.Unchecked)
            self.setbackgroundColour((255, 204, 204))
        self.setFlags(self.flags() | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)

    def setbackgroundColour(self, colourTuple):
        for i in range(0, self.columnCount()):
            self.setBackground(i, QtGui.QColor(colourTuple[0], colourTuple[1], colourTuple[2]))


class ModList(QtWidgets.QTreeWidget):

    def __init__(self, parent):
        super(ModList, self).__init__()
        self.main = parent
        self.setRootIsDecorated(False)
        self.setAlternatingRowColors(True)
        # self.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.setHeaderLabels(self.main.modManager.getModInfoHeaders())
        self.setDragEnabled(True)
        self.setHorizontalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOn)
        self.currentItemChanged.connect(self.onSelectionChanged)
        self.main.modManager.newModList.connect(self.setMods)
        self.main.modManager.refreshModInfo()

    def getColumnIndex(self, label):
        ind = -1
        header = self.headerItem()
        for i in range(0, header.columnCount()):
            if header.text(i) == label:
                ind = i
                break
        return ind

    def getModName(self):
        try:
            name = self.currentItem().text(self.getColumnIndex("Name"))
            return name
        except Exception as exc:
            self.parent.log([self, "exception", str(exc)])
            return ""

    def getModVersion(self):
        try:
            return self.currentItem().text(self.getColumnIndex("Version"))
        except Exception as exc:
            self.main.log([self, "exception", str(exc)])
            return ""

    def setModName(self, newName):
        oldName = self.getModName()
        self.main.modManager.setModName(oldName, newName)
        self.currentItem().setText(self.getColumnIndex("name"), newName)

    def setModVersion(self, newVersion):
        modName = self.getModName()
        self.main.modManager.setModVersion(modName, newVersion)
        self.currentItem().setText(self.getColumnIndex("version"), newVersion)

    def onSelectionChanged(self, oldItem, newItem):
        print(oldItem, newItem)

    def setMods(self, modList):
        self.clear()
        l = [ModListItem(m) for m in modList]
        self.addTopLevelItems(l)

    def updateContents(self):
        self.clear()
        self.parent.log([self, "info", "Updating installer list"])
        itemList = []
        for modInfo in self.parent.modManager.getModInfo(False):
            itemList.append(ModListItem(modInfo["installed"], "a", "b", 1))
        self.addTopLevelItems(itemList)
        for i in range(0, len(self.columnCount()) - 1):
            self.resizeColumnToContents(i)
            self.header().resizeSection(i, self.header().sectionSize(i) + 50)
        # self.header().setResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        # self.header().setStretchLastSection(True)
