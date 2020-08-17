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
nSuccessful=0
nEmpty=0
listOfDicts=list()
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
            continue
    print(r.url, 'downloaded successfully')
    nSuccessful+=1

    ortDict = hittaut.main(webPage)
    listOfDicts.append(ortDict)

    if len(ortDict["draws"]) == 0:
        nEmpty+=1
        print('No dates found.')
    else:
        print('Dates (successfully?) extracted')
        

print('Loaded pages: ', nSuccessful,'/',len(pageMenu))
print('Non-empty date sets: ', len(pageMenu)-nEmpty,'/',len(pageMenu))


filename=dictsToExcel.main(listOfDicts)
print('Successully created: ',filename)