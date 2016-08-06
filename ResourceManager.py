# -*- coding: utf-8 -*-

from PyQt5.QtGui import QIcon, QImage, QPixmap
from PyQt5.QtCore import QFile
# import pathlib


class ResourceManager:
    def __init__(self, a_app):
        self.app = a_app
        self.fileMap = {}

    def getImage(self, path):
        path = "resource/" + path
        f = self.getFile(path)
        return QImage(f.read(f.size()))

    def getIcon(self, path):
        path = "resource/" + path
        f = self.getFile(path)
        return QIcon(f.read(f.size()))

    def getPixmap(self, path):
        path = "resource/" + path
        # f = self.getFile(path)
        return QPixmap("resource/icon.png")

    def readFile(self, path):
        path = self.app.pathManager.getPath(path, False)
        if not path:
            return ""
        else:
            with open(str(path), "r", encoding="utf-8") as f:
                return f.read()

    def getFile(self, path):
        path_a = path
        path = self.app.pathManager.getPath(path, False)
        if not path:
            self.app.log([self, "error", "GetFile: inexistent (" + str(path_a) + ")"])
            return QFile()
        name = path.name
        if name in self.fileMap.keys():
            self.app.log([self, "info", "GetFile: use existing (" + str(path_a) + ")"])
            return self.fileMap[name]
        else:
            f = QFile(str(path))
            if f.exists():
                self.fileMap[name] = f
                self.app.log([self, "info", "GetFile: load new (" + str(path_a) + ")"])
                return f
            else:
                return QFile()
