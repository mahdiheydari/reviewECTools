import os, sys
from operator import itemgetter, attrgetter, methodcaller
class Result:
    genomeName=""
    method=""
    brownie_N50=""
    genome_coverage=""
    kmersExist=""
    nodeExist=""
    noeNotExist=""
    Break_Points=""
    graph_size=""
    largest_contig=""
    number_nodes=""
    number_arcs=""
    kmerLost=""
    kmerLostRel=""
    genomeSize=0
    breakpointsRel=""
    _1_9_matches_per=""
    _00_matches_per=""
    _m9_matches_per=""
    gainName=""
    tp=0
    tn=0
    fp=0
    fn=0
    gain=""
    assemeblerName=""
    NGA50=""
    GenomeFraction=""
    mismatchRate=""
    indelsRate=""
assembler = ['spades', 'idba', 'minia', 'velvet', 'discovar']
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""
def connectDebruijnToAssembly(methodNameSet,genomeNameSet,results):
    genomeNameSet=sorted(genomeNameSet)
    methodNameSet=sorted(methodNameSet)
    for ass in assembler:
        directory="real/plots/correlation/"+ass+"/"
        if not os.path.exists(directory):
            os.makedirs(directory)
        for g in genomeNameSet: 
            fobw=open(directory+g+"_full.dat",'w')
            fobw.writelines("# the following table represent the correlation of De Bruijn Graph specifications and the quality of contigs after assembly "+g+'\n');
            fobw.writelines("tool\t\tNGA50\t\tGenomeFraction\t\tmismatchRate\t\tindelsRate\t\tbreakpointsRel\t\tkmerLostRel\t\tGain\n");
            for m in methodNameSet:
		#print(m)
                for r in results:
                    if (r.gain==''):
                            r.gain='n/a'
                    if (r.method==m and r.genomeName==g and r.assemeblerName==ass ):
			#print(r.method)
                        row=m+"\t\t"+str(r.NGA50)+'\t\t'+str(r.GenomeFraction)+'\t\t'+str(r.mismatchRate)+'\t\t'+str(r.indelsRate)+"\t\t"+str(r.breakpointsRel)+"\t\t"+str(r.kmerLostRel)+"\t\t"+str( r.gain)
                        fobw.writelines(row+'\n')
            fobw.close();
        for g in genomeNameSet:
            fobw=open(directory+g+".dat",'w')
            fobw.writelines("# the following table represent the correlation of De Bruijn Graph specifications and the quality of contigs after assembly "+g+'\n');
            fobw.writelines("tool\tGain\tLostkmer\tNGA50\tBreakpoint\n");
            for m in methodNameSet:
                for r in results:
                    base_breakpoint = [item.Break_Points for item in results if item.method == 'Uncorrected' and item.genomeName==g]
                    base_kmerLost   = [item.kmerLost for item in results if item.method == 'Uncorrected' and item.genomeName==g]
                    if (r.method==m and r.genomeName==g and r.assemeblerName==ass):
                        if (r.kmerLost=='' or m=='Uncorrected' ):
                            break;
                        if (r.gain==''):
                            r.gain='n/a' 
                        a= int(r.kmerLost)-int(base_kmerLost[0])
                        kmerlost=str (round ((int(r.kmerLost)-int (base_kmerLost[0])) *1000000/float(r.genomeSize), 2))
                        row=m+"\t"+str( r.gain)+"\t"+kmerlost+"\t"+str(r.NGA50)+"\t"+str(r.breakpointsRel)
                        fobw.writelines(row+'\n')
            fobw.close();
def MakeNGA50ColorTable(results,methodNameSet,genomeNameSet,assembler, outFileName):
    fobw=open(outFileName,'w')
    minDiff=1000
    genomeNameSet=sorted(genomeNameSet)
    methodNameSet=sorted(methodNameSet)
    fobw.writelines("\documentclass[a4paper,10pt]{article} \r");

    fobw.writelines(" \\usepackage{datetime} \r")
    fobw.writelines(" \\usepackage{booktabs} \r")
    fobw.writelines("\\usepackage{colortbl,dcolumn} ")

    c='a'
    for g in genomeNameSet:
        #print(g)
        base_NGA50=0;
        temp= [item.NGA50 for item in results if item.method == 'Uncorrected' and item.genomeName==g and item.assemeblerName==assembler]
        if (len(temp)):
            base_NGA50=temp[0]
            if (base_NGA50=="n/a"):
                base_NGA50=0;
        fobw.writelines(" \\def\\"+c+"#1{% \r")
        fobw.writelines(" \\ifnum0#1>"+str(int(base_NGA50)+minDiff)+ "\r")
        fobw.writelines(" \\cellcolor{green}\\else \r")
        fobw.writelines(" \\ifnum0#1<"+ str(int(base_NGA50)-minDiff)+"\r")
        fobw.writelines("  \\cellcolor{red}\\else \r")
        fobw.writelines(" \\cellcolor{yellow}\\fi\\fi\r")
        fobw.writelines(" #1}\r")
        c=chr(ord(c) + 1)
        

    
    fobw.writelines('\\begin{document}   \r');
    fobw.writelines('\\  \\footnote{ Compiled on \\today\ at \\currenttime} \r' );
    fobw.write("\r  NGA50 of contigs assembled by "+assembler+" before and after error correction by mentioned tools. Cells in the table are\n"+
               "colored based on the value of uncorrected row. If the tool improves the NGA50 length"+
               "\n more than 1kb it changes to green. If it  decreases the length more than 1kb it turns to red, otherwise it remains yellow."
               " n/a means that there are not any contig longer than 500 or the genome fraction is less than 50\%\r" );
    fobw.write('\\\ \r')
    fobw.write('\\\ \r')
    fobw.write('\\begin{tabular}{' );
    
    temp="c "
    i=1;
    colNum=1+len(genomeNameSet)
    while (i<colNum):
        temp=temp+"c "
        i=i+1
    
    fobw.writelines(temp+"}\r");
    fobw.writelines("\\toprule\r");
    temp="";
    i=1;
    for genome in genomeNameSet:
        temp=temp+"\r &\multicolumn{1}{ c } {"+genome+"}";
        i=i+1;
    fobw.writelines("\multicolumn{1}{ c }{Tools} "+temp)
    fobw.write('\\\ \r')
    fobw.writelines("\\toprule\r");
    for m in methodNameSet:
        tempLine= m
        c='a'
        avg=0
        genomeNumber=0;
        for g in genomeNameSet:
            find=0;
            base_NGA50=0;
	    temp= [item.NGA50 for item in results if item.method == 'Uncorrected' and item.genomeName==g and item.assemeblerName==assembler]
	    if (len(temp)):
		base_NGA50=temp[0]
		if (base_NGA50=="n/a"):
		    base_NGA50=0;
            for r in results: 
                if (r.genomeName==g and r.method==m and r.assemeblerName==assembler):
                    tempVal="";
                    if (r.NGA50!="n/a"):
                        tempVal=" & \\"+c+"{"+ str(r.NGA50)+"}";
                        if (base_NGA50!=0):
                            avg=avg+(float( float (r.NGA50)/float (base_NGA50)))
                            genomeNumber=genomeNumber+1;
                    else:
                        tempVal=" & "+r.NGA50;
                    #tempVal=" &"+str(r.NGA50);
                    find=1;
            if (find):
                tempLine=tempLine+tempVal
            else:
                tempLine=tempLine+"& n/a "
            c=chr(ord(c) + 1)
        #print(assembler+"\t"+m+"\t"+  '{0:.2f}'.format(float (avg)/float(genomeNumber)))
        tempLine=tempLine+"\\\ \r"
        fobw.write(tempLine)
    fobw.writelines("\\toprule\r");
    fobw.write('\end{tabular}');
    fobw.write('\\\ \r')
    fobw.write( '\end{document}')
    fobw.close();
def MakeNGA50Table(results,methodNameSet,genomeNameSet,outFileName):
    fobw=open(outFileName,'w')

    fobw.writelines("\documentclass[a4paper,10pt]{article} \r");

    fobw.writelines(" \\usepackage{datetime} \r")
    fobw.writelines(" \\usepackage{booktabs} \r")

    
    fobw.writelines('\\begin{document}   \r');
    fobw.writelines('\\  \\footnote{ Compiled on \\today\ at \\currenttime} \r' );
    fobw.write('\r NGA50 \r' );
    fobw.write('\\\ \r')
    fobw.write('\\\ \r')
    fobw.write('\\begin{tabular}{' );
    genomeNameSet=sorted(genomeNameSet)
    temp="c "
    i=1;
    colNum=1+len(genomeNameSet)
    while (i<colNum):
        temp=temp+"c "
        i=i+1
    
    fobw.writelines(temp+"}\r");
    fobw.writelines("\\toprule\r");
    temp="";
    i=1;
    for genome in genomeNameSet:
        temp=temp+"\r &\multicolumn{1}{ c } {"+genome+"}";
        i=i+1;
    fobw.writelines("\multicolumn{1}{ c }{Tools} "+temp)
    fobw.write('\\\ \r')
    fobw.writelines("\\toprule\r");
    for m in methodNameSet:
        tempLine= m
        for g in genomeNameSet:
            find=0;
            for r in results: 
                if (r.genomeName==g and r.method==m):
                    tempVal="";
                    tempVal=" & "+ str(r.NGA50);
                    find=1;
            if (find):
                tempLine=tempLine+tempVal
            else:
                tempLine=tempLine+"& 0 "         
        tempLine=tempLine+"\\\ \r"
        fobw.write(tempLine)
    fobw.writelines("\\toprule\r");
    fobw.write('\end{tabular}');
    fobw.write('\\\ \r')
    fobw.write( '\end{document}')
    fobw.close();
def extractAssemblyInfo(results): 
    for ass in assembler:
        fobr=open('real/quast_assembly/'+ass+'.tex','r')
        s= fobr.read();
        genomes = s.split("contains the Quast report after assembling")
        genomes.pop(0)
        genomeNameSet=set();
        methodNameSet=set();
        for genome in genomes:
            genomeName=find_between( genome, "dataset ", " with " )
            genomeNameSet.add(genomeName)
            assemeblerName=find_between( genome, " with ", " .\n" )
            lines = genome.split("\hline")
            lines.pop(0)
            lines.pop()
            toolsLine=[];
            for line in lines:
                elements = line.split("&")
                #print(elements[0])
                if ("Assembly" in elements[0]):
                    toolsLine=elements;
                if ("NGA50" in elements[0]):
                    NGA50line=elements;
                if ("Genome fraction " in elements[0]):
                    GFline=elements;
                if ("mismatches per 100 kbp" in elements[0]):
                    mismatchesLine=elements
                if ("indels per 100 kbp" in elements[0]):
                    indelLine=elements
            index=1;
            toolsLine.pop(0)
            #print(NGA50line)
            for tool in toolsLine:
                toolname=tool.split()
                #print(toolname[0])
                methodNameSet.add(toolname[0])
                r = Result()
                r.genomeName=genomeName
                #print(r.genomeName)
                r.assemeblerName=assemeblerName
                import re
                temp=re.findall(r'\b\d+\b', NGA50line[index])
                #print(temp)
                if (len(temp)>0):
                    r.NGA50=temp[0]
                else:
                    r.NGA50="n/a"
                temp=re.findall(r'\d+\.\d+', GFline[index])

                if (len(temp)>0):
                    r.GenomeFraction=temp[0]
                else:
                    r.GenomeFraction="n/a"
                temp=re.findall(r'\d+\.\d+', mismatchesLine[index])
                if (len(temp)>0):
                    r.mismatchRate=temp[0]
                else:
                    r.mismatchRate="n/a"
                temp=re.findall(r'\d+\.\d+', indelLine[index])
                if (len(temp)>0):
                    r.indelsRate=temp[0]
                else:
                    r.indelsRate="n/a"                              
                r.method=toolname[0]
                r.assemeblerName=ass
                results.append(r)
                index=index+1
        MakeNGA50ColorTable(results,methodNameSet,genomeNameSet,ass,"real/quast_assembly/NGA50_"+ass+".tex")
        #MakeNGA50ColorTable(results,methodNameSet,genomeNameSet,"spades.tex")            
def extracDeBruijnInfo(results):
    fobr=open('real/logFiles/deBruijn_Log_new_21.txt','r')
    s= fobr.read();
    methods = s.split("The results for next method:")
    methods.pop(0)
    genomeNameSet=set();
    methodNameSet=set();
    for method in methods:
        #print(method)
        methodName= find_between(method , "the method name is<<", ">>." )
        #print(methodName)
        genomes=method.split("next DataSet Starts<<");
        genomes.pop(0)
        genomeSize=0
        for genome in genomes:
            genomeName=find_between( genome, "The dataSet is<< ", " >>" )
            #print(genomeName)
            #print(genome)
            N50=find_between(genome ,"N50: ", "\n")
            genome_coverage=find_between(genome ,"The fraction of the genome that is covered: ", "%\n")
            genomeSize=find_between(genome ,"genomeZise:  ", "\n")
            kmersExist=find_between(genome ,"Number of k-mers in the DBG: ", "\n")
            kmerLost=find_between(genome ,"Number of k-mers in the DBG: ", " (")
            kmerLostlist=kmerLost.split("/")
            if (len(kmerLostlist)>1):
                kmerLost= int (kmerLostlist[1])-int(kmerLostlist[0])
            nodeExist=find_between(genome ,"Number of nodes that exist: ", "\n")
            #print(nodeExist)
            nodeExist=find_between(nodeExist, "(", "%)")
            #print(nodeExist)
            noeNotExist=find_between(genome ,"Number of nodes that do not exist: ", "\n")
            
            Break_Points=find_between(genome ,"Number of breakpoints: ", "\n")
            #print(Break_Points)
            graph_size=find_between(genome ,"Total size (kmers): ", "\n")
            largest_contig=find_between(genome ,"The largest node contains ", " basepairs.")
            #print(largest_contig)
            number_nodes=find_between(genome ,"Extracted ", " nodes and")
            number_arcs=find_between(genome ," nodes and ", " arcs.")
            genomeNameSet.add(genomeName)
            methodNameSet.add(methodName)
            for r in results:
                if (r.genomeName==genomeName and r.method==methodName):
                    #print("hi")
                    r.brownie_N50=N50
                    r.genome_coverage=genome_coverage
                    r.kmersExist=kmersExist
                    r.nodeExist=nodeExist
                    r.noeNotExist=noeNotExist
                    r.Break_Points=Break_Points
                    r.graph_size=graph_size
                    r.largest_contig=largest_contig
                    r.number_nodes=number_nodes
                    r.number_arcs=number_arcs
                    r.kmerLost=kmerLost
                    r.genomeSize=genomeSize
                    #print(r.kmerLost)
                    #print(r.Break_Points)
                    if (kmerLost!="" and Break_Points!=""):
                        r.kmerLostRel=round (r.kmerLost*1000000/float (r.genomeSize), 2)    
                        r.breakpointsRel=round (float (Break_Points)*1000000/float (r.genomeSize), 2)
                        #print(r.kmerLostRel)
                        #print(r.breakpointsRel)
    genomeNameSet=sorted(genomeNameSet)
    methodNameSet=sorted(methodNameSet)
    fobr.close();
    connectDebruijnToAssembly(methodNameSet,genomeNameSet,results)
def makeMappedReal(results):

    fobr=open('real/logFiles/Gainlog.txt','r')
    
    s= fobr.read();
    methods = s.split("The results for next method:")
    methods.pop(0)
    for method in methods:
        #print(method)
        methodName= find_between(method , "the method name is<<", ">>." )
        #print(methodName)
        genomes=method.split("next DataSet Starts<<");
        genomes.pop(0)
        for genome in genomes:
            genomSize=find_between(genome , "the size of the genome is:<< ", ">>" )
            genomeName=find_between( genome, "The dataSet is<< ", " >>" )    
            accuracyEva=find_between(genome ,"<<<The evaluation report based on base pairs>>>", "<<<The evaluation report based full read recovery>")
            errorCorrGain=find_between(accuracyEva,"The Gain value percentage is: (","%)")
            errorCorrGain=errorCorrGain.strip()
            if (errorCorrGain!="nan"):
                errorCorrGain='{0:.2f}'.format(round( float( errorCorrGain),2))
            else:
                errorCorrGain="na"
            try:
                tp=int (find_between(accuracyEva,"TP:","TN").strip())
            except ValueError:
                tp="na"
            
            try:
                tn=int (find_between(accuracyEva,"TN:","FP").strip())
            except:
                tn="na"
                
            try:
                fp=int (find_between(accuracyEva,"FP:","FN").strip())
            except:
                fp="na"

            try:
                fn=int (find_between(accuracyEva,"FN:","\n").strip())
            except:
                fn="na"

            
            for r in results:
                if (methodName != "Uncorrected" and r.genomeName==genomeName and r.method==methodName):
                    r.gain=errorCorrGain
                    r.gainName="ErrorCorrectionGain"
                    r.tp=tp
                    r.fp=fp
                    r.tn=tn
                    r.fn=fn
    fobr.close();

results=[];
extractAssemblyInfo(results)
makeMappedReal(results)
extracDeBruijnInfo(results)
