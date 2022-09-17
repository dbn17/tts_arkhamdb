from tts.TTSObject import TTSObject


class Board(TTSObject):

    def __init__(self, game, imageURL, scaleX=1.0, scaleY=1.0, scaleZ=1.0):
        TTSObject.__init__(self)
        self.game = game
        self.imageURL = imageURL
        self.scaleX = scaleX
        self.scaleY = scaleY
        self.scaleZ = scaleZ

    def render(self):
        template = self.game.env.get_template("tts_board.json.j2")
        return template.render(this = self)

    def getScaleX(self):
        return self.scaleX
    def getScaleY(self):
        return self.scaleY
    def getScaleZ(self):
        return self.scaleZ
