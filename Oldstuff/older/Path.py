# -*- coding: utf-8 -*-

import PyQt5.QtCore as QtCore
import pathlib
import sys
import os


class Path(QtCore.QObject):

    def __init__(self, app):
        super(Path, self).__init__()
        self.app = app

    def make(self, args):
        if type(args) in [tuple, list]:
            path = pathlib.Path(*args)
        else:
            path = pathlib.Path(args)
        if not path.exists():
            if len(path.suffix) < 1:
                path.mkdir(parents=True)
            else:
                path.touch()
        return str(path.resolve())

    def asset(self, name):
        try:
            path = sys._MEIPASS
        except Exception:
            path = '.'
        return str(pathlib.Path(path, 'assets', name).resolve())

    def mod(self, name):
        try:
            path = pathlib.Path(self.app.preferences().pathMods(), name)
            try:
                return str(path.resolve())
            except Exception:
                return str(path)
        except Exception:
            return ""

    def renameMod(self, oldName, newName):
        src = self.mod(oldName)
        dst = self.mod(newName)
        if os.path.isdir(dst):
            self.app.log(self, 2, 'rename target exists: ' + str(dst))
            return False
        try:
            os.rename(src, dst)
            return True
        except Exception as exc:
            self.app.log(self, 1, str(exc))
            return False

    def getFiles(self, path, relative=False):
        self.pathList = []
        self.getFilesRecursive(path)
        if relative:
            self.pathList[:] = [os.path.relpath(p, path) for p in self.pathList]
        return self.pathList

    def getFilesRecursive(self, path):
        for f in sorted(os.scandir(path), key=lambda e: e.inode()):
            if f.is_dir():
                self.getFilesRecursive(f.path)
            else:
                self.pathList.append(os.path.abspath(f.path))

    def scandir(self, path):
        if not os.path.isdir(path):
            return []
        else:
            entries = os.scandir(path)
            return sorted(entries, key=lambda e: e.inode(), reverse=False)
