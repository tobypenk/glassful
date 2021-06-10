class Model:
	
	def __init__(self,corpus,embeddings,global_hyperparameters,local_hyperparameters,number_of_categories):
		self.corpus = corpus
		self.embeddings = embeddings
		self.max_length = global_hyperparameters["max_length"]
		self.num_epochs = local_hyperparameters["num_epochs"]
		self.number_of_categories = number_of_categories

	def initialize(self):
		import tensorflow as tf
		
		self.model = tf.keras.Sequential([
		    tf.keras.layers.Embedding(
		        self.corpus.vocab_size+1, 
		        self.embeddings.embedding_dim, 
		        input_length=self.max_length, 
		        weights=[self.embeddings.embeddings_matrix], 
		        trainable=False
		    ),
		    tf.keras.layers.Dropout(0.2),
		    tf.keras.layers.Conv1D(64, 4, activation='relu'),
		    tf.keras.layers.MaxPooling1D(pool_size=4),
		    #tf.keras.layers.LSTM(128),
		    tf.keras.layers.Bidirectional(tf.keras.layers.GRU(256,return_sequences=False)),
		    tf.keras.layers.Dense(self.number_of_categories, activation='softmax')
		])
		
	def compile_model(self):
		self.model.compile(
		    loss='sparse_categorical_crossentropy',
		    optimizer='adam',
		    metrics=['accuracy']
		)
		
		num_epochs = 1

	def fit(self):
		self.history = self.model.fit(
		    self.corpus.training_padded, 
		    self.corpus.training_labels, 
		    epochs=self.num_epochs, 
		    validation_data=(self.corpus.testing_padded, self.corpus.testing_labels), 
		    verbose=1
		)
			
	def run(self):
		self.initialize()
		self.compile_model()
		self.fit()
		return self



