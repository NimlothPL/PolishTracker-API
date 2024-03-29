#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" PolishTracker API script """

__author__ = "Nimloth"
__copyright__ = "Copyright 2019, Nimloth"
__license__ = "GPLv3"
__version__ = "1.0.0"

import argparse
from colorama import Fore, Back, Style
import json
import math
import sys
from pathlib import Path
import requests

parser = argparse.ArgumentParser(description='PolishTracker API script')

parser.add_argument('--menu', dest="menu",
                    help='Shows menu.', action='store_true')
parser.add_argument('--account', dest="account",
                    help='Retrieves information about user account.', action='store_true')
parser.add_argument('--list', type=int, dest="list",
                    help='Number of torrents to return (1-250).')
parser.add_argument('--torrent',  type=int, dest="torrent",
                    help='Retrieves information about specific torrent.')
parser.add_argument('--download',  type=int, dest="download",
                    help='Download specific torrent.')
parser.add_argument('--version', action='version', version='%(prog)s 0.1')

args = parser.parse_args()

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
        print(json.dumps(response.json(), indent=4))
#        json_data = json.loads(response.text)
#        print("Username: "+ Style.BRIGHT + str(json_data['username']) + Style.NORMAL)
#        print("Rank: "+ Style.BRIGHT + str(json_data['rank']) + Style.NORMAL)
#        print("Downloaded: "+ Style.BRIGHT + str(convert_size(json_data['downloaded'])) + Style.NORMAL)
#        print("Uploaded: "+ Style.BRIGHT + str(convert_size(json_data['uploaded'])) + Style.NORMAL)
    else:
        print(response.status_code)
        print(json.dumps(response.json(), sort_keys=True, indent=4))

def torrents_list():
    if args.list is None:
        try:
            amount = int(input('Number of torrents to return (1-250): '))
        except ValueError:
            print("Wrong value entered. Defaulting to 50..")
            print("")
            amount = 50
        
        if amount > 250:
            print('Value is higher than 250. Defaulting to 50..')
            print("")
        
        api_url_base = 'https://api.pte.nu/torrents/list?num=%s' % (amount)
        response = requests.get(api_url_base, headers=headers)
    else:
        api_url_base = 'https://api.pte.nu/torrents/list?num=%r' % (args.list)
        response = requests.get(api_url_base, headers=headers)

    if response.status_code == 200:
        json_data = json.loads(response.text)
        for item in json_data:
            print("ID: "+ Style.BRIGHT + str(item['id']) + Style.NORMAL + "   Size: "+ Style.BRIGHT + str(convert_size(item['size'])) + Style.NORMAL + "   Name: " + Style.BRIGHT + str(item['name']) + Style.NORMAL)
    else:
        print(response.status_code)
        print(json.dumps(response.json(), sort_keys=True, indent=4))

def torrent_details():
    if args.torrent is None:
        loop=True
        while loop:
            try:
                torrent_id = int(input('Please enter Torrent ID: '))
                loop=False
            except ValueError:
                print("Wrong ID entered. Please try again..")
                print("")
        
        api_url_base = 'https://api.pte.nu/torrents/torrent/%s' % (torrent_id)
        response = requests.get(api_url_base, headers=headers)
    else:
        api_url_base = 'https://api.pte.nu/torrents/torrent/%r' % (args.torrent)
        response = requests.get(api_url_base, headers=headers)

    if response.status_code == 200:
        print(json.dumps(response.json(), sort_keys=True, indent=4))
    else:
        print(response.status_code)
        print(json.dumps(response.json(), sort_keys=True, indent=4))

def torrent_download():
    if args.download is None:
        loop=True
        while loop:
            try:
                download = int(input('Please enter Torrent ID: '))
                api_url_base = 'https://api.pte.nu/torrents/torrent/%s' % (download)
                response = requests.get(api_url_base, headers=headers)
                loop=False
            except ValueError:
                print("Wrong ID entered. Please try again..")
                print("")
    else:
        api_url_base = 'https://api.pte.nu/torrents/torrent/%r' % (args.download)
        response = requests.get(api_url_base, headers=headers)

    if response.status_code != 200:
        print(response.status_code)
        print(json.dumps(response.json(), sort_keys=True, indent=4))
    else:
        json_data = json.loads(response.text)

        if args.download is None:
            api_url_base = 'https://api.pte.nu/torrents/download/%s' % (download)
        else:
            api_url_base = 'https://api.pte.nu/torrents/download/%r' % (args.download)

        ## Retrieve watch path from config file
        with open('config.json', 'r') as output:
            data = json.load(output)
            for item in data["config"]:
                path = (item['watch_path'])

        file = (json_data['name']) + ".torrent"
        response = requests.get(api_url_base, headers=headers)
        open(path+file,"wb").write(response.content)

        if response.status_code == 200:
            print('File ' + Fore.GREEN + json_data['name'] + '.torrent' + Fore.RESET + ' created in ' + Fore.GREEN + path + Fore.RESET + ' folder.')
        else:
            print(response.status_code)
            print(json.dumps(response.json(), sort_keys=True, indent=4))

def print_menu():
    print(29 * "-" , "PTv2 API" , 28 * "-")
    print("1. Account details")
    print("2. Torrents List")
    print("3. Retrieve Torrent Info")
    print("4. Download Torrent")
    print("5. Exit")
    print(67 * "-")

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
                #print(67 * "-")
                #print("PT v2 API Key:   " + Style.BRIGHT + api_token + Style.NORMAL)
                #print("Watch Directory: " + Style.BRIGHT + watch_path + Style.NORMAL)
                #print(67 * "-")
                loop=False
    else:
        # Create config file
        print("Config file is missing.")
        with open("config.json", "w") as json_config_file:
            key = input('Enter API Key (20 character long): ')
            print("API Key set to: ", key)
            print("")

            path = input('Enter torrent watch directory (ex. /tmp/): ')
            print("Torrent watch directory set to: ", path)
            print("")

            data = {"config":[{'api_token': key,'watch_path': path}]}
            json.dump(data, json_config_file, sort_keys=True, indent=4)

headers = {'API-Key': api_token}

if args.menu:
    loop=True
    while loop:
        print_menu()

        loop2=True
        while loop2:
            try:
                choice = int(input("Enter your choice [1-5]: "))
                loop2=False
            except ValueError:
                print("Wrong option selection. Please try again..")
                print()
       
        if choice==1:
            account_details()
        elif choice==2:
            torrents_list()
        elif choice==3:
            torrent_details()
        elif choice==4:
            torrent_download()
        elif choice==5:
            loop=False
        else:
            input("Wrong option selection. Enter any key to try again..")

if args.account:
    account_details()

if args.list:
    torrents_list()

if args.torrent:
    torrent_details()

if args.download:
    torrent_download()
