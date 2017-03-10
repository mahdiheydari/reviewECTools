'''this script find the read coverage of kmers in a contig. 
Using grep instead of jellyfish helps to avoid counting multiple occurance of a kmer in one read several times.'''

import sys 
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
    
    freq= int (commands.getstatusoutput("grep -e " + query + " " + fileName +" | wc -l" )[1]) +int (commands.getstatusoutput("grep -e " + ReverseComplement(query) + " " + fileName +" | wc -l" )[1])
    return freq


def countReadCov(contigFile,  readFile, outputFile, kmerSize, startIndex):
    from Bio import SeqIO
    fasta_contig = SeqIO.parse(open(contigFile),'fasta')
    out = open(outputFile, 'w')
    i=startIndex
    print(i)
    for contig in fasta_contig:
         out.writelines(contig.id+"\n") 
         sequence =str (contig.seq).upper() 
         print(len(sequence))
         print(kmerSize)
         while(i<len(sequence)-kmerSize+1 ):
            
             kmer=sequence[i:i+kmerSize]
             print(kmer)
             freq=countReadFreq(kmer, readFile)
             out.writelines(str(i)+"\t"+str(freq)+"\t"+str(kmer)+"\n")
             i=i+1
    out.close()
    fasta_contig.close()

contigFile=sys.argv[1]
readFile= sys.argv[2]
outputFile=sys.argv[3]
kmerSize=int(sys.argv[4])
startIndex=int(sys.argv[5])

countReadCov(contigFile,  readFile, outputFile, kmerSize, startIndex)
