# Python includes
import json
import atexit
import inspect

# PyQt5 imports
import PyQt5.QtCore as QtCore


class ConfigHandler(QtCore.QObject):
    """Multipurpose JSON module for providing configuration
    file management for arbitrary modules/classes. The name
    of the configuration file will be the name of the class"""

    def __init__(self, module):
        super().__init__()
        self._module = module
        self._name = module.__class__.__name__
        self._configPath = inspect.getfile(module.__class__)[:-2] + 'json'
        try:
            with open(self._configPath, 'r', encoding='utf-8') as configFile:
                self._configMap = json.loads(configFile.read())
        except Exception as exc:
            print('Exception:', exc)
            self._configMap = {}
        atexit.register(self.dump)  # wite config to disk on program close

    def dump(self):
        """Dump configuration dictionary back to the file in JSON form"""
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
            print('Exception:', exc)

    def get(self, key, defaultReturn):
        """Fetch value from configuration dictionary, if the key is not found,
        return defaultReturn and write defaultReturn as new value to key"""
        try:
            return self._configMap[key]
        except Exception as exc:
            print('Exception:', exc)
            self._configMap[key] = defaultReturn
            return defaultReturn

    def set(self, key, newValue):
        """Write value to configuration dictionary"""
        try:
            self._configMap[key] = newValue
        except Exception as exc:
            print('Exception:', exc)
