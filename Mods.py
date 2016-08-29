# -*- coding: utf-8 -*-

import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui
import PyQt5.Qt as Qt
import os


class Mods(QtWidgets.QWidget):

    def __init__(self, app):
        super(Mods, self).__init__()
        self.app = app

        # widgets
        self.modList = Mods.ModList(self, app)
        self.fileList = Mods.FileList(app, ["file"])
        self.loseList = Mods.FileList(app, ["file", "source"])
        self.winList = Mods.FileList(app, ["file", "source"])

        # mod selection signal connections
        self.modList.currentItemChanged.connect(self.updateTabs)

        # right hand side tabwidget
        self.tabwidget = QtWidgets.QTabWidget(self)
        self.tabwidget.addTab(self.fileList, "all files")
        self.tabwidget.addTab(self.loseList, "conflict defeats")
        self.tabwidget.addTab(self.winList, "conflict victories")

        # update mod data and the mod list widget
        self.updateDatabase()
        self.modList.setMods(self.app.database().getMods())

        # horisontal splitter
        self.splitter = QtWidgets.QSplitter(Qt.Qt.Horizontal, self)
        self.splitter.addWidget(self.modList)
        self.splitter.addWidget(self.tabwidget)
        self.splitter.setStretchFactor(0, 4)
        self.splitter.setStretchFactor(1, 3)

        # layout
        self.vbox = QtWidgets.QVBoxLayout(self)
        self.vbox.addWidget(self.splitter)
        self.setLayout(self.vbox)

    def updateTabs(self, newItem, oldItem):
        if not newItem:
            self.fileList.setItems([])
            self.loseList.setItems([])
            self.winList.setItems([])
            for i in range(0, self.modList.topLevelItemCount()):
                self.modList.topLevelItem(i).setConflictStatus(0)
        else:
            everything = newItem.getAllFileStuff()
            self.fileList.setItems(everything["own"])
            self.loseList.setItems(everything["loses"])
            self.winList.setItems(everything["wins"])

    def updateDatabase(self):
        path = self.app.preferences().pathMods()
        names = [e.name for e in os.scandir(path)]
        self.app.database().setMods(names)

    class ModList(QtWidgets.QTreeWidget):

        def __init__(self, widget, app):
            super(Mods.ModList, self).__init__(widget)
            self.app = app
            self.setUniformRowHeights(True)
            self.setRootIsDecorated(False)
            self.setAlternatingRowColors(False)
            self.header().setStretchLastSection(False)
            self.header().setSectionResizeMode(0, self.header().Stretch)
            self.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
            self.setHorizontalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOff)
            self.setVerticalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOn)
            self.sortByColumn(self.columnCount() - 1, Qt.Qt.AscendingOrder)
            self.itemChanged.connect(self.itemChangedHandler)

        def setMods(self, info):
            self.selectionModel().clearSelection()
            self.invisibleRootItem().takeChildren()
            self.setHeaderLabels([s for s in info["labels"] if s != "active"])
            items = [Mods.ModItem(self.app, info["labels"], i) for i in info["data"]]
            self.setSorting(False)
            self.invisibleRootItem().addChildren(items)
            self.setSorting(True)

        def setSorting(self, enabled):
            header = self.header()
            self.setSortingEnabled(enabled)
            header.setSortIndicatorShown(enabled)
            if enabled:
                self.sortItems(header.sortIndicatorSection(), header.sortIndicatorOrder())

        def itemChangedHandler(self, item, column):
            item.changed(column)

        def dropEvent(self, event):
            try:
                item = self.currentItem()
                index = self.indexOfTopLevelItem(self.itemAt(self.mapFrom(self, event.pos())))
                if index > -1 and item:
                    item.setIndex(index)
                    event.acceptProposedAction()
                else:
                    raise Exception()
            except Exception:
                event.ignore()

        def sortedItems(self, column):
            items = [self.topLevelItem(i) for i in range(0, self.topLevelItemCount())]
            return sorted(items, key=lambda i: i.text(column))

    class ModItem(QtWidgets.QTreeWidgetItem):

        def __init__(self, app, labels, info):
            super(Mods.ModItem, self).__init__()
            self.app = app
            self.labels = labels
            self.data = list(info)
            for i in range(0, len(self.data)):
                if self.labels[i] == "active":
                    continue
                self.setText(i, str(self.data[i]))
            self.setChecked(self.info("active"), onlyCheckbox=True)
            self.setFlags(self.flags() | Qt.Qt.ItemIsEditable)
            self.files = self.app.path().getFiles(self.getPath(), relative=True)

        def info(self, label):
            return self.data[self.labels.index(label)]

        def label(self, column):
            return self.labels[column]

        def set(self, label, value):
            column = self.labels.index(label)
            self.data[column] = value
            self.setText(column, str(value))

        def changed(self, column):
            text = self.text(column)
            label = self.label(column)
            if label == "name":
                self.setName(text)
                self.setChecked(self.getChecked())
            elif label == "version":
                self.setVersion(text)
            elif label == "index":
                if not text.isdigit() or int(text) < 0:
                    self.setText(column, str(self.info("index")))
                else:
                    self.setIndex(int(text))

        def setIndex(self, index, force=False):
            if not force and index == self.info("index"):
                return
            if not force:
                self.app.database().setModIndex(self.info("name"), index)
                tree = self.treeWidget()
                tree.setSorting(False)
                items = tree.invisibleRootItem().takeChildren()
                items.remove(self)
                items.insert(index, self)
                for i in range(0, len(items)):
                    items[i].setIndex(i, force=True)
                tree.invisibleRootItem().addChildren(items)
                tree.setSorting(True)
            self.set("index", index)

        def setVersion(self, text):
            if text == self.info("version"):
                return
            self.app.database().setModVersion(self.info("name"), text)
            self.set("version", text)

        def setName(self, text):
            if text == self.info("name"):
                return
            self.app.database().setModName(self.info("name"), text)
            self.set("name", text)

        def setChecked(self, checked, onlyCheckbox=False):
            if checked == self.info("active") and not onlyCheckbox:
                return
            if checked:
                state = Qt.Qt.Checked
            else:
                state = Qt.Qt.Unchecked
            self.setCheckState(self.labels.index("name"), state)
            if not onlyCheckbox:
                self.app.database().setModActive(self.info("name"), checked)
                self.set("active", checked)

        def setConflictStatus(self, status):
            colour = [
                QtGui.QColor(255, 255, 255, 150),
                QtGui.QColor(153, 255, 153, 150),
                QtGui.QColor(255, 153, 153, 150)
            ][status]
            [self.setBackground(i, colour) for i in range(0, len(self.labels))]

        def getChecked(self):
            return self.checkState(self.labels.index("name")) == Qt.Qt.Checked

        def getPath(self):
            return os.path.join(self.app.preferences().pathMods(), self.info("name"))

        def relativeFiles(self):
            return sorted(self.files)

        def getAllFileStuff(self):
            tree = self.treeWidget()
            everything = {
                "own": self.files,
                "wins": [],
                "loses": []
            }
            addTo = "loses"
            for item in reversed(tree.sortedItems(self.labels.index("index"))):
                if item == self:
                    addTo = "wins"
                    continue
                if not item.info("active"):
                    item.setConflictStatus(0)
                    continue
                name = item.info("name")
                conflicts = set(item.relativeFiles()).intersection(self.files)
                count = len(conflicts)
                if count < 1:
                    item.setConflictStatus(0)
                elif addTo == "loses":
                    item.setConflictStatus(2)
                elif addTo == "wins":
                    item.setConflictStatus(1)
                [everything[addTo].append([f, name]) for f in conflicts]
            everything["wins"].sort()
            everything["loses"].sort()
            return everything

    class FileList(QtWidgets.QTreeWidget):

        def __init__(self, app, columns):
            super(Mods.FileList, self).__init__()
            self.app = app
            self.setRootIsDecorated(False)
            self.setUniformRowHeights(True)
            # self.header().setStretchLastSection(False)
            self.header().setSectionResizeMode(0, self.header().Stretch)
            self.setHorizontalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOff)
            self.setVerticalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOn)
            self.setHeaderLabels(columns)

        def setItems(self, newItems):
            self.invisibleRootItem().takeChildren()
            if len(newItems) < 1:
                return
            try:
                if type(newItems[0]) not in [list, tuple]:
                    newItems = [[i] for i in newItems]
                items = [QtWidgets.QTreeWidgetItem(i) for i in newItems]
                self.invisibleRootItem().addChildren(items)
            except Exception as exc:
                self.app.log(self, 1, str(exc))
