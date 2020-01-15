import os
import sys

raisecount = 0

dirExist = False

directory = ''

while dirExist == False:
    directory = input('Please input a directory to scan for files to raise.\n\t')

    if os.path.exists(directory):
        print('Path found. Processing for files in directory and any subdirectories.\n\n\n')
        dirExist = True
    else:
        print('Sorry! Path not found. Please try again.\n\n')

directoryCount = len(directory)

#for file in os.walk(directory, topdown=false)
#Use os.walk to find every file in every folder/subfolder
    #If the file needs to be moved, increase the counter by 1
    #Only do this if the file isnt already in the directory.

#Display the amount of files that would be raised by the program.
    #Check with user that the directory and all details of the the directory are correct.
    #For each file, take it and move it to original directory
