#for time.sleep:
import time
#import threading

class Rule(object):

    ### Base class for rules
    ### A rule must run as a thread, in the background.

    def __init__(self,engine):
        self.engine = engine
