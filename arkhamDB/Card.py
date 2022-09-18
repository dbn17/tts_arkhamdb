import json
import urllib.request
import hashlib
import arkhamDB.CardCache

class Cards:

    def __init__(self, cardsFilename):
        self.cardsFilename = cardsFilename
        f = open(self.cardsFilename, "r")
        self.jsonData = json.load(f)
        f.close()

        self.cards = []
        for c in self.jsonData:
            self.cards.append(Card(c))

    def allCards(self):
        for c in self.cards:
            yield c

    def getCard(self, num):
        return self.cards[num]

class Card:

    def __init__(self, jsonData):
        self.jsonData = jsonData

    def __str__(self):
        #print(self.jsonData)
        if 'name' in self.jsonData.keys():
            return f"{self.jsonData['name']}"
        return f"Duplicate: {self.jsonData['duplicate_of']}"

    def getFaceURL(self):
        if "imagesrc" in self.data.keys():
            return "https://arkhamdb.com" + self.data["imagesrc"]
        else:
            return "https://i.ibb.co/4F8tjt2/0f31cbb43bc30443ab4cc8e9d03ad9fb49272cea-Back-URL.jpg"
    def getBackURL(self):
        #print(self.data)
        if "backimagesrc" in self.data.keys():
            return "https://arkhamdb.com" + self.data["backimagesrc"]
        if "encounter_code" in self.data:
            # Encounter cards
            return "https://i.ibb.co/8dR1KJB/dbddcc316fa54470001c65b002d7974eb5053053-Back-URL.jpg"
        if self.data["type_code"] in ("asset",):
            # All other get the blueish back
            return "https://i.ibb.co/4F8tjt2/0f31cbb43bc30443ab4cc8e9d03ad9fb49272cea-Back-URL.jpg"
        # Failsafe blueish back
        return "https://i.ibb.co/4F8tjt2/0f31cbb43bc30443ab4cc8e9d03ad9fb49272cea-Back-URL.jpg"

    def getGUID(self):
        h = hashlib.new("sha256")
        h.update( (self.jsonData["code"] + "_" + self.jsonData["name"]).encode("utf-8"))
        d = h.hexdigest()
        return d[0:6]

    def getName(self):
        return json.dumps(self.jsonData["name"])

    def getFaction(self):
        return self.jsonData["faction_code"]

    def getTypeCode(self):
        return self.jsonData["type_code"]

    def getEncounterCode(self):
        return self.jsonData["encounter_code"]

    def getCode(self):
        code = self.jsonData["code"]
        if code.endswith("a") or code.endswith("b"):
            code = 9999 + int(code[0:-1])
        return code

    def getQuantity(self):
        return int(self.jsonData["quantity"])

    def isDuplicationCard(self):
        if "duplicate_of" in self.jsonData.keys():
            return True
        return False

    def syncOnline(self):
        url = "https://arkhamdb.com/api/public/card/" + self.jsonData["code"]
        self.data = arkhamDB.CardCache.cache.getCard(url)
        if self.data is None:
            req = urllib.request.Request(url)
            resp = urllib.request.urlopen(req).read()
            self.data = json.loads(resp.decode('utf-8'))
            arkhamDB.CardCache.cache.addCard(url, self.data)

