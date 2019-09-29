#!/usr/bin/python3

# Polish Tracker API script
# Created by: Nimloth

import json
import requests
from pathlib import Path
import os
import math
from colorama import Fore, Back, Style

os.system('clear')

def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    power = math.pow(1024, i)
    size = round(size_bytes / power, 2)
    return "{} {}".format(size, size_name[i])

def account_details():
    api_url_base = 'https://api.pte.nu/users/myprofile'
    response = requests.get(api_url_base, headers=headers)

    if response.status_code == 200:
        print json.dumps(response.json(), sort_keys=True, indent=4)
    else:
        print (response.status_code)
        print json.dumps(response.json(), sort_keys=True, indent=4)

def torrents_list():
    amount = int(input('Number of torrents to return (1-250): '))

    if amount > 250:
        print ('More than 250 entered. Defaulting to 50.')

    api_url_base = 'https://api.pte.nu/torrents/list?num=%s' % (amount)
    response = requests.get(api_url_base, headers=headers)

    if response.status_code == 200:
        json_data = json.loads(response.text)
        for item in json_data:
            print ("ID: "+ Style.BRIGHT + str(item['id']) + Style.NORMAL + "   Size: "+ Style.BRIGHT + str(convert_size(item['size'])) + Style.NORMAL + "   Name: " + Style.BRIGHT + str(item['name']) + Style.NORMAL)
    else:
        print (response.status_code)
        print json.dumps(response.json(), sort_keys=True, indent=4)

def torrent_details():
    amount = int(input('Please enter Torrent ID: '))
    api_url_base = 'https://api.pte.nu/torrents/torrent/%s' % (amount)
    response = requests.get(api_url_base, headers=headers)

    if response.status_code == 200:
        print json.dumps(response.json(), sort_keys=True, indent=4)
    else:
        print (response.status_code)
        print json.dumps(response.json(), sort_keys=True, indent=4)

def torrent_download():
    download = int(input('Please enter Torrent ID: '))
    api_url_base = 'https://api.pte.nu/torrents/torrent/%s' % (download)
    response = requests.get(api_url_base, headers=headers)

    if response.status_code != 200:
        print (response.status_code)
        print json.dumps(response.json(), sort_keys=True, indent=4)
    else:
        json_data = json.loads(response.text)

        api_url_base = 'https://api.pte.nu/torrents/download/%s' % (download)

        ## Retrieve watch path from config file
        with open('config.json', 'r') as output:
            data = json.load(output)
            for item in data["config"]:
                path = (item['watch_path'])

        file = (json_data['name']) + ".torrent"
        response = requests.get(api_url_base, headers=headers)
        open(path+file,"wb").write(response.content)

        if response.status_code == 200:
            print (Fore.GREEN + json_data['name'] + Fore.RESET + ' file downloaded to ' + Fore.BLUE + path + Fore.RESET)
            try:
                input("Press enter to continue")
            except SyntaxError:
                pass
        else:
            print (response.status_code)
            print json.dumps(response.json(), sort_keys=True, indent=4)

def print_menu():
    print 29 * "-" , "PTv2 API" , 28 * "-"
    print "1. Account details"
    print "2. Torrents List"
    print "3. Retrieve Torrent Info"
    print "4. Download Torrent"
    print "5. Exit"
    print 67 * "-"

loop=True

while loop:
    config_file = Path("config.json")
    # Check if config file exists
    if config_file.is_file():
        # Get API Key from Config
        with open('config.json', 'r') as output:
            data = json.load(output)
            for item in data["config"]:
                api_token = (item['api_token'])
                watch_path = (item['watch_path'])
                print 67 * "-"
                print ("API Key: " + Fore.MAGENTA + api_token + Fore.RESET)
                print ("Watch dir: " + Fore.MAGENTA + watch_path + Fore.RESET)
                loop=False
    else:
        # Create config file
        print ("Config file is missing.")
        with open("config.json", "w") as json_config_file:
            key = raw_input('Enter API Key (20 character long): ')
            print "API Key set to: ", key
            print ""

            path = raw_input('Enter torrent watch directory (ex. /tmp/): ')
            print "Torrent watch directory set to: ", path
            print ""

            data = {"config":[{'api_token': key,'watch_path': path}]}
            json.dump(data, json_config_file, indent=4)

            os.system('clear')

headers = {'API-Key': api_token}

loop=True

while loop:
    print_menu()
    choice = int(input("Enter your choice [1-5]: "))

    if choice==1:
        account_details()
    elif choice==2:
        torrents_list()
    elif choice==3:
        torrent_details()
    elif choice==4:
        torrent_download()
    elif choice==5:
        loop=False # This will make the while loop to end as not value of loop is set to False
    else:
        raw_input("Wrong option selection. Enter any key to try again..")
