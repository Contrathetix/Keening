# -*- coding: utf-8 -*-

import PyQt5.QtWidgets as QtWidgets


class LauncherDropdown(QtWidgets.QComboBox):

    def __init__(self):
        super(LauncherDropdown, self).__init__()

    def setItems(self, items):
        self.clear()
        self.addItems(items)
