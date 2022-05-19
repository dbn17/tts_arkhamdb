import json
import hashlib

from jinja2 import Environment, PackageLoader, select_autoescape

import arkhamDB.Pack
import arkhamDB.Cycle
import arkhamDB.CardCache

env = Environment(
    loader=PackageLoader("arkhamDB"),
    autoescape=select_autoescape()
)
class Deck:

    def __init__(self):
        self.cards = []

    def addCard(self, card):
        self.cards. append(card)

class Card:

    def __init__(self, data):
        self.data = data

    def getGUID(self):
        h = hashlib.new("sha256")
        h.update( (self.data["code"] + "_" + self.data["name"]).encode("utf-8"))
        d = h.hexdigest()
        return d[0:6]

    def getCode(self):
        return self.data["code"]

    def getName(self):
        return self.data["name"]

    def getFaceURL(self):
        print(self.data)
        return "https://arkhamdb.com" + self.data["imagesrc"]

    def getBackURL(self):
        return "https://arkhamdb.com" + self.data["backimagesrc"]


def loadDeck(cycles, code, encounter=False):
    deck = Deck()
    for pack in cycles.getByCode(code).packs:
        cards = pack.cards.allCards()
        if encounter:
            if pack.encounterCards is None:
                return deck
            cards = pack.encounterCards.allCards()
        for card in cards:
            card.syncOnline()
            # For now we skip replacement cards
            if card.isDuplicationCard():
                continue
            for i in range(card.getQuantity()):
                deck.addCard(card)
            print(f"Processing: {card.getName()}")
    return deck

if __name__ == '__main__':

    arkhamDB.CardCache.cache.load("arkhamDBCache.json")
    cycles = arkhamDB.Cycle.Cycles("arkhamdb-json-data")
    print(cycles)
    for c in cycles.all():
        print(c)
        for p in c.allPacks():
            print(f"   {p}")
        if c.getCode() == "core":
            for p in c.allPacks():
                for c in p.allCards():
                    print(c)

    #daisy = cycles.getByCode("core").packs[0].cards.getCard(2)
    #machete = cycles.getByCode("core").packs[0].cards.getCard(20)
    #agenda = cycles.getByCode("core").packs[0].encounterCards.getCard(2)

    #daisy.syncOnline()
    #machete.syncOnline()
    #agenda.syncOnline()

    env = Environment(
        loader=PackageLoader("arkhamDB"),
        autoescape=select_autoescape()
    )


    encounterDeck = Deck()

    coreDeck = loadDeck(cycles, "core")
    coreEncounterDeck = loadDeck(cycles, "core", encounter=True)
    tfaDeck = loadDeck(cycles, "tfa")
    tfaEncounterDeck = loadDeck(cycles, "tfa", encounter=True)
    dwlDeck = loadDeck(cycles, "dwl")
    dwlEncounterDeck = loadDeck(cycles, "dwl", encounter=True)

    #i = 0
    #for card in cycles.getByCode("core").packs[0].encounterCards.allCards():
    #    card.syncOnline()
    #    for i in range(card.getQuantity()):
    #        encounterDeck.addCard(card)
    #    print(f"Processing: {card.getName()}")
    #    #i += 1
    #    if i > 10:
    #        break

    #deck.addCard(daisy)
    #deck.addCard(machete)
    #deck.addCard(agenda)

    template = env.get_template("arkhamdb_loader.json.j2")
    f = open("new_table.json", "w")
    f.write(template.render(decks = [coreDeck, coreEncounterDeck, tfaDeck, tfaEncounterDeck, dwlDeck, dwlEncounterDeck]))
    f.close()

    arkhamDB.CardCache.cache.save("arkhamDBCache.json")