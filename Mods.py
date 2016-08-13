# -*- coding: utf-8 -*-

import PyQt5.QtWidgets as QtWidgets
import PyQt5.Qt as Qt
import os


class Mods(QtWidgets.QWidget):

    def __init__(self, app):
        super(Mods, self).__init__()
        self.app = app
        self.modList = Mods.ModList(self, app)

        # horisontal splitter
        self.splitter = QtWidgets.QSplitter(Qt.Qt.Horizontal, self)
        self.splitter.setStretchFactor(0, 2)
        self.splitter.setStretchFactor(1, 1)
        self.splitter.addWidget(self.modList)
        self.splitter.addWidget(QtWidgets.QWidget(self))

        # layout
        self.hbox = QtWidgets.QHBoxLayout(self)
        self.hbox.addWidget(self.splitter)
        self.setLayout(self.hbox)

    class ModList(QtWidgets.QTreeWidget):

        def __init__(self, widget, app):
            super(Mods.ModList, self).__init__(widget)
            self.app = app
            self.setRootIsDecorated(False)
            self.setAlternatingRowColors(False)
            # self.setDragEnabled(True)
            self.setAcceptDrops(True)
            self.header().setStretchLastSection(False)
            self.header().setSectionResizeMode(0, self.header().Stretch)
            self.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
            self.setHorizontalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOff)
            self.setVerticalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOn)
            self.updateDatabase()
            self.updateFromDb()
            self.sortByColumn(self.columnCount() - 1, Qt.Qt.AscendingOrder)
            self.itemChanged.connect(self.itemChangedHandler)

        def setSorting(self, enabled):
            header = self.header()
            self.setSortingEnabled(enabled)
            header.setSortIndicatorShown(enabled)
            if enabled:
                self.sortItems(header.sortIndicatorSection(), header.sortIndicatorOrder())

        def updateDatabase(self):
            path = self.app.preferences().pathMods()
            names = [e.name for e in os.scandir(path)]
            self.app.database().setMods(names)

        def updateFromDb(self):
            self.selectionModel().clearSelection()
            self.invisibleRootItem().takeChildren()
            info = self.app.database().getMods()
            self.setHeaderLabels([s for s in info["labels"] if s != "active"])
            items = [Mods.ModItem(self.app, info["labels"], i) for i in info["data"]]
            self.setSorting(False)
            self.invisibleRootItem().addChildren(items)
            self.setSorting(True)

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
            self._app = app
            self._labels = labels
            self._info = list(info)
            for i in range(0, len(self._info)):
                if self._labels[i] == "active":
                    continue
                self.setText(i, str(self._info[i]))
            self.setChecked(self.info("active"), onlyCheckbox=True)
            self.setFlags(self.flags() | Qt.Qt.ItemIsEditable)

        def info(self, label):
            return self._info[self._labels.index(label)]

        def label(self, column):
            return self._labels[column]

        def set(self, label, value):
            column = self._labels.index(label)
            self._info[column] = value
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

        def setIndex(self, index):
            if index == self.info("index"):
                return
            self._app.database().setModIndex(self.info("name"), index)
            self.treeWidget().updateFromDb()

        def setVersion(self, text):
            if text == self.info("version"):
                return
            self._app.database().setModVersion(self.info("name"), text)
            self.set("version", text)

        def setName(self, text):
            if text == self.info("name"):
                return
            self._app.database().setModName(self.info("name"), text)
            self.set("name", text)

        def setChecked(self, checked, onlyCheckbox=False):
            if checked == self.info("active") and not onlyCheckbox:
                return
            if checked:
                state = Qt.Qt.Checked
            else:
                state = Qt.Qt.Unchecked
            self.setCheckState(self._labels.index("name"), state)
            if not onlyCheckbox:
                self._app.database().setModActive(self.info("name"), checked)
                self.set("active", checked)

        def getChecked(self):
            return self.checkState(self._labels.index("name")) == Qt.Qt.Checked
