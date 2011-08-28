'''
Created on Mar 27, 2009

@author: kent
'''
from dao import *
import config
import util
import gui.myGui as myGui
import datetime

class RemoveTagException: pass

class Service:
    def __init__(self):        
        ''' constructor '''
    
    def getConnection(self):
        conn = sqlite.connect(config.CONN_PATH)
        return conn
         
    
    
class MasterService(Service):
    '''
    classdocs
    '''


    def __init__(selfparams):
        '''
        Constructor
        '''
    def getMasterPwd(self):
        '''
        get master passwd (md5 encrypted)
        '''
        conn = self.getConnection()
        masterDao = MasterDao(conn)
        result = masterDao.getMasterPwd()
        conn.close()
        return result    
    
    
    def authentication(self,pwd):
        md5String = util.md5Encode(pwd)
        md5Pwd = self.getMasterPwd()
        return True if md5String == md5Pwd else False
    
    def changeRootPwd(self,newRootPwd):
        oldPwd = config.getRootPwd()
        
        conn = self.getConnection()
        masterDao = MasterDao(conn)
        pwdDao = PwdDao(conn)
        
        # 1 re-encrypt all passwords with new root pwd
        accountList = pwdDao.getAllPasswd()
        currentDate = datetime.datetime.today()
        for account in accountList:
            dePassword = util.decrypt(oldPwd, account.pwd)
            enPassword = util.encrypt(newRootPwd, dePassword)

            deSecret = util.decrypt(oldPwd, account.secret)
            enSecret = util.encrypt(newRootPwd, deSecret)

            deUsername = util.decrypt(oldPwd, account.username)
            enUsername = util.encrypt(newRootPwd, deUsername)

            account.pwd = enPassword
            account.username = enUsername
            account.secret = enSecret

            account.lastupdate = currentDate
            pwdDao.updateAccount(account.id,account.title, account.description, account.username, 
                                 account.pwd, account.secret,account.lastupdate)
            
        
        # 2 get md5 of new root pwd, update the rootpassword table
        newMd5String = util.md5Encode(newRootPwd)
        masterDao.updateMasterPwd(newMd5String)
        
        # 3 update master password in config module.
        config.setRootPwd(newRootPwd)
        
        conn.commit()
        conn.close()
        
        
            
class PwdService(Service):
    '''
    classdocs
    '''


    def __init__(selfparams):
        '''
        Constructor
        '''
    def decryptUsername(self, pwd):
        if pwd.username:
            pwd.username = util.decrypt(config.getRootPwd(),pwd.username)
        return pwd
        

    def getAllPasswd(self):
        conn = self.getConnection()
        pwdDao = PwdDao(conn)
        result = pwdDao.getAllPasswd()
        #decrypt username
        result = [ self.decryptUsername(pwd) for pwd in result ]
        conn.close()
        return result
    
    def getPwdById(self,pwdId):
        conn = self.getConnection()
        pwdDao = PwdDao(conn)
        result = pwdDao.getPwdById(pwdId)
        result.username = util.decrypt(config.getRootPwd(), result.username)
        conn.close()
        return result
        
        
    def getAllPwdCount(self):
        result = 0
        conn = self.getConnection()
        pwdDao = PwdDao(conn)
        result = pwdDao.getAllPwdCount()
        conn.close()
        return result
    
    def getPwdCountInTrash(self):
        result = 0
        conn = self.getConnection()
        pwdDao = PwdDao(conn)
        result = pwdDao.getPwdCountInTrash()
        conn.close()
        return result

    def getPwdListFromTagId(self,tagId,keyword=''): 
        conn = self.getConnection()
        pwdDao = PwdDao(conn)
        result = []
        if tagId == myGui.ID_TAG_ALL: # ALL selected
            result = pwdDao.getAllPasswd()       
        elif tagId == myGui.ID_TAG_TRASH : #trash select    
            result = pwdDao.getPwdListInTrash()
        else:
            result = pwdDao.getPwdListFromTagId(tagId)
        
        #decrypt username
        result = [ self.decryptUsername(pwd) for pwd in result ]
        conn.close()
        return result
    
    def getSearchResult(self, keyword):
        conn = self.getConnection()
        pwdDao = PwdDao(conn)
        result = pwdDao.getSearchResult(keyword)
        #decrypt username
        result = [ self.decryptUsername(pwd) for pwd in result ]

        conn.close()
        
        return result
    
    
    def editAccount(self,id,title,description,account,password,secret,tagIds):
        '''
        update account 
        @param title: account title
        @param description: account description
        @param account: account name/username, emailaddr, ....
        @param secret: secret text from user
        @param password: password , it will not get updated if value is None
        @param tagIds: a list of related tagIds
        
        '''
        conn = self.getConnection()
        pwdDao = PwdDao(conn)
        pwdObj = pwdDao.getPwdById(id)
        masterPwd = config.getRootPwd()
        
        
        ePassword = util.encrypt(masterPwd, password) if password else pwdObj.pwd
        eSecret = util.encrypt(masterPwd,secret) if secret else ""
        eUsername = util.encrypt(masterPwd, account) if account else ""

        current = datetime.datetime.today()
        pwdDao.updateAccount(id, title, description, eUsername, ePassword, eSecret, current)
        
        #2 process tags
        pwdDao.updateAccountTags(id, tagIds)
        
        conn.commit()
        conn.close()
        
    def addAccount(self,title,description,account,password,secret,tagIds):
        '''
        add a user input account to database
        @param title: account title
        @param description: account description
        @param account: account name/username, emailaddr, ....
        @param password: password
        @param secret: the secret text from user
        @param tagIds: a list of related tagIds
        
        '''
        conn = self.getConnection()
        pwdDao = PwdDao(conn)
        
         # encode account & password
        master = config.getRootPwd()
        ePassword = util.encrypt(master, password)
        eSecret = util.encrypt(master,secret) if secret else ""
        eAccount = util.encrypt(master, account) if account else ""
        current = datetime.datetime.today()
        id = pwdDao.getPwdId()
        #insert the account
        pwdDao.insertAccount(id, title, description, eAccount, ePassword, eSecret, current)
        
        #add tag to the new account if there is
        if len(tagIds) > 0 :
            pwdDao.setTagsOnAccount(id, tagIds)
            
        conn.commit()
        conn.close()
        
    def recoverFromTrash(self,pwdId):
        conn = self.getConnection()
        pwdDao = PwdDao(conn)       
        pwdDao.recoverFromTrash(pwdId)            
        conn.commit()
        conn.close()
        
    def moveToTrash(self,pwdId):
        conn = self.getConnection()
        pwdDao = PwdDao(conn)       
        pwdDao.moveToTrash(pwdId)            
        conn.commit()
        conn.close()
        
    def deleteAccount(self,pwdId):
        conn = self.getConnection()
        pwdDao = PwdDao(conn)       
        pwdDao.deleteAccount(pwdId)            
        conn.commit()
        conn.close()
        
    def emptyTrash(self):
        conn = self.getConnection()
        pwdDao = PwdDao(conn)       
        pwdDao.emptyTrash()           
        conn.commit()
        conn.close()
        
    def isTagNameValid(self,name,id=-1):
        conn = self.getConnection()
        pwdDao = PwdDao(conn)
        result = pwdDao.isAccountNameValid(name, id)
        conn.close()
        return result   
        
class TagService(Service):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    def getAllTags(self):
        conn = self.getConnection()
        tagDao = TagDao(conn)
        result = tagDao.getAllTags()
        conn.close()
        return result
        
    def getPwdCountByTagId(self, tagId):
        conn = self.getConnection()
        tagDao = TagDao(conn)
        result = tagDao.getPwdCountByTagId(tagId)
        conn.close()
        return result

    def addNewTag(self,name):
        conn = self.getConnection()
        tagDao = TagDao(conn)
        tagDao.insertTag(name)
        conn.commit()
        conn.close()

    def editTag(self,tagId,name):
        conn = self.getConnection()
        tagDao = TagDao(conn)
        tagDao.updateTag(tagId, name)
        conn.commit()
        conn.close()
        
    def removeTag(self,tagId):
        conn = self.getConnection()
        tagDao = TagDao(conn)
        tagDao.deleteTag(tagId)
        conn.commit()
        conn.close();
        
    def removeTagInUse(self,tagId):
        conn = self.getConnection()
        tagDao = TagDao(conn)
        
        tagDao.removeTagFromAccount(tagId)
        tagDao.deleteTag(tagId)
        conn.commit()
        conn.close();
    
    def getTagById(self,tagId):
        conn = self.getConnection()
        tagDao = TagDao(conn)
        result = tagDao.getTagById(tagId)
        conn.close()
        return result
        
        
    def isTagNameValid(self,name,id=-1):
        conn = self.getConnection()
        tagDao = TagDao(conn)
        result = tagDao.isTagNameValid(name,id)
        conn.close()
        return result
    
    def getTagNameString(self,tags):
        tagStr = '<'
        for tag in tags:
            if tag:
                tagStr += tag.name
                if tag!=tags[-1]:
                    tagStr += '> <'
        tagStr +='>'  
        return tagStr
        
        
        
