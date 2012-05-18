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
Basic wizard and automatic wizard in order to make
easy config files

@see:          Repository.py, RepositorySVN.py
@author:       Alvaro Navarro
@organization: Grupo de Sistemas y Comunicaciones, Universidad Rey Juan Carlos
@copyright:    Universidad Rey Juan Carlos (Madrid, Spain)
@license:      GNU GPL version 2 or any later version
@contact:      anavarro@gsyc.escet.urjc.es
"""

import os
import sys
import getpass
from time import gmtime, strftime

def wizard(filename):
    """
    Shows a wizard in order to create a new config file step by step
    """

    #file = "./" + filename

    overwrite = "yes"
    if os.path.isfile(filename):
        overwrite = raw_input("WARNING! File " + filename + " already exists! Overwrite? (yes/no) [yes]: ")

    if overwrite == "no":
        sys.exit()

    # Config_repository_type
    sys.stdout.write("Type of repository? (cvs/svn) [default=cvs]")
    repository_type = raw_input(" : ")
    if repository_type == "":
        repository_type = "cvs"
    else:
        repository_type = "svn"

    modules = ""
    if (repository_type == "cvs"):
        sys.stdout.write("Repository parameters? (:pserver:anonymous@proyect:/path/to/cvs)")
        repository = raw_input(" : ")
        sys.stdout.write("What module do you want to study? [default = '.']")
        modules = raw_input(" : ")
        if modules == "":
                modules = ['.']
    else:
        sys.stdout.write("Repository path? (svn:// or http://. 'trunk' branch recommended!)")
        repository = raw_input(" : ")

    # Database Config
    print "\ncarnarvon stores results in a MySQL Database. Let's configure it..\n"

    sys.stdout.write("MySQL database name?")
    project_name = raw_input(" : ")

    sys.stdout.write("MySQL user name?")
    dbuser = raw_input(" : ")

    #sys.stdout.write("MySQL user password?")
    #dbpass = raw_input(" : ")

    dbpass = getpass.getpass("MySQL user password?")

    sys.stdout.write("MySQL hostname? [localhost]")
    dbhost = raw_input(" : ")
    if dbhost == "":
        dbhost = "localhost"

    print "\nOk! Don't forget to create the database using following instructions:"
    print "CREATE DATABASE " + str(project_name) + ";"
    print "GRANT ALL ON " + str(project_name) + ".* TO " + str(dbuser)+ "@" + str(dbhost) +" IDENTIFIED BY '" + str(dbpass) + "';\n\n"

    print "\nCarnarvon requires a directory to download source code, store logs and more..\n"

    sys.stdout.write("Where do you want to store the results? (absolute path without final '/')")
    workspace = raw_input(" : ")

    sys.stdout.write("\nDo you want to perform an evolutionary study? [default=no]")
    evolution = raw_input(" : ")

    current = str(strftime('%Y-%m-%d'))

    if evolution == "yes":
        start_date = current
        sys.stdout.write("Date for first analysis, most current (year-month-dat format) [default=" + current + "]")
        start_date = raw_input(" : ")
        if start_date == "":
            start_date = current

        sys.stdout.write("Date for last analysis, first one chronologically (year-month-day format)")
        end_date = raw_input(" : ")
        sys.stdout.write("Frecuency of the analysis (in months)")
        frecuency = raw_input(" : ")
    else:
        evolution = "no"
        start_date = current
        frecuency = "12"
        end_date = "1995-01-01"

    sys.stdout.write("\nDo you want Carnarvon to send you an mail when finnished? [default=no]")
    sendmail = raw_input(" : ")
    if sendmail == "yes":
        sys.stdout.write("SMTP server (relay)")
        smtpserver = raw_input(" : ")
        sys.stdout.write("E-mail address?")
        mail = raw_input(" : ")
    else:
        sendmail = "no"
        smtpserver = "localhost"
        mail = "user@localhost"

    write_wizard(filename, dbuser, dbpass, dbhost, project_name, workspace, repository_type, repository, modules, start_date, evolution,frecuency, end_date, sendmail, smtpserver, mail)

def automatic_wizard(filename):
    """
    Create a new config file in user $HOME
    """

    user_home_dir = os.environ['HOME']
    modules = ""
    file = "./" + filename

    if os.path.isfile(file):
        overwrite = raw_input("WARNING! File " + file + " already exists! Overwrite? (yes/no) [yes]: ")

    workspace = user_home_dir + "/myproject/"
    cvsroot = ":pserver:user@cvs.server.org/cvs"
    current = str(strftime('%Y-%m-%d'))

    write_wizard(file, "operator", "operator", "localhost", "myproject", workspace, "cvs", cvsroot, "module", current, "no", "1995-01-01", "4", "no", "localhost", "user@localhost")

def write_wizard(filename,
                     username='',
                     password='',
                     hostname='',
                     database='',
                     workspace='',
                     type='',
                     cvsroot='',
                     modules='',
                     start_date='',
                     evolution='',
                     frecuency='',
                     max_date='',
                     sendmail = '',
                     smtpserver = '',
                     mail = ''
                     ):

    config = open(filename, 'w')
    config.write("# Config file created automatically. Please adjust your preferences!\n\n")
    config.write("# MySQL user/password \n")
    config.write("username = " + str(username) + "\n")
    config.write("password = " + str(password) + "\n")
    config.write("hostname = " + str(hostname) + "\n\n")
    config.write("# MySQL Database name\n")
    config.write("database = " + str(database) + "\n\n")
    config.write("# Directory where sources, logs and graphs are stored. Should finnish with '/'\n")
    config.write("workspace = " + str(workspace) + "\n\n")
    config.write("# Type of repository\n")
    config.write("type = " + str(type) + "\n")
    config.write("# Repository URL\n")
    config.write("# cvs: pserver or ext\n")
    config.write("# svn: svn:// or http://\n")
    config.write("cvsroot = " + str(cvsroot) + "\n")
    config.write("# Modules: (only required for CVS)\n")
    config.write("modules = " + str(modules) + "\n\n")
    config.write("# Starting date of analysis (default is current date). year-month-day format\n")
    config.write("start_date = " + str(start_date) + "\n\n")
    config.write("# Evolutionary analysis?\n")
    config.write("evolution = " + str(evolution) + "\n")
    config.write("# Frequency (in months) - only required if evolution is yes)\n")
    config.write("frequency = " + str(frecuency) + "\n")
    config.write("# Oldest date to analyze in year-month-day format (only for evolutionary study)\n")
    config.write("max_date = " + str(max_date) + "\n\n")
    config.write("# E-Mail configuration\n")
    config.write("smtpserver = " + str(smtpserver) + "\n")
    config.write("# Your e-mail address\n")
    config.write("mail = " + str(mail) + "\n")
    config.write("# HTML templates\n")
    config.write("html_templates = \"\"" + "\n")
    config.close()

    print "\nconfig file created in " + filename +". Please, edit it and adjust your preferences\n"
