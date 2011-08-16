#!/usr/bin/python

import wx
import config
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
    pwdApp = PwdMgmtApp()
    pwdApp.MainLoop()
