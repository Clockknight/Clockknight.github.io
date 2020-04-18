import os
import sys
import shutil
from shutil import copyfile

i = -2
raiseCount = 0

deleteMode = False
unsafeMode = False
dirNoExist = True

errorIndexes = []
errorList = []
fileList = []
fileDestinationList = []

directory = ''

#Check argv for any modes passed through
if len(sys.argv) > 1:
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == '-u' and unsafeMode == False:
            print('\nUnsafe Mode activated! The program will no longer prompt to okay moving or copying files.')
            unsafeMode = True
        if sys.argv[i] == '-d' and deleteMode == False:
            print('\nDelete Mode activated! The program will now move files instead of copying them.')
            deleteMode = True

#Take input from user, to an exiting directory
while dirNoExist:
    directory = input('\nPlease input a directory to scan for files to raise.\n\t')

    #If the path exists, leave the loop and continue with the rest of the program.
    if os.path.exists(directory):
        print('\nPath found. Processing for files in directory and any subdirectories.\n')
        directoryCount = len(directory)
        dirNoExist = False
    #Otherwise, keep looping until the program is done.
    else:
        print('\nSorry! Path not found. Please try again.')

#Use os.walk to find every file in every folder/subfolder
for root, dirs, files in os.walk(directory, topdown=False):
    #If the file needs to be moved, increase the counter by 1
    if root != directory:
        for name in files:#For each file in a subfolder
            scanFile = os.path.join(root, name)#Identify it by its full path
            fileList.append(scanFile)#Make a list with all of those files
            fileDestinationList.append(os.path.join(directory, name))
            raiseCount += 1
            print(scanFile)

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
    print(i)

    try:
        #If deleteMode is on use the move function instead of copyfile
        if deleteMode:
            shutil.move(fileList[i], fileDestinationList[i])
            print(fileList[i], 'moved to\n', fileDestinationList[i])

        #Otherwise, just copy the file
        else:
            shutil.copyfile(fileList[i], fileDestinationList[i])
            print(fileList[i], 'copied to\n', fileDestinationList[i])

    except:
        errorIndexes.append(i)#Keep track of failed raises' indexes
        errorList.append(sys.exc_info()[0])#Keep track of the errors of the raise errors

    i += 1

if len(errorList) > 0:
    for error in errorList:
        print('Could not raise the following files:')

        print(error)
