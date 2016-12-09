# -*- coding: utf-8 -*-

import PyQt5.QtCore as QtCore
import sqlite3
import re


class Database(QtCore.QObject):

    def __init__(self, app):
        super(Database, self).__init__()
        self.app = app
        self.conn = None
        self.cursor = None
        try:
            self.conn = sqlite3.connect("Keening.db")
            self.cursor = self.conn.cursor()
            self.parseSQL(self.app.path().asset("database.sql"))
            self.app.log(self, 0, "db connection ready")
        except Exception as exc:
            self.app.log(self, 1, str(exc))

    def __del__(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def parseSQL(self, filePath):
        if not self.cursor or not self.conn:
            self.app.log(self, 2, "no db cursor, will not parse sql")
        else:
            self.app.log(self, 0, "sql parsing from \"" + str(filePath) + "\"")
            regex = re.compile("((.*) already exists|unique(.*))", re.IGNORECASE)
            with open(filePath, encoding='utf-8') as file:
                comms = [c.strip() for c in file.read().split(";")]
                comms[:] = [c.replace("\t", "") for c in comms if len(c) > 0]
                comms[:] = [c.replace("\n", " ") + ";" for c in comms]
                for c in comms:
                    try:
                        self.cursor.execute(c)
                    except Exception as exc:
                        if regex.match(str(exc)):
                            continue
                        self.app.log(self, 1, str(exc))
                self.conn.commit()
            self.app.log(self, 0, "sql parsing complete")

    def argGenerator(self, items):
        items = [i if type(i) in [list, tuple] else [i] for i in items]
        for item in items:
            yield(item)

    def setPreferences(self, preferences):
        try:
            self.cursor.execute('DELETE FROM Preferences;')
            items = [[str(a[0]), str(a[1])] for a in preferences.items()]
            self.cursor.executemany(
                'INSERT INTO Preferences ("key", "value") VALUES (?,?);',
                self.argGenerator(items)
            )
            self.conn.commit()
        except Exception as exc:
            self.conn.rollback()
            self.app.log(self, 1, "setPrefs, " + str(exc))

    def getPreferences(self):
        try:
            prefs = {}
            self.cursor.execute('SELECT "key", "value" FROM Preferences;')
            for item in self.cursor.fetchall():
                prefs[item[0]] = item[1]
            return prefs
        except Exception as exc:
            self.app.log(self, 1, "getPrefs, " + str(exc))
            return {}

    def setMods(self, names):
        self.setItems("Mods", names)

    def getMods(self):
        mods = {
            "labels": ["name", "version", "index", "active"],
            "data": []
        }
        try:
            self.cursor.execute('SELECT "name", "version", "index", "active" FROM Mods;')
            [mods['data'].append(i) for i in self.cursor.fetchall()]
        except Exception as exc:
            self.app.log(self, 1, "getPrefs, " + str(exc))
        return mods

    def getInstalledMods(self):
        return [m[0] for m in self.getMods()["data"] if m[3]]

    def setPlugins(self, names):
        self.setItems("Plugins", names)

    def getPlugins(self):
        pass

    def setItems(self, table, newNames):
        self.app.log(self, 0, "Updating table \"" + table + "\"...")
        try:
            self.cursor.execute('SELECT "name" FROM {};'.format(table))
            oldNames = set([t[0] for t in self.cursor.fetchall()])
            newNames = set(newNames)
            delNames = list(oldNames - newNames)
            addNames = list(newNames - oldNames)
            self.cursor.executemany(
                'DELETE FROM {} WHERE "name"=?;'.format(table),
                self.argGenerator(delNames)
            )
            self.cursor.execute(
                'SELECT "name", "index" FROM {} ORDER BY "index";'.format(table)
            )
            oldNames = self.cursor.fetchall()
            oldNames = [(i, oldNames[i][0]) for i in range(0, len(oldNames))]
            self.cursor.executemany(
                'UPDATE {} SET "index"=? WHERE "name"=?;'.format(table),
                self.argGenerator(oldNames)
            )
            addNames = [(len(oldNames) + i, addNames[i]) for i in range(0, len(addNames))]
            self.cursor.executemany(
                'INSERT INTO {} ("index","name") VALUES (?,?);'.format(table),
                self.argGenerator(addNames)
            )
            self.conn.commit()
        except Exception as exc:
            self.conn.rollback()
            self.app.log(self, 1, str(exc))
        self.app.log(self, 0, "Updated table \"" + table + "\"")

    def setModIndexes(self, names):
        self.setIndexes("Mods", names)

    def setPluginIndexes(self, names):
        self.setIndexes("Plugins", names)

    def setIndexes(self, table, names):
        self.app.log(self, 0, "Updating indexes on \"" + table + "\"...")
        try:
            self.cursor.executemany(
                'UPDATE {} SET "index"=? WHERE "name"=?;'.format(table),
                self.argGenerator(names)
            )
            self.conn.commit()
        except Exception as exc:
            self.conn.rollback()
            self.app.log(self, 1, str(exc))
        self.app.log(self, 0, "Updated indexes on \"" + table + "\"")

    def setModActive(self, name, active):
        self.setTableValue("Mods", "active", active, "name", name)

    def setPluginActive(self, name, active):
        self.setTableValue("Plugins", "active", active, "name", name)

    def setModVersion(self, name, version):
        self.setTableValue("Mods", "version", version, "name", name)

    def setModName(self, name, newName):
        if not self.app.path().renameMod(name, newName):
            print("failed to rename")
            return
        self.setTableValue("Mods", "name", newName, "name", name)

    def setModIndex(self, name, index):
        try:
            self.cursor.execute(
                'SELECT "name" FROM Mods ORDER BY "index";'
            )
            names = [t[0] for t in self.cursor.fetchall()]
            names.remove(name)
            names.insert(index, name)
            names = enumerate(names)
            self.cursor.executemany(
                'UPDATE Mods SET "index"=? WHERE "name"=?;',
                self.argGenerator(names)
            )
            self.conn.commit()
        except Exception as exc:
            self.conn.rollback()
            self.app.log(self, 1, str(exc))

    def setTableValue(self, table, column, value, rowname, rowvalue):
        """UPDATE <table> SET <column> = <value> WHERE <rowname> = <rowvalue>;"""
        try:
            self.cursor.execute(
                'UPDATE {} SET "{}"=? WHERE "{}"=?;'.format(table, column, rowname),
                [value, rowvalue]
            )
            self.conn.commit()
        except Exception as exc:
            self.conn.rollback()
            self.app.log(self, 1, str(exc))

    def getApps(self):
        try:
            self.cursor.execute(
                'SELECT "path" FROM Apps;'
            )
            return [t[0] for t in self.cursor.fetchall()]
        except Exception as exc:
            self.app.log(self, 1, str(exc))
            return []

    def setApps(self, newPaths):
        try:
            self.cursor.execute(
                'DELETE FROM Apps;'
            )
            self.cursor.executemany(
                'INSERT INTO Apps ("path") VALUES (?);',
                self.argGenerator(newPaths)
            )
            self.conn.commit()
        except Exception as exc:
            self.conn.rollback()
            self.app.log(self, 1, str(exc))
