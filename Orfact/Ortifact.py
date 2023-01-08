class Ortifact:
    def __init__(self, sName, sKind, iLevel, iRarity):
        self.sName = sName
        self.sKind = sKind
        self.iLevel = iLevel
        self.iRarity = iRarity

    def __str__(self):
        return self.sName + ' is a level ' + str(self.iLevel) + ' ' + self.sKind