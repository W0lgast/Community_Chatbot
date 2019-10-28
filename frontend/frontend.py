'''
Defines an abstract base class for frontend classes.

Kipp Freud
28/10/2019
'''

#------------------------------------------------------------------

from abc import ABC, abstractmethod

from util.message import message
import util.utilities as ut

#------------------------------------------------------------------

class CFrontend(ABC):
    '''
    A base class interface for frontends to the rest of the framework. The child classes should be easily
    interchangeable with each other.
    '''

    def __init__(self, agent):
        '''
        :param agent: a :class:`CAgent` to handle messages.
        '''
        self.m_agent = agent

    @abstractmethod
    def sendMessage(self, msg):
        '''
        Send a msg to the user.
        '''
        message.logError("This function must be overwritten in derived classes.",
                         "CFrontend::sendMessage")
        ut.exit(0)