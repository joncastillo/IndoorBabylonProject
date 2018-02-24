import sqlite3
from lxml import etree

def rebuildDb():
    tree = etree.parse("./config.xml")
    db = sqlite3.connect("./test2.sql")


    # Rebuild tables:
    db.execute("""DROP TABLE IF EXISTS Gpio""")
    db.execute("""DROP TABLE IF EXISTS Alias""")
    db.execute("""DROP TABLE IF EXISTS GpioSorted""")
    db.execute("""DROP TABLE IF EXISTS Rules""")

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

    db.execute("""
      CREATE TABLE IF NOT EXISTS CronJobs (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        cronStatement TEXT NOT NULL UNIQUE,
        triggeredScript TEXT NOT NULL
      )""")

    db.execute("""
      CREATE TABLE IF NOT EXISTS Rules (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        GpioID INTEGER NOT NULL,
        newValue INTEGER NOT NULL,
        triggeredScript TEXT NOT NULL, 
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


            for item3 in item2:
                alias = item3.text
                if alias == "NOT_ASSIGNED":
                    continue
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

    tree = etree.parse("./rules.xml")
    for item in tree.iterfind("ONCHANGERULES"):
        for item2 in item:
            print(item2)

    for item in tree.iterfind("CRONRULES"):
        for item2 in item:
            print(item2)
