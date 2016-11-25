import sys
def ReverseComplement(seq):
    for base in seq:
        if base not in 'ATCGatcg':
            print ("Error: NOT a DNA sequence")
            print base
            print(seq)
            return None
    # too lazy to construct the dictionary manually, use a dict comprehension
    seq1 = 'ATCGTAGCatcgtagc'
    seq_dict = { seq1[i]:seq1[i+4] for i in range(16) if i < 4 or 8<=i<12 }
    return "".join([seq_dict[base] for base in reversed(seq)])

def FindKmersPos(kmerFile,contigFile):
    from Bio import SeqIO
    fasta_contig = SeqIO.parse(open(contigFile),'fasta')
    for contig in fasta_contig:
         sequence =str (contig.seq).upper()
         fasta_kmers = SeqIO.parse(open(kmerFile),'fasta')
         for kmerfasta in fasta_kmers:
             kmer =str (kmerfasta.seq).upper()
             if (kmer in sequence or ReverseComplement(kmer) in sequence):
                 print(kmer)
                 print(contig.id)
                 if (ReverseComplement(kmer) in sequence):
                     print(sequence.find(ReverseComplement(kmer)))
                 else:
                     print(sequence.find(kmer))
             #if ((sequence.find(kmer)!= -1 ) or (sequence.find(ReverseComplement(kmer))!= -1)):
             #  print(kmer)

   
def FindKmersPosBykmer(kmer,contigFile):
    from Bio import SeqIO
    fasta_contig = SeqIO.parse(open(contigFile),'fasta')
    for contig in fasta_contig:
         sequence =str (contig.seq).upper()
         kmer =kmer.upper()
         if (kmer in sequence or ReverseComplement(kmer) in sequence):
             print(kmer)
             print(contig.id)
             if (ReverseComplement(kmer) in sequence):
                 print(sequence.find(ReverseComplement(kmer)))
             else:
                 print(sequence.find(kmer))
             #if ((sequence.find(kmer)!= -1 ) or (sequence.find(ReverseComplement(kmer))!= -1)):
             #  print(kmer)


def FindKmersPosBykmer(kmer,contigFile):
    from Bio import SeqIO
    fasta_contig = SeqIO.parse(open(contigFile),'fasta')
    for contig in fasta_contig:
         sequence =str (contig.seq).upper()
         kmer =kmer.upper()
         if (kmer in sequence or ReverseComplement(kmer) in sequence):
             print(kmer)
             print(contig.id)
             if (ReverseComplement(kmer) in sequence):
                 print(sequence.find(ReverseComplement(kmer)))
             else:
                 print(sequence.find(kmer))
             #if ((sequence.find(kmer)!= -1 ) or (sequence.find(ReverseComplement(kmer))!= -1)):
             #  print(kmer)




def FindKmersPosByFile(kmerfile,contigFile):
    from Bio import SeqIO
    fasta_contig = SeqIO.parse(open(contigFile),'fasta')
    for contig in fasta_contig:
         sequence =str (contig.seq).upper()
         with open(kmerfile,'r') as fh:
             kmerId=""
             kmer=""
             for line in fh:
                 parts=line.split("\n")
                 line=parts[0]
                 if line.startswith(">"):
                     kmerId=line;
                 else:
                     kmer=line;
                     kmer =kmer.upper()
                     
                     if (kmer in sequence or ReverseComplement(kmer) in sequence):
                         print(kmer)
                         print(contig.id)
                         if (ReverseComplement(kmer) in sequence):
                             print(sequence.find(ReverseComplement(kmer)))
                         else:
                             print(sequence.find(kmer))
 


def FindKmersPos(contigFile):
    from Bio import SeqIO
    import commands
    kmerSize=21
    fasta_contig = SeqIO.parse(open(contigFile),'fasta')
    for contig in fasta_contig:
         sequence =str (contig.seq).upper()
         i=0
         
         while(i<len(sequence)-kmerSize+1):
	     kmer=sequence[i:i+kmerSize]
	     i=i+1
             if str((commands.getstatusoutput("grep -Fxq "+ kmer +" initialKmers.dat")[0]))=="0" :
		 print (kmer +"exist")
             
	     
	     
	     
	     
#kmerFile= sys.argv[1]
contigFile=sys.argv[1]

FindKmersPos(contigFile)