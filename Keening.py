#!/usr/bin/python3

import os
import sys
import shutil
import importlib
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets


class Keening(QtWidgets.QMainWindow):

    def __init__(self, app):
        super().__init__()
        self.__app = app
        self.__funcdict = {}
        self.__modules = {}
        self.call = self.function_call
        self.init_modules()
        self.init_gui()
        # print(self.function_call("path_get_paths", "."))

    def init_modules(self):
        a = [f.name.split(".")[0] for f in os.scandir("modules")]
        for f in a:
            if f == "__pycache__":
                continue
            obj = getattr(importlib.import_module("modules." + f), f)
            self.__modules[f] = obj(self)
        shutil.rmtree(os.path.join("modules", "__pycache__"))

    def init_plugins(self):
        pass

    def init_gui(self):
        self.resize(600, 400)
        self.setWindowTitle("Keening")
        self.setWindowIcon(self.call("asset_get_icon", "icon.png"))
        self.show()

    def function_register(self, funcname, method):
        try:
            self.__funcdict[funcname] = method
        except Exception as exc:
            print("exception:", exc)

    def function_unregister(self, funcname):
        try:
            self.__funcdict.remove(funcname)
        except Exception as exc:
            print("exception:", exc)

    def function_call(self, funcname, *funcargs):
        try:
            func = self.__funcdict[funcname]
            return func(*funcargs)
        except Exception as exc:
            print("exception:", exc)
            return None


if __name__ == "__main__":
    os.chdir("./Documents/Keening")
    app = QtWidgets.QApplication(sys.argv)
    gui = Keening(app)
    sys.exit(app.exec_())
