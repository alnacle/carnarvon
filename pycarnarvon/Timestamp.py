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
#
"""
Module that builds an abstraction object to timestamps

@author:       Alvaro Navarro
@organization: Grupo de Sistemas y Comunicaciones, Universidad Rey Juan Carlos
@copyright:    Universidad Rey Juan Carlos (Madrid, Spain)
@license:      GNU GPL version 2 or any later version
@contact:      anavarro@gsyc.escet.urjc.es
"""

from Database import *
from Globals import *

class Timestamp:

    __times = {}

    def settimes(times,db=''):
        if times not in Timestamp.__times:
            # Add index and times 
            Timestamp.__times[times] = len(Timestamp.__times)


            query = "INSERT INTO dates (timestamp_id, timestamp) VALUES ("
            query += "'" + str(Timestamp.__times[times]) + "','" + str(times) + "');\n"
            if db != '':
                db.insertData(query)

        return(Timestamp.__times[times])

    def getid(times):
        return (Timestamp.__times[times])

    # statics methods
    settimes = staticmethod(settimes)
    getid = staticmethod(getid)

