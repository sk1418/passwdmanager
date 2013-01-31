#!/usr/bin/python

import wx
import config
import confighandler,upgradehandler
import os
from gui.mainFrame import  MainWindow, UpdateChecker
from gui.dialogs import LoginDialog

'''
Created on Mar 19, 2009

@author: kent
'''



class PwdMgmtApp(wx.App):
    def OnInit(self):
        
        # show the authentication Dialog first 
        pwdDlg = LoginDialog(None)
        result = pwdDlg.authenticate()
        pwdDlg.Destroy()
        
        if result:            
            #here check version and do upgrade if necessary
            upgradehandler.upgrade() 
            mainWin = MainWindow()
            self.SetTopWindow(mainWin)  
            mainWin.Show()
            #checking new version in new thread
            updatechk = UpdateChecker(mainWin)
            updatechk.start()
            return True
        else:
            return False
     

if __name__ == '__main__':
    # if the conf dir doesn't exist, create the conf dir
    # This is only for linux
    if not os.path.exists(confighandler.getConfDir()) :
        confighandler.initHomeConfPath()

    # load config
    if not confighandler.loadConfig():
        print "your config file cannot be loaded. Did you change it?"
        exit(1)
    
    #start application GUI
    pwdApp = PwdMgmtApp()
    pwdApp.MainLoop()
