import requests
from bs4 import BeautifulSoup
import random
from urllib.parse import urlsplit

numsite = 0
def websitelinks(url):
    code = requests.get(url)
    text = code.text
    soup = BeautifulSoup(text, "html.parser")
    filename = str(random.randrange(1001,9999)) + ".txt"
    sumezer = 0
    title = "-1"
    for link in soup.findAll('title'):
        sumezer += 1
        title = link.string + ".txt"
    if sumezer == 1:
        filename = title
    open('website links/' + filename, 'a')

    spider(url, filename)


def spider(url, filename):
    code = requests.get(url)
    text = code.text
    soup = BeautifulSoup(text, "html.parser")
    for link in soup.findAll('a'):
        href = link.get('href')
        try:
            if isinstance(href, str) and (len(href) < 5 or getdomain(url) == getdomain(href) or href[4] != ':') and (len(href) != 1 and url != href):
                with open('website links/' + filename) as f:
                    lines = f.readlines()
                    boolezer = True
                    for i in lines:
                        newi = i[:-1]
                        if newi == href or getdomain(url) + href == newi or href[1:] == newi or i == link.string:
                            boolezer = False
                    if boolezer == True:
                        ezer = href
                        if len(href) < 5 or ezer[4] != ':':
                            ezer = getdomain(url) + href
                        if ezer[0] == '/':
                            ezer = ezer[1:]
                        with open("website links/" + filename, mode='a', encoding='utf-8') as myfile:
                            if isinstance(link.string, str):
                                myfile.write(link.string + " -" + '\n')
                                global numsite
                                numsite += 1
                                print(str(numsite) + "    " + ezer)
                                myfile.write(ezer + '\n' + '\n')
                        spider(ezer, filename)
        except:
            print("error:   " + href)

def getdomain(url):
    base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url))
    return base_url

websitelinks("http://www.google.com")
