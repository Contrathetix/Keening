# -*- coding: utf-8 -*-

import PyQt5.QtWidgets as QtWidgets
import PyQt5.Qt as Qt


class LogList(QtWidgets.QTreeWidget):

    def __init__(self, logManager, headerLabels):
        super(LogList, self).__init__()
        self.setRootIsDecorated(False)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(False)
        self.setHorizontalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOn)
        self.setHeaderLabels(headerLabels)

    def newItem(self, item):
        try:
            self.addTopLevelItem(item)
        except Exception:
            pass
        header = self.header()
        for i in range(0, self.columnCount() - 1):
            self.resizeColumnToContents(i)
            header.resizeSection(i, header.sectionSize(i) + 20)
