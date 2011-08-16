from Crypto.Cipher import CAST
from Crypto.Hash import MD5
import binascii
import urllib2
import string, random

#algorithm
MODE = CAST.MODE_CFB

def __getKeyObject(key):
    
    obj = CAST.new(key, MODE)
    return obj

def md5Encode(txt):
    '''
    get Md5 encrypted text
    @param txt:plain text msg
    '''
    m = MD5.new()
    m.update(txt)
    s =m.hexdigest()
    return s


def getRadomString(length,optionlist=['number','lower','upper','punc']):
    charPool = {'number':  string.digits,
        'lower' : string.lowercase,
        'upper' : string.uppercase,
        'punc' : string.punctuation }
    value = ''
    pool = ''
    for key in optionlist:
        if charPool.has_key(key):
            pool = pool + charPool.get(key)
    for i in range(length):
        value = value + random.choice(pool)
    # another way: but need to do something on the length
    #value = random.sample(pool, length)
    #return string.join(value,'')
    
    return value
    
def encrypt(key, msg):    
    '''
    Encrypt Message using given password
    @param key: the password (master password)
    @param msg: plain message need to be encrypted
    '''
    obj = __getKeyObject(key)
    
    #encrypt
    after = obj.encrypt(msg)    
    #convert to string
    s = binascii.b2a_hex(after)
    
    return s


    
#msg was string, should convert into bin first    
def decrypt(key, msg):
    '''
    Decrypt message
    @param key: the password (master password)
    @param msg: encrypted message need to be decrypted
    '''
    obj = __getKeyObject(key)
    #decoding
    b = binascii.a2b_hex(msg)
    #decrypt
    after = obj.decrypt(b)
    return after

def getLatestVersion(versionUrl):
    #proxy is only for testing
#    proxy_support = urllib2.ProxyHandler({"http":"10.48.187.80:8080"})
#    opener = urllib2.build_opener(proxy_support)
#    urllib2.install_opener(opener)
    #proxy is only for testing
    
    result = ''
    try:
        f = urllib2.urlopen(versionUrl)
        s = f.read()
        f.close()
        result = s.split("#LATEST_VERSION#")[1]
    except:
        pass
    return result
    
# encrypt/decrypt file, not used

#def encryptFile(fullFileName, key, overwrite=False):
#    '''
#    encrypting a given file (path). using 'DES' algorithm. 
#    @param fullFileName: input file path
#    @param key: the key for en/decryption, 8 didgits
#    @param overwrite: if overwriting the original file. Default : No Overwriting. Creating a new file, appending ".encrypted" to original filename.    
#    
#    '''
#    # get the keyobject
#    obj = __getKeyObject(key)    
#    
#    sourceF = open(fullFileName,'r')    
#    txtList = sourceF.readlines()
#    sourceF.close()
#    
#    # target file object
#    targetF = open(fullFileName,'w') if overwrite else open(fullFileName+'.encrypted', 'w')
#    for txt in txtList:
#        targetF.write(obj.encrypt(txt))
#
#    targetF.close()
#    
#def decryptFile(fullFileName, key, overwrite=False):
#     # get the keyobject
#    obj = __getKeyObject(key)    
#    
#    sourceF = open(fullFileName,'r')    
#    txtList = sourceF.readlines()
#    sourceF.close()
#    
#    # target file object
#    targetF = open(fullFileName,'w') if overwrite else open(fullFileName+'.decrypted', 'w')
#    for txt in txtList:
#        targetF.write(obj.decrypt(txt))
#
#    targetF.close()
    



    
    
