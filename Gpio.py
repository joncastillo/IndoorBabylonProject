from Pin import Pin


class Gpio(Pin):
    """Representation of a Raspberry Pi Gpio"""
    def __init__(self, pinNumber, gpioNumber, label):
        super().__init__(pinNumber, label)
        self.setGpio(gpioNumber)

    def setGpio(self, gpioNumber):
        if not isinstance(gpioNumber, int):
            raise TypeError("gpioNumber must be an Integer.")
        self.gpioNumber = gpioNumber

    def getGpio(self):
        return self.gpioNumber
