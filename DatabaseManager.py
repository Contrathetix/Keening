# -*- coding: utf-8 -*-

import PyQt5.QtCore as QtCore
import sqlite3


class DatabaseManager(QtCore.QObject):

    def __init__(self, backend, dbPath, sqlPath):
        super(DatabaseManager, self).__init__()
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

    def parseSQL(self, path):
        if not self.cursor or not self.conn:
            self.backend.log(self, 2, "no db cursor, will not parse sql")
        self.backend.log(self, 0, "sql parsing from \"" + str(path) + "\"")
        with open(path, encoding="UTF-8") as sql:
            for s in sql.read().split(";"):
                if len(s) < 1:
                    continue
                s = [x.strip() for x in s.split("\n")]
                s = " ".join(s).strip() + ";"
                try:
                    self.cursor.execute(s)
                except Exception as exc:
                    self.backend.log(self, 1, str(exc))
            self.conn.commit()
        self.backend.log(self, 0, "Sql parsing complete")

    def getModNames(self):
        names = []
        try:
            self.cursor.execute("SELECT name FROM Mod ORDER BY ind DESC;")
            names = list(self.cursor.fetchall())
            print("mod names -->", names)
        except Exception as exc:
            self.backend.log(self, 1, str(exc))
        return names

    def getModInfo(self):
        info = {}
        try:
            self.cursor.execute("SELECT name, ind, version, active FROM Mod;")
            for m in self.cursor.fetchall():
                info[m[0]] = {"ind": m[1], "version": m[2], "active": m[3]}
        except Exception as exc:
            self.backend.log(self, 1, str(exc))
        return info

    def addNewMod(self, modName, index):
        try:
            self.cursor.execute(
                "INSERT INTO Mod (name, ind) VALUES (?, ?);", modName, index
            )
            self.conn.commit()
        except Exception as exc:
            self.conn.rollback()
            self.backend.log(self, 1, str(exc))

    def removeMods(self, modNames):
        try:
            for name in modNames:
                self.cursor.execute("DELETE FROM Mod WHERE name=?;", name)
            self.conn.commit()
        except Exception as exc:
            self.backend.log(self, 1, str(exc))

    def setModAttribute(self, modName, attribute, newValue):
        try:
            s = "UPDATE Mod SET {} = ? WHERE name = ?;".format(attribute)
            self.cursor.execute(s, newValue, modName)
            self.conn.commit()
        except Exception as exc:
            self.conn.rollback()
            self.backend.log(self, 1, str(exc))

    def getModAttribute(self, modName, attribute):
        try:
            s = "SELECT {} FROM Mod WHERE name = ?;".format(attribute)
            self.cursor.execute(s, modName)
            return self.cursor.fetchone()[0]
        except Exception as exc:
            self.conn.rollback()
            self.backend.log(self, 1, str(exc))
            return None
