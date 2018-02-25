from rules.Rule import Rule
import time

class RuleWater(Rule):
    def __init__(self, engine):
        super().__init__(engine)

    def start(self):
        print ("TEST: triggered water")
        #todo: use engine's messaging system.
        message = self.engine.SetGpioValueMessage("PRIME_THE_PUMP", 1)
        self.engine.postMessage(message)
        time.sleep(1)
        message = self.engine.SetGpioValueMessage("MIST_OVERHEAD", 1)
        self.engine.postMessage(message)
        time.sleep(5)
        message = self.engine.SetGpioValueMessage("MIST_OVERHEAD", 0)
        self.engine.postMessage(message)
        message = self.engine.SetGpioValueMessage("PRIME_THE_PUMP", 0)
        self.engine.postMessage(message)
