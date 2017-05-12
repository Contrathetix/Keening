# -*- coding: utf-8 -*-

import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui
import PyQt5.Qt as Qt
import sys
import time
import Log
import Path
import Mods
import Launcher
import Usvfs
import Backdater
import Preferences
import Database


class Keening(QtWidgets.QApplication):

    def __init__(self, argv):
        super(Keening, self).__init__(argv)
        self._path = Path.Path(self)
        self._splash = QtWidgets.QSplashScreen(
            QtGui.QPixmap(self._path.asset("splash.png"))
        )
        self._splash.show()
        self._log = Log.Log(self)
        self._bd = Backdater.Backdater(self)
        self._database = Database.Database(self)
        self._preferences = Preferences.Preferences(self)
        self._launcher = Launcher.Launcher(self)
        self._mods = Mods.Mods(self)
        self._gui = Keening.Gui(self)
        self._u = Usvfs.Usvfs()
        time.sleep(1)
        self._splash.close()
        self._gui.show()

    def database(self):
        return self._database

    def preferences(self):
        return self._preferences

    def launcher(self):
        return self._launcher

    def backdater(self):
        return self._bd

    def path(self):
        return self._path

    def gui(self):
        return self._gui

    def mods(self):
        return self._mods

    def log(self, src=None, num=None, msg=None):
        if src or num or msg:
            self._log.log(src, num, msg)
        else:
            return self._log

    def progress(self, current, maximum):
        self._gui.setProgress(current, maximum)

    class Gui(QtWidgets.QMainWindow):

        def __init__(self, app):
            super(Keening.Gui, self).__init__()
            self.app = app
            self.app.setStyle("fusion")
            self.resize(app.preferences().guiSize())
            self.setWindowTitle("Keening")
            self.setWindowIcon(QtGui.QIcon(app.path().asset("icon.png")))

            # central widget + layout for it
            self.widget = QtWidgets.QWidget(self)
            self.layout = QtWidgets.QVBoxLayout(self.widget)

            # widgets
            self.progressbar = QtWidgets.QProgressBar(self.widget)
            self.tabWidget = QtWidgets.QTabWidget(self.widget)
            # self.tabWidget.addTab(QtWidgets.QWidget(), "Installers")
            self.tabWidget.addTab(app.mods(), "Mods")
            self.tabWidget.addTab(QtWidgets.QWidget(), "Plugins")
            self.tabWidget.addTab(app.preferences(), "Preferences")
            self.tabWidget.addTab(app.backdater(), "Backdater")

            # progressbar height
            self.progressbar.setMaximumHeight(10)

            # vertical splitter
            self.splitter = QtWidgets.QSplitter(Qt.Qt.Vertical, self.widget)
            self.splitter.addWidget(self.tabWidget)
            self.splitter.addWidget(app.log())
            self.splitter.setStretchFactor(0, 3)
            self.splitter.setStretchFactor(1, 1)

            # layout and main widget
            self.layout.addWidget(self.app.launcher())
            self.layout.addWidget(self.splitter)
            self.layout.addWidget(self.progressbar)
            self.widget.setLayout(self.layout)
            self.setCentralWidget(self.widget)

        def setProgress(self, current, maximum):
            try:
                if current < maximum:
                    self.progressbar.setRange(0, maximum)
                    self.progressbar.setValue(current)
                    self.progressbar.setDisabled(False)
                    self.widget.setDisabled(True)
                else:
                    self.progressbar.setRange(0, 1)
                    self.progressbar.setValue(0)
                    self.progressbar.setDisabled(True)
                    self.widget.setDisabled(False)
            except Exception:
                pass


if __name__ == "__main__":
    app = Keening(sys.argv)
    sys.exit(app.exec_())
