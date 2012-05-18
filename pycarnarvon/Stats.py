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
Make graphs

@author:       Alvaro Navarro
@organization: Grupo de Sistemas y Comunicaciones, Universidad Rey Juan Carlos
@copyright:    Universidad Rey Juan Carlos (Madrid, Spain)
@license:      GNU GPL version 2 or any later version
@contact:      anavarro@gsyc.escet.urjc.es
"""

import os
import time
import sys
import string
from time import gmtime, strftime
from Database import *

class GeneralStat:
    """
    A python singleton implementation
    """
    __instance = None

    stats = {}

    def __init__(self):

        if GeneralStat.__instance:
            raise GeneralStat.__single

        GeneralStat.__single = self

    def add_stats(self, timestamp, values):
        if not self.stats.has_key(timestamp):
            self.stats[timestamp] = values

    def stats2dat(self, path):

        columns = ["snapshot_aging",
                   "snapshot_progeria",
                   "snapshot_relaging",
                   "snapshot_size",
                   "snapshot_orphaned",
                   "snapshot_age",
                   "snapshot_date50",
                   "snapshot_orphFactor"]
        
        output = open (path + "/generalstat.dat", 'w')

        count = 1
        output.write('#Snapshot\tAging\tProgeria\tRelAging\tSize\tOrphaned\tAge\tFifty\tOrphFactor\tTimestamp\n')

        # tmpList to have the stats in chronological order!
        tmpList = []
        for timestamp in self.stats:
            tmpList.append(timestamp)
        tmpList.sort()
        for stat in tmpList:
            svalues = self.stats[stat]

            result  = str(count) + '\t'
            #result = str(stat).replace("-","/") + '\t'
            result += str(svalues["aging"]) + '\t'
            result += str(svalues["progeria"]) + '\t'
            result += str(svalues["relaging"]) + '\t'
            result += str(svalues["size"]) + '\t'
            result += str(svalues["orphy"]) + '\t'
            result += str(svalues["age"]) + '\t'
            fifty = svalues["date_50"][svalues["date_50"].find('(')+1:svalues["date_50"].find(' month')]
            if not fifty:
                result += str(0) + '\t'
            else:
                result += str(fifty) + '\t'
            result += str(svalues["orphy_factor"]) + '\t'
            result += str(stat) + '\t'
            result += str(svalues["AggSize"]) + '\n'

            output.write(result)

            count += 1
            
        output.close()

        # generate gnuplot file from .dat
        count = 2
        for column in columns:
            output = open (path + "/" + column + ".gnuplot", "w")
            output.write('set title \"' + column.split("_")[1] + '\"' + "\n")
            output.write('set xlabel \"snapshots\"' + "\n")
            output.write('set ylabel \"' +  column.split("_")[1] + '\"' + "\n")
            output.write('set autoscale' + "\n")
            output.write('set yrange [0:]' + "\n")
            output.write('set grid' + "\n")
            output.write('set data style linespoints'+ "\n")
            output.write('set pointsize 1.2' + "\n")
            output.write('set terminal png' + "\n")
            output.write('set output "' + path + '/' + column + '.png"' + "\n")
            output.write('plot "' + path + '/generalstat.dat"')
            output.write(' using 1:' + str(count) + " title \'" + column.split("_")[1] + "\'" + '\n')
            output.close()
            
            count += 1

        
    def print_stats(self):
        print str(self.stats)

class Stats:

    def __init__(self, stats_dir, db_object, dir_id, date, flags = 15):
        self.config_start_year = 0
        self.config_end_month = 0
        self.config_end_year = 0
        self.config_actual_year = date.split("-")[0]
        self.config_actual_date = date
        self.stats_dir = stats_dir
        self.db = db_object
        self.dir_id = dir_id
        self.tic_space = int(flags)

        if dir_id:
            self.where = "dir_id=" + str(self.dir_id)
        else:
            self.where = ""
        
    def setDates(self, table):
        start_year,end_year = self.db.query('min(date),max(date)', table, self.where)[0]

        self.config_start_year = int(str(start_year).split("-")[0])
        self.config_end_year = int(str(end_year).split("-")[0])
        self.config_end_month = int(str(end_year).split("-")[1])

    def revisionStats(self,table):

        # Number of lines
        totalLines = int(self.db.query('count(*)', table, self.where)[0][0])
        
        # Revision numbers (lines)
        output = open(self.stats_dir + '/revLines.dat', 'w')

        output.write('#Rev\tLines\tAgg\tPer\tPerAgg\n')
        linesTuple = self.db.query('revision, count(revision)', table, self.where, 'revision', 'revision')
        linesList = []
        
        for tuple in linesTuple:
            linesList.append([str(tuple[0]), int(tuple[1])])
            
        linesList.sort()
        sum = 0
        sumPer = 0
        
        for line in linesList:
            sum += int(line[1])
            percentage = int(line[1]) * 100.0/totalLines
            sumPer += percentage

            result  = str(line[0]) + '\t'
            result += str(line[1]) + '\t'
            result += str(sum) + '\t'
            result += str(round(percentage,2)) + '\t'
            result += str(round(sumPer,2)) + '\n'

            output.write(result)

        output.close()
            
        self.plot('revLines', 'revLines', 'Revision Stats', 'revision', 'lines', 1, 2, 'false','true')
        self.plot('revLines', 'revLines', 'Revision Stats', 'revision', 'Agg', 1, 3, 'false','true')
        self.plot('revLines', 'revLines', 'Revision Stats', 'revision', 'Per', 1, 4, 'false','true')
        self.plot('revLines', 'revLines', 'Revision Stats', 'revision', 'PerAgg', 1, 5, 'false','false')


    def linesInTimeStats(self,table):

        # Number of lines in time (on a per-month basis)
        last = 0
        total = int(self.db.query('COUNT(*)', table, self.where)[0][0])

        output = open(self.stats_dir + '/lines.dat', 'w')
        output.write('#Id\tYear\tMonth\tAgg\tDiff\tPerAgg\tPerDiff\n')

        # Try to plot the special graph (not uses plot function)
        gnuplot_command_diff = 'set key top left;\n set style data linespoints;\n set terminal png;\n '
        gnuplot_command_peragg = gnuplot_command_diff

        gnuplot_command_diff += 'set output "' + self.stats_dir + '/line_diff.png";\n'
        gnuplot_command_peragg += 'set output "' + self.stats_dir + '/line_peragg.png";\n'

        gnuplot_command_diff += ' set xtics ('
        gnuplot_command_peragg += ' set xtics ('

        # Tics between dates
        count = 1

        for year in range(self.config_start_year, self.config_end_year+1):
            for month in range(1,13):
                if year == self.config_end_year and month > self.config_end_month:
                   break
                # Aggregated
                if self.dir_id:
                    where = "date < '" + str(year) + "-" + str(month) + "-01 00:00:00' AND " + self.where
                else:
                     where = "date < '" + str(year) + "-" + str(month) + "-01 00:00:00'"

                aggregated = int(self.db.query('COUNT(*)',table,where)[0][0])
                diff = aggregated - last
                last = aggregated
                relative = round(aggregated*100.0/total,2)
                relativeDiff = round(diff*100.0/total,2)

                result  = str(count) + '\t'
                result += str(year) + '\t'
                result += str(month) + '\t'
                result += str(aggregated) + '\t'
                result += str(diff) + '\t'
                result += str(relative) + '\t'
                result += str(relativeDiff) + '\n'

                tic = str(month) + '/' + str(year)

                if count % int(self.tic_space) == 0: # Put tic each tic_space (f.e, 15) values
                    gnuplot_command_diff += '\"'+tic+'\" '+str(count)+','
                    gnuplot_command_peragg += '\"'+tic+'\" '+str(count)+','

                count += 1

                output.write(result)

        output.close()

        gnuplot_command_diff = gnuplot_command_diff.rstrip(",") + ");\n "
        gnuplot_command_peragg = gnuplot_command_peragg.rstrip(",") + ");\n "

        gnuplot_command_diff += 'set xlabel "";\n'
        gnuplot_command_peragg += 'set xlabel "";\n'

        gnuplot_command_diff += 'set ylabel "remaining lines ";\n'
        gnuplot_command_peragg += 'set ylabel "remaining lines (%)";\n'

        gnuplot_command_diff += 'set title "SLOC remaining";\n'
        gnuplot_command_peragg += 'set title "SLOC remaining (aggregated over time)";\n'

        # END COMMENT IF DON'T DESIRE DATES IN X LABEL

        begin_graph = '*'
        end_graph = '*'
        gnuplot_command_diff += ' plot ['+begin_graph+':'+end_graph+'] '
        gnuplot_command_peragg += ' plot ['+begin_graph+':'+end_graph+'] '

        project_name = 'lines'
        filename = 'lines.dat'
        gnuplot_command_diff += " '"+filename+"' using 1:5 title 'lines' ,"
        gnuplot_command_peragg += " '"+filename+"' using 1:6 title 'lines' ,"

        gnuplot_command_diff = gnuplot_command_diff.rstrip(",")
        gnuplot_command_peragg = gnuplot_command_peragg.rstrip(",")

        command_file = open(self.stats_dir + '/lines_diff.gnuplot',"w")
        command_file.write(gnuplot_command_diff)
        command_file.close()

        command_file = open(self.stats_dir + '/lines_peragg.gnuplot',"w")
        command_file.write(gnuplot_command_peragg)
        command_file.close()

    def commiterStats(self,table):
        orders = ['Total_Lines', 'Modified_Files']
        column = 2
        for order in orders:
            self.commiterStatsOrder(table, order, column)
            column += 1

    def commiterStatsOrder(self,table, order, column):

        filename = 'commiters_' + order
        output = open(self.stats_dir + '/' + filename + '.dat', 'w')
        output.write('#Author\tLines\tFiles\tTSpan\tLastTime\n')

        select = ' COUNT(*) as Total_Lines, COUNT(DISTINCT(file_id)) as Modified_Files, MIN(date), MAX(date)'
        result = self.db.query(select, table, self.where, order, "commiter_id")

        commiter_id = 1
        for (lines,files,firstDate, lastDate) in result:
            result  = str(commiter_id) + '\t'
            result += str(lines) + '\t'
            result += str(files) + '\t'
            result += str(self.daysPassed(firstDate, lastDate)) + '\t'
            result += str(self.daysPassed(lastDate, self.config_actual_date + ' 00:00:00')) + '\n'
            commiter_id += 1
            output.write(result)

        output.close()

        self.plot(filename, filename, 'Commiters', 'authors', order, 1, column)

    def fileStats(self,table):
        orders = ['All_Lines','Number_Authors','Number_Revisions','Last_Modified']
        column = 2
        for order in orders:
            self.fileStatsOrder(table,order,column)
            column += 1

    def fileStatsOrder(self,table, order, column):
        """    
        # Number of files with all their lines with revision 1.1    
        # Number of files with none of their lines with revision 1.1    
        # For each file:    
        #     * Number of distinct revisions    
        #     * Number of distinct authors    
        #     * Timespan from newest revision to oldest one    
        """

        # filename which contains the values
        filename = 'files_' + order
        output = open(self.stats_dir + '/' + filename + '.dat', 'w')
        output.write("#FileId\tLines\tAuthors\tRevs\tLastModified\n")

        # Total files
        select  = "COUNT(*) as All_Lines, COUNT(DISTINCT(commiter_id)) as Number_Authors,"
        select += " COUNT(DISTINCT(revision)) as Number_Revisions, MIN(date) as oldRevision, MAX(date) as Last_Modified"
        totalfiles = self.db.query(select, table, self.where, order,"file_id")

        file_id = 1
        for (allLines, numberAuthors, numberRevisions, oldRevision, newRevision) in totalfiles:
            try:
                final = str(file_id) + '\t'
                final += str(allLines) + '\t'
                final += str(numberAuthors) + '\t'
                final += str(numberRevisions) + '\t'
                final += str(self.daysPassed(oldRevision, newRevision)) + '\n'

                file_id += 1
                output.write(final)

            except ZeroDivisionError:
                # File empty (or contains only comments or blank lines)
                pass

        self.plot(filename, filename, 'Files', 'files', order, 1, column)

    def daysPassed(self,old, new):
        oldSeconds = time.mktime(time.strptime(str(old), '%Y-%m-%d %H:%M:%S'))
        newSeconds = time.mktime(time.strptime(str(new), '%Y-%m-%d %H:%M:%S'))
        return (round((newSeconds - oldSeconds) / (24 * 3600)))


    def plot(self, outputFile,
                    values,
                    title,
		    xlabel,
		    ylabel,
		    xvalue,
                    yvalue,
                    xlogscale = 'false',
                    ylogscale = 'false',
		    dataStyle = 'linespoints'):

        output = open(self.stats_dir + '/' + outputFile + "_" + str(xlabel) + "_" + str(ylabel) + ".gnuplot", 'w')

        # Title of the Graph
        if (ylogscale == '1' or ylogscale == 'true') and (xlogscale == '1' or ylogscale == 'true'):
            output.write('set title "' + title + ' (log log)"' + "\n")
        else:
            output.write('set title "' + title + '"\n')

        # X axis Label
        if xlogscale == '1' or xlogscale == 'true':
            output.write('set xlabel "'+ xlabel +' (log)"' + "\n")
        else:
            output.write('set xlabel "'+ xlabel +'"' + "\n")

        # Y axis Label
        if ylogscale == '1' or ylogscale == 'true':
            output.write('set ylabel "'+ ylabel +' (log)"' + "\n")
        else:
            output.write('set ylabel "'+ ylabel +'"' + "\n")

        output.write('set autoscale' + "\n")
        output.write('set yrange [0:]' + "\n")
        output.write('set grid' + "\n")
        output.write('set data style ' + dataStyle + "\n")
        output.write('set pointsize 1.2' + "\n")

        # Logscale Y
        if ylogscale == '1' or ylogscale == 'true':
            output.write('set logscale y' + "\n")

        # Logscale X
        if xlogscale == '1' or xlogscale == 'true':
            output.write('set logscale x' + "\n")

        output.write('set terminal png' + "\n")

        mstring = 'set output "' + self.stats_dir + '/' + outputFile + '.png"' + "\n"
        mstring += 'plot "' + self.stats_dir + '/' + values + '.dat"'

        if ylogscale == '1' or ylogscale == 'true':
            mstring += ' using ' + str(xvalue) + ':' + str(yvalue) + ' title \'' + title + ' (log) \'' + '\n'
        else:
            mstring += ' using ' + str(xvalue) + ':' + str(yvalue) + ' title \'' + title + '\'' + '\n'

        output.write(mstring)
        output.close()

