# -*- coding: utf-8 -*-


def parseIni(path, convertTypes=False, encoding="utf-8"):
    output = {}
    try:
        file = open(path, "r", encoding=encoding)
        lines = file.read().split("\n")
        file.close()
        for line in lines:
            try:
                s = [t.strip() for t in line.split("=")]
                if len(s[0]) < 1 or len(s[1]) < 1:
                    continue
                key = s[0]
                if convertTypes and key[0] is "f":
                        value = float(s[1])
                elif convertTypes and key[0] is "i":
                    value = int(s[1])
                else:
                    value = s[1]
                output[key] = value
            except Exception:
                pass
    except Exception:
        pass
    return output


def writeIni(path, valueMap, encoding="utf-8"):
    try:
        file = open(path, "w", encoding=encoding)
        for key in valueMap.keys():
            file.write(str(key).strip() + "=" + str(valueMap[key]).strip() + "\n")
        file.close()
    except Exception:
        pass
