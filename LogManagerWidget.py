# -*- coding: utf-8 -*-

import PyQt5.QtWidgets as QtWidgets
import PyQt5.Qt as Qt


class LogList(QtWidgets.QTreeWidget):

    def __init__(self, logManager):
        super(LogList, self).__init__()
        self.setRootIsDecorated(False)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.setHorizontalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOn)
        self.header().setSortIndicator(self.columnCount() - 1, Qt.Qt.AscendingOrder)
        self.header().setSortIndicatorShown(True)
        logManager.updateWidget.connect(self.updateItems)

    def updateItems(self, itemList):
        [self.takeTopLevelItem(i) for i in range(0, self.topLevelItemCount())]
        if len(itemList) > 0:
            self.setHeaderLabels(itemList[0].getColumnNames())
            self.addTopLevelItems(itemList)
        header = self.header()
        for i in range(0, self.columnCount() - 1):
            self.resizeColumnToContents(i)
            header.resizeSection(i, header.sectionSize(i) + 20)
        self.sortItems(header.sortIndicatorSection(), header.sortIndicatorOrder())
