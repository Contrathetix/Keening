# -*- coding: utf-8 -*-

import sys
import pathlib
import PyQt5.QtCore as QtCore


class PathManager(QtCore.QObject):

    def __init__(self):
        super(PathManager, self).__init__()

    def getResource(self, fileName, make=False, toString=True):
        try:
            base = str(sys._MEIPASS)
        except Exception:
            base = "."
        return self.getPath([base, "assets", fileName], make, toString)

    def getData(self, fileName, make=False, toString=True):
        return self.getPath(["data", fileName], make, toString)

    def getPath(self, args, make=False, toString=True):
        if type(args) is list:
            path = pathlib.Path(args[0]).joinpath(*args[1:])
        else:
            path = pathlib.Path(args)
        if make and not path.exists():
            if len(path.suffix) > 0:
                path.touch()
            else:
                path.mkdir()
        if toString:
            return str(path)
        else:
            return path
