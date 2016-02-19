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
Abstract class that implements the basic operations with a File.
It contains three static methods to access to the __files structure

@see:          FileCVS.py, FileSVN.py

@author:       Alvaro Navarro
@organization: Grupo de Sistemas y Comunicaciones, Universidad Rey Juan Carlos
@copyright:    Universidad Rey Juan Carlos (Madrid, Spain)
@license:      GNU GPL version 2 or any later version
@contact:      anavarro@gsyc.escet.urjc.es
"""

from threading import Thread
from Database import *
import time
import os
import string
import sys

class File:

    __files = {}

    def __init__ (self,name,timestamp, db_object):
        self.name = name
        self.timestamp = timestamp
        self.db = db_object

    @staticmethod
    def file2sql(file,db):
        if file not in File.__files:
            File.__files[file] = len(File.__files)
            query = "INSERT INTO files (file_id, file) VALUES ('"
            query += str(File.__files[file]) + "','" + str(file)  +"');\n"
            db.insertData(query)

    @staticmethod
    def getid(file):
        return (File.__files[file])

    @staticmethod
    def numfiles():
        return len(File.__files)

    def line2sql(self, data):

        fields = data.split("#")

        query  = "INSERT INTO annotates_" + str(self.timestamp).replace("-","_")
        query += " (line_id, file_id, revision, commiter_id, date, timestamp_id, iscomment, isblank, dir_id) "
        query += " VALUES ('" + fields[0] + "','"
        query += fields[1] + "','"
        query += fields[2] + "','"
        query += fields[3] + "','"
        query += fields[4] + "','"
        query += fields[5] + "','"
        query += fields[6] + "','"
        query += fields[7] + "','"
        query += fields[8] + "');\n"

        self.db.insertData(query)

    def normalize_whitespace(self, text):
        "Remove redundant whitespace from a string"

        return string.join(string.split(text), ' ')

    def lineNotAComment(self,line,flag):
        "returns if line is a comment (1) or not (0)"

        line = self.normalize_whitespace(line)

        if flag:
            if line[-2:] != '*/':
                return (1, 1)
            else:
                return (1, 0)

        if line[:2] == '/*':
            if line[-2:] == '*/':
                return (1, 0)
            else:
                return (1, 1)
        elif line[:2] == '# ':
            if line[2:7] == 'undef':
                return (0, 0)
            elif line[2:8] == 'define':
                return (0, 0)
            else:
                return (1, 0)
        elif line == '#':
            return (1, 0)
        elif line[:2] == '//':
            return (1, 0)
        elif line[:2] == '--': # ADA Comments
            return (1, 0)
        elif line[:2] == ';;':
            return (1, 0)
        else:
            return (0, 0)

    def transformIntoDateTime(self,date):
        """
        Transformation into MySQL datetime: YYYY-MM-DD HH:MM:SS
        gets DD-mmm-YY
        """

        monthList = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        year = int(date[-2:])
        month = int(monthList.index(date[3:-3])) + 1
        day = date[:2]

        if year < 80:
            year = 2000 + year
        else:
            year = 1900 + year

        if month < 10:
            month = '0' + str(month)
        else:
            month = str(month)

        date = str(year) + '-' + month + '-' + day + ' 00:00:00'

        return date

    def analyse(self):
        pass

