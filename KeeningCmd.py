# -*- coding: utf-8 -*-

import PyQt5.QtCore as QtCore


class KeeningCmd(QtCore.QObject):

    def __init__(self, app):
        super(KeeningCmd, self).__init__(app)
        self.app = app
        self.backend = app.backend
        print("-" * 40 + "\nKeening Command Line Interface\n" + "-" * 40)
        while True:
            i = input(">>> ").strip().replace("\n", "").split(" ")
            if "exit" not in i:
                self.parseInput(i)
            else:
                print("Quit...")
                break

    def info(self):
        usage = [
            "Usage:",
            "usage\t\tshow this message",
            "install [<mod>|*]\tinstall one or all mods",
            "uninstall [<mod>|*]\tuninstall one or all mods",
            "list [all|i|u]\tlist all, installed or uninstalled"
        ]
        [print(">>>\t" + s + "\n") for s in usage]

    def parseInput(self, args):
        try:
            try:
                arg = args[1]
            except Exception:
                arg = ""
            if "usage" in args:
                self.info()
            elif "list" in args:
                if arg == "all":
                    print("--all")
                elif arg == "i":
                    print("--installed")
                elif arg == "u":
                    print("--uninstalled")
            elif "install" in args:
                print("--install", arg)
            elif "uninstall" in args:
                print("--uninstall", arg)

        except Exception as exc:
            print(exc)
