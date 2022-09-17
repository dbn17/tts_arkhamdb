from tts.TTSObject import TTSObject


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
