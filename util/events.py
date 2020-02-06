"""
Tools for gathering event info from ENTS24 API.

Kipp Freud
30/01/2020
"""

# --------------------------------

import requests as r

import util.utilities as ut

# --------------------------------

GENRE_SYNONYMS = {
    "Music": ["folk", "indie", "jazz", "acoustic", "rock", "country", "world", "pop", "rapandhiphop", "ska", "metal",
              "1960s", "1970s", "1980", "1990", "americana", "punk", "alternative", "rocknroll", "covers", "tribute",
              "blues", "rnbandsoul", "electronic"],
    "Standup Comedy": ["comedy"],
    "Theatre": ["theatreandarts", "play", "opera", "musical", "panto", "ballet", "ballroom", "westend"],
    "Shows & Events": ["adult", "cabaret", "showsandevents", "talk", "family", "circus", "magic", "poetry",
                       "sports", "tv", "online", "kids"],
    "Festivals": [],
    "Cinema": []}

# --------------------------------

CLIENT_ID = "2e16b35a18c40cf04711903c1efddfa03e315cd4"
CLIENT_SECRET = "4a7ba6ef8ea6c792e41f716087e6796ce530de08"
AUTHORIZATION_URL = 'https://api.ents24.com/auth/token'
response = r.post(AUTHORIZATION_URL,
                  data={'client_id': CLIENT_ID,
                        'client_secret': CLIENT_SECRET})
AUTH_DICT = ut.parseStr(response._content.decode())

# -----------------------------------------------------------------------------------------
# public functions
# -----------------------------------------------------------------------------------------

def getEventsList(location="postcode:BS4 1NL",
                  radius_distance=5,
                  date=None,
                  genre=None):
    if isinstance(genre, str): genre = genre.lower()
    params = {"location": location,
              "radius_distance": radius_distance,
              "distance_unit": "mi",
              "date": date,
              "genre": genre}
    params = {k: v for k, v in params.items() if v is not None}

    resp = r.get('https://api.ents24.com/event/list',
                 headers={"Authorization": AUTH_DICT["access_token"]},
                 params=params)
    ret = resp._content.decode()
    if ret == '': return []
    return ut.parseStr(ret)

def getEventByID(id):
    response = r.get('https://api.ents24.com/event/read',
                     headers={"Authorization": AUTH_DICT["access_token"]},
                     params={"id": id})
    str = response._content.decode()
    return ut.parseStr(str)