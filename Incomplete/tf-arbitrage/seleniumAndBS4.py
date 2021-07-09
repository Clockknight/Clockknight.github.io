import time
import requests, bs4
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




#Load variables from other files
infoFile = open(".\info.txt", "r")
infoArray = infoFile.readlines()
# Set API
api_key = infoArray[1]
# Steam username
username = infoArray[3]
# Steam password
password = infoArray[5]
authcode = "A"

#Define other Variables
delay = 3

'''
#Trying out "steam" library to get authentication
wa = MobileWebAuth('steamuser')
wa.cli_login()

sa = SteamAuthenticator(backend=wa)
sa.add()    # SMS code will be send to the account's phone number
sa.secrets  # dict with authenticator secrets (SAVE THEM!!)

# save the secrets, for example to a file
json.dump(sa.secrets, open('./mysecrets.json', 'w'))

# HINT: You can stop here and add authenticator on your phone.
#       The secrets will be the same, and you will be able to
#       both use your phone and SteamAuthenticator.

sa.finalize('SMS CODE')  # activate the authenticator
sa.get_code()  # generate 2FA code for login
sa.remove()  # removes the authenticator from the account
'''


#Using selenium to log in and then get the page
browser = webdriver.Chrome()
browser.get('https://scrap.tf/buy/hats')
#Log into steam then proceed to new page
userbox = browser.find_element_by_name("username")
userbox.send_keys(username)
passbox = browser.find_element_by_name("password")
passbox.send_keys(password)
signin = browser.find_element_by_id("imageLogin")
#signin.click()
WebDriverWait(browser, delay).until(EC.presence_of_element_located(browser.find_element_by_id('twofactorcode_entry')))
authbox = browser.find_element_by_id("twofactorcode_entry")
authbox.send_keys(authcode)
submitBtn = browser.find_element_by_class("auth_button leftbtn")
submitBtn.click()

#Load listings from site
WebDriverWait(browser, delay).until(EC.presence_of_element_located(browser.find_element_by_id('...')))



#Use soup on finished page
soup = bs4.BeautifulSoup(browser.page_source, "html.parser")
elements = soup.select('')
print(elements)
