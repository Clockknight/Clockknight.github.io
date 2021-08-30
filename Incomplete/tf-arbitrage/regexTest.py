import re

#Declare file directory
fileDir = "regexResults.txt"
#Give permission to read from file
file = open(fileDir, "r")
#Store lines
strings = file.readlines()
strings.append('')
file.close()
#Open file with write permission
file = open(fileDir, "w")

print(strings[0])

#Use regexes to parse information and then
regex = re.compile(r"\s[\d\s\w.,]*refined")
strings[1] = regex.findall(strings[0])[0][1:] + "\n"
strings[3] = regex.findall(strings[2])[0][1:] + "\n"

#Write results to text file
file.writelines(strings)
file.close()
