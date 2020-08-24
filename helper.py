from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import datetime
import hittaut
import dictsToExcel
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
nFailed=0 # number of "failed to load webpage"
nEmpty=0 # number of "failed to find any dates"
listOfDicts=list()
for item in pageMenu:
    webPage = basePage + item.a["href"]

    ortDict = hittaut.main(webPage)

    if ortDict is None:
        nFailed+=1
    else:
        listOfDicts.append(ortDict)
        if len(ortDict["draws"]) == 0:
            nEmpty+=1
            print('No dates found.')
        else:
            print('Dates (successfully?) extracted')
        

print('Loaded pages: ', len(pageMenu)-nFailed,'/',len(pageMenu))
print('Non-empty date sets: ', len(pageMenu)-nEmpty,'/',len(pageMenu))


filename=dictsToExcel.main(listOfDicts)
print('Successully created: ',filename)