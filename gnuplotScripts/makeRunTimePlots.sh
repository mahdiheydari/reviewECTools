#!/bin/bash 

#how to use:
#./makePlostScripts.sh runTime/discovar


i=0                   # Integer.
for directory in `find  $1  -maxdepth 1 -mindepth 1   -type f | sort`
   do
    arr[i]=$directory
    #ass[i]=$( echo $directory | cut -d "." -f 2 )
    let "i += 1"
    echo $directory
done


assm=`basename $1`

outputName=runTime_$assm

outputPlot="autoRunTimePlos.dem"
echo "#plot for runtime " >$outputPlot

echo "set output \"$outputName\"" >>$outputPlot 
echo "set boxwidth 0.75 absolute" >>$outputPlot 
echo "set style fill   solid 1.00 border lt -1" >>$outputPlot
echo "set key outside right top vertical Left reverse noenhanced autotitle columnhead nobox" >>$outputPlot
echo "set key invert samplen 4 spacing 1 width 0 height 0" >>$outputPlot
echo "set style histogram rowstacked title textcolor lt -1" >>$outputPlot
echo "set datafile missing '-'" >>$outputPlot
echo "set style data histograms" >>$outputPlot
echo "set xtics border in scale 0,0 nomirror rotate by -45  autojustify" >>$outputPlot
echo "set xtics  norangelimit" >>$outputPlot
echo "set yrange [0:]" >>$outputPlot
echo "set title """ >>$outputPlot
echo "set terminal pdf" >>$outputPlot

#echo "set multiplot layout 4,2" >>$outputPlot 

for i in "${arr[@]}"
do
    data=`basename $i`
   
    echo "set xlabel \"Error Correction Tool\"" >>$outputPlot
    echo "set ylabel \"Run Time (seconds)\"" >>$outputPlot
    echo "set title \"Showing the overall runtime of assembling $data by $assm,\n  Pre error correction has been done with different tools. \"" >>$outputPlot
    echo "plot for [COL=2:3] '$i' using COL:xticlabels(1) title columnheader" >>$outputPlot
done
#echo "unset multiplot" >>$outputPlot
gnuplot $outputPlot



