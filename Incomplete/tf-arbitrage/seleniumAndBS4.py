import bs4
import json
import time
import requests
from steampy.guard import generate_one_time_code
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

#Load variables from other files
infoFile = open(".\info.txt", "r")
infoArray = infoFile.readlines()
# Set API
api_key = infoArray[1][:-1]
# Steam steamname
steamname = str(infoArray[3][:-1])
# Steam password
password = str(infoArray[5][:-1])
# steam's Shared Secret
secret = infoArray[7]
delay = 5

def getAuthCode():
    steamPyAuthCode = generate_one_time_code(secret)
    return steamPyAuthCode


#Logs into steam, given correct authcode
def scraptfScan(authCode):
    elements = []

    #Browser setup
    browser = webdriver.Chrome()
    browser.maximize_window()
    browser.get("https://scrap.tf/buy/hats")
    wait = WebDriverWait(browser, delay)
    wait.until(EC.element_to_be_clickable((By.ID, "steamAccountName"))).send_keys(steamname)
    wait.until(EC.element_to_be_clickable((By.ID, "steamPassword"))).send_keys(password)
    wait.until(EC.element_to_be_clickable((By.ID, "steamPassword"))).send_keys(Keys.RETURN)
    wait.until(EC.element_to_be_clickable((By.ID, "twofactorcode_entry"))).send_keys(authCode)
    wait.until(EC.element_to_be_clickable((By.ID, "twofactorcode_entry"))).send_keys(Keys.RETURN)

    #Load listings from site
    time.sleep(delay)
    browser.get("https://scrap.tf/buy/hats")
    time.sleep(delay)
    #Use soup on finished page
    soup = bs4.BeautifulSoup(browser.page_source, "html.parser")
    elementContainers = soup.find_all('div', class_="items-container")
    for container in elementContainers:#Site has all items in divs in item container classes, this selects all of them
        for element in container.find_all('div'):#Tracks down all divs in the results
            dataID = element.get('data-id')#Only processes divs with a data-id attribute
            if (dataID != None and element.get('data-content') != "&lt;b&gt;This item is overstocked and cannot be sold.&lt;/b&gt;"):
                elemData = [] #Refresh elemData variable, to store information
                elemData.append(element['class'][2][-1])#Item Quality Number
                elemData.append(element.get('data-title'))#Item Name
                elemData.append(element.get('data-bot23-count'))#Num of item available
                elemData.append(dataID)#Item ID Number
                elemData.append(element.get('data-content')[-20:-5])#Item content, incl. Cost
                elements.append(elemData) #Should select each item

    for elem in elements:
        print(elem)

def main():
    scraptfScan(getAuthCode())

main()
