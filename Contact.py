import pigpio
import ThreadBehavior

from enum import Enum
from Gpio import Gpio

from ThreadBehavior import ContactThreadBehaviorPersistent

class Contact(Gpio):
    """Represents an ordinary GPIO input pin"""

    e_state = Enum('state', 'High Low')
    threadBehavior = None

    def __init__(self, pinNumber, gpioNumber, label):
        super().__init__(pinNumber,gpioNumber, label)
        self.setPersistence(0)
        self.threadBehavior = ThreadBehavior.ContactThreadBehaviorPersistent

        #initialise pin as input
        pi = pigpio.pi()
        pi.set_mode(self.getGpio(), pigpio.INPUT)ß


    def getState(self):
        return self.state

    def __repr__(self):
        return "GPIO"+str(self.gpioNumber)+"[CON]:"+str(self.state)
