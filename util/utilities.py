'''
We'll put utility functions here - timing decorators, exiting functions, and maths stuff are here atm.

Kipp Freud
28/10/2019
'''

#------------------------------------------------------------------

import time
from math import sqrt
import sys
from ast import literal_eval as lit
import random

from util.message import message

#------------------------------------------------------------------

TIMING_INFO = False

#------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# system functions
#-----------------------------------------------------------------------------------------

def exit(code):
    '''
	Exit the program, 0 is failure, 1 is success.
	'''
    if not isinstance(code, int):
        message.logError('Exit code must be an interger.')
        exit(0)
    if code == 0:
        message.logError('Exiting program with failure status.')
    elif code == 1:
        if TIMING_INFO is True:
            showTiming()
        message.logDebug('Exiting program with success status.')
    else:
        message.logError('Exiting program with unknown error status ('+str(code)+')')
    sys.exit()

#-----------------------------------------------------------------------------------------
# timing functions
#-----------------------------------------------------------------------------------------

def timeit(method):
    '''
    Use as a decorator on methods to print timing information for that call to the log file.
    '''
    def timed(*args, **kw):
        if TIMING_INFO is True:
            ts = time.time()
        result = method(*args, **kw)
        if TIMING_INFO is True:
            te = time.time()
            message.logTiming(method, te-ts)
        return result
    return timed

def showTiming():
    '''
    Show a chart of any timing info stored in the message class, and write it to the log file.
    '''
    if TIMING_INFO is True:
        message.logDebug("Showing average timing info for method instances:", "utilities::showTiming")
        for k, v in message.timing.items():
            message.logDebug("{0:.2f} (sigma={1:.2f}, total={2:.2f}): {3}".format(mean(v), stdEstimate(v), sum(v), k))

#-----------------------------------------------------------------------------------------
# maths functions
#-----------------------------------------------------------------------------------------

def mean(x):
    '''
    Returns the mean of the list of numbers.
    '''
    return sum(x) / (len(x)+0.0)

def stdEstimate(x):
    '''
    Returns an estimate of the standard deviation of the list of numbers.
    '''
    meanx = mean(x)
    norm = 1./(len(x)+0.0)
    y = []
    for v in x:
        y.append( (v - meanx)*(v - meanx) )
    return sqrt(norm * sum(y))

#-----------------------------------------------------------------------------------------
# list functions
#-----------------------------------------------------------------------------------------

def randomSample(lst, num_sample):
    """Will return a randomly selected num_sample elements from lst."""
    if not isinstance(lst, list):
        message.logError("lst must be a list instance.", "utilities::randomSample")
        exit(0)
    if not isinstance(num_sample, int):
        message.logError("num_sample must be an int instance.", "utilities::randomSample")
        exit(0)
    return random.sample(lst, num_sample)

#-----------------------------------------------------------------------------------------
# string functions
#-----------------------------------------------------------------------------------------

def parseStr(str):
    """
    Converts string representation of a literal to actual literal.
    """
    str = str.replace("null", "None").replace("false","False").replace("true","True")
    return lit(str)

#-----------------------------------------------------------------------------------------
# date functions
#-----------------------------------------------------------------------------------------

def dateCheck(date, start_date, end_date):
    """
    Will check if :param:`date` is between :param:`start_date` and :param:`end_date`.

    :return: Boolean.
    """
    date = date.split("-")
    start_date = start_date.split("-")
    if not _dateCheck(start_date, date):
        return False
    end_date = end_date.split("-")
    return _dateCheck(date, end_date)

def _dateCheck(date_1, date_2):
    """
    Will return True if date_1 is before or equal to date_2.
    Date params are lists with 3 elements, year, month, day.
    """
    if date_1[0] < date_2[0]:
        return True
    if date_1[0] > date_2[0]:
        return False
    if date_1[1] < date_2[1]:
        return True
    if date_1[1] > date_2[1]:
        return False
    if date_1[2] < date_2[2]:
        return True
    if date_1[2] > date_2[2]:
        return False
    return True


