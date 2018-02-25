import abc
from enum import Enum

import threading
import importlib
import sqlite3
import pigpio

from Switch import Switch
from Contact import Contact
from PWM import PWM

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from rules.Rule import Rule
from rules.water import RuleWater

class TestScheduler1(Rule):
    def start(self):
        print("testScheduler 1 triggered!")
class TestScheduler2(Rule):
    def start(self):
        print("testScheduler 2 triggered!")
class TestScheduler3(Rule):
    def start(self):
        print("testScheduler 3 triggered!")
class TestScheduler4(Rule):
    def start(self):
        print("testScheduler 4 triggered!")

class Engine(threading.Thread):
    e_messageType = Enum('messageType', 'eOnSwitchChange eOnPwmChange eOnContactChange eSetGpio')


    class Message(object):
        __metaclass__ = abc.ABCMeta

        @abc.abstractmethod
        def __init__(self):
            self.messageType = None

    class OnSwitchChangeMessage(Message):
        def __init__(self,gpioNumber, value):
            self.gpioNumber = gpioNumber
            self.value = value
            self.messageType = Engine.e_messageType.eOnSwitchChange

    class OnPwmChangeMessage(Message):
        def __init__(self,gpioNumber, value):
            self.gpioNumber = gpioNumber
            self.value = value
            self.messageType = Engine.e_messageType.eOnPwmChange

    class OnContactChangeMessage(Message):
        def __init__(self,gpioNumber, value):
            self.gpioNumber = gpioNumber
            self.value = value
            self.messageType = Engine.e_messageType.eOnContactChange

    class SetGpioValueMessage(Message):
        def __init__(self,gpioAlias, value):
            self.gpioAlias = gpioAlias
            self.value = value
            self.messageType = Engine.e_messageType.eSetGpio

    def __init__(self):
        super().__init__()
        self.messageQueue = []
        self.ruleTable = {}
        #self.gpioList = []
        self.gpioMap = {}
        self.gpioLabelMapping = {}
        self.ruleTableCronType = {}
        self.ruleTableSwitchType = {}
        self.cv = threading.Condition()
        self.pi = pigpio.pi()

        self.initialiseLists()
        # create apscheduler:
        self.scheduler = BackgroundScheduler()

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
                #self.gpioList.append(switch)
                self.gpioLabelMapping[label] = gpioNumber

                self.gpioMap[gpioNumber]= switch

            elif gpioType == 'in':
                # create a contact
                contact = Contact(pinNumber, gpioNumber, label, self)
                #self.gpioList.append(contact)
                self.gpioLabelMapping[label] = gpioNumber

                self.gpioMap[gpioNumber]= contact
            elif gpioType == 'PWM':
                # create a pwm
                pwm = PWM(pinNumber, gpioNumber, label, self)
                #self.gpioList.append(pwm)
                self.gpioLabelMapping[label] = gpioNumber

                self.gpioMap[gpioNumber]= pwm
            # else:
            #     print("Skipped pin for now")

        for gpio in self.gpioMap.values():
            if gpio.threadBehavior != None:
                gpio.threadBehavior.start()

        table = db.execute(""" SELECT * FROM Alias""")
        self.gpioAliasMapping = {}
        for row in table:
            alias = row[1]
            gpio = row[2]
            self.gpioAliasMapping[alias] = gpio

        self.gpioAliasMapping = {**self.gpioLabelMapping, **self.gpioAliasMapping}
        print("---------------")
        print("GPIO Map:")
        print("---------------")
        print(self.gpioMap)
        print("---------------")
        print("Alias Map:")
        print("---------------")
        print(self.gpioAliasMapping)

        db = sqlite3.connect("./test2.sql")

        rules = db.execute(""" SELECT * FROM Rules """)

        for row in rules:
            ruleGpioTrigger = row[1]
            ruleGpioNewValue = row[2]
            ruleTriggeredScript = row[3]

            if ruleGpioTrigger not in self.ruleTableSwitchType:
                self.ruleTableSwitchType[ruleGpioTrigger] = []
            self.ruleTableSwitchType[ruleGpioTrigger].append([ruleGpioNewValue, ruleTriggeredScript])

        cronJobs = db.execute(""" SELECT * FROM CronJobs """)

        for row in cronJobs:
            ruleCronStatement = row[1]
            ruleTriggeredScript = row[2]

            if ruleCronStatement not in self.ruleTableCronType:
                self.ruleTableCronType[ruleCronStatement] = []
            self.ruleTableCronType[ruleCronStatement].append(ruleTriggeredScript)


    def processMessage(self, message):
        if not isinstance(message, Engine.Message):
            raise TypeError("unrecognized message format.")

        if message.messageType == Engine.e_messageType.eOnSwitchChange:
            # todo: search if rules has an onChange event for this gpio
            # todo: execute corresponding triggered rule.
            gpio = message.gpioNumber

            if gpio in self.ruleTableSwitchType:
                rule = self.ruleTableSwitchType[gpio]
                #todo dynamically import rule files and run their exec
                rule_module = importlib.import_module('rules/'+str(rule))
                rule_module.runRule()

        elif message.messageType == Engine.e_messageType.eOnContactChange:
            # todo: search if rules has an onChange event for this gpio
            # todo: execute corresponding triggered rule.
            gpio = message.gpioNumber

            if gpio in self.ruleTableSwitchType:
                rule = self.ruleTableSwitchType[gpio]
                #todo dynamically import rule files and run their exec
                rule_module = importlib.import_module('rules/'+str(rule))
                rule_module.runRule()

        elif message.messageType == Engine.e_messageType.eSetGpio:
            gpioAlias = message.gpioAlias
            value = message.value
            gpioNumber = self.gpioAliasMapping[gpioAlias]
            self.gpioMap[gpioNumber].setValue(value)


    def run(self):

        #run scheduler jobs
        for cronjob in self.ruleTableCronType:
            for script_to_run in self.ruleTableCronType[cronjob]:
                cronStatement = cronjob + " " + "rule: " + script_to_run
                print ("cronstatement: " +cronStatement)
                newrule = eval(script_to_run)(self)
                self.scheduler.add_job(newrule.start, CronTrigger.from_crontab(cronjob))

        self.scheduler.start()


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