import requests
from bs4 import BeautifulSoup
from Craigs_india.craigslist_india_alljobs import parse_all_jobs

def parse_city_jobs(citilink):
    print('citilink', citilink)
    rawfile = requests.get(citilink)
    soup = BeautifulSoup(rawfile.text, 'lxml')
  #  print(soup.prettify())

   # f = open("craigslist_city.html", "w")
    #f.write(soup.prettify())

    filter1 = soup.find("div", {"class" : "jobs"})
    filter2 = filter1.find("div", {"class" : "cats"})
    filter3 = filter2.find("a", {"class": "sof"})
    jobs_link = citilink[:-1] + filter3.get("href")


   # https: // washingtondc.craigslist.org / d / software - qa - dba - etc / search / sof
    #print(jobs_link)
    parse_all_jobs(jobs_link)
  #  print("city over")