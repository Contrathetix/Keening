# -*- coding: utf-8 -*-

import MiscUtilities


class ConfigManager:
    def __init__(self, main):
        self.main = main
        self.valueMap = {
            "sPathGame": "Morrowind",
            "sPathMods": "Mods",
            "iGuiWidth": 1000,
            "iGuiHeight": 600
        }
        self.initValues()

    def initValues(self):
        self.main.log([self, "info", "Reading config data from ini..."])
        tempMap = MiscUtilities.parseIni("Keening.ini", True)
        for key in tempMap.keys():
            self.valueMap[key] = tempMap[key]
        self.main.log([self, "info", "Config data reading finished"])

    def getValue(self, valueName):
        try:
            return self.valueMap[valueName]
        except Exception as exc:
            self.main.log([self, "exception", str(exc)])
            if valueName[0] is "s":
                return ""
            else:
                return 0

    def setValue(self, key, value):
        self.valueMap[key] = value

    def writeToFile(self):
        MiscUtilities.writeIni("Keening.ini", self.valueMap)
