# PasswdManager -- Password management tool
# Copyright (C) 2009 -- 2013 Kai Yuan <kent.yuan@gmail.com>
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

import shutil
import datetime
import sqlite3 as sqlite
import passwdmanager.config as config
import passwdmanager.util as util
import passwdmanager.service as service
import passwdmanager.dao as dao
import os.path
import re

def __getConnection():
    """
    get database connection
    """
    conn = sqlite.connect(config.CONN_PATH)
    return conn

def export():
    """
    do the export logic
    """
    msg  = '' #return value
    conn = __getConnection()
    #root password
    key  = config.getRootPwd()


    sql = 'select title,  username,password, secret, description FROM ACCOUNT'
    cur = conn.cursor()
    cur.execute(sql)

    lines = []
    for row in cur.fetchall():
        (title,uid,pwd,secret,description) = row
        #decrypt
        title = '"' + title
        if secret:
            secret = util.decrypt(key, secret)
        uid = util.decrypt(key, uid)
        pwd = util.decrypt(key, pwd)
        note = description + u"\\n>>>>>>>>>>>>>>>>>>>>>>\\n" + secret + u'"'
        note = re.sub("\n|\r","\\n",note)
        lines.append(u'","'.join((title,uid,pwd,u"",note)))
    cur.close()
    # print re.sub(r"\\u([a-f0-9]{4})", lambda mg: unichr(int(mg.group(1), 16)), lines.__repr__())

    print "\n".join(lines)
    # with open(os.path.join(os.getenv("HOME") , ".passwdManager" + "/export.csv") ,'w') as f:
        # f.writelines(lines)
