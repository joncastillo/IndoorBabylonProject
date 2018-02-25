from Pin import Pin


class Gpio(Pin):
    """Representation of a Raspberry Pi Gpio"""
    def __init__(self, pinNumber, gpioNumber, label, engine):
        super().__init__(pinNumber, label, engine)
        self.setGpio(gpioNumber)
        self.threadBehavior = None

    def setGpio(self, gpioNumber):
        if not isinstance(gpioNumber, int):
            raise TypeError("gpioNumber must be an Integer.")
        self.gpioNumber = gpioNumber

    def getGpio(self):
        return self.gpioNumber

    #abstractmethod
    def setValue(self, value):
        pass