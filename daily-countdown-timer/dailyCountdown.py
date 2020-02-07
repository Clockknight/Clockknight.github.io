import os
import sys
'''
PLAN for the code:
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
year = 2020
month = 2
day = 6


dailyDirectory = str(sys.path[0])[:-int(length(sys.argv[0]))] #Should be the directory of the script, not including the script itself
directory = ''
dirExist = False


#Check for the existance of the correct file
while not dirExist:
    directory = str(input('Please input the directory of the '))
