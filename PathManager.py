# -*- coding: utf-8 -*-

import os
import pathlib


class PathManager:
    def __init__(self, main):
        self.main = main

    def initPaths(self):
        self.pathGame = self.getPath(self.main.configManager.getValue("sPathGame"))
        self.pathMods = self.getPath(self.main.configManager.getValue("sPathMods"))

    def getPathGame(self, to_string=False):
        if to_string:
            return str(self.pathGame)
        else:
            return self.pathGame

    def getPathData(self, to_string=False):
        path = self.getPath(str(self.pathGame) + "\Data Files")
        if to_string:
            return str(path)
        else:
            return path

    def getPathMods(self, to_string=False):
        if to_string:
            return str(self.pathMods)
        else:
            return self.pathMods

    def setPathGame(self, path):
        self.pathGame = self.getPath(path)

    def setPathMods(self, newPath):
        self.pathMods = self.getPath(newPath)
        self.main.configManager.setValue("sPathMods", str(self.pathMods))
        self.main.log([self, "info", "SetPathMods (" + str(self.pathMods) + ")"])

    def getPath(self, path, to_str=True, create_if_not_exist=True):
        path = pathlib.Path(os.path.abspath(path))
        if not path.exists() and create_if_not_exist:
            if len(path.suffix) < 1:
                path.mkdir()
            else:
                path.touch()
        path = pathlib.Path(path).resolve()
        path = pathlib.PurePath(path)
        if to_str:
            return str(path)
        else:
            return path

    def makePath(self, argv):
        return os.path.normcase(os.path.normpath(os.path.join(*argv)))

    def isValid(self, path):
        try:
            if pathlib.Path(path).exists():
                return True
            else:
                return False
        except Exception:
            return False
