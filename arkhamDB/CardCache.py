import json

class CardCache:

    def __init__(self):
        self.cache = {}

    def getCard(self, key):
        if key in self.cache.keys():
            return self.cache[key]
        return None

    def addCard(self, key, value):
        self.cache[key] = value

    def load(self, filename):
        try:
            f = open(filename)
            self.cache = json.load(f)
            f.close()
        except:
            print("Couldn't read cache")
            pass

    def save(self, filename):
        f = open(filename, "w")
        json.dump(self.cache, f)
        f.close()

cache = CardCache()