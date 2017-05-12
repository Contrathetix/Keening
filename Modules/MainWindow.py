# PyQt5 import
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets

# Keening imports
import Common.ConfigHandler as ConfigHandler


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.config = ConfigHandler.ConfigHandler(self)
        self.mainWidget = QtWidgets.QWidget(self)
        self.layout = QtWidgets.QVBoxLayout(self.mainWidget)
        self.tabHolder = QtWidgets.QTabWidget(self)
        self.toolBar = QtWidgets.QToolBar(self)
        self.progressBar = QtWidgets.QProgressBar(self)
        self.layout.addWidget(self.toolBar)
        self.layout.addWidget(self.tabHolder)
        self.layout.addWidget(self.progressBar)
        self.setWindowTitle(
            self.config.get('window_title', 'Keening'),
        )
        self.setWindowIcon(QtGui.QIcon(self.app.path(
            'Assets', self.config.get('window_icon', 'icon.png')
        )))
        self.resize(
            self.config.get('window_w', 800),
            self.config.get('window_h', 500)
        )
        # defaultPos = self.size()
        # defaultPos =
        self.move(
            self.config.get('window_x', 100),
            self.config.get('window_y', 100)
        )

    def closeEvent(self, event):
        currentSize = self.size()
        self.config.set('window_w', currentSize.width())
        self.config.set('window_h', currentSize.height())
        currentPos = self.pos()
        self.config.set('window_x', currentPos.x())
        self.config.set('window_y', currentPos.y())
        event.accept()

    def addTabWidget(self, newWidget, tabName):
        self.tabHolder.addTab(newWidget, tabName)

    def addToolBarWidget(self, newWidget, iconObject, toolTip):
        pass
