#!/bin/bash
#
#
# Script to run the appropriate assembly software according to the input argument
# It should first go to the Destination directory which fastq files exists there
####
#       $1:first argument:      specific data set address
#       $2:second argument:     the assembler program name
#
dataRootDir=/home/share/data/mahdi
binDir=/home/mahdi/bin
#methods=(initial ace bless blue karect lighter racer sga bfc bayesHammer)
methods=(initial ace bayesHammer bfc bless blue fiona karect lighter musket racer sga trowel)

dataSet=$1
assembler=$2


outputDir="quastReports/quast4_"$assembler


konsule_output=terminal/$assembler"_quast"
konsule_output_err=terminal/$assembler"_quast_err"

cd $dataRootDir/$dataSet
mkdir -p "quastReports"
mkdir -p $outputDir  
rm -r $outputDir/*
mkdir -p "terminal"

echo "output file for quast  start"> $konsule_output
echo "error  file for quast start"> $konsule_output_err

if [ "${assembler}" == "velvet" ];
then
contigFileName="contigs.fa"
fi

if [ "${assembler}" == "idba" ];
then
contigFileName="scaffold.fa"
fi

if [ "${assembler}" == "discovar" ];
then
contigFileName="a.final/a.lines.fasta"
fi

if [ "${assembler}" == "minia" ];
then
contigFileName="minia.contigs.fa"
fi

if [ "${assembler}" == "spades" ];
then
contigFileName="scaffolds.fasta"
fi

   
toolsText=""
labelText=""
for  m in ${methods[@]}
do
    toolsText+=$m"/"asm_$assembler"_"$m"/"$contigFileName" "
    labelText+=$m","
done
labelText=$(echo "${labelText%?}")"\""
quastCommand=$toolsText" -R genome.fasta -1 initial/asm_spades_initial/split_input/checked.initialCorrected_1.fastq -2 initial/asm_spades_initial/split_input/checked.initialCorrected_2.fastq -o "$outputDir" --plots-format ps --labels \""$labelText 

/usr/bin/time -v python $binDir/quast-4.3/quast.py --debug -j $quastCommand >> $konsule_output 2>>$konsule_output_err



