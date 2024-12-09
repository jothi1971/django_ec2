"""
go to selected countries
each country go to selected cities
go to software/qa
search for selected tags on particuler date
https://greatfalls.craigslist.org
"""
import requests
from bs4 import BeautifulSoup
from Craigs_US.craigslist_city import parse_city_jobs

def usamain():
    f = open("jobs.html", "w")

    main_url = 'https://greatfalls.craigslist.org'

    rawfile = requests.get(main_url)
    print('raw file ', rawfile.text)

    soup = BeautifulSoup(rawfile.text, 'lxml')

    f = open("craigslist_us.html", "w", encoding='utf-8')
    f.write(soup.prettify())

    filter1 = soup.find_all("h5", {"class" : "ban"})[1]
    print('filter 1 ', filter1)
    print('parent  ', filter1.parent.ul)
    filter2 =  filter1.parent.ul
    cities = filter2.find_all("a")
    cities = cities[:-1] 
    """delete last row"""

    print('cities  ', cities)
    for item in cities:
        print(item.get("href"))
        parse_city_jobs("https:" + item.get("href"))

    #parse_city_jobs("https://washingtondc.craigslist.org")

    print("write all cities over")
