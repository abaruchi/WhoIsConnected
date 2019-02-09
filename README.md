# WhoIsConnected

[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/23a523978b6a457e9e9d5d2cef3c91fb)](https://www.codacy.com/app/abaruchi/WhoIsConnected?utm_source=github.com&utm_medium=referral&utm_content=abaruchi/WhoIsConnected&utm_campaign=Badge_Coverage) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/23a523978b6a457e9e9d5d2cef3c91fb)](https://www.codacy.com/app/abaruchi/WhoIsConnected?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=abaruchi/WhoIsConnected&amp;utm_campaign=Badge_Grade) [![MIT Licence](https://badges.frapsoft.com/os/mit/mit.svg?v=103)](https://opensource.org/licenses/mit-license.php)

## Contents
1. [Introduction](#introduction)
2. [How to Install](#how-to-install)
3. [Implementation Details](#implementation-details)


## Introduction
This is another personal project that aims to detect new connections on my home network and warn me about it. I installed some time ago a raspiberry as DNS and DHCP ([Pi-Hole](https://pi-hole.net/)). So, I wanted to be aware of which devices was being connected, disconnected and for how long it was using my network. Of course that checking the DHCP log file I could get this kind of data, but I wanted to organize it in a database and be able to follow the connection and see the history of all connections.

The WhoIsConnected project aims to warn the user about devices using his network. Any of conditions bellow, the user will receive an email:
- New devices: Any device(s) that was never connected to the network;
- Status Change: If any device goes online or offline.  


## How to Install
For now, just clone this repository and run the script `runner.py`.

- Clone this repository
```bash****
$ git clone https://github.com/abaruchi/WhoIsConnected.git
```

- Install all requirements.
```bash
$ pip install -r requirements.txt
```

- Customize a `config.ini`. There is an example which you can copy and change according to your needs. 
```bash
$ cp -p config_example.ini config.ini
$ vi config.ini
```
This configuration file you can set your email address, pooling time, where the DHCP file is located and so on.

- Run the `runner.py` script.
```bash
$ python runner.py
```

Since this is script run as a daemon, you will not receive any message (even error messages). Since all devices inside DHCP file will not be stored in SQLite database, you should receive an email after the firs run with a list of **New Devices**.

### Dependencies
This project was written in Python 3.6, so you should run it using Python > 3. Also, all dependencies are listed in `requirements.txt` file.


## Implementation Details

### Pony ORM and DB Design


### Code Structure

