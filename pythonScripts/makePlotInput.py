import sys
interval=100
def makeAlignmentFile(inputFileName,outputFileName ):
    inputFile=open(inputFileName)
    outputFile=open(outputFileName,'w')
    contigs=inputFile.read().split('>')

    contigs.pop(0)
    for contig in contigs:
        lines=contig.split('\n')
        if (len(lines)>2):
            outputFile.write(lines[0]+",")
	    lines.pop(0)
	    lines.pop()
	    outputFile.write(lines[0].split()[0] +","+str(int (lines[len(lines)-1].split()[0])+int (lines[len(lines)-1].split()[2]))+",")
	    if (int (lines[len(lines)-1].split()[1]< int (lines[0].split()[1]))):
		outputFile.write(lines[0].split()[1] +","+str(int (lines[len(lines)-1].split()[1])+int (lines[len(lines)-1].split()[2])))
	    else:
		outputFile.write(str(int(lines[len(lines)-1].split()[1]))+","+ str(int(lines[0].split()[1])+int (lines[0].split()[2])))
	    outputFile.write("\n")
    outputFile.close()
    inputFile.close()

def getBreakpoints(  alignmentLogList):
    i=0
    breakpoint=[]
    breakpoint.append(interval)
    while (i<len(alignmentLogList)):
	breakpoint.append(int (alignmentLogList[i][2]))
        i=i+1
    return breakpoint;
def getAlignmetLog(path):
    import csv
    import operator
    with open(path) as f:
        reader = csv.reader(f, delimiter=',')
        d = list(reader)
    sortedList=sorted(d, key = lambda x: (int(x[1])))
    return sortedList;

def makeInputFile(inputFile,outputFile,contigLength):
    makeAlignmentFile(inputFile,outputFile)
    breakPoints=getBreakpoints(getAlignmetLog(outputFile))
    out = open(outputFile, 'w')
    innerContigNum=1
    i=0
    last = breakPoints[len(breakPoints)-1]
    for b in breakPoints:
             i=b-interval
             print (b)
             while(i<contigLength and i<b+interval and i<last ):
                 if (i<b and i>interval):
                        out.writelines(str(i)+"\t"+str(innerContigNum-1)+"\n")
                 else:
                        out.writelines(str(i)+"\t"+str(innerContigNum)+"\n")
                 i=i+1
             innerContigNum=innerContigNum+1
         
    out.close()
inputFile=sys.argv[1]
outputFile= sys.argv[2]
makeInputFile(inputFile,outputFile, 500000)          


