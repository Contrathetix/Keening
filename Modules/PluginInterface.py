import os
import importlib
import PyQt5.QtCore as QtCore


class PluginInterface(QtCore.QObject):
    """Plugin intrface class for
    - communication between various plugins
    - communication between plugins and the app
    - plugin query, plugin loading and function map maintenance"""

    def __init__(self, app):
        super().__init__()
        self.app = app
        self._funcMap = {}
        self._plugins = []

    def loadPlugins(self):
        for fp in os.scandir(self.app.path('Plugins')):
            try:
                name = fp.name.split('.')[0]
                module = importlib.import_module('Plugins.' + name)
                obj = getattr(module, name)(self)
                query = obj.pluginQuery()
                if query[0]:
                    self._plugins.append(query)
            except Exception as exc:
                print('Exception:', exc)

    def registerFunction(self, name, handle):
        self._funcMap[name] = handle

    def unregisterFunction(self, name):
        try:
            self._funcMap.popitem(name)
        except Exception as exc:
            print('Exception:', exc)

    def call(self, name, defaultReturn, *args):
        try:
            f = self._funcMap[name]
            return f(*args)
        except Exception as exc:
            print('Exception:', exc)
            return defaultReturn
