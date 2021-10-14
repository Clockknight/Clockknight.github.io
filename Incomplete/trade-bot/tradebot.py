import time
from steampy.client import SteamClient

def main():
    #Setting up robot
    src = "./secureinfo.txt"
    file = open(src, "r")

    info[] = (file.readlines())
    API = info[1]
    username = info[3]
    file = info[5]

    print(API)
    print(username)
    print(file)

    file.close


main()
