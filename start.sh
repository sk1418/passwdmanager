#!/bin/bash
a=`dirname $0`
if [ $a = '.' ];then
   a=`pwd`
fi
current=$a
echo "current path:"$current
cd $current
python passwdManager.py
