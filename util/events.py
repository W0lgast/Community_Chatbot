"""
Tools for gathering event info from ENTS24 API.

Kipp Freud
30/01/2020
"""

# --------------------------------

import requests as r
from bs4 import BeautifulSoup

import util.utilities as ut
from util.message import message

# --------------------------------

GENRE_SYNONYMS = {
    "Music": ["folk", "indie", "jazz", "acoustic", "rock", "country", "world", "pop", "rapandhiphop", "ska", "metal",
              "1960s", "1970s", "1980", "1990", "americana", "punk", "alternative", "rocknroll", "covers", "tribute",
              "blues", "rnbandsoul", "electronic"],
    "Comedy": ["comedy"],
    "Theatre": ["theatreandarts", "play", "opera", "musical", "panto", "ballet", "ballroom", "westend"],
    "Shows & Events": ["adult", "cabaret", "showsandevents", "talk", "family", "circus", "magic", "poetry",
                       "sports", "tv", "online", "kids"]}

# --------------------------------

CLIENT_ID = "2e16b35a18c40cf04711903c1efddfa03e315cd4"
CLIENT_SECRET = "4a7ba6ef8ea6c792e41f716087e6796ce530de08"
AUTHORIZATION_URL = 'https://api.ents24.com/auth/token'
response = r.post(AUTHORIZATION_URL,
                  data={'client_id': CLIENT_ID,
                        'client_secret': CLIENT_SECRET})
AUTH_DICT = ut.parseStr(response._content.decode())

DEFAULT_HEADERS = {'User-Agent':'Mozilla/5.0'}

# --------------------------------

START_DATE = "startDate"
END_DATE = "endDate"
GENRE_KEY = "genre"
HEADLINE_KEY = "headline"
TITLE_KEY = "title"
IMAGE_KEY = "image"
IMAGE_URL_KEY = "url"
WEBLINK_KEY = "webLink"

# -----------------------------------------------------------------------------------------
# public functions
# -----------------------------------------------------------------------------------------

def getEventsList(location="postcode:BS4 1NL",
                  radius_distance=5,
                  date=None,
                  genre=None):
    if isinstance(genre, str):
        genre = genre.lower()
        if genre not in [g.lower() for g in GENRE_SYNONYMS.keys()]:
            message.logError("Unknown Genre", "events::getEventsList")
            ut.exit(0)
    params = {"location": location,
              "radius_distance": radius_distance,
              "distance_unit": "mi",
              "date": date,
              "genre": genre}
    params = {k: v for k, v in params.items() if v is not None}
    if "genre" in params.keys():
        if isinstance(params["genre"], list):
            new_g = [GENRE_SYNONYMS[g.capitalize()] for g in params["genre"]]
            new_g = [item for sublist in new_g for item in sublist]
            params["genre"] = new_g
        else:
            new_g = GENRE_SYNONYMS[params["genre"]]
            params["genre"] = new_g
    all_params = _generateParams(params)
    all_events = []
    all_ids = []
    for p in all_params:
        evs = _getEvents(p)
        for ev in evs:
            if ev["id"] not in all_ids:
                all_events.append(ev)
                all_ids.append(ev["id"])
    return all_events

def getEventByID(id):
    response = r.get('https://api.ents24.com/event/read',
                     headers={"Authorization": AUTH_DICT["access_token"]},
                     params={"id": id})
    str = response._content.decode()
    return ut.parseStr(str)

def scrapeDescription(weblink):
    """
    Will scrape the full text description of the event from the given weblink.

    :param weblink: The ents24 web address of the event.
    :return: The string description of the event.
    """
    response = r.get(weblink, headers=DEFAULT_HEADERS)
    websoup = BeautifulSoup(response.text, "html.parser")
    tag = websoup.find(True, {"class":'fat-column'})
    desc_text_sections = [t for t in tag.find_all("p") if t not in \
                          tag.find_all("p", {"class": ["with-side-padding", "text-center", "text-dull"]})]
    descs = [d_t.contents[0] for d_t in desc_text_sections if isinstance(d_t.contents[0], str)]
    return descs

# -----------------------------------------------------------------------------------------
# private functions
# -----------------------------------------------------------------------------------------

def _generateParams(param_dict):
    """
    Will take a dictionary, where *potentially* some values are lists. Will return a list of dictionaries
    with no lists, where each possible list member combination is included.
    """
    keys = param_dict.keys()
    list_key = None
    for key in keys:
        if isinstance(param_dict[key], list):
            list_key = key
            break
    if list_key is None:
        return [param_dict]
    new_dics = []
    for list_val in param_dict[list_key]:
        new_dict = {}
        for key in keys:
            if key is not list_key:
                new_dict[key] = param_dict[key]
            else:
                new_dict[key] = list_val
        new_dics.append(new_dict)
    ret = []
    for dic in new_dics:
        ret += _generateParams(dic)
    return ret

def _getEvents(params):
    """
    Gets the events form the ENTS24 API. Returns events dict.
    """
    params["results_per_page"] = 100
    params["full_description"] = 1
    resp = None
    ret = []
    while True:
        if resp is not None:
            params["page"] = resp.headers._store["x-next-page"][1]
        resp = r.get('https://api.ents24.com/event/list',
                     headers={"Authorization": AUTH_DICT["access_token"]},
                     params=params)
        if resp.status_code not in [200, 204]:
            message.logError("Error code in response.", "events::getEventsList")
            ut.exit(0)
        lst = resp._content.decode()
        if lst == '':
            return ret
        lst = ut.parseStr(lst)
        ret += lst
