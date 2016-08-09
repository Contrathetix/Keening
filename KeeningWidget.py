# -*- coding: utf-8 -*-

import PyQt5.Qt as Qt
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
import time


class KeeningGui(QtWidgets.QMainWindow):

    def __init__(self, app):
        super(KeeningGui, self).__init__()
        splash = KeeningGui.Splash(app.backend)
        self.app = app
        self.app.setStyle("fusion")
        self.backend = app.backend
        self.backend.progressChange.connect(self.setProgress)
        self.backend.interfaceLock.connect(self.setLocked)
        self.guiBreather = KeeningGui.GuiBreather(app, 100)
        self.mainWidget = KeeningGui.MainWidget(self)
        self.resize(self.backend.getGuiSize())
        self.setWindowTitle("Keening")
        self.setWindowIcon(QtGui.QIcon(self.backend.getResource("icon.png")))
        self.setCentralWidget(self.mainWidget)
        self.setProgress(1, 2)
        time.sleep(1)
        splash.close()
        self.show()

    def setProgress(self, maxProgress, currentProgress):
        self.mainWidget.setProgress(maxProgress, currentProgress)

    def setLocked(self, widget, locked):
        self.mainWidget.setLocked(widget, locked)

    class Splash(QtWidgets.QSplashScreen):

        def __init__(self, backend):
            super(KeeningGui.Splash, self).__init__()
            self.setPixmap(
                QtGui.QPixmap(backend.getResource("splash.png"))
            )
            self.show()

    class GuiBreather(QtCore.QThread):

        def __init__(self, app, updateInterval):
            super(KeeningGui.GuiBreather, self).__init__()
            self.updateInterval = updateInterval
            app.aboutToQuit.connect(self.quit)
            self.start()

        def run(self):
            while True:
                QtWidgets.QApplication.processEvents()
                self.sleep(self.updateInterval)

    class MainWidget(QtWidgets.QWidget):

        def __init__(self, main):
            super(KeeningGui.MainWidget, self).__init__()
            self.main = main
            self.backend = self.main.backend
            self.progressBar = QtWidgets.QProgressBar(self)
            self.widgetLog = self.backend.widgetLog()
            self.widgetMods = self.backend.widgetMods()
            self.widgetPlugins = self.backend.widgetPlugins()
            # self.launcherList = KgWidgets.LauncherDropdown()
            # self.launcherList.setMinimumHeight(30)
            # self.launcherButton = QtWidgets.QPushButton(
            #     QtGui.QIcon(main.pathManager.resolveResource("btnlaunch.png")), None
            # )
            # self.launcherButton.setMinimumHeight(30)

            # right hand side widgets
            layout = QtWidgets.QGridLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setColumnStretch(0, 10)
            layout.setColumnStretch(1, 1)
            # layout.addWidget(self.launcherList, 0, 0, 1, 1)
            # layout.addWidget(self.launcherButton, 0, 1, 1, 1)
            layout.addWidget(self.widgetPlugins, 1, 0, 1, 2)
            rightPane = QtWidgets.QWidget()
            rightPane.setLayout(layout)

            # horizontal splitter
            splitterH = QtWidgets.QSplitter(Qt.Qt.Horizontal, self)
            splitterH.addWidget(self.widgetMods)
            splitterH.addWidget(rightPane)
            splitterH.setStretchFactor(0, 2)
            splitterH.setStretchFactor(1, 1)

            # vertical splitter
            splitterV = QtWidgets.QSplitter(Qt.Qt.Vertical, self)
            splitterV.addWidget(splitterH)
            splitterV.addWidget(self.widgetLog)
            splitterV.setStretchFactor(0, 4)
            splitterV.setStretchFactor(1, 1)

            # toolbar
            exitAction = Qt.QAction(
                QtGui.QIcon(self.backend.getResource("icon.png")),
                "Quit",
                self
            )
            exitAction.setShortcut('Ctrl+Q')
            exitAction.triggered.connect(main.app.quit)
            preferences = Qt.QAction(
                QtGui.QIcon(self.backend.getResource("btnprefs.png")),
                "Preferences",
                self
            )
            # preferences.setShortcut('Ctrl+Q')
            # preferences.triggered.connect(lambda: KgWidgets.PreferencesMenu(self))
            toolbar = main.addToolBar("Tools")
            toolbar.addAction(exitAction)
            toolbar.addAction(preferences)
            toolbar.setIconSize(Qt.QSize(32, 32))
            toolbar.setToolButtonStyle(Qt.Qt.ToolButtonIconOnly)
            toolbar.setContextMenuPolicy(Qt.Qt.PreventContextMenu)
            toolbar.setMovable(False)
            self.toolbar = toolbar

            # add to vertical layout
            vbox = QtWidgets.QVBoxLayout()
            vbox.addWidget(splitterV)
            vbox.addWidget(self.progressBar)
            self.setLayout(vbox)

        def resolveResource(self, name):
            return self.main.resolveResource(name)

        def setLocked(self, widget, lock):
            self.activeWidget = widget
            self.setDisabled(lock)
            self.toolbar.setDisabled(lock)
            QtWidgets.QApplication.processEvents()

        def setProgress(self, maxProgress, currentProgress):
            try:
                self.progressBar.setMaximum(maxProgress)
                self.progressBar.setValue(currentProgress)
                if (currentProgress >= maxProgress):
                    self.progressBar.setDisabled(True)
            except Exception:
                pass
