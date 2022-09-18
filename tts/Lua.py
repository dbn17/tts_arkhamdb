import glob

class Lua:

    def __init__(self, globPatterns):
        self.globPatterns = globPatterns
        self.luaString = ""
        self.loadAllFiles()

    def loadAllFiles(self):
        for g in self.globPatterns:
            files = glob.glob(g)
            for file in files:
                f = open(file)
                c = f.read()
                f.close()
                c = c.replace("\n", "\\n")
                self.luaString += "\\n" + c

    def getLua(self):
        return self.luaString