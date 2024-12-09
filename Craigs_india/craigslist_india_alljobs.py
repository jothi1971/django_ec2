import requests
import re
from bs4 import BeautifulSoup
import globals

def parse_all_jobs(jobslink):
    f = open("jobs.html", "a")

    #    print('all jobs', jobslink)
    rawfile = requests.get(jobslink)
    soup = BeautifulSoup(rawfile.text, 'lxml')

  #  f = open("craigslist_jobs.html", "w")
  #  f.write(soup.prettify())

    filter1 = soup.find("ul", {"class" : "rows"})
    #print(filter1)
    print("\n\n")
    filter2 = filter1.find_all("time", datetime=lambda value: value and value.startswith(globals.india_date))

  #  print('filter2', filter2)
    keywords = globals.search_keywords
    for item in filter2:
        title_string = item.parent.find("a").text
        if any(re.findall('|'.join(keywords), title_string,re.IGNORECASE)):
            print('matchlink',item.parent.find('a').get("href"))
            f.write(str(item.parent.find('a')))
            f.write("<br>")




