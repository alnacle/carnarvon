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
SQL Tables

@author:       Alvaro Navarro
@organization: Grupo de Sistemas y Comunicaciones, Universidad Rey Juan Carlos
@copyright:    Universidad Rey Juan Carlos (Madrid, Spain)
@license:      GNU GPL version 2 or any later version
@contact:      anavarro@gsyc.escet.urjc.es
"""

dates = {'timestamp_id':'int(8) NOT NULL',
         'timestamp':'datetime',
         'primary key':'timestamp_id'}

annotates = {'line_id':'int(8) NOT NULL',
             'file_id':'int(8) NOT NULL',
             'timestamp_id':'int(8) NOT NULL',
             'revision':'varchar(10) NOT NULL',
             'commiter_id':'int(8) NOT NULL',
             'date':'datetime',
             'iscomment':'int(1)',
             'dir_id':'int(8)',
             'primary key':'line_id,timestamp_id,file_id'}


files = {'file_id':'int(8) unsigned NOT NULL',
         'file':'varchar(128)',
         'primary key':'file_id'}

commiters = {'commiter_id':'int(8) unsigned NOT NULL',
             'commiter':'varchar(20)',
             'primary key':'commiter_id'}

directories = { 'module_id': 'int(8) NOT NULL',
                'module': 'varchar(64) NOT NULL',
                'lft':'int(8) NOT NULL',
                'rgt':'int(8) NOT NULL',
                'father_dir': 'int(8) NOT NULL',
                'primary key': 'module_id'}

functions = {'function_id': 'int(8) NOT NULL',
             'name':'varchar(128) NOT NULL',
             'file_id': 'int(8) NOT NULL',
             'start_line':'int(8) NOT NULL',
             'end_line':'int(8) NOT NULL',
             'primary key':'function_id'}

