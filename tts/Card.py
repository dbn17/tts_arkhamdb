from tts.TTSObject import TTSObject


class Card(TTSObject):

    def __init__(self, data):
        TTSObject.__init__(self)
        self.data = data

    def getCode(self):
        return self.data["code"]

    def getName(self):
        return self.data["name"]

    def getFaceURL(self):
        print(self.data)
        return "https://arkhamdb.com" + self.data["imagesrc"]

    def getBackURL(self):
        return "https://arkhamdb.com" + self.data["backimagesrc"]
