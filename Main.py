# -*- coding: utf-8 -*-

import PyQt5.Qt as Qt
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets

import ResourceManager
import ConfigManager
import PathManager
import ModManager

import datetime
import time
import sys


class Main(QtWidgets.QMainWindow):
    def __init__(self, app, parent=None):
        QtWidgets.QMainWindow.__init__(self)
        self.app = app
        self.app.setStyle("fusion")
        self.logList = []
        self.splash = QtWidgets.QSplashScreen(QtGui.QPixmap("resource/splash.png"))
        self.splash.show()
        self.pathManager = PathManager.PathManager(self)
        self.configManager = ConfigManager.ConfigManager(self)
        self.pathManager.initPaths()
        self.modManager = ModManager.ModManager(self)
        self.modManager.collectModInfo()
        self.resourceManager = ResourceManager.ResourceManager(self)
        time.sleep(4)
        self.initUI()
        self.splash.close()
        self.show()

    def initUI(self):
        self.resize(self.configManager.getValue("iGuiWidth"), self.configManager.getValue("iGuiHeight"))
        layout = QtWidgets.QGridLayout()
        self.mainTabWidget = self.MainTabWidget(self)
        self.progressBar = QtWidgets.QProgressBar(self)
        self.setProgress(1, 2)
        layout.addWidget(self.mainTabWidget, 0, 0)
        layout.addWidget(self.progressBar, 1, 0)
        layoutWidget = QtWidgets.QWidget()
        layoutWidget.setLayout(layout)
        self.setCentralWidget(layoutWidget)
        self.setWindowTitle("Keening")
        self.setWindowIcon(QtGui.QIcon("resource/icon.png"))

    def closeEvent(self, event):
        try:
            self.configManager.writeToFile()
        except Exception:
            pass
        event.accept()

    def processAppEvents(self):
        self.app.processEvents()

    def log(self, argv):
        """Usage: [<class>, <message type>, <message>]"""
        try:
            self.mainTabWidget.log(argv)
        except Exception:
            self.logList.append(argv)

    def setProgress(self, maxProgress, currentProgress):
        try:
            self.progressBar.setMaximum(maxProgress)
            self.progressBar.setValue(currentProgress)
            if (currentProgress >= maxProgress):
                self.progressBar.setDisabled(True)
        except Exception:
            pass

    class MainTabWidget(QtWidgets.QTabWidget):
        def __init__(self, parent):
            super(parent.MainTabWidget, self).__init__(parent)
            self.parent = parent
            self.tabInstallersUI()
            self.tabPluginsUI()
            self.tabPreferencesUI()
            self.tabLogUI()
            self.currentChanged.connect(self.onTabChanged)

        def onTabChanged(self):
            if self.currentWidget() is self.tabInstallers:
                self.installerModList.updateContents()
            elif self.currentWidget() is self.tabPreferences:
                self.loadPreferences()

        def log(self, msg):
            log = self.logWidget
            msg = [datetime.datetime.now().strftime("%Y-%m-%d %H:%m:%S"),
                   msg[1],
                   msg[0].__class__.__name__,
                   " ".join(msg[2:])
                   ]
            log.addTopLevelItem(QtWidgets.QTreeWidgetItem(msg))
            [log.resizeColumnToContents(i) for i in range(0, 4)]
            [log.setColumnWidth(i, log.columnWidth(i) + 20) for i in range(0, 3)]

        def applyPreferences(self):
            self.log([self, "info", "Saving preferences..."])
            try:
                text = self.txtPathMods.text()
                if len(text) > 1:
                    self.parent.pathManager.setPathMods(text)
                text = self.txtPathGame.text()
                if len(text) > 1:
                    self.parent.pathManager.setPathGame(text)
                self.log([self, "info", "Preferences saved"])
            except Exception as exc:
                self.log([self, "exception", str(exc)])

        def loadPreferences(self):
            try:
                self.txtPathGame.setText(self.parent.pathManager.getPathGame())
                self.txtPathMods.setText(self.parent.pathManager.getPathMods())
            except Exception as exc:
                self.log([self, "exception", str(exc)])

        def tabLogUI(self):
            self.tabLog = QtWidgets.QWidget()
            grid = QtWidgets.QGridLayout()
            self.logWidget = QtWidgets.QTreeWidget()
            self.logWidget.setRootIsDecorated(False)
            self.logWidget.setAlternatingRowColors(True)
            self.logWidget.setHeaderLabels(["time", "type", "module", "message"])
            [self.log(msg) for msg in self.parent.logList]
            grid.addWidget(self.logWidget, 0, 0, 1, 1)
            self.tabLog.setLayout(grid)
            self.addTab(self.tabLog, "Logview")

        def tabPreferencesUI(self):
            self.tabPreferences = QtWidgets.QWidget()
            grid = QtWidgets.QGridLayout()
            self.txtPathGame = QtWidgets.QLineEdit()
            self.txtPathMods = QtWidgets.QLineEdit()
            self.btnApply = QtWidgets.QPushButton("Apply")
            self.btnApply.clicked.connect(self.applyPreferences)
            grid.addWidget(QtWidgets.QLabel("Path Definitions"), 0, 0, 1, 1)
            grid.addWidget(QtWidgets.QLabel("Game"), 1, 0, 1, 1)
            grid.addWidget(self.txtPathGame, 1, 1, 1, 1)
            grid.addWidget(QtWidgets.QLabel("Mods"), 2, 0, 1, 1)
            grid.addWidget(self.txtPathMods, 2, 1, 1, 1)
            grid.addWidget(self.btnApply, 10, 1, 1, 2)
            self.tabPreferences.setLayout(grid)
            self.addTab(self.tabPreferences, "Preferences")

        def tabPluginsUI(self):
            self.tabPlugins = QtWidgets.QWidget()
            grid = QtWidgets.QGridLayout()
            grid.addWidget(QtWidgets.QLineEdit(), 0, 1)
            grid.addWidget(QtWidgets.QLineEdit(), 1, 1)

            model = QtGui.QStandardItemModel()

            for k in range(0, 10):
                parentItem = model.invisibleRootItem()
                item = QtGui.QStandardItem("rivi {}".format(k))
                parentItem.appendRow(item)

            view = QtWidgets.QTreeView()
            view.setModel(model)
            view.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
            grid.addWidget(view, 0, 0, 2, 1)
            self.tabPlugins.setLayout(grid)
            self.addTab(self.tabPlugins, "Load Order")

        def tabInstallersUI(self):
            self.tabInstallers = QtWidgets.QWidget()

            # main installer list with mods
            self.installerModList = self.parent.InstallerListWidget(self.parent)

            # subpackage selector
            packageSelector = QtWidgets.QListWidget()
            packageSelector.setAlternatingRowColors(True)

            # conflict lists
            self.installerConflictWin = QtWidgets.QTreeWidget()
            self.installerConflictWin.setAlternatingRowColors(True)
            self.installerConflictWin.setRootIsDecorated(False)
            self.installerConflictWin.setHeaderLabels(["origin", "file"])
            self.installerConflictLose = QtWidgets.QTreeWidget()
            self.installerConflictLose.setAlternatingRowColors(True)
            self.installerConflictLose.setRootIsDecorated(False)
            self.installerConflictLose.setHeaderLabels(["origin", "file"])

            # mod info stuff
            modNameEntry = QtWidgets.QLineEdit()
            modVersionEntry = QtWidgets.QLineEdit()

            # connect the side panel info entries to the main mod list widget
            self.installerModList.itemSelectionChanged.connect(
                lambda: self.installerModList.onSelectionChanged(modNameEntry, modVersionEntry, packageSelector)
            )

            # tab widget for single mod subpackage+conflict
            tabWidget = QtWidgets.QTabWidget()

            # tab for subpackage selection
            tabPackages = QtWidgets.QWidget()
            layout = QtWidgets.QGridLayout()
            layout.setContentsMargins(2, 2, 2, 2)
            layout.addWidget(packageSelector)
            tabPackages.setLayout(layout)
            tabWidget.addTab(tabPackages, "Subpackages")

            # tab for conflict defeat detection
            tabConflictLose = QtWidgets.QWidget()
            layout = QtWidgets.QGridLayout()
            layout.setContentsMargins(2, 2, 2, 2)
            layout.addWidget(self.installerConflictLose)
            tabConflictLose.setLayout(layout)
            tabWidget.addTab(tabConflictLose, "Overwritten")

            # tab for conflict victory detection
            tabConflictWin = QtWidgets.QWidget()
            layout = QtWidgets.QGridLayout()
            layout.setContentsMargins(2, 2, 2, 2)
            layout.addWidget(self.installerConflictWin)
            tabConflictWin.setLayout(layout)
            tabWidget.addTab(tabConflictWin, "Overwrites")

            # add the widgets to layout - with QSplitter for resize
            grid = QtWidgets.QGridLayout()
            grid.addWidget(modNameEntry, 0, 0, 1, 2)
            grid.addWidget(modVersionEntry, 1, 0, 1, 1)
            grid.addWidget(tabWidget, 2, 0, 1, 2)
            grid.setContentsMargins(0, 0, 0, 0)
            widget = QtWidgets.QWidget()
            widget.setLayout(grid)
            splitter = QtWidgets.QSplitter(self.tabInstallers)
            splitter.addWidget(self.installerModList)
            splitter.addWidget(widget)
            splitter.setContentsMargins(0, 0, 0, 0)
            splitter.setStretchFactor(0, 2)
            splitter.setStretchFactor(1, 1)
            hbox = QtWidgets.QHBoxLayout()
            hbox.addWidget(splitter)
            self.tabInstallers.setLayout(hbox)
            self.addTab(self.tabInstallers, "Installers")

    class InstallerListWidget(QtWidgets.QTreeWidget):
        def __init__(self, parent):
            QtWidgets.QTreeWidget.__init__(self, parent)
            self.parent = parent
            self.setRootIsDecorated(False)
            self.setAlternatingRowColors(True)
            # self.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
            self.setHeaderLabels(self.parent.modManager.getModInfoHeaders())
            self.setDragEnabled(True)

        def getColumnIndex(self, label):
            ind = -1
            header = self.headerItem()
            for i in range(0, header.columnCount()):
                if header.text(i) == label:
                    ind = i
                    break
            return ind

        def getModName(self):
            try:
                name = self.currentItem().text(self.getColumnIndex("Name"))
                return name
            except Exception as exc:
                self.parent.log([self, "exception", str(exc)])
                return ""

        def getModVersion(self):
            try:
                return self.currentItem().text(self.getColumnIndex("Version"))
            except Exception as exc:
                self.parent.log([self, "exception", str(exc)])
                return ""

        def setModName(self, newName):
            oldName = self.getModName()
            self.parent.modManager.setModName(oldName, newName)
            self.currentItem().setText(self.getColumnIndex("name"), newName)

        def setModVersion(self, newVersion):
            modName = self.getModName()
            self.parent.modManager.setModVersion(modName, newVersion)
            self.currentItem().setText(self.getColumnIndex("version"), newVersion)

        def onSelectionChanged(self, nameEntry, versionEntry, packageSelector):
            self.applySidePanelInfo(nameEntry, versionEntry, packageSelector)
            self.updateSidePanelInfo(nameEntry, versionEntry, packageSelector)

        def updateSidePanelInfo(self, nameEntry, versionEntry, packageSelector):
            try:
                modName = self.getModName()
                nameEntry.setText(modName)
                versionEntry.setText(self.getModVersion())
                packageSelector.clear()
                subPackages = self.parent.modManager.getModSubPackages(modName)
                itemList = []
                for s in sorted(subPackages.keys()):
                    item = QtWidgets.QListWidgetItem(s)
                    item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
                    if subPackages[s]:
                        item.setCheckState(Qt.Qt.Checked)
                    else:
                        item.setCheckState(Qt.Qt.Unchecked)
                    itemList.append(item)
                packageSelector.addItems(itemList)
            except Exception as exc:
                self.parent.log([self, "exception", str(exc)])

        def applySidePanelInfo(self, nameEntry, versionEntry, packageSelector):
            try:
                oldName = self.getModName()
                oldVersion = self.getModVersion()
                newName = nameEntry.text()
                newVersion = versionEntry.text()
                print("----------------")
                print("name: " + oldName + " --> " + newName)
                print("version: " + oldVersion + " --> " + newVersion)
                if len(newName) > 0 and newName != oldName:
                    print("update name")
                    self.setModName(newName)
                if len(newVersion) > 0 and newVersion != oldVersion:
                    print("update version")
                    self.setModVersion(newVersion)
                print("----------------")
            except Exception as exc:
                self.parent.log([self, "exception", str(exc)])

        def updateContents(self):
            self.clear()
            self.parent.log([self, "info", "Updating installer list"])
            columnCount = self.headerItem().columnCount()
            itemList = []
            for modInfo in self.parent.modManager.getModInfo(False):
                item = QtWidgets.QTreeWidgetItem(
                    [modInfo["name"], modInfo["version"], modInfo["size"], modInfo["fileCount"]]
                )
                if modInfo["installed"]:
                    # item.setIcon(0, QtGui.QIcon("resource/mod_a.png"))
                    item.setCheckState(0, Qt.Qt.Checked)
                    c = [204, 255, 204]
                else:
                    # item.setIcon(0, QtGui.QIcon("resource/mod_b.png"))
                    item.setCheckState(0, Qt.Qt.Unchecked)
                    c = [255, 204, 204]
                for i in range(0, columnCount):
                    item.setBackground(i, QtGui.QColor(c[0], c[1], c[2]))
                item.setFlags(
                    item.flags() | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled
                )
                itemList.append(item)
            self.addTopLevelItems(itemList)
            [self.resizeColumnToContents(i) for i in range(0, columnCount)]
            [self.header().resizeSection(i, self.header().sectionSize(i) + 50) for i in range(0, columnCount - 1)]
            # self.header().setResizeMode(QtWidgets.QHeaderView.ResizeToContents)
            # self.header().setStretchLastSection(True)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Main(app)
    sys.exit(app.exec_())
