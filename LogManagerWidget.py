# -*- coding: utf-8 -*-

import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import PyQt5.Qt as Qt


class LogList(QtWidgets.QTreeWidget):

    def __init__(self, logManager):
        super(LogList, self).__init__()
        self.setRootIsDecorated(False)
        self.setAlternatingRowColors(True)
        self.setHorizontalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOn)
        self.setIconSize(QtCore.QSize(10, 10))

    def updateItems(self, itemList):
        if len(itemList) > 0:
            self.setHeaderLabels(itemList[0].getColumnNames())
            self.addTopLevelItems(itemList)
        for i in range(0, self.columnCount() - 1):
            self.resizeColumnToContents(i)
            self.setColumnWidth(i, self.columnWidth(i) + 20)
