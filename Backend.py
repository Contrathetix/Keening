# -*- coding: utf-8 -*-

import PyQt5.QtCore as QtCore
import shutil
import LogManager
import ModManager
import PathManager
import PluginManager
import ConfigManager
import DatabaseManager


class Backend(QtCore.QObject):

    progressChange = QtCore.pyqtSignal(int, int)
    interfaceLock = QtCore.pyqtSignal(bool)

    def __init__(self, app):
        super(Backend, self).__init__()
        self.app = app
        self.ptm = PathManager.PathManager()
        self.lgm = LogManager.LogManager(
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
        self.plm = PluginManager.PluginManager(
            self
        )

    def progress(self, current, maximum):
        self.progressChange.emit(current, maximum)

    def widgetLog(self):
        return self.lgm.widget

    def widgetMods(self):
        return self.mdm.widget

    def widgetPlugins(self):
        return self.plm.widget

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

    def getModNames(self):
        return self.dbm.getModNames()

    def getModInfo(self):
        return self.dbm.getModInfo()

    def removeMods(self, modNames):
        self.dbm.removeMods(modNames)

    def addNewMod(self, modName, index):
        self.dbm.addNewMod(modName, index)

    def setModName(self, oldName, newName):
        try:
            mods = self.ptm.getPathMods()
            src = self.ptm.getPath([mods, oldName], toString=False)
            dst = self.ptm.getPath([mods, newName], toString=False)
            if dst.exists():
                Exception("name already in use: \"" + str(newName) + "\"")
            shutil.move(src, dst)
            self.dbm.setModAttribute(oldName, "name", newName)
        except Exception as exc:
            self.lm.log(self, 1, str(exc))

    def setModVersion(self, modName, newVersion):
        self.dbm.setModAttribute(modName, "version", newVersion)

    def setModIndex(self, modName, newIndex):
        self.dbm.setModAttribute(modName, "index", newIndex)
