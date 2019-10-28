'''
Contains a class for answering generic questions using some database.

Kipp Freud
28/10/2019
'''

#------------------------------------------------------------------

from util.message import message
import util.utilities as ut
from knowledge.knowledge_base import CKnowledgeBase

#------------------------------------------------------------------

class CAgent(object):
    '''
    This is a class for answering generic questions using some database.
    '''
    def __init__(self, knowledge_base):
        if not isinstance(knowledge_base, CKnowledgeBase):
            message.logError("Given knowledge base is not a CKnowledgeBase instance.",
                             "CAgent::__init__")
            ut.exit(0)

        self.m_knowledge_base = knowledge_base

    # ------------------------------------------------------------------
    # 'public' members
    # ------------------------------------------------------------------

    def getAnswer(self, input):
        '''
        Will return an answer to the question given in input.
        Currently it will always return "I don't want to help you at the moment, ask me another time."

        :param input: The string question.
        '''
        if not isinstance(input, str):
            message.logError("Given input must be a string instance", "CAgent::getAnswer")
            ut.exit(0)

        return "I don't want to help you at the moment, ask me another time."

    # ------------------------------------------------------------------
    # 'private' members
    # ------------------------------------------------------------------