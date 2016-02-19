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
Class that implements CVS File. Extends from File

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

import File as fmodule
import Commiter as cmodule
import Timestamp as tmodule
import Globals as gbmodule
import Directory as dmodule
import Functions as fnmodule

class FileCVS(fmodule.File):

    def __init__ (self,name,timestamp, db_object, src_dir):
        self.name = name
        self.timestamp = timestamp
        self.src_dir = src_dir
        self.db_object = db_object
        fmodule.File.__init__(self,name,timestamp,db_object)

    def reportBug(self, invalid_id, file, date):
        """
        write error output when a file contains a line with an
        incorrect line
        """
        log_dir = os.path.join(Globals.workspace, "error_", str(self.timestamp).replace("-","_"))
        file_name = file[len(self.src_dir):]
        gbmodule.Globals.createdir(log_dir)
        output = open(log_dir + '/' + str(file_name).replace("/","_") + '.dat', 'a')
        output.write("Error #" + str(invalid_id) + ": " + date + " is not correct\n")
        output.close()

    def checkdate(self,d):
        """
        Check a date to belongs between timestamp and max_date
        Return: boolean
        """
        valid = 1

        min_date = str(Globals.max_date)
        max_date = str(self.timestamp)
        act_date = self.transformIntoDateTime(str(d))

        # Only actual_date from log file, has 00:00:00 format, so
        # we need to normalize that
        min = time.strptime(min_date + " 00:00:00", "%Y-%m-%d %H:%M:%S")
        max = time.strptime(max_date + " 00:00:00", "%Y-%m-%d %H:%M:%S")
        act = time.strptime(act_date, "%Y-%m-%d %H:%M:%S")

        if (act < min) or (act > max):
            valid = 0

        return valid

    def analyse(self):
        aux = self.name.split("/")
        root = string.join(aux[:-1],"/")
        f = aux[-1]
        ext = f.split('.')[-1]

        try:
            os.chdir(root)
        except:
            sys.exit("Cannot change to " + str(root))

        comment = 0
        inComment = 0
        line_id = 1
        invalids = 0
        iscomment = 0

        sys.stderr.write (root[len(self.src_dir):] + "/" + str(f) + "\n")

        annotate = os.popen3('cvs annotate -D"' + str(self.timestamp) + '"' + ' ' + str(f))

        # Obtain index from static classes
        time_id = tmodule.Timestamp.getid(self.timestamp)
        file_id = fmodule.File.getid(self.name[len(self.src_dir):])
        dir_id  = dmodule.Directory.get_id(root[len(self.src_dir):])

        # Only extract functions for C files
        if (ext == "c") or (ext == "cpp"):
            func = fnmodule.Function(str(root) + "/" + f, file_id)

        while 1:
            line = annotate[1].readline()
            isblank = 0
            if not line: break
            elif line[:16] == 'Annotation for ':
                pass
            elif line[:15] == '***************':
                pass
            else:
                alist = line[:-1].split()
                if len(alist) == 3:
                    isblank = 1
                if len(alist) > 3:
                    (comment, inComment) = self.lineNotAComment(' '.join(alist[3:]).strip(), inComment)
                    if not comment and not inComment:
                        iscomment = 0
                    else:
                        iscomment = 1
                try:
                    # Extract date, revision from log
                    date = alist[2][:-2]
                    date = self.transformIntoDateTime(alist[2][:-2])
                    revision = alist[0]

                    commiter_id = cmodule.Commiter.setcommiter(alist[1][1:], self.db_object)

                    # Better than pass few many arguments
                    # Add a '#' character between elements which can be parser later.
                    aux = str(line_id) + "#" + str(file_id)
                    aux += "#" + str(revision) + "#" + str(commiter_id)
                    aux += "#" + str(date) + "#" + str(time_id) + "#" + str(iscomment) + "#" + str(isblank) + "#" + str(dir_id)
                    self.line2sql(aux)

                    line_id += 1

                except ValueError as e:
                    print "Ops! Something went bad while parsing: {}".format(e)

