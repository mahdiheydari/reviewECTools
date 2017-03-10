'''
Copyright (C) 2016  Mahdi Heydari
this reads the file and if a read with a same id happens 2 time, it gives different id to them.
'''
import sys
inputFile= sys.argv[1]
outputFile=sys.argv[2]
idset =set()
infile = open(inputFile)
w=open(outputFile, 'w')  
i=0	     
for line in infile:
    line=line.rstrip('\n')
    if (i%4==0):
	if (line.split()[0] not in idset):
	    idset.add(line.split()[0])
	    w.write (line.split()[0]+".1 "+' '.join(line.split()[1:])+"\n")
	else:
	    w.write (line.split()[0]+".2 "+' '.join(line.split()[1:])+"\n")
    else:
       w.write(line+"\n")    
    i=i+1;
