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
from pathlib import Path
import pandas as pd
import pickle as pkl

from util.message import message

#------------------------------------------------------------------

TIMING_INFO = True

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
# pickle functions
#-----------------------------------------------------------------------------------------

def save(save_this, file_name):
    output = open(file_name, 'wb')
    pkl.dump(save_this, output)
    output.close()

def load(file_name):
    pkl_file = open(file_name, 'rb')
    obj = pkl.load(pkl_file)
    pkl_file.close()
    return obj

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


def merge_events(api_events: list, pd_events: pd.DataFrame) :
    # I don't know why this is necessary
    pd_events.to_csv("expanded_events.csv", index=False)
    pd_events = pd.read_csv("expanded_events.csv")
    pd_events = pd_events.rename(columns={"Date": "startDate", \
                                            "TimeStart": "startTimeString", \
                                            "TimeEnd": "endTimeString", \
                                            "Description": "description", \
                                            "Category": "genre", \
                                            "Title": "title", \
                                            "Location": "venue", \
                                            "URL": "webLink"
                                          })
    pd_events['headline'] = pd_events['title']
    pd_events['startDate'] = pd.to_datetime(pd_events['startDate'])
    pd_events['startDate'] = pd_events['startDate'].dt.strftime('%Y-%m-%d')
    pd_events["endDate"] = pd_events["startDate"]
    pd_events["image"] = "https://theparkcentre.org.uk/wp/wp-content/uploads/2017/07/cropped-logo-small-1.png"
    hardcoded_list_of_dicts = list( pd_events.T.to_dict().values() )

    for event in hardcoded_list_of_dicts :
        event["genre"] = [event["genre"]]
        event["image"] = {"url": event["image"]}

    return api_events + hardcoded_list_of_dicts


def get_project_root() -> Path:
    """Returns project root folder."""
    return Path(__file__).parent.parent