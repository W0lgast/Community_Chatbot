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

        knowledge_list = self._restrictSearchSpace(input)
        response = self._getResponse(input, knowledge_list)

        return response

    # ------------------------------------------------------------------
    # 'private' members
    # ------------------------------------------------------------------

    def _restrictSearchSpace(self, input):
        '''
        This will search the internal knowledge base :param:`self.m_knowledge_base` and will return a subset of the
        :class:`CKnowledgeUnit` instances contained by it in the form of a list. These knowledge units will
        hopefully be the most relevant for answering the question.

        :param input: A string question.
        :return: A :list: of :class:`CKnowledgeUnit` instances.
        '''
        return []

    def _getResponse(self, input, knowledge_list):
        '''
        This will search the :class:`CKnowledgeUnit` instances contained in the :param:`knowledge_list`, and will
        return a string response to the question. If an empty list is given, an "I don't know" type response is
        returned.

        :param input: A string question.
        :param knowledge_list: The :list: of :class:`CKnowledgeUnit` instances returned by \
        :func:`_restrictSearchSpeace`.
        '''

        return "I don't want to help you at the moment, ask me another time."