# -*- coding: utf-8 -*-

import PyQt5.QtCore as QtCore
import sqlite3
import os


class DatabaseManager(QtCore.QObject):

    def __init__(self, main):
        super(DatabaseManager, self).__init__()
        self.main = main
        self.dbName = "Keening.db"
        self.sqlName = "database.sql"
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        self.disconnect()
        try:
            path = self.main.pathManager.makePath(self.dbName, create=True)
            self.main.log(self, 0, "connect " + str(path))
            self.connection = sqlite3.connect(path)
            self.cursor = self.connection.cursor()
            if self.isDbEmpty():
                self.parseSQL()
            self.main.log(self, 0, "connected")
        except Exception as exc:
            self.main.log(self, 1, str(exc))

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def parseSQL(self):
        if not self.cursor or not self.connection:
            self.main.log(self, 2, "no db cursor, will not parse sql")
        path = self.main.pathManager.resolveResource(self.sqlName)
        self.main.log(self, 0, "sql parsing from " + str(path))
        with open(path, encoding="UTF-8") as sql:
            comms = []
            for s in sql.read().split(";"):
                if len(s) < 1:
                    continue
                s = [x.strip() for x in s.split("\n")]
                s = " ".join(s).strip() + ";"
                comms.append(s)
            for s in comms:
                try:
                    self.cursor.execute(s)
                except Exception as exc:
                    self.main.log(self, 1, str(exc))
            self.connection.commit()
        self.main.log(self, 0, "Sql parsing complete")

    def clear(self):
        self.disconnect()
        os.unlink(self.main.pathManager.makePath(self.dbName))
        self.connect()
        self.parseSQL()

    def isDbEmpty(self):
        isEmpty = True
        try:
            self.cursor.execute("SELECT COUNT (*) FROM Mod;")
            isEmpty = self.cursor.fetchone()[0] < 1
        except Exception:
            pass
        self.main.log(self, 0, "isDbEmpty >> " + str(isEmpty))
        return isEmpty

    def setModName(self, modId, newName):
        self.setModAttribute(modId, "name", newName)

    def setModVersion(self, modId, newVersion):
        self.setModAttribute(modId, "version", newVersion)

    def setModIndex(self, modId, newIndex):
        self.setModAttribute(modId, "index", newIndex)

    def setModAttribute(self, modId, attribute, newValue):
        try:
            s = "UPDATE Mod SET {} = ? WHERE id = ?;".format(attribute)
            self.cursor.execute(s, newValue, modId)
            self.conn.commit()
        except Exception as exc:
            self.main.log(self, 1, str(exc))

    def getModAttribute(self, modName, attribute):
        try:
            s = "SELECT {} FROM Mod WHERE name = ?;".format(attribute)
            self.cursor.execute(s, modName)
            return self.cursor.fetchone()
        except Exception as exc:
            self.main.log(self, 1, str(exc))
            return None
