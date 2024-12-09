import requests
from bs4 import BeautifulSoup
from Craigs_US.craigslist_city import parse_city_jobs

def indiamain():

    main_url = 'https://bangalore.craigslist.org'

    rawfile = requests.get(main_url)
    print('raw file ', rawfile.text)

    soup = BeautifulSoup(rawfile.text, 'lxml')

    #f = open("craigslist_india.html", "w", encoding='utf-8')
    #f.write(soup.prettify())

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
