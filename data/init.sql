/*********************************
 * Table RootPassword
 *********************************/
CREATE TABLE ROOTPASSWORD ( 
    md5String TEXT(700) NOT NULL 
    );



/*********************************
 * TABLE Account
 *********************************/
CREATE TABLE ACCOUNT  (
        id INTEGER NOT NULL,
        title TEXT NOT NULL,
        username TEXT,
        description TEXT,
        secret TEXT,
        password TEXT NOT NULL,
        deleted INTEGER DEFAULT 0,
        createdate DATETIME,
		lastupdate DATETIME,
        PRIMARY KEY (id),
        CONSTRAINT ix1 UNIQUE (title)
    );

/*********************************
 * TABLE TAG
 *********************************/
CREATE TABLE TAG (
    id INTEGER NOT NULL, 
    name TEXT(200) NOT NULL, 
    PRIMARY KEY (id) 
    );


/*********************************
 * TABLE PWDTAGJOIN
 *********************************/
CREATE TABLE PWDTAGJOIN    (
        tagid INTEGER NOT NULL,
        pwdid INTEGER NOT NULL,
        CONSTRAINT fktag FOREIGN KEY (tagid) REFERENCES TAG(id)
        CONSTRAINT fkpwd FOREIGN KEY (pwdid) REFERENCES ACCOUNT(id)
    );
    
/*********************************
 * Initial Data
 *********************************/

-- Favorite Tag 
INSERT INTO TAG (id,name) VALUES (0,'Favorite');
INSERT INTO TAG (id,name) VALUES (1,'Bank');
INSERT INTO TAG (id,name) VALUES (2,'Website');

-- Default root password: 'password'
INSERT INTO ROOTPASSWORD(md5String) VALUES ('5f4dcc3b5aa765d61d8327deb882cf99') 

