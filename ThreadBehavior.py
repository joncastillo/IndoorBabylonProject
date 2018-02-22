from abc import ABCMeta
import pigpio
import time

class GPIOThreadBehavior(object):
    __metaclass__ = ABCMeta

    def __init__(self, gpioNumber, engine):
        pi = pigpio.pi()
        self.gpioNumber = gpioNumber
        self.engine = engine
        self.quit = False
        self.old_status = pi.read(self.gpioNumber)

    @abstractmethod
    def run(self):
        pass

class ContactThreadBehaviorPersistent(GPIOThreadBehavior):
    def __init__(self, gpioNumber, engine, persistenceRate):
        super().__init__(gpioNumber,engine)
        self.persistenceRate = persistenceRate

    def run(self):
        pi = pigpio.pi()
        while self.quit == False:
            new_status = pi.read(self.gpioNumber)
            if new_status != old_status:
                old_status = new_status
                m = self.engine.engineMessageGPIOStateChange(GPIO,new_status)
                self.engine.postMessage(m)

            time.sleep(self.persistenceRate)

    def stop(self):
        self.quit = True

