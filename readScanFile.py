# -*- coding: utf-8 -*-
import sys

infile = sys.argv[1]
lookFor = sys.argv[2]+" "
if len(sys.argv)>3: 
	skipFirst= int(sys.argv[3]) 	
else:
	skipFirst=1
found=0

with open(infile) as inf:
	for line in inf:
		if lookFor in  line and int(line.split()[4]) >0:
			found+=1
			if skipFirst==found:
				print line.split()[7]


	
