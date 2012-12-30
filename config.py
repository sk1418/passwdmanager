'''
Created on Apr 3, 2009

@author: kent
'''
import os, sys
import util


# root password
#Default:password
#MD5:5f4dcc3b5aa765d61d8327deb882cf99 
__ROOT_PWD=''

# database path
CONN_PATH      = 'data/data.pmgr'

#version
VERSION        = '1.1.0'
VERSION_URL    = "http://code.google.com/p/passwdmanager/wiki/version"
LATEST_VERSION = None

# APPL name
APP_NAME='Passwd Manager'

# Default conf file for linux
DEFAULT_CONF = 'conf/passwdManager.conf'
SAMPLE_DATA  = 'data/data.pmgr'

def setLatestVersion(version):
    global LATEST_VERSION
    LATEST_VERSION = version

def setRootPwd(newPwd):
    global __ROOT_PWD
    __ROOT_PWD = newPwd

def getRootPwd():
    global __ROOT_PWD
    return __ROOT_PWD


def getConfDir():
    if sys.platform.upper().beginWith('WIN'):
        return 'conf'
    else:
        return os.getenv("HOME") + "/.passwdManager"

def initHomeConfPath():
    """
    If ~/.passwdManager directory is not found, then create the directory and copy sample data file and default config file into that directory. This function is only used for non-windows system
    """
    if util.isWindows():
        return
    else:
        confDir = getConfDir()
        dataDir = os.path.join(confDir, "data")
        #mkdir and copy files
        if not os.path.exists(confDir):
            os.makedirs(dataDir)

        global DEFAULT_CONF, SAMPLE_DATA
        shutil.copy(DEFAULT_CONF,confDir)
        shutil.copy(SAMPLE_DATA, dataDir)

        # set permissions
        for root, dirs, files in os.walk(confDir):  
            for d in dirs:  
                os.chmod(d, 0755)
            for f in files:
                fname = os.path.join(root, f)
                os.chmod(f, 0644)
