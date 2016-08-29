# -*- coding: utf-8 -*-

import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import Usvfs
import os


class Launcher(QtWidgets.QWidget):

    def __init__(self, app):
        super(Launcher, self).__init__()
        self.app = app
        self.processes = []
        self.dropdown = QtWidgets.QComboBox(self)
        self.btnRun = QtWidgets.QPushButton("launch", self)
        self.btnAdd = QtWidgets.QPushButton("+", self)
        self.btnDel = QtWidgets.QPushButton("-", self)

        # update programs
        self.getPrograms()

        # widget signals
        self.btnRun.clicked.connect(self.runProgram)
        self.btnAdd.clicked.connect(self.addProgram)
        self.btnDel.clicked.connect(self.delProgram)

        # layout
        self.hbox = QtWidgets.QHBoxLayout(self)
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.hbox.addWidget(self.btnAdd)
        self.hbox.setStretchFactor(self.btnAdd, 0)
        self.hbox.addWidget(self.btnDel)
        self.hbox.setStretchFactor(self.btnDel, 0)
        self.hbox.addWidget(self.dropdown)
        self.hbox.setStretchFactor(self.dropdown, 1)
        self.hbox.addWidget(self.btnRun)
        self.hbox.setStretchFactor(self.btnRun, 0)
        self.setLayout(self.hbox)

    def getPrograms(self):
        apps = self.app.database().getApps()
        self.dropdown.clear()
        [self.dropdown.addItem(a) for a in apps if os.path.isfile(a)]

    def addProgram(self):
        path = QtWidgets.QFileDialog.getOpenFileName(
            parent=self,
            caption="Select executable to add",
            directory=".",
            filter="*.*",
            # options=(QtWidgets.QFileDialog.DontUseNativeDialog)
        )[0].replace("/", "\\")
        if not os.path.isfile(path):
            self.app.log(self, 2, "invalid path: " + path)
        else:
            apps = [self.dropdown.itemText(i) for i in range(0, self.dropdown.count())]
            apps.append(path)
            self.app.database().setApps(apps)
            self.app.log(self, 0, "added app: " + path)
            self.getPrograms()

    def delProgram(self):
        toRemove = self.dropdown.currentText()
        items = [self.dropdown.itemText(i) for i in range(0, self.dropdown.count())]
        items.remove(toRemove)
        self.app.database().setApps(items)
        self.getPrograms()
        self.app.log(self, 0, "removed app: " + toRemove)

    def runProgram(self):
        program = self.dropdown.currentText()
        if len(program) < 3 or not os.path.isfile(program):
            self.app.log(self, 2, "invalid program: " + program)
        else:
            self.app.log(self, 0, "launching " + program)
            self.processes.append(Launcher.Launch(
                self.app,
                self.dropdown.currentText(),
                self.app.preferences().pathMods(),
                self.app.preferences().pathData(),
                self.app.database().getInstalledMods()
            ))

    class Launch(QtCore.QThread):

        progressUpdate = QtCore.pyqtSignal(int, int)

        def __init__(self, app, program, pathMods, pathData, mods):
            super(Launcher.Launch, self).__init__()
            self.app = app
            self.progressUpdate.connect(self.app.progress)
            self.program = program  # + " \"" + pathData + "\""
            self.workingDir = os.path.dirname(os.path.realpath(program))
            self.pathMods = pathMods
            self.pathData = pathData
            self.mods = mods
            self.start()

        def run(self):
            self.vfs = Usvfs.Usvfs()
            progress = [0, len(self.mods)]
            self.progressUpdate.emit(*progress)
            for mod in self.mods:
                self.vfs.VirtualLinkDirectoryStatic(
                    str(os.path.join(self.pathMods, mod)),
                    self.pathData
                )
                progress[0] += 1
                self.progressUpdate.emit(*progress)
                self.sleep(0.3)
            print(self.vfs.CreateVFSDump())
            print(self.vfs.CreateProcessHooked(
                self.program,
                self.workingDir
            ))
            self.progressUpdate.emit(1, 1)
            print("launcher finished")
