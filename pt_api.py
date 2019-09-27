#!/usr/bin/python3

# Polish Tracker API script
# Created by: Nimloth

import json
import requests
from pathlib import Path

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
                print ("Used API-Key: " + api_token)
                loop=False
    else:
        # Create config file
        with open("config.json", "w") as json_config_file:
            key = raw_input('Enter API Key (20 character long): ')
            print "Your API Key is: ", key

            path = raw_input('Enter torrent watch directory: ')
            print "Your Torrent watch directory is: ", path

            data = {"config":[{'api_token': key,'watch_path': path}]}
            json.dump(data, json_config_file, indent=4)

headers = {'API-Key': api_token}

def get_account_details():
    api_url_base = 'https://api.pte.nu/users/myprofile'
    response = requests.get(api_url_base, headers=headers)

    if response.status_code == 200:
	print json.dumps(response.json(), sort_keys=True, indent=4)
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
            print ("ID: "+ str(item['id']) + "     Name: " + str(item['name']))
    else:
        print (response.status_code)
        print json.dumps(response.json(), sort_keys=True, indent=4)

def get_torrent_details():
    amount = int(input('Please enter Torrent ID: '))
    api_url_base = 'https://api.pte.nu/torrents/torrent/%s' % (amount)
    response = requests.get(api_url_base, headers=headers)

    if response.status_code == 200:
        print json.dumps(response.json(), sort_keys=True, indent=4)
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
            print (json_data['name'] + ' file downloaded to ' + path)
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
