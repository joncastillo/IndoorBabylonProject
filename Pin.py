class Pin(object):
    """Representation of a Raspberry Pi pin"""
    def __init__(self, pinNumber, label):
        self.setPinNumber(pinNumber)
        self.setLabel(label)

    def setPinNumber(self, pinNumber):
        if not isinstance(pinNumber, int):
            raise TypeError("pinNumber must be an Integer.")
        self.pinNumber = pinNumber

    def setLabel(self, label):
        if not isinstance(label, str):
            raise TypeError("label must be a string.")
        self.label = label

    def getPinNumber(self):
        return self.pinNumber

    def getLabel(self):
        return self.label


