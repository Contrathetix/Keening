# -*- coding: utf-8 -*-

import os
import sys
import pathlib
import PyQt5.QtCore as QtCore


class PathManager(QtCore.QObject):

    def __init__(self, main):
        super(PathManager, self).__init__()
        self.main = main

    def resolveResource(self, fileName):
        try:
            basePath = sys._MEIPASS
        except Exception:
            basePath = os.path.abspath(".")
        return os.path.join(basePath, "Resource", fileName)

    def makePath(self, args, create=False):
        if type(args) is list:
            path = pathlib.Path(os.path.join(*args))
        else:
            path = pathlib.Path(args)
        if create and not path.exists():
            if len(path.suffix) > 0:
                path.touch()
            else:
                path.mkdir()
        return str(path)

    def formatPath(self, path):
        return str(os.path.abspath(str(path))).replace("/", "\\")

    def pathExists(self, args):
        if type(args) is list:
            path = pathlib.Path(os.path.join(args))
        else:
            path = pathlib.Path(args)
        return path.exists()
