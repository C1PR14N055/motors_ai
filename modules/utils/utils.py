from core import Config

from difflib import SequenceMatcher
import os
import random
import re
import string
import sys
import time
import pprint


class Tools():
    ''' LOG LEVELS '''
    LOG_LEVEL_NONE = 0
    LOG_LEVEL_LOW = 1
    LOG_LEVEL_HIGH = 2
    LOG_LEVEL_SPEAK = 3

    @staticmethod
    def log(log, verbose=LOG_LEVEL_LOW):
        '''
        Logs on 4 levels, default low, see above

        Parameters:
            log (str): Is used to pass the log
            varbose (int, default=LOG_LEVEL_LOW)
        '''
        # no print
        if verbose == Tools.LOG_LEVEL_NONE:
            pass
        # on low, print if low
        elif verbose == Tools.LOG_LEVEL_LOW:
            Tools.pretty_print(log)
        # on high, show high and low
        elif verbose == Tools.LOG_LEVEL_HIGH:
            Tools.pretty_print(log)
        # on speak, speak and show both high and low
        elif verbose == Tools.LOG_LEVEL_SPEAK:
            Tools.pretty_print(log)
            Tools.speak(log)

    def random_str(length=8):
        return ''.join(
            random.choice(
                string.ascii_letters + string.digits
            )
            for _ in range(length)
        )

    def strip_number(numberString):
        nr = numberString.replace(' ', '')
        nr = re.findall('\\d+', nr)[0]
        nr = int(nr)
        return nr

    def similar(a, b):
        return SequenceMatcher(None, a, b).ratio()

    def speak(what):
        Tools.log(what, Tools.LOG_LEVEL_HIGH)
        if sys.platform.startswith('linux'):
            import subprocess
            subprocess.call(['speech-dispatcher'])
            subprocess.call(['spd-say', what])
        elif sys.platform.startswith('darwin'):
            os.system('say \'{0}\''.format(what))

    def timestamp():
        return int(time.time())

    def pretty_print(log):
        print("*" * 42)
        if type(log) == dict:
            pprint.pformat(log)
        else:
            print(log)
