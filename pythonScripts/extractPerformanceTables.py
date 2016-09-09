import os, sys
import subprocess
import time
import math
from operator import itemgetter, attrgetter, methodcaller
class Result:
 genomName=""   
 method=""
 memory=0.0
 runTime=0.0
 wallTime=0.0
 wallTime_minute=""

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

def plotStackBarRunTime(methodNameSet,genomeNameSet,results):
    path = 'real/plots/runTime'
    fobw=open(path+"/allRuntime.dat", 'w')
    fobw.writelines("dataSet")
    for m in methodNameSet:
        if (m!="brownie" ):
            fobw.writelines("\t"+m);
    fobw.writelines("\n");    
    for g in genomeNameSet:
        row=g
        for r in results:
            if (r.genomName==g): 
                for m in methodNameSet:       
                    if (r.method==m and m!="brownie"):
                        row=row+"\t"+ '{0:.2f}'.format(round (float (r.wallTime)/60,2))
        fobw.writelines(row+'\n')
def plotStackBarMemory(methodNameSet,genomeNameSet,results):
    path = 'real/plots/memory'
    fobw=open(path+"/memory.dat", 'w')
    fobw.writelines("dataSet")
    for m in methodNameSet:
        if (m!="brownie" ):
            fobw.writelines("\t"+m);
    fobw.writelines("\n");    
    for g in genomeNameSet:
        row=g
        for r in results:
            if (r.genomName==g): 
                for m in methodNameSet:       
                    if (r.method==m and m!="brownie" ):
                        row=row+"\t"+ r.memory
        fobw.writelines(row+'\n')       
def especifyMin_wallTime(genomeNameSet,results):
    for g in genomeNameSet:
        max_set=set();
        for r in results:
            if (r.genomName==g ):
                if (r.wallTime=="" or r.wallTime=="na" or r.wallTime=="nan"):
                    r.wallTime="na"
                else:
                    max_set.add(float( r.wallTime))
                    #print(r.wallTime)
        min_R=min(max_set)
        for r in results:
            if (r.genomName==g  ):
                if (r.wallTime!="na" and float(r.wallTime )== min_R):
                    r.wallTime_minute="\\bf{"+ '{0:.2f}'.format(round (float (r.wallTime)/60, 2))+"}"
                    r.wallTime="\\bf{" +time.strftime("%H:%M:%S", time.gmtime(r.wallTime))+"}"
                else:
                    r.wallTime_minute='{0:.2f}'.format(round (float (r.wallTime)/60,2))
                    r.wallTime=time.strftime("%H:%M:%S", time.gmtime(r.wallTime))
                   
def especifyMin_Memory(genomeNameSet,results):
    for g in genomeNameSet:
        min_set=set();
        for r in results:
            if (r.genomName==g ):
                if (r.memory=="" or r.memory=="na" or r.memory=="nan"):
                    r.memory="na"
                else:
                    min_set.add(float( r.memory))
        min_M=min(min_set)
        for r in results:
            if (r.genomName==g  ):
                if (r.memory!="na" and float(r.memory )== min_M):
                    r.memory="\\bf{" +r.memory+"}"


def makeMemory(results,genomeNameSet,methodNameSet,outFileName):
    fobw=open(outFileName,'w')
    #covSet.pop(0);
    fobw.writelines("\documentclass[a4paper,10pt]{article} \r");

    fobw.writelines(" \\usepackage{datetime} \r")
    fobw.writelines(" \\usepackage{booktabs} \r")
    
 
    
    fobw.writelines('\\begin{document}   \r');
    fobw.writelines('\\  \\footnote{ Compiled on \\today\ at \\currenttime} \r' );
    fobw.write('\r Memory(GB) \r' );
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
                    tempVal=" & "+ str(r.memory);
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

def makeRuntime(results,genomeNameSet,methodNameSet,outFileName):
    fobw=open(outFileName,'w')
    #covSet.pop(0);
    fobw.writelines("\documentclass[a4paper,10pt]{article} \r");

    fobw.writelines(" \\usepackage{datetime} \r")
    fobw.writelines(" \\usepackage{booktabs} \r")
    
 
    
    fobw.writelines('\\begin{document}   \r');
    fobw.writelines('\\  \\footnote{ Compiled on \\today\ at \\currenttime} \r' );
    fobw.write('\r runTime \r' );
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
                    tempVal=" & "+ str(r.wallTime_minute);
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



def MakePerformanceTable(gresults,methodNameSet,genomeNameSet,outFileName):
   
    fobw=open(outFileName,'w')
    fobw.writelines("\documentclass[a4paper,10pt]{article} \r");
    fobw.writelines(" \\usepackage{multirow} \r");
    fobw.writelines(" \\usepackage{pdflscape} \r");
    fobw.writelines(" \\usepackage{adjustbox} \r")
    fobw.writelines(" \\usepackage{datetime} \r")
    fobw.writelines('\\begin{document}   \r');
    fobw.writelines('\\begin{landscape}   \r');
    fobw.writelines('\\  \\footnote{ Compiled on \\today\ at \\currenttime} \r' );
    fobw.write('Comparison of different methods on real DataSets\r' );
    fobw.write('\\\ \r')
    fobw.write('\\\ \r')
    fobw.write('\\begin{adjustbox}{width=2\\textwidth}')
    fobw.write('\\begin{tabular}{' );
 
    factorSet=set();
    factorSet.add("Memory(GB)")
    factorSet.add("Run Time(hh:mm:ss)")    
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
            #print("2:hi , not here?")
            fobw.write('\multicolumn{1}{ |c| }{'+meth_item+'}')
            tempLine="";
            for g in genomeNameSet:
                tempVal=""
                find =0;
                for r in gresults:
                    if (r.genomName==g ):
                        if (r.method==meth_item):                            
                            if(factor_item=="Memory(GB)"):
                                tempVal=" & " +str (r.memory)
                                find=1;
                            if(factor_item=="Run Time(hh:mm:ss)"):
                                tempVal=" & "+str(r.wallTime)
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
    #fobr=open('logFiles/infoLog.txt','r')
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
        for genome in genomes:
            genomSize=find_between(genome , "the size of the genome is:<< ", ">>" )
            genomeName=find_between( genome, "The dataSet is<< ", " >>" )
            
            parts = genome.split("Command being timed:")
            parts.pop(0)
            memory=0
            runTime=0
            second =0
            for part in parts:
                temp=find_between(part ,"Maximum resident set size (kbytes): ", "\n").strip()
                if (int(temp)>memory):
                    memory=(float (temp))
                temp=find_between(part ,"User time (seconds): ", "\n").strip()
                runTime=runTime+(float(temp))
                
                temp=find_between(part, "Elapsed (wall clock) time (h:mm:ss or m:ss):", "\n").strip()
                
                timeParts = temp.split(":")
                timeParts=timeParts[::-1]
                timeIndex=1
                second=second+float (timeParts[0])
                while (timeIndex<len(timeParts)):
                    second=second+math.pow(60, timeIndex)* float (timeParts[timeIndex])
                    timeIndex=timeIndex+1
                

            memory=(float (memory)/1000000)
            memory='{0:.2f}'.format(round( float( memory),2))
            if (methodName!="Uncorrected"):
                genomeNameSet.add(genomeName)
                methodNameSet.add(methodName)
                r = Result()
                r.genomName=genomeName
                r.method=methodName
                r.memory=memory
                r.runTime=runTime
                r.wallTime=second
                results.append(r)
                #print(r.wallTime)
    results=sorted(results, key=attrgetter('method', 'genomName'))
    genomeNameSet=sorted(genomeNameSet)
    methodNameSet=sorted(methodNameSet)
    plotStackBarRunTime(methodNameSet,genomeNameSet,results);
    plotStackBarMemory(methodNameSet,genomeNameSet,results)
    especifyMin_wallTime(genomeNameSet,results)
    especifyMin_Memory(genomeNameSet,results)
    
    colNum=2+len(genomeNameSet);
   
    MakePerformanceTable(results,methodNameSet,genomeNameSet,sys.argv[2]+"memory_wallTime.tex");
    makeMemory(results,genomeNameSet,methodNameSet,sys.argv[2]+"memory_EC.tex")
    makeRuntime(results,genomeNameSet,methodNameSet,sys.argv[2]+"wallTime_minute_EC.tex")
    
    fobr.close();
    
makeMappedReal()

