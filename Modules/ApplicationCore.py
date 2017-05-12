# Python imports
import os
import shutil
import atexit

# PyQt5 imports
import PyQt5.QtWidgets as QtWidgets

# Keening imports
import Common.ConfigHandler as ConfigHandler
import Modules.MainWindow as MainWindow
import Modules.PluginInterface as PluginInterface


class ApplicationCore(QtWidgets.QApplication):

    def __init__(self, argv):
        super().__init__(argv)
        self.appDir = os.getcwd()  # assuming this is the program directory
        atexit.register(self.cleanup, self.appDir)
        self.config = ConfigHandler.ConfigHandler(self)
        self.pluginInterface = PluginInterface.PluginInterface(self)
        self.mainWindow = MainWindow.MainWindow(self)
        self.pluginInterface.loadPlugins()
        self.mainWindow.show()

    def cleanup(self, baseDir):
        """Recursively delete all '__pycache__' folders from the tree"""
        for fp in os.scandir(baseDir):
            if fp.is_file():
                continue
            if fp.name == '__pycache__':
                shutil.rmtree(fp.path)
            else:
                self.cleanup(fp.path)

    def path(self, *pathElements):
        """Build and return the path to an item inside the 'Assets' folder"""
        return os.path.normpath(os.path.abspath(os.path.join(
            self.appDir, *pathElements
        )))
