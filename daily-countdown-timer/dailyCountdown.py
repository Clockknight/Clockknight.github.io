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
#filename = 'CountDownTimer.ini'
filename = 'dummy.txt'

#Check for the existance of the correct file
while not dirExist:
    directory = str(input('Please input the directory of the directory of the script here: '))
    if os.path.exists(directory):
        for root, dirs, file in os.walk(directory, topdown=False):
            if not dirExist:
                for item in file:
                    if dirExist:
                        break

                    itemDir = os.path.join(root, item)

                    if str(item) == filename:
                        print('File found! Directory is:\t' + itemDir)
                        dirExist = True

#write directory to file
targetFile = open('target.txt', 'w')
targetFile.write(itemDir)
targetFile.close

#Editing the settings file
itemFile = open(itemDir, 'r')
itemContents = itemFile.readlines()
itemContents[30] = 'year = ' + year
itemContents[31] = 'month = ' + month
itemContents[32] = 'day = ' + day
