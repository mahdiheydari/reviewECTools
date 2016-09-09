#!/bin/bash
COUNTER=1

while [  $COUNTER -lt 9 ]; do
name="genomeName"
minYrange=0
maxYrange=20
case "$COUNTER" in
"1")
    name="Bifidobacterium dentium"
;;
"2")
    name="E. coli str. K-12 substr. DH10B"
;;
"3")
    name="E. coli str. K-12 substr. MG1655"
;;
"4")
    name="Salmonella enterica"
;;
"5")
    name="Pseudomonas aeruginosa"
;;
"6")
    name="Human Chr 21"
    minYrange=20
    maxYrange=40
;;
"7")
    name="Caenorhabditis elegans"
    minYrange=0
    maxYrange=20
;;
"8")
    name="Drosophila melanogaster"
    minYrange=18
    maxYrange=65
;;
esac

gnuplot << EOF
        
	
	set output "/home/mahdi/haloServerTables/real/quastPlot/spades/D$COUNTER/NGA50.pdf"
	set style data lines
	set terminal pdf
	
	set multiplot
	set yrange [0:]
	set xrange [0:100]
	set ytics 100
	set xtics 10
	#set title "NGAx for $name reads, assembled by Spades"
	set ylabel "Contig length(kbp)"
	set xlabel "x"
	set datafile separator "\t"
	plot"NGA50Data/spades/D$COUNTER/initial" using 1:2 smooth freq   lc rgb"#990000"  title "uncorrected",\
	    "NGA50Data/spades/D$COUNTER/ace" using 1:2   smooth freq   lc rgb"#2BCE48" title "ACE",\
	    "NGA50Data/spades/D$COUNTER/bayesHammer" using 1:2   smooth freq   lc rgb"#00998F" title "BayesHammer",\
	    "NGA50Data/spades/D$COUNTER/bfc" using 1:2   smooth freq   lc rgb"#005C31" title "BFC",\
	    "NGA50Data/spades/D$COUNTER/bless" using 1:2  smooth freq   lc rgb"#005C31"  title "BLESS",\
	    "NGA50Data/spades/D$COUNTER/blue" using 1:2   smooth freq   lc rgb"#0075DC" title "Blue",\
	    "NGA50Data/spades/D$COUNTER/karect" using 1:2   smooth freq   lc rgb"red" title "Karect",\
	    "NGA50Data/spades/D$COUNTER/lighter" using 1:2   smooth freq   lc rgb"#C20088" title "Lighter",\
	    "NGA50Data/spades/D$COUNTER/racer" using 1:2  smooth freq   lc rgb"#993F00" title "RACER",\
	    "NGA50Data/spades/D$COUNTER/sga" using 1:2  smooth freq   lc rgb"#F0A3FF" title "SGA-EC",\
	    "NGA50Data/spades/D$COUNTER/trowel" using 1:2  smooth freq   lc rgb"#003380" title "Trowel",\
	    "NGA50Data/spades/D$COUNTER/fiona" using 1:2  smooth freq   lc rgb "#5EF1F2" title "Fiona" 
	
	set grid
	set size 0.35,0.53
	set origin 0.32,0.36
	set xrange [45:55]
	set yrange [$minYrange:$maxYrange]
	set xtics 5
	set ytics 20
	set title ""
	set ylabel ""
	set xlabel ""
	set datafile separator "\t"
	plot"NGA50Data/spades/D$COUNTER/initial" using 1:2 smooth freq   lc rgb"#990000"  notitle,\
	    "NGA50Data/spades/D$COUNTER/ace" using 1:2   smooth freq   lc rgb"#2BCE48" notitle,\
	    "NGA50Data/spades/D$COUNTER/bayesHammer" using 1:2   smooth freq   lc rgb"#00998F" notitle,\
	    "NGA50Data/spades/D$COUNTER/bfc" using 1:2   smooth freq   lc rgb"#005C31" notitle,\
	    "NGA50Data/spades/D$COUNTER/bless" using 1:2  smooth freq   lc rgb"#005C31"  notitle,\
	    "NGA50Data/spades/D$COUNTER/blue" using 1:2   smooth freq   lc rgb"#0075DC" notitle,\
	    "NGA50Data/spades/D$COUNTER/karect" using 1:2   smooth freq   lc rgb"red" notitle,\
	    "NGA50Data/spades/D$COUNTER/lighter" using 1:2   smooth freq   lc rgb"#C20088" notitle,\
	    "NGA50Data/spades/D$COUNTER/racer" using 1:2  smooth freq   lc rgb"#993F00" notitle ,\
	    "NGA50Data/spades/D$COUNTER/sga" using 1:2  smooth freq   lc rgb"#F0A3FF" notitle ,\
	    "NGA50Data/spades/D$COUNTER/trowel" using 1:2  smooth freq   lc rgb"#003380" notitle ,\
	    "NGA50Data/spades/D$COUNTER/fiona" using 1:2  smooth freq   lc rgb "#5EF1F2" notitle
	
	unset multiplot
EOF
let COUNTER=COUNTER+1 
done
exit 0;
