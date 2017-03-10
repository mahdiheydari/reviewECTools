'''
Copyright (C) 2016  Mahdi Heydari
this script finds the lines which occur more than a threshholdFreq
'''
import sys
def findFrequentKmers(inputFile, outputFile):
  w=open(outputFile, 'w')
  lines = [line.rstrip('\n') for line in open(inputFile)]
  index=0
  lineNum=0
  lastlineBreakpoint=-1
  threshholdFreq=1000
  while (not( lines[0].startswith( "0" ))):
      lines.pop(0)
      
  lastLine=line[0]
  for line in lines:
    index=int(line.split()[0])
    freq=int(line.split()[1])
    cov=int(line.split()[2])
    kmer=line.split()[3]
    Breakpoint=int(line.split()[4])
    if (cov>=threshholdFreq):
        cov=threshholdFreq
    if ( cov >=threshholdFreq):
      w.write(str(index)+"\t"+str(freq)+"\t"+str(cov)+"\t"+str(kmer)+"\t"+str(Breakpoint)+ "\n")
    else:
      if(Breakpoint!=lastlineBreakpoint):
          if (lastlineBreakpoint!=-1):
              w.write(lastLine+"\n")
          w.write(line+"\n")
    lastlineBreakpoint=Breakpoint
    lastLine=line
  w.write(line+"\n")

inputFile=sys.argv[1]
outputFile= sys.argv[2]
findFrequentKmers(inputFile, outputFile)
