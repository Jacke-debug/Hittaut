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
nFailedVinstsida=0 # number of "sida saknas" for vinstdragningar
n_dates=0 # number of "Dates (successfully?) extracted"
n_heading=0 # number of times dates extracted with heading based method
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
        print('method',end=' <> ')
        if ortDict["method"] == 0:
            print('brute force')
            n_heading+=1
        elif ortDict["method"] == -1:
            print('no winners page')
            nFailedVinstsida+=1
        else:
            print('heading based')
        print('nCheckpts',end=' <> ')
        if ortDict["nCheckpts"] == -1:
            print('fail')
        else:
            n_nCheckpts+=1
            print('success?')

# sort on start date
listOfDicts = sorted(listOfDicts, key=lambda k: k['Start']) 

total = len(pageMenu)
loaded = total-nFailed
loaded_winner = loaded-nFailedVinstsida

print('Loaded main pages: ', loaded,'/',total)
print('Loaded winners pages: ', loaded_winner,'/',loaded)
print('"dragningar" extracted: ', n_dates,'/',loaded)
print('Heading based extraction: ', n_heading,'/',loaded)
print('"nCheckpts" extracted: ', n_nCheckpts,'/',loaded)


filename=dictsToExcel.main(listOfDicts)
print('Successully created: ',filename)