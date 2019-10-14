# Polish Tracker API script
Tool to use existing API provided by PolishTracker

---

### Installation
#### Requirements
- git
- python3
- python3-pip

#### Download  
`git clone https://github.com/NimlothPL/PolishTracker-API.git`

#### Enter project folder  
`cd PolishTracker-API`

#### Install modules  
`pip3 install -r requirements.txt`

---

### Usage
#### General
1. Menu version:
    'python3 pt_api.py --menu'
    
2. Cli version:
    'python3 pt_api.py --help'

#### Example  
`python3 pt_api.py --help'

#### Command line arguments
```
usage: pt_api.py [-h] [--menu] [--account] [--list LIST] [--torrent TORRENT]
                 [--download DOWNLOAD] [--version]

PolishTracker API script

optional arguments:
  -h, --help           show this help message and exit
  --menu               Shows menu.
  --account            Retrieves information about user account.
  --list LIST          Number of torrents to return (1-250).
  --torrent TORRENT    Retrieves information about specific torrent.
  --download DOWNLOAD  Download specific torrent.
  --version            show program's version number and exit
```

---
