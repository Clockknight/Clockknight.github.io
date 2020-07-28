import sys
import urllib
import requests
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
    resultCount = 0
    resultLinks = []

    #Get input for a songwriter
    #Temporarily listing query as madeon by default
    #searchArtist = input('\nPlease input the name of the artist you want to search the discography of.\n\t')
    searchArtist = 'eminem'
    query = 'https://www.discogs.com/artist/' + searchArtist + '?type=Releases&subtype=Albums&filter_anv=0'
    #Replace spaces with + to fit google search URL format

    #Try to find all albums from them
    try:
        page = requests.get(query, headers=headers)#Use requests on the new URL
        soup = BeautifulSoup(page.text, "html.parser")#Take requests and decode it
        divList = soup.find_all('script', {'type': 'application/ld+json'})
        for item in divList:
            resultLinks.append(item.contents[0])
            resultCount += 1

        for item in divList:
            for i in item:
                print(i)
                print()
                print()
                print()
                print()
        #Create array of links to google searches with song titles


        #Run downloadAlbum
            #downloadAlbum(resultLinks)

    except TypeError:
        print('Error:' + str(TypeError))

    '''
    #TEST FOR DOWNLOAD ALBUM
    resultLinks = ['https://www.google.com/search?rlz=1C1CHBF_enUS899US899&sxsrf=ALeKk036F02P9rnhODzJf_1lXsLL7IAFYw%3A1595754306716&ei=QkcdX-muK5zC0PEPpLqqyA8&q=+Adventure+songs+Madeon&oq=+Adventure+songs+Madeon&gs_lcp=CgZwc3ktYWIQAzoHCAAQsAMQQzoFCAAQkQI6BggAEAcQHjoCCABQqz5Y4EtguFBoAXAAeACAAVCIAd8BkgEBM5gBAKABAaABAqoBB2d3cy13aXrAAQE&sclient=psy-ab&ved=0ahUKEwjp1-aEyOrqAhUcITQIHSSdCvkQ4dUDCAw&uact=5']
    downloadAlbum(resultLinks)
    '''

def downloadAlbum(givenArray):
    for link in givenArray:
        #Refresh variables for each link
        songList = []
        songCount = 0
        #try:
        #Process each link and grab song titles from them
        page = requests.get(link, headers=headers)#Use requests on the new URL
        soup = BeautifulSoup(page.text, "html.parser")#Take requests and decode it
        divList = soup.find_all('div', {'class': 'title'})
        for item in divList:
            songList.append(item.contents[0])#Refer to the first item of contents, since .contents returns an array
            songCount += 1#Keep track of songList length

        #Process each song by appending the song title to the search
        for song in songList:
            url = link + urllib.parse.quote_plus( ' ' + song)
            page = requests.get(url, headers=headers)
            soup = BeautifulSoup(page.text, "html.parser")
            resultList = soup.find_all('a', href=True)
            for result in resultList:
                if (result['href'][:22] == 'https://www.youtube.com') or (result['href'][7:21] == 'http://www.youtube.com'):
                    print(ping)

            print(len(resultList))


        #except TypeError:
        #    print('Error:' + str(TypeError.content))

        #Take note of song title (Try to leave out extraneous things like numbers)
        #Find respective YT video
        #download them to a directory based on album name

#Prompt the user for an option

optionSelect()
