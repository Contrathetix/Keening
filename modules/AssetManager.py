import PyQt5.QtCore as QtCore


class AssetManager(QtCore.QObject):

    def __init__(self, parent=None):
        super().__init__()
        self.__parent = parent
