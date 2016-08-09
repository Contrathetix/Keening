# -*- coding: utf-8 -*-

import PyQt5.QtWidgets as QtWidgets
import sys
import Backend
import KeeningWidget


class Keening(QtWidgets.QApplication):

    def __init__(self, argv):
        super(Keening, self).__init__(argv)
        self.backend = Backend.Backend(self)
        if "-launch" in argv and len(argv) > 2:
            app = argv[argv.index("-launch") + 1]
            print("-----> launch", app)
            self.quit()
        else:
            self.widget = KeeningWidget.KeeningGui(self)


if __name__ == "__main__":
    app = Keening(sys.argv)
    sys.exit(app.exec_())
