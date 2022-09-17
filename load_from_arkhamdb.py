from jinja2 import Environment, PackageLoader, select_autoescape

import arkhamDB.Cycle
import arkhamDB.CardCache
import tts

env = Environment(
    loader=PackageLoader("tts"),
    autoescape=select_autoescape()
)

def loadDeck(game, cycles, code, encounter=False):
    deck = tts.Deck.Deck(game)
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
                        print(card.getName())
                        deck = codeBag.getDeckByName(card.getEncounterCode())
                    else:
                        deck = codeBag.getDeckByName(card.getFaction())

                for i in range(card.getQuantity()):
                    deck.addCard(card)

                print(f"Processing: {card.getName()}")
    return top


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

    table = tts.Table.CustomTable("mat.jpg")
    game = tts.Game(table)
    topBag = tts.Bag(game)

    topBag = loadDeckBaggy(game, cycles, ["core", "tfa", "dwl", "ptc", "tic"])

    f = open("savegame.json", "w")
    game.addObject(topBag)
    deckBuildBoard = tts.Board(game, "mat_create_deck.jpg", scaleX=0.5, scaleY=0.5, scaleZ=0.5)
    game.addObject(deckBuildBoard)

    f.write(game.render())
    f.close()

    arkhamDB.CardCache.cache.save("arkhamDBCache.json")