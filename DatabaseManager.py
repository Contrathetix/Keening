# -*- coding: utf-8 -*-

import PyQt5.QtCore as QtCore
import sqlite3


class DatabaseManager(QtCore.QObject):

    def __init__(self, backend, dbPath, sqlPath):
        super(DatabaseManager, self).__init__(backend)
        self.backend = backend
        self.conn = None
        self.cursor = None
        try:
            self.conn = sqlite3.connect(dbPath)
            self.cursor = self.conn.cursor()
            self.parseSQL(sqlPath)
        except Exception as exc:
            self.backend.log(self, 1, str(exc))

    def __del__(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def parseSQL(self, filePath):
        if not self.cursor or not self.conn:
            self.backend.log(self, 2, "no db cursor, will not parse sql")
        else:
            self.backend.log(self, 0, "sql parsing from \"" + str(filePath) + "\"")
            with open(filePath, encoding="utf-8") as file:
                comms = [c.strip() for c in file.read().split(";")]
                comms[:] = [c.replace("\t", "") for c in comms if len(c) > 0]
                comms[:] = [c.replace("\n", " ") + ";" for c in comms]
                for c in comms:
                    try:
                        self.cursor.execute(c)
                    except Exception as exc:
                        self.backend.log(self, 1, str(exc))
                self.conn.commit()
            self.backend.log(self, 0, "sql parsing complete")

    def argGenerator(self, items):
        for item in items:
            if type(item) is list or type(item) is tuple:
                yield(item)
            else:
                yield([item])

    def getInstallers(self):
        output = {
            "columns": ["name", "version", "active", "index"],
            "data": []
        }
        try:
            self.cursor.execute('SELECT "name", "version", "active", "index" FROM Installers;')
            for t in self.cursor.fetchall():
                output["data"].append({
                    "name": t[0], "version": t[1], "active": t[2], "index": t[3]
                })
        except Exception as exc:
            self.backend.log(self, 1, str(exc))
        return output

    def addInstallers(self, newNames):
        self.backend.log(self, 0, "Updating installer database...")
        try:
            oldNames = []
            self.cursor.execute('SELECT "name" FROM Mod;')
            oldNames = set([t[0] for t in self.cursor.fetchall()])
            newNames = set(newNames)
            delNames = list(oldNames - newNames)
            addNames = list(newNames - oldNames)
            self.cursor.executemany(
                'DELETE FROM Mod WHERE "name" = ?;',
                self.argGenerator(delNames)
            )
            self.cursor.execute('SELECT "name", "index" FROM Mod ORDER BY "index";')
            oldNames = self.cursor.fetchall()
            oldNames = [(i, oldNames[i][0]) for i in range(0, len(oldNames))]
            self.cursor.executemany(
                'UPDATE Mod SET "index" = ? WHERE "name" = ?;',
                self.argGenerator(oldNames)
            )
            addNames = [(len(oldNames) + i, addNames[i]) for i in range(0, len(addNames))]
            self.cursor.executemany(
                'INSERT INTO Mod ("index", "name") VALUES (?, ?);',
                self.argGenerator(addNames)
            )
            self.conn.commit()
        except Exception as exc:
            self.conn.rollback()
            self.backend.log(self, 1, str(exc))
        self.backend.log(self, 0, "Installer database updated")

    def setModName(self, oldName, newName):
        try:
            self.cursor.execute(
                'UPDATE Mod SET "name" = ? WHERE "name" = ?;',
                [newName, oldName]
            )
            self.conn.commit()
        except Exception as exc:
            self.conn.rollback()
            self.backend.log(self, 1, str(exc))

    def getModIndex(self, modName):
        try:
            self.cursor.execute(
                'SELECT "index" FROM Mod WHERE "name" = ?;',
                [modName]
            )
            return self.cursor.fetchone()[0]
        except Exception as exc:
            self.backend.log(self, 1, str(exc))
            return -1

    def setModIndex(self, modName, newIndex):
        try:
            self.cursor.execute(
                "SELECT 'id' FROM Mod WHERE 'name' = ?;",
                [modName]
            )
            modId = self.cursor.fetchone()[0]
            print(modId)
            self.cursor.execute(
                "UPDATE Mod SET 'index' = ? WHERE 'id' = ?;",
                [newIndex, modId]
            )
            self.cursor.execute(
                "SELECT 'id', 'index' FROM Mod WHERE 'index' > ? AND 'id' != ?;",
                [newIndex - 1, modId]
            )
            rows = self.cursor.fetchall()
            move = [tuple(t) for t in rows]
            move[:] = [(t[0], t[1] + 1) for t in move]
            self.cursor.executemany(
                "UPDATE Mod SET 'index' = ? WHERE 'id' = ?;",
                [move]
            )
            self.conn.commit()
        except Exception as exc:
            self.conn.rollback()
            self.backend.log(self, 1, str(exc))

    def getModActive(self, modName):
        try:
            self.cursor.execute(
                'SELECT "active" FROM Mod WHERE "name" = ?;',
                [modName]
            )
            return self.cursor.fetchone()[0]
        except Exception as exc:
            self.backend.log(self, 1, str(exc))
            return False

    def setModActive(self, modName, isActive):
        try:
            self.cursor.execute(
                'UPDATE Mod SET "active" = ? WHERE "name" = ?;',
                [isActive, modName]
            )
            self.conn.commit()
        except Exception as exc:
            self.conn.rollback()
            self.backend.log(self, 1, str(exc))

    def getModVersion(self, modName):
        try:
            self.cursor.execute(
                'SELECT "version" FROM Mod WHERE "name" = ?;',
                [modName]
            )
            return self.cursor.fetchone()[0]
        except Exception as exc:
            self.backend.log(self, 1, str(exc))
            return "-"

    def setModVersion(self, modName, newVersion):
        try:
            self.cursor.execute(
                'UPDATE Mod SET "version" = ? WHERE "name" = ?;',
                [newVersion, modName]
            )
            self.conn.commit()
        except Exception as exc:
            self.conn.rollback()
            self.backend.log(self, 1, str(exc))
