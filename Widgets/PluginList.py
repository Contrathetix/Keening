# -*- coding: utf-8 -*-

import PyQt5.QtWidgets as QtWidgets
import PyQt5.Qt as Qt


class PluginListItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, argv):
        super(PluginListItem, self).__init__()


class PluginList(QtWidgets.QTreeWidget):
    def __init__(self, parent):
        super(PluginList, self).__init__()
        self.parent = parent
        self.setHorizontalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOn)
