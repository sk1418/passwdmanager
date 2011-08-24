'''
Created on Apr 3, 2009

@author: kent
'''


# root password
#Default:password
#MD5:5f4dcc3b5aa765d61d8327deb882cf99 
__ROOT_PWD=''

# database path
CONN_PATH='data/data.pmgr'

# APPL name
APP_NAME='Passwd Manager'

#version
VERSION = '1.1.0'
VERSION_URL="http://code.google.com/p/passwdmanager/wiki/version"
LATEST_VERSION=None

def setLatestVersion(version):
    global LATEST_VERSION
    LATEST_VERSION = version

def setRootPwd(newPwd):
    global __ROOT_PWD
    __ROOT_PWD = newPwd

def getRootPwd():
    global __ROOT_PWD
    return __ROOT_PWD

