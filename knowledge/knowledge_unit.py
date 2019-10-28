'''
Contains a class that will contain a "unit" of knowledge known by the agent, and functions for interacting with that
information. Maybe a "unit" of knowledge is a single article?

Kipp Freud
28/10/2019
'''

#------------------------------------------------------------------

from util.message import message
import util.utilities as ut

#------------------------------------------------------------------

class CKnowledgeUnit(object):
    '''
    This contains a single unit of knowledge.
    '''
    def __init__(self, knowledge_name, knowledge_content):
        '''
        :param knowledge_name: The name of this piece of knowledge.
        :param knowledge_content: The content of this knowledge.
        '''
        if not isinstance(knowledge_name, str):
            message.logError("Given knowledge name is not a string instance.",
                             "CKnowledgeBase::__init__")
            ut.exit(0)
        self.m_knowledge_name = knowledge_name
        self.m_knowledge_content = knowledge_content

    # ------------------------------------------------------------------
    # 'public' members
    # ------------------------------------------------------------------

    def getKnowledgeName(self):
        '''
        :return: The :param:`self.m_knowledge_name`
        '''
        return self.m_knowledge_name

    def getContent(self):
        '''
        :return: The :param:`self.m_knowledge_content`
        '''
        return self.m_knowledge_content

    # ------------------------------------------------------------------
    # 'private' members
    # ------------------------------------------------------------------
