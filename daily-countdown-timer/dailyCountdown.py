'''
PLAN for the code:
#Get constants
    #Get current Year number
    #Get current Month number
    #Get current Day number

#Check for a countdownDir.txt in this file's location
    #If it doesn't exist, move on
    #If it does, check for the existance of the target
        #If any of the above fails, prompt for file location. Repeat until everything is okay.

#Once done prompting, move onto updating the file.
    #Line 31 of the file is Year
    #Line 32 of the file is Month
    #Line 33 of the file is Day
'''
import os
import sys
import datetime

year = str(datetime.date.today().year)
month = str(datetime.date.today().month)
day = str(datetime.date.today().day)


scriptDirectory = str(sys.path[0])[:-int(len(sys.argv[0]))] #Should be the directory of the script, not including the script itself

directory = ''
newString = ''

dirExist = False
filename = 'CountDownTimer.ini'
fileLength = len(filename)

#Check for the existance of the correct file
while not dirExist:
    targetDir = open('target.txt', 'r')
    listDir = targetDir.readlines()
    if len(listDir) != 0:
        itemDir = listDir[0]
        if itemDir[-fileLength:] == filename:
            print('File found! Directory is:\t' + itemDir)
            dirExist = True
            break


    if not dirExist:
        directory = str(input('\nPlease input the directory of the CountDownTimer.ini file of the script.\nIt\'s typically stored in C:\\Users\\(username)\\Documents\\Rainmeter\\Skins\\Magnumizer\'s Countdown Timer: \n\t'))

    if os.path.exists(directory):
        for root, dirs, file in os.walk(directory, topdown=False):
            if not dirExist:
                for item in file:
                    if dirExist:
                        break

                    itemDir = os.path.join(root, item)

                    if str(item) == filename:
                        print('\nFile found! Directory is:\t' + itemDir)
                        dirExist = True

#write directory to file
targetFile = open('target.txt', 'w')
targetFile.write(itemDir)
targetFile.close

#Editing the settings file string
itemFile = open(itemDir, 'r')
itemContents = itemFile.readlines()

contentLength = len(itemContents)
if contentLength < 33:
    print('Something is wrong with the file. Please check it for any errors.')
else:
    itemContents[30] = 'year = ' + year + '\n'
    itemContents[31] = 'month = ' + month + '\n'
    itemContents[32] = 'day = ' + day + '\n'

itemFile.close

#Creatubg a new string to write to the file
newItemFile = open(itemDir, 'w')
i = 0
while True:
    if i == contentLength:
        break
    newString += str(itemContents[i])
    i += 1

newItemFile.write(newString)
