"""
Class for commonly needed configuration file management.

Using this class, a module can use a JSON file by the same name as the
module itself for storing its configuration data. The class offers the
functions to get and set values, and also to dump the file back to disk.
At application exit, configuration file is automatically dumped to disk.
"""

# Python imports
import json
import atexit
import inspect

# PyQt5 imports
import PyQt5.QtCore as QtCore


class Configuration(QtCore.QObject):
    """Configuration class."""

    def __init__(self, module):
        """Init Configuration class, supply the parent object as argument."""
        super().__init__()
        self._module = module
        self._name = module.__class__.__name__
        self._configPath = inspect.getfile(module.__class__)[:-2] + 'json'
        try:
            with open(self._configPath, 'r', encoding='utf-8') as configFile:
                self._configMap = json.loads(configFile.read())
        except Exception as exc:
            self._module.interface().log('Exception:', exc)
            self._configMap = {}
        atexit.register(self.dump)  # wite config to disk on program close

    def dump(self):
        """Dump configuration back to JSON file."""
        try:
            with open(self._configPath, 'w', encoding='utf-8') as configFile:
                json.dump(
                    self._configMap,
                    configFile,
                    indent=4,
                    sort_keys=True,
                    ensure_ascii=False
                )
        except Exception as exc:
            self._module.interface().log('Exception:', exc)

    def get(self, key, defaultReturn):
        """Fetch value from configuration dictionary.

        If the key is not found, return defaultReturn and
        write defaultReturn as new value for key to configuration."""
        try:
            return self._configMap[key]
        except Exception as exc:
            self._module.interface().log('Exception:', exc)
            self._configMap[key] = defaultReturn
            return defaultReturn

    def set(self, key, newValue):
        """Write value for key to configuration."""
        try:
            self._configMap[key] = newValue
        except Exception as exc:
            self._module.interface().log('Exception:', exc)
