from tts.Deck import Deck
from tts.TTSObject import TTSObject


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
        n = Bag(self.game)
        n.nickname = name
        self.objects.append(n)
        return n

    def getDeckByName(self, name):
        for o in self.objects:
            if isinstance(o, Deck) and o.nickname == name:
                return o
        n = Deck(self.game)
        n.nickname = name
        self.objects.append(n)
        return n
