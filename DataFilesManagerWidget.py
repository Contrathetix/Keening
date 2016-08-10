# -*- coding: utf-8 -*-

import PyQt5.QtWidgets as QtWidgets
import PyQt5.Qt as Qt


class DataTabWidget(QtWidgets.QTabWidget):

    def __init__(self, dataFilesManager):
        super(DataTabWidget, self).__init__()
        self.dataFilesManager = dataFilesManager
        self.backend = dataFilesManager.backend

    class PluginList(QtWidgets.QTreeWidget):
        def __init__(self, parent):
            super(DataTabWidget.PluginList, self).__init__()
            self.parent = parent
            self.setHorizontalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOff)
            self.setVerticalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOn)
