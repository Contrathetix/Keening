# -*- coding: utf-8 -*-

import PyQt5.QtWidgets as QtWidgets
import PyQt5.Qt as Qt
import datetime


class Log(QtWidgets.QTreeWidget):

    def __init__(self, app):
        super(Log, self).__init__()
        self.app = app
        self.app.aboutToQuit.connect(self.dump)
        self.types = ['info', 'exception', 'error']
        self.setRootIsDecorated(False)
        self.setAlternatingRowColors(False)
        self.setHorizontalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOn)
        self.setHeaderLabels(['time', 'type', 'source', 'message'])

    def log(self, src, num, msg):
        if type(msg) is list:
            msg = ' '.join(msg)
        self.addTopLevelItem(Log.LogItem([
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            self.types[num],
            src.__class__.__name__,
            msg
        ]))
        for i in range(0, self.columnCount()):
            self.resizeColumnToContents(i)
            self.setColumnWidth(i, self.columnWidth(i) + 50)

    def dump(self):
        with open('Keening.log', 'w', encoding='utf-8') as file:
            for i in range(0, self.topLevelItemCount()):
                file.write(str(self.topLevelItem(i)) + '\n')

    class LogItem(QtWidgets.QTreeWidgetItem):

        def __init__(self, values):
            super(Log.LogItem, self).__init__()
            self.values = values
            for i in range(0, len(self.values)):
                self.setText(i, self.values[i])

        def __str__(self):
            try:
                return ''.join([
                    '{} | '.format(self.values[0]),
                    '{0: <10} | '.format(self.values[1]),
                    '{0: <16} | '.format(self.values[2]),
                    self.values[3]
                ])
            except Exception:
                return "<error>"
