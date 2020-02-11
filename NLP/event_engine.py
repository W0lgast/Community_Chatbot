'''
Contains a class for event recommendation.

Kipp Freud
31/01/2020
'''

# ------------------------------------------------------------------

from util.message import message
import util.utilities as ut
import util.events as ents
from util.events import GENRE_SYNONYMS, START_DATE, END_DATE, GENRE_KEY, HEADLINE_KEY
from util.events import TITLE_KEY, IMAGE_KEY, IMAGE_URL_KEY, WEBLINK_KEY
from NLP.agent import CAgent
from frontend.presentation import STANDARD_MSG, CALENDAR_MSG, GENRE_BTN_MSG, EVENT_MSG

# ------------------------------------------------------------------

MAIN_GENRES = list(GENRE_SYNONYMS.keys())

INITIAL_MESSAGE = "Let's find an event for you!"
DATE_FOUND_MESSAGE = "Got it, thanks!"
GENRE_FOUND_MESSAGE = "Great choice!"
DATE_STATE_INITIAL = "Which dates are you interested in?"
GENRE_STATE_INITIAL = "What kind of events are you interested in?:" + ":".join(MAIN_GENRES)
DESIRED_EVENT_INFO_INITIAL = "Tell me a bit about your dream event."
PRESENT_EVENTS_INITIAL = "We think you'll love these events:"

# ------------------------------------------------------------------

DATE_STATE = "DATE_STATE"
GENRE_STATE = "GENRE_STATE"
DESIRED_EVENT_INFO = "DESIRED_EVENT_INFO"
PRESENT_EVENTS = "PRESENT_EVENTS"

# State path MUST end with PRESENT_EVENTS.
STATE_PATH = [DATE_STATE,
              GENRE_STATE,
              #DESIRED_EVENT_INFO,
              PRESENT_EVENTS]

STATE_INITIAL_MESSAGES = {
    DATE_STATE: (DATE_STATE_INITIAL, CALENDAR_MSG),
    GENRE_STATE: (GENRE_STATE_INITIAL, GENRE_BTN_MSG),
    DESIRED_EVENT_INFO: (DESIRED_EVENT_INFO_INITIAL, STANDARD_MSG),
    PRESENT_EVENTS: (PRESENT_EVENTS_INITIAL, STANDARD_MSG)
}

# ------------------------------------------------------------------

class CEventEngine(CAgent):
    """
    This is a class for answering generic questions using some database.
    """
    def __init__(self, max_events=3, name="Event Engine"):
        super(CEventEngine, self).__init__(name)
        if not isinstance(max_events, int):
            message.logError("Max events must be an int.", "CEventsEngine::__init__")
            ut.exit(0)
        self._initial_message = [self._make_standard_message(INITIAL_MESSAGE)]
        self._state_index = 0
        self._state = STATE_PATH[0]
        self._initial_message.append(STATE_INITIAL_MESSAGES[self._state])
        self._events_list = ents.getEventsList()
        self._max_events = max_events
        self._debugInfo()

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
        if self._state == PRESENT_EVENTS:
            self._present_events()

    def _process_date_state(self, input):
        """
        Processes date, changes state, and returns response.

        :return: tuple response to input.
        """
        dates = input.split(", ")
        self._restrictEventsListByDate(dates)
        self._update.append(self._make_standard_message(DATE_FOUND_MESSAGE))
        self._transition_states()

    def _process_desired_event_info(self, input):
        """
        Processes desired event info, changes state, and returns response.

        :return: tuple response to input.
        """
        ut.exit(0)

    def _present_events(self):
        """
        Presents selected events to the user.
        """
        if len(self._events_list) == 0:
            message.logError("There aren't any events to present, this function shouldn't have been called."
                             "CEventEngine::_present_events")
            ut.exit(0)
        if len(self._events_list) <= 3:
            events_to_present = self._events_list
        else:
            events_to_present = ut.randomSample(self._events_list, self._max_events)
        for event in events_to_present:
            self._update.append(self._make_event_message(event))
        return self._update

    def _process_genre_state(self, input):
        """
        Processes genre info, changes state, and returns response.

        :return: tuple response to input.
        """
        genres = input.split(", ")
        self._restrictEventsListByGenre(genres)
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

    def _restrictEventsListByGenre(self, genres):
        """
        Will remove members of :param`self._events_list` which do not satisfy the given genres.

        :param genres: List of genres. Must only contain genres which are keys of the GENRE_SYNONYMS dict.
        """
        if not isinstance(genres, list):
            message.logError("List of genres must be a list.",
                             "CEventEngine::_restrictEventsListByGenre")
            ut.exit(0)
        ok_genres = []
        for genre in genres:
            if genre not in GENRE_SYNONYMS.keys():
                message.logError("Unknown genre (it's not in the genre synonym dictionary).",
                                 "CEventEngine::_restrictEventsListByGenre")
                ut.exit(0)
            ok_genres += GENRE_SYNONYMS[genre]
        new_ents = []
        for ent in self._events_list:
            if GENRE_KEY in ent.keys():
                for genre in ent[GENRE_KEY]:
                    if genre in ok_genres:
                        new_ents.append(ent)
                        break
        self._events_list = new_ents
        self._debugInfo()

    def _restrictEventsListByDate(self, dates):
        """
        Will remove members of :param`self._events_list` which do not happen at the specified dates.

        :param dates: List of dates.
        """
        if not isinstance(dates, list):
            message.logError("List of dates must be a list.",
                             "CEventEngine::_restrictEventsListByGenre")
            ut.exit(0)
        new_ents = []
        for ent in self._events_list:
            start_date = ent[START_DATE]
            end_date = ent[END_DATE]
            for date in dates:
                if ut.dateCheck(date, start_date, end_date):
                    new_ents.append(ent)
                    break
        self._events_list = new_ents
        self._debugInfo()

    def _debugInfo(self):
        """
        Prints a debug message about the number of acceptable events at this stage.
        """
        message.logDebug("There are " + str(len(self._events_list)) + " acceptable events at this stage.",
                         "CEventEngine::_debugInfo")

    def _make_event_message(self, event):
        headline = event[HEADLINE_KEY]
        title = event[TITLE_KEY]
        if IMAGE_KEY in event.keys():
            image_url = event[IMAGE_KEY][IMAGE_URL_KEY].replace("\\/", "/")
        else:
            image_url = "_"
        if WEBLINK_KEY in event.keys():
            weblink = event[WEBLINK_KEY].replace("\\/", "/")
        else:
            weblink = "_"
        text = headline
        if text is None: text = title
        elif title is not None: text += ": " + title
        text += "::" + image_url + "::" + weblink
        return (text, EVENT_MSG)