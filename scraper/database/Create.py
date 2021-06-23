class Create:
	
	def __init__(self,query_string,return_insert_id = False):
		self.query_string = query_string
		self.return_insert_id = return_insert_id
		
	def get_data(self):
		
		if not hasattr(self,"result"):
			self.insert()
			
		return self.result
		
		
	def insert(self):
			
		from database.Connection import Connection
		from database.Credentials import Credentials
		
		creds = Credentials()
		
		con = Connection(
			host = creds.host,
			user = creds.user,
			pwd = creds.pwd,
			dbname = creds.dbname
		)
		
		try:
		
			with con.connection() as connection:
				with connection.cursor() as cursor:
					cursor.execute(self.query_string)
					result = cursor.fetchall()
					
			if self.return_insert_id:
				insert_id = self.get_insert_id()
			else:
				insert_id = None	
					
		except Exception as e:
			result = e
			insert_id = None
		
		self.result = {
			"result": result,
			"insert_id": insert_id
		}
		
		
	def get_insert_id(self):
		
		from database.Connection import Connection
		from database.Credentials import Credentials
		import re
		
		creds = Credentials()
		
		con = Connection(
			host = creds.host,
			user = creds.user,
			pwd = creds.pwd,
			dbname = creds.dbname
		)
		
		insert_result = []
		table = re.search("(?<=insert into )(.*?)(?= )",self.query_string.lower()).group(0)
		last_insert_query_string = "SELECT max(id) last_insert_id FROM "+table+";"
			
		with con.connection() as connection:
			with connection.cursor() as cursor:
				cursor.execute(last_insert_query_string)
				result = cursor.fetchall()
				for row in result:
					insert_result.append(row)
		
		return insert_result[0][0]
		
		
		
		
		
		
		
		
		
		
		