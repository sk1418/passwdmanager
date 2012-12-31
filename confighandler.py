"""
 handle config files
 read config file, create home config directory, set config settings etc.
"""
import os, sys, shutil
import ConfigParser
import util
import config


# Default conf file for linux
DEFAULT_CONF = 'conf/passwdManager.conf'
SAMPLE_DATA  = 'data/data.pmgr'
DEFAULT_DATA_PATH= os.path.join(os.getenv("HOME") , ".passwdManager","data","data.pmgr")

def getConfigFile():
    if util.isWindows():
        return 'conf/win.conf'
    else:
        return os.path.join(os.getenv("HOME") , ".passwdManager","passwdManager.conf")


def getConfDir():
    if util.isWindows():
        return 'conf'
    else:
        return os.path.join(os.getenv("HOME") , ".passwdManager")

def updateconfig(section, key, value):
    """ update the given config option"""
    cf = ConfigParser.ConfigParser()
    configFile = getConfigFile()
    with open( configFile , 'r') as cfgf:
        cf.readfp(cfgf)
    cf.set(section, key, value)
    with open( configFile, 'w') as cfgf:
        cf.write(cfgf)


def loadConfig():
    """
        load config from config file 
        return True if sucessful, otherwise False
    """
    cf = ConfigParser.ConfigParser()
    configFile = getConfigFile()
    if not os.path.exists(configFile):
        return False
    cf.read(configFile);

    #load options
    config.CONN_PATH = cf.get("settings","data.path")
    config.BACKUP = cf.getboolean("settings","backup.required")
    config.BACKUP_SIZE = cf.getint("settings", "backup.size")

    return True


def initHomeConfPath():
    """
    If ~/.passwdManager directory is not found, then create the directory and copy sample data file and default config file into that directory. This function is only used for non-windows system
    """
    if util.isWindows():
        return
    else:
        print "run the application 1st time. homeConf dir needs to be created"
        confDir = getConfDir()
        dataDir = os.path.join(confDir, "data")
        #mkdir and copy files
        if not os.path.exists(confDir):
            os.makedirs(dataDir)

        global DEFAULT_CONF, SAMPLE_DATA
        print "copy default conf file"
        shutil.copy(DEFAULT_CONF,confDir)
        print "copy sample data file"
        shutil.copy(SAMPLE_DATA, dataDir)

        # update the default data path
        global DEFAULT_DATA_PATH
        updateconfig("settings", "data.path", DEFAULT_DATA_PATH)
