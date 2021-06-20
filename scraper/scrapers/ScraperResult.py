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
		
	def map_payload_ingredients(self,ing_cache,msr_cache,corpus,classifier,global_hyperparameters):
		
		from tensorflow.keras.preprocessing.sequence import pad_sequences
		import numpy as np
		import re
		
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
			
				tmp_ing = self.clean_raw_string(self.payload["ingredients"][i])
				try:
					q = self.extract_quantity(tmp_ing)
				except:
					q = "UNKNOWN_QUANTITY"
					
				msr = "UNKNOWN_MEASURE"
				for m in msr_cache:
				    if re.search("(?<=[0-9]| )("+"|".join(m).lower()+")(?= )",tmp_ing[0:12].lower()) or re.search("^("+"|".join(m).lower()+")(?= )",tmp_ing[0:12].lower()):
				        msr = m[0]
				        break
					
				pred_id = np.argmax(pred[i])
				matched_ing = list(filter(lambda x: x[1] == pred_id,ing_cache))[0]
				self.payload["mapped_ingredients"].append([
					self.payload["ingredients"][i],
					q,
					msr,
					matched_ing[0],
					pred_id
				])
				
		return self.payload
		
		

	def extract_quantity(self,s):
	    import re
	    
	    s = s.lower()
	    
	    if len(s) == 0:
	        q = 0
	    elif (re.match("[a-z]",s[0])):
	        q = 1
	    elif (re.search("\\.",s[0:7])):
	        q = float(re.sub("[a-z]","",s[0:7]))
	    else:
	        q = re.sub("[a-z]","",s[0:7]).strip()
	        q = q.split(" ")
	        if (len(q) == 1):
	            q = q[0]
	            if (re.search("/",q)):
	                q = q.split("/")
	                n = int(q[0])
	                d = int(q[1])
	                q = n/d
	            else:
	                q = int(q)
	        else:
	            if (re.search("/",q[1])):
	                f = q[1].split("/")
	                n = int(f[0])
	                d = int(f[1])
	                if re.search("/",q[0]):
	                    q = n/d
	                else:
	                    q = int(q[0]) + n/d
	            else:
	                return int(q[0])
	
	    return q



	def clean_raw_string(self,s):
		
	    import re
	    
	    s = s.lower()
	    
	    s = re.sub("(?<=\\()(.*?)(?=\\))","",s)
	    s = re.sub("\\(","",s)
	    s = re.sub("\\)","",s)
	    s = re.sub("(?<=, such as)(.*?)$","",s)
	    s = re.sub(", such as","",s)
	    s = re.sub("é","e",s)
	    s = re.sub("è","e",s)
	    s = re.sub("î","i",s)
	    s = re.sub("'","",s)
	    s = re.sub("’","",s)
	    s = re.sub("(?<=[a-zA-Z])/"," ",s)
	    s = re.sub("/(?=[a-zA-Z])"," ",s)
	
	    s = re.sub("½"," 1/2",s)
	    s = re.sub("⅓"," 1/3",s)
	    s = re.sub("¼"," 1/4",s)
	    s = re.sub("¾"," 3/4",s)
	
	    s = re.sub("⅔"," 2/3",s)
	    s = re.sub("⅛"," 1/8",s)
	    s = re.sub("⅜"," 3/8",s)
	    s = re.sub("⅝"," 5/8",s)
	    s = re.sub("⅞"," 7/8",s)
	    s = re.sub("⅒"," 1/10",s)
	
	    s = re.sub("ﬁ","fi",s)
	    s = re.sub("ç","c",s)
	    s = re.sub("ñ","n",s)
	    s = re.sub("\\*","",s)
	    s = re.sub("û","u",s)
	
	    s = re.sub("^a few"," 3",s)
	
	    s = re.sub("(?<=\\d) - \\d+\\/\\d+","",s)
	    s = re.sub("(?<=\\d) - \\d+","",s)
	    s = re.sub("(?<=\\d)- \\d+\\/\\d+","",s)
	    s = re.sub("(?<=\\d)- \\d+","",s)
	    s = re.sub("(?<=\\d) -\\d+\\/\\d+","",s)
	    s = re.sub("(?<=\\d) -\\d+","",s)
	    s = re.sub("(?<=\\d)-\\d+\\/\\d+","",s)
	    s = re.sub("(?<=\\d)-\\d+","",s)
	    s = re.sub("(?<=\\d) to \\d+\\/\\d+","",s)
	    s = re.sub("(?<=\\d) to \\d+","",s)
	    s = re.sub("(?<=\\d) or \\d+\\/\\d+","",s)
	    s = re.sub("(?<=\\d) or \\d+","",s)
	    s = re.sub("(?<=\\d) and (?=\\d+)"," ",s)
	
	    s = re.sub("-"," ",s)
	    s = re.sub(" +"," ",s)
	    s = re.sub("approximately","",s)
	    s = re.sub("^about","",s)
	
	    s = re.sub("\\s+"," ",s)
	    s = re.sub("barspoon","teaspoon",s)
	    s = re.sub("brulee torch","kitchen torch",s)
	    
	    return s.strip()
	    
	    
	    
	    