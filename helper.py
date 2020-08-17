from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import datetime
import hittaut
import requests
from requests.exceptions import HTTPError

# "manadsvinnare"
my_url = "https://www.orientering.se/provapaaktiviteter/hittaut/"

# opening up connection, grabbing the page
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

# html parsing
page_soup = soup(page_html, "html.parser")

# grabs each product
pageMenu = page_soup.find("ul",{"class":"secondary-topmenu__submenu regions"}).findAll("li", {"class":"secondary-topmenu__submenu-item"})

basePage = "https://www.orientering.se/"
nFail=0
for item in pageMenu:
    try:
        webPage = basePage + item.a["href"] + "manadsvinnare/" # some cities uses "vinstdragning/" as extension
        r = requests.get(webPage)
        r.raise_for_status()
    except HTTPError:
        try: 
            webPage = basePage + item.a["href"] + "vinstdragning/"
            r = requests.get(webPage)
            r.raise_for_status()
        except HTTPError:
            print(item)
            print('Could not download page')
            nFail+=1
            continue
    print(r.url, 'downloaded successfully')
    hittaut.main(webPage)

print('Loaded pages: ', nFail,'/',len(pageMenu))