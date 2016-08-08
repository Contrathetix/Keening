# -*- coding: utf-8 -*-

import os
import sys
import time
import shutil
import subprocess


class SpecFile(object):

    def __init__(self, file):
        super(SpecFile, self).__init__()
        self.win_private_assemblies = False
        self.win_no_prefer_redirects = False
        self.console = False
        self.debug = False
        self.strip = False
        self.upx = True
        self.file = file
        self.name = self.file.split(".")[0]
        self.icon = ""
        self.pathex = []
        self.datas = []
        self.excludes = []

    def addExtraPath(self, path):
        self.pathex.append(path)

    def addDataPath(self, path):
        self.datas.append((path, os.path.split(path)[0]))

    def addExclude(self, path):
        self.excludes.append(path)

    def setPrivateAssemblies(self, b):
        self.win_private_assemblies = b

    def setNoPreferRedirects(self, b):
        self.win_no_prefer_redirects = b

    def setConsole(self, b):
        self.console = b

    def setDebug(self, b):
        self.debug = b

    def setName(self, name):
        self.name = name

    def setIcon(self, path):
        if "\\\\" not in path:
            path = str(path).replace("\\", "\\\\")
        self.icon = path

    def setStrip(self, b):
        self.strip = b

    def setUPX(self, b):
        self.upx = b

    def writeToFile(self):
        time.sleep(0.5)
        fileName = self.name + ".spec"
        print("Writing to file \"" + fileName + "\"...")
        lines = ["# -*- mode: python -*-\n",
                 "block_cipher = None\n",
                 "a = Analysis(['Keening.py'],",
                 "             pathex=" + str(self.pathex) + ",",
                 "             binaries=None,",
                 "             datas=" + str(self.datas) + ",",
                 "             hiddenimports=[],",
                 "             hookspath=[],",
                 "             runtime_hooks=[],",
                 "             excludes=" + str(self.excludes) + ",",
                 "             win_no_prefer_redirects=" + str(self.win_no_prefer_redirects) + ",",
                 "             win_private_assemblies=" + str(self.win_private_assemblies) + ",",
                 "             cipher=block_cipher)\n"
                 "pyz = PYZ(a.pure, a.zipped_data,",
                 "          cipher=block_cipher)\n",
                 "exe = EXE(pyz,",
                 "          a.scripts,",
                 "          a.binaries,",
                 "          a.zipfiles,",
                 "          a.datas,",
                 "          name='" + self.name + "',",
                 "          debug=" + str(self.debug) + ",",
                 "          strip=" + str(self.strip) + ",",
                 "          upx=" + str(self.upx) + ",",
                 "          console=" + str(self.console) + ",",
                 "          icon=\'" + str(self.icon) + "\' )\n"]
        with open(fileName, "w", encoding="utf-8") as file:
            for line in lines:
                file.write(line + "\n")
        time.sleep(1.0)
        print("Done.")


class PackageCreator(object):
    def __init__(self):
        super(PackageCreator, self).__init__()
        self.upxPath = None
        self.specFile = SpecFile("Keening.py")
        print("Keening Executable Package Creator")
        self.cleanup()
        # self.upxPath = "C:\\Program Files\\UPX"
        self.specFile.setUPX(False)
        self.includeResources()
        self.includePaths()
        self.specFile.writeToFile()
        self.runPyinstaller()
        time.sleep(0.5)
        print("Finished.\n")
        time.sleep(1.0)

    def includePaths(self):
        time.sleep(0.5)
        print("Adding paths to include...")
        l = ["C:\\Program Files\\Python35\\Lib\\site-packages\\PyQt5\\Qt\\bin"]
        # "C:\\Program Files (x86)\\Windows Kits\\10\\Redist\\ucrt\\DLLs\\x64",
        for p in l:
            time.sleep(0.5)
            print("\t" + p)
            self.specFile.addExtraPath(p)
        time.sleep(0.5)
        print("Done.")

    def includeResources(self):
        time.sleep(0.5)
        print("Collecting resource list...")
        self.listResources("Resource")
        self.specFile.setIcon("Resource\\icon.ico")
        time.sleep(0.5)
        print("Done.")

    def listResources(self, path):
        for f in os.scandir(path):
            if f.is_dir():
                self.listResources(f.path)
            else:
                self.specFile.addDataPath(str(f.path))

    def cleanup(self):
        time.sleep(0.5)
        print("Cleaning up old files...")
        l = ["build", "dist", "Keening.spec"]
        for f in l:
            if len(f.split(".")) < 2 and os.path.isdir(f):
                time.sleep(0.5)
                shutil.rmtree(f)
                print("\tRemoved \"" + f + "\"")
            elif os.path.isfile(f):
                time.sleep(0.5)
                os.unlink(f)
                print("\tRemoved \"" + f + "\"")
        time.sleep(0.5)
        print("Done.")

    def runPyinstaller(self):
        time.sleep(0.5)
        print("Running pyinstaller...")
        args = ["\"" + str(os.path.join(sys.prefix, "Scripts", "pyinstaller")) + "\"",
                "--onefile",
                "--ascii",
                "--noconsole",
                "--clean",
                "--noconfirm",
                "\"" + str(os.path.abspath("Keening.spec")) + "\""]
        # "--upx-dir \"" + str(self.upxPath) + "\"",
        print("\t" + " ".join(args))
        subprocess.call(" ".join(args), shell=False)
        time.sleep(0.5)
        print("Done.")


if __name__ == "__main__":
    PackageCreator()
