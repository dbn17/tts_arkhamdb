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
class TTSObject(object):

    def __init__(self):
        h = hashlib.new("sha256")
        h.update(str(id(self)).encode("utf-8"))
        d = h.hexdigest()
        self.GUID = d[0:6]

    def getGUID(self):
        return self.GUID

class Deck(TTSObject):

    def __init__(self, game):
        TTSObject.__init__(self)
        self.game = game
        self.nickname = ""
        self.cards = []

    def addCard(self, card):
        self.cards. append(card)

    def render(self):
        template = self.game.env.get_template("tts_deck.json.j2")
        return template.render(this = self)

    def getNickname(self):
        return self.nickname

class Bag(TTSObject):

    def __init__(self, game):
        TTSObject.__init__(self)
        self.game = game
        self.nickname = ""
        self.objects = []

    def addObject(self, obj):
        self.objects.append(obj)

    def render(self):
        template = self.game.env.get_template("tts_bag.json.j2")
        return template.render(this = self)

    def getNickname(self):
        return self.nickname

    def getBagByName(self, name):
        for o in self.objects:
            if isinstance(o, Bag) and o.nickname == name:
                return o
        n = Bag(game)
        n.nickname = name
        self.objects.append(n)
        return n

    def getDeckByName(self, name):
        for o in self.objects:
            if isinstance(o, Deck) and o.nickname == name:
                return o
        n = Deck(game)
        n.nickname = name
        self.objects.append(n)
        return n

class Card(TTSObject):

    def __init__(self, data):
        TTSObject.__init__(self)
        self.data = data

    def getCode(self):
        return self.data["code"]

    def getName(self):
        return self.data["name"]

    def getFaceURL(self):
        print(self.data)
        return "https://arkhamdb.com" + self.data["imagesrc"]

    def getBackURL(self):
        return "https://arkhamdb.com" + self.data["backimagesrc"]

def loadDeck(game, cycles, code, encounter=False):
    deck = Deck(game)
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

def loadDeckBaggy(game, cycles, codes):
    top = Bag(game)

    for code in codes:
        for pack in cycles.getByCode(code).packs:
            cards = [c for c in pack.cards.allCards()]
            if pack.encounterCards is not None:
                cards = cards + [ c for c in pack.encounterCards.allCards()]
            for card in cards:
                card.syncOnline()
                # For now we skip replacement cards
                if card.isDuplicationCard():
                    continue

                codeBag = top.getBagByName(code)
                deck = None
                if card.getTypeCode() in [ "location", "act", "agenda", "scenario", "story", "enemy", "investigator"]:
                    deck = codeBag.getDeckByName(card.getTypeCode())
                else:
                    if card.getFaction() == "mythos":
                        print(card.getName())
                        deck = codeBag.getDeckByName(card.getEncounterCode())
                    else:
                        deck = codeBag.getDeckByName(card.getFaction())

                for i in range(card.getQuantity()):
                    deck.addCard(card)

                print(f"Processing: {card.getName()}")
    return top

class Game:

    def __init__(self):
        self.objects = []
        self.tableType = "Table_Custom"
        self.tableURL = "mat.jpg"
        self.env = Environment(
            loader=PackageLoader("arkhamDB"),
            autoescape=select_autoescape()
        )

    def addObject(self, obj):
        self.objects.append(obj)

    def render(self):
        template = self.env.get_template("tts_savegame.json.j2")
        return template.render(this = self)

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



    game = Game()
    topBag = Bag(game)

    #encounterDeck = Deck(game)

    #coreDeck = loadDeck(game, cycles, "core")
    #coreEncounterDeck = loadDeck(game, cycles, "core", encounter=True)
    #tfaDeck = loadDeck(game, cycles, "tfa")
    #tfaEncounterDeck = loadDeck(game, cycles, "tfa", encounter=True)
    #dwlDeck = loadDeck(game, cycles, "dwl")
    #dwlEncounterDeck = loadDeck(game, cycles, "dwl", encounter=True)
    ## Has problems, missing images etc.
    ##eoeDeck = loadDeck(cycles, "eoe")
    ##eoeEncounterDeck = loadDeck(cycles, "eoe", encounter=True)
    ##investigatorDeck = loadDeck(cycles, "investigator")
    #ptcDeck = loadDeck(game, cycles, "ptc")
    #ptcEncounterDeck = loadDeck(game, cycles, "ptc", encounter=True)
    #ticDeck = loadDeck(game, cycles, "tic")
    #ticEncounterDeck = loadDeck(game, cycles, "tic", encounter=True)

    topBag = loadDeckBaggy(game, cycles, ["core", "tfa", "dwl", "ptc", "tic"])
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


    f = open("new_table.json", "w")
    #for deck in [coreDeck, coreEncounterDeck, tfaDeck, tfaEncounterDeck,
    #                                 dwlDeck, dwlEncounterDeck, ptcDeck, ptcEncounterDeck,
    #                                 ticDeck, ticEncounterDeck]:
    #    topBag.addObject(deck)
    game.addObject(topBag)

    f.write(game.render())
    f.close()

    arkhamDB.CardCache.cache.save("arkhamDBCache.json")