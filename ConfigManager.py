# -*- coding: utf-8 -*-

import PyQt5.Qt as Qt
import PyQt5.QtCore as QtCore
import os
import shutil


class ConfigManager(QtCore.QObject):

    pathModsChanged = QtCore.pyqtSignal()

    def __init__(self, backend, filePath):
        super(ConfigManager, self).__init__(backend)
        self.backend = backend
        self.valueMap = {
            "sPathGame": "game",
            "sPathMods": "mods",
            "sPathData": "data",
            "iGuiWidth": 1000,
            "iGuiHeight": 600
        }
        # self.initValues()
        # self.initDirs()
        # self.initData()

    def initValues(self):
        self.backend.log(self, 0, "Reading config data from ini...")
        tempMap = self.parseIni("Keening.ini", True)
        for key in tempMap.keys():
            self.valueMap[key] = tempMap[key]
        self.backend.log(self, 0, "Config data reading finished")

    def initDirs(self):
        try:
            self.backend.pathManager.makePath(self.getPathMods(), create=True)
            self.backend.pathManager.makePath(self.getPathGame(), create=True)
        except Exception as exc:
            self.backend.log(self, 1, str(exc))

    def getGuiSize(self):
        return Qt.QSize(self.valueMap["iGuiWidth"], self.valueMap["iGuiHeight"])

    def getPathMods(self):
        return self.valueMap["sPathMods"]

    def setPathMods(self, path):
        if path != self.valueMap["sPathMods"]:
            self.valueMap["sPathMods"] = self.main.pathManager.makePath(path, create=True)
            self.pathModsChanged.emit()

    def getPathGame(self):
        return self.valueMap["sPathGame"]

    def setPathGame(self, path):
        self.valueMap["sPathGame"] = self.main.pathManager.makePath(path, create=True)

    def getPathData(self, path):
        return self.main.pathManager.makePath([self.getPathGame(), "Data Files"], create=True)

    def getValue(self, valueName):
        try:
            return self.valueMap[valueName]
        except Exception as exc:
            self.main.log(self, 1, str(exc))
            if valueName[0] is "s":
                return ""
            else:
                return 0

    def setValue(self, key, value):
        self.valueMap[key] = value

    def dumpPreferences(self, fileName):
        self.writeIni(fileName, self.valueMap)

    def parseIni(self, path, convertTypes=False, encoding="utf-8"):
        output = {}
        try:
            file = open(path, "r", encoding=encoding)
            lines = file.read().split("\n")
            file.close()
            for line in lines:
                try:
                    s = [t.strip() for t in line.split("=")]
                    if len(s[0]) < 1 or len(s[1]) < 1:
                        continue
                    key = s[0]
                    if convertTypes and key[0] is "f":
                        value = float(s[1])
                    elif convertTypes and key[0] is "i":
                        value = int(s[1])
                    elif convertTypes and key[0] is "s":
                        value = os.path.abspath(s[1])
                    else:
                        value = s[1]
                    output[key] = value
                except Exception as exc:
                    self.main.log(self, 1, str(exc))
        except Exception as exc:
            self.main.log(self, 1, str(exc))
        return output

    def writeIni(self, path, valueMap, encoding="utf-8"):
        try:
            file = open(path, "w", encoding=encoding)
            for key in sorted(valueMap.keys()):
                file.write(str(key).strip() + "=" + str(valueMap[key]).strip() + "\n")
            file.close()
        except Exception:
            pass

    def initData(self):
        self.main.log(self, 0, "Checking user data...")
        pathData = self.getPathData()
        pathIniCustom = self.main.pathManager.makePath([pathData, "Morrowind.ini"])
        if not self.main.pathManager.pathExists(pathIniCustom):
            pathIniDefault = self.main.pathManager.makePath([self.getPathGame(), "Morrowind.ini"])
            try:
                shutil.copy2(pathIniDefault, pathIniCustom)
            except Exception as exc:
                self.main.log(self, 1, str(exc))
        self.main.log(self, 0, "User data checked")
