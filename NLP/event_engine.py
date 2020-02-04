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
from frontend.presentation import STANDARD_MSG, CALENDAR_MSG, GENRE_BTN_MSG

# ------------------------------------------------------------------

MAIN_GENRES = ["Music","Standup Comedy","Theatre","Shows & Events","Festivals","Cinema"]

INITIAL_MESSAGE = "Let's find an event for you!"
DATE_FOUND_MESSAGE = "Got it, thanks!"
GENRE_FOUND_MESSAGE = "Great choice!"
DATE_STATE_INITIAL = "Which dates are you interested in?"
GENRE_STATE_INITIAL = "What kind of events are you interested in?:" + ":".join(MAIN_GENRES)
DESIRED_EVENT_INFO_INITIAL = "Tell me a bit about your dream event."

# ------------------------------------------------------------------

DATE_STATE = "DATE_STATE"
GENRE_STATE = "GENRE_STATE"
DESIRED_EVENT_INFO = "DESIRED_EVENT_INFO"
PRESENT_EVENTS = "PRESENT_EVENTS"

STATE_PATH = [DATE_STATE,
              GENRE_STATE,
              DESIRED_EVENT_INFO,
              PRESENT_EVENTS]

STATE_INITIAL_MESSAGES = {
    DATE_STATE: (DATE_STATE_INITIAL, CALENDAR_MSG),
    GENRE_STATE: (GENRE_STATE_INITIAL, GENRE_BTN_MSG),
    DESIRED_EVENT_INFO: (DESIRED_EVENT_INFO_INITIAL, STANDARD_MSG)
}

# ------------------------------------------------------------------

class CEventEngine(CAgent):
    """
    This is a class for answering generic questions using some database.
    """
    def __init__(self, name="Event Engine"):
        super(CEventEngine, self).__init__(name)
        self._initial_message = [self._make_standard_message(INITIAL_MESSAGE)]
        self._dates = None
        self._genres = None
        self._state_index = 0
        self._state = STATE_PATH[0]
        self._initial_message.append(STATE_INITIAL_MESSAGES[self._state])
        self._events_list = ents.getEventsList()

    # ------------------------------------------------------------------
    # 'public' members
    # ------------------------------------------------------------------

    def process_input(self, input):
        """
        Will return an answer to the question given in input.

        :param input: The string question.
        """
        if not isinstance(input, str):
            message.logError("Given input must be a string instance", "CQueryEngine::getAnswer")
            ut.exit(0)

        if self._state == DATE_STATE:
            self._process_date_state(input)
        elif self._state == GENRE_STATE:
            self._process_genre_state(input)
        elif self._state == DESIRED_EVENT_INFO:
            self._process_desired_event_info(input)
        elif self._state == PRESENT_EVENTS:
            self._process_present_events(input)
        return self._update

    # ------------------------------------------------------------------
    # 'private' members
    # ------------------------------------------------------------------

    def _transition_states(self):
        """
        Move to the next state according to the :param:`STATE_PATH`.
        """
        self._state_index += 1
        self._state = STATE_PATH[self._state_index]
        self._update.append(STATE_INITIAL_MESSAGES[self._state])

    def _process_date_state(self, input):
        """
        Processes date, changes state, and returns response.

        :return: tuple response to input.
        """
        dates = input.split(", ")
        events = []
        self._dates = dates
        for date in dates:
            for ev in ents.getEventsList(date=date):
                if ev not in events:
                    events.append(ev)
        self._events_list = events
        self._update.append(self._make_standard_message(DATE_FOUND_MESSAGE))
        self._transition_states()

    def _process_desired_event_info(self, input):
        """
        Processes desired event info, changes state, and returns response.

        :return: tuple response to input.
        """
        ut.exit(0)

    def _process_genre_state(self, input):
        """
        Processes genre info, changes state, and returns response.

        :return: tuple response to input.
        """
        genres = input.split(", ")
        events = []
        self._genres = genres
        for date in self._dates:
            for genre in genres:
                for ev in ents.getEventsList(date=date,
                                             genre=genre):
                    if ev not in events:
                        events.append(ev)
        self._events_list = events
        self._update.append(self._make_standard_message(GENRE_FOUND_MESSAGE))
        self._transition_states()

    def _process_present_events(self, input):
        """
        Processes response to presented dates, changes state, and returns response.

        :return: tuple response to input.
        """
        ut.exit(0)

    def _resetEvents(self):
        """
        Resets :param:`_events_dict`.
        """
        self._events_dict = ents.getEventsList()