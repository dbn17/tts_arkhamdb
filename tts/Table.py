import tts.Geometry
import tts.Color
import tts.HandTrigger

class CustomTable:

    def __init__(self, game, imageUrl):
        self.game = game
        self.tableType = "Table_Custom"
        self.tableUrl = imageUrl
        self.handTriggers = None
        self.createHandZones()

    def createHandZones(self):
        handTriggerSpec = {
            "Red": {"color" : tts.Color.Color(0.85, 1.0, 1.0, 0.0),
                     "geometry" : tts.Geometry.Geometry([-32.0, 1.0, -32.0], [0.0, 0.0, 0.0], [10.0, 6.0, 5.0])
                    },
            "Yellow": {"color": tts.Color.Color(0.9, 0.9, 0.2, 0.0),
                    "geometry": tts.Geometry.Geometry([-20.0, 1.0, -32.0], [0.0, 0.0, 0.0], [10.0, 6.0, 5.0])
                    },
            "Blue": {"color": tts.Color.Color(0.1, 0.5, 1.0, 0.0),
                    "geometry": tts.Geometry.Geometry([-8, 1.0, -32.0], [0.0, 0.0, 0.0], [10.0, 6.0, 5.0])
                    },
            "White": {"color": tts.Color.Color(1.0, 1.0, 1.0, 0.0),
                    "geometry": tts.Geometry.Geometry([4.0, 1.0, -32.0], [0.0, 0.0, 0.0], [10.0, 6.0, 5.0])
                    },
            "Green": {"color": tts.Color.Color(0.2, 0.7, 0.15, 0.0),
                    "geometry": tts.Geometry.Geometry([16.0, 1.0, -32.0], [0.0, 0.0, 0.0], [10.0, 6.0, 5.0])
                    },
            "Pink": {"color": tts.Color.Color(0.96, 0.43, 0.8, 0.0),
                    "geometry": tts.Geometry.Geometry([28.0, 1.0, -32.0], [0.0, 0.0, 0.0], [10.0, 6.0, 5.0])
                    },
        }

        self.handTriggers = []
        for k,v in handTriggerSpec.items():
            self.handTriggers.append(tts.HandTrigger.HandTrigger(k, v["color"], v["geometry"]))

    def getTableType(self):
        return self.tableType

    def getTableUrl(self):
        return self.tableUrl

    def getHandTriggers(self):
        return self.handTriggers

    def renderHandTrigger(self):
        template = self.game.env.get_template("tts_handtrigger.json.j2")
        return template.render(this = self)