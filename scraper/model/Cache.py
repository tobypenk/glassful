class Cache:
    
    def __init__(self):
        pass

    def get_ingredients(self):
        from database.Query import Query
        
        if not hasattr(self,'ingredients'):
            self.ingredients = Query("select singular_name, id from ingredient;").get_data()

        return self.ingredients