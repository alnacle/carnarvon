#Copyright (C) 2006 Alvaro Navarro Clemente
#
#This program is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 2 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU Library General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
#Authors : Alvaro Navarro <anavarro@gsyc.escet.urjc.es>

"""
Commiter class that implements actions with commiter
information parserd from repository

@author:       Alvaro Navarro
@organization: Grupo de Sistemas y Comunicaciones, Universidad Rey Juan Carlos
@copyright:    Universidad Rey Juan Carlos (Madrid, Spain)
@license:      GNU GPL version 2 or any later version
@contact:      anavarro@gsyc.escet.urjc.es
"""
import threading
from Database import *

class Commiter:

    __commiters = {}
    m = threading.Lock()

    def setcommiter(commiter,db):
        Commiter.m.acquire()
        if commiter not in Commiter.__commiters:
            Commiter.__commiters[commiter] = len(Commiter.__commiters)
            query = "INSERT INTO commiters (commiter_id, commiter) VALUES ("
            query += "'" + str(Commiter.__commiters[commiter]) + "','" + str(commiter) + "');\n"
            db.insertData(query)
        Commiter.m.release()

        return(Commiter.__commiters[commiter])

    setcommiter = staticmethod(setcommiter)
