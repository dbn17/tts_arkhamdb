import json
import hashlib

from jinja2 import Environment, PackageLoader, select_autoescape

import arkhamDB.Pack
import arkhamDB.Cycle

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

if __name__ == '__main__':

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

    daisy = cycles.getByCode("core").packs[0].cards.getCard(2)
    machete = cycles.getByCode("core").packs[0].cards.getCard(20)
    agenda = cycles.getByCode("core").packs[0].encounterCards.getCard(2)

    daisy.syncOnline()
    machete.syncOnline()
    agenda.syncOnline()

    env = Environment(
        loader=PackageLoader("arkhamDB"),
        autoescape=select_autoescape()
    )

    deck = Deck()
    encounterDeck = Deck()
    i = 0
    for card in cycles.getByCode("core").packs[0].cards.allCards():
        card.syncOnline()
        deck.addCard(card)
        print(f"Processing: {card.getName()}")
        #i += 1
        if i > 10:
            break
    i = 0
    for card in cycles.getByCode("core").packs[0].encounterCards.allCards():
        card.syncOnline()
        encounterDeck.addCard(card)
        print(f"Processing: {card.getName()}")
        #i += 1
        if i > 10:
            break

    #deck.addCard(daisy)
    #deck.addCard(machete)
    #deck.addCard(agenda)

    template = env.get_template("arkhamdb_loader.json.j2")
    f = open("new_table.json", "w")
    f.write(template.render(decks = [deck, encounterDeck]))
    f.close()