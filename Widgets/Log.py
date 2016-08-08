# -*- coding: utf-8 -*-

import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import PyQt5.Qt as Qt


class LogItem(QtWidgets.QTreeWidgetItem):

    def __init__(self, logEntry):
        super(LogItem, self).__init__()
        columns = logEntry.getColumns()
        for i in range(0, len(columns)):
            self.setText(i, columns[i])


class Log(QtWidgets.QTreeWidget):

    def __init__(self, main):
        super(Log, self).__init__()
        self.setRootIsDecorated(False)
        self.setHeaderLabels(main.logManager.getItemElementNames())
        self.setHorizontalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOn)
        self.setIconSize(QtCore.QSize(10, 10))
        for i in main.logManager.logList:
            self.add(i)
        main.logManager.entryAdded.connect(self.add)

    def add(self, logEntry):
        self.addTopLevelItem(LogItem(logEntry))
        for i in range(0, self.columnCount()):
            self.resizeColumnToContents(i)
            self.setColumnWidth(i, self.columnWidth(i) + 20)
