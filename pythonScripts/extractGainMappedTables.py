'''
Copyright (C) 2016  Mahdi Heydari
this script makes the latex table for the error correction gain.'''
import os, sys
from operator import itemgetter, attrgetter, methodcaller
class Result:
 genomName=""   
 method=""
 gainName=""

 tp=0
 tn=0
 fp=0
 fn=0
 gain=""
 specificity=""
 sensitivity=""
 fpRate=0

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def getValueByName(name, r):
    if (name== "fullRecGain"):
        return r.fullRecGain
    if (name== "errorCorrGain"):
        return r.errorCorrGain
def setValueByName(name, r, value):
    if (name== "fullRecGain"):
        r.fullRecGain=value
    if (name== "errorCorrGain"):
        r.errorCorrGain=value

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


def especifyMax(genomeNameSet,gainName,results):
    for g in genomeNameSet:
        min_set=set();
        for r in results:
            if (r.genomName==g and r.gainName==gainName ):
                if (r.fp=="" or r.fp=="na" or r.fp=="nan"):
                    r.fp="na"
                else:
                    min_set.add(float( r.fp))
        min_fp=min(min_set)
        for r in results:
            if (r.genomName==g and r.gainName==gainName ):
                if (r.fp!="na" and float(r.fp )== min_fp):
                    r.fp="\\bf{" +str (r.fp)+"}"

    for g in genomeNameSet:
        min_set=set();
        for r in results:
            if (r.genomName==g and r.gainName==gainName ):
                if (r.fn=="" or r.fn=="na" or r.fn=="nan"):
                    r.fn="na"
                else:
                    min_set.add(float( r.fn))
        min_fn=min(min_set)
        for r in results:
            if (r.genomName==g and r.gainName==gainName ):
                if (r.fn!="na" and float(r.fn )== min_fn):
                    r.fn="\\bf{" +str (r.fn)+"}"

                    
    for g in genomeNameSet:
        max_set=set();
        for r in results:
            if (r.genomName==g and r.gainName==gainName ):
                if (r.tn=="" or r.tn=="na" or r.tn=="nan"):
                    r.tn="na"
                else:
                    max_set.add(float( r.tn))
        max_tn=max(max_set)
        for r in results:
            if (r.genomName==g and r.gainName==gainName ):
                if (r.tn!="na" and float(r.tn )== max_tn):
                    r.tn="\\bf{" +str (r.tn)+"}"
                    
    for g in genomeNameSet:
        max_set=set();
        for r in results:
            if (r.genomName==g and r.gainName==gainName ):
                if (r.gain=="" or r.gain=="na" or r.gain=="nan"):
                    r.gain="na"
                else:
                    max_set.add(float( r.tp))
        max_tp=max(max_set)
        for r in results:
            if (r.genomName==g and r.gainName==gainName ):
                if (r.tp!="na" and float(r.tp )== max_tp):
                    r.tp="\\bf{" +str (r.tp)+"}"


    for g in genomeNameSet:
        max_set=set();
        for r in results:
            if (r.genomName==g and r.gainName==gainName ):
                if (r.gain=="" or r.gain=="na" or r.gain=="nan"):
                    r.gain="na"
                else:
                    max_set.add(float( r.gain))
        max_G=max(max_set)
        for r in results:
            if (r.genomName==g and r.gainName==gainName ):
                if (r.gain!="na" and float(r.gain )== max_G):
                    r.gain="\\bf{" +r.gain+"}"


def makeGain(results,genomeNameSet,methodNameSet,gainName,outFileName):
    fobw=open(outFileName+"_"+gainName+"_only.tex",'w')
    #print (outFileName+"_"+gainName+"_only.tex")
    #covSet.pop(0);
    fobw.writelines("\documentclass[a4paper,10pt]{article} \r");

    fobw.writelines(" \\usepackage{datetime} \r")
    fobw.writelines(" \\usepackage{booktabs} \r")
    
    fobw.writelines('\\begin{document}   \r');
    fobw.writelines('\\  \\footnote{ Compiled on \\today\ at \\currenttime} \r' );
    fobw.write('\r Gain(\%) \r' );
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
                if (r.genomName==g and r.method==m and r.gainName==gainName):
                    tempVal="";
                    tempVal=" & "+ str(r.gain);
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
                 
def MakeReaMappedTable(gresults,methodNameSet,genomeNameSet,gainName,outFileName):
   
    fobw=open(outFileName+"_"+gainName+".tex",'w')
    fobw.writelines("\documentclass[a4paper,10pt]{article} \r");
    fobw.writelines(" \\usepackage{multirow} \r");
    fobw.writelines(" \\usepackage{pdflscape} \r");
    fobw.writelines(" \\usepackage{adjustbox} \r")
    fobw.writelines(" \\usepackage{datetime} \r")
    fobw.writelines('\\begin{document}   \r');
    fobw.writelines('\\begin{landscape}   \r');
    fobw.writelines('\\  \\footnote{ Compiled on \\today\ at \\currenttime} \r' );
    title="Comparison of different Error Correction methods by looking at "+gainName +" \r"
    fobw.write(title );
    fobw.write('\\\ \r')
    fobw.write('\\\ \r')
    fobw.write('\\begin{adjustbox}{width=.9\\textwidth}')
    fobw.write('\\begin{tabular}{' );
 
    #factorSet = [" Gain", "Sensitivity", "Specificity", "TP", "TN","FP","FN"]
    factorSet = [ "TP", "TN","FP","FN"]
    #factorSet[0]=" Gain"
    #factorSet.add("TP")
    #factorSet.add("TN")
    #factorSet.add("FP")
    #factorSet.add("FN")
    #factorSet.add("sensitivity")
    #factorSet.add("specificity")
    #factorSet=sorted(factorSet)
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
                        if (r.method==meth_item and r.gainName==gainName):                            
                            if(factor_item==" Gain"):
                                tempVal=" & " +str(r.gain)
                                find=1;
                            if(factor_item=="TP"):
                                tempVal=" & " +str(r.tp)
                                find=1;
                            if(factor_item=="TN"):
                                tempVal=" & " +str(r.tn)
                                find=1;
                            if(factor_item=="FP"):
                                tempVal=" & " +str(r.fp)
                                find=1;
                            if(factor_item=="FN"):
                                tempVal=" & " +str(r.fn)
                                find=1;
                            if(factor_item=="Sensitivity"):
                                tempVal=" & " +str(r.sensitivity)
                                find=1;
                            if(factor_item=="Specificity"):
                                tempVal=" & " +str(r.specificity)
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

def MakeReaMappedGainTable(gresults,methodNameSet,genomeNameSet,gainName,outFileName):
    fobw=open(outFileName+"_"+gainName+"Paper.tex",'w')
    fobw.writelines("\documentclass[a4paper,10pt]{article} \r");
    fobw.writelines(" \\usepackage{multirow} \r");
    fobw.writelines(" \\usepackage{pdflscape} \r");
    fobw.writelines(" \\usepackage{adjustbox} \r")
    fobw.writelines(" \\usepackage{datetime} \r")
    fobw.writelines(" \\usepackage{booktabs} \r")
    fobw.writelines('\\begin{document}   \r');
    fobw.writelines('\\begin{landscape}   \r');
    fobw.writelines('\\  \\footnote{ Compiled on \\today\ at \\currenttime} \r' );
    title="Comparison of different Error Correction methods by looking at "+gainName +" \r"
    fobw.write(title );
    fobw.write('\\\ \r')
    fobw.write('\\\ \r')
    fobw.write('\\begin{adjustbox}{width=.5\\textwidth}')
    fobw.write('\\begin{tabular}{' );
    factorSet = [" Gain", "Sensitivity", "Specificity", "fpRate"]
    colNum=len(genomeNameSet)+1;
    temp="c"
    i=1;
    while (i<colNum):
        temp=temp+"c"
        i=i+1
    fobw.writelines(temp+"l}\r");
    fobw.writelines("\\\ \multicolumn{1}{ c } {} & \multicolumn{"+str( colNum-1)+"}{ c}{\\bf{DataSet}}  \r");
    fobw.write("\\\ \multicolumn{1}{ c } {Tools} &")
    temp=""
    i=1
    for g in genomeNameSet:
        temp=temp+g+' & '
        i=i+1
    fobw.writelines(temp+ "\r")   
    fobw.writelines(" \\\ \\toprule \r");
    for factor_item in factorSet:
        fobw.writelines("\\\ \multicolumn{1}{ c } {} & \multicolumn{"+str( colNum-1)+"}{ c}{\\bf{"+factor_item+ "}} \\\ \r");
        i=0;
        for meth_item in methodNameSet:
            fobw.write('\multicolumn{1}{ c }{'+meth_item+'}')
            tempLine="";
            for g in genomeNameSet:
                tempVal=""
                find =0;
                for r in gresults:
                    if (r.genomName==g ):
                        if (r.method==meth_item and r.gainName==gainName):                            
                            if(factor_item==" Gain"):
                                tempVal=" & " +str(r.gain)
                                find=1;
                            if(factor_item=="Sensitivity"):
                                tempVal=" & " +str(r.sensitivity)
                                find=1;
                            if(factor_item=="Specificity"):
                                tempVal=" & " +str(r.specificity)
                                find=1;
                            if(factor_item=="fpRate"):
				tempVal=" & " +str(r.fpRate)
                                find=1;
                if (find):
                    tempLine=tempLine+tempVal
                else:
                    tempLine=tempLine+" & "+"na "
            tempLine=tempLine+' & '
            fobw.write(tempLine)
            i=i+1;
	    if i!= len(methodNameSet):
		fobw.write ('\\\ \r')
        fobw.writelines(" \\\ \\toprule \r");
    fobw.write('\end{tabular}');
    fobw.write('\\\ \r')
    fobw.write('\end{adjustbox}')
    fobw.write( '\end{landscape}')
    fobw.write( '\end{document}')
    fobw.close();

def MakeReaMappedGainTableByFactor(gresults,methodNameSet,genomeNameSet,gainName,outFileName,factorSet):
    print(methodNameSet)
    print(genomeNameSet)
    fobw=open(outFileName+"_"+gainName,'w')
    fobw.writelines("\documentclass[a4paper,10pt]{article} \r");
    fobw.writelines(" \\usepackage{multirow} \r");
    fobw.writelines(" \\usepackage{pdflscape} \r");
    fobw.writelines(" \\usepackage{adjustbox} \r")
    fobw.writelines(" \\usepackage{datetime} \r")
    fobw.writelines(" \\usepackage{booktabs} \r")
    fobw.writelines('\\begin{document}   \r');
    fobw.writelines('\\begin{landscape}   \r');
    fobw.writelines('\\  \\footnote{ Compiled on \\today\ at \\currenttime} \r' );
    title="Comparison of different Error Correction methods by looking at "+gainName +" \r"
    fobw.write(title );
    fobw.write('\\\ \r')
    fobw.write('\\\ \r')
    fobw.write('\\begin{adjustbox}{width=.5\\textwidth}')
    fobw.write('\\begin{tabular}{' );
    #factorSet = [" Gain", "Sensitivity", "Specificity", "TP", "TN","FP","FN"]
    colNum=len(genomeNameSet)+1;
    temp="c"
    i=1;
    while (i<colNum):
        temp=temp+"c"
        i=i+1
    fobw.writelines(temp+"l}\r");
    fobw.writelines("\\\ \multicolumn{1}{ c } {} & \multicolumn{"+str( colNum-1)+"}{ c}{\\bf{DataSet}}  \r");
    fobw.write("\\\ \multicolumn{1}{ c } {Tools} &")
    temp=""
    i=1
    for g in genomeNameSet:
        temp=temp+g+' & '
        i=i+1
    fobw.writelines(temp+ "\r")   
    fobw.writelines(" \\\ \\toprule \r");
    for factor_item in factorSet:
        fobw.writelines("\\\ \multicolumn{1}{ c } {} & \multicolumn{"+str( colNum-1)+"}{ c}{\\bf{"+factor_item+ "}} \\\ \r");
        i=0;
        for meth_item in methodNameSet:
            fobw.write('\multicolumn{1}{ c }{'+meth_item+'}')
            tempLine="";
            for g in genomeNameSet:
                tempVal=""
                find =0;
                for r in gresults:
		    #print (r.genomName)
		    #print(g)
                    if (r.genomName==g ):
			#print(g)
                        if (r.method==meth_item and r.gainName==gainName):
			    if(factor_item==" Gain"):
                                tempVal=" & " +str(r.gain)
                                find=1;
                            if(factor_item=="TP"):
                                tempVal=" & " +str(r.tp)
                                find=1;
                            if(factor_item=="TN"):
                                tempVal=" & " +str(r.tn)
                                find=1;
                            if(factor_item=="FP"):
                                tempVal=" & " +str(r.fp)
                                find=1;
                            if(factor_item=="FN"):
                                tempVal=" & " +str(r.fn)
                                find=1;
                            if(factor_item=="Sensitivity"):
                                tempVal=" & " +str(r.sensitivity)
                                find=1;
                            if(factor_item=="Specificity"):
                                tempVal=" & " +str(r.specificity)
                                find=1;
                            if(factor_item=="fpRate"):
				tempVal=" & " +str(r.fpRate)
                                find=1;
                if (find):
                    tempLine=tempLine+tempVal
                else:
                    tempLine=tempLine+" & "+"na "
            tempLine=tempLine+' & '
            fobw.write(tempLine)
            i=i+1;
	    if i!= len(methodNameSet):
		fobw.write ('\\\ \r')
        fobw.writelines(" \\\ \\toprule \r");
    fobw.write('\end{tabular}');
    fobw.write('\\\ \r')
    fobw.write('\end{adjustbox}')
    fobw.write( '\end{landscape}')
    fobw.write( '\end{document}')
    fobw.close();
    
def makeMappedReal():
    #subprocess.call("scp vsc41448@gengar.ugent.be:./Result/run_produceResultTable_script/RealDataMapped/log.txt ./Mappedlog.txt", shell=True)

    #fobr=open('Gainlog.txt','r')
    fobr=open(sys.argv[1],'r')
    s= fobr.read();
    methods = s.split("The results for next method:")
    methods.pop(0)
    results=[];
    genomeNameSet=set();
    methodNameSet=set();
    gainSet=set();
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
            if (isfloat(errorCorrGain) and (errorCorrGain!="nan")):
                errorCorrGain='{0:.1f}'.format(round( float( errorCorrGain),2))
            else:
                errorCorrGain="na"
            try:
                tp=int (find_between(accuracyEva,"TP:","TN").strip())
            except ValueError:
                tp="na"
            
            #print(tp)
            try:
                tn=int (find_between(accuracyEva,"TN:","FP").strip())
            except:
                tn="na"
            #print(tn)
            try:
                fp=int (find_between(accuracyEva,"FP:","FN").strip())
            except:
                fp="na"
            #print(fp)
            try:
                fn=int (find_between(accuracyEva,"FN:","\n").strip())
            except:
                fn="na"
            #print(fn)
            if methodName != "Uncorrected":
                genomeNameSet.add(genomeName)
                methodNameSet.add(methodName)
                r = Result()
                r.genomName=genomeName
                r.method=methodName
                r.gain=errorCorrGain
                r.gainName="ErrorCorrectionGain"
                r.tp=tp
                r.fp=fp
                r.tn=tn
                r.fn=fn
                if (float( tn)+float( fp)!=0):
		  r.specificity= '{0:.1f}'.format(float(tn*100)/(float( tn)+float( fp)));
                else:
		  r.specificity="n/a" 
                #print(r.specificity)
                if (float( tp)+float( fn)!=0):
		  r.sensitivity= '{0:.1f}'.format(float( tp*100)/(float( tp)+float( fn)));
                else:
		  r.sensitivity="n/a"
		r.fpRate='{0:.0f}'.format((1- float(tn)/(float( tn)+float( fp)))*1000000);
		#print(r.fpRate)  
		#print(r.sensitivity)
                gainSet.add("ErrorCorrectionGain")
                results.append(r)

            fullRecovery=find_between(genome ,"<<<The evaluation report based full read recovery>>>", "<<<Quality based reports>>>") 
            fullRecGain=find_between(fullRecovery,"The Gain value percentage for full recovery of reads is: (","%)")
            fullRecGain=fullRecGain.strip()
            if (isfloat(fullRecGain)and (errorCorrGain!="nan")):
                fullRecGain='{0:.2f}'.format(round( float( fullRecGain),2))
            else:
                fullRecGain="na"
            try:
                tp=int (find_between(fullRecovery,"TP:","TN").strip())
            except:
                tp="na"
                
            #print(tp)
            try:
                tn=int (find_between(fullRecovery,"TN:","FP").strip())
            except:
                tn="na"
            #print(tn)
            try:
                fp=int (find_between(fullRecovery,"FP:","FN").strip())
            except:
                fp="na"
            #print(fp)
            try:
                fn=int (find_between(fullRecovery,"FN:","\n").strip())
            except:
                fn="na"
            if methodName != "Uncorrected":
                genomeNameSet.add(genomeName)
                methodNameSet.add(methodName)
                r = Result()
                r.genomName=genomeName
                r.method=methodName
                r.gain=fullRecGain
                r.gainName="FullRecoveryGain"
                r.tp=tp
                r.fp=fp
                r.tn=tn
                r.fn=fn
                if (float( tn)+float( fp)!=0):
		  r.specificity= '{0:.1f}'.format(float(tn*100)/(float( tn)+float( fp)));
                else:
		  r.specificity="n/a"
		r.fpRate='{0:.2f}'.format((1- float(tn)/(float( tn)+float( fp)))*1000000);
		#print(r.fpRate)  
                #print(r.specificity)
                if (float( tp)+float( fn)!=0):
		  r.sensitivity= '{0:.1f}'.format(float( tp*100)/(float( tp)+float( fn)));
                else:
		  r.sensitivity="n/a"
		#print(r.sensitivity)
                #gainSet.add("FullRecoveryGain")  #uncomment this line if you want to have the full recovery statistic tables
                results.append(r)
    results=sorted(results, key=attrgetter('method', 'genomName'))
    genomeNameSet=sorted(genomeNameSet)
    print(genomeNameSet)
    methodNameSet=sorted(methodNameSet)
    print(methodNameSet)
    colNum=2+len(genomeNameSet);
    #especifyBest( genomeNameSet,results, "errorCorrGain", 1)
    
    ##especifyMax_Gain(genomeNameSet,results)
    #especifyBest( genomeNameSet,results, "fullRecGain", 1)
    #MakeReaMappedTable(results,methodNameSet,genomeNameSet, "Mappedlog.tex");
    #MakeReaMappedTable(results,methodNameSet,genomeNameSet,sys.argv[2]);
    for gainName in gainSet:
        especifyMax(genomeNameSet,gainName,results)
        #print(gainName)
        #MakeReaMappedTable(results,methodNameSet,genomeNameSet, gainName,sys.argv[2]);#
        #MakeReaMappedGainTable(results,methodNameSet,genomeNameSet, gainName,sys.argv[2]);#
        #makeGain(results,genomeNameSet,methodNameSet,gainName,sys.argv[2])
        factorSet = [" Gain", "Sensitivity", "Specificity", "TP", "TN","FP","FN", "fpRate"]
        MakeReaMappedGainTableByFactor(results,methodNameSet,genomeNameSet, gainName,sys.argv[2]+".all.tex",factorSet)
        factorSet = [" Gain"]
        MakeReaMappedGainTableByFactor(results,methodNameSet,genomeNameSet,gainName,sys.argv[2]+".onlyGain.tex",factorSet)
	factorSet = [" Gain", "Sensitivity","Specificity" ,"fpRate"]
        MakeReaMappedGainTableByFactor(results,methodNameSet,genomeNameSet,gainName,sys.argv[2]+".parameter.tex",factorSet)
        factorSet = [ "TP", "TN","FP","FN"]
        MakeReaMappedGainTableByFactor(results,methodNameSet,genomeNameSet,gainName,sys.argv[2]+".number.tex",factorSet)
    fobr.close();
    
makeMappedReal()















  
