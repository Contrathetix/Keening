import os
import sys
import shutil
import importlib
import PyQt5.QtWidgets as QtWidgets


class KeeningTemplate(QtWidgets.QMainWindow):

    def __init__(self, app=None):
        super().__init__()
        self.__app = app
        self.call = self.function_call
        self.init_modules()
        self.init_gui()
        self.init_plugins()
        # print(self.function_call("path_get_paths", "."))

    def init_modules(self):
        self.__modules = {}
        a = [f.name.split(".")[0] for f in os.scandir("modules")]
        for f in a:
            if f == "__pycache__":
                continue
            obj = getattr(importlib.import_module("modules." + f), f)
            self.__modules[f] = obj(self)
        shutil.rmtree(os.path.join("modules", "__pycache__"))

    def init_plugins(self):
        self.__plugins = {}
        a = [f.name.split(".")[0] for f in os.scandir("plugins")]
        for f in a:
            if f == "__pycache__":
                continue
            obj = getattr(importlib.import_module("plugins." + f), f)
            self.__plugins[f] = obj(self)
        shutil.rmtree(os.path.join("plugins", "__pycache__"))

    def init_gui(self):
        layout = QtWidgets.QVBoxLayout(self)
        self.__layout = {}
        self.__layout["tabs"] = QtWidgets.QTabWidget(self)
        self.__layout["log"] = QtWidgets.QWidget(self)
        self.__layout["toolbar"] = QtWidgets.QToolBar(self)
        self.setWindowTitle("Keening")
        self.setWindowIcon(self.call("asset_get_icon", "icon.png"))
        self.show()

    def function_register(self, funcname, method):
        try:
            if not self.__funcdict:
                print("create funcdict")
                self.__funcdict = {}
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

    def widget_register(self, widget):
        try:
            self.__layout[widget.widget_type()] = widget
        except Exception as exc:
            print("exception:", exc)
