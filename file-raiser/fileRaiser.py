import os
import sys

raisecount = 0

dirExist = False
deleteMode = False

directory = ''

if len(sys.argv) > 1:
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == '-d' and deleteMode == False:
            print('\nDelete Mode activated! The program will now delete files after moving them.')
            deleteMode = True

while dirExist == False:
    directory = input('\nPlease input a directory to scan for files to raise.\n\t')

    if os.path.exists(directory):
        print('\nPath found. Processing for files in directory and any subdirectories.\n')
        dirExist = True
    else:
        print('\nSorry! Path not found. Please try again.')

directoryCount = len(directory)

#for file in os.walk(directory, topdown=false):
#Use os.walk to find every file in every folder/subfolder
    #If the file needs to be moved, increase the counter by 1
    #Only do this if the file isnt already in the directory.

#Display the amount of files that would be raised by the program.
    #Check with user that the directory and all details of the the directory are correct.
    #For each file, take it and move it to original directory
