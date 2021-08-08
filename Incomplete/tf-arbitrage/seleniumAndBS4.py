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
def seleniumLogin(authCode):
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
    #WebDriverWait(browser, delay).until(EC.presence_of_element_located(browser.find_element_by_id('...')))

    #Use soup on finished page
    soup = bs4.BeautifulSoup(browser.page_source, "html.parser")
    elements = soup.select('')
    print(elements)

def main():
    authCode = getAuthCode()
    seleniumLogin(authCode)

main()
