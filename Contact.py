import pigpio
import ThreadBehavior

from enum import Enum
from Gpio import Gpio

from ThreadBehavior import ContactThreadBehaviorPersistent

class Contact(Gpio):
    """Represents an ordinary GPIO input pin"""

    e_state = Enum('state', 'Low High')

    def __init__(self, pinNumber, gpioNumber, label, engine):
        super().__init__(pinNumber,gpioNumber, label, engine)
        self.persistence = 0
        # check every 1000 milli seconds (1s)
        self.threadBehavior = ThreadBehavior.ContactThreadBehaviorPersistent(gpioNumber,self.engine,1000)

        currentState = self.engine.pi.read(gpioNumber)
        self.state = Contact.e_state.Low if currentState == 0 else Contact.e_state.High

        #initialise pin as input
        self.engine.pi.set_mode(gpioNumber, pigpio.INPUT)

    def setPersistence(self, persistence):
        self.persistence = persistence

    def getPersistence(self):
        return self.persistence

    def getState(self):
        return self.state

    def setValue(self, value):
        print("Error: There was an attempt to set contact#" + str(gpioNumber))

    def __repr__(self):
        return "GPIO"+str(self.gpioNumber)+"[CON]:"+str(self.state)
