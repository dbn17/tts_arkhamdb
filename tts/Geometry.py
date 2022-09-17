
class Geometry:

    def __init__(self, pos, rot, scale):
        self.pos = pos
        self.rot = rot
        self.scale = scale

    def getPosX(self):
        return self.pos[0]

    def getPosY(self):
        return self.pos[1]

    def getPosZ(self):
        return self.pos[2]

    def getRotX(self):
        return self.rot[0]

    def getRotY(self):
        return self.rot[1]

    def getRotZ(self):
        return self.rot[2]

    def getScaleX(self):
        return self.scale[0]

    def getScaleY(self):
        return self.scale[1]

    def getScaleZ(self):
        return self.scale[2]
