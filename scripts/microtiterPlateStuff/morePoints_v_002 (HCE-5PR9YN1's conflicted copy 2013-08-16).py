  
"""  
 Created: 15.04.2013, DJW
 Description: 
  
 morepoints.py 
  
 Copyright (C) 2013 daniel james white 
  
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
__version__ = "$Revision: 2.0 $"
__date__ = "$Date: 2013/08/13 14:00:00 $"
  
          
  
""" 
more points, by dan white 
  
What does it need to do?: 
parse a text file created by saving a points list in SoftWoRx, where 
points list generated from
Experiment Designer - Plate tab - generate points (one point per well), 
then create a new points list, with multiple new points per point, 
as if to create multiple fields of view per well of a microtiter plate: 
  
1) read x,z,y points into a list of lists 
2) calculate clusters of points around each read point in eg. a square grid (or something else)
of user defined n by n dims, and user defined seapration between fields of view.  
3) output new points as a softworx format points list, retaining Well ID field
    (not that Well ID seems to get used in filenames,
    maybe there is a way to make softworx do that...?)
  
Let's, like, do it:  
"""  


#Import the python modules we need. 
 
#use optparse for command line option parsing, ie. to define log file and output file names 
from optparse import OptionParser


# The main function calls the other functions as required by the command line input parameters. 
# so here is the main() function that controls overall workflow. 
def main():
   inputParams = getInputParams()

   # open and read the original .pts file 
   originalPointsFile = open(inputParams['infile'])
   originalPoints = originalPointsFile.readlines()
   #print(originalPoints)
   
   # decide what pattern of panels to use controlled by -p commadn line parameter
   # there are several paterns psooible, so need to define their names so we can
   # check for valid ones we have a pattern generation funtion for and complain if not.   
   validPatterns = ["Square", "Cross"]

   # now check the string entered as pattern command line argument is one we have a method for.
   if inputParams['pattern'] in validPatterns:
      thePatternName = inputParams['pattern']
      patternFunctionName = "make"+thePatternName+"Panels"
      print(patternFunctionName)
      panelPattern = eval(patternFunctionName)(inputParams['rowsandcolumns'], inputParams['separation'])
   elif print("invalid pattern"):
                 return

   # make the new panel points and get the points list computed. 
   allNewPoints = makeAllNewPoints(originalPoints, panelPattern)

   # fix point numbering of all the new points, so all unique. 
   renumberedNewPoints = renumberNewPoints(allNewPoints)

   writeOutputFile(renumberedNewPoints, inputParams)
   print("output file written")


"""  
Write .pst file containing all the new points from the allNewPoints.
line by line iterating though the list of lists, 
lets use a function called writeOutputFile to do that
"""
def writeOutputFile(renumberedNewPoints, inputParams):
   outputFile = open(inputParams['outfile'], 'w+')    # open the results file in write mode

   # write the list of values for each point as a text string, separated by a space, newline at end.
   for point in renumberedNewPoints:
      for item in point:
         outputFile.write(' ')
         outputFile.write(str(item))
      outputFile.write('\n')

   outputFile.close()     # its nice to close the file. 





""" 
1) softworx point list, filename extension .pts,
    from generate button in plate tab, looks like this: 
  
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
  
"""
here we use optparse python module to make a
standard unix like command line interface that
does help and reads command line arguments.

turn this into a function called getInputParams
which returns a dictionary of key vlaue pairs
containing the user parameters for the script
"""

def getInputParams():                        
   commandLineUsage = "usage: %prog -i INFILE -o OUTFILE -s SEPARATION -n ROWSANDCOLUMNS -p PATTERN" 
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
   commandLineOptionParser.add_option("-p", "--pattern",  
                                      action="store", type="string", dest="pattern", 
                                      help="pattern for panels, can be square or cross", metavar="PATTERN") 
   # parses the command line and puts filenames and parameters supplied in object
   # commandLineOptionParser.theParameter, eg. commandLineOptionParser.infile
   (commandLineOptions, args) = commandLineOptionParser.parse_args() 
     
   print(commandLineOptions.infile, "is the input file")
   print(commandLineOptions.outfile, "is the output file") 
   print(commandLineOptions.separation, "is the fields of view separation in microns") 
   print(commandLineOptions.rowsandcolumns, "is the number of columns and rows panels per well") 
   print(commandLineOptions.pattern, "is the pattern for the panels")
   print(args, "are the left over command line option arguments. There should be none!")

   #check that all of input file, output file,
   # separation, rowsandcolumns and pattern are specified on command line 
   if commandLineOptions.infile == None or commandLineOptions.outfile == None: 
       commandLineOptionParser.error("you must give command line options: -i INFILE -o OUTFILE") 
   if commandLineOptions.separation == None or commandLineOptions.rowsandcolumns == None: 
       commandLineOptionParser.error("you must give command line options: -s SEPRATION -n ROWSANDCOLUMNS")
   if commandLineOptions.pattern == None:
       commandLineOptionParser.error("You must give a valid command line option: -p PATTERN")
   if commandLineOptions.pattern != "square" and commandLineOptions.pattern != "cross":
       commandLineOptionParser.error("You must give a valid command line option: -p PATTERN")


   # read the number of rows and columns, panel separation and pattern from cmd line args
   # and the infile out file params , and return their values in a dictionary.
   infile =          commandLineOptions.infile
   outfile =         commandLineOptions.outfile
   rowsandcolumns =  commandLineOptions.rowsandcolumns
   separation =      commandLineOptions.separation
   pattern =         commandLineOptions.pattern

   inputParams = {'infile':infile,
                  'outfile':outfile,
                  'separation':separation,
                  'rowsandcolumns':rowsandcolumns,
                  'pattern':pattern}
   return inputParams
                        
"""
Below are Functions for making distributions of fields of view -
panels for a microtiter plate well.
Need to input the appropriate command line parameters
for that pattern type of panel distribution
and create a panelPatternList of structure, list of x,y pairs lists:
[ [relativeXposn,relativeYposn], [x2,y2] , etc. ]

"""

"""
              Maths for making a certain number of positions on a line
              centered around zero: oneDListOfPanels
              
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

i need a function for creating the one dimensional listOfPanels 
which i can use in square grid, upright cross (and perhaps also twice for rectangular grid)
"""
def oneDListOfPanels(rowsandcolumns):
   # make incremental list of integers from zero to value of rowsandcolumns-1 
   listOfPanels = list(range(0, int(rowsandcolumns))) 
   print("this is the list of panel positions " , listOfPanels)

   #shift the list values to centre over zero
   #newList = [i/myInt for i in myList]
   listOfPanels = [(i-(float(rowsandcolumns)/2)+0.5) for i in listOfPanels]
   print("shifted panels around zero ", listOfPanels)   
   return listOfPanels



"""
      Math for separating panel positions according to the
      command line parameter separation
      function called panelsSeparation
"""
def panelsSeparation(separation, listOfPanels):
   
   # Separate the panels according to separation command line parameter
   listOfSeparatedPanels = list(i*float(separation) for i in listOfPanels)
   print("this is the separation ", separation)
   print("this is the shifted, separated, panel position centered on zero ", listOfSeparatedPanels)
   return listOfSeparatedPanels


"""
        panel position calc maths
        for a + pattern of panels, an upright cross (but not a heavy one):

upright cross of 2x2 is same as a square grid, but 3x3 isnt, as it has only 5 fields. 

its just the way we iterate through the positions in 2 dimensions to make the list of panels
in an upright cross as we only take the middle row or column,
and must remove the duplicated centre panel if number of rowsandcolumns is odd.
"""
def makeCrossPanels(rowsandcolumns, separation):
   listOfVerticalPanels = oneDListOfPanels(rowsandcolumns)
   listOfSeparatedVerticalPanels = panelsSeparation(separation, listOfVerticalPanels)

   # list of horizontal panels is exactly the same as vertical
   # unless the number is odd, in which case we need to remove the duplicate middle panel.

   # first make a new list witg a copy of the other list ocntents,
   # Note: not only a reference to the original list! Use list(thing), not thingb = thinga
   listOfSeparatedHorizontalPanels = list(listOfSeparatedVerticalPanels)
   if int(rowsandcolumns) % 2 == 1:  # if it's odd
      listLength = len(listOfSeparatedVerticalPanels)
      # delete the middle panel position, as it will be made in the other direction already. 
      middlePanel = int( (listLength / 2) - 0.5 )
      del listOfSeparatedVerticalPanels[middlePanel]
      print("vertical panels and horiz panels ", listOfSeparatedVerticalPanels, listOfSeparatedHorizontalPanels)

   # now make the panels, with horizontal using zero for y position
   # and vertical using zero for x position. Thats a cross.
   panelPatternList = []
   for verticalPanel in listOfSeparatedVerticalPanels:
      thePanel = [0.00, verticalPanel]
      print(thePanel)
      panelPatternList.append(thePanel)
   for horizontalPanel in listOfSeparatedHorizontalPanels:
      thePanel = [horizontalPanel, 0.00]
      print(thePanel)
      panelPatternList.append(thePanel)
   return panelPatternList

"""
  
        panel position calc maths
        for a square matrix of panels: 

Get the one dimensional panel positions using oneDListOfPanels function
multiply the values by user supplied separation in microns 
duplicate the list, so we have an x and a y list to iterate through. 

turn the below into a function that
takes input params and makes the appropriate
panelPatternList for use to make the new points list, allNewPoints
"""

def makeSquarePanels(rowsandcolumns, separation):

   listOfXPanels = oneDListOfPanels(rowsandcolumns)
   listOfSeparatedXPanels = panelsSeparation(separation, listOfXPanels)
   
   # list of y panels is exactly the same as in x.
   listOfSeparatedYPanels = list(listOfSeparatedXPanels)

   panelPatternList = []
   for xPanel in listOfSeparatedXPanels:
      for yPanel in listOfSeparatedYPanels:
         thePanel = [xPanel,yPanel]
         print(thePanel)
         panelPatternList.append(thePanel)
   print("pannel pattern list is ")
   print(panelPatternList)

   # should i return the result list? sure!
   return panelPatternList 



""" 
in the loop going through the original well point positions in microns, 
add the original well point position to the pre calculated values in the list. 
  
eg. 
for wellPoint in wellPointsList 
   for xyPanel in listOfXYPanels     
  
  
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
    set Z value to 0.00, so autofocus will fix it. 
    remember list indices start counting at 0, list[0] is the first item 
      
    newPointLine is a placeholder list containing the new point coordinates 
    Append this into the allNewPoints  master list of lists.

    inserting the right number of spaces? 
    modify well ID by adding underscore and a number for the panel ID
    for that well panel. eg C01_0_5
    i wonder if softworx will accept well IDs like A01_4_9?
    Good news! Yes it likes those just fine, so we will do it like that!

A function called makeAllNewPoints
which takes the output of a panels creation function, a panelPatternList
and creates an allNewPoints list
"""
def makeAllNewPoints(originalPoints, panelPatternList):
   allNewPoints = [] 
   for wellPoint in originalPoints:
   #for wellPoint in testPoints:
      splitPointLine = wellPoint.split()
      #print("the split point line is ", splitPointLine)

      for panelIndex, xyPanel in enumerate(panelPatternList):
      #print("iterate through list of [x,y] panels in well panel pattern list")
     
         # initialise new list with dummy values of right types
         newPointLine = ["a","2","3","4","e"]
         newPointLine[0] = splitPointLine[0] 
         newPointLine[1] = float(splitPointLine[1]) + float(xyPanel[0])
         newPointLine[2] = float(splitPointLine[2]) + float(xyPanel[1])

         # z position of point can be left as was using this line
         #newPointLine[3] = splitPointLine[3]

         # or z position can be set to zero...
         # so user sets sets the stage z position to 0.00 before starting
         # and sets the correct focus at first well using the objective turret focus knob on the stand
         newPointLine[3] = 0.00

         # add ID of panel to well ID by adding list index as a string
         newPointLine[4] = splitPointLine[4] + "_" + str(panelIndex+1)
         #print("the new point is ", newPointLine)

         allNewPoints.append(newPointLine)

   #print("these are all the new points ", allNewPoints)
         
   # do i need to return the result? Oh Yes!
   return allNewPoints



"""
need to re number the new point IDs, so they are consecutive,
counting up from  1, not 0, with a colon at the end
and all the panels in a well dont have the same point ID!

lets have a function for this called renumberNewPoints
"""
def renumberNewPoints(allNewPoints):
   for index, point in enumerate(allNewPoints):
      point[0] = str(index+1) + ":"
      #print("the renumbered point is ", point)

   # do i need to return the result?
   allRenumberedNewPoints = allNewPoints
   return allRenumberedNewPoints



# now we have defined all the functions, run the main function to actually do sometihng!
main()
print("Done! Have fun imaging all those points!")
