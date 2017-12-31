# Ants: A virtual random based ant-like life form


## Screenshot

![Ants screenshot](screenshot.png)

## Disclaimer

This module is intended to run as a python 2.7 module and is provided AS IS under the WTFPL (See LICENSE.TXT).

This module has been tested on Linux systems **ONLY**.

As it uses python 2.7 standard modules only it may run on Windows or MacOS.


## Content

./README.md
./screenshot.png
./playground.py
./config.py
./farm.py
./mine.py
./ant.py
./LICENSE.TXT
./url.txt
./ants.py
./display.py
./utils.py
./doc/playground.html
./doc/ant.html
./doc/farm.html
./doc/mine.html
./doc/display.txt
./doc/farm.txt
./doc/config.txt
./doc/mine.txt
./doc/config.html
./doc/ant.txt
./doc/utils.html
./doc/playground.txt
./doc/utils.txt
./doc/display.html


## Install from file:

* Copy the module directory in any directory of your home dir.

## Install from github

Clone the Github repository with the followning command

```
$ git clone https://github.com/doug-letough/ants.git ants
```


## Run the Ants application

Run the following commands

```
$ cd ants
$ python -m ants
```

As **this module is a multitheaded program**, closing the main window will **NOT** exit the application.

To quit the application, run the following command:

```
$ kill -15 $(ps aux | grep "python -m ants" | grep -v grep | awk -F ' ' '{print $2}')
```


## Logging

This application logs many things to stderr.

If you want to keep the logs of your runs, start the application with the following command:

```
$ python -m ants 2>&1 | tee -a ants.log
```

This will still display the log to stderr and log this output to the ants.log file.

## API documentation

See ./documentation

## Uninstall

Simply remove the module directory. 


## Configuration

The configuration of this application is done by modifing
