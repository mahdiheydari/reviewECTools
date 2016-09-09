import os, sys , re
from operator import itemgetter, attrgetter, methodcaller
class Result:
    toolName=""
    x_coordinate=""
    y_coordinate=""
    
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def extractFiles(n):
    fobr=open("real/quastPlot/spades/D"+str(n)+"/coordNGAx.json",'r')
    s= fobr.read();
    methodNamesline= find_between(s , "filenames\":[", "]" )
    methods=methodNamesline.split(",");
    
    yCoordinateline= find_between(s , "\"coord_y\":[", "],\"coord_x\"" )
    yCoordinates=yCoordinateline.split("],");

    xCoordinateline= find_between(s , "\"coord_x\":[", "],\"filenames\"" )
    xCoordinates=xCoordinateline.split("],");
    directory="real/plots/NGA50Data/spades/D"+str(n)+"/"
    if not os.path.exists(directory):
        os.makedirs(directory)
    methodIndex=0
    for method in methods:
        method =method[1:-1]
        fobw=open(directory+method,'w')
        fobw.writelines("# the following table represent the corrdination of x and y axes in NGA50 plot reads corrected by "+method+'\n');
        xArray=xCoordinates[methodIndex].split(",");
        yArray=yCoordinates[methodIndex].split(",");
        i=0
        for x in xArray:
            y=yArray[i]
            temp=re.findall(r'\d+\.\d+', x)
            if (len(temp)>0):
                x=temp[0]
            temp=re.findall(r'\b\d+\b',y)
            if (len(temp)>0):
                y=temp[0]
            #print(x +"\t"+ y)
            fobw.writelines(x+"\t"+ str(float (y)/1000)+"\n");
            i=i+1
        methodIndex=methodIndex+1

i=1
while (i<9):
    extractFiles(i)
    i=i+1
