# -*- coding: utf-8 -*-

import PyQt5.QtWidgets as QtWidgets


class ModInspector(QtWidgets.QMainWindow):
    def __init__(self, parent):
        super(ModInspector, self).__init__()
        self.parent = parent
        self.setWindowTitle("Keening - ModInspector")
        self.setWindowIcon("resource/icon.png")

    def closeEvent(self, event):
        print("closing")
        event.accept()
