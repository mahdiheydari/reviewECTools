'''
        Copyright (C) 2016 Giles Miclotte (giles.miclotte@intec.ugent.be) , Mahdi Heydari

        This program is free software; you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation; either version 2 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with this program; if not, write to the
        Free Software Foundation, Inc.,
        59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
        
        
        This script find the reads in one given interval
'''

from __future__ import print_function
import sys
import re
import hashlib
from Bio import SeqIO
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class SAMEntry:
        def __init__(self, line):
                props = line.strip().split('\t')
                self.qname = props[0]
                self.flag = props[1]
                self.rname = props[2]
                self.pos = int(props[3]) - 1 #change to 0-based
                self.mapq = props[4]
                self.cigar = re.findall(r'(\d+)([A-Z]{1})', props[5])
                self.cigar = [(int(c), s) for c, s in self.cigar]
                if self.cigar[0][1] == 'S' or self.cigar[0][1] == 'H':
                        self.pos -= self.cigar[0][0]
                self.rnext = props[6]
                self.pnext = props[7]
                self.tlen = props[8]
                self.seq = props[9]
                self.qual = props[10]
                self.optional = {}
                for i in range(11, len(props)):
                        field = props[i].split(':')
                        if field[1] == 'i':
                                field[2] = int(field[2])
                        elif field[1] == 'f':
                                field[2] = float(field[2])
                        self.optional[field[0]] = [field[1], field[2]]
                        
        def len(self):
                return len(self.seq)

class Sequence:
        def __init__(self, meta, seq):
                self.meta = meta
                self.name = meta.strip().split('\t')[0].split(' ')[0]
                self.seq = seq


def fasta_parse(ifname):
        infile = open(ifname)
        meta = ""
        seq = ""
        for line in infile:
                if line.startswith('>'): #header
                        if meta != "":
                                yield [meta, seq]
                                meta = ""
                                seq = ""
                        meta = line[1:]
                else:
                        seq += line.strip()
        if meta != "":
                yield [meta, seq]
        infile.close()

def fastq_parse(ifname):
        infile = open(ifname)
        meta = ""
        seq = ""
        count = 0
        for line in infile:
                if count == 0:
                        if meta != "":
                                yield [meta, seq]
                                meta = ""
                                seq = ""
                        meta = line[1:]
                elif count == 1:
                        seq = line.strip()
                count = (count + 1) % 4
        if meta != "":
                yield [meta, seq]
        infile.close()


def sam_parse(ifname, start, end):
        infile = open(ifname)
        sam = []
        print("[ "+str(start)+"\t" +str(end)+" ]")
        for line in infile:
                if line.startswith('@'): #header
                        continue
                else: #entry
			sam_entry = line.strip().split('\t')
			if (int (sam_entry[3])< int (end) and int (sam_entry[3]) > int (start) and sam_entry[5]!='*' ):
			    print(line)
			    sam += [SAMEntry(line)]
			if (int(sam_entry[3])> int(end)):
			    return sam     
        infile.close()
        return sam

def RC(seq):
    for base in seq:
        if base not in 'ATCGatcg':
            print ("Error: NOT a DNA sequence")
            return None
    seq1 = 'ATCGTAGCatcgtagc'
    seq_dict = { seq1[i]:seq1[i+4] for i in range(16) if i < 4 or 8<=i<12 }
    return "".join([seq_dict[base] for base in reversed(seq)])
def executeCommadnd(query):
    import commands
    return(commands.getstatusoutput(query)[1])

def extracReads(sam_entries,outMapped, outMappedCorrected, uncorrectedReads,correctedReads ):
    mu = open(outMapped, 'w')
    mc = open(outMappedCorrected, 'w')
    readSet=set()
    #idset =set()
    RCSet=set(['89', '121', '181', '117', '153', '185', '147' , '83' , '115' , '179' , '81' , '145' , '113' , '177', '16' ])
    for sam in sam_entries:
        print("*************************************************\n")
        print(sam.seq+"\n")
        num=int(hashlib.sha1(sam.qname.encode('utf-8')).hexdigest(), 16) % (10 ** 4)  	        
        print(num)
        if (num not in readSet):
            readSet.add(num) 
	    command=" grep -n -m 1 "+sam.qname+" "+uncorrectedReads + " | cut -f1 -d: "
            #if (sam.flag in RCSet):
            #    command=" grep -n "+RC(sam.seq)+" "+uncorrectedReads + " | head -n 1 | cut -f1 -d: "
            print(command+"\n")
            result=executeCommadnd(command)
            print(result)
            if (result!=''):
	        lineNum=int (result)
	        print(lineNum)
	        #queryName=executeCommadnd("awk 'NR == "+str(lineNum)+" { print ; exit ;} ' " +uncorrectedReads)
	        queryName="@"+sam.qname
                uncorrectedSeq=executeCommadnd("awk 'NR == "+str(lineNum+1)+" { print ; exit ;} ' " +uncorrectedReads)
	        orientation=executeCommadnd("awk 'NR == "+str(lineNum+2)+" { print ; exit ;} ' " +uncorrectedReads)
	        print(uncorrectedSeq)
	        
                #if (queryName.split()[0] not in idset):
	        #    idset.add(queryName.split()[0])
                #    queryName=queryName.split()[0]+".1\t"+' '.join(queryName.split()[1:])
                #else:
                #    queryName=queryName.split()[0]+".2\t"+' '.join(queryName.split()[1:])

                if (sam.flag in RCSet):
                    print("writing RC of this sequence in mapped file\n"+uncorrectedSeq )
                    mu.writelines(queryName+"\t RC\t \n")
                    mu.writelines(RC(uncorrectedSeq)+"\n")
                    mc.writelines(queryName+"\t RC\t \n")
                    mc.writelines(RC(executeCommadnd("awk 'NR == "+str(lineNum+1)+" { print ; exit ;} ' " +correctedReads))+"\n")
                else:
                    print("writing this sequence in mapped file\n"+uncorrectedSeq )
                    mu.writelines(queryName+"\n")
                    mu.writelines(uncorrectedSeq+"\n")
                    mc.writelines(queryName+"\n")
                    mc.writelines(executeCommadnd("awk 'NR == "+str(lineNum+1)+" { print ; exit ;} ' " +correctedReads)+"\n")
	        mu.writelines(orientation+"\n")
	        mu.writelines(sam.qual+"\n")
                mc.writelines(orientation+"\n")
                mc.writelines(executeCommadnd("awk 'NR == "+str(lineNum+3)+" { print ; exit ;} ' " +correctedReads)+"\n") 
def main(argv=None):

        if argv == None:
                argv = sys.argv
        if len(argv) < 4:
                print('Usage: extractReadsFromSam.py ref_begin_idx ref_distance sorted.sam ')
                exit()
        #specify input, can be changed to cl options of course
        
        start=int(argv[1])
        end=start+int(argv[2])
        sam_file = argv[3]   
        readsFile = argv[4]
        readsFileCorrected = argv[5]
        outMapped = argv[6]
        outMappedCorrected = argv[7] 
        
        sam_entries = sam_parse(sam_file,start, end)
        samReadSet=set()
        
        for sam in sam_entries:
	    samReadSet.add (sam.seq)
        extracReads(sam_entries,outMapped, outMappedCorrected, readsFile, readsFileCorrected )
	    
main()
