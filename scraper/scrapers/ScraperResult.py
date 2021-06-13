class ScraperResult:
	
	def __init__(self, title, steps, ingredients, recipe_yield, timing):
		self.title = title
		self.steps = steps
		self.ingredients = ingredients
		self.recipe_yield = recipe_yield
		self.timing = timing

	def get_payload(self):
		
		if not hasattr(self,"payload"):
			self.payload = {
				"title": self.title,
				"steps": self.steps,
				"ingredients": self.ingredients,
				"yield": self.recipe_yield,
				"timing": self.timing
			}
			
		return self.payload
		
	def map_payload_ingredients(self,ing_cache,corpus,classifier,global_hyperparameters):
		
		from tensorflow.keras.preprocessing.sequence import pad_sequences
		import numpy as np
		
		if not hasattr(self,"payload"):
			self.get_payload()
			
		if not hasattr(self.payload,"mapped_ingredients"):
		
			self.payload["mapped_ingredients"] = []
			
			tokens = corpus.tokenizer.texts_to_sequences(self.payload["ingredients"])
			tokens = pad_sequences(
				tokens, 
				maxlen=global_hyperparameters["max_length"], 
				padding=global_hyperparameters["padding_type"], 
				truncating=global_hyperparameters["trunc_type"]
			)
			
			pred = classifier.model.predict(tokens)
			
			for i in range(len(self.payload["ingredients"])):
				pred_id = np.argmax(pred[i])
				matched_ing = list(filter(lambda x: x[1] == pred_id,ing_cache))[0]
				self.payload["mapped_ingredients"].append([self.payload["ingredients"][i],matched_ing[0],pred_id])
				
		return self.payload
			