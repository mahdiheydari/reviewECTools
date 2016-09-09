import os, sys
from operator import itemgetter, attrgetter, methodcaller
class Result:
    genomeName=""
    method=""
    N50=""
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
def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def makeBreakpoint(gresults,methodNameSet,genomeNameSet,outFileName):
                  
    fobw=open(outFileName+"_breakpoints_only.tex",'w')
    #print (outFileName+"_"+gainName+"_only.tex")
    #covSet.pop(0);
    fobw.writelines("\documentclass[a4paper,10pt]{article} \r");

    fobw.writelines(" \\usepackage{datetime} \r")
    fobw.writelines(" \\usepackage{booktabs} \r")
    
    fobw.writelines('\\begin{document}   \r');
    fobw.writelines('\\  \\footnote{ Compiled on \\today\ at \\currenttime} \r' );
    fobw.write('\r Break Points(1Mb) \r' );
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
            base_breakpoint = [item.Break_Points for item in gresults if item.method == 'Uncorrected' and item.genomeName==g]
            for r in gresults:
                if (r.genomeName==g and r.method==m and r.Break_Points!=""):
		    tempVal=" & " +'{0:.2f}'.format(round (float (int (r.Break_Points)-int (base_breakpoint[0]))*1000000/float (r.genomeSize), 2))
                    find=1;
            if (find):
                tempLine=tempLine+tempVal
            else:
                tempLine=tempLine+"& n/a "         
        tempLine=tempLine+"\\\ \r"
        fobw.write(tempLine)
    fobw.writelines("\\toprule\r");
    fobw.write('\end{tabular}');
    fobw.write('\\\ \r')

    fobw.write( '\end{document}')
    fobw.close();                        
def makeLostKmers(gresults,methodNameSet,genomeNameSet,outFileName):
    fobw=open(outFileName+"_lostKmers_only.tex",'w')
    #print (outFileName+"_"+gainName+"_only.tex")
    #covSet.pop(0);
    fobw.writelines("\documentclass[a4paper,10pt]{article} \r");

    fobw.writelines(" \\usepackage{datetime} \r")
    fobw.writelines(" \\usepackage{booktabs} \r")
    
    fobw.writelines('\\begin{document}   \r');
    fobw.writelines('\\  \\footnote{ Compiled on \\today\ at \\currenttime} \r' );
    fobw.write('\r Lost true kmers per Mb \r' );
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
	    base_kmerLost   = [item.kmerLost for item in gresults if item.method == 'Uncorrected' and item.genomeName==g]
	    tempVal="";
	    find=0
            for r in gresults:
		
                if (r.genomeName==g and r.method==m and r.kmerLost!=""):
                    tempVal=" & " +'{0:.2f}'.format(round ((r.kmerLost-base_kmerLost[0]) *1000000/float (r.genomeSize), 2))
                    #tempVal=" & " +str (r.kmerLost)
                    find=1;
            if (find):
                tempLine=tempLine+tempVal
            else:
                tempLine=tempLine+"& n/a "         
        tempLine=tempLine+"\\\ \r"
        fobw.write(tempLine)
    fobw.writelines("\\toprule\r");
    fobw.write('\end{tabular}');
    fobw.write('\\\ \r')

    fobw.write( '\end{document}')
    fobw.close();                
def MakeReaMappedTable(gresults,methodNameSet,genomeNameSet,outFileName, relative, normalized):
    if (relative==1):
	outFileName=outFileName+".relative.tex"
    fobw=open(outFileName,'w')
    fobw.writelines("\documentclass[a4paper,10pt]{article} \r");
    fobw.writelines(" \\usepackage{multirow} \r");
    fobw.writelines(" \\usepackage{pdflscape} \r");
    fobw.writelines(" \\usepackage{adjustbox} \r")
    fobw.writelines(" \\usepackage{datetime} \r")
    fobw.writelines('\\begin{document}   \r');
      
    fobw.writelines('\\begin{landscape}   \r');
    fobw.writelines('\\  \\footnote{ Compiled on \\today\ at \\currenttime} \r' );
    fobw.write('Quality of De Bruijn graph contigs after Error Correction\r' );
    fobw.write('\\\ \r')
    fobw.write('\\\ \r')
    fobw.write('\\begin{adjustbox}{width=1.5\\textwidth}')
    
    fobw.write('\\begin{tabular}{|c|c|} \r' );
    fobw.write(' \cline{1-2} \r')
    fobw.write(' \multicolumn{1}{ |c| } {ShortName} & \multicolumn{1}{ |c| }{LongName} ' )
    fobw.write('\\\ \r')
    fobw.write(' \cline{1-2} \r')
    fobw.write(' \cline{1-2} \r')
    i=1
    for g in genomeNameSet:
        fobw.write(' \multicolumn{1}{ |c| } {D'+str(i)+'} & \multicolumn{1}{ |c| }')
	if (i==1):
	    fobw.write('{Bifidobacterium dentium}')
        if (i==2):
	    fobw.write('{E. coli str. K-12 substr. DH10B}')
	if (i==3):
	    fobw.write('{E. coli str. K-12 substr. MG1655}')
	if (i==4):
	    fobw.write('{Salmonella enterica}')
	if (i==5):
	    fobw.write('{Pseudomonas aeruginosa}')
	if (i==6):
	    fobw.write('{Human Chr 21}')
	if (i==7):
	    fobw.write('{Caenorhabditis elegans}')
	if (i==8):
	    fobw.write('{Drosophila melanogaster}')

        fobw.write('\\\ \cline{1-2} ')
        i=i+1
    fobw.write("\n")
    fobw.write('\end{tabular}\r');
    

    fobw.write('\\begin{tabular}{' );
 
    factorSet=set();
    #factorSet.add("N50")
    #factorSet.add("genome coverage")
    #factorSet.add("kmers Exist")
    #factorSet.add("Break Points")
    #factorSet.add("graph size")
    #factorSet.add("number nodes")
    #factorSet.add("number arcs")
    #factorSet.add("largest contig")
    #factorSet.add("nodeExist")
    
    if (normalized==1):
	factorSet.add("Lost true kmers per Mb")
	factorSet.add("Break Points(1Mb)")
    else:
	factorSet.add("Lost true kmers")
	factorSet.add("Break Points")
	
    factorSet=sorted(factorSet)
    colNum=len(genomeNameSet)+2;
    temp="|c|"
    i=1;
    while (i<colNum):
        temp=temp+"c|"
        i=i+1
    fobw.writelines(temp+"l}\r");
    fobw.writelines("\cline{1-"+str(colNum)+"} \r");
    fobw.writelines("\multicolumn{1}{ |c } {} &\multicolumn{1}{ |c| } {Methods} & \multicolumn{"+str( colNum-2)+"}{ c| }{Sequences} \\\ \cline{3-"+str(colNum)+"} \r");
    fobw.write("\multicolumn{1}{ |c } {} &\multicolumn{1}{ |c| } {}")
    temp=""
    i=1
    for g in genomeNameSet:
        temp=temp+' & '+g
        i=i+1
    fobw.writelines(temp+" \\\ \cline{1-"+str(colNum)+"} \r");
    
    for factor_item in factorSet:
        fobw.write('\multicolumn{1}{ |c  }{\multirow{2}{*}{'+str(factor_item )+'} } & \r')
        i=0;
        for meth_item in methodNameSet:
            
            fobw.write('\multicolumn{1}{ |c| }{'+meth_item+'}')
            tempLine="";
            for g in genomeNameSet:
                tempVal=""
                find =0;
                for r in gresults:
                    #print(r.Break_Points)
                    if (r.genomeName==g ):
			base_breakpoint = [item.Break_Points for item in gresults if item.method == 'Uncorrected' and item.genomeName==g]
		        base_kmerLost   = [item.kmerLost for item in gresults if item.method == 'Uncorrected' and item.genomeName==g]
		        #print(base_breakpoint[0])
		        #print(base_kmerLost[0])
                        if (r.method==meth_item):
                            
			    if(factor_item=="Lost true kmers per Mb" and r.kmerLost!=""):
                                    if (relative==1):
					tempVal=" & " + '{0:.2f}'.format(round ((r.kmerLost-base_kmerLost[0]) *1000000/float (r.genomeSize), 2))
                                    else:
					tempVal=" & " +'{0:.2f}'.format (round ((r.kmerLost) *1000000/float (r.genomeSize), 2))
                                    find=1;
                            if(factor_item=="Break Points(1Mb)" and r.Break_Points!=""):
                                    #r.breakpointsRel=print (str (round (float (int (r.Break_Points)-int (base_breakpoint[0]))*1000000/float (r.genomeSize), 2)))
				    if (relative==1):
					tempVal=" & " +'{0:.2f}'.format (round (float (int (r.Break_Points)-int (base_breakpoint[0]))*1000000/float (r.genomeSize), 2))
				    else:
					tempVal=" & "+'{0:.2f}'.format (round (float (int (r.Break_Points))*1000000/float (r.genomeSize), 2))
                                    find=1;
                            if(factor_item=="N50"):
                                    tempVal=" & " +r.N50
                                    find=1;
                            if(factor_item=="genome coverage"):
                                    tempVal=" & "+r.genome_coverage
                                    find=1;
                            if(factor_item=="graph size"):
                                    tempVal=" & " +r.graph_size
                                    find=1;
                            if(factor_item=="number nodes"):
                                    tempVal=" & "+r.number_nodes
                                    find=1;
                            if(factor_item=="number arcs"):
                                    tempVal=" & " +r.number_arcs
                                    find=1;
                            if(factor_item=="largest contig"):
                                    tempVal=" & "+r.largest_contig
                                    find=1;
                            if(factor_item=="Break Points" and r.Break_Points<>""):
				    #print(r.Break_Points)
				    if (relative==1):
					tempVal=" & "+str( int(r.Break_Points)- int (base_breakpoint[0]))
				    else:
					tempVal=" & "+r.Break_Points
                                    find=1;
                            if(factor_item=="Lost true kmers" and r.kmerLost<>""):
				    #print(r.kmerLost)
				    if (relative==1):
					tempVal=" & "+str(r.kmerLost-base_kmerLost[0])
				    else:
					tempVal=" & "+str(r.kmerLost)
                                    find=1;
                            if(factor_item=="kmers Exist"):
                                    tempVal=" & "+r.kmersExist.replace("%", "\%")
                                    find=1;
                            if(factor_item=="nodeExist"):
                                    tempVal=" & "+r.nodeExist.replace("%", "\%")
                                    find=1;

                if (find):
                    tempLine=tempLine+tempVal
                else:
                    tempLine=tempLine+" & "+"na "
            tempLine=tempLine+' & '
            fobw.write(tempLine)
            i=i+1;
            if i!= len(methodNameSet):
                fobw.write ('\\\ \cline{2-'+str(colNum)+'}\r \multicolumn{1}{ |c  }{}      &\r')
        fobw.write('\\\ \cline{1-'+str(colNum)+'}\r')      
   
    fobw.write('\end{tabular}');

    fobw.write('\\\ \r')
    #fobw.write('\\\ \r')
    #fobw.write('\\\ \r')
    #fobw.write('\\\ \r')

    fobw.write('\end{adjustbox}')
    fobw.write( '\end{landscape}')

    fobw.write( '\end{document}')
    fobw.close();
    
def makeMappedReal():
    #subprocess.call("scp vsc41448@gengar.ugent.be:./Result/run_produceResultTable_script/RealDataMapped/log.txt ./Mappedlog.txt", shell=True)
    #fobr=open('deBruijn_Log.txt','r')
    fobr=open(sys.argv[1],'r')
    s= fobr.read();
    methods = s.split("The results for next method:")
    methods.pop(0)
    results=[];
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
            graph_size=find_between(genome ,"Total size (kmers): ", "\n")
            largest_contig=find_between(genome ,"The largest node contains ", " basepairs.")
            #print(largest_contig)
            number_nodes=find_between(genome ,"Extracted ", " nodes and")
            number_arcs=find_between(genome ," nodes and ", " arcs.")
            genomeNameSet.add(genomeName)
            methodNameSet.add(methodName)
            r = Result()
            r.genomeName=genomeName
            #print(r.genomeName)
            r.method=methodName
            r.N50=N50
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
            

            if (kmerLost!="" and Break_Points!=""):
                r.kmerLostRel=round (r.kmerLost*1000000/float (r.genomeSize), 2)
                #print(r.Break_Points)    
                r.breakpointsRel=round (float (Break_Points)*1000000/float (r.genomeSize), 2)
            results.append(r)
    results=sorted(results, key=attrgetter('method', 'genomeName'))
    genomeNameSet=sorted(genomeNameSet)
    methodNameSet=sorted(methodNameSet)
    colNum=2+len(genomeNameSet);

    
    MakeReaMappedTable(results,methodNameSet,genomeNameSet,sys.argv[2],0,0);
    MakeReaMappedTable(results,methodNameSet,genomeNameSet,sys.argv[2],1,1);
    makeBreakpoint(results,methodNameSet,genomeNameSet,sys.argv[2])
    makeLostKmers(results,methodNameSet,genomeNameSet,sys.argv[2])
    fobr.close();
    
makeMappedReal()
