# -*- coding: utf-8 -*-

import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.Qt as Qt
import ModManagerWidget
import os


class ModManager(QtCore.QObject):

    updateWidget = QtCore.pyqtSignal(list)

    def __init__(self, backend, pathModsChanged):
        super(ModManager, self).__init__()
        self.backend = backend
        self.modList = []
        pathModsChanged.connect(self.refreshModInfo)
        self.widget = ModManagerWidget.ModList(self)
        self.refreshModInfo()
        self.loadInfoToList()

    def widgetItemChanged(self, item, column):
        print(column, item)

    def modListFromDisk(self):
        path = self.backend.getPathMods()
        return sorted(os.scandir(path), key=lambda e: e.inode(), reverse=True)

    def refreshModInfo(self):
        onDisk = [e.name for e in self.modListFromDisk()]
        dbNames = self.backend.getModNames()
        unknown = sorted(list(set(onDisk) - set(dbNames).intersection(onDisk)))
        self.backend.removeMods(list(set(dbNames) - set(onDisk)))
        for i in range(len(dbNames), len(dbNames) + len(unknown)):
            self.backend.addNewMod(unknown[i], i)

    def loadInfoToList(self):
        self.modList.clear()
        modMap = self.backend.getModInfo()
        diskDirEntries = self.modListFromDisk()
        for e in diskDirEntries:
            self.modList.append(ModManager.Mod(
                _dirEntry=e,
                _index=modMap[e.name]["ind"],
                _active=modMap[e.name]["active"],
                _version=modMap[e.name]["version"]
            ))
        self.updateWidget.emit(self.modList)

    class Mod(QtWidgets.QTreeWidgetItem):

        def __init__(self, _dirEntry, _index, _active, _version):
            super(ModManager.Mod, self).__init__()
            self.__path = _dirEntry.path
            self.__name = _dirEntry.name
            self.__files = list(_dirEntry.glob("**/*.*"))
            self.__count = len(self.__files)
            self.__size = 0
            self.__index = _index
            self.__version = _version
            self.__active = _active
            self.updateRow()

        def size(self):
            return self.__size

        def fileCount(self):
            return self.__fileCount

        def files(self):
            return self.__files

        def version(self):
            return self.__version

        def index(self):
            return self.__index

        def updateRow(self):
            self.setText(0, str(self.__name))
            self.setText(1, str(self.__version))
            self.setText(2, str(self.__index))
            if self.__active:
                self.setCheckState(0, Qt.Qt.Checked)
                self.setbackgroundColour((204, 255, 204))
            else:
                self.setCheckState(0, Qt.Qt.Unchecked)
                self.setbackgroundColour((255, 204, 204))
            self.setFlags(
                self.flags() | QtCore.Qt.ItemIsUserCheckable |
                QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable
            )

        def getColumnHeaders(self):
            return ["name", "version", "index"]

        def setbackgroundColour(self, colourTuple):
            for i in range(0, self.columnCount()):
                self.setBackground(i, QtGui.QColor(colourTuple[0], colourTuple[1], colourTuple[2]))
