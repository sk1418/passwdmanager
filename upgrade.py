#!/usr/bin/python

import shutil
import sqlite3 as sqlite
import config,util,service,dao
import wx
import os.path


SIZE_WINDOW = (900,610)
SIZE_MULTILINE = (400,300)
SIZE_ROOT = (300,28)



def chkRootPwd(path, pwd):
    '''check given root password on given path'''
    if os.path.isfile(path):
        conn = sqlite.connect(path)
        masterDao = dao.MasterDao(conn)
        md5Pwd = masterDao.getMasterPwd()
        md5String = util.md5Encode(pwd)
        conn.close()
        return md5Pwd == md5String
    else:
        return False


def showErrorDialog(ErrMsg):
    dlg = wx.MessageDialog(None, ErrMsg, 'Error' , wx.OK |  wx.ICON_ERROR)
    dlg.ShowModal()      

class UpgradeService:

    def __init__(self):
        '''
        constructor
        '''
        self.log = None

    def getConnection(self):
        conn = sqlite.connect(config.CONN_PATH)
        return conn

    def addLog(self,msg):
        self.log.SetValue(self.log.GetValue()+"\n"+msg)

    def upgrade(self,src,key,log):
        try:
            
            self.log = log
            self.log.SetValue("")
            self.addLog("Starting upgrade")
            #the original datafile in new version
            newData=config.CONN_PATH;
            # backup the newData(sample data) with .bak
            shutil.copy(newData,newData+".bak")
            self.addLog("backup 1.1.0 datafile->"+newData+".bak")
            
            shutil.copy(src, newData)
            self.addLog("copy 1.0.x datafile->"+newData)

            shutil.copy(src, newData+"_v1.0.x.bak")
            self.addLog("backup 1.0.x datafile->"+newData+"_v1.0.x.bak")
            
            conn = self.getConnection()
            self.addLog("Adding Secret Info column to datafile.... ")
            self.__addSecretColumn(conn)
            self.addLog("Done!")
            
            self.addLog("Encrypting username/loginName for all existing accounts....")
            c = self.__encryptAccounts(key,conn)
            self.addLog("Done! "+ str(c) + " accounts were updated.")
            self.addLog("Upgrade Finished, also your old data were migrated to new PasswdManager.")
            self.addLog("Close Upgrade tool, and start PasswdManager, login with your old master password.")
            self.addLog("Thanks for using PasswordManager")
            conn.commit()
            conn.close()
        except sqlite.OperationalError:
            self.addLog("Upgrade datafile failed. Is selected datafile with version 1.0.x?")
            showErrorDialog("Upgrade datafile failed. Is selected datafile with version 1.0.x?")

    def __addSecretColumn(self,conn):
        sql = """
        ALTER TABLE ACCOUNT ADD COLUMN secret TEXT
            """
        cur = conn.cursor()
        cur.execute(sql)
        cur.close()

    def __encryptAccounts(self,key,conn):
        cur = conn.cursor()
        cur2 =conn.cursor()
        sql = 'select id,  username FROM ACCOUNT'
        cur.execute(sql)
        
        upsql = 'update Account set username=? where id=?'
        
        c=0
        for row in cur.fetchall():
            (id,uid) = row
            newUid=util.encrypt(key,uid)
            cur2.execute(upsql,(newUid,id,))
            c += 1
            
            
        cur2.close()
        cur.close()
        return c
            

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
            "\nNote:\n"
            "- a backup of given data file will be automatically created\n"
            "- Master password of your data file is needed for upgrading.(for encrypting account names)",
            wx.DefaultPosition, [700,120], 0 )
        item0.Add( item1, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        item2 = wx.FlexGridSizer( 0, 2, 0, 0 )
        
        item3 = wx.StaticText( self, ID_FILE, "1.0.x Database File", wx.DefaultPosition, wx.DefaultSize, 0 )
        item2.Add( item3, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )

        item4 = wx.FilePickerCtrl( self, ID_FILEPICKER, "", "Choose file", "passwd Manager Data file (*.pmgr)|*.pmgr", wx.DefaultPosition, [300,28], wx.FLP_OPEN|wx.FLP_USE_TEXTCTRL| wx.FLP_FILE_MUST_EXIST )
        item2.Add( item4, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        item5 = wx.StaticText( self, ID_PWD, "Master Password", wx.DefaultPosition, wx.DefaultSize, 0 )
        item2.Add( item5, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )

        item6 = wx.TextCtrl( self, ID_TEXTCTRL, "", wx.DefaultPosition, [300,28], wx.TE_PASSWORD )
        item2.Add( item6, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        item0.Add( item2, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        item7 = wx.StaticLine( self, ID_LINE, wx.DefaultPosition, [500,20], wx.LI_HORIZONTAL )
        item0.Add( item7, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        item8 = wx.StaticText( self, ID_TEXT, "Upgrade log", wx.DefaultPosition, [440,-1], 0 )
        item0.Add( item8, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        item9 = wx.TextCtrl( self, ID_TEXTCTRL, "", wx.DefaultPosition, [500,400], wx.TE_MULTILINE|wx.TE_READONLY)
        item0.Add( item9, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        item10 = wx.FlexGridSizer( 0, 3, 0, 0 )
        
        item10.Add( placeHolder , 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        item11 = wx.Button( self, wx.ID_OK, "Start", wx.DefaultPosition, wx.DefaultSize, 0 )
        item12 = wx.Button( self, wx.ID_CLOSE, "Close", wx.DefaultPosition, wx.DefaultSize, 0 )
        item10.Add( item11, 0, wx.ALIGN_RIGHT|wx.LEFT|wx.TOP|wx.BOTTOM, 5 )
        item10.Add( item12, 0, wx.ALIGN_RIGHT|wx.LEFT|wx.TOP|wx.BOTTOM, 5 )

        item0.Add( item10, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP|wx.BOTTOM|wx.SHAPED, 5 )

        self.SetSizer( item0 )
        item0.SetSizeHints( self )

        self.pwd = item6
        self.filepicker = item4
        self.log = item9
        self.okbt= item11

        self.Bind(wx.EVT_BUTTON, self.onStart, item11)
        self.Bind(wx.EVT_BUTTON, self.exitUpg, item12)

        self.upgService = UpgradeService()

    def exitUpg(self,event):
        exit() 

    def onStart(self,event):
        '''user click upgrade'''

        if not self.pwd.GetValue():
            showErrorDialog("Master password cannot be empty!")
            self.pwd.SetFocus()
        elif not self.filepicker.GetPath():
            showErrorDialog("please choose the passwd Manager data file in old version.")
            self.filepicker.SetFocus()

        elif not os.path.isfile(self.filepicker.GetPath()):
            showErrorDialog("Seleced data file doesn't exist.")
            self.filepicker.SetFocus()

        elif not chkRootPwd(self.filepicker.GetPath(), self.pwd.GetValue()):
            showErrorDialog("The given root password is not correct for the given data file.")
            self.pwd.SetFocus()

        else:
            #here start the upgrade logic
            

            self.upgService.upgrade(self.filepicker.GetPath(),self.pwd.GetValue(), self.log)
            self.okbt.Disable()




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

