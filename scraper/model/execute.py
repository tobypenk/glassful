import json
import random
import re
import numpy as np
import tensorflowjs as tfjs
from model.Corpus import Corpus
from model.Model import Model
from model.Embeddings import Embeddings

from tensorflow.keras.utils import to_categorical
from tensorflow.keras import regularizers

# Dimensions in the GloVe embedding
embedding_dim = 100
# Enforced max and min length of an example
max_length = 60
# truncate from the end where necessary
trunc_type='post'
# pad to the end where necessary
padding_type='post'
oov_tok = "<OOV>"

num_epochs = 1

# number of training examples to use
training_size= 62000
test_portion=.1

corpus = Corpus(
	"training_data/augmented_training_labels.csv",
	training_size,
	max_length,
	padding_type,
	trunc_type,
	test_portion
).initialize()


embeddings = Embeddings(
	"glove.6B.100d.txt",
	embedding_dim,
	corpus
).activate()
       



classifier = Model(
	corpus,
	embeddings,
	max_length,
	num_epochs
).run()






