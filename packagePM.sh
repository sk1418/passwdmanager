#! /bin/bash
version=1.1.0
hg archive --exclude "data/init.sql" /tmp/passwdManager$version
cd /tmp
tar -cvzf /tmp/pm$version.tar.gz passwdManager$version
