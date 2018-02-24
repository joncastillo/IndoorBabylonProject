import abc
import pigpio
import time
import threading

class GPIOThreadBehavior(threading.Thread):
    __metaclass__ = abc.ABCMeta

    def __init__(self, gpioNumber, engine):
        super().__init__()
        pi = pigpio.pi()
        self.gpioNumber = gpioNumber
        self.engine = engine
        self.quit = False
        self.old_status = pi.read(self.gpioNumber)

    @abc.abstractmethod
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
            if new_status != self.old_status:
                print("Contact[" + str(self.gpioNumber) + "] changed to: " + str(new_status))
                self.old_status = new_status
                m = self.engine.OnContactChangeMessage(self.gpioNumber,new_status)
                self.engine.postMessage(m)

            time.sleep(self.persistenceRate / 1000)

    def stop(self):
        self.quit = True

