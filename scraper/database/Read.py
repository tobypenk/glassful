class Read:
	
	def __init__(self, query_string):
		self.query_string = query_string
		
	def get_data(self,force_update=False):
		
		if force_update or not hasattr(self,"result"):
			
			from database.Connection import Connection
			from database.Credentials import Credentials
			
			creds = Credentials()
			
			con = Connection(
				host = creds.host,
				user = creds.user,
				pwd = creds.pwd,
				dbname = creds.dbname
			)
			
			self.result = []
			
			with con.connection() as connection:
				with connection.cursor() as cursor:
					cursor.execute(self.query_string)
					result = cursor.fetchall()
					for row in result:
						self.result.append(row)
					
		return self.result
		
	