#!/usr/bin/python

# Anubis, a program to do quality analysis of GNSS receiver data,  is at 

# anubisplot.py makes plots, onscreen or in image files, of Anubis results.

# The anubisplot.py web site is http://www.westernexplorers.us/GNSSplotters/
# This file is online at        http://www.westernexplorers.us/GNSSplotters/anubisplot.py
# See also                      http://www.westernexplorers.us/GNSSplotters/Anubisplot_Documentation.txt.

# Version 1.0 May 20, 2016 

# Copyright (c) 2016 Stuart K. Wier

#         ============  to save plots automatically as PNG files ===============
# As supplied anubisplot is an interactive program, that makes one plot image in a window on your screen. 
#     You can save that image with a click on the disc icon in the window lower margin.
# To automatically make and save the plot image as a PNG file, do these code changes in this anubisplot.py file:
# 1. Uncomment the line  #mptl.use('Agg')   below, i.e. remove the #, and preserving the indentation level
# 2. Comment out the line  plt.show() ;           i.e. start the line with #,  preserving the indentation level
# 3. Uncomment the line # plt.savefig(filename) ; i.e. remove the # , preserving the indentation level

# Configuration.
# To enable making figures in .png files:
# the next line is used ONLY to save figures as PNG files (see also lines around 'savefig' below):
#mptl.use('Agg') # uncomment when needed to save figures as PNG files.

# To see debug statements, set the value noprint=0 in the noprint= near line 800. 

import os
import sys
import string
import datetime
import numpy as np 
import matplotlib as mptl
import matplotlib.cm as cm 
import matplotlib.pyplot as plt

from numpy import *
from datetime import timedelta
from datetime import datetime
from matplotlib.pyplot import grid, figure, plot, savefig
from time import gmtime, strftime

anubisfile=""
parmfile=""
parmtype=""
debug=False
dogps=True
doglonass=True
dogalileo=True
dosbas=True
dobeidou=True
doqzss=True
trackCountLimit=6 
colorMax=1.234567
colorMin=1.234567
maxHour= -999.0 
minHour= -999.0 
global lineSize
colorname="" 
showLegend=False
showLabel= True
doParmPlot=False
svs=[]
svslist=[]
parmsvslist=[]
options=[]
files=[]
SVpositionList=[] 
allAzisList=[]
allElesList=[]
allParmsList=[]
SVparmList=[]     
SVidList=[]       
SVtypesList=[]       
SVparmidList=[]   
doShowSVslist=[]
doNotShowSVslist=[]
global asciiStartTime 
global maxT 
global minT 
global noprint
widthDistance = 7.3  # for width of plot;  inches is units of distance in matplotlib; 
pixeldensity  = 100  
global parmname 

helptext="""

 
   ==============================      How to Use Anubisplot      ==============================      

May 20, 2016

Preparation 

To install and run anubisplot, first verify your system requirements, and download the anubisplot.py file, as described 
in  http://www.westernexplorers.us/GNSSplotters/Anubisplot_Documentation.txt.
You need Python, and the Python libraries numpy version 1.5 and matplotlib version 1.3.

Anubisplot plots data from *xtr files created by Anubis, http://www.pecny.cz/gop/index.php/gnss/sw/anubis.

As supplied anubisplot is an interactive program, that makes one plot image in a window on your screen. 

For automatic scripting of anubisplot image file generation, to automatically make and 
save the plot image as a PNG file, do these code changes in this anubisplot.py file:
 1. Uncomment the line  # mptl.use('Agg') above, i.e. remove the # , preserving the indentation level
 2. Comment out the line  plt.show()             i.e. start the line with #,  preserving the indentation level
 3. Uncomment the line # plt.savefig(filename) ; i.e. remove the # , preserving the indentation level


Anubisplot Commands

Anubisplot uses command line commands, with data file names and command "options."  
Spaces " " are not allowed inside options. Option order should not matter. 

Each run of anubisplot.py in interactive mode makes one plot on your screen. 
To stop the program, click on the 'x' in the upper right corner of the window which pops up. 

Examples of anubisplot commands:

To run anubisplot.py, you use the command anubisplot.py in the working directory where that file is, 
or use ./anubisplot.py if that directory is not in your Linux PATH.  
These examples simply show 'anubisplot.py' in commands to run anubisplot, not ./anubisplot.py.

Entering the single command anubisplot.py shows this help message.


To make skyplots (polar plots):
   anubisplot.py +skyplot GOPE150010.xtr
where GOPE150010.xtr is a sample Anubis .xtr file name.  This creates a skyplot of tracks of SVs.
Use typically also option +tcl=n where n is how many lines (SVs) to plot on the graph. 

To make azimuth-elevation plots (azimuth on x axis; elevation on y axis):
   anubisplot.py +azelplot GOPE150010.xtr
This shows an azimuth-elevation plot of tracks of SVs.

To make plots with time of day on the x axis and elevation on the y axis 
   anubisplot.py +timeelplot GOPE150010.xtr  
Note the ee in timeelplot.

Options may added to the command, for example using the option -R means do not plot any GLONASS SVs. 
   anubisplot.py +skyplot GOPE150010.xtr -R
This makes a skyplot of tracks of SVs, but with no GLONASS SVs shown. 
Likewise use -G for no GPS SVs, -E for no Galileo, -J for no QZSS, -C for no Beidou, and -S for no SBAS.

To save an image file of the display, click on the "Save the figure" button on the bottom of the window which pops up.
To change the plot image file size (pixels) use the options +pw and +pd described next.

SVs are selected to plot from the data files, in the order the SVs appear in the data file.  If you choose to plot
10 tracks and the first 5 are GPS and the next five are GLONASS in the file, those are the ones plotted, unless 
options change SV selection. 

More choices:

How many lines plotted:
+tcl=n 
n, an integer, is the maximum number of how many tracks to show (lines in plot). Default is 6.

How big are the markers or symbols:
+msize=f.f
f.f is a float number (or integer) denoting point marker size, for line width or thickness.  Default is 2.5.

-tracklabels 
do not show the SV id (like G12) on each track (line on plot). Default is to show the SV labels.

+legend 
to show a legend of colors identifying each SV next to the figure. Default is no legend. This is for plots
where each SV data has one color, not for parameter plots.  A legend shrinks the plot from right to left
to make room for the legend in the image size. In many plots the curves are labeled and the legend is not needed.
Default is the legend is not shown.


To set picture size and pixel density:

+pw=f.f 
f.f, a float number, sets the width of plot in centimeters. Default value is 20.0 cm. 
+pd=nn 
nn, an integer, is the pixel density, how many pixels per centimeter. Default is 50. (* 2.54 is "dots per inch") 
For illustrations to print later, you can adjust the quality of the plot's image file by changing pw and/or pd.  For example:

    anubisplot.py  +skyplot  +tcl=8  GOPE150010.xtr +pw=25.0 +pd=80 


To select by constellation and by SV number:

+GNN, +GNN-MM, +RNN, +RNN-MM, +J01, etc.  Select SVs to plot by constellation and a single number or number range.
    +G12 to plot only data from GPS G12; likewise +R20 for GLONASS; +J01 for QZSS 
    +G12-20 to plot only data from GPS SVs included in the list from G12 through G20; 
    likewise +R20-24 for GLONASS from R20 through R24
    +G12,23,24,25 to plot only data from G12, G23, G24 and G25; likewise +R15,20,22 to plot these three GLONASS SVs 
     With the +G, +R, etc. options you may to also include a +tcl=N option.
  Example:
    anubisplot.py +skyplot GOPE150010.xtr +R15,20,22,23,25 +G12,23,24,25  +tcl=9


+color=orange 
sets this one color for all tracks (lines in plot). Use standard HTML color names. 
Has no effect on plot lines colored by parameter values as described below.


+minHour=8.0, +maxHour=16.5
  You can limit the time range shown in time plots with options +minHour, +maxHour:

    anubisplot.py +timeelplot p2301220.azi p2301220.ele p2301220.m12 +G22 +minHour=8 +maxHour=16


To Color Tracks by Parameter Value

To make plots like the above, and also color the SV tracks by data values, including signal to noise ratios, use a command option
of the parameter symbol in the Anubis .xtr file, such as +S1C for S/N data, and +M1C for multipath:

    anubisplot.py  +skyplot GOPE150010.xtr +S1C

    anubisplot.py  +timeelplot GOPE150010.xtr +M1C

    anubisplot.py  +axelplot GOPE150010.xtr +S1Y

Color ranges used depend on the parameter type, each of which has a preset range of values, 
to enable equal comparion of several plots, and to not stretch the color scale to cover a 
few extreme high and low values.    

The default limits for colors of values are:

signal to noise: 20.0 to 60.0
"M" values:       0.0 to 80.0

Another colored plot is the Band Plot.  To make GNSS band plots, with a horizontal line for each SV, versus time, 
  use the plot type option +bandplot:
    anubisplot.py  +bandplot GOPE150010.xtr  +M1X

You can change the max and min parm values for the colors with either or both of the options +colorMax and +colorMin, for example

    anubisplot.py +bandplot GOPE150010.xtr +colorMax=50  +colorMin=10

The default color map is the Python matplotlib's "hsv." By experience this is the most distinct color.
You can change the Python code to change the color map used to any other matplotlib color map name.  
Change the color map name in the line cmap=mptl.cm.hsv.


Time-Parameter Plots. To make plots with time of day on the x axis and the parameter on the y axis.  Not colored.
    anubisplot.py +timeparmplot GOPE150010.xtr  +G23  +M1X
  Usually this is done with data from one SV, with an option like +G23.  You must includew the parameter option like +M1X.


You can limit the time range shown with options +minHour, +maxHour:
    anubisplot.py +timeparmplot GOPE150010.xtr  +mp +G22 +minHour=8 +maxHour=16


Visibility Plot 
  Bandplots without a 3rd (parameter values) file make a "Visibility" plot:
    anubisplot.py  +bandplot GOPE150010.xtr  


Spaces " " are not allowed in options. Option order should not matter.


Automatic colors
   If you do not like the automatically-generated colors of markers, you can change the
   numerical value in a line with the comment " alter colors".  For example, the value 1.75 in
       color=cm.gist_ncar(1.75*svPRNIndex/numberColors) )  # alter colors
   Which colors will be made are easier to determine by experiment than by prior coding in this case.

                                               Copyright (C) 2016 Stuart K. Wier
 
   ==============================     end of How to Use Anubisplot      ==============================      

    """


def readAnubisXtrFile ():
    global noprint
    global asciiStartTime
    global parmname 
    if parmname != "   ":
       print ("      Plotting parameter values for "+parmname)
    # open the anubis xtr  file
    datapath1 = os.path.dirname (anubisfile)
    filename1 =   os.path.basename(anubisfile)
    fileext = string.split(filename1, ".")
    anubisFile = open (anubisfile)

    # count lines in input file
    allLines = anubisFile.readlines()
    anubisFilelinecount = len(allLines)
    anubisFile.seek(0) 

    epoch = None 
    gotepoch=False
    seelinecount=0

    doc=''' sample lines

#====== Elevation & Azimuth (v.9)
#GNSELE 2015-01-01 00:00:00    Mean x01 x02 x03 x04 x05 x06 x07 x08 x09 x10 x11 x12 x13 x14 x15 x16 x17 x18 x19 x20 x21 x22 x23 x24 x25 x26 x27 x28 x29 x30 x31 x32 x33 x34 x35
 GPSELE 2015-01-01 00:00:00      34  41   -  19  20   -   -  33   -  78  17  36   -   -   -   -   -  49   -   -  30   -   -  52   -   -   -   -  16   -  16   -   -   -   -   -
 GPSELE 2015-01-01 00:20:00      33  39   -  16  15   -   -  39   -  70  19  30   -   -   -   -   -  54   -   -  28   -   -  43   -   -   -   -  14   -  22   -   -   -   -   -
...
[AZI data starts]
#GNSAZI 2015-01-01 00:00:00    Mean x01 x02 x03 x04 x05 x06 x07 x08 x09 x10 x11 x12 x13 x14 x15 x16 x17 x18 x19 x20 x21 x22 x23 x24 x25 x26 x27 x28 x29 x30 x31 x32 x33 x34 x35
 GPSAZI 2015-01-01 00:00:00     155  84   -  32 110   -   - 158   - 315 289 119   -   -   -   -   - 300   -   -  11   -   -  23   -   -   -   - 226   - 190   -   -   -   -   -
 GPSAZI 2015-01-01 00:20:00     158  96   -  40 118   -   - 150   - 342 298 127   -   -   -   -   - 285   -   -  21   -   -  22   -   -   -   - 217   - 184   -   -   -   -   -

 
where plot data starts, at this line:

#====== Code multipath (v.9)
#GNSMxx 2015-01-01 00:00:00    mean x01 x02 x03 x04 x05 x06 x07 x08 x09 x10 x11 x12 x13 x14 x15 x16 x17 x18 x19 x20 x21 x22 x23 x24 x25 x26 x27 x28 x29 x30 x31 x32 x33 x34 x35
=GPSM1C 2015-01-01 00:00:00   74.17  82  58  65  79  57  63  75  45  58  84  76  57  78  57  64  63  59  94 109  76  66  96  59  89  87  89  82  89  56  64  60  49   -   -   -
...
 GPSM1C 2015-01-01 00:00:00   70.92  95   -   -   -   -   -  59   -  33 107  70   -   -   -   -   -  34   -   -  82   -   -  62   -   -   -   -   -   -  95   -   -   -   -   -
 GPSM1C 2015-01-01 00:20:00   83.00  77   -   -   -   - 183  42   -  38 115 104   -   -   -   -   -  41   -   -  89   -   -  64   -   -   -   -  97   -  64   -   -   -   -   -

    '''
    elazstart=0
    asciiStartTime= " "
    asciiStartTimeAZI= " "
    asciiStartTimeELE= " "
    firstLine = True
    inELEs = False
    inAZIs = False 
    inParms = False 
    seelinecnt=0
    azislist = []
    eleslist = []
    lincecounter=0

 
    # step through each line in the anubis file
    for ln in range( anubisFilelinecount) :
      line  = anubisFile.readline()
      lincecounter+=1
      #if lincecounter % 50 ==0:
      #    print "\n  line counter "+`lincecounter`


      #if seelinecnt> 3200:
      #  break

      lineSvList = []
      lineEleList= []
      lineAziList= []
      lineParmList= []

      svtype = "0"

      lines_like='''
#GNSELE 2015-01-01 00:00:00    Mean x01 x02 x03 x04 x05 x06 x07 x08 x09 x10 x11 x12 x13 x14 x15 x16 x17 x18 x19 x20 x21 x22 x23 x24 x25 x26 x27 x28 x29 x30 x31 x32 x33 x34 x35
GPSELE 2015-01-01 00:20:00      33  39   -  16  15   -   -  39   -  70  19  30   -   -   -   -   -  54   -   -  28   

#GNSAZI 2015-01-01 00:00:00    Mean x01 x02 x03 x04 x05 x06 x07 x08 x09 x10 x11 x12 x13 x14 x15 x16 x17 x18 x19 x20 ... x35
GPSAZI 2015-01-01 00:00:00     155  84   -  32 110   -   - 158   - 315 289 119   -   -   -   -   - 300   -   -  11  
        '''

      #  Check each line for starting point of data of interest for plotting, where line has  #====== Elevation & Azimuth
      #      first, all lines before first encountering "#====== Elevation & Azimuth" :

      if   elazstart==0 and line[0:27] != "#====== Elevation & Azimuth" :
            continue

      elif elazstart==0 and line[0:27] == "#====== Elevation & Azimuth" :
            # at the one line "#====== Elevation & Azimuth"  which begins part of file with values of eles, azis, parms
            elazstart=1
            continue
      elif elazstart==1 and "ELE"==line[4:7] :
        inELEs = True 
        #   at one of the lines with eles values; can be for any or several SV constellations including GPS GLO etc.
        # Get ELE data values 
        svtype= line[1:4] 
        #seelinecnt +=1
        #print "\n   "+ `seelinecnt`+" ele line = "+line[:-1]
        #print "   svtype 1 ="+svtype # debug  like GLO GPS, etc 
        # you are at the "ELE- Mean " line starting the ELEs values section:
        #   so get the ONE start time for ELE data in this file
        if asciiStartTime== " "  and  inELEs:
		startTimeELE = line[8:27] 
		# make python DateTime object:
		starttimeDT =   datetime.strptime(startTimeELE, '%Y-%m-%d %H:%M:%S')
		# make time strings:
		asciiStartTime= starttimeDT.strftime('%Y %m %d %H:%M:%S')
		asciiStartTimeELE = asciiStartTime
		#print "   ELE start time = "+asciiStartTimeELE
                # get list of ALL sv numbers from the "Mean" line for ELEs:
		svns=line[36:-1]
		svns=svns.replace("x", "")
		svns=svns.replace("    ", " ") 
		svns=svns.replace("   ", " ")
		svns=svns.replace("  ", " ")
		#svns=svns[1:-1]
		# debug print " ALL possible sv NUMBERS in the line ="+svns
		svnslist = string.split(svns," ") # split on whitespace; makes a List
		# debug print " ALL possible svns NUMBERS in the line ="
                # debug print svnslist #print "\n"
                #firstLine = false 
        elif  inELEs :                 # for each  ELE  line after the first ELE line
                svtype = line[1:4]
		# get 'epoch ' for this line of data; convert epoch  to hours since start time
		et1 = line[8:27] 
		epochDT =   datetime.strptime(et1, '%Y-%m-%d %H:%M:%S')
		dt = epochDT - starttimeDT
		# dthours = dt/( timedelta(hours=1))
		dthours = dt.total_seconds() / 3600.000
		# debug 
                #print "   ele line at time offset = "+`epoch` +" hours.  :" # debug
		epoch = dthours # float 
		eles=line[36:-1]
		eles=eles.replace("    ", " ") 
		eles=eles.replace("   ", " ")
		eles=eles.replace("  ", " ")
		eles=eles[1:-1] # debug
		# debug print "   elevs in the line ="+eles + " at time "+ et1 # debug
		eleslist = string.split(eles," ") # split on whitespace; makes a List
                # NOTE last item is "" not "-" print eleslist # debug
                # for ind in range ( len(svnslist)) :
                #     tsp = svtype + svnslist[ind] 
                #     svnslist[ind] = tsp
                for ind in range (1, len(eleslist)) :
                    if eleslist[ind] =="-" or eleslist[ind] =="" :
                        pass
                    else:
                       #print " append good elev="+ eleslist[ind] + " at sv="+ svnslist[ind]
                       # LOOK ASSUMING THAT ELES and AXIs lines always have same Svs
                       lineSvList.append (svnslist[ind] )
                       lineEleList.append (eleslist[ind] )
                #print "   one ELE line of svs:" 
                #print lineSvList
                #print "   and its elevation values:" 
                #print lineEleList
	    	eletuple =  (epoch, lineSvList, lineEleList )
		allElesList.append(eletuple)

      elif elazstart==1 and "AZI"==line[4:7] :    #   GET AZIMUTH DATA VALUES
        inELEs = False 
        inAZIs = True 
        #   at one of the lines with azi values; can be for any or several SV constellations including GPS GLO etc.
        svtype= line[1:4] 
        #seelinecnt +=1
        #print `seelinecnt`+" azi line = "+line[:-1]

        #print " svtype 2 ="+svtype # debug  like GLO GPS, etc 
        # you are at the "Azi - Mean " line starting the AZI values section:
        #   so get the ONE start time for AZI data in this file
        if asciiStartTimeAZI == " "  and  inAZIs:
                #print " svtype 2b ="+svtype +"; convert to plotter ID letter:"
                if svtype == "GPS":
                   svtype = "G"
                elif svtype == "GLO":
                   svtype = "R"
                elif svtype == "GAL":
                   svtype = "E"
                elif svtype == "BDS":
                   svtype = "C"
                elif svtype == "QZS":
                   svtype = "J"
                #print " svtype 3 ="+svtype # debug  like GLO GPS, etc 

		startTimeELE = line[8:27] 
		# make python DateTime object:
		starttimeDT =   datetime.strptime(startTimeELE, '%Y-%m-%d %H:%M:%S')
		# make time strings:
		asciiStartTime= starttimeDT.strftime('%Y %m %d %H:%M:%S')
		asciiStartTimeAZI = asciiStartTime

		#if asciiStartTimeELE != asciiStartTimeAZI :
		#   #print " \n  PROBLEM : ELE start time  NOT  asciiStartTimeELE \n"
		#print " \n  AZI start time = "+asciiStartTimeAZI

                # get list of ALL sv numbers from the "Mean" line for AZI:
		svns=line[36:-1]
		svns=svns.replace("x", "")
		svns=svns.replace("    ", " ") 
		svns=svns.replace("   ", " ")
		svns=svns.replace("  ", " ")
		svnslist = string.split(svns," ") # split on whitespace; makes a List
        elif  inAZIs :                 #  "AZI"==line[4:7] : # for AZI lines after the first AZI - Mean line
                svtype = line[1:4]
                #print " svtype 4a ="+svtype
                if svtype == "GPS":
                   svtype = "G"
                elif svtype == "GLO":
                   svtype = "R"
                elif svtype == "GAL":
                   svtype = "E"
                elif svtype == "BDS":
                   svtype = "C"
                elif svtype == "QZS":
                   svtype = "J"
		# get 'epoch ' for this line of data; convert epoch  to hours since start time
		et1 = line[8:27] 
		epochDT =   datetime.strptime(et1, '%Y-%m-%d %H:%M:%S')
		dt = epochDT - starttimeDT
		# dthours = dt/( timedelta(hours=1))
		dthours = dt.total_seconds() / 3600.000
		#print " azi line at time offset = "+`epoch` +" hours.  :" # debug
		epoch = dthours # float 
		azis=line[36:-1]
		azis= azis.replace("    ", " ") 
		azis=azis.replace("   ", " ")
		azis=azis.replace("  ", " ")
		azis=azis[1:-1] # debug
		azislist = string.split(azis," ") # split on whitespace; makes a List
		#print azislist # debug
                # make the lineSvList and lineAziList for this line at time epoch 
                # 
                for ind in range (1, len(azislist)) :
                    if azislist[ind] =="-" or azislist[ind] =="":
                        pass
                    else:
                       # debug print " append good azi="+ azislist[ind] + " at sv="+ svnslist[ind]
                       # LOOK ASSUMING THAT ELES and AXIs lines always have same Svs mmm
                       lineSvList.append ( (svtype+svnslist[ind]) )
                       lineAziList.append (azislist[ind] )

	    	azituple =  (epoch, lineSvList, lineAziList )
                # LOOK try to skip empty sets, where len(lineSvList)==0
                if len(lineSvList)==0:
                   continue

		allAzisList.append(azituple)
                # this List has azituples

                # debug the List azilist for this line should correspond to the List of SVS svslist
                #if len(lineSvList) != len(lineAziList):
                #    print "  Problem:  number of SVs does not match number of azis; " +`len(lineSvList)`+"  "+`len(lineAziList)`
                #if len(lineEleList) != len(lineAziList):
                #    print "  Problem:  number of eles does not match number of azis; " +`len(lineEleList)`+"  "+`len(lineAziList)`


      elif elazstart==1 and len(line)> 4 and parmname[0]==line[4] :  # M or S   in parm rows area # GET PARM VALUES
        inELEs = False 
        inAZIs = False 
        inParms = True 
        seelinecount+=1 

        #   at one of the lines with this parm's values; can be for any or several SV constellations including GPS GLO etc.
        svtype= line[1:4] 
        #print " svtype 3 ="+svtype # debug  like GLO GPS, etc 
        seelinecnt +=1

        # you are at the  line starting the multipath or S/N parm values section:
        #GNSMxx 2015-01-01 00:00:00    mean x01 x02 x03 x04 x05 x06 x07 x08 x09 x10 x11 x12 x13 x14 x15 x16 x17 x18 x19 x2 
        #GNSSxx 2015-01-01 00:00:00    mean x01 x02 x03 x04 x05 x06 x07 x08 x09 x10 x11 x12 x13 x14 x15 x16 x17 x18 x19 x2 
        #   so get the ONE start time for the parm data in this file
        if asciiStartTimeAZI == " "  and inParms and line[0]=="#":
                #print " svtype 2b ="+svtype +"; convert to plotter ID letter:"
                if svtype == "GPS":
                   svtype = "G"
                elif svtype == "GLO":
                   svtype = "R"
                elif svtype == "GAL":
                   svtype = "E"
                elif svtype == "BDS":
                   svtype = "C"
                elif svtype == "QZS":
                   svtype = "J"

		startTimep = line[8:27]  
		# make python DateTime object:
		starttimeDT =   datetime.strptime(startTimep, '%Y-%m-%d %H:%M:%S')
		# make time strings:
		asciiStartTime= starttimeDT.strftime('%Y %m %d %H:%M:%S')
		asciiStartTimeparm = asciiStartTime

		#if asciiStartTimeELE != asciiStartTimeparm :
		#   #print " \n  PROBLEM : ELE start time  NOT  asciiStartTimeparm \n"
                if seelinecount < 50 :
		  print "   parm start time = "+asciiStartTimeparm # ddd

                # get list of ALL sv numbers from the "Mean" line for this parm:
		svns=line[36:-1]
		svns=svns.replace("x", "")
		svns=svns.replace("    ", " ") 
		svns=svns.replace("   ", " ")
		svns=svns.replace("  ", " ")
		#svns=svns[1:-1]
		svnslist = string.split(svns," ") # split on whitespace; makes a List
                # for ind in range (1, len(svnslist)) :
                #    svnslist[ind] = svtype + svnslist[ind] 
		# print " parm start line ALL possible svns NUMBERS in the line =".join(svnslist)

        elif  inParms and parmname==line[4:7] and line[0]==" " :    #   THIS parm type line after the first parm-section line
                svtype = line[1:4]
                #print " svtype 4a ="+svtype
                if svtype == "GPS":
                   svtype = "G"
                elif svtype == "GLO":
                   svtype = "R"
                elif svtype == "GAL":
                   svtype = "E"
                elif svtype == "BDS":
                   svtype = "C"
                elif svtype == "QZS":
                   svtype = "J"

		# get 'epoch ' for this line of data; convert epoch  to hours since start time
		et1 = line[8:27] 
		epochDT =   datetime.strptime(et1, '%Y-%m-%d %H:%M:%S')
		dt = epochDT - starttimeDT
		# dthours = dt/( timedelta(hours=1))
		dthours = dt.total_seconds() / 3600.000
		epoch = dthours # float 

                skip='''if seelinecount < 20 :
                  print "parm line at SV svtype 4b ="+svtype # debug  GOOD use this svtype
                  print "  parm line _"+line[:-1]
		  print "  at time offset = "+`epoch` +" hours.  :" # debug
                    '''

		parms=line[36:-1]  #ppp
		parms= parms.replace("    ", " ") 
		parms=parms.replace("   ", " ")
		parms=parms.replace("  ", " ")
		parms=parms[1:-1] # debug
		parmslist = string.split(parms," ") # split on whitespace; makes a List
		#print " parn values=".join(parmslist) # debug ddd
                # make the lineSvList and lineParmList lineAziList for this line at time epoch 
                # 
                for ind in range (1, len(parmslist)) :
                    if parmslist[ind] =="-" or parmslist[ind] =="":
                        pass
                    else:
                       # debug 
                       #print " append good parm="+ parmslist[ind] + " at sv="+ svnslist[ind]
                       # LOOK ASSUMING THAT ELES and parm lines always have same valid Svs 
                       lineSvList.append ( (svtype+svnslist[ind]) )
                       lineParmList.append (parmslist[ind] )
	    	parmtuple =  (epoch, lineSvList, lineParmList )

                # to knock 
                # save list of all sv constellations which have azi [and ele] data values
                if len(lineSvList)>0:
                   thissvt=lineSvList[0][:1]
                   if thissvt in SVtypesList:
                      pass
                   else:
                      # debug print "  new parm sv type = "+lineSvList[0][:1]
                      SVtypesList.append(thissvt)

                # this one thing has a bunch of parmtuples
		allParmsList.append(parmtuple)

                # debug the List parmlist for this line should correspond to the List of SVS svslist
                if len(lineSvList) != len(lineParmList):
                    print "  Problem:  number of SVs does not match number of parms; " +`len(lineSvList)`+"  "+`len(lineParmList)`


    # debug print "   have done all lines in anubis file "

    # debug for ind in range (0, len( SVtypesList)):
    #   print "                parm SV ="+SVtypesList[ind]


    # wrangle lists into plot-able objects
    #print " len of allAzisList= "+`len( allAzisList)`
    #print " len of allElesList= "+`len( allElesList)`
    #print " len of allParmsList= "+`len( allParmsList)`
    for ti in range ( len( allAzisList) ) :
        #print "   merge azi and ele lines at epoch "+ `atup[0]` 

        atup = allAzisList[ti] # pull out the azi tuple
        etup = allElesList[ti] # pull out the ele tuple

        # match epochs
        if atup[0] != etup[0] :
            #print "  no match in epoch in list of azis at svs and list of eles at svs in a line pair in anubis file" 
            # checking the assumption that the list and order of epochs in the ele section and azi seciton of the anubis file is the same.
            break

        #if not doParmPlot:  
        for ist in range( len(atup[1]) ) :  # for each single SV from this single epoch's set of all-SV data
            # a set of 4 single values for this epoch and SV:
            #             sv#              epcoh        azi                  elev
	    #         (SvList[ist],        epoch,   AziList[ist],         EleList[ist] )
	    # epoch in hours print    "  azi atup[0]   = "+atup[0]
  
            if not doParmPlot:  # kkk
                try:
	                posituple =  (atup[1][ist] ,  atup[0],   atup[2][ist], etup[2][ist] )
                #print " no parm tuple:"
                #print posituple
                # ('C05', 21.083333333333332, '116', '16')
                except IndexError:
                    pass
	        SVpositionList.append(posituple)

            elif  doParmPlot:
                  # first, only use cases of azi data which are for an svtype which type has parm values of this parameter type
                  azisvt = atup[1] [ist] [:1]
                 
                  if azisvt in SVtypesList: # the list of svs TYPES like G R E with parm data
                     # check all parm data rows
                     for pi in range ( len( allParmsList) ) :
                         ptup = allParmsList[pi] # pull out the parm tuple
                         # check this parm data row for this exact time
                         if (  atup[0] ==  ptup[0] ): 
                             #print " ok at time"+`ptup[0]` # float hours
                             # now find if there is any matching parm sv to atup[1] [ist] 
                             #print "  len ptup[1]="+ `(len( ptup[1]))`
                             for pi2 in range (len( ptup[1])):
                                 if atup[1] [ist] == ptup[1] [pi2]:
                                     #  ptup[2][pi2] is the parm's value for this time and this SV
				     posituple =  (atup[1] [ist] ,  atup[0],   atup[2][ist], etup[2][ist],  ptup[2][pi2])
				     #print "  parm tuple:"
				     #print posituple
				     SVpositionList.append(posituple)
                  else:
                     pass #print " skip "+azisvt

        out='''
        if  doParmPlot:
          # print "\n len of ptup 2 ="+`len(ptup[2])` +"\n"
          #for ist in range( len(atup[1]) ) :  # for each single SV from this single epoch's set of all-SV data
          for ist in range( len(ptup[2]) ) :  # for each single SV from this single epoch's set of all-SV data
		  # original psv=parmsvslist[ist]  
		  # done above  ptup = allParmsList[ti] # pull out the parm tuple
		  #print " parm list at ist "+`ist`+":"
		  #print    "  atup[1] [ist]    = "+atup[1] [ist] 
		  print    "  possible sv in azi data  = "+atup[1] [ist] [:1]
                  psvt = atup[1] [ist] [:1]
                  if psvt in SVtypesList:
                    pass
                  else:
                    print " skip "+psvt
                    continue

               
		  #print    "  atup[0]   = "+`atup[0]`
		  #print    "  atup[2][ist]    = "+atup[2][ist]
		  #print    "  etup[2][ist]   = "+etup[2][ist]
		  #print    "  ptup[2][ist]   = "+ptup[2][ist]

		  posituple =  (atup[1] [ist] ,  atup[0],   atup[2][ist], etup[2][ist],  ptup[2][ist])

                  debug   =print " len of allAzisList= "+`len( allAzisList)`
                  #print " len of allElesList= "+`len( allElesList)`
                  print " len of allParmsList= "+`len( allParmsList)`
		  # make one of these tuples with ONE value of SV, time, azi, ele, parm-value.
                  print "  append the parm posituple:"
                  print posituple
                   

		  SVpositionList.append(posituple)
                  '''

        #

    # end function readAnubisXtrFile()



def makePlot ():  
    global noprint
    global asciiStartTime 
    global maxT 
    global minT 
    global lineSize
    maxPV=-999.0
    minPV=9999.0
    svid=""
    allToPlot ={}
    maxT= -100000.0 # float hours
    minT=  100000.0 # float hours
    numberplotted=0
    for svid in SVidList:
            # debug print ' plot '+svid
	    times = []
	    azis = []
	    eles = []
	    parms = []
            slipcount=0
	    for aRow in SVpositionList:
	        if svid == aRow[0]:
                            if plottype == "Skyplot":
			        times.append (aRow[1] )       
                                #print " aRow[2]="
                                #print aRow[2]
                                azv =   float(aRow[2])
			        azis.append( azv*(np.pi/180))  
                                anele = float(aRow[3])
			        eles.append(90.00-anele)    
                            else:
                                t=float(aRow[1])
                                if t>maxT: maxT = t
                                if t<minT: minT = t
			        times.append ( aRow[1] )       
                                azv =   float(aRow[2])
			        azis.append(azv)
                                anele = float(aRow[3])
			        eles.append(anele)
                            if doParmPlot :
                                pv = aRow[4]
                                #if pv[-1:]=="S" : 
				#   pv = pv[:-1]    
                                pv = float(pv)
                                if pv>maxPV: maxPV= pv
                                if pv<minPV: minPV= pv
			        parms.append (pv) 
	    if doParmPlot : 
                plotDataArrays= (times, azis, eles, parms)   
            else:
	        plotDataArrays= (times, azis, eles)
	    allToPlot[svid] = plotDataArrays

    if noprint!=1 : 
       if parmname != "   ":
          print "      "+parmtype+"data values span "+`minPV`+" to "+`maxPV`
    if noprint!=1 : print "      Done reading data to plot.  The figure is being created."

    starttime_t1= datetime.now()
    bgcolor="#FFFFff" 
    if plottype == "Skyplot":
        fig= figure (figsize=(widthDistance, widthDistance), dpi=pixeldensity, facecolor=bgcolor, edgecolor='k')
        ax = fig.add_axes([0.1, 0.1,  0.8, 0.8], projection='polar', axisbg=bgcolor) 
    else:
        fig= figure (figsize=(1.6*widthDistance, 1.2*widthDistance/1.62), dpi=pixeldensity, facecolor=bgcolor, edgecolor='k')
        ax = fig.add_axes([0.1, 0.13, 0.8, 0.8],  axisbg=bgcolor) 
    if showLegend :
	box = ax.get_position()
	ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    numberColors=30 
    size=0.3
    svPRNIndex=0 
    plotlist=[]
    svlist=[]
    trackcount=1
    bandindex=0
    mplot=None
    pvtop=-9999
    pvbot = 9999
    numberplotted = 0
    for svid in sorted(allToPlot.keys()) : 
        bandindex += 1
        # do not plot unwanted SVs:
        if svid[0:1]=="R" and doglonass!=True : continue 
        if svid[0:1]=="G" and dogps!=True     : continue 
        if svid[0:1]=="E" and dogalileo!=True : continue 
        if svid[0:1]=="S" and dosbas!=True    : continue 
        if svid[0:1]=="J" and doqzss!=True   : continue
        if svid[0:1]=="C" and dobeidou!=True : continue 
    	if len(doShowSVslist)>0:
	    if svid not in doShowSVslist:
		continue;
        if trackcount > trackCountLimit : continue
    	trackcount+=1
        svPRNIndex= int(svid [1:])
        if svid[0:1]=="R" : svPRNIndex += 32 
	plotDataArrays=allToPlot[svid]
        times=plotDataArrays[0]
        azis= plotDataArrays[1]
        eles= plotDataArrays[2] 
        if parmtype  ==  "Parameter " : # old "Multipath combination" :
		# orig minPV=-1.5
		# orig maxPV= 1.5
		minPV= 0.0
		maxPV= 80.0 
        elif parmtype ==  "Signal to Noise" :
		minPV= 20.0
		maxPV= 60.0
        elif parmtype =="Ionspheric Delay (m)": 
		minPV=-30.0
		maxPV= 40.0
        elif  parmtype =="Ionspheric Delay Derivative (m/min)":
		minPV= -0.5
		maxPV=  0.5
        if colorMax != 1.234567 :
                maxPV= colorMax
        if colorMin != 1.234567 :
                minPV= colorMin
        # else use minPV maxPV values already found from the data

        if plottype == "Skyplot" or plottype == "Azimuth-elevation plot":
	    if True==doParmPlot:
                parms= plotDataArrays[3] 
                colmap=mptl.cm.hsv 
		prange= maxPV - minPV 
		pvtop = -999993.0
		pvbot= 999993.0
		for pi in range (0, len(parms)):
		    pnew=parms[pi]
		    if pnew>maxPV : pnew=maxPV;
		    if pnew<minPV : pnew=minPV;
		    pnew = (pnew - minPV) / prange 
		    parms[pi]=pnew
		    if parms[pi] > pvtop : pvtop = parms[pi] 
		    if parms[pi] < pvbot : pvbot = parms[pi] 
		#if debug: print "        pvbot, pvtop= "+`pvbot`+" to "+`pvtop`+"     min max PV="+`minPV`+" to "+`maxPV` +"\n"
		norm=mptl.colors.Normalize(vmin=0.0, vmax=1.0)
		mplot = plt.scatter (azis, eles, c=parms, norm=norm, s=lineSize, cmap=mptl.cm.hsv, lw=0) # 1sss 
		numberplotted += 1
            else:
              if colorname == "" : 
                  # debug print "    plot scatter # " +`numberplotted`
                  # about right size = 7 
                  size=lineSize
                  if plottype == "Skyplot" :
		     #print "    debug plot skyplot nc "
                     mplot = plt.scatter(azis, eles, s=size, color=cm.gist_ncar(1.0*svPRNIndex/numberColors) ) # alter colors
                  if plottype == "Azimuth-elevation plot":
		     #print "    debug plot azelplot nc "
                     mplot  = plt.scatter(azis, eles, s=size, color=cm.gist_ncar(1.75*svPRNIndex/numberColors) )  # alter colors
                     #mplot = plt.plot(azis, eles, label=  svid) # 2ss plots lines betwwen dots
		     #mplot = plt.plot (azis,eles  ) 
                  numberplotted += 1
              else :
                  # size = 6.3 
                  size=lineSize
                  if plottype == "Skyplot" :
		     print "    debug plot skyplot color"
                     plot = plt.scatter(azis, eles, s=size, color=colorname) # sss 
                  if plottype == "Azimuth-elevation plot":
		     print "    debug plot azelplot color"
		     mplot = plt.plot (azis,eles  )  # LOOK FIX set line color
                  numberplotted += 1
        elif plottype == "Time-elevation plot":  
	    if True==doParmPlot:
                parms= plotDataArrays[3] 
                colmap=mptl.cm.hsv 
		#print "  parameter allowed range ="+`maxPV`+" to "+`minPV`
		prange= maxPV - minPV 
		pvtop = -999993.0
		pvbot= 999993.0
		for pi in range (0, len(parms)):
		    pnew=parms[pi]
		    if pnew>maxPV : pnew=maxPV;
		    if pnew<minPV : pnew=minPV;
		    pnew = (pnew - minPV) / prange 
		    parms[pi]=pnew
		    if parms[pi] > pvtop : pvtop = parms[pi] 
		    if parms[pi] < pvbot : pvbot = parms[pi] 
		norm=mptl.colors.Normalize(vmin=0.0, vmax=1.0)
                # LOOK FIX choose best type
		mplot = plt.scatter (times, eles, c=parms,   norm=norm,  s=lineSize, cmap=mptl.cm.hsv, lw=0) 
		#mplot = plt.plot (azis,eles  )  # LOOK FIX set line color
		numberplotted += 1
            else:
              if colorname == "" : 
                mplot = plt.scatter (times, eles, s=lineSize, color=cm.gist_ncar(0.5*svPRNIndex/numberColors) )  # alter colors
                numberplotted += 1
              else :
                mplot = plt.scatter(times, eles, s=lineSize, color=colorname)
                numberplotted += 1
        elif plottype == "Time-parameter plot":  
	    if True==doParmPlot:
                parms= plotDataArrays[3] 
                yvals=[]
		for pi in range (0, len(parms)):
		    yvals.append(parms[pi] )
                colmap=mptl.cm.hsv 
		prange= maxPV - minPV 
                # to set color legend and color of points correctly, need this: 
		pvtop = -999993.0
		pvbot= 999993.0
		for pi in range (0, len(parms)):
		    pnew=parms[pi]
		    if pnew>maxPV : pnew=maxPV;
		    if pnew<minPV : pnew=minPV;
		    pnew = (pnew - minPV) / prange  # shoves parm values into 0 to 1 range
		    parms[pi]=pnew
		    if parms[pi] > pvtop : pvtop = parms[pi] 
		    if parms[pi] < pvbot : pvbot = parms[pi] 
		norm=mptl.colors.Normalize(vmin=0.0, vmax=1.0)
                # plt.plot line style: in plt.plot function: k- means a connected black line;  solid linestyle ppp
                # see matplotlib.org/1.3.1/api/pyplot_api.html
                # ko means black circle point markers.  g green, b blue , etc.
		mplot = plt.plot (times, yvals, 'ko',  markersize=1.5 ) # 
		# LOOK sss for anubis try k- solid line mplot = plt.plot (times, yvals, 'k-',  markersize=1.5 )
		numberplotted += 1
            else :
		print "\n   Your anubisplot command needs a parameter input filename, to make a time-parameter plot.\n"
		sys.exit(1)
        elif   "GNSS_Band_Plot"==plottype : 
            # debug print " bandindex ="+ `bandindex`
            for yi in range (0, len(eles)):
                eles[yi]= bandindex * 0.6 # eles become Y axis values for each Svs line
	    if True==doParmPlot:
                parms= plotDataArrays[3] 
                colmap=mptl.cm.hsv 
		prange= maxPV - minPV 
		pvtop = -999993.0
		pvbot= 999993.0
		for pi in range (0, len(parms)):
		    pnew=parms[pi]
		    if pnew>maxPV : pnew=maxPV;
		    if pnew<minPV : pnew=minPV;
		    pnew = (pnew - minPV) / prange 
		    parms[pi]=pnew
		    if parms[pi] > pvtop : pvtop = parms[pi] 
		    if parms[pi] < pvbot : pvbot = parms[pi] 
		norm=mptl.colors.Normalize(vmin=0.0, vmax=1.0)
		mplot = plt.scatter (times, eles, c=parms,   norm=norm,  s=(0.4*lineSize), marker='s', cmap=mptl.cm.hsv, lw=0)
		numberplotted += 1
            else:
                mplot = plt.scatter(times, eles, s=(0.4*lineSize), color=cm.gist_ncar(1.0*svPRNIndex/numberColors)) # alter colors 
                numberplotted += 1
        else:
            print "  NOTE: plot type=_"+plottype+"_ is not recognized.  Exit. \n"
            sys.exit()

        if showLabel : # plot labels titles
            if plottype == "Skyplot" or plottype == "Azimuth-elevation plot": 
                lenaz=len(azis)
                # LOOK FIX match label color to line or symbol marker colors:
                ax.annotate (svid, (azis[ (lenaz/3)], eles[(lenaz/3)]) )
            elif plottype == "Time-elevation plot" or "GNSS_Band_Plot"==plottype:
                lenaz=len(times)
                ax.annotate (svid, ( times[(lenaz/3)], eles[(lenaz/3)] )                         )
            elif plottype == "Time-parameter plot" :  # ppp lll
                svnumb =  5 * (int(svid[1:])) # for an offset from start point
                ax.annotate (svid, (times[ svnumb ], parms[ svnumb ]) )
                #print "      put svid label at time=" + `times[0]` + "    y="+ `eles[0]`
        plotlist.append(mplot)
        svlist.append(svid)

    if True==doParmPlot and mplot!= None and plottype != "Time-parameter plot": 
        pvtop=1.0000
        pvbot=0.0
        dran=(pvtop-pvbot) /4
	m1= pvbot 
	m2= m1 + dran  
	m3= m1 + 2* dran 
	m4= m1 + 3*dran
	m5= pvtop
        lran=(maxPV-minPV) /4
	l1= minPV                       
	l2= l1 + lran  
	l3= l1 + 2* lran 
	l4= l1 + 3*lran
	l5= maxPV                      
        colorbar = plt.colorbar(mplot, shrink=0.85, pad=0.075) 
	colorbar.set_ticks     ([m1,m2,m3,m4,m5]) 
        colorbar.set_ticklabels([l1,l2,l3,l4,l5]) 
    #print "  Colors limited to values "+`minPV`+" to "+`maxPV`
    ax.grid(True)
    if plottype == "Skyplot" : 
	    ax.set_theta_zero_location('N')
	    ax.set_theta_direction(-1)
	    ax.set_rmax(90.0)
	    ax.set_yticks(range              (0, 90, 10))    # (min int, max int, increment) 
	    ax.set_yticklabels(map(str, range(90, 0, -10)))
    if plottype == "Azimuth-elevation plot":
            #                  min max   delta
	    # orig ax.set_xticks(range(-360, 405, 45))              
	    # orig ax.set_xticklabels(map(str, range(-360, 405, 45)))   
	    ax.set_xticks(range(0, 360, 30))              
	    # to set  0 to 360 degr axis range  see below at   pl plt.xlim(-5.0, 365.0)
            ax.set_xticklabels(map(str, range(0, 360, 30)) )  
	    ax.set_yticks(range              (0, 100, 10))                 
	    ax.set_yticklabels(map(str, range(0, 100, 10)))   
    if plottype == "Time-elevation plot" :
	    ax.set_xticks(range(0, 25, 3))              
	    ax.set_yticks(range              (0, 100, 10))                 
	    ax.set_yticklabels(map(str, range(0, 100, 10)))   
    if plottype=="Time-parameter plot" :        # ppp
	    ax.set_xticks(range(0, 25, 3))              
            spacing = int ( (maxPV-minPV) / 5.0)
            if 1>spacing : spacing = 1
	    ax.set_yticks(range              (int(minPV), int(maxPV+1.0), spacing))
	    ax.set_yticklabels(map(str, range(int(minPV), int(maxPV+1.0), spacing)))   
    if plottype == "GNSS_Band_Plot" :
	    ax.set_xticks(range(0, 25, 3))              
            plt.setp(ax.get_yticklabels(), visible=False)
    if showLegend :
        plots=tuple(plotlist)
        svs= tuple(svlist) # 3ss
    	plt.legend(plots,svs,scatterpoints=1,ncol=1,fontsize=8,markerscale=2.0, loc=2, bbox_to_anchor=(1.05, 1))

    title1= plottype+" for station "+anubisfile[:4]
    if "" != parmtype :
        title1= title1 + ".    "+parmtype+" " +parmname +"    Data file " +anubisfile #yyy
    elif "" == parmtype and plottype == "GNSS_Band_Plot" :
        # FIX title1= "   Visibility for station "+anubisfile[-12:-8]
        title1= "   Visibility for station "
    if plottype == "Skyplot" : 
        plt.suptitle(title1, y=0.977, fontsize=11)
    else:
        plt.suptitle(title1,         fontsize=10)
    # FIX doyear=anubisfile[-8:-5]
    doyear="YYYY"
    if len(doyear) < 3 : doyear=""
    if plottype == "Azimuth-elevation plot":
        # old title2= " \n Azimuth, degrees \n Data starts "+asciiStartTime+".  Day of year "+doyear
        title2= " \n Azimuth, degrees \n Data starts "+asciiStartTime
    elif plottype == "Time-elevation plot" or plottype=="Time-parameter plot" or "GNSS_Band_Plot"==plottype :
        # old title2=  " \n Time, hours of day \n Data starts "+asciiStartTime+".  Day of year "+doyear
        title2=  " \n Time, hours of day \n Data starts "+asciiStartTime
    else:
        # old title2= "Data starts "+asciiStartTime+".  Day of year "+doyear 
        title2= "Data starts "+asciiStartTime
    if plottype == "Skyplot" :
        if True==doParmPlot:
            plt.title(title2, y= -0.15, fontsize=11)  
        else:
            plt.title(title2, y= -0.11, fontsize=11)  
    else:
        plt.title(title2, y= -0.15, fontsize=11)  
    if plottype == "Azimuth-elevation plot" or plottype == "Time-elevation plot":
        plt.ylim(-2.0, 92.0)
        plt.ylabel('Elevation, degrees', fontsize=10)
    if plottype == "Azimuth-elevation plot":
        # old plt.xlim(-370.0, 370.0)
        plt.xlim(-5.0, 365.0)
    if plottype == "Time-elevation plot" or plottype=="Time-parameter plot" :
        # sett
        if minHour > -998.0 :
            minT = minHour
        if maxHour > -998.0 :
            maxT = maxHour
        plt.xlim(minT-1, maxT+1) 
    if plottype=="Time-parameter plot" : #ppp
        plt.ylim( (minPV), (maxPV))
    if  "GNSS_Band_Plot"==plottype :
        plt.ylim(-1.0, trackCountLimit+1.0)
        plt.xlim(minT-1, maxT+1) 
        plt.ylabel('SVs', fontsize=10)
    elapsedtime= (datetime.now() - starttime_t1)
    #if noprint!=1 : print "  Plotted "+`numberplotted`+" tracks in "+`(elapsedtime.total_seconds())`+" seconds. \n"

    filestarttime= strftime( '%Y%m%d_%H:%M:%S', gmtime())
    filename=svid+"_"+plottype[:10]+"_"+filestarttime+".png"

    # ============       To show the new plot in a pop-up window in the screen:
    plt.show() # Note: process pauses here until user clicks on something.
    # ============   end To show the new plot in a pop-up window in the screen.

    # OR do this:

    # ============      To automatically make and save plot in a PNG file ===============
    # Comment out the line plt.show() four lines above, i.e. #plt.show(), and uncomment this next line (remove the #):
    #plt.savefig(filename) 
    #   For more arguments to savefig(), see the section "matplotlib.pyplot.savefig(*args, **kwargs)" 
    #                                    in http://matplotlib.org/api/pyplot_api.html
    # ============      end to automatically save plot in a PNG file ===============

    # end function makePlot


# def Main program:  
global maxT
global minT
global asciiStartTime 
global lineSize
global noprint
global parmname 

lineSize = 2.5
noprint=0  # noprint=1 means do not print debug statements to the screen. 
print " " #  "    anubisplot.py March 20, 2016"
parmname ="   "

args = sys.argv 
lenargs = len(args)
if lenargs==1:
   print helptext
   sys.exit()
if lenargs==2:
   print "\n   Your anubisplot command is missing either a command option or an input filename.  "
   print "   Please read the help:"
   print helptext
   sys.exit(1)
plottype = " " 
# parse all the command ling arguments (which can be in any order):
for arg in args:
    if arg=="+skyplot" :
        plottype = "Skyplot" 
    if arg=="+azelplot" :
        plottype = "Azimuth-elevation plot"
    if arg=="+timeelplot":
        plottype = "Time-elevation plot"
    if arg=="+timeparmplot":
        plottype = "Time-parameter plot"
    if arg=="+bandplot":
        plottype = "GNSS_Band_Plot"
    if arg=="-R" and len(arg)==2:
        doglonass=False
    if arg=="-G" and len(arg)==2:
        dogps=False
    if arg=="-E" and len(arg)==2:
        dogalileo=False
    if arg=="-S" and len(arg)==2:
        dosbas=False
    if arg=="-J" and len(arg)==2:
        doqzss=False
    if arg=="-C" and len(arg)==2:
        dobeidou=False
    if arg[0:4]=='+pw=' and len(arg)>=5 : # set plot width in cm; matplotlib uses inches so / 2.54
	widthDistance = float(arg[4:]) / 2.54
    if arg[0:4]=='+pd=' and len(arg)>=5   : # set pixel density per cm (matplotlib uses dpi or dots per inch)
	pixeldensity = int( 2.54 * int(arg[4:]))
    if arg[0:5]=='+tcl=' and len(arg)>=6 :
	trackCountLimit= int(arg[5:])
    if arg[0:10]=='+colorMax=' and len(arg)>=11 :
	colorMax = float(arg[10:])
    if arg[0:10]=='+colorMin=' and len(arg)>=11 :
	colorMin = float(arg[10:])
    if arg[0:9]=='+minHour=' and len(arg)>=10 :
	minHour = float(arg[9:])
    if arg[0:9]=='+maxHour=' and len(arg)>=10 :
	maxHour = float(arg[9:])
    if arg[0:7]=='+msize=' and len(arg)>=8 :
	lineSize= float(arg[7:])
    if arg[0:7]=='+color=' and len(arg)>=9 :
	colorname = arg[7:]
    if arg=="+legend" :
        showLegend=True
    if arg=="-tracklabels" :
        showLabel=False
    if arg[0:2]=="+G" and len(arg)>2:
        liststr=arg[2:]   
        if "," in liststr:
		svnumbers=liststr.split(",")
		for svn in svnumbers:
			doShowSVslist.append("G"+svn)
        elif "-" in liststr:
		numbers=liststr.split("-")		
                i1=int(numbers[0])
                i2=int(numbers[1])
		for numb in range(i1, (i2+1)) :
                        svn = ""+`numb` 
                        if len(svn)==1 : svn = "0"+svn
			doShowSVslist.append("G"+svn)
        else:
           	doShowSVslist.append("G"+liststr)
    if arg[0:2]=="+R" and len(arg)>2:
        liststr=arg[2:]   
        if "," in liststr:
		numbers=liststr.split(",")		
		for svn in numbers:
			doShowSVslist.append("R"+svn)
        elif "-" in liststr:
		numbers=liststr.split("-")		
                i1=int(numbers[0])
                i2=int(numbers[1])
		for svn in range(i1, (i2+1)) :
			doShowSVslist.append("R"+`svn`)
        else:
           	doShowSVslist.append("R"+liststr)
    if arg[0:2]=="+J" and len(arg)>2:
        liststr=arg[2:]   
        if "," in liststr:
		numbers=liststr.split(",")		
		for svn in numbers:
			doShowSVslist.append("J"+svn)
        elif "-" in liststr:
		numbers=liststr.split("-")		
                i1=int(numbers[0])
                i2=int(numbers[1])
		for svn in range(i1, (i2+1)) :
			doShowSVslist.append("J"+`svn`)
        else:
           	doShowSVslist.append("J"+liststr)
    # find the anubis file of results aaaa
    if arg[-4:]==".xtr": 
            anubisfile=arg
    if arg[0:2]=="+M" and 4==len(arg):
            parmname=arg[1:] # Like M1C
            #print "   do parm "+parmname  # debug 
            # orig parmtype="Multipath combination"
            parmtype="Parameter "
	    doParmPlot=True # pppp
    if arg[0:2]=="+S" and 4==len(arg):
            parmname=arg[1:] # Like 
            #print "   do parm "+parmname  # debug 
            parmtype="Signal to Noise"
	    doParmPlot=True


    old='''
    if len(arg)>5 and arg[-4]==".":  
        files.append(arg)
        if arg[-4:]==".azi": 
            anubisfile=arg
        if arg[-4:]==".ele": 
            elefile=arg
        if arg[-4:-2]==".i": 
            parmfile=arg
            parmtype="Ionspheric Delay (m)"
        if arg[-4:-2]==".d": 
            parmfile=arg
            parmtype="Ionspheric Delay Derivative (m/min)"
        if arg[-4:-1]==".sn": 
            parmfile=arg
            parmtype="Signal to Noise"
        if arg[-4:-2]==".m": 
            parmfile=arg
            parmtype="Multipath combination"

        if parmtype!="":
	        doParmPlot=True
        '''


if plottype == "GNSS_Band_Plot" :
    lineSize *= 10.0 
elif (plottype == "Skyplot" or plottype == "Azimuth-elevation plot") and doParmPlot :
    lineSize *= 2 
elif (plottype ==  "Time-elevation plot") and doParmPlot :
    lineSize *= 3 
elif (plottype ==  "Time-parameter plot") and doParmPlot :
    lineSize *= 3 

if noprint!=1 : print "      Anubisplot: do "+ plottype +" with file "+ anubisfile 

readAnubisXtrFile ()

for tuples in SVpositionList:
    svid =tuples[0]
    if svid not in SVidList :
        #debug print "    plotting: new SV to use "+svid
        SVidList.append(svid)
SVidList.sort()

# debug print    "  There are "+`len(SVidList)`+" SVs with plottable data, and " \
#    +`len(SVpositionList)`+" sets of SV, time, azimuth, and elevation."

noplot=""
if doglonass!=True : noplot+= " GLONASS"
if dogps!=True     : noplot+= " GPS"
if dogalileo!=True : noplot+= " Galileo"
if dosbas!=True    : noplot+= " SBAS"
if doqzss!=True    : noplot+= " QZSS"
if dobeidou!=True  : noplot+= " Beidou"
if "" != noplot : print "\n      Will not plot SVs from constellation(s): "+noplot
if doParmPlot: 
    if len(SVparmidList)>0:
       if noprint!=1 : print "  There are "+`len(SVparmidList)`+" SVs with parm values, and "+`len(SVparmList)`+" sets of SV parm values."

makePlot() 

#end main
