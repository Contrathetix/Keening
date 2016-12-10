import os
import PyQt5.QtCore as QtCore
import templates.ModuleTemplate as ModuleTemplate


class PathManager(ModuleTemplate.ModuleTemplate):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.method_register("path_get_paths", self.get_paths)

    def get_paths(self, start_path="."):
        self.__path_list = []
        start_path = os.path.abspath(start_path)
        if os.path.isdir(start_path):
            self.__recursive_paths(start_path)
        return self.__path_list

    def __recursive_paths(self, path):
        a = sorted([f for f in os.scandir(path)], key=lambda x: x.inode())
        for f in a:
            if f.is_file():
                self.__path_list.append(f.path)
            else:
                self.__recursive_paths(f.path)
