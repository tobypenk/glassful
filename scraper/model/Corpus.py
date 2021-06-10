class Corpus:
	
	def __init__(self, corpus_file, global_hyperparameters, local_hyperparameters):
		self.corpus_file = corpus_file
		self.training_size = local_hyperparameters["training_size"]
		self.max_length = global_hyperparameters["max_length"]
		self.padding_type = global_hyperparameters["padding_type"]
		self.trunc_type = global_hyperparameters["trunc_type"]
		self.test_portion = global_hyperparameters["test_portion"]
		
	def read_corpus(self):
		import csv
		
		self.corpus = []
		with open(self.corpus_file, errors='ignore') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			next(reader)
			for row in reader:
				self.corpus.append(row)
	
	def separate_labels(self):
		import random
		
		self.sentences=[]
		self.labels=[]
		random.shuffle(self.corpus)
		for x in range(self.training_size):
		    self.sentences.append(self.corpus[x][0])
		    self.labels.append(int(self.corpus[x][1]))
		    
	def tokenize(self):
		from tensorflow.keras.preprocessing.text import Tokenizer
		from tensorflow.keras.preprocessing.sequence import pad_sequences
		
		self.tokenizer = Tokenizer()
		self.tokenizer.fit_on_texts(self.sentences)
		self.word_index = self.tokenizer.word_index
		self.vocab_size = len(self.word_index)
		self.sequences = self.tokenizer.texts_to_sequences(self.sentences)
		self.padded_sequences = pad_sequences(
			self.sequences, 
			maxlen=self.max_length, 
			padding=self.padding_type, 
			truncating=self.trunc_type
		)
		
		
	def split_into_training_and_test(self):
		import numpy as np
		
		split = int(self.test_portion * self.training_size)
		self.test_sequences = self.padded_sequences[0:split]
		self.training_sequences = self.padded_sequences[split:self.training_size]
		self.test_labels = self.labels[0:split]
		self.training_labels = self.labels[split:self.training_size]
		
		self.training_padded = np.array(self.training_sequences)
		self.training_labels = np.array(self.training_labels)
		self.testing_padded = np.array(self.test_sequences)
		self.testing_labels = np.array(self.test_labels)

		
	def initialize(self):
		self.read_corpus()
		self.separate_labels()
		self.tokenize()
		self.split_into_training_and_test()
		return self
		
		
		