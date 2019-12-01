'''
Contains a class for messages to be used within the framework. Make sure to include "message" and
not "CMessage". This acts as a static class.

Kipp Freud
28/10/2019
'''

# ------------------------------------------------------------------

DEBUG_TAG = "DEBUG"
WARNING_TAG = "WARNING"
ERROR_TAG = "ERROR"

# ------------------------------------------------------------------

class CMessage(object):
    '''
    A class for printing terminal messages and saving them to a log file.
    '''

    def __init__(self, logfile='log.txt'):
        self._logname = logfile
        # start the logfile
        self._logfile = None
        self._logFile(self._logname)
        # store timing info
        self.timing = {}

    # ------------------------------------------------------------------
    # 'public' members
    # ------------------------------------------------------------------

    def logError(self, message, funcname=''):
        '''
        Log a message with the 'ERROR' tag.

        :param str message: Is the text of the message to be dispalyed.
        :param str funcname: Is an optional argument that is used for printing the name of \
        the function where the message is coming from.
        '''
        self._log(message, ERROR_TAG, funcname)

    def logWarning(self, message, funcname=''):
        '''
        Log a message with the 'WARNING' tag.

        :param str message: Is the text of the message to be dispalyed.
        :param str funcname: Is an optional argument that is used for printing the name of \
        the function where the message is coming from.
        '''
        self._log(message, WARNING_TAG, funcname)

    def logDebug(self, message, funcname=''):
        '''
        Log a message with the 'DEBUG' tag.

        :param str message: Is the text of the message to be dispalyed.
        :param str funcname: Is an optional argument that is used for printing the name of \
        the function where the message is coming from.
        '''
        self._log(message, DEBUG_TAG, funcname)


    def logTiming(self, method, time_taken):
        '''
        Log timing info that will be printed now and saved in the log now, but also will be held and shown again
        when :func:`showTiming` is called.
        '''
        strm = str(method)
        tt = time_taken * 1000
        message.logDebug('{0}  {1:.2f} ms'.format(strm, tt), "CMessage::timeit")
        if strm not in self.timing: self.timing[strm] = [tt]
        else: self.timing[strm].append(tt)

    # ------------------------------------------------------------------
    # 'private' members
    # ------------------------------------------------------------------

    def _log(self, msg, level, funcname=''):
        # format message and send it to console
        if funcname != '':
            message = "{0}::{1}::{2}".format(level, funcname, msg)
            print(message)
        else:
            message = "{0}::{1}".format(level, msg)
            print(message)
        # save it to the log file
        if self._logfile is not None:
            self._logfile.write((message + '\n').encode('utf-8'))

    def _logFile(self, newname):
        '''
        Make a new log file at the given location
        :param newname: A string of the path and name to the new log file
        '''
        if self._logfile is not None:
            self._logfile.close()
        self._logname = newname
        self._logfile = open(newname, 'wb')


message = CMessage()
