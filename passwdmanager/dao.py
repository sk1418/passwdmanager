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
Created on Mar 27, 2009

@author: kent
'''
import sqlite3 as sqlite
from entity import *
import util

class MasterDao(object):
    '''
    data access object for Entity MasterPassword
    default master password: password
    encrypted MD5:5f4dcc3b5aa765d61d8327deb882cf99
    '''


    def __init__(self, conn):
        '''
        Constructor
        '''
        self.conn = conn
        
    def getMasterPwd(self):
        '''
        get master passwd (md5 encrypted)
        '''
        sql = """ SELECT md5String FROM ROOTPASSWORD """
        cur = self.conn.cursor()
        cur.execute(sql)
        mPwd = cur.fetchone()[0]
        cur.close()
        return mPwd
    
    def updateMasterPwd(self,newMd5):
        sql = """
                update ROOTPASSWORD set md5String=?
            """
        cur = self.conn.cursor()
        cur.execute(sql,(newMd5,))
        cur.close()



class PwdDao():
    '''
    Pwd Dao
    '''


    def __init__(self,conn):
        '''
        Constructor
        '''
        self.conn = conn

    def getAllPasswd(self):
        '''
        Get all UNDELETED account(password items), 
        '''
        pwdList = []
        cur = self.conn.cursor()
        sql = 'select id, title,  description, username, password,secret, deleted,createdate,lastupdate FROM ACCOUNT where deleted<>1'
        cur.execute(sql)
        
        tagDao = TagDao(self.conn)
        
        for row in cur.fetchall():
            pwd = Passwd()
            (pwd.id,pwd.title, pwd.description,    pwd.username,  pwd.pwd, pwd.secret, pwd.deleted,pwd.createdate,pwd.lastupdate) = row
            
            if pwd.id != 0:
                tagList = tagDao.getTagsByPwdId(pwd.id);
                pwd.tags = tagList
                pwdList.append(pwd)
            
        cur.close()
        return pwdList
    
    def getPwdById(self,pwdId):
        cur = self.conn.cursor()
        sql = 'select id, title,  description, username, password,secret,deleted,createdate,lastupdate FROM ACCOUNT where id=?'
        cur.execute(sql,(pwdId,))
        
        tagDao = TagDao(self.conn)
        
        pwd = Passwd()
        (pwd.id,pwd.title, pwd.description,    pwd.username,  pwd.pwd, pwd.secret, pwd.deleted,pwd.createdate,pwd.lastupdate) = cur.fetchone()
            
        if pwd.id != 0:
            tagList = tagDao.getTagsByPwdId(pwd.id);
            pwd.tags = tagList
            
            
        cur.close()
        return pwd
    
    def getAllPwdCount(self):
        result =  0
        cur = self.conn.cursor()
        sql = 'SELECT count(id) FROM ACCOUNT WHERE deleted<>1 '
        cur.execute(sql)
        result = cur.fetchone()[0]
        cur.close()
        return result


    def getPwdListFromTagId(self,tagId):
        
        pwdList = []
        sql = """select id, title,  description, username, password, secret,deleted,createdate,lastupdate FROM ACCOUNT WHERE id in (
                    SELECT pwdid FROM PWDTAGJOIN WHERE tagid = ? AND deleted<>1
                 ) 
        """
        
        cur = self.conn.cursor()
        cur.execute(sql,(tagId,))
        tagDao = TagDao(self.conn)
        
        for row in cur.fetchall():
            pwd = Passwd()
            (pwd.id,pwd.title, pwd.description, pwd.username,pwd.pwd, pwd.secret,pwd.deleted,pwd.createdate,pwd.lastupdate) = row
            
            if pwd.id != 0:
                tagList = tagDao.getTagsByPwdId(pwd.id);
                pwd.tags = tagList
                pwdList.append(pwd)
            
        cur.close()
        return pwdList
    
    def updateAccount(self,id,title, description, username, password,secret,lastupdate):
        
        sql = """
                UPDATE ACCOUNT SET title=?, description=?, username=?,password=?,secret=?,lastupdate=?   WHERE id=?
            """
        cur = self.conn.cursor()
        cur.execute(sql,(title,description,username,password,secret,lastupdate,id))
        cur.close()
        return id
        
            
            
        
    def insertAccount(self, id,title, description, account, password,secret,createdate):
        sql = """
                Insert Into ACCOUNT (id,title,description,username,password,secret,createdate,lastupdate)
                VALUES(?,?,?,?,?,?,?,?)
        """
     
        cur = self.conn.cursor()
        cur.execute(sql,(id,title,description,account,password,secret,createdate,createdate))
        cur.close()
        
        return id
    
    def recoverFromTrash(self,pwdId):
        sql = """ UPDATE ACCOUNT SET deleted = 0 WHERE id=?"""
        cur = self.conn.cursor()
        cur.execute(sql,(pwdId,))
        cur.close()
    
    
    def moveToTrash(self,pwdId):
        sql = """ UPDATE ACCOUNT SET deleted = 1 WHERE id=?"""
        cur = self.conn.cursor()
        cur.execute(sql,(pwdId,))
        cur.close()
    
    def emptyTrash(self):
        sql = """ DELETE FROM ACCOUNT WHERE deleted=1"""
        cur = self.conn.cursor()
        cur.execute(sql)
        cur.close()
        
    def deleteAccount(self,pwdId):
        sql = """ DELETE FROM ACCOUNT WHERE id=?"""
        cur = self.conn.cursor()
        cur.execute(sql,(pwdId,))
        cur.close()
    
    def setTagsOnAccount(self,accountId, tagIds):
        sql = """
            INSERT INTO PWDTAGJOIN(pwdid,tagid)VALUES(?,?)            
            """
        cur = self.conn.cursor()
        for tagId in tagIds:
            cur.execute(sql,(accountId,tagId))
        cur.close()
    
    def updateAccountTags(self,accountId,tagIds):
        #1 remove all related tags by the accountId
        sql=""" DELETE FROM PWDTAGJOIN WHERE pwdid=?"""
        cur = self.conn.cursor()
        cur.execute(sql,(accountId,))
        cur.close()
        
        #2 insert passed in tagids
        self.setTagsOnAccount(accountId, tagIds)
        
        
    def getPwdId(self):
        '''
        get the next available id
        '''
        sql = """
            SELECT max(id) from ACCOUNT
        """
        cur = self.conn.cursor()
        cur.execute(sql)
        row = cur.fetchone()[0]
        return row+1 if row !=None else  1
    
    def getSearchResult(self,keyword):
        '''
        username is also encrypted, so it is not in search.
        '''
        pwdList=[]
        sql = """ 
            SELECT id, title,  description, username, password FROM ACCOUNT WHERE 
                (title LIKE ? OR
                description LIKE ? 
                 )AND
                deleted<>1
        """
        keyword = '%'+keyword+'%'
        cur = self.conn.cursor()
        cur.execute(sql,(keyword,keyword))
        tagDao = TagDao(self.conn)
        
        for row in cur.fetchall():
            pwd = Passwd()
            (pwd.id,pwd.title, pwd.description,    pwd.username,  pwd.pwd) = row
            
            if pwd.id != 0:
                tagList = tagDao.getTagsByPwdId(pwd.id);
                pwd.tags = tagList
                pwdList.append(pwd)
            
        cur.close()
        return pwdList
    
    def getPwdListInTrash(self):
        pwdList = []
        cur = self.conn.cursor()
        sql = """
            select id, title,  description, username, password,deleted,createdate,lastupdate 
            FROM ACCOUNT where deleted=1
            """
        cur.execute(sql)
        
        tagDao = TagDao(self.conn)
        
        for row in cur.fetchall():
            pwd = Passwd()
            (pwd.id,pwd.title, pwd.description,    pwd.username,  pwd.pwd, pwd.deleted,pwd.createdate,pwd.lastupdate) = row
            
            if pwd.id != 0:
                tagList = tagDao.getTagsByPwdId(pwd.id);
                pwd.tags = tagList
                pwdList.append(pwd)
            
        cur.close()
        return pwdList
    
    def getPwdCountInTrash(self):
        result = 0
        sql = """
            SELECT count(id) from account where deleted =1
        """
        cur = self.conn.cursor()
        cur.execute(sql)
        result = cur.fetchone()[0]
        return result
    
    def isAccountNameValid(self,name,id=-1):
        cur = self.conn.cursor()
        if id == -1 :
            sql = """  select id from ACCOUNT where title=?   """
            cur.execute(sql,(name,))
        else:
            sql =  """  select id from ACCOUNT where title=? AND id<>?   """
            cur.execute(sql,(name,id))
        row = cur.fetchone()
        cur.close()
        return True  if row ==None else  False
    
    
class TagDao():
    '''
    Dao class for Tag 
    '''


    def __init__(self, conn):
        '''
        Constructor
        '''
        self.conn = conn
    
    def updateTag(self,tagId,name):
        sql = """ UPDATE TAG SET name=? where id=?"""
        cur = self.conn.cursor()
        cur.execute(sql,(name,tagId))
        cur.close()
    
    def deleteTag(self,tagId):
        sql = """ DELETE FROM TAG where id=?"""
        cur = self.conn.cursor()
        cur.execute(sql,(tagId,))
        cur.close()
        
    def insertTag(self,name):
        tagId = self.getAvailableTagId()
        sql = """ INSERT INTO TAG (id,name) VALUES(?,?)"""
        cur = self.conn.cursor()
        cur.execute(sql,(tagId,name))
        cur.close()
    
        
    
    def getAllTags(self):
        tagList = []   
        sql = 'SELECT id, name FROM TAG'
        cur = self.conn.cursor()
        cur.execute(sql)
        for row in cur.fetchall():
            tag = Tag()
            (tag.id, tag.name) = row
            tagList.append(tag)
        
        cur.close()
        return tagList;
    
    def getTagsByPwdId(self, pwdId):
        tagList = []
        sql = """select id, name  from TAG WHERE id in (
        SELECT tagid FROM PWDTAGJOIN WHERE pwdid = ?
        ) GROUP BY id , name
        """
        cur = self.conn.cursor()
        cur.execute(sql,(pwdId,))
        for row in cur.fetchall():
            tag = Tag()
            (tag.id, tag.name) = row
            tagList.append(tag)
            
        cur.close()
        return tagList
    
    def getTagById(self, tagId):
        sql = """select id, name  from TAG WHERE id =?
        """
        cur = self.conn.cursor()
        cur.execute(sql,(tagId,))
        row = cur.fetchone()
        tag = Tag()
        (tag.id, tag.name) = row
        
            
        cur.close()
        return tag
    
    
    def getPwdCountByTagId(self, tagId):
        result = 0
        sql = """
            SELECT count(j.pwdid) from  PWDTAGJOIN j, ACCOUNT  a
                WHERE j.tagid = ?
                    AND j.pwdid = a.id
                    AND a.deleted <>1
            
            """
        cur = self.conn.cursor()
        cur.execute(sql,(tagId,))
        result = cur.fetchone()[0]
        cur.close()
        return result
    
    def removeTagFromAccount(self,tagId):
        sql=""" DELETE FROM PWDTAGJOIN WHERE tagid=?"""
        cur = self.conn.cursor()
        cur.execute(sql,(tagId,))
        cur.close()
        
    def getAvailableTagId(self):
        '''
        get the next available id
        '''
        sql = """
            SELECT max(id) from TAG
        """
        cur = self.conn.cursor()
        cur.execute(sql)
        row = cur.fetchone()[0]
        cur.close()
        return row+1 if row !=None else  1
    
    def isTagNameValid(self,name,id=-1):
        cur = self.conn.cursor()
        if id == -1 :
            sql = """  select id from TAG where name=?   """
            cur.execute(sql,(name,))
        else:
            sql =  """  select id from TAG where name=? AND id<>?   """
            cur.execute(sql,(name,id))
        row = cur.fetchone()
        cur.close()
        return True  if row ==None else  False
