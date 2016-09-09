#plot for runtime 

set output "runTime_spades_multi.pdf"
set boxwidth 0.5 absolute
set style fill   solid 1.00 border lt -1
set key outside right top vertical Left reverse noenhanced autotitle columnhead nobox
set key invert samplen 4 spacing 1 width 0 height 0
set style histogram rowstacked title textcolor lt -1
set datafile missing '-'
set style data histograms

set xtics  norangelimit
set yrange [0:]

set tics font ", 4"
set terminal pdf
set xtics rotate by 90 offset 0,-2

set tmargin 3
set bmargin 4
set lmargin 4
set rmargin 3

set multiplot layout 2,4
set key ins vert
set key top left

set yrange [0:]
set xlabel "Error correctio tools" font "sans, 5" offset 0,-.75,-2
set ylabel "Run time (minutes)"  font "sans, 5" offset 5,0,0

set title "Bifidobacterium dentium" font "sans, 7"  offset 0,-.7
plot for [COL=2:3] 'runTime/spades/D1' using COL:xticlabels(1) notitle

set title "E. coli str. K-12 substr. DH10B"
plot for [COL=2:3] 'runTime/spades/D2' using COL:xticlabels(1) notitle

set title "E. coli str. K-12 substr. MG1655"
plot for [COL=2:3] 'runTime/spades/D3' using COL:xticlabels(1) notitle 

set title "Salmonella enterica"
plot for [COL=2:3] 'runTime/spades/D4' using COL:xticlabels(1) notitle

set title "Pseudomonas aeruginosa"
plot for [COL=2:3] 'runTime/spades/D5' using COL:xticlabels(1) notitle 

set title "Human Chr 21"
plot for [COL=2:3] 'runTime/spades/D6' using COL:xticlabels(1) notitle

set title "Caenorhabditis elegans"
plot for [COL=2:3] 'runTime/spades/D7' using COL:xticlabels(1) notitle

set key at 1,75000
set key font "sans, 5"
set title "Drosophila melanogaster" 
plot for [COL=2:3] 'runTime/spades/D8' using COL:xticlabels(1)
