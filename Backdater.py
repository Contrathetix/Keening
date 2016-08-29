# -*- coding: utf-8 -*-

import PyQt5.QtWidgets as QtWidgets
import datetime
import time
import os


class Backdater(QtWidgets.QWidget):

    def __init__(self, app):
        super(Backdater, self).__init__()
        self.app = app
        self.times = self.oldTime()

        # button
        self.btn = QtWidgets.QPushButton("back-date BSAs", self)

        # connect signal
        self.btn.clicked.connect(self.backdate)

        # layout
        self.hbox = QtWidgets.QHBoxLayout(self)
        self.hbox.addWidget(self.btn)
        self.setLayout(self.hbox)

    def backdate(self):
        try:
            self.recurse(self.app.preferences().pathData())
            self.app.log(self, 0, "backdated files")
        except Exception as exc:
            self.app.log(self, 1, str(exc))

    def recurse(self, path):
        for e in self.app.path().scandir(path):
            if e.is_file():
                print(e.path, self.times)
                os.utime(path=str(e.path), times=self.times)
            else:
                self.recurse(e.path)

    def oldTime(self):
        t = datetime.datetime(2002, 2, 2, 0, 0, 0)
        t = int(time.mktime(t.timetuple()))
        t = (t, t)
        print(t)
        print(datetime.datetime.fromtimestamp(t[0]))
        return t
