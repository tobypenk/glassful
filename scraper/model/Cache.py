class Cache:
    
    def __init__(self):
        pass

    def get_ingredients(self):
        from database.Query import Query
        
        if not hasattr(self,'ingredients'):
            self.ingredients = Query("select singular_name, id from ingredient;").get_data()

        return self.ingredients
        
    def get_measures(self):
        from database.Query import Query
        
        if not hasattr(self,'measures'):
            self.measures = Query("select "+
            	"short_name "+
            	", long_name "+
            	", plural_name "+
            	", long_plural "+
            	"from measure where is_common = 1;").get_data()

        return self.measures