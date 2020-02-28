'''
Will initialise the chatbot.

Kipp Freud
28/10/2019
'''

#------------------------------------------------------------------

from util.message import message
import util.utilities as ut
from NLP.event_engine import CEventEngine
from frontend.terminal_frontend import CTerminalFrontend
from frontend.botui_frontend import CBotUIFrontend

#------------------------------------------------------------------


def main():
    '''
    This will initialize the chatbot.
    '''

    # initialise nlp module
    agent = CEventEngine()
    message.logDebug("Agent loaded.","main::main")

    # initialize frontend
    frontend = CBotUIFrontend(agent)
    frontend.start()


if __name__ == "__main__":
    main()
    ut.exit(1)

