class Connection:
	
	def __init__(self,host,user,pwd,dbname):
		self.host = host
		self.user = user
		self.pwd  = pwd
		self.dbname = dbname
		
		
	def connection(self):
		from mysql.connector import connect, Error
		
		return connect(
			host=self.host,
			user=self.user,
			password=self.pwd,
			database=self.dbname
		)