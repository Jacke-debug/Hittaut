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
n_dates=0 # number of "Dates (successfully?) extracted"
n_nCheckpts=0 # number of "nCheckpts (successfully?) extracted"
listOfDicts=list()
for item in pageMenu:
    webPage = basePage + item.a["href"]

    ortDict = hittaut.main(webPage)

    if ortDict is None:
        nFailed+=1
    else:
        listOfDicts.append(ortDict)
        print('draws',end=' <> ')
        if len(ortDict["draws"]) == 0:
            print('fail')
        else:
            n_dates+=1
            print('success?')
        print('nCheckpts',end=' <> ')
        if ortDict["nCheckpts"] == -1:
            print('fail')
        else:
            n_nCheckpts+=1
            print('success?')

total = len(pageMenu)
loaded = total-nFailed

print('Loaded pages: ', loaded,'/',total)
print('Date sets: ', n_dates,'/',loaded)
print('nCheckpts sets: ', n_nCheckpts,'/',loaded)


filename=dictsToExcel.main(listOfDicts)
print('Successully created: ',filename)