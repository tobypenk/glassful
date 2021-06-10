import numpy

def scrape_spruce_eats_cocktail_links():
    
    files = []
    for i in range(1,60):
        files.append("scraper_working_data/sp_c/"+str(i)+".html")
    
    cl = "results__item"
    
    links = []
    
    for file in files:
        print(file)
        soup = BeautifulSoup(open(file),'html.parser')

        grid = soup.find_all("li", {"class": cl})
        grid = BeautifulSoup(str(grid),'html.parser')

        for a in grid.find_all("a",href=True):
            links.append(a['href'])

    return np.unique(links)
    
 
 
   



def scrape_cookie_and_kate_cocktail_links():
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
    
    return ck_links
    

def scrape_cookie_and_kate_links():
    tl = [
        "https://cookieandkate.com/category/food-recipes/entrees/"
    ]
    for i in range(2,13):
        tl.append("https://cookieandkate.com/category/food-recipes/entrees/page/"+str(i)+"/")

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
            print(a['href'])
            ck_links.append(a['href'])
    
    return ck_links
    
    
    


def scrape_ab_cocktail_links(filepath):
    
    cl = "recipe-item-detail"

    links = []

    soup = BeautifulSoup(open(filepath),'html.parser')

    grid = soup.find_all("div", {"class": cl})
    grid = BeautifulSoup(str(grid),'html.parser')

    for a in grid.find_all("a",href=True):
        links.append(a['href'])

    return links
    
#ab_cocktail_links = scrape_ab_cocktail_links("scraper_working_data/ab-cocktails.html")
    
    
    
    
    
def scrape_bbc_cocktail_links():
    bbcc = [
        "https://www.bbcgoodfood.com/recipes/collection/cocktail-recipes",
        "https://www.bbcgoodfood.com/recipes/collection/cocktail-recipes/2",
        "https://www.bbcgoodfood.com/recipes/collection/cocktail-recipes/3"
    ]

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
            bbcc_links.append(a['href'])

    return bbcc_links



def scrape_bbc_comfort_links():
    bbcc = [
        "https://www.bbcgoodfood.com/recipes/collection/comfort-food-recipes",
        "https://www.bbcgoodfood.com/recipes/collection/comfort-food-recipes/2",
        "https://www.bbcgoodfood.com/recipes/collection/comfort-food-recipes/3",
        "https://www.bbcgoodfood.com/recipes/collection/comfort-food-recipes/4"
    ]

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
            bbcc_links.append(a['href'])

    return bbcc_links
    
    

def scrape_bbc_vegan_breakfast_links():
    bbcc = [
        "https://www.bbcgoodfood.com/recipes/collection/vegan-breakfast-recipes",
        "https://www.bbcgoodfood.com/recipes/collection/vegan-breakfast-recipes/2"
    ]

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
            bbcc_links.append(a['href'])

    return bbcc_links





def scrape_serious_eats_cocktail_links():
    
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
    return se_links

def scrape_serious_eats_links():
    se = [
        "https://www.seriouseats.com/recipes/topics/cuisine"
    ]
    for i in range(2,20):
        se.append("https://www.seriouseats.com/recipes/topics/cuisine?page="+str(i)+"#recipes")

    cl = "c-cards"

    se_links = []

    for s in se:
        print(s)
        request = urllib.request.Request(s,None,headers)
        f = urllib.request.urlopen(request)
        file = f.read()
        soup = BeautifulSoup(file,'html.parser')

        grid = soup.find_all("section", {"class": cl})
        grid = BeautifulSoup(str(grid),'html.parser')

        for a in grid.find_all('a', href=True):
            se_links.append(a['href'])

    se_links = list(filter(lambda x: re.search(r"/recipes/[0-9]{4}/[0-9]{2}",x), np.unique(se_links)))
    return se_links
    
    
    
	
	
	
	
def scrape_google_search(filepath):
    
    cl = "a-no-hover-decoration"

    links = []

    soup = BeautifulSoup(open(filepath),'html.parser')

    grid = soup.find_all("a", {"class": cl})
    grid = BeautifulSoup(str(grid),'html.parser')

    for a in grid.find_all("a",href=True):
        links.append(a['href'])

    return links