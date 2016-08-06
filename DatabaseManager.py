# -*- coding: utf-8 -*-

import sqlite3


class DatabaseManager:
    def __init__(self, a_app):
        self.app = a_app
        self.conn = None
        self.cursor = None
        try:
            path = self.app.pathManager.getPath("Keening.db")
            self.conn = sqlite3.connect(path)
            self.cursor = self.conn.cursor()
            self.parseSQL()
        except Exception as exc:
            self.app.log([self, "exception", "Init:", str(exc)])

    def parseSQL(self):
        if not self.cursor or not self.conn:
            self.app.log([self, "error", "ParseSQL:", "no db cursor, will not parse"])
        else:
            path = self.app.pathManager.getPath("resource/database.sql")
            self.app.log([self, "info", "ParseSQL:", "parsing from", str(path)])
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
                        self.app.log([self, "exception", "ParseSQL:", str(exc)])
                self.conn.commit()
            self.app.log([self, "info", "ParseSQL:", "parsing complete"])

    def setDataValue(self, valueName, newValue):
        try:
            self.cursor.execute("UPDATE Data SET value = ? WHERE name = ?;", [newValue, valueName])
            self.conn.commit()
        except Exception as exc:
            self.app.log([self, "exception", "SetDataValue:", str(exc)])

    def getDataValue(self, valueName):
        try:
            self.cursor.execute("SELECT * FROM Data WHERE name = ?;", [valueName])
            return self.cursor.fetchone()[1]
        except Exception as exc:
            self.app.log([self, "exception", "GetDataValue:", str(exc)])
            return None

    def getModInfo(self, mod):
        try:
            if mod is int:
                self.cursor.execute("SELECT * FROM Mod WHERE id = ?;", [mod])
            elif mod is str:
                self.cursor.execute("SELECT * FROM Mod WHERE name = ?;", [mod])
            else:
                self.cursor.execute("SELECT * FROM Mod;")
            return self.cursor.fetchall()
        except Exception as exc:
            self.app.log([self, "exception", "GetModInfo:", str(exc)])
            return []

    def setModInfo(self, info):
        try:
            self.cursor.execute(
                "INSERT OR REPLACE INTO Mod (name, version, size, files, ind) VALUES (?,?,?,?,?);",
                [info["name"], info["version"], info["size"], info["files"], info["ind"]]
            )
            self.conn.commit()
        except Exception as exc:
            self.app.log([self, "exception", "SetModInfo:", str(exc)])
