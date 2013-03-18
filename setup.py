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

from setuptools import setup, find_packages
import glob
setup(
    name = 'passwdManager',
    version = '1.2.0',
    install_requires=[ 'wxpython>=2.8','pycrypto>=2.6' ],
    packages = find_packages(),
    data_files=[('icons',glob.glob("icons/*.*")),
            ('data',glob.glob('data/*.pmgr')),
            ('conf',glob.glob('conf/*.*')),
            ('backup',['backup/info.txt']),
            ('/usr/share/applications',['data/passwdManager.desktop']),
            ('/usr/share/pixmaps',['icons/passwdManager.png']),
        ],
    include_package_data= True,
    zip_safe=False,
    scripts=['pwmanager'],
    author='Kai Yuan',
    author_email='kent.yuan@gmail.com',
    platforms=['POSIX'],
    keywords='password security',
    description='a password management tool',
)


