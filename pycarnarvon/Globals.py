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
Some static data


@author:       Alvaro Navarro
@organization: Grupo de Sistemas y Comunicaciones, Universidad Rey Juan Carlos
@copyright:    Universidad Rey Juan Carlos (Madrid, Spain)
@license:      GNU GPL version 2 or any later version
@contact:      anavarro@gsyc.escet.urjc.es
"""

import sys
import os

class Globals:
    """
    Static variables with information about project
    very useful when need a value from other class
    """

    # General program metadata
    version = "0.8.5"
    author = "Alvaro Navarro"
    mail = "anavarro@gsyc.es"

    # Limit date until we make analysis
    max_date = ''

    # Maximun numbers of threads
    max_threads = 1

    # Workspace path. Should finnish with '/' character
    workspace = ''

    # Databse name
    database = ''

    # HTML Templates
    templates = ''

    # Connection string
    connection = ''

    def createdir(newdir):
        """
        works the way a good mkdir should :-)
            - already exists, silently complete
            - regular file in the way, raise an exception
            - parent directories does not exist, make them as well
        """
        if os.path.isdir(newdir):
            pass
        elif os.path.isfile(newdir):
            raise OSError("a file with the same name as the desired dir, '%s', already exists." % newdir)
        else:
            head, tail = os.path.split(newdir)
            if head and not os.path.isdir(head):
                Globals.createdir(head)
            if tail:
                os.mkdir(newdir)

    createdir = staticmethod(createdir)
