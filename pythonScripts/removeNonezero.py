
import sys  
inputFile=sys.argv[1]
outPutFile= sys.argv[2]

w=open(outPutFile, 'w')
lines = [line.rstrip('\n') for line in open(inputFile)]
index=0
lineNum=0
lastlineBreakpoint=-1


lastFreq=1
line=lines[0]
while (line.split()[0]!='0'):
    lines.pop(0)
    line=lines[0]
for line in lines:
  index=int(line.split()[0])
  freq=int(line.split()[1])
  Breakpoint=int(line.split()[4])
  if (freq !=0):
    #w.write(line+"\n")
    w.write(line.split()[0]+"\t"+"10"+"\t"+line.split()[2]+"\t"+line.split()[3]+"\t"+line.split()[4]+"\n" )
  else:
    if(Breakpoint!=lastlineBreakpoint):
	if (lastFreq==0):
	    w.write(lastLine+"\n")
	w.write(line+"\n")
  lastlineBreakpoint=Breakpoint
  lastLine=line
  lastFreq=freq
w.write(line+"\n")