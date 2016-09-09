#!/bin/bash 

#how to use:
#./makePlostScripts.sh runTime/discovar


i=0                   # Integer.
for directory in `find  $1  -maxdepth 1 -mindepth 1   -type f | sort`
   do
    arr[i]=$directory
    let "i += 1"
    echo $directory
done


assm=`basename $1`
outputName=memroy_$assm

outputPlot="autoMemoryPlos.dem"
echo "#plot for runtime " >$outputPlot
echo "set output \"$outputName\"" >>$outputPlot 
echo "set boxwidth 0.75 absolute" >>$outputPlot 
echo "set style fill   solid 1.00 border lt -1" >>$outputPlot
echo "set key outside right top vertical Left reverse noenhanced autotitle columnhead nobox" >>$outputPlot
echo "set key invert samplen 4 spacing 1 width 0 height 0" >>$outputPlot
echo "set style data histograms" >>$outputPlot
echo "set datafile missing '-'" >>$outputPlot
echo "set style histogram clustered" >>$outputPlot
echo "set xtics border in scale 0,0 nomirror rotate by -45  autojustify" >>$outputPlot
echo "set xtics  norangelimit" >>$outputPlot
#echo "set yrange [0:]" >>$outputPlot
echo "set title """ >>$outputPlot
echo "set terminal pdf" >>$outputPlot



for i in "${arr[@]}"
do
    data=`basename $i`
   
    echo "set xlabel \"Error Correction Tool\"" >>$outputPlot
    echo "set ylabel \"Memory (GB)\"" >>$outputPlot
    echo "set title \"Showing Memory usage of assembling $data by $assm,\n  Error correction has been done with different tools. \"" >>$outputPlot
    echo  "plot for [COL=2:3] '$i' using COL:xticlabels(1) title columnheader">>$outputPlot

done

gnuplot $outputPlot



