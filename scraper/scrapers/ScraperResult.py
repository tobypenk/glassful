class ScraperResult:
	
	def __init__(self, title, steps, ingredients, recipe_yield, timing):
		self.title = title
		self.steps = steps
		self.ingredients = ingredients
		self.recipe_yield = recipe_yield
		self.timing = timing

	def get_payload(self):
		self.payload = {
			"title": self.title,
			"steps": self.steps,
			"ingredients": self.ingredients,
			"yield": self.recipe_yield,
			"timing": self.timing
		}
		return self.payload

	def map_payload_to_known_ingredients(self,ing_cache,corpus,classifier):
		
		from tensorflow.keras.preprocessing.sequence import pad_sequences
		if hasattr(self,"payload") == False:
			self.get_payload()

		tokens = corpus.tokenizer.texts_to_sequences(self.payload.ingredients)
		# need to bring in max_length,padding_type,trunc_type
		tokens = pad_sequences(
			tokens, 
			maxlen=max_length, 
			padding=padding_type, 
			truncating=trunc_type
		)
		pred = classifier.model.predict(tokens)
		
		for i in range(len(self.payload.ingredients)):
			pred_id = np.argmax(pred[i])
			matched_ing = list(filter(lambda x: x[1] == pred_id,ing_cache))[0]
			self.payload.ingredients[i] = [self.payload.ingredients[i],matched_ing[0],pred_id]
			    
			    