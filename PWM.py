import pigpio

from enum import Enum
from Gpio import Gpio

class PWM(Gpio):
    """Represents a PWM output pin"""

    def __init__(self, pinNumber, gpioNumber, label):
        super().__init__(pinNumber, gpioNumber, label)
        self.setDutyCycle(0)
        self.setFrequency(100)
        #initialise pin as hardware pwm
        pi = pigpio.pi()
        pi.hardware_PWM(self.getGpio(), self.getFrequency(), self.getDutyCycle())


    def setDutyCycle(self, dutyCycle):
        pi = pigpio.pi()
        if not isinstance(dutyCycle, int):
            raise TypeError("duty cycle must be an Integer.")
        if dutyCycle < 0 or dutyCycle > 100:
            raise TypeError("duty cycle must be between 0 and 100%.")
        self.dutyCycle = dutyCycle
        pi.set_PWM_dutycycle(self.getGpio(), dutyCycle)

    def setFrequency(self, frequency):
        if not isinstance(frequency, int):
            raise TypeError("frequency must be an Integer.")
        self.frequency = frequency
        set_PWM_frequency(self.getGpio(), frequency)

    def getDutyCycle(self):
        return self.dutycycle

    def getFrequency(self):
        return self.frequency

    def __repr__(self):
        return "GPIO"+str(self.gpioNumber)+"[PWM]:"+str(self.dutyCycle)+"%"