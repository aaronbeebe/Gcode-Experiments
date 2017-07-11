#import libraries
import sys
from decimal import *


#Create the function to extract the X and Y values from a file that's assumed to have the format "G1 X[a] Y[b]""
#First break each line from the file into separate items at the spaces.
#the extracted coordinate is filled with zeros to the left (zfill) padding it to 9 places and eliminating the first character (the X or Y).
#(f it's negative, it get's moved)
#Returns the extracted X and Y coordinates as strings.
def extract(coordinate):
	extracted_coordinate = coordinate.split()
	X=extracted_coordinate[1][1:][:9].zfill(9)
	print(X)
	Y=extracted_coordinate[2][1:][:9].zfill(9)
	print(Y)
	if Decimal(X)<0:
		X=Decimal(X) + Decimal(100.00000) 
	if Decimal(Y)<0:
		Y=Decimal(Y) + Decimal(100.00000)
	#newfile.write(str(X) + ", " + str(Y) +"\n")
	print("extracted X and Y are " + str(X) + " and " + str(Y))	
	return(X, Y)


#Create the function that preserves the largest number
#THE PROBLEM HERE IS THAT THE SCRIPT LOOPS THROUGH THE ENTIRE FILE EVERY LINE.
def find_largest(opened_file, axis):
	largest = Decimal(0)
	with open(filename) as opened_file:
		for d in opened_file:
			extracted = Decimal(extract(d)[axis])
			if largest < extracted:
				largest = extracted	
		#print(largest)
		#newfile.write(str(largest)) 
		return(largest)	

#Create the function that preserves the smallest number
#THE PROBLEM HERE IS THAT THE SCRIPT LOOPS THROUGH THE ENTIRE FILE EVERY LINE.
def find_smallest(opened_file, axis):
	smallest = Decimal(1000000.0)
	with open(filename) as opened_file:	
		for d in opened_file:
			extracted = Decimal(extract(d)[axis])
			if smallest > extracted:
				smallest = extracted			
		#print(smallest)
		#newfile.write(str(smallest))
		return(smallest)


#Create the function that finds the ratio to do the resizing
def find_ratio(opened_file):
	smallestx = find_smallest(opened_file, 0)
	#print("smallestx = " + str(smallestx))
	largestx = find_largest(opened_file, 0)
	#print("largestx = " + str(largestx))
	smallesty = find_smallest(opened_file, 1)
	#print("smallesty = " + str(smallesty))
	largesty = find_largest(opened_file, 1)
	#print("largesty = " + str(largesty))
	oldx = largestx - smallestx #(approx 2.0)
	oldy = largesty - smallesty #approx 2.0)
	#print("largestx - smallestx is " + str(oldx))
	#print("largesty - smallesty is " + str(oldy))
	if oldx > oldy:
		oldsize = oldx
		papersize = (Decimal(paperwidth) - Decimal(origin))
	else:
		oldsize = oldy 
		papersize = (Decimal(paperheight) - Decimal(origin))
	newratio = Decimal(papersize) / Decimal(oldsize)
	#print(newratio)
	return(newratio)

	# at a ratio of 2, points 6,.5 and .25,4 become 12,1 and .5,8, which then becomes 24,2 and 1,16.


def resize(old_coordinate):
	loop_no=loop_no+1
	new_x = (Decimal(extract(d)[0]) - Decimal(find_smallest(opened_file, 0)))
	new_y = (Decimal(extract(d)[1]) - Decimal(find_smallest(opened_file, 1)))
	print("moved x is " + str(new_x) + "\n")
	new_x = (new_x * Decimal(find_ratio(opened_file)))
	new_y = (new_y * Decimal(find_ratio(opened_file)))
	print("\npass number " + str(loop_no) + "\n")
	newfile.write("G1 X" + str(new_x)[:9] + " Y" + str(new_y)[:9] + "\n")
	

#Create the function that appends the latest value to the growing list for later parsing
#def append_List(extract_criteria):
	#m=extract(extract_criteria)
	#List.append(m)
	#return(m)

#----------------------------------------
#The executable program begins here.
#----------------------------------------

#Set the values for the maximum width and height (in mm)
origin=1
paperwidth=250
paperheight=190
largest = origin
smallest = paperheight
loop_no=0


#Make sure there's actually a file in the command line to open:
if (len(sys.argv) < 2):
	print ('Please define the original file... (for example "python RoundGcode.py myfile.gco")')
	sys.exit("File not defined. Exiting...")

#open the file (the second item in the command line) and turns it into a list:
filename = sys.argv[1] 

#Open the new file to be saved: 
newfile = open(filename+'.changed','w')


#this is the loop that does it all:
with open(filename) as opened_file:
		for d in opened_file:
			
			loop_no=loop_no+1
			new_x = (Decimal(extract(d)[0]) - Decimal(find_smallest(opened_file, 0))) 
			new_y = (Decimal(extract(d)[1]) - Decimal(find_smallest(opened_file, 1)))
			print("moved x is " + str(new_x) + "\n")
			new_x = (new_x * Decimal(find_ratio(opened_file)))
			new_y = (new_y * Decimal(find_ratio(opened_file)))
			print("\npass number " + str(loop_no) + "\n")
			newfile.write("G1 X" + str(new_x)[:9] + " Y" + str(new_y)[:9] + "\n")

#The loop ends here	

# Write the results to a new file
print ('Your new file is '+filename+'.changed')
newfile.close()	
