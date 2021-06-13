def process_page(url,classifier,corpus,max_length,padding_type,trunc_type,threshold = 0.5):
	
	import re
	import urllib
	from bs4 import BeautifulSoup, Comment
	from tensorflow.keras.preprocessing.sequence import pad_sequences
	
	user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
	headers={'User-Agent':user_agent,}
	
	request = urllib.request.Request(url,None,headers)
	f = urllib.request.urlopen(request)
	file = f.read()
	soup = BeautifulSoup(file,'html.parser')
	
	for match in soup.findAll('span'):
		for p in match.findAll('p'):
			p.replace_with(' ' + p.text + ' ')
		match.replace_with(' ' + match.text + ' ')
	for match in soup.findAll('a'):
		match.replace_with(' ' + match.text + ' ')
	for match in soup.findAll('i'):
		match.replace_with(' ' + match.text + ' ')
	for match in soup.findAll('b'):
		match.replace_with(' ' + match.text + ' ')
	for match in soup.findAll('em'):
		match.replace_with(' ' + match.text + ' ')
	for match in soup.findAll('strong'):
		match.replace_with(' ' + match.text + ' ')
	for match in soup.findAll('br'):
		match.replace_with(' ' + match.text + ' ')
	for match in soup.findAll('time'):
		match.replace_with(' ' + match.text + ' ')
	for match in soup.findAll('dt'):
		match.replace_with(' ' + match.text + ' ')
	for match in soup.findAll('dd'):
		match.replace_with(' ' + match.text + ' ')
	for match in soup.findAll('sup'):
		match.replace_with(' ' + match.text + ' ')
	for match in soup.findAll('sub'):
		match.replace_with(' ' + match.text + ' ')
	for match in soup.findAll('li'):
		for p in match.findAll('p'):
			p.replace_with(' ' + p.text + ' ')
		for span in match.findAll('span'):
			span.replace_with(' ' + span.text + ' ')
		match.replace_with(BeautifulSoup(re.sub("[\s]+"," ",re.sub("<!-- -->"," ",str(match).strip())),'html.parser'))
	for match in soup.findAll('div',{'class':'ERSTime'}):
		for div in match.findAll('div'):
			div.replace_with(' ' + div.text + ' ')
		for p in match.findAll('p'):
			p.replace_with(' ' + p.text + ' ')

	soup = BeautifulSoup(str(soup),'html.parser')
	
	ingredients = []
	steps = []
	counter = 0
	total = []
	
	for string in soup.stripped_strings:
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
		
		tst_snt = [s]
		tst_snt = corpus.tokenizer.texts_to_sequences(tst_snt)
		tst_snt = pad_sequences(tst_snt, maxlen=max_length, padding=padding_type, truncating=trunc_type)
		pred = classifier.model.predict(tst_snt)
		
		if pred[0][1] > threshold:
			category = 1
			#print("step")
			ingredients.append([counter,s])
		elif pred[0][2] > threshold:
			category = 2
			#print("ingredient")
			ingredients.append([counter,s])
		elif pred[0][3] > threshold:
			category = 3
			#print("yield")
			ingredients.append([counter,s])
		elif pred[0][4] > threshold:
			category = 4
			#print("timing")
			ingredients.append([counter,s])
		else:
			category = 0
			
		#writer.writerow([string,pred[0][0],pred[0][1],pred[0][2],pred[0][3],pred[0][4],category,counter,url])
		total.append([string,pred[0][0],pred[0][1],pred[0][2],pred[0][3],pred[0][4],category,counter,url])
		
		counter += 1
	
	return total
	
	
	
	
	
	
	
	


def lasso_inward(df,gap_tolerance,target_column,target_value,count_column):
	# assumes the actual value is in the first column
	# returns the longest continuous range of target values
	
	last_match = False
	gap = 0
	total = []
	
	for i in range(1,len(df)):
		if len(df[i][0]) > 1e4:
			df[i][target_column] = 0
	
	df = list(filter(lambda x: x[target_column] == target_value, df))
	if (len(df) == 0): 
		return [[[""]]]
	subtotal = [df[0]]
	for i in range(1,len(df)):
		diff = df[i][count_column] - df[i-1][count_column]
		if diff > gap_tolerance:
			total.append(subtotal)
			subtotal = [df[i]]
		else:
			subtotal.append(df[i])
	if len(subtotal) > 0:
		total.append(subtotal)

	max_val = max([x for x in map(lambda x: len(x),total)])
	largest_range = list(filter(lambda x: len(x) == max_val, total))
	
	return largest_range
	
	
	
	
	
	
	
	
	
def lasso_outward(df,count_column,count_items):
	#returns the first parent of 
	None