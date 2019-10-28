'''
Will initialise the chatbot.

Kipp Freud
28/10/2019
'''

#------------------------------------------------------------------

from util.message import message
import util.utilities as ut
from knowledge.knowledge_base import CKnowledgeBase
from NLP.agent import CAgent
from frontend.terminal_frontend import CTerminalFrontend

#------------------------------------------------------------------

PATH_TO_DATA = "data/data.csv"

#------------------------------------------------------------------


def main():
    '''
    This will initialize the chatbot.
    '''

    # initialise knowledge base
    knowledge = CKnowledgeBase(PATH_TO_DATA)
    message.logDebug("Knowledge base loaded.","main::main")

    # initialise nlp module
    agent = CAgent(knowledge)
    message.logDebug("Agent loaded.","main::main")

    # initialize frontend
    frontend = CTerminalFrontend(agent)
    frontend.start()


if __name__ == "__main__":
    main()
    ut.exit(1)