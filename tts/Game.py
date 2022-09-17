from jinja2 import Environment, PackageLoader, select_autoescape


class Game:

    def __init__(self, table):
        self.objects = []
        self.table = table
        self.env = Environment(
            loader=PackageLoader("tts"),
            autoescape=select_autoescape()
        )

    def addObject(self, obj):
        self.objects.append(obj)

    def render(self):
        template = self.env.get_template("tts_savegame.json.j2")
        return template.render(this = self)
