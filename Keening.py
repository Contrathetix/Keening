# -*- coding: utf-8 -*-

import PyQt5.QtWidgets as QtWidgets
import sys
import Backend
import KeeningCmd
import KeeningWidget


class Keening(QtWidgets.QApplication):

    def __init__(self, argv):
        super(Keening, self).__init__(argv)
        self.backend = Backend.Backend(self)
        if len(argv) < 2:
            self.widget = KeeningWidget.KeeningGui(self)
        else:
            if "-info" in argv:
                self.info()
            elif "-cmd" in argv:
                KeeningCmd.KeeningCmd(self)
            elif "-launch" in argv:
                app = argv[argv.index("-launch") + 1]
                print("-----> launch", app)
            else:
                self.info()
            self.backend.exit()

    def info(self):
        usage = [
            "Usage:",
            "\t-info\t\tshow this and exit",
            "\t-cmd\t\topen command line interface",
            "\t-launch <exe>\tlaunch a program"
        ]
        [print("\t" + u) for u in usage]


if __name__ == "__main__":
    app = Keening(sys.argv)
    sys.exit(app.exec_())
