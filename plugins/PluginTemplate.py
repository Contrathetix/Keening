import PyQt5.QtWidgets as QtWidgets


class PluginTemplate(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__()
        self.__parent = parent
