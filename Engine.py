from abc import ABCMeta
import threading
import importlib
import sqlite3
import pigpio

class Engine(object):
    e_messageType = Enum('messageType', 'eOnSwitchChange eOnPwmChange eOnContactChange')

    class Message(object):
        __metaclass__ = ABCMeta

        @abstractmethod
        def __init__(self):
            self.messageType = None

    class OnSwitchChangeMessage(Message):
        def __init__(self,gpuNumber, value):
            self.gpuNumber = gpuNumber
            self.value = value
            self.messageType = Engine.OnSwitchChangeMessage

    class OnPwmChangeMessage(Message):
        def __init__(self,gpuNumber, value):
            self.gpuNumber = gpuNumber
            self.value = value
            self.messageType = Engine.eOnPwmChange

    class OnContactChangeMessage(Message):
        def __init__(self,gpuNumber, value):
            self.gpuNumber = gpuNumber
            self.value = value
            self.messageType = Engine.eOnContactChange


    cv = threading.Condition()

    def __init__(self):
        self.messageQueue = []
        self.ruleTable = {}
        self.gpioList = []
        self.gpioLabelMapping = {}


    def initialiseLists(self):
        db = sqlite3.connect("./test2.sql")
        gpio = db.execute(""" SELECT * FROM Gpio """)
        pi = pigpio.pi()

        for row in gpio:
            gpioType = row[2]
            pinNumber = row[0]
            gpioNumber = row[1]
            label = row[3]

            if gpioType == 'out':
                # create a switch
                switch = Switch(pinNumber, gpioNumber, label)
                self.gpioList.append(switch)
                self.gpioLabelMapping[label] = gpioNumber

            elif gpioType == 'in':
                # create a contact
                contact = Contact(pinNumber, gpioNumber, label)
                self.gpioList.append(contact)
                self.gpioLabelMapping[label] = gpioNumber

            elif gpioType == 'PWM':
                # create a pwm
                pwm = PWM(pinNumber, gpioNumber, label)
                self.gpioList.append(pwm)
                self.gpioLabelMapping[label] = gpioNumber

            else:
                print("Skipped pin for now")

        table = db.execute(""" SELECT * FROM Alias""")
        gpioAliasMapping = {}
        for row in table:
            alias = row[1]
            gpio = row[2]
            self.gpioAliasMapping[alias] = gpio

        self.gpioAliasMapping = {**self.gpioLabelMapping, **self.gpioAliasMapping}
        print(self.gpioList)
        print(self.gpioAliasMapping)

        db = sqlite3.connect("./rules.sql")
        gpio = db.execute(""" SELECT * FROM Rules """)


        for row in gpio:
            gpioType = row[2]
            pinNumber = row[0]
            gpioNumber = row[1]
            label = row[3]



    def processMessage(self, message):
        if not isinstance(message, engineMessage):
            raise TypeError("unrecognized message format.")

        if message.type == StateChange:
            # todo: search if rules has an onChange event for this gpio
            # todo: execute corresponding triggered rule.
            gpio = message.gpio

            if self.ruleTable[gpio] != None:
                rule = ruleTable[gpio]
                #todo dynamically import rule files and run their exec
                rule_module = importlib.import_module('rules/'+str(rule))
                rule_module.runRule()

    def run(self):
        while (1):
            cv.acquire()

            if len(messageQueue) == 0:
                cv.wait()

            message = messageQueue[0]
            del messageQueue[0]

            cv.release()
            self.processMessage(message)

    def postMessage(self, message):
        # Produce one item
        cv.acquire()
        self.messageQueue.append(message)
        cv.notify()
        cv.release()