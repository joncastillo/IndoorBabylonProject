import sqlite3
from lxml import etree

from Switch import Switch
from Contact import Contact
from PWM import PWM

import reinitdb

reinitdb.rebuildDb()

tree = etree.parse("./config.xml")
db = sqlite3.connect("./test2.sql")


# for each gpio in SQL, create a pin object:

#factory

gpio = db.execute(""" SELECT * FROM Gpio """)

gpioList = []
nameMapping = {}

for row in gpio:
    gpioType = row[2]
    pinNumber = row[0]
    gpioNumber = row[1]
    label = row[3]

    if gpioType == 'out':
        #create a switch
        switch = Switch(pinNumber, gpioNumber, label)
        gpioList.append(switch)
        nameMapping[label]=gpioNumber
    elif gpioType == 'in':
        #create a contact
        contact = Contact(pinNumber, gpioNumber, label)
        gpioList.append(contact)
        nameMapping[label]=gpioNumber
    elif gpioType == 'PWM':
        #create a pwm
        pwm = PWM(pinNumber, gpioNumber, label)
        gpioList.append(pwm)
        nameMapping[label]=gpioNumber
    else:
        print("Skipped pin for now")


table = db.execute(""" SELECT * FROM Alias""")
aliasMapping = {}
for row in table:
    alias = row[1]
    gpio = row[2]
    aliasMapping[alias] = gpio

aliasMapping = {**aliasMapping, **nameMapping}
print (gpioList)
print (aliasMapping)
