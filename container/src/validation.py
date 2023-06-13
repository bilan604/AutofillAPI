import os


def load_credentials():
    credentials = {}
    with open('.env', 'r') as f:
        for line in f.readlines():
            line = line.strip()
            if not line: continue
            lineLst = line.split("=")
            KEY = lineLst[0]
            VALUE = "".join(lineLst[1:])
            credentials[KEY] = VALUE
    return credentials