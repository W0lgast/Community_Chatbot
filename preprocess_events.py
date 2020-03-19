'''
Preprocesses events list and adds saves it as pkl file. Speeds up system as events are already embedded.

Kipp Freud
03/03/2020
'''

# ------------------------------------------------------------------

from util.message import message
import util.utilities as ut
import util.events as ents
import util.nlp_util as nlp
from util.events import HEADLINE_KEY
from util.events import TITLE_KEY, WEBLINK_KEY
from data import expand_recurring_events as hardcoded

# ------------------------------------------------------------------

PREPROCESSED_FILE_PATH_FULL = "preprocessed_ents_full.pkl"
PREPROCESSED_FILE_PATH_KNOWLE = "preprocessed_ents_knowle.pkl"

#PREPROCESS_TYPE = "FULL"
PREPROCESS_TYPE = "KNOWLE"
if PREPROCESS_TYPE == "FULL":
    FILE_PATH = PREPROCESSED_FILE_PATH_FULL
elif PREPROCESS_TYPE == "KNOWLE":
    FILE_PATH = PREPROCESSED_FILE_PATH_KNOWLE

# ------------------------------------------------------------------

def _getNewHeadline(event):
    headline = event[HEADLINE_KEY]
    title = event[TITLE_KEY]
    text = headline
    if text is None:
        text = title
    elif title is not None:
        if title != text:
            text += ": " + title
    return text


# Generate the next month's events from the handcoded timetable
new_ents = []
recurring_events = hardcoded.get_all_recurrers(days=90)
events_from_ents = ents.getEventsList()
if PREPROCESS_TYPE == "FULL":
    _events_list = ut.merge_events(events_from_ents, recurring_events)
elif PREPROCESS_TYPE == "KNOWLE":
    _events_list = ut.merge_events([], recurring_events)
for i, event in enumerate(_events_list):
    message.logDebug("Parsing event " + str(i) + "/" + str(len(_events_list)) + ".",
                     "preprocess_events::main")
    if WEBLINK_KEY in event.keys():
        n_h = _getNewHeadline(event)
        if n_h is not None:
            try:
                weblink = event[WEBLINK_KEY].replace("\\/", "/")
                description = ents.scrapeDescription(weblink,
                                                     n_h)
            except:
                description = [event[HEADLINE_KEY]]
            event["descriptions_embeddings"] = [(d, nlp.embed(d)) for d in description]
            if len(event["descriptions_embeddings"]) > 0:
                new_ents.append(event)

ut.save(new_ents, FILE_PATH)