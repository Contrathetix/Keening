# -*- coding: utf-8 -*-

import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
import PluginManagerWidget


class Plugin(QtWidgets.QTreeWidgetItem):
    def __init__(self, argv):
        super(Plugin, self).__init__()


class PluginManager(QtCore.QObject):

    def __init__(self, backend):
        super(PluginManager, self).__init__()
        self.widget = PluginManagerWidget.PluginList(self)
