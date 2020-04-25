import sys
import bs4
import requests
import pyperclip

followedSoup = ''
userUrl = ''

urlDNE = True

linkList = []

while urlDNE:
    userUrl = input('Please input the id of the target twitter account.\nFor example, Bernie Sanders would input \"BernieSanders\", not \"Bernie Sanders\".\n')
    userUrl = 'https://twitter.com/' + userUrl + '/following'

    try:
        res = requests.get(userUrl)
        res.raise_for_status()
        urlDNE = False#If it raises succesfully, the code will stop looping

    except:
        print("Error.\n" + sys.exc_info()[0])


followedSoup = bs4.BeautifulSoup(res.text, 'lxml')
linkList = followedSoup.select('a')
for link in linkList:
    print('\n\n' + str(link))

#Will scrape the account's following page for users
#Will append '/media\n' at the end of each url, finding media pages
#Gather all the links together and then use pyperclip to copy all of that onto the user's clipboard
