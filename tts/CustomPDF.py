import tts.TTSObject


class CustomPDF(tts.TTSObject):

    def __init__(self, game, filename, nickName, color, geometry, locked=False, lua=[]):
        tts.TTSObject.__init__(self, geometry)
        self.game = game
        self.filename = filename
        self.color = color
        self.nickName = nickName
        self.locked = locked
        self.xmlUi = None
        self.luaCollector = tts.LuaCollector(lua)

    def setXmlUI(self, xmlUi):
        self.xmlUi = xmlUi

    def getXmlUi(self):
        if self.xmlUi is None:
            return ""
        else:
            return self.xmlUi.render()

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

    def getFilename(self):
        return self.filename

    def render(self):
        template = self.game.env.get_template("tts_custompdf.json.j2")
        return template.render(this=self)
