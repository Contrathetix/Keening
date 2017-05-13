"""Main application definitions."""

# PyQt5 imports
import PyQt5.QtWidgets as QtWidgets

# project imports
import Common.Configuration as ConfigModule
import Common.Interface as InterfaceModule


class Application(QtWidgets.QApplication):
    """Main application class for the tool."""

    def __init__(self, argv):
        """Init function for main application, supply sys.argv as arguments."""
        super().__init__(argv)
        self.interface().loadPlugins()
        self.crash()

    def interface(self):
        """Return the Interface object."""
        try:
            return self._interface
        except AttributeError:
            self._interface = InterfaceModule.Interface(self)
            return self._interface

    def config(self):
        """Return the configuration object for this module."""
        try:
            return self._config
        except AttributeError:
            self._config = ConfigModule.Configuration(self)
            return self._config
