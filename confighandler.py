"""
 handle config files
 read config file, create home config directory, set config settings etc.
"""
import os, sys, shutil
import ConfigParser
import util
import config

# conf entries for Windows
WIN_CONF_DIR='conf'
WIN_CONF_FILE=os.path.join(WIN_CONF_DIR,'win.conf')
WIN_BACKUP_PATH='backup'


# Default conf file for linux
DEFAULT_CONF = 'conf/passwdManager.conf'
SAMPLE_DATA  = 'data/data.pmgr'
DEFAULT_DATA_PATH= os.path.join(os.getenv("HOME") , ".passwdManager","data","data.pmgr")

def getConfigFile():
    if util.isWindows():
        global WIN_CONF_FILE
        return WIN_CONF_FILE
    else:
        return os.path.join(getConfDir(),"passwdManager.conf")


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

    #load options from config file
    config.CONN_PATH = cf.get("settings","data.path")
    config.BACKUP = cf.getboolean("settings","backup.required")
    config.BACKUP_SIZE = cf.getint("settings", "backup.size")

    # set backup dir in config
    if util.isWindows():
        global WIN_BACKUP_PATH, WIN_CONF_DIR, WIN_CONF_FILE
        config.BACKUP_DIR=WIN_BACKUP_PATH
    else:
        config.BACKUP_DIR=os.path.join(getConfDir(), 'backup')

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
        backupDir = os.path.join(confDir, "backup")
        #mkdir and copy files
        if not os.path.exists(confDir):
            os.makedirs(dataDir)
            os.makedirs(backupDir)

        global DEFAULT_CONF, SAMPLE_DATA
        print "copy default conf file"
        shutil.copy(DEFAULT_CONF,confDir)
        print "copy sample data file"
        shutil.copy(SAMPLE_DATA, dataDir)

        # update the default data path
        global DEFAULT_DATA_PATH
        updateconfig("settings", "data.path", DEFAULT_DATA_PATH)
