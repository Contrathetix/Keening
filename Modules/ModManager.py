# -*- coding: utf-8 -*-

import PyQt5.QtCore as QtCore
import os
import shutil


class Mod(QtCore.QObject):

    def __init__(self, args):
        super(Mod, self).__init__()
        try:
            self.args = args
            self.index = args[0]
            self.name = args[1]
            self.version = args[2]
            self.fileCount = 0
            self.size = 0
            self.active = True
        except Exception:
            pass

    def __str__(self):
        return self.name

    def getColumns(self):
        return [self.name, self.version, str(self.index)]

    def getColumnHeaders(self):
        return ["name", "version", "index"]

    def isActive(self):
        return self.active


class ModManager(QtCore.QObject):

    newModList = QtCore.pyqtSignal(list)

    def __init__(self, main):
        super(ModManager, self).__init__()
        self.main = main
        self.main.configManager.pathModsChanged.connect(self.refreshModInfo)

    def getModInfoHeaders(self):
        return Mod([]).getColumnHeaders()

    def refreshModInfo(self):
        modDirs = self.getModDirs()
        modList = []
        for i in range(0, len(modDirs)):
            modList.append(Mod([i, modDirs[i], "1.0"]))
        self.newModList.emit(modList)

    def getModDirs(self):
        self.main.log(self, 0, "collecting list of mod directories...")
        modNames = []
        try:
            entryList = list(os.scandir(self.main.configManager.getPathMods()))
            entryList = sorted(entryList, key=lambda e: e.inode(), reverse=True)
            [modNames.append(e.name) for e in entryList if not e.name.startswith(".")]
        except Exception as exc:
            self.main.log(self, 1, str(exc))
        self.main.log(self, 0, "mod directory list collected")
        return modNames

    def getModSubPackages(self, name):
        subPackageMap = {}
        path = self.main.pathManager.getPath(self.main.pathManager.getPathMods() + "/" + name, True, False)
        self.main.log([self, "info", "Subpackages for ", str(path)])
        for f in os.scandir(path):
            if not f.is_dir():
                continue
            try:
                if f.name.split(" ")[0].isdigit():
                    if ".ignore" in f.name:
                        subPackageMap[f.name.split(".ignore")[0]] = False
                    else:
                        subPackageMap[f.name] = True
            except Exception:
                pass
        return subPackageMap

    def setModName(self, oldName, newName):
        self.main.log([self, "info", "Rename mod", "'" + oldName + "'", "-->", newName])
        try:
            pathMods = self.main.pathManager.getPathMods()
            pathOld = self.main.pathManager.makePath([pathMods, oldName])
            pathNew = self.main.pathManager.makePath([pathMods, newName])
            if self.main.pathManager.isValid(str(pathNew)):
                raise Exception("path already exists")
            else:
                i = self.findModMetaIndex(oldName)
                if i < 0:
                    raise Exception("mod info list index not valid: " + str(i))
                modInfo = self.modInfo[i]
                modInfo["name"] = newName
                self.modInfo[:] = [e for e in self.modInfo if e["name"] is not oldName]
                self.modInfo.append(modInfo)
                shutil.move(pathOld, pathNew)
                self.writeModMeta(newName)
        except Exception as exc:
            self.main.log([self, "exception", str(exc)])

    def setModVersion(self, modName, newVersion):
        self.main.log([self, "info", "Set version", modName, "-->", newVersion])
        try:
            self.modInfo[self.findModMetaIndex(modName)]["version"] = newVersion
            self.writeModMeta(modName)
        except Exception as exc:
            self.main.log([self, "exception", str(exc)])
