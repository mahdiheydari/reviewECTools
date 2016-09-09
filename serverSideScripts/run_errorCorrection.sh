 
#!/bin/bash
#
#
# Script to run the appropriate Error Correction software according to the input argument
# It should first go to the Destination directory which fastq files exists there
####
#       $1:first argument:      specific data set address
#       $2:second argument:     the error Correction tool used for preProcessing
#

dataRootDir=/home/share/data/mahdi
binDir=/home/mahdi/bin

kmerSize=31
kaerectKmerSize=9
karectMem=32
#threadNum=$(nproc --al)
threadNum=32
dataSet=$1
errorCorrection=$2
do_error_correction=$3
trimming="noTrimming" #other options , noTrimming, trimmomatic, SolexaQA


inputData=../checked.reads.fastq
mappedInputData=../mappedReads.fastq
outputDir=$errorCorrection"Out"

outputFile=$errorCorrection"Corrected.fastq"
output_mapped_Dir=$errorCorrection"OutMapped"
mappedOutFile=$errorCorrection"Corrected.mapped.fastq"
trimmingFolder=$trimming"_out"

konsule_output=terminal/$errorCorrection
konsule_output_err=terminal/$errorCorrection"_err"

konsule_output_mapped=terminal/$errorCorrection"_mapped"
konsule_output_mapped_err=terminal/$errorCorrection"_mapped_err"


konsule_output_brownie=terminal/$errorCorrection"_brownie_21"
konsule_output_brownie_err=terminal/$errorCorrection"_brownie_err_21"


konsule_output_brownie_new=terminal/$errorCorrection"_brownie_new_21"
konsule_output_brownie_new_err=terminal/$errorCorrection"_brownie_new_err_21"



mismatch_output=terminal/$errorCorrection"_BWA_mismatch"
mapGain_output=terminal/$errorCorrection"_mappedReads_gain"

mkdir -p $dataRootDir$dataSet/$errorCorrection
cd $dataRootDir$dataSet/$errorCorrection
rm -rf $dataRootDir$dataSet/$errorCorrection/*

mkdir -p terminal
mkdir -p alignment
mkdir -p brownieEvaluation

if [ $do_error_correction -eq "1" ];
then
  echo "do error correction"
  rm -rf $outputDir 
  mkdir -p $outputDir  
  rm -r $output_mapped_Dir
  mkdir -p $output_mapped_Dir

  echo "output file for:\n"   $errorCorrection "data start"> $konsule_output
  echo "error  file for:\n"   $errorCorrection "data start"> $konsule_output_err
  dt=$(date)
  echo $dt $HOSTNAME >$konsule_output
  echo $dt $HOSTNAME >$konsule_output_err

  echo $dt $HOSTNAME >$konsule_output_mapped
  echo $dt $HOSTNAME >$konsule_output_mapped_err

fi




FILESIZE=$(stat -c%s ../genome.fasta)


if [ "${errorCorrection}" == "initial" ]
then
    cp $inputData $outputDir/$outputFile    
    mkdir -p ../reference
    
    python $binDir/removeNonATGC.py ../genome.fasta ../reference/genome.fasta
    bwa index ../reference/genome.fasta
    bwa mem -M -t 16 ../reference/genome.fasta $inputData >alignment/$outputFile".sam" 
    python $binDir/extractCorrectReads2.py alignment/$outputFile".sam" ../genome.fasta ../mappedReads.fastq ../correctReads.fasta
                
fi


if [ "${errorCorrection}" == "brownie" ]&& [ $do_error_correction -eq "1" ];
then
     echo "do error correction"
     mkdir $trimmingFolder
     rm $trimmingFolder/*
     if [ "${trimming}" == "trimmomatic" ];
     then
     	python $binDir/split.py $inputData reads1.fastq reads2.fastq
     	java -jar $binDir/Trimmomatic-0.36/trimmomatic-0.36.jar PE reads1.fastq reads2.fastq s1_pe s1_se s2_pe s2_se LEADING:4 TRAILING:4 MINLEN:$kmerSize
     	$binDir/shuffleSequences_fastq.pl s1_pe s2_pe trimmed.fastq
     	rm s1_pe
     	rm s2_pe
     	rm s1_se
     	rm s2_se
     	rm reads1.fastq
     	rm reads2.fastq
     fi

     if [ "${trimming}" == "SolexaQA" ];
     then
       
       $binDir/Solexa/Linux_x64/SolexaQA++ dynamictrim $inputData -d $trimmingFolder/
       cp $trimmingFolder/*.trimmed trimmed.fastq
       rm -rf $trimmingFolder/

     fi

     if [ "${trimming}" == "noTrimming" ];
     then
       cp $inputData trimmed.fastq
     fi

     /usr/bin/time -v  $binDir/brownie-0.1/build/src/brownie graphCorrection -t $threadNum -p $outputDir -k $kmerSize -o $outputDir/$outputFile trimmed.fastq >>$konsule_output 2>>$konsule_output_err
     /usr/bin/time -v  $binDir/brownie-0.1/build/src/brownie -t $threadNum -p $outputDir -k $kmerSize -o $outputDir/$outputFile $inputData >>$konsule_output 2>>$konsule_output_err
     
     /usr/bin/time -v  $binDir/brownie-0.1/build/src/brownie -t $threadNum -p $output_mapped_Dir -k $kmerSize -o $output_mapped_Dir/$mappedOutFile $mappedInputData >> $konsule_output_mapped 2>>$konsule_output_mapped_err

     rm trimmed.fastq    
fi


if [ "${errorCorrection}" == "blue" ]&& [ $do_error_correction -eq "1" ];
then
      KmerDef=25
     /usr/bin/time -v  mono $binDir/Blue/Tessel.exe -k $KmerDef -g $FILESIZE  -t $threadNum $outputDir/Cspor $inputData >>$konsule_output 2>>$konsule_output_err
     /usr/bin/time -v  mono $binDir/Blue/Blue.exe -m 10 -t $threadNum -o $outputDir $outputDir/Cspor_$KmerDef.cbt $inputData >> $konsule_output 2>>$konsule_output_err
      mv $outputDir/checked.reads_corrected_10.fastq $outputDir/$outputFile    


     cd $output_mapped_Dir
     /usr/bin/time -v mono $binDir/Blue/Tessel.exe -k $KmerDef -g $FILESIZE  -t 4 Cspor "../"$mappedInputData >>"../"$konsule_output_mapped 2>>"../"$konsule_output_mapped_err
     /usr/bin/time -v mono $binDir/Blue/Blue.exe -m 10 -t 1 -o . Cspor_$KmerDef.cbt "../"$mappedInputData >>"../"$konsule_output_mapped 2>>"../"$konsule_output_mapped_err
     mv mappedReads_corrected_10.fastq $mappedOutFile
     cd ..
     

fi


if [ "${errorCorrection}" == "karect" ]&& [ $do_error_correction -eq "1" ];
then
     

 /usr/bin/time -v  $binDir/karect/karect -correct -inputfile=$inputData -matchtype=hamming -celltype=diploid -resultdir=$outputDir -kmer=$kaerectKmerSize -threads=$threadNum >>$konsule_output 2>>$konsule_output_err
 mv $outputDir/karect_checked.reads.fastq $outputDir/$outputFile


/usr/bin/time -v  $binDir/karect/karect -correct -inputfile=$mappedInputData -matchtype=hamming -celltype=diploid -resultdir=$output_mapped_Dir -kmer=$kaerectKmerSize -threads=$threadNum >> $konsule_output_mapped 2>>$konsule_output_mapped_err
 mv $output_mapped_Dir/karect_mappedReads.fastq $output_mapped_Dir/$mappedOutFile


 rm res_graph_a.txt
 rm res_graph_b.txt
 rm temp_res_checked.reads.fastq
 rm temp_res_mappedReads.fastq
 rm input_file.txt

fi


if [ "${errorCorrection}" == "racer" ]&& [ $do_error_correction -eq "1" ];
then
       /usr/bin/time -v $binDir/Racer/racer.exe $inputData $outputDir/$outputFile $FILESIZE >> $konsule_output 2>>$konsule_output_err

       /usr/bin/time -v $binDir/Racer/racer.exe $mappedInputData $output_mapped_Dir/$mappedOutFile $FILESIZE >> $konsule_output_mapped 2>>$konsule_output_mapped_err

fi


if [ "${errorCorrection}" == "bless" ]&& [ $do_error_correction -eq "1" ];
then
       /usr/bin/time -v $binDir/bless2/bless -read $inputData -prefix $outputDir/bless -kmerlength $kmerSize -smpthread $threadNum >> $konsule_output 2>>$konsule_output_err
       mv $outputDir/bless.corrected.fastq $outputDir/$outputFile
      
       /usr/bin/time -v $binDir/bless2/bless -read $mappedInputData -prefix $output_mapped_Dir/blessMapped -kmerlength $kmerSize -smpthread 1  >> $konsule_output_mapped 2>>$konsule_output_mapped_err
       mv $output_mapped_Dir/blessMapped.corrected.fastq $output_mapped_Dir/$mappedOutFile
      
fi





if [ "${errorCorrection}" == "ace" ]&& [ $do_error_correction -eq "1" ];
then
       /usr/bin/time -v $binDir/ACE/ace $FILESIZE $inputData $outputDir/$outputFile >> $konsule_output 2>>$konsule_output_err
       /usr/bin/time -v $binDir/ACE/ace $FILESIZE $mappedInputData  $output_mapped_Dir/$mappedOutFile >> $konsule_output_mapped 2>>$konsule_output_mapped_err

fi

if [ "${errorCorrection}" == "bfc" ]&& [ $do_error_correction -eq "1" ];
then

   /usr/bin/time -v $binDir/bfc/bfc -s $FILESIZE -k $kmerSize -t $threadNum $inputData >> $outputDir/$outputFile  2>>$konsule_output_err
   /usr/bin/time -v $binDir/bfc/bfc -s $FILESIZE -k $kmerSize -t $threadNum $mappedInputData >> $output_mapped_Dir/$mappedOutFile  2>>$konsule_output_mapped_err

fi



if [ "${errorCorrection}" == "sga" ]&& [ $do_error_correction -eq "1" ];
then

     /usr/bin/time -v $binDir/sga/src/SGA/sga preprocess --permute-ambiguous  --no-primer-check -o $outputDir/reads.fastq -p=2 -m 11 $inputData  >> $konsule_output 2>>$konsule_output_err
     /usr/bin/time -v $binDir/sga/src/SGA/sga index -a ropebwt -t $threadNum --no-reverse $outputDir/reads.fastq  >> $konsule_output 2>>$konsule_output_err
     /usr/bin/time -v $binDir/sga/src/SGA/sga correct --learn -t $threadNum -o $outputDir/$outputFile $outputDir/reads.fastq >> $konsule_output 2>>$konsule_output_err
     
     rm mreads.bwt
     rm mreads.sai
     rm reads.bwt
     rm reads.sai
     rm $outputDir/reads.fastq

     /usr/bin/time -v $binDir/sga/src/SGA/sga preprocess --permute-ambiguous  --no-primer-check -o $output_mapped_Dir/mreads.fastq -p=2 -m 11 $mappedInputData>> $konsule_output_mapped 2>>$konsule_output_mapped_err
     /usr/bin/time -v $binDir/sga/src/SGA/sga index -a ropebwt -t $threadNum --no-reverse $output_mapped_Dir//mreads.fastq  >> $konsule_output_mapped 2>>$konsule_output_mapped_err
     /usr/bin/time -v $binDir/sga/src/SGA/sga correct --learn -t $threadNum -o $output_mapped_Dir/$mappedOutFile $output_mapped_Dir/mreads.fastq >> $konsule_output_mapped 2>>$konsule_output_mapped_err

     rm mreads.bwt
     rm mreads.sai
     rm reads.bwt
     rm reads.sai
     rm $output_mapped_Dir/mreads.fastq 

fi




if [ "${errorCorrection}" == "fiona" ]&& [ $do_error_correction -eq "1" ];
then

       /usr/bin/time -v $binDir/fiona-0.2.5-Linux-x86_64/bin/fiona  -nt $threadNum -g $FILESIZE $inputData $outputDir/$outputFile >> $konsule_output 2>>$konsule_output_err
    
       /usr/bin/time -v $binDir/fiona-0.2.5-Linux-x86_64/bin/fiona  -nt $threadNum -g $FILESIZE $mappedInputData $output_mapped_Dir/$mappedOutFile >> $konsule_output_mapped 2>>$konsule_output_mapped_err

fi




if [ "${errorCorrection}" == "lighter" ]&& [ $do_error_correction -eq "1" ];
then  
       KmerDef=17
        /usr/bin/time -v $binDir/Lighter/lighter -t $threadNum -K $KmerDef $FILESIZE -r $inputData -od $outputDir >> $konsule_output 2>>$konsule_output_err
        mv $outputDir/checked.reads.cor.fq $outputDir/$outputFile
        /usr/bin/time -v $binDir/Lighter/lighter -t $threadNum -K $KmerDef $FILESIZE -r $mappedInputData -od $output_mapped_Dir  >> $konsule_output_mapped 2>>$konsule_output_mapped_err
        mv $output_mapped_Dir/mappedReads.cor.fq $output_mapped_Dir/$mappedOutFile
fi  


if [ "${errorCorrection}" == "musket" ]&& [ $do_error_correction -eq "1" ];
then
       
          /usr/bin/time -v   $binDir/musket-1.1/musket -inorder -p $threadNum $inputData -o $outputDir/$outputFile  >> $konsule_output 2>>$konsule_output_err
          /usr/bin/time -v   $binDir/musket-1.1/musket -inorder -p $threadNum $mappedInputData -o $output_mapped_Dir/$mappedOutFile  >> $konsule_output_mapped 2>>$konsule_output_mapped_err
fi  



if [ "${errorCorrection}" == "coral" ]&& [ $do_error_correction -eq "1" ];
then
        KmerDef=21

        /usr/bin/time -v $binDir/coral-1.4.1/coral -p $threadNum -k $KmerDef -fq $inputData -o $outputDir/$outputFile >> $konsule_output 2>>$konsule_output_err
#       /usr/bin/time -v $binDir/coral-1.4.1/coral -p $threadNum -k $KmerDef -fq $mappedInputData -o $output_mapped_Dir/$mappedOutFile  > $konsule_output_mapped 2>$konsule_output_mapped_err

fi

if [ "${errorCorrection}" == "bayesHammer" ]&& [ $do_error_correction -eq "1" ];
then

   /usr/bin/time -v python $binDir/SPAdes-3.7.1-Linux/bin/spades.py  --careful --12 $inputData -o $outputDir --only-error-correction --disable-gzip-output >> $konsule_output 2>>$konsule_output_err
   $binDir/shuffleSequences_fastq.pl $outputDir/corrected/checked.reads_1.00.0_0.cor.fastq $outputDir/corrected/checked.reads_2.00.0_0.cor.fastq $outputDir/$outputFile
   
   rm -rf $outputDir/corrected
   rm -rf $outputDir/split_input
   
   
   /usr/bin/time -v python $binDir/SPAdes-3.7.1-Linux/bin/spades.py --careful --12 $mappedInputData -o $output_mapped_Dir --only-error-correction --disable-gzip-output >> $konsule_output_mapped 2>>$konsule_output_mapped_err
   $binDir/shuffleSequences_fastq.pl $output_mapped_Dir/corrected/mappedReads_1.00.0_0.cor.fastq $output_mapped_Dir/corrected/mappedReads_2.00.0_0.cor.fastq $output_mapped_Dir/$mappedOutFile
   
   rm -rf $output_mapped_Dir/corrected
   rm -rf $output_mapped_Dir/split_input
		
fi



if [ "${errorCorrection}" == "trowel" ]&& [ $do_error_correction -eq "1" ];
then
     echo ../$inputData> $outputDir/trowelInput
    /usr/bin/time -v $binDir/trowel.0.2.0.4.linux.64 -k $kmerSize -t $threadNum -f $outputDir/trowelInput >> $konsule_output 2>>$konsule_output_err
    mv $inputData.out $outputDir/$outputFile
     echo ../$mappedInputData> $output_mapped_Dir/trowelInput
    /usr/bin/time -v $binDir/trowel.0.2.0.4.linux.64 -k $kmerSize -t $threadNum -f $output_mapped_Dir/trowelInput >> $konsule_output_mapped 2>> $konsule_output_mapped_err
    mv $mappedInputData.out $output_mapped_Dir/$mappedOutFile
fi



  
if  [ $do_error_correction -eq "1" ];
then
  python  $binDir/checkFastq.py $outputDir/$outputFile $outputDir/"checked."$outputFile
fi



#evaluation part



   $binDir/comparison/build/compare2.exe $mappedInputData ../correctReads.fasta $output_mapped_Dir/$mappedOutFile >$mapGain_output 2>$mapGain_output"_err"

   mkdir -p brownieEvaluation/
   #rm brownieEvaluation/*
    cp ../genome.fasta genome.fasta
   /usr/bin/time -v  $binDir/brownie_debug/Debug/src/brownie graphCorrection -t 64 -p brownieEvaluation -k 21 $outputDir/"checked."$outputFile > $konsule_output_brownie 2>$konsule_output_brownie_err   

  cp ../alignedContigs.fasta genome.fasta
   /usr/bin/time -v  $binDir/brownie_debug/Debug/src/brownie graphCorrection -t 64 -p brownieEvaluation -k 21 $outputDir/"checked."$outputFile > $konsule_output_brownie_new 2>$konsule_output_brownie_new_err



   bwa mem -M -t $threadNum -p ../reference/genome.fasta $outputDir/$outputFile >alignment/$outputFile".sam"
   python $binDir/countMismatch.py alignment/$outputFile".sam">$mismatch_output
  

rm $outputDir/$outputFile
rm $output_mapped_Dir/$mappedOutFile
rm alignment/$outputFile".sam"
rm genome.fasta

