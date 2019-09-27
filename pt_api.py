#!/usr/bin/python3

# Polish Tracker API script
# Created by: Nimloth

import json
import requests
from pathlib import Path
import os

os.system('clear')

class bcolors:
    PINK = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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
                print ("API Key: " + bcolors.PINK + api_token + bcolors.ENDC)
                print ("Watch dir: " + bcolors.PINK + watch_path + bcolors.ENDC)
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
            try:
                input("Press enter to continue")
            except SyntaxError:
                pass
            os.system('clear')

headers = {'API-Key': api_token}

def get_account_details():
    api_url_base = 'https://api.pte.nu/users/myprofile'
    response = requests.get(api_url_base, headers=headers)

    if response.status_code == 200:
        print json.dumps(response.json(), sort_keys=True, indent=4)
        try:
            input("Press enter to continue")
        except SyntaxError:
            pass
    else:
        print (response.status_code)
        print json.dumps(response.json(), sort_keys=True, indent=4)

def get_torrents_list():
    amount = int(input('Number of torrents to return (1-250): '))

    if amount > 250:
        print ('More than 250 entered. Defaulting to 50.')

    api_url_base = 'https://api.pte.nu/torrents/list?num=%s' % (amount)
    response = requests.get(api_url_base, headers=headers)

    if response.status_code == 200:
        json_data = json.loads(response.text)
        for item in json_data:
            print ("ID: "+ bcolors.BOLD + str(item['id']) + bcolors.ENDC + "     Name: " + bcolors.BOLD + str(item['name']) + bcolors.ENDC)
        try:
            input("Press enter to continue")
        except SyntaxError:
            pass
    else:
        print (response.status_code)
        print json.dumps(response.json(), sort_keys=True, indent=4)

def get_torrent_details():
    amount = int(input('Please enter Torrent ID: '))
    api_url_base = 'https://api.pte.nu/torrents/torrent/%s' % (amount)
    response = requests.get(api_url_base, headers=headers)

    if response.status_code == 200:
        print json.dumps(response.json(), sort_keys=True, indent=4)
        try:
            input("Press enter to continue")
        except SyntaxError:
            pass
    else:
        print (response.status_code)
        print json.dumps(response.json(), sort_keys=True, indent=4)

def download_torrent():
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
            print (bcolors.GREEN + json_data['name'] + bcolors.ENDC + ' file downloaded to ' + bcolors.BLUE + path + bcolors.ENDC)
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
    print_menu()
    choice = int(input("Enter your choice [1-5]: "))
     
    if choice==1:
        get_account_details()
    elif choice==2:
        get_torrents_list()
    elif choice==3:
        get_torrent_details()
    elif choice==4:
        download_torrent()
    elif choice==5:
        loop=False # This will make the while loop to end as not value of loop is set to False
    else:
        raw_input("Wrong option selection. Enter any key to try again..")
