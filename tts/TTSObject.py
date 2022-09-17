import hashlib


class TTSObject(object):

    def __init__(self):
        h = hashlib.new("sha256")
        h.update(str(id(self)).encode("utf-8"))
        d = h.hexdigest()
        self.GUID = d[0:6]

    def getGUID(self):
        return self.GUID
