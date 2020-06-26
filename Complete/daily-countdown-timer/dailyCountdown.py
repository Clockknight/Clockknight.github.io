import os
import sys
import datetime

targetDay = datetime.date.today + datetime.timedelta(days=1)
year = str(targetDay.year)
month = str(targetDay.month)
day = str(targetDay.day)


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
        directory = str(input('\nPlease input the directory of the CountDownTimer.ini file of the script.\nIt\'s typically stored in C:\\Users\\(username)\\Documents\\Rainmeter\\Skins\\Magnumizer\'s Countdown Timer: \n(The script may target Skins\\@Backup):\t'))

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
