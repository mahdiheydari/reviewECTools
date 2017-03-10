
#methods=(ace racer karect musket bless blue fiona lighter sga bayesHammer trowel bfc)
#for method in ${methods[@]}
#do  

    
     method=$1
    
   if [ $2 -eq "1" ];
   then
       analisesDir=$method"/reads/1/"
       rm $analisesDir/mapped.fastq
       rm $analisesDir/mappedCorrected.fastq 
       python ../extractUniqueReads.py $analisesDir/41kmer_NODE_1_length_482029_cov_17.7599_ID_1072487 $analisesDir/mapped_ori.fastq $analisesDir/mappedCorrected_ori.fastq ../reads.fastq ../$method/$method"Out/checked."$method"Corrected.fastq" $analisesDir/mapped.fastq $analisesDir/mappedCorrected.fastq
       mkdir $analisesDir/reference
       cat ../initial/asm_spades_initial/contigs.fasta | sed -n '/>NODE_1_/,/>NODE_2_/p' |head -n -1 >$analisesDir/reference/1_contig.fasta
       bwa index $analisesDir/reference/1_contig.fasta
       bwa mem -M -t 4 -p $analisesDir/reference/1_contig.fasta $analisesDir/mapped.fastq | samtools view  -Sb - | samtools sort - $analisesDir/sorted && samtools index $analisesDir/sorted.bam
       samtools view $analisesDir"/sorted.bam" > $analisesDir"/sorted.sam"
       bwa mem -M -t 4 -p $analisesDir/reference/1_contig.fasta $analisesDir/mappedCorrected.fastq | samtools view  -Sb - | samtools sort - $analisesDir/sortedCorr && samtools index $analisesDir/sortedCorr.bam
       samtools view $analisesDir"/sortedCorr.bam" > $analisesDir"/sortedCorr.sam"
   fi
   if [ $2 -eq "2" ];
   then
    	echo "in the second"
        analisesDir=$method"/reads/2/"
    	mkdir $analisesDir
    	rm $analisesDir/mapped.fastq
    	rm $analisesDir/mappedCorrected.fastq
    	cat ../initial/asm_spades_initial/contigs.fasta | sed -n '/>NODE_2_/,/>NODE_3_/p' |head -n -1 >$analisesDir/reference/2_contig.fasta
    	echo "extract reads from data"
        python ../extractUniqueReads.py $analisesDir/41kmer_NODE_2_length_405178_cov_15.7823_ID_1072511 $analisesDir/mapped_ori.fastq $analisesDir/mappedCorrected_ori.fastq ../reads.fastq ../$method/$method"Out/checked."$method"Corrected.fastq" $analisesDir/mapped.fastq $analisesDir/mappedCorrected.fastq
    	mkdir $analisesDir/reference
    	bwa index $analisesDir/reference/2_contig.fasta
    	bwa mem -M -t 4 -p $analisesDir/reference/2_contig.fasta $analisesDir/mapped.fastq | samtools view  -Sb - | samtools sort - $analisesDir/sorted && samtools index $analisesDir/sorted.bam
    	samtools view $analisesDir"/sorted.bam" > $analisesDir"/sorted.sam"
    	bwa mem -M -t 4 -p $analisesDir/reference/2_contig.fasta $analisesDir/mappedCorrected.fastq | samtools view  -Sb - | samtools sort - $analisesDir/sortedCorr && samtools index $analisesDir/sortedCorr.bam
    	samtools view $analisesDir"/sortedCorr.bam" > $analisesDir"/sortedCorr.sam"
    fi
    if [ $2 -eq "3" ];
    then
    	analisesDir=$method"/reads/3/"
    	echo $analisesDir
    	mkdir $analisesDir
    	rm $analisesDir/mapped.fastq
    	rm $analisesDir/mappedCorrected.fastq
    	cat ../initial/asm_spades_initial/contigs.fasta | sed -n '/>NODE_3_/,/>NODE_4_/p' |head -n -1 >$analisesDir"reference/3_contig.fasta"
    	python ../extractUniqueReads.py $analisesDir"41kmer_NODE_3_length_378768_cov_17.4572_ID_1072515" $analisesDir"mapped_ori.fastq" $analisesDir"mappedCorrected_ori.fastq" ../reads.fastq ../$method/$method"Out/checked."$method"Corrected.fastq" $analisesDir"mapped.fastq" $analisesDir"mappedCorrected.fastq"
    	mkdir $analisesDir/reference
    	bwa index $analisesDir/reference/3_contig.fasta
    	bwa mem -M -t 4 -p $analisesDir/reference/3_contig.fasta $analisesDir/mapped.fastq | samtools view  -Sb - | samtools sort - $analisesDir/sorted && samtools index $analisesDir/sorted.bam
    	samtools view $analisesDir"/sorted.bam" > $analisesDir"/sorted.sam"
    	bwa mem -M -t 4 -p $analisesDir/reference/3_contig.fasta $analisesDir/mappedCorrected.fastq | samtools view  -Sb - | samtools sort - $analisesDir/sortedCorr && samtools index $analisesDir/sortedCorr.bam
    	samtools view $analisesDir"/sortedCorr.bam" > $analisesDir"/sortedCorr.sam"
   fi

#done





