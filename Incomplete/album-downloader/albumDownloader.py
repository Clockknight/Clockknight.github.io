import sys
import urllib
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

#Global Variables
ua = UserAgent()

def optionSelect():
    option = input('''
    Welcome to Clockknight's Album Downloader. Please choose from an option below by entering the option number:

    1) Cache Mode
    Provide a .txt file with links to album's google result pages, seperated by lines.

    2) Search Mode
    Search for an artist or album, and pull songs directly.

    0) Exit

    ''')

    if option == '1':
        cacheMode()
    elif option == '2':
        searchMode()
    elif option == '0':
        sys.exit()
    else:
        print('Invalid option selected. Please try again.\n\n')
        optionSelect()

def cacheMode():
    fileDir = ''
    resultArray = []

    #Find text file with links to google searches of albums' songs
    fileDir = input('Please enter the directory of the text file that has the links to appropriate files seperated by newlines.\n')

    #Use readlines to seperate out the links of albums
    file = open(fileDir, 'r')
    resultArray = file.readlines()
    #Run downloadAlbum
    downloadAlbum(resultArray)

def searchMode():
    resultLinks = []
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13'}

    #Get input for a songwriter
        #Temporarily listing query as madeon by default
        #query = 'https://www.google.com/search?q=' + urllib.parse.quote_plus(input('\nPlease input the name of the artist you want to search the discography of.\n\t') + ' albums')
    query = 'https://www.google.com/search?q=' + urllib.parse.quote_plus('madeon' + '+albums')
    #Replace spaces with + to fit google search URL format

    #Try to find all albums from them
    try:
        page = requests.get(query, headers=headers)#Use requests on the new URL
        soup = BeautifulSoup(page.text, "html.parser")#Take requests and decode it
        #for link in soup.find_all('div', {'class':'title'}):
        divList = soup.find_all('div', {'class': 'title'})
        for item in divList:
                print(item)

        #Create search links in formula of "artist album songs"


        #Run downloadAlbum
        downloadAlbum(resultLinks)

    except TypeError:
        print('Error:' + TypeError)

def downloadAlbum(givenArray):
    #For each link
        #Find every song inside
        #Take note of song title (Try to leave out extraneous things like numbers)
        #Find respective YT video
        #download them to a directory based on album name
    print('null')

#Prompt the user for an option

optionSelect()
