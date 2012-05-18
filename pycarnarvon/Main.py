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
This module contains the analysis sequence used in carnavon
it is just an ordered list of the actions (usually functions
implemented in other modules) that are to be run


@author:       Alvaro Navarro
@organization: Grupo de Sistemas y Comunicaciones, Universidad Rey Juan Carlos
@copyright:    Universidad Rey Juan Carlos (Madrid, Spain)
@license:      GNU GPL version 2 or any later version
@contact:      anavarro@gsyc.escet.urjc.es
"""

import sys
import os
import time
import string
import stat
import getopt


import Database as dbmodule
import ParserConfigFile as parsermodule
import Repository as rpmodule
import Wizard as wz
import Timestamp as timemodule
import Globals as gb
import SendMail as mailmodule
import Directory as dmodule
import Functions as fmodule
import Tables


# Some stuff about the project
author = "(C) 2005-7 %s <%s>" % (gb.Globals.author, gb.Globals.mail)
name = "carnarvon %s - GSyC/Libresoft Group http://libresoft.urjc.es" % (gb.Globals.version)
credits = "\n%s \n%s\n" % (name,author)

def cprint(charname):
    if verbose:
        print charname
    else:
        pass

def usage():
    print credits
    print "Usage: %s [options] config_file" % (sys.argv[0])
    print """
Options:

  -h, --help               Print this usage message.

  -v, --verbose            Verbose output
  -d, --driver             Output driver [mysql|stdout]
  -t, --max-threads        Max number of threads [default=2]
  -w, --wizard             Create a config file step by step
  -a, --automatic          Autogenerate a basic template config file
  -r, --clean              Clean source directory after checkout
  -c, --no-checkout        Don't checkout repository automatically.
  -l, --no-log             Don't log repository automatically.
"""

def main():

    short_opts = "hvawclt:d:r"
    long_opts = [ "help", "verbose", "wizard", "automatic", "clean"
                  "no-checkout", "no-log", "max-threads=", "driver="]

    try:
        opts, args = getopt.getopt(sys.argv[1:], short_opts, long_opts)
    except getopt.GetoptError:
        usage()
        sys.exit(1)

    # Initialize of general stuff
    global verbose
    rc_file = ''
    checkout_step = 1
    log_step = 1
    clean = 0
    verbose = 0
    maxthreads = 2
    driver = "mysql"

    if args == []:
        usage()
        sys.exit(0)

    # Config file comes from args
    rc_file = args[0]

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-a", "--automatic"):
            wz.automatic_wizard(rc_file)
            sys.exit(0)
        elif o in ("-t", "--max-threads"):
            maxthreads = a
        elif o in ("-c", "--no-checkout"):
            checkout_step = 0
        elif o in ("-l", "--no-log"):
            log_step = 0
        elif o in ("-w", "--wizard"):
            wz.wizard(rc_file)
            sys.exit(0)
        elif o in ("-d", "--driver"):
            driver = a
        elif o in ("-r", "--clean"):
            clean = 1
        elif o in ("-v", "--verbose"):
            verbose = 1
            print credits

    # Parse config file
    cprint ("[*] Reading config file: " + str(rc_file))
    rc = parsermodule.ParserConfigFile()
    rc.read_rcfile(rc_file)
    rc.buildstamps()

    # Get values from config file
    workspace = rc.get_workspace()
    user = rc.get_username()
    password = rc.get_password()
    host = rc.get_hostname()
    database = rc.get_database()

    # Create workspace
    if os.path.isdir(workspace):
        cprint ("[*] Using workspace: " + str(workspace))
    else:
        cprint ("[*] Creating workspace: " + str(workspace))
        gb.Globals.createdir(workspace)

    # Access Database
    conection = driver + "://" + user + ":" + password + "@" + host + "/" + database
    gb.Globals.connection = conection
    db = dbmodule.Database(conection)

    # Create database and tables
    db.create_database()
    db.create_table('files',Tables.files)
    db.create_table('commiters',Tables.commiters)
    db.create_table('dates',Tables.dates)
    db.create_table('directories', Tables.directories)
    db.create_table('functions', Tables.functions)
    cprint ("[*] Database %s succesfully created" % (database))

    # CVS/SVN interactive
    parser = rpmodule.RepositoryFactory.create(rc.config_map['type'], maxthreads)

    parser.modules = rc.get_modules()
    parser.repository = rc.get_repository()
    parser.type = rc.get_type()

    # Main Loop. All actions should be under this 'for'
    for mydate in rc.dates:

        # create table for actual annotate timestamp
        taux = 'annotates_' + str(mydate).replace("-","_")
        db.create_table(taux, Tables.annotates)

        # Add to the Timestamp object the new reference
        timemodule.Timestamp.settimes(mydate,db)

        # Config values for checkout and create dir
        parser.src_dir = workspace + 'src_' + str(mydate)
        parser.date = mydate
        gb.Globals.createdir(workspace + 'src_' + str(mydate))

        if checkout_step:
            parser.checkout()

        # Log step in time
        if log_step:
            # blame method creates new Line objects
            cprint ("[*] Parsing logs for date: " + str(mydate))
            parser.collect()
            parser.annotate()
            print "\n"

        # clean checkout
        if clean:
            cprint ("[*] Deleting checkout ...")
            parser.clean()

        cprint ("[*] Creating index database...")
        db.create_index(taux, ["line_id","file_id","dir_id","commiter_id","revision"],"index_"+taux)

    # Directories
    dmodule.Directory.directory2sql(db)
    # Functions
    fmodule.Function.functions2sql(db)



    db.close()

    # Only if user has set send mail
    if rc.config_map['sendmail']:
        server = rc.config_map['smtpserver']
        mail = rc.config_map['mail']
        mailmodule.sendMail('carnarvon',mail, server, database)

    cprint ("\nProcess Completed! \n")
