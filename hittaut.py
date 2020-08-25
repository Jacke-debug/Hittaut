from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import requests
import datetime
import dateutil.parser as dparser


def findDate(winnerDatesStr):
    words = winnerDatesStr.lower().split(' ')
    #months = ['maj','juni','juli','augusti','september','oktober','november','december']
    dates = set()
    lastWord="+"
    for word in words:
        monthNum = monthParser(word.replace('.','').replace(',','')) # convert month to number. No match returns 0. Remove '.' and ',' before conversion attempt.
        #print(word,"---",monthNum)
        if monthNum != 0: # if monthNum returned a month, save it in dates together with the previous number
            prevNum = ''.join(filter(str.isdigit, lastWord))
            if prevNum.isdigit(): # check if the previous word was a number, if so assume that is the day. False if prevNum is '' (empty string).
                dateNum = monthNum*100 + int(prevNum) # save date as a 4 digit number. First 2 digit for month. Last 2 for day.
            else:
                dateNum = monthNum*100 # Day is 00
            dates.add(dateNum)
        lastWord=word

    # winnerDatesStr = winnerDatesStr.lower()
    # winnerDatesStr = monthTranslate(winnerDatesStr)
    # x=dparser.parse("Datum då månadsvinnare utses: vinstdragningen 29 may",fuzzy=True)

    # # assumes month to be written as a word
    #month = monthParser(winnerDatesStr)
    # print(winnerDatesStr)
    # # extract numbers from the string
    # numbers = [int(s) for s in str.split(winnerDatesStr) if s.isdigit()]
    # if len(numbers) == 1:
    #     # use the one number as a date
    #     date = numbers[0]
    #     month = 1
    # else:
    #     # string contains more than one number
    #     # may be a numbering of the dates i.e. 1. 2. 3.. 
    #     # or that the month is written with a number
    #     # or possibly both..
    #     date = 1
    #     if month == 0:
    #         # month is written as a number not a word
    #         # do something clever
    #         month = 1
    #     pass
    # x = datetime.datetime(2020, month, date)
    return dates

def monthParser(word):
    month = 0
    if word == "maj":
        month = 5
    elif word in ["juni","jun"]:
        month = 6
    elif word in ["juli","jul"]:
        month = 7
    elif word in ["augusti","aug"]:
        month = 8
    elif word in ["september","sep"]:
        month = 9
    elif word in ["oktober","okt"]:
        month = 10
    elif word in ["november","nov"]:
        month = 11
    elif word in ["december","dec"]:
        month = 12
    return month

def monthTranslate(textBody):
    translated_textBody = textBody.lower()
    monthDictionary = {'maj':'may','juni':'june','juli':'july','augusti':'august','oktober':'october'} #april,september,november,december
    for k, v in monthDictionary.items():
        translated_textBody=translated_textBody.replace(k,v)
    return translated_textBody

def main(ort_url): 
    try:
        vinst_url = ort_url + "manadsvinnare/" 
        r = requests.get(vinst_url)
        r.raise_for_status()
    except:
        try: 
            vinst_url = ort_url + "vinstdragning/" # some cities uses "vinstdragning/" as extension
            r = requests.get(vinst_url)
            r.raise_for_status()
        except:
            print('Could not download page')
            return

    print(r.url, 'downloaded successfully')


    # opening up connection, grabbing the page
    try:
        uClient = uReq(vinst_url)
    except:
        exit

    page_html = uClient.read()
    uClient.close()
    # html parsing
    page_soup = soup(page_html, "html.parser")

    # grabs main text of the page
    mainText = page_soup.find("div", {"class":"editorial__offset"})
    #print(mainText) # debugging
    #print(containers[1]) # debugging

# look for header containing keyword

    # # grabs all headlines/subtitles
    # headers = mainText.findAll("h2")

    # list of words to look for
    # keywordlist = ['vinstdragning', 'dragningar','utlottning']

    # if headers is not None:
    #     index=0
    #     for header in headers:
    #         if header.string is not None:
    #             if any(word in header.string.lower() for word in keywordlist):
    #                 print('>>>',header.string)
    #                 # pass corresponding bodyText to method for finding dates
    #                 if header.find_next("div", {"class":"rich-text"}) is not None:
    #                     textMass = header.find_next("div", {"class":"rich-text"}).get_text(' ')
    #                     print(textMass)
    #                     dates = findDate(textMass)
    #                     print(dates)
    #             else:
    #                 print('---',header.string)
    #         index = index + 1
    #     #return dates
    # else:
    #     return
    
# brute force method; extracts all dates on the page
    mainTextasText=mainText.get_text(' ')
    draws = findDate(mainTextasText)

# get "ort"
    ort=page_soup.find("li", {"class":"hittaut-navigation__item item-1"}).get_text().strip()[10:]
    #print(ort)

# get dates "ort", "dates" and "nCheckpts"
    # opening up connection, grabbing the page
    uClient = uReq(ort_url)
    page_html = uClient.read()
    uClient.close()

    # html parsing
    page_soup = soup(page_html, "html.parser")

    # get section containing ort+dates. May increase speed.
    hero_wrapper = page_soup.find("div", {"class":"hero__wrapper"})
    
    # ort
    ort = hero_wrapper.find("h1", {"class":"hittaut-hero__heading"}).get_text().split(' ',2)[2]

    # dates
    dates = hero_wrapper.find("li", {"class":"hittaut-hero__dates"}).get_text().strip()

    # nCheckpts
    nCheckpts = page_soup.find("ul", {"class":"toplist"}).find("span", {"class":"count"}).get_text()

# create dictionary
    hittautDict = {"ort":ort, "dates":dates,"nCheckpts":nCheckpts,"draws":draws}

    return hittautDict

if __name__ == '__main__': # for testing/debugging
    # webPage='https://www.orientering.se/provapaaktiviteter/hittaut/kungalv/'
    # webPage='https://www.orientering.se/provapaaktiviteter/hittaut/trollhattan/'
    webPage='https://www.orientering.se/provapaaktiviteter/hittaut/kalmar/'
    #https://www.orientering.se//provapaaktiviteter/hittaut/katrineholm/

    result=main(webPage)

    print(result)