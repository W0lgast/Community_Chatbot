'''
We'll put utility functions here - timing decorators, exiting functions, and maths stuff are here atm.

Kipp Freud
28/10/2019
'''

#------------------------------------------------------------------

import time
from math import sqrt
import sys

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
