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
Class that impements access and parsing to the Config file.
config file should be an ascii text written in common language
i.e: variable = value

@author:       Alvaro Navarro
@organization: Grupo de Sistemas y Comunicaciones, Universidad Rey Juan Carlos
@copyright:    Universidad Rey Juan Carlos (Madrid, Spain)
@license:      GNU GPL version 2 or any later version
@contact:      anavarro@gsyc.escet.urjc.es
"""

from datetime import datetime, timedelta
from time import gmtime, strftime

import Globals as gbmodule
import sys
import os
import time
import string
import stat

class ParserConfigFile:
    """
    Parse config file and set values for variables
    """

    def __init__(self):

        self.user_home_dir = ''

        self.bool_map = {'evolution': 1,
                         'sendmail': 1}

        self.config_map = { 'username':'',
                            'password':'',
                            'workspace':'',
                            'database':'',
                            'hostname':'',
                            'type':'',
                            'cvsroot':'',
                            'modules':'',
                            'evolution':'',
                            'frequency':'',
                            'start_date':'',
                            'max_date':'',
                            'sendmail':'',
                            'smtpserver':'',
                            'mail':'',
                            'html_templates':''}
        self.dates = []

    def get_workspace(self):
        return self.config_map['workspace']

    def get_username(self):
        return self.config_map['username']

    def get_password(self):
        return self.config_map['password']

    def get_database(self):
        return self.config_map['database']

    def get_hostname(self):
        return self.config_map['hostname']

    def get_modules(self):
        return self.config_map['modules']

    def get_repository(self):
        return self.config_map['cvsroot']

    def get_type(self):
        return self.config_map['type']

    def errmsg(self):
        "Return an error message."

        s = sys.exc_info()[1]
        if s is None:
            return "unknown error"

        return str(s)

    def check_values(self):
        "Check correct values readed from config file"

        for val in self.config_map:
            if self.config_map[val] == '':
                sys.stderr.write ("WARNING: no value found for " + str(val) + "\n")

    def read_rcfile(self,rcfile):
        "Parse rcfile wich contains the config variables"

        try:
            f = open(rcfile,'r')
        except IOError:
            msgerror  = "Unable to open rcfile '%s': %s. Exiting." % (rcfile, self.errmsg()) + "\n"
            msgerror += "Try with --automatic to create a simple config template"
            sys.exit(msgerror)

        while 1:
            line = f.readline()
            if not line:
                break
            line = line[:-1]        # discard newline character
            if line == "":          # discard blank lines
                pass
            elif line[0] == '#':    # discard comments
                pass
            else:
                rawvalue = string.split(line,'=',1)
                if len(rawvalue) < 2:
                    sys.exit("Error: invalid line, %s" % (line))
                else:
                    var_name = string.lower(string.strip(rawvalue[0]))
                    var_value = string.strip(rawvalue[1])

                    # Store value in diccionary
                    try:
                        valuekey = self.config_map[var_name]
                        self.config_map[var_name] = var_value
                    except KeyError:
                        sys.exit ("Error: invalid value in line %s" % (line))

                    # Check if variable is boolean
                    try:
                        valuebool = self.bool_map[var_name]
                        realbool = self.parse_bool(var_value)
                        if realbool == -1:
                            sys.exit ("Error: invalid value in line %s" % (line))
                            self.config_map[var_name] = realbool
                    except KeyError:
                        pass

        f.close()
        self.check_values()

        gbmodule.Globals.workspace = self.config_map['workspace']
        gbmodule.Globals.database = self.config_map['database']
        gbmodule.Globals.html_templates = self.config_map['html_templates']

    def buildstamps(self):
        """
        Look if we have evolution study
        If not, we add the current date only
        """
        if self.config_map['start_date'] == '':
            current = strftime('%Y-%m-%d')
        else:
            current = self.config_map['start_date']

        components = current.split("-")
        if len(components) <= 1:
            sys.exit("\nError in start_date format. Check your config file\n")

        year = components [0]
        month = components[1]
        day = components[2]

        x = datetime(int(year),int(month),int(day))
        d = str(x).split(" ")

        #print "[*] Calculating range of dates: "
        #print "\t* Adding " + str(str(d[0]))

        self.dates.append(str(d[0]))

        if self.parse_bool(self.config_map['evolution']):
            self.normalize_dates(x)


    def DaysMonth(self,f):
        if f.month-1 in (0,1,3,5,7,8,10,12):
            return 31
        elif f.month-1 in (4,6,9,11):
            return 30
        else:  # febrero
            if (f.year % 4) == 0 and not((f.year % 400) in (100,200,300)):
                return 29
            else:
                return 28

    def SumMonths(self,delta, ini):
        #res = ini.replace(day=1)
        res = ini
        for x in range (0,delta):
            res -= timedelta(self.DaysMonth(res))

        if ini.day > self.DaysMonth(res):
            return res.replace(day = self.DaysMonth(res))
        else:
            return res.replace(day = ini.day)

    def normalize_dates(self,start):
        """
        Get current datetime and calculate secuence of dates
        """
        #current = strftime('%d/%m/%Y')
        #components = current.split("/")

        myear = str(self.config_map['max_date']).split("-")
        if len(myear) <= 1:
            sys.exit("\nError in max_date format. Check your config file\n")

        gbmodule.Globals.max_date = self.config_map['max_date']
        x = start
        while int(x.year) >= int(myear[0]):
            x = self.SumMonths(int(self.config_map['frequency']),x)
            d = str(x).split(" ")
            #print "\t* Adding " + str(str(d[0]))
            self.dates.append(str(d[0]))

    def parse_bool(self,instr):
        "Parse a boolean string, return 0 or 1, or -1 on error."

        if instr in ("yes", "y", "true", "t", "on", "1", "si"):
            return 1
        elif instr in ("no", "n", "false", "f", "off", "0", "no"):
            return 0
        else:
            return -1

