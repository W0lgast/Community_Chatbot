'''
File for testing Allen NLP.

Kipp Freud
01/11/2019
'''

# --------------------------------

import allennlp as al
from allennlp.predictors.predictor import Predictor
import util.utilities as ut
from util.message import message
import util.events as ents
import requests as r
from ast import literal_eval as lit
import ast

# --------------------------------



events = ents.getEventsList(location="postcode:BS9 4EX",
                            radius_distance=10)
genres = []
for event in events:
    genres += event['genre']
genres = list(set(genres))

for genre in genres:
    message.logDebug(genre)
message.logDebug("Exiting successfully")
