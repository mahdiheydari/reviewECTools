import sys
w=open("ouput_21.fasta", 'w')
lines = [line.rstrip('\n') for line in open("21_2.fasta")]
index=0
lineNum=0

for line in lines:
  index=int(line.split()[0])
  colorId=int(line.split()[4])
  while (index>lineNum):
    w.writelines(str(lineNum)+"\t0\t0\t \t"+str(colorId)+"\n")
    lineNum=lineNum+1
  w.writelines(str(line)+"\n")
  lineNum=lineNum+1