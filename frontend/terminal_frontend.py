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
INITIAL_MESSAGE = "How can I help you?"
STOP_COMMAND = "stop"

#------------------------------------------------------------------

class CTerminalFrontend(CFrontend):
    '''
    A class for running a terminal frontend.
    '''
    def __init__(self, agent, **kwargs):
        '''
        :param agent: Instance of :class:`CAgent` that handles messages.
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
        message.logDebug("Starting terminal frontend message loop.", "CTerminalFrontend::start")
        message.logDebug("Sending message '" + INITIAL_MESSAGE + "'", "CTerminalFrontend::start")
        self.sendMessage(INITIAL_MESSAGE)
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
                msg = self._agent.get_answer(ui)
                message.logDebug("Sending message: '" + msg + "'", "CTerminalFrontend::start")
                self.sendMessage(msg)

    def stop(self):
        '''
        Stop the message loop.
        '''
        self._running = False