import pigpio

from enum import Enum
from Gpio import Gpio

class PWM(Gpio):
    """Represents a PWM output pin"""

    def __init__(self, pinNumber, gpioNumber, label, engine):
        super().__init__(pinNumber, gpioNumber, label, engine)
        self.dutyCycle = 0
        self.frequency = 100
        #initialise pin as hardware pwm
        self.engine.pi.hardware_PWM(self.getGpio(), self.getFrequency(), 1000000)


    def setDutyCycle(self, dutyCycle):
        if not isinstance(dutyCycle, int):
            raise TypeError("duty cycle must be an Integer.")
        if dutyCycle < 0 or dutyCycle > 100:
            raise TypeError("duty cycle must be between 0 and 100%.")
        self.dutyCycle = dutyCycle
        setting = int((1 - (float(dutyCycle) / 100)) * 255)
        self.engine.pi.set_PWM_dutycycle(self.getGpio(), setting)

    def setFrequency(self, frequency):
        pi = pigpio.pi()
        if not isinstance(frequency, int):
            raise TypeError("frequency must be an Integer.")
        self.frequency = frequency
        pi.set_PWM_frequency(self.getGpio(), frequency)

    def getDutyCycle(self):
        return self.dutyCycle

    def getFrequency(self):
        return self.frequency

    def setValue(self, value):
        self.setDutyCycle(value)

    def __repr__(self):
        return "GPIO"+str(self.gpioNumber)+"[PWM]:"+str(self.dutyCycle)+"%"