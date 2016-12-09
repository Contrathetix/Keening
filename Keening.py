#!/usr/bin/python3

import os
import sys
import shutil
import importlib
import PyQt5.QtWidgets as QtWidgets


class Keening(QtWidgets.QMainWindow):

    def __init__(self, app):
        super().__init__()
        self.__app = app
        self.__modules = {}
        self.init_modules()
        self.init_gui()
        print(self.__modules["PathManager"].get_paths())

    def init_modules(self):
        print("importing modules...")
        a = [f.name.split(".")[0] for f in os.scandir("modules")]
        for f in a:
            if f == "__pycache__":
                continue
            print("import", f)
            obj = getattr(importlib.import_module("modules." + f), f)
            self.__modules[f] = obj()
        shutil.rmtree(os.path.join("modules", "__pycache__"))
        print("import finished")

    def init_plugins(self):
        pass

    def init_gui(self):
        self.resize(600, 400)
        self.setWindowTitle("Keening")
        self.show()

if __name__ == "__main__":
    os.chdir("./Documents/Keening")
    app = QtWidgets.QApplication(sys.argv)
    gui = Keening(app)
    sys.exit(app.exec_())
