# -*- coding: utf-8 -*-

import PyQt5.QtCore as QtCore
import datetime


class LogItem(QtCore.QObject):

    def __init__(self, sourceModule, msgType, msg):
        super(LogItem, self).__init__()
        try:
            self.time = datetime.datetime.now()
            self.source = sourceModule
            self.msgType = msgType
            self.msg = msg
        except Exception:
            pass

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
        return self.time.strftime("%Y-%m-%d %H:%m:%S")

    def sourceName(self):
        return self.source.__class__.__name__

    def getColumns(self):
        return [self.timeString(), self.msgTypeString(), self.sourceName(), self.msgString()]

    def getColumnNames(self):
        return ["time", "type", "source", "message"]


class LogManager(QtCore.QObject):

    entryAdded = QtCore.pyqtSignal(LogItem)

    def __init__(self, fileName, main):
        super(LogManager, self).__init__()
        self.main = main
        self.logList = []

    def log(self, src, msgType, args):
        item = LogItem(src, msgType, args)
        self.logList.append(item)
        self.entryAdded.emit(item)

    def getItemElementNames(self):
        return LogItem(None, 0, "").getColumnNames()

    def dumpLog(self, fileName):
        with open(fileName, "w", encoding="utf-8") as file:
            for i in range(0, len(self.logList)):
                file.write(str(self.logList[i]) + "\n")
