"""
Single unified module/class for managing each and every extension.

One Object to rule them all, One Object to find them,
One Object to bring them all, and in the application bind them.
"""

# Python imports
import os
import atexit
import shutil
import importlib

# PyQt5 imports
import PyQt5.QtCore as QtCore


class Interface(QtCore.QObject):
    """Interface class for extension management."""

    signalSlot = QtCore.pyqtSignal(object)

    def __init__(self, application):
        """Interface init, supply the application object as argument."""
        self._application = application
        self._appDir = os.getcwd()
        atexit.register(self.cleanup, self._appDir)

    def app(self):
        """Return the main application object."""
        return self._application

    def appDir(self):
        """Return the directory the application was run in."""
        return self._appDir

    def cleanup(self, baseDir):
        """Recursively delete all '__pycache__' folders from a tree."""
        for fp in os.scandir(baseDir):
            if fp.is_file():
                continue
            if fp.name == '__pycache__':
                shutil.rmtree(fp.path)
            else:
                self.cleanup(fp.path)

    def path(self, *pathElements):
        """Build and return a path to an item inside the app directory."""
        return os.path.normcase(os.path.normpath(os.path.abspath(os.path.join(
            self._appDir, *pathElements
        ))))

    def log(self, *args):
        """Write to common application logfile."""
        print(*args)

    def signal(self, *args):
        """Send a signal to every extension."""
        self.signalSlot.emit(*args)

    def registerSignalHandler(self, handle):
        """Register a function to receive ALL signals."""
        self.signalSlot.connect(handle)

    def registerFunction(self, funcName, handle):
        """Register function to be called by its name by other extensions."""
        self._functionMap[funcName] = handle

    def call(self, funcName, defaultReturn, *args):
        """Call a function by name, return defaultReturn if fails."""
        try:
            f = self._functionMap[funcName]
            return f(*args)
        except Exception as exc:
            self.log('Exception:', exc)
            return defaultReturn

    def loadPlugins(self):
        """Load all application extensions."""
        try:
            self._pluginList = []
            for fp in os.scandir(self.path('Plugins')):
                print(fp.path)
                if fp.is_file():
                    continue
                name = fp.name.split('.')[0]
                module = importlib.import_module(
                    'Plugins.' + name + '.' + name
                )
                plugin = getattr(module, name)(self)
                query = plugin.pluginQuery()
                if query[0]:
                    self._pluginList.append((query[1], plugin))
            print(self._pluginList)
        except Exception as exc:
            self.log('Exception:', exc)
