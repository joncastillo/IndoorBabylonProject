import threading
from Engine import Engine
from reinitdb import rebuildDb
def main():

    rebuildDb()
    engine = Engine();
    engine.start()
    engine.join()



if __name__ == "__main__":
    main()