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
Database wrapper class

@see:          File.py

@author:       Alvaro Navarro
@organization: Grupo de Sistemas y Comunicaciones, Universidad Rey Juan Carlos
@copyright:    Universidad Rey Juan Carlos (Madrid, Spain)
@license:      GNU GPL version 2 or any later version
@contact:      anavarro@gsyc.escet.urjc.es
"""

import os
import time
import sys
import getpass
import re
from ConnectionFactory import ConnectionFactory as cf

class Database:

    def __init__(self, driver):

        server = ''
        user = ''
        pwd = ''
        db = ''
        conn = ''

        # Parse and extract items from driver string
        match=re.match('([^:]*)://(.*)/([^\?]*)\?*(.*)', driver)
        if match:
            gps = match.groups()

            # Match at least with connection type
            if len(gps) >= 1:
                conn = gps[0]

            # Match at least with connection + user/pass
            if len(gps) >= 2:
                aux = gps[1]
                if aux.find('@') >= 0:
                    upwd, server = aux.split('@')
                    if aux.find(":") >= 0:
                        user, pwd = upwd.split(':')
                else:
                    if aux.find(':') >= 0:
                        user, pwd = aux.split(':')
                    else:
                        server = aux

            # Math with everything
            if len(gps) >= 3:
                db = gps[2]

        self.username = user
        self.password = pwd
        self.hostname = server
        self.database = db
        self.conn = conn

        # Create connection
        self.__connection = None
        self.__connection = cf.create_connector (conn)
        #try:
        self.__connection.connect (self.username, self.password, self.hostname, self.database)
        """
        except:
            self.create_user ()
            self.__connection.connect (self.username, self.password, self.hostname, self.database)
        """

    def connect(self, user='', password='', hostname='', database=''):
        """
        method that establishes a new database connection

        @type  user: string
        @param user: user name
        @type  password: string
        @param password: user's password
        @type  hostname: string
        @param hostname: host which contains database server
        @type  database: string
        @param database: name of the database
        """

        self.__connection.connect(self.username, self.password, self.hostname, self.database)

    def query(self, select, tables, where='', order='', group=''):
        """
        Singleton method to access the database
        Input is the query (given by several parameters)
        Output is a row (of rows)

        @type  select: string 
        x@param select: Fields to select
        @type  tables: string
        @param tables: Database tables involved in this query
        @type  where: string
        @param where: Where clause (optional; default: not used)
        @type  order: string
        @param order: Order clause (optional; default: not used)
        @type  group: string
        @param group: Group clause (optional; default: not used)
        """

        if order and where and group:
            query = "SELECT " + select + " FROM " + tables + " WHERE " + where  + " GROUP BY " + group + " ORDER BY " + order
        elif order and where:
            query = "SELECT " + select + " FROM " + tables + " WHERE " + where + " ORDER BY " + order
        elif order and group:
            query = "SELECT " + select + " FROM " + tables + " GROUP BY " + group + " ORDER BY " + order
        elif order:
            query = "SELECT " + select + " FROM " + tables + " ORDER BY " + order
        elif where:
            query = "SELECT " + select + " FROM " + tables + " WHERE " + where
        else:
            query = "SELECT " + select + " FROM " + tables


        r = self.__connection.execute(query)

        try:
            row = r.fetch_row(0)
        except AttributeError:
            sys.exit("Unknown error with mysql server")

        return row

    def close(self):
        """
        Closes actual connection
        """

        self.__connection.close()

    def get_tables(self):
        """
        Get a list of tables which start with 'annotate' prefix
        Very useful to crate graphs instead of calculate them

        return: python list with all tables
        """
        query = "SHOW TABLES"
        r = self.__connection.execute(query)

        row = r.fetch_row(0)
        tables = []
        for r in row:
            tables.append(r)

        return tables

    def create_index(self, table_name, columns, name):
        """
        Create index in a table.

        @type   table_name: string
        @param  table_name: name of the table
        @type   columns: list
        @param  columns: list of columns which will be included in the indexes
        @type   name: string
        @param  name: name of the index
        """

        sql_code = "CREATE INDEX " + name + " ON " + table_name + "("
        for column in columns:
            sql_code += column + ","

        # Extract last quote
        sql_code = sql_code[:-1] + ");\n"
        self.__connection.execute(sql_code)

        sql_code = "ANALYZE table " + table_name + ";\n"
        self.__connection.execute(sql_code)

        sql_code = "OPTIMIZE table " + table_name + ";\n"
        self.__connection.execute(sql_code)

    def create_table(self, table_name, table_format):
        """
        Creates a table.

        @type  table_name: string
        @param table_name: name of the table
        @type  table_format: dictionary
        @param table_format: key of each field is the name of the column (string).
        The value of each field is the type of each column (string).
        If key is 'Primary Key' the value of the field is the primary key of the table.
        """

        sql_code = "DROP TABLE IF EXISTS " + str(table_name) + ";\n"
        self.__connection.execute(sql_code)

        sql_code = "CREATE TABLE IF NOT EXISTS "+table_name+" (\n"
        prim_key_code = ""

        for k in table_format.keys():
            if k.lower() == "primary key":
                prim_key_code = "    PRIMARY KEY ("+table_format[k]+")\n"
            else:
                sql_code += "    "+k+" "+table_format[k]+",\n"

        if prim_key_code != "":
            sql_code += prim_key_code
        else:
            sql_code = sql_code.rstrip(",\n")+"\n"

        sql_code += ");\n\n"

        r = self.__connection.execute(sql_code)


    def create_user(self, user='', password='', hostname='', database=''):
        """
        Create User. Connection needs to have privileges
        """

        admin_user =  raw_input ("MySQL admin username: ")
        admin_password = getpass.getpass("MySQL admin password: ")

        mysqlquery  = "GRANT ALL ON "+str(self.database)
        mysqlquery += ".* TO " + str(self.username) + "@" + str(self.hostname)
        mysqlquery += " IDENTIFIED BY \""+str(self.password)+"\";\n"

        try:
            connaux = cf.create_connector(self.conn)
            connaux.connect(admin_user, admin_password, self.hostname)
            connaux.execute(mysqlquery)
            connaux.close()
            self.create_database()

        except StandardError:
            sys.exit("Error: Cannot create user")

    def create_database(self, database=''):
        """
        Try to create new database
        assumes that we have privileges to create new one 
        and try to drop database with the normal user
        """

        if database:
            name = database
        else:
            name = self.database

        try:
            co = cf.create_connector (self.conn)
            co.connect(self.username, self.password, self.hostname)

            mysqlquery = "DROP DATABASE IF EXISTS " + str(name) + ";\n"
            co.execute(mysqlquery)

            mysqlquery = "CREATE DATABASE " + str(name) + ";\n"
            co.execute(mysqlquery)
            co.close()

        except StandardError:
            sys.stderr.write ("WARNING: unable to create database. User " + self.username + " doesn't have privileges")
            self.create_user()

    def insertData(self,sqlcode):

         r = self.__connection.execute(sqlcode)

