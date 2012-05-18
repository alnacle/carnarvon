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
SVG.py - Construct/display SVG scenes.

The following code is a lightweight wrapper around SVG files. The metaphor
is to construct a scene, add objects to it, and then write it to a file
to display it.

This program uses ImageMagick to display the SVG files. ImageMagick also 
does a remarkable job of converting SVG files into other formats.

@author:       Alvaro Navarro
@organization: Grupo de Sistemas y Comunicaciones, Universidad Rey Juan Carlos
@copyright:    Universidad Rey Juan Carlos (Madrid, Spain)
@license:      GNU GPL version 2 or any later version
@contact:      anavarro@gsyc.escet.urjc.es
"""

import os
display_prog = 'inkscape'


class Scene:
    def __init__(self,name="svg",height=400,width=400):
        self.name = name
        self.items = []
        self.height = height
        self.width = width
        return

    def add(self,item):
        self.items.append(item)

    def strarray(self):
        var = ["<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n"+\
	    "<svg\n"+\
	    "   xmlns:dc=\"http://purl.org/dc/elements/1.1/\"\n"+\
	    "   xmlns:cc=\"http://web.resource.org/cc/\"\n"+\
	    "   xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\"\n"+\
	    "   xmlns:svg=\"http://www.w3.org/2000/svg\"\n"+\
	    "   xmlns=\"http://www.w3.org/2000/svg\"\n"+\
	    "   xmlns:sodipodi=\"http://inkscape.sourceforge.net/DTD/sodipodi-0.dtd\"\n"+\
	    "   xmlns:inkscape=\"http://www.inkscape.org/namespaces/inkscape\"",
	    "   height=\"%d\" width=\"%d\">"% (self.height,self.width),
        " <g style=\"fill-opacity:1.0; stroke:black;\n","  stroke-width:1;\">\n"]

        for item in self.items:
            var += item.strarray()

        var += [" </g>\n</svg>\n"]
        return var

    def write_svg(self,filename=None):
        if filename:
            self.svgname = filename
        else:
            self.svgname = self.name + ".svg"
        file = open(self.svgname,'w')
        file.writelines(self.strarray())
        file.close()
        return

    def display(self,prog=display_prog):
        os.system("%s %s" % (prog,self.svgname))
        return

class Line:
    def __init__(self,start,end):
        self.start = start #xy tuple
        self.end = end     #xy tuple
        return

    def strarray(self):
        return ["  <line x1=\"%d\" y1=\"%d\" x2=\"%d\" y2=\"%d\" />\n" %\
                (self.start[0],self.start[1],self.end[0],self.end[1])]


class ColorLine:
    def __init__(self,start,end, color):
        self.start = start #xy tuple
        self.end = end     #xy tuple
        self.color = color
        return

    def strarray(self):
        return ["  <line x1=\"%d\" y1=\"%d\" x2=\"%d\" y2=\"%d\" " %\
                (self.start[0],self.start[1],self.end[0],self.end[1]),"    style=\"stroke:%s;\"  />\n" % colorstr(self.color)]

class Circle:
    def __init__(self,center,radius,color):
        self.center = center #xy tuple
        self.radius = radius #xy tuple
        self.color = color   #rgb tuple in range(0,256)
        return

    def strarray(self):
        return ["  <circle cx=\"%d\" cy=\"%d\" r=\"%d\"\n" %\
                (self.center[0],self.center[1],self.radius),
                "    style=\"fill:%s;\"  />\n" % colorstr(self.color)]

class Rectangle:
    def __init__(self,origin,height,width,color):
        self.origin = origin
        self.height = height
        self.width = width
        self.color = color
        return

    def strarray(self):
        return ["  <rect x=\"%d\" y=\"%d\" height=\"%d\"\n" %\
                (self.origin[0],self.origin[1],self.height),
                "    width=\"%d\" style=\"fill:%s;\" />\n" %(self.width,colorstr(self.color))]


class StyleRectangle:
    def __init__(self,origin,height,width,style):
        self.origin = origin
        self.height = height
        self.width = width
        self.style = style
        return

    def strarray(self):
        return ["  <rect x=\"%d\" y=\"%d\" height=\"%d\"\n" %\
                (self.origin[0],self.origin[1],self.height),
                "    width=\"%d\" style=\"%s\" />\n" %(self.width,self.style)]


class Text:
    def __init__(self,origin,text,size=12):
        self.origin = origin
        self.text = text
        self.size = size
        return

    def strarray(self):
        return ["  <text x=\"%d\" y=\"%d\" font-size=\"%d\">\n" %\
                (self.origin[0],self.origin[1],self.size),
                "   %s\n" % self.text,
                "  </text>\n"]

class Title:
    def __init__(self,origin,text,size=20):
        self.origin = origin
        self.text = text
        self.size = size
        return

    def strarray(self):
        return ["  <text x=\"%d\" y=\"%d\" font-size=\"%d\">\n" %\
                (self.origin[0],self.origin[1],self.size),
                "   %s\n" % self.text,
                "  </text>\n"]

def colorstr(rgb):
    return "#%x%x%x" % (rgb[0]/16,rgb[1]/16,rgb[2]/16)


class LinesGraph:

    def __init__(self):
        self.top_margin = 30
        self.bottom_margin = 30
        self.left_margin = 30
        self.right_margin = 30

        self.file_bar_default_height = 4
        self.line_bar_default_width = 5
        self.default_bar_color = (65,238,235)

        self.m_secene = None
        self.values = None
        self.cursor_x = self.left_margin
        self.cursor_y = self.top_margin
        self.line_scale_resolution = 10   #Used for statistic line meter.
        self.separation_between_file_bars = self.file_bar_default_height * 3

    def set_style(self, rate):
        #Given a rate, the result is a colour
        if rate==1:
            return "fill:#FFFF00;fill-opacity:1;stroke:#000000;stroke-width:0;"
        if rate==2:
            return "fill:#FFCC00;fill-opacity:1;stroke:#000000;stroke-width:0;"
        if rate==3:
            return "fill:#FF9900;fill-opacity:1;stroke:#000000;stroke-width:0;"
        if rate==4:
            return "fill:#FF6600;fill-opacity:1;stroke:#000000;stroke-width:0;"
        if rate==5:
            return "fill:#FF3300;fill-opacity:1;stroke:#000000;stroke-width:0;"
        if rate==6:
            return "fill:#FF0000;fill-opacity:1;stroke:#000000;stroke-width:0;"
        if rate==7:
            return "fill:#CC3300;fill-opacity:1;stroke:#000000;stroke-width:0;"
        if rate==8:
            return "fill:#CC0000;fill-opacity:1;stroke:#000000;stroke-width:0;"
        if rate==9:
            return "fill:#993333;fill-opacity:1;stroke:#000000;stroke-width:0;"
        if rate==10:
            return "fill:#990033;fill-opacity:1;stroke:#000000;stroke-width:0;"
        if rate==11:
            return "fill:#990066;fill-opacity:1;stroke:#000000;stroke-width:0;"
        if rate==12:
            return "fill:#990099;fill-opacity:1;stroke:#000000;stroke-width:0;"
        if rate==13:
            return "fill:#666699;fill-opacity:1;stroke:#000000;stroke-width:0;"
        if rate==14:
            return "fill:#663399;fill-opacity:1;stroke:#000000;stroke-width:0;"
        if rate==15:
            return "fill:#6600CC;fill-opacity:1;stroke:#000000;stroke-width:0;"
        if rate==16:
            return "fill:#3300CC;fill-opacity:1;stroke:#000000;stroke-width:0;"
        if rate==17:
            return "fill:#0033FF;fill-opacity:1;stroke:#000000;stroke-width:0;"
        if rate==18:
            return "fill:#0000FF;fill-opacity:1;stroke:#000000;stroke-width:0;"
        if rate==19:
            return "fill:#006699;fill-opacity:1;stroke:#000000;stroke-width:0;"
        if rate==20:
            return "fill:#009999;fill-opacity:1;stroke:#000000;stroke-width:0;"
        if rate==21:
            return "fill:#00CC66;fill-opacity:1;stroke:#000000;stroke-width:0;"
        if rate==22:
            return "fill:#00CC00;fill-opacity:1;stroke:#000000;stroke-width:0;"
        if rate==23:
            return "fill:#00FF00;fill-opacity:1;stroke:#000000;stroke-width:0;"
        if rate==24:
            return "fill:#66FF00;fill-opacity:1;stroke:#000000;stroke-width:0;"
        if rate==25:
            return "fill:#99FF00;fill-opacity:1;stroke:#000000;stroke-width:0;"
        if rate==26:
            return "fill:#CCFF00;fill-opacity:1;stroke:#000000;stroke-width:0;"
        if rate>=27:
            return "fill:#000000;fill-opacity:1;stroke:#000000;stroke-width:0;"

    def print_to_file (self, filename, values):
        self.values = values
        self.build_scene(filename)

    def build_scene(self, filename):
        self.m_scene = Scene(filename)
        self.draw_lines()
        self.m_scene.write_svg(filename)

    def draw_lines(self):
        #Colocando el cursor de pintado.
        
        self.cursor_y   += self.separation_between_file_bars
        
        square_height = self.file_bar_default_height
        square_width =  self.line_bar_default_width*70

        for val in self.values:
            self.m_scene.add(StyleRectangle((self.cursor_x, self.cursor_y), square_height, square_width, self.set_style(val)))
            self.cursor_y += self.file_bar_default_height


class BarGraph:

    def __init__(self):
        #Format properties
        self.top_margin = 50
        self.bottom_margin = 50
        self.left_margin = 50
        self.right_margin = 50

        self.legenda_height = 50

        self.text_file_name = 300
        self.file_bar_default_height = 10
        self.line_bar_default_width  = 5

        self.default_bar_color = (65,238,235)

        self.values = None
        self.m_scene  = None
        self.cursor_x    = self.left_margin
        self.cursor_y    = self.top_margin

        #Lines meter
        self.line_scale_resolution = 10   #Used for statistic line meter.
        self.separation_between_file_bars = self.file_bar_default_height * 3

    def print_to_file (self, filename, values):
        self.values = values
        self.build_scene(filename)

    def build_scene(self, filename):
        self.m_scene = Scene(filename)
        project_name = "prueba"
        #self.m_scene.add(Title((40,20),"Archaeology analysis: "+project_name))
        self.draw_quad()
        self.m_scene.write_svg(filename)

    def draw_quad(self):

        tamano_x = 200
        tamano_y = 200

        orientation = 'v'

        size = 0
        for l in self.values:
            size += l

        self.cursor_x = 0
        self.cursor_y = 0

        origin = (self.cursor_x, self.cursor_y)

        for l in self.values:
            aux = float(l)/float(size)

            if orientation == 'v':
                tamano_aux =int( float(aux)*float(tamano_x))
                tamano_x -= tamano_aux
                self.m_scene.add(Rectangle((self.cursor_x, self.cursor_y), tamano_y, tamano_aux, (self.cursor_x,tamano_y,tamano_x)))
                self.cursor_x += tamano_aux
                orientation = 'h'
            else:
                tamano_aux = int(float(aux)*float(tamano_y))
                tamano_y -= tamano_aux
                self.m_scene.add(Rectangle((self.cursor_x, self.cursor_y), tamano_aux, tamano_x, (self.cursor_y, tamano_x ,tamano_y)))
                self.cursor_y += tamano_aux
                orientation = 'v'

            size -= l

    def draw_legenda (self):
        self.cursor_x = self.left_margin + self.text_file_name + self.left_margin + self.left_margin
        self.cursor_y = self.m_scene.height
        square_height=50
        square_width=50
        self.m_scene.add(Rectangle((self.cursor_x-25, self.cursor_y),140,1200,(255,255,255)))
        self.m_scene.add(Title((self.cursor_x+400,self.cursor_y+20),"Number of Modifications"))
        self.cursor_y += 70

        for i in range(0,11):
            self.m_scene.add(Text((self.cursor_x+20,self.cursor_y),str(i)))
            self.m_scene.add(StyleRectangle((self.cursor_x, self.cursor_y+10),\
                                                                square_height,\
                                                                square_width,\
                                                                self.set_style(i)))
            self.cursor_x += square_width * 2

        #El ultimo cuadrado
        self.m_scene.add(Text((self.cursor_x+20,self.cursor_y),"+10"))
        self.m_scene.add(StyleRectangle((self.cursor_x, self.cursor_y+10),\
                                                            square_height,\
                                                            square_width,\
                                                            self.set_style(11)))

        self.m_scene.height += 200

if __name__ == '__main__':
    d = BarGraph()
    d.print_to_file("balbla.svg")

