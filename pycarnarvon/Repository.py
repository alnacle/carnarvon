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
Abastract class that implements basic methods to work with
repositories

@author:       Alvaro Navarro
@organization: Grupo de Sistemas y Comunicaciones, Universidad Rey Juan Carlos
@copyright:    Universidad Rey Juan Carlos (Madrid, Spain)
@license:      GNU GPL version 2 or any later version
@contact:      anavarro@gsyc.escet.urjc.es
"""

import os
import sys
import threading

import Database as dbmodule
import ThreadWork as twmodule
import File as fmodule
import Globals as gbmodule
import Directory as dmodule
import Functions as fnmodule
from ConfigFiles import *


class RepositoryFactory:
    """
    Basic Factory that abastracts the process to create new repositories
    """
    def create(type, nthreads):
        if type.upper() == "CVS":
            return RepositoryCVS(nthreads)
        if type.upper() == "SVN":
            return RepositorySVN(nthreads)

    # We make it static
    create = staticmethod(create)


class Repository:
    """
    Generic class with basic information
    """

    def __init__(self):
        self.src_dir = ''
        self.repository = ''
        self.type = ''
        self.maxfiles = []
        self.maxthreads = None
        self.date = ''

    def checkout(self):
        pass

    def collect(self):
        """
        Collect a set of files 
        """

        # collect the set of files that we are going to analize
        if self.src_dir == '':
            sys.exit("ERROR: source dir empty! Maybe you forget checkout step?")
        else:
            self.maxfiles = []
            # Create new connection in order to add files
            db = dbmodule.Database(gbmodule.Globals.connection)
            for root, dirs, files in os.walk(self.src_dir):
                for file in files:
                    if analyseFile(file) == 'code':
                        # Path to analyze
                        real_path = str(root[len(self.src_dir):])
                        self.maxfiles.append(root + "/" + file)
                        # file to obtain file_id
                        subdirs = real_path.split("/")
                        aux = ""
                        for sd in subdirs[1:]:
                            aux += "/" + sd
                            dmodule.Directory.add_directory(aux)
                        fmodule.File.file2sql(real_path + "/" + file, db)

        # create a progressbar object with max = total files collected
        total = len(self.maxfiles)
        #print "[*] Files in this timestamp: " + str(len(self.maxfiles))
        #print "[*] Files total: " + str(fmodule.File.numfiles())

    def annotate(self):
        """
        CVS annotate function. Reads file log and returns its content
        """
        t = str(self.date).split(" ")
        timestamp = t[0]

        total = len(self.maxfiles)

        parserlist = []

        # quotas for each thread
        quota = int(total) / int(self.maxthreads)
        min = 0
        if int(total) < self.maxthreads:
            max = int(total)
        else:
            max = quota

        # run n threads
        for n in range(int(self.maxthreads)):

            # New object database for each thread
            db = dbmodule.Database(gbmodule.Globals.connection)

            current = twmodule.ThreadWork(self.maxfiles[min:max],timestamp, self.type, db, self.src_dir)

            parserlist.append(current)
            current.start()

            # modify index values
            min = max
            if max + quota >= len(self.maxfiles):
                max = len(self.maxfiles)
            else:
                max = min + quota

        # Wait for the rest of threads
        for parse in parserlist:
            parse.join()

    def clean(self):
        """
        Delete checkout directory

        @param type: string
        @param dir: directory with checkout
        """
        try:
            import shutil
            shutil.rmtree(self.src_dir)
        except:
            sys.stderr.write ("WARNING: unable to delete checkout directory")

class RepositoryCVS(Repository):
    """
    Child Class that implements CVS Repository basic access
    """
    def __init__(self,nthreads):
        Repository.__init__(self)
        self.modules = ''   # list
        self.maxthreads = nthreads
        self.type = "CVS"

    def checkout(self):
        """
        CVS Checkout
        """

        os.chdir(self.src_dir);

        os.system ('/usr/bin/cvs -d ' + self.repository + ' co -D"' + str(self.date) + '" ' + self.modules)

class RepositorySVN(Repository):
    """
    Child Class that implements SVN Repository basic access
    """

    def __init__(self, nthreads):
        Repository.__init__(self)
        self.maxthreads = nthreads
        self.type = "SVN"

    def checkout(self):
        """
        SVN Checkout
        """
        os.chdir(self.src_dir);

        os.system('svn co --revision {' + str(self.date) + '} ' +  self.repository)
