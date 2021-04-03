from difflib import SequenceMatcher
import os
import random
import re
import string
import sys
import time
import pprint

from . import const


def log(log, verbose=const.LOG_LEVEL_LOW):
    if (verbose == const.LOG_LEVEL_NONE):
        pass
    elif (verbose == const.LOG_LEVEL_LOW):
        if (type(log) is dict):
            pprint.pformat(log)
        else:
            print(log)
    elif (verbose == const.LOG_LEVEL_LOW or const.LOG_LEVEL_HIGH):
        if (type(log) is dict):
            pprint.pformat(log)
        else:
            print(log)


def random_str(length=8):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def strip_number(numberString):
    nr = numberString.replace(' ', '')
    nr = re.findall('\\d+', nr)[0]
    nr = int(nr)
    return nr


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def speak(what):
    if sys.platform.startswith('linux'):
        import subprocess
        subprocess.call(['speech-dispatcher'])
        subprocess.call(['spd-say', what])
    elif sys.platform.startswith('darwin'):
        os.system('say \'{0}\''.format(what))


def timestamp():
    return int(time.time())
