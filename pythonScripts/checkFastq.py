'''
Copyright (C) 2016  Mahdi Heydari
this script check if the output fastq is in the correct format or not. 
It checks the read lengh and the lengh of quality profile, they shoud be the same. Then in writes back the reads to the outpu '''


import sys
def checkLenght(inputFileName, outputFileName):
    
    import io
    fobw = io.open(outputFileName, 'wb')   # newline='' means don't convert \n
    #subprocess.call("scp vsc41448@gengar.ugent.be:./Result/run_produceResultTable_script/log.txt ./art.log", shell=True)
    
    from operator import itemgetter, attrgetter, methodcaller

    i=-1;
    readLengh=0;
    qualityLengh=0
    with open(inputFileName) as infile:
        for line in infile:
            i=i+1
            if (i%4==0):
                fobw.write(line)
            if (i%4==1):
                readLengh=len(line)
                fobw.write(line)
            if(i%4==2):
                fobw.write(line)
            if(i%4==3):
                qualityLengh=len(line)
                if (qualityLengh==readLengh):
                    fobw.write(line)
                if (qualityLengh>readLengh):
                    line = line[:-(qualityLengh-readLengh+1)]
                    fobw.write(line);
                    fobw.write("\n");
                    #print("num:",i)
                    #print("quality Lengh is:",qualityLengh )
                    #print("read lengh is   :", readLengh) 
                    #print("quality lengh is bigger!!!!\n")
                if (readLengh>qualityLengh):
                    line = line[:-1]
                    qualityAppend='!' * (readLengh-qualityLengh)
                    line=line+qualityAppend
                    fobw.write(line);
                    fobw.write("\n");
                    #print("read leangh is bigger!!!!1\n")
    fobw.close()
    infile.close()
print ("First argument: %s" % str(sys.argv[1]))
print ("Second argument: %s" % str(sys.argv[2]))
inputFileName=str(sys.argv[1])
outputFileName=str(sys.argv[2]);
checkLenght(inputFileName, outputFileName)
 
