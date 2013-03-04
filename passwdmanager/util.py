# -*- coding:utf-8 -*-
from Crypto.Cipher import CAST
from Crypto.Hash import MD5
from Crypto import Random
import binascii
import urllib2
import string, random
import os,sys
import shutil, datetime
import config
import glob


#algorithm
MODE = CAST.MODE_CFB

def __getKeyObject(key, iv):
    global MODE
    cipher = CAST.new(key, MODE, iv)
    return cipher

def md5Encode(txt):
    '''
    get Md5 encrypted text
    @param txt:plain text msg
    '''
    m = MD5.new()
    m.update(txt)
    s =m.hexdigest()
    return s


def isWindows():
    """check if the application is running on Windows"""
    return sys.platform.upper().startswith('WIN')




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
    iv =Random.new().read(CAST.block_size)
    cipher = __getKeyObject(key,iv)
    #encrypt
    after = cipher.encrypt(iv+msg.encode('utf-8'))    
    #convert to string
    s = binascii.b2a_hex(after).upper()
    return s

    
def decrypt(key, msg):
    '''
    Decrypt message
    @param key: the password (master password)
    @param msg: encrypted message need to be decrypted
    '''
    #decoding, msg was string, should convert into bin first    
    encrypted_msg   = binascii.a2b_hex(msg)
    eiv = encrypted_msg[:CAST.block_size]

    ciphertext = encrypted_msg[CAST.block_size:]
    cipher = __getKeyObject(key,eiv)
    #decrypt
    plain = cipher.decrypt(ciphertext).decode('utf-8')

    return plain

def reencrypt_with_pycrp26(key,ct):
    """
        decrypt and re-encrypt with pycrypto2.6 library
        used only for upgrading from 1.1.0 or 1.0.x
    """
    global MODE
    oiv="\x00\x00\x00\x00\x00\x00\x00\x00"
    ocipher = __getKeyObject(key,oiv)
    old_msg = binascii.a2b_hex(ct)
    plaintext = ocipher.decrypt(old_msg)

    iv = Random.new().read(CAST.block_size)
    cipher = __getKeyObject(key,iv)
    msg = cipher.encrypt(iv+plaintext)
    newEncrypted = binascii.b2a_hex(msg).upper()
    return newEncrypted


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
    
def backupDB():
    """
    backup data file to backup DIR
    """
    #do file coping
    src = config.CONN_PATH
    srcfn = os.path.basename(src)
    targetfn = srcfn+"_"+ datetime.datetime.now().strftime('%Y%m%d%H%M%S') + ".bak"
    backupDB_with_fn(targetfn)

    #check backup size, if reached, delete the oldest backup
    flist = glob.glob(os.path.join(config.BACKUP_DIR,"*.bak"))
    flist.sort()
    if flist and len(flist) >= config.BACKUP_SIZE:
        map(lambda x: os.remove(x), flist[0:-config.BACKUP_SIZE])


    

def backupDB_with_fn(dest_filename):
    src = config.CONN_PATH
    dest = config.BACKUP_DIR
    destFile = os.path.join(dest,dest_filename)
    shutil.copy(src, destFile)
