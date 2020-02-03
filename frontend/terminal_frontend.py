'''
Defines a frontend that uses terminal input.

Kipp Freud
28/10/2019
'''

#------------------------------------------------------------------

from util.message import message
import util.utilities as ut
from frontend.frontend import CFrontend

#------------------------------------------------------------------

CHATBOT_NAME = "Knowledge_Bot"
STOP_COMMAND = "stop"

#------------------------------------------------------------------

class CTerminalFrontend(CFrontend):
    '''
    A class for running a terminal frontend.
    '''
    def __init__(self, agent, **kwargs):
        '''
        :param agent: Instance of :class:`CQueryEngine` that handles messages.
        '''
        super(CTerminalFrontend, self).__init__(agent)
        self._running = False

    def sendMessage(self, msg):
        '''
        Send a string msg to the user.
        '''
        print(CHATBOT_NAME + ": " + msg)

    def start(self):
        '''
        Start the message loop.
        '''
        initial_message = self.get_initial_message()
        message.logDebug("Starting terminal frontend message loop.", "CTerminalFrontend::start")
        message.logDebug("Sending message '" + initial_message + "'", "CTerminalFrontend::start")
        self.sendMessage(initial_message)
        self._running = True
        while self._running:
            ui = input("> ")
            if not isinstance(ui, str):
                message.logError("User input must be a string.","CTerminalFrontend::start")
                ut.exit(0)
            message.logDebug("Received message: '" + ui + "'", "CTerminalFrontend::start")
            if STOP_COMMAND == ui.lower():
                self.stop()
            else:
                msg = self._agent.process_input(ui)
                message.logDebug("Sending message: '" + msg + "'", "CTerminalFrontend::start")
                self.sendMessage(msg)

    def stop(self):
        '''
        Stop the message loop.
        '''
        self._running = False