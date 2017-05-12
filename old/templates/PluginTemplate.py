import PyQt5.QtWidgets as QtWidgets


class PluginTemplate(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__()
        self.__parent = parent
        self.init_layout()
        self.__parent.widget_register(self)

    def init_layout(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(QtWidgets.QLabel("DEFAULT"))

    def widget_type(self):
        return "tab"
