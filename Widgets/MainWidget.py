# -*- coding: utf-8 -*-

import PyQt5.Qt as Qt
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets

import Widgets as KgWidgets


class MainWidget(QtWidgets.QWidget):

    def __init__(self, main):
        super(MainWidget, self).__init__()
        self.main = main
        self.progressBar = QtWidgets.QProgressBar(self)
        self.logWidget = KgWidgets.Log(main)
        self.modList = KgWidgets.ModList(main)
        self.pluginList = KgWidgets.PluginList(main)

        # right hand side widgets
        layout = QtWidgets.QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.pluginList, 0, 0, 1, 1)
        rightPane = QtWidgets.QWidget()
        rightPane.setLayout(layout)

        # horizontal splitter
        splitterH = QtWidgets.QSplitter(Qt.Qt.Horizontal, self)
        splitterH.addWidget(self.modList)
        splitterH.addWidget(rightPane)
        splitterH.setStretchFactor(0, 2)
        splitterH.setStretchFactor(1, 1)

        # vertical splitter
        splitterV = QtWidgets.QSplitter(Qt.Qt.Vertical, self)
        splitterV.addWidget(splitterH)
        splitterV.addWidget(self.logWidget)
        splitterV.setStretchFactor(0, 4)
        splitterV.setStretchFactor(1, 1)

        # toolbar
        exitAction = Qt.QAction(QtGui.QIcon(main.resolveResource("icon.png")), "Quit", self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(main.app.quit)
        preferences = Qt.QAction(QtGui.QIcon(main.resolveResource("btnprefs.png")), "Preferences", self)
        # preferences.setShortcut('Ctrl+Q')
        preferences.triggered.connect(lambda: KgWidgets.PreferencesMenu(self))
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
