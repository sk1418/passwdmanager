from setuptools import setup, find_packages
import glob
setup(
    name = 'passwdManager',
    version = '1.2.0',
    install_requires='wxpython',
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

