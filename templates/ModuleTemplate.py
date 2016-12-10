import PyQt5.QtCore as QtCore


class ModuleTemplate(QtCore.QObject):

    def __init__(self, parent):
        super().__init__()
        self.__parent = parent

    def parent(self):
        return self.__parent

    def call(self, funcname, *funcargs):
        try:
            self.__parent.function_call(funcname, funcargs)
        except Exception as exc:
            print("exception:", exc)

    def method_register(self, funcname, method):
        try:
            self.__parent.function_register(funcname, method)
        except Exception as exc:
            print("exception:", exc)

    def method_unregister(self, funcname):
        try:
            self.__parent.function_unregister(funcname)
        except Exception as exc:
            print("exception:", exc)
