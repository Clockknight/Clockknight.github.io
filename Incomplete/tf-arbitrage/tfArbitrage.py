import os
import openpyxl
from openpyxl import Workbook
import requests
from bs4 import BeautifulSoup
import time
from steampy.client import SteamClient
from fake_useragent import UserAgent


#Function definitions
#Creates info.txt file
def infoCreate():
    infoFile = open(infoDirectory, "w+")
    infoFile.write('''#Put steam API key on line below

    #Put Username on line below

    #Put Password on line below

    #Put shared secret on line below''')
    infoFile.close()

#Creates spreadsheet for data storage
def sheetCreate():
    print("--Creating tfArbitrage.xlsx in current directory")
    workbook = Workbook()
    sheet = workbook.active

    sheet["A1"] = "Name"
    sheet["B1"] = "Quality"
    sheet["C1"] = "Listed Price"
    sheet["D1"] = "Site Found"
    sheet["E1"] = "Profitability"

    workbook.save(filename="tfArbitrage.xlsx")

    listingSearch()

#Will look through websites and note all items listed
def listingSearch():
    print(api_key)
    print("-- Beginning search for discounted items.")
    try:
        print("-- searching scrap.tf for discounted items")


        scrapurl = 'https://scrap.tf/buy/hats'

        #Checking for url error codes
        req = requests.get(scrapurl)
        print(req.status_code)

        page = requests.get(scrapurl, headers=headers)
        soup = BeautifulSoup(page.text, "html.parser")
        print(soup)
    except:
        print('-- scraptf Fail Case.')
    '''
        try:
            print("-- searching backpack.tf for discounted items")

            bpurl = 'https://scrap.tf/buy/hats'

            #Checking for url error codes
            req = requests.get(scrapurl)
            print(req.status_code)

            page = requests.get(scrapurl)
            soup = BeautifulSoup(page.text, "html.parser")
        except:
            print('-- bptf Fail Case)
    '''
    listingPosts()

#Will create listings for each item considered "Viable" on the spreadsheet
def listingPosts():
    print("-- Posting listings for inventory.")
    tradeBot()

#Will respond to appropriate messages on steam
    #Should be running consistently, as the rest of the program is running. Or run itermittently as it checks for messages.
def tradeBot():
    print("-- Managing incoming trade offers and messages.")
    listingPosts()

def main():
    if(os.path.exists(sheetDirectory)):
        listingSearch()
    else:
        sheetCreate()

#Global Variables
#User Agent Variables
ua = UserAgent()
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13'}

#SteamPy Variables
#Read info.txt
infoDirectory = ".\info.txt"
if(os.path.exists(infoDirectory) != True):
    infoCreate()

infoFile = open(infoDirectory, "r")
infoArray = infoFile.readlines()
# Set API
api_key = infoArray[1]
# Steam username
username = infoArray[3]
# Steam password
password = infoArray[5]
# Set path to SteamGuard file
steamguard_path = '..\Steamguard.txt'


sheetDirectory = ".\tfArbitrage.xlsx"

main()
