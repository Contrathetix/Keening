import os
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
import modules.ModuleTemplate as ModuleTemplate


class AssetManager(ModuleTemplate.ModuleTemplate):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__assetlist = {}
        self.method_register("asset_get_icon", self.get_icon)

    def __get_asset(self, obj_type, name):
        if name not in list(self.__assetlist.keys()):
            obj = obj_type(os.path.abspath(os.path.join("assets", name)))
            self.__assetlist[name] = obj
        else:
            obj = self.__assetlist[name]
        return obj

    def get_icon(self, assetname="default.png"):
        return self.__get_asset(QtGui.QIcon, assetname)
