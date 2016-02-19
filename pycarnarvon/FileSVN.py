
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
Class that implements SVN File. Extends from File

@see:          File.py

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
import sys

import Commiter as cmodule
import File as fmodule
import Timestamp as tmodule
import Directory as dmodule
import Functions as fnmodule

class FileSVN(fmodule.File):

    def __init__ (self,name,timestamp,db_object, src_dir):

        self.name = name
        self.timestamp = timestamp
        self.src_dir = src_dir
        self.db_object = db_object
        fmodule.File.__init__(self, name, timestamp, db_object)

    def analyse(self):
        aux = self.name.split("/")
        root = string.join(aux[:-1],"/")
        f = aux[-1]

        try:
            os.chdir(root)
        except:
            sys.exit("Cannot change to : " + str(root))

        comment = 0
        inComment = 0
        line_id = 0
        iscomment = 0

        sys.stderr.write (root + "/" + str(f) + '\n')

        i,o,e = os.popen3('svn annotate --revision {' + str(self.timestamp) + '} ' + ' ' + str(f) + ' --verbose')

        time_id = tmodule.Timestamp.getid(self.timestamp)
        file_id = fmodule.File.getid(self.name[len(self.src_dir):])
        dir_id  = dmodule.Directory.get_id(root[len(self.src_dir):])

        # Only extract functions for C files
        ext = f.split('.')[-1]
        if (ext == "c") or (ext == "cpp"):
            func = fnmodule.Function(str(root) + "/" + f, file_id)

        while 1:
            line = o.readline()
            isblank = 0
            if not line: break
            else:
                list = line[:-1].split()
                if len(list) == 9:
                    isblank = 1
                if len(list) > 2:
                    (comment, inComment) = self.lineNotAComment(' '.join(list[9:]), inComment)
                if not comment and not inComment:
                    iscomment = 0
                else:
                    iscomment = 1

                try:
                    date = list[2] + ' ' + list[3]
                    revision = list[0]
                    try:
                        commiter_id = cmodule.Commiter.setcommiter(list[1],self.db_object)
                    except IndexError:
                        # Error because log doesn't contain commiter
                        commiter_id = -1

                    # Better than passing many arguments
                    # Add a '#' character between elements which can be parsed later.
                    aux = str(line_id) + "#" + str(file_id)
                    aux += "#" + str(revision) + "#" + str(commiter_id)
                    aux += "#" + str(date) + "#" + str(time_id) + "#" + str(iscomment) + "#" + str(isblank) + "#"  + str(dir_id)
                    self.line2sql(aux)

                    line_id += 1

                except ValueError:
                    print "Ops! Something went bad while parsing: {}".format(e)
