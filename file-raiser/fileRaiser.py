import os
import sys
import shutil
from shutil import copyfile

i = 0
raiseCount = 0

deleteMode = False
unsafeMode = False
dirNoExist = True

errorIndexes = []
errorList = []
fileList = []
fileDestinationList = []
directoryList = []

directory = ''

#Check argv for any modes passed through
if len(sys.argv) > 1:
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == '-u' and unsafeMode == False:
            print('\nUnsafe Mode activated! The program will no longer prompt to okay moving or copying files.')
            unsafeMode = True
        if sys.argv[i] == '-d' and deleteMode == False:
            print('\nDelete Mode activated! The program will now delete files\' folders instead of just moving them.')
            deleteMode = True

#Take input from user, to an exiting directory
while dirNoExist:
    directory = input('\nPlease input a directory to scan for files to raise.\n\t')

    #If the path exists, leave the loop and continue with the rest of the program.
    if os.path.exists(directory):
        print('\nPath found. Processing for any subfiles in subdirectories.')
        directoryCount = len(directory)

        #Use os.walk to find every file in every folder/subfolder
        for root, dirs, files in os.walk(directory, topdown=False):
            if deleteMode == True:
                if len(directoryList) == 0 or directoryList[-1] != root:
                    directoryList.append(root)

            if root != directory:#Check if the root of a file is different than the inputted directory
                for name in files:#If so...
                    scanFile = os.path.join(root, name)#Identify it by its full path
                    fileList.append(scanFile)#Make a list with all of those files
                    fileDestinationList.append(os.path.join(directory, name))#Make a second list with where all the files WILL go
                    raiseCount += 1#If the file needs to be moved, increase the counter by 1


        #If any files that need to be raised are found, continue with the rest of the program.
        if raiseCount > 0:
            print(scanFile)
            dirNoExist = False

        #Otherwise, try again at the start of the loop.
        else:
            print('\nSorry! No files in subfolders to be found. Please input another directory.')

    else:
        print('\nSorry! Path not found. Please input another directory.')


print('ping')
print(directoryList)

#Display the amount of files that would be raised by the program.
while not unsafeMode:
    #Check with user that the directory and all details of the the directory are correct.
    print('\n',raiseCount, 'files in sub-folders were found. Please type\n\tRAISE\tor\tQUIT\nto raise the highlighted files or stop the program now, respectively.')
    confirmation = input()

    if confirmation == 'RAISE':
        unsafeMode = True
        print('\nProcessing...')
    elif confirmation == 'QUIT':
        print('\nClosing down...')
        sys.exit()
    else:
        print('\nNo valid input was found. Be sure to correctly capitalize your input')

#For each file, take it and move it to original directory
while i < raiseCount:
    print('\nMoving file', fileList[i])

    try:
        #If deleteMode is on use the move function instead of copyfile
        if deleteMode:
            shutil.move(fileList[i], fileDestinationList[i])
            print(fileList[i], 'moved to\n', fileDestinationList[i])
            shutil.rmtree(directoryList[i])


        #Otherwise, just copy the file
        else:
            shutil.move(fileList[i], fileDestinationList[i])
            print(fileList[i], 'moved to\n', fileDestinationList[i])

    except:
        errorIndexes.append(i)#Keep track of failed raises' indexes
        errorList.append(sys.exc_info()[0])#Keep track of the errors of the raise errors
        print('Error. Moving to next file.')

    i += 1

for dirs in os.walk(directory, topdown=False):
    print(dirs)

if len(errorList) > 0:
    for error in errorList:
        print('Could not raise the following files:')

        print(error)
