#!/usr/bin/python

import shutil
import sqlite3 as sqlite
import config,util,service
import wx


SIZE_WINDOW = (900,610)
SIZE_MULTILINE = (400,300)
SIZE_ROOT = (300,28)


def backupAndCopy(src,dst):
    #backup
    shutil.copy(src,dst +".bak")
    #copy to data dir
    shutil.copy(src,dst)

class UpgradeService(service.Service):
    def __init__(self):
        '''
        constructor
        '''
        self.rootService = service.MasterService()


class MainFrame(wx.Frame):
    '''
    main window
    '''
    def __init__(self):

        ID_INFO = 10000
        ID_FILE = 10001
        ID_FILEPICKER = 10002
        ID_PWD = 10003
        ID_TEXTCTRL = 10004
        ID_LINE = 10005
        ID_TEXT = 10006
        ID_BUTTON = 10007

        placeHolder = (200,20)
        pos = wx.DefaultPosition
        size = (900,340)
        style = wx.DEFAULT_FRAME_STYLE

        wx.Frame.__init__(self,None,-1, 'PasswdManager Upgrade 1.0.x -> 1.1.x', pos, size, style)
        
        item0 = wx.BoxSizer( wx.VERTICAL )
        item0.Add(placeHolder)#place holder
        item1 = wx.StaticText( self, ID_INFO, 
            "This tool will upgrade the data file of passwdManager 1.0.x to 1.1.x. \n"
            "Note:\n\n"
            "- a backup of given data file will be automatically created\n"
            "- Master password of your data file is needed for upgrading.(encryption account names)",
            wx.DefaultPosition, [700,120], 0 )
        item0.Add( item1, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        item2 = wx.FlexGridSizer( 0, 2, 0, 0 )
        
        item3 = wx.StaticText( self, ID_FILE, "1.0.x Database File", wx.DefaultPosition, wx.DefaultSize, 0 )
        item2.Add( item3, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        item4 = wx.FilePickerCtrl( self, ID_FILEPICKER, "", "Choose file", "*.*", wx.DefaultPosition, [300,-1], wx.FLP_OPEN|wx.FLP_USE_TEXTCTRL|wx.FLP_FILE_MUST_EXIST )
        item2.Add( item4, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        item5 = wx.StaticText( self, ID_PWD, "Root Password", wx.DefaultPosition, wx.DefaultSize, 0 )
        item2.Add( item5, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        item6 = wx.TextCtrl( self, ID_TEXTCTRL, "", wx.DefaultPosition, [200,-1], wx.TE_PASSWORD )
        item2.Add( item6, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        item0.Add( item2, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        item7 = wx.StaticLine( self, ID_LINE, wx.DefaultPosition, [500,20], wx.LI_HORIZONTAL )
        item0.Add( item7, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        item8 = wx.StaticText( self, ID_TEXT, "Upgrade log", wx.DefaultPosition, [440,-1], 0 )
        item0.Add( item8, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        item9 = wx.TextCtrl( self, ID_TEXTCTRL, "", wx.DefaultPosition, [500,400], wx.TE_MULTILINE )
        item0.Add( item9, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        item10 = wx.FlexGridSizer( 0, 3, 0, 32 )
        
        item10.Add( [ 20, 20 ] , 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        item10.Add( [ 20, 20 ] , 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        item11 = wx.Button( self, ID_BUTTON, "OK", wx.DefaultPosition, wx.DefaultSize, 0 )
        item10.Add( item11, 0, wx.ALIGN_CENTER|wx.LEFT|wx.TOP|wx.BOTTOM, 5 )

        item0.Add( item10, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP|wx.BOTTOM|wx.SHAPED, 5 )

        self.SetSizer( item0 )
        item0.SetSizeHints( self )
    
    


class UpApp(wx.App):
    ''' upgrade application starting point'''
    def OnInit(self):
        wx.InitAllImageHandlers()
        frame = MainFrame()
        frame.Show(True)
        
        return True

if __name__ == '__main__':


    upApp = UpApp()
    upApp.MainLoop()

    #get rootPwd and old db path from GUI
    #origDB="/tmp/a.txt"
    #rootPwd="password"
    ##backup
    #backupAndCopy("/tmp/a.txt",config.CONN_PATH)
    #upService = UpgradeService()




