class CustomTable:

    def __init__(self, imageUrl):
        self.tableType = "Table_Custom"
        self.tableUrl = imageUrl

    def getTableType(self):
        return self.tableType

    def getTableUrl(self):
        return self.tableUrl
