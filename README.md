Passwd Manager README FILE

# Project Home

[project @ Github](http://github.com/sk1418/passwdmanager/)

# Introduction
Passwd Manager is a cross-platform password management tool.

# Features
As a password managment tool, Passwd Manager keeps as simple as possible. Currently Passwd Manager has following features:

- Master password encrypted with MD5
- all password and username/account name entries encrypted with CAST algorithm
- flexible tags
- with random password generator
- simple,fast search
- internationalized note encryption (secret text)
- auto-backup up to most recent x times of application starts. (x is configurable)
- Simple enough huh? ;)

# Screenshots

![mainWindow](https://raw.github.com/sk1418/sharedResources/master/passwdmanager/passwd1.png)

![accountDetails](https://raw.github.com/sk1418/sharedResources/master/passwdmanager/passwd2.png)

![pwdGenerator](https://raw.github.com/sk1418/sharedResources/master/passwdmanager/passwd3.png)

![addAccount](https://raw.github.com/sk1418/sharedResources/master/passwdmanager/passwd4.png)

# Requirement to run passwd manager:

- python 2.6.x
- wxPython 2.8
- pycrypto 2.6

# Download

- Source code downloading: simple via github
- All-in-one binary package for windows, please click[ here ](https://code.google.com/p/passwdmanager/downloads/list)

# Installation (Linux)

	sudo python setup.py install


## For Archlinux user

The passwdmanager is available in AUR, for stable version:
	
	yaourt -S passwdmanager

for git version:

	yaourt -S passwdmanager-git


# Upgrade

**since version 1.2.0, upgrade the application by installation new version.**

- 1.0.x to 1.1.x upgrade (deprecated):

using upgrade tool `<appHome>/passwdmanager/upgrade.py `to upgrade

##for Windows user
1. Exit the application
2. Backup your data directory and config directory. (`<appHome>/data and conf`)
3. Download and extract the new version
4. overwrite the data directory with your backup
5. start the application, check the version number via Help->About

# Tips
- change the `data.path` in  `$HOME/.passwdManager/passwdManager.conf` (`$APP_HOME/conf/win.conf` on Windows) to some cloud storage (Dropbox for example) managed directory, your data file would be automatically synced. Useful when working on different computers.

# Command to start the application

	pwmanager

or find the launcher in menu 


# DEFAULT MASTER PASSWORD

`"password"` (without the quotes)

#change logs

v1.2.0
 
* using pycrypto 2.6 (auto upgrade with backup)
* code cleaning
* auto focus search textbox when entering the application
* introduce new config file
* Feature: auto backup
* Feature: data and config file under $HOME/.passwdManager (Linux)

v1.1.0

* some improvement on GUI
* code cleaning
* Feature: secret text
* Feature: username/accountname is also stored with encryption.

v1.0.4

* Feature: Password Generator
* Tag removing: now tag still in used can also be removed.
* Search box :  pressing <Enter> key in search textbox will trigger the search 

v1.0.3

* Feature:Update notification (popup & statusbar)
* Feature:Update checking menu item
* Current chosen tag will be selected automatically in Add New Account dialog
* BugFix: [WINDOWS] GUI dialog/button size  


v1.0.2

* BugFix: [WINDOWS] UTF-8 encoding problem when printing the tag names

v1.0.1

* BugFix: [WINDOWS] click 'Exit' in Login Dialog, application exits with error message.
* BugFix: [ALL] Edit Account Dialog, error occurs when doing the user input validation

v1.0.0

* 1st release


