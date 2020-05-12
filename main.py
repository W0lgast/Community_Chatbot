'''
Runs all the services we want.

Currently, an Events bot and a data entry

Kipp Freud & Gavin Leech
15/04/2020
'''

#------------------------------------------------------------------

from util.message import message
import util.utilities as ut
from NLP.event_engine import CEventEngine
from frontend.terminal_frontend import CTerminalFrontend
from frontend.botui_frontend import CBotUIFrontend

#------------------------------------------------------------------


def run_events_bot():
    agent = CEventEngine()
    message.logDebug("Agent loaded.", "main::main")

    # initialize frontend
    return CBotUIFrontend(agent)


def run_event_form() :
    message.logDebug("Form launched", "main::main")
    return 


def main():
    '''
    This will run the specified components
    '''
    # TODO: Probably have to spawn two threads
    # TODO: Is this best left as two scripts anyway?
    #run_event_form()
    run_events_bot().start()



if __name__ == "__main__":
    main()
    ut.exit(1)

