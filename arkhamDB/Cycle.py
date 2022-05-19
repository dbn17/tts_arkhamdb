import json
import arkhamDB.Pack
import os.path

class Cycles:

    def __init__(self, arkhamdbBasePath):
        self.arkhamdbBasePath = arkhamdbBasePath
        f = open(os.path.join(self.arkhamdbBasePath, "cycles.json"), "r")
        self.jsonData = json.load(f)
        f.close()

        self.cycles = []
        for c in self.jsonData:
            self.cycles.append(Cycle(self.arkhamdbBasePath, c))

    def all(self):
        for c in self.cycles:
            yield c

    def getByCode(self, code):
        for c in self.cycles:
            if c.getCode() == code:
                return c
        return None

class Cycle:

    def __init__(self, arkhamdbBasePath, jsonData):
        self.arkhamdbBasePath = arkhamdbBasePath
        self.jsonData = jsonData
        self.packs = arkhamDB.Pack.Packs(self.arkhamdbBasePath).getPacksByCycle(self.getCode())

        for p in self.packs:
            p.loadCards(os.path.join(self.arkhamdbBasePath, "pack", self.getSubdirname()))

    def __str__(self):
        return f"{self.jsonData['name']} ({self.jsonData['code']})"

    def getCode(self):
        return self.jsonData["code"]

    def getSubdirname(self):
        s = self.jsonData["code"]
        # Inconsistent Naming
        if s == "promotional":
            return "promo"
        if s == "side_stories":
            return "side"
        return s

    def allPacks(self):
        for p in self.packs:
            yield p