  
""" 
 Unit: more points 
 Project: more points 
 Created: 15.04.2013, DJW 
 Description: 
  
 morepoints.py 
  
 Copyright (C) 2013 dan white 
  
 License: GPL v3. 
  
 This program is free software: you can redistribute it and/or modify 
    it under the terms of the GNU General Public License as published by 
    the Free Software Foundation, either version 3 of the License, or 
    (at your option) any later version. 
  
    This program is distributed in the hope that it will be useful, 
    but WITHOUT ANY WARRANTY; without even the implied warranty of 
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
    GNU General Public License for more details. 
  
    You should have received a copy of the GNU General Public License 
    along with this program.  If not, see <http://www.gnu.org/licenses/>. 
  
"""
__author__ = "dan white"
__version__ = "$Revision: 1.0 $"
__date__ = "$Date: 2013/05/15 13:42:03 $"
  
          
  
""" 
more points, by dan white 
  
What does it need to do?: 
parse a text file created by saving a points list in softworx, where 
points list generated from plate tab, generate points, one point per well, 
then create a new points list, with multiple new points per point, 
as if to create multiple fields of view per well of a microtiter plate: 
  
1) read x,z,y poionts into a list of lists 
2) calculate clusters of points around each read point in a.... ummmm... square grid, 
of user defined n by n dims, and user defines offset between fields of view.  
3) output new points as a softworx format points, retaining Well ID field. 
  
Lets, like, do it:  
  
Import the python modules we need. 
"""
  
#use optparse for command line option parsing, ie. to define log file and output file names 
from optparse import OptionParser   
""" 
1) softworx point list, filename extension .pts, from generate button in plate tab looks like this: 
  
"""
testPoints ="""\
   1:  +49500.00  -31500.00    -70.58  A01 
   2:  +40500.00  -31500.00    -70.58  A02 
   3:  +31500.00  -31500.00    -70.58  A03 
   4:  +22500.00  -31500.00    -70.58  A04 
   5:  +13500.00  -31500.00    -70.58  A05 
   6:   +4500.00  -31500.00    -70.58  A06 
   7:   -4500.00  -31500.00    -70.58  A07 
   8:  -13500.00  -31500.00    -70.58  A08 
   9:  -22500.00  -31500.00    -70.58  A09 
  10:  -31500.00  -31500.00    -70.58  A10 
  11:  -40500.00  -31500.00    -70.58  A11 
  12:  -49500.00  -31500.00    -70.58  A12 
  13:  -49500.00  -22500.00    -70.58  B12 
  14:  -40500.00  -22500.00    -70.58  B11 
  15:  -31500.00  -22500.00    -70.58  B10 
  16:  -22500.00  -22500.00    -70.58  B09 
  17:  -13500.00  -22500.00    -70.58  B08 
  18:   -4500.00  -22500.00    -70.58  B07 
  19:   +4500.00  -22500.00    -70.58  B06 
  20:  +13500.00  -22500.00    -70.58  B05 
  21:  +22500.00  -22500.00    -70.58  B04 
  22:  +31500.00  -22500.00    -70.58  B03 
  23:  +40500.00  -22500.00    -70.58  B02 
  24:  +49500.00  -22500.00    -70.58  B01 
  25:  +49500.00  -13500.00    -70.58  C01""".splitlines() 
  
""" 
  
etc..... 
  
2) Read .pts file (or test data) in one go, and use readlines to get each line, one for each point. 
use command line options to set infile and outfile, field separation and number of rows and columns. 
"""
  
#here we use optparse python module to make a
#standard unix like command line interface that
#does help and reads command line arguments. 


commandLineUsage = "usage: %prog -i INFILE -o OUTFILE -s SEPARATION -n ROWSANDCOLUMNS" 
commandLineOptionParser = OptionParser(usage=commandLineUsage)  
                                            
commandLineOptionParser.add_option("-i", "--infile",  
                                   action="store", type="string", dest="infile", 
                                   help="define name of input INFILE", metavar="INFILE") 
commandLineOptionParser.add_option("-o", "--outfile",  
                                   action="store", type="string", dest="outfile", 
                                   help="define name of file for OUTFILE", metavar="OUTFILE") 
commandLineOptionParser.add_option("-s", "--separation",  
                                   action="store", type="string", dest="separation", 
                                   help="define separation of fields of view in each well", metavar="SEPARATION") 
commandLineOptionParser.add_option("-n", "--rowsandcolumns",  
                                   action="store", type="string", dest="rowsandcolumns", 
                                   help="number of rows and columns of fields of view per well", metavar="NUMBEROFROWSCOLUMNS") 
# parses the command line and puts filenames and parameters supplied in 
# commandLineOptionParser.infile and commandLineOptionParser.outfile 
# and  commandLineOptionParser.separation and commandLineOptionParser.rowsandcolumns 
(commandLineOptions, args) = commandLineOptionParser.parse_args() 
  
print(commandLineOptions.infile, "is the input file")
print(commandLineOptions.outfile, "is the output file") 
print(commandLineOptions.separation, "is the fields of view spearation in microns") 
print(commandLineOptions.rowsandcolumns, "is the number of columns and rows panels per well") 
print(args, "are the left over command line option arguments. There should be none!")

#check that both input file and output file names,
# and spearation and rowsandcolumns are specified on command line 
if (commandLineOptions.infile == None) or (commandLineOptions.outfile == None): 
    commandLineOptionParser.error("you must give command line options: -i INFILE -o OUTFILE") 
if (commandLineOptions.separation == None) or (commandLineOptions.rowsandcolumns == None): 
    commandLineOptionParser.error("you must give command line options: -s SEPRATION -n ROWSANDCOLUMNS")
  

# open and read the original .pts file
originalPointsFile = open(commandLineOptions.infile)
originalPoints = originalPointsFile.readlines()

print(originalPoints)


#comment out and use command line options to set these variables.
#rowsandcolumns = 2
#separation = 100 

# read the number of rows and columns and panel separation from cmd line args.
rowsandcolumns = commandLineOptions.rowsandcolumns
separation = commandLineOptions.separation

"""
  
        new panel position calc maths: 
  
2x2 set of panels in a well, point coordinate x,y. 
panel separation is 1. 
  
top left panel point is at 
x-(1/2), y+(1/2) 
  
what is the general rule to make the panels position matrix? 
eg. in x direction: 
1   0/2 
2  -1/2 , +1/2 
3  -2/2 , 0/2 , +2/2 
4  -3/2 , -1/2 , +1/2 , +3/2 
5  -4/2 , -2/2 , 0/2 , +2/2 , +4/2 
  
precalculate the matrix of panel positions: 
list of panel locations is centred around zero (actually really the well point position), 
and has rowsandcolumns entries. 
make list of integers 0 through rowsandcolumns-1 
offet the values in the list by -(rowsandcolumns/2)+0.5
multiply the values by user supplied separation in microns 
duplicate the list, so we have an x and a y list to iterate through. 
"""

# make incremental list of integers from zero to value of rowsandcolumns-1
listOfXPanels = list(range(0, int(rowsandcolumns))) 
print("this is the list of x panel positions " , listOfXPanels)

#shift the list values to centre over zero
#newList = [i/myInt for i in myList]
listOfXPanels = [(i-(float(rowsandcolumns)/2)+0.5) for i in listOfXPanels]
print("shifted x panels around zero ", listOfXPanels)

listOfXPanels = [i*float(separation) for i in listOfXPanels] 

print("this is the shifted, separated, x panel position centered on zero ", listOfXPanels)

# list of y panels is exactly the same as in x.
listOfYPanels = listOfXPanels

""" 
in the loop going through the original well point positions in microns, 
add the original well point position to the pre calculated values in the list. 
  
eg. 
for wellPoint in wellPointsList 
   for xPanel in listOfXPanels 
      for yPanel in listOfYPanels 
              
  
  
3) For each line of the file 
  
>>> line="a sentence with a few words" 
>>> line.split() 
['a', 'sentence', 'with', 'a', 'few', 'words'] 
  
"   1:  +49500.00  -31500.00    -70.58  A01" 
goes to 
['1:', '+49500.00', '-31500.00', '-70.58', 'A01'] 
  
4) work on lines of the input data, each line is a point as  a list of values.
   make a new point for each point and panel in each well. 

5)   append the new points (each is a list) into another master list, allNewPoints, 
        with consecutive numbers in 1st column, retaining Well ID eg. B01. 
          
    2nd and 3rd list entries are the x and z coordinates respectively. 
    z doesnt matter, just reuse what is there, autofocus will fix it. 
    remember list indices start counting at 0, list[0] is the first item 
      
    newPointLine is a placeholder list containing the new point coordinates 
    Append this into the allNewPoints  master list of lists.

    inserting the right number of spaces? 
    modify well ID by adding underscore and a number for the panel ID
    for that well panel. eg C01_0_5
    i wonder if softworx will accept well IDs like A01_4_9?
    Good news! Yes it like those just fine, so we will do it like that!
"""

allNewPoints = [] 
for wellPoint in originalPoints:
#for wellPoint in testPoints:
   splitPointLine = wellPoint.split()
   print("the split point line is ", splitPointLine)
   for idxX, xPanel in enumerate(listOfXPanels):
      #print("iterate through x panels")
      for idxY, yPanel in enumerate(listOfYPanels):
         #print("iterate through y panels")
         # initialise new list with dummy values of right types
         newPointLine = ["a","2","3","4","e"]
         newPointLine[0] = splitPointLine[0] 
         newPointLine[1] = float(splitPointLine[1]) + xPanel
         newPointLine[2] = float(splitPointLine[2]) + yPanel

         # z position of point can be left as was using this line
         #newPointLine[3] = splitPointLine[3]

         #or z position can be set to zero...
         # so user sets sets the stage z position to before starting
         # and sets the correct focus at first well using the objective turret focus knob on the stand
         newPointLine[3] = 0.00

         # add position of panel to well ID by adding index in the 2 looped through
         # x and y panel lists to the end of the Well ID. 
         newPointLine[4] = splitPointLine[4] + "_" + str(idxX) + "_" + str(idxY)

         #print(newPointLine)
         
         allNewPoints.append(newPointLine) 

# need to re number the point IDs, so they are consecutive,
# counting up from  1, not 0, with a colon at the end
# and all the panels in a well dont have the same point ID!

for index, point in enumerate(allNewPoints):
   point[0] = str(index+1) + ":"

# print the new points, point by point - are they right?
for point in allNewPoints:
   print(point)

"""  
6) Write .pst file containing all the new points from the allNewPoints. 
    line by line iterating though the list of lists, 
"""

outputFile = open(commandLineOptions.outfile, 'w+')    # open the results file in write mode

# write the list of values for each point as a text string, separated by a space, newline at end.
for point in allNewPoints:
   for item in point:
      outputFile.write(' ')
      outputFile.write(str(item))
   outputFile.write('\n')

outputFile.close()     # its nice to close the file. 

print("Done! Have fun imaging all those points!")
