'''
File for testing Allen NLP.

Kipp Freud
01/11/2019
'''

# --------------------------------

import allennlp as al
from allennlp.predictors.predictor import Predictor

# --------------------------------

predictor = Predictor.from_path("https://storage.googleapis.com/allennlp-public-models/bidaf-elmo-model-2018.11.30-charpad.tar.gz")
res = predictor.predict(
  passage="her vision said 'hello!'",
  question="What did Penelope's vision say?"
)
print("yo")
