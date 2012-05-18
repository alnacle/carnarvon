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
This module contains basic instructions for send mails
The code for this modules has been partially taken from
the Python documentation at
http://www.python.org/doc/lib/SMTP-example.html

@author:       Alvaro Navarro
@organization: Grupo de Sistemas y Comunicaciones, Universidad Rey Juan Carlos
@copyright:    Universidad Rey Juan Carlos (Madrid, Spain)
@license:      GNU GPL version 2 or any later version
@contact:      anavarro@gsyc.escet.urjc.es
"""

import smtplib
import string
import sys

def sendMail(fromAddress = '',
             toAddress = '',
             smtpServer = '',
             project = ''):
    """
    Sends mail announcing that the analysis process has finised
    The default values are taken from config.py

    @type  fromAddress: string
    @param fromAddress: From E-mail address
    @type  toAddress: string
    @param toAddress: To E-mail address
    @type  smtpServer: string
    @param smtpServer: SMTP server
    @type  project: string
    @param project: Name of the project (usually the database name)

    """

    fromaddr = "From: Carnarvon Administrator <carnarvon@gsyc.escet.urjc.es>"
    toaddrs  = "To: Carnarvon User <" + toAddress + ">"
    msg = "Carnarvon has finished the analysis for " + project + "\n.\n"

    try:
        server = smtplib.SMTP(smtpServer)
        server.set_debuglevel(0)
        server.sendmail(fromaddr, toaddrs, msg)
        server.quit()
    except:
        sys.stderr.write ("\n Cannot send mail: Server not available at this moment")

