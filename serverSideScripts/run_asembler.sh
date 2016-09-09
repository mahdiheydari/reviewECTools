#!/bin/bash
#
#
# Script to run the appropriate assembly software according to the input argument
# It should first go to the Destination directory which fastq files exists there
####
#	$1:first argument: 	specific data set address
#       $2:second argument:      the error Correction tool used for preProcessing
#	$3:second argument:	the assembler program name
#
dataRootDir=/home/share/data/mahdi
binDir=/home/mahdi/bin
kmerSize=21
alocatedMemory=128
threadNum=32

dataSet=$1
errorCorrection=$2
assembler=$3
outputDir="asm_"$assembler"_"$errorCorrection
inputDir=$errorCorrection"Out"/"checked."$errorCorrection"Corrected.fastq"

konsule_output=terminal/$outputDir
konsule_output_err=terminal/$outputDir"_err"
#outputFile=$errorCorrection"Corrected.fastq"

cd $dataRootDir/$dataSet/$errorCorrection
mkdir $outputDir  
rm -r $outputDir/*

echo "output file for:\n Assembly algorithm by" $assembler "for" $errorCorrection "data start"> $konsule_output
echo "error  file for:\n Assembly algorithm by" $assembler "for" $errorCorrection "data start"> $konsule_output_err



if [ "${assembler}" == "velvet" ];
then
     /usr/bin/time -v $binDir/velvet-master/velveth $outputDir $kmerSize -fastq -shortPaired $inputDir > $konsule_output 2>$konsule_output_err
     /usr/bin/time -v $binDir/velvet-master/velvetg $outputDir -exp_cov auto -cov_cutoff auto >> $konsule_output 2>>$konsule_output_err
     rm $outputDir/Sequences
     rm $outputDir/LastGraph
     rm $outputDir/Graph2
     rm $outputDir/Roadmaps
     rm $outputDir/PreGraph
fi

if [ "${assembler}" == "idba" ];
then


       /usr/bin/time -v $binDir/idba-master/bin/fq2fa $inputDir $outputDir/$errorCorrectionCorrected.fa --paired > $konsule_output 2>$konsule_output_err
      /usr/bin/time -v $binDir/idba-master/bin/idba --no_correct -r $outputDir/$errorCorrectionCorrected.fa -o $outputDir --num_threads $threadNum>> $konsule_output 2>>$konsule_output_err
       
       rm $outputDir/kmer
fi

if [ "${assembler}" == "discovar" ];
then
     # /usr/bin/time -v DiscovarDeNovo READS=$inputDir OUT_DIR=$outputDir MAX_MEM_GB=$alocatedMemory MEMORY_CHECK=true NUM_THREADS=$threadNum >$konsule_output 2>$konsule_output_err
      /usr/bin/time -v DiscovarDeNovo READS=$inputDir OUT_DIR=$outputDir NUM_THREADS=$threadNum >$konsule_output 2>$konsule_output_err
      rm -rf $outputDir/data/
fi

if [ "${assembler}" == "minia" ];
then
      /usr/bin/time -v $binDir/minia-2.0.3-Linux/bin/minia -nb-cores $threadNum -in $inputDir -kmer-size $kmerSize -abundance-min 3 -out $outputDir/minia > $konsule_output 2>$konsule_output_err
fi

if [ "${assembler}" == "spades" ];
then
      /usr/bin/time -v python /home/mahdi/bin/SPAdes-3.7.1-Linux/bin/spades.py -t $threadNum --only-assembler --12 $inputDir -o $outputDir > $konsule_output 2>$konsule_output_err
      rm -rf $outputDir/split_input/*
      rm -rf $outputDir/K*
fi

