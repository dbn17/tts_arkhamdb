import tts.TTSObject

class HandTrigger(tts.TTSObject.TTSObject):

    def __init__(self, fogColor, color, geometry):
        tts.TTSObject.TTSObject.__init__(self)
        self.fogColor = fogColor
        self.color = color
        self.geometry = geometry

