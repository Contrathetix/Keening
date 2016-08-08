# -*- coding: utf-8 -*-

import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets


class InterfaceRefresher(QtCore.QThread):

    def __init__(self, app, updateInterval):
        super(InterfaceRefresher, self).__init__()
        self.updateInterval = updateInterval
        app.aboutToQuit.connect(self.quit)
        self.start()

    def run(self):
        while True:
            QtWidgets.QApplication.processEvents()
            self.sleep(self.updateInterval)
