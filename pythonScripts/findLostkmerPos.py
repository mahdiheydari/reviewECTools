

def ReverseComplement(seq):
    for base in seq:
        if base not in 'ATCGatcg':
            print ("Error: NOT a DNA sequence")
            return None
    # too lazy to construct the dictionary manually, use a dict comprehension
    seq1 = 'ATCGTAGCatcgtagc'
    seq_dict = { seq1[i]:seq1[i+4] for i in range(16) if i < 4 or 8<=i<12 }
    return "".join([seq_dict[base] for base in reversed(seq)])

def FindKmersPos(inputFile):
    with open(inputFile,'r') as fh:
    for line in fh:
        if (!line.startswith(">"))
            fobw.writelines(line);
            print(line)

inputFile= sys.argv[1]
#outPutFile=sys.argv[2]
FindKmersPos(inputFile)
