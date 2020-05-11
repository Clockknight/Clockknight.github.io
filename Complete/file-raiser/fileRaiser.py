import os
import sys
import shutil
from shutil import copyfile
import pyperclip

i = 0

deleteMode = False
unsafeMode = False
dirNoExist = True

errorIndexes = []
errorList = []
fileList = []
fileDestinationList = []
directoryList = []

directory = ''
pasteDir = ''
filepath = './settings.txt'




'''#Check for previous settings
settingsFile = open(filePath, 'r+')
settingsData = settingsFile.read()
for char in settingsData:


settingsFile.close()

#Check argv for any modes passed through
if len(sys.argv) > 1:
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == '-u'
            unsafeMode = True
        if sys.argv[i] == '-d'
            deleteMode = True

if deleteMode == True:
    print('\nDelete Mode activated! The program will now delete files\' folders instead of just moving them.')
if unsafeMode == False:
    print('\nUnsafe Mode activated! The program will no longer prompt to okay moving or copying files.')'''


def doesDirExist(directory):
    targetCount = 0

    #If the path exists, leave the loop and continue with the rest of the program.
    if os.path.exists(directory):
        print('Path found. Processing for any subfiles in subdirectories.')
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
                    targetCount += 1#If the file needs to be moved, increase the counter by 1

        print(directoryList)

        #If any files that need to be raised are found, the code can stop referring to this function.
        if targetCount > 0:
            dirNoExist = False

        #Otherwise, try again at the start of the loop.
        else:
            print('\nSorry! No files in subfolders to be found. Please input another directory.')

    else:
        print('\nSorry! Path not found. Please input another directory.')

    #No matter what, return targetCount as a count and as a check
    print('\n')
    return targetCount



def main():
    raiseCount = 0

    #Take input from user, to an exiting directory
    while dirNoExist:
        directory = input('\nPlease input a directory to scan for files to raise.\nOr, type \"PASTE\" to grab the directory from your clipboard.\n')

        #If the user inputs paste
        if directory.casefold() == 'PASTE'.casefold():
            #The program checks the immediate clipboard for a directory
            pasteDir = pyperclip.paste()
            print('\nNew paste found. Text is: ' + pasteDir)
            raiseCount = doesDirExist(pasteDir)



            #If the function fails, it prints this error message for the user
            if not (raiseCount > 0):
                print('The directory doesn\'t work. Please put another one on your clipboard and input paste again.')

        #If it succeeds, then it will just leave the while loop
        else:
            print('\n')
            raiseCount = doesDirExist(directory)



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

        #Try to raise the files
        try:
            #If deleteMode is on use the move function instead of copyfile
            if deleteMode:
                shutil.move(fileList[i], fileDestinationList[i])
                print(fileList[i], 'moved to\n', fileDestinationList[i])

                emptyDir = directoryList[i]
                shutil.rmtree(emptyDir)
                directoryList.remove(emptyDir)


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

main()
