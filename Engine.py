import abc
from enum import Enum

import threading
import importlib
import sqlite3
import pigpio

from Switch import Switch
from Contact import Contact
from PWM import PWM

class Engine(threading.Thread):
    e_messageType = Enum('messageType', 'eOnSwitchChange eOnPwmChange eOnContactChange')


    class Message(object):
        __metaclass__ = abc.ABCMeta

        @abc.abstractmethod
        def __init__(self):
            self.messageType = None

    class OnSwitchChangeMessage(Message):
        def __init__(self,gpuNumber, value):
            self.gpioNumber = gpuNumber
            self.value = value
            self.messageType = Engine.e_messageType.eOnSwitchChange

    class OnPwmChangeMessage(Message):
        def __init__(self,gpuNumber, value):
            self.gpioNumber = gpuNumber
            self.value = value
            self.messageType = Engine.e_messageType.eOnPwmChange

    class OnContactChangeMessage(Message):
        def __init__(self,gpuNumber, value):
            self.gpioNumber = gpuNumber
            self.value = value
            self.messageType = Engine.e_messageType.eOnContactChange

    def __init__(self):
        super().__init__()
        self.messageQueue = []
        self.ruleTable = {}
        self.gpioList = []
        self.gpioLabelMapping = {}
        self.ruleTableCronType = {}
        self.ruleTableSwitchType = {}
        self.ruleTablePWMType= {}
        self.cv = threading.Condition()
        self.pi = pigpio.pi()

        self.initialiseLists()

    def initialiseLists(self):
        db = sqlite3.connect("./test2.sql")
        gpio = db.execute(""" SELECT * FROM Gpio """)

        for row in gpio:
            gpioType = row[2]
            pinNumber = row[0]
            gpioNumber = row[1]
            label = row[3]

            if gpioType == 'out':
                # create a switch
                switch = Switch(pinNumber, gpioNumber, label, self)
                self.gpioList.append(switch)
                self.gpioLabelMapping[label] = gpioNumber

            elif gpioType == 'in':
                # create a contact
                contact = Contact(pinNumber, gpioNumber, label, self)
                self.gpioList.append(contact)
                self.gpioLabelMapping[label] = gpioNumber

            elif gpioType == 'PWM':
                # create a pwm
                pwm = PWM(pinNumber, gpioNumber, label, self)
                self.gpioList.append(pwm)
                self.gpioLabelMapping[label] = gpioNumber

            else:
                print("Skipped pin for now")

        for gpio in self.gpioList:
            if gpio.threadBehavior != None:
                gpio.threadBehavior.start()

        table = db.execute(""" SELECT * FROM Alias""")
        self.gpioAliasMapping = {}
        for row in table:
            alias = row[1]
            gpio = row[2]
            self.gpioAliasMapping[alias] = gpio

        self.gpioAliasMapping = {**self.gpioLabelMapping, **self.gpioAliasMapping}
        print(self.gpioList)
        print(self.gpioAliasMapping)

        db = sqlite3.connect("./test2.sql")

        rules = db.execute(""" SELECT * FROM Rules """)

        for row in rules:
            ruleType = row[0]
            ruleTrigger = row[1]
            ruleCondition = row[2]
            ruleScript = row[3]

            if ruleType == Engine.eOnSwitchChangeMessage:
                if self.ruleTableSwitchType[ruleTrigger] == None:
                    self.ruleTableSwitchType[ruleTrigger] = []
                self.ruleTableSwitchType[ruleTrigger].append({ruleCondition, ruleScript})

            elif ruleType == Engine.eOnPwmChange:
                if self.ruleTablePWMType[ruleTrigger] == None:
                    self.ruleTablePWMType[ruleTrigger] = []
                self.ruleTablePWMType[ruleTrigger].append({ruleCondition, ruleScript})

            elif ruleType == Engine.eOnContactChange:
                if self.ruleTableContactType[ruleTrigger] == None:
                    self.ruleTableContactType[ruleTrigger] = []
                self.ruleTableContactType[ruleTrigger].append({ruleCondition, ruleScript})


    def processMessage(self, message):
        if not isinstance(message, Engine.Message):
            raise TypeError("unrecognized message format.")

        if message.messageType == Engine.e_messageType.eOnSwitchChange or message.messageType == Engine.e_messageType.eOnContactChange:
            # todo: search if rules has an onChange event for this gpio
            # todo: execute corresponding triggered rule.
            gpio = message.gpioNumber

            if self.ruleTable[gpio] is not None:
                rule = self.ruleTable[gpio]
                #todo dynamically import rule files and run their exec
                rule_module = importlib.import_module('rules/'+str(rule))
                rule_module.runRule()

    def run(self):
        while (1):
            self.cv.acquire()

            if len(self.messageQueue) == 0:
                self.cv.wait()

            message = self.messageQueue[0]
            del self.messageQueue[0]

            self.cv.release()
            self.processMessage(message)

    def postMessage(self, message):
        # Produce one item
        self.cv.acquire()
        self.messageQueue.append(message)
        self.cv.notify()
        self.cv.release()