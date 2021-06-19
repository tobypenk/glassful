class CocktailLinkScraper:
	
	def __init__(self):
		pass
		
	def alton_brown(self,filepath):
		
		# to implement caching
    
	    import urllib
	    from bs4 import BeautifulSoup, Comment
	    
	    cl = "recipe-item-detail"
	    links = []
	    soup = BeautifulSoup(open(filepath),'html.parser')
	    grid = soup.find_all("div", {"class": cl})
	    grid = BeautifulSoup(str(grid),'html.parser')
	
	    for a in grid.find_all("a",href=True):
	        links.append(a['href'])
	
	    self.alton_brown = links
	    return self.alton_brown
	    
	def bbc(self):
		
	    import urllib
	    from bs4 import BeautifulSoup, Comment
	    
	    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
	    headers={'User-Agent':user_agent,} 
	    bbcc = ["https://www.bbcgoodfood.com/search/recipes/?q=Cocktail+recipes&sort=-relevance"]
	    for i in range(2,11):
	        bbcc.append("https://www.bbcgoodfood.com/search/recipes/page/"+str(i)+"/?q=Cocktail+recipes&sort=-relevance")
	
	    cl = "standard-card-new__display-title"
	    bbcc_links = []
	
	    for s in bbcc:
	        print(s)
	        request = urllib.request.Request(s,None,headers)
	        f = urllib.request.urlopen(request)
	        file = f.read()
	        soup = BeautifulSoup(file,'html.parser')
	
	        grid = soup.find_all("h4", {"class": cl})
	        grid = BeautifulSoup(str(grid),'html.parser')
	
	        for a in grid.find_all("a",href=True):
	            bbcc_links.append("https://www.bbcgoodfood.com"+a['href'])
	
	    self.bbc = bbcc_links
	    return self.bbc
	    
	def serious_eats(self):
    
	    import urllib
	    from bs4 import BeautifulSoup, Comment
	    import numpy as np
	    import re
	    
	    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
	    headers={'User-Agent':user_agent,} 
	    
	    se = []
	    for i in range(1,45):
	        se.append("https://www.seriouseats.com/recipes/topics/meal/drinks/cocktails?page="+str(i)+"#recipes")
	
	    cl = "o-link-wrapper"
	
	    se_links = []
	
	    for s in se:
	        print(s)
	        request = urllib.request.Request(s,None,headers)
	        f = urllib.request.urlopen(request)
	        file = f.read()
	        soup = BeautifulSoup(file,'html.parser')
	
	        grid = soup.find_all("a", {"class": cl})
	        grid = BeautifulSoup(str(grid),'html.parser')
	
	        for a in grid.find_all('a', href=True):
	            se_links.append(a['href'])
	
	    se_links = list(filter(lambda x: re.search(r"/recipes/[0-9]{4}/[0-9]{2}",x), np.unique(se_links)))
	    self.serious_eats = se_links
	    return self.serious_eats
	    
	def cookie_and_kate(self):
    
	    import urllib
	    from bs4 import BeautifulSoup, Comment
	    
	    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
	    headers={'User-Agent':user_agent,} 
	    
	    tl = []
	    for i in range(1,6):
	        tl.append("https://cookieandkate.com/category/food-recipes/drinks/page/"+str(i)+"/")
	
	    cl = "lcp_catlist"
	
	    ck_links = []
	
	    for t in tl:
	        request = urllib.request.Request(t,None,headers)
	        f = urllib.request.urlopen(request)
	        file = f.read()
	        soup = BeautifulSoup(file,'html.parser')
	        grid = soup.find_all("div", {"class": cl})
	        grid = BeautifulSoup(str(grid),'html.parser')
	
	        for a in grid.find_all('a', href=True):
	            ck_links.append(a['href'])
	    
	    self.cookie_and_kate = ck_links
	    return self.cookie_and_kate
	    
	def spruce_eats(self):
	    
	    import urllib
	    from bs4 import BeautifulSoup, Comment
	    
	    files = []
	    for i in range(1,60):
	        files.append("../scraper_working_data/sp_c/"+str(i)+".html")
	    
	    cl = "results__item"
	    links = []
	    
	    for file in files:
	        print(file)
	        soup = BeautifulSoup(open(file),'html.parser')
	
	        grid = soup.find_all("li", {"class": cl})
	        grid = BeautifulSoup(str(grid),'html.parser')
	
	        for a in grid.find_all("a",href=True):
	            links.append(a['href'])
	
	    self.spruce_eats = np.unique(links)
	    return self.spruce_eats

	def mixthatdrink():
    
	    import urllib
	    from bs4 import BeautifulSoup, Comment
	    import numpy as np
	    import re
	    
	    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
	    headers={'User-Agent':user_agent,} 
	    
	    mt = ["https://mixthatdrink.com/category/cocktails/"]
	    for i in range(2,158):
	        mt.append("https://mixthatdrink.com/category/cocktails/page/"+str(i)+"/")
	
	    cl = "entry-title-link"
	
	    mt_links = []
	
	    for s in mt:
	        print(s)
	        request = urllib.request.Request(s,None,headers)
	        f = urllib.request.urlopen(request)
	        file = f.read()
	        soup = BeautifulSoup(file,'html.parser')
	
	        grid = soup.find_all("a", {"class": cl})
	
	        for a in grid:
	            mt_links.append(a['href'])
	    
	    mt_links = list(filter(lambda x: re.search(r"recipes|cocktails|drinks",x) == None, np.unique(mt_links)))
	
	    self.mixthatdrink = mt_links
	    return self.mixthatdrink





