class PageProcessor:
	
	def __init__(self,url,classifier,corpus,global_hyperparameters,writer,threshold = 0.5):
		self.url = url
		self.writer = writer
		self.classifier = classifier
		self.corpus = corpus
		self.global_hyperparameters = global_hyperparameters
		self.threshold = threshold
		self.user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
		self.headers={'User-Agent':self.user_agent,}
		
		
	def local_url_path(self):
		from os.path import join
		if not hasattr(self,"url_local"):
			import re
			self.url_local = re.sub('\\.|/|:', '', self.url)
			
		return self.url_local
		
		
	def fetch_page_data(self):
		
		from os import listdir
		from os.path import isfile, join
		cached_pages = [file for file in listdir("site_data_cache") if isfile(join("site_data_cache",file))]
		
		if self.local_url_path() in cached_pages:
			print("local")
			self.file_data = open(join("site_data_cache",self.local_url_path()))
		else:
			print("remote")
			import urllib
			import re
			
			request = urllib.request.Request(self.url,None,self.headers)
			f = urllib.request.urlopen(request)
			self.file_data = f.read()
			
			write_file = open(join("site_data_cache",self.local_url_path()),"wb")
			write_file.write(self.file_data)
			write_file.close()
		
		
	def soupify(self):
		
		if not hasattr(self,"file_data"):
			self.fetch_page_data()
			
		from bs4 import BeautifulSoup, Comment
		self.soup = BeautifulSoup(self.file_data,'html.parser')
		self.extract_texts()
		self.clean_string_characters()
		self.classify_strings()
	
	
	def extract_texts(self):
		
		from bs4 import BeautifulSoup, Comment
		import re
		
		for match in self.soup.findAll('span'):
			for p in match.findAll('p'):
				p.replace_with(' ' + p.text + ' ')
			match.replace_with(' ' + match.text + ' ')
		for match in self.soup.findAll('a'):
			match.replace_with(' ' + match.text + ' ')
		for match in self.soup.findAll('i'):
			match.replace_with(' ' + match.text + ' ')
		for match in self.soup.findAll('b'):
			match.replace_with(' ' + match.text + ' ')
		for match in self.soup.findAll('em'):
			match.replace_with(' ' + match.text + ' ')
		for match in self.soup.findAll('strong'):
			match.replace_with(' ' + match.text + ' ')
		for match in self.soup.findAll('br'):
			match.replace_with(' ' + match.text + ' ')
		for match in self.soup.findAll('time'):
			match.replace_with(' ' + match.text + ' ')
		for match in self.soup.findAll('dt'):
			match.replace_with(' ' + match.text + ' ')
		for match in self.soup.findAll('dd'):
			match.replace_with(' ' + match.text + ' ')
		for match in self.soup.findAll('sup'):
			match.replace_with(' ' + match.text + ' ')
		for match in self.soup.findAll('sub'):
			match.replace_with(' ' + match.text + ' ')
		for match in self.soup.findAll('li'):
			for p in match.findAll('p'):
				p.replace_with(' ' + p.text + ' ')
			for span in match.findAll('span'):
				span.replace_with(' ' + span.text + ' ')
			match.replace_with(BeautifulSoup(re.sub("[\s]+"," ",re.sub("<!-- -->"," ",str(match).strip())),'html.parser'))
		for match in self.soup.findAll('div',{'class':'ERSTime'}):
			for div in match.findAll('div'):
				div.replace_with(' ' + div.text + ' ')
			for p in match.findAll('p'):
				p.replace_with(' ' + p.text + ' ')
	
		self.soup = BeautifulSoup(str(self.soup),'html.parser')


	def clean_string_characters(self):
		
		import re
		
		for string in self.soup.stripped_strings:
			s = re.sub('[\s]+', ' ', string).replace("\n"," ").replace(u'\xa0', u' ')
			s = re.sub(r'\([^)]*\)', '', s).strip()
			s = re.sub(r'(?<=\d)(?=[a-zA-Z])|(?<=[a-zA-Z])(?=\d)'," ", s).strip()
			s = s.replace("-"," ")
			s = s.replace("½","1/2")
			s = s.replace("⅓","1/3")
			s = s.replace("⅔","2/3")
			s = s.replace("¼","1/4")
			s = s.replace("¾","3/4")
			
			string = string.replace("\n"," ").replace(u'\xa0', u' ')
			string = re.sub('[\s]+', ' ', string)
			string = re.sub(r'\([^)]*\)', '', string).strip()
			string = re.sub(r'(?<=\d)(?=[a-zA-Z])|(?<=[a-zA-Z])(?=\d)'," ", string).strip()
			string = string.replace("-"," ")
			string = string.replace("½","1/2")
			string = string.replace("⅓","1/3")
			string = string.replace("⅔","2/3")
			string = string.replace("¼","1/4")
			string = string.replace("¾","3/4")
	
	
	
	def classify_strings(self):
		
		from bs4 import BeautifulSoup, Comment
		from tensorflow.keras.preprocessing.sequence import pad_sequences
		
		self.ingredients = []
		self.steps = []
		counter = 0
		self.classifications = []
		
		for s in self.soup.stripped_strings:
		
			tst_snt = [s]
			tst_snt = self.corpus.tokenizer.texts_to_sequences(tst_snt)
			tst_snt = pad_sequences(
				tst_snt, 
				maxlen = self.global_hyperparameters["max_length"], 
				padding = self.global_hyperparameters["padding_type"], 
				truncating = self.global_hyperparameters["trunc_type"]
			)
			pred = self.classifier.model.predict(tst_snt)
		
			if pred[0][1] > self.threshold:
				category = 1
				self.ingredients.append([counter,s])
			elif pred[0][2] > self.threshold:
				category = 2
				self.ingredients.append([counter,s])
			elif pred[0][3] > self.threshold:
				category = 3
				self.ingredients.append([counter,s])
			elif pred[0][4] > self.threshold:
				category = 4
				self.ingredients.append([counter,s])
			else:
				category = 0
				
			self.writer.writerow([s,category,counter,pred[0][0],pred[0][1],pred[0][2],pred[0][3],pred[0][4],self.url])
			self.classifications.append([s,category,counter,pred[0][0],pred[0][1],pred[0][2],pred[0][3],pred[0][4],self.url])
			
			counter += 1
			
			
			
			
	
			