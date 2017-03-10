'''
Copyright (C) 2016  Mahdi Heydari
This script find the uniqe reads based on the input kmer file, its better to use the sam file as an input to find the reads.'''
import hashlib
import sys
import subprocess
class Read:
    seq_id=""
    seq=""
    ori=""
    quality=""

def RC(seq):
    for base in seq:
        if base not in 'ATCGatcg':
            print ("Error: NOT a DNA sequence")
            return None
    # too lazy to construct the dictionary manually, use a dict comprehension
    seq1 = 'ATCGTAGCatcgtagc'
    seq_dict = { seq1[i]:seq1[i+4] for i in range(16) if i < 4 or 8<=i<12 }
    return "".join([seq_dict[base] for base in reversed(seq)])
def executeCommadnd(query):
    import commands
    return(commands.getstatusoutput(query)[1])
def extractReads(kmerFile, mappedUncorrectedReads, mappedCorrectedReads,uncorrectedReads,correctedReads):
    from Bio import SeqIO
    kmers = SeqIO.parse(open(kmerFile),'fasta')
    readSet=set()
    mu = open(mappedUncorrectedReads, 'w')
    mc = open(mappedCorrectedReads, 'w')
    for kmer in kmers:
        command=" grep -e \""+str(kmer.seq)+"\" "+uncorrectedReads+" -A 2 -B 1"
        log=executeCommadnd(command)
        command=" grep -e \""+str(RC(kmer.seq))+"\" "+uncorrectedReads+" -A 2 -B 1"
        log= log+ executeCommadnd(command)
        newLog=""
        for line in log.split("\n"):
            if not line.startswith("--"):
                newLog=newLog+line+"\n"
        reads=newLog.split("@SRR823377")
        #print(newLog)
        for read in reads:
            readLines=read.split("\n")
            if (len(readLines)>3):
                r =Read()
                r.seq_id="@SRR823377"+readLines[0]
                r.seq=readLines[1]
                r.ori=readLines[2]
                r.quality=readLines[3]
                num=int(hashlib.sha1(r.seq.encode('utf-8')).hexdigest(), 16) % (10 ** 4)
                if (num not in readSet):
                    readSet.add(num)
                    command=" grep -n "+r.seq+" "+uncorrectedReads + " | head -n 1 | cut -f1 -d: "
                    lineNum=int (executeCommadnd(command))
                   
                    if (str(kmer.seq) in str(r.seq)):
                        mu.writelines(r.seq_id+"_"+str(kmer.id)+"\n")
                        mu.writelines(r.seq+"\n")
                    else:
                        mu.writelines(r.seq_id+"_RC_"+str(kmer.id)+"\n")
                        mu.writelines(RC(r.seq)+"\n")
                    
                    mu.writelines(r.ori+"\n")
                    mu.writelines(r.quality+"\n")
                    correctedRead =Read()
                    correctedRead.seq_id=executeCommadnd("awk 'NR == "+str(lineNum-1)+" { print ; exit ;} ' " +correctedReads)
                    correctedRead.seq=executeCommadnd("awk 'NR == "+str(lineNum)+" { print ; exit ;} ' " +correctedReads)
                    correctedRead.ori=executeCommadnd("awk 'NR == "+str(lineNum+1)+" { print ; exit ;} ' " +correctedReads)
                    correctedRead.quality=executeCommadnd("awk 'NR == "+str(lineNum+2)+" { print ; exit ;} ' " +correctedReads)
                    
                    if (str(kmer.seq) in str(r.seq)):
                        print(str(kmer.id))
                        mc.writelines(correctedRead.seq_id+"_"+str(kmer.id)+"\n")
                        mc.writelines(correctedRead.seq+"\n")
                    else:
                        mc.writelines(correctedRead.seq_id+"_RC_"+"_"+str(kmer.id)+"\n")
                        mc.writelines(RC(correctedRead.seq)+"\n")
                    mc.writelines(correctedRead.ori+"\n")
                    mc.writelines(correctedRead.quality+"\n")
    mu.close();
    mc.close();
    readSet.clear()
kmerFile=sys.argv[1]
mappedUncorrectedReads= sys.argv[2]
mappedCorrectedReads= sys.argv[3]
uncorrectedReads= sys.argv[4]
correctedReads=sys.argv[5]    
extractReads(kmerFile, mappedUncorrectedReads, mappedCorrectedReads,uncorrectedReads,correctedReads)

