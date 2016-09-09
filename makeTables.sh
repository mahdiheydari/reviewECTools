rm real/logFiles/*
rm real/quast_assembly/*
#rm artificial/tables/*
rm real/tables/*
#rm artificial/logFiles/*
#rm artificial/quast_assembly/*

 scp mahdi@halo.intec.ugent.be:/home/mahdi/autoScripts/artificialScripts/results/logFiles/Gainlog.txt artificial/logFiles/Gainlog.txt
 scp mahdi@halo.intec.ugent.be:/home/mahdi/autoScripts/artificialScripts/results/logFiles/infoLog.txt artificial/logFiles/infoLog.txt
 scp mahdi@halo.intec.ugent.be:/home/mahdi/autoScripts/artificialScripts/results/tables/realData/quast/discovar_sum.tex  artificial/quast_assembly/discover_sum.tex
 scp mahdi@halo.intec.ugent.be:/home/mahdi/autoScripts/artificialScripts/results/tables/realData/quast/spades_sum.tex  artificial/quast_assembly/spades_sum.tex
 
 scp mahdi@halo.intec.ugent.be:/home/mahdi/autoScripts/results/tables/quast/velvet.tex  real/quast_assembly/velvet.tex
 scp mahdi@halo.intec.ugent.be:/home/mahdi/autoScripts/results/tables/quast/velvet_sum.tex real/quast_assembly/velvet_sum.tex
 scp mahdi@halo.intec.ugent.be:/home/mahdi/autoScripts/results/tables/quast/spades.tex real/quast_assembly/spades.tex
 scp mahdi@halo.intec.ugent.be:/home/mahdi/autoScripts/results/tables/quast/spades_sum.tex real/quast_assembly/spades_sum.tex
 scp mahdi@halo.intec.ugent.be:/home/mahdi/autoScripts/results/tables/quast/minia.tex real/quast_assembly/minia.tex
 scp mahdi@halo.intec.ugent.be:/home/mahdi/autoScripts/results/tables/quast/minia_sum.tex real/quast_assembly/minia_sum.tex
 scp mahdi@halo.intec.ugent.be:/home/mahdi/autoScripts/results/tables/quast/idba.tex real/quast_assembly/idba.tex
 scp mahdi@halo.intec.ugent.be:/home/mahdi/autoScripts/results/tables/quast/idba_sum.tex real/quast_assembly/idba_sum.tex
 scp mahdi@halo.intec.ugent.be:/home/mahdi/autoScripts/results/tables/quast/discovar.tex real/quast_assembly/discovar.tex
 scp mahdi@halo.intec.ugent.be:/home/mahdi/autoScripts/results/tables/quast/discovar_sum.tex real/quast_assembly/discovar_sum.tex

 scp mahdi@halo.intec.ugent.be:/home/mahdi/autoScripts/results/logFiles/deBruijn_Log_new_21.txt real/logFiles/deBruijn_Log_new_21.txt
 scp mahdi@halo.intec.ugent.be:/home/mahdi/autoScripts/results/logFiles/asmInfoLog.txt real/logFiles/asmInfoLog.txt
 scp mahdi@halo.intec.ugent.be:/home/mahdi/autoScripts/results/logFiles/BWAlogTest.txt real/logFiles/BWAlogTest.txt
 #scp mahdi@halo.intec.ugent.be:/home/mahdi/autoScripts/results/logFiles/deBruijn_Log_21.txt real/logFiles/deBruijn_Log_21.txt
 #scp mahdi@halo.intec.ugent.be:/home/mahdi/autoScripts/results/logFiles/deBruijn_Log_31.txt real/logFiles/deBruijn_Log_31.txt
 scp mahdi@halo.intec.ugent.be:/home/mahdi/autoScripts/results/logFiles/Gainlog.txt real/logFiles/Gainlog.txt
 scp mahdi@halo.intec.ugent.be:/home/mahdi/autoScripts/results/logFiles/infoLog.txt real/logFiles/infoLog.txt
 scp mahdi@halo.intec.ugent.be:/home/mahdi/autoScripts/results/tables/spadesNG50.pdf real/plots/spades.nga50.pdf
 #scp mahdi@halo.intec.ugent.be:/home/mahdi/autoScripts/results/logFiles/deBruijn_Log_0_21.txt real/logFiles/deBruijn_Log_0_21.txt
 
 sed -i -e 's/initial/Uncorrected/g' artificial/logFiles/*
 sed -i -e 's/initial/Uncorrected/g' real/logFiles/*
 sed -i -e 's/initial/Uncorrected/g' real/quast_assembly/*
 sed -i -e 's/initial/Uncorrected/g' /home/mahdi/haloServerTables/real/quastPlot/spades/D*/coordNGAx.json
 
python extractNGA50.py 
echo "extract Gain Mapped Tables for artificial data" 
python extractGainMappedTables.py artificial/logFiles/Gainlog.txt artificial/tables/gain
echo "extract Performance Tables (memory and run time) for artificial data"
python extractPerformanceTables.py artificial/logFiles/infoLog.txt artificial/tables/infoLog.tex
echo "extract Gain Mapped Tables for real data" 
python extractGainMappedTables.py real/logFiles/Gainlog.txt real/tables/gain
echo "extract BWA Mismatch Table real data"
python extractBWAMismatchTable.py real/logFiles/BWAlogTest.txt real/tables/0_.tex real/tables/m10_.tex
echo "extract Performance Tables (memory and run time) for real data"
python extractPerformanceTables.py real/logFiles/infoLog.txt real/tables/
echo "extract deBruijn graph stat Tables  for real data"
#python extractDeBruijn_info.py real/logFiles/deBruijn_Log_21.txt real/tables/deBruijn_log_21.tex
echo "extract deBruijn graph stat Tables  for real data"
#python extractDeBruijn_info.py real/logFiles/deBruijn_Log_31.txt real/tables/deBruijn_log_31.tex
#python extractDeBruijn_info.py real/logFiles/deBruijn_Log_0_21.txt real/tables/deBruijn_log_0_21.tex
echo "extract Performance Tables with asseembly (memory and run time) for real data"
python extractPerformanceAssmTables.py real/logFiles/asmInfoLog.txt real/tables/asmInfoLog.tex

python extractDeBruijn_info.py real/logFiles/deBruijn_Log_new_21.txt real/tables/deBruijn_Log_new_21.tex
python extractAllData.py real/quast_assembly/velvet.tex real/quast_assembly/NGA50_velvet.tex
python extractAllData.py real/quast_assembly/spades.tex real/quast_assembly/NGA50_spades.tex
python extractAllData.py real/quast_assembly/discovar.tex real/quast_assembly/NGA50_discovar.tex
python extractAllData.py real/quast_assembly/minia.tex real/quast_assembly/NGA50_minia.tex



#./real/plots/makeRunTimePlots.sh real/plots/runTime/discovar/
#./real/plots/makeRunTimePlots.sh real/plots/runTime/spades/
#./real/plots/makeMemoryPlots.sh real/plots/memory/spades/
#./real/plots/makeMemoryPlots.sh real/plots/memory/discovar/
#cd ./real/plots/
#gnuplot runtTimeDiscoverMulti.plot
#gnuplot runtTimeSpadesMulti.plot
 
