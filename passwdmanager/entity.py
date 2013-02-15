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
    
    
