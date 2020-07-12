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

    switch(option){
        case 1:
            cacheMode()
            break;

        case 2:
            searchMode()
            break;

        case 0:
            sys.quit()
            break;

        default:
            optionSelect()
            break;
    }

def cacheMode():
    #Find text file with links to google searches of albums' songs
    #Use readlines to seperate out the links of albums
    #Run downloadAlbum
    downloadAlbum()

def searchMode():
    #Search for a songwriter
    #Try to find all albums from them
    #Run downloadAlbum
    downloadAlbum()

def downloadAlbum():
    #For each link
        #Find every song inside
        #Take note of song title (Try to leave out extraneous things like numbers)
        #Find respective YT video
        #download them to a directory based on album name
    print('null')
