import os
import sys

raiseCount = 0

deleteMode = False
dirNoExist = True
unconfirmed = True

directory = ''

if len(sys.argv) > 1:
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == '-d' and deleteMode == False:
            print('\nDelete Mode activated! The program will now delete files after moving them.')
            deleteMode = True

while dirNoExist:
    directory = input('\nPlease input a directory to scan for files to raise.\n\t')

    if os.path.exists(directory):
        print('\nPath found. Processing for files in directory and any subdirectories.\n')
        dirNoExist = False
    else:
        print('\nSorry! Path not found. Please try again.')

directoryCount = len(directory)

#Use os.walk to find every file in every folder/subfolder
for root, dirs, files in os.walk(directory, topdown=False):
    #If the file needs to be moved, increase the counter by 1
    if root != directory:
        for name in files:
            scanFile = os.path.join(root, name)
            raiseCount += 1
            print(scanFile)
            #Only do this if the file isnt already in the directory.


#Display the amount of files that would be raised by the program.
while unconfirmed:
    print('\n',raiseCount, 'files in sub-folders were found. Please type\n\tRAISE\tor\tQUIT\nto raise the highlighted files or stop the program now, respectively.')
    #Check with user that the directory and all details of the the directory are correct.
    confirmation = input()

    if confirmation == 'RAISE':
        unconfirmed = False
        print('\nProcessing...')
    elif confirmation == 'QUIT':
        print('\nClosing down...')
        sys.exit()
    else:
        print('\nNo valid input was found. Be sure to correctly capitalize your input')

    #For each file, take it and move it to original directory
