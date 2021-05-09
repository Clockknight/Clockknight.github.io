<<<<<<< HEAD
import requests
from bs4 import BeautifulSoup
import time
from steampy.client import SteamClient
from fake_useragent import UserAgent
=======
import time
from steampy.client import SteamClient
>>>>>>> 8d1051a72c99e1e7ac67a773cfea636ccaabb6c7

# Set API key
api_key = '13C314DA0B61D2A625935F856F1F9958'
# Set path to SteamGuard file
steamguard_path = '..\Steamguard.txt'
# Steam username
username = 'Clockknight'
# Steam password
password = 'Tyler69here413'
<<<<<<< HEAD

#Will look through websites and try to buy any discounted items
    #Called at program start and itermittently
def listingSearch():
    print("-- Beginning search for discounted items.")
    try:
        print("-- searching scrap.tf for discounted items")

        scrapurl = 'https://scrap.tf/buy/hats'

        #Checking for url error codes
        req = requests.get(scrapurl)
        print(req.status_code)

        page = requests.get(scrapurl)
        soup = BeautifulSoup(page.text, "html.parser")
        #print(soup)
    except:
        print('scraptf fail case')

    listingPosts()

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
        print('bptf fail case')
'''

#Will post listings on sites like bazaar.tf and backpack.tf
    #Called after listingSearch
def listingPosts():
    print("-- Posting listings for inventory .")

#Will respond to appropriate messages on steam
    #Should be running consistently, as the rest of the program is running. Or run itermittently as it checks for messages.
def tradeBot():
    print("-- Managing incoming trade offers and messages.")

def main():
    listingSearch()

main()
=======


def main():
    print('This is the chat bot.')
    if not are_credentials_filled():
        print('You have to fill the credentials to run the example')
        print('Terminating bot')
        return
    client = SteamClient(api_key)
    client.login(username, password, steamguard_path)
    print('Bot logged in successfully, polling messages every 10 seconds')
    while True:
        time.sleep(10)
        messages = client.chat.fetch_messages()['received']
        for message in messages:
            client.chat.send_message(message['partner'], "Got your message: " + message['message'])


def are_credentials_filled() -> bool:
    return api_key != '' and steamguard_path != '' and username != '' and password != ''


if __name__ == "__main__":
    # execute only if run as a {value for value in variable}ript
    main()
>>>>>>> 8d1051a72c99e1e7ac67a773cfea636ccaabb6c7
