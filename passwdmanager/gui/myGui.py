# -*- coding:utf-8 -*-
'''
Created on Mar 24, 2009

@author: kent

'''
import wx,os
import passwdmanager.config as config

##################################
# ICON path properties
##################################
# icon root path
ICON_ROOT=os.path.join( os.path.abspath(os.path.dirname(__file__)),"../../icons/")
#ICON_ROOT='icons/'

ICON_APP_LOGO = ICON_ROOT + 'app.png'
ICON_APP_ICON = ICON_ROOT + 'app16.png'
ICON_APP_UPDATE = ICON_ROOT + 'update.png'


#tag icon used in main window
ICON_TAG_CUSTOM = ICON_ROOT + 'tagM.png'
ICON_TAG_ALL = ICON_ROOT + 'allTags.png'
ICON_TAG_TRASH = ICON_ROOT + 'trash.png'
ICON_TAG_SEARCH = ICON_ROOT + 'result.png'
ICON_TAG_FAV = ICON_ROOT + 'favs.png'

ICON_TOOLBAR_ADD = ICON_ROOT + 'add.png'
ICON_TOOLBAR_QUIT = ICON_ROOT + 'exit.png'
ICON_TOOLBAR_SEARCH = ICON_ROOT + 'search.png'
ICON_TOOLBAR_REMOVE = ICON_ROOT + 'remove.png'
ICON_TOOLBAR_TRASH = ICON_TAG_TRASH
ICON_TOOLBAR_EMPTYTRASH = ICON_ROOT + 'empty.png'
ICON_TOOLBAR_DETAIL = ICON_ROOT + 'detail.png'
ICON_TOOLBAR_RECOVER = ICON_ROOT + 'recover.png'
ICON_TOOLBAR_ROOTPWD = ICON_ROOT + 'rootpwd.png'
ICON_TOOLBAR_EDIT = ICON_ROOT + 'edit.png'
ICON_TOOLBAR_PWDGEN =ICON_ROOT + 'pwdgen.png'

ICON_MENU_ADD = ICON_ROOT + 'add16.png'
ICON_MENU_REMOVE = ICON_ROOT + 'remove16.png'
ICON_MENU_QUIT = ICON_ROOT + 'exit16.png'
ICON_MENU_DETAIL = ICON_ROOT + 'detail16.png'
ICON_MENU_EMPTYTRASH = ICON_ROOT + 'empty16.png'
ICON_MENU_ABOUT = ICON_ROOT + 'about16.png'
ICON_MENU_UPDATE = ICON_ROOT + 'update16.png'
ICON_MENU_RECOVER = ICON_ROOT + 'recover16.png'
ICON_MENU_TRASH = ICON_ROOT + 'trash16.png'
ICON_MENU_PASTE = ICON_ROOT + 'paste16.png'
ICON_MENU_ROOTPWD = ICON_ROOT + 'rootpwd16.png'
ICON_MENU_NEWTAG =ICON_ROOT + 'newtag16.png'
ICON_MENU_DELTAG =ICON_ROOT + 'deltag16.png'
ICON_MENU_EDIT =ICON_ROOT + 'edit16.png'
ICON_MENU_PWDGEN =ICON_ROOT + 'pwdgen16.png'





##################################
# GUI size/position properties
##################################
#Application window size,position
MAIN_WINDOW_SIZE=(1100,700)
MAIN_WINDOW_POSITION=(100,80)
#Dialog position is needed for windows platform.
DIALOG_POSITION=(270,150)

# Button
#BUTTON_SIZE=(100,28)
BUTTON_SIZE= wx.DefaultSize

# Long Textbox
SIZE_LONG_TEXT=(300,28)

SIZE_NORMAL_TEXT=(200,28)
SIZE_MULTILINE_TEXT=(400,100)
# textbox in create/edit/detail dialog. keeping same length with multilineTextBox
SIZE_DETAIL_TEXT= (400,28) 
SIZE_SECRET_TEXT= (400,200) 



# Dialog
SIZE_DIALOG_LOGIN = (400, 130)
SIZE_DIALOG_NEWACCOUNT = (900, 610)
SIZE_DIALOG_EDITACCOUNT = (900,610)
SIZE_DIALOG_ACCOUNTDETAIL = (650,680)
SIZE_DIALOG_CHGROOTPWD = (500, 240)   
SIZE_DIALOG_PWDGEN = (520, 360)      


# splitterwindow min pane size
SPLITTERWINDOW_MIN_SIZE = 100 

##################################
# GUI Position properties
##################################


# splitterwindow Sash Position
SPLITTERWINDOW_SASH_POS = 200 


##################################
# GUI Window name
##################################
TAG_LIST_NAME = 'tagListCtrl'
PWD_LIST_NAME = 'pwdListCtrl'
NAME_TEXTBOX_SEARCH = 'searchTextBox'

##################################
# special tag id
##################################

ID_TAG_FAV = 0
ID_TAG_ALL = -3
ID_TAG_SEARCH = -2
ID_TAG_TRASH = -1

ID_TOOLBAR_DETAIL   = 7677 
ID_TOOLBAR_REMOVE   = 7676
ID_TOOLBAR_TRASH    = 7675
ID_TOOLBAR_RECOVER  = 7674
ID_TOOLBAR_EDIT     = 7673

ID_MENU_DETAIL      = 7672
ID_MENU_REMOVE      = 7670
ID_MENU_TRASH       = 7669
ID_MENU_RECOVER     = 7668
ID_MENU_EDIT        = 7667

#enable/disable IDs
IDS_ENDISABLE_MENU = (ID_MENU_DETAIL,ID_MENU_TRASH,ID_MENU_EDIT)

IDS_ENDISABLE_TOOLBAR = (ID_TOOLBAR_DETAIL,
                         ID_TOOLBAR_TRASH,ID_TOOLBAR_EDIT)

IDS_TRASHTAG_MENU = (ID_MENU_REMOVE,ID_MENU_RECOVER)
IDS_TRASHTAG_TOOLBAR = (ID_TOOLBAR_REMOVE,ID_TOOLBAR_RECOVER)


##################################
#Information messages
##################################
INFO_CLIPBOARD = """ The password of [%s] has been copied to Clipboard. """
INFO_PWD_CLIPBOARD = """ The password has been copied to Clipboard. """
INFO_MOVETO_TRASH = """ The account [%s] has been moved to trash,\n you can recover at any time """
INFO_COMPLETE_REMOVE = """ The account [%s] has been deleted from trash. """
INFO_RECOVERED = """ The account [%s] has been recovered from trash. """
INFO_ROOTPWD = """ The Master password was successfully changed. """
INFO_HIDE_TXT = """[ Hidden ]"""
INFO_ACCOUNT_ACTIVE = """[ Active ]"""
INFO_ACCOUNT_INTRASH = """[ In Trash ]"""

##################################
#Confirmation messages
##################################
CONFIRM_MOVETO_TRASH = """Are you sure to move the account [%s]?"""
CONFIRM_COMPLETE_REMOVE = """Are you sure to PERMANENTLY DELETE the account [%s]?"""
CONFIRM_EMPTY_TRASH = """Are you sure to empty the trash?"""
CONFIRM_REMOVE_TAG = """Are you sure to remove the tag [%s]?"""
CONFIRM_REMOVE_USEDTAG = """Removing tag [%s] will NOT remove related accounts. Continue to remove Tag?"""

##################################
#Error messages
##################################
ERR_LOGIN = 'Password is not correct!'
ERR_TITLE_EMPTY='Title cannot be empty!'
ERR_ACCOUNT_EMPTY='Account cannot be empty!'
ERR_PWD_EMPTY = 'Password cannot be empty!'
ERR_SEARCH_EMPTY = 'Search Keyword cannot be empty!'
ERR_ROOTPWD_LEN = 'Master Password length should between 5 and 16 digits'
ERR_NEWROOT_IDENTICAL = 'The two new Master Passwords are not identical, please input again!'
ERR_OLDROOT_WRONG = 'Given current Master Password is not correct!'
ERR_NEWTAG_EMPTY = 'Tag name cannot be empty!'
ERR_NEWTAG_UNIQUE = 'Tag name has already existed!'
ERR_ACCOUNTTITLE_UNIQUE = 'Account title has already existed!'
ERR_PWD_LEN = 'Password length should be a positive integer!'
ERR_PWD_EMPTYPATTERN= 'At least one Password Pattern needs to be choosen!'
ERR_PWD_COPY= 'Before do the coping, please generating a password first.'

def showErrorDialog(ErrMsg):
    dlg = wx.MessageDialog(None, ErrMsg, 'Error' , wx.OK |  wx.ICON_ERROR)
    dlg.ShowModal()      
    

def showConfirmationDialog(msg,name=''):
    if not name: # name =''
        dlg = wx.MessageDialog(None, msg , 'Confirmation',  wx.YES_NO  | wx.NO_DEFAULT | wx.ICON_EXCLAMATION)
    else:
        dlg = wx.MessageDialog(None, msg % name , 'Confirmation',  wx.YES_NO  | wx.NO_DEFAULT | wx.ICON_EXCLAMATION)
    return dlg.ShowModal()

def showInfoDialog(msg, name=''):
    if not name: #name=''
        dlg =  wx.MessageDialog(None, msg, 'Information',  wx.OK | wx.ICON_INFORMATION)
    else:
        dlg =  wx.MessageDialog(None, msg % name, 'Information',  wx.OK | wx.ICON_INFORMATION)
    dlg.ShowModal()


def showUpdateDialog(version):
    description = """
Passwd Manager version """+version+""" is available. New version contains new features and bug fixings. 
    
Upgrade is HIGHLY RECOMMENDED! 
    
Click the link below to download and upgrade."""
    info = wx.AboutDialogInfo()
    info.SetName("New Update Available!")
    info.SetIcon(wx.Icon(ICON_APP_UPDATE, wx.BITMAP_TYPE_PNG))
    info.SetDescription(description)
    info.SetWebSite('http://code.google.com/p/passwdmanager/downloads/list')

    wx.AboutBox(info)
        
def showAboutDialog():
    description = """Passwd Manager is an OS independent password management tool."""

    licence = """
Passwd Manager is free software; you can redistribute it and/or modify it 
under the terms of the GNU General Public License as published by the Free 
Software Foundation; either version 3 of the License, or (at your option) 
any later version.

Passwd Manager is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
See the GNU General Public License for more details. You should have received a copy of 
the GNU General Public License along with File Hunter; if not, write to the Free Software 
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA"""


    info = wx.AboutDialogInfo()

    info.SetIcon(wx.Icon(ICON_APP_LOGO, wx.BITMAP_TYPE_PNG))
    info.SetName(config.APP_NAME)
    info.SetVersion(config.VERSION)
    info.SetDescription(description)
    info.SetCopyright('(C) 2009 Kai Yuan')
    info.SetWebSite('http://code.google.com/p/passwdmanager/')
#    info.SetLicence(licence)
#    info.AddDeveloper('Kai Yuan')
#    info.AddDocWriter('Kai Yuan')
#    info.AddArtist('Kai Yuan')
#    info.AddTranslator('Kai Yuan')

    wx.AboutBox(info)
