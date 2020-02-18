'''
Contains an abstract base class for agents, these are like conversation handlers.

Kipp Freud
31/01/2020
'''

# ------------------------------------------------------------------

from abc import ABC, abstractmethod

from util.message import message
import util.utilities as ut
from frontend.presentation import STANDARD_MSG, CALENDAR_MSG

# ------------------------------------------------------------------

INITIAL_MESSAGE = "Hi, I'm a default agent; that means I'm pretty useless."

# ------------------------------------------------------------------

class CAgent(ABC):
    """
    This is a base class for any conversation handling agent.
    """
    def __init__(self, name="Agent"):
        if not isinstance(name, str):
            message.logError("Agents name is not a string instance.",
                             "CAgent::__init__")
            ut.exit(0)
        self._initial_message = [self._make_standard_message(INITIAL_MESSAGE)]
        self._most_recent_update = self._initial_message
        self._update = []

    # ------------------------------------------------------------------
    # 'public' members
    # ------------------------------------------------------------------

    @abstractmethod
    def process_input(self, input):
        """
        Will return a response to the given input
        Will add this response to the self._update param.

        :param input: The string question.
        """
        message.logError("Function should be overwritten by a derived class.",
                         "CAgent::process_input")
        ut.exit(0)

    def get_update(self):
        """
        Returns any updates to be sent to the user.
        Also clears the update list.
        """
        ret = self._update
        self._most_recent_update = ret
        self._update = []
        return ret

    def get_initial_message(self):
        return self._initial_message

    def get_most_recent_message(self):
        return self._most_recent_update

    # ------------------------------------------------------------------
    # 'private' members
    # ------------------------------------------------------------------

    def _make_standard_message(self, msg):
        return (msg, STANDARD_MSG)

    def _make_calander_message(self, msg):
        return (msg, CALENDAR_MSG)