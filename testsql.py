import sqlite3
from lxml import etree


tree = etree.parse("./config.xml")
db = sqlite3.connect("./test.sql")

db.execute("""DROP TABLE IF EXISTS Gpio""")
db.execute("""DROP TABLE IF EXISTS Alias""")

db.execute("""
  CREATE TABLE IF NOT EXISTS Gpio (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Pin INTEGER NOT NULL UNIQUE,
    Type TEXT NOT NULL,
    name TEXT NOT NULL UNIQUE
  )""")

db.execute("""
  CREATE TABLE IF NOT EXISTS Alias (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    alias TEXT NOT NULL UNIQUE,
    GpioID INTEGER NOT NULL,
    FOREIGN KEY(GpioID) REFERENCES Gpio(ID)
  )""")

for item in tree.iterfind("GPIO"):
    for item2 in item:
        print (item2.tag, end='')
        attribute = (item2.attrib)
        print (attribute)
        db.execute(""" 
            INSERT OR REPLACE  INTO Gpio ( Pin, Type, name )
            VALUES ( ?, ?, ?  )
        """,(int(attribute["pin"]), attribute["direction"], attribute["name"]))

for item in tree.iterfind("PWM"):
    for item2 in item:
        print (item2.tag,end ='')
        attribute = (item2.attrib)
        print (item2.attrib)
        db.execute(""" 
            INSERT OR REPLACE  INTO Gpio ( Pin, Type, name )
            VALUES ( ?, ?, ?  )
        """,(int(attribute["pin"]), "PWM", attribute["name"]))

for item in tree.iterfind("I2C"):
    for item2 in item:
        print (item2.tag,end='')
        attribute = (item2.attrib)
        print (item2.attrib)
        db.execute(""" 
            INSERT OR REPLACE  INTO Gpio ( Pin, Type, name )
            VALUES ( ?, ?, ?  )
        """,(int(attribute["pin"]), "I2C", attribute["name"]))

for item in tree.iterfind("SPI"):
    for item2 in item:
        print (item2.tag,end='')
        attribute = (item2.attrib)
        print (item2.attrib)
        db.execute(""" 
            INSERT OR REPLACE  INTO Gpio ( Pin, Type, name )
            VALUES ( ?, ?, ?  )
        """,(int(attribute["pin"]), "SPI", attribute["name"]))


db.execute("""
  CREATE TABLE IF NOT EXISTS GpioSorted (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Pin INTEGER NOT NULL UNIQUE,
    Type TEXT NOT NULL,
    name TEXT NOT NULL UNIQUE
  )""")

db.execute("""
  INSERT INTO GpioSorted ( Pin, Type, name)
  SELECT Pin, Type, name FROM Gpio
  ORDER BY Pin """)

for item in tree.iterfind("ALIAS"):
    for item2 in item:
        print (item2.tag,end='')
        attribute = (item2.attrib)
        print (item2.attrib)
        name = item2.attrib["name"]
        if name == "NOT_ASSIGNED":
            continue

        for item3 in item2:
            alias = item3.text
            gpioId = db.execute(""" 
              SELECT ID FROM Gpio WHERE name='"""+name+"""'""")
            gpoIdNum = gpioId.fetchone()[0]

            db.execute("""
                INSERT OR REPLACE  INTO Alias ( alias, GpioID )
                VALUES ( ?, ? )
            """, (alias, gpoIdNum))

db.commit()
table = db.execute(""" SELECT * FROM Gpio """)
print (table.fetchall())
table = db.execute(""" SELECT * FROM Alias """)
print (table.fetchall())