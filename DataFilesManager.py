# -*- coding: utf-8 -*-

import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
import DataFilesManagerWidget


class Plugin(QtWidgets.QTreeWidgetItem):
    def __init__(self, argv):
        super(Plugin, self).__init__()


class DataFilesManager(QtCore.QObject):

    def __init__(self, backend):
        super(DataFilesManager, self).__init__()
        self.backend = backend
        self.backend.dataFilesChanged.connect(self.dataFilesChanged)
        self.widget = DataFilesManagerWidget.DataTabWidget(self)
        self.fileList = []
        self.pluginList = []

    def dataFilesChanged(self, newPairs):
        for p in newPairs.keys():
            print("Map \"" + str(p) + "\" --> \"" + str(newPairs[p]) + "\"")
