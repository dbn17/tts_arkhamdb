import hashlib
from copy import deepcopy

import tts

class TTSObject(object):

    def __init__(self, geometry=None):
        h = hashlib.new("sha256")
        h.update(str(id(self)).encode("utf-8"))
        d = h.hexdigest()
        self.GUID = d[0:6]
        if geometry is None:
            self.geometry = tts.Geometry([0.0, 0.0, 0.0], [0.0, 180.0, 0.0], [1.0, 1.0, 1.0])
        else:
            self.geometry = geometry
    def getGUID(self):
        return self.GUID

    def setGeometry(self, geometry):
        self.geometry = geometry

    def getGeometry(self):
        return deepcopy(self.geometry)
