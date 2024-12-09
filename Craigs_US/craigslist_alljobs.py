import requests
import re
from bs4 import BeautifulSoup
import globals
import sys

def parse_all_jobs(jobslink):
    f = open("jobs.html", "a")

#    print('all jobs', jobslink)
    rawfile = requests.get(jobslink)
    soup = BeautifulSoup(rawfile.text, 'lxml')
    #f = open("craigslist_jobs.html", "w", encoding='utf-8')
    #f.write(soup.prettify())

    filter1 = soup.find("ol", {"class" : "cl-static-search-results"})
    filter2 = filter1.find_all("li")
    filter2 = filter2[1:] #discard first row
    #print('jothi ',filter2)



    print("\n\n")

    #filter2 = filter1.find_all("time", datetime=lambda value: value and value.startswith(globals.us_date))


    keywords = globals.search_keywords
    print('keywords ', keywords)
    
    for item in filter2:
        joblink = item.parent.find('a').get("href")
        print('jothi job link', joblink)
        jobinfo = requests.get(joblink)
        jobsoup = BeautifulSoup(jobinfo.text, 'lxml')
        jobstring = jobsoup.get_text()
        #findall(pattern, inputstring)
        if any(re.findall('|'.join(keywords), jobstring, re.IGNORECASE)):
            print('match link', item.parent.find('a').get("href"))
            te1 = item.parent.find('a')
            print('te1 ', te1)
            te2 = te1.find("div", {"class" : "details"})

            te3 = te2.find("div", {"class" : "price"})
            print('te3 ', te3)
            if te3 != None:
                te3.decompose()

            print('after decompose ', te1)
            f.write(str(te1))
            f.write("<br>")
            
    #sys.exit("stop")




