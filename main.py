'''
Will initialise the chatbot.

Kipp Freud
28/10/2019
'''

#------------------------------------------------------------------

from util.message import message
import util.utilities as ut
from knowledge.knowledge_base import CKnowledgeBase
from frontend.web_frontend import CWebFrontend
from NLP.query_engine import CQueryEngine
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
    agent = CQueryEngine(knowledge)
    message.logDebug("Agent loaded.","main::main")

    # initialize frontend
    frontend = CWebFrontend(agent)
    frontend.start()


if __name__ == "__main__":
    main()
    ut.exit(1)


