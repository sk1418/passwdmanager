"""
 handle config files
 read config file, create home config directory, set config settings etc.
"""
import os, sys, shutil
import ConfigParser
import passwdmanager.util as util
import passwdmanager.config as config



# conf entries for Windows
WIN_CONF_DIR = ''
WIN_CONF_FILE=''
WIN_BACKUP_PATH=''
#WIN_LOG_DIR= os.path.join(WIN_CONF_DIR,'logs')

# Default conf file for linux
DEFAULT_CONF = ''
SAMPLE_DATA  = ''
DEFAULT_DATA_PATH= ''


def init():
    global WIN_CONF_DIR, WIN_CONF_FILE, WIN_BACKUP_PATH, DEFAULT_DATA_PATH, SAMPLE_DATA, DEFAULT_CONF
    WIN_CONF_DIR = os.path.join(config.APP_ROOT,'conf')
    WIN_CONF_FILE=os.path.join(WIN_CONF_DIR,'win.conf')
    WIN_BACKUP_PATH=os.path.join(WIN_CONF_DIR,'backup')
    #WIN_LOG_DIR= os.path.join(WIN_CONF_DIR,'logs')

    # Default conf file for linux
    DEFAULT_CONF = os.path.join(config.APP_ROOT,'conf/passwdManager.conf')
    SAMPLE_DATA  = os.path.join(config.APP_ROOT,'data/data.pmgr')
    DEFAULT_DATA_PATH= os.path.join(os.getenv("HOME") , ".passwdManager","data","data.pmgr")

def getConfigFile():
    if util.isWindows():
        global WIN_CONF_FILE
        return WIN_CONF_FILE
    else:
        return os.path.join(getConfDir(),"passwdManager.conf")


def getConfDir():
    if util.isWindows():
        return WIN_CONF_DIR
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
    config.BACKUP_SIZE = cf.getint("settings", "backup.size") if cf.getint("settings", "backup.size") >0 else 3

    # set backup/log dir in config
    if util.isWindows():
        global WIN_BACKUP_PATH, WIN_CONF_DIR, WIN_CONF_FILE
        config.BACKUP_DIR=WIN_BACKUP_PATH
        #config.LOG_DIR=WIN_LOG_DIR

    else:
        config.BACKUP_DIR=os.path.join(getConfDir(), 'backup')
        #config.LOG_DIR=os.path.join(getConfDir(), 'logs')

    #backup after loading config
    util.backupDB()

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
        #logDir = os.path.join(confDir, "logs")
        #mkdir and copy files
        if not os.path.exists(confDir):
            os.makedirs(dataDir)
            os.makedirs(backupDir)
            #os.makedirs(logDir)

        global DEFAULT_CONF, SAMPLE_DATA
        print "copy default conf file to " + confDir
        shutil.copy(DEFAULT_CONF,confDir)
        print "copy sample data file to " + dataDir
        shutil.copy(SAMPLE_DATA, dataDir)

        # update the default data path
        global DEFAULT_DATA_PATH
        updateconfig("settings", "data.path", DEFAULT_DATA_PATH)
