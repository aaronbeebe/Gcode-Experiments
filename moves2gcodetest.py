"""
This is an amateur, inelegant script that should (ideally) take a text export of moves data and turn it into Gcode. 
Who knows if it will work for more than the single file I've been testing it on.
"""

import sys
from decimal import *
import re

listoforiginalXcoordinates=[]
listoforiginalYcoordinates=[]
X_moved=[]
Y_moved=[]
finalxlist=[]
finalylist=[]
gcoded=[]

def convert_to_gcode(filename):
	regex = ".+?\{\"lon\":(.*?),.*?\"lat\":(.*?)\}"
	line = open(filename, 'r').read()
	coordinates = re.findall(regex, line)
	for d in coordinates:
		gcoded.append(("G1 X" + d[0]) +  " Y" + (d[1]) + "\n")

def extract(iterable): #run this first (in a loop). It goes through the G1 X(a) Y(b) lines and extracts a list of X coordinates and a list of Y coordinates as Decimals.
	extracted_coordinate = iterable.split()
	X=(Decimal(extracted_coordinate[1][1:][:9].zfill(9)))
	Y=(Decimal(0) - Decimal(newy) - Decimal(extracted_coordinate[2][1:][:9].zfill(9)))
	listoforiginalXcoordinates.append(Decimal(X))
	listoforiginalYcoordinates.append(Decimal(Y))
	
def get_ratio(listx, listy): #run this next (by itself). It looks at the two lists and finds the ratio of the old size to the new size.
	if max(listx) > max(listy): #picks the largest dimension of the original and saves it and it's corresponding minimum for use in the ratio.
		maxvalue = max(listx)
		minvalue = min(listx) 
		new = newx
	else:
		maxvalue = max(listy)
		minvalue = min(listy)
		new = newy
	ratio = new / (maxvalue - minvalue + Decimal(0.0001))
	return ratio

def move(iterable): #relocates the design to 0.0001 on both axes.
	moved = []
	for i in iterable:
		i = i - min(iterable) + Decimal(0.0001)
		moved.append(i)
	return moved	

def resize(iterable): #applies the ratio and makes any vectors that are longer than 50mm "0".
	finallist = []
	nextline = iterable[1]*ratio
	vectorlength = ratio * (max(X_moved) - min(Y_moved) + Decimal(0.0001)) / 11
	for i in iterable:
		thisline = i*ratio
		if (nextline > (thisline + Decimal(vectorlength))) or (nextline < (thisline - Decimal(vectorlength))):
			finalwritten = Decimal(300) + thisline
		else:
			finalwritten = thisline
		finallist.append(str(finalwritten)[:9].zfill(9))
		nextline = thisline
	return(finallist)	

def reorient(y):
	reorientedy = Decimal(newy) - Decimal(y)
	return reorientedy

###########################################

#The action starts here - with calling the original text dump file.

if (len(sys.argv) < 2):
	print ('Please define the original file... (for example "python RoundGcode.py myfile.gco")')
	sys.exit("File not defined. Exiting...")

filename = sys.argv[1] 

newfile = open(filename+'.gcode','w')

convert_to_gcode(filename)

newx = Decimal(input("Widest value in mm: "))
newy = Decimal(input("Tallest value in mm: "))

for d in gcoded:	
	extract(d)
X_moved = move(listoforiginalXcoordinates)
Y_moved = move(listoforiginalYcoordinates)

ratio=get_ratio(X_moved, Y_moved)	
finalxlist = resize(X_moved)
finalylist = resize(Y_moved)

finallist = []
firstline = (finalxlist[0], finalylist[0])
secondline = (finalxlist[1], finalylist[1])
thirdline = (finalxlist[2], finalylist[2])
newfile.write("G1 Z5\nG1 X" + str(firstline[0]) + " Y" + str(firstline[1]) + "\nG1 Z0\n")
for a, b in zip(finalxlist, finalylist):
	thirdline = Decimal(a), Decimal(b)
	newthirdline0 = thirdline[0]
	newthirdline1 = thirdline[1]
	if thirdline[0] >= Decimal(300) or thirdline[1] >= Decimal(300):
		if thirdline[0] >= Decimal(300): 
			newthirdline0 = (thirdline[0] - Decimal(300))
		if thirdline[1] >= Decimal(300):
			newthirdline1 = (thirdline[1] - Decimal(300))
		newfile.write("G1 Z5\nG1 X" + str(newthirdline0) + " Y" + str(newthirdline1) + "\nG1 Z0\n")
	elif thirdline == secondline:
		newfile.write("")
	else:
		newfile.write('G1 X{0} Y{1}\n'.format(a, b))
	firstline = secondline
	secondline = thirdline
newfile.write("G1 Z5\nG1 X0 Y0\n")	

print ('Your new file is '+filename+'.gcode')
newfile.close()	