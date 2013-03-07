# -*- coding:utf-8 -*-
# PasswdManager -- Password management tool
# Copyright (C) 2008 -- 2013 Kai Yuan <kent.yuan@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''
Created on Apr 3, 2009

@author: kent
'''
from os import path
import  sys, shutil
import ConfigParser
import util,logging


# root password
#Default:password
#MD5:5f4dcc3b5aa765d61d8327deb882cf99 
__ROOT_PWD     = ''

# database path
CONN_PATH      = '' #filled by confighandler

#backup option
BACKUP_DIR = '' # filled by confighandler
BACKUP         = True
BACKUP_SIZE    = 1

#log file dir
# logging information will go to database later
#LOG_DIR = '' # filled by confighandler
#LOG_FILE = 'pwm.log' # log filename

#version
VERSION        = '1.2.0'
VERSION_URL    = "http://code.google.com/p/passwdmanager/wiki/version"
LATEST_VERSION = None




# APPL name
APP_NAME       = 'Passwd Manager'

#APP Root path
# using this complicated assignment because the exe file by py2exe doesn't 
# work with path.dirname(__file__)
APP_ROOT =  path.dirname(unicode(sys.executable, sys.getfilesystemencoding( ))) \
        if hasattr(sys, "frozen") else path.abspath(path.join(path.dirname(__file__), "../"))

def setLatestVersion(version):
    global LATEST_VERSION
    LATEST_VERSION = version

def setRootPwd(newPwd):
    global __ROOT_PWD
    __ROOT_PWD = newPwd

def getRootPwd():
    global __ROOT_PWD
    return __ROOT_PWD


