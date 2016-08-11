# -*- coding: utf-8 -*-

import PyQt5.Qt as Qt
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets


class KeeningGui(QtWidgets.QMainWindow):

    def __init__(self, app):
        super(KeeningGui, self).__init__()
        self.app = app
        self.app.setStyle("fusion")
        self.backend = app.backend
        self.setupUI()
        self.backend.interfaceLock.connect(self.mainWidget.setDisabled)
        self.backend.progressChange.connect(self.mainWidget.progressBar.setProgress)
        self.show()

        # display the splash screen
        # self.splash = QtWidgets.QSplashScreen(QtGui.QPixmap(self.backend.getResource("splash.png")))
        # self.splash.close()

    def setupUI(self):
        self.mainWidget = MainWidget(self, self.backend)
        self.resize(self.backend.getGuiSize())
        self.setWindowTitle("Keening")
        self.setWindowIcon(QtGui.QIcon(self.backend.getResource("icon.png")))
        self.setCentralWidget(self.mainWidget)


class Splash(QtWidgets.QSplashScreen):

    def __init__(self, gui, backend):
        super(Splash, self).__init__(gui)
        self.setPixmap(
            QtGui.QPixmap(backend.getResource("splash.png"))
        )
        self.show()


class MainWidget(QtWidgets.QWidget):

    def __init__(self, gui, backend):
        super(MainWidget, self).__init__(gui)
        self.gui = gui
        self.backend = backend
        self.progressBar = ProgressWidget(self)

        # tab widget with tabs from various modules
        self.tabWidget = QtWidgets.QTabWidget(self)
        self.tabWidget.addTab(self.backend.widgetMods(), "Installers")
        self.tabWidget.addTab(QtWidgets.QWidget(), "Plugins")
        self.tabWidget.addTab(QtWidgets.QWidget(), "Savegames")
        self.tabWidget.addTab(QtWidgets.QWidget(), "Preferences")

        # vertical splitter
        self.splitter = QtWidgets.QSplitter(Qt.Qt.Vertical, self)
        self.splitter.addWidget(self.tabWidget)
        self.splitter.addWidget(self.backend.widgetLog())
        self.splitter.setStretchFactor(0, 3)
        self.splitter.setStretchFactor(1, 1)

        self.vbox = QtWidgets.QVBoxLayout(self)
        self.vbox.addWidget(self.splitter)
        self.vbox.addWidget(self.progressBar)

        # the final layout
        self.setLayout(self.vbox)


class ProgressWidget(QtWidgets.QProgressBar):

    def __init__(self, main):
        super(ProgressWidget, self).__init__(main)
        self.setRange(0, 1)
        self.setValue(0)
        self.setDisabled(True)

    def setProgress(self, _cur, _max):
        isDone = (_cur >= _max)
        self.setDisabled(isDone)
        if _max != self.maximum():
            self.setRange(0, _max)
        self.setValue(_cur)
