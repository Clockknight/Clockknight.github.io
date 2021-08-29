import re

#Declare file directory
fileDir = "regexResults.txt"
#Give permission to read from file
file = open(fileDir, "r")
#Store lines
strings = file.readlines()
file.close()
#Open file with write permission
file = open(fileDir, "w")

print(strings)

#Use regexes to parse information 
regex = re.compile('Costs[\d\s\w.,]*refined')
strings[1] = regex.match(strings[0])
strings[3] = regex.match(strings[2])
regex = re.compile('\d{1,2}')
strings[5] = regex.match(strings[4])
strings[7] = regex.match(strings[6])


#Write results to text file
file.writelines(strings)
file.close()
