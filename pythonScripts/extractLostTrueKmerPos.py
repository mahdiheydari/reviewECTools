'''
Copyright (C) 2016  Mahdi Heydari
This script find the position of kmers and the frequency of them in contig. '''
import sys
interval=500
def ReverseComplement(seq):
    for base in seq:
        if base not in 'ATCGatcg':
            print ("Error: NOT a DNA sequence")
            return None
    # too lazy to construct the dictionary manually, use a dict comprehension
    seq1 = 'ATCGTAGCatcgtagc'
    seq_dict = { seq1[i]:seq1[i+4] for i in range(16) if i < 4 or 8<=i<12 }
    return "".join([seq_dict[base] for base in reversed(seq)])

def countReadFreq(query, fileName):
    import commands
    freq= int (commands.getstatusoutput("grep -e " + query + " " + fileName +" | wc -l" )[1].split()[1]) +int (commands.getstatusoutput("grep -e " + ReverseComplement(query) + " " + fileName +" | wc -l" )
    return freq


def countFreq(query, fileName):
    import commands
    freq= int (commands.getstatusoutput("jellyfish query "+ fileName + " " + query )[1].split()[1]) +int (commands.getstatusoutput("jellyfish query  " + fileName+" "+ReverseComplement(query)  )[1].split()[1])
    return freq
def getAlignmetLog(path):
    import csv
    import operator
    with open(path) as f:
        reader = csv.reader(f, delimiter=',')
        d = list(reader)
    #print(d)
    sortedList=sorted(d, key = lambda x: (str(x[1]), int(x[3])))
    #print(sortedList)
    return sortedList;
def getBreakpointsLog(path):
    import csv
    import operator
    with open(path) as f:
        reader = csv.reader(f, delimiter=',')
        d = list(reader)
    sortedList=sorted(d, key = lambda x: (int(x[1])))
    return sortedList;

def getBreakpoints(contigID,  alignmentLogList):
    i=0
    breakpoint=[]
    breakpoint.append(interval)
    while (i<len(alignmentLogList)):
        if (alignmentLogList[i][1]==contigID):
            breakpoint.append(int (alignmentLogList[i][4]))
        i=i+1
    #print(breakpoint)
    return breakpoint;
def getBreakpoints( alignmentLogList):
    i=0
    breakpoint=[]
    breakpoint.append(interval)
    while (i<len(alignmentLogList)):
	breakpoint.append(int (alignmentLogList[i][2]))
        i=i+1
    return breakpoint;
def FindKmersPos(contigFile, lostTrueKmersFile, readFile, alignmentFile, outputFile, kmerSize,OutFileDir):
    readSearchSize=500
    from Bio import SeqIO
    maxContigSize=600000
    bigKmerSize=41
    alignmentLogList=getAlignmetLog(alignmentFile)
    fasta_contig = SeqIO.parse(open(contigFile),'fasta')
    out = open(outputFile, 'w')
    contigNum=0
    for contig in fasta_contig:
         contigNum=contigNum+1
         out.writelines(contig.id+"\n")
         directory=OutFileDir+"/reads/"+str(contigNum)
         if not os.path.exists(directory):
             os.makedirs(directory)
         outkmer = open(directory+"/"+str(bigKmerSize)+"kmer_"+str(contig.id), 'w')
         sequence =str (contig.seq).upper()
         breakPoints=getBreakpoints(contig.id, alignmentLogList)
         trueLostKmerCov=[0]*maxContigSize
         initialCov=[0]*maxContigSize
         innerContigNum=1
         for b in breakPoints:
             i=b-interval
             #print(i)
             #print(b)
             while(i<len(sequence)-kmerSize+1 and i<b+interval): #and i<b+interval
                 #print(i)
                 kmer=sequence[i:i+kmerSize]
                 freq=countFreq(kmer, readFile)
                 if (kmerSize==21 and countFreq(kmer, lostTrueKmersFile)>0):
                        trueLostKmerCov[i]=freq
                 initialCov[i]=freq
                 if (i<b and i>interval):
                        out.writelines(str(i)+"\t"+str(trueLostKmerCov[i])+"\t"+str(initialCov[i])+"\t"+str(kmer)+"\t"+str(innerContigNum-1)+"\n")
                 else:
                        out.writelines(str(i)+"\t"+str(trueLostKmerCov[i])+"\t"+str(initialCov[i])+"\t"+str(kmer)+"\t"+str(innerContigNum)+"\n")
                 if (i%5==0 and  abs(b-i)<readSearchSize and b>interval and i<len(sequence)-interval):
                        bigKmer=sequence[i:i+bigKmerSize]
                        outkmer.writelines(">"+str(b)+"_"+str(i)+"\n")
                        outkmer.writelines(bigKmer+"\n")
                 i=i+1
             innerContigNum=innerContigNum+1
         outkmer.close()
    out.close()
    fasta_contig.close()
def FindKmersPosAll(contigFile, lostTrueKmersFile, readFile, alignmentFile, outputFile, kmerSize, OutFileDir):
    from Bio import SeqIO
    alignmentLogList=getAlignmetLog(alignmentFile)
    fasta_contig = SeqIO.parse(open(contigFile),'fasta')
    out = open(outputFile, 'w')
    for contig in fasta_contig:
         outkmer = open(str(kmerSize)+"kmer_"+contig.id, 'w')
         out.writelines(contig.id+"\n")
         sequence =str (contig.seq).upper()
         breakPoints=getBreakpoints(contig.id, alignmentLogList)
         innerContigNum=1
         i=0
         while(i<len(sequence)-kmerSize+1):
             if (breakPoints[innerContigNum-1]<i):
                 innerContigNum=innerContigNum+1
             kmer=sequence[i:i+kmerSize]
             freq=countFreq(kmer, readFile)
             lostFreq=0
             if (countFreq(kmer, lostTrueKmersFile)>0):
                 lostFreq=freq
             out.writelines(str(i)+"\t"+str(lostFreq)+"\t"+str(freq)+"\t"+str(kmer)+"\t"+str(innerContigNum)+"\n")

	     outkmer.writelines(str(kmer)+"\n")
	     i=i+1
         outkmer.close() 
    out.close()
    fasta_contig.close()  

def FindKmersPos_mummer(contigFile, lostTrueKmersFile, readFile, alignmentFile, outputFile, kmerSize,OutFileDir):
    from Bio import SeqIO
    import os
    maxContigSize=600000
    bigKmerSize=41
    readSearchSize=200
    alignmentLogList=getBreakpointsLog(alignmentFile)    
    fasta_contig = SeqIO.parse(open(contigFile),'fasta')
    out = open(outputFile, 'w')
    contigNum=0
    for contig in fasta_contig:
         contigNum=contigNum+1
         out.writelines(contig.id+"\n")
         directory=OutFileDir
         if not os.path.exists(directory):
             os.makedirs(directory)
         outkmer = open(directory+"/"+str(bigKmerSize)+"kmer_"+str(contig.id), 'w')
         sequence =str (contig.seq).upper()
         breakPoints=getBreakpoints( alignmentLogList)
         trueLostKmerCov=[0]*maxContigSize
         initialCov=[0]*maxContigSize
         innerContigNum=1
         last = breakPoints[len(breakPoints)-1]
         for b in breakPoints:
             i=b-interval
             while(i<len(sequence)-kmerSize+1 and i<int(b)+interval and i<last):   
                 kmer=sequence[i:i+kmerSize]
                 freq=countFreq(kmer, readFile)
                 if (kmerSize==21 and countFreq(kmer, lostTrueKmersFile)>0):
                        trueLostKmerCov[i]=freq
                 initialCov[i]=freq
                 if (i<b and i>interval):
                        out.writelines(str(i)+"\t"+str(trueLostKmerCov[i])+"\t"+str(initialCov[i])+"\t"+str(kmer)+"\t"+str(innerContigNum-1)+"\n")
                 else:
                        out.writelines(str(i)+"\t"+str(trueLostKmerCov[i])+"\t"+str(initialCov[i])+"\t"+str(kmer)+"\t"+str(innerContigNum)+"\n")
                 if (i%5==0 and abs(b-i)<readSearchSize and b>interval and i<len(sequence)-interval):   
                        bigKmer=sequence[i:i+bigKmerSize]
                        outkmer.writelines(">"+str(b)+"_"+str(i)+"\n")
                        outkmer.writelines(bigKmer+"\n")
                 i=i+1
             innerContigNum=innerContigNum+1
         outkmer.close()
    out.close()
    fasta_contig.close()

def FindKmersPosAll_mummer(contigFile, lostTrueKmersFile, readFile, alignmentFile, outputFile, kmerSize):
    from Bio import SeqIO
    alignmentLogList=getBreakpointsLog(alignmentFile)
    fasta_contig = SeqIO.parse(open(contigFile),'fasta')
    out = open(outputFile, 'w')
    for contig in fasta_contig:
         out.writelines(contig.id+"\n")
         sequence =str (contig.seq).upper()
         breakPoints=getBreakpoints(alignmentLogList)
         breakPoints.pop(0)
         print(breakPoints)
         innerContigNum=1
         i=0
         last = breakPoints[len(breakPoints)-1]
         while(i<len(sequence)-kmerSize+1 ):
             if (breakPoints[innerContigNum-1]<i and i<last):
                 innerContigNum=innerContigNum+1
             kmer=sequence[i:i+kmerSize]
             freq=countFreq(kmer, readFile)
             lostFreq=0
             if (countFreq(kmer, lostTrueKmersFile)>0):
                 lostFreq=freq
             out.writelines(str(i)+"\t"+str(lostFreq)+"\t"+str(freq)+"\t"+str(kmer)+"\t"+str(innerContigNum)+"\n")
	     i=i+1
    out.close()
    fasta_contig.close()  



countReadFreq


def FindKmerReadCov(contigFile,  readFile, outputFile, kmerSize, startIndex):
    from Bio import SeqIO
    fasta_contig = SeqIO.parse(open(contigFile),'fasta')
    out = open(outputFile, 'w')
    i=startIndex
    for contig in fasta_contig:
         out.writelines(contig.id+"\n")
         sequence =str (contig.seq).upper()
         while(i<len(sequence)-kmerSize+1 ):
             kmer=sequence[i:i+kmerSize]
             freq=countReadFreq(kmer, readFile)
             out.writelines(str(i)+"\t"+str(freq)+"\t"+str(kmer)+"\n")
             i=i+1
    out.close()
    fasta_contig.close()



def removeNoneZero(inputFile, outputFile):
    w=open(inputFile, 'w')
    lines = [line.rstrip('\n') for line in open(outputFile)]
    index=0
    lineNum=0
    lastlineBreakpoint=-1
    lastLine=line[0]
    w.write(lastLine+"\n")
    for line in lines:
	index=int(line.split()[0])
	freq=int(line.split()[1])
	Breakpoint=int(line.split()[4])
	if (freq !=0):
	    w.write(line+"\n")
	else:
	    if(Breakpoint!=lastlineBreakpoint):
		w.write(lastLine+"\n")
		w.write(line+"\n")
	lastlineBreakpoint=Breakpoint
	lastLine=line
    w.write(line+"\n")
def makeAlignmentFile(inputFileName,outputFileName ):
    #print(inputFileName)
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
            #print(contig)
	    outputFile.write(lines[0].split()[0] +","+str(int (lines[len(lines)-1].split()[0])+int (lines[len(lines)-1].split()[2]))+",")
	    if (int (lines[len(lines)-1].split()[1]< int (lines[0].split()[1]))):
		outputFile.write(lines[0].split()[1] +","+str(int (lines[len(lines)-1].split()[1])+int (lines[len(lines)-1].split()[2])))
	    else:
		outputFile.write(str(int(lines[len(lines)-1].split()[1]))+","+ str(int(lines[0].split()[1])+int (lines[0].split()[2])))
	    outputFile.write("\n")
    outputFile.close()
    inputFile.close()
contigFile=sys.argv[1]
lostTrueKmersFile= sys.argv[2]
readFile= sys.argv[3]
alignmentFile= sys.argv[4]
outputFile=sys.argv[5]
kmerSize=int(sys.argv[6])
OutFileDir=sys.argv[7]
mummerFile= sys.argv[8]




#FindKmersPos(contigFile, lostTrueKmersFile,readFile, alignmentFile, outputFile, kmerSize)
#FindKmersPosAll(contigFile, lostTrueKmersFile,readFile, alignmentFile, outputFile, kmerSize)


makeAlignmentFile(mummerFile,alignmentFile)
#FindKmersPos_mummer(contigFile, lostTrueKmersFile, readFile, alignmentFile, outputFile, kmerSize,OutFileDir)

findAll=sys.argv[9]


if (findAll=="true"):
    print("finding all kmers")
    FindKmersPosAll_mummer(contigFile, lostTrueKmersFile, readFile, alignmentFile, outputFile, kmerSize)
else:
    print("finding kmers around breakpoints")
    FindKmersPos_mummer(contigFile, lostTrueKmersFile, readFile, alignmentFile, outputFile, kmerSize,OutFileDir)
