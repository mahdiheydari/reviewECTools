import sys
import os
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
def countFreq(query, fileName):
    import commands
    #print("jellyfish query  " + fileName+" "+ReverseComplement(query)+"\n")
    #print("jellyfish query "+ fileName + " " + query+"\n")
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
def FindKmersPosAll(contigFile, lostTrueKmersFile, readFile, alignmentFile, outputFile, kmerSize):
    from Bio import SeqIO
    alignmentLogList=getAlignmetLog(alignmentFile)
    fasta_contig = SeqIO.parse(open(contigFile),'fasta')
    out = open(outputFile, 'w')
    for contig in fasta_contig:
         outkmer = open(str(kmerSize)+"kmer_"+contig.id, 'w')
         out.writelines(contig.id+"\n")
         sequence =str (contig.seq).upper()
         breakPoints=getBreakpoints(contig.id, alignmentLogList)
         del breakPoints[0]
         print(breakPoints)
         innerContigNum=1
         i=0
         while(i<len(sequence)-kmerSize+1):
             if (breakPoints[innerContigNum-1]<i):
                print(innerContigNum)
                print(breakPoints[innerContigNum])
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



def FindKmersPos(contigFile, lostTrueKmersFile, readFile, alignmentFile, outputFile, kmerSize,OutFileDir):
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
             while(i<len(sequence)-kmerSize+1 and i<b+interval ):
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
                 if (i%5==0 and (b-i)>(bigKmerSize-41) and (b-i)<41 and b>interval and i<len(sequence)-interval):
                        bigKmer=sequence[i:i+bigKmerSize] 
                        outkmer.writelines(">"+str(b)+"_"+str(i)+"\n")
                        outkmer.writelines(bigKmer+"\n")
                 i=i+1
             innerContigNum=innerContigNum+1
         outkmer.close()
    out.close()
    fasta_contig.close()             
contigFile=sys.argv[1]
lostTrueKmersFile= sys.argv[2]
readFile= sys.argv[3]
alignmentFile= sys.argv[4]
outputFile=sys.argv[5]
kmerSize=int(sys.argv[6])
OutFileDir=sys.argv[7]
#FindKmersPos(contigFile, lostTrueKmersFile,readFile, alignmentFile, outputFile, kmerSize, OutFileDir)
FindKmersPosAll(contigFile, lostTrueKmersFile,readFile, alignmentFile, outputFile, kmerSize)


