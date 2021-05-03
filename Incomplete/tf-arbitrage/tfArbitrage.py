import time
from steampy.client import SteamClient

# Set API key
api_key = '13C314DA0B61D2A625935F856F1F9958'
# Set path to SteamGuard file
steamguard_path = '..\Steamguard.txt'
# Steam username
username = 'Clockknight'
# Steam password
password = 'Tyler69here413'


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
