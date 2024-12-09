import time
from bs4 import BeautifulSoup
import csv
import threading
import os
import requests
import time
import re
import shared
import globals

class ScrapUSA:

    #global variables
    main_url = 'https://greatfalls.craigslist.org'
    open("jobs.html", "w")

    def __init__(self,keywords,queue):
        self.keywords = keywords.split(",")
        self.queue = queue

    def usamain(self):

        rawfile = requests.get(self.main_url)
        #print('raw file ', rawfile.text)

        soup = BeautifulSoup(rawfile.text, 'lxml')

        #f = open("craigslist_us.html", "w", encoding='utf-8')
        #f.write(soup.prettify())

        filter1 = soup.find_all("h5", {"class" : "ban"})[1]
        #print('filter 1 ', filter1)
        #print('parent  ', filter1.parent.ul)
        filter2 =  filter1.parent.ul
        cities = filter2.find_all("a")
        cities = cities[:-1] 
        """delete last row"""

        #print('cities  ', cities)
        for item in cities:
            #print(item.get("href"))
            self.parse_city_jobs("https:" + item.get("href"))


        print("write all cities over")

    def parse_city_jobs(self,citilink):
        #print('citilink', citilink)
        rawfile = requests.get(citilink)
        soup = BeautifulSoup(rawfile.text, 'lxml')
        #print(soup.prettify())

        #f = open("craigslist_city.html", "w", encoding='utf-8')
        #f.write(soup.prettify())

        filter1 = soup.find("div", {"class" : "jobs"})
        filter2 = filter1.find("div", {"class" : "cats"})
        filter3 = filter2.find("a", {"class": "sof"})
        jobs_link = citilink + filter3.get("href")
        print('jothi job link ', jobs_link)

        self.parse_all_jobs(jobs_link)
    #  print("city over")

    def parse_all_jobs(self,jobslink):
        if shared.stop_scrap == True:
            print('jothi stop scrap')
            exit()
    
        f = open("jobs.html", "a") #append mode

    #    print('all jobs', jobslink)
        rawfile = requests.get(jobslink)
        soup = BeautifulSoup(rawfile.text, 'lxml')
        #f = open("craigslist_jobs.html", "w", encoding='utf-8')
        #f.write(soup.prettify())

        filter1 = soup.find("ol", {"class" : "cl-static-search-results"})
        filter2 = filter1.find_all("li")
        filter2 = filter2[1:] #discard first row
        #print('jothi ',filter2)



        print("test break \n\n")
        print(filter2)

        #filter2 = filter1.find_all("time", datetime=lambda value: value and value.startswith(globals.us_date))


        
        for item in filter2:
            joblink = item.parent.find('a').get("href")
            print('jothi job link', joblink)
            jobinfo = requests.get(joblink)
            jobsoup = BeautifulSoup(jobinfo.text, 'lxml')
            jobstring = jobsoup.get_text()
            #findall(pattern, inputstring)
            if any(re.findall('|'.join(self.keywords), jobstring, re.IGNORECASE)):
                #print('match link', str(joblink))
                te1 = item.parent.find('a')
                self.queue.put(str(joblink))
                self.queue.put("\n")

                #print('te1 ', te1)
                title = te1.find("div",{"class":"title"}).text
                self.queue.put(title)
                self.queue.put("\n")

                te2 = te1.find("div", {"class" : "details"})

                te3 = te2.find("div", {"class" : "price"})
                location = te2.find("div", {"class" : "location"})
                if location != None:
                    self.queue.put(location.text.strip())

                #print('te3 ', te3)
                if te3 != None:
                    te3.decompose()

                #print('after decompose ', te1)
                #f.write(str(te1))
                #f.write("<br>")
                self.queue.put("\n==========\n")

        #sys.exit("stop")
    