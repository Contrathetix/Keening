# -*- coding: utf-8 -*-

import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets


class PreferencesMenu(QtWidgets.QMainWindow):

    def __init__(self, parent):
        super(PreferencesMenu, self).__init__()
        self.parent = parent
        self.parent.setLocked(self, True)
        self.initUI()
        self.show()

    def initUI(self):
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.pathDefinitions())
        layout.setContentsMargins(20, 20, 20, 20)
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        # self.resize(600, self.height())
        self.setFixedWidth(600)
        self.setWindowTitle("Keening - Preferences")
        self.setWindowIcon(QtGui.QIcon(self.parent.resolveResource("icon.png")))

    def pathDefinitions(self):
        self.pathGame = QtWidgets.QLineEdit(self.parent.main.configManager.getPathGame())
        self.pathMods = QtWidgets.QLineEdit(self.parent.main.configManager.getPathMods())
        self.pathData = QtWidgets.QLineEdit(self.parent.main.configManager.getPathData())
        btnGame = QtWidgets.QPushButton("select")
        btnGame.clicked.connect(lambda: self.pickPath("game"))
        btnMods = QtWidgets.QPushButton("select")
        btnMods.clicked.connect(lambda: self.pickPath("mods"))
        btnData = QtWidgets.QPushButton("select")
        btnData.clicked.connect(lambda: self.pickPath("data"))
        groupBox = QtWidgets.QGroupBox("Path definitions")
        layout = QtWidgets.QGridLayout()
        # layout.setSpacing(30)
        layout.addWidget(QtWidgets.QLabel("game"), 0, 0, 1, 1)
        layout.addWidget(QtWidgets.QLabel("mods"), 1, 0, 1, 1)
        layout.addWidget(QtWidgets.QLabel("data"), 2, 0, 1, 1)
        layout.addWidget(self.pathGame, 0, 1, 1, 1)
        layout.addWidget(self.pathMods, 1, 1, 1, 1)
        layout.addWidget(self.pathData, 2, 1, 1, 1)
        layout.addWidget(btnGame, 0, 2, 1, 1)
        layout.addWidget(btnMods, 1, 2, 1, 1)
        layout.addWidget(btnData, 2, 2, 1, 1)
        groupBox.setLayout(layout)
        return groupBox

    def pickPath(self, whichPath):
        self.centralWidget().setDisabled(True)
        path = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        if whichPath == "game":
            self.parent.main.configManager.setPathGame(path)
            self.pathGame.setText(self.parent.main.configManager.getPathGame())
        elif whichPath == "mods":
            self.parent.main.configManager.setPathMods(path)
            self.pathMods.setText(self.parent.main.configManager.getPathMods())
        elif whichPath == "data":
            self.parent.main.configManager.setPathData(path)
            self.pathMods.setText(self.parent.main.configManager.getPathData())
        self.centralWidget().setDisabled(False)

    def closeEvent(self, event):
        self.parent.setLocked(None, False)
        event.accept()
