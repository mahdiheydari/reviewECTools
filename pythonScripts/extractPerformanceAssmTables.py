import os, sys
import subprocess
import time, math
from operator import itemgetter, attrgetter, methodcaller
class Result:
 genomName=""   
 method=""
 assmebler=""

 memory=0.0
 runTime=0.0
 wallTime=0.0
 wallTimeSeconds=0.0
 
 assemblyRunTime=0.0
 assemblyWallTime=""
 assemblyWallTimeSeconds=0.0
 assemblyMemory=0.0
 
 toolRunTime=0.0
 toolWallTime=""
 toolWallTimeSeconds=0.0
 toolMemory=0.0
def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False



def plotStackBarRunTime(methodNameSet,genomeNameSet,results, assemblerName):
    genomeNameSet=sorted(genomeNameSet)
    methodNameSet=sorted(methodNameSet)
    path = 'real/plots/runTime/'+assemblerName 
    if not os.path.exists(path):
        os.makedirs(path)
    for g in genomeNameSet:
        fobw=open(path+"/"+g, 'w')
        fobw.writelines("tools\tEC\tassembly"+'\n')
        for r in results:
            if (r.genomName==g): 
                for m in methodNameSet:
                    if (r.method==m and r.assmebler==assemblerName):
                        row=m+"\t"+ str(r.toolWallTimeSeconds)+'\t'+str(r.assemblyWallTimeSeconds)
                        fobw.writelines(row+'\n')
                        
                    
        fobw.close();
    fobw=open(path+"/allRuntime.dat", 'w')
    for m in methodNameSet:
        if (m!="Uncorrected"):
            fobw.writelines("\t"+m);
    fobw.writelines("\n");    
    for g in genomeNameSet:
        row=g
        for r in results:
            if (r.genomName==g): 
                for m in methodNameSet:       
                    if (r.method==m and r.assmebler==assemblerName):
                        row=row+"\t"+ str(r.toolWallTimeSeconds)
        fobw.writelines(row+'\n')
                

    fobw.close();
def plotStackBarMemory(methodNameSet,genomeNameSet,results, assemblerName):
    genomeNameSet=sorted(genomeNameSet)
    methodNameSet=sorted(methodNameSet)
    path = r'real/plots/memory/'+assemblerName
    if not os.path.exists(path):
        os.makedirs(path)
    for g in genomeNameSet:
        fobw=open(path+"/"+g, 'w')
        fobw.writelines("tools\tEC\tassembly"+'\n');
        for r in results:
            if (r.genomName==g): 
                for m in methodNameSet:
                    if (r.method==m and r.assmebler==assemblerName):
                        row=m+"\t"+ str(r.toolMemory)+'\t'+str(r.assemblyMemory)
                        fobw.writelines(row+'\n')
        fobw.close();
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


def especifyMin_wallTime(genomeNameSet,asmNameSet,results):
    for g in genomeNameSet:
        for a in asmNameSet:
            min_set=set();
            for r in results:
                if (r.genomName==g and r.assmebler==a ):
                    if (r.wallTimeSeconds=="" or r.wallTimeSeconds=="na" or r.wallTimeSeconds=="nan"):
                        r.wallTime="na"
                    else:
                        min_set.add(float( r.wallTimeSeconds))
                        #print(r.wallTimeSeconds)
                        
            min_R=min(min_set)
            #print(min_R)
            for r in results:
                if (r.genomName==g and r.assmebler==a):
                    if (r.wallTime!="na" and float(r.wallTimeSeconds )== min_R):
                        r.wallTime="\\bf{" +time.strftime("%H:%M:%S", time.gmtime(r.wallTimeSeconds))+"}"
                    else:
                        r.wallTime=time.strftime("%H:%M:%S", time.gmtime(r.wallTimeSeconds))



                    

def especifyMin_Memory(genomeNameSet,asmNameSet,results):
    for g in genomeNameSet:
        for a in asmNameSet:
            min_set=set();
            for r in results:
              if (r.genomName==g and r.assmebler==a ):
                    if (r.memory=="" or r.memory=="na" or r.memory=="nan"):
                        r.memory="na"
                    else:
                        min_set.add(float( r.memory))
            min_M=min(min_set)
            for r in results:
                if (r.genomName==g and r.assmebler==a ):
                    if (r.memory!="na" and float(r.memory )== min_M):

                        r.memory="\\bf{" +r.memory+"}"

def MakePerformanceTable(gresults,methodNameSet,genomeNameSet,asmemblerName,outFileName):
   
    fobw=open(outFileName+asmemblerName+".tex",'w')
    fobw.writelines("\documentclass[a4paper,10pt]{article} \r");
    fobw.writelines(" \\usepackage{multirow} \r");
    fobw.writelines(" \\usepackage{pdflscape} \r");
    fobw.writelines(" \\usepackage{datetime} \r")
    fobw.writelines(" \\usepackage{adjustbox} \r")
    fobw.writelines('\\begin{document}   \r');
    fobw.writelines('\\begin{landscape}   \r');
    fobw.writelines('\\  \\footnote{ Compiled on \\today\ at \\currenttime} \r' );
    fobw.write('Comparison the memory usage and run time of different error correction methods added to the assembly time and memory '+asmemblerName + ' \r' );
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
                    if (r.genomName==g and r.assmebler==asmemblerName):
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
    #fobr=open('asmInfoLog.txt','r')
    fobr=open(sys.argv[1],'r')
    s= fobr.read();
    methods = s.split("The results for next method:")
    methods.pop(0)
    results=[];
    genomeNameSet=set();
    methodNameSet=set();
    asmNameSet=set();
    for method in methods:

        #print("####################################################################")
        methodName= find_between(method , "the method name is<<", ">>." )
        #print(methodName)
        genomes=method.split("next DataSet Starts<<");
        genomes.pop(0)
        for genome in genomes:
            genomSize=find_between(genome , "the size of the genome is:<< ", ">>" )
            genomeName=find_between( genome, "The dataSet is<< ", " >>" )
            #print(genomeName)
            assmeblers=genome.split("new assembler starts")
            assmeblers.pop(0)
            for assembler in assmeblers:
                assmeblerName=find_between( assembler, "the assembler name is<<", ">>" )
                asmNameSet.add(assmeblerName)
                
                assemblerParts=find_between(assembler ,"Assembler starts<", ">Assembler ends").strip()
                assParts = assemblerParts.split("Command being timed:")
                #print(assmeblerName)
                assParts.pop(0)
                memory=0
                runTime=0
                seconds =0                
                for part in assParts:
                    temp=find_between(part ,"Maximum resident set size (kbytes): ", "\n").strip()
                    #print(temp)
                    if (int(temp)>memory):
                        memory=(float (temp)) 
                    temp=find_between(part ,"User time (seconds): ", "\n").strip()
                    runTime=runTime+(float(temp))
                    temp=find_between(part, "Elapsed (wall clock) time (h:mm:ss or m:ss):", "\n").strip()
                    timeParts = temp.split(":")
                    timeParts=timeParts[::-1]
                    timeIndex=1
                    seconds=seconds+float (timeParts[0])
                    while (timeIndex<len(timeParts)):
                        seconds=seconds+math.pow(60, timeIndex)* float (timeParts[timeIndex])
                        timeIndex=timeIndex+1    
                #memory=memory/ 1000000
                #memory='{0:.2f}'.format(round( float( memory),2))

                assemblyRunTime=runTime
                assemblyWallTime=time.strftime("%H:%M:%S", time.gmtime(seconds))
                assemblyWallTimeSeconds=seconds
                assemblyMemory=memory
                #print("assembly memory", assemblyMemory)
                #print("assembly walltime", assemblyWallTime)


                toolsParts=find_between(assembler ,"EC starts<", ">EC ends").strip()
                toolParts = toolsParts.split("Command being timed:")
                #print(assmeblerName)
                toolParts.pop(0)
                memory=0
                runTime=0
                seconds =0                
                for part in toolParts:
                    temp=find_between(part ,"Maximum resident set size (kbytes): ", "\n").strip()
                    #print(temp)
                    if (int(temp)>memory):
                        memory=(float (temp)) 
                    temp=find_between(part ,"User time (seconds): ", "\n").strip()
                    runTime=runTime+(float(temp))
                    temp=find_between(part, "Elapsed (wall clock) time (h:mm:ss or m:ss):", "\n").strip()
                    timeParts = temp.split(":")
                    timeParts=timeParts[::-1]
                    timeIndex=1
                    seconds=seconds+float (timeParts[0])
                    while (timeIndex<len(timeParts)):
                        seconds=seconds+math.pow(60, timeIndex)* float (timeParts[timeIndex])
                        timeIndex=timeIndex+1    
                #memory=memory/ 1000000
                #memory='{0:.2f}'.format(round( float( memory),2))

                toolRunTime=runTime
                toolWallTime=time.strftime("%H:%M:%S", time.gmtime(seconds))
                toolWallTimeSeconds=seconds
                toolMemory=memory
                #print("tool memory", toolMemory)
                #print("tool walltime", toolWallTime)

                if (toolWallTimeSeconds+assemblyWallTimeSeconds!=0):
                    r = Result()
		    r.memory=toolMemory
		    #print("****")
		    #print("tool:", toolMemory/1000000)
		    #print("assm:", assemblyMemory/1000000)
		    if (toolMemory<assemblyMemory):
			r.memory=assemblyMemory
		    #print("max:",r.memory/1000000)
		    toolMemory=toolMemory/ 1000000
		    toolMemory='{0:.2f}'.format(round( float( toolMemory),2))
		    assemblyMemory=assemblyMemory/ 1000000
		    assemblyMemory='{0:.2f}'.format(round( float( assemblyMemory),2))
		    r.memory=r.memory/ 1000000
		    r.memory='{0:.2f}'.format(round( float( r.memory),2))
		    r.assemblyRunTime=assemblyRunTime
		    r.assemblyWallTime=assemblyWallTime
		    r.assemblyWallTimeSeconds=assemblyWallTimeSeconds
		    r.assemblyMemory=assemblyMemory
		    r.toolRunTime=toolRunTime
		    r.toolWallTime=toolWallTime
		    r.toolWallTimeSeconds=toolWallTimeSeconds
		    r.toolMemory=toolMemory
		    genomeNameSet.add(genomeName)
		    methodNameSet.add(methodName)
		    r.assmebler=assmeblerName
		    r.genomName=genomeName
		    r.method=methodName
		    r.wallTime=time.strftime("%H:%M:%S", time.gmtime(toolWallTimeSeconds+assemblyWallTimeSeconds))
		    r.runTime=toolRunTime+assemblyRunTime
		    r.wallTimeSeconds=toolWallTimeSeconds+assemblyWallTimeSeconds
		    #print(methodName)
		    #print(genomeName)
		    #print("*********************************************")
		    results.append(r)
    results=sorted(results, key=attrgetter('method', 'genomName'))
    genomeNameSet=sorted(genomeNameSet)
    methodNameSet=sorted(methodNameSet)
    asmNameSet=sorted(asmNameSet)
    especifyMin_wallTime(genomeNameSet,asmNameSet,results)
    especifyMin_Memory(genomeNameSet,asmNameSet,results)
    
    colNum=2+len(genomeNameSet);
    #MakePerformanceTable(results,methodNameSet,genomeNameSet,sys.argv[2]);
    for asm in asmNameSet:
        #print(asm)
        MakePerformanceTable(results,methodNameSet,genomeNameSet,asm,sys.argv[2]);
        plotStackBarRunTime(methodNameSet,genomeNameSet,results, asm)
        plotStackBarMemory(methodNameSet,genomeNameSet,results, asm)
    fobr.close();
    
makeMappedReal()

