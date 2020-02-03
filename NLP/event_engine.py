'''
Contains a class for event recommendation.

Kipp Freud
31/01/2020
'''

# ------------------------------------------------------------------

from util.message import message
import util.utilities as ut
import util.events as ents
from NLP.agent import CAgent

# ------------------------------------------------------------------

INITIAL_MESSAGE = "Let's find an event for you!"

DATE_STATE = "DATE_STATE"
DESIRED_EVENT_INFO = "DESIRED_EVENT_INFO"
PRESENT_EVENTS = "PRESENT_EVENTS"
STATE_PATH = [DATE_STATE,
              DESIRED_EVENT_INFO,
              PRESENT_EVENTS]

# ------------------------------------------------------------------

class CEventEngine(CAgent):
    """
    This is a class for answering generic questions using some database.
    """
    def __init__(self, name="Event Engine"):
        super(CEventEngine, self).__init__(name)
        self._initial_message = INITIAL_MESSAGE
        self._events_dict = ents.getEventsList()

    # ------------------------------------------------------------------
    # 'public' members
    # ------------------------------------------------------------------

    def process_input(self, input):
        """
        Will return an answer to the question given in input.
        Currently it will always return "I don't want to help you at the moment, ask me another time."

        :param input: The string question.
        """
        if not isinstance(input, str):
            message.logError("Given input must be a string instance", "CQueryEngine::getAnswer")
            ut.exit(0)
        response = "I recommend you watch The Mummy Returns."
        self._update.append(response)
        return response

    # ------------------------------------------------------------------
    # 'private' members
    # ------------------------------------------------------------------

    def _resetEvents(self):
        """
        Resets :param:`_events_dict`.
        """
        self._events_dict = ents.getEventsList()