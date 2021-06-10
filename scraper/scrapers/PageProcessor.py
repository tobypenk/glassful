class PageProcessor:
	
	def __init__(self,url,writer,classifier,corpus,max_length,padding_type,trunc_type,threshold = 0.5):
		self.url = url
		self.writer = writer
		self.classifier = classifier
		self.corpus = corpus
		self.max_length = max_length
		self.padding_type = padding_type
		self.trunc_type = trunc_type
		self.user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
		self.headers={'User-Agent':self.user_agent,}
		
	def soupify_url(self):
		import urllib
		from bs4 import BeautifulSoup, Comment
		
		request = urllib.request.Request(self.url,None,headers)
		f = urllib.request.urlopen(request)
		file = f.read()
		self.soup = BeautifulSoup(file,'html.parser')
	
	
	def extract_texts(self):
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
			match.replace_with(Beautifulsoup(re.sub("[\s]+"," ",re.sub("<!-- -->"," ",str(match).strip())),'html.parser'))
		for match in self.soup.findAll('div',{'class':'ERSTime'}):
			for div in match.findAll('div'):
				div.replace_with(' ' + div.text + ' ')
			for p in match.findAll('p'):
				p.replace_with(' ' + p.text + ' ')
	
		self.soup = Beautifulsoup(str(self.soup),'html.parser')
	
	#import re
	#import urllib
	#from bs4 import Beautifulsoup, Comment
	#from tensorflow.keras.preprocessing.sequence import pad_sequences
	
	def clean_string_characters(self):
		import re
		
		self.ingredients = []
		self.steps = []
		self.counter = 0
		self.total = []
		
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
			
			if pred[0][1] > threshold:
				category = 1
				ingredients.append([counter,s])
			elif pred[0][2] > threshold:
				category = 2
				ingredients.append([counter,s])
			elif pred[0][3] > threshold:
				category = 3
				ingredients.append([counter,s])
			elif pred[0][4] > threshold:
				category = 4
				ingredients.append([counter,s])
			else:
				category = 0
				
			writer.writerow([string,category,counter,pred[0][0],pred[0][1],pred[0][2],pred[0][3],pred[0][4],url])
			total.append([string,category,counter,pred[0][0],pred[0][1],pred[0][2],pred[0][3],pred[0][4],url])
			
			counter += 1
			
			