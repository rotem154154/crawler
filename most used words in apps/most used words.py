import requests
from bs4 import BeautifulSoup
import operator
from urllib.parse import urlsplit

page = 0
numapps = 0
numwords = 0
wordsperapp = 0
def wordinpage(url):
    code = requests.get(url)
    text = code.text
    soup = BeautifulSoup(text, "html.parser")
    firsttime = True
    for link in soup.findAll('a', {'class' : 'title'}):
       if firsttime == False:
           words = link.string.lower().split()
           for word in words:
               symbols = '!@#$%^&*()_+={}[]"|/?:.><,*-`' + "'"
               for i in range(0,len(symbols)):
                   word = word.replace(symbols[i],"")
               if len(word) > 1:
                   global numapps, numwords, wordsperapp
                   numapps += 1
                   numwords += len(word)
                   wordsperapp = numwords / numapps
                   addword(word)
       firsttime = False
    global page, wordsperapp
    page += 1
    print("page " + str(page) + ".   every app has " + str(wordsperapp) + " words.")
    with open("most used words.txt", mode='w', encoding='utf-8') as myfile:
        myfile.write("page " + str(page) + "\n\n\n")
        global wordcount
        for key, value in sorted(wordcount.items(), key=operator.itemgetter(1)):
            myfile.write(str(key) + " - " + str(value) + "\n")


def addword(word):
    global wordcount
    if word in wordcount:
        wordcount[word] += 1
    else:
        wordcount[word] = 1






wordcount = {}
for i in range(1, 3100):
    wordinpage('http://ios.hipstore.mobi/game/' + str(i))
for key, value in sorted(wordcount.items(), key=operator.itemgetter(1)):
    print(key , value)
