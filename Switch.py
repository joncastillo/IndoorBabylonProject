import pigpio

from enum import Enum
from Gpio import Gpio


class Switch(Gpio):
    """Represents an ordinary gpio output pin"""

    e_state = Enum('state', 'Off On')

    def __init__(self, pinNumber, gpioNumber, label, engine):
        super().__init__(pinNumber,gpioNumber, label, engine)

        #initialise pin as output
        self.engine.pi.set_mode(gpioNumber, pigpio.OUTPUT)

        currentState = self.engine.pi.read(gpioNumber)
        self.state = Switch.e_state.Off if currentState == 0 else Switch.e_state.On

    def setState(self, state):
        if state != self.state:

            self.state = state
            if state == Switch.e_state.Off or state == Switch.e_state.Off.name:
                self.engine.pi.write(self.gpioNumber, 0)
            else:
                self.engine.pi.write(self.gpioNumber, 1)

            # implement on change method here
            print("Switch[" + str(self.gpioNumber) + "] changed to: " + str(state))
            message = self.engine.OnSwitchChangeMessage(self.gpioNumber, self.state)
            self.engine.postMessage(message)

    def getState(self):
        return self.state

    def setValue(self, value):
        if value == 1:
            self.setState(Switch.e_state.On)
        elif value == 0:
            self.setState(Switch.e_state.Off)
        else:
            self.setState(value)

    def __repr__(self):
        return "GPIO"+str(self.gpioNumber)+"[SW]:"+str(self.state)