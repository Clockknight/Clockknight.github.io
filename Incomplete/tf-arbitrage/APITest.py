import json
import requests

infoDirectory = ".\info.txt"
infoFile = open(".\info.txt", "r")
info = infoFile.readlines()

#Get key from info file, remove the \n at the end of the line from using readlines method
key = info[9][:-1]
#attach key to end of api request
apiGet = 'https://backpack.tf/api/IGetPrices/v4?raw=1&key=' + key

#Get result from bp.tf server
request = requests.get(apiGet).text
#Parse the json into a dict so it's readable
response = json.loads(request)
#test itemName to work with
#Pull itemName from spreadsheet in complete version
itemName = "Australium Tomislav"
#In real version, pull this from spreadsheet
qualNum = "11"
itemInfo = response["response"]["items"][itemName]["prices"][qualNum]["Tradable"]["Craftable"][0]

print(itemInfo["value"])
print(itemInfo["currency"])
