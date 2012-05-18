# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006 Alvaro Navarro Clemente
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
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
This modules contains configuration parameters regarding filetypes
(documentation, develompent, sound, images...)

@author:       Alvaro Navarro
@organization: Grupo de Sistemas y Comunicaciones, Universidad Rey Juan Carlos
@copyright:    Universidad Rey Juan Carlos (Madrid, Spain)
@license:      GNU GPL version 2 or any later version
@contact:      anavarro@gsyc.escet.urjc.es
"""

import re

# Code files (headers and the like included)
# (most common languages first)

config_files_code = [
    re.compile('\.c$'), # C 
    re.compile('\.pc$'), # C
    re.compile('\.ec$'), # C
    re.compile('\.ecp$'), # C
    re.compile('\.C$'), # C++
    re.compile('\.cpp$'), # C++
    re.compile('\.c\+\+$'), # C++
    re.compile('\.cxx$'), # C++
    re.compile('\.cc$'), # C++
    re.compile('\.pcc$'), # C++
    re.compile('\.cpy$'), # C++
    re.compile('\.h$'), # C or C++ header
    re.compile('\.hh$'), # C++ header
    re.compile('\.hpp$'), # C++ header
    re.compile('\.hxx$'), # C++ header
    re.compile('\.sh$'), # Shell
    re.compile('\.pl$'), # Perl
    re.compile('\.pm$'), # Perl
    re.compile('\.pod$'), # Perl
    re.compile('\.perl$'), # Perl
    re.compile('\.cgi$'), # CGI
    re.compile('\.php$'), # PHP
    re.compile('\.php3$'), # PHP
    re.compile('\.php4$'), # PHP
    re.compile('\.inc$'), # PHP
    re.compile('\.py$'), # Python
    re.compile('\.java$'), # Java
    re.compile('\.class$'), # Java Class (or at least a class in some OOPL)
    re.compile('\.ada$'), # ADA
    re.compile('\.ads$'), # ADA
    re.compile('\.adb$'), # ADA
    re.compile('\.pad$'), # ADA
    re.compile('\.s$'), # Assembly
    re.compile('\.S$'), # Assembly
    re.compile('\.asm$'), # Assembly
    re.compile('\.awk$'), # awk
    re.compile('\.cs$'), # C#
    re.compile('\.csh$'), # CShell (including tcsh)
    re.compile('\.cob$'), # COBOL
    re.compile('\.cbl$'), # COBOL
    re.compile('\.COB$'), # COBOL
    re.compile('\.CBL$'), # COBOL
    re.compile('\.exp$'), # Expect
    re.compile('\.l$'), # (F)lex
    re.compile('\.ll$'), # (F)lex
    re.compile('\.lex$'), # (F)lex
    re.compile('\.f$'), # Fortran
    re.compile('\.f77$'), # Fortran
    re.compile('\.F$'), # Fortran
    re.compile('\.hs$'), # Haskell
    re.compile('\.lhs$'), # Not preprocessed Haskell
    re.compile('\.el$'), # LISP (including Scheme)
    re.compile('\.scm$'), # LISP (including Scheme)
    re.compile('\.lsp$'), # LISP (including Scheme)
    re.compile('\.jl$'), # LISP (including Scheme)
    re.compile('\.ml$'), # ML
    re.compile('\.ml3$'), # ML
    re.compile('\.m3$'), # Modula3
    re.compile('\.i3$'), # Modula3
    re.compile('\.m$'), # Objective-C
    re.compile('\.p$'), # Pascal
    re.compile('\.pas$'), # Pascal
    re.compile('\.rb$'), # Ruby
    re.compile('\.sed$'), # sed
    re.compile('\.tcl$'), # TCL
    re.compile('\.tk$'), # TCL
    re.compile('\.itk$'), # TCL
    re.compile('\.y$'), # Yacc
    re.compile('\.yy$'), # Yacc
    re.compile('\.idl$'), # CORBA IDL
    re.compile('\.gnorba$'), # GNOME CORBA IDL
    re.compile('\.oafinfo$'), # GNOME OAF
    re.compile('\.mcopclass$'), # MCOP IDL compiler generated class
    re.compile('\.autoforms$'), # Autoform
    re.compile('\.atf$'), # Autoform
    re.compile('\.gnuplot$'),
    re.compile('\.xs$'), # Shared library? Seen a lot of them in gnome-perl
    re.compile('\.js$'), # JavaScript (and who knows, maybe more)
    re.compile('\.patch$'),
    re.compile('\.diff$'), # Sometimes patches appear this way
    re.compile('\.ids$'), # Not really sure what this means
    #re.compile('\.upd$'), # ���??? (from Kcontrol)
    re.compile('$.ad$'),  # ���??? (from Kdisplay and mc)
    re.compile('$.i$'), # Appears in the kbindings for Qt
    re.compile('$.pri$'), # from Qt
    re.compile('\.schema$'), # Not really sure what this means
    re.compile('\.fd$'), # Something to do with latex
    re.compile('\.cls$'), # Something to do with latex
    re.compile('\.pro$'), # Postscript generation
    re.compile('\.ppd$'), # PDF generation
    re.compile('\.dlg$'), # Not really sure what this means
    re.compile('\.plugin$'), # Plug-in file
    re.compile('\.dsp'), # Microsoft Developer Studio Project File
    re.compile('\.vim$'), # vim syntax file
    re.compile('\.trm$'), # gnuplot term file
    re.compile('\.font$'), # Font mapping
    re.compile('\.ccg$'), # C++ files - Found in gtkmm*
    re.compile('\.hg$'), # C++ headers - Found in gtkmm*
    re.compile('\.dtd'), # XML Document Type Definition
    re.compile('\.bat') # DOS batch files
    ]

# Development documentation files (for hacking generally)

config_files_devel_doc = [
    re.compile('readme.*$'),
    re.compile('changelog.*'),
    re.compile('todo.*$'),
    re.compile('credits.*$'),
    re.compile('authors.*$'),
    re.compile('changes.*$'),
    re.compile('news.*$'),
    re.compile('install.*$'),  
    re.compile('hacking.*$'),
    re.compile('copyright.*$'),
    re.compile('licen(s|c)e.*$'),
    re.compile('copying.*$'),
    re.compile('manifest$'),
    re.compile('faq$'),
    re.compile('building$'),
    re.compile('howto$'),
    re.compile('design$'),
    re.compile('\.files$'),
    re.compile('files$'),
    re.compile('subdirs$'),
    re.compile('maintainers$'),
    re.compile('developers$'),
    re.compile('contributors$'),
    re.compile('thanks$'),
    re.compile('test$'),
    re.compile('testing$'),
    re.compile('build$'),
    re.compile('comments?$'),
    re.compile('bugs$'),
    re.compile('buglist$'),
    re.compile('problems$'),
    re.compile('debug$'),
    re.compile('hacks$'),
    re.compile('hacking$'),
    re.compile('versions?$'),
    re.compile('mappings$'),
    re.compile('tips$'),
    re.compile('ideas?$'),
    re.compile('spec$'),
    re.compile('compiling$'),
    re.compile('notes$'),
    re.compile('missing$'),
    re.compile('done$'),
    re.compile('\.omf$'), # XML-based format used in GNOME
    re.compile('\.lsm$'),
    re.compile('\.kdevprj$'),
    re.compile('\.directory$'),
    re.compile('\.dox$')
    ]

# Building, compiling, configuration and CVS admin files

config_files_building = [
    re.compile('\.in.*$'),
    re.compile('configure.*$'),
    re.compile('makefile.*$'), 
    re.compile('config.sub$'),
    re.compile('config$'),
    re.compile('conf$'),
    re.compile('cvsignore$'),
    re.compile('\.cfg$'), 
    re.compile('\.m4$'),
    re.compile('\.mk$'),
    re.compile('\.mak$'),
    re.compile('\.make$'),
    re.compile('\.mbx$'),
    re.compile('\.protocol$'),
    re.compile('\.version$'),
    re.compile('mkinstalldirs$'),
    re.compile('install-sh$'),
    re.compile('rules$'),
    re.compile('\.kdelnk$'),
    re.compile('\.menu$'),
    re.compile('\.shlibs$'), # Shared libraries
#    re.compile('%debian%'),
#    re.compile('%specs/%'),
    re.compile('\.spec$') # It seems they're necessary for RPM building
    ]



# Documentation files

config_files_documentation = [
#   'doc/%'),
#    re.compile('%HOWTO%'),
    re.compile('\.html$'),
    re.compile('\.txt$'),
    re.compile('\.ps$'),
    re.compile('\.dvi$'),
    re.compile('\.lyx$'),
    re.compile('\.tex$'),
    re.compile('\.texi$'),
    re.compile('\.pdf$'),
    re.compile('\.sgml$'),
    re.compile('\.docbook$'),    
    re.compile('\.wml$'),
    re.compile('\.xhtml$'),
    re.compile('\.phtml$'),
    re.compile('\.shtml$'),
    re.compile('\.htm$'),
    re.compile('\.rdf$'),
    re.compile('\.phtm$'),
    re.compile('\.tmpl$'),
    re.compile('\.ref$'), # References
    re.compile('\.css$'),
    re.compile('%tutorial%'),
    re.compile('\.templates$'),
    re.compile('\.dsl$'),
    re.compile('\.ent$'),
    re.compile('\.xml$'),
    re.compile('\.xsl$'),
    re.compile('\.entities$'),
    re.compile('\.man$'),
    re.compile('\.manpages$'),
    re.compile('\.doc$'),
    re.compile('\.rtf$'),
    re.compile('\.wpd$'),
    re.compile('\.qt3$'),
    re.compile('man\d?/.*\.\d$'),
    re.compile('\.docs$'),
    re.compile('\.sdw$'), # OpenOffice.org Writer document
    re.compile('\.en$'), # Files in English language
    re.compile('\.de$'), # Files in German
    re.compile('\.es$'), # Files in Spanish
    re.compile('\.fr$'), # Files in French
    re.compile('\.it$'), # Files in Italian
    re.compile('\.cz$') # Files in Czech
    ]

# Images

config_files_images = [
    re.compile('\.png$'),
    re.compile('\.jpg$'),
    re.compile('\.jpeg$'),
    re.compile('\.bmp$'),
    re.compile('\.gif$'),
    re.compile('\.xbm$'), 
    re.compile('\.eps$'), 
    re.compile('\.mng$'),
    re.compile('\.pnm$'),
    re.compile('\.pbm$'),
    re.compile('\.ppm$'),
    re.compile('\.pgm$'),
    re.compile('\.gbr$'),
    re.compile('\.svg$'),
    re.compile('\.fig$'),
    re.compile('\.tif$'),
    re.compile('\.swf$'),
    re.compile('\.svgz$'),
    re.compile('\.shape$'), # XML files used for shapes for instance in Kivio
    re.compile('\.sml$'), # XML files used for shapes for instance in Kivio
    re.compile('\.bdf$'), #  vfontcap  - Vector Font Capability Database (VFlib Version 2)
    re.compile('\.ico$')
    ]

# Translation files

config_files_translation = [
    re.compile('\.po$'),
    re.compile('\.pot$'),
    re.compile('\.charset$'),
    re.compile('\.mo$')
    ]

# User interface files

config_files_ui = [
    re.compile('\.desktop$'),
    re.compile('\.ui$'),
    re.compile('\.xpm$'),
    re.compile('\.xcf$'),
    re.compile('\.3ds$'),
    re.compile('\.theme$'),
    re.compile('\.kimap$'),
    re.compile('\.glade$'),
    re.compile('rc$')
    ]

# Sound files

config_files_sound = [
    re.compile('\.mp3$'),
    re.compile('\.ogg$'),
    re.compile('\.wav$'),
    re.compile('\.au$'),
    re.compile('\.mid$'),
    re.compile('\.vorbis$'),
    re.compile('\.midi$'),
    re.compile('\.arts$')
    ]

# Unknown files (just leave it as it is!!!)

config_files_unknown = []

# 

config_files_list =  [
    config_files_documentation,
    config_files_images,
    config_files_translation,
    config_files_ui,
    config_files_sound,
    config_files_code,
    config_files_building,
    config_files_devel_doc,
    config_files_unknown
    ]

# The following is used to determine the database names
#
# If you change this, please notice you should also configure
# the colorDict (next configuration variable) properly

config_files_names = [
    'documentation',
    'images',
    'i18n',
    'ui',
    'multimedia',
    'code',
    'build',
    'devel-doc',
    'unknown'
    ]

# Colors for the pie
config_colorDict = {'code': 'red',
	     'documentation': 'blue',
	     'i18n': 'green',
	     'multimedia': 'yellow',
	     'images': 'orange',
	     'ui': 'purple',
	     'build': 'white',
	     'devel-doc': 'black',
	     'unknown': 'gray(0.8)'}

def analyseFile(file):
        """
        Given a filename, returns what type of file it is.
        The file type is set in the config_files configuration file
        and usually this depends on the extension, although other
        simple heuristics are used.

        @type  file: string
        @param file: filename

        @rtype: string
        @return: file type (documentation, development, i18n, sound, etc.)
        """
        i = 0
        for fileTypeSearch_list in config_files_list:
                for searchItem in fileTypeSearch_list:
                        if searchItem.search(file.lower()):
                                return config_files_names[i]
                i+=1
        # if not found, specify it as unknown           
        return 'unknown'

