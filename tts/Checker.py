import tts.TTSObject


class Checker(tts.TTSObject):

    def __init__(self, game, nickName, color, geometry, locked=False, lua=[]):
        tts.TTSObject.__init__(self)
        self.game = game
        self.color = color
        self.nickName = nickName
        self.geometry = geometry
        self.locked = locked
        self.xmlUi = None
        self.luaCollector = tts.LuaCollector(lua)

    def setXmlUI(self, xmlUi):
        self.xmlUi = xmlUi

    def getXmlUi(self):
        return self.xmlUi

    def getNickName(self):
        return self.nickName

    def isLocked(self):
        return self.locked

    def getLockJson(self):
        return "true" if self.locked else "false"

    def lock(self):
        self.locked = True

    def unlock(self):
        self.locker = False

    def getLua(self):
        if self.luaCollector is None:
            return ""
        return self.luaCollector.getLua()

    def render(self):
        template = self.game.env.get_template("tts_checker.json.j2")
        return template.render(this=self)
