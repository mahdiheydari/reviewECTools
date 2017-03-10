'''
Copyright (C) 2016  Mahdi Heydari
This script makes the tables for the mismatches and essential files to make the plots. 
It should be run afte running countMismatch.py'''
import subprocess
from math import pi
import sys
class Result:
 genomName=""   
 method=""
 directory=""
 numberOfAllReads=0
 _00_matches=0
 _01_matches=0
 _02_matches=0
 _03_matches=0
 _04_matches=0
 _05_matches=0
 _06_matches=0
 _07_matches=0
 _08_matches=0
 _09_matches=0
 _m9_matches=0
 
 _1_2_matches=0
 _3_5_matches=0
 _6_9_matches=0
 _1_9_matches=0
 
 _01_matches_per=""
 _02_matches_per=""
 _1_2_matches_per=""
 _3_5_matches_per=""
 _6_9_matches_per=""
 
 _1_9_matches_per=""
 _00_matches_per=""
 _m9_matches_per=""

def changeMethodsName(inputName):
    if (inputName=="ace" ):
	return "ACE"
    if (inputName=="blue" ):
	return "Blue"
    if (inputName=="bless" ):
	return "BLESS2"    
    if (inputName=="bayesHammer" ):
	return "BayesHammer"                
    if (inputName=="bfc" ):
	return "BFC"
    if (inputName=="musket" ):
	return "Musket"
    if (inputName=="lighter" ):
	return "Lighter"
    if (inputName=="karect" ):
	return "Karect"                
    if (inputName=="fiona" ):
	return "Fiona"
    if (inputName=="trowel" ):
	return "Trowel"
    if (inputName=="racer" ):
	return "RACER"
    if (inputName=="sga" ):
	return "SGA-EC"
    if (inputName=="initial" ):
	return "Uncorrected"
    if (inputName=="Uncorrected" ):
	return "Uncorrected"
    
    return "null"
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""
def plotStackBar(methodNameSet,genomeNameSet,results,outFileName):
    genomeNameSet=sorted(genomeNameSet)
    methodNameSet=sorted(methodNameSet)
    allDataSets=[];
    fobwa=open("real/countMismatch/all.dat",'w');
 
    for g in genomeNameSet:
        fobw=open("real/countMismatch/"+g+".dat",'w')
        fobwa.writelines("# the following table represent number of mismatches in "+g+'\n');
        dataset=[];
        fobw.writelines("tools	0	1	2	3	4	5	6	7	8	9	m9	all"+'\n');
        fobwa.writelines("tools	0	1	2	3	4	5	6	7	8	9	m9	all"+'\n');
        for r in results:
            if (r.genomName==g): 
                for m in methodNameSet:
                    row=[];
                    order=[]
                    color=[]
                    if (r.method==m):
                        row=m+'  '+str(r._00_matches)+' '+str(r._01_matches)+' '+str(r._02_matches)+' '+str(r._03_matches)+' '+str(r._04_matches)+' '+str(r._05_matches)+' '+str(r._06_matches)+' '+str(r._07_matches)+' '+str(r._08_matches)+' '+str(r._09_matches)+'  '+str(r._m9_matches)+'    '+str(r.numberOfAllReads)
                        fobw.writelines(row+'\n')
                        fobwa.writelines(row+'\n');
                    
        fobw.close();
        fobwa.writelines('#\n');
        allDataSets.append(dataset)
    fobwa.close();
    
    
def plotStackBarPer(methodNameSet,genomeNameSet,results,outFileName):
    genomeNameSet=sorted(genomeNameSet)
    methodNameSet=sorted(methodNameSet)
    allDataSets=[];
    fobwa=open("real/countMismatch/all_per.dat",'w');
 
    for g in genomeNameSet:
        fobw=open("real/countMismatch/"+g+"_per_.dat",'w')
        fobwa.writelines("# the following table represent number of mismatches in "+g+'\n');
        dataset=[];
        fobw.writelines("tools	m_0\tm_1\tm_2\tm_3_5\tm_6_9\tm_+9\tm_1_9"+'\n');
        fobwa.writelines("tools	m_0\tm_1\tm_2\tm_3_5\tm_6_9\tm_+9\tm_1_9"+'\n');
        for r in results:
            if (r.genomName==g): 
                for m in methodNameSet:
                    row=[];
                    order=[]
                    color=[]
                    if (r.method==m):
                        row=changeMethodsName(m)+"	"+str(r._00_matches_per)+"\t"+str (r._01_matches_per)+"\t"+str (r._02_matches_per)+"\t"+str(r._3_5_matches_per)+"\t"+str(r._6_9_matches_per)+"\t"+str(r._m9_matches_per)+"\t"+str(r._1_9_matches_per)
                        fobw.writelines(row+'\n')
                        fobwa.writelines(row+'\n');
                    
        fobw.close();
        fobwa.writelines('#\n');
        allDataSets.append(dataset)
    fobwa.close();

def makeMismatchTable(results,genomeNameSet,methodNameSet,outFileName):
    fobw=open(outFileName,'w')
    #covSet.pop(0);
    fobw.writelines("\documentclass[a4paper,10pt]{article} \r");
    fobw.writelines(" \\usepackage{multirow} \r");
    fobw.writelines(" \\usepackage{pdflscape} \r");
    fobw.writelines(" \\usepackage{adjustbox} \r")
    fobw.writelines(" \\usepackage{datetime} \r")
    fobw.writelines('\\begin{document}   \r');
    fobw.writelines('\\  \\footnote{ Compiled on \\today\ at \\currenttime} \r' );
    fobw.write('\r percentages of reads which mapped with 0 mismatches and don not match even allowing 9 mismatches\r' );
    fobw.write('\\\ \r')
    fobw.write('\\\ \r')
    fobw.write('\\begin{adjustbox}{width=1\\textwidth}')
    fobw.write('\\begin{tabular}{' );
    temp="|c|"
    import math
    colNum=1+len(genomeNameSet)*2
    i=1;
    
    while (i<colNum):
        temp=temp+"c|"
        i=i+1

    fobw.writelines(temp+"l}\r");
    fobw.writelines("\cline{1-"+str(colNum)+"} \r");
    temp="";
    i=1;
    genomeNameSet=sorted(genomeNameSet)
    for genome in genomeNameSet:
        temp=temp+"&\multicolumn{2}{ |c| } {"+genome+"}";
        i=i+1;
    fobw.writelines("\multicolumn{1}{ |c| }{kmerSize} "+temp)
    fobw.write('\\\ \r')
    fobw.writelines("\cline{1-"+str(colNum)+"} \r");


    temp="";
    for genome in genomeNameSet:
        temp=temp+"&{0Mis\%} &{m9Mis\%} ";
    
    fobw.writelines("\multicolumn{1}{ |c| } {}"+temp)
    fobw.write('\\\ \r')
    fobw.writelines("\cline{1-"+str(colNum)+"} \r");

    for m in methodNameSet:
        tempLine="\multicolumn{1}{ |c| }{"+m+"}"
        for g in genomeNameSet:
            find=0;
            for r in results: 
                if (r.genomName==g and r.method==m):
                    tempVal="";
                    #tempVal=" & "+'{0:.2f}'.format(round(r._00_matches_per,2))+" & "+'{0:.2f}'.format(round (r._1_9_matches_per,2))
                    tempVal=" & "+r._00_matches_per+" & "+r._1_9_matches_per
                    find=1;
            if (find):
                tempLine=tempLine+tempVal
            else:
                tempLine=tempLine+"& N/A & N/A"         
        tempLine=tempLine+"\\\ \r"
        fobw.write(tempLine)
        fobw.writelines("\cline{1-"+str(colNum)+"} \r"); 
    fobw.write('\end{tabular}');
    fobw.write('\\\ \r')
    #fobw.write('\\\ \r')
    #fobw.write('\\\ \r')
    #fobw.write('\\\ \r')
    fobw.write('\\begin{tabular}{|c|c|} \r' );
    fobw.write(' \cline{1-2} \r')
    
    fobw.write(' \multicolumn{1}{ |c| } {ShortName} & \multicolumn{1}{ |c| }{LongName} ' )
    fobw.write('\\\ \r')
    fobw.write(' \cline{1-2} \r')
    fobw.write(' \cline{1-2} \r')
    i=1
    for g in genomeNameSet:
        fobw.write(' \multicolumn{1}{ |c| } {D\\_'+str(i)+'} & \multicolumn{1}{ |c| }{'+g.replace("_", ".")+'}\r' )
        fobw.write('\\\ \cline{1-2} ')
        i=i+1
    fobw.write("\n")
    fobw.write('\end{tabular}\r');
    fobw.write( '\end{adjustbox}')
    fobw.write( '\end{document}')
    fobw.close();

def makeMismatchTable_0_M(results,genomeNameSet,methodNameSet,outFileName):
    fobw=open(outFileName,'w')
    #covSet.pop(0);
    fobw.writelines("\documentclass[a4paper,10pt]{article} \r");
    fobw.writelines(" \\usepackage{xcolor} \r");
    fobw.writelines(" \\usepackage{pgf} \r");
    fobw.writelines(" \\usepackage{collcell} \r")
    fobw.writelines(" \\usepackage{multirow} \r");
    fobw.writelines(" \\usepackage{pdflscape} \r");
    fobw.writelines(" \\usepackage{adjustbox} \r")
    fobw.writelines(" \\usepackage{datetime} \r")
    fobw.writelines(" \\usepackage{booktabs} \r")
    
    fobw.writelines("\\newcommand*{\MinNumber}{0}\r");
    fobw.writelines("\\newcommand*{\MaxNumber}{100}\r");
    
    fobw.writelines("\\newcommand{\ApplyGradient}[1]{\r");
    fobw.writelines("\\pgfmathsetmacro{\PercentColor}{100.0*(#1-\MinNumber)/(\MaxNumber-\MinNumber)}\r");
    fobw.writelines("\\textcolor{black!\PercentColor}{#1}\r");
    fobw.writelines("}\r");
    fobw.writelines("\\newcolumntype{R}{>{\\collectcell\\ApplyGradient}{r}<{\\endcollectcell}}\r");
    fobw.writelines("\\newcolumntype{N}{>{\\collectcell\\ApplyGradient}{r}<{\\endcollectcell}}\r");
    
    fobw.writelines('\\begin{document}   \r');
    fobw.writelines('\\  \\footnote{ Compiled on \\today\ at \\currenttime} \r' );
    fobw.write('\r Percentages of reads which mapped with 0 mismatches \r' );
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
                if (r.genomName==g and r.method==m):
                    tempVal="";
                    #tempVal=" & "'{0:.2f}'.format(round(r._00_matches_per,2)) #+" & "+str (round (r._1_9_matches_per,2))
                    tempVal=" & "+ str(r._00_matches_per);
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



def makeMismatchTable_m_9(results,genomeNameSet,methodNameSet,outFileName):
    fobw=open(outFileName,'w')
    #covSet.pop(0);
    fobw.writelines("\documentclass[a4paper,10pt]{article} \r");
    fobw.writelines(" \\usepackage{xcolor} \r");
    fobw.writelines(" \\usepackage{pgf} \r");
    fobw.writelines(" \\usepackage{collcell} \r")
    fobw.writelines(" \\usepackage{multirow} \r");
    fobw.writelines(" \\usepackage{pdflscape} \r");
    fobw.writelines(" \\usepackage{adjustbox} \r")
    fobw.writelines(" \\usepackage{datetime} \r")
    fobw.writelines(" \\usepackage{booktabs} \r")
    
    fobw.writelines("\\newcommand*{\MinNumber}{0}\r");
    fobw.writelines("\\newcommand*{\MaxNumber}{100}\r");
    
    fobw.writelines("\\newcommand{\ApplyGradientCool}[1]{\r");
    fobw.writelines("\\pgfmathsetmacro{\PercentColor}{100.0*(\MaxNumber-#1)/(\MaxNumber-\MinNumber)}\r");
    fobw.writelines("\\textcolor{black!\PercentColor}{#1}\r");
    fobw.writelines("}\r");

    fobw.writelines("\\newcolumntype{N}{>{\\collectcell\\ApplyGradientCool}{r}<{\\endcollectcell}}\r");
    
    fobw.writelines('\\begin{document}   \r');
    fobw.writelines('\\  \\footnote{ Compiled on \\today\ at \\currenttime} \r' );
    fobw.write('\r Percentages of reads which do not align allowing less than 9 mismatches \r' );
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
                if (r.genomName==g and r.method==m):
                    tempVal="";
                    #tempVal=" & "+'{0:.2f}'.format(round (r._m9_matches_per,2))
                    tempVal=" & "+ r._m9_matches_per;
                    find=1;
            if (find):
                tempLine=tempLine+tempVal
            else:
                tempLine=tempLine+"&\multicolumn{1}{ c } {NA}"         
        tempLine=tempLine+"\\\ \r"
        fobw.write(tempLine)
    fobw.writelines("\\toprule\r");
    fobw.write('\end{tabular}');
    fobw.write('\\\ \r')
    fobw.write( '\end{document}')
    fobw.close();

def especifyMin_M9(methodNameSet,genomeNameSet,results):
    for g in genomeNameSet:
        minM_9_Set=set();
        for r in results:
            if (r.genomName==g):
                minM_9_Set.add(float (r._m9_matches_per))
        minM_9=min(minM_9_Set)
        for r in results:
            if (r.genomName==g ):
                if (float (r._m9_matches_per )==minM_9):
                    r._m9_matches_per="\\bf{" +str(r._m9_matches_per)+"}"
def especifyMax_M0(methodNameSet,genomeNameSet,results):
    for g in genomeNameSet:
        max_M0_set=set();
        for r in results:
            if (r.genomName==g ):
                max_M0_set.add(float( r._00_matches_per))
        maxM_0=max(max_M0_set)
        for r in results:
            if (r.genomName==g  ):
                if ( float(r._00_matches_per )== maxM_0):
                    r._00_matches_per="\\bf{" +str(r._00_matches_per)+"}"
def extractMismatch():
    #subprocess.call("scp vsc41448@gengar.ugent.be:./Result/run_produceResultTable_script/RealData/logBWAcountMisMatch.txt ./realDataMismatchNum.txt", shell=True)
    gfr= open(sys.argv[1],'r')
    #gfr= dkobr=open("logFiles/BWAlogTest.txt",'r')
    
    s= gfr.read();
    methods = s.split("The results for next method:")
    methods.pop(0)
    results=[];
    genomeNameSet=set();
    methodNameSet=set();
    for method in methods:
        #print(method)
        methodName= find_between(method , "the method name is<<", ">>." )
        methodNameSet.add(methodName)
        #print(methodName)
        genomes=method.split("next DataSet Starts<<");
        genomes.pop(0)
        for genome in genomes:
            #print(genome)
            genomSize=find_between(genome , "the size of the genome is:<< ", ">>" )
            genomeName=find_between( genome, "The dataSet is<< ", " >>" )
            #print(genomeName)
            if (genomeName!="E.coli_SRR522163" and genomeName!="Ostreococcus"):
                if (genomeName=="B.dentium_SRR1151311"):
                    genomeName="D1"
                if (genomeName=="C.elegans_SRR543736"):
                    genomeName="D2"
                if (genomeName=="D.melanogaster_SRR823377"):
                    genomeName="D3"
                if (genomeName=="E.coli_str.K-12_substr.DH10B"):
                    genomeName="D4"
                if (genomeName=="E.coli_str.K-12_substr.MG1655"):
                    genomeName="D5"
                if (genomeName=="HiSeq_chr21"):
                    genomeName="D6"
                if (genomeName=="P.seudomonas_ERR330008_120"):
                    genomeName="D7"
                if (genomeName=="S.enterica_SRR1206093"):
                    genomeName="D8"
                genomeNameSet.add(genomeName)
                #print(genomeName)
                r = Result()
                r.genomName=genomeName
                r.method=methodName
             
                if ("only 0 mismatches" in genome):
                    
                    r._00_matches=float(find_between(genome , "     only 0 mismatches : <<', ", ", '>>'" ))
                    r._01_matches=float(find_between(genome , "     only 1 mismatches : <<', ", ", '>>'" ))
                    r._02_matches=float(find_between(genome , "     only 2 mismatches : <<', ", ", '>>'" ))
                    r._03_matches=float(find_between(genome , "     only 3 mismatches : <<', ", ", '>>'" ))
                    r._04_matches=float(find_between(genome , "     only 4 mismatches : <<', ", ", '>>'" ))
                    r._05_matches=float(find_between(genome , "     only 5 mismatches : <<', ", ", '>>'" ))
                    r._06_matches=float(find_between(genome , "     only 6 mismatches : <<', ", ", '>>'" ))
                    r._07_matches=float(find_between(genome , "     only 7 mismatches : <<', ", ", '>>'" ))
                    r._08_matches=float(find_between(genome , "     only 8 mismatches : <<', ", ", '>>'" ))
                    r._09_matches=float(find_between(genome , "     only 9 mismatches : <<', ", ", '>>'" ))
                    r._m9_matches=float(find_between(genome , "more than 9 mismatches : <<', ", ", '>>'" ))

                    r._1_9_matches=r._01_matches+r._02_matches+r._03_matches+r._04_matches+r._05_matches+r._06_matches+r._07_matches+r._08_matches+r._09_matches
                    
                    r._1_2_matches=r._01_matches+r._02_matches;
		    r._3_5_matches=r._03_matches+r._04_matches+r._05_matches
		    r._6_9_matches=r._06_matches+r._07_matches+r._08_matches+r._09_matches
		    
                    r.numberOfAllReads=r._00_matches+r._01_matches+r._02_matches+r._03_matches+r._04_matches+r._05_matches+r._06_matches+r._07_matches+r._08_matches+r._09_matches+r._m9_matches
                    if (r.numberOfAllReads==0):
                        r._1_9_matches_per=0
                    else:
                        r._1_9_matches_per=r._1_9_matches*100/r.numberOfAllReads
                        r._1_9_matches_per='{00:.2f}'.format(round (r._1_9_matches_per,4))
                        
                    if (r.numberOfAllReads==0):
                        r._00_matches_per=0
                    else:
                        r._00_matches_per=r._00_matches*100/r.numberOfAllReads
                        r._00_matches_per='{00:.2f}'.format(round (r._00_matches_per, 4))

                        
                    if (r.numberOfAllReads==0):
                        r._m9_matches_per=0
                    else:
                        r._m9_matches_per=r._m9_matches*100/r.numberOfAllReads
                        r._m9_matches_per='{00:.2f}'.format(round (r._m9_matches_per, 4))


                    if (r.numberOfAllReads==0):
                        r._1_2_matches_per=0
                    else:
                        r._1_2_matches_per=r._1_2_matches*100/r.numberOfAllReads
                        r._1_2_matches_per='{00:.2f}'.format(round (r._1_2_matches_per,4))


                    if (r.numberOfAllReads==0):
                        r._3_5_matches_per=0
                    else:
                        r._3_5_matches_per=r._3_5_matches*100/r.numberOfAllReads
                        r._3_5_matches_per='{00:.2f}'.format(round (r._3_5_matches_per,4))



                    if (r.numberOfAllReads==0):
                        r._6_9_matches_per=0
                    else:
                        r._6_9_matches_per=r._6_9_matches*100/r.numberOfAllReads
                        r._6_9_matches_per='{00:.2f}'.format(round (r._6_9_matches_per,4))
                    
                    
                    if (r.numberOfAllReads==0):
                        r._01_matches_per=0
                    else:
                        r._01_matches_per=r._01_matches*100/r.numberOfAllReads
                        r._01_matches_per='{00:.2f}'.format(round (r._01_matches_per,4))
                    
                    if (r.numberOfAllReads==0):
                        r._02_matches_per=0
                    else:
                        r._02_matches_per=r._02_matches*100/r.numberOfAllReads
                        r._02_matches_per='{00:.2f}'.format(round (r._02_matches_per,4))
                    
                    
                    results.append(r)

    from operator import attrgetter
    results=sorted(results, key=attrgetter('method'))
    genomeNameSet=sorted(genomeNameSet)
    methodNameSet=sorted(methodNameSet)
    plotStackBar(methodNameSet,genomeNameSet,results,"outfig")
    plotStackBarPer(methodNameSet,genomeNameSet,results,"outfig")
    especifyMin_M9(methodNameSet,genomeNameSet,results);
    especifyMax_M0(methodNameSet,genomeNameSet,results);


    makeMismatchTable_0_M(results,genomeNameSet,methodNameSet,sys.argv[2]);
    makeMismatchTable_m_9(results,genomeNameSet,methodNameSet,sys.argv[3]);
    #subprocess.call("gnuplot -e \"filename='all.dat'\" countMismatch\/plot.dem", shell=True)
extractMismatch()
