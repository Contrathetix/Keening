#!/usr/bin/python3

import os
import sys
import PyQt5.QtWidgets as QtWidgets
import templates.KeeningTemplate as KeeningTemplate


class Keening(KeeningTemplate.KeeningTemplate):

    def __init__(self, app):
        super().__init__(app)


if __name__ == "__main__":
    os.chdir("./Documents/Keening")
    app = QtWidgets.QApplication(sys.argv)
    gui = Keening(app)
    sys.exit(app.exec_())
