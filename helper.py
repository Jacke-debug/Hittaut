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
pageMenu = page_soup.findAll("li", {"class":"secondary-topmenu__submenu-item"})

basePage = "https://www.orientering.se/"
for item in pageMenu:
    webPage = basePage + item.a["href"] + "manadsvinnare/" # some cities uses "vinstdragning/" as extension
    # TODO: Add check if page exists or if it should be something else at the end..
    try:
        r = requests.get(webPage)
        r.raise_for_status()
    except HTTPError:
        print('Could not download page')
    else:
        print(r.url, 'downloaded successfully')
        hittaut.main(webPage)
    