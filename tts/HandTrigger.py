import tts.TTSObject


class HandTrigger(tts.TTSObject):

    def __init__(self, fogColor, color, geometry):
        tts.TTSObject.__init__(self)
        self.fogColor = fogColor
        self.color = color
        self.geometry = geometry

