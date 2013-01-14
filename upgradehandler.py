import shutil
import sqlite3 as sqlite
import config,util,service,dao
import os.path

def __getConnection():
    conn = sqlite.connect(config.CONN_PATH)
    return conn

def __upgrade_from_10x(conn):
    """
    if current version is 1.0.x, do this upgrade. 
    """
    sql_add_secret = """
    ALTER TABLE ACCOUNT ADD COLUMN secret TEXT

        """
    cur = conn.cursor()
    cur.execute(sql_add_secret)

    cur2 =conn.cursor()
    sql = 'select id,  username FROM ACCOUNT'
    cur.execute(sql)
    
    upsql = 'update Account set username=? where id=?'
    
    c=0
    for row in cur.fetchall():
        (id,uid) = row
        newUid=util.encrypt(config.getRootPwd() ,uid)
        cur2.execute(upsql,(newUid,id,))
        c += 1
        
        
    cur2.close()
    cur.close()
    return c

def __upgrade_from_110():
    """
    if current version is 1.1.0, do this upgrade. 
    """
    pass



def __encryptAccounts(key,conn):
    cur = conn.cursor()


def __column_exists(conn,table_name,column_name):
    sql = "PRAGMA table_info(" + table_name + ")"
    cur = conn.cursor()
    cur.execute(sql)
    result = False
    for row in cur.fetchall():
        if row[1]==column_name:
            result = True
            break
    cur.close()
    return result


def __table_exists(conn,table_name):
    sql = "PRAGMA table_info(" + table_name + ")"
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    return len(rows)>0

def upgrade():
    #root password
    key = config.getRootPwd()

    #check column "secret" in Account table. if doesn't exist, v 1.0.x
    conn = __getConnection()
    secretColumnExists=__column_exists('account','secret')
    if  not secretColumnExists:
        __upgrade_from_10x(conn)

    pass




