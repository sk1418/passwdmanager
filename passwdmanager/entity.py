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

class Passwd:
    
    def __init__(self):
       # database fields:
       self.id = 0
       self.title = ''
       self.username = ''
       self.description = ''
       self.pwd = ''
       self.secret = ''
       self.createdate=None
       self.lastupdate=None
       self.deleted=0
       self.tags = []
       
            
    def __repr__(self):
        return '\nPwdItem:\nid:%s\ntitle:%s\ndescription:%s\npwd:%s\nTags:%s\n SecretInfo:%s \n' % (self.id,self.title.encode("utf-8"),self.description.encode("utf-8"),self.pwd,self.tags,self.secret) 

        
class Tag(object):
    '''
    tags for password items
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.id = 0
        self.name = ""
        
    def eq(self,tag):
        if not tag:
            return False
        elif self.id == tag.id:
            return True
        
        
    def __repr__(self):
        return '%s' % (self.name) 
    
    
