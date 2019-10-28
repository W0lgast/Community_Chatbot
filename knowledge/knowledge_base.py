'''
Contains a class that will contain all the knowledge known by the agent, and functions for interacting with the
data.

Kipp Freud
28/10/2019
'''

#------------------------------------------------------------------

from util.message import message
import util.utilities as ut

#------------------------------------------------------------------

class CKnowledgeBase(object):
    '''
    This contains all the knowledge.
    '''
    def __init__(self, path_to_data):
        '''
        This should be given the path to the dataset, it should parse it and store it.

        :param path_to_data: the file location of the data.
        '''
        if not isinstance(path_to_data, str):
            message.logError("Given path to data is not a string instance.",
                             "CKnowledgeBase::__init__")
            ut.exit(0)

    # ------------------------------------------------------------------
    # 'public' members
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # 'private' members
    # ------------------------------------------------------------------