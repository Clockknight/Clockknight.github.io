import sys
import urllib
import requests
from pytube import YouTube
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

#Global Variables
ua = UserAgent()
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13'}

#Functions for
def optionSelect():
    option = input('''
    Welcome to Clockknight's Album Downloader. Please choose from an option below by entering the option number:

    1) Cache Mode
    Provide a .txt file with links to album's google result pages, seperated by lines.

    2) Search Mode
    Search for an artist's discography, and pull songs directly.

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
    '''
    resultCount = 0
    resultLinks = []

    #Get input for a songwriter
    #artist = input('\nPlease input the name of the artist you want to search the discography of.\n\t')
    #Temporarily listing searchArtist as Masami Ueda by default
    artist = 'Masami Ueda'
    searchLen = len(artist)
    searchArtist = urllib.parse.quote_plus(artist)

    #discogs Google results scrape
    query = 'https://www.google.com/search?q=discogs+' + searchArtist
    try:
        page = requests.get(query, headers=headers)#Use requests on the new URL
        soup = BeautifulSoup(page.text, "html.parser")#Take requests and decode it
        aList = soup.find_all('a', href=True)
        for item in aList:
            if item['href'][:30] == 'https://www.discogs.com/artist':
                temp = item['href'] + '?type=Releases&subtype=Albums&filter_anv=0'
                print('Going to page ' + temp + '...')
                break#Take the first viable link and then process it.
    except:
        print('Error:')

    #Find album name and find google results based on previous inputs & results
    try:
    albumCheck = artist + ' - '#Create string to check against later
    page = requests.get(temp, headers=headers)#Use requests on the new URL
    soup = BeautifulSoup(page.text, "html.parser")#Take requests and decode it
    imgList = soup.find_all('img', alt=True)#Make array of img tags with alt
    for item in imgList:
        if item['alt'][:searchLen+3] == albumCheck:#Check alt text against albumCheck string, based on Discogs formatting
            #Convert all info into one google search URL
            temp = 'https://www.google.com/search?q=' + urllib.parse.quote_plus(artist + ' ' +  item['alt'][searchLen+3:-10]) + '+songs'
            resultLinks.append(temp)#Add Link to array
    except:
       print('Error:')

    '''
    #TEST FOR DOWNLOAD ALBUM
    resultLinks = ['https://www.google.com/search?q=madeon+adventure+songs&rlz=1C1CHBF_enUS899US899&oq=madeon+adventure+songs&aqs=chrome..69i57.311j0j7&sourceid=chrome&ie=UTF-8']

    downloadAlbum(resultLinks)#Call download Album with all songs wanted

def downloadAlbum(givenArray):
    for link in givenArray:
        #Refresh variables for each link
        songList = []
        infoList = []
        artistName = ''
        songCount = 0
        artistIndex = 0

        #Process each link and grab song titles from the pages
        #try:
        page = requests.get(link, headers=headers)#Use requests on the new URL
        soup = BeautifulSoup(page.text, "html.parser")#Take requests and decode it

        #Get album and artist title to save as folder
        albumTitle = soup.find('title')
        albumTitle = albumTitle.contents[0][:-22]

        #Ask user for input regarding the artist's name in the search
        infoList = albumTitle.split()
        for item in infoList:
            print(item)
        artistName = searchParse(infoList)
        print(artistName)

        divList = soup.find_all('div', {'class': 'title'})
        for div in divList:
            songList.append(div.contents[0])#Refer to the first item of contents, since .contents returns an array


        #Process each song by appending the song title to the search
        songIndex = songCount
        for item in songList:
            songIndex -= 1
            #temp stores each song's google search video results
            temp = 'https://www.google.com/search?q=' + urllib.parse.quote_plus(item) + '+' + link[32:]
            #try:
            page = requests.get(link, headers=headers)#Use requests on the new URL
            soup = BeautifulSoup(page.text, "html.parser")#Take requests and decode it

            aList = soup.find_all('a', href=True)
            for a in aList:
                if a['href'][:29] == 'https://www.youtube.com/watch':
                    soup = a.contents[-1]

                    temp = a['href']
                    YouTube(temp).streams.first().download()#NOTE: fix settings to download with correct dir and name
                    songCount += 1


            #except TypeError:
            #    print('Error:' + str(TypeError.content))


        #except TypeError:
        #    print('Error:' + str(TypeError.content))

    def searchParse(searchTerms):

        while artistIndex == 0:
            artistIndex = input('Please input how many words long the artist\'s name is. (Elvis Presley is two words, for example.)\n')
            if artistIndex.isnumeric():#Check to make sure the string is made of numbers
                artistIndex = int(artistIndex)#Convert the string into an integer
                if artistIndex <= 0 or artistIndex > len(infoList):
                     print('Sorry, not a valid response. Please try again.')
                     artistIndex = 0
                else:
                    for i in range(0, artistIndex-1):
                        print(i)
                        confirmedString.append(infoList[i])
                        print(infoList[i])
                    print(artistName)



        return confirmedString

optionSelect()
