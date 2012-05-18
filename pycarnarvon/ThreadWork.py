# Copyright (C) 2006 Alvaro Navarro Clemente
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Authors : Alvaro Navarro <anavarro@gsyc.escet.urjc.es>

"""
Threads implementation

@author:       Alvaro Navarro
@organization: Grupo de Sistemas y Comunicaciones, Universidad Rey Juan Carlos
@copyright:    Universidad Rey Juan Carlos (Madrid, Spain)
@license:      GNU GPL version 2 or any later version
@contact:      anavarro@gsyc.escet.urjc.es
"""

from threading import Thread

import time
import os
import string

import FileCVS as fcvs
import FileSVN as fsvn

# Clase herencia de thread
class ThreadWork(Thread):

    def __init__ (self, files, timestamp,type, db_object, src_dir):
        Thread.__init__(self)
        self.files = files
        self.timestamp = timestamp
        self.type = type
        self.db = db_object
        self.src_dir = src_dir

    def run(self):
        for f in self.files:
            if self.type.upper() == "CVS":
                myfile = fcvs.FileCVS(f,self.timestamp,self.db, self.src_dir)
                myfile.analyse()
            if self.type.upper() == "SVN":
                myfile = fsvn.FileSVN(f,self.timestamp,self.db, self.src_dir)
                myfile.analyse()


