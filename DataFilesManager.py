# -*- coding: utf-8 -*-

import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
import DataFilesManagerWidget
import os


class Plugin(QtWidgets.QTreeWidgetItem):
    def __init__(self, dataFilesManager, argv):
        super(Plugin, self).__init__(dataFilesManager)
        self.dataFilesManager = dataFilesManager


class DataFilesManager(QtCore.QObject):

    def __init__(self, backend):
        super(DataFilesManager, self).__init__(backend)
        self.backend = backend
        self.backend.modSetupChanged.connect(self.updateInstalledFiles)
        self.widget = DataFilesManagerWidget.DataTabWidget(self)
        self.fileMap = []

    def updateInstalledFiles(self, modList):
        gamePath = self.backend.getPath([self.backend.getPathGame(), "Data Files"])
        self.bgWorker = DataFilesManager.FilePairGenerator(self, modList, gamePath)
        self.bgWorker.progressUpdate.connect(self.backend.progressChange)
        self.bgWorker.finished.connect(self.fileListReady)
        self.backend.setInterfaceLocked(True)
        self.bgWorker.start()

    def fileListReady(self, newMap):
        self.backend.setInterfaceLocked(False)
        [self.fileMap.append(i) for i in newMap]
        # for p in fileMap.keys():
        #    print("Map \"" + str(p) + "\" --> \"" + str(fileMap[p]) + "\"")

    class FilePairGenerator(QtCore.QThread):

        progressUpdate = QtCore.pyqtSignal(int, int)
        finished = QtCore.pyqtSignal(dict)

        def __init__(self, parent, modList, gamePath):
            super(DataFilesManager.FilePairGenerator, self).__init__(parent)
            self.modList = modList
            self.gamePath = gamePath

        def run(self):
            try:
                maxProgress = len(self.modList)
                curProgress = 0
                installed = {}
                self.progressUpdate.emit(curProgress, maxProgress)
                self.sleep(0.5)
                for mod in reversed(self.modList):
                    curProgress += 1
                    self.progressUpdate.emit(curProgress, maxProgress)
                    if not mod.active():
                        continue
                    for file in mod.relativeFiles():
                        installed[file] = os.path.join(self.gamePath, file)
            except Exception as exc:
                print(exc)
            self.sleep(0.5)
            self.progressUpdate.emit(2, 1)
            self.sleep(0.5)
            self.finished.emit(installed)
            self.installer = None
            self.modList = None
