"""Plugin template, every plugin should be based on this."""

# PyQt5 imports
import PyQt5.QtCore as QtCore

# project imports
import Common.Configuration as ConfigModule


class PluginTemplate(QtCore.QObject):
    """Plugin template class, base each plugin on this one."""

    def __init__(self, pluginInterface):
        """Plugin init function, leave as is."""
        self._pluginInterface = pluginInterface
        self._config = ConfigModule.Configuration(self)

    def pluginQuery(self):
        """Function used to query plugin status.

        Must return a tuple of form (bool, int) where
        bool = should the plugin be loaded or not
        int = load order for the plugin (guideline only)"""
        return (False, 999)

    def pluginLoad(self):
        """Called when the plugin is loaded by the app."""
        pass

    def config(self):
        """Get configuration object."""
        return self._config

    def interface(self):
        """Get plugin interface object."""
        return self._pluginInterface
