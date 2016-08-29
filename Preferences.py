# -*- coding: utf-8 -*-

import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore


class Preferences(QtWidgets.QWidget):

    def __init__(self, app):
        super(Preferences, self).__init__()
        self.app = app
        self.app.aboutToQuit.connect(self.updateDatabase)

        # init preferences (default + from db)
        self.prefs = {
            "pathGame": "game",
            "pathMods": "mods",
            "guiWidth": "1000",
            "guiHeight": "600"
        }
        self.updateFromDb()

        # widgets
        self.pathGameTxt = QtWidgets.QLineEdit(self.pathGame(), self)
        self.pathGameBtn = QtWidgets.QPushButton("select", self)
        self.pathModsTxt = QtWidgets.QLineEdit(self.pathMods(), self)
        self.pathModsBtn = QtWidgets.QPushButton("select", self)

        # widget signal connections
        self.pathGameBtn.clicked.connect(lambda: self.pickPath("Game"))
        self.pathModsBtn.clicked.connect(lambda: self.pickPath("Mods"))

        # layout
        self.grid = QtWidgets.QGridLayout(self)
        self.grid.addWidget(QtWidgets.QLabel("Game", self), 0, 0, 1, 1)
        self.grid.addWidget(QtWidgets.QLabel("Mods", self), 1, 0, 1, 1)
        self.grid.addWidget(self.pathGameTxt, 0, 1, 1, 1)
        self.grid.addWidget(self.pathModsTxt, 1, 1, 1, 1)
        self.grid.addWidget(self.pathGameBtn, 0, 2, 1, 1)
        self.grid.addWidget(self.pathModsBtn, 1, 2, 1, 1)

        # set the layout
        self.setLayout(self.grid)

    def pickPath(self, which):
        try:
            path = QtWidgets.QFileDialog.getExistingDirectory(
                self, which + " folder", ".", QtWidgets.QFileDialog.ShowDirsOnly
            )
            path = self.app.path().make(path)
            self.prefs["path" + which] = path
            self.pathGameTxt.setText(self.pathGame())
            self.pathModsTxt.setText(self.pathMods())
        except Exception as exc:
            self.app.log(self, 1, str(exc))

    def updateFromDb(self):
        info = self.app.database().getPreferences()
        for key in info.keys():
            try:
                self.prefs[key] = info[key]
            except Exception:
                pass

    def guiSize(self, size=None):
        try:
            self.prefs["guiWidth"] = str(size.width())
            self.prefs["guiHeight"] = str(size.height())
        except AttributeError:
            return QtCore.QSize(
                int(self.prefs["guiWidth"]),
                int(self.prefs["guiHeight"])
            )
        except Exception:
            return QtCore.QSize(500, 500)

    def updateDatabase(self):
        self.guiSize(self.app.gui().size())
        self.app.database().setPreferences(self.prefs)

    def pathMods(self):
        try:
            return self.app.path().make(self.prefs["pathMods"])
        except Exception:
            self.prefs["pathMods"] = "game"
            return self.app.path().make("mods")

    def pathGame(self):
        try:
            return self.app.path().make(self.prefs["pathGame"])
        except Exception:
            self.prefs["pathGame"] = "game"
            return self.app.path().make("game")

    def pathData(self):
        try:
            return self.app.path().make([self.prefs["pathGame"], "Data Files"])
        except Exception:
            return self.app.path().make(["game", "Data Files"])
