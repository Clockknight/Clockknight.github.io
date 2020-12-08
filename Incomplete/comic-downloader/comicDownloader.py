import os
import bs4
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent

#Global Variables
ua = UserAgent()
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13'}

def init():#Function to ensure that the file is ready before the main program runs
    if not os.path.exists("./downloaderSettings.txt"):
        file = open("./downloaderSettings.txt", "w+")
        file.write('''Boku No Hero Academia
        https://readheromanga.com/manga/
        0
        Chainsaw Man
        http://manganelos.com/chainsaw-man-chapter-94
        0
        Goblin Slayer
        https://mangakakalot.com/chapter/hgj2047065412/chapter_53
        0''')

    main()#After running init, run the actual program
def main():
    settingsFile = open("./downloaderSettings.txt", 'r')
    settingsList = []
    passList = ['','','','']
    i = 0
    multi = 0

    settingsList = settingsFile.readlines()

    while i < 4:
        passList[i] = settingsList[i + 4*multi]
        i += 1
    i = 0
    TEMP disable bnhaCheck(passList)
    multi += 1
    while i < 4:
        passList[i] = settingsList[i + 4*multi]
        i += 1
    gsCheck(passList)
    multi += 1

def bnhaCheck(info):
    page = requests.get(info[2], headers=headers)#Use requests on the new URL
    soup = BeautifulSoup(page.text, "html.parser")#Take requests and decode it

    if not os.path.exists(info[0][:-1]):
        os.makedirs(info[0][:-1])

    #NOTE: ADJUST BELOW CODE FOR EACH COMIC SERIES USED IN SETTINGS, DIFFERENT SITES WILL HAVE DIFFERENT ARCHITECTURE
    target = soup.find_all('ul')
    target = target[-1].contents[0].contents[1]#Use the most recent chapter uploaded. In the source, always happens to be the last ul tag's first li tag, and contents makes the a tag in that li tag the second item in the list.
    target = target['href']

    max = target[-4:-1]

    if max != info[3]:
        info.append(max)
        bnhaVolume(info)#Only call this function if the volume is downloadable & previously unexamined
    #If the conditional doesn't trigger, a new chapter isn't out, and there's nothing worth changing.
def bnhaVolume(info):
    print(info)
    bookmark = str(int(info[3]) + 1)
    url = info[1][:-1] + bookmark

    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, "html.parser")

    #NOTE: ADJUST BELOW CODE FOR EACH COMIC SERIES USED IN SETTINGS, DIFFERENT SITES WILL HAVE DIFFERENT ARCHITECTURE
    target = soup.find_all('img')

    if len(target) == 1:#Source only has 1 image on a new chapter occasionally, this is to stop false positives
        print('No new issue since last check.')

    else:
        for image in target:
            downloadImage(info, image, bookmark)

        info[3] = bookmark

        if bookmark != info[4]:
            bnhaVolume(info)
        else:
            settings(info, 0)

def downloadImage(info, tag, volume):
    url = tag['src']
    name = info[0][:-1] + ' - ' + volume + ' - ' + tag['alt']

    res = requests.get(url)
    imageFile = open(os.path.join(info[0][:-1], os.path.basename(name)), 'wb')
    for chunk in res.iter_content(100000):
        imageFile.write(chunk)
    imageFile.close()
def settings(info, multi):
    i = 0
    dir = './downloaderSettings.txt'
    rFile = open(dir, 'r')
    wFile = open(dir, 'w')

    edit = rFile.readlines()

    while i < 4:
        edit[i + 4*multi] = info[i]
        i += 1

    wFile.writelines(edit)

    rFile.close()
    wFile.close()

init()



'''
Formatting for a series to be downloaded:

def testCheck(info):
    page = requests.get(info[2], headers=headers)#Use requests on the new URL
    soup = BeautifulSoup(page.text, "html.parser")#Take requests and decode it

    if not os.path.exists(info[0][:-1]):
        os.makedirs(info[0][:-1])

    #NOTE: ADJUST BELOW CODE FOR EACH COMIC SERIES USED IN SETTINGS, DIFFERENT SITES WILL HAVE DIFFERENT ARCHITECTURE
    target = soup.find_all('ul')
    target = target[-1].contents[0].contents[1]#Use the most recent chapter uploaded. In the source, always happens to be the last ul tag's first li tag, and contents makes the a tag in that li tag the second item in the list.
    target = target['href']

    max = target[-4:-1]

    if max != info[3]:
        info.append(max)
        testVolume(info)#Only call this function if the volume is downloadable & previously unexamined
    #If the conditional doesn't trigger, a new chapter isn't out, and there's nothing worth changing.
def testVolume(info):
    print(info)
    bookmark = str(int(info[3]) + 1)
    url = info[1][:-1] + bookmark

    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, "html.parser")

    #NOTE: ADJUST BELOW CODE FOR EACH COMIC SERIES USED IN SETTINGS, DIFFERENT SITES WILL HAVE DIFFERENT ARCHITECTURE
    target = soup.find_all('img')

    if len(target) == 1:#Source only has 1 image on a new chapter occasionally, this is to stop false positives
        print('No new issue since last check.')

    else:
        for image in target:
            downloadImage(info, image, bookmark)

        info[3] = bookmark

        if bookmark != info[4]:
            testVolume(info)
        else:
            settings(info, 0)
'''
