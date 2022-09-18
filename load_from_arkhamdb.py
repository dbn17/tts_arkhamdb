from jinja2 import Environment, PackageLoader, select_autoescape

import arkhamDB.Cycle
import arkhamDB.CardCache
import tts

env = Environment(
    loader=PackageLoader("tts"),
    autoescape=select_autoescape()
)

def loadDeck(game, cycles, codes, encounter=False):
    deck = tts.Deck(game)
    for code in codes:
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

            #print(f"Processing: {card.getName()}")
    return deck

def loadDeckBaggy(game, cycles, codes):
    top = tts.Bag(game)

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
                        #print(card.getName())
                        deck = codeBag.getDeckByName(card.getEncounterCode())
                    else:
                        deck = codeBag.getDeckByName(card.getFaction())

                for i in range(card.getQuantity()):
                    deck.addCard(card)

                #print(f"Processing: {card.getName()}")
    return top

def getAllFactionCards(game, cycles, codes):
    deck = tts.Deck(game)
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
                if not (card.getTypeCode() in [ "location", "act", "agenda", "scenario", "story", "enemy", "investigator"]):
                    if not(card.getFaction() == "mythos"):
                       deck.addCard(card.getFaction())
    return deck

if __name__ == '__main__':

    arkhamDB.CardCache.cache.load("arkhamDBCache.json")
    cycles = arkhamDB.Cycle.Cycles("arkhamdb-json-data")
    # print(cycles)
    # for c in cycles.all():
    #     print(c)
    #     for p in c.allPacks():
    #         print(f"   {p}")
    #     if c.getCode() == "core":
    #         for p in c.allPacks():
    #             for c in p.allCards():
    #                 print(c)

    game = tts.Game(["./arkhamDB/lua/global/*.lua"])
    table = tts.Table.CustomTable(game, "mat.jpg")
    game.setTable(table)

    topBag = loadDeckBaggy(game, cycles, ["core", "tfa", "dwl", "ptc", "tic"])
    factionDeck = loadDeck(game, cycles, ["core", "tfa", "dwl", "ptc", "tic"])

    f = open("savegame.json", "w")
    game.addObject(topBag)
    game.addObject(factionDeck)

    deckBuildBoard = tts.Board(game, "mat_create_deck.jpg")
    deckBuildBoard.setGeometry(tts.Geometry([-15.0, 1.0, 5.5], [0.0, 180.0, 0.0], [0.5, 0.5, 0.5]))
    game.addObject(deckBuildBoard)

    factionPos = tts.Geometry([-6.0, 1.0, 1.0], [0.0, 180.0, 0.0], [1.0, 1.0, 1.0])
    factionPos.translate(deckBuildBoard.getGeometry().getPos())
    factionDeck.setGeometry(factionPos)

    checkerPos = tts.Geometry([4.0, 2.0, -3.0], [0.0, 0.0, 0.0], [1.0, 1.0, 1.0])
    checkerPos.translate(deckBuildBoard.getGeometry().getPos())
    checker = tts.Checker(game, "SetupButton",
                          tts.Color(1.0, 0.0, 0.0, 1.0),
                          checkerPos,
                          locked=True, lua=["./arkhamDB/lua/setup.lua"])

    checker.setXmlUI(tts.XmlUi.Button(onClick="onSetupCards",
                                      position=[0.0, 0.0, -30.0],
                                      width=600,
                                      height=200,
                                      fontsize=72,
                                      text="Set up cards"))

    game.addLuaGUID("FACTION_DECK_GUID", factionDeck.getGUID())
    game.addLuaGUID("CREATE_DECK_BOARD_GUID", deckBuildBoard.getGUID())

    game.addObject(checker)
    f.write(game.render())
    f.close()

    arkhamDB.CardCache.cache.save("arkhamDBCache.json")