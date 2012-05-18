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
Web class 


@author:       Alvaro Navarro
@organization: Grupo de Sistemas y Comunicaciones, Universidad Rey Juan Carlos
@copyright:    Universidad Rey Juan Carlos (Madrid, Spain)
@license:      GNU GPL version 2 or any later version
@contact:      anavarro@gsyc.escet.urjc.es
"""

import sys
import os
from time import gmtime, strftime
import Globals as gb
import Database as dbmodule
import Stats as stmodule
import SVG as svgmodule

class Web:

    def __init__(self):
        # Where to save the webpage
        self.path = ''
        self.templates = ''
        self.filename = ''
        self.dates = None
        self.styles = ['newstyle.css']
        self.images = [ 'background.jpg',
                        'bg.gif',
                        'carnarvon-logo.png']

    def generate_head(self):
        """
        Generates header file
        """
        html = self.read_file(self.templates + "/header.html")

        return html

    def generate_menu(self, index=0):
        """
        Generate right menu
        """
        html = ''
        html += '<div id=\"navcontainer\">\n'
        html += '<b> navigation </b>\n'
        html += '<br/><br/>\n'
        html += '<ul id=\"navlinks\">\n'
        html += '<li><a href=.../index.html>main index</a></li>\n'
        for d in self.dates:
            if index:
                html += '<li><a href=stats_' + str(d) + "/index.html>" + d + "</a></li>\n"
            else:
                html += '<li><a href=../stats_' + str(d) + "/index.html>" + d + "</a></li>\n"

        html += "</ul><br/><br/><b>powered by <a href=http://carnarvon.tigris.org>carnarvon</a>"
        html += "</b><br/></div>\n"

        return html

    def read_file(self, file):

        files = open(file,'r')

        aux = ''
        while (1):
            l = files.readline()
            l = l[:-1]
            if not l:
                break
            aux += l + "\n"

        files.close()

        return aux

    def generate_html(self, dates):
        # Create HTML output from metadatafile, graphs and metrics
        self.dates = dates

        #output = open(self.path + "/" + self.filename + ".html", 'w')
        output = open(self.path + "/" + "index.html", 'w')

        head = self.generate_head()
        body = self.generate_body()
        html = head + body

        output.write(html)
        output.close()

        # Copy images and css
        gb.Globals.createdir(self.path + "/images/")

        try:
            for img in self.images:
                os.system("cp -fR " + self.templates + "/images/" + img + " " + self.path + "/images/")
            for stl in self.styles:
                os.system("cp -fR " + self.templates + "/" + stl + " " + self.path)
        except:
            pass

    def generate_graphs(self):
        import os

        os.system("cd " + self.path + " && gnuplot *plot 2> /dev/null")
        
    def generate_body(self):
        pass

class WebIndex(Web):
    """
    Class that represents the Index.html Web of the site
    """
    def __init__(self):
        """
        Constructor
        """

        self.graphs = ['snapshot_age.png',
                       'snapshot_size.png',
                       'snapshot_AggSize.png',
                       'snapshot_aging.png',
                       'snapshot_relaging.png',
                       'snapshot_date50.png',                       
                       'snapshot_progeria.png',
                       'snapshot_orphaned.png',                      
                       'snapshot_orphFactor.png']
        
        Web.__init__(self)
        self.path = gb.Globals.workspace
        self.templates = gb.Globals.templates
        self.filename = "index"
        gb.Globals.createdir(self.path)

    def generate_body(self):
        # Create HTML output from metadatafile, graphs and metrics

        print "         => Generating Stats"
        gstat = stmodule.GeneralStat()
        gstat.stats2dat(self.path)
        print "         => Generating Graphs"
        self.generate_graphs()
        
        html = "<body>\n"
        html += "<div class=\"header\" style=\"height:76px;\"><b>Archaeology Stats</b></div>\n"
        html += "<div id=\"logo\">\n"
        html += "<a style=\"background-image: url(images/carnarvon-logo.png);\"\n"
        html += "href=\"http://carnarvon.tigris.org\"\n"
        html += "title=\"Carnarvon Project Homepage\"></a>\n"

        html += "<br><br><br><br>"
        for img in self.graphs:
                 html += "<img border=\"0\" src=\"" + img + "\" height=480 width=640>\n"
                 
        html += "</div>\n"
        html += "<div style=\"float:left;\">\n"
        html += "</div>\n"
        menu = self.generate_menu(index=1)
        html += menu + "\n</body></html>"

        return html


class WebStat(Web):

    def __init__(self, date, target, flags=15):
        """
        Constructor
        
        @type  date: String
        @param date: Date of the current stamp
        @type  target: database_object
        @param target: Database which store the data
        @type  flags: String
        @param flags: flags for gnuplot
        """
        Web.__init__(self)

        self.metrics = {'size'     :0,
                        'AggSize'  :0,
                        'age'      :0,
                        'aging'    :0,
                        'relaging' :0,
                        'progeria' :0,
                        'orphy'    :0,
                        'orphy_factor': 0,
                        'date_50'  :''}

        self.source = { 'lines': 'lines.dat',
                        'commiters' : 'commiters.dat',
                        'files': 'files.dat'}

        self.graphs = {'lines': ['line_diff.png',
                                 'line_peragg.png'],

                       'commiters' : ['commiters_Total_Lines.png',
                                      'commiters_Modified_Files.png'],

                       'files' : ['files_All_Lines.png',
                                  'files_Number_Authors.png',
                                  'files_Number_Revisions.png',
                                  'files_Last_Modified.png'],

                       'revlines': ['revLines_revision_Agg.png',
                                    'revLines_revision_lines.png']
                       }

        self.date = date.replace("_","-")
        self.db = target
        self.flags = flags

        # Is the current page a statistic web of a directory?
        self.isDirectory = 0
        
        # Path to disk data
        self.filename = date
        self.path_without_dir = ""
        self.path = gb.Globals.workspace + "/stats_" + self.filename + "/"

        # Create path which will contain the current web
        gb.Globals.createdir(self.path)

        # Path to the html's templates
        self.templates = gb.Globals.templates

        # Path to database data
        self.table = 'annotates_' + date

    #def generate_graphs(self):
    #    import os
    #    os.system("cd " + self.path + " && gnuplot *plot 2> /dev/null")

    def read_file2table(self, file):

        files = open(str(self.path) + "/" + file,'r')

        aux = ''

        while (1):
            l = files.readline()
            l = l[:-1]
            if not l:
                break
            if l[0] == '#':
                pass
            if l == "":
                pass

            fields = l.split('\t')
            aux += "<tr>"
            for f in fields:
                aux += "<td> " + str(f) + "</td>\n"
            aux += "</tr>\n"

        files.close()

        return aux

    def get_general_stats(self):
        """
        Extract general info about current timestampt
        """
        lines = self.db.query("count(distinct(line_id))", self.table)[0][0]
        commiters = self.db.query("count(distinct(commiter_id))", self.table)[0][0]
        files = self.db.query("count(distinct(file_id))", self.table)[0][0]

        return lines, commiters, files

    def generate_body(self):
        # Create HTML output from metadatafile, graphs and metrics

        lines = 0
        commiters = 0
        files = 0
        
        try:
            print "         => Generating Stats"
            self.generate_stats()
            print "         => Generating Graphs"
            self.generate_graphs()
            print "         => Generating Metrics"
            self.generate_metrics()
            print "         => Generating General Stats"
            lines, commiters, files = self.get_general_stats()
        except:
            pass
        """
        print "         => Generating Stats"
        self.generate_stats()
        print "         => Generating Graphs"
        self.generate_graphs()
        print "         => Generating Metrics"
        self.generate_metrics()
        print "         => Generating General Stats"
        lines, commiters, files = self.get_general_stats()
        """

        html = ''
        html += "<body>\n"
        html += "<div class=\"header\" style=\"height:76px;\"><b>Archaeology Stats: " + self.filename.replace('_','/') + "</b></div>\n"
        html += "<div id=\"logo\">\n"
        html += "<a style=\"background-image: url(images/carnarvon-logo.png);\"\n"
        html += "href=\"http://carnarvon.tigris.org\"\n"
        html += "title=\"Carnarvon Project Homepage\"></a>\n"
        html += "</div>\n"
        html += "<div style=\"float:left;\">\n"
        html += "<h3 class=\"title\"> metrics </h3>\n"
        html += "<table border=0>\n"
        html += "<tr><td> <b>Software Size</b> </td><td> " + str(self.metrics['size']) + " SLOC </td><td>Size of the software in SLOC (lines of code not including comments and blank lines)</td></tr>\n"
        html += "<tr><td> <b>Software Age</b> </td><td> " + str(self.metrics['age']) + " months</td><td>Months since the first commit</td></tr>\n"
        html += "<tr><td> <b>Commiters</b> </td><td>" + str(commiters) + "</td><td>Number of contributors</td></tr>\n"
        html += "<tr><td> <b>Files</b> </td><td>" + str(files) + "</td><td>Number of source code files</td></tr>\n"
        html += "<tr><td> <b>Aging</b></td><td> " + str(self.metrics['aging']) + " SLOC-month</td><td>Area under the aggregated curve</td></tr>\n"
        html += "<tr><td> <b>Relative Aging</b> </td><td> %2.2f </td><td>Gives the amount of time to have the same aging if the project had started with the current number of lines (or the amount of time required to double the aging of the project)</td></tr>\n" % self.metrics['relaging']
        html += "<tr><td> <b>50% of current code</b> </td><td>" + str(self.metrics['date_50']) + "</td><td>Number of months where 50% of the current code base mark is achieved</td></tr>\n"
        html += "<tr><td> <b>Progeria</b> </td><td> %2.2f </td><td>&gt;1 means the code base of the project is getting older (legacy) while &lt;1 means that the project code base is getting younger</td></tr>\n" % self.metrics['progeria']
        html += "<tr><td> <b>Orphaning</b> </td><td>" + str(self.metrics['orphy']) + " SLOC-month</td><td></td></tr>\n"
        html += "<tr><td> <b>Orphaning factor</b> </td><td>" + str(self.metrics['orphy_factor']) + "</td><td></td></tr>\n"
#        html += "<tr><td> <b>Total Lines</b> </td><td>" + str(lines) + "</td></tr>\n"
        html += "</table>\n"

        gstat = stmodule.GeneralStat()
        gstat.add_stats(self.date, self.metrics)
        
        # Tables and graphs
        for fdate in self.source:
             html += "<h3 class=\"title\"> " + fdate + " </h3>\n"
             images = self.graphs[fdate]
             for img in images:
                 html += "<img border=\"0\" src=\"" + img + "\" height=480 width=640>\n"


        if not self.isDirectory:
            html += self.create_directories(entire=1)
        else:
            html += self.create_directories(entire=0)
            html += self.create_files()

        html += "</div>\n"

        menu = self.generate_menu()
        html += menu + "\n</body></html>"

        return html

    def create_files(self):
        """
        Extract files from the actual timestamp/directory
        """
        files = self.db.query("distinct(f.file)", self.table + " as a, files as f", "dir_id=" + self.dir_id + " and a.file_id = f.file_id")

        html = "<h3 class=\"title\"> Files </h3>\n"
        for (file,) in files:
            html += "<a href=" + self.path_without_dir + str(file[1:]) + "/index.html>" + str(file[1:]) + "</a><br>\n"

        html += "<br><br>"
        return html


    def create_directories(self, entire=0):
        """
        Extract current directories from the timestamp we're building

        @type entire: int
        @param entire: if 0, querys will use dir_id index, else, query will use the entire table 
        """
        
        if entire == 0:
            dirs = self.db.query("module_id, module", "directories", "father_dir=" + self.dir_id)
        else:
            dirs = self.db.query("module_id, module", "directories")


        html = "<h3 class=\"title\"> Directories </h3>\n"
        for (module_id, module) in dirs:
            html += "<a href=" + self.path_without_dir + str(module[1:]) + "/index.html>" + str(module[1:]) + "</a><br>\n"

        html += "<br><br>"
        
        return html

    def generate_stats(self):
        """
        Create metadata files from the tables.
        """
        # create new object stats
        if self.isDirectory:
            st = stmodule.Stats(self.path, self.db, self.dir_id, self.date, self.flags)
        else:
             st = stmodule.Stats(self.path, self.db, None, self.date, self.flags)
        st.setDates(self.table)

        # Stats from database
        #st.revisionStats(self.table)
        st.linesInTimeStats(self.table)
        st.commiterStats(self.table)
        st.fileStats(self.table)

    def get_orphaning(self):
        """
        Auxiliar function that calculate orphaning factor
        """
        sum = 0
        totalCommiters = self.db.query("distinct(commiter_id), count(line_id), max(date)", self.table, "", "commiter_id", "commiter_id")
        for (commiter_id, totalLines, lastdate) in totalCommiters:
            #print str(commiter_id) , " ", str(totalLines) ," ", str(lastdate)
            lastyear = str(lastdate).split("-")[0]
            lastmonth = str(lastdate).split("-")[1]
            # Actual timestamp
            actualmonth = self.date.split("-")[1]
            actualyear  = self.date.split("-")[0]
            # number of months between dates
            total = (int(actualyear) - int(lastyear) - 1) * 12 + (12 - int(lastmonth)) + int(actualmonth)
#            print str(lastyear), str(lastmonth), str(actualyear), str(actualmonth), total, str(totalLines)
            total = int(total) * int(totalLines)
            sum += int(total)

        return sum

    def generate_metrics(self):
        """
        get metrics from file
        """

        try:
            input = open(self.path + '/' + self.source['lines'], 'r')
        except:
            sys.exit("Error: File " + str(self.source['lines']) + " not found")

        actualyear = self.date.split("-")[0]
        actualmonth = self.date.split("-")[1]

        # Extract metrics from metadata stored in .dat files
        sum = 0
        months = 0
        stored = 0
        while 1:
            line = input.readline()
            if not line:
                break
            if line[0] == '#':
                pass
            else:
                percent = float(line.split('\t')[5])
                if (percent >= 50) and not stored:
                    year = int(line.split('\t')[1])
                    ms = int(line.split('\t')[2])
                    #print "* 50% of code on: " + str(year) + "/" + str(ms)
                    total = (int(actualyear) - year - 1) * 12 + (12 - ms) + int(actualmonth)
                    stored = 1

                lastMonth = int(line.split('\t')[3])
                sum += lastMonth
                if lastMonth > 0:
                    months+=1

        # indexes
        self.metrics['size'] = lastMonth
        self.metrics['AggSize'] += lastMonth * months
        self.metrics['age'] = months
        self.metrics['aging'] = sum - lastMonth
        self.metrics['relaging'] = (sum-lastMonth)*1.0/lastMonth
#        self.metrics['rel5a'] = (sum-lastMonth)*1.0/(lastMonth * 60)
#        self.metrics['abs5a'] = (sum-lastMonth)*1.0/(100000 * 60)
        self.metrics['progeria'] = ((sum-lastMonth)*1.0/lastMonth) / total
        self.metrics['date_50'] = str(year) + "/" + str(ms) + " (" + str(total) + " months)"
        self.metrics['orphy'] = self.get_orphaning()
        self.metrics['orphy_factor']= round(self.metrics['orphy']*10000.0/self.metrics['aging'])/100.0


class WebDirStat(WebStat):

    def __init__(self, date, target, directory, dir_id, flags):
        WebStat.__init__(self, date, target, flags)
        #self.date = date.replace("_","-")
        #self.db = target
        self.directory = directory
        self.dir_id = dir_id

        # we're building an stadistical web of a directory
        self.isDirectory = 1

        # Path to disk data
        self.filename = date
        self.path = gb.Globals.workspace + "/stats_" + self.filename + "/" + self.directory + "/"
        gb.Globals.createdir(self.path)

        # Path to the html's templates
        self.templates = gb.Globals.templates

        # Path to database data
        self.table = 'annotates_' + date

        # Path without Dir file
        self.path_without_dir = gb.Globals.workspace + "/stats_" + self.filename + "/"

class WebFileStat(WebStat):
    def __init__(self, date, target, file, file_id):
        WebStat.__init__(self, date, target)
        self.date = date.replace("_","-")
        self.db = target
        self.file = file
        self.file_id = file_id

        # Path to disk data
        self.filename = date
        self.path = gb.Globals.workspace + "/stats_" + self.filename + "/" + self.file + "/"
        gb.Globals.createdir(self.path)

        # Path to the html's templates
        self.templates = gb.Globals.templates

        # Path to database data
        self.table = 'annotates_' + date

    def generate_svg(self):

        files = self.db.query("file_id, file", "files", "file_id=" + self.file_id)

        for (file_id, file) in files:
            revisions = self.db.query("revision", self.table, "file_id="+str(file_id))
            revs = []
            for rev in revisions:
                revs.append(int(str(rev[0]).split('.')[1]))

            line_graph =svgmodule.LinesGraph()
            line_graph.print_to_file("/tmp/fichero_id_"+str(file_id)+".svg", revs)
            #bar_graph = svgmodule.BarGraph()
            #bar_graph.print_to_file("fichero_id_2.svg", revs)

    def generate_functions(self):
        pass

    def generate_body(self):
        html = ''
        html += "<body>\n"
        html += "<div class=\"header\" style=\"height:76px;\"><b>Archaeology Stats: " + self.filename.replace('_','/') + "</b></div>\n"
        html += "<div id=\"logo\">\n"
        html += "<a style=\"background-image: url(images/carnarvon-logo.png);\"\n"
        html += "href=\"http://carnarvon.tigris.org\"\n"
        html += "title=\"Carnarvon Project Homepage\"></a>\n"
        html += "</div>\n"
        html += "<div style=\"float:left;\">\n"
        html += "<h3 class=\"title\"> metrics </h3>\n"

        html += "</div>\n"

        menu = self.generate_menu()
        html += menu + "\n</body></html>"


        return html

