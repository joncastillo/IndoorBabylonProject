import pigpio

from enum import Enum
from Gpio import Gpio


class Switch(Gpio):
    """Represents an ordinary gpio output pin"""

    e_state = Enum('state', 'Off On')

    def __init__(self, pinNumber, gpioNumber, label):
        super().__init__(pinNumber,gpioNumber, label)
        self.setState(Switch.e_state.Off)

        #initialise pin as output
        pi = pigpio.pi()
        pi.set_mode(self.getGpio(), pigpio.OUTPUT)

    def setState(self, state):
        pi = pigpio.pi()
        if state != self.state:
            self.state = state
            pi.write(self.gpioNumber, state)
            # implement on change method here
            message = self.engine.OnSwitchChangeMessage(self.gpioNumber, state)

            self.engine.postMessage()

    def setNotificationBehavior(self, notificationBehavior):
        if not isinstance(notificationBehavior, NotifyBehavior):
            raise TypeError("notificationBehavior must be derived from NotifyBehavior.")
        self.notificationBehavior = notificationBehavior

    def getState(self):
        return self.state

    def __repr__(self):
        return "GPIO"+str(self.gpioNumber)+"[SW]:"+str(self.state)