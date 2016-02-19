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
MySQL connection implementation

@author:       Alvaro Navarro
@organization: Grupo de Sistemas y Comunicaciones, Universidad Rey Juan Carlos
@copyright:    Universidad Rey Juan Carlos (Madrid, Spain)
@license:      GNU GPL version 2 or any later version
@contact:      anavarro@gsyc.escet.urjc.es
"""

import os
import time
import sys
try:
    import _mysql
    import _mysql_exceptions
except:
    sys.exit("python MySQLdb not found! Please install first")

import Connection as cn

class ConnectionMySQL(cn.Connection):

    def __init__(self):
        self._conn = None

    def connect(self, user=None, passwd=None, host=None, db=None):
        self._conn = _mysql.connect(host, user, passwd, db)

    def execute(self, query):
        self._conn.query(query)
        return self._conn.store_result()

    def close(self):
        if self._conn != None:
            self._conn.close()

        self._conn = None

