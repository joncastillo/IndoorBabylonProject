import pigpio

from enum import Enum
from Gpio import Gpio


class Switch(Gpio):
    """Represents an ordinary gpio output pin"""

    e_state = Enum('state', 'Off On')

    def __init__(self, pinNumber, gpioNumber, label, engine):
        super().__init__(pinNumber,gpioNumber, label, engine)
        self.state = Switch.e_state.Off

        #initialise pin as output
        self.engine.pi.set_mode(gpioNumber, pigpio.OUTPUT)

    def setState(self, state):
        if state != self.state:

            self.state = state
            if state == Switch.e_state.Off:
                self.engine.pi.write(self.gpioNumber, 0)
            else:
                self.engine.pi.write(self.gpioNumber, 1)

            # implement on change method here
            print("Switch[" + str(self.gpioNumber) + "] changed to: " + str(state))
            message = self.engine.OnSwitchChangeMessage(self.gpioNumber, self.state)
            self.engine.postMessage(message)

    def getState(self):
        return self.state

    def __repr__(self):
        return "GPIO"+str(self.gpioNumber)+"[SW]:"+str(self.state)