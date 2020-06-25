from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import datetime


def findDate(winnerDatesStr):
    winnerDatesStr = winnerDatesStr.lower()
    # assumes month to be written as a word
    month = monthParser(winnerDatesStr)
    print(winnerDatesStr)
    # extract numbers from the string
    numbers = [int(s) for s in str.split(winnerDatesStr) if s.isdigit()]
    if len(numbers) == 1:
        # use the one number as a date
        date = numbers[0]
        month = 1
    else:
        # string contains more than one number
        # may be a numbering of the dates i.e. 1. 2. 3.. 
        # or that the month is written with a number
        # or possibly both..
        date = 1
        if month == 0:
            # month is written as a number not a word
            # do something clever
            month = 1
        pass
    x = datetime.datetime(2020, month, date)
    return x

def monthParser(winnerDatesStr):
    month = 0
    if "maj" in winnerDatesStr:
        month = 5
    elif "juni" in winnerDatesStr:
        month = 6
    elif "juli" in winnerDatesStr:
        month = 7
    elif "augusti" in winnerDatesStr:
        month = 8
    elif "september" in winnerDatesStr:
        month = 9
    return month

def main(my_url): 
    # opening up connection, grabbing the page
    try:
        uClient = uReq(my_url)
    except:
        exit

    page_html = uClient.read()
    uClient.close()
    # html parsing
    page_soup = soup(page_html, "html.parser")

    # grabs each product
    containers = page_soup.findAll("div", {"class":"rich-text"})
    if containers is not None:
        dates = []
        for container in containers:
            if container.ul is not None:
                for content in container.ul:
                    dates.append(findDate(content.text))
        return dates
    else:
        return


if __name__ == '__main__': # for testing/debugging
    #webPage='https://www.orientering.se/provapaaktiviteter/hittaut/kungalv/manadsvinnare/'
    webPage='https://www.orientering.se/provapaaktiviteter/hittaut/trollhattan/manadsvinnare/'
    #https://www.orientering.se/provapaaktiviteter/hittaut/kalmar/vinstdragning/
    #https://www.orientering.se//provapaaktiviteter/hittaut/katrineholm/manadsvinnare/

    main(webPage)