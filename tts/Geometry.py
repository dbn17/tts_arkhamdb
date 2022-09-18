
class Geometry:

    def __init__(self, pos, rot, scale):
        self.pos = pos
        self.rot = rot
        self.scale = scale

    def translate(self, offset):
        self.pos[0] += offset[0]
        self.pos[1] += offset[1]
        self.pos[2] += offset[2]

    def getPos(self):
        return self.pos

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
