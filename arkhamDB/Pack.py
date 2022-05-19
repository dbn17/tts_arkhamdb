import json
import os.path
import arkhamDB.Card

class Packs:
    def __init__(self, arkhamdbBasePath):
        self.arkhamdbBasePath = arkhamdbBasePath
        f = open(os.path.join(self.arkhamdbBasePath, "packs.json"), "r")
        self.jsonData = json.load(f)
        f.close()

        self.packs = []

        for p in self.jsonData:
            self.packs.append(Pack(self.arkhamdbBasePath, p))

    def all(self):
        for p in self.packs:
            yield p

    def getPackByCode(self, code):
        for p in self.all():
            if p.getCode() == code:
                return p
        return None

    def getPacksByCycle(self, code):
        r = []
        for p in self.all():
            if p.getCycle() == code:
              r.append(p)
        return r

    def getPack(self, num):
        return self.packs[num]

class Pack:

    def __init__(self, arkhamdbBasePath, jsonData):
        self.arkhamdbBasePath = arkhamdbBasePath
        self.jsonData = jsonData

    def __str__(self):
        return f"{self.jsonData['name']} ({self.jsonData['code']})"

    def loadCards(self, basename):
        cardsFilename = os.path.join(basename, self.getFilename())
        encounterCardsFilename = os.path.join(basename, self.getEncounterFilename())
        self.cards = None
        if os.path.exists(cardsFilename):
            self.cards = arkhamDB.Card.Cards(cardsFilename)

        self.encounterCards = None
        if os.path.exists(encounterCardsFilename):
            self.encounterCards = arkhamDB.Card.Cards(encounterCardsFilename)

    def allCards(self):
        if self.cards is not None:
            for c in self.cards.allCards():
                yield c
        if self.encounterCards is not None:
            for c in self.encounterCards.allCards():
                yield c

    def getCode(self):
        return self.jsonData["code"]

    def getCycle(self):
        return self.jsonData["cycle_code"]

    def getFilename(self):
        return f"{self.getCode()}.json"

    def getEncounterFilename(self):
        return f"{self.getCode()}_encounter.json"
