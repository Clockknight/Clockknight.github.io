import sys
import beautifulSoup4

#"Cache Mode", uses a text file with pre-written links
    #Find text file with links to google searches of albums' songs
    #Use readlines to seperate out the links of albums
    #Run downloadAlbum

#"Search Mode"
    #Search for a songwriter
    #Try to find all albums from them
    #Run downloadAlbum

#downloadAlbum Function
    #For each link
        #Find every song inside
        #Take note of song title (Try to leave out extraneous things like numbers)
        #Find respective YT video
        #download them to a directory based on album name
