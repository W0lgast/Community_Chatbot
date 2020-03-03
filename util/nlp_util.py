'''
NLP utility functions e.g sentence embedding functions.

Kipp Freud
12/02/2020
'''

#------------------------------------------------------------------

import sister
import numpy as np

from util.message import message
import util.utilities as ut

#------------------------------------------------------------------

EMBEDDER = sister.MeanEmbedding(lang="en")

#------------------------------------------------------------------

# -----------------------------------------------------------------------------------------
# public functions
# -----------------------------------------------------------------------------------------

@ut.timeit
def embed(sent):
    """
    Will return a vector embedding of the given string sentence.
    """
    if not isinstance(sent, str):
        message.logError("Given sentence must be a string.", "nlp_util::embed")
        ut.exit(0)
    return EMBEDDER(sent)

def compare_embeddings(emb_1, emd_2):
    """
    Returns the euclidean distance between emb_1 and emb_2.
    """
    return np.linalg.norm(emb_1 - emd_2)