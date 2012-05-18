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
Installer

@author:       Alvaro Navarro
@organization: Grupo de Sistemas y Comunicaciones, Universidad Rey Juan Carlos
@copyright:    Universidad Rey Juan Carlos (Madrid, Spain)
@license:      GNU GPL version 2 or any later version
@contact:      anavarro@gsyc.escet.urjc.es
"""

from distutils.core import setup
import pycarnarvon.Globals as gb

setup(name = "carnarvon",
      version = gb.Globals.version,
      author =  gb.Globals.author,
      author_email = "anavarro@gsyc.escet.urjc.es",
      maintainer =  "Gregorio Robles",
      maintainer_email = "grex@gsyc.escet.urjc.es",
      description = "A software archaeology analysis tool",
      url = "http://carnarvon.tigris.org",
      packages = ['pycarnarvon'],
      scripts = ["carnarvon", "carnarvon2web"],
      data_files = [ ("man/man1", ["man/carnarvon.1", "man/carnarvon2web.1"]),
         ("carnarvon/html", ["html/header.html", "html/index.html", "html/newstyle.css"]),
         ("carnarvon/html/images", ["html/images/background.jpg", "html/images/bg.gif", "html/images/carnarvon-logo.png"]) ] )
