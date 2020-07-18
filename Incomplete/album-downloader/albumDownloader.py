import sys
import bs4

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
    fileDir = input('Please enter the directory of the text file that has the links to appropriate files seperated by newlines.\n\n')

    #Use readlines to seperate out the links of albums
    file = open(fileDir, 'r')
    resultArray = readlines(file)

    #Run downloadAlbum
    downloadAlbum(resultArray)

def searchMode():
    query = ''
    resultLinks = []

    #Search for a songwriter
    #Try to find all albums from them
    #Create search links in formula of "artist album songs"

    #Run downloadAlbum
    downloadAlbum(resultLinks)

def downloadAlbum(givenArray):
    #For each link
        #Find every song inside
        #Take note of song title (Try to leave out extraneous things like numbers)
        #Find respective YT video
        #download them to a directory based on album name
    print('null')

#Prompt the user for an option
optionSelect()
