# -*- coding: utf-8 -*-

import PyQt5.QtCore as QtCore
import shutil
import sys
import LogManager
import ModManager
import PathManager
import DataFilesManager
import ConfigManager
import DatabaseManager


class Backend(QtCore.QObject):

    # gui-related signals
    interfaceLock = QtCore.pyqtSignal(bool)
    progressChange = QtCore.pyqtSignal(int, int)

    # signals related to data files
    modSetupChanged = QtCore.pyqtSignal(list)

    def __init__(self, app):
        super(Backend, self).__init__(app)
        self.app = app
        self.ptm = PathManager.PathManager(
            self
        )
        self.lgm = LogManager.LogManager(
            self,
            self.app,
            self.ptm.getPath("Keening.log")
        )
        self.cfm = ConfigManager.ConfigManager(
            self,
            self.ptm.getPath("Keening.ini")
        )
        self.dbm = DatabaseManager.DatabaseManager(
            self,
            self.ptm.getPath("Keening.db"),
            self.ptm.getResource("database.sql")
        )
        self.mdm = ModManager.ModManager(
            self,
            self.cfm.pathModsChanged
        )
        self.dfm = DataFilesManager.DataFilesManager(
            self
        )

    def exit(self):
        sys.exit(0)

    def setInterfaceLocked(self, isLocked):
        self.interfaceLock.emit(isLocked)

    def setProgress(self, current, maximum):
        self.progressChange.emit(current, maximum)

    def progressWidget(self):
        return self.pgb

    def widgetLog(self):
        return self.lgm.widget

    def widgetMods(self):
        return self.mdm.widget

    def widgetData(self):
        return self.dfm.widget

    def log(self, src, i, msg):
        self.lgm.log(src, i, msg)

    def getResource(self, fileName, make=False, toString=True):
        return self.ptm.getResource(fileName, toString)

    def getData(self, fileName, make=False, toString=True):
        return self.ptm.getData(fileName, toString)

    def getPath(self, args, make=False, toString=True):
        return self.ptm.getPath(args, make, toString)

    def getPathMods(self):
        return self.ptm.getPath(self.cfm.getPathMods(), make=True)

    def getPathGame(self):
        return self.ptm.getPath(self.cfm.getPathGame(), make=True)

    def getGuiSize(self):
        return self.cfm.getGuiSize()

    def addInstallers(self, nameList):
        self.dbm.addInstallers(nameList)

    def getInstallers(self):
        return self.dbm.getInstallers()

    def setModName(self, oldName, newName):
        # print("rename", oldName, "-->", newName)
        if oldName == newName:
            return
        try:
            mods = self.cfm.getPathMods()
            src = self.ptm.getPath([mods, oldName], toString=False)
            dst = self.ptm.getPath([mods, newName], toString=False)
            if dst.exists():
                Exception("name already in use: \"" + str(newName) + "\"")
            shutil.move(str(src), str(dst))
            self.dbm.setModName(oldName, newName)
        except Exception as exc:
            self.lgm.log(self, 1, str(exc))

    def getModActive(self, modName):
        return self.dbm.getModActive(modName)

    def setModActive(self, modName, isActive):
        self.dbm.setModActive(modName, isActive)

    def getModVersion(self, modName):
        return self.dbm.getModVersion(modName)

    def setModVersion(self, modName, newVersion):
        self.dbm.setModVersion(modName, newVersion)

    def getModIndex(self, modName):
        return self.dbm.getModIndex(modName)

    def setModIndex(self, modName, newIndex):
        self.dbm.setModIndex(modName, newIndex)
