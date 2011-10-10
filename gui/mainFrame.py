# -*- coding: utf-8 -*-
import myGui,util,config
import wx,sys
from service import TagService, PwdService
from wx.lib.mixins.listctrl import  ListCtrlAutoWidthMixin
from dialogs import *
from threading import Thread
#NewPwdDialog,ChgRootPwdDialog,NewTagDialog,EditTagDialog

'''
Created on Mar 23, 2009

@author: kent
'''
class MainWindow(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, - 1, config.APP_NAME + " " + config.VERSION)
        # values for the listCtrl
        self.pwdList = []
        self.searchResult = []
        
        # selected accountId/Tag id
        self.selectedPwdId = None
        self.selectedTagId = None
        
        #service obj
        self.pwdService = PwdService()
        self.tagService = TagService()
        
        # create menu
        self.__createMenu()
        
        # toolbar
        self.__createToolBar()
        
        #splitter window
        self.__createSplitterWindow()
        
        
        self.SetIcon(wx.Icon(myGui.ICON_APP_ICON, wx.BITMAP_TYPE_PNG))
       
        # set the status bar
        bar = self.CreateStatusBar()        
        bar.SetStatusText('Welcome to use Passwd Manager!')
        self.statusBar = bar
        
        self.SetPosition(myGui.MAIN_WINDOW_POSITION)
        self.SetSize(myGui.MAIN_WINDOW_SIZE)
    
        
        
    def updateStatusBar(self,lv):
            self.statusBar.SetStatusText('<=* ! *=>New Version ' + lv + ' is available. Upgrade is HIGHLY RECOMMENDED!')
            myGui.showUpdateDialog(lv)

    def empty(self):
        pass
    
        
    def fixSplitter(self,event):
        self.sp.SetSashPosition(myGui.SPLITTERWINDOW_SASH_POS)
        event.Veto()
        
    
       
    def enableButtons(self):
        if self.selectedTagId == myGui.ID_TAG_TRASH:
            self.__chgTrashTagButtons(True)
        else:    
            self.__chgButtonStatus(True)   
                 
                
    def disableButtons(self):
        self.__chgButtonStatus(False)
        self.__chgTrashTagButtons(False)
        
    
    def __chgTrashTagButtons(self,status):    
        for toolId in myGui.IDS_TRASHTAG_TOOLBAR:
            toolbar = self.GetToolBar()
            toolbar.EnableTool(toolId,status)
            
        for menuId in myGui.IDS_TRASHTAG_MENU:
            menubar = self.GetMenuBar()
            menubar.Enable(menuId,status)
            
            
    def __chgButtonStatus(self,status):
        for toolId in myGui.IDS_ENDISABLE_TOOLBAR:
            toolbar = self.GetToolBar()
            toolbar.EnableTool(toolId,status)
            
        for menuId in myGui.IDS_ENDISABLE_MENU:
            menubar = self.GetMenuBar()
            menubar.Enable(menuId,status)
        
        
    def __createToolBar(self):
        toolbarData = (
                       (wx.ID_ANY,'New',wx.Bitmap(myGui.ICON_TOOLBAR_ADD),'Add new account',self.onNewPwd),
                       (myGui.ID_TOOLBAR_DETAIL,'Account details',wx.Bitmap(myGui.ICON_TOOLBAR_DETAIL),'Show detailed information of selected account',self.showDetail),
                       (myGui.ID_TOOLBAR_EDIT,'Edit account',wx.Bitmap(myGui.ICON_TOOLBAR_EDIT),'Edit the selected account',self.onEditAccount),
                       (myGui.ID_TOOLBAR_TRASH,'Move to trash',wx.Bitmap(myGui.ICON_TOOLBAR_TRASH),'Move selected account to trash',self.onRemove),
                       (myGui.ID_TOOLBAR_RECOVER,'Recover from trash',wx.Bitmap(myGui.ICON_TOOLBAR_RECOVER),'Recover selected account from trash',self.onRecover),
                       (myGui.ID_TOOLBAR_REMOVE,'Remove',wx.Bitmap(myGui.ICON_TOOLBAR_REMOVE),'Remove selected account',self.onRemove),
                       ('','',None,'',None),            
                       (wx.ID_ANY,'Add new tag',wx.Bitmap(myGui.ICON_MENU_NEWTAG),'Add new tag',self.onNewTag),
                       (wx.ID_ANY,'Change Master Password',wx.Bitmap(myGui.ICON_TOOLBAR_ROOTPWD),'Change Master Password',self.onRootPwd),
                       (wx.ID_ANY,'Empty trash',wx.Bitmap(myGui.ICON_TOOLBAR_EMPTYTRASH),'Empty trash',self.onEmptyTrash),
                       (wx.ID_ANY,'Password Generator', wx.Bitmap(myGui.ICON_TOOLBAR_PWDGEN), 'Generating a random password', self.onPwdGen),
                       ('','',None,'',None),
                       ('TEXTAREA','',None,'',None),
                       (wx.ID_ANY,'Search',wx.Bitmap(myGui.ICON_TOOLBAR_SEARCH),'Search',self.onSearch),
                       ('','',None,'',None),                    
                       (wx.ID_ANY,'Quit',wx.Bitmap(myGui.ICON_TOOLBAR_QUIT),'Quit PasswdManager',self.onQuit)
                    )
        toolbar = self.CreateToolBar()
        for id, label, icon, helpInfo, handler in toolbarData:
            if id == 'TEXTAREA':
                txtBox = wx.TextCtrl(toolbar,-1,size =myGui.SIZE_NORMAL_TEXT, style=wx.TE_PROCESS_ENTER)
                txtBox.SetName(myGui.NAME_TEXTBOX_SEARCH)
                toolbar.AddControl(txtBox)
                txtBox.Bind(wx.EVT_TEXT_ENTER, self.onSearch) # bind the <Enter> key

            elif id == '':
                toolbar.AddSeparator()
            else:                
                tool = toolbar.AddLabelTool(id,label,icon,shortHelp=helpInfo)
                self.Bind(wx.EVT_TOOL, handler, tool)

        toolbar.Realize()
    
  


    def __createSplitterWindow(self):
        
        # boxsizer for the splitter
        boxM = wx.BoxSizer(wx.HORIZONTAL)        
        splitter = wx.SplitterWindow(self,-1,style=wx.SP_LIVE_UPDATE | wx.SP_NOBORDER)
        
        boxR = wx.BoxSizer(wx.VERTICAL)  
        panelR = wx.Panel(splitter, style=wx.SUNKEN_BORDER)
        listRight = PwdListCtrl(panelR, -1)
        
        boxR.Add(listRight,1,wx.EXPAND)
        panelR.SetSizer(boxR)       
        
        boxL = wx.BoxSizer(wx.VERTICAL)
        panelL = wx.Panel(splitter, style=wx.SUNKEN_BORDER)        
        listLeft = TagListCtrl(panelL, -1)
        
        boxL.Add(listLeft,1,wx.EXPAND)
        panelL.SetSizer(boxL)
        panelL.SetBackgroundColour('WHITE')
        
        
        splitter.SplitVertically(panelL,panelR)
        splitter.Bind(wx.EVT_SPLITTER_DCLICK,self.fixSplitter)
        splitter.SetSashPosition(myGui.SPLITTERWINDOW_SASH_POS)
        
        boxM.Add(splitter,1,wx.EXPAND|wx.TOP| wx.BOTTOM,1)
        self.SetSizer(boxM)
        
        #default select the first tag       
        listLeft.Select(0,True)
        
        self.sp = splitter
        
     
       

    def __createMenu(self):  
        menuData = (
                    ('Account',         (-1,'&New Account','Add new account',self.onNewPwd,myGui.ICON_MENU_ADD),
                                        (myGui.ID_MENU_DETAIL,'Account details','Show detailed information of selected account',self.showDetail,myGui.ICON_MENU_DETAIL),
                                        (myGui.ID_MENU_EDIT,'Edit account','Edit the selected account',self.onEditAccount,myGui.ICON_MENU_EDIT),
                                        (myGui.ID_MENU_TRASH,'Move to trash','Move selected account to trash',self.onRemove,myGui.ICON_MENU_TRASH),
                                        (myGui.ID_MENU_RECOVER,'Recover from trash','Recover selected account from',self.onRecover,myGui.ICON_MENU_RECOVER),
                                        (myGui.ID_MENU_REMOVE,'Remove selected account','Remove selected account',self.onRemove,myGui.ICON_MENU_REMOVE),
                                        ('','','','',None),
                                        (-1,'&Quit','Quit Passwd Manager',self.onQuit,myGui.ICON_MENU_QUIT)),
                                        
                    ('Setting',         (-1,'Master password','managing master password',self.onRootPwd,myGui.ICON_MENU_ROOTPWD),
                                        (-1,'Password Generator', 'Generating a random password', self.onPwdGen, myGui.ICON_MENU_PWDGEN),
                                        (-1,'New Tag','Add new Tag',self.onNewTag,myGui.ICON_MENU_NEWTAG),
                                        (-1,'&Empty trash','Empty trash',self.onEmptyTrash,myGui.ICON_MENU_EMPTYTRASH)),
                                        
                    ('Help',            (-1, 'Check updates','Check update...',self.onUpdate,myGui.ICON_MENU_UPDATE),
                                        (-1, 'About','About Passwd Manager...',self.onAbout,myGui.ICON_MENU_ABOUT))
                    )
        menuBar = wx.MenuBar(wx.MB_DOCKABLE);
        for entry in menuData:
            menuLabel = entry[0]
            menuItems = entry[1:]        
            menuBar.Append(self.__getMenu(menuItems),menuLabel)
        self.SetMenuBar(menuBar)
        
    
    
    def __getMenu(self,menuItems):
        menu = wx.Menu()
        for id, label, status, handler, icon in menuItems:
            if not label:
                menu.AppendSeparator()
                continue
            menuItem = wx.MenuItem(menu, id, label)
            menuItem.SetHelp(status)
            if icon != None:
                menuItem.SetBitmap(wx.Bitmap(icon))
            menu.AppendItem(menuItem)
            
            self.Bind(wx.EVT_MENU, handler,menuItem)
        return menu
    
    #menu handlers
    def onNewPwd(self,event):
#        print 'click addnew'
        newDlg = NewPwdDialog(self)
        newDlg.doSave()
        self.reLoadWindow()
        
    def onQuit(self,event):
        self.Close()
        exit()
        
    def onUpdate(self, event):        
        lv = config.LATEST_VERSION
        if lv == None: # the html not get fetched yet
            updatechk = UpdateChecker(self,True)
            updatechk.start()
            
        elif lv>config.VERSION:
            myGui.showUpdateDialog(lv)
        else:
            myGui.showInfoDialog("Your passwd Manager is up to date.")
        
    def onSearch(self,event):    
        
        kwBox = self.FindWindowByName(myGui.NAME_TEXTBOX_SEARCH)
        keyword = kwBox.GetValue()
        if(len(keyword)==0):
            myGui.showErrorDialog(myGui.ERR_SEARCH_EMPTY)
            kwBox.SetFocus()
        else:
            self.searchResult = self.pwdService.getSearchResult(keyword)
            self.reLoadWindow(myGui.ID_TAG_SEARCH)

        
        
    def showDetail(self,event):
        dlg = AccountDetailDialog(self,self.selectedPwdId)
        dlg.onClick()
        dlg.Destroy()
        
    def onEditAccount(self,event):
        dlg = EditAccountDialog(self,self.selectedPwdId)
        dlg.onSave()
        self.reLoadWindow()
        dlg.Destroy()
    
    def onCopyPassword(self,event):
        account = self.pwdService.getPwdById(self.selectedPwdId)
        # decrypted password
        dePwd = util.decrypt(config.getRootPwd(),account.pwd)
        text_data = wx.TextDataObject(dePwd)
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(text_data)
            wx.TheClipboard.Close()
        myGui.showInfoDialog(myGui.INFO_CLIPBOARD , account.title)
        
    def onEmptyTrash(self,event):
        if myGui.showConfirmationDialog(myGui.CONFIRM_EMPTY_TRASH)==wx.ID_YES:
            self.pwdService.emptyTrash()
            self.reLoadWindow()
        
    
    def onRecover(self,event):
        account = self.pwdService.getPwdById(self.selectedPwdId)
        self.pwdService.recoverFromTrash(account.id)
        self.reLoadWindow()
        myGui.showInfoDialog(myGui.INFO_RECOVERED, account.title)
        
    def onRemove(self,event):
        '''
        if the currentTag was not Trash, move the selected account to trash. otherwise remove the account.
        @param event:        
        '''
        account = self.pwdService.getPwdById(self.selectedPwdId)
        
        if self.selectedTagId == myGui.ID_TAG_TRASH:
            if myGui.showConfirmationDialog(myGui.CONFIRM_COMPLETE_REMOVE , account.title)==wx.ID_YES:
                self.pwdService.deleteAccount(account.id)
                self.reLoadWindow()

        else:    # move to Trash
            if myGui.showConfirmationDialog(myGui.CONFIRM_MOVETO_TRASH , account.title) ==wx.ID_YES:
                self.pwdService.moveToTrash(account.id)

                # if in search, searchList needs to be maintained.
                if self.selectedTagId == myGui.ID_TAG_SEARCH: 
                    for pwd in self.searchResult:
                        if pwd.id == account.id:
                            self.searchResult.remove(pwd)
                            break;
                        
                self.reLoadWindow()

            
    def onAbout(self,event):
        myGui.showAboutDialog()
        
        
    def onRootPwd(self,event):
        rootDlg = ChgRootPwdDialog(self)
        rootDlg.onChange()
        self.reLoadWindow()
        rootDlg.Destroy()
        
        
    def onTagMgmt(self,event):
        pass
    
    def onNewTag(self,event):
        newTagDlg =  NewTagDialog(self)
        newTagDlg.onSave()
        self.reLoadWindow()
        newTagDlg.Destroy()
        
    def onEditTag(self,event):
        editTagDlg =  EditTagDialog(self,self.selectedTagId)
        editTagDlg.onSave()
        self.reLoadWindow()   
        editTagDlg.Destroy()
        
    def onRemoveTag(self,event):
        tag = self.tagService.getTagById(self.selectedTagId)
        count = self.tagService.getPwdCountByTagId(tag.id)
        if count>0:
            if myGui.showConfirmationDialog(myGui.CONFIRM_REMOVE_USEDTAG,tag.name)==wx.ID_YES:
                self.tagService.removeTagInUse(tag.id)
                self.reLoadWindow(tag.id)
        elif myGui.showConfirmationDialog(myGui.CONFIRM_REMOVE_TAG, tag.name)==wx.ID_YES:            
            self.tagService.removeTag(tag.id)
            self.reLoadWindow()   
    
    def onPwdGen(self,event):
        pwdGenDlg = PwdGenDialog(self)
        pwdGenDlg.generatePwd()
    
    def reLoadWindow(self, selectedTag=None):
        '''
        reload the window data.  calling the TagListCtrl loadTags        
        '''
        if not selectedTag:
            selectedTag = self.selectedTagId
        self.FindWindowByName(myGui.TAG_LIST_NAME).loadTags(selectedTag)
    
    
# tag list at left side of window splitter
class TagListCtrl(wx.ListCtrl):
    '''
    Tag list ctrlList widget
    '''
    
    def __init__(self,parent,id):
        
        images = (myGui.ICON_TAG_CUSTOM, myGui.ICON_TAG_ALL,myGui.ICON_TAG_SEARCH, myGui.ICON_TAG_TRASH, myGui.ICON_TAG_FAV)
        
        wx.ListCtrl.__init__(self,parent,id,style=wx.LC_REPORT|wx.LC_HRULES| wx.LC_SINGLE_SEL)
       
        
        
        self.SetName(myGui.TAG_LIST_NAME)
        self.parent = parent
        self.mainFrm = self.GetTopLevelParent() # main Frame
        il = wx.ImageList(24,24)
        for image in images:
            il.Add(wx.Bitmap(image,wx.BITMAP_TYPE_PNG))

        self.InsertColumn(0,'Tags')
        self.AssignImageList(il,wx.IMAGE_LIST_SMALL)
        
        #popup menu
        self.popmenu = None
        
        # bind the events
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelect)
        
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.onTagMgmt)   # right click
         
        self.loadTags()
        

    def onTagMgmt(self,event):
        tagId = event.GetData()
        pos = event.GetPosition()
        if tagId <= 0:
          
            #popup menu:

            popMenuData = (
                           (-1,'Add new tag','Add new tag',self.mainFrm.onNewTag,myGui.ICON_MENU_NEWTAG),
                        )  
        else : # editable tag right clicked
            popMenuData = (
                           (-1,'Edit Tag','Edit tag',self.mainFrm.onEditTag,myGui.ICON_MENU_EDIT),
                           (-1,'Delete Tag','Delete tag',self.mainFrm.onRemoveTag,myGui.ICON_MENU_DELTAG),
                           (-1,'Add new Tag','Add new account',self.mainFrm.onNewTag,myGui.ICON_MENU_NEWTAG)
                        )  
                
                
        self.popmenu = None
        self.popmenu = wx.Menu()
                        
        for id, label, info, handler,icon in popMenuData:            
#                m = self.popmenu.Append(-1, lbl, info)
#                self.Bind(wx.EVT_MENU, handler, m)    
                
            menuItem = wx.MenuItem(self.popmenu, id, label)
            menuItem.SetHelp(info)
            if icon != None:
                menuItem.SetBitmap(wx.Bitmap(icon))
            self.popmenu.AppendItem(menuItem)
                
            self.Bind(wx.EVT_MENU, handler,menuItem)
                
                
        self.PopupMenu(self.popmenu,pos)
        pass
        
    def loadTags(self, selectedId=myGui.ID_TAG_FAV):
        '''
         load Tags, including "All", search 
         default select Favorite         
        '''
        mw = self.mainFrm
        pwdListCtrl = mw.FindWindowByName(myGui.PWD_LIST_NAME)
        tagService = TagService()
        pwdService = PwdService()

        allPwdCount = pwdService.getAllPwdCount()
        trashPwdCount = pwdService.getPwdCountInTrash()
        tagList = tagService.getAllTags()
        self.DeleteAllItems()
        
        idx_data = [] # [ (data,idx)]
        
        for tag in tagList:
            count = tagService.getPwdCountByTagId(tag.id)
            if tag.id == myGui.ID_TAG_FAV:       #Fav tag, using fav. icon. Fav id is always 0
                idx = self.InsertStringItem(sys.maxint,'%s (%d)' % (tag.name,count) ,4)
            else:
                idx = self.InsertStringItem(sys.maxint,'%s (%d)' % (tag.name,count) ,0)
            self.SetItemData(idx,tag.id)
            idx_data.append((tag.id,idx))
        
        #all tag
        idxAll = self.InsertStringItem(sys.maxint, 'All (%d)' % allPwdCount,1)
        self.SetItemData(idxAll, myGui.ID_TAG_ALL)
        idx_data.append((myGui.ID_TAG_ALL,idxAll))
        
        #search result tag
        idxSearch = self.InsertStringItem(sys.maxint, 'Result (%d)' % len(mw.searchResult) ,2)
        self.SetItemData(idxSearch, myGui.ID_TAG_SEARCH)
        idx_data.append((myGui.ID_TAG_SEARCH,idxSearch))
        
        #TRASH tag
        idxTrash = self.InsertStringItem(sys.maxint, 'Trash (%d)' % trashPwdCount ,3)
        self.SetItemData(idxTrash, myGui.ID_TAG_TRASH)
        idx_data.append((myGui.ID_TAG_TRASH,idxTrash))
        
       
        #get selected index
        sIdx = idxAll
        for data, tmpIdx in idx_data:
            if data != selectedId:
                continue
            else:
                sIdx = tmpIdx
                break 
      
        self.Select(sIdx,1)
        
            
    def OnSize(self, event):
        size = self.parent.GetSize()
        self.SetColumnWidth(0, size.x-5)        
        event.Skip()
        

            
    def OnSelect(self, event):
        mw = self.mainFrm
        tagId = event.GetData()
        #set mainwindow selected tagid
        mw.selectedTagId = tagId
        pwdService = PwdService()
#        print "tag: %d was clicked" % tagId
        pwdListCtrl = mw.FindWindowByName(myGui.PWD_LIST_NAME)
        
        if tagId == myGui.ID_TAG_SEARCH:
            pwdListCtrl.loadSearchResult()            
        else:
            mw.pwdList = pwdService.getPwdListFromTagId(tagId)
            pwdListCtrl.loadPwd()
        
        
        

class PwdListCtrl(wx.ListCtrl,  ListCtrlAutoWidthMixin):
    
    def __init__(self, parent, id,tagId=-1):
        self.parent = parent
        wx.ListCtrl.__init__(self,parent,id,style=wx.LC_REPORT| wx.LC_SINGLE_SEL)
        self.SetName(myGui.PWD_LIST_NAME)
        self.mainFrm = self.GetTopLevelParent()
        #popup menu
        self.popmenu =None
        
        ListCtrlAutoWidthMixin.__init__(self)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.mainFrm.showDetail)   # Dbclick
        
    def loadSearchResult(self): 
        mw = self.mainFrm
        mw.pwdList = mw.searchResult
        self.loadPwd()      

        
    
    def loadPwd(self):
        tagService = TagService()
        mw = self.mainFrm
#        columns = ['check','Tag','Name','Description','Account']
        self.ClearAll()        
  
        #columns
        self.InsertColumn(0,'Tags',width=200)
        self.InsertColumn(1,'Title',width=150)
        self.InsertColumn(2,'Account',width=200)
        self.InsertColumn(3,'Description')
        
        # load pwd items
        for pwd in mw.pwdList:
            tags = pwd.tags
            tagStr = tagService.getTagNameString(tags)
            index = self.InsertStringItem(sys.maxint,tagStr)    

            self.SetStringItem(index,1,pwd.title)
            self.SetStringItem(index,2,pwd.username)
            self.SetStringItem(index,3,pwd.description)
            
            # attach pwd id on the row 
            self.SetItemData(index,pwd.id)
        
        #clean the selected id for the mainWindow
        #disable tools and menuitems
        self.mainFrm.currentId = None
        self.mainFrm.disableButtons()

     # if the list has entries, select the first one index=0.
#        if self.GetItemCount > 0: 
#            self.Select(0,True)
            
                
        #bind the event handler    
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.onRightClick,self)   # right click     
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onSelect,self)    # select
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.onDeSelect,self)    # deselect
    
        self.resizeLastColumn(200)
        
        
        
    def onDeSelect(self,event):
        #clean the selected id
        self.mainFrm.selectedPwdId = None
        #disable buttons
        self.mainFrm.disableButtons()
        
    def onSelect(self,event):
        pwdId = event.GetData()
        self.mainFrm.selectedPwdId = pwdId
        # once there is any entry selected, active buttons
        self.mainFrm.enableButtons()
            
    def onRightClick(self,event):
        pwdId = event.GetData()
        if pwdId != 0:
            pos = event.GetPosition()
          
            #popup menu:
            if self.mainFrm.selectedTagId != myGui.ID_TAG_TRASH: # normal tag
                popMenuData = (
                           (-1,'Copy password to clipboard','Copy decrypted password of selected account to clipboard',self.mainFrm.onCopyPassword,myGui.ICON_MENU_PASTE),
                           (myGui.ID_MENU_DETAIL,'Account details','Show detailed information of selected account',self.mainFrm.showDetail,myGui.ICON_MENU_DETAIL),
                           (myGui.ID_MENU_EDIT,'Edit account','Edit the selected account',self.mainFrm.onEditAccount,myGui.ICON_MENU_EDIT),
                           (-1,'Add new account','Add new account',self.mainFrm.onNewPwd,myGui.ICON_MENU_ADD),
                           (myGui.ID_MENU_TRASH,'Move to trash','Move selected account to trash',self.mainFrm.onRemove,myGui.ICON_MENU_TRASH)
                        )  
            else : # trash tag
                popMenuData = (
                           (myGui.ID_MENU_REMOVE,'Delete from trash','Delete selected account from trash',self.mainFrm.onRemove,myGui.ICON_MENU_REMOVE),
                           (myGui.ID_MENU_RECOVER,'Recover from trash','Recover selected account from trash',self.mainFrm.onRecover,myGui.ICON_MENU_RECOVER)
                        )  
                
                
            self.popmenu = None
            self.popmenu = wx.Menu()
                        
            for id, label, info, handler,icon in popMenuData:            
                
                menuItem = wx.MenuItem(self.popmenu, id, label)
                menuItem.SetHelp(info)
                if icon != None:
                    menuItem.SetBitmap(wx.Bitmap(icon))
                self.popmenu.AppendItem(menuItem)
            
                self.Bind(wx.EVT_MENU, handler,menuItem)
                
                
            self.PopupMenu(self.popmenu,pos)
        
    


class UpdateChecker(Thread):
    def __init__(self,mainWindow,popup=False):
        Thread.__init__(self)
        self.mw = mainWindow
        self.popup = popup #anyway popup a dialog, evenif there is no update
    
    def run(self):
        
        lv = util.getLatestVersion(config.VERSION_URL)
        config.setLatestVersion(lv)     
        if lv>config.VERSION:
            wx.CallAfter(self.mw.updateStatusBar,lv)
        else :
            if self.popup:
                myGui.showInfoDialog("Your password Manager is up to date.")
            wx.CallAfter(self.mw.empty)

    
