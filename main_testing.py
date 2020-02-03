'''
File for testing Allen NLP.

Kipp Freud
01/11/2019
'''

# --------------------------------

import allennlp as al
from allennlp.predictors.predictor import Predictor
import util.utilities as ut
import util.events as ents
import requests as r
from ast import literal_eval as lit
import ast

# --------------------------------

events = ents.getEventsList()
for event in events:
    event['description'] = ents.getEventByID(event["id"])['description']
