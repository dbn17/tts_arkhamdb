from jinja2 import Environment, PackageLoader, select_autoescape
import os.path
import tts.LuaCollector

class Game:

    def __init__(self, lua=[]):
        self.objects = []
        self.env = Environment(
            loader=PackageLoader("tts"),
            autoescape=select_autoescape()
        )
        self.table = None
        self.luaGlobPatterns = lua
        if len(lua) == 0:
            ttsPath = os.path.dirname(tts.__file__)
            self.luaGlobPatterns = [os.path.join(ttsPath, "lua", "*.lua")]
        self.luaCollector = tts.LuaCollector(self.luaGlobPatterns)
        self.luaGuids = []

    def setTable(self, table):
        self.table = table

    def addObject(self, obj):
        self.objects.append(obj)

    def render(self):
        template = self.env.get_template("tts_savegame.json.j2")
        return template.render(this=self)

    def addLuaGUID(self, varname, val):
        self.luaGuids.append({"varname": varname, "val" : val})

    def getLua(self):
        r= ""
        for g in self.luaGuids:
            r += "{varname} = \\\"{value}\\\"\\n".format(varname=g["varname"], value=g["val"])
        r += '\\n'
        r += self.luaCollector.getLua()
        return r
