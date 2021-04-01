from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import requests
import datetime
# import dateutil.parser as dparser


def findDates(winnerDatesStr):
    winnerDatesStr = winnerDatesStr.replace('.',' ').replace(',',' ')
    words = winnerDatesStr.lower().split(' ')
    #months = ['maj','juni','juli','augusti','september','oktober','november','december']
    dates = set()
    lastWord="+"
    for word in words:
        # monthNum = monthParser(word.replace('.','').replace(',','')) # convert month to number. No match returns 0. Remove '.' and ',' before conversion attempt.
        monthNum = monthParser(word)
        #print(word,"---",monthNum)
        if monthNum != 0: # if monthNum returned a month, save it in dates together with the previous number
            prevNum = ''.join(filter(str.isdigit, lastWord))
            if prevNum.isdigit(): # check if the previous word was a number, if so assume that is the day. False if prevNum is '' (empty string).
                dateNum = monthNum*100 + int(prevNum) # save date as a 4 digit number. First 2 digit for month. Last 2 for day.
            else:
                dateNum = monthNum*100 # Day is 00
            dates.add(dateNum)
        lastWord=word

    dates_list = sorted(dates)

    return dates_list

def monthParser(word):
    month = 0
    if word in ["mars","mar"]:
        month = 3
    elif word in ["april","apr"]:
        month = 4
    elif word in ["maj","may"]:
        month = 5
    elif word in ["juni","jun"]:
        month = 6
    elif word in ["juli","jul"]:
        month = 7
    elif word in ["augusti","aug"]:
        month = 8
    elif word in ["september","sep"]:
        month = 9
    elif word in ["oktober","okt","oct"]:
        month = 10
    elif word in ["november","nov"]:
        month = 11
    elif word in ["december","dec"]:
        month = 12
    return month

def monthTranslate(textBody): # for use with dateutil.parser
    translated_textBody = textBody.lower()
    monthDictionary = {'maj':'may','juni':'june','juli':'july','augusti':'august','oktober':'october'} #april,september,november,december
    for k, v in monthDictionary.items():
        translated_textBody=translated_textBody.replace(k,v)
    return translated_textBody

def main(ort_url):
    print(ort_url)

## get "ort", "dates" and "nCheckpts"
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
    datesStr = hero_wrapper.find("li", {"class":"hittaut-hero__dates"}).get_text().strip()
    dates = findDates(datesStr)

    # nCheckpts
    try:
        toplist = page_soup.find("ul", {"class":"toplist"})
        leader = toplist.find("span", {"class":"name"}).get_text()
        nCheckpts = int(toplist.find("span", {"class":"count"}).get_text())
        # set nChekcpts to -1 if the toplist is just the default one
        if leader == 'Erik Segersäll' & nCheckpts == 87:
            nCheckpts = -1
    except:
        nCheckpts = -1

## download winner page
    # try:
    #     vinst_url = ort_url + "manadsvinnare/" 
    #     r = requests.get(vinst_url, verify=False)
    #     r.raise_for_status()
    # except:
    #     try: 
    #         vinst_url = ort_url + "vinstdragning/" # some cities uses "vinstdragning/" as extension
    #         r = requests.get(vinst_url, verify=False)
    #         r.raise_for_status()
    #     except:
    #         print('Could not download winner page.')
    # print(r.url, 'downloaded successfully')

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

    grab_success = True
    # opening up connection, grabbing the paged
    try:
        vinst_url = ort_url + "manadsvinnare/" 
        uClient = uReq(vinst_url)
    except:
        try:
            vinst_url = ort_url + "vinstdragning/"
            uClient = uReq(vinst_url)
        except:
            grab_success = False
            
    if grab_success:
        page_html = uClient.read()
        uClient.close()
        # html parsing
        page_soup = soup(page_html, "html.parser")

        # grabs main text of the page
        mainText = page_soup.find("div", {"class":"editorial__offset"})
        #print(mainText) # debugging
        #print(containers[1]) # debugging

        # brute force method; extracts all dates on the page
        mainTextasText=mainText.get_text(' ')
        print(mainTextasText)
        draws = findDates(mainTextasText)
    else:
        # if not able to get the webpage for draws, just set draws to empty list
        draws = []

# create dictionary
    hittautDict = {"ort":ort,"url":ort_url,"start":dates[0],"end":dates[1],"nCheckpts":nCheckpts,"draws":draws}

    return hittautDict

if __name__ == '__main__': # for testing/debugging
    # webPage='https://www.orientering.se/provapaaktiviteter/hittaut/kungalv/'
    # webPage='https://www.orientering.se/provapaaktiviteter/hittaut/trollhattan/'
    # webPage='https://www.orientering.se/provapaaktiviteter/hittaut/kalmar/'
    # webPage='https://www.orientering.se/provapaaktiviteter/hittaut/skane/'
    #https://www.orientering.se//provapaaktiviteter/hittaut/katrineholm/
    webPage='https://www.orientering.se/provapaaktiviteter/hittaut/goteborg/'

    result=main(webPage)

    print(result)