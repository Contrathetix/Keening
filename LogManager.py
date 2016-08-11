# -*- coding: utf-8 -*-

import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
import datetime
import LogManagerWidget


class LogManager(QtCore.QObject):

    def __init__(self, backend, app, filePath):
        super(LogManager, self).__init__(backend)
        self.logList = []
        self.widget = LogManagerWidget.LogList(self, ["time", "type", "source", "message"])
        app.aboutToQuit.connect(lambda: self.dumpLog(filePath))

    def log(self, src, msgType, args):
        item = LogItem(self, src, msgType, args)
        self.logList.append(item)
        self.widget.newItem(item)

    def dumpLog(self, filePath):
        with open(filePath, "w", encoding="utf-8") as file:
            for i in range(0, len(self.logList)):
                file.write(str(self.logList[i]) + "\n")


class LogItem(QtWidgets.QTreeWidgetItem):

    def __init__(self, logManager, sourceModule, msgType, msg):
        super(LogItem, self).__init__()
        self.time = datetime.datetime.now()
        self.source = sourceModule
        self.msgType = msgType
        self.msg = msg
        self.updateColumns()

    def __str__(self):
        return self.timeString() + " | " + self.sourceName() + "\t| " + self.msgString()

    def msgString(self):
        if type(self.msg) is str:
            return self.msg
        else:
            return " ".join(self.msg)

    def msgTypeString(self):
        return ["info", "exception", "error"][self.msgType]

    def timeString(self):
        return self.time.strftime("%Y-%m-%d %H:%M:%S")

    def sourceName(self):
        return self.source.__class__.__name__

    def updateColumns(self):
        self.setText(0, self.timeString())
        self.setText(1, self.msgTypeString())
        self.setText(2, self.sourceName())
        self.setText(3, self.msgString())

    def getColumnNames(self):
        return ["time", "type", "source", "message"]
