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
import ParserConfigFile as parser
import Globals as gb
import Web as wmodule


# Some stuff about the project
author = "(C) 2005,2007 %s <%s>" % (gb.Globals.author, gb.Globals.mail)
name = "carnarvon %s - Libresoft Group http://libresoft.urjc.es" % (gb.Globals.version)
credits = "\n%s \n%s\n" % (name,author)


def usage():
    print "Usage: %s [options] config_file" % (sys.argv[0])
    print """
Options:

  -h, --help               Print this usage message.
  -o, --options            Print additional posting options.

  -d, --driver             Output driver [mysql|stdout]
  -w, --no-html            Don't create html output (only graphs).
  -s, --stic-time          Modify tic space time in lines/time graph
  -r, --recursive          Generate Stats recursively (long time)
"""

def main():

    print credits

    short_opts = "hword:s:"
    long_opts = [ "help", "options", "stic-time=", "no-html", "--recursive", "driver="]

    try:
        opts, args = getopt.getopt(sys.argv[1:], short_opts, long_opts)
    except getopt.GetoptError:
        usage()
        sys.exit(1)
    
    # Default we use this config file in user $HOME
    rc_file = ''
    html_step = 1
    driver = "mysql"
    stic_time = 15
    recursive = 0
    
    if args == []:
        usage()
        sys.exit(0)

    
    # Config file comes from args
    rc_file = args[0]

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-w", "--no-html"):
            html_step = 0
        elif o in ("-d", "--driver"):
            driver = a
        elif o in ("-s", "--stic-time"):
            stic_time= int(a)
        elif o in ("-r", "--recursive"):
            recursive = 1
            
    # Parse config file
    print "[*] Reading config file: " + str(rc_file)
    rc = parser.ParserConfigFile()
    rc.read_rcfile(rc_file)

    workspace = rc.config_map['workspace']
    templates = rc.config_map['html_templates']

    gb.Globals.templates = templates

    # Create workspace
    if os.path.isdir(workspace):
        print "[*] Using workspace: " + str(workspace)
    else:
        print "[*] Creating workspace: " + str(workspace)
        gb.Globals.createdir(workspace)

    # Access Database
    user = rc.config_map['username']
    password = rc.config_map['password']
    host = rc.config_map['hostname']
    name = rc.config_map['database']

    conection =  driver + "://" + user + ":" + password + "@" + host + "/" + name
    db = dbmodule.Database(conection)
    print "[*] Using current database: " + str(name)

    # get all tables
    dates = db.get_tables()

    # generate html content of each timestamp
    ds = []
    for (d,) in dates:
        if d[0:9] == 'annotates':
            stamp = d[10:len(d)]
            ds.append(stamp)

    # generate html timestamps
    dirs = db.query("module, module_id", "directories")
    for d in ds:
        print "[*] Working on " + str(d).replace("_","/")
        total = db.query("count(*)","annotates_" + d)

        # Look if the current timestamp contains something
        if int(total[0][0]) != 0:
            print "   => Creating Stats for " + str(d)
            wstat = wmodule.WebStat(d, db, stic_time)
            wstat.generate_html(ds)
            
            if recursive:
                # Generate Directories HTML
                for (module, module_id) in dirs:
                    print "   => Creating Stats for " + str(module)
                    wstat = wmodule.WebDirStat(d, db, str(module), str(module_id), stic_time)
                    wstat.generate_html(ds)

                    # Generate Files HTML
                    files = db.query("distinct(f.file),f.file_id", "annotates_" + d + " as a, files as f", "dir_id=" + module_id + " and a.file_id = f.file_id")
                    for (file, file_id) in files:
                        print "               => Creating Stats for " + str(file)
                        wstat = wmodule.WebFileStat(d, db, file, file_id)
                        wstat.generate_html(ds)

    # Generate index html
    windex = wmodule.WebIndex()
    windex.generate_html(ds)

    db.close()

    print "\nDone! Use your web browser and open " + workspace + "index.html \n"
