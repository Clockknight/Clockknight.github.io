'''
PLAN for the code:
#DONE
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

year = datetime.date.today().year
month = datetime.date.today().month
day = datetime.date.today().day

scriptDirectory = str(sys.path[0])[:-int(len(sys.argv[0]))] #Should be the directory of the script, not including the script itself
directory = ''
dirExist = False


#Check for the existance of the correct file
while not dirExist:
    directory = str(input('Please input the directory of the directory of the script here: '))
    if os.path.exists(directory):
        for file in os.walk(directory):
            print(file)
            if file == 'dailyCountdown.py':
                print('ding')
