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
import util.nlp_util as nlp

# --------------------------------

vector = nlp.embed("I love to do sentence embeddings!")  # 300-dim vector

ut.exit(1)