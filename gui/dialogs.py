# -*- coding:utf-8 -*-
'''
Created on Mar 23, 2009

@author: kent
'''
import logging
import wx
import wx.grid
import myGui,config,util
from service import * 


RETRY = 5


class LoginDialog(wx.Dialog):
    def __init__(self,parent,id=-1,title="Login"):
        wx.Dialog.__init__(self,parent,id,title)
        self.parent = parent
         
        ID_TEXT = 10000
        ID_TEXTCTRL = 10001
        ID_BUTTON = 10002
        
        item0 = wx.BoxSizer( wx.VERTICAL )
    
        self.lbl = wx.StaticText( self, ID_TEXT, "")
        item0.Add( self.lbl, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
    
        self.pwdBox = wx.TextCtrl( self, ID_TEXTCTRL, "",  size = myGui.SIZE_LONG_TEXT,style=wx.TE_PASSWORD)
        item0.Add( self.pwdBox, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
    
        item3 = wx.BoxSizer( wx.HORIZONTAL )
        
    
        self.cancelBt = wx.Button( self, wx.ID_CANCEL, "Exit",  wx.DefaultPosition,wx.DefaultSize, 0 )
        item3.Add( self.cancelBt, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        item3.Add( [ 20, 20 ] , 0, wx.ALIGN_CENTER|wx.ALL, 5 )
    
        self.okBt = wx.Button( self, wx.ID_OK, "OK",  wx.DefaultPosition, wx.DefaultSize, 0 )
        item3.Add( self.okBt, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
    
        item0.Add( item3, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        
       
        self.SetSizer(item0)  
        self.__set_properties()
        
        
        # ok button as default
        self.okBt.SetDefault()
        self.pwdBox.SetFocus()

    def __set_properties(self):
        # begin wxGlade: LoginDialog.__set_properties
        self.SetTitle("Login")
        self.SetSize(myGui.SIZE_DIALOG_LOGIN)
        self.SetPosition(wx.DefaultPosition)        
        self.__setLabelText()
        # end wxGlade

    
   
    
    def __setLabelText(self):
        
            if RETRY == 1:
                str =  'Please Enter The Master Password: ( Last Try!! )'
            else :
                str =  'Please Enter The Master Password: ( %d tries left )' % (RETRY)
            self.lbl.SetLabel(str)


    def authenticate(self):
        mService = MasterService()

        val = self.ShowModal()
        if val == wx.ID_OK:
            pwd = self.pwdBox.GetValue()#def encryptFile(fullFileName, key, overwrite=False):

            if not(mService.authentication(pwd)):
                #logging.warning("Login fails")
                myGui.showErrorDialog(myGui.ERR_LOGIN)
                global RETRY

                if RETRY > 1:
                    RETRY=RETRY-1
                    self.__setLabelText()
                    self.pwdBox.SetValue('')
                    return self.authenticate()
                else:
                    return False                 
            else:
                #logging.warning("Login successful.")
                config.setRootPwd(pwd)
                return True
        else:
            return False
            
class AccountDetailDialog(wx.Dialog):
    '''
    show account details (read only)
    '''
    def __init__(self,parent,pwdId):        
        wx.Dialog.__init__(self,parent,id=-1,title="Account Detail",pos=myGui.DIALOG_POSITION)
        
        # IDs for widgets
        #==================================
        titleId = 3015
        usernameId = 3016
        tagId = 3017
        createId = 3018
        updateId = 3019
        statusId = 3020
        descriptionId = 3021
        passwordId = 3022
        secretId = 3023
        ID_TEXT = -1
        chkId = -1
        #==================================
        
        self.parent = parent
        self.pwdId = pwdId
        
        item0 = wx.BoxSizer( wx.VERTICAL )
    
        item2 = wx.StaticBox( self, -1, "Account Detail" )
        item1 = wx.StaticBoxSizer( item2, wx.VERTICAL )
        
        item3 = wx.FlexGridSizer( 0, 2, 0, 0 )
        item3.AddGrowableCol( 1 )
        item3.AddGrowableRow( 6 )
        
        item4 = wx.StaticText( self, ID_TEXT, "Title", wx.DefaultPosition, wx.DefaultSize, 0 )
        item3.Add( item4, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
    
        item5 = wx.TextCtrl( self, titleId, "", wx.DefaultPosition, myGui.SIZE_DETAIL_TEXT, wx.TE_READONLY)
        item3.Add( item5, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
    
        item6 = wx.StaticText( self, ID_TEXT, "Account", wx.DefaultPosition, wx.DefaultSize, 0 )
        item3.Add( item6, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
    
        item7 = wx.TextCtrl( self, usernameId, "", wx.DefaultPosition, myGui.SIZE_DETAIL_TEXT, wx.TE_READONLY)
        item3.Add( item7, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
    
        item8 = wx.StaticText( self, ID_TEXT, "Tags", wx.DefaultPosition, wx.DefaultSize, 0 )
        item3.Add( item8, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
    
        item9 = wx.TextCtrl( self, tagId, "", wx.DefaultPosition, myGui.SIZE_DETAIL_TEXT, wx.TE_READONLY)
        item3.Add( item9, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
    
        item10 = wx.StaticText( self, ID_TEXT, "Created time", wx.DefaultPosition, wx.DefaultSize, 0 )
        item3.Add( item10, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
    
        item11 = wx.TextCtrl( self, createId, "", wx.DefaultPosition, myGui.SIZE_DETAIL_TEXT, wx.TE_READONLY)
        item3.Add( item11, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
    
        item12 = wx.StaticText( self, ID_TEXT, "Last update at", wx.DefaultPosition, wx.DefaultSize, 0 )
        item3.Add( item12, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
    
        item13 = wx.TextCtrl( self, updateId, "", wx.DefaultPosition,myGui.SIZE_DETAIL_TEXT, wx.TE_READONLY)
        item3.Add( item13, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
    
    
        item16 = wx.StaticText( self, ID_TEXT, "Description", wx.DefaultPosition, wx.DefaultSize, 0)
        item3.Add( item16, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
    
        item17 = wx.TextCtrl( self, descriptionId, "", wx.DefaultPosition, myGui.SIZE_MULTILINE_TEXT, wx.TE_MULTILINE|wx.TE_READONLY)
        item3.Add( item17, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
    
        item18 = wx.StaticText( self, ID_TEXT, "Password", wx.DefaultPosition, wx.DefaultSize, 0 )
        item3.Add( item18, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
    
#        item19 = wx.StaticText( self, passwordId, "", wx.DefaultPosition, wx.DefaultSize, 0 )
        item19 = wx.TextCtrl( self, passwordId, "", wx.DefaultPosition, myGui.SIZE_DETAIL_TEXT, wx.TE_READONLY)
        item3.Add( item19, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        item30 = wx.StaticText( self, ID_TEXT, "Secret notes", wx.DefaultPosition, wx.DefaultSize, 0 )
        item3.Add( item30, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
    
        item31 = wx.TextCtrl( self, secretId, "", wx.DefaultPosition, myGui.SIZE_SECRET_TEXT, wx.TE_MULTILINE|wx.TE_READONLY)
        item3.Add( item31, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
    
        item1.Add( item3, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
    
        item20 = wx.CheckBox( self, chkId, "Show Password and Secret notes", wx.DefaultPosition, wx.DefaultSize, 0 )
        item1.Add( item20, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
    
        item0.Add( item1, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
    
        item21 = wx.BoxSizer( wx.HORIZONTAL )
        
        item22 = wx.Button( self, wx.ID_OK, "Edit", wx.DefaultPosition, wx.DefaultSize, 0 )
        item21.Add( item22, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
    
        item21.Add( [ 20, 20 ] , 0, wx.ALIGN_CENTER|wx.ALL, 5 )
    
        item23 = wx.Button( self, wx.ID_CANCEL, "Close", wx.DefaultPosition, wx.DefaultSize, 0 )
        item21.Add( item23, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
    
        item0.Add( item21, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        
        self.title = item5
        self.username = item7
        self.tags = item9
        self.create = item11
        self.lastupdate = item13
        self.description = item17
        self.password = item19
        self.secret = item31
        
        self.title.SetBackgroundColour( '#EFEBE7' )
        self.username.SetBackgroundColour( '#EFEBE7' )
        self.tags.SetBackgroundColour( '#EFEBE7' )
        self.create.SetBackgroundColour( '#EFEBE7' )
        self.lastupdate.SetBackgroundColour( '#EFEBE7' )
        self.description.SetBackgroundColour( '#EFEBE7' )
        self.password.SetForegroundColour( '#E2644F' )
        self.password.SetBackgroundColour( 'BLACK' )
        self.secret.SetForegroundColour( '#E2644F' )
        self.secret.SetBackgroundColour( 'BLACK' )
        
        self.chk = item20 # checkbox
        
        #bind event handler 
        self.Bind(wx.EVT_CHECKBOX,self.showHidePassword,self.chk)
        self.pwdService = PwdService() 
        self.tagService = TagService()
        self.accountObj = self.pwdService.getPwdById(self.pwdId)       
        self.SetSize(myGui.SIZE_DIALOG_ACCOUNTDETAIL)        
        self.SetSizer(item0)        
        
        self.loadData()
        
#        self.Show()
        
    def onClick(self):
        val = self.ShowModal()
        if val == wx.ID_OK: # go to edit window
            self.parent.onEditAccount(None)
        
            
        
    def loadData(self):
        #account
        a = self.accountObj
        self.title.SetValue(a.title)
        self.username.SetValue(a.username)
        self.tags.SetValue(self.tagService.getTagNameString(a.tags))
        self.create.SetValue(a.createdate)
        self.lastupdate.SetValue(a.lastupdate)
        self.description.SetValue(a.description)
        self.password.SetValue(myGui.INFO_HIDE_TXT)
        self.secret.SetValue(myGui.INFO_HIDE_TXT)
    
    def showHidePassword (self,event):
        if self.chk.GetValue():
            self.password.SetValue(util.decrypt(config.getRootPwd(),self.accountObj.pwd))
            self.secret.SetValue(util.decrypt(config.getRootPwd(),self.accountObj.secret).decode('utf-8') if self.accountObj.secret else "")
        else:
            self.password.SetValue(myGui.INFO_HIDE_TXT)
            self.secret.SetValue(myGui.INFO_HIDE_TXT)
                   

class EditAccountDialog(wx.Dialog):
    def __init__(self,parent,pwdId):
        wx.Dialog.__init__(self,parent,id=-1,title="Edit account",pos=myGui.DIALOG_POSITION)
        # IDs for widgets
        #==================================  
        titleId = 4014
        descriptionId = 4015
        usernameId = 4016
        passwordId = 4017
        secretId = 4010
        tagsListId = 4018
        #==================================
        
        item0 = wx.BoxSizer( wx.VERTICAL )
    
        item1 = wx.BoxSizer( wx.HORIZONTAL )
        
        item3 = wx.StaticBox( self, -1, "Edit Account" )
        item2 = wx.StaticBoxSizer( item3, wx.VERTICAL )
        
        item4 = wx.FlexGridSizer( 0, 2, 0, 0 )
        item4.AddGrowableCol( 1 )
        item4.AddGrowableRow( 1 )
        
        item5 = wx.StaticText( self, -1, "Title", wx.DefaultPosition, wx.DefaultSize, 0 )
        item4.Add( item5, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
    
        item6 = wx.TextCtrl( self, titleId, "", wx.DefaultPosition, myGui.SIZE_DETAIL_TEXT, 0 )
        item4.Add( item6, 0, wx.ALIGN_LEFT|wx.ALL, 5 )
    
        item7 = wx.StaticText( self, -1, "Description", wx.DefaultPosition, wx.DefaultSize, 0 )
        item4.Add( item7, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
    
        item8 = wx.TextCtrl( self, descriptionId, "", wx.DefaultPosition, myGui.SIZE_MULTILINE_TEXT, wx.TE_MULTILINE )
        item4.Add( item8, 0, wx.ALIGN_LEFT|wx.ALL, 5 )
    
        item9 = wx.StaticText( self, -1, "Account", wx.DefaultPosition, wx.DefaultSize, 0 )
        item4.Add( item9, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
    
        item10 = wx.TextCtrl( self, usernameId, "", wx.DefaultPosition,myGui.SIZE_DETAIL_TEXT, 0 )
        item4.Add( item10, 0, wx.ALIGN_LEFT|wx.ALL, 5 )
    
        item20 = wx.StaticText( self, -1, "Secret notes", wx.DefaultPosition, wx.DefaultSize, 0 )
        item4.Add( item20, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
    
        item21 = wx.TextCtrl( self,secretId, "", wx.DefaultPosition, myGui.SIZE_SECRET_TEXT, wx.TE_MULTILINE )
        item4.Add( item21, 0, wx.ALIGN_LEFT|wx.ALL, 5 )

        item11 = wx.StaticText( self, -1, "(*) Password", wx.DefaultPosition, wx.DefaultSize, 0 )
        item4.Add( item11, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
    
        item12 = wx.TextCtrl( self, passwordId, "", wx.DefaultPosition, myGui.SIZE_DETAIL_TEXT, 0 )
        item4.Add( item12, 0, wx.ALIGN_LEFT|wx.ALL, 5 )
    
        item2.Add( item4, 0, wx.ALIGN_LEFT|wx.ALL, 5 )
    
        item13 = wx.StaticText( self, -1, 
            "(*) Leave the password empty if you wanna keep the old password.",
            wx.DefaultPosition, wx.DefaultSize, 0 )
        item13.SetForegroundColour( wx.RED )
        item2.Add( item13, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
    
        item1.Add( item2, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
    
        item15 = wx.StaticBox( self, -1, "Tags" )
        item14 = wx.StaticBoxSizer( item15, wx.VERTICAL )
        
        item16 = wx.ListBox( self, tagsListId, wx.DefaultPosition, [200,230], 
            [] , wx.LB_MULTIPLE )
        item14.Add( item16, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
    
        item1.Add( item14, 0, wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
    
        item0.Add( item1, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
    
        item17 = wx.BoxSizer( wx.HORIZONTAL )
        
    
        item19 = wx.Button( self, wx.ID_CANCEL, "Cacnel", wx.DefaultPosition, wx.DefaultSize, 0 )
        item17.Add( item19, 0, wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

        item17.Add( [ 50, 20 ] , 0, wx.ALIGN_CENTER|wx.ALL, 5 )
    
        item18 = wx.Button( self, wx.ID_OK, "Save", wx.DefaultPosition, wx.DefaultSize, 0 )
        item17.Add( item18, 0, wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
    
        item0.Add( item17, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        
        self.pwdId = pwdId
        self.parent = parent
        
        self.title = item6
        self.username = item10
        self.tags = item16
        self.description = item8
        self.secret = item21
        self.password = item12
        
       
        
        self.pwdService = PwdService()        
        self.accountObj = self.pwdService.getPwdById(self.pwdId)
               
        self.SetSize(myGui.SIZE_DIALOG_EDITACCOUNT)        
        self.SetSizer(item0)        
        
        self.loadTags()
        self.loadData()
        self.Show()
        
    def loadData(self):
        a = self.accountObj
        self.title.SetValue(a.title)
        self.username.SetValue(a.username)
        self.description.SetValue(a.description)
        self.secret.SetValue(util.decrypt(config.getRootPwd(), a.secret).decode('utf-8') if a.secret else "")
        for tag in a.tags:
            name = tag.name
            self.tags.SetStringSelection(name,True)
        
        
        
      #load tags
    def loadTags(self):
        tagService = TagService()
        allTags = tagService.getAllTags()
        accountTags = self.accountObj.tags
        #print accountTags
        for tag in allTags:
            idx = self.tags.Append(tag.name,tag.id)
            
    def onSave(self):
        val = self.ShowModal()
        if val == wx.ID_OK:
            
            if len(self.title.GetValue()) == 0:
                myGui.showErrorDialog(myGui.ERR_TITLE_EMPTY)
                self.title.SetFocus()
                self.onSave()
            elif len(self.username.GetValue()) ==0:
                myGui.showErrorDialog(myGui.ERR_ACCOUNT_EMPTY)
                self.account.SetFocus()
                self.onSave()
            elif not self.pwdService.isTagNameValid(self.title.GetValue(),self.pwdId):
                myGui.showErrorDialog(myGui.ERR_ACCOUNTTITLE_UNIQUE)
                self.title.SetFocus()
                self.onSave()

            else:
                vTitle = self.title.GetValue()
                vDescription = self.description.GetValue()
                vAccount = self.username.GetValue()
                vPassword = self.password.GetValue() if len(self.password.GetValue())>0 else None               
                #vSecret = unicode.encode(self.secret.GetValue(),'utf-8')
                vSecret = self.secret.GetValue().encode('utf-8')
                vTagIds = []
                for idx in self.tags.GetSelections():
                    vTagIds.append(self.tags.GetClientData(idx))
                
                self.pwdService.editAccount(self.pwdId,vTitle,vDescription,vAccount,vPassword, vSecret,vTagIds)
            
            
            
            
class NewPwdDialog(wx.Dialog):
    '''
    add new password entry dialog
    '''
    
    def __init__(self,parent,id=-1,title="Add new account"):
        wx.Dialog.__init__(self,parent,id,title,pos=myGui.DIALOG_POSITION)
        
        # IDs for widgets
        #==================================
        titleLbl = 100
        titleValue = 101
        descriptionLbl = 102
        descriptionValue = 103
        accountLbl = 104
        accountValue = 105
        pwdLbl = 106
        pwdValue = 107
        infoLbl = 108
        tags = 109

        secretLbl = 110
        secretValue = 111
        #===================================
       
        item0 = wx.BoxSizer( wx.VERTICAL )
        
        item1 = wx.BoxSizer( wx.HORIZONTAL )
        
        item3 = wx.StaticBox( self, -1, "Account Details" )
        item2 = wx.StaticBoxSizer( item3, wx.VERTICAL )
        
        item4 = wx.FlexGridSizer( 0, 2, 0, 0 )
        item4.AddGrowableCol( 1 )
        item4.AddGrowableRow( 1 )
        
        item5 = wx.StaticText( self, titleLbl, "Title", wx.DefaultPosition, wx.DefaultSize, 0 )
        item4.Add( item5, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
    
        item6 = wx.TextCtrl( self, titleValue, "", wx.DefaultPosition, myGui.SIZE_DETAIL_TEXT, 0 )
        item4.Add( item6, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
    
        item7 = wx.StaticText( self, descriptionLbl, "Description", wx.DefaultPosition, wx.DefaultSize, 0 )
        item4.Add( item7, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
    
        item8 = wx.TextCtrl( self, descriptionValue, "", wx.DefaultPosition,myGui.SIZE_MULTILINE_TEXT, wx.TE_MULTILINE )
        item4.Add( item8, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
    
        item9 = wx.StaticText( self, accountLbl, "Account", wx.DefaultPosition, wx.DefaultSize, 0 )
        item4.Add( item9, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
    
        item10 = wx.TextCtrl( self, accountValue, "", wx.DefaultPosition, myGui.SIZE_DETAIL_TEXT, 0 )
        item4.Add( item10, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
    
        item11 = wx.StaticText( self, pwdLbl, "(*) Password", wx.DefaultPosition, wx.DefaultSize, 0 )
        item4.Add( item11, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
    
        item12 = wx.TextCtrl( self, pwdValue, "", wx.DefaultPosition, myGui.SIZE_DETAIL_TEXT, 0 )
        item4.Add( item12, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        item20 = wx.StaticText( self,secretLbl, "(*) Secret Notes", wx.DefaultPosition, wx.DefaultSize, 0 )
        item4.Add( item20, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
    
        item21 = wx.TextCtrl( self, secretValue, "", wx.DefaultPosition, myGui.SIZE_SECRET_TEXT, wx.TE_MULTILINE )
        item4.Add( item21, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        item2.Add( item4, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
    
        item13 = wx.StaticText( self, infoLbl, "(*) The password and secret notes in the textbox will be visible. \n(*) Account(username), password and secret notes will be encrypted-stored.", wx.DefaultPosition, wx.DefaultSize, 0 )
        item2.Add( item13, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
    
        item1.Add( item2, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
    
        item15 = wx.StaticBox( self, -1, "Tags" )
        item14 = wx.StaticBoxSizer( item15, wx.VERTICAL )
        
        item16 = wx.ListBox( self, tags, wx.DefaultPosition, [200,200],[] ,wx.LB_MULTIPLE )
        item14.Add( item16, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
    
        item1.Add( item14, 0, wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
    
        item0.Add( item1, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
    
        item17 = wx.BoxSizer( wx.HORIZONTAL )
        
        item19 = wx.Button( self, wx.ID_CANCEL, "Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
        item17.Add( item19, 0, wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
    
        item17.Add( [ 60, 20 ] , 0, wx.ALIGN_CENTER|wx.ALL, 5 )
    
        item18 = wx.Button( self, wx.ID_OK, "OK", wx.DefaultPosition, wx.DefaultSize, 0 )
        item17.Add( item18, 0, wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
    
        item0.Add( item17, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        
        self.parent = parent
        self.title = item6
        self.description = item8
        self.account = item10
        self.password = item12
        self.secret = item21
        self.tags = item16
        self.okBt = item18
        
        self.SetSize(myGui.SIZE_DIALOG_NEWACCOUNT)        
        self.loadTags()
        
        self.SetSizer(item0)        
        self.Show()
    
    
    #load tags
    def loadTags(self):
        tagService = TagService()
        tagList = tagService.getAllTags()
        
        for tag in tagList:
            idx = self.tags.Append(tag.name,tag.id) 
            # select the current selected tag if not in All or Trash
            selectedTagId = self.parent.selectedTagId
            if tag.id ==  selectedTagId and selectedTagId >= 0:
                self.tags.Select(idx)
        
   
    def doSave(self):
        pwdService = PwdService()
        val = self.ShowModal()
        if val == wx.ID_OK:
            
            if len(self.title.GetValue()) == 0:
                myGui.showErrorDialog(myGui.ERR_TITLE_EMPTY)
                self.title.SetFocus()
                self.doSave()
            elif len(self.account.GetValue()) ==0:
                myGui.showErrorDialog(myGui.ERR_ACCOUNT_EMPTY)
                self.account.SetFocus()
                self.doSave()
            elif len(self.password.GetValue()) ==0:
                myGui.showErrorDialog(myGui.ERR_PWD_EMPTY)
                self.password.SetFocus()
                self.doSave()
            elif not pwdService.isTagNameValid(self.title.GetValue()):
                myGui.showErrorDialog(myGui.ERR_ACCOUNTTITLE_UNIQUE)
                self.title.SetFocus()
                self.doSave()
            
            else:
                vTitle = self.title.GetValue()
                vDescription = self.description.GetValue()
                vAccount = self.account.GetValue()
                vPassword = self.password.GetValue()                
                #vSecret = unicode.encode(self.secret.GetValue(),'utf-8')
                vSecret = self.secret.GetValue().encode('utf-8')
                vTagIds = []
                for idx in self.tags.GetSelections():
                    vTagIds.append(self.tags.GetClientData(idx))
                
                pwdService.addAccount(vTitle,vDescription,vAccount,vPassword,vSecret, vTagIds)
                
               
    
class ChgRootPwdDialog(wx.Dialog):
    def __init__(self,parent,id=-1,title="Change Master Password"):
        wx.Dialog.__init__(self,parent,id,title,pos=myGui.DIALOG_POSITION)
        #ID for widges
        #------------------
        ID_TEXT = 2010
        oldRootPwdId = 2011
        newRootPwdId = 2012
        newRootPwdId2 = 2013
        #------------------
        
        item0 = wx.BoxSizer( wx.VERTICAL )
    
        item2 = wx.StaticBox( self, -1, "Change Master password" )
        item1 = wx.StaticBoxSizer( item2, wx.VERTICAL )
        
        item3 = wx.GridSizer( 0, 2, 0, 0 )
        
        item4 = wx.StaticText( self, ID_TEXT, "Current Master password", wx.DefaultPosition, wx.DefaultSize, 0 )
        item3.Add( item4, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
    
        item5 = wx.TextCtrl( self, oldRootPwdId, "", wx.DefaultPosition, myGui.SIZE_NORMAL_TEXT, wx.TE_PASSWORD )
        item3.Add( item5, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
    
        item6 = wx.StaticText( self, ID_TEXT, "New Password", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
        item3.Add( item6, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
    
        item7 = wx.TextCtrl( self, newRootPwdId, "", wx.DefaultPosition, myGui.SIZE_NORMAL_TEXT, wx.TE_PASSWORD )
        item3.Add( item7, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
    
        item8 = wx.StaticText( self, ID_TEXT, "New Password again", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
        item3.Add( item8, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
    
        item9 = wx.TextCtrl( self, newRootPwdId2, "", wx.DefaultPosition, myGui.SIZE_NORMAL_TEXT, wx.TE_PASSWORD )
        item3.Add( item9, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
    
        item1.Add( item3, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
    
        item0.Add( item1, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
    
        item10 = wx.BoxSizer( wx.HORIZONTAL )
        
    
        item12 = wx.Button( self, wx.ID_CANCEL, "Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
        item12.SetDefault()

        item10.Add( [ 20, 20 ] , 0, wx.ALIGN_CENTER|wx.ALL, 5 )
    
        item11 = wx.Button( self, wx.ID_OK, "OK", wx.DefaultPosition, wx.DefaultSize, 0 )
        item10.Add( item11, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        item10.Add( item12, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
    
        item0.Add( item10, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        
        self.parent = parent
        self.oldPwd = item5
        self.newPwd = item7
        self.newPwd2 = item9
        self.okBt = item11
        self.cancelBt = item12
        
        self.SetSize(myGui.SIZE_DIALOG_CHGROOTPWD)        
        
        self.SetSizer(item0)        
        self.Show()
        
    def onChange(self):
        pwdService = PwdService()
        masterService = MasterService()
        
        val = self.ShowModal()
        if val == wx.ID_OK:
            if len(self.oldPwd.GetValue()) < 5 or len(self.oldPwd.GetValue()) > 16:
                myGui.showErrorDialog(myGui.ERR_ROOTPWD_LEN)
                self.oldPwd.SetFocus()
                self.onChange()
            elif len(self.newPwd.GetValue()) < 5 or len(self.newPwd.GetValue()) >16:
                myGui.showErrorDialog(myGui.ERR_ROOTPWD_LEN)
                self.newPwd.SetFocus()
                self.onChange()
            elif self.newPwd.GetValue() != self.newPwd2.GetValue():
                myGui.showErrorDialog(myGui.ERR_NEWROOT_IDENTICAL)
                self.newPwd.SetValue('')
                self.newPwd2.SetValue('')
                self.newPwd.SetFocus()
                self.onChange()
            elif self.oldPwd.GetValue() != config.getRootPwd():
                myGui.showErrorDialog(myGui.ERR_OLDROOT_WRONG)
                self.oldPwd.SetFocus()
                self.onChange()
            
        # validation checking done
            else:
                masterService.changeRootPwd(self.newPwd.GetValue())
                myGui.showInfoDialog(myGui.INFO_ROOTPWD)
            
class PwdGenDialog(wx.Dialog):            
    def __init__(self,parent,id=-1,title="Password Generator", setBack=False):
        wx.Dialog.__init__(self,parent,id,title,pos=myGui.DIALOG_POSITION)
        
        #--------------
        ID_TEXT = 32000
        ID_TEXTCTRL = 32001
        ID_BUTTON_GEN = 32002
        ID_BUTTON_USEIT = 32003
        ID_CHECKBOX=32004
        #--------------
        item0 = wx.BoxSizer( wx.VERTICAL )
    
        item1 = wx.BoxSizer( wx.HORIZONTAL )
        
        item2 = wx.StaticText( self, ID_TEXT, "Password Length", wx.DefaultPosition, wx.DefaultSize, 0 )
        item1.Add( item2, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
    
        item3 = wx.TextCtrl( self, ID_TEXTCTRL, "", wx.DefaultPosition, [80,-1], 0 )
        item1.Add( item3, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
    
        item0.Add( item1, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
    
        item5 = wx.StaticBox( self, -1, "Password Pattern Options" )
        item4 = wx.StaticBoxSizer( item5, wx.HORIZONTAL )
        
        item6 = wx.BoxSizer( wx.VERTICAL )
        
        item7 = wx.CheckBox( self, ID_CHECKBOX, "Lowercase letters (a,b,c,d,e.....z)", wx.DefaultPosition, wx.DefaultSize, 0 )
        item7.SetValue( True )
        item6.Add( item7, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
    
        item8 = wx.CheckBox( self, ID_CHECKBOX, "Uppercase letters (A,B,C,D,E.....Z)", wx.DefaultPosition, wx.DefaultSize, 0 )
        item8.SetValue( True )
        item6.Add( item8, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
    
        item9 = wx.CheckBox( self, ID_CHECKBOX, "Numbers (0,1,2,3,4...9)", wx.DefaultPosition, wx.DefaultSize, 0 )
        item9.SetValue( True )
        item6.Add( item9, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
    
        item10 = wx.CheckBox( self, ID_CHECKBOX, "Punctuations ( #, $, @, [, ), /, ; ,\\,  _, - ... )", wx.DefaultPosition, wx.DefaultSize, 0 )
        item6.Add( item10, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
    
        item4.Add( item6, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
    
        item0.Add( item4, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
    
        item12 = wx.StaticBox( self, -1, "Generated Password" )
        item11 = wx.StaticBoxSizer( item12, wx.HORIZONTAL )
        
        item13 = wx.TextCtrl( self, ID_TEXTCTRL, "", wx.DefaultPosition, [250,-1], wx.TE_READONLY )
        item11.Add( item13, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
    
        item14 = wx.Button( self, -1, "Copy to clipboard", wx.DefaultPosition, wx.DefaultSize, 0 )
        item11.Add( item14, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
    
        item0.Add( item11, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
    
        item15 = wx.BoxSizer( wx.HORIZONTAL )
        
        item16 = wx.Button( self, ID_BUTTON_GEN, "Generate", wx.DefaultPosition, wx.DefaultSize, 0 )
        item15.Add( item16, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
    
        # USE IT Button
        if setBack:
            item15.Add( [ 20, 20 ] , 0, wx.ALIGN_CENTER|wx.ALL, 5 )    
            item17 = wx.Button( self, ID_BUTTON_USEIT, "Use it", wx.DefaultPosition, wx.DefaultSize, 0 )
            self.btUseIt= item17
            item15.Add( item17, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        
    
        item15.Add( [ 20, 20 ] , 0, wx.ALIGN_CENTER|wx.ALL, 5 )
    
        item18 = wx.Button( self, wx.ID_CANCEL, "Close", wx.DefaultPosition, wx.DefaultSize, 0 )
        item15.Add( item18, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
    
        item0.Add( item15, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
    
        self.SetSizer( item0 )
        self.SetSize(myGui.SIZE_DIALOG_PWDGEN) 
        
        self.parent = parent
        self.txtLength= item3
        self.txtPwd= item13
        self.chkLower = item7
        self.chkUpper = item8
        self.chkNumber = item9
        self.chkChar = item10
        self.btCopy = item14
        self.btClose = item12
        self.btGen=item16

            
        
        # set initial disable button, textctrl colors
        self.btCopy.Disable()
        self.txtPwd.SetForegroundColour( '#E2644F' )
        self.txtPwd.SetBackgroundColour( 'BLACK' )
        
        self.Bind(wx.EVT_BUTTON,self.doGenerate,self.btGen)
        self.Bind(wx.EVT_BUTTON,self.copyToClipboard, self.btCopy)
        
        
        
    def doGenerate(self,event):
        patternList=[]
        if self.chkLower.GetValue():
            patternList.append('lower')
        if self.chkUpper.GetValue():
            patternList.append('upper')
        if self.chkNumber.GetValue():
            patternList.append('number')
        if self.chkChar.GetValue():
            patternList.append('punc')
        
        if len(patternList)==0:
            myGui.showErrorDialog(myGui.ERR_PWD_EMPTYPATTERN)
        else:            
            try:                
                length = int(self.txtLength.GetValue())
                if length>0:
                    self.txtPwd.SetValue(util.getRadomString(length, patternList))
                    self.btGen.SetLabel('Regenerate')
                    self.btCopy.Enable(True)
                else:
                    myGui.showErrorDialog(myGui.ERR_PWD_LEN)
                    self.txtLength.SetFocus()
            except ValueError:
                myGui.showErrorDialog(myGui.ERR_PWD_LEN)
                self.txtLength.SetFocus()
    
    def copyToClipboard(self,event):
        if len(self.txtPwd.GetValue().strip()) > 0:
            text_data = wx.TextDataObject(self.txtPwd.GetValue())
            if wx.TheClipboard.Open():
                wx.TheClipboard.SetData(text_data)
                wx.TheClipboard.Close()
            myGui.showInfoDialog(myGui.INFO_PWD_CLIPBOARD )
        else:
            myGui.showErrorDialog(myGui.ERR_PWD_COPY)
                
    def generatePwd(self):
        result=''
        patternList=[]
        val = self.ShowModal()
        
                
class NewTagDialog(wx.TextEntryDialog):
    def __init__(self,parent,id=-1,title="Add new tag"):
        label = 'The name of new tag:'
        wx.TextEntryDialog.__init__(self,parent,label,title,style=wx.OK|wx.CANCEL)
    
    def onSave(self):
        tagService = TagService()
        val = self.ShowModal()
        if val == wx.ID_OK:
            name = self.GetValue()
            if not name:
                myGui.showErrorDialog(myGui.ERR_NEWTAG_EMPTY)
                self.onSave()
            elif not tagService.isTagNameValid(name):
                myGui.showErrorDialog(myGui.ERR_NEWTAG_UNIQUE)
                self.onSave()
                
            else:
                tagService.addNewTag(name)
            
    
            
class EditTagDialog(wx.TextEntryDialog):
    def __init__(self,parent,tagId,title="Edit tag"):
        self.tagId = tagId
        self.tagService = TagService()
        tag = self.tagService.getTagById(tagId)
        label = 'The new name of tag:'
        wx.TextEntryDialog.__init__(self,parent,label,title,defaultValue=tag.name,style=wx.OK|wx.CANCEL)
    
    def onSave(self):
        
        val = self.ShowModal()
        if val == wx.ID_OK:
            name = self.GetValue()
            if not name:
                myGui.showErrorDialog(myGui.ERR_NEWTAG_EMPTY)
                self.onSave()
            elif not self.tagService.isTagNameValid(name,self.tagId):
                myGui.showErrorDialog(myGui.ERR_NEWTAG_UNIQUE)
                self.onSave()
                
            else:
                self.tagService.editTag(self.tagId,name)
