# -*- coding: utf-8 -*-

import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets

import Widgets as KgWidgets
import Modules as Kg

import sys


class Keening(QtWidgets.QMainWindow):

    def __init__(self, app, parent=None):
        super(Keening, self).__init__()
        self.app = app
        self.app.setStyle("fusion")
        self.app.aboutToQuit.connect(self.closing)
        self.refresher = Kg.InterfaceRefresher(app, 100)
        self.logManager = Kg.LogManager("Keening.log", self)
        self.pathManager = Kg.PathManager(self)
        self.configManager = Kg.ConfigManager(self)
        self.databaseManager = Kg.DatabaseManager(self)
        self.modManager = Kg.ModManager(self)
        self.splash = KgWidgets.Splash(self)
        self.modManager.refreshModInfo()
        self.initUI()
        self.splash.close()

    def log(self, src, i, a):
        """Usage: [<source>, <type>, <args>]"""
        self.logManager.log(src, i, a)

    def resolveResource(self, name):
        return self.pathManager.resolveResource(name)

    def initUI(self):
        self.resize(self.configManager.getGuiSize())
        self.mainWidget = KgWidgets.MainWidget(self)
        self.setCentralWidget(self.mainWidget)
        self.setProgress(1, 2)
        self.setWindowTitle("Keening")
        self.setWindowIcon(QtGui.QIcon(self.resolveResource("icon.png")))
        self.show()

    def setProgress(self, maxProgress, currentProgress):
        self.mainWidget.setProgress(maxProgress, currentProgress)

    def setLocked(self, widget, locked):
        self.mainWidget.setLocked(widget, locked)

    def closing(self):
        try:
            self.configManager.dumpPreferences("Keening.ini")
        except Exception:
            pass
        try:
            self.logManager.dumpLog("Keening.log")
        except Exception:
            pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Keening(app)
    sys.exit(app.exec_())
