import requests
from bs4 import BeautifulSoup

def spider(maxpage):
    page = 1
    numitem = 0
    sum = 0.0
    avg = 0.0
    while page <= maxpage:
        url = "http://www.ebay.com/sch/i.html?_from=R40&_sacat=0&_sop=10&_nkw=iphone+case&_pgn="+str(page)+"&_skc=1200&rt=nc"
        code = requests.get(url)
        text = code.text
        soup = BeautifulSoup(text, "html.parser")
        for link in soup.findAll('a', {'class': 'vip'}):
            href = link.get('href')
            rating = itemrating(href)
            if type(rating) is float:
                sum += rating
                numitem += 1
                avg = sum / numitem
                print("average of " + str(numitem) + " items is " + str(avg))
        page += 1


def itemrating(url):
    code = requests.get(url)
    text = code.text
    soup = BeautifulSoup(text, "html.parser")
    for rating in soup.findAll('div', {'id': 'si-fb'}):
        str = rating.string
        place = str.find("%")
        str2 = ""
        for i in range(0, place):
            str2 += str[i]
        return float(str2)

spider(60)