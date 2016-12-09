import PyQt5.QtCore as QtCore


class DataManager(QtCore.QObject):

    def __init__(self, parent=None):
        super().__init__()
        self.__parent = parent

    def set_modlist(self, new_list):
        pass

    def get_modlist(self):
        with open(os.path.join("data", "modlist.txt"), "r") as f:
            l = list(set(filter(None, f.readlines())))
            for i in range(0, len(l)):
                a = l[i].split(" ")
                l[i] = [a[0] == "++", a[1]]
            return l
        return []

    def get_pluginlist(self):
        return []
