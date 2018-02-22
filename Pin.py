class Pin(object):
    """Representation of a Raspberry Pi pin"""
    def __init__(self, pinNumber, label):
        self.setPinNumber(pinNumber)
        self.setLabel(label)

    #@classmethod
    def setPinNumber(self, pinNumber):
        if not isinstance(pinNumber, int):
            raise TypeError("pinNumber must be an Integer.")
        self.pinNumber = pinNumber

    #@classmethod
    def setLabel(self, label):
        if not isinstance(label, str):
            raise TypeError("label must be a string.")
        self.label = label

    #@classmethod
    def getPinNumber(self):
        return self.pinNumber

    #@classmethod
    def getLabel(self):
        return self.label


