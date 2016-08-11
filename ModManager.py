# -*- coding: utf-8 -*-

import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.Qt as Qt
import ModManagerWidget
import os
import time


class ModManager(QtCore.QObject):

    def __init__(self, backend, pathModsChanged):
        super(ModManager, self).__init__(backend)
        self.backend = backend
        self.updateInstallersFromDisk()

        # create widget, set items
        self.widget = ModManagerWidget.ModManagerWidget(self)

        # collect info to the list
        self.generateLists()

    def updateInstallersFromDisk(self):
        path = self.backend.getPathMods()
        mods = sorted(os.scandir(path), key=lambda e: e.inode(), reverse=False)
        mods[:] = [m.name for m in mods]
        self.backend.addInstallers(mods)

    def generateLists(self):
        valueDict = self.backend.getInstallers()
        headers = valueDict["columns"]
        headers.remove("active")
        valueList = valueDict["data"]
        self.widget.modList.newHeaderLabels(headers)
        for values in valueList:
            self.widget.modList.addTopLevelItem(Mod(
                backend=self.backend,
                headers=headers,
                values=values
            ))

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

    def __init__(self, backend, values, headers):
        super(Mod, self).__init__()
        self.backend = backend
        self.headers = headers
        self.name = values["name"]
        self.version = values["version"]
        self.active = values["active"]
        self.index = values["index"]
        self.updateColumnText()
        self.setFlags(self.flags() | Qt.Qt.ItemIsEditable)

    def __str__(self):
        return self.name

    def getHeaderLabel(self, column):
        try:
            return self.headers[column]
        except Exception:
            return ""

    def getValues(self):
        try:
            return {
                "active": self.active,
                "name": self.name,
                "version": self.version,
                "index": self.index
            }
        except Exception:
            return {}

    def updateColumnText(self):
        values = self.getValues()
        for key in self.headers:
            self.setColumnValue(key, str(values[key]))
        self.updateChecked()

    def getColumnText(self, label):
        i = self.getHeaderLabelIndex(label)
        if i > -1:
            return self.text(i)
        else:
            return ""

    def setColumnValue(self, column, value):
        try:
            if type(column) is str:
                column = self.headers.index(column)
            self.setText(column, str(value))
        except Exception as exc:
            self.backend.log(self, 1, str(exc))

    def newColumnValue(self, column, value):
        # print(self.name, column, value)
        try:
            if type(column) is int:
                column = self.headers[column]
            if column == "name":
                self.setActive(self.getChecked())
                self.setName(value)
            elif column == "version":
                self.setVersion(value)
            elif column == "index":
                self.setIndex(value)
        except Exception as exc:
            self.backend.log(self, 1, str(exc))

    def getChecked(self):
        return self.checkState(self.headers.index("name"))

    def updateChecked(self):
        self.setCheckState(self.headers.index("name"), self.active)

    def getIndex(self):
        return self.index

    def setIndex(self, index, dbUpdate=True):
        if index == self.index:
            return
        self.index = int(index)
        self.setColumnValue("index", str(index))
        if dbUpdate:
            self.backend.setModIndex(self.getName(), int(index))

    def getName(self):
        return self.name

    def setName(self, name):
        if name == self.name:
            return
        self.backend.setModName(self.getName(), name)
        self.name = name
        self.setColumnValue("name", name)

    def getVersion(self):
        return self.version

    def setVersion(self, version):
        if version == self.version:
            return
        self.version = version
        self.backend.setModVersion(self.getName(), version)
        self.setColumnValue("version", version)

    def getActive(self):
        return self.active

    def setActive(self, enabled, updateUi=False):
        if enabled == self.active:
            return
        self.enabled = enabled
        self.backend.setModActive(self.getName(), enabled)
        if updateUi:
            self.updateChecked()

    def getPath(self):
        return os.path.join(self.backend.getPathMods(), self.name)

    def getFiles(self):
        return sorted(self.scanFiles([], self.getPath()))

    def getFileCount(self):
        return len(self.getFiles())

    def getRelativeFiles(self):
        files = [os.path.abspath(str(p)) for p in self.getFiles()]
        files = [os.path.relpath(p, self.getPath()) for p in files]
        return files

    def scanFiles(self, files, path):
        for f in sorted(os.scandir(path), key=lambda e: e.inode(), reverse=False):
            if not f.name.startswith("."):
                if not f.is_dir():
                    files.append(f.path)
                else:
                    [files.append(f) for f in self.scanFiles([], f.path)]
        return files

    def getConflictingFiles(self, fileList):
        return []

    def setbackgroundColour(self, colourTuple):
        return
        for i in range(0, self.columnCount()):
            self.setBackground(i, QtGui.QColor(colourTuple[0], colourTuple[1], colourTuple[2]))
