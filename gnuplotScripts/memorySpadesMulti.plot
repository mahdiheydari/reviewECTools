#plot for runtime 

set output "memroy_spades.pdf"
set boxwidth 0.75 absolute
set style fill   solid 1.00 border lt -1
set key outside right top vertical Left reverse noenhanced autotitle columnhead nobox
set key invert samplen 4 spacing 1 width 0 height 0
set style data histograms
set datafile missing '-'
set style histogram clustered
set xtics border in scale 0,0 nomirror rotate by -45  autojustify
set xtics  norangelimit
set xtics  norangelimit


set tics font ", 4"
set terminal pdf
set xtics rotate by 90 offset .5,-2

set tmargin 3
set bmargin 4
set lmargin 3
set rmargin 3

set multiplot layout 2,4
set key ins vert
set key top left
set yrange [0:]
set xlabel "Error correctio tools" font "sans, 5" offset 0,-.75,-2
set ylabel "Peak memory usage(GB)"  font "sans, 5" offset 3.5,0,0


set title "Bifidobacterium dentium" font "sans, 7"  offset 0,-.7
plot for [COL=2:3] 'memory/spades/D1' using COL:xticlabels(1) notitle

set title "E. coli str. K-12 substr. DH10B"
plot for [COL=2:3] 'memory/spades/D2' using COL:xticlabels(1) notitle

set title "E. coli str. K-12 substr. MG1655"
plot for [COL=2:3] 'memory/spades/D3' using COL:xticlabels(1) notitle 

set title "Salmonella enterica"
plot for [COL=2:3] 'memory/spades/D4' using COL:xticlabels(1) notitle

set title "Pseudomonas aeruginosa"
plot for [COL=2:3] 'memory/spades/D5' using COL:xticlabels(1) notitle 

set title "Human Chr 21"
plot for [COL=2:3] 'memory/spades/D6' using COL:xticlabels(1) notitle

set title "Caenorhabditis elegans"
plot for [COL=2:3] 'memory/spades/D7' using COL:xticlabels(1) notitle

set key at 4,260
set key font "sans, 5"
set title "Drosophila melanogaster" 
plot for [COL=2:3] 'memory/spades/D8' using COL:xticlabels(1) 

