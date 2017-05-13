"""UI Manager for controlling the program UI."""

# project imports
import Common.PluginTemplate as PluginTemplate

# plugin imports
import Plugins.UIManager.MainWindow as MainWindow


class UIManager(PluginTemplate.PluginTemplate):
    """UI Manager class for controlling the program UI."""

    def pluginQuery(self):
        """Should be loaded somewhat early."""
        return (True, 10)

    def pluginLoad(self):
        """Prepare for use."""
        self.mainWindow = MainWindow(self)
