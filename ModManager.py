# -*- coding: utf-8 -*-

import os
import shutil
import MiscUtilities


class ModManager:
    def __init__(self, main):
        self.main = main
        self.modInfo = []

    def getModInfoHeaders(self):
        return ["Name", "Version", "Files", "Size", "Index"]

    def getModInfo(self, forceRefresh):
        if len(self.modInfo) < 1 or forceRefresh:
            self.collectModInfo()
        info = []
        for oldInfo in self.modInfo:
            newInfo = {
                "installed": False,
                "name": oldInfo["name"],
                "version": oldInfo["version"],
                "size": str(oldInfo["size"]),
                "fileCount": str(oldInfo["fileCount"])
            }
            info.append(newInfo)
        return info

    def collectModInfo(self):
        self.main.log([self, "info", "Collecting mod info..."])
        try:
            entryList = list(os.scandir(self.main.pathManager.getPathMods()))
            entryList = sorted(entryList, key=lambda e: e.inode(), reverse=True)
            for e in entryList:
                if e.name.startswith("."):
                    continue
                meta = self.parseModMeta(e.path)
                self.modInfo.append({
                    "name": e.name,
                    "version": meta["version"],
                    "size": 0,
                    "fileCount": 0,
                    "index": 0
                })
        except Exception as exc:
            self.main.log([self, "exception", str(exc)])
        # print(self.modInfo)
        self.main.log([self, "info", "Mod info collected"])

    def findModMetaIndex(self, modName):
        ind = -1
        for i in range(0, len(self.modInfo)):
            if self.modInfo[i]["name"] == modName:
                ind = i
                break
        return ind

    def parseModMeta(self, path):
        path = self.main.pathManager.getPath(path + "/meta.ini")
        meta = {
            "version": "1.0.0.0"
        }
        if self.main.pathManager.isValid(path):
            tempMap = MiscUtilities.parseIni(path)
            for key in tempMap.keys():
                meta[key] = tempMap[key]
        else:
            MiscUtilities.writeIni(path, meta)
        return meta

    def writeModMeta(self, modName):
        self.main.log([self, "info", "Write meta for ", modName])
        try:
            path = self.main.pathManager.makePath([self.main.pathManager.getPathMods(), modName, "meta.ini"])
            meta = self.modInfo[self.findModMetaIndex(modName)]
            meta = {"version": meta["version"]}
            MiscUtilities.writeIni(path, meta)
        except Exception as exc:
            self.main.log([self, "exception", str(exc)])

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
