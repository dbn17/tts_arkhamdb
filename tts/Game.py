from jinja2 import Environment, PackageLoader, select_autoescape
import os.path
import tts.Lua

class Game:

    def __init__(self, luaGlobPatterns=None):
        self.objects = []
        self.env = Environment(
            loader=PackageLoader("tts"),
            autoescape=select_autoescape()
        )
        self.table = None
        self.luaGlobPatterns = luaGlobPatterns
        if luaGlobPatterns is None:
            ttsPath = os.path.dirname(tts.__file__)
            self.luaGlobPatterns = [os.path.join(ttsPath, "lua", "*.lua")]
        self.lua = tts.Lua.Lua(self.luaGlobPatterns)

    def setTable(self, table):
        self.table = table

    def addObject(self, obj):
        self.objects.append(obj)

    def render(self):
        template = self.env.get_template("tts_savegame.json.j2")
        return template.render(this=self)

    def getLua(self):
        return self.lua.getLua()
