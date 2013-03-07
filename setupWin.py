# PasswdManager -- Password management tool
# Copyright (C) 2008 -- 2013 Kai Yuan <kent.yuan@gmail.com>
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

from distutils.core import setup
import glob
import py2exe

setup(windows=[{"script":"pwmanager","icon_resources":[(1,"icons/pm.ico")]}], 
      data_files=[("data",glob.glob("data/*.*")),
                  ("icons",glob.glob("icons/*.png")),
                  ("conf",glob.glob("conf/*.*")),
                  ("backup",glob.glob("backup/*.*")),
                  ] 
      )
