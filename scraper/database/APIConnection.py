class APIConnection:
	
	def __init__(self,base_url):
		self.base_url = base_url
		
	def call(self):
		
		import urllib
		from urllib.parse import unquote
		import json
		
		request = urllib.request.Request(self.base_url,None)
		f = urllib.request.urlopen(request)
		j = json.loads(f.read())
		
		self.total = []
		for row in j:
			self.total.append(unquote(row))
			
		return self.total