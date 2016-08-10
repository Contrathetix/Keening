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
        super(ModManager, self).__init__(backend)
        self.backend = backend
        self.modList = []
        self.widget = ModManagerWidget.ModManagerWidget(self)
        # pathModsChanged.connect(self.refreshModInfo)

        # connect signals between the widget and this one
        self.widget.modList.itemChanged.connect(self.widgetItemChanged)
        self.widget.modList.itemDropped.connect(self.widgetItemDropped)
        self.updateWidget.connect(self.widget.modList.setMods)

        # refresh mod info, create list
        self.refreshModInfo()
        self.loadInfoToList()

    def widgetItemChanged(self, item, column):
        item.userInput(column)
        self.updateWidget.emit(self.modList)
        self.backend.modSetupChanged.emit(self.modList)

    def widgetItemDropped(self, item, index):
        self.modList.remove(item)
        self.modList.sort(key=lambda m: m.index(), reverse=False)
        self.modList.insert(index, item)
        toUpdate = []
        for i in range(0, len(self.modList)):
            self.modList[i].setIndex(i)
            toUpdate.append([self.modList[i].name(), i])
        self.backend.setModIndexes(toUpdate)
        self.updateWidget.emit(self.modList)

    def getColumnHeaders(self):
        return self.Mod.columnHeaders

    def modListFromDisk(self):
        path = self.backend.getPathMods()
        return sorted(os.scandir(path), key=lambda e: e.inode(), reverse=False)

    def refreshModInfo(self):
        onDisk = [e.name for e in self.modListFromDisk()]
        dbNames = self.backend.getModNames()
        unknown = sorted(list(set(onDisk) - set(dbNames).intersection(onDisk)))
        self.backend.removeMods(list(set(dbNames) - set(onDisk)))
        indStart = len(self.backend.getModNames())
        mods = []
        for i in range(0, len(unknown)):
            mods.append([unknown[i], indStart + i])
        self.backend.addNewMods(mods)

    def loadInfoToList(self):
        self.modList.clear()
        modMap = self.backend.getModInfo()
        diskDirEntries = self.modListFromDisk()
        for e in diskDirEntries:
            self.modList.append(Mod(
                backend=self.backend,
                dirEntry=e,
                index=modMap[e.name]["ind"],
                active=modMap[e.name]["active"],
                version=modMap[e.name]["version"]
            ))
        self.updateWidget.emit(self.modList)
        self.backend.modSetupChanged.emit(self.modList)


class Mod(QtWidgets.QTreeWidgetItem):

    def __init__(self, backend, dirEntry, index, active, version):
        super(Mod, self).__init__()
        self._backend = backend
        self._path = dirEntry.path
        self._name = dirEntry.name
        self._index = index
        self._version = version
        self._active = active
        self.updateRow()

    def __str__(self):
        return self._name

    def columnHeaders(self):
        return ["name", "version", "index"]

    def scanFiles(self, files, path):
        for f in sorted(os.scandir(path), key=lambda e: e.inode(), reverse=False):
            if not f.name.startswith("."):
                if not f.is_dir():
                    files.append(f.path)
                else:
                    [files.append(f) for f in self.scanFiles([], f.path)]
        return files

    def fileCount(self):
        return len(self.files())

    def name(self):
        return self._name

    def path(self):
        return self._path

    def files(self):
        return sorted(self.scanFiles([], self._path))

    def active(self):
        return self._active

    def relativeFiles(self):
        files = [os.path.abspath(str(p)) for p in self.files()]
        files = [os.path.relpath(p, self._path) for p in files]
        return files

    def version(self):
        return self._version

    def index(self):
        return int(self._index)

    def setName(self, newName):
        self._name = newName
        self._path = os.path.join(os.path.split(self._path)[0], self._name)

    def setIndex(self, newIndex):
        self._index = newIndex
        self.setText(self.columnHeaders().index("index"), str(self._index))

    def userInput(self, column):
        attr = self.columnHeaders()[column]
        if attr == "name":
            newName = self.text(column).strip()
            indActive = self.columnHeaders().index("name")
            newActive = (self.checkState(indActive) == Qt.Qt.Checked)
            if self._name != newName:
                self._backend.setModName(self._name, newName)
                self.setName(newName)
            if newActive != self._active:
                self._active = newActive
                if self._active:
                    self.setCheckState(column, Qt.Qt.Checked)
                else:
                    self.setCheckState(column, Qt.Qt.Unchecked)
                self._backend.setModActive(self._name, self._active)
        elif attr == "version":
            newVersion = self.text(column).strip()
            if newVersion != self._version:
                self._version = newVersion
                self.setText(column, self._version)
                self._backend.setModVersion(self._name, newVersion)
        elif attr == "index":
            newIndex = int(self.text(column).strip())
            if newIndex != self._index:
                self.treeWidget().itemDropped.emit(self, newIndex)
        else:
            self._backend.log(self, 2, "uknown edited column " + str(column))

    def updateRow(self):
        h = self.columnHeaders()
        self.setText(h.index("name"), self._name)
        self.setText(h.index("version"), self._version)
        self.setText(h.index("index"), str(self._index))
        if self._active:
            self.setCheckState(0, Qt.Qt.Checked)
            self.setbackgroundColour((204, 255, 204))
        else:
            self.setCheckState(0, Qt.Qt.Unchecked)
            self.setbackgroundColour((255, 204, 204))
        self.setFlags(
            self.flags() |
            QtCore.Qt.ItemIsUserCheckable |
            QtCore.Qt.ItemIsEnabled |
            QtCore.Qt.ItemIsEditable
        )

    def setbackgroundColour(self, colourTuple):
        return
        for i in range(0, self.columnCount()):
            self.setBackground(i, QtGui.QColor(colourTuple[0], colourTuple[1], colourTuple[2]))
